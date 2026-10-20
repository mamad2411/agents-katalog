---
name: qmv-calculator
description: >
  Calculate Qualified Majority Voting (QMV) outcomes for the Council of the EU.
  Given a dossier and a set of member-state positions (supporting, opposing, or
  abstaining), determines whether a qualified majority is available, whether a
  blocking minority has formed, which swing states are decisive, and what
  coalition-building strategy the Presidency should pursue. Also handles Enhanced
  QMV (second reading), unanimity checks, and simple majority (procedural votes).
  Use as a standalone arithmetic tool or chain it from council-eu, coreper, or
  council-presidency when precise vote arithmetic is needed.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-simulation
  triggers: >
    QMV, qualified majority voting, blocking minority, vote arithmetic, Council vote,
    member state positions, population threshold, 55% threshold, 65% population,
    enhanced QMV, second reading Council, unanimity check, simple majority Council,
    swing states, coalition building, Council adoption, vote count, QMV calculator,
    Art. 16 TEU, Art. 238 TFEU, Council decision-making, vote simulation
  role: specialist
  scope: qmv-arithmetic
  output-format: qmv-assessment
  institution: Council of the European Union
  related-skills: council-eu, coreper, council-presidency, timeline, subsidiarity-stress
---

# QMV Calculator — Council of the EU

Precision vote arithmetic for Council of the EU decisions under Qualified Majority
Voting. QMV is not a simple head count: a proposal can have a majority of member
states and still fail on population grounds, or have population support without
enough states. The blocking minority threshold (4 states representing >35% of
population) creates asymmetric dynamics — three large states (DE, FR, IT) cannot
alone form a blocking minority on population grounds without a fourth state, but
DE + FR alone control ~33% of EU population, making them near-indispensable for
blocking if they align.

This skill runs vote arithmetic with full 27-member-state population data, models
abstentions correctly (an abstention counts against the 55% state threshold but
not against the 65% population threshold), and identifies the minimum winning
coalition and minimum blocking minority for any given dossier.

---

## Voting Rules Reference

```
QUALIFIED MAJORITY VOTING (Art. 16(4) TEU + Art. 238(3)(a) TFEU):
  State threshold:      ≥ 55% of member states  = ≥ 15 of 27
  Population threshold: ≥ 65% of EU population  ≈ ≥ 294M of 452M
  BOTH thresholds must be met simultaneously.

  ABSTENTIONS: count against the 55% state threshold (an abstaining MS is not
    "in favour") but do NOT reduce the denominator for the population threshold
    (population of abstaining MS still counts in the total EU population base).
    A vote can fail on state threshold alone even with population support.

BLOCKING MINORITY (Art. 16(4) TEU):
  ≥ 4 member states representing > 35% of EU population (> 158M)
  A blocking minority MUST include at least 4 states — 3 large states cannot
  form a blocking minority regardless of their combined population share.

ENHANCED QMV (Art. 238(2) TFEU — Council acting NOT on Commission/HR/VP proposal):
  State threshold:      ≥ 72% of member states  = ≥ 20 of 27
  Population threshold: ≥ 65% of EU population
  Used for: Council amendments to Commission proposal (unanimity required
    instead if Commission has not modified — Art. 293(1) TFEU); certain
    Council measures without Commission initiative.

SIMPLE MAJORITY (Art. 238(1) TFEU):
  > 50% of member states = ≥ 14 of 27
  Used for: procedural decisions, Rules of Procedure, referral to European Council.
  No population threshold.

UNANIMITY:
  All 27 member states in favour; abstentions do not prevent unanimity (Art. 238(4) TFEU).
  Abstaining MS is bound by the decision.
  Used for: CFSP, taxation, constitutional matters, some JHA, own resources.
  A single NO vote blocks.
```

---

## Population Reference Table (approximate — 2024 figures)

