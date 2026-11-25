---
name: agent-workboard
description: Plan and execute agent work in Soulsteads Agent Workboard using its JSON CLI or MCP tool. Use for epics, stories, bugs, dependencies, assignments, leased claims and issue handoffs in a configured workboard.
---

# Agent Workboard

Use `workboard` on PATH with the configured `WORKBOARD_DB` (absolute path) and
`WORKBOARD_ACTOR` (this worker's stable ID). All agents on a board share the DB
and use distinct actor IDs. The CLI and MCP operate on the same persisted state.
Do not silently create an unrelated board if the intended DB is unknown.

## Discover and bootstrap

- `workboard schema` describes every operation, field and enum.
- `workboard run '{"op":"project_list"}'` discovers projects.
- `workboard run '{"op":"agent_list"}'` checks registered identities.
- Register the configured actor if missing with `agent_register` (`id`, `name`,
  optional `capabilities`). Registration of existing IDs conflicts.
- If using MCP, send the same JSON command object directly to
  `workboard_execute`. Its input schema is the CLI schema.

Run one command per invocation. Large descriptions can use stdin:

```bash
workboard run <<'JSON'
{"op":"issue_create","project":"AG","kind":"bug","title":"Fix worker restart","description":"Describe reproduction and expected behavior","acceptance_criteria":["Restart preserves progress"],"priority":"high"}
JSON
```

CLI responses have `ok` and `result`, or `error` with a nonzero exit status.
MCP returns JSON text plus `structuredContent.result`; check `isError` and
`structuredContent.error` on failure. Unknown fields are rejected.

## Plan work

Use `board` with a project key and `issue_get` with an issue key to read current
context. `issue_get` includes the issue, links, blockers and direct children.
Kinds are `epic`, `story`, `task`, `bug`, `subtask`, `spike`. Hierarchy is
`epic -> story/task/bug/spike -> subtask`; subtasks need a parent. Parents stay
in the same project. Write concrete acceptance criteria and attach relevant
repo/artifact references in `metadata` or comments.

Use `link_add` with `source`, `target` and `kind`: source `blocks` target;
`relates_to` is symmetric; `duplicates` is informational. Blocking links plus
hierarchy must remain acyclic. Canceled blockers count as resolved. Blockers
apply directly, not through ancestor inheritance.

Use `issue_assign` to reserve work for an active agent, or null to unassign.
Assignment is a coordinator override that revokes a lease, so do not use it
merely to refresh your own claim. Use labels, priorities and sprints to organize
work. To find an issue by what it says, use `issue_search` with a query such as
`lease timeout state:ready -flaky` (words, "phrases", prefix*, OR, -exclusions, and
`state:` `kind:` `priority:` `assignee:` `label:` `is:actionable` filters); it ranks the best
match first and returns a snippet. `filter_save` keeps a search under a name for others.
`issue_list` supports a filter for project/kind/state/assignee/parent/sprint/
label/text/actionable and offset/limit. `epic_progress` counts all descendants.

## Execute safely

1. Read the board and issue context. Move executable backlog work to `ready`
   using `issue_transition` with the current `expected_revision`.
2. `issue_claim` with `project` and optionally `key` atomically selects ready
   non-epic work assigned to nobody or yourself. It returns `claimed: null` if
   none is eligible. Do not treat null as an error or busy-loop.
3. Retain `claimed.lease.token`, expiry and revision. The default lease is 900
   seconds; `lease_seconds` accepts 1–86400. Heartbeat before expiry with
   `issue_heartbeat` (`key`, `lease_token`, optional `lease_seconds`). Heartbeats
   return a new issue revision.
4. Implement and validate the acceptance criteria. `issue_update` and
   `issue_transition` require the latest `expected_revision` and, while leased,
   `lease_token`. Use the revision returned by each mutation or fetch it again.
   Arrays/metadata updates replace values; nullable fields are removed with
   `clear_parent`, `clear_sprint`, `clear_estimate` rather than null.
5. Submit completed work with `issue_submit`: `key`, `expected_revision`, the
   current `lease_token`, a `summary`, and 1–64 `evidence` objects containing
   `reference` and `summary`. This records a snapshot and moves to `in_review`,
   releasing the lease for handoff. Comments alone do not authorize closure.
6. A different registered actor inspects the submission and calls `issue_review`
   with `key`, `expected_revision`, `submission_id`, `approved`, and a substantive
   `note`. The worker cannot approve its own submission. A rejected submission
   must return to `in_progress` and be resubmitted after corrections.
7. After approval, `issue_transition` to `done` with the latest revision and no
   old lease token. Finish descendants before closing parents. Review records
   capture a reviewer's attestation; `external_outcome_verified` remains false
   because Workboard does not execute or verify the referenced external work.

On a revision conflict, reread and reconcile before editing. On an expired or
revoked lease, stop submitting that work: a fresh revision does not restore
ownership. The next project claim recovers expired work and issues a new token.
Only the owning actor and unexpired token can renew, edit or release a lease.
After a lost response, retry a command you sent with an idempotency key (CLI
`--idempotency-key`, HTTP `Idempotency-Key`, MCP `idempotency_key`): a repeat returns the
original result marked `replayed` instead of applying twice. For a command sent without
one, inspect `issue_get` and `events` before retrying a mutation;
creation, comments and claims are not automatically deduplicated.

## Block or hand off

Use `issue_release` with key/token to return interrupted work to ready and clear
assignment. To record a blocked condition, add a comment and transition to
`blocked`; this clears the lease but retains assignment. Unassign explicitly if
another agent should pick it up later. Use `workflow` for the complete transition
map. Reopen terminal work to backlog only after reopening ancestors, resolving
dependent-state conflicts and moving it out of any completed sprint.

For handoffs, use comments for context and `events` with optional issue key and
exclusive `after` event ID for incremental history. `comment_list` also accepts
`after`. Both default to 100 results, max 1000; advance using the last returned ID.
Issue-list offset pages are snapshots, not an incremental event feed.

This is a trusted local workspace: actor IDs attribute work, not authenticate it.
Respect the caller's requested project and scope when coordinating other agents.

## Assigned keys and remote access

An operator assigns a key to your registered agent using `api_key_create`. Keep
that credential private in `WORKBOARD_API_KEY`. Do not issue or revoke keys from
a worker session. With a local DB, the CLI and MCP use the key's agent identity
instead of `WORKBOARD_ACTOR`. A missing/invalid/revoked key fails authentication;
contact the board operator instead of switching to another agent's identity.

For a remote board, use `WORKBOARD_URL` and the assigned key with the HTTP API:

```bash
curl --fail-with-body --silent --show-error "$WORKBOARD_URL/api/commands" \
  -H "Authorization: Bearer $WORKBOARD_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary @- <<'JSON'
{"op":"issue_claim","project":"AG","lease_seconds":900}
JSON
```

The HTTP command result is the object itself, without the CLI's `ok`/`result`
wrapper. Errors return `error` with an HTTP failure status. Use the same revision
and lease-token rules. Keys bind the actor; do not include an `actor` field.
Authenticate every request using the header, never a URL query parameter. Use
HTTPS beyond localhost. Never put the key in issue text, comments or logs.

The web dashboard follows work through read-only `/api` views. Those views redact
lease tokens; use command responses to manage your own claims. Other agents can
see the board; assignments reserve work and claims coordinate execution.
