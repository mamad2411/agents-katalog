---
name: red-team-emulation
description: Red-team adversary-emulation engagement (vs. straightforward pentest). Use when the user mentions red team, adversary emulation, threat-actor emulation, TIBER-EU, CBEST, CREST STAR, MITRE ATT&CK chain, kill chain, C2 (Cobalt Strike, Sliver, Mythic, Havoc, Brute Ratel, Nighthawk), AMSI/ETW bypass, indirect syscalls (SysWhispers, HellsGate), sleep obfuscation (Ekko, Foliage), donut, ScareCrow, Inceptor, Evilginx, OAuth consent phishing, MFA fatigue, BYOVD/LOLDriver, KrbRelayUp, NanoDump, malleable profile, JA3, domain fronting, redirector, OPSEC, purple team, or detection engineering.
---

# Red Team Engagement

Apply `09-red-team/` from the pentest-templates library.

## Library root

`$PENTEST_LIBRARY` — caminho absoluto deste repositório clonado (definido pelo instalador; veja INSTALL.md).

Read `09-red-team/00-overview.md` first.

## Phase order (ATT&CK-aligned)

1. `09-red-team/01-targeting-intel.md` — TTP plan tied to actor profile, OSINT depth, infra warming.
2. `09-red-team/02-initial-access.md` — phishing (Evilginx AitM), OAuth consent, drive-by, vulnerable edge, cloud trust, USB.
3. `09-red-team/03-c2-infrastructure.md` — redirector, domain, TLS, malleable profile, backup channels, sleep obfuscation, anti-analysis.
4. `09-red-team/04-execution-defense-evasion.md` — loader chain, in-memory exec, AMSI/ETW bypass, AppLocker/WDAC bypass, BYOVD, process injection, LOLBins.
5. `09-red-team/05-credential-access.md` — opsec-aware LSASS, browser creds, DPAPI, SaaS tokens.
6. `09-red-team/06-discovery.md` — opsec-aware AD enum, network discovery, share enumeration, Tier-0 mapping, cloud/SaaS posture.
7. `09-red-team/07-lateral-movement.md` — native protocols, BOFs, cloud / SaaS lateral.
8. `09-red-team/08-persistence-privesc.md` — AD persistence, endpoint persistence, cloud persistence, SaaS persistence + cleanup planning.
9. `09-red-team/09-collection-exfil.md` — crown jewels, email / repo / cloud collection, exfil channels, DLP bypass.
10. `09-red-team/10-impact-objectives.md` — objective demonstration, simulated impact, detection-engineering deliverable, purple-team handoff.

## How to operate

1. Lock the actor profile + objective set in `01-targeting-intel.md` before standing up infra. The TTPs you choose must mirror that actor.
2. C2 infrastructure must be built BEFORE initial access — redirector, aged domain, malleable profile, sleep obfuscation, JA3/JA3S tuning. Default profiles for any C2 are signature-detected; require custom profile + sleep mask + indirect syscalls.
3. Cross-link to other skills for technique depth: `pentest-active-directory` for AD chains, `pentest-cloud` for cloud/SaaS lateral, `pentest-infra-internal` for endpoint primitives. The `09-red-team/` files are intentionally lean and reference those.
4. Document IOCs for every primitive — the purple-team handoff IS the deliverable.
5. Cleanup discipline: every persistence primitive has a removal procedure; verify at engagement end.

## When NOT to use

- Compliance-focused pentest (vulnerability inventory) → use the relevant `pentest-*` skill.
- Engagement explicitly NOT detection-aware — red-team techniques over-engineer for that case.

## Pre-conditions

- ROE explicitly defines red-team scope: white team, trusted agent, objectives, simulated impact allowance.
- C2 framework selected and infrastructure ready.
- White-team comm channel established.
- Detection-engineering deliverable expected (tabletop or purple-team session at close).

## OPSEC

- Custom malleable profile + sleep mask + indirect syscalls are baseline, not optional.
- Domain hygiene: aged domain, business-categorised, custom JA3/JA3S, realistic certificate chain.
- Catalog "expected detection × actual response" per TTP fired.

## References inside the library

- Tooling: `tools/install-infra.md` (post-ex), `tools/c2-frameworks.md`, `tool-mappings/09-red-team-tools.md`.
- Frameworks: `frameworks/mitre-attack-enterprise.md`.
- Phishing infra: `cheatsheets/initial-access.md`.
- Playbook: `playbooks/06-red-team-week-1.md`.
