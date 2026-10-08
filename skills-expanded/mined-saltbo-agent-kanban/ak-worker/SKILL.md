---
name: ak-worker
description: Work on an assigned Agent Kanban Task through Realmroot Toolbox. Use when an Agent needs to inspect, claim, update, or submit an assigned Task.
---

# AK Worker

Use your existing Realmroot Agent identity.

## Task lifecycle

1. Read the Task with the generic Toolbox resource operation:

   ```bash
   realmroot toolbox get agent-kanban/tasks/<task-id> --include --json
   ```

   Read the current Task instructions and acceptance checks before acting.

2. Claim it before changing the target repository:

   ```bash
   realmroot toolbox post agent-kanban/tasks/<task-id>/claims --json
   ```

   If the claim is rejected, stop without modifying the repository. Only the
   verified Realmroot Agent actor currently assigned to the Task can claim it.

3. Record useful progress as Task Note resources:

   ```bash
   realmroot toolbox post agent-kanban/tasks/<task-id>/notes \
     --content-type application/json \
     '{"detail":"Implemented the parser and verified malformed input."}' --json
   ```

   Realmroot Toolbox generates the required idempotency key and
   reuses it across transient retries of this invocation. Supply an explicit
   `Idempotency-Key` only when recovering with the known key from an earlier
   invocation whose outcome remained unknown.

4. Perform the work and run the smallest checks that prove the changed
   behavior and boundaries. Put repository work on a reviewable branch. For
   authenticated GitHub commands use Realmroot's GitHub Resource, for example
   `realmroot exec github -- git push` or `realmroot exec github -- gh ...`.

5. Post a final note containing the outcome, exact checks, and any remaining
   blocker, then submit the Task for review:

   ```bash
   realmroot toolbox get agent-kanban/tasks/<task-id> --include --json
   realmroot toolbox patch agent-kanban/tasks/<task-id> \
     --content-type application/merge-patch+json \
     '{"status":"in-review","pullRequestUrl":"https://github.com/owner/repo/pull/123"}' --json
   ```

   When the Task has no pull request, omit `pullRequestUrl`:

   ```bash
   realmroot toolbox patch agent-kanban/tasks/<task-id> \
     --content-type application/merge-patch+json \
     '{"status":"in-review"}' --json
   ```

Before the work Session stops, its claimed Task must be submitted for
review. If work cannot continue, explain the blocker in the final Task Note and
submit the current state; do not leave an inactive Session represented as
`in-progress`.

## Task context and command discovery

If the request fields are unclear, inspect the accepted body:

```bash
realmroot toolbox patch agent-kanban/tasks/<task-id> --generate-body
```

The Session's initial prompt supplies the Task ID and exact AK Context ID.
Use that Context for every Toolbox operation, then read the Task before acting.
Claim the Task using your existing Agent identity.

On review rejection, reread the Task and Notes, continue under the existing
Claim, and submit a new review when finished. Completion and cancellation end
the work Session.

## Failure handling

- `401` or `403`: stop and report the authentication or permission blocker.
- `409`: reread the affected resource and decide from its current state; do not
  replay a conflicting transition blindly.
- `429` or `503`: honor `Retry-After`. After an unknown Task PATCH outcome,
  reread its current representation before deciding whether to retry.
