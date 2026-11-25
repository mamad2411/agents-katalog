---
name: install
description: One-line install for dragoon. Detects supported coding agents (claude-code, codex, cursor, opencode, factory, kiro) and installs the skill pack into each. Multi-host on day one. Use when the user wants to install dragoon, mentions setup, or asks how to add dragoon to their environment. The install script is `./setup` at the repo root.
version: 1.0.0
---

# /install

Sets up dragoon across every supported coding agent on the machine.

## When to use

- The user is installing dragoon for the first time
- The user wants to add dragoon to a new agent
- The user mentions "setup", "install", "configure dragoon"
- The user wants to uninstall dragoon

## Run it

```
# default install (auto-detects all hosts)
./setup

# specific hosts
./setup --hosts claude-code,cursor

# dry run (see what would happen)
./setup --dry-run

# uninstall
./setup --uninstall

# list supported hosts
./setup --list-hosts
```

## What it does

1. Copies the dragoon source pack to `~/.dragoon/`
2. For each detected host, symlinks (or copies if symlinks unsupported) `~/.dragoon` into the host's skills directory:
   - claude-code: `~/.claude/skills/dragoon`
   - codex: `~/.codex/skills/dragoon`
   - cursor: `~/.cursor/skills/dragoon`
   - opencode: `~/.opencode/skills/dragoon`
   - factory: `~/.factory/skills/dragoon`
   - kiro: `~/.kiro/skills/dragoon`
3. Verifies the dragoon binary works

## Requirements

- node 18 or higher
- bash 4 or higher
- one or more supported coding agents installed

That's it. Zero npm dependencies. No registry account needed.

## Updating

Re-run `./setup` from the latest source. The script does an idempotent rsync.

## Uninstall

```
./setup --uninstall
```

Removes the dragoon symlink/copy from every host that has it. Leaves `~/.dragoon/` source untouched (delete it manually if desired).
