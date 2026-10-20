---
name: ad-discover
description: "Map an in-scope subnet and identify the Domain Controllers. nmap service sweep plus read-only host facts, producing a clean host inventory for enumeration. Non-destructive."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# AD Discover

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing.


DISCOVER phase. Point at an in-scope subnet and produce a clean map: live hosts, their
AD-relevant services, and the likely Domain Controllers — the starting inventory for
enumeration. Non-destructive.

## When to Use

- Start of an internal/AD engagement, once `engagement-scope` is loaded.
- When asked to "explore subnet X", "find the domain controllers", or "map the topology".

## Quick Reference

| Tool            | Role                              | Typical invocation |
| --------------- | --------------------------------- | ------------------ |
| `nmap`          | host / service discovery          | `nmap -sS -p 53,88,135,139,389,445,464,636,3268,3269,5985 -oA disco <cidr>` |
| `netexec` (nxc) | quick read-only SMB/host facts    | `nxc smb <cidr>` (names, domain, signing, OS) |

DC tells: Kerberos (88) + LDAP (389), with Global Catalog (3268/3269), DNS (53), and SMB (445) alongside.

## Procedure

1. **Scope first.** Ensure `engagement-scope` is loaded; run its `scope_check` on each target/CIDR with `--action active_scan` (host discovery is active). Drop anything non-zero.
2. **Sweep services.** Run `nmap` over the AD-relevant ports across the in-scope range; save with `-oA`.
3. **Identify DCs.** Classify the scan output:
   ```bash
   python3 <skill-dir>/scripts/nmap_dc_parse.py disco.xml -o hosts.json
   ```
4. **Confirm domain facts.** Use `nxc smb` to read domain name, SMB signing posture, and OS — read-only.
5. **Output inventory.** Hand `hosts.json` (host, role guess, services) to `ad-enumerate`. Write it to the evidence dir (`<active-engagement>`).

## Pitfalls

- **Shared VLANs** mix in out-of-scope hosts — re-gate every host before touching it.
- **Aggressive timing** trips IDS and skews results; pace it (`-T3`, sane `--max-rate`).
- **LDAP+Kerberos ≈ DC, not = DC.** RODCs and members running services can look similar; confirm.
- **Assume multiple domains.** Note forest/child-domain hints for later phases.

## Verification

- `hosts.json` lists in-scope hosts with services and flags DC candidate(s).
- Domain name(s) and SMB signing posture are recorded.
