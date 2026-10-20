---
name: ctf-fscan
description: Use when pi needs the fscan tool for fast host discovery, port scanning, service identification, weak-password-oriented service checks, web title detection, or broad internal-network recon. Trigger on mentions of fscan or when the user wants a quick all-in-one scanner before deeper tooling.
---

# Local Assets

- Tool root: wherever `fscan` is installed (put it on PATH, or `cd` into its directory).
- Primary binary: `fscan` (Linux amd64 build) / `fscan.exe` (Windows).
- Read the bundled `doc.md` only when you need flag details or scan-engine behavior.

# Workflow

- Confirm authorization and target scope before scanning.
- On this Linux host, invoke `fscan` directly (Linux build).
- Start with a conservative discovery scan, then narrow ports/modules.
- Save scan logs under the current working directory unless the user asked for another path.

# Common Commands

```bash
# fscan should be on PATH or run from its install dir (Linux amd64 build)
fscan -h 192.168.1.10
fscan -h 192.168.1.0/24 -p 1-1000 -nopoc
fscan -h 192.168.1.10 -m ssh -nobr
fscan -h 192.168.1.10 -o result.txt
```

# Notes

- Use `-nopoc` when the user wants safer recon before active checks.
- Use `-m` to focus on a service family instead of scanning everything.
- Follow up with `nmap`, `dirsearch`, `hydra`, or `xray` when fscan finds interesting ports.