```
Member State    Population (M)    % of EU (452M)
─────────────────────────────────────────────────
Germany (DE)       83.8              18.5%
France (FR)        68.4              15.1%
Italy (IT)         58.9              13.0%
Spain (ES)         48.6              10.7%
Poland (PL)        36.8               8.1%
Romania (RO)       19.1               4.2%
Netherlands (NL)   17.9               4.0%
Belgium (BE)       11.6               2.6%
Czech Republic (CZ) 10.8              2.4%
Sweden (SE)        10.5               2.3%
Portugal (PT)      10.4               2.3%
Greece (GR)        10.4               2.3%
Hungary (HU)        9.7               2.1%
Austria (AT)        9.1               2.0%
Bulgaria (BG)       6.5               1.4%
Denmark (DK)        5.9               1.3%
Finland (FI)        5.6               1.2%
Slovakia (SK)       5.5               1.2%
Ireland (IE)        5.1               1.1%
Croatia (HR)        3.9               0.9%
Lithuania (LT)      2.9               0.6%
Slovenia (SI)       2.1               0.5%
Latvia (LV)         1.8               0.4%
Estonia (EE)        1.4               0.3%
Cyprus (CY)         0.9               0.2%
Luxembourg (LU)     0.7               0.2%
Malta (MT)          0.5               0.1%
─────────────────────────────────────────────────
EU TOTAL           452.0M            100%
QMV population threshold (65%): ≥ 293.8M
Blocking minority pop. threshold (35%): > 158.2M
```

---

## Core Workflow

1. **Establish the voting rule** — confirm which rule applies:
   - Standard QMV (Art. 16(4) TEU): OLP first and second reading, most legislative acts
   - Enhanced QMV (Art. 238(2) TFEU): Council acting without Commission proposal
   - Unanimity: taxation, CFSP, constitutional matters — list the legal basis
   - Simple majority: procedural decisions

2. **Map member-state positions** — classify each of the 27 MS as:
   - **YES**: supports adoption (counts toward 55% state + 65% population thresholds)
   - **NO**: opposes adoption (counts toward blocking minority if ≥4 and >35% pop.)
   - **ABSTAIN**: neither yes nor no (counts against 55% state threshold; population
     still in the denominator; abstaining MS is bound by the decision if adopted)
   - **UNKNOWN**: position not yet determined — model scenarios

3. **Calculate state threshold** — count YES votes:
   - ≥ 15 YES: state threshold met
   - < 15 YES: state threshold not met (check if abstentions are preventing it)

4. **Calculate population threshold** — sum population of YES member states:
   - ≥ 293.8M in YES column: population threshold met
   - < 293.8M: population threshold not met

5. **Check blocking minority** — count NO votes and their combined population:
   - ≥ 4 NO states AND combined population > 158.2M: blocking minority formed
   - < 4 NO states OR combined population ≤ 158.2M: no blocking minority
   - Note: 3 large states (e.g. DE + FR + IT = 211M) cannot alone form a blocking
     minority regardless of population share — the 4-state floor is absolute

6. **Identify swing states** — which UNKNOWN or ABSTAIN states are pivotal:
   - Which states, if moved to YES, would clear both thresholds?
   - Which states, if moved to NO, would form a blocking minority?
   - These are the Presidency's priority for bilateral pre-cooking

7. **Coalition strategy** — based on the arithmetic, recommend:
   - Minimum winning coalition (fewest states needed to clear both thresholds)
   - Maximum pressure scenario (largest YES coalition achievable)
   - Blocking minority prevention strategy (which NO states must be separated)

---

## Abstention Mechanics (Often Misunderstood)

An abstention in the Council of the EU is not a neutral act. Under Art. 238(4) TFEU,
an abstaining member state is **bound by the decision** if it is adopted — abstention
is not equivalent to voting no on the outcome, but it is equivalent to voting no on
the state-count threshold.

