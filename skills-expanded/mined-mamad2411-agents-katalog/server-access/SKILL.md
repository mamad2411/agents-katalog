---
name: server-access
description: Access named servers over SSH using a local credentials file, then run safe inspection commands or delegated checks. Use when the user asks to check a server by name, inspect Docker/container state on a remote machine, verify health over SSH, or use credentials from ~/.systemcraft/ssh/creds.yml.
---

# Server Access

Resolve a named server from `~/.systemcraft/ssh/creds.yml`, connect over SSH, and run the smallest command that answers the question. Prefer delegated execution for remote checks that may take time, and report concise results back to the user.

## Quick start

Credential file path:

```bash
~/.systemcraft/ssh/creds.yml
```

Supported fields per server:

```yaml
servers:
  - name: Server 1
    host: 203.0.113.10
    user: root          # optional; default: current user or ssh config default
    key: ~/.ssh/id_ed25519   # optional; omit to use default SSH key selection
```

For a Docker stopped-container check, run the helper:

```bash
python3 <skill-dir>/scripts/server_access.py \
  --config ~/.systemcraft/ssh/creds.yml \
  docker-stopped \
  --server "Server 1"
```

## Workflow

### 1. Resolve the server

Read `~/.systemcraft/ssh/creds.yml` and locate the requested server by `name`.

Required:
- `name`
- `host`

Optional:
- `user`
- `key`

If `user` is missing, let SSH use its default user resolution.
If `key` is missing, let SSH use its normal key discovery / agent.

If the named server does not exist, stop and ask for the correct name or for the credentials file to be updated.

### 2. Use the helper script instead of hand-rolling SSH

Prefer the bundled helper script for repeatable access patterns:

```bash
python3 <skill-dir>/scripts/server_access.py --config ~/.systemcraft/ssh/creds.yml inspect --server "Server 1" -- "hostname"
```

For the specific Docker health request from this skill, use:

```bash
python3 <skill-dir>/scripts/server_access.py --config ~/.systemcraft/ssh/creds.yml docker-stopped --server "Server 1"
```

### 3. Delegate remote checks when the user asks for asynchronous server inspection

When the user says things like:
- "check Server 1"
- "inspect Server 1"
- "see if any docker containers are stopped"
- "ssh into Server 1 and report back"

spawn a sub-agent/session to do the remote check, then return the result to the user in the main session. The delegated task should:

1. resolve the server from `~/.systemcraft/ssh/creds.yml`
2. run the helper script
3. summarize the result clearly
4. avoid destructive commands unless explicitly requested

### 4. Keep commands read-only by default

Safe defaults:
- `hostname`
- `uptime`
- `docker ps`
- `docker ps -a --filter status=exited`
- `systemctl status <service>` (read-only)
- `df -h`
- `free -h`

Do not restart containers, prune images, edit files, or change server state unless the user explicitly asks.

## Output format

For stopped-container checks, report:
- server name
- host
- whether any stopped containers were found
- container names / status lines if found

Preferred reply shape:

```text
Server: Server 1 (203.0.113.10)
Stopped containers: 2
- api: Exited (1) 3 hours ago
- worker: Exited (137) 25 minutes ago
```

If none are stopped:

```text
Server: Server 1 (203.0.113.10)
Stopped containers: 0
All containers currently look running or absent.
```

## Guardrails

- Treat the credentials file as sensitive; never echo private key contents.
- Only use the `key` field as a file path to an existing private key.
- Prefer `BatchMode=yes` and bounded timeouts for non-interactive SSH.
- Report connection failures plainly: DNS failure, timeout, auth failure, or missing Docker.
- If YAML parsing libraries are unavailable, use JSON instead only if the credentials file is JSON. Do not silently reinterpret malformed YAML.

## References

- `references/creds-example.yml` — example credentials layout.
- `scripts/server_access.py` — deterministic helper for config loading and SSH command execution.
