---
name: network-audit
description: >
  Deep network audit and remediation skill. DEPRECATED in this repo — 
  the canonical version lives in techstack-inventory-private as techstack-network-audit.
  This skill now delegates to that repo. Examples: "audit network", "check network health",
  "deep network scan", "find network bottlenecks", "analyze TCP retransmissions"
---

# Network Audit (Delegated)

This skill has been superseded by `techstack-network-audit` in the `techstack-inventory-private` repo.

## Why the move

- The v2 audit script (argparse, Finding dataclass, health score, delta sampling, ethtool, 
  tailscale netcheck, docker deep-dive, before/after comparison) lives in techstack-inventory-private.
- Network audit data belongs with the fleet inventory, not in the Pi control extension.
- The techstack repo has the Makefile target, reports directory, and inventory context.

## How to use

```bash
cd ~/OrgChefgroep/techstack-inventory-private

# Full audit
python3 scripts/network_audit.py

# Delta sampling
python3 scripts/network_audit.py --sample 30

# Compare before/after
python3 scripts/network_audit.py --compare before.json after.json

# Make target
make network-audit
```

Output: `reports/network-audit/network-audit.md` + `.json`

Skill reference: `skills/techstack-network-audit/SKILL.md`

## What it covers

- Interfaces, ethtool driver/ring/drops/offloads
- TCP/UDP sockets, BBR per-socket analysis
- IRQ/RSS/softnet imbalance detection
- ARP/neighbor health
- Kernel TCP tuning parameters
- Tailscale mesh + netcheck
- Docker networks, stats, exposed ports
- Structured Findings with severity, evidence, impact, fix commands, rollback
- Health score (0-100)
- Delta sampling for active vs lifetime counter distinction
