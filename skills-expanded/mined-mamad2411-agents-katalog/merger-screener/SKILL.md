---
name: merger-screener
description: >
  Use when assessing a concentration (merger, acquisition, or joint venture) under
  Council Regulation (EC) No 139/2004 (EU Merger Regulation — EUMR). Covers: EU
  jurisdictional thresholds (Arts. 1–2 EUMR), the SIEC test (significant impediment
  to effective competition), horizontal and non-horizontal merger analysis, market
  definition for concentrations, Phase I (25 working days) and Phase II (90 working
  days) procedure, simplified procedure eligibility, pre-notification contacts, Article
  6(1)(c) and Article 8 decisions, remedies design (structural vs. behavioural), and
  the referral system between the Commission and national competition authorities
  (Arts. 4(4), 4(5), 9, 22 EUMR). Distinct from lawyer-competition-antitrust and
  market-definer — those handle Art. 101/102 analysis; this skill handles merger
  control exclusively.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-competition-merger
  triggers: >
    merger, acquisition, concentration, joint venture, EUMR, EU Merger Regulation,
    Regulation 139/2004, merger control, merger notification, Phase I, Phase II,
    SIEC test, significant impediment effective competition, horizontal merger,
    non-horizontal merger, vertical merger, conglomerate merger, market share HHI,
    Herfindahl-Hirschman Index, merger remedies, structural remedy, divestiture,
    behavioural remedy, simplified procedure, pre-notification, Art. 6(1)(b),
    Art. 6(1)(c), Art. 8(2), Art. 8(3) EUMR, referral NCA, Art. 9, Art. 22,
    gun-jumping, notification threshold, combined market share, coordinated effects,
    unilateral effects, merger clearance, merger prohibition
  role: specialist
  scope: merger-control-eumr
  output-format: jurisdiction-assessment, siec-analysis, remedies-note, phase-assessment
  institution: European Commission / DG COMP
  related-skills: market-definer, lawyer-competition-antitrust, lawyer-legal-service, state-aid-review
---

# Merger Screener — European Commission / DG COMP

Senior DG COMP merger case handler specialising in the assessment of concentrations
under the EU Merger Regulation. Applies the SIEC test with the precision required by
the General Court: unilateral and coordinated effects must be distinguished; market
definition precedes competition analysis; remedies must be structural where possible
and precisely scoped to eliminate the identified competitive harm. Every assessment
runs from jurisdiction to decision — no shortcuts on thresholds, no conflation of
merger control with antitrust.

---

## Core Workflow

1. **Jurisdictional assessment** — Verify whether the concentration has an EU dimension:
   - **Standard thresholds** (Art. 1(2) EUMR): combined worldwide turnover > €5bn AND
     EU-wide turnover of each of at least two parties > €250m — unless each achieves
     more than 2/3 of its EU turnover in the same member state
   - **Alternative thresholds** (Art. 1(3) EUMR): combined worldwide > €2.5bn AND
     combined turnover in each of ≥3 MS > €100m AND each party > €25m in each of those
     MS AND EU-wide turnover of each of ≥2 parties > €100m — with same 2/3 rule
   - If no EU dimension: refer to national authorities; advise on Art. 4(5) voluntary
     referral to Commission if the concentration affects ≥3 MS

2. **Simplified procedure eligibility** — Before full assessment, check whether the
   simplified procedure applies (Commission Notice on simplified procedure):
   - Horizontal overlap: combined market share < 20%
   - Vertical relationship: individual or combined market share < 30%
   - No horizontal/vertical relationship (pure conglomerate)
   - JV with no EU-scope activities or turnover below de minimis

3. **Market definition** — Apply the SSNIP test (see `market-definer` skill for depth):
   - Define the relevant product market and geographic market
   - This determines the market shares that drive the SIEC analysis

4. **SIEC analysis — Horizontal mergers**:
   - **Unilateral effects**: Post-merger combined market share and HHI delta;
     presumption of concern if combined share > 50% (C-413/14 *Intel*);
     significant concern if HHI post-merger > 2000 and delta > 150
   - **Coordinated effects**: assess whether the merger makes coordination easier,
     more stable, or more effective — oligopolistic market structure, transparency,
     retaliation mechanisms
   - **Countervailing factors**: buyer power, entry/expansion barriers, efficiencies
     (must be merger-specific, verifiable, and passed on to consumers)

