---
name: relay-fleet
description: Drive an immutable cohort of already-planned relay leaves through fan-out and derived status.
compatibility: Requires git, gh CLI, Node.js 18+, and sibling skills; Linux independent isolation requires Node.js 22+.
argument-hint: --fleet-id <id> --leaves-file <path>
metadata:
  related-skills: relay-ready, relay-plan, relay-dispatch, relay-review, relay-merge
  keywords: relay-fleet, fleet, fan-out, parallel dispatch, resume, status, 병렬, 재개, 상태
---
## Inputs
- Env: optional `RELAY_SKILL_ROOT` defaults to `skills`.
- Files: leaves JSON passed by `--leaves-file`, child prompt/rubric/Done Criteria files, immutable cohorts under `~/.relay/fleets/`, and child runs under `~/.relay/runs/`.
- Sibling scripts: `${RELAY_SKILL_ROOT:-skills}/relay-fleet/scripts/relay-fleet.js`, `${RELAY_SKILL_ROOT:-skills}/relay-dispatch/scripts/dispatch.js`, `${RELAY_SKILL_ROOT:-skills}/relay-review/scripts/review-runner.js`, `${RELAY_SKILL_ROOT:-skills}/relay-merge/scripts/finalize-run.js`.

# relay-fleet

## Use when

- Driving already planned relay leaves through fan-out, review/redispatch, serial merge, and close
- Re-running the same fleet command after a crashed or killed session
- Continuing an immutable cohort from its current child-run facts
- Printing read-only aggregate status for a fleet

## Do not use when

- Decomposing raw or ambiguous requests into leaves — use `relay-ready`
- Authoring per-leaf rubrics or dispatch prompts — use `relay-plan`
- Dispatching a single task or run — use `relay-dispatch`
- Reviewing one standalone child PR — use `relay-review`

Run multi-leaf orchestration after `relay-ready` and `relay-plan` have already produced leaf artifacts. A fleet stores only one immutable cohort. Status is derived afresh from vNext `run.json` records and canonical `inspect` results; it never owns child state, retry history, or a cache. Legacy manifests are not read.

Design rationale, rejected alternatives, non-goals, and the Phase 2/3 roadmap: [references/design.md](references/design.md).

To run a dev-backlog sprint batch as one fleet wave, use the mapping recipe in [references/sprint-to-leaves.md](references/sprint-to-leaves.md).

## Input Contract

Use a JSON file containing a non-empty `leaves[]` array. Each leaf must include:

- `leaf_ref`: stable fleet-local child key derived during planning
- `issue_number`: GitHub issue number for fleet issue-lock admission
- `branch`: child dispatch branch
- `prompt_file`: prepared dispatch prompt
- `rubric_file`: prepared relay-plan rubric
- `done_criteria_file`: frozen Done Criteria snapshot
- `ownership`: validated `{ "sprint", "track", "component" }` copied from the dev-backlog sprint-state JSON that supplied the batch

relay-fleet only fans out already-decomposed leaf contracts; it never splits a raw or ambiguous request itself — route that intake through `relay-ready` first and pass its leaf output here.

All leaves must carry the same normalized owner. `ownership.track` must equal the basename of `ownership.sprint` without `.md`; `component` is a separate dev-backlog scope key and need not equal the track. Before admission, the canonical path, track, and component must exactly match the trusted schema-v2 `sprint-state.js --track` result, and the path must resolve to an existing regular file in the current repo's `backlog/sprints/`; relay-fleet does not parse that markdown. Missing, malformed, contradictory, unresolved, stale, or mixed-track ownership is rejected before a cohort or child dispatch exists: one fleet is one track.

Optional per-leaf fields passed through to the current `dispatch.js` contract are `executor`, `model`, `sandbox`, `network_access`, `timeout`, `reasoning`, and `copy`. Submit dependent work in a later fleet wave after its prerequisite fleet is terminal; the immutable cohort intentionally carries no second dependency scheduler.
If a leaf selects an unsupported executor or an unavailable model provider, pause that leaf and correct the explicit leaf input before resuming the fleet.

## Commands

```bash
node "${RELAY_SKILL_ROOT:-skills}/relay-fleet/scripts/relay-fleet.js" \
  --repo . \
  --fleet-id fleet-481 \
  --leaves-file /tmp/fleet-481-leaves.json \
  --parallel 4
```

Read-only aggregate status:

```bash
node "${RELAY_SKILL_ROOT:-skills}/relay-fleet/scripts/relay-fleet.js" \
  --repo . \
  --fleet-id fleet-481 \
  --status
```

The cohort is written with exclusive creation. Repeating exactly the same normalized leaves is idempotent; any byte difference fails closed. `--status` never writes it.

Dry-run validates the leaf file and invokes child `dispatch.js --dry-run` for each leaf without writing a cohort:

```bash
node "${RELAY_SKILL_ROOT:-skills}/relay-fleet/scripts/relay-fleet.js" \
  --repo . \
  --fleet-id fleet-481 \
  --leaves-file /tmp/fleet-481-leaves.json \
  --dry-run \
  --json
```

## Behavior

- The default command invokes `skills/relay-dispatch/scripts/dispatch.js` once per leaf that has no derived child run, and always passes `--fleet-id` plus the typed `--ownership-json` owner.
- A child matches only when its immutable parent id, branch, Done Criteria hash, and ownership digest all match its cohort leaf. Zero matches is retry-pending; multiple matches or an unmatched parent child is operator attention.
- `--review` additionally drives review-pending children and serially finalizes ready-to-merge children. It writes no fleet state; each child remains the sole owner of its lifecycle.
- Pre-record failures have no durable synthetic child state. The same cohort invocation retries its no-run leaf, while the subprocess receipt is the immediate evidence.
- The fleet is `closed` only when every derived child is `merged`. `escalated`, merge blocks, drift, duplicate matches, and orphan parent children remain operator attention.
- Each child dispatch owns worktree creation, in-flight run checks, executor invocation, and child run/fact writes.
- Fleet issue locks are checked before each child spawn; `dispatch.js --fleet-id` performs the durable lock during the actual child run.
- `--status` is read-only and derives the complete view from immutable cohort bytes plus child records and canonical inspections. It never creates files, changes child records, or repairs artifacts.

## SPOF

There is intentionally no daemon. A fleet makes progress only while `relay-fleet` is actively running. Pause by killing the process. Resume by re-running the same primary command with the same `--fleet-id` and, when available, the same `--leaves-file`; the command re-derives child actions, skips waiting children, and continues no-run or exact-redispatch leaves.

## /goal Persistence

For long fleets, the operator may activate host `/goal` after fan-out to keep one session driving the daemonless loop. Use the copy-paste condition and idempotent operating loop in [references/goal-persistence.md](references/goal-persistence.md); the condition must name the transcript-visible `--status --json` check, not just an operator process.