A practical consequence: a Presidency facing a borderline 55% state count will
sometimes prefer to have a hesitant delegation vote NO rather than ABSTAIN, if the
NO vote does not contribute to a blocking minority (i.e., there are fewer than 3
other NO states or the combined population of NO states is below 35%). This is rare
but occurs when the Presidency wants the decision to be politically clean.

---

## Common Blocking Minority Scenarios

```
SCENARIO 1 — Large-state alignment (most common):
  DE + FR + any 2 others with combined pop > 35%
  DE (18.5%) + FR (15.1%) = 33.6% → need ~1.6% more (e.g. IT, ES, PL)
  DE + FR + IT = 46.6% → well above 35%; 3 states NOT sufficient (need 4th)
  DE + FR + IT + any 1 = blocking minority on population; depends on 4th state

SCENARIO 2 — Eastern bloc alignment:
  PL + RO + CZ + HU = 17.8% — well below 35% population
  Eastern bloc of 4 cannot form a blocking minority on population grounds alone
  BUT they can block on state threshold if they attract 11 more NO votes (total 15)

SCENARIO 3 — Mixed:
  DE/FR + eastern bloc: if DE/FR + PL + RO = 45.9%; add 1 more large MS → >35%
  This is structurally the most dangerous blocking coalition for the Commission

SCENARIO 4 — Small-state majority without large-state support:
  Many small states can achieve 15/27 state threshold but fail on 65% population
  Politically possible to have 18 small states in YES and still fail QMV
```

---

## Constraints

### MUST DO
- **Apply both thresholds simultaneously** — a result that meets the state threshold
  but not the population threshold (or vice versa) is a QMV failure; the proposal
  is not adopted; flag which threshold is blocking
- **Apply the 4-state floor on blocking minority** — no matter how large their
  combined population, 3 states cannot form a blocking minority; this is a hard
  treaty rule (Art. 16(4) TEU); model it correctly
- **Treat abstentions correctly** — abstentions count against the 55% state threshold
  but not against the population denominator; do not add abstaining states' population
  to the YES column; the abstaining state is counted in the total EU population base
- **Check the voting rule before calculating** — QMV thresholds differ for standard
  QMV (55%/65%), enhanced QMV (72%/65%), and unanimity (100%/no pop. threshold);
  the legal basis determines which applies
- **Flag ioannina-style requests** — if a near-blocking minority (close to but below
  35% population or fewer than 4 states) requests additional deliberation time, the
  Presidency should take note; this is a political signal even when not legally
  binding

### MUST NOT DO
- **Do not treat a QMV calculation as final** — member-state positions shift;
  label all calculations as based on stated or modelled positions at a given point
  in time; flag which positions are confirmed vs. estimated
- **Do not confuse Council of the EU QMV with European Council** — the European
  Council (heads of state) uses different rules; European Council acts by consensus
  or unanimity (Art. 15(4) TEU); QMV in the European Council is the exception,
  not the rule

---

## Output Template

QMV ASSESSMENT — [DOSSIER TITLE]
Legal basis: [TFEU Art. X]
Voting rule: [Standard QMV / Enhanced QMV / Unanimity / Simple majority]
Date of assessment: [DD Month YYYY]

---

### Member State Position Map

