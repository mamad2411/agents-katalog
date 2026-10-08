---
name: pith-install
description: >
  Install Pith into Claude Code. Copies hooks, patches settings.json,
  registers slash commands (/pith, /budget, /focus), and records the
  plugin root so hooks can resolve paths.
---

## When to use

- User runs `/pith install`
- User asks "how do I install pith" or "set up pith"

---

## Steps

### 1 — Locate the pith directory

Find where pith lives. Try in order:
1. `~/.claude/plugins/cache/pith/pith/*/` (installed via plugin marketplace)
2. The directory containing this SKILL.md file (cloned from GitHub)
3. Ask the user: "Where did you clone pith to?"

### 2 — Run the install script

```bash
bash "<pith_dir>/install.sh"
```

Stream the output to the user so they can see each step tick off.

### 3 — Verify success

After the script completes, confirm all five things installed:

```bash
# Hooks copied
ls ~/.claude/hooks/pith/

# Slash commands registered
ls ~/.claude/commands/ | grep -E "pith|budget|focus"

# Settings patched
node -e "const s=require(require('os').homedir()+'/.claude/settings.json'); console.log(JSON.stringify({hooks:Object.keys(s.hooks||{}), statusLine:!!s.statusLine},null,2))"

# Plugin root recorded
cat ~/.config/pith/config.json

# State dir exists
ls ~/.pith/
```

If any check fails, show the specific error and offer to re-run just that step.

### 4 — Confirm to user

Show this summary:

```
Pith installed.

Active automatically (zero config):
  ✓ Tool output compression
  ✓ Token meter in statusline  [PITH 0k/200k]
  ✓ Auto-compact at 70% context

On-demand:
  /pith lean|ultra|precise   output compression
  /pith debug|arch|plan      structured formats
  /pith commit               commit message
  /pith wiki                 project knowledge base
  /pith status               token usage
  /pith tour                 interactive walkthrough
  /budget <n>                hard token ceiling
  /focus <file>              load relevant sections only

Restart Claude Code to activate hooks.
```

---

## Error handling

| Error | Fix |
|-------|-----|
| `node: command not found` | Tell user to install Node.js ≥18 |
| `settings.json` parse error | Show the broken JSON, offer to reset to `{}` |
| Permission denied on hooks dir | Run `mkdir -p ~/.claude/hooks/pith` first |
| Plugin root not found | Ask user to re-clone: `git clone https://github.com/abhisekjha/pith` |

One-shot. Does not persist.
