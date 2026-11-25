---
name: pause-for-review
description: >
  Use before crossing a decision boundary: a direction choice (multiple
  valid implementations), a contract commitment (public API, database
  schema, proto/GraphQL field, migration, auth/tenant boundary, event
  format), a costly-to-reverse action (delete data, force push, deploy
  to shared env), after a discovery that invalidates the plan, or
  after completing an independently reviewable slice. Not for routine
  work inside the agreed slice — never pre-emptively, never based on
  size.
---

# Pause for Review

Pause only at the **decision boundaries** listed below — direction, contract, reversibility, discovery, or slice complete. Do not pause for size. Do not manufacture checkpoints on noise.

## Continue Without Pausing

Stay inside the agreed slice. Examples:

- Happy path → error cases for the same behavior
- Adding more tests or edge cases under the same contract
- Fixing failures uncovered by the current verification command
- Local refactor inside the slice (extract helper, rename a private symbol)
- Mechanical cleanup: formatting, imports, narrow renames
- Running more verification

The user can interrupt at any time. Do not pre-emptively pause "to be safe" — pre-emptive pauses train the user to rubber-stamp, which destroys the signal of a real pause.

"Same slice" means the same behavior under the same contract. Adding a new helper module, a new public function, or a new code path that wasn't in the agreed scope is a new slice — see the boundaries below. If no slice has been explicitly agreed, treat the user's last instruction as the slice.

## Stop and Surface for Review

Pause when about to cross any of these boundaries. Cross only after the user acknowledges.

### 1. Direction — multiple valid paths exist

- Choosing between materially different implementation strategies
- Picking a name or abstraction other code will depend on
- Resolving an ambiguous line in the spec
- Deciding what "done" means when the spec is silent

### 2. Contract — committing to something external

- Public API, GraphQL/REST schema, gRPC proto message
- Database schema, migration, or index change
- CLI flag, env var, config file format
- Permission, authorization, tenant, or data-ownership boundary
- Event or message format consumed by other services

### 3. Reversibility — costly to undo

- Data migration with non-trivial backfill
- Deleting code, data, branches, or files (especially `git reset --hard`, `rm -rf`)
- Deploying to a shared environment
- Force push, history rewrite, dependency downgrade

### 4. Discovery — the plan turned out wrong

- Verification reveals the spec contradicts code reality
- Hit a constraint that invalidates the chosen approach
- A "small fix" turned out to require crossing boundaries 1–3

### 5. Slice complete — independently reviewable unit done

- A vertical slice is end-to-end working
- All tests for the agreed scope pass
- A new architectural path runs end-to-end for the first time, even if not all cases are covered

## Pause Output

When pausing, produce this summary so the user can review without re-reading the diff:

```text
Pause: <which boundary, in 1 line — e.g. "Contract: about to commit gRPC proto field numbers">
Done this round:
  - <bullet per behavior change, not per file>
Files: <list of changed paths>
Verified: <command + result, or "not run because <reason>">
Risks / unknowns: <none, or list>
Decision needed: <specific question, or "review and ack to continue">
```

Notes on the template:

- **`Pause:` first**: lets the user pick a review mindset (decision / approval / sign-off) before reading details.
- **`Verified:` is mandatory**: if you didn't run anything, write "not run because <reason>". Silence reads as "passed".
- **Risks vs Done**: if you're not sure something works, put it under `Risks / unknowns`, not under `Done this round`. The summary is a navigation aid for the user — don't use it as a self-confirmation that review happened.
