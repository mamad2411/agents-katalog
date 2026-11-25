---
name: create-heartbeat
description: "Create a new heartbeat (proactive agent scheduled with a decision prompt) for EvoNexus. Guides the user through picking an agent, setting interval, wake triggers, and the decision prompt that governs when the agent acts. Writes to config/heartbeats.yaml with pydantic validation. Use when the user says 'create a heartbeat', 'make X agent proactive', 'wake Y every 4h', 'automate X to check state and act', or wants to turn a manual state check into a scheduled protocol-run."
---

# Create Heartbeat

> **Auth note:** For any API calls use `from dashboard.backend.sdk_client import evo` — auto-handles URL + auth, no Bearer token needed in code.

Create a new heartbeat — a proactive agent that wakes on a schedule, runs the 9-step protocol, and decides whether to act.

## When to use

Use heartbeats when:
- The agent should **check state and conditionally act** (e.g., Atlas checks Linear for blockers)
- You want **no work when state is calm** (vs routines which always run)
- The same topic is **picked from an inbox** of tickets (heartbeats query tickets in step 3)

Don't use heartbeats for:
- Deterministic scheduled jobs (use a routine)
- One-off actions (use a skill or ticket)

## Step 1: Understand the trigger

Ask the user:
1. **Which agent?** List agents from `.claude/agents/*.md`. Suggest by domain:
   - `atlas-project` — project tracking (Linear, GitHub)
   - `flux-finance` — payments, billing
   - `zara-cs` — support queue
   - `pulse-community` — community sentiment
   - `pixel-social-media` — scheduled posting
2. **How often?** Interval in minutes / hours. Min 60s. Typical: 2h, 4h, 6h.
3. **What state to check?** This becomes the `decision_prompt`.
4. **Link to a goal?** Optional `goal_id` for context injection. Skip if no goal fits.

## Step 2: Compose the decision prompt

The decision_prompt is injected into the agent's context and asks the agent:

> "Given the current state of [X], should you act? If yes, do the work and report. If no, explain briefly and skip."

Good decision prompts are specific:

✅ "Check Linear for issues in `In Progress` assigned to an unresponsive person (> 48h inactive) or blocked > 24h. If any, create action items and notify Davidson. Otherwise skip."

❌ "Check stuff" (too vague — will always act or always skip randomly)

## Step 3: Pick wake triggers

Default: `interval` + `manual`. Optional:
- `new_task` — wake when a ticket is assigned
- `mention` — wake when `@<agent-slug>` appears in a comment
- `approval_decision` — wake when an approval affects this agent

30s debounce prevents multiple triggers coalescing into multiple runs.

## Step 4: Required secrets (optional)

If the decision/work requires API keys (Stripe, Linear, etc.), list them as `required_secrets`. They'll be validated at startup (presence, not value).

## Step 5: Write to YAML

Append the new heartbeat to `config/heartbeats.yaml`:

```yaml
heartbeats:
  - id: <agent-slug>-<interval>h
    agent: <agent-slug>
    interval_seconds: <N>
    max_turns: 10
    timeout_seconds: 600
    lock_timeout_seconds: 1800
    wake_triggers: [interval, manual]
    enabled: false            # opt-in — user enables after testing
    goal_id: null
    required_secrets: []
    decision_prompt: |
      <the prompt from step 2>
```

Validate with `make heartbeat-lint` before suggesting the user enables.

## Step 6: Guide the user

After writing:

1. Run `make heartbeat-lint` to validate
2. Test manually: UI `/scheduler` → Heartbeats tab → Run Now on this heartbeat
3. Review the run in `workspace/ADWs/logs/heartbeats/<id>-<date>.jsonl`
4. If the decision quality is right, flip `enabled: true` and restart dashboard

## Notes

- Source of truth is the YAML. UI CRUD rewrites it atomically (temp file + rename).
- Delete a heartbeat via `/scheduler` → Heartbeats → Delete, or remove the entry from YAML and restart.
- Heartbeat cost appears in `/costs` once runs start generating `heartbeat_runs` rows.

Related: `.claude/rules/heartbeats.md`, `.claude/rules/tickets.md` (inbox), `.claude/rules/goals.md` (context).
