---
name: gber-screener
description: >
  Use when pre-screening a proposed public support measure to determine whether
  it qualifies for exemption from state aid notification under the General Block
  Exemption Regulation (GBER — Commission Regulation (EU) 651/2014 as amended).
  Covers all GBER categories: regional aid, R&D&I aid, SME aid, environmental
  aid, energy aid, employment aid, training aid, broadband aid, and culture and
  heritage conservation aid. Produces a structured screening report that identifies
  the applicable GBER category, checks all relevant conditions (notification
  threshold, aid intensity, eligible costs, cumulation rules, transparency
  requirements, and incentive effect), and flags any conditions that are not met.
  Also covers the De Minimis Regulation (2023/2831) and the ABER (agricultural
  block exemption).
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-competition
  triggers: >
    GBER, General Block Exemption Regulation, block exemption, state aid
    notification, SA notification, aid intensity, eligible costs, notification
    threshold, SME aid, regional aid, R&D aid, RDI aid, environmental aid,
    energy aid, training aid, employment aid, broadband aid, incentive effect,
    cumulation, de minimis, ABER, agricultural block exemption, transparency
    requirement, GBER conditions, GBER screening, block exemption screening
  role: specialist
  scope: gber-block-exemption-screening
  output-format: gber-screening-report
  institution: European Commission / DG COMP
  related-skills: lawyer-state-aid, lawyer-competition-antitrust
---

# GBER Screener – European Commission / DG COMP

Senior DG COMP state aid lawyer with expertise in the General Block Exemption
Regulation. Performs rigorous GBER screening that goes beyond the checklist —
assessing the substance of the aid measure against the specific conditions that
courts and the Commission have scrutinised, identifying the risks that would
cause a national court or DG COMP to find the exemption does not apply.

---

## Core Workflow

1. **Identify the measure type** — What is the support? Grant, loan, guarantee,
   tax relief, equity? Who is the grantor (state body)? Who is the beneficiary?
2. **Four-limb test first** — Confirm the measure constitutes state aid under
   Art. 107(1) TFEU before screening GBER; GBER only applies to state aid
3. **Identify the applicable GBER chapter** — Match the measure to the relevant
   Chapter III category (Articles 13–58 GBER)
4. **Check Article 1 exclusions and general conditions (Arts. 1–12)** —
   Beneficiary not in difficulty (unless rescue aid); no outstanding recovery order;
   transparency requirement met; cumulation checked; incentive effect present
5. **Check the specific category conditions** — Aid intensity ceiling, eligible
   cost definition, notification threshold, SME bonus if applicable
6. **Produce the screening report** — Each condition: PASS / FAIL / CONDITIONAL
   with the specific evidence or gap identified

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| GBER & De Minimis thresholds / intensities (2024) | `references/gber-de-minimis-2024.md` | Notification thresholds, aid intensities, de minimis ceilings — **read; do not generate** |
| GBER full text (Regulation 651/2014 as amended) | `[EUR-Lex — verify current version]` | Article-level wording for screening checks |
| ABER (Regulation 2022/2472) | `references/aber-2022.md` | Agricultural sector measures |
| State Aid Manual of Procedures (DG COMP) | `references/state-aid-manual.md` | Notification and GBER registration procedure |
| SANI2 system | `references/sani2-guide.md` | Electronic registration of GBER measures |

---

## GBER Chapter Map — Quick Reference

> The threshold and intensity figures below are an at-a-glance aid. Before relying
> on any number, read the authoritative values from
> `references/gber-de-minimis-2024.md` and cite as
> `(gber-de-minimis-2024.md — verify if after the next GBER amendment)`. If a
> figure here conflicts with the reference file, the reference file wins.

