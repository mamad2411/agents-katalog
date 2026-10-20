# Hunt compatibility command

Use the `research-agent` skill.

`/research` is retained as a compatibility command, but the user-facing workflow is **Hunt**.
Do not launch the legacy `/research/*` verifier or `/agent/hunt/*` engine for a Hunt request.

Resolve the authorized target, create a target-bound expiring credential approval, then start:

```http
POST /hunts
{
  "target_id": "...",
  "objective": "...",
  "budget_profile": "balanced",
  "approval_receipt_id": "..."
}
```

Drive the returned run from the current coding-agent session through its bounded query, capability,
candidate, verifier, and finish endpoints. Candidates must cite real evidence references; prose is
not evidence. Stop on `completed`, `failed`, `cancelled`, or `budget_exhausted`.

Use `/hunt?run={hunt_id}` as the UI link.
