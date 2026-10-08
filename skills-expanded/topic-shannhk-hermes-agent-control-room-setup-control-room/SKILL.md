---
name: setup-control-room
description: Use when bootstrapping an SSH-accessible Ubuntu/Debian VPS with the Agent Control Room template, core agent tooling, and linked control-room skills.
---

# Setup Control Room

Use this skill to turn an SSH-accessible VPS into a tooled Agent Control Room box.

It installs core tools, clones the Agent Control Room template, and links bundled skills.

## Triggers

- "set up control room"
- "bootstrap the vps"
- "install hermes"
- "install agents on the vps"
- "set up the agent box"
- "configure vps for agents"
- `/setup-control-room`

## Inputs

- `SSH_ALIAS`: required unless discoverable from local SSH config.
- `CONTROL_ROOM_PATH`: default `/root/agent-control-room`.
- `CONTROL_ROOM_REPO`: default `https://github.com/shannhk/hermes-agent-control-room.git`.

## Prerequisites

Before running:

1. Confirm `ssh <alias>` works.
2. Confirm target is Ubuntu or Debian.

If SSH does not work, stop and tell the user to create/fix the VPS first.

## Flow

1. Smoke test SSH:

```bash
ssh -o ConnectTimeout=10 <alias> 'echo connected as $(whoami) on $(hostname); lsb_release -a'
```

2. Copy `assets/bootstrap.sh` to the VPS.

3. Run the bootstrap script:

```bash
ssh <alias> '/tmp/bootstrap-control-room.sh' 2>&1 | tee /tmp/control-room-bootstrap.log
```

4. Report installed versions and next steps.

## What The Bootstrap Installs

- base packages: `curl`, `ca-certificates`, `git`, `tmux`, `htop`
- Node.js 22
- Claude Code
- Codex CLI
- Docker
- Hermes Agent best-effort install
- Agent Control Room repo at `/root/agent-control-room`
- symlinks from bundled skills into `~/.claude/skills`

## What This Skill Does Not Do

- It does not handle Claude Code OAuth.
- It does not handle Codex auth.
- It does not complete the Hermes interactive wizard.
- It does not write secrets.
- It does not create specialist containers.

Those are intentionally left for the user or a later agent setup flow.

## Final User Instructions

After bootstrap, tell the user:

```bash
ssh <alias>
claude /login
codex
hermes
cd /root/agent-control-room
cat README.md
```

Also remind them that interactive auth should happen in a real SSH terminal.