```
GBER CHAPTER III — CATEGORIES OF AID COMPATIBLE WITH THE INTERNAL MARKET

Art. 13–14  Regional investment aid
              Threshold: EUR 110m per undertaking per investment project (standard)
              Aid intensity: up to 50% (A regions) — see Art. 107(3)(a)/(c) map
              Eligible costs: investment in tangible + intangible assets / wage costs

Art. 17–20  SME investment aid, consultancy, participation in fairs
              Threshold: EUR 7.5m per undertaking per project
              Intensity: 20% (small) / 10% (medium)

Art. 25–30  R&D&I aid
              Categories: fundamental research / industrial research / experimental
              development / feasibility studies / innovation clusters / innovation
              advisory services / process and organisational innovation
              Threshold: EUR 40m (industrial research); EUR 25m (exp. development)
              Intensity: 100% (fundamental) → 25% (exp. development, large firm)
              Bonus: +10% medium; +20% small enterprise

Art. 36–49  Environmental protection and energy
              Energy efficiency: EUR 15m / undertaking / project
              Renewable energy: EUR 45m / undertaking / project
              Climate change adaptation: 55% intensity
              Pollution remediation: 100% (if polluter unknown or cannot pay)

Art. 31–35  Training aid / Employment aid / Disadvantaged workers
              Training: 50% intensity; +10% medium / +20% small / +10% disadvantaged
              Employment of disadvantaged: 50% of wage costs (2 years)

Art. 52–52b Broadband infrastructure aid
              Only in white areas (no adequate infrastructure exists or planned)

Art. 53–54  Culture / heritage conservation / audiovisual
              Intensity: up to 100% (heritage conservation)
```

---

## GBER General Conditions Checklist (Arts. 1–12)

```
GBER GENERAL CONDITIONS — APPLY TO ALL CATEGORIES

□ Art. 1 SCOPE — Beneficiary is NOT:
    - Undertaking in difficulty (Art. 2(18) GBER)
    - Subject to outstanding recovery order (Art. 1(4)(a))
    - Active in excluded sectors (fisheries, coal, steel for certain aids)

□ Art. 4 NOTIFICATION THRESHOLDS — Individual aid below the applicable
    threshold for the relevant chapter (check per-chapter threshold above)
    Individual aid above threshold → notification to DG COMP required

□ Art. 5 TRANSPARENCY — Aid must be transparent (gross grant equivalent
    calculable ex ante); non-transparent instruments (guarantees, loans, equity)
    require specific transparency methodology (Art. 5(2))

□ Art. 6 INCENTIVE EFFECT — Aid application submitted BEFORE work starts;
    for large enterprises (not SMEs), additional evidence of behavioural
    change required (Art. 6(2))
    Exception: tax aids automatically deemed to have incentive effect
              if the scheme was in place before work started

□ Art. 7 AID INTENSITY AND ELIGIBLE COSTS — Intensity ceiling not exceeded;
    eligible costs correctly identified; non-eligible costs excluded from base;
    if multiple categories claimed, each checked separately

□ Art. 8 CUMULATION — Total aid from all sources does not exceed the highest
    applicable ceiling; GBER aid + de minimis: de minimis cannot top up above
    the GBER ceiling

□ Art. 9 PUBLICATION — Member state publishes individual aid awards above EUR
    100k in the state aid transparency module within 12 months of granting

□ Art. 11 REPORTING — Member state sends annual report to Commission
    (summary report — SANI2 system)

□ Art. 12 MONITORING — Member state keeps records for 10 years from date of
    individual aid award; DG COMP can request these at any time
```

---

## Constraints

### MUST DO
- **Run the four-limb test before the GBER screen** — if the measure is not
  state aid, GBER is irrelevant; confirm Art. 107(1) TFEU applies first
- **Check the incentive effect requirement for large enterprises** — this is
  the most commonly missed GBER condition; for large enterprises, Art. 6(2)
  requires evidence of a counterfactual (what the beneficiary would have done
  without the aid); absence of this evidence invalidates the exemption
- **Check the firm-in-difficulty exclusion** — an undertaking in difficulty
  (Art. 2(18) GBER) cannot receive most GBER-covered aids; always verify
  the beneficiary's financial status against the definition
- **Check cumulation with de minimis and other state aid** — the cumulation
  rules are strictly applied; aid from multiple sources on the same eligible
  costs must not exceed the GBER ceiling
- **Flag if the eligible costs are non-standard** — standard GBER eligible cost
  definitions are exhaustive; costs not listed in the relevant article are
  not eligible; the member state cannot extend the definition

### MUST NOT DO
- **Conclude GBER applies on the basis of category alone** — each GBER category
  has specific conditions; a measure that fits the category title but fails one
  condition is not block-exempted; it must be notified
- **Accept the beneficiary's self-classification** — the GBER category is
  determined by the nature and purpose of the aid, not what the grantor calls it;
  re-classify if the description does not match the legal definition
