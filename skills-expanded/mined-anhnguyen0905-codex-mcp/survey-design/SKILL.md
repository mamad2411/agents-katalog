---
name: survey-design
description: Design surveys and questionnaires that produce usable data — question wording, leading and double-barrelled and loaded questions, Likert and bipolar response scales, don't-know and neutral options, question order and priming, screening and quota questions, sample size and representativeness, translation equivalence, pilot testing, response bias (acquiescence, social desirability, satisficing, straightlining), and designing the instrument so cross-tabs and significance testing remain possible.
---

# Survey Design (questionnaire construction for analysable data)

## Design backwards from the analysis

Write the analysis plan before the questions. For each intended output — a cross-tab, a segment
comparison, a tracked trend — name the variable that produces it; if no question yields it at the
needed granularity, the instrument blocks the analysis and fieldwork cannot repair it.

```
Per question, record: variable name | type (nominal/ordinal/interval)
                      | analysis it feeds | breakdown it must survive
```

## Question types and when each fits

- **Single-choice (nominal)** — mutually exclusive, exhaustive; add "other (specify)" unless closed.
- **Multi-select** — co-occurring behaviours; cannot be averaged, so analyse per-option incidence
  and randomise option order against primacy.
- **Ordinal rating** — intensity or agreement; means are defensible only if you state the
  equal-interval assumption, otherwise report distributions and medians.
- **Numeric** — counts and amounts, range-validated at entry. **Open text** — discovery and the
  *why*, costly to code, placed before the closed items it would prime. **Ranking** — lists of
  roughly ≤5 only. **Matrix/grid** — efficient, and the main cause of straightlining; keep short.

## Wording faults and response scales

**Leading** ("how much did you enjoy the update?") presupposes the answer — use a symmetric stem.
**Double-barrelled** ("fast and easy to use?") is two constructs and one answer — split it. **Loaded**
value-laden terms import the conclusion. **Assumptive** items ask about behaviour not yet
established — gate behind a filter. **Vague** periods ("regularly", "recently") mean something
different to each respondent — give a concrete window ("in the last 7 days"). Negated and
double-negated items cut comprehension; use few, only as acquiescence controls.

Likert measures agreement with a statement; bipolar (very dissatisfied → very satisfied) measures a
signed attitude — never mix them in one grid. Balance positive and negative points and label every
point verbally so the scale means the same thing in every language. A midpoint is legitimate for real
indifference but attracts satisficers: decide deliberately, keep it constant across waves. Offer
don't-know/N-A wherever a respondent may lack the knowledge, and keep it off the scale so it is never
averaged in. Changing a scale between waves ends the comparison.

## Order, screening, sample

Funnel general → specific; a specific item asked first contaminates the general one after it.
Screeners first, sensitive and demographic items last, order randomised within blocks and the served
order recorded. Screeners must not reveal the target profile, or respondents self-select in. Define
population, frame and the gap between them (coverage bias, which weighting only partly repairs). Size
from the smallest subgroup you will report on: 1,000 respondents with 40 in a key segment supports no
claim about that segment. Precision scales with √n. Non-response is not random — report the response
rate and compare respondent profile against known population marginals.

## Translation, bias, pilot

Translate the construct, not the words: back-translation, bilingual reconciliation, then a check that
scale labels carry equal intensity per locale — unequal intensity manufactures fake cross-country
differences. Acquiescence → balanced, occasionally reversed items. Social desirability → indirect
phrasing, anonymity, no interviewer. Satisficing/straightlining → shorter instrument, fewer grids,
attention checks. Recall error → short concrete periods. Then pilot on the real population: time it,
read verbatims, cognitively interview a few respondents, walk every routing path and quota, and
confirm one clean export column per variable.

## Failure modes

- Questions written to confirm a decision already taken; instrument so long that quality collapses in
  the back half, where the important items sit; age or spend captured in bands you cannot regroup.
- Significance tested on unweighted convenience samples and reported as fact; dozens of cross-tabs
  run and only the ones that "came out" reported; percentages on tiny bases with no n shown.

## Reviewer checklist

- [ ] Every question maps to a named analysis and a required breakdown
- [ ] No leading, loaded, double-barrelled, or assumptive items
- [ ] Scales balanced, fully labelled, midpoint decision deliberate and consistent across waves
- [ ] Don't-know/N-A offered where plausible and excluded from averages
- [ ] Screeners first, sensitive items last, blocks randomised, served order recorded, and every
      subgroup base size stated and adequate for the claim made
- [ ] Reference periods concrete ("last 7 days"), not "regularly" or "recently"
- [ ] Back-translation plus scale-label intensity check per locale
- [ ] Pilot run; routing, quotas and data export verified; trend items identical to prior wave

## Provenance

Standard questionnaire-design and survey-methodology practice (analysis-first design, wording faults,
balanced scales, order effects, response-style bias). All numeric guidance here — ranking list
length, subgroup base sizes, reference-period windows — is **derived, unverified** rule of thumb;
replace with the project's own measured values before treating as a target. No vendor benchmark or
published statistic is cited.
