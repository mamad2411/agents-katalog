---
name: create-vps
description: Use when creating a fresh Hetzner Cloud VPS with an SSH alias, local project folder, provisioning script, destroy script, and optional handoff into setup-control-room.
---

# Create VPS

Use this skill to provision a fresh Hetzner Cloud VPS from a local machine.

This skill creates a server, SSH key, local SSH alias, and project folder. It can optionally chain into `setup-control-room` after the server is reachable.

## Triggers

Standalone:

- "create a vps"
- "new vps"
- "provision a server"
- "create a hetzner vps"
- "set up a new hetzner box"
- `/create-vps`

Chained into `setup-control-room`:

- "create an agent vps"
- "create a fully loaded vps"
- "create a vps and bootstrap it"
- "new agent box"
- `/create-agent-vps`

## Inputs

Required:

- `PROJECT_NAME`: collected from the user.

Derived from `PROJECT_NAME`:

```text
SERVER_NAME
SSH_ALIAS
SSH_KEY_FILE
SSH_KEY_NAME
```

Defaults:

```text
SERVER_TYPE=cx23
SERVER_LOCATION=hel1
SERVER_IMAGE=ubuntu-24.04
```

Server type and location should be selected from live `hcloud` output after the user adds the token to `.env`.

## Prerequisites

Check first:

1. `hcloud` CLI is installed.
2. User has a Hetzner Cloud account.

If `hcloud` is missing, stop and give install instructions.

## Security Rule

Never accept the Hetzner token in chat.

If the user pastes it, tell them to revoke it and create a new one.

The token must be pasted directly into the local `.env` file by the user.

## Flow

1. Ask for project name.
2. Create local project folder.
3. Write `.env`, `.gitignore`, `scripts/provision.sh`, and `scripts/destroy.sh`.
4. Tell the user how to create a Hetzner API token.
5. Tell the user to paste it after `HCLOUD_TOKEN=` in `.env`.
6. After confirmation, source `.env` and query:

```bash
hcloud server-type list
hcloud location list
```

7. Ask for server type and location using live options.
8. Write selected values into `.env`.
9. Run `scripts/provision.sh`.
10. Verify:

```bash
ssh <alias> 'echo connected as $(whoami) on $(hostname); uname -a'
```

11. If the original trigger asked for an agent VPS, invoke `setup-control-room` with `SSH_ALIAS`.
12. Otherwise ask whether the user wants to bootstrap the Agent Control Room.

## Outputs

- Working `ssh <alias>` connection.
- Local project folder with idempotent scripts.
- Hetzner server visible in `hcloud server list`.
- SSH keypair.
- SSH config entry.
- Optional handoff into `setup-control-room`.

## Idempotency

`provision.sh` should be safe to rerun:

- Skip key generation if key exists.
- Skip SSH key upload if key exists in Hetzner.
- Skip server creation if server exists.
- Update `.env` with current IP.
- Update SSH config block in place.

## Files

```text
create-vps/
  SKILL.md
  assets/
    env.template
    gitignore.template
    provision.sh
    destroy.sh
  references/
    env-guide.md
    server-types.md
    troubleshooting.md
    daily-use.md
```
