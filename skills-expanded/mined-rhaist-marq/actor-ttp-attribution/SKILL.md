---
name: actor-ttp-attribution
description: Guides going from observed behavior or IOCs to a candidate threat actor and concrete MITRE ATT&CK technique IDs with calibrated confidence, starting from ORKL report search. Use when the user asks who is behind an attack, which APT or group matches observed TTPs, to map behavior to ATT&CK, or how confident an attribution is.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Actor & TTP attribution

Map what you saw to ATT&CK techniques and, cautiously, to a named actor. Behaviour
attributes more reliably than infrastructure; actors swap IPs/domains, but reuse
tradecraft. Lead with TTPs, treat actor naming as a hypothesis.

## 1. Search the evidence: ORKL first

- For every IOC and tool/malware name you have, search ORKL:
  marq's `orkl` tool (`query`), or without marq
  `curl -s 'https://orkl.eu/api/v1/library/search?query=<ioc-or-tool-or-actor>'`.
  Returns the threat reports that mention it. Overlapping reports across several
  of your indicators = a candidate cluster. Read them for the actor's named TTPs.
- urlscan / Shodan pivots (see `ioc-pivoting`) to find infra also named in those
  reports: corroboration, not proof.

## 2. Map behaviour to ATT&CK technique IDs

- Translate each observation into a technique ID, e.g. spearphish link →
  **T1566.002**; scheduled task persistence → **T1053.005**; LSASS dump →
  **T1003.001**; WMI exec → **T1047**; web shell → **T1505.003**; living-off-the-
  land binaries → **T1218**.
- Web-fetch the current technique page `https://attack.mitre.org/techniques/T####/`
  to confirm scope, sub-techniques, and which groups use it; do **not** rely on
  memorised mappings; pages change.
- Build the kill-chain row by row: tactic → technique ID → your evidence →
  source. Gaps are fine; note "not observed", don't invent.

## 3. Candidate actor: converge, don't guess

- Intersect: which group(s) appear in the ORKL reports AND use your observed
  technique set AND match victim sector/geo/timing. Convergence of independent
  axes raises confidence; a single shared tool does not.
- Beware: shared open-source tooling (Cobalt Strike, Mimikatz, Impacket), false
  flags, and copied IOCs from prior reports. Commodity malware ≠ attribution.
- **APAC source-bias pitfall:** ORKL and English-language reporting skew Western
  and under-cover APAC-targeting activity. For actors hitting JP/KR/IN/SEA, a "no
  ORKL hits" result is often a coverage gap, not a clean sheet; cross-check
  regional CERTs (JPCERT/CC, KrCERT/KISA, CERT-In, AusCERT) and regional vendors
  (AhnLab, NSFOCUS, QiAnXin), and expect heavier alias sprawl across them.

## 4. Confidence + output

- State confidence explicitly (low/medium/high) with the reasons. Default to
  **low** unless multiple independent axes converge. "Consistent with X" ≠ "is X".
- Note actor-name aliasing (vendors name the same group differently): list the
  aliases you found rather than picking one.
- `write_file` an ATT&CK Navigator-style layer or a tactic→technique table;
  `report_finding` the TTPs (durable, defensible) with report URLs as references.
  Attribution goes in the narrative as a hypothesis, not as a finding's fact.
