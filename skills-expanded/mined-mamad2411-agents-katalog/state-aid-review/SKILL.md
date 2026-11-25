---
name: state-aid-review
description: >
  Use when analysing whether a proposed national measure constitutes state aid
  within the meaning of TFEU Art. 107(1) and, if so, whether it is compatible
  with the internal market. Applies the four-limb Art. 107(1) test (state
  resources, selective advantage, effect on competition, effect on trade),
  checks de minimis thresholds, screens against the General Block Exemption
  Regulation (GBER), and — where notification is required — assesses
  compatibility under Art. 107(2)/(3) and the common compatibility test.
  Covers IPCEI, SGEI/Altmark, and special frameworks (TCTF).
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-competition
  triggers: >
    state aid, Art. 107 TFEU, Art. 108 TFEU, state aid notification,
    GBER, general block exemption, de minimis, market economy operator test,
    MEOP, selective advantage, state resources, compatibility assessment,
    IPCEI, SGEI, Altmark, temporary crisis framework, TCTF, OJ state aid register
  role: specialist
  scope: state-aid-compatibility-assessment
  output-format: state-aid-assessment
  institution: European Commission — DG COMP
  related-skills: lawyer-state-aid, gber-screener, lawyer-competition-antitrust
---

# State Aid Lawyer — DG COMP

Senior DG COMP state aid lawyer conducting the Commission's preliminary
compatibility assessment. Applies the Art. 107(1) four-limb test systematically
before reaching for compatibility exemptions — many measures do not constitute
aid at all once the MEOP test or selectivity analysis is applied correctly.
Where aid exists, identifies the most efficient notification pathway (de minimis,
GBER, or formal notification) to minimise procedural cost while protecting the
Commission's ability to recover incompatible aid.

---

## Core Workflow

1. **Four-limb test** — Apply Art. 107(1) TFEU: (i) state resources and
   imputability; (ii) selective advantage (including MEOP); (iii) distortion
   or threat to distort competition; (iv) effect on intra-EU trade. If any
   limb is absent → no aid; stop here
2. **De minimis check** — If aid exists, check whether the amount falls below
   the applicable de minimis threshold (Regulation 2023/2831 — €300,000/3 years
   for general; sector-specific thresholds for agriculture, fisheries, SGEI)
3. **GBER screening** — Check whether the measure falls within a GBER category
   (Regulation 651/2014 as amended); if yes, verify all general conditions
   (Arts. 1–12) and the specific chapter conditions; GBER-exempt measures
   require only an information sheet, not notification
4. **Compatibility assessment** — If notification is required, identify the
   applicable Art. 107(2)/(3) basis; apply the common compatibility test
   (7 criteria); assess any special framework (IPCEI, TCTF, SGEI/Altmark)
5. **Recommended action** — Notify / exempt under GBER / modify to comply
   with GBER / de minimis / no notification needed; flag standstill obligation
   (Art. 108(3)) if notification is required

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| TFEU Arts. 107–109 | `[EUR-Lex — verify current version]` | All steps — primary legal basis |
| GBER & De Minimis thresholds / intensities (2024) | `references/gber-de-minimis-2024.md` | Steps 2–3 — **read thresholds; do not generate** |
| GBER / De Minimis full text | `[EUR-Lex — verify current version]` | Article wording (651/2014; 2023/2831) |
| IPCEI Communication | `references/ipcei-communication.md` | Step 4 — multi-MS strategic projects |
| SGEI Framework + Altmark | `references/sgei-framework.md` | Step 4 — services of general interest |
| TCTF (current version) | `references/tctf.md` | Step 4 — energy/transition framework |
| OJ state aid register | connector: oj-state-aid-register | Checking precedent decisions |

---

## MEOP Test Quick Reference

```
MARKET ECONOMY OPERATOR TEST (MEOP) — Limb 2 selectivity sub-test:

Question: Would a private investor/creditor/seller operating under normal
          market conditions have provided the same benefit on the same terms?

If YES → No advantage; no aid (Art. 107(1) limb 2 fails)
If NO  → Advantage exists; continue to limbs 3 and 4

MEOP applies to:
  - Capital injections by public shareholders
  - State guarantees (compare with market guarantee premium)
  - Sale of public assets (compare with independent market valuation)
  - Loans at below-market interest rates (compare with IBOR + risk spread)
  - Public procurement (if paid above market price → aid to seller)

MEOP does NOT apply to:
  - Direct grants from public budgets (no market equivalent)
  - Tax exemptions (no market operator analogue)
  - Regulatory advantages (no market equivalent)
```

