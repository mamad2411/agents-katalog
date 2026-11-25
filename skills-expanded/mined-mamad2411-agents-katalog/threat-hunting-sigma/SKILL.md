---
name: threat-hunting-sigma
description: Use Sigma detection rules to structure threat hunts, map log fields to rule logic, and reason about false positives — for SIEM-style analysis and security event review. Use when the user mentions Sigma rules, detection engineering, or hunting with YAML rules.
version: 1.0.1
---

# Threat hunting with Sigma rules

**Portability:** Applies to any assistant helping with detection engineering; execution still depends on the user’s SIEM and Sigma converter, not on a specific coding agent.

[Sigma](https://github.com/SigmaHQ/sigma) is a generic signature format for SIEM queries. This skill helps agents **interpret**, **adapt**, and **hunt** with rules — not to run production conversions without the user’s toolchain.

## Core concepts

- **Title / id / status:** Human context and maturity (experimental, test, stable).
- **logsource:** Product/category/service — must match the data source you actually have (Windows Security, Zeek, AWS CloudTrail mapping via backends).
- **detection:** `selection` + `condition` (boolean logic over fields).
- **fields / falsepositives / level:** Tuning and severity hints.

## Hunting workflow

1. **Clarify data:** Which platform feeds the hunt (EDR, firewall, CloudTrail, proxy)? Confirm field names differ by backend — Sigma is abstract; concrete queries need a Sigma backend or manual mapping.
2. **Start broad, filter fast:** Use high-signal selections first (rare binaries, unique command lines, sensitive paths).
3. **Timebox:** Define window, baseline noise, then narrow with `filter` blocks or extra predicates.
4. **Validate FPs:** Read listed `falsepositives`; extend with organisational exclusions (approved admin paths, patch tools).
5. **Document:** For each hit cluster — entity, timeline, hypothesis, disproof, next query.

## Working with a rule file

- Read `detection.selection` identifiers — each lists field predicates.
- Combine with `condition` (`selection1 and not filter1`).
- Map placeholders (`1 of selection*`) to “any child selection matched”.

## Safe agent behaviour

- Treat rules as **logic templates**; do not assume 1:1 execution without the user’s converter (e.g. `sigmac`, pySigma).
- Never fabricate log lines; when examples are needed, use clearly synthetic values.
- Prefer suggesting **test queries** in the user’s native query language when the log source is known.

## Pointers

- Specification and examples: [SigmaHQ/sigma/wiki](https://github.com/SigmaHQ/sigma/wiki)
- Rule repository: [SigmaHQ/sigma rules](https://github.com/SigmaHQ/sigma/tree/master/rules)

**Inspiration:** Community skill listings such as [threat-hunting-with-sigma-rules-skill](https://github.com/jthack/threat-hunting-with-sigma-rules-skill) — adapt rule packs to your environment before relying on them.
