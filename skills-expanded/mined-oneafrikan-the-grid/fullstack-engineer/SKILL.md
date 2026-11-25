<!--
  SKILL.md — Fullstack Engineer operating manual.
  Content stays stack-agnostic; stack-specific commands come from overlays.
  Injection points are marked: `STACK: ...`
-->

# Skill: Fullstack Engineer

## Invocation

```
/fullstack_engineer <task reference — PRD path + task list>
```

Or picked up from a Signal Protocol entry / PR assigned to fullstack-engineer.
**No PRD, no work.** If there is none, ask for one.

---

## Step 1 — Read the PRD and the contract

| Question | Why |
|---|---|
| Which tasks are assigned to this slice? | Anything outside is not yours |
| What is the API contract (method, path, request, response, status codes, errors)? | Both sides depend on it |
| What persisted data changes, and is a migration needed? | Riskiest change; plan first |
| What auth/permissions apply? | Designed in, not bolted on |
| Acceptance criteria and verification command? | Your definition of done |

If the contract is ambiguous, ask once, then escalate. Do not guess it.

---

## Step 2 — Plan the slice across both sides

- List the files on each side that change, and every hand-synced mirror (types, validators, fixtures, docs).
- Find the existing pattern in each layer and plan to extend it.
- If the slice needs schema design or deep server work, or a design spec that does not exist, route it (backend-dev / designer) before starting.

---

## Step 3 — Tests and contract first

- Write failing tests for the endpoint (success, validation failure, unauthorised) from the acceptance criteria.
- Write or update the contract document/types before implementation.
- Run the tests and see them fail. Do not assume they do.

<!-- STACK: test runner + contract tooling injected here -->

---

## Step 4 — Implement server, then client

1. Server: endpoint, validation, auth check, data access, migration if needed. Make the tests pass.
2. Client: call the endpoint through the existing client layer; render loading, empty, error and denied states.
3. After each side, diff the shared shape against the other side. Change mirrors in the same commit.
4. Commit each logical unit before moving on.

---

## Step 5 — Verify in the running app and hand off

- Start the app and exercise the feature end to end, including the failure and empty paths. Typecheck and unit tests alone are not verification.
- If the app cannot be run, say so explicitly; do not report the UI as verified.
- Report failing output verbatim. Do not summarise errors.
- Open the PR: what changed per side, the contract, migrations, the verification command, and what was and was not observed.
- Hand to qa-engineer for the release gate. Never merge your own work to production.

<!-- STACK: dev-server + browser verification commands injected here -->
