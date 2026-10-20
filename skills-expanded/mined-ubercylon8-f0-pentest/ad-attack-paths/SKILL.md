---
name: ad-attack-paths
description: "Analyze collected BloodHound and AD CS data to find realistic privilege-escalation paths (Kerberoasting, AS-REP roasting, ACL abuse, delegation, certificate-template abuse) and rank them by feasibility and reversibility. Analysis only, no execution."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# AD Attack Paths

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing.


Analyze the collected graph and AD CS data to find realistic privilege-escalation paths, then
rank them by feasibility and reversibility. This phase is **analysis and planning** — nothing
is executed here.

## When to Use

- After `ad-enumerate`, with BloodHound data ingested.
- When asked to "find attack paths", "what escalates to Domain Admin", or "any roastable accounts / cert-template abuse".

## Quick Reference

Path classes to look for:

| Class             | Signal |
| ----------------- | ------ |
| Kerberoasting     | user accounts with SPNs |
| AS-REP roasting   | accounts that do not require pre-auth |
| ACL abuse         | GenericAll / GenericWrite / WriteDACL / Owns over high-value objects |
| Delegation        | unconstrained, constrained, or resource-based (RBCD) |
| AD CS             | enrollable templates with risky configuration (ESC-class patterns) |

Trace paths with BloodHound's UI and shortest-path queries; review `certipy find` output for template misconfigurations.

## Procedure

1. **Record context.** Analysis runs on already-collected data; note the engagement/scope it belongs to.
2. **Ingest.** Load the BloodHound zip; mark owned principals and high-value targets.
3. **Trace paths.** Use shortest-path-to-high-value queries and enumerate the path classes above.
4. **Review AD CS.** Cross-check `certipy find` output for the known misconfiguration patterns (enrollee-supplied SAN, dangerous EKUs, weak enrollment rights). Confirm the actual template config — don't rely on a heuristic flag alone.
5. **Prioritize.** Rank candidate paths by feasibility, required privilege, reversibility/impact, and noise. Mark which steps would be irreversible (writes, relays, cert issuance, secret replication) — those are approval-gated when executed.
6. **Output a path plan.** For each candidate: preconditions → the tool that executes it → impact → reversibility tier. Hand to `ad-access-escalate` (gated) and inform `ad-report`.

## Pitfalls

- **BloodHound shows *possible* edges**, some stale or impractical — validate before planning execution.
- **Collection noise hides the real paths** — filter to owned → high-value.
- **Cert "abuse vectors" need confirmation**, not just a flag.
- **Planning is not doing.** A path that needs a write/relay isn't "achieved" until it's been approved and tested — keep this phase separate from execution.

## Verification

- A ranked path plan exists; each path is tagged with the executing tool and a reversibility tier.
- Irreversible steps are explicitly flagged for the approval gate.
