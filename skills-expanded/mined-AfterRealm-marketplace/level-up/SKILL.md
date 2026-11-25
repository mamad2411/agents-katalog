---
name: level-up
description: >-
  Use this skill when the user wants to manage, inspect, promote, merge, or analyze usage of their Claude Code
  agents. IMPORTANT: Contains scanner scripts that search all .claude/agents/ directories and session history.
  Triggers: "list agents", "show agents", "promote to global", "agent manager", "level up", "manage agents",
  "inspect agent", "merge agents", "combine agents", "agent stats", "agent usage", "which agents are unused",
  "most used agents", or follow-ups like "move that one to global" when agents are discussed.
  Do NOT trigger for: running agents (/agents), debugging agent errors, or general questions.
  Note: Claude handles agent CREATION natively — no skill needed. If user says "create an agent",
  respond directly without invoking this skill.
license: MIT
compatibility: Requires Python 3.x for scanner scripts
metadata:
  author: AfterRealm
  version: "1.1.2"
---

# Level Up — Agent Management Skill

Inspect, promote, merge, and analyze usage of your Claude Code agents across projects and global scope.

## Glossary

- **"Ask as chat"** = output a text question in your reply. **Do NOT use AskUserQuestion** — that burns context on every picker. Plain chat messages keep follow-ups lightweight.
- **Subagent** = heavy work handler, spawned via the Agent tool. Keeps big payloads out of main context.
- **Resolved path** = absolute path to a script, computed from `SKILL_DIR`. Pass these to subagents — they can't resolve `SKILL_DIR` themselves.

## Scripts

Resolve these paths once before any action:
- Scanner: `SKILL_DIR/scripts/scan_agents.py`
- Stats: `SKILL_DIR/scripts/agent_stats.py`

## Flow

### Step 1: Scan (subagent)

Always start here. Spawn a subagent to scan all agents:

```
Agent(description: "Scan agents", prompt: "Run: python \"<SCANNER_PATH>\" --action list
Parse the JSON. Return ONLY a compact summary:
GLOBAL: agent1, agent2
PROJECT_NAME (count): agent1 (model), agent2 (model)
One line per project, agents comma-separated. Nothing else.")
```

Present the results directly in the chat:

```
**GLOBAL** — agent1, agent2
**Ark Claude** (14) — Accountant (sonnet), BP Architect (sonnet), ...
**Vox Memori** (4) — Architect (opus), Neurologist (opus), ...
```

If zero agents found, tell the user and stop.

### Step 2: Action Menu (the ONLY AskUserQuestion in the whole skill)

Immediately after presenting the scan results, show ONE AskUserQuestion with exactly 4 options:

1. **Inspect** — View the full source of an agent
2. **Promote & Adapt** — Copy or adapt an agent to a different scope
3. **Merge** — Combine two agents into one
4. **Stats** — Agent usage analytics from session data

The user picks one. No more pickers after this — everything else is chat or subagent.

### Step 3: Execute the action

#### If Inspect

**Ask as chat:** "Which agent? (name and project if ambiguous)"

User replies. Resolve the agent — if the name is unique across all projects, use it directly. If ambiguous, ask once as chat to clarify.

Then spawn a subagent:
```
Agent(description: "Inspect agent", prompt: "Run: python \"<SCANNER_PATH>\" --action inspect --name \"NAME\" --project \"PROJECT\"
Show the full agent markdown content. Format readably.")
```

#### If Promote & Adapt

**Ask as chat:** "Which agent do you want to promote? (name and project)"

User replies. Resolve the agent. **Ask as chat:** "Direct copy to global, or adapt it first to remove project-specific references?"

**Direct copy** → subagent runs `--action promote --name NAME --project PROJECT`.

**Adapt** → subagent inspects the agent, rewrites to remove project-specific references (hardcoded paths, project names, data references), and returns the adapted content. Show the result. **Ask as chat:** "Save this, or edit first?" Write to `~/.claude/agents/NAME.md` when approved.

#### If Merge

**Ask as chat:** "Which two agents do you want to merge? (name + project for each)"

