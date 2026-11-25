---
name: nis2-dora
description: "Covers EU NIS2 and DORA: who is in scope (essential/important entities, financial entities), the 24h/72h incident-notification clocks, security obligations, supervision and penalties, ICT third-party risk, and the DORA-over-NIS2 precedence for financial entities. Use when the user asks whether NIS2 or DORA applies, incident reporting deadlines, management liability, or how the two overlap."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# EU operational resilience: NIS2 & DORA

Two EU cybersecurity regimes (distinct from GDPR's _privacy_ focus; for that see
`load_skill privacy-eu`). Different scope, different regulators, different clocks,
and a financial-sector incident can implicate both plus GDPR at once.

- **NIS2**: cybersecurity of essential/important entities. Regulator: national
  NIS authority / CSIRT. Directive (EU) 2022/2555.
- **DORA**: ICT operational resilience of the financial sector. Regulator:
  financial supervisors (ESAs / national). Regulation (EU) 2022/2554 + RTS/ITS.

Canonical text (web-fetch for current detail): NIS2 = eur-lex Directive (EU)
2022/2555; DORA = eur-lex Regulation (EU) 2022/2554 and its RTS/ITS on ESMA/EBA/
EIOPA. These cite RTS that get revised; verify exact figures before relying.

## Who's in scope

- **NIS2: essential or important entity** in a covered sector: energy,
  transport, banking, financial market infra, health, drinking/waste water,
  digital infrastructure, ICT service management, public admin, space (essential);
  - postal, waste, chemicals, food, manufacturing, digital providers, research
    (important). Generally medium+ enterprises (size-cap rule, with exceptions).
    It's a **Directive** → obligations come from _national transposition law_, so
    specifics vary by member state.
- **DORA: financial entity** (banks, payment/e-money, investment firms,
  insurers, crypto-asset providers, funds, etc.) **or a critical ICT third-party
  provider** to them. It's a **Regulation**: directly applicable, uniform EU-wide.

## Security obligations (build the control once)

- **NIS2 (Art. 21):** risk-management measures: policies, incident handling,
  business continuity/backup, supply-chain security, vuln handling/disclosure,
  crypto, access control/MFA, and effectiveness testing. Management bodies must
  approve and oversee them.
- **DORA, five pillars:** (1) ICT risk-management framework, (2) ICT-incident
  management & reporting, (3) digital operational-resilience **testing** (incl.
  threat-led penetration testing / TLPT for significant entities), (4) **ICT third-party risk** (incl. an oversight
  regime for critical providers), (5) information sharing.

## Notification clocks (verify against the RTS)

**NIS2: significant incident (three-step, Art. 23)**

- **Early warning: within 24 hours** of becoming aware.
- **Incident notification: within 72 hours** (assessment, severity, IoCs).
- **Final report: within 1 month** of the notification. (Intermediate update on request.)

**DORA: major ICT-related incident (RTS: Commission Delegated Regulation (EU) 2025/301)**

- **Initial: within 4 hours of classifying** as major, and **≤24 hours** from awareness
  (classification itself due within 24h of detection).
- **Intermediate: within 72 hours** of the initial notification.
- **Final: within 1 month** of the intermediate report. Significant cyber-_threat_
  notification is voluntary; inform affected clients where relevant.

## Overlap & precedence

- **DORA is _lex specialis_ for finance** and generally supersedes NIS2's
  incident-reporting for in-scope financial entities; **verify the carve-out**
  for your entity type before assuming one or the other.
- A ransomware hit on an EU **bank** holding PII can fire **all three**: GDPR
  (personal-data breach, `load_skill privacy-eu`), DORA _or_ NIS2, and sector
  supervisor rules. Build the control once, report to the right regulator on the
  right clock.
- **Management is personally accountable** under both: board oversight is an
  explicit legal requirement, not a nicety.

## Dates

- **NIS2:** member-state **transposition deadline was 17 Oct 2024**, widely
  missed; as of **Oct 2026, 24 of 27** states have a transposition law in force
  (Germany 6 Dec 2025, Poland 3 Apr 2026, Luxembourg ~May 2026, Netherlands
  Cyberbeveiligingswet 15 Aug 2026; tracker count; the Commission only counts
  a state once its secondary legislation is complete too). **Ireland, Spain
  and France** are still outstanding; on **8 Jul 2026 the Commission referred
  them (and NL) to the CJEU** seeking financial sanctions. France's bill is
  still in Assemblée first reading (Oct 2026), Spain's has not reached the
  Cortes, Ireland's is unpublished (notification promised by end-2026). Check the specific national
  law that binds you, entry-into-force dates, competent authorities
  and penalties differ. Verify:
  https://digital-strategy.ec.europa.eu/en/policies/nis-transposition
- **DORA:** **applies from 17 Jan 2025.** Machinery is live: the ESAs
  **designated 19 critical ICT third-party providers on 18 Nov 2025** (AWS,
  Microsoft, Google Cloud, IBM, Oracle, SAP, Equinix, TCS et al.), each with a
  Lead Overseer + Joint Examination Team. The **register-of-information** filing
  recurs annually (2026 cycle: reference date 31 Dec 2025, ESA deadline 31 Mar
  2026; national windows opened earlier). TLPT RTS = **CDR (EU) 2025/1190** (in
  force 8 Jul 2025); TLPT cadence is ≥ every 3 years.
- **Pending changes (proposals; the clocks above still apply):**
  - **Digital Omnibus** (COM(2025)837, Nov 2025) would route NIS2/DORA/GDPR/
    eIDAS/CER incident reports through a **single entry point** run by ENISA.
    **Still a proposal**: after failed attempts (late Jun, 7 and 11 Oct 2026)
    the **Council agreed its mandate on 21 Oct 2026**, replacing the single EU
    entry point with a **national entry point per member state**; no EP
    position yet, so no trilogues. (The
    _AI_ half of the omnibus package split off and _was_ adopted (see
    `load_skill eu-ai-act`), so "the omnibus passed" is ambiguous; ask which.)
  - **NIS2 amendment + Cybersecurity Act revision** proposed **20 Jan 2026**
    (clearer sector thresholds, a "small midcap" category, certification as
    compliance evidence, standardised supply-chain questionnaires, ransomware-
    payment reporting). First reading; agreement targeted 2027.

## Penalties (orders of magnitude: NIS2 set in national law, verify)

- **NIS2:** essential up to **€10M or 2%** of global turnover; important up to
  **€7M or 1.4%**.
- **DORA:** supervisory measures + penalties per national/ESA regime; periodic
  penalty payments for critical ICT third-party providers.

## Pairs with

- `load_skill privacy-eu` (GDPR), `load_skill eu-cra` (product cybersecurity),
  `load_skill choosing-a-framework` (which regimes apply to you).
- Implementing the controls: `load_skill control-mapping`, `load_skill gap-analysis`,
  `load_skill incident-response-leadership` (the reporting-clock decisions).
- To map this finding to IEC 62443 / CRA / NIS2 obligations, `load_skill finding-control-crosswalk`.
