#!/usr/bin/env python3
"""Focused behavior tests for validate-skill-bundles.py."""

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate-skill-bundles.py")
SPEC = importlib.util.spec_from_file_location("validate_skill_bundles", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


def header(name="sample", metadata="", extra=""):
    return f"""---
name: {name}
description: A useful skill.
license: MIT
metadata:
  author: ContractorKeith
  version: 1.0.0
  domain: testing
  scope: validation
  output-format: report
{metadata}---
{extra}"""


class ValidateSkillBundlesTests(unittest.TestCase):
    def make_skill(self, root, relative="sample", content=None):
        skill = root / relative
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(content or header(skill.name), encoding="utf-8")
        (skill / "agents").mkdir()
        (skill / "agents" / "openai.yaml").write_text("interface: test\n", encoding="utf-8")
        return skill

    def test_missing_metadata_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            content = header().replace("  version: 1.0.0\n", "")
            skill = self.make_skill(Path(directory), content=content)
            errors = validator.validate_skill(skill)
            self.assertIn("metadata.version must be a nonempty string", errors)

    def test_required_scalar_must_be_a_string(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory), content=header(metadata="  author: [ContractorKeith]\n"))
            errors = validator.validate_skill(skill)
            self.assertIn("metadata.author must be a nonempty string", errors)

    def test_missing_local_markdown_link_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory), content=header(extra="See [details](references/details.md).\n"))
            self.assertIn("missing linked Markdown file references/details.md", validator.validate_skill(skill))

    def test_root_reference_file_link_is_not_treated_as_a_placeholder(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory), content=header(extra="See [reference](reference.md).\n"))
            self.assertIn("missing linked Markdown file reference.md", validator.validate_skill(skill))

    def test_fenced_markdown_link_example_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory), content=header(extra="```md\n[example](reference.md)\n```\n"))
            self.assertEqual([], validator.validate_skill(skill))

    def test_loose_supporting_markdown_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory))
            (skill / "DETAILS.md").write_text("support", encoding="utf-8")
            self.assertIn("loose supporting Markdown file DETAILS.md", validator.validate_skill(skill))

    def test_readme_is_allowed_at_skill_root(self):
        with tempfile.TemporaryDirectory() as directory:
            skill = self.make_skill(Path(directory))
            (skill / "README.md").write_text("package note", encoding="utf-8")
            self.assertEqual([], validator.validate_skill(skill))

    def test_discovers_public_and_private_layouts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            public = self.make_skill(root, "public-skill")
            private = self.make_skill(root, "category/private-skill")
            self.assertEqual(sorted([public, private]), validator.discover_skill_dirs(root))


if __name__ == "__main__":
    unittest.main()
