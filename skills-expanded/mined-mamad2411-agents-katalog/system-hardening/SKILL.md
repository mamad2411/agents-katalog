---
name: system-hardening
description: |
  This skill should be used when the user mentions "harden", "hardening", "sysctl",
  "kernel parameters", "SSH config", "sshd_config", "firewall rules", "iptables",
  "nftables", "ufw", "fail2ban", "file permissions", "SUID", "SGID", "service minimization",
  "disable services", "auditd", "SELinux", "AppArmor", "CIS benchmark",
  "security baseline", "OS hardening", "attack platform", "operator machine",
  "Kali hardening", "disk encryption", "LUKS", "swap encryption", "encrypted swap",
  "secure boot", "firejail", "sandboxing", "credential storage", "pass", "keepassxc",
  "gpg-agent", "browser hardening", "USB security", "USBGuard", "memory protection",
  "ASLR", "stack protection", "application isolation", "service attack surface",
  "patch management", "update strategy", or discusses securing an operator's
  attack platform, engagement machine, or Kali/Debian workstation for red team operations.
  Always use this skill when an operator wants to lock down their own machine — this is
  about protecting the operator, not hardening a target.
version: 2.0.0
---

# System Hardening — Operator Platform Security

Comprehensive hardening for red team operator machines, attack platforms, and engagement workstations. This skill treats the operator's machine as the most sensitive asset in the engagement — a compromised operator platform means compromised operations, compromised clients, and compromised credentials.

The threat model here is different from server hardening: the operator needs a functional offensive toolkit while minimizing attack surface, protecting credentials, and preventing forensic recovery of engagement data.

## Opsec Profile Integration

Hardening depth scales with the active opsec profile. Check the current profile before applying changes:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/opsec-profile.js" get
```

| Profile | Kernel | Firewall | SSH | Disk | Services | Memory | Credentials |
|---------|--------|----------|-----|------|----------|--------|-------------|
| `loud` | ASLR only | Default accept | Key auth | Optional | All running | No wipe | Plain files OK |
| `normal` | Basic sysctl | INPUT drop | Key + non-default port | Home encrypted | Minimal | Swap encrypted | `pass` or `keepassxc` |
| `stealth` | Full sysctl | Strict in/out | ProxyJump + knockd | Full LUKS | Whitelist only | RAM wipe on lock | GPG-backed `pass` |
| `paranoid` | Full + modules locked | Egress filtered + Tor | Ephemeral keys per op | LUKS + detached header | Minimal + sandboxed | Encrypted swap + no core dumps | Hardware token + `pass` |

## Reference Files

Read the appropriate reference based on the hardening category:

| Category | Reference | When to Read |
|----------|-----------|-------------|
| Kernel parameters, ASLR, ptrace, namespaces | `references/kernel-hardening.md` | Sysctl tuning, kernel lockdown, memory protections |
| Firewall rulesets for operator machines | `references/firewall-config.md` | Inbound/outbound filtering, engagement-aware rules, Tor/VPN integration |
| SSH client and server hardening | `references/ssh-hardening.md` | Key management, ProxyJump chains, agent forwarding, tunneling |
| Disk, swap, and memory protection | `references/disk-and-memory.md` | LUKS encryption, swap encryption, RAM security, core dump prevention |
| Service minimization and sandboxing | `references/services-and-sandboxing.md` | Attack surface reduction, firejail profiles, AppArmor, service audit |
| Credential storage and browser security | `references/credential-and-browser.md` | `pass`, `keepassxc`, GPG agent, browser profiles, USB security |

## Workflow

1. **Profile check**: Read the active opsec profile — it determines minimum hardening depth
2. **Audit**: Scan current configuration across all categories (kernel, firewall, SSH, disk, services, credentials)
3. **Plan**: Map gaps to profile requirements, prioritize by risk, note which changes need a reboot
4. **Backup**: Snapshot current configs before modification (`/etc/sysctl.d/`, `/etc/ssh/`, firewall rules)
5. **Apply**: Execute hardening changes category by category, testing between each
6. **Verify**: Re-scan to confirm each change took effect
7. **Log**: Record all operations via `ops-tracker.js`
8. **Report**: Generate hardening report with before/after state

## Quick Audit Commands

Run these to assess current hardening state across all categories:

```bash
# Kernel — check critical sysctl values
sysctl kernel.randomize_va_space kernel.dmesg_restrict kernel.kptr_restrict kernel.yama.ptrace_scope fs.suid_dumpable net.ipv4.ip_forward 2>/dev/null

# Firewall — check default policies
sudo iptables -L -n --line-numbers 2>/dev/null | head -20 || sudo nft list ruleset 2>/dev/null | head -20

# SSH — check server config
sudo sshd -T 2>/dev/null | grep -iE "(permitrootlogin|passwordauth|pubkeyauth|port |x11forward|allowtcpforward)"

# Disk — check encryption
lsblk -o NAME,FSTYPE,MOUNTPOINT,SIZE | grep -E "(crypt|luks)"
swapon --show

# Services — count running
systemctl list-units --type=service --state=running --no-pager | wc -l

# SUID/SGID — find dangerous binaries
find / -perm -4000 -o -perm -2000 2>/dev/null | wc -l

# Credentials — check for plaintext secrets
find ~ -maxdepth 3 -name "*.key" -o -name "*.pem" -o -name "id_rsa" -o -name "*.p12" 2>/dev/null
```

## Cross-Skill References

- **VPS Security** (`vps-security`): For remote server provisioning and hardening — delegates system-level hardening back to this skill
- **Network Anonymity** (`network-anonymity`): For proxy chains, Tor, VPN, and leak prevention — complements firewall egress rules defined here
- **Anti-Forensics** (`anti-forensics`): For trace removal after operations — the memory and swap protections here reduce what forensics can recover

## Logging

All hardening operations MUST be logged:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-tracker.js" add --category "system-hardening" --action "<action>" --detail "<detail>"
```

Categories for ops-tracker: `kernel`, `ssh`, `firewall`, `services`, `permissions`, `storage`, `memory`, `credentials`, `monitoring`.
