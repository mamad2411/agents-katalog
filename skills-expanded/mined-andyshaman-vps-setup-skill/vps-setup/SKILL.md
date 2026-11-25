---
name: vps-setup
description: Use this skill to set up, harden, or audit a Linux server (VPS, dedicated, or cloud instance). Triggers - configuring a fresh server from any provider (Hetzner, DigitalOcean, Vultr, Linode, AWS, OVH, Timeweb, Beget, etc.), installing UFW firewall, setting up fail2ban, disabling root/password SSH login, kernel sysctl hardening, creating sudo user with SSH keys, auditing an existing server for SSH brute-force or misconfiguration. Russian triggers - "купил VPS/впску/сервер", "настроить сервер", "захардить", "поднять ufw/fail2ban", "защитить сервер", "свежий дебиан/убунту в облаке". English triggers - "got new server", "secure my VPS", "harden Ubuntu/Debian", "lock down SSH", "server hardening checklist", "audit server security". Beginner-safe - password lockout deferred until SSH key login is verified, so user cannot accidentally lock themselves out. Do NOT use for - app deployment (Docker/Nginx config), DNS, domain setup, or managing already-hardened servers needing only routine updates.
allowed-tools: Bash,Read,Write,Edit
---

# VPS Initial Setup

Secure a fresh Linux server from provider credentials to a
production-ready state. The defining property of this skill: **password
authentication and root login are disabled only at the very end, after
the user has verified that key-based login works from their own
machine.** Beginners cannot lock themselves out by following this guide.

## Workflow Overview

```
Provider email (IP + root + password)
  → Determine execution mode (Remote or Local)
  → Generate SSH key (Remote) / defer (Local)
  → Connect as root
  → Handle forced password change if prompted
  → Update system (noninteractive)
  → Create non-root user + sudo
  → Install SSH key
  → ⚠ TEST new user login (CRITICAL CHECKPOINT)
  → Firewall (ufw)
  → Kernel hardening (sysctl)
  → Time sync + base packages
  → Configure local ~/.ssh/config
  → Quick audit
  → Generate guide file (credentials + commands)
  → ⚠ Re-verify ssh {nickname} works
  → fail2ban + lock SSH (PermitRootLogin no, PasswordAuthentication no)
  → Confirm ssh {nickname} still works after lockdown
  → ✅ Server secured
```

## Step 0: Determine Execution Mode and Collect Information

First, determine **execution mode**:

**Where is Claude Code running?**
- **On the user's local computer** (Remote mode) — we configure the
  remote server over SSH.
- **On the server itself** (Local mode) — we configure the same
  machine directly. Lockdown is more delicate because the user has not
  yet copied a key to their laptop.

### Remote Mode — ASK the user for:

1. **Server IP** — from provider email
2. **Root password** — from provider email
3. **Desired username** — for the new non-root account
4. **Server nickname** — for SSH config (e.g., `myserver`, `prod1`)

If the user pastes the full provider email, extract these values from
it and confirm them back.

### Detect the user's operating system (Remote mode)

The user's local OS dictates how Steps 1, 12, and the Guide File's
"SSH Key Setup" section are run. Detect first, ask only if detection is
ambiguous:

```bash
uname -s 2>/dev/null
```

- `Darwin` → **macOS** (use macOS/Linux variants)
- `Linux` → **Linux** (use macOS/Linux variants)
- command unknown / output starts with `Microsoft` / running in
  PowerShell or cmd → **Windows** (use Windows variants)

If detection fails (e.g. cross-platform terminal), ask the user
directly: "What OS is your laptop — macOS, Linux, or Windows?"

In **Local mode**, the server is Linux — OS detection for the user's
laptop is deferred to Step 14, since the user only touches their laptop
at that point.

### Local Mode — ASK the user for:

1. **Desired username** — for the new non-root account
2. **Server nickname** — for SSH config from the user's laptop later
   (e.g., `myserver`, `prod1`)

In Local mode, get the server's public IP automatically:

