---
name: install
description: "Install openwolf npm and run `openwolf init` in cwd. TRIGGERS - install openwolf, openwolf init, set up openwolf."
allowed-tools: Read, Bash, Glob, AskUserQuestion
---

# Install OpenWolf

Install the third-party `openwolf` npm package and initialize it in the **current project** (cwd at invocation). The plugin itself contains no openwolf code — it shells out to the published binary.

> **Self-Evolving Skill**: If install steps drift (renamed flags, new prerequisites, npm vs pnpm churn), fix this file. Only update for real, reproducible issues.

## Prerequisites

| Component    | Required | Check                                                                          |
| ------------ | -------- | ------------------------------------------------------------------------------ |
| Node.js 20+  | Yes      | `node --version`                                                               |
| npm/pnpm/bun | One      | `command -v npm pnpm bun`                                                      |
| PM2          | Optional | `command -v pm2` (for the auto-started daemon — degrades gracefully if absent) |

## When NOT to run this

Confirm with the user before initializing in any of these:

- The cc-skills marketplace repo itself (this repo) — anatomy.md would be noise across 197 skills.
- Tiny one-shot scripts or directories without a clear "project" boundary.
- Any project where `.claude/settings.json` is auto-managed by another tool that does not preserve foreign hook entries.

## Workflow

### Step 1: Preflight + confirm

```bash
node --version || { echo "FAIL: Node.js 20+ required"; exit 1; }
PROJECT_ROOT="$(pwd)"
echo "Will install openwolf globally and initialize in: $PROJECT_ROOT"
[ -d "$PROJECT_ROOT/.wolf" ] && echo "NOTE: .wolf/ already exists — init will run in upgrade mode (preserves user data)."
```

If `CLAUDE.md` already exists in the project, warn the user that openwolf will **prepend** a 225-byte snippet to it. Use AskUserQuestion if the project's `CLAUDE.md` has structured top-of-file metadata that the user might not want disturbed.

### Step 2: Install the global binary

Pick the first available package manager:

```bash
if command -v pnpm >/dev/null; then pnpm add -g openwolf
elif command -v bun  >/dev/null; then bun add -g openwolf
else                                 npm install -g openwolf
fi
openwolf --version || { echo "FAIL: openwolf binary not on PATH after install"; exit 1; }
```

### Step 3: Initialize in the current project

```bash
cd "$PROJECT_ROOT" && openwolf init
```

This creates `.wolf/`, merges 6 hooks into `.claude/settings.json`, writes `.claude/rules/openwolf.md`, prepends a snippet to `CLAUDE.md`, registers in `~/.openwolf/registry.json`, and (if PM2 is installed) starts daemon `openwolf-$(basename "$PROJECT_ROOT")`.

### Step 4: Verify

```bash
openwolf status
```

Confirm: `.wolf/` files present, hook scripts present, hooks registered, anatomy file count matches expectations.

### Step 5: Surface what was added

Tell the user concisely:

- `.wolf/` directory at `$PROJECT_ROOT/.wolf/` (data the user owns)
- 6 hooks merged into `$PROJECT_ROOT/.claude/settings.json`
- Snippet prepended to `$PROJECT_ROOT/CLAUDE.md`
- Rules file at `$PROJECT_ROOT/.claude/rules/openwolf.md`
- Registry entry at `~/.openwolf/registry.json`
- Daemon: whatever `openwolf status` reported

To remove cleanly later: `/openwolf:remove`.

## Post-Execution Reflection

After this skill completes, before closing the task:

0. **Locate yourself.** — This SKILL.md path before editing.
1. **What failed?** — Fix the failing step here, not in a separate doc.
2. **Did the package manager preference order misfire?** — Reorder pnpm/bun/npm if needed.
3. **Did `openwolf init` mutate something unexpected?** — Document under "When NOT to run this".

Do NOT defer. The next invocation inherits whatever you leave behind.
