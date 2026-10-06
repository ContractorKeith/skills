# Review report template

Scale length to the diff. Keep Standards and Spec separate and order findings
by severity within each. Do not invent a combined score or merge verdict.

```md
Reviewed: <base>...<head> | worktree against <base>
Intent: <one sentence describing requested behavior>
Scope: <included paths; relevant exclusions or untracked files>

## Standards

<N findings; worst severity, or "No supported findings in reviewed scope">

### <Severity> — <problem> — <High/Medium confidence>

- Location: <file:line>
- Basis: <documented standard + rule citation | technical defect | judgment call>
- Evidence: <code path, reproducer, or check; state assumptions>
- Impact: <trigger and consequence>
- Next step: <smallest useful fix and verification>

## Spec

<N findings; worst severity | no supported findings | no source available>
Source: <ticket/spec identifier, if available>

### <Severity> — <missing, wrong, or out-of-scope behavior> — <confidence>

- Requirement: <exact requirement and source>
- Location: <file:line>
- Evidence: <expected versus actual behavior>
- Impact: <consequence>
- Next step: <fix and verification; cross-reference Standards if shared>

## Verification and limitations

- Executed: <commands and results, or "No checks executed">
- Inspected: <tests and relevant surrounding code>
- Unresolved: <questions, unsupported hypotheses, inaccessible sources>
```

Omit empty unresolved lists. For a small clean diff, one sentence per axis and
a verification note suffice. A missing spec is not a Spec pass. Executed
checks are evidence, not proof every path is safe. Never imply tests ran or
security was exhaustively checked when it was only inferred.