| MS  | Position | Population (M) | Notes |
|-----|----------|---------------|-------|
| DE  | [YES/NO/ABSTAIN/UNKNOWN] | 83.8 | [any specific note] |
| FR  | [YES/NO/ABSTAIN/UNKNOWN] | 68.4 | |
| IT  | [YES/NO/ABSTAIN/UNKNOWN] | 58.9 | |
| ES  | [YES/NO/ABSTAIN/UNKNOWN] | 48.6 | |
| PL  | [YES/NO/ABSTAIN/UNKNOWN] | 36.8 | |
| RO  | [YES/NO/ABSTAIN/UNKNOWN] | 19.1 | |
| NL  | [YES/NO/ABSTAIN/UNKNOWN] | 17.9 | |
| BE  | [YES/NO/ABSTAIN/UNKNOWN] | 11.6 | |
| CZ  | [YES/NO/ABSTAIN/UNKNOWN] | 10.8 | |
| SE  | [YES/NO/ABSTAIN/UNKNOWN] | 10.5 | |
| PT  | [YES/NO/ABSTAIN/UNKNOWN] | 10.4 | |
| GR  | [YES/NO/ABSTAIN/UNKNOWN] | 10.4 | |
| HU  | [YES/NO/ABSTAIN/UNKNOWN] |  9.7 | |
| AT  | [YES/NO/ABSTAIN/UNKNOWN] |  9.1 | |
| BG  | [YES/NO/ABSTAIN/UNKNOWN] |  6.5 | |
| DK  | [YES/NO/ABSTAIN/UNKNOWN] |  5.9 | |
| FI  | [YES/NO/ABSTAIN/UNKNOWN] |  5.6 | |
| SK  | [YES/NO/ABSTAIN/UNKNOWN] |  5.5 | |
| IE  | [YES/NO/ABSTAIN/UNKNOWN] |  5.1 | |
| HR  | [YES/NO/ABSTAIN/UNKNOWN] |  3.9 | |
| LT  | [YES/NO/ABSTAIN/UNKNOWN] |  2.9 | |
| SI  | [YES/NO/ABSTAIN/UNKNOWN] |  2.1 | |
| LV  | [YES/NO/ABSTAIN/UNKNOWN] |  1.8 | |
| EE  | [YES/NO/ABSTAIN/UNKNOWN] |  1.4 | |
| CY  | [YES/NO/ABSTAIN/UNKNOWN] |  0.9 | |
| LU  | [YES/NO/ABSTAIN/UNKNOWN] |  0.7 | |
| MT  | [YES/NO/ABSTAIN/UNKNOWN] |  0.5 | |

---

### QMV Arithmetic

YES votes:     [N] states / 27   → [X.X%]   Threshold: ≥ 55% (≥15)  → [MET / NOT MET]
YES population: [XXX.X]M / 452M  → [X.X%]   Threshold: ≥ 65%        → [MET / NOT MET]
ABSTAIN:       [N] states — counted against state threshold; population in denominator

NO votes:      [N] states        → [X.X%]
NO population: [XXX.X]M          → [X.X%]   Blocking minority (>35%, ≥4 MS): [YES / NO]

─────────────────────────────────────────────────────────────
RESULT: [ADOPTED / NOT ADOPTED / BLOCKING MINORITY / INSUFFICIENT STATES /
         INSUFFICIENT POPULATION]
─────────────────────────────────────────────────────────────

---

### Swing State Analysis

States whose position is UNKNOWN or ABSTAIN and whose shift to YES would be decisive:
  [MS] (+[X.X]M population): [why decisive — moves state count / population over threshold]
  [MS] (+[X.X]M population): [why decisive]

States whose shift to NO would form or complete a blocking minority:
  [MS] ([X.X]M): [current position — why pivotal for blocking minority]

---

### Coalition Strategy

Minimum winning coalition (fewest additional YES votes needed):
  Current YES + [MS list]: [N] states / [XXX.X]M — clears both thresholds

Maximum achievable YES coalition (optimistic scenario):
  [MS list] → [N] states / [XXX.X]M

Blocking minority prevention priority:
  The Presidency should focus on separating: [MS] from the NO bloc
  Reason: [population arithmetic — losing this state drops NO population below 35%
           OR reduces NO states below 4]

Recommended Presidency action:
  [ ] QMV available — recommend A-point or call vote
  [ ] QMV marginal — pre-cook bilaterally with [MS list] before calling vote
  [ ] Blocking minority present — do not call vote; continue compromise text discussions
  [ ] Unanimity required and not available — flag to ministers

[model knowledge — verify current member-state populations and dossier-specific
political positions]

> **DRAFT** — Simulation output. Not an official Council position.
