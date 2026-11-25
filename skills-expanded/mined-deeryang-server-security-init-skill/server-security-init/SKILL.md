---
name: server-security-init
description: "Use when safely initializing or hardening a newly installed or rebuilt Ubuntu/Debian server over SSH, including SSH keys, a non-root sudo user, SSH policy, server timezone, UFW, fail2ban, local SSH config, and lockout-safe verification."
---

# Server Security Init

## Purpose and Scope

Harden a fresh Ubuntu/Debian server without locking the operator out. Treat SSH, firewall, fail2ban, and service-manager changes as high-risk: inspect first, add and verify a parallel access path, then remove old access paths.

This workflow targets OpenSSH with systemd. UFW and fail2ban are optional. For another distribution, firewall, init system, or SSH implementation, stop before mutation, explain the differences, and obtain agreement on an adapted plan.

## Intake

Collect the bootstrap facts before touching the server. Infer values from prior context or local SSH config when safe, but show inferred values and obtain confirmation before high-risk mutations.

| Parameter | Meaning |
| --- | --- |
| `root_public_key_installed` | Whether the selected public key already works for the initial login user |
| `target_host` | Server IP, hostname, or existing SSH alias |
| `initial_user` | Current login user, often `root` |
| `initial_port` | Current SSH port, often `22` |
| `admin_user` | Non-root human administrator account to create or verify |
| `public_key_source` | Local `.pub` file, existing authorized key, or pasted public key |
| `local_key_name` | Local key basename, usually derived from the server alias |
| `identity_file` | Matching local private-key path used for every access-path gate |
| `ssh_config_alias` | Local SSH alias to create or update |
| `new_ssh_port` | Final SSH port |
| `target_timezone` | Desired IANA timezone such as `UTC` or `Asia/Shanghai`, or `keep-current` |
| `recovery_access` | Available provider console, VNC, rescue panel, or other out-of-band recovery path |
| `external_firewall_ready` | Whether provider/security-group rules permit the temporary and final SSH ports |

Collect these choices at the same intake gate:

| Parameter | Default |
| --- | --- |
| `disable_root_login` | `true`; when false, retain root public-key login rather than enabling root passwords |
| `disable_password_login` | `true` |
| `enable_ufw` | `true` |
| `rebuild_ufw` | `false`; preserve existing rules unless the user explicitly approves rebuilding them |
| `allowed_tcp_ports` | No additional ports; `new_ssh_port` is handled separately |
| `enable_fail2ban` | Ask; do not infer consent |
| `management_ips` | Required only when enabling fail2ban; current and usual admin egress IPs/CIDRs |
| `fail2ban_maxretry` | `3` |
| `fail2ban_findtime` | `86400` |
| `fail2ban_bantime` | `86400` |
| `generate_local_keypair` | Ask if no usable key exists |
| `local_key_comment` | Server alias or user-specified comment |
| `local_key_passphrase` | Ask; do not assume an empty passphrase |

Do not infer `target_timezone` from the operator's computer. Ask which timezone the server should use and validate the exact IANA name on the server.

## Input Validation

- `admin_user`: require `^[a-z_][a-z0-9_-]{0,31}$`; reject `root`. If it exists, require UID >= 1000, a real home directory, and an interactive shell. Never grant passwordless sudo to a service account.
- Ports: require numeric TCP ports in `1..65535`; prefer `1024..65535` unless the user explicitly chooses a privileged port. Deduplicate `allowed_tcp_ports`.
- Public key: resolve to exactly one non-empty valid public-key line and validate it with `ssh-keygen -lf` through a temporary file. Never print or transmit the private key.
- `target_timezone`: require `keep-current` or an exact entry from `timedatectl list-timezones`.
- `management_ips`: accept only explicit IP addresses or CIDRs recognized by the user. If the current egress cannot be determined confidently, ask before enabling fail2ban.
- Hostnames, aliases, paths, and other substituted values must not contain newlines. Treat all values as data, never shell fragments.

## Safety Invariants