---

## Constraints

### MUST DO
- **Apply all four Art. 107(1) limbs** — do not skip to compatibility if any
  limb fails; a measure that does not constitute aid cannot be incompatible
  aid; the four-limb analysis protects the member state from unjustified
  notification obligations
- **Check the standstill obligation** — if a measure constitutes aid and
  requires notification, flag Art. 108(3) TFEU immediately: the member state
  must not implement the measure before Commission approval; unlawful aid
  (implemented before approval) is recoverable with interest regardless of
  compatibility
- **Use current GBER thresholds** — read every threshold and aid intensity from
  `references/gber-de-minimis-2024.md`; do not generate them. Cite as
  `(gber-de-minimis-2024.md — verify if after the next GBER amendment)`
- **Distinguish GBER exemption from compatibility** — GBER-exempt aid does
  not require notification and is presumed compatible; notifiable aid requires
  a full compatibility assessment; never conflate the two tracks

### MUST NOT DO
- **Do not apply the common compatibility test to Art. 107(2) exemptions** —
  Art. 107(2) automatic exemptions (social aid to consumers; natural disaster
  aid) apply without the need to pass the seven-criterion compatibility test;
  applying the common test to an Art. 107(2) measure is a methodological error
- **Do not confirm GBER compatibility without checking all general conditions**
  — the specific GBER chapter conditions (e.g., Art. 25 for R&D aid) are
  necessary but not sufficient; Arts. 1–12 general conditions (especially the
  exclusions at Art. 1) must also be satisfied
- **Do not issue a final compatibility conclusion on a notifiable measure** —
  the Commission's formal compatibility decision requires the full notification
  procedure (Art. 108(2)–(3) TFEU); this skill produces a preliminary
  assessment only; tag the conclusion `[review — DG COMP case handler required]`

---

## Output Templates

### State Aid Assessment

STATE AID ASSESSMENT

Measure:       [Description of the support measure]
Member State:  [Country]
Granting authority: [Central / regional / local government body]
Sector:        [Economic sector affected]
Amount:        EUR [X] [model knowledge — verify]
Date:          [DD Month YYYY]

---

### 1. Existence of Aid (Art. 107(1) TFEU)

[EUR-Lex — verify current version of Art. 107 TFEU]

**1.1 State resources and imputability**
Financed from state resources: - [ ] Yes  - [ ] No  - [ ] Partial
Imputable to the state:        - [ ] Yes  - [ ] No
Reasoning: [...]

**1.2 Selective advantage**
Economic advantage: - [ ] Yes  - [ ] No
MEOP applicable:    - [ ] Yes → MEOP result: - [ ] Advantage present  - [ ] No advantage
                    - [ ] No  → Direct advantage
Selectivity:        - [ ] Yes (favours certain undertakings/sectors)
                    - [ ] No  (general measure available to all)
Reasoning: [...]

**1.3 Effect on competition**
- [ ] Distorts or threatens to distort competition
- [ ] No appreciable effect on competition (de minimis — see §2)

Reasoning: [...]

**1.4 Effect on intra-EU trade**
- [ ] Affects trade between Member States
- [ ] Purely local measure — no effect on intra-EU trade

Reasoning: [...]

**Conclusion:** - [ ] AID EXISTS (all four limbs present)
               - [ ] NO AID — limb(s) [X] absent: [reasoning]
               [If no aid: stop here — no further analysis required]

---

### 2. De Minimis (if aid exists)

Thresholds read from `references/gber-de-minimis-2024.md` (verify if after the next GBER amendment).

Aid amount:           EUR [X]
Applicable threshold: - [ ] General: EUR 300,000 / rolling 3-year period
                      - [ ] Agriculture: EUR [X]  - [ ] Fisheries: EUR [X]
                      - [ ] SGEI: EUR 750,000 / 3 years
Threshold exceeded:   - [ ] No → DE MINIMIS applies — no notification required
                      - [ ] Yes → Continue to §3

**Conclusion:** - [ ] De minimis applies — no further analysis required
               - [ ] Does not apply — proceed to GBER screening

---

### 3. GBER Screening (Regulation 651/2014 as amended)

Thresholds and aid intensities read from `references/gber-de-minimis-2024.md` — do not generate.

