# Approval Gating

The orchestrator invokes this skill before any destructive action to pause execution and request explicit human approval.

## When to invoke
- Before calling a tool listed in `rules/governance.yaml` destructive_actions.
- Before any action that could materially change production state (merge, close, delete, deploy).

## Input
- `action`: a human-readable description of the action (string).
- `target_url`: the URL or identifier of the target resource (string).
- `requester`: who/what triggered the action (string).
- `channel`: the originating chat channel or dashboard session (string).
- `timeout_minutes`: from `rules/governance.yaml` (default 15).

## Destructive actions (from `rules/governance.yaml`)
Examples:
- `github.merge_pull_request`
- `github.delete_branch`
- `ado.merge_pr`
- `ado.close_work_item`
- `servicenow.close_incident`
- `jira.transition_issue` with status `Closed`

## Flow
1. Detect a destructive tool call.
2. Return `approval_required` with an `approval_id`.
3. Write a pending approval record to the session store.
4. Post an approval card to the originating chat channel with `Approve` and `Deny` buttons.
5. Wait for the user's response.
6. On approval, re-issue the tool call. On denial, abort the action and report the decision.
7. If the request times out, mark it `timed_out` and default to **deny**.

## Output
Return a status object:

```json
{
  "approval_id": "string",
  "status": "pending|approved|denied|timed_out",
  "action": "string",
  "target_url": "string",
  "requested_at": "ISO timestamp",
  "timeout_at": "ISO timestamp"
}
```

## Timeout rule
Approval requests expire after the configured timeout (default 15 minutes). **Default is always deny on timeout** — never auto-approve.
