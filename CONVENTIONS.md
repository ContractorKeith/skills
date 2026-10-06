# Skill conventions

How every skill in this repo is structured. Follow this exactly when adding or
rewriting a skill.

## Layout

```
<skill-name>/
├── SKILL.md            # the skill itself
├── agents/
│   └── openai.yaml     # Codex-facing metadata
└── <REFERENCE>.md      # optional supporting files, SCREAMING-KEBAB names
```

## SKILL.md frontmatter

```yaml
---
name: <skill-name>            # matches the directory name
description: <one or two sentences, third person, trigger-rich — this is what
  the model reads to decide relevance. Say what it does AND when to use it.>
disable-model-invocation: true   # ONLY on user-invoked skills (slash-command style)
---
```

User-invoked skills (a human types `/name`): `grill`, `spec`,
`tickets`, `implement`, `unslop`, `handoff`, `ship`.
Model-invoked skills (the agent reaches for them mid-task): `tdd`,
`code-review`, `debug`, `merge-conflicts`, `research`, `codebase-design`,
`prototype`. Model-invoked skills omit `disable-model-invocation`.

## agents/openai.yaml

Codex reads this; Claude Code ignores it. Mirror the frontmatter:

```yaml
interface:
  display_name: "<Title Case Name>"
  short_description: "<one line>"
policy:
  allow_implicit_invocation: false   # false for user-invoked, true for model-invoked
```

## Voice and style

- Plain-spoken and direct. Written by a construction veteran who builds
  software: job-site clarity, no academic filler. An occasional construction
  analogy is welcome when it genuinely clarifies; never forced.
- Address the agent in second person ("Read the ticket. Do not start coding
  until…"). Skills are instructions to an agent, not essays.
- Short sections with strong headers. Rules as bullet lists. Every rule earns
  its place — cut anything an agent would ignore.
- Small-team / internal-tool context by default. Not enterprise SaaS.
- Cross-CLI: skills must work in Claude Code, Codex, and any agent CLI that
  reads SKILL.md. Never depend on a tool only one CLI has; when a step uses a
  CLI-specific tool (e.g. AskUserQuestion), name the fallback ("or ask in
  plain text, one question at a time").

## Cross-references

Skills reference each other by slash-name: `/grill`, `/spec`, `/tickets`,
`/implement`, `/tdd`, `/code-review`, `/debug`, `/unslop`,
`/merge-conflicts`, `/research`, `/codebase-design`, `/prototype`,
`/handoff`, `/ship`. Use only these names — no legacy names from
other skill collections.

## The main flow

Idea → `/grill` (sharpen it, docs trail) → small job: `/implement` directly;
big job: `/spec` → `/tickets` → `/implement` per ticket (fresh context each).
`/implement` drives `/tdd` and closes with `/code-review`. `/ship` is the
end-of-work landing gate.

## Issue tracker

Default is GitHub Issues via the `gh` CLI. If the repo has no GitHub remote
(or `gh` is unauthenticated), fall back to local markdown tickets under
`.scratch/<effort>/issues/`, one file per ticket, worked blockers-first.
Skills that touch tickets state this default inline — there is no separate
setup skill.

## Docs trail

`/grill` maintains the repo's domain docs: `CONTEXT.md` (glossary only) at the
root and `docs/adr/` for architecture decision records. Other skills read
these for vocabulary; only `/grill` (and the user) writes them.
