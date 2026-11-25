---
name: vps-hardening
description: >
  Expert Ubuntu 24.04 LTS VPS hardening assistant. Produces ready-to-run bash
  scripts, audits existing server security posture, and guides through all 15
  hardening categories (SSH, firewall, kernel, Docker, Nginx, TLS, backups,
  zero-trust, and more) aligned to CIS Benchmarks, NIST, and 2025–2026
  security standards. Use this skill whenever the user asks about hardening,
  securing, or auditing a VPS or server — even if they just say "how do I
  secure my server", "what do I need to do after spinning up a VPS", "make my
  server safe", "lock down my Ubuntu box", "check if my server is secure",
  "Docker firewall issue", "SSH hardening", "fail2ban setup", or any variation.
  Also trigger for questions about CrowdSec, nftables, AppArmor, WireGuard on a
  server, server backups, auditd, or systemd sandboxing.
---

# VPS Hardening — Ubuntu 24.04 LTS

## What can you do in your time budget?

Set realistic posture targets up-front. The skill is designed for incremental application — you do not need to clear all four P-levels to be safe, and pretending you can in one sitting causes the mistakes documented in "Operator gotchas" below.

- **2 hours → P0 + P1.** SSH hardening, UFW, CrowdSec, unattended-upgrades, sysctl network hardening, fail2ban-equivalent. Expected USG CIS Level 1 score: **~75%**. This is the "blocks 90%+ of automated attacks" tier — get here first, always.
- **1 day → add P2.** PAM hardening, GRUB cmdline (password optional — see GRUB landmine), AIDE, ClamAV, AppArmor enforcement (skip profiles you don't have), modprobe blacklists, fstab tmpfs hardening, audit rules, sandboxed systemd services. Expected: **~85% on Docker hosts / ~94% on host-only stacks**. The Docker delta is structural — IP forwarding, nftables management, ufw-vs-Docker — not a skill gap.
- **1 week → add P3.** Centralized logging, Wazuh agent (if you run a manager), backup automation + restore tests, USG tailoring file for architectural exemptions, full custom AppArmor profiles for your apps. Expected: **stable >90%**, durable against drift.

If you're under time pressure, ship P0+P1 today and schedule P2+P3 across the next maintenance windows. Half-applied P2 is worse than no P2 — see the AIDE baseline-timing gotcha.

## Reference material

All scripts, configs, and commands in this skill come from a single authoritative
source: `references/ubuntu-24-04-hardening.md`. Read it before generating any
output. It covers 15 categories with exact commands validated against Ubuntu
24.04 LTS defaults and aligned to CIS Benchmark v1.0.0, NIST SP 800-123/800-207,
and current CISA advisories.

**Read the reference file now — do not produce any scripts or recommendations
without consulting it first.**

---

## How to approach a request

Every request falls into one or more of three modes. Determine which apply,
then execute them in order: Audit → Guide → Scripts.

### Mode 1 — Audit (assess current state)

If the user has an existing server, run a quick audit before generating scripts.
Give them this diagnostic block to run and paste back:

```bash
echo "=== OS ===" && lsb_release -a
echo "=== SSH ===" && sudo sshd -T 2>/dev/null | grep -E "^(permitrootlogin|passwordauth|pubkeyauth|kex|cipher|mac|port)" | head -20
echo "=== UFW ===" && sudo ufw status verbose 2>/dev/null || echo "UFW not active"
echo "=== nftables ===" && sudo nft list ruleset 2>/dev/null | head -20 || echo "No nftables"
echo "=== SYSCTL ===" && sysctl kernel.randomize_va_space kernel.kptr_restrict kernel.dmesg_restrict net.ipv4.tcp_syncookies 2>/dev/null
echo "=== FAIL2BAN/CROWDSEC ===" && (systemctl is-active fail2ban 2>/dev/null || systemctl is-active crowdsec 2>/dev/null || echo "Neither active")
echo "=== DOCKER ===" && (docker info 2>/dev/null | grep -E "(Rootless|Security|userns)" || echo "Docker not running")
echo "=== DOCKER-BENCH ===" && (docker image ls docker/docker-bench-security 2>/dev/null | grep -q bench && echo "image cached" || echo "run: docker run --rm --net host --pid host -v /var/run/docker.sock:/var/run/docker.sock:ro docker/docker-bench-security")
echo "=== AUDITD ===" && systemctl is-active auditd 2>/dev/null
echo "=== UNATTENDED-UPGRADES ===" && dpkg -l unattended-upgrades 2>/dev/null | grep ^ii
echo "=== APPARMOR ===" && sudo aa-status --summary 2>/dev/null
echo "=== WIREGUARD ===" && (wg show 2>/dev/null || echo "WireGuard not active")
echo "=== SYSTEMD-SECURITY ===" && sudo systemd-analyze security 2>/dev/null | sort -k 2 -n | head -20
echo "=== LYNIS ===" && (which lynis >/dev/null 2>&1 && sudo lynis show version || echo "Lynis not installed")
echo "=== SSH-AUDIT ===" && (which ssh-audit >/dev/null 2>&1 && echo "ssh-audit available" || echo "ssh-audit not installed — install: pip install ssh-audit")
echo "=== TLS-HEADERS ===" && (curl -sI https://localhost 2>/dev/null | grep -iE "(strict-transport|x-content-type|x-frame|content-security)" || echo "No TLS headers (check externally via ssllabs.com/ssltest and observatory.mozilla.org)")
echo "=== SUID-FILES ===" && sudo find / -xdev -type f \( -perm -4000 -o -perm -2000 \) -ls 2>/dev/null | wc -l && echo "SUID/SGID files (count)"
echo "=== USG ===" && (which usg >/dev/null 2>&1 && sudo usg audit cis_level1_server 2>/dev/null || echo "USG not installed (requires Ubuntu Pro)")
```

Parse the output and produce a **gap report** organized by P-level (P0/P1/P2/P3).
Be specific: "SSH still allows root login", not "SSH needs hardening".

### Mode 2 — Guide (explain the approach)

When the user wants to understand what they're doing — brief explanations of
*why* each step matters, what changed in 2025–2026, and what tools to use.
Keep it concise: one paragraph per category maximum. The research file has a
"What changed in 2025–2026" section — use it.

Key 2025–2026 facts you must get right every time:
- **CrowdSec** is recommended over fail2ban (fail2ban has Python 3.12 issues on 24.04)
- **Wazuh** not OSSEC (OSSEC abandoned since January 2021)
- **Coraza WAF** not ModSecurity (ModSecurity reached EOL March 31, 2024)
- **nftables** is the default backend — `iptables` is just `iptables-nft` now
- **`systemctl restart ssh.socket`** not `systemctl restart sshd` on Ubuntu 24.04 (this applies to EVERY ssh restart, including after enabling MFA/PAM)
- **Ed25519** keys (DSA removed in OpenSSH 9.7+, RSA-SHA1 deprecated in 9.8+)
- **`PerSourcePenalties` requires OpenSSH 9.8+** — Ubuntu 24.04 ships 9.6p1 so the directive must stay commented out. `sshd -t` only warns and exits 0 if you leave it active; new connections then fail silently. Probe with `sshd -T 2>/dev/null | grep -i persourcepenalties` before enabling.
- **`sshd -t` is not strict.** Pair it with `sshd -T` AND a TCP loopback probe (`exec 3<>/dev/tcp/127.0.0.1/<port>; head -n 1 <&3` should return an `SSH-2.0-...` banner) before logging out of a session you just hardened.
- **Adding `admin` to sudoers without a password is a lockout trap.** `adduser admin` (interactive, sets a Unix password) → `usermod -aG sudo` → deploy keys → confirm `sudo -v` works in a new session → THEN disable `PasswordAuthentication`. If password-less sudo is the goal, install `/etc/sudoers.d/90-admin` with `NOPASSWD` explicitly; never just rely on the default sudoers and an unset password.
- **Host-key regeneration is destructive on existing servers.** It invalidates every `known_hosts` entry pointing at the host. Run only on a fresh install (or after coordinating a fingerprint rotation with all clients) — guard the script with a host-key age check.
- **Probe, don't assume features from version numbers.** Ubuntu/Debian sometimes backport directives; sometimes they don't. Check with `sshd -T 2>/dev/null | grep <directive>` or `sshd -G` at install time rather than gating on a release version.
- **NO OCSP stapling** for Let's Encrypt — dropped OCSP August 6, 2025
- **AppArmor fix required** before rootless Docker works on 24.04
- **Docker bypasses UFW** — patch DOCKER-USER chain (Option A) OR bind to 127.0.0.1 (Option B), never both. If containers already publish only to `127.0.0.1:` with a host reverse proxy in front, the DOCKER-USER patch will silently drop public traffic to that proxy. If you do apply Option A, the `ufw route allow proto tcp from any to any port 80,443` follow-up is MANDATORY, and verification must happen from an *external* host — on-box `curl` traverses INPUT, not FORWARD, and will lie to you.
- **Don't hardcode `storage-driver`** in `daemon.json`. Docker 29.x (Nov 2025+) defaults to `overlayfs`, not `overlay2`. Setting the wrong one against an existing `/var/lib/docker` makes the daemon refuse to start. Always run `docker info | grep "Storage Driver"` first; omit the key unless you have a specific reason to override.
- **GRUB superuser password locks out unattended reboot unless `--unrestricted` is set.** Without `--unrestricted` on the auto-generated menu entries (added via `/etc/grub.d/10_linux` `CLASS=`), every kernel update, panic, or host migration hangs the box at the bootloader. For VPS users, the threat this defends against (physical USB-keyboard access) does not exist — the provider's account login already gates console access. Default recommendation: skip GRUB password hardening on cloud VMs entirely. If applied anyway: `--unrestricted` is mandatory, the password must be typable on a US-layout console with no clipboard paste, and any `*.bak`/`*.orig` files in `/etc/grub.d/` must be `chmod -x`'d first (they are re-sourced by every `update-grub`).
- **No MTA = silent monitoring.** Ubuntu 24.04 server ships without a mail-transfer agent. The AIDE, ClamAV, rkhunter, and chkrootkit scripts in the reference all pipe to `mail`, which fails closed if nothing is listening on the local sendmail interface — alerts are then dropped without any error surfacing through cron. Configure msmtp (recommended for single-VPS alerts) or a Postfix null client BEFORE deploying any of those tools. STARTTLS on 587, scoped credential (App Password / API key, never an account password — Gmail killed Less Secure Apps on 2024-09-30), credential file at 0600, and a real end-to-end send to the destination inbox (not just a log line saying `status=sent`) before declaring it done. See "Alert delivery infrastructure" in §6 of the reference.
- **pam_faillock** not pam_tally2 (pam_tally2 is deprecated)
- **`sntrup761x25519-sha512`** post-quantum KEX is production-ready on 24.04
- **Recommended 2025 IDS stack**: CrowdSec (IPS with community intelligence) + Wazuh (SIEM/HIDS/FIM) — use both together
- **FORTIFY_SOURCE=3** — Ubuntu 24.04 upgraded from level 2 (enhances buffer overflow detection)
- **TLS 1.0/1.1 disabled system-wide** — OpenSSL and GnuTLS enforce TLS 1.2+ minimum; legacy apps may break
- **OpenSSH decoupled from libsystemd** — direct response to XZ-utils backdoor (CVE-2024-3094); reduces supply-chain attack surface

### Mode 3 — Scripts (ready-to-run bash)

This is the most important mode. Produce executable, commented bash scripts
that the user can run directly on their server. Always match commands exactly
from the reference file — do not substitute or improvise.

---

## Script generation workflow

### Step 0 — Pre-flight safety (ALWAYS include in any script that touches SSH/sudo/firewall)

The user is hardening a server they are CURRENTLY connected to. A single misstep can lock them out with no recovery path. Every script you produce must:

1. **Open with a banner** that tells the user to open a second SSH session in another terminal AND verify the VPS provider's console/KVM works, BEFORE running the script. Refuse to make this implicit.
2. **Take backups before edits** — `cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%s)` style, never overwrite blind.
3. **Probe features, don't assume them** — gate every `sshd_config` directive that depends on an OpenSSH version with `sshd -T 2>/dev/null | grep -i <directive>` (or `sshd -G`) before writing it into the config. Especially `PerSourcePenalties` on Ubuntu 24.04 (9.6p1).
4. **Validate strictly before reload** — `sshd -t` exits 0 on warnings. Combine `sshd -t` + `sshd -T >/dev/null` + a TCP loopback probe (read the `SSH-2.0-...` banner from `/dev/tcp/127.0.0.1/<port>`) after reload, with a clear "DO NOT LOG OUT" message if the probe fails.
5. **Set a sudo password before disabling root SSH.** `adduser admin` (interactive) → keys → confirm `sudo -v` works in a new session → THEN flip `PermitRootLogin no` / `PasswordAuthentication no`. If password-less sudo is the goal, install a `/etc/sudoers.d/90-admin` NOPASSWD file explicitly — don't silently rely on the default sudoers with an unset password.
6. **Gate destructive steps** — host-key regeneration breaks every existing client. Guard with a host-key age check (`stat -c %Y /etc/ssh/ssh_host_ed25519_key`) so the script refuses to run on a server that's not fresh, unless the user removes the guard intentionally.

If the user asks for a "one-liner" or "quick" script that skips these, push back. The cost of an extra 60 seconds of validation is much smaller than the cost of a locked-out server at 2am.

### Step 1 — Gather setup context

Before writing scripts, ask (or infer from context) these three questions:
1. Fresh VPS or existing server?
2. Which stack? (Docker Y/N, Nginx Y/N, Node.js/other app Y/N)
3. Admin username (needed for SSH AllowUsers and sudo setup)

If the user wants to get started immediately, assume: fresh VPS, Docker + Nginx,
admin user = `deploy`. Note assumptions at the top of the script.

### Step 2 — Produce scripts organized by P-level

Generate four scripts based on the priority checklist from the reference:

**`harden-p0.sh`** — Critical (run first, 15 minutes, blocks 90%+ of attacks):
- Package updates
- Create non-root admin user with sudo
- SSH hardening (sshd_config drop-in, Ed25519 host keys, socket activation)
- UFW: default deny, allow SSH/80/443
- CrowdSec install + nftables bouncer (primary recommendation)
- unattended-upgrades configuration

**`harden-p1.sh`** — High impact (run second, ~1 hour):
- Docker-UFW bypass fix (DOCKER-USER chain patch OR localhost binding — explain both, default to localhost binding)
- Hardened Docker daemon.json
- sysctl network hardening (`/etc/sysctl.d/99-network-hardening.conf`)
- sysctl kernel hardening (`/etc/sysctl.d/99-security-hardening.conf`)
- WireGuard VPN setup + lock SSH to VPN interface
- restic encrypted backup to S3 setup (credentials file chmod 600, init, backup, forget/prune, check)
  - S3 Object Lock in Compliance mode — immutable against ransomware (nobody, including AWS root, can delete during retention)
  - BorgBackup append-only mode alternative: `command="borg serve --restrict-to-path /backup/repo --append-only",restrict` in authorized_keys
  - 3-2-1 rule: 3 copies (production + local + offsite S3), 2 media types (SSD + object storage), 1 offsite

**`harden-p2.sh`** — Defense in depth (run third, first day):
- Disable unnecessary kernel modules (`/etc/modprobe.d/hardening.conf`) — CIS Benchmark
- GRUB boot security: hardened kernel parameters (`audit=1 init_on_alloc=1 pti=on randomize_kstack_offset=on vsyscall=none`). **GRUB superuser password is opt-in only** — default-skip on VPS (threat model doesn't apply, breaks unattended reboot); if requested, MUST include `--unrestricted` on `/etc/grub.d/10_linux` `CLASS=` and a console-typability check on the password.
- User and privilege management:
  - sudo hardening (`visudo`: use_pty, logfile, log_input/output, timestamp_timeout=5, requiretty)
  - pam_faillock account lockout (`/etc/security/faillock.conf`: deny=5, unlock_time=900, even_deny_root, fail_interval=900, audit)
  - pam_pwquality password policy (`/etc/security/pwquality.conf`: minlen=14, minclass=3, maxrepeat=3, dictcheck=1, enforce_for_root)
  - umask 027 via `/etc/profile.d/umask.sh`
  - lock root password (`passwd -l root`)
- auditd with CIS benchmark rules (4 rule files from reference)
- journald persistence configuration
- **Alert delivery infrastructure (msmtp or Postfix null client)** — required by every monitoring tool below that pipes to `mail`. Pick msmtp for single-VPS alerts, Postfix null client when queue durability matters. STARTTLS:587, scoped credential at 0600, real end-to-end inbox delivery test before moving on.
- Nginx security headers snippet
- Nginx TLS hardening (Mozilla Intermediate profile, NO OCSP for LE, certbot with `--key-type ecdsa`)
- Nginx rate limiting
- AIDE file integrity monitoring
- Filesystem hardening (fstab noexec mounts, immutable flags, permissions)
- systemd sandboxing for Nginx (and Node.js if applicable)
- Docker Compose hardening template
- Trivy install — **not Docker-only.** Install on every VPS regardless of stack. `trivy rootfs /` scans installed `.deb` packages AND every language lockfile (composer.lock for Laravel, package-lock.json for Node, Gemfile.lock, requirements.txt, go.mod, Cargo.lock) in one sweep. `trivy fs <path>` targets a single app directory. `trivy config` catches dangerous IaC defaults. Image scanning is only one of four modes. Weekly cron scan recommended on host-only stacks where Docker image-scan workflows don't apply.
- AppArmor enforcement for services
- Docker socket security: `chmod 660 /var/run/docker.sock && chown root:docker /var/run/docker.sock`,
  `getent group docker` to audit who has root-equivalent access via the socket,
  audit rules for docker.sock and docker binary (`/etc/audit/rules.d/docker.rules`),
  recommend `tecnativa/docker-socket-proxy` if any container needs Docker API access
  (never mount raw `/var/run/docker.sock` into containers)

**`harden-p3.sh`** — Operational security (run within first week):
- ClamAV automated scanning
- rkhunter + chkrootkit setup
- Scan schedule cron jobs (freshclam daily, rkhunter daily, AIDE daily, ClamAV weekly, chkrootkit weekly)
- Ubuntu Pro attach + Livepatch (template with placeholder token)
- Wazuh agent install (template with placeholder manager IP)
- CIS compliance scan setup: install Lynis (`apt install lynis`) + USG if Ubuntu Pro attached
- Coraza WAF or CrowdSec Nginx bouncer for application-layer protection (explain both options)
- SUID/SGID audit: find all SUID/SGID binaries, baseline to `/root/suid_baseline.txt`, remove unnecessary ones
- Centralized logging: rsyslog forwarding config OR Grafana Loki agent setup (explain both)
- Backup restore test script: automated monthly restic restore test to `/tmp/restore-test` with diff verification

Also generate **`audit.sh`** and **`verify.sh`** from the "Verification commands"
section at the end of the reference file.

### Step 3 — Script formatting rules

Every script must follow this structure:

```bash
#!/bin/bash
set -euo pipefail

# ============================================================
# VPS Hardening — Ubuntu 24.04 LTS
# Script: harden-p0.sh — Critical (P0)
# Source: CIS Benchmark v1.0.0, NIST SP 800-123, CISA advisories
# Tested on: Ubuntu 24.04 LTS (Noble Numbat)
# Run as: root or with sudo
# ============================================================
# ASSUMPTIONS (edit before running):
ADMIN_USER="deploy"        # Your non-root admin username
ADMIN_EMAIL="admin@example.com"
SSH_PORT="22"              # Change to custom port if desired
# ============================================================

# Color output
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()    { echo -e "${GREEN}[+]${NC} $1"; }
warn()    { echo -e "${YELLOW}[!]${NC} $1"; }
require() { echo -e "${RED}[✗]${NC} $1"; exit 1; }

[[ $EUID -ne 0 ]] && require "Run as root: sudo bash $0"
[[ $(lsb_release -rs) != "24.04" ]] && warn "Tested on Ubuntu 24.04 only"

info "Starting P0 hardening..."
```

Each section must have:
- A `# === SECTION NAME ===` header
- An `info "What this does..."` line before each block
- A `warn "MANUAL STEP REQUIRED: ..."` comment where human action is needed
  (e.g., copy SSH public key before disabling password auth)

### Step 4 — Always flag these manual steps

These cannot be automated — always warn the user explicitly:

```
⚠️  MANUAL STEPS REQUIRED (before running scripts):
1. Generate Ed25519 SSH key on your LOCAL machine first:
   ssh-keygen -t ed25519 -C "yourname@hostname" -a 100
   ssh-copy-id -i ~/.ssh/id_ed25519.pub ADMIN_USER@SERVER_IP
   Then verify key login works in a NEW terminal before running p0 script.

2. After running harden-p0.sh, test SSH still works before closing your session.

3. For WireGuard (p1): generate client config separately on your local machine.

4. For restic backups (p1): create S3 bucket and credentials before running.
   Enable S3 Object Lock in Compliance mode on the bucket for immutable ransomware-proof backups.

5. For Ubuntu Pro (p3): get your free token at ubuntu.com/pro (free for 5 machines).

6. For Wazuh (p3): deploy the Wazuh manager separately before installing the agent.

7. GRUB password (p2): **most VPS users should skip this entirely** — the threat model (physical/USB-keyboard access to a running box) doesn't apply to cloud VMs, and getting it wrong locks out unattended reboots. If the user insists: (a) run `grub-mkpasswd-pbkdf2` interactively, (b) the `--unrestricted` flag on `/etc/grub.d/10_linux` `CLASS=` is MANDATORY or the box won't reboot unattended, (c) the password must be typable on a US-layout console with no clipboard paste (browser KVMs strip both), (d) schedule a maintenance window with the console open before rebooting, (e) `chmod -x` any `/etc/grub.d/*.bak` files first — `update-grub` sources every executable file in that directory, including stale backups. See §4 GRUB boot security in the reference.
```

---

## Responding to specific scenarios

### "Just spun up a fresh VPS"
Run Mode 3. Ask the 3 setup questions, then generate all 4 scripts + the
manual steps warning. Suggest running them in order: p0 → reboot → p1 → p2 → p3.

### "Is my server secure?" / "Check my server"
Run Mode 1 (audit). Give them the diagnostic block, wait for output,
produce a gap report. Then offer to generate targeted scripts for the gaps.

### "Harden my SSH" / single category question
Generate just the relevant script section. Still use exact commands from
the reference. Note what other P-levels they're missing.

### "Change SSH port" / "move SSH to a different port"
Ubuntu 24.04 uses socket activation — the standard `Port 2222` in sshd_config alone
is NOT enough. Must also override the socket unit:
```bash
sudo mkdir -p /etc/systemd/system/ssh.socket.d/
cat <<EOF | sudo tee /etc/systemd/system/ssh.socket.d/override.conf
[Socket]
ListenStream=
ListenStream=2222
EOF
echo "Port 2222" | sudo tee /etc/ssh/sshd_config.d/port.conf
sudo ufw allow 2222/tcp comment 'SSH'
sudo ufw delete allow 22/tcp
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket
```
Always warn: test new port in a NEW terminal before closing the current session.

### "Docker and firewall not working"
This is almost certainly the Docker-UFW bypass problem. Explain it, offer
both fix options (DOCKER-USER chain patch and localhost binding), generate
the fix. Read section 2 of the reference first.

### "fail2ban not working on Ubuntu 24.04"
Explain the Python 3.12 asynchat issue. Recommend migrating to CrowdSec.
If they want to keep fail2ban: install `rsyslog` alongside fail2ban (`sudo systemctl enable --now rsyslog` — required for `auth.log`), then apply the asynchat compatibility patch from the reference.

### "WAF" / "web application firewall" / "ModSecurity"
ModSecurity reached EOL March 31, 2024. Recommend Coraza WAF (Go-based,
OWASP CRS v4 compatible, drop-in replacement). Mention open-appsec (AI/ML-based,
zero-day detection), NAXSI (lightweight Nginx-native module), and CrowdSec Nginx
bouncer as alternatives. Never suggest installing ModSecurity.

### "DDoS protection" / "getting hammered" / "Cloudflare"
Recommend placing the domain behind Cloudflare free tier (477 Tbps unmetered DDoS
capacity). Then restrict origin web traffic to Cloudflare IPs only via UFW:
```bash
for ip in $(curl -s https://www.cloudflare.com/ips-v4); do
    sudo ufw allow from $ip to any port 80,443 proto tcp
done
```
Also recommend the cloud provider's external firewall (DigitalOcean Cloud Firewalls,
AWS Security Groups) as a layer before traffic reaches the VPS.

### "SSH certificates" / "SSH CA" / "many servers"
Explain SSH CA as the gold standard at scale — certificates carry identity, expiration,
and principal restrictions, eliminating static `authorized_keys` management.
Include the CA key generation, user cert signing (12-hour), host cert signing (1-year),
and `TrustedUserCAKeys` sshd_config directive from the reference.

### "nginx not starting after reboot" / "mount namespacing failed" / "status=226/NAMESPACE"

Caused by the systemd hardening drop-in referencing `/run/nginx` in `ReadWritePaths` — `/run` is a tmpfs cleared on every boot, so `/run/nginx` doesn't exist when systemd tries to set up the mount namespace. Symptom:

```
nginx.service: Failed to set up mount namespacing: /run/nginx: No such file or directory
nginx.service: Control process exited, code=exited, status=226/NAMESPACE
```

Fix: add `RuntimeDirectory=nginx` to the drop-in so systemd creates the directory before each start:

```bash
sudo tee /etc/systemd/system/nginx.service.d/hardening.conf > /dev/null <<'EOF'
[Service]
RuntimeDirectory=nginx
RuntimeDirectoryMode=0755
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
...
EOF
sudo systemctl daemon-reload && sudo systemctl start nginx
```

Always include `RuntimeDirectory=nginx` whenever `ProtectSystem=strict` or any mount namespacing option is used in the nginx service drop-in. Never list `/run/nginx` in `ReadWritePaths` without it.

### "MFA" / "two-factor SSH" / "TOTP"
Explain Google Authenticator PAM module for SSH MFA. Include the pam.d/sshd config
(`auth required pam_google_authenticator.so nullok`) and sshd_config
(`AuthenticationMethods publickey,keyboard-interactive`). Always warn to
**test in a new terminal before closing the current session**.

### "WordPress" / "PHP site" / "CMS hosting"
In addition to standard hardening, mention **Monarx** — a commercial behavior-based
malware detection platform for PHP/CMS hosting that catches zero-days via execution
analysis rather than signatures. Useful alongside ClamAV (signature-based).

---

## Output format guidance

For a fresh VPS full hardening request, the ideal response structure is:

```
## Quick summary
[2-3 sentences: what you'll do, what tools you're using, why]

## ⚠️ Manual steps before running scripts
[The mandatory manual steps list]

## Setup variables
[Ask for or note assumptions about: admin user, email, SSH port, stack]

## Scripts
### harden-p0.sh — Critical (run first)
[full script in code block]

### harden-p1.sh — High impact (run after p0 + reboot)
[full script in code block]

... and so on

## After running all scripts: verify
[verify.sh or inline verification commands from the reference]
```

For targeted single-category requests, a single focused script block is
fine. Don't generate all 4 scripts when the user only asked about one thing.

---

## Operator gotchas

These are the failure modes that bit careful operators on real production VPSes. They share a pattern: a recommendation that's correct in isolation, applied without the context that makes it dangerous. Read every gotcha that applies before generating scripts in that area.

### `chattr +i` scope — narrow whitelist, never broad

The immutable flag is a tamper-detection helper, not a wholesale defense. Apply it only to files no legitimate tool needs to modify.

✅ **DO `chattr +i` on:**
- `/etc/ssh/sshd_config`
- `/etc/ssh/sshd_config.d/99-hardening.conf`
- `/boot/grub/grub.cfg`

❌ **DON'T `chattr +i` on:**
- `/etc/passwd` — breaks `adduser`, `useradd`, every package postinst that creates a service user, AND causes `chage --maxdays N <user>` to **silently exit 0 without writing anything** (chage opens `passwd` read-only as part of writing `shadow`; the read-only open fails on immutable, the write skips, the exit code lies). Password-aging policy enforcement looks successful but isn't.
- `/etc/shadow` — breaks `passwd`, `chage`, PAM `sp_lstchg` updates on login, `usermod -p`.
- `/etc/group`, `/etc/gshadow` — breaks `groupadd`, `gpasswd`, `usermod -aG`.
- `/etc/sudoers`, `/etc/sudoers.d/*` — breaks `visudo`, package installs that drop sudoers files.

The threat these were meant to defend (an attacker with brief root access writes a backdoor user) is better covered by `auditd -w /etc/passwd -p wa -k identity` (logs the write attempt) + AIDE alerts on those same paths (next-day notification). Detection beats brittle prevention here.

### Cloud-init SSH drop-in pre-flight

OpenSSH parses `/etc/ssh/sshd_config.d/*.conf` lexicographically and is **first-match-wins for most directives**. If an earlier-numbered drop-in (cloud-init or provider image default) sets `PasswordAuthentication yes`, a later `99-hardening.conf` saying `no` is silently overridden — `sshd -T` will report the *winning* value but you may not notice. Before writing the hardening drop-in, ALWAYS run:

```bash
grep -nE '^(PasswordAuthentication|PermitRootLogin|KbdInteractiveAuthentication|ChallengeResponseAuthentication)' \
  /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf
```

Filename and content vary by provider and image. On Hostinger, DigitalOcean, OVH, and stock Ubuntu cloud images, common offenders are `50-cloud-init.conf` and `60-cloudimg-settings.conf`. Treat the grep output as authoritative — never assume the image default matches the docs.

**Fix path:** if an earlier drop-in contains a conflicting directive, EITHER edit that file directly to remove the offending line, OR delete the drop-in entirely if you've confirmed cloud-init won't regenerate it on next boot. Don't try to "out-number" it with a higher-numbered file — `sshd -T` will pick whichever is *first* in the drop-in scan order for that directive.

### Policy directory backup mechanism — per-directory, not universal

The "don't leave `.bak` files in a policy directory" advice depends on **how that specific directory filters its contents**. The mechanism is different in each one, and a safe backup convention in `/etc/sudoers.d/` is a *bug* in `/usr/share/pam-configs/`. Use this table:

| Directory | Active filter | Safe backup |
|---|---|---|
| `/etc/grub.d/` | executable bit | `chmod -x` OR move to `/root/` |
| `/etc/sudoers.d/` | `[a-zA-Z0-9_-]+` (no dots) | rename to `*.bak` (inert) OR move out |
| `/etc/cron.d/` | `[a-zA-Z0-9_-]+` (no dots) | rename to `*.bak` (inert) OR move out |
| `/usr/share/pam-configs/` | **everything iterated** | **move out — no safe rename** |
| `/etc/sysctl.d/`, `/usr/lib/sysctl.d/` | ends in `.conf` | rename to `*.bak` OR move out |
| `/etc/profile.d/` | ends in `.sh` AND executable | `chmod -x` OR rename |
| `/etc/modprobe.d/` | ends in `.conf` | rename or move out |
| `/etc/ssh/sshd_config.d/` | ends in `.conf` | rename to `*.bak` (inert) |

**The `/usr/share/pam-configs/` row is the killer.** `pam-auth-update --force` iterates every file in that directory regardless of extension. A `unix.bak-20260606` backup gets loaded as a *second* `unix` profile, producing duplicate `pam_unix.so` lines in `common-auth` — and depending on which duplicate's options win, you can break login entirely. Always move backups out of that directory, never rename in place.

## What NOT to do

- Don't suggest `fail2ban` as the primary IPS — CrowdSec is the 2025 standard
- Don't suggest `iptables` directly — use UFW or native nftables
- Don't use `systemctl restart sshd` — Ubuntu 24.04 uses `ssh.socket`
- Don't add OCSP stapling to Let's Encrypt configs — LE dropped it August 2025
- Don't suggest OSSEC — it's been abandoned since 2021; use Wazuh
- Don't suggest ModSecurity — EOL March 2024; use Coraza WAF
- Don't suggest `pam_tally2` — deprecated; use pam_faillock
- Don't enable rootless Docker without the AppArmor fix first
- Don't generate scripts that disable UFW before nftables is confirmed working
- Don't suggest DSA keys — removed in OpenSSH 9.7+
- Never disable password authentication before confirming key-based auth works
- Don't add `X-XSS-Protection` header to Nginx — deprecated and can actually introduce XSS in safe sites; remove it if present
- Don't add `Expect-CT` header to Nginx — deprecated; browsers enforce Certificate Transparency natively; remove it if present
- Don't add `/run/nginx` to `ReadWritePaths` in a systemd hardening drop-in without also adding `RuntimeDirectory=nginx` — `/run` is a tmpfs cleared on boot, so `/run/nginx` won't exist and nginx will fail with status=226/NAMESPACE
- Don't set `Port 2222` in sshd_config alone to change the SSH port on Ubuntu 24.04 — socket activation requires overriding the ssh.socket unit as well
