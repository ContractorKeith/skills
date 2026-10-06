# Review checklist

Apply checks relevant to changed behavior. Follow execution paths, not just
changed lines. Record important gaps instead of guessing.

## Correctness and reliability

- Trace happy paths, empty inputs, boundaries, and failures.
- Check state transitions, ordering, retries, cancellation, and idempotency.
- Look for races, stale reads, partial writes, and missing cleanup.
- Check errors propagate usefully without hiding failures.
- Verify compatibility at callers, public APIs, persisted data, and migrations.
- Inspect library semantics before asserting a call behaves incorrectly.

## Security and data protection

- Trace untrusted input to queries, commands, paths, templates, and output.
- Check authentication and authorization separately, including ownership and
  tenant boundaries. A logged-in user may still lack access.
- Check secrets and sensitive data in logs, errors, and responses.
- Inspect injection, path traversal, unsafe deserialization, and unsafe output
  rendering where those operations occur.
- Explain the reachable attack path and consequence; inspect surrounding
  safeguards before claiming a vulnerability.

## Performance and resources

- Check queries or requests inside loops and unexpectedly repeated work.
- Check bounds on input size, pagination, concurrency, memory, and retries.
- Look for leaks and blocking operations on latency-sensitive paths.
- Establish a relevant workload before claiming a defect. Do not invent
  timings or suggest caching without a concrete need.

## Tests and proof

- Map requirements and risky paths to behavioral assertions.
- Check denied access, invalid input, failures, and boundaries.
- Look for tests that pass despite the defect, unrealistic mocks, and missing
  integration coverage at changed boundaries.
- Check regression tests fail for old behavior when practical.
- Run focused checks that resolve uncertainty; report commands and results.
  Say when tests were only inspected. Do not demand exhaustive tests for harmless
  edits or tests that simply mirror the implementation.

## Design and repository standards

Use the smell baseline in [SKILL.md](../SKILL.md) only when it explains a concrete cost.
Automated formatting belongs to tooling. Repository design preferences outrank
generic advice; a demonstrated technical defect still requires a finding.
Do not prescribe an abstraction solely because a pattern has a name.
