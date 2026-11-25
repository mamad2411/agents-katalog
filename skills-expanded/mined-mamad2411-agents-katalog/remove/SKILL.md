---
name: remove
description: "Cleanly remove openwolf from cwd (.wolf/, hooks, rules, CLAUDE.md snippet, PM2, registry). Idempotent. TRIGGERS - remove openwolf, uninstall openwolf."
allowed-tools: Read, Bash, Glob, AskUserQuestion
---

# Remove OpenWolf

Cleanly tear down openwolf for the **current project** (cwd at invocation). The npm package ships no `uninstall` command — this skill is the canonical removal path.

> **Self-Evolving Skill**: If openwolf changes its file layout, hook substring, or registry shape — fix this file. Only for real, reproducible drift.

## What gets removed (all from the current project)

1. `.wolf/` directory (data + hook scripts)
2. Hook entries in `.claude/settings.json` whose `command` includes `.wolf/hooks/` — every other hook is preserved verbatim
3. `.claude/rules/openwolf.md`
4. The 225-byte openwolf snippet at the top of `CLAUDE.md` (only that block; rest of file untouched)
5. PM2 daemon `openwolf-$(basename "$PROJECT_ROOT")` (if PM2 is installed)
6. Project entry in `~/.openwolf/registry.json`

## What does NOT get removed

- The global `openwolf` npm binary (separate decision; ask user explicitly).
- Backups under `.wolf/backups/` are removed with `.wolf/` itself — if you need them, copy out first.

## Workflow

### Step 1: Confirm with user

Use AskUserQuestion. List all six removal targets above. Offer:

- `Yes, remove openwolf from this project` (default)
- `Also uninstall the global openwolf binary` (extra step, runs `pnpm remove -g openwolf` || `npm uninstall -g openwolf`)
- `Cancel` — exit cleanly

### Step 2: Capture project basename for PM2 daemon name

```bash
PROJECT_ROOT="$(pwd)"
PROJECT_BASE="$(basename "$PROJECT_ROOT")"
PLUGIN_DIR="$(cc-plugin-root openwolf)"
```

### Step 3: Run the removal script

```bash
bash "$PLUGIN_DIR/scripts/openwolf-remove.sh"
```

The script handles all six targets with `set -e` + step-level error reporting. It is idempotent — every step uses `|| true` for the "already absent" case but reports each action.

### Step 4: Optional — uninstall global binary

If the user chose this in step 1:

```bash
if command -v pnpm >/dev/null; then pnpm remove -g openwolf
elif command -v bun  >/dev/null; then bun remove -g openwolf
else                                 npm uninstall -g openwolf
fi
```

### Step 5: Verify

```bash
[ ! -d "$PROJECT_ROOT/.wolf" ] && echo "  ✓ .wolf/ removed"
[ ! -f "$PROJECT_ROOT/.claude/rules/openwolf.md" ] && echo "  ✓ rules file removed"
grep -q '\.wolf/hooks/' "$PROJECT_ROOT/.claude/settings.json" 2>/dev/null && echo "  ✗ stray .wolf/hooks/ entry in settings.json — investigate" || echo "  ✓ settings.json clean"
grep -q '@\.wolf/OPENWOLF\.md' "$PROJECT_ROOT/CLAUDE.md" 2>/dev/null && echo "  ✗ snippet still in CLAUDE.md — investigate" || echo "  ✓ CLAUDE.md clean"
```

### Step 6: Report

Summarize what was removed and what (if anything) was left behind on purpose.

## Post-Execution Reflection

0. **Locate yourself.** — This SKILL.md path.
1. **Did the removal script error on any step?** — Fix the script (`scripts/openwolf-remove.sh`), not just this skill.
2. **Did openwolf change its CLAUDE.md snippet?** — Update both the script's removal pattern AND the verify regex above.
3. **Did the registry shape change?** — Update the `node` block in the script.

The script `scripts/openwolf-remove.sh` is the load-bearing component — keep it precise.
