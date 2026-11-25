---
name: looks-expensive-update
version: 1.0.0
description: |
  Updates the /looks-expensive design skill to the latest version published on GitHub.
  Auto-detects Claude Code, Cursor, and Codex, updates the skill in each tool it finds,
  and shows the old → new version per tool.
  Trigger on: "update looks-expensive", "looks-expensive update",
  "upgrade looks-expensive", "check for looks-expensive updates",
  "is there a new version of looks-expensive".
user-invocable: true
allowed-tools:
  - Bash
  - Read
triggers:
  - update looks-expensive
  - looks-expensive update
  - looks-expensive-update
  - upgrade looks-expensive
  - check for looks-expensive updates
---

# Update /looks-expensive

This skill updates the `/looks-expensive` design skill to the latest version published at github.com/TuahaJawaid/looks-expensive.

## What it does

Runs the official installer script, which:

1. Downloads the latest release from GitHub
2. Auto-detects which AI tools the user has (Claude Code, Cursor, Codex)
3. Updates the skill in each detected tool
4. Shows the old → new version per tool

The installer is idempotent — running it when already on the latest version does a clean reinstall, not an error.

## How to run

### Step 1 — Show the user what you're about to do

Before running anything, tell the user:
- You're going to run the official installer from `raw.githubusercontent.com/TuahaJawaid/looks-expensive/main/install.sh`
- It will update `/looks-expensive` AND this `/looks-expensive-update` skill in every detected AI tool
- They'll need to start a new session of their tool for the update to take effect

### Step 2 — Optionally check current version first

If the user wants to know what version they currently have before updating:

```bash
grep "^version:" ~/.claude/skills/looks-expensive/SKILL.md 2>/dev/null \
  | head -1 \
  | sed -E 's/version:[[:space:]]*//; s/[[:space:]]*$//'
```

(Adjust path to `~/.cursor/skills-cursor/looks-expensive/SKILL.md` or `~/.codex/skills/looks-expensive/SKILL.md` for Cursor or Codex.)

### Step 3 — Run the update

```bash
curl -fsSL https://raw.githubusercontent.com/TuahaJawaid/looks-expensive/main/install.sh | bash
```

### Step 4 — Show the output

The installer prints which tools were updated and from which version to which version. Relay this to the user verbatim — they want to see the actual version numbers.

## After updating

The user must start a NEW session of their AI tool (Claude Code, Cursor, or Codex) for the updated skill to load. Existing sessions have the old skill loaded in memory. Tell them this explicitly — it's the #1 source of "I updated but nothing changed" confusion.

## If the update fails

Network errors, missing curl/wget, or other transient failures: suggest the manual fallback.

```bash
git clone https://github.com/TuahaJawaid/looks-expensive.git
cd looks-expensive
bash install.sh
```

If even that fails, the user can manually copy the skill folders:

```bash
# Claude Code
cp -r skills/looks-expensive ~/.claude/skills/looks-expensive
cp -r skills/looks-expensive-update ~/.claude/skills/looks-expensive-update

# Cursor
cp -r skills/looks-expensive ~/.cursor/skills-cursor/looks-expensive
cp -r skills/looks-expensive-update ~/.cursor/skills-cursor/looks-expensive-update

# Codex
cp -r skills/looks-expensive ~/.codex/skills/looks-expensive
cp -r skills/looks-expensive-update ~/.codex/skills/looks-expensive-update
```

## Reading the changelog

After updating, the user can see what changed:

```bash
curl -fsSL https://raw.githubusercontent.com/TuahaJawaid/looks-expensive/main/CHANGELOG.md | less
```

Or visit https://github.com/TuahaJawaid/looks-expensive/blob/main/CHANGELOG.md in a browser.

## Rules

- ALWAYS show the user the command before running it. Network commands deserve consent.
- ALWAYS surface the installer output. The version numbers are the point — the user wants to see "v1.0.0 → v1.1.0" not just "updated successfully."
- ALWAYS remind the user they need a new session for the update to take effect.
- NEVER claim a version that wasn't actually printed by the installer. Read the installer output and quote it back.
- This skill does not run `/looks-expensive` itself. It only updates it. The user runs `/looks-expensive` afterward.
