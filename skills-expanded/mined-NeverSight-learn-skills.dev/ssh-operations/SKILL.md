---
name: ssh-operations
description: "SSH operations skill for connecting, running commands, file transfer, key setup, hardening, and troubleshooting across Windows, Linux, macOS, and WSL."
---

# SSH Operations Skill

Last audited: 2026-07-09
Generic placeholder pass: 2026-07-09

## Purpose

Use this skill whenever the user asks for SSH-related work, including:

- Connecting to a remote host
- Running commands over SSH
- Setting up SSH keys
- Fixing SSH login failures
- Configuring OpenSSH client or server
- Copying files with `scp`, `sftp`, or `rsync`
- Using jump hosts, bastions, tunnels, SOCKS proxies, HTTP proxies, or port forwarding
- Troubleshooting SSH on Windows, Linux, macOS, WSL, VPS providers, cloud servers, LAN devices, or network appliances
- Hardening SSH safely without locking the user out

This skill covers:

- Windows client to Linux server
- Linux client to Linux server
- Windows client to Windows server
- Linux client to Windows server
- macOS client to Linux or Windows server
- WSL as a Linux-like client
- Bastion and jump-host access
- IPv4 and IPv6
- Password, key, agent, and certificate-based workflows

## Non-negotiable rules

1. Never ask the user to paste a private key, password, token, recovery code, or full unredacted debug log.
2. Never print or store secrets.
3. Never use brute force, password spraying, credential guessing, bypass attempts, exploit chaining, stealth access, log deletion, or unauthorized persistence.
4. Never disable password login, root login, or an existing access path until a replacement login has been tested in a separate session.
5. Never auto-accept a changed host key.
6. Never use `StrictHostKeyChecking=no` or `UserKnownHostsFile=/dev/null` by default.
7. Prefer public-key authentication with a passphrase-protected private key.
8. Prefer Ed25519 keys for new keys unless the target is legacy.
9. Use least privilege. Do not run as root or Administrator unless required.
10. Treat SSH access changes as lockout-risk changes.
11. Back up config files before editing.
12. Validate SSH server config before restarting or reloading.
13. Keep an active fallback SSH session open during server-side SSH changes when possible.
14. Report exactly what changed and how it was verified.

## Minimum clarification rule

Ask only for missing information that blocks the task. Ask for hostname or IP, username, key path or auth method, port only if custom or port 22 fails, local OS only if command-dependent and not inferable, remote OS only if the task depends on it and cannot be detected safely after login. Do not ask for the remote OS if the agent can log in and run safe detection commands.

## Required SSH request model

For every SSH task, internally normalize the request to this model:

```yaml
local_os: windows | linux | macos | wsl | unknown
remote_os: linux | windows | macos | network_device | unknown
host: string
port: 22
remote_user: string
auth:
  method: key | password | agent | certificate | unknown
  key_path: string | null
jump:
  enabled: true | false
  host: string | null
  user: string | null
  port: 22
proxy:
  enabled: true | false
  type: socks5 | http | unknown
  address: string | null
operation:
  type: connect | run_command | copy_file | setup_key | configure_server | troubleshoot | harden | tunnel
risk_level: low | medium | high
```

If several fields are unknown but the request can still proceed safely, proceed with conservative defaults and report assumptions.

## Placeholder convention for publishable examples

Use placeholder tokens such as `<REMOTE_USER>`, `<TARGET_HOST>`, `<SSH_PORT>`, `<PRIVATE_KEY_PATH>`, `<KEY_NAME>`, `<HOST_ALIAS>`, `<BASTION_HOST>`, `<BASTION_USER>`, `<TARGET_ALIAS>`, `<PROXY_HOST>`, `<PROXY_PORT>`, `<LOCAL_BIND_ADDRESS>`, `<LOCAL_PORT>`, `<REMOTE_BIND_ADDRESS>`, `<REMOTE_PORT>`, `<DESTINATION_HOST>`, `<DESTINATION_PORT>`, `<LOCAL_PATH>`, `<REMOTE_PATH>`, `<SSH_ALLOWED_GROUP>`, `<SOURCE_IP_OR_CIDR>`. For shell examples prefer shell variables assigned from these placeholders. When giving a final user-specific answer, replace placeholders with values from the user request or detected environment; if a value is missing and required, ask only for that value.

