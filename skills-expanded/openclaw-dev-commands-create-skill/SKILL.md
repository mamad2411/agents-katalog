---
name: create-skill
description: Guided workflow to create a new OpenClaw skill from scratch. Walks through requirements, design, implementation, validation, and deployment.
---

# Create OpenClaw Skill

You are guiding the user through creating a new OpenClaw skill. Follow these steps strictly.

## Step 1: Gather Requirements

Ask the user:

1. **Which agent?** — List agents from `~/.openclaw/openclaw.json` via:
   ```bash
   jq -r '.agents.list[] | "\(.id) — workspace: \(.workspace // "shared")"' ~/.openclaw/openclaw.json
   ```

2. **What does the skill do?** — Get a clear description of the capability.

3. **Trigger mode?** — Options:
   - Always-on (behavioral protocol, loaded every session)
   - Model-triggered (auto-activates when task matches description)
   - User-invocable (triggered via `/skill-name` command)
   - Hybrid (always-on + user-invocable)

4. **Dependencies?** — Any required binaries, env vars, or config?

## Step 2: Resolve Workspace

```bash
AGENT_ID="<from step 1>"
WORKSPACE=$(jq -r ".agents.list[] | select(.id==\"$AGENT_ID\") | .workspace // empty" ~/.openclaw/openclaw.json)
if [ -z "$WORKSPACE" ]; then
  echo "WARNING: Agent has no dedicated workspace. Skill will go to shared workspace."
  echo "Consider adding a per-agent workspace first."
else
  WORKSPACE=$(eval echo "$WORKSPACE")
  echo "Workspace: $WORKSPACE"
  ls "$WORKSPACE/skills/" 2>/dev/null || echo "(no existing skills)"
fi
```

If no per-agent workspace exists, warn the user and offer to create one.

## Step 3: Scaffold

Generate the skill name (lowercase kebab-case, under 64 chars). Create the directory and SKILL.md:

```bash
mkdir -p "$WORKSPACE/skills/<skill-name>"
```

Write `SKILL.md` following the format from the `openclaw-skill-development` skill reference. Key rules:
- `name` must match directory name
- `description` must include trigger contexts (this is what makes the skill activate)
- `metadata` must be valid JSON
- Body in imperative voice, under 500 lines
- No README, CHANGELOG, or auxiliary files

## Step 4: Validate

Run the validation script:
```bash
bash scripts/validate-skill.sh "$WORKSPACE/skills/<skill-name>"
```

Fix any failures before proceeding.

## Step 5: Deploy & Verify

1. If `openclaw.json` was modified, restart gateway: `pkill -TERM openclaw-gateway`
2. Tell user to send `/new` to the agent via messaging platform
3. Verify skill loaded in session:
   ```bash
   bash scripts/verify-skill.sh "<agent-id>" "<skill-name>"
   ```

## Step 6: Report

Use this format:
```
Skill created: <skill-name>
  Location: <workspace>/skills/<skill-name>/SKILL.md
  Agent: <agent-id>
  Mode: <always-on | model-triggered | user-invocable | hybrid>
  Status: <loaded in session | pending /new>
  Verify: bash scripts/verify-skill.sh "<agent-id>" "<skill-name>"
```
