---
name: termux-sshd
description: Set up, harden, and debug the OpenSSH server on Termux (port 8022, key authentication, connection refused, permission denied, host key warnings). Use when the user wants to log in to the phone from a computer, or an ssh connection to Termux fails. Do NOT use for outbound ssh and git keys (see git-credentials), and never expose the server beyond a trusted network.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "medium"
  triggers: "termux sshd,ssh into phone,port 8022,connection refused termux,sshd not starting,authorized_keys termux,login to termux from pc"
---
# Termux SSH Server

## Purpose
Give a trusted computer shell access to Termux, or find out why that connection fails, without leaving a weakly protected network service behind.

## When to use
- The user wants to ssh or scp into the phone.
- `Connection refused`, `Connection timed out`, `Permission denied`, or a host key warning when connecting to Termux.

## When NOT to use
- Outbound ssh from Termux to a server or GitHub: `git-credentials`.
- Any request to make the phone reachable from the public internet. Decline port forwarding to the internet; suggest a VPN or tunnel the user controls.

## Preconditions
Run `sh scripts/check-sshd.sh` (read-only; reports file modes and config lines, never key contents). Know the client OS and whether both devices are on the same trusted network.

## Decision tree
1. Needs the `openssh` package. The server listens on port 8022, not 22, because Android does not let unprivileged apps bind ports below 1024. The login name is the output of `whoami`.
2. Start with `sshd`; stop with `pkill sshd`. It does not start by itself; for that see `termux-services`.
3. Prefer key authentication: put the client's public key in `~/.ssh/authorized_keys`. `~/.ssh` must be mode 700 and `authorized_keys` mode 600; home must not be writable by others, or sshd ignores the key.
4. Set a password only as a fallback (`passwd`). After a key login works in a second session, set `PasswordAuthentication no` in `$PREFIX/etc/ssh/sshd_config` and restart sshd.
5. `Connection refused`: sshd is not running, wrong port, or wrong address. `Connection timed out`: wrong network, or the access point isolates clients. Find the phone's address in Android Wi-Fi details (interface listing commands are restricted on recent Android).
6. `Permission denied (publickey)`: modes from step 3, wrong user name, wrong key offered (`ssh -v`), or the key line is split across lines.
7. `REMOTE HOST IDENTIFICATION HAS CHANGED` after reinstalling Termux is expected; remove the old entry on the client after confirming the change is yours.
8. For a server-side view run `sshd -D -d -p 8022` in a spare session; stop it with Ctrl-C.
9. Sessions that drop when the screen turns off are Android suspending Termux: `background-processes`.

## Example
- Situation: ssh user@phone times out on port 22.
- Without the skill: Tries to bind sshd to port 22 and enables password login.
- With the skill: Explains Termux listens on 8022, logs in with the `whoami` name, installs the public key with modes 700 and 600, and disables password login only after a key login works.

## Safety
This opens an inbound network service. Use it only on a trusted network, with key authentication, and stop it when done. Never edit `sshd_config` without a copy, never enable root-style options or empty passwords, and never print private keys or `authorized_keys` content beyond key comments the user already shared.

## Verification
From the client, `ssh -p 8022 <user>@<phone-address>` logs in with the key and no password prompt; `pgrep sshd` shows the daemon on the phone; after hardening, a password attempt is refused.

## Rollback
Restore the saved `sshd_config` copy, `pkill sshd`, and remove any `authorized_keys` line added for this session.

## Handoffs
- `termux-services` to start sshd at boot with supervision.
- `termux-network` when the device is unreachable for network reasons.
- `background-processes` when sessions drop with the screen off.
- `git-credentials` for outbound keys.

## Report
Address and port, auth method in effect, what was changed in config (with the backup path), and the client login result.
