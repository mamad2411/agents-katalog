---
name: eng-code-review
version: 1.0.0
description: Review a diff or pull request for correctness, security, and performance, returning specific, severity-ranked, fix-ready findings anchored to file and line.
author: matrixx0070
tags: [code-review, security, performance, correctness, quality, pull-request]
capabilities: []
---

## When to use

Any time you are handed a diff, PR, or patch to assess before merge. Review the change, but read enough surrounding context to judge its blast radius.

**Not for:** whole-codebase audits, style bikeshedding a formatter already handles, or rewriting the author's approach when the existing one is correct. Review what changed, not what you'd have written.

## Method

1. **Understand intent first.** Read the description and diff; restate what the change should do. If intent is unclear, that is finding #1 — stop and ask.
2. **Correctness.** Trace edge cases: empty/null inputs, off-by-one, timezone/locale, concurrency and races, error paths, partial failure, idempotency. If the change touches shared state or async flow, escalate scrutiny here.
3. **Security.** Check injection (SQL/command/template), missing authz, unvalidated input, secrets in code, unsafe deserialization, SSRF, and leaky error messages. If the diff touches an auth or trust boundary, treat every input as hostile.
4. **Performance.** Hunt N+1 queries, unbounded loops/allocations, missing indexes, synchronous work in hot paths, chatty network calls.
5. **Design & maintainability.** Naming, duplication, dead code, test coverage of the new logic, backward compatibility.
6. **Rank each finding** Critical / Major / Minor / Nit. Quote `path:line`, explain the concrete risk, propose a fix.
7. **Set the verdict from the worst finding**: any Critical or unaddressed Major ⇒ Request-changes or Block; only Nits ⇒ Approve-with-nits.

Prioritize findings that cause bugs, breaches, or outages over stylistic preference.

## Example

```
Finding (Critical) — src/api/orders.ts:88
  `db.query("... WHERE id=" + req.params.id)` — SQL injection via `id`.
  Why: `id` is unvalidated user input concatenated into SQL.
  Fix: use a parameterized query: db.query("... WHERE id=$1", [id]).
```

## Pitfalls

- **Approving because it "looks fine"** without tracing the error and concurrency paths.
- **Vague findings** ("this could be cleaner") with no line, risk, or suggested fix — unactionable noise.
- **Nit-flooding** that buries the one Critical under twenty style comments.
- **Missing the diff's blast radius** — a changed shared helper affects every caller; check them.

## Output format

```
Summary: <1-2 lines: intent + overall verdict>
Verdict: Approve | Approve-with-nits | Request-changes | Block
Findings:
  [Critical] path:line — issue — why it matters — suggested fix
  [Major]    path:line — ...
  [Minor]    path:line — ...
  [Nit]      path:line — ...
Questions for author: <blocking unknowns, if any>
```
