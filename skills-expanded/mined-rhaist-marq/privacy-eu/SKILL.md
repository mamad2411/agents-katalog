---
name: privacy-eu
description: "Covers EU GDPR essentials for a security team: what creates the obligation, the 72-hour breach notification clock, data-subject rights and DPIAs, fines, international transfers (Chapter V), and differences from US privacy. Use when the user asks whether GDPR applies, whether and when to notify a breach to a supervisory authority, about DPIAs, or about transferring personal data outside the EU."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# EU privacy: GDPR

GDPR is _personal-data_ protection (Regulation (EU) 2016/679). Regulator: national
DPAs. For the EU _cybersecurity/resilience_ regimes (NIS2, DORA) see
`load_skill nis2-dora`; for the EU product-security regime see `load_skill eu-cra`;
for the US side and an EU/US comparison see `load_skill privacy-us`.

Canonical text (web-fetch for current wording): eur-lex Regulation (EU) 2016/679.

## What creates the obligation

- Processing **personal data** of people in the EU/EEA, **extraterritorial**:
  triggered by the data subject's location, not where the company sits. Offering
  goods/services to, or monitoring, EU people pulls a non-EU company in.
- Roles matter: **controller** decides purposes/means; **processor** acts on the
  controller's instructions. Obligations and liability differ.
- Lawful basis is required for every processing activity (consent, contract,
  legal obligation, vital/public interest, or legitimate interest).

## Breach notification clock

- A **personal-data breach** = breach of confidentiality, integrity, **or**
  availability; **ransomware counts** even with no exfiltration.
- To the **supervisory authority: within 72 hours** of becoming _aware_ (Art. 33),
  unless unlikely to risk rights/freedoms. Late = document and explain the delay.
- To **affected data subjects: "without undue delay"** when **high risk** to their
  rights (Art. 34). Strong encryption of the lost data can remove this duty.
- **Processor → controller: "without undue delay"**: push this into your DPAs
  (see `load_skill legal-contractual`).
- **Pending change:** the EU **Digital Omnibus** proposal (Nov 2025) would raise
  the Art. 33 trigger to _high risk_ and extend the clock to **96 hours** via a
  single EU reporting entry point: **proposal only, not law as of Nov 2026**
  (Council mandate agreed 21 Oct 2026: keeps a longer breach deadline but
  swaps the EU entry point for national ones; Parliament position pending);
  the 72-hour regime above still applies. Web-verify before relying.

## Data-subject rights & DPIAs

- Rights: access, rectification, erasure ("right to be forgotten"), restriction,
  portability, objection, with statutory response deadlines (generally 1 month).
- **DPIA** required for high-risk processing (Art. 35); the privacy-engineering
  process for running one is in `load_skill privacy-engineering`.

## Penalties

- Up to **€20M or 4%** of global annual turnover, whichever is higher.

## International transfers (Chapter V)

- Moving personal data outside the EEA needs a transfer tool: an **adequacy
  decision**, **SCCs** (+ a transfer impact assessment post-_Schrems II_), or **BCRs**.
- **EU-US: Data Privacy Framework**: adequacy for US firms self-certified to the
  DPF (in force July 2023). The General Court **upheld it (Sept 2025, dismissing
  the _Latombe_ challenge)**, but an appeal is **pending at the CJEU (C-703/25 P,
  filed Oct 2025; no ruling as of mid-2026)**: a third _Schrems_-style
  invalidation isn't off the table, so keep **SCCs as a fallback**. Web-verify
  status before relying.
- **APAC pitfall**: GDPR compliance does **not** satisfy APAC transfer/localization
  law. **China PIPL** mandates local storage of important data plus a cross-border
  route (security assessment / SCC filing / certification); **India DPDP Act**
  (rules notified Nov 2025) and others regulate outbound transfer on their own
  terms. Map each jurisdiction; don't extrapolate from GDPR.

## vs the US

- GDPR is **opt-in / omnibus**: one law, all personal data, consent-forward. The
  US is **opt-out / sectoral patchwork** (`load_skill privacy-us`). Don't assume
  a US privacy posture satisfies GDPR, or vice versa.

## Pairs with

- EU cyber/resilience law: `load_skill nis2-dora`; product security: `load_skill eu-cra`.
- Breach-response handling & reporting decisions: `load_skill incident-response-leadership`.
- Mapping obligations onto your control set: `load_skill control-mapping`, `load_skill gap-analysis`.