Spawn a subagent to do the full merge:
```
Agent(description: "Merge agents", prompt: "Run: python \"<SCANNER_PATH>\" --action merge-prep --name \"NAME1\" --project \"P1\" --name2 \"NAME2\" --project2 \"P2\"
Parse the JSON. Build a complete merged agent:
- Frontmatter: use the more capable model, union of tools, combine descriptions
- Include ALL sections from both agents
- Common sections: concatenate both under the same heading with clear attribution
- Unique sections: include as-is
Return the complete merged agent markdown, ready to save.")
```

Show the merged result. **Ask as chat:** "Save this? What name and scope (global or a specific project)?" Write the file when approved, verify with scanner.

If the user wants section-by-section control instead of the smart merge, read `SKILL_DIR/references/flows.md` for the granular merge flow.

#### If Stats

Spawn a subagent immediately — no user input needed:
```
Agent(description: "Agent usage stats", prompt: "Run: python \"<STATS_PATH>\" --action summary --since 7d
Also run: python \"<STATS_PATH>\" --action unused --since all
Parse both JSON outputs. Format a readable report:
- Total invocations and sessions scanned
- Weekly budget utilization if weekly_usage field is present
- Table: agent type, invocations, avg turns, avg work tokens, avg total tokens, projects
- List of unused agents (exist on disk, never invoked)
- Bullet the caveats from the 'caveats' array
- Note unmatched_invocations count if > 0
Keep it compact.")
```

Present the results. Then **ask as chat:**

> "Want optimization suggestions for any of these agents? I can audit an agent's definition against its usage patterns and suggest ways to reduce turns, cache growth, or redundant work. Note: each audit spawns a subagent (~10-15k work tokens, may add ~1-2% to weekly usage)."

If the user says yes and names one or more agents, spawn a single audit subagent per agent (or batch if they list multiple):

```
Agent(description: "Agent optimization audit", prompt: "For each of these agents, run: python \"<SCANNER_PATH>\" --action inspect --name \"AGENT_NAME\" --project \"PROJECT\"
Read the full agent definition. Then consider its usage stats:
- Invocations: N
- Avg turns per invocation: T
- Avg work tokens: W
- Avg total tokens: TT
- Projects used in: [list]

Audit each agent for optimization opportunities:
1. High turn count → look for redundant tool calls, sequential reads that could be parallel, missing scope constraints
2. High cache/total ratio → reduce per-turn re-reading with targeted reads and 'stop after X' instructions
3. Vague instructions → add specificity so the agent doesn't explore
4. Missing structure → add a checklist or output template to constrain scope
5. Unused sections or bloat in the definition itself

Return: for each agent, a concrete list of 3-5 optimization suggestions with BEFORE/AFTER edits to the .md file. Do NOT modify files — suggest only.")
```

Present the suggestions. **Ask as chat:** "Want me to apply any of these? Audit another agent? Or done?" If the user wants to audit more, inform them of the current weekly utilization before proceeding. If they want fixes applied, edit the agent file directly.

For extended Stats flows (drill-down into a specific agent via `--action detail`, changing the time period via `--since 30d/all`, or the versioning commands `scan_agents.py` still supports), read `SKILL_DIR/references/flows.md`.

## Rules

These are non-negotiable:

1. **One AskUserQuestion per invocation.** The action menu. That's it. Every other interaction is chat.
2. **Heavy work goes to subagents.** Scanning, inspecting, merging, stats, audits — never do these in the main thread.
3. **Pass resolved absolute paths.** Subagents cannot resolve `SKILL_DIR`. Store the two script paths once, pass them into every subagent prompt.
4. **Never delete an agent without explicit user confirmation.**
5. **Check for name collisions before promoting.** The scanner already does this — don't skip the check.
6. **Surface the weekly budget when relevant.** Especially before spawning multiple audit subagents. Users should see the cost at the decision point.

## Scopes

- **Global agents:** `~/.claude/agents/` — available in every project
- **Project agents:** `<project>/.claude/agents/` — only work in that project
- Agent files are `.md` with YAML frontmatter

## Version Notes

See `CHANGELOG.md` in the skill root for release history.
