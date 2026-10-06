---
name: code-review
description: "Reviews diffs for correctness, security, performance, test coverage, repository standards, and ticket or spec compliance. Use before committing or merging a ticket, when reviewing a branch or PR, or when asked to review since a base ref."
license: MIT
metadata:
  author: ContractorKeith
  version: "1.2.0"
  domain: quality
  scope: review
  output-format: report
  related-skills: codebase-design, implement, tdd, debug, ship
---

# Code Review

Review the same diff two ways and keep the answers separate.

- **Standards:** Is the change technically sound, and does it follow this
  repository’s documented rules?
- **Spec:** Does the change deliver the originating ticket or specification —
  no less and no more?

One axis cannot excuse a failure on the other. Clean code can build the wrong
thing; a correct feature can still ignore the project’s rules.

## Reference guide

| Reference | Read when |
|---|---|
| [REVIEW-CHECKLIST.md](REVIEW-CHECKLIST.md) | Starting Standards; select checks relevant to the change |
| [FINDING-EXAMPLES.md](FINDING-EXAMPLES.md) | Calibrating severity, confidence, and evidence |
| [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md) | Writing the report, including clean or incomplete reviews |

## 1. Pin the comparison

Require a fixed point: a commit, branch, tag, merge-base, or the ticket’s
starting commit. Verify it first with `git rev-parse --verify <base>^{commit}`.

For committed branch work, capture these once:

```sh
git diff <base>...HEAD
git log <base>..HEAD --oneline
```

The three-dot diff compares `HEAD` with the merge-base, which is the default
review artifact. Pin the resolved base and head commits so reviewers see the
same artifact. Check that the diff is non-empty and run
`git diff --check <base>...HEAD` before delegation.

For `/implement` work that has not been committed yet, review the current
worktree against the same fixed point with `git diff <base>` instead. Include
staged changes and list untracked files explicitly; do not silently review an
empty `...HEAD` diff and miss the ticket work.
Run `git diff --check <base>` in this mode and read relevant untracked files;
listing their names alone is not a review. Capture the worktree artifact before
delegation, and record exclusions of unrelated files.

If the caller supplied no base, ask for one rather than guessing. If there is
no change, report that plainly and stop.

## 2. Gather the two contracts

Find the originating requirement in this order:

1. the ticket passed by the caller or referenced by the branch and commits;
2. a GitHub Issue via `gh issue view <number>` when a GitHub remote and
   authenticated `gh` are available;
3. a matching spec under `docs/`, `specs/`, or `.scratch/`;
4. a local markdown ticket under `.scratch/<effort>/issues/` when GitHub is
   unavailable.

If no spec or ticket can be found, say **Spec: no source available**. Do not
invent requirements.

Read the repository’s standards sources before reviewing: root and applicable
subdirectory `AGENTS.md` or `CLAUDE.md`, `CONTRIBUTING.md`, coding standards,
test guidance, and relevant `CONTEXT.md` or ADRs. Repository rules outrank the
smell baseline below.
Summarize the requested behavior in one sentence. Repository design preferences
cannot excuse demonstrated bugs or security flaws.

## 3. Review independently

When the host CLI supports sub-agents, run the Standards and Spec reviews in
parallel with the same pinned diff. Give each reviewer only its contract and
the diff context it needs. When parallel agents are unavailable, do two
separate sequential passes; finish and record one axis before starting the
other.

### Standards pass

When the diff changes module structure, interfaces, or dependency placement,
read `/codebase-design` and use it to assess caller burden, ownership of rules,
dependency seams, and testability. Read its `DEEPENING.md` for consolidation
changes. Use `DESIGN-IT-TWICE.md` only if an unresolved interface choice warrants
a separate design follow-up; review does not start a redesign exercise.

Treat these principles as judgment guidance, not new acceptance criteria.
Repository rules and ADRs govern architectural choices. Explain concrete impact
before flagging a shallow module or seam; do not demand adapters or abstractions
for hypothetical future uses. Keep design findings in Standards, and reserve
Spec findings for actual ticket requirements.

Read REVIEW-CHECKLIST.md. Check every changed hunk and trace callers, data
flows, and tests far enough to establish behavior. Check correctness, security,
performance, and test quality even when repository guidance is silent. Run
focused checks when useful; distinguish inspected tests from executed ones.
Verify delegated findings before reporting them. Label each finding as:

- **documented standard** — cite the file and rule; or
- **technical defect** — demonstrate a concrete failure or risk; or
- **judgment call** — cite a relevant smell below and explain why it matters.

Use this smell baseline only where tooling does not already enforce the rule:

- **Mysterious name:** a name hides what the value or function means; give it
  an honest name or clarify the design.
- **Duplicated code:** two changed places carry the same logic shape; extract
  the shared behavior when doing so makes the code clearer.
- **Feature envy:** a method knows another object’s data better than its own;
  consider moving that behavior to the object it depends on.
- **Data clumps:** the same fields travel together repeatedly; consider one
  meaningful type or value object.
- **Primitive obsession:** a string or number stands in for a domain concept;
  give the concept a small type when its rules need protection.
- **Repeated switches:** the same conditional tree appears in several places;
  centralize it or use a behavior-bearing type.
- **Shotgun surgery:** one small behavior change needs scattered edits; bring
  the behavior’s moving parts closer together.
- **Divergent change:** one module changes for unrelated reasons; separate
  those responsibilities.
- **Speculative generality:** a hook, parameter, or abstraction serves no
  current requirement; remove it until a real need arrives.
- **Message chains:** a caller walks a long object path; hide the navigation
  behind a useful operation.
- **Middle men:** a type only passes every request onward; remove the layer
  unless it adds a real boundary.
- **Refused inheritance:** a subtype fights most of its parent contract;
  prefer composition or a better interface.

These are prompts for judgment, not automatic violations. If repository
guidance deliberately permits a pattern, its guidance wins.

### Spec pass

Compare the diff and tests directly with each acceptance criterion. Report:

- missing or partial requirements;
- behavior outside the requested scope; and
- requirements that look present but are implemented incorrectly.

Quote or cite the exact ticket/spec requirement for every finding. Do not call
an optional idea a missing requirement.

## 4. Report without blending the axes

Give findings with file and line, evidence, impact, and a practical next step.
Use FINDING-EXAMPLES.md and REPORT-TEMPLATE.md. Calibrate severity and confidence
independently. Report introduced defects or old defects made reachable by this
change; exclude unrelated pre-existing issues. Verify suspected problems against
surrounding code. Unresolved hypotheses belong in limitations, not blocking
findings. Never invent issues to fill the template or imply a clean review
proves absence of bugs.
Keep these headings distinct:

```md
## Standards

## Spec
```

State the finding count and worst issue within each axis. Do not combine or
rerank them into one score. If an axis is clean, say so; if its source was
missing, say that instead of pretending it passed.

When `/implement` requested the review, return the actionable findings to its
loop. It fixes the relevant issues, reruns proof, and reviews the changed diff
again before committing. This skill does not commit, push, or close tickets.
