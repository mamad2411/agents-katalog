---
name: cmd-system-audit
description: Command — Deep health audit of the installed Claude Code configuration (agents, commands, hooks, memory tiers, logs) — NOT an OS-level audit
---

Comprehensive health audit of the user's Claude Code configuration. Run monthly or after major changes (new plugins installed, hooks enabled, agents added). This is NOT an operating-system audit — it inspects the Claude Code runtime (`.claude/` in the current project, plus installed plugin contents at `~/.claude/plugins/`).

## Scope detection (Step 0)

Before running checks, determine the audit target:

```bash
if [[ -d "agents" && -d "commands" && -d "hooks" && -d "skills" ]]; then
  # Inside a devkit-style plugin source repo. Audit the repo's own structure.
  TARGET_AGENTS="agents"
  TARGET_COMMANDS="commands"
  TARGET_HOOKS="hooks"
  TARGET_SKILLS="skills"
  MODE="plugin-source"
else
  # Audit the user's installed Claude Code config.
  TARGET_AGENTS=".claude/agents"
  TARGET_COMMANDS=".claude/commands"
  TARGET_HOOKS=".claude/hooks"
  TARGET_SKILLS=".claude/skills"
  MODE="installed"
fi
```

Apply this `$TARGET_*` resolution to every check below.

## Checks

### Check 1: Agent Health

- Read every file in `$TARGET_AGENTS/**/*.md`
- Verify each has valid frontmatter (---)
- Verify no TBD/TODO markers
- Check that referenced tools exist in the agent's `tools:` list
- Check agent-memory directories exist for agents that need them

### Check 2: Command Health

- Read every file in `$TARGET_COMMANDS/**/*.md`
- Verify each has valid frontmatter (including required `name:`)
- Check that `allowed-tools` are minimum-necessary (no phantom grants)
- Verify no broken cross-references to other commands

### Check 3: Hook Health

- Verify `.claude/settings.json` is valid JSON (always at project `.claude/`, regardless of MODE): `jq empty .claude/settings.json`.
- Check every hook script referenced in settings.json exists at `$TARGET_HOOKS/`.
- Verify all hook scripts are executable (`ls -la $TARGET_HOOKS/*.sh | awk '$1 !~ /x/ {print}'` — should be empty).
- Dry-test note: a true hook dry-test requires shell-executing each script, which this command does NOT grant (no unscoped `Bash`, no `Bash(bash:*)`). Skip the dry-test or run `bash scripts/test-hooks.sh` separately if you need it.

### Check 4: Memory Tier Health

**Skip in `plugin-source` mode** — the memory tiers being checked belong to the user's installed configuration, not to the plugin source repo. If `MODE=plugin-source`, write "N/A (plugin-source mode)" to all Check 4 lines.

- `.claude/memory.md`: Is it under 100 lines? Is "Now" current?
- `.claude/knowledge-base.md`: Is it under 200 lines? Do all entries have `[Source:]`?
- `.claude/knowledge-nominations.md`: Are there stale nominations (>30 days)?
- `.claude/agent-memory/`: Do directories match existing agents in `$TARGET_AGENTS/`?

### Check 5: Log Health

**Skip in `plugin-source` mode** — log files belong to the user's installed configuration. If `MODE=plugin-source`, write "N/A (plugin-source mode)" to all Check 5 lines.

- `.claude/logs/audit-trail.md`: Is it under 5000 lines?
- `.claude/logs/incident-log.md`: Are there unresolved CRITICAL/HIGH events?
- `.claude/logs/failure-log.md`: Are there recurring patterns?
- `.claude/logs/verdicts.jsonl`: What's the block rate? Any task-type clustering?

### Check 6: Permission & Config Coherence

- `.claude/settings.json` hooks match actual hook files in `$TARGET_HOOKS/`
- No orphaned hook scripts (exist on disk but not referenced in settings.json)
- No missing hook scripts (referenced in settings.json but don't exist)

### Check 7: Cross-File Coherence

In `installed` mode: `CLAUDE.md` references match actual file locations; if `command-index.md` exists, it matches actual commands; no circular dependencies between commands.

In `plugin-source` mode: same checks but against the plugin repo's own `CLAUDE.md` and (if present) `docs/command-index.md`.

### Check 8: Backup & Storage

**Skip in `plugin-source` mode** — backups belong to the installed config. If `MODE=plugin-source`, write "N/A (plugin-source mode)".

- `.claude/backups/`: Is auto-pruning working? (no dirs >7 days old)
- Large files in project root that shouldn't be there?

### Check 9: Via Negativa Sweep

- Are there files/agents/commands that are never used?
- Could any hook be removed without loss?
- Is there duplicated logic between agents?
- Propose removals — simpler is better.

## Grading

| Grade | Criteria                                                           |
| ----- | ------------------------------------------------------------------ |
| A     | All checks pass, no issues                                         |
| B     | Minor issues only (cosmetic, non-blocking)                         |
| C     | Some issues need attention (missing provenance, stale nominations) |
| D     | Structural issues (broken hooks, invalid JSON, missing agents)     |
| F     | Critical failures (security issues, data loss risk)                |

## Output

Report results to the user, and append them to `.claude/logs/audit-trail.md` under:

```markdown
## System Audit — MMDDYY (mode: [plugin-source|installed])

**Grade:** [A-F]
**Checks:** [passed]/9
**Issues:** [bullets with severity]
**Actions:** [corrective actions, if any]
```

Call out the corrective actions needed for any D or F grade issues.
