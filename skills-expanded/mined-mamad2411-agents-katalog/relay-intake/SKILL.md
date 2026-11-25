---
name: relay-intake
argument-hint: "[raw request or ambiguous task description]"
description: Shape a raw request into one-or-more relay-ready leaf contracts with frozen Done Criteria snapshots. Use before relay-plan when the task is ambiguous, oversized, or missing a stable review anchor.
compatibility: Requires git and Node.js 18+.
metadata:
  related-skills: "relay, relay-plan, relay-dispatch, relay-review"
---

# Relay Intake

Use this skill when `/relay` cannot safely bypass straight to planning.

## When Intake Is Required

Run intake when any of these are true:
- the request is free-form or ambiguous
- the task may contain multiple steps or multiple leaves
- no stable Done Criteria anchor exists yet
- the issue/task text is too broad to review safely as-is

Bypass intake only for a single relay-ready task with a trustworthy review anchor already available.

## Output Contract

Persist all of the following under `~/.relay/requests/<repo-slug>/<request-id>/`:
- request artifact: `../<request-id>.md`
- raw request: `raw-request.md`
- relay-ready handoffs: `relay-ready/<leaf-id>.md`
- frozen Done Criteria snapshots: `done-criteria/<leaf-id>.md`
- append-only events: `events.jsonl`

The request artifact frontmatter may also carry:
- `readiness.clarity`
- `readiness.granularity`
- `readiness.dependency`
- `readiness.verifiability`
- `readiness.risk`
- `next_action`
- `leaf_count`
- `paths.handoff` + `paths.done_criteria` for single-leaf requests
- `paths.handoffs` + `paths.done_criteria` for multi-leaf requests
- `decomposition.leaf_order`
- `decomposition.dependencies`

Each normalized handoff must contain:
- `request_id`
- `leaf_id`
- `title`
- `goal`
- `order`
- `depends_on`
- `in_scope`
- `out_of_scope`
- `assumptions`
- `done_criteria_path`
- `escalation_conditions`

## Persistence Step

Write a JSON contract file with:
- `source.kind`
- `request_text`
- either `handoff` for single-leaf or `handoffs[]` for multi-leaf
- per leaf: `leaf_id`, `title`, `goal`, `order`
- optional per leaf: `depends_on`
- per leaf: `in_scope`, `out_of_scope`, `assumptions`
- per leaf: `done_criteria_markdown`, `escalation_conditions`

Persist it with:

```bash
${CLAUDE_SKILL_DIR}/scripts/persist-request.js --repo . --contract-file /tmp/relay-intake-contract.json --json
```

Optional contract fields:
- `readiness.clarity`: `high | medium | low`
- `readiness.granularity`: `single_task | multi_task | unclear`
- `readiness.dependency`: `none | internal | external`
- `readiness.verifiability`: `high | medium | low`
- `readiness.risk`: `low | medium | high`

Preflight shaping stays append-only in `events.jsonl`. Use the portable intake event types:
- `proposal_presented`
- `question_asked`
- `question_answered`
- `proposal_accepted`
- `proposal_edited`

Track the immediate follow-up as `next_action` on the request artifact. Do not create a second state machine for intake.

## Downstream Handoff

After persistence succeeds:
1. use `relay-ready/<leaf-id>.md` as the source-of-truth input for `relay-plan`
2. dispatch with:

```bash
${CLAUDE_SKILL_DIR}/../relay-dispatch/scripts/dispatch.js . \
  -b <branch> \
  --prompt-file <dispatch-prompt-path> \
  --rubric-file <rubric-path-from-relay-plan> \
  --request-id <request-id> \
  --leaf-id <leaf-id> \
  --done-criteria-file <done-criteria-path>
```

3. for multi-leaf requests, dispatch leaves in `decomposition.leaf_order`, respecting `depends_on`
4. let `relay-review` read the frozen snapshot from the run manifest anchor

Do not create a second lifecycle. Intake stops once the relay-ready contract is persisted.