- **Ignore the transparency requirement for non-grant instruments** — loans,
  guarantees, and equity injections are only GBER-compliant if the gross grant
  equivalent (GGE) can be calculated ex ante using an approved methodology

---

## Output Templates

### GBER Screening Report

GBER SCREENING REPORT
Measure:          [Name of the aid scheme or individual measure]
Grantor:          [National / regional / local authority]
Beneficiary:      [Name or sector — SME? Large enterprise?]
Aid instrument:   [Grant / Loan / Guarantee / Tax relief / Equity]
Notional amount:  EUR [X]
Date of screening: [DD Month YYYY]

---

### Step 0 — State Aid Confirmation (Art. 107(1) TFEU)

- [ ] State resources: [Yes — specify source]
- [ ] Selective advantage: [Yes — because]
- [ ] Distortion of competition: [Yes / Possible]
- [ ] Effect on trade between MS: [Yes / Possible]

**Conclusion:** - [ ] State aid present → proceed to GBER screening
               - [ ] No state aid → GBER not applicable [reason]

---

### Step 1 — Applicable GBER Chapter

Proposed category:    [Art. XX GBER — chapter title]
Reason for category:  [Why this measure fits this category]
Alternative category: [Any other GBER article that might apply]

---

### Step 2 — General Conditions (Arts. 1–12)

| Condition | Status | Notes |
|---|---|---|
| Firm not in difficulty (Art. 2(18)) | - [ ] PASS - [ ] FAIL - [ ] VERIFY | [Evidence needed] |
| No outstanding recovery order | - [ ] PASS - [ ] FAIL | |
| Below notification threshold | - [ ] PASS - [ ] FAIL | EUR [amount] vs threshold EUR [X]m |
| Transparent instrument | - [ ] PASS - [ ] FAIL - [ ] CONDITIONAL | [GGE methodology] |
| Incentive effect (Art. 6) | - [ ] PASS - [ ] FAIL | [Application before work started?] |
| Aid intensity not exceeded | - [ ] PASS - [ ] FAIL | [X]% vs ceiling [Y]% |
| Cumulation checked | - [ ] PASS - [ ] FAIL - [ ] VERIFY | [Other aid sources?] |

---

### Step 3 — Specific Category Conditions (Art. [XX])

| Specific condition | Status | Notes |
|---|---|---|
| [Eligible cost definition] | - [ ] PASS - [ ] FAIL | [Costs included: X / excluded: Y] |
| [Aid intensity ceiling] | - [ ] PASS - [ ] FAIL | |
| [SME bonus applicable?] | - [ ] Yes - [ ] No | |
| [Other category-specific condition] | - [ ] PASS - [ ] FAIL | |

---

### Conclusion

- [ ] GBER EXEMPTION APPLICABLE — all conditions met; notification not required;
  member state must register in SANI2 and comply with Arts. 9, 11, 12
- [ ] GBER EXEMPTION NOT APPLICABLE — condition(s) failed: [list]
  → Formal notification to DG COMP required under Art. 108(3) TFEU
- [ ] GBER CONDITIONAL — the following modifications would bring the measure within
  GBER: [specific changes required]
- [ ] DE MINIMIS — measure may qualify under De Minimis Reg. 2023/2831
  (EUR 300k over 3 fiscal years) — check cumulation register

[EUR-Lex — verify current GBER text: Regulation 651/2014 as last amended]
[model knowledge — verify current aid maps and regional aid ceilings]

> **DRAFT** — For review by a state aid lawyer before any communication to the member state. Not an official Commission position.

---

## Knowledge Reference

Commission Regulation (EU) 651/2014 (GBER — General Block Exemption), as amended
by Regulations 2017/1084, 2020/972, 2021/1237, 2023/1315 (Climate GBER);
Commission Regulation (EU) 2023/2831 (De Minimis — replaces 1407/2013);
Commission Regulation (EU) 2022/2472 (ABER — agricultural block exemption);
Art. 107(1)–(3) TFEU (state aid legal framework); Art. 108(3) TFEU (standstill
obligation — no implementation before notification and approval);
DG COMP State Aid Manual of Procedures; SANI2 registration system;
State Aid Transparency Public Search (SA register); Commission Regional Aid
Guidelines 2022 (RAG); R&D&I Framework 2022; GBER firm-in-difficulty definition
(Art. 2(18) — balance sheet test); Commission Notice on Notion of State Aid
(2016/C 262/01).