## Identify local environment

Linux/macOS/WSL: `uname -a; command -v ssh; ssh -V`. Detect WSL: `grep -qi microsoft /proc/version && echo WSL || echo native`.
Windows PowerShell: `$PSVersionTable; Get-Command ssh -ErrorAction SilentlyContinue; ssh -V`. Check Admin: `(New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)`.

## Identify remote environment after login

Safe OS probe:
```bash
ssh "${REMOTE_USER}@${TARGET_HOST}" 'uname -a 2>/dev/null || ver 2>NUL || powershell -NoProfile -Command "$PSVersionTable.PSVersion"'
```
Linux probe: `cat /etc/os-release 2>/dev/null || uname -a`. Windows probe: `powershell -NoProfile -Command "Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber"`. If remote shell is cmd.exe, prefix PowerShell with `powershell -NoProfile -Command`.

## Runtime variables

Before using command examples, resolve values from the user request, SSH config, environment, or safe detection: REMOTE_USER, TARGET_HOST, SSH_PORT, PRIVATE_KEY_PATH, PUBLIC_KEY_PATH, BASTION_USER, BASTION_HOST, BASTION_PORT, LOCAL_BIND_ADDRESS, LOCAL_PORT, DESTINATION_HOST, DESTINATION_PORT.

## Default connection commands

Basic:
```bash
ssh -p "$SSH_PORT" -o ConnectTimeout=10 -o ServerAliveInterval=30 -o ServerAliveCountMax=3 "${REMOTE_USER}@${TARGET_HOST}"
```
With private key:
```bash
ssh -i "$PRIVATE_KEY_PATH" -p "$SSH_PORT" -o IdentitiesOnly=yes "${REMOTE_USER}@${TARGET_HOST}"
```
Non-interactive connectivity test:
```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 "${REMOTE_USER}@${TARGET_HOST}" 'echo SSH_OK'
```
Force public-key only:
```bash
ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no -i "$PRIVATE_KEY_PATH" -o IdentitiesOnly=yes "${REMOTE_USER}@${TARGET_HOST}"
```
Custom port: `ssh -p "$SSH_PORT" "${REMOTE_USER}@${TARGET_HOST}"`. IPv6: `ssh -6 "${REMOTE_USER}@${IPV6_TARGET_HOST}"`. IPv6 in config preferred.

## Host key verification

Do not bypass host keys casually. First connection: `ssh -o StrictHostKeyChecking=accept-new "${REMOTE_USER}@${TARGET_HOST}"` (only for first-time trusted hosts). Inspect known host: `ssh-keygen -F "$TARGET_HOST"`; with port: `ssh-keygen -F "[${TARGET_HOST}]:${SSH_PORT}"`. Remove stale key only after verification: `ssh-keygen -R "$TARGET_HOST"`. Collect host keys: `ssh-keyscan -T 5 -p "$SSH_PORT" -t ed25519,rsa "$TARGET_HOST"` - does not prove authenticity; compare through a trusted source. Fingerprint: `ssh-keygen -lf <HOST_PUBLIC_KEY_PATH>`.

## Key generation

