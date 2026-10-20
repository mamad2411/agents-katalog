---
name: npm-supply-chain-security
description: Checklist and procedures for auditing npm packages and repo configs for supply chain attacks — covering poisoned install scripts, editor/agent config hijacking, and the keyv worm incident (Aug 2026) as a reference case.
---

# npm Supply Chain Security

## The keyv incident (reference case — Aug 4 2026)

- **150M weekly downloads, 2,234 poisoned versions, 444 packages** affected
- Attack vector: malicious commit `1f79edd` in `jaredwray/keyv` added `setup.mjs` as a `preinstall` script
- The script stole GitHub credentials and wrote to up to 50 branches per repo
- Persistence mechanism: the worm hid across two config files that pointed at each other's scripts:
  - `.vscode/tasks.json` — VS Code task that ran `node .claude/setup.mjs`
  - `.claude/settings.json` — Claude Code SessionStart hook that ran `node .vscode/setup.mjs`
- Neither file alone looked suspicious; the cross-reference made both easy to miss

## Before opening an unfamiliar clone

Run these three checks in order:

```bash
# 1. Read both config files before executing anything
cat .claude/settings.json .vscode/tasks.json

# 2. Block all install scripts
npm ci --ignore-scripts

# 3. Check lockfile — match versions against the published poisoned-package list
#    before rotating any credentials
```

**Important:** some packages genuinely need `preinstall`/`postinstall` scripts
(native bindings, code generation). Don't turn `--ignore-scripts` back off
globally once you've added it. Instead, allow specific packages by name:

```bash
npm config set ignore-scripts true
# then per legitimate package:
npm pkg set scripts.prepare=""  # or use .npmrc per-package allow-list
```

## What to look for in config files

### `.vscode/tasks.json`
Flag any task whose `command` references a `.js`, `.mjs`, or `.cjs` file that:
- is not in the project's own source tree
- is named generically (`setup`, `init`, `bootstrap`, `install`)
- has `"runOn": "folderOpen"` or `"presentation": {"reveal": "never"}`

### `.claude/settings.json`
Flag any `hooks` entry (especially `SessionStart`) that runs a script from:
- `.vscode/` (cross-directory reference is a red flag)
- a path not in version control
- a minified or obfuscated file

### General
- A file that runs another file in a *different* config directory is the keyv persistence pattern
- Rotate all GitHub tokens immediately if a suspicious `preinstall` script ran, even once
- Check all branches the repo touched — the worm wrote to up to 50

## After Claude Code 2.1.222 (Aug 4 2026)

Repo-local `settings.json` can no longer **enable** Remote Control auto-start.
It can still disable it. To enable Remote Control: user-scope config only,
via `/config` in an interactive session or `~/.claude/settings.json`.

This closes the class of attacks where a malicious repo turns on Remote
Control to receive external commands through an agent session.

## Quick reference: safe install patterns

| Goal | Command |
|---|---|
| Install without running any scripts | `npm ci --ignore-scripts` |
| Audit install scripts before running | `npm pack --dry-run` then inspect the tarball |
| See what `preinstall` would run | `cat node_modules/<pkg>/package.json \| jq .scripts` |
| Check a package for known malicious versions | `npm audit` + cross-ref Datadog Security Labs advisories |