5. **SIEC analysis — Non-horizontal mergers** (vertical/conglomerate):
   - **Vertical**: input/customer foreclosure risk; assess ability and incentive
     to foreclose; net effect on competition
   - **Conglomerate**: portfolio effects, tying/bundling risk; very high legal
     threshold for prohibition (Commission v Tetra Laval)

6. **Remedies assessment** — Where a SIEC is identified:
   - **Structural remedies** (preferred): divestiture of a business unit or assets;
     the Commission's Remedies Notice specifies conditions for acceptability
   - **Behavioural remedies**: access obligations, licensing, interoperability — less
     favoured; only where structural remedies are disproportionate
   - Assess whether the proposed remedy eliminates the competitive harm identified
   - Fix-it-first vs. upfront buyer conditions

7. **Phase I / Phase II decision pathway**:
   - Phase I (25 working days from complete notification): Art. 6(1)(b) clearance /
     Art. 6(1)(c) initiation of Phase II / Art. 6(2) conditional clearance with remedies
   - Phase II (90 working days, extendable to 105): Art. 8(1) clearance / Art. 8(2)
     conditional clearance / Art. 8(3) prohibition

---

## Jurisdictional Threshold Calculator

EU MERGER REGULATION — JURISDICTIONAL ASSESSMENT
Transaction:      [Target / Acquirer / JV structure]
Date assessed:    [DD Month YYYY]
Assessed by:      [Name / unit]

---

### Art. 1(2) EUMR — Standard Thresholds

Combined worldwide turnover of all parties:        €[X]bn   > €5bn?   - [ ] YES  - [ ] NO
EU-wide turnover — Party A:                        €[X]m    > €250m?  - [ ] YES  - [ ] NO
EU-wide turnover — Party B:                        €[X]m    > €250m?  - [ ] YES  - [ ] NO
2/3 rule — does each party achieve > 2/3 of EU
  turnover in the SAME member state?               - [ ] YES (no EU dimension) - [ ] NO

Art. 1(2) EU dimension:  - [ ] YES  - [ ] NO → check Art. 1(3)

---

### Art. 1(3) EUMR — Alternative Thresholds (if Art. 1(2) not met)

Combined worldwide turnover:                        €[X]bn   > €2.5bn? - [ ] YES  - [ ] NO
In each of ≥3 MS, combined turnover of all parties: €[X]m    > €100m?  - [ ] YES  - [ ] NO
In each of those ≥3 MS, each party individually:    €[X]m    > €25m?   - [ ] YES  - [ ] NO
EU-wide turnover — Party A:                         €[X]m    > €100m?  - [ ] YES  - [ ] NO
EU-wide turnover — Party B:                         €[X]m    > €100m?  - [ ] YES  - [ ] NO
2/3 rule — same member state?                        - [ ] YES (no EU dimension) - [ ] NO

Art. 1(3) EU dimension:  - [ ] YES  - [ ] NO → no EU-level notification obligation

---

### Conclusion

- [ ] EU dimension confirmed → mandatory Commission notification (Art. 4(1) EUMR)
  Standstill obligation: gun-jumping risk if transaction completes before clearance
- [ ] No EU dimension → national NCA filings required: [list affected MS]
  Art. 4(5) voluntary referral to Commission possible if ≥3 MS have jurisdiction
- [ ] Simplified procedure likely:  - [ ] YES  - [ ] NO  - [ ] Unclear pending market definition

Gun-jumping risk assessment:
  Is the transaction (or any preparatory step) capable of changing competitive dynamics
  before Commission clearance?  - [ ] YES [flag — Art. 14(2)(b) EUMR fine risk]  - [ ] NO

[model knowledge — verify current EUMR thresholds; verify current simplified procedure notice]

---

## SIEC Analysis Template

SIEC ASSESSMENT — HORIZONTAL CONCENTRATION
Case ref:        M.[NNNNN] — [Transaction name]
Market:          [Relevant product market] / [Geographic market]
Post-merger combined share: [X%]   HHI post-merger: [X]   HHI delta: [X]

---

### Market Structure

Party A market share:    [X%]   Party B market share:    [X%]
Combined:                [X%]   Next competitor:         [X%]
Market concentration:    - [ ] Low (HHI < 1000)  - [ ] Moderate (1000–2000)  - [ ] High (> 2000)

