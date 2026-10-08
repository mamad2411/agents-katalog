---
name: pith-uninstall
description: >
  Uninstall Pith from Claude Code. Removes hooks, slash commands, and
  cleans pith entries from settings.json. Preserves ~/.pith/state.json
  (token history) unless user explicitly asks to wipe all data.
---

## When to use

- User runs `/pith uninstall`
- User asks "remove pith", "uninstall pith", or "clean up pith"

---

## Steps

### 1 — Confirm intent

Before running, ask once:

```
This will remove:
  • ~/.claude/hooks/pith/   (all hook scripts)
  • ~/.claude/commands/pith.md, budget.md, focus.md
  • pith entries in ~/.claude/settings.json

Your project wikis (wiki/) and token history (~/.pith/) are NOT deleted.

Proceed? (yes / no)
```

If user says no, stop. If yes, continue.

### 2 — Run the uninstall script

Locate the pith directory (same logic as pith-install step 1), then:

```bash
bash "<pith_dir>/uninstall.sh"
```

Stream the output so user sees each item removed.

### 3 — Verify clean

```bash
# Hooks gone
ls ~/.claude/hooks/pith/ 2>/dev/null && echo "STILL EXISTS" || echo "removed ok"

# Slash commands gone
ls ~/.claude/commands/ | grep -E "pith|budget|focus" 2>/dev/null && echo "STILL EXISTS" || echo "removed ok"

# Settings clean
node -e "const s=require(require('os').homedir()+'/.claude/settings.json'); const h=JSON.stringify(s.hooks||''); console.log(h.includes('pith')?'pith still in hooks':'hooks clean'); console.log(s.statusLine?'statusLine still set':'statusLine clean')"
```

### 4 — Optionally wipe all data

If the user said "remove everything" or "wipe all data", also run:

```bash
rm -rf ~/.pith
rm -f ~/.config/pith/config.json
```

Warn first: "This deletes your lifetime token savings history. Are you sure?"

### 5 — Confirm to user

```
Pith uninstalled.

Removed:
  ✓ hooks (session-start, post-tool-use, prompt-submit, stop)
  ✓ slash commands (/pith, /budget, /focus)
  ✓ settings.json entries

Preserved:
  • wiki/ directories in your projects
  • ~/.pith/state.json  (token history)

To reinstall: /pith install
```

---

## Error handling

| Error | Fix |
|-------|-----|
| `uninstall.sh` not found | Run the node cleanup inline: remove `~/.claude/hooks/pith`, delete command files, patch settings manually |
| `settings.json` malformed | Show the file, offer to remove pith keys manually |
| Hook files already missing | Skip silently, still clean settings.json |

One-shot. Does not persist.