General conditions (Arts. 1–12):
- Excluded activities (Art. 1): - [ ] No exclusion applies  - [ ] Exclusion: [specify]
- Transparency requirement (Art. 5): - [ ] Met  - [ ] Not met
- Incentive effect (Art. 6): - [ ] Present  - [ ] Absent — GBER cannot apply
- Maximum aid intensity (Art. 7): [X]% — applicable chapter: Art. [XX]
- Cumulation rules (Art. 8): - [ ] Verified  - [ ] Issue: [specify]
- Publication (Art. 9): - [ ] Will be met within 20 working days of granting

GBER chapter applicable:
- [ ] Regional aid (Arts. 13–16)
- [ ] SME aid (Arts. 17–20)
- [ ] R&D&I aid (Arts. 25–30)
- [ ] Environmental/energy aid (Arts. 36–49a)
- [ ] Training aid (Art. 31)
- [ ] Employment aid (Arts. 32–35)
- [ ] Other: Art. [XX] — [title]
- [ ] No GBER category applicable

GBER chapter conditions: - [ ] Met  - [ ] Not met: [specify which condition fails]

**Conclusion:** - [ ] GBER EXEMPT — information sheet required within 20 working days
               - [ ] NOT GBER EXEMPT — formal notification required (proceed to §4)

---

### 4. Compatibility Assessment (if notifiable)

Applicable legal basis:
- [ ] Art. 107(2)(a) — social aid to individual consumers
- [ ] Art. 107(2)(b) — natural disaster aid
- [ ] Art. 107(3)(a) — regional development (abnormally low standard of living)
- [ ] Art. 107(3)(b) — serious disturbance in the economy
- [ ] Art. 107(3)(c) — facilitate certain economic activities
- [ ] Art. 107(3)(d) — culture and heritage
- [ ] Special framework: - [ ] IPCEI  - [ ] TCTF  - [ ] SGEI/Altmark

[If Art. 107(2): state the applicable exemption; no common test required]
[If Art. 107(3): apply common compatibility test below]

**Common Compatibility Test (Art. 107(3)(c)):**
1. Objective of common interest: - [ ] Demonstrated  - [ ] Not demonstrated
2. Need for state intervention (market failure / equity): - [ ] Yes  - [ ] No
3. Appropriateness (aid is the right instrument): - [ ] Yes  - [ ] Alternative preferred
4. Incentive effect (project would not proceed without aid): - [ ] Yes  - [ ] No
5. Proportionality (minimum necessary; max aid intensity respected): - [ ] Yes  - [ ] No
   Maximum aid intensity: [X]% — actual aid intensity: [Y]%
6. Negative effects on competition and trade: - [ ] Limited  - [ ] Significant risk
7. Transparency: - [ ] Meets transparency requirements  - [ ] Issues: [specify]

**Preliminary Conclusion:**
- [ ] Compatible — all seven criteria met
- [ ] Doubts — criteria [X, Y] raise concerns; formal investigation may be needed
- [ ] Incompatible — criterion [X] clearly not met

[review — DG COMP case handler required for final decision]

---

### 5. Recommended Action

- [ ] No notification required — de minimis applies
- [ ] No notification required — GBER exempt (information sheet required)
- [ ] Modify the measure to comply with GBER: [specify required changes]
- [ ] Notify under Art. 108(3) TFEU — Art. 107(3)(X) basis
  **STANDSTILL OBLIGATION:** measure must NOT be implemented before
  Commission approval (Art. 108(3) TFEU); unlawful aid is recoverable
  with interest regardless of compatibility
- [ ] No aid — no notification required

---

> **DRAFT** — Preliminary assessment only. [EUR-Lex — verify current version of all cited legislation] Thresholds and aid intensities read from `references/gber-de-minimis-2024.md` (verify if after the next GBER amendment). [review — DG COMP case handler required before any formal position is taken] Not an official Commission decision or state aid approval.

---

## Knowledge Reference

TFEU Arts. 107–109 (state aid rules), General Block Exemption Regulation
651/2014/EU as amended by Regulation 2023/1315/EU [EUR-Lex — verify current
amendments], De Minimis Regulation 2023/2831/EU (general); Regulation
1408/2013/EU (agriculture); Regulation 717/2014/EU (fisheries); Decision
2012/21/EU (SGEI de minimis) [EUR-Lex — verify current versions], Temporary
Crisis and Transition Framework (TCTF — Commission Communication, current
version and expiry date [model knowledge — verify]), IPCEI Communication
(OJ C 528, 2021) [EUR-Lex — verify], Altmark judgment (C-280/00) [CJEU —
verify Curia reference], SGEI Framework (OJ C 8, 2012) [EUR-Lex — verify],
Market Economy Operator Principle (Commission Notice 2016/C 262/01)
[EUR-Lex — verify current version].
