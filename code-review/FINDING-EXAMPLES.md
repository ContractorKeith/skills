# Finding examples and calibration

## Severity and confidence

Severity describes impact; confidence describes strength of evidence.

| Severity | Meaning |
|---|---|
| Critical | Reachable security compromise, severe data loss, or widespread outage; blocks landing |
| Major | Demonstrated wrong behavior, meaningful regression, or material maintenance cost; fix before landing |
| Minor | Limited impact with concrete benefit; normally nonblocking |

| Confidence | Evidence |
|---|---|
| High | Reproduced, or established by a complete code path and verified semantics |
| Medium | Supported by code with a specific remaining assumption stated explicitly |
| Low | Hypothesis needing evidence; ask a question or list a limitation |

Do not lower severity because evidence is weak. Investigate instead. A
blocking finding needs sufficient evidence to establish the failure.

## Ownership check missing

**Standards — technical defect — Critical — High confidence**

`src/invoices/download.ts:18`: the new handler looks up an invoice by the
request's ID and returns its file. Middleware verifies login, but neither the
query nor the handler compares ownership with the caller. Following the full
route confirms no intervening authorization check.

Another authenticated account can download the invoice by supplying its ID.
Restrict the lookup to permitted resources and add a test with a different
account. Authentication alone does not establish ownership.

Use this finding only after checking surrounding authorization. Absence of a
local check is not proof if middleware enforces ownership.

## Wrong sort direction

**Spec — Major — High confidence**

`src/jobs/list.ts:42`: issue #17 requires newest jobs first, but the query sorts
creation time ascending. Two differently dated jobs return oldest first.
Use descending order and assert the returned sequence.

If the requirement merely says "sort by date", ask which direction is intended
instead of inventing a requirement.

## Unsupported performance claim

Weak: "This file response probably blocks the event loop. Replace it."

Better: inspect the API's implementation or official documentation and call
path. Drop the claim if asynchronous streaming is already used. If semantics
cannot be established, record uncertainty instead of a blocking defect.

## Preference disguised as a finding

Weak: "Extract this small conditional into a strategy class."

Better: omit it unless a documented rule or concrete maintenance problem
justifies the change. A design smell is a prompt, not evidence.

## Reporting rules

- Cite a precise changed location, trigger, evidence, consequence, and remedy.
  Include a short example only when it clarifies the fix.
- Cite exact rules for documented standards and requirements for Spec findings.
- Separate actual defects from questions and optional suggestions.
- Combine duplicate root causes within an axis. If both axes identify one,
  cross-reference evidence rather than repeating it.
- Report no findings when none are supported; do not populate empty sections
  with invented defects or obligatory praise.
