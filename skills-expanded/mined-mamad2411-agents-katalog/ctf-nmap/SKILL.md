---
name: ctf-nmap
description: Use when pi needs Nmap guidance or local Nmap installers for host discovery, port scanning, service/version detection, NSE scripts, OS detection, or precise network recon. Trigger on mentions of nmap, NSE, service detection, or when the user wants more control than fscan provides.
---

# Local Assets

- `nmap` should be available. Per AGENTS.md 安装约定，下载/构建到 `tools/bin/` 并在会话内加 PATH，不要全局 `apt install`。
- Read the local `doc.md` when you need detailed option references or NSE guidance.

# Workflow

- First check whether `nmap` is already installed and in `PATH`.
- If missing, per AGENTS.md 把它装进 `tools/bin/`（源码构建或预编译包），不要全局安装。
- Prefer targeted commands such as `-sV`, `-sC`, `-p-`, or specific NSE scripts instead of overusing `-A`.

# Common Commands

```bash
nmap -sC -sV 192.168.1.10
nmap -Pn -p- --min-rate 3000 192.168.1.10
nmap -sV --script http-title,http-headers -p 80,443 192.168.1.10
nmap -O --osscan-guess 192.168.1.10
```

# Notes

- Use `-Pn` when ICMP or discovery probes are filtered.
- Use NSE scripts only for the service family relevant to the user’s target.
- If the user only needs quick surface recon, fscan may be faster; use Nmap for precision.