- Do not disable root login, password login, the old SSH listener, or the old firewall rule until the new admin path succeeds in a separate SSH process.
- Every access-path gate must use the selected key explicitly with `BatchMode=yes`, `IdentitiesOnly=yes`, `ConnectTimeout`, and `-i identity_file`; success through an unrelated ssh-agent key is not proof.
- Keep the original SSH session open. Before changing listeners, confirm `recovery_access` and provider/security-group rules for `new_ssh_port`.
- Back up every changed configuration and record restoration commands. If a stage fails, stop mutations and either restore that checkpoint through the still-working session or use out-of-band recovery.
- Prefer owned drop-ins. Do not bulk-comment arbitrary SSH directives. If non-stock directives, `Match` blocks, config-management ownership, or an unexpected effective policy prevents a clean drop-in, stop and propose a targeted migration.
- Validate SSH syntax and effective policy before restart; after restart, use `sshd -T`, `sshd -T -C`, `ss -ltnp`, and systemd state as server-side truth.
- Inspect `ssh.socket`. Socket activation may own a listener independently of `sshd_config`; never assume changing `Port` moved the real listener.
- `enable_ufw=false` means do not install, reset, enable, or modify UFW. When enabled, preserve existing rules by default. Run `ufw --force reset` only when `rebuild_ufw=true` was explicitly confirmed and a restorable backup exists.
- Configure fail2ban `ignoreip` before enabling its SSH jail. Do not enable fail2ban without confirmed management IPs/CIDRs.
- Never overwrite an existing private key, automate a root password by default, or place passwords/private keys in commands, logs, config, or reports.
- Update only the requested local SSH `Host` block after backing up the file. Avoid regexes that can consume adjacent blocks.
- A reboot is a separate disruptive action. Perform it only with explicit authorization and an available recovery path.

## Workflow

1. **Intake and key bootstrap**
   - Collect and confirm the intake table, including `target_timezone`.
   - If needed, read `references/ubuntu-openssh-ufw-fail2ban.md` for local key generation and one-time public-key installation.
   - Stop until the selected key passes the initial public-key login gate.

2. **Read-only preflight and plan**
   - Read `references/ubuntu-openssh-ufw-fail2ban.md`.
   - Confirm Ubuntu/Debian version, current timezone, effective SSH policy, listeners, socket/service state, UFW rules, fail2ban state, existing admin account, and external firewall readiness.
   - Show the intended changes, preserved ports/rules, checkpoints, and recovery path before high-risk mutation.

3. **Add and verify a parallel admin path**
   - Set the confirmed timezone if it is not `keep-current`, then verify it.
   - Create or validate `admin_user`, install the selected public key, and validate passwordless sudo with `visudo` and `sudo -n`.
   - Add `new_ssh_port` while retaining `initial_port`. If UFW is enabled, allow both SSH ports plus explicit application ports without deleting unrelated rules.
   - Handle `ssh.socket` deliberately, restart SSH, verify the actual listener, and prove the new admin path in a separate local SSH process using `identity_file` explicitly.

4. **Apply and verify the final SSH/firewall state**
   - Apply the requested root/password policy through an owned drop-in; abort on unexpected effective values instead of rewriting unrelated files.
   - Restart SSH and re-prove the new admin path before removing the old listener or firewall rule.
   - If UFW is enabled, retain `new_ssh_port` and every confirmed `allowed_tcp_port`; remove the old SSH rule only when that port is not intentionally retained.
   - Verify root-key refusal when root login is disabled. Prove password policy with `sshd -T`/`sshd -T -C`; a client command using `BatchMode=yes` is not evidence that password authentication is disabled.

5. **Optional fail2ban**
   - Run only when `enable_fail2ban=true`.
   - Detect whether the chosen backend and ban action fit the host, configure `ignoreip` first, then enable and verify the jail. Unban and stop if a management IP is present in the ban list.

6. **Local SSH config and final verification**
   - Back up and update only `ssh_config_alias`; verify the resolved settings with `ssh -G` and reconnect through the alias.
   - Read and follow `references/verification-checklist.md`, including timezone, firewall conditionals, checkpoint locations, and service enablement.
   - Report meaningful redacted outputs. Do not echo inline public-key material, secrets, or unnecessary personal infrastructure details.
   - Offer an explicitly authorized reboot-and-reconnect test for persistence; do not reboot automatically.

## References

- `references/ubuntu-openssh-ufw-fail2ban.md`: read for Ubuntu/Debian command patterns, UFW branches, socket handling, fail2ban, and recovery checkpoints.
- `references/verification-checklist.md`: read for initial gates and final observable assertions.
