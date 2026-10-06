#!/usr/bin/env python3
"""Validate the portable structure of public and private skill bundles.

This intentionally recognizes only the simple scalar YAML emitted for skill
headers. Package tooling performs full YAML parsing separately.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = ("name", "description", "license")
REQUIRED_METADATA_FIELDS = ("author", "version", "domain", "scope", "output-format")
ALLOWED_ROOT_MARKDOWN = {"README.md", "CHANGELOG.md"}
MARKDOWN_LINK = re.compile(r"\[[^]]*\]\(([^)]+)\)")
SIMPLE_FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):(?:[ \t]*(.*))?$")


def discover_skill_dirs(root: Path) -> list[Path]:
    """Find public ``root/skill`` and private ``root/category/skill`` bundles."""
    skills = set()
    if not root.is_dir():
        return []
    for child in root.iterdir():
        if not child.is_dir():
            continue
        if (child / "SKILL.md").is_file():
            skills.add(child)
        for grandchild in child.iterdir():
            if grandchild.is_dir() and (grandchild / "SKILL.md").is_file():
                skills.add(grandchild)
    return sorted(skills)


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = re.search(r"^---[ \t]*$", text[4:], re.MULTILINE)
    if not end:
        return None, text
    header_end = 4 + end.start()
    body_start = 4 + end.end()
    if body_start < len(text) and text[body_start] == "\n":
        body_start += 1
    return text[4:header_end], text[body_start:]


def is_nonempty_string(value: str | None) -> bool:
    """Accept YAML's ordinary or quoted scalar strings, not collections/types."""
    if value is None:
        return False
    value = value.strip()
    if not value or value[0] in "[{|>&*!":
        return False
    if value[0] in "\"'":
        return len(value) >= 2 and value[-1] == value[0] and bool(value[1:-1])
    if value.lower() in {"null", "~", "true", "false", "yes", "no", "on", "off"}:
        return False
    return not re.fullmatch(r"[-+]?\d+(?:\.\d+)?", value)


def parse_header(header: str) -> tuple[dict[str, str | None], dict[str, str | None]]:
    """Read the narrow mapping shape used by skill frontmatter."""
    fields: dict[str, str | None] = {}
    metadata: dict[str, str | None] = {}
    in_metadata = False
    for line in header.splitlines():
        if line == "metadata:":
            in_metadata = True
            continue
        if line and not line.startswith((" ", "\t")):
            in_metadata = False
            match = SIMPLE_FIELD.match(line)
            if match:
                fields[match.group(1)] = match.group(2)
            continue
        if in_metadata:
            match = re.match(r"^  ([A-Za-z][A-Za-z0-9-]*):(?:[ \t]*(.*))?$", line)
            if match:
                metadata[match.group(1)] = match.group(2)
    return fields, metadata


def is_generic_example_link(target: str) -> bool:
    normalized = target.lower().lstrip("./")
    return (
        normalized.startswith(("path/to/", "your-", "<", "{{", "$"))
    )


def local_markdown_links(body: str) -> list[str]:
    links = []
    in_fence = False
    for line in body.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in MARKDOWN_LINK.finditer(line):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            target = target.split(None, 1)[0].split("#", 1)[0]
            if not target or target.startswith(("#", "/", "http://", "https://", "mailto:")):
                continue
            if target.lower().endswith(".md") and not is_generic_example_link(target):
                links.append(target)
    return links


def validate_skill(skill: Path) -> list[str]:
    errors = []
    source = skill / "SKILL.md"
    if not source.is_file():
        return ["missing SKILL.md"]
    if not (skill / "agents" / "openai.yaml").is_file():
        errors.append("missing agents/openai.yaml")
    text = source.read_text(encoding="utf-8")
    header, body = split_frontmatter(text)
    if header is None:
        return ["missing frontmatter"]
    fields, metadata = parse_header(header)
    for field in REQUIRED_FIELDS:
        if not is_nonempty_string(fields.get(field)):
            errors.append(f"{field} must be a nonempty string")
    if is_nonempty_string(fields.get("name")):
        name = fields["name"].strip().strip("\"'")
        if name != skill.name:
            errors.append(f"name {name!r} does not match directory {skill.name!r}")
    for field in REQUIRED_METADATA_FIELDS:
        if not is_nonempty_string(metadata.get(field)):
            errors.append(f"metadata.{field} must be a nonempty string")
    for target in local_markdown_links(body):
        if not (skill / target).is_file():
            errors.append(f"missing linked Markdown file {target}")
    for sibling in skill.glob("*.md"):
        if sibling.name == "SKILL.md" or sibling.name in ALLOWED_ROOT_MARKDOWN:
            continue
        if sibling.name.upper().startswith("LICENSE"):
            continue
        errors.append(f"loose supporting Markdown file {sibling.name}")
    return errors


def validate_root(root: Path) -> tuple[int, list[str]]:
    skills = discover_skill_dirs(root)
    messages = []
    failed = 0
    for skill in skills:
        errors = validate_skill(skill)
        label = str(skill)
        if errors:
            failed += 1
            messages.extend(f"FAIL {label}: {error}" for error in errors)
        else:
            messages.append(f"OK {label}")
    return failed, messages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path, help="skill root to validate")
    args = parser.parse_args(argv)
    failed = 0
    for root in args.roots:
        count, messages = validate_root(root)
        failed += count
        for message in messages:
            print(message)
        if not discover_skill_dirs(root):
            print(f"FAIL {root}: no skill bundles found")
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
