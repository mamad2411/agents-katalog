---
name: oe-plane-triage
description: Improve manually created Open Engine Backlog issues into agent-ready tasks without guessing the target agent code. Use for triage agents such as Hermes, Agent Zero, Claude Code, or any runtime that prepares Plane issues for Open Engine execution.
triggers:
  - "triage Open Engine backlog"
  - "improve Open Engine task"
  - "needs-agent-triage"
  - "agent-ready Plane issue"
---

# Open Engine Task Triage

Use this skill when acting as a **triage/task-refinement agent** for Open Engine Backlog work items in Plane.

The triage agent improves issue quality. It does **not** execute the underlying task.

Open Engine coordination is stigmergic: agents and humans coordinate by reading and improving visible traces in Plane rather than relying on hidden chat context. The triage pattern is:

```text
observe trace → interpret local state → improve task trace → leave triage receipt
```

## Core role

For each eligible Backlog issue:

1. Inspect the title, description, labels, comments, and current state.
2. Decide whether the issue is eligible for triage.
3. If eligible, improve it into an agent-ready Open Engine task using the task-writing guide.
4. If essential information is missing, make the need visible to a human.
5. Stop without executing the task.

Process a bounded amount of work per run. Prefer **one issue per run** unless the caller explicitly sets a safe small limit.

## Eligibility rule

A triage agent may refine an issue only when all of these are true:

- The issue is in `Backlog` or another explicit intake/triage state.
- The issue is labeled `needs-agent-triage` **or** the caller explicitly scopes this run to that issue.
- The issue is not clearly human-only.
- The issue contains an explicit target signal, or the agent can safely refine without assigning a target.

The strongest target signal is a valid agent code already present in the title.

## Agent-code rule

Do **not** search for, infer, invent, or guess the target agent code.

Allowed:

- Validate an agent code that is already present in the title against the Open Engine routing map.
- Normalize a malformed but explicit title into the canonical form.
- Preserve an explicitly provided target runtime/agent code from the issue body.

Not allowed:

- Choosing an agent code based on task semantics alone.
- Adding a likely agent code because it “seems right”.
- Moving an issue toward execution when the target agent is ambiguous.

Canonical executable title pattern:

```text
[agent instructions][<agent-code>][task] <short outcome>
```

Example normalization:

```text
[vps-hermes-default] Set up 30-minute queue check
```

may become:

```text
[agent instructions][vps-hermes-default][task] Set up 30-minute queue check
```

only if `vps-hermes-default` is already explicit and valid.

## Human-action visibility

A comment alone is not enough when a human must act.

When the triage agent needs human input, it should use visible Plane signals where available:

- Move to `Agent Needs Input` when information or authority is missing.
- Add `requires-human`.
- Assign or mention the responsible human/operator if the runtime has that authority.
- Leave one concrete question or decision request.

When the issue was refined and only needs human review/approval:

- Move to `Agent Review` if permitted.
- Add or keep `requires-human` if approval is required.
- Leave a summary of what changed and what the human should verify.

Use `AGENT BLOCKED` for missing public issue/project information that belongs on the Plane work item.
Use `AGENT HUMAN HOLD` only for private operator-thread requirements such as local/VPS permission, credentials, account authority, or destructive/external approval.

## Trace-first triage rule

Every triage action should make the next safe action more obvious from the Plane issue itself.

Prefer visible, durable traces over private explanations:

- Put missing context, acceptance criteria, boundaries, blocker rules, and output handoff in the issue body.
- Use state and labels as sparse signals, not as decoration.
- Ask one concrete question when blocked.
- Leave a concise triage receipt only when the issue meaningfully changed or needs human action.
- Do not depend on previous chat context that a fresh runtime cannot inspect.

A triaged issue is good when a cold runtime can read the issue and know what to do, what not to do, how to verify, and how to hand off the result.

## Refinement checklist

Use the bundled Open Engine task-writing guide:

- `references/task-writing-guide.md`

The triage skill must remain self-contained so Hermes, Agent Zero, Claude Code, or another runtime can install it without also installing `oe-plane-runner`.

Every refined agent task should include, or explicitly mark as not needed:

1. Requester
2. Desired outcome
3. Sources
4. Acceptance criteria
5. Boundaries
6. Blocker rule
7. Output handoff
8. Target runtime / agent code, when the issue is meant for agent execution

## Safe status policy

Do not move an issue to `Agent Todo` unless all of these are true:

- The title follows the canonical executable pattern.
- The agent code is valid in the routing map.
- The description is complete enough for cold execution.
- Boundaries and blocker rules are explicit.
- The issue is not waiting for human input.
- The caller or local policy explicitly permits promotion to `Agent Todo`.

If promotion is not explicitly allowed, refine the issue and move it to `Agent Review` or leave it in `Backlog` with a clear triage comment.

## Labels

Recommended labels:

- `needs-agent-triage`: issue may be inspected/refined by the triage agent.
- `agent-task`: issue is intended to become executable agent work.
- `agent-instructions`: issue contains or should contain runtime instructions.
- `requires-human`: human input, decision, approval, or authority is needed.

`needs-agent-triage` is an opt-in signal for triage. It is not an execution signal.

A valid canonical title plus readiness criteria are the execution signal.

## Receipt comments

Receipts are system memory, not bureaucracy. Use concise receipt-style comments so humans and agents can audit what happened and decide the next action.

Recommended tokens:

- `AGENT TRIAGE UPDATED`: issue was refined but not necessarily ready.
- `AGENT TASK REFINED`: issue was rewritten into agent-ready shape.
- `AGENT BLOCKED`: public issue/project information is missing.
- `AGENT HUMAN HOLD`: private human/operator authority or credentials are missing.

Avoid posting duplicate receipts on repeated runs. Update only when there is a meaningful change.

## Non-goals

The triage agent must not:

- Execute the task being described.
- Guess the target agent code.
- Create broad subtask trees unless explicitly instructed.
- Change priorities or deadlines unless explicitly instructed.
- Publish, deploy, delete, email, Slack-post, change billing, or change credentials.
- Move ambiguous issues into `Agent Todo`.
