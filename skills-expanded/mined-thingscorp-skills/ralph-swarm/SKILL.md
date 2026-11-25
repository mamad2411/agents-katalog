---
name: ralph-swarm
description: >-
  use this when independent Ralph lanes must run in parallel — full clones,
  source checkout unchanged, results under refs/ralph/swarm, never merge
  or push those refs
license: MIT
metadata:
  portability: portable
---
# ralph-swarm

Run independent Ralph sessions in parallel. Each lane is a full clone with
its own Git directory, topic branch, `.ralph/` state, lock, recovery refs,
and log. The source checkout does not change. Integrate by review, not by
auto-merge.

Load **ralph-loop** first. This skill only adds the parallel contract.

## When

- Several goals are independent enough to run at the same time.
- You want isolation stronger than linked worktrees.
- You need namespaced result refs you can inspect before any merge.

Do **not** swarm goals that share a mutable database, a fixed port, a
browser profile, or a remote deploy target.

## Manifest

Keep the manifest **outside** the repo (temp file, not committed).

```json
{
  "version": 1,
  "jobs": 5,
  "max_iterations": 3,
  "max_turns": 40,
  "sessions": [
    { "id": "api", "goal": "Complete the API work." },
    { "id": "ui", "goal": "Complete the user interface work." }
  ],
  "pass_env": []
}
```

- `jobs` — parallel cap. Hard ceiling: 32 jobs, 64 sessions.
- `max_iterations` / `max_turns` — per-lane caps.
- `sessions[].id` — stable lane id (kebab-case).
- `sessions[].goal` — one independent objective.
- `pass_env` — allowlist of extra env var **names**. Default worker env
  has no keys, tokens, passwords, or auth variables. Never pass `*_API_KEY`,
  `*_TOKEN`, or `*_SECRET` unless the owner named that exact variable.

## How

1. Confirm every lane goal is independent. If two lanes would contend on
   the same file, port, DB, or deploy — split the swarm or run ralph-loop
   serially.
2. Snapshot the source HEAD. Do not mutate the source checkout.
3. For each lane: `git clone --no-local` into an isolated directory.
   No linked worktrees. No shared `.git`.
4. In the clone, create a topic branch and a fresh `.ralph/` plan+items
   for **that lane's goal only**. Then run ralph-loop under the lane cap.
5. On lane success, store the lane HEAD at
   `refs/ralph/swarm/<run-id>/<lane-id>` on the source repo (fetch the
   clone ref; do not merge).
6. On lane failure, keep `refs/ralph/recovery/…` inside the clone and
   record the stop reason in swarm status. Do not merge a failed lane.
7. Never merge or push swarm refs. The owner reviews:
   `git log main..refs/ralph/swarm/<run>/<lane>`
   `git diff main...refs/ralph/swarm/<run>/<lane>`
   then cherry-picks or merges **by hand**.
8. Stop: kill the lane process groups, set running false, leave refs
   intact.

## Status

Durable swarm state (JSON) records: run id, source HEAD, per-lane clone
path, branch, item counts, last progress line, ref name, stop reason.
Print that. Do not require the clones to stay mounted after refs are saved.

## Rules

- Full clone per lane. Linked worktrees are a defect.
- Source checkout stays clean.
- Results live only under `refs/ralph/swarm/<run>/<lane>`.
- Never merge, push, or force-push those refs.
- Each lane owns its lock. Do not share `.git/ralph.lock`.
- Worker env is a small allowlist. Keys stay out.
- Temporary provider limits: retry twice with exponential backoff, then stop
  that lane and report. Do not spin the whole swarm on one 429.

## Anti-patterns

- Five lanes on one working tree.
- Auto-merging swarm refs because "they all passed."
- Sharing `node_modules`, a Docker volume, or a staging URL across lanes.
- Putting API keys in the manifest body instead of `pass_env` names.
- One swarm session whose goal is "do the whole product."

## Related

ralph-loop · to-spec · quality-loop · handoff
