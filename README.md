# ContractorKeith / skills

14 engineering skills for agent CLIs — Claude Code, Codex, and anything else
that reads `SKILL.md`. Written by a construction veteran who builds software:
a complete idea-to-ship flow with job-site clarity and no ceremony.

## Install

```bash
npx skills@latest add ContractorKeith/skills
```

Or clone and symlink the skill folders you want into your CLI's skills
directory (`~/.claude/skills`, `~/.codex/skills`, …).

## The flow

```
   idea ──► /grill ──► small job ──────────► /implement ──► /ship
                     │                          ▲
                     └► /spec ──► /tickets ─────┘ (one ticket per
                                                    fresh context)
```

`/implement` drives `/tdd` one red-green slice at a time and closes with
`/code-review`. `/ship` is the landing gate — gates green, branches merged,
pushed, verified.

For architectural changes, `/implement` and `/code-review` load
`/codebase-design` to guide module structure, interfaces, dependencies, and
testability. Routine edits do not require a design exercise. For a reported
failure, `/debug` reproduces and isolates the cause, verifies the fix, then
hands the change to `/code-review`.

## Skills

### User-invoked (you type the slash command)

| Skill | What it does |
|---|---|
| [/grill](grill/SKILL.md) | Relentless interview to stress-test a plan; writes CONTEXT.md + ADRs as it goes |
| [/spec](spec/SKILL.md) | Turns a grilled idea into a written spec |
| [/tickets](tickets/SKILL.md) | Splits a spec into tracer-bullet tickets with blocking edges (GitHub Issues via `gh`) |
| [/implement](implement/SKILL.md) | Builds one ticket: design guidance when needed, TDD slices, review, commit, close |
| [/unslop](unslop/SKILL.md) | Surveys the codebase for slop and architectural drift; produces cleanup candidates |
| [/handoff](handoff/SKILL.md) | Compacts the session into a file so a fresh session can pick it up |
| [/ship](ship/SKILL.md) | End-of-work landing gate: gates, merges, push, verified git state |

### Model-invoked (the agent reaches for them)

| Skill | What it does |
|---|---|
| [/tdd](tdd/SKILL.md) | Red-green-refactor discipline for building behavior test-first |
| [/code-review](code-review/SKILL.md) | Separate Standards and Spec passes covering defects, security, performance, tests, and requirements |
| [/debug](debug/SKILL.md) | Reproduce a failure, prove its cause, verify a fix, then review the change |
| [/merge-conflicts](merge-conflicts/SKILL.md) | Resolves in-progress git merge/rebase conflicts |
| [/research](research/SKILL.md) | Clarify-first parallel research (codebase, docs, web) before planning |
| [/codebase-design](codebase-design/SKILL.md) | Shared module/interface design guidance with deepening and alternative-design references |
| [/prototype](prototype/SKILL.md) | Throwaway code that answers one design question |

## Repository layout

Each skill lives in its own folder at the repo root:

```text
<skill-name>/
├── SKILL.md             # Instructions, MIT license declaration, and metadata
├── LICENSE              # License notice included with the bundle
├── agents/openai.yaml   # Codex display and invocation metadata
├── references/          # Supporting guidance, where needed
└── scripts/             # Helpers for this skill, where needed
```

The top-level [`scripts/`](scripts/) directory contains repository validation
tools and their tests. It is maintenance tooling, not an installable skill;
it has no `SKILL.md`. Install the skill folders with their bundled resources.

## Conventions

Structure, voice, frontmatter, and the cross-reference map live in
[CONVENTIONS.md](CONVENTIONS.md). Every skill ships an `agents/openai.yaml`
so Codex gets proper display metadata alongside Claude Code's frontmatter.

## Validation

Run `python3 scripts/validate-skill-bundles.py .` to check required metadata,
reference links, and bundle layout. Run `python3 scripts/validate-skill-bundles.test.py`
for validator tests. These checks use the Python standard library; full YAML
schema validation remains a separate package check.

## Credits

The flow structure and several skills are rewritten from
[Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT) — a
great collection worth studying in the original. `/research` is adapted from
a workflow by [Josh Pigford](https://x.com/Shpigford). All rewrites are MIT
as well. See [LICENSE](LICENSE) for the repository's MIT terms; each skill
also includes its own copy of the license notice.
