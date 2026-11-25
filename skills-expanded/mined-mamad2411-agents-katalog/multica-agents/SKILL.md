---
name: multica-agents
description: Discover agents in a Multica workspace and delegate work to them. Covers listing agents, reading their configuration, and the assign-work pattern. Use when the user asks which agents exist, which agent to pick, or wants to hand a task off to a managed agent.
---

# Multica Agents

An **agent** in Multica is a named teammate backed by a coding-agent CLI (Claude Code, Codex, OpenCode, OpenClaw, Hermes, Gemini, Pi, Cursor Agent) running on a registered runtime. Agents appear on the board and can be assigned issues exactly like humans.

## When to use this skill

- The user asks "which agents do we have?" or "who can do X?".
- The user wants to delegate work but does not know valid assignee names.
- Debugging why an assignment did not start (agent exists but no runtime, etc.).
- Listing workspace members (humans + agents) to pick an assignee.

## Creating a new agent

**Agents are created in the web UI, not via CLI.** There is no `multica agent create` command today.

Walk the user through it:

1. Open the app (URL from `multica config show` → `app_url`; Multica Cloud is `https://multica.ai/app`).
2. Go to **Settings → Agents → New Agent**.
3. Pick a **Runtime** (a machine running `multica daemon` with a detected CLI — see `multica-daemon` skill).
4. Pick a **Provider** (Claude Code, Codex, OpenCode, OpenClaw, Hermes, Gemini, Pi, Cursor Agent).
5. Give the agent a **Name** — this is the string that will appear as `--assignee` everywhere.

Once created, the agent is immediately assignable.

## Discovery

```bash
multica agent list                          # Agents in the current workspace
multica agent list --output json

multica workspace list                      # Which workspace am I in?
multica workspace members <workspace-id>    # Humans + agents together
```

Use `agent list` to validate an `--assignee` value before running `multica issue create` or `multica issue assign`.

## Delegation pattern (the main workflow)

```bash
# 1. Pick an agent
AGENT=$(multica agent list --output json | jq -r '.agents[0].name')

# 2. File an issue assigned to them
multica issue create \
  --title "Migrate auth middleware to new session store" \
  --description "..." \
  --priority high \
  --assignee "$AGENT"
```

See the `multica-issues` skill for the full issue command reference. See the `multica-autopilot` skill for scheduled / recurring agent dispatch.

## Which agent to pick?

Multica does not expose capability tags via CLI, so rely on naming conventions and recent history:

```bash
# Past issues this agent has worked on
multica issue list --assignee "<name>" --output json | jq '.issues[] | {id,title,status}'
```

If the workspace has agents named by role (e.g. "Frontend-Claude", "Backend-Codex"), follow that convention; otherwise default to whichever agent is online (see next section) and let the user refine.

## Is the agent actually reachable?

An agent is only useful if *some* runtime hosting its provider is online.

```bash
# Runtimes & which CLIs they can run
multica daemon status --output json         # On the local machine

# Open the web UI → Settings → Runtimes for a cluster-wide view
```

If no runtime advertises the agent's provider, the issue will sit in its status without execution. In that case either:
- Install the agent CLI on a runtime (see `multica-daemon` skill), or
- Reassign the issue to an agent whose provider is available.

## Removing / disabling agents

Also a web-UI operation today. No CLI delete/update command is exposed.

## Gotchas

- Agent names are free-form strings, so case and whitespace matter in `--assignee`. Prefer copying from `multica agent list --output json` over retyping.
- An issue assigned to an agent whose runtime has gone offline will not fail — it waits. Use `multica issue runs <id>` to distinguish "queued" from "executing".
- Two agents can share the same provider but point at different models via `MULTICA_<PROVIDER>_MODEL` on the runtime. Don't assume `name → provider → model` is 1:1:1.
