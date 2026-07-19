# ContractorKeith / skills

Engineering skills for agent CLIs — Claude Code, Codex, and anything else
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
                 /ask-kod  ←  "which skill do I use?"
                     │
   /kodmap ── too big for one session? map it first
                     │
   idea ──► /grill ──► small job ──────────► /implement ──► /ship
                     │                          ▲
                     └► /spec ──► /tickets ─────┘ (one ticket per
                                                    fresh context)
```

`/implement` drives `/tdd` one red-green slice at a time and closes with
`/code-review`. `/ship` is the landing gate — gates green, branches merged,
pushed, verified.

## Skills

### User-invoked (you type the slash command)

| Skill | What it does |
|---|---|
| `/ask-kod` | Routes you to the right skill or flow for your situation |
| `/grill` | Relentless interview to stress-test a plan; writes CONTEXT.md + ADRs as it goes |
| `/spec` | Turns a grilled idea into a written spec |
| `/tickets` | Splits a spec into tracer-bullet tickets with blocking edges (GitHub Issues via `gh`) |
| `/implement` | Builds one ticket: tdd slices, code review, commit, close |
| `/kodmap` | Maps a huge foggy effort as decision tickets, resolved until the way is clear |
| `/unslop` | Surveys the codebase for slop and architectural drift; produces cleanup candidates |
| `/handoff` | Compacts the session into a file so a fresh session can pick it up |
| `/ship` | End-of-work landing gate: gates, merges, push, verified git state |

### Model-invoked (the agent reaches for them)

| Skill | What it does |
|---|---|
| `/tdd` | Red-green-refactor discipline for building behavior test-first |
| `/code-review` | Two-axis review of a diff — Standards and Spec — since a fixed point |
| `/debug` | Diagnosis loop for hard bugs: tight feedback loop first, then hypotheses |
| `/merge-conflicts` | Resolves in-progress git merge/rebase conflicts |
| `/research` | Clarify-first parallel research (codebase, docs, web) before planning |
| `/codebase-design` | Deep-module vocabulary for designing a module's shape |
| `/prototype` | Throwaway code that answers one design question |

## Conventions

Structure, voice, frontmatter, and the cross-reference map live in
[CONVENTIONS.md](./CONVENTIONS.md). Every skill ships an `agents/openai.yaml`
so Codex gets proper display metadata alongside Claude Code's frontmatter.

## Credits

The flow structure and several skills are rewritten from
[Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT) — a
great collection worth studying in the original. `/research` is adapted from
a workflow by [Josh Pigford](https://x.com/Shpigford). All rewrites are MIT
as well.
