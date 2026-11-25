---
name: qa-api
description: Author, execute, diagnose and maintain API or service-contract tests during QA. Use for request/response, persisted state, asynchronous completion and integration behavior.
---

# API execution

Use through `qa`; load `qa-workflow` and `.agent/rules/test-automation.md`.
Those own execution evidence and verdicts. This skill supplies API-specific work,
using the team's existing language, client, collection or runner.

## Prepare the contract and fixtures

1. Resolve the deployed specification, relevant requirements and actual client
   version. Record base URL, API/schema version, authentication mechanism and
   observable state boundary. A generated schema describes structure; domain
   requirements supply constraints and business outcomes it may omit.
2. Map operations to actors, inputs, transitions and observations: request →
   response → persisted/read-back state or asynchronous completion. Identify an
   independent expected value for each assertion. Verify which omissions, nulls,
   coercions, defaults, formats, limits and unknown fields the contract permits.
3. Allocate run-specific users, resources and idempotency keys. Prepare teardown
   that works after partial creation and records unresolved leftovers. Establish
   the authorized target identity before sending mutations. Read access alone
   does not establish a safe write target.

## Author a useful slice

Create executable tests before calling the plan covered. Use data-driven cases
for equivalence partitions and limits; separate scenarios when their state or
failure diagnosis differs.

| Risk | Test and observable assertion |
|---|---|
| Contract drift | Method/path/media type, required fields, types, enum/length/range boundaries and documented error shape; assert values and absence of forbidden fields as well as schema. |
| Invalid input | Missing versus null, below/at/above limit, malformed body and unsupported format; assert agreed rejection and unchanged business state. |
| Authorization | Own-object positive control and another fixture actor's object/action; use `qa-security` when access control is in scope. |
| Persistence | Create/update then read through the independent public observation path; verify exact fields, ownership, totals and applicable invariant. |
| Retry/idempotency | Same key and payload twice, conflicting payload under one key, and a fresh key; assert resource/side-effect count under the actual contract. Idempotent effect need not mean identical responses. |
| Async work | Capture operation identity; poll documented status to a terminal state within its agreed deadline, then assert output and business state. Test failure/cancellation only where specified. |
| Pagination/concurrency | Controlled dataset with boundaries and ties; prove no duplicate/missing records under the promised ordering/snapshot model. For a race, synchronize competing actions and check the final invariant. |

Choose only applicable rows. No declared async deadline means the observation
can be incomplete without proving a timeout defect. Do not turn eventual
consistency into an arbitrary immediate read assertion.

## Run and diagnose

Inspect the real test-discovery command and run a small positive control first.
Execute the selected suite with transport timeouts and bounded response capture;
preserve semantic HTTP errors for assertions instead of treating every non-2xx
as a client exception. Retain sanitized requests, responses, correlation IDs and
read-back evidence with the shared run identity.

On failure, compare the request actually sent with the contract. Distinguish
serialization/authentication/setup problems from response, state or completion
failures using a minimal request and correlated logs when available. A missing
log is an observation gap. If a server accepted a write before a transport error,
reconcile state before repeating it. Keep test corrections separate from product
corrections; changing an oracle needs requirement evidence.

## Maintain

Keep fixture creation and cleanup in the runner's lifecycle; assertions belong
at the public contract boundary. Update tests alongside versioned contract
changes, preserving valid older-client cases when compatibility is promised.
Turn a reproduced defect into its smallest stable regression and retain one real
integration path when other checks use doubles. Recheck actor isolation and
stale IDs when parallelizing a suite.

For the disposable local service or Python stdlib authoring, read
[the HTTP recipe](references/python-http.md). It is a reference exercise, not
a required team stack. General async/idempotency rationale: [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html),
sections 9.2.2 and 15.3.3.
