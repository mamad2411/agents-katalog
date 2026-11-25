---
name: kali-environment
description: "Detect Kali pentest tools, wordlist paths, and environment readiness before running engagements."
metadata:
  {
    "openclaw":
      {
        "emoji": "🐧",
        "os": ["linux"],
      },
  }
---

# Kali environment

Use at session start or when tool availability is unclear. Read-only checks unless the operator asks to install packages.

## Quick readiness scan

Run relevant checks (batch in one approval when possible):

```bash
cat /etc/os-release | head -5
command -v nmap gobuster ffuf sqlmap hydra john msfconsole tmux dig whois 2>/dev/null
ls -d /usr/share/wordlists /usr/share/seclists /usr/share/nmap/scripts 2>/dev/null
nmap --version 2>/dev/null | head -1
msfconsole --version 2>/dev/null | head -1
```

## Wordlists

```bash
test -f /usr/share/wordlists/rockyou.txt && echo rockyou:ok
test -f /usr/share/wordlists/rockyou.txt.gz && echo rockyou:gz
test -d /usr/share/seclists/Discovery/Web-Content && ls /usr/share/seclists/Discovery/Web-Content | head -5
```

If rockyou is gzipped:

```bash
zcat /usr/share/wordlists/rockyou.txt.gz 2>/dev/null | head -1
```

## Network interfaces

```bash
ip -br a
ip route | head -3
```

Use for `-e` on nmap when scans fail or VPN is required.

## Privileges

```bash
id
sudo -n true 2>/dev/null && echo sudo:passwordless || echo sudo:needs_password
```

Note: SYN scans (`-sS`) often need root or `cap_net_raw`.

## Missing tools

If a required binary is missing:

1. Tell the operator which tool is absent.
2. Suggest Kali package: `sudo apt install <pkg>` (map common names: `nmap`, `gobuster`, `sqlmap`, `hydra`, `john`, `metasploit-framework`).
3. Do not run `apt` without approval.

## Output to operator

Summarize as:

- OS/version
- Tools present/missing
- Wordlist paths available
- Sudo/raw scan capability
- Recommended fixes before engagement

Reference local paths in `TOOLS.md` when they differ from defaults.
