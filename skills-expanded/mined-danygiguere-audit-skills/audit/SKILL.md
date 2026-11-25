---
name: audit
description: Full security, correctness, and operability audit of code. Use when reviewing a diff, endpoint, or feature for vulnerabilities or bugs without a specific topic in mind — security review, audit, code review for safety, "check this for issues".
---

# Audit procedure

The audit target is whatever the user specified; if nothing was specified,
default to the current diff (uncommitted changes, or the branch's changes
against the default branch). If there is no diff either, ask what to audit
rather than picking a scope yourself.

1. **Identify** what the code under audit does. Trace the data flow: what
   inputs arrive, what is looked up, what is written, what is rendered or
   returned, what runs async. If the target is larger than a diff — a
   module, service, or whole repo — load `references/methodology/scope.md`
   first and follow its inventory, ranking, and budget procedure.
2. **Load** only the checklist files matching that behavior, from the map
   below.
3. **Check** each invariant in the loaded files against the code.
4. **Verify before reporting**: load `references/methodology/verify.md`
   and run every candidate through it — name the attacker and the victim,
   hunt for existing mitigations in the surrounding code (middleware, base
   classes, decorators, callers), and when auditing a diff, anchor each
   finding to the lines that introduce or enable it. A candidate survives
   only if you cannot refute it with cited evidence.
5. **Report** each finding with: severity (assigned per
   `references/methodology/severity.md`), `file:line`, the violated
   invariant, and a one-line fix direction. Say explicitly which checklists
   were applied and came back clean.
6. **Fix only on request**: never change code during an audit. When the
   user asks for remediation, check the finding's checklist: if it ends
   with a `## Remediation` section, load the playbook it names under
   `references/remediation/` and choose among its patterns; otherwise
   apply the fixed shape from the checklist's `## Example` section. Either
   way, make the smallest change that restores the invariant, match the
   surrounding code's conventions, and add a test demonstrating the fix.

Do not manufacture findings for topics that don't apply (e.g., CSRF on a
token-authenticated API, tenant isolation in a single-tenant app).

# What to load

Paths relative to this skill's directory. Load every row that matches; skip
the rest.

| The code…                                                                           | Read                                                                                                                                       |
|-------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Gates actions by role, permission, or ownership                                     | `references/access-data-security/authorization.md`                                                                                         |
| Handles login, logout, reset, tokens, sessions                                      | `references/access-data-security/authn-session.md`                                                                                         |
| Verifies JWTs, API keys, signed URLs, or webhook signatures                         | `references/access-data-security/token-validation.md`                                                                                      |
| Fetches/mutates a resource by an ID from the request                                | `references/access-data-security/idor.md` + `references/access-data-security/authorization.md`                                             |
| Serializes models, formats errors, writes logs                                      | `references/access-data-security/data-exposure.md`                                                                                         |
| Hashes, encrypts, generates or compares secrets                                     | `references/access-data-security/crypto-data-protection.md`                                                                                |
| Renders user data into HTML/JS/URLs/headers/emails                                  | `references/access-data-security/output-encoding.md`                                                                                       |
| Touches data or caches in a multi-tenant app                                        | `references/access-data-security/tenant-isolation.md`                                                                                      |
| Changes state with cookie/session-based auth                                        | `references/access-data-security/csrf.md`                                                                                                  |
| Binds request payloads onto models/entities                                         | `references/access-data-security/mass-assignment.md`                                                                                       |
| Builds queries/commands/templates/paths from input                                  | `references/input-api-dependency/injection.md`                                                                                             |
| Deserializes untrusted bytes (sessions, caches, queues, uploads)                    | `references/input-api-dependency/deserialization.md`                                                                                       |
| Configures CORS, headers, cookies, debug, env                                       | `references/input-api-dependency/config.md`                                                                                                |
| Touches API keys, credentials, tokens                                               | `references/input-api-dependency/secrets.md`                                                                                               |
| Validates (or should validate) request input                                        | `references/input-api-dependency/api-contract-validation.md`                                                                               |
| Accepts, stores, processes, or serves files                                         | `references/input-api-dependency/file-handling.md`                                                                                         |
| Makes network requests to user-influenced URLs                                      | `references/input-api-dependency/ssrf.md`                                                                                                  |
| Adds validators, regexes, allowlists, or parsing                                    | `references/input-api-dependency/parser-differentials.md`                                                                                  |
| Adds or upgrades packages; edits manifests, lockfiles, Dockerfiles, or CI workflows | `references/input-api-dependency/dependencies.md`                                                                                          |
| Writes to multiple tables/stores/systems at once                                    | `references/correctness/atomicity.md`                                                                                                      |
| Handles payments, webhooks, retries, emails                                         | `references/correctness/idempotency.md`                                                                                                    |
| Runs jobs, scheduled tasks, or queue consumers                                      | `references/correctness/background-work.md`                                                                                                |
| Shares mutable state, caches, counters                                              | `references/correctness/state-management.md`                                                                                               |
| Reads or writes assuming a query matches exactly one row                            | `references/correctness/cardinality.md`                                                                                                    |
| Computes money, totals, taxes, splits, or rounding                                  | `references/correctness/numeric-precision.md`                                                                                              |
| Stores or computes timestamps, durations, timeouts, expiry                          | `references/correctness/time-clock.md`                                                                                                     |
| Catches/throws errors, maps errors to HTTP statuses                                 | `references/correctness/exception-handling.md`                                                                                             |
| Creates promises, futures, tasks, or publishers                                     | `references/correctness/discarded-async.md`                                                                                                |
| Loads related data inside a loop over a collection                                  | `references/operability/nplus1.md`                                                                                                         |
| Adds endpoints/jobs, handles errors                                                 | `references/operability/observability.md`                                                                                                  |
| Changes database schema                                                             | `references/operability/migration-safety.md` + `references/operability/schema-design.md`                                                   |
| Does work proportional to input or data size (incl. `IN` lists, bulk statements)    | `references/operability/resource-limits.md`                                                                                                |
| Searches, joins, dedupes, or sorts collections in memory                            | `references/operability/algorithmic-complexity.md`                                                                                         |
| Runs async/await, event-loop, or coroutine code                                     | `references/operability/blocking-io-async.md`                                                                                              |
| Calls remote dependencies; sets timeouts, retries, fallbacks, or probes             | `references/operability/downstream-failure.md`                                                                                             |
| Is meant to scale out / run as multiple replicas                                    | `references/operability/statelessness.md`                                                                                                  |
| Caches values, responses, or computed results                                       | `references/operability/caching.md`                                                                                                        |
| — Scoping a target larger than a diff (step 1)                                      | `references/methodology/scope.md`                                                                                                          |
| — Verifying candidate findings (step 4, always)                                     | `references/methodology/verify.md`                                                                                                         |
| — Rating finding severity (step 5, always)                                          | `references/methodology/severity.md`                                                                                                       |
| — Fixing confirmed findings                                                         | `references/remediation/authz-patterns.md`, `references/remediation/async-patterns.md`, `references/remediation/observability-patterns.md` |
