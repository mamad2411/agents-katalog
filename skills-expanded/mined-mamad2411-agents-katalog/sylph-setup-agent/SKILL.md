---
name: sylph-setup-agent
description: Set up an AI agent by validating her scope, schedule, and delivery channel. Run as `/sylph-setup-agent <agent-name>` or `/sylph-setup-agent all`.
---

# Setup Agent

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Slack | Validate the Chief of Staff delivery channel |

## Core principle: derive from ROLE.md, confirm with the CAO

Each agent already has a `ROLE.md` and `PROMPT.md` in `agents/<name>/`. Read them first. Derive scope, tasks, and cadence from those files. Only ask the CAO to confirm.

## When to use

Run `/sylph-setup-agent <name>` after completing `/sylph-setup` (global setup) and before scheduling any agent. Run it once per agent you want to activate.

## Usage

```
/sylph-setup-agent chief-of-staff
/sylph-setup-agent cmo
/sylph-setup-agent all
```

## Available agents

| Agent | Directory | Default cadence |
|-------|-----------|----------------|
| chief-of-staff | `agents/chief-of-staff/` | Daily 08:00 |
| cmo | `agents/cmo/` | Daily (content), Weekly (planning) |
| product-manager | `agents/product-manager/` | Daily |
| customer-success | `agents/customer-success/` | Weekly (Monday) |
| head-of-data | `agents/head-of-data/` | Daily |
| head-of-sales | `agents/head-of-sales/` | Daily |
| executive-assistant | `agents/executive-assistant/` | Daily |
| brand-designer | `agents/brand-designer/` | On-demand |

---

## How it works

### Step 1: Read the agent definition

1. Read `agents/<name>/ROLE.md` for identity, responsibilities, decision boundaries, and tone
2. Read `agents/<name>/PROMPT.md` for the execution routine
3. Read `CONTEXT.md` for company context

From these files, derive:
- **Scope**: what this agent owns (list of responsibilities from ROLE.md)
- **Tasks**: the concrete steps she runs (from PROMPT.md routine)
- **Default cadence**: how often she runs (from ROLE.md "Working rhythm" or similar)
- **Outputs**: what she produces and where it goes (from ROLE.md "Output rules")
- **Dependencies**: which other agents or tools she needs

### Step 2: Confirm scope and schedule

Present the derived scope to the CAO:

> Here's what **[agent name]** will do:
>
> **Scope:**
> - [responsibility 1 from ROLE.md]
> - [responsibility 2]
> - [responsibility 3]
>
> **She produces:**
> - [output 1 and where it goes]
> - [output 2]
>
> **She escalates to you:**
> - [escalation 1 from decision boundaries]
> - [escalation 2]
>
> **Proposed schedule:** [cadence from ROLE.md, e.g. "Daily at 08:00"]
>
> Anything to add, remove, or change?

Incorporate the CAO's corrections. If the CAO adjusts the schedule, note it.

### Step 3: Chief of Staff only - validate Slack delivery

The Chief of Staff is the only agent that writes to Slack. She delivers her daily briefing as a Slack DM to the CAO.

**Only for chief-of-staff:**

1. **Connect to Slack** - if not already connected, ask the CAO to connect the Slack MCP
2. **Ask the CAO:**

> Where should the Chief of Staff deliver her daily briefing? (Slack DM to you, or a specific channel?)

3. **Validate the channel or DM exists** via Slack MCP
4. **Save the Slack user ID or channel ID** for delivery

For all other agents, skip this step. Other agents write to the repo (`_drafts/`, `_logs/`, `_plans/`) and deliver in chat. They don't post to Slack.

### Step 4: Write agent config

Create or update `agents/<name>/CONFIG.md` with the confirmed settings:

```markdown
---
agent: [name]
status: active
---

# [Agent Name] - Configuration

## Schedule
- Cadence: [daily / weekly / on-demand]
- Time: [HH:MM local time, if scheduled]
- Special: [e.g. "Monday: extended run with weekly planning"]

## Scope
- [responsibility 1]
- [responsibility 2]
- [responsibility 3]

## Escalation rules
- [what she escalates to the CAO]

## Dependencies
- Agents: [other agents she delegates to or receives from]
- Tools: [MCP connectors she needs]
```

For the Chief of Staff only, add the delivery section:

```markdown
## Delivery
- Channel: [Slack DM or channel name]
- Channel ID: [Slack channel/user ID]
- Fallback: chat message (if Slack fails)
```

### Step 5: Schedule the Chief of Staff as a cloud agent

The Chief of Staff should run automatically every morning. After writing her CONFIG.md:

1. **Create a scheduled remote agent** using the scheduling system (Claude Code's `/schedule` or equivalent)
2. **Configure the schedule:**
   - **Trigger**: cron, daily at the CAO's preferred time (default: 08:00 local)
   - **Prompt**: "Run the chief-of-staff routine: load ROLE.md and PROMPT.md from agents/chief-of-staff/, execute the full daily routine, commit the briefing, and deliver via Slack DM."
   - **Monday variant**: the routine automatically branches for weekly planning (this is handled in PROMPT.md, no separate schedule needed)
3. **Verify the schedule is active** and show the CAO a confirmation:

> Chief of Staff is now scheduled to run every day at [HH:MM]. She'll deliver her briefing to [Slack channel/DM]. You can also invoke her on demand with `/chief-of-staff`.

For other agents with daily cadence, inform the CAO they can be scheduled the same way but don't auto-schedule them. Ask:

> Want me to schedule any other agents to run automatically? (e.g., CMO daily, Head of Data daily)

Only schedule additional agents if the CAO explicitly asks.

### Step 6: Test the agent

1. Run a dry test of the agent's routine
2. Verify she can access all required MCP connectors
3. For the Chief of Staff: verify she can post to the configured Slack channel
4. Show the CAO a sample output
5. Capture any feedback in the agent's CONFIG.md

---

## Batch mode: `/sylph-setup-agent all`

When the CAO runs `/sylph-setup-agent all`:

1. List all agents in `agents/` directory
2. For each agent, run Steps 1-4 in sequence
3. For the Chief of Staff, also run Step 5 (schedule)
4. Present a summary table at the end:

```
| Agent | Schedule | Status |
|-------|----------|--------|
| chief-of-staff | Daily 08:00 (scheduled, Slack DM) | Active |
| cmo | Daily (on-demand) | Active |
| product-manager | Daily (on-demand) | Active |
| customer-success | Weekly Monday (on-demand) | Active |
| head-of-data | Daily (on-demand) | Active |
| head-of-sales | Daily (on-demand) | Active |
| executive-assistant | Daily (on-demand) | Active |
| brand-designer | On-demand | Active |
```

5. Ask: "Chief of Staff is scheduled. Want me to schedule any other agents too?"

---

## Adding a new agent

If the CAO asks to set up an agent that doesn't exist yet:

1. Create the directory: `agents/<name>/`
2. Ask the CAO to describe what this agent should do (2-3 sentences)
3. Generate `ROLE.md` following the pattern of existing agents:
   - Identity section
   - Responsibilities (numbered)
   - Decision boundaries (you decide / you escalate)
   - Tone
   - Output rules
4. Generate `PROMPT.md` with the execution routine
5. Create the matching skill in `.claude/skills/<name>/SKILL.md`
6. Add to the skill index in `AGENTS.md`
7. Then proceed with the normal setup flow (Steps 2-6)
