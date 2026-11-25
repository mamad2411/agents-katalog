---
name: operating-tailscale-agent-hosts
# prettier-ignore
description: "Private remote coding-agent hosts over Tailscale. Use when configuring unattended Linux workers, persistent remote agents, or private access to development services."
metadata:
  last_updated: "2026-07-18"
  verified_against: "Tailscale SSH on Linux with systemd, NetworkManager, and tmux"
---

# Operating Tailscale Agent Hosts

Turn an existing Linux machine into a private, persistent coding-agent worker without exposing SSH or development ports to the public internet.

## Core Rules

- Treat Tailscale as the private network path; still configure a service to accept SSH, desktop, or HTTP traffic.
- Prefer Tailscale SSH and narrowly scoped access rules over public SSH or router port forwarding.
- Keep privileged operations and OAuth approval user-driven; never request passwords or expose tokens in logs.
- Verify unattended boot instead of assuming it: networking, Tailscale, sleep policy, encrypted-disk prompts, and services are separate concerns.
- Use tmux for persistence and git worktrees for concurrent mutating agents.
- Bind dev servers to localhost and expose them with Tailscale Serve when possible.
- Transfer configuration selectively; exclude credentials, histories, caches, databases, host keys, and machine-specific trust records by default.

## Workflow

1. Run `scripts/readiness-check.sh` on the proposed host.
2. Follow [setup.md](references/setup.md) to establish unattended private access.
3. Follow [agent-operations.md](references/agent-operations.md) for tmux, worktrees, authentication, and delivery.
4. Use [troubleshooting.md](references/troubleshooting.md) when access only works after login, OAuth fails, or remote services are unreachable.

## Security Boundary

Disabling Tailscale SSH check mode removes periodic browser re-authentication; it does not remove tailnet identity or encryption. Only use an `accept` rule when source identity, destination device, and destination user are narrowly restricted. Never broaden the default self/root rule merely for convenience.