Use Ed25519 for new keys. Linux/macOS/WSL:
```bash
mkdir -p ~/.ssh; chmod 700 ~/.ssh
ssh-keygen -t ed25519 -a 100 -C "$KEY_COMMENT" -f "$PRIVATE_KEY_PATH"
chmod 600 "$PRIVATE_KEY_PATH"; chmod 644 "${PRIVATE_KEY_PATH}.pub"
```
Windows PowerShell:
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.ssh" | Out-Null
ssh-keygen -t ed25519 -a 100 -C "$env:USERNAME@purpose-$(Get-Date -Format yyyyMMdd)" -f $PrivateKeyPath
```
Legacy fallback (RSA 4096) only when Ed25519 unsupported. Do not generate DSA.

## Private key handling

Private key stays on client; public key goes to server. Never paste private key. Use passphrase unless automation requires unencrypted key. For automation prefer a dedicated restricted key. If exposed, treat as compromised and rotate.

## SSH agent

Linux/macOS/WSL: `eval "$(ssh-agent -s)"; ssh-add "$PRIVATE_KEY_PATH"; ssh-add -l`. Windows: `Get-Service ssh-agent | Set-Service -StartupType Automatic; Start-Service ssh-agent; ssh-add $PrivateKeyPath`. Avoid agent forwarding; use ProxyJump instead. If required, scope to a specific host only.

## Client configuration

File locations: Linux/macOS/WSL `~/.ssh/config` and `/etc/ssh/ssh_config`. Windows `%UserProfile%\.ssh\config` and `%ProgramData%\ssh\ssh_config`. OpenSSH uses first value found per directive; put specific Host blocks before wildcards. Use `ssh -G <HOST_ALIAS>` to test resolved config. Use `Include ~/.ssh/config.d/*.conf` for snippets.

## Jump hosts and bastions

One-time: `ssh -J "${BASTION_USER}@${BASTION_HOST}" "${REMOTE_USER}@${TARGET_HOST}"`. Custom jump port: `ssh -J "${BASTION_USER}@${BASTION_HOST}:${BASTION_PORT}" ...`. Use `ProxyJump` in config. Multiple jumps: comma-separated `ProxyJump` list. Avoid agent forwarding through bastions unless explicitly required.

## Network proxies

SOCKS5 with OpenBSD netcat: `ProxyCommand nc -x <PROXY_HOST>:<PROXY_PORT> -X 5 %h %p`. HTTP proxy: `ProxyCommand nc -x <LOCAL_BIND_ADDRESS>:<LOCAL_PORT> -X connect %h %p`. Windows with Ncat: `ProxyCommand ncat --proxy <PROXY_HOST>:<PROXY_PORT> --proxy-type socks5 %h %p`. If `nc` lacks `-x`/`-X`, check `nc -h` or use `ncat`.

## Port forwarding

Local forward: `ssh -L "${LOCAL_BIND_ADDRESS}:${LOCAL_PORT}:${DESTINATION_HOST}:${DESTINATION_PORT}" "${REMOTE_USER}@${TARGET_HOST}"`. Remote forward: `ssh -R "${REMOTE_BIND_ADDRESS}:${REMOTE_PORT}:${LOCAL_SERVICE_HOST}:${LOCAL_SERVICE_PORT}" ...`. Dynamic SOCKS: `ssh -D "${LOCAL_BIND_ADDRESS}:${SOCKS_PORT}" -N ...`. Safer tunnel: `ssh -N -T -o ExitOnForwardFailure=yes -L ...`. Avoid binding to wildcard unless explicitly wanted.

## Connection reuse

Use ControlMaster on Linux/macOS/WSL: `ControlMaster auto; ControlPath ~/.ssh/cm-%r@%h:%p; ControlPersist 10m`. Check: `ssh -O check <HOST_ALIAS>`. Stop: `ssh -O exit <HOST_ALIAS>`. Do not rely on it in restricted Windows environments unless tested.

## File transfer

Prefer rsync for large/repeated Linux transfers, sftp for interactive and Windows path edge cases, scp for simple one-shot. SCP upload: `scp -P "$SSH_PORT" -i "$PRIVATE_KEY_PATH" "<LOCAL_PATH>" "${REMOTE_USER}@${TARGET_HOST}:<REMOTE_DIR>/"`. SCP download reverse. SFTP custom port uses `-oPort` not `-P`. Rsync: `rsync -azP -e "ssh -i $PRIVATE_KEY_PATH -p $SSH_PORT" "<LOCAL_DIR>/" "${REMOTE_USER}@${TARGET_HOST}:<REMOTE_DIR>/"`. Quote paths with spaces; for Windows remote paths prefer SFTP with forward slashes.

## Remote command execution

Linux: `ssh "${REMOTE_USER}@${TARGET_HOST}" 'uname -a && id && pwd'`. Safe Bash heredoc with `ssh ... 'bash -s' <<'EOF'` using single-quoted EOF. Sudo: check non-interactive `sudo -n true`; interactive use `ssh -tt`. Windows: `ssh ${REMOTE_USER}@${WINDOWS_TARGET_HOST} 'powershell -NoProfile -Command "..."'`. For complex scripts: write locally, upload with scp/sftp, execute, delete if sensitive, report result.

## Linux OpenSSH client/server setup

Client: apt/dnf/zypper/pacman/apk install openssh-client/openssh-clients/openssh. Server: install openssh-server, `systemctl enable --now ssh` (or sshd), check status and listener. Service name may be `ssh` or `sshd`; check both. Listener: `sudo ss -tlnp | grep ":${SSH_PORT}"`.

## Windows OpenSSH client/server setup

Client check: `Get-Command ssh; ssh -V`. Install via `Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Client*'` and `Add-WindowsCapability`. Server: `Get-Service sshd`; install `OpenSSH.Server*`; `Start-Service sshd; Set-Service sshd -StartupType Automatic`; firewall rule `OpenSSH-Server-In-TCP` on the SSH port; check listener `Get-NetTCPConnection -LocalPort $SshPort -State Listen`. On Windows Server 2025 OpenSSH Server may already be installed.

## Linux firewall rules

UFW: `sudo ufw allow "${SSH_PORT}/tcp"`. Firewalld: `sudo firewall-cmd --permanent --add-service=ssh; sudo firewall-cmd --reload` (custom port: `--add-port="${SSH_PORT}/tcp"`). nftables/iptables: inspect first with `sudo nft list ruleset` / `sudo iptables -S`.

## Linux authorized_keys setup

On server as target user: `mkdir -p ~/.ssh; chmod 700 ~/.ssh; touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys`. Append public key with `cat >> ~/.ssh/authorized_keys` (paste only the public key). From client: `ssh-copy-id -i "$PUBLIC_KEY_PATH" "${REMOTE_USER}@${TARGET_HOST}"` or fallback `cat <PUBLIC_KEY_PATH> | ssh ...`. SELinux fix if key auth fails: `restorecon -Rv ~/.ssh`.

## Linux sshd_config workflow

Main: `/etc/ssh/sshd_config`. Snippets: `/etc/ssh/sshd_config.d/*.conf` (check Include). Backup before changes: `sudo cp -a /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d-%H%M%S)`. Validate: `sudo sshd -t`. Show effective: `sudo sshd -T | sort`. Reload: `sudo systemctl reload ssh || sudo systemctl reload sshd`; restart only when reload unavailable.

## Linux lockout-safe hardening

Order: keep current session open; add new public key; test key login from second terminal; back up config; apply hardening; `sudo sshd -t`; reload; test new login; then close fallback. Key-only baseline: `PubkeyAuthentication yes; PasswordAuthentication no; PermitEmptyPasswords no; PermitRootLogin no`. If PAM MFA/OTP used, do not blindly set `KbdInteractiveAuthentication no`. Optional: `X11Forwarding no; AllowTcpForwarding no; PermitTunnel no; MaxAuthTries 3; LoginGraceTime 30; ClientAliveInterval 300; ClientAliveCountMax 2`. Do not set AllowTcpForwarding no if tunnels needed. Restrict: `AllowUsers <REMOTE_USER>` or `AllowGroups <SSH_ALLOWED_GROUP>`; always test in a second session.

## Windows sshd_config workflow

Main: `%ProgramData%\ssh\sshd_config`. Backup with `Copy-Item`. Validate: `& "$env:WINDIR\System32\OpenSSH\sshd.exe" -t -f "$env:ProgramData\ssh\sshd_config"`. Restart to apply: `Restart-Service sshd`. Windows sshd reads config at service start.

## Windows default SSH shell

Default is cmd.exe. Set PowerShell: `New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -PropertyType String -Force; Restart-Service sshd`. PowerShell 7 if present: check `Test-Path "C:\Program Files\PowerShell\7\pwsh.exe"` then set the path accordingly.

## Windows authorized_keys setup

Standard user: `%USERPROFILE%\.ssh\authorized_keys`. Create dir/file, then restrict ACLs with `icacls /inheritance:r` and grant the user full control; inspect ACLs if auth fails; remove broad write access (Everyone, Authenticated Users). Administrator accounts use `C:\ProgramData\ssh\administrators_authorized_keys` with ACL `/inheritance:r /grant "Administrators:F" /grant "SYSTEM:F"` (or SIDs `*S-1-5-32-544:F` and `*S-1-5-18:F` for localized installs). If the user is in Administrators, placing the key in the user profile may not work with default config.

## Windows OpenSSH restrictions

Supports local Windows accounts and AD domain accounts for key auth; Microsoft Entra ID accounts do not support key-based auth. Admin accounts use `administrators_authorized_keys`. `PermitRootLogin` not applicable. To block admins: `DenyGroups administrators` or lower-case localized equivalent. In Windows sshd_config, user/group names for allow/deny must be lower case. Supports only password and publickey under AuthenticationMethods.

## Authorized key restrictions

Force single command: `command="<FORCED_COMMAND>",restrict ssh-ed25519 AAAA... comment`. Restrict source IP: `from="<SOURCE_IP_OR_CIDR>",restrict ssh-ed25519 AAAA... comment`. Allow only a port forward: `restrict,port-forwarding,permitopen="<DESTINATION_HOST>:<DESTINATION_PORT>" ssh-ed25519 AAAA... comment`. Use restricted dedicated keys for automation.

## SSH certificates

Use only when the user has or wants CA-based access. Do not invent a CA. Sign: `ssh-keygen -s <CA_USER_PRIVATE_KEY_PATH> -I <CERT_ID> -n <REMOTE_USER> -V +52w <USER_PUBLIC_KEY_PATH>`. Client: `ssh -i "$USER_PRIVATE_KEY_PATH" -o CertificateFile="$USER_CERT_PATH" "${REMOTE_USER}@${TARGET_HOST}"`. Server trust: `TrustedUserCAKeys /etc/ssh/<CA_USER_PUBLIC_KEY_PATH>`. Validate config and test login from a second session after trust changes.

## Common troubleshooting decision tree

1. DNS/host: "Could not resolve hostname" - `getent hosts`, `nslookup`, PowerShell `Resolve-DnsName`.
2. Port blocked/host down: "Connection timed out"/"No route to host" - `nc -vz`, `Test-NetConnection`; check security group, ACL, firewall, public IP, instance state, subnet, port.
3. Service not listening: "Connection refused" - `systemctl status ssh/sshd`, `ss -tlnp`, Windows `Get-Service sshd; Get-NetTCPConnection`.
4. Public key rejected: "Permission denied (publickey)" - `ssh -vvv -i ... -o IdentitiesOnly=yes`; common causes wrong user/key, public key not installed, bad permissions, bad AuthorizedKeysFile, Windows admin needs administrators_authorized_keys, too many keys offered, SELinux context, PubkeyAuthentication no, AllowUsers/AllowGroups block. Force one key: `ssh -i "$PRIVATE_KEY_PATH" -o IdentitiesOnly=yes ...`.
5. Too many authentication failures: `ssh -o IdentitiesOnly=yes -i "$PRIVATE_KEY_PATH" ...`; optional `ssh-add -l; ssh-add -d "<OLD_KEY>"`.
6. Host key changed: "REMOTE HOST IDENTIFICATION HAS CHANGED" - stop, verify rebuild/IP reassign/rotation through trusted channel, then `ssh-keygen -R "$TARGET_HOST"`.
7. Bad permissions: Linux `chmod 700 ~/.ssh; chmod 600 <PRIVATE_KEY_PATH>; chmod 644 <PUBLIC_KEY_PATH>; chmod 600 ~/.ssh/config; chmod 700 ~/.ssh; chmod 600 ~/.ssh/authorized_keys`. Windows `icacls $PrivateKeyPath /inheritance:r /grant "$env:USERNAME:F"`.
8. Legacy algorithm mismatch: "no matching host key type/kex/cipher" - upgrade server, generate modern host keys, prefer Ed25519/ECDSA; temporary workaround only with explicit user acceptance: `ssh -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa ...`; do not add weak algorithms globally.
9. SFTP/SCP subsystem failure: "subsystem request failed" - check `Subsystem sftp` in sshd_config; common `Subsystem sftp /usr/lib/openssh/sftp-server` or `internal-sftp`; validate and reload.
10. SSH disconnects/hangs: "Broken pipe"/"Connection reset"/"kex_exchange_identification"/"banner exchange" - client keepalive; server checks `journalctl -u ssh/sshd`; causes fail2ban, firewall timeout, NAT timeout, IDS/WAF, MaxStartups, TCP wrappers, proxy failure.

## Logs

Debian/Ubuntu: `sudo journalctl -u ssh -n 100 --no-pager; sudo tail -n 100 /var/log/auth.log`. RHEL: `journalctl -u sshd; /var/log/secure`. Windows: `Get-WinEvent -LogName OpenSSH/Operational -MaxEvents 50 | Format-List`; file logs under `$env:ProgramData\ssh\logs`. Redact hostnames, public IPs if sensitive, usernames if sensitive, and accidental secrets; do not paste full unredacted logs.

## Safe deployment over SSH

Workflow: connect and identify OS; check user/privilege; check disk space; create backup; upload to temp path; validate syntax or dry run; move into place atomically; reload/restart; verify health; keep rollback ready; report exactly what changed. Linux example uses `ssh "${REMOTE_USER}@${TARGET_HOST}" 'bash -s' <<'EOF'` with `set -euo pipefail`, backup, validate, reload, `systemctl is-active`. Windows example uses `powershell -NoProfile -Command "Copy-Item; Restart-Service; Get-Service"`.

## Recovery if SSH access breaks

Do not attempt bypasses. Use authorized recovery paths: cloud serial console, provider web console, rescue mode, recovery ISO, attach disk to rescue VM, out-of-band management, physical keyboard/monitor, existing VPN/bastion session, cloud-init user data if supported, provider support if ownership proven. Linux recovery targets: `/home/<REMOTE_USER>/.ssh/authorized_keys`, `/etc/ssh/sshd_config`, `/etc/ssh/sshd_config.d/*.conf`, `/root/.ssh/authorized_keys`. Windows: `%USERPROFILE%\.ssh\authorized_keys`, `C:\ProgramData\ssh\administrators_authorized_keys`, `C:\ProgramData\ssh\sshd_config`.

## Reporting format after SSH work

Report as: Result (success/partial/failed); Host; User; Auth used; Changes made; Verification; Risks; Next action. Never include private keys, passwords, tokens, recovery codes, full sensitive config files, secrets from env vars, or unredacted `ssh -vvv` logs.

## Quick command reference

Define runtime variables first. Connect: `ssh "${REMOTE_USER}@${TARGET_HOST}"`. Connect with key: `ssh -i "$PRIVATE_KEY_PATH" -o IdentitiesOnly=yes "${REMOTE_USER}@${TARGET_HOST}"`. Custom port: `ssh -p "$SSH_PORT" "${REMOTE_USER}@${TARGET_HOST}"`. Run command: `ssh "${REMOTE_USER}@${TARGET_HOST}" '<REMOTE_COMMAND>'`. Debug to file: `ssh -vvv -E "<SSH_DEBUG_LOG>" "${REMOTE_USER}@${TARGET_HOST}"`. Resolved config: `ssh -G <HOST_ALIAS>`. Find known host: `ssh-keygen -F "$TARGET_HOST"`. Remove known host: `ssh-keygen -R "$TARGET_HOST"`. Copy to server: `scp -P "$SSH_PORT" "<LOCAL_PATH>" "${REMOTE_USER}@${TARGET_HOST}:<REMOTE_DIR>/"`. Copy from server (reverse). SFTP custom port: `sftp -oPort="$SSH_PORT" "${REMOTE_USER}@${TARGET_HOST}"`. Rsync over SSH: `rsync -azP -e "ssh -p $SSH_PORT -i $PRIVATE_KEY_PATH" "<LOCAL_DIR>/" "${REMOTE_USER}@${TARGET_HOST}:<REMOTE_DIR>/"`. Jump host: `ssh -J "${BASTION_USER}@${BASTION_HOST}" "${REMOTE_USER}@${TARGET_HOST}"`. Local tunnel: `ssh -N -T -o ExitOnForwardFailure=yes -L "${LOCAL_BIND_ADDRESS}:${LOCAL_PORT}:${DESTINATION_HOST}:${DESTINATION_PORT}" "${REMOTE_USER}@${TARGET_HOST}"`. SOCKS: `ssh -N -D "${LOCAL_BIND_ADDRESS}:${SOCKS_PORT}" "${REMOTE_USER}@${TARGET_HOST}"`. Test key-only login: `ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no -i "$PRIVATE_KEY_PATH" -o IdentitiesOnly=yes "${REMOTE_USER}@${TARGET_HOST}" 'echo KEY_LOGIN_OK'`.

## Agent-specific instruction

When a user prompt contains an SSH request, first apply any project-specific rules the user has already provided, then apply this skill. Project-specific rules override general examples in this skill when they are stricter, especially for required proxy use, approved servers, approved usernames, virtual environment paths, service names, deployment order, backup location, secret handling, and company security policy.