Safe harbours (Horizontal Merger Guidelines §§ 19-21):
- Combined share < 25%?  - [ ] YES → unlikely to raise concerns
- HHI < 1000?            - [ ] YES → unlikely regardless of delta

---

### Unilateral Effects

Are the merging parties close competitors?          - [ ] YES  - [ ] NO  [evidence]
Diversion ratio (if available):                     [X%] — indicates strength of rivalry
Can customers switch to remaining competitors?      - [ ] YES (countervailing buyer power)
Barriers to entry/expansion:                        - [ ] High  - [ ] Medium  - [ ] Low
Unilateral effects concern:   - [ ] None  - [ ] Possible  - [ ] Serious [explain]

---

### Coordinated Effects

Oligopolistic market structure post-merger?         - [ ] YES  - [ ] NO
Market transparency (price, volume observable)?     - [ ] YES  - [ ] NO
Retaliation mechanism credible?                     - [ ] YES  - [ ] NO
Coordinated effects concern:  - [ ] None  - [ ] Possible  - [ ] Serious

---

### Countervailing Factors

Efficiencies claimed:  - [ ] YES → are they merger-specific, verifiable, pro-consumer? [assess]
Buyer power:           - [ ] Significant  - [ ] Moderate  - [ ] None
Entry/expansion:       - [ ] Timely, likely, sufficient to constrain  - [ ] NOT sufficient

---

### Overall SIEC Assessment

- [ ] No SIEC — clearance Art. 6(1)(b) / Art. 8(1)
- [ ] SIEC identified in market [X] — remedies required for clearance
- [ ] Serious doubts — Phase II initiation Art. 6(1)(c)
- [ ] SIEC — likely prohibition Art. 8(3) absent fundamental remedy

Remedies required:  - [ ] Structural (divestiture of [business/assets])
                    - [ ] Behavioural [describe — justify departure from structural preference]
                    - [ ] None

[EUR-Lex — verify current EUMR thresholds and Horizontal Merger Guidelines]
[CJEU — verify case references: M.7000 UPS/TNT; T-399/16 CK Hutchison; C-553/10P Cisco]
[review — political judgement required for remedies acceptance/rejection]

---

## Constraints

### MUST DO
- **Run market definition before SIEC analysis** — market shares are meaningless
  without a defined relevant market; never assert a combined share figure without
  identifying the product and geographic market it relates to.
- **Distinguish unilateral from coordinated effects** — they require different factual
  analyses and different remedies; conflating them produces an analytically weak case.
- **Respect the standstill obligation** — Art. 7 EUMR prohibits implementation before
  clearance; gun-jumping (any step that changes competitive reality pre-clearance) is
  a separate infringement subject to fines up to 10% of turnover.
- **Apply the simplified procedure where eligible** — failing to use the simplified
  procedure where conditions are met delays clearance and wastes resources.

### MUST NOT DO
- **Apply the dominance test (pre-2004)** — the EU has applied the SIEC test since
  2004; assessing only whether the merged entity will be dominant is legally insufficient
  and will produce wrong results for non-dominant concentrations with coordinated effects.
- **Treat behavioural remedies as equivalent to structural** — the Commission's
  Remedies Notice expresses a clear preference for structural remedies; proposing
  behavioural remedies where divestiture is feasible will be challenged in Phase II.
- **Conflate merger control with antitrust** — the EUMR provides a standalone legal
  framework; Art. 101/102 TFEU do not apply to concentrations within the EUMR's scope.

---

## Key Legal Framework

| Instrument | Subject | Key Provision |
|---|---|---|
| Regulation (EC) 139/2004 (EUMR) | EU merger control | Arts. 1–2 (jurisdiction); Art. 6 (Phase I); Art. 8 (Phase II); Art. 7 (standstill) |
| Commission Horizontal Merger Guidelines | SIEC analysis — horizontal | Safe harbours, unilateral/coordinated effects, efficiencies |
| Commission Non-Horizontal Merger Guidelines | Vertical and conglomerate | Foreclosure, portfolio effects |
| Commission Remedies Notice | Remedies design | Structural vs. behavioural; fix-it-first; upfront buyer |
| CJEU / GC case law | SIEC standard | T-399/16 CK Hutchison; C-553/10P Cisco/Impax; T-691/14 Servier |

[EUR-Lex — verify current version] [CJEU — verify Curia reference]

---

> **DRAFT** — For review by a Competition lawyer or Legal Service lawyer before use. Not an official Commission position.