```bash
curl -4 -s ifconfig.me
```

## Execution Modes — How Steps Differ

All commands in `references/workflow.md` and `references/lockdown.md`
are written for **Remote mode** (executed via SSH from the user's
laptop). For **Local mode**, adapt as follows:

| Step | Remote Mode (default) | Local Mode |
|------|----------------------|------------|
| Step 1 | Generate SSH key on LOCAL machine | **SKIP** — user creates key on laptop later (Step 14) |
| Step 2 | `ssh root@{SERVER_IP}` | Already on server. If not root: `sudo su -` |
| Steps 3–4 | Run on server via root SSH | Run directly (already on server) |
| Step 5 | Install user's local public key on server | **SKIP** — user sends `.pub` via SCP later (Step 14) |
| Step 6 | SSH test from LOCAL: `ssh -i ... user@IP` | Switch user: `su - {username}`, then `sudo whoami` |
| Step 7 | **SKIP** — lockdown deferred to Step 14 | **SKIP** — lockdown deferred to Step 14 |
| Steps 8–11 | `sudo` on server via SSH | `sudo` directly (no SSH prefix) |
| Step 12 | Write `~/.ssh/config` on LOCAL | **SKIP** — user does this from guide file (Step 14) |
| Step 13 | Verify via `ssh {nickname}` | Run audit directly, **skip SSH lockdown checks** |
| Step 14 | Generate guide + fail2ban + lock SSH | Generate guide → SCP download → key setup on laptop → upload `.pub` → fail2ban + lock SSH |

In **both modes**, the end result is identical: the user has key-based
SSH access from their laptop via `ssh {nickname}`, and password +
root authentication are disabled.

## Where to find each step

This SKILL.md keeps Step 0 and the safety contract. The mechanical
steps live in two reference files — load them when you reach each
phase:

- **Steps 1–13** (key generation, root login, user creation, the
  Step-6 checkpoint, ufw, kernel hardening, time sync, local SSH
  config, pre-lockdown audit) → read `references/workflow.md`
- **Step 14** (deferred lockdown: guide file generation, fail2ban,
  PermitRootLogin/PasswordAuthentication off, post-lockdown
  verification) → read `references/lockdown.md`

The split keeps the trigger context small while making the full
procedure available on demand. **Always read both files in sequence
when running a fresh setup** — Step 14 cannot be skipped, that's the
whole point of the deferred-lockdown design.

## Critical Rules

1. **NEVER skip Step 6** (test login) — the user can be locked out
   permanently.
2. **NEVER disable root or password authentication before Step 14** —
   Step 14 is the only place lockdown is allowed, after key-based
   login has been verified end-to-end.
3. **NEVER store passwords in files on the server** that you do not
   delete at the end. The guide file on the server is removed in
   Step 14L-8.
4. **If connection drops after the password change**, reconnect — that
   is normal.
5. **If Step 6 fails**, fix it before proceeding. Keep the root
   session alive in Remote mode so you have a way back in.
6. **Generate the SSH key BEFORE the first connection** in Remote
   mode — the server can be set up in one pass.
7. **All operations after Step 6 use `sudo`** — never run as root.
8. **Steps 7 and 9 are deferred** — SSH lockdown and fail2ban happen
   only in Step 14.

## Optional Software

After initial setup, the user may want additional software (Docker,
Nginx, Node.js, Certbot, PM2, swap). See
`references/optional-software.md`.

## Security Audit

For auditing an existing server (or re-checking after setup), see
`references/security-audit.md`.

## Dangerous Operations

Always confirm before executing:

| Operation | Risk |
|-----------|------|
| `rm -rf` | CRITICAL — data loss |
| `docker system prune` | CRITICAL — data loss |
| `ufw disable` | HIGH — security |
| `systemctl restart sshd` | HIGH — can lock out (only safe after Step 14 verifies key works) |
| Database migrations | HIGH — schema changes |
| `--force` on any package manager | MEDIUM-HIGH — may break the system |
