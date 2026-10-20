---
name: ssh-remote-exec
description: Execute a command on a remote server via SSH proxy API
---

# SSH Remote Command

Execute a command on a remote server via SSH proxy API

## When to Use

- User wants to ssh exec
- User wants to remote exec
- Keywords: ssh, remote, server, command

## Required Parameters

- **host** (string): SSH host address
- **command** (string): Command to execute

## Output

- **stdout** (string): Command stdout
- **exit_code** (number): Exit code
- **stderr** (string): Command stderr

## Security

- Sandbox level: standard
- Max execution time: 60000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `sanitize` -> 7 steps -> Exit: `ret_ok`, `ret_unsafe`, `ret_fail`
