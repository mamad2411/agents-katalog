---
name: orchestrator-status
format: procedural
description: "Returns current orchestrator state: active SDD changes, loaded skills, configuration source, classification enabled/disabled"
---

# orchestrator-status

> Returns a structured snapshot of the SDD Orchestrator's current state: whether intent classification is enabled, active SDD changes in progress, and skills registered in CLAUDE.md.

**Triggers**: User invokes `/orchestrator-status`

## Process

### Step 1 — Read CLAUDE.md

Read the project's `CLAUDE.md` (located at the project root, e.g., `C:/Users/juanp/claude-config/CLAUDE.md` or the current working directory's `CLAUDE.md`).

Extract:
- Whether `intent_classification: disabled` appears under any `## Always-On Orchestrator — Override` section. If absent, `classification_enabled = true`.
- Count the numbered items under `## Unbreakable Rules` (each `### N.` or numbered list item = 1 rule).
- The file path used as `configuration_source`.

### Step 2 — Scan active SDD changes

List directories under `openspec/changes/` (non-recursively). Exclude `archive/`.

For each non-archived directory:
- Record `name` (directory basename)
- Identify `status`:
  - If `verify-report.md` present → `"verified"`
  - Else if `tasks.md` present → `"in-progress"`
  - Else if `design.md` present → `"designing"`
  - Else if `proposal.md` present → `"proposed"`
  - Else → `"unknown"`
- List artifact filenames present (proposal.md, exploration.md, design.md, specs/, tasks.md, verify-report.md)

### Step 3 — Extract loaded skills

From CLAUDE.md's `## Skills Registry` section, collect all lines matching `` `~/.claude/skills/<name>/SKILL.md` `` pattern. Extract `<name>` values.

Count total as `skills_registry_count`.

Identify orchestrator + SDD phase skills specifically:
- Core: `sdd-ff`, `sdd-new`, `sdd-status`, `orchestrator-status`
- Phases: `sdd-explore`, `sdd-propose`, `sdd-spec`, `sdd-design`, `sdd-tasks`, `sdd-apply`, `sdd-verify`, `sdd-archive`

### Step 4 — Build JSON output

Emit a fenced JSON code block:

```json
{
  "orchestrator_state": {
    "classification_enabled": <true|false>,
    "unbreakable_rules_count": <N>,
    "session_start": "<ISO 8601 timestamp>",
    "configuration_source": "<absolute path to CLAUDE.md>"
  },
  "active_sdd_changes": [
    {
      "name": "<change-dir-name>",
      "status": "<proposed|designing|in-progress|verified|unknown>",
      "artifacts": ["<filename>", ...]
    }
  ],
  "loaded_orchestrator_skills": [
    "<skill-name>",
    ...
  ],
  "skills_registry_count": <N>
}
```

### Step 5 — Write prose interpretation

After the JSON block, output a prose section titled `## Interpretation`:

```
Orchestrator Status (<date> UTC)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Orchestrator: ENABLED  (or DISABLED if classification_enabled is false)
  Rules loaded: <N> unbreakable rules from CLAUDE.md
  Configuration: <configuration_source>

Active SDD Changes: <count>
  (list each: • <name> (<status>) — Artifacts: <comma-separated artifact list>)
  (if zero: "None — no active changes found in openspec/changes/")

Loaded Skills: <orchestrator-skill-count> orchestrator + SDD phase skills
  Core: <list core skill names>
  Phases: <list phase skill names>
  Project catalog: <skills_registry_count> total skills

Ready to accept: /sdd-ff <slug> | /sdd-explore <topic> | /sdd-new <change>
```

## Rules

1. **Read-only**: This skill MUST NOT modify any files. It is a pure read/inspect operation.
2. **No external calls**: Do not make network requests or invoke shell commands that mutate state.
3. **Classification check**: Always check for the Override section in CLAUDE.md before defaulting `classification_enabled` to `true`.
4. **Exclude archive/**: Never count archived changes as active. Only list entries directly under `openspec/changes/` that are NOT under `openspec/changes/archive/`.
5. **Format contract**: Output MUST contain the JSON code block first, then the `## Interpretation` prose section. Do not reverse the order.
6. **Graceful fallback**: If `openspec/changes/` does not exist, set `active_sdd_changes: []`. If `## Skills Registry` section is absent from CLAUDE.md, set `skills_registry_count: 0` and `loaded_orchestrator_skills: []`.
