---
name: deploy-skill
description: Deploy an OpenClaw skill to an agent's workspace, restart gateway if needed, trigger new session, and verify the skill loaded.
---

# Deploy OpenClaw Skill

Deploy and verify an OpenClaw skill is live in an agent's session.

## Usage

`/deploy-skill <skill-name> [agent-id]`

If agent-id not provided, use the default agent.

## Step 1: Locate

```bash
AGENT_ID="${agent-id or default}"
WORKSPACE=$(jq -r ".agents.list[] | select(.id==\"$AGENT_ID\") | .workspace // empty" ~/.openclaw/openclaw.json)
WORKSPACE=$(eval echo "$WORKSPACE")
SKILL_DIR="$WORKSPACE/skills/<skill-name>"
```

Verify the skill exists at `$SKILL_DIR/SKILL.md`.

## Step 2: Validate First

Run validation before deploying:
```bash
bash scripts/validate-skill.sh "$SKILL_DIR"
```

If validation fails, stop and report. Do not deploy broken skills.

## Step 3: Gateway Check

Check if gateway needs restart (only if `openclaw.json` was modified in this session):
```bash
ps aux | grep openclaw-gateway | grep -v grep
```

If config was changed, restart:
```bash
pkill -TERM openclaw-gateway
sleep 3
ps aux | grep openclaw-gateway | grep -v grep && echo "Gateway restarted" || echo "WARNING: Gateway not running"
```

## Step 4: New Session

Tell the user: "Send `/new` to the agent via Telegram/Discord to create a fresh session that loads the new skill."

Wait for confirmation.

## Step 5: Verify

```bash
bash scripts/verify-skill.sh "$AGENT_ID" "<skill-name>"
```

## Step 6: Report

```
Deployment complete: <skill-name>
  Agent: <agent-id>
  Session: <new-session-id or "pending">
  Skill loaded: YES/NO
  Verify: bash scripts/verify-skill.sh "<agent-id>" "<skill-name>"
```
