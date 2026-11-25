---
name: engineering-standards
description: The engineering standards agentic-forge always applies when writing code in a target repo — change discipline, test discipline, a security baseline, and conventions. Loaded by the software-engineer base role (and reusable by reviewers/QA); kept off the always-on listing.
disable-model-invocation: true
---

# Engineering standards

The standards we hold to when implementing in a target repo. This is deliberately short — it
lists only what is project-opinionated or easy to skip, not general programming knowledge the
model already has. Read the matching **stack pack** (`${CLAUDE_PLUGIN_ROOT}/skills/<stack>-patterns/SKILL.md`
— like this file, off the listing, so read rather than invoked) for language/framework idioms.

## Always

- **Fit the repo.** Read neighbouring code first; mirror its conventions, naming, structure,
  and error style. Do not impose a new style or framework.
- **Small, scoped changes.** Do exactly the task; surface unrelated issues as follow-ups
  rather than fixing them inline. State any assumption you had to make.
- **Tests ship with behaviour.** Every behaviour change adds or updates tests, including the
  boundary/error cases. Never weaken, skip, or delete a test to make the suite pass — fix the
  code.
- **Fail loudly.** Handle errors or propagate them with context; no silent excepts, no
  swallowed failures.
- **Security baseline.** Two separate duties at a trust boundary, and one does not discharge
  the other. *Validate*: a value that arrives from a user, a request, a file or the network gets
  an explicit check where it enters — type, emptiness, length or range, allowed shape — and a
  bad value is rejected with a clear error before it reaches a query, a command, a path or a
  template. *Parameterise*: queries and commands take that value as a bound parameter, never
  string-built. A parameterised query prevents injection; it still accepts an empty name, a
  10 MB string or the wrong type, so it is not validation — a delegated engineer once wrote
  "the name crosses a trust boundary, so it is bound as a parameter" and stopped there, five
  runs out of five (ADR 0099). No secrets in code or logs; safe defaults; least privilege.
- **Dependencies are a cost.** Prefer the standard library and what the repo already uses;
  justify any new dependency.
- **Leave the gate green.** Match the repo's lint/type/test gate before handing off.

## Debugging a defect (before you write the fix) — ADR 0074

- **Systemic or per-input?** If it fails for *every* case — never worked for anyone, since launch
  — the cause is almost always parsing, serialization, or one config/wiring mistake. Do not
  theorize about input-specific edge cases. A query showing the feature never once succeeded is
  the tell.
- **Two-strike rule.** After ~2 failed hypotheses, **stop shipping fixes**. Get ground truth
  first: add temporary diagnostic logging (or raise existing DEBUG logs to INFO) and capture one
  real failing run before the next change. Production log levels routinely hide diagnostics that
  already exist; a tiny raise-then-revert is faster than another speculative fix.
- **Read the signal, not the theory.** An empty result on an HTTP 200 with a populated body is a
  **parsing** bug, not a reachability bug. External APIs are not type-uniform — the same object can
  return `"0.03"` as a string beside sibling fields that are numbers.
- **Verify against the real failure, not the unit tests.** Field case: two consecutive wrong fixes
  were reviewed, merged and deployed, both with green tests; one diagnostic run found the cause
  immediately.

## Don't

- Don't restate or re-derive well-known concepts in code comments or output — be concise.
- Don't touch the main checkout; work in the provided worktree.
- Don't broaden scope, change public contracts, or reformat untouched code without reason.
