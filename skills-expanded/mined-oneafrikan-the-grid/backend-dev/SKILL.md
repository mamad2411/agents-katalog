<!--
  SKILL.md — Backend Dev operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific framework unless injected via a stack overlay.
  Stack-specific commands are NOT here — they live in stacks/<stack>/ overlays.
  Injection points are marked: `STACK: ...`
-->

# Skill: Backend Dev

## Invocation

```
/backend_dev <task reference — PRD path + task list>
```

Or picked up from a Signal Protocol entry / PR assigned to backend-dev. Either
way: **no PRD, no work.** If there's no PRD to reference, ask for one.

---

## Step 1 — Read the PRD and confirm the contract

Before writing code, confirm from the PRD:

| Question | Why |
|---|---|
| What are the exact tasks assigned to backend? | Bounds the work; anything outside is not yours to build |
| What is the API contract? (method, path, request, response, status codes) | The frontend builds against this — it must be agreed, not assumed |
| What data model changes are needed? | Migrations are the riskiest change; plan them first |
| What auth/permissions apply? | Security is designed in, not bolted on |
| What are the acceptance criteria + verification command? | This is your definition of done |

**Rule:** If the contract is ambiguous or the PRD is silent on something you
need, ask once. If still unclear, escalate — do not guess the contract.

---

## Step 2 — Write failing tests first

For each acceptance criterion, write a test that fails for the right reason:

- Happy path — the criterion as stated.
- Boundary — empty input, max size, missing optional fields.
- Error path — invalid input, unauthorised, not found, conflict.
- Security — unauthenticated access rejected, injection attempt parameterised away.

<!-- STACK: stack-specific test framework + how to run a single test injected here -->

Run them. Confirm they fail. Now you have a target.

---

## Step 3 — Implement to the contract

Build the smallest code that turns the tests green:

**Data layer**
- Define/extend the model. Make invalid states unrepresentable where you can.
- Write the migration: forward-safe, reversible if possible, never destructive without explicit sign-off.
- <!-- STACK: stack-specific ORM / migration syntax injected here -->

**API layer**
- Validate every input at the boundary before any processing.
- Parameterise every query — never string-build SQL.
- Return the agreed status codes and the agreed error format.
- Enforce auth/permissions per the PRD.

**Business rules**
- Keep them in one place, not scattered across handlers.
- Make side effects explicit and testable.

---

## Step 4 — Verify

- All tests green, including the boundary and error cases.
- Run the PRD's verification command — it must pass.
- Lint / type-check clean.
- No secret in logs, no secret in the diff.
- Re-read the diff as a reviewer would: does every line trace to a task?

---

## Step 5 — Hand off (async)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.

Open a PR (or append to `signals/→<agent>.md`) with:

```markdown
## Backend — <Feature Name>

### PRD
PRD: <path> (Section: <backend tasks>)

### What changed
- <endpoint / model / migration> — <one line why>

### API contract (for frontend-dev)
- `<METHOD> <path>` → request: <shape> | response: <shape> | errors: <codes/format>

### Migration notes (for devops)
- <forward-safe? reversible? data backfill needed?>

### Verification
- Command: `<verification command>`
- Tests: <count> added, all passing

### Definition of done
- [ ] All assigned PRD acceptance criteria met
- [ ] Verification command passes
- [ ] Contract documented above for frontend
```

Then flag QA (qa-engineer) to verify, and the Tech Lead to review. Do not merge
your own work to production — QA gates, the human approves the deploy.

---

## API contract checklist

Every endpoint you ship answers all of these:

- [ ] Method + path follow the project's REST conventions
- [ ] Request body validated; bad input → documented 4xx, not a 500
- [ ] Response shape matches the contract the frontend was given
- [ ] Auth enforced; unauthenticated/unauthorised → 401/403
- [ ] Errors use the project's standard error format
- [ ] Pagination/filtering follow the existing pattern (don't invent a new one)
- [ ] No N+1 query on the common path

---

## Migration safety rules

- **Additive first.** Add columns/tables nullable or with defaults before backfilling.
- **Two-phase for renames/drops.** Deploy code that tolerates both shapes, migrate, then remove the old shape.
- **Never destructive without sign-off.** Dropping a column or table needs explicit human confirmation (escalate).
- **Always reversible where possible.** Write the down-migration; if it can't be reversed, say so loudly in the PR.

<!-- STACK: stack-specific migration tool + isolation (per-worktree DB/schema) injected here -->
