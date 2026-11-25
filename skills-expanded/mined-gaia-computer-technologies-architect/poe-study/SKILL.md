---
name: poe-study
description: Designs and analyses a post-occupancy evaluation (POE) — occupant survey and interview guides, a walk-through observation protocol, and a framework for analysing returned survey data and any measured data into findings and lessons — keeping occupant-reported results separate from measured ones. Use when the architect wants a "POE", "post-occupancy evaluation", "occupant survey", "building in use study", "soft landings feedback", "lessons learned from a completed building", or to analyse survey results. Covers consent and ethics. Feeds findings back into design-brief and design-critique for the next project.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# POE Study

Post-occupancy evaluation asks whether the building works for the people in it, and whether it performs as intended. Few practices do it because it looks expensive; a light-touch POE (a short survey, a walk-through, a few interviews) is cheap and is the best design feedback an architect can get. The rule: keep what people say separate from what was measured, and never overclaim from a small sample.

## When to use

- Six to eighteen months after occupation (after a full seasonal cycle, where possible).
- At handover / soft-landings aftercare stages.
- When analysing survey data that has already been collected.
- Building a practice-wide lessons-learned record across projects.

## Input

- Building type, size, occupancy (number and kind of users), date of occupation.
- The original brief and design intent, so findings can be tested against them.
- Access: who can be surveyed or interviewed, client permission, any facilities-management contact.
- Available measured data, if any: energy and water meter readings, temperature / CO2 / humidity logging, daylight readings. Note the source and period for each.
- Returned survey data (CSV or spreadsheet), if at analysis stage.

## Process

### Design the study

1. **Set the questions.** Three to five things the study must answer, tied to the brief ("Does the atrium work as the social heart?", "Are the north studios comfortable in winter?").
2. **Pick the methods to match.** Light-touch: survey + walk-through + 4–8 interviews. Deeper: add environmental monitoring and meter analysis over a season.
3. **Write the survey.** Short (10–15 minutes). Cover the usual occupant-experience themes: overall satisfaction, thermal comfort (winter / summer), air quality, lighting and daylight, noise, space and layout, control over environment, amenity, perceived productivity or wellbeing, and open comments. Use consistent scales (e.g. 1–7) with anchored ends. Collect only the demographics needed to interpret results (e.g. location in building, hours present). Established POE survey instruments exist (e.g. BUS methodology, CBE occupant survey); if the practice wants benchmarkable results, recommend licensing one rather than imitating it.
4. **Write the interview guide.** Open questions in a sequence: arrival, daily routine, best and worst places, changes they have made, what they would change. Include building managers and cleaners, not only primary users.
5. **Write the walk-through protocol.** Route, what to observe at each stop (how spaces are actually used, adaptations, workarounds, signage added, furniture moved, blinds down), photo log, time of day.
6. **Ethics and consent.** Information sheet, voluntary participation, anonymity, data storage and retention, right to withdraw, and client permission. Follow the data-protection law that applies (e.g. GDPR in the EU/UK). Do not collect health data without a clear need and consent.

### Analyse

7. **Describe the sample first.** Responses / invited, response rate, and who is missing. Small samples (say, under 30) support description, not statistics; say so.
8. **Summarise each theme** with the counts and distribution, not just the mean. Show the basis: "Thermal comfort in winter: 14 of 22 respondents (64%) scored 1–3 on a 7-point scale (1 = too cold)."
9. **Code open comments** into themes; quote short anonymised examples.
10. **Set measured data alongside reported,** clearly labelled, and note where they agree or conflict. If measured data is compared with a target or design figure, state the target's source.
11. **Findings to lessons.** For each finding: what it means for this building (quick fixes, FM changes) and for the next design (brief, detail, specification).

## Domain knowledge

- **Reported vs measured.** People report comfort, not temperature. Both matter. Never present a survey result as a measured fact, or a single spot reading as typical performance.
- **Timing.** Avoid the first months (teething, unfamiliarity) and ideally capture both heating and cooling seasons.
- **Bias.** Self-selected respondents skew towards the unhappy and the very happy. Low response rates limit conclusions.
- **Performance gap.** Measured energy use often differs from design predictions; a finding, not an accusation. Report with the basis and leave diagnosis to the services engineer.
- **Feedback loop.** POE is only useful if lessons reach the next brief. Output a short "lessons for the practice" list in a form that can be filed.

## Output format

Design stage:
```
POE PLAN — [Building] — [date]
Questions to answer: [3–5]
Methods: [survey / walk-through / interviews / monitoring] — timing and effort
Survey: [question list with scales]
Interview guide: [questions]
Walk-through protocol: [route and observation checklist]
Consent and data: [information sheet points, storage, retention]
```

Analysis stage:
```
POE FINDINGS — [Building]
Sample: [n responses / n invited, response rate, who is missing]
| Theme | Reported (survey) | Measured (source, period) | Finding |
Key comments (anonymised): [ ]
Lessons — this building: [ ]
Lessons — next project: [ ]
Limits of this study: [ ]
```

## What you don't do

- Don't invent survey results, response counts, or measurements. Analyse only what is supplied.
- Don't present reported comfort as measured performance, or extrapolate from a small sample.
- Don't reproduce a licensed survey instrument verbatim; recommend licensing it.
- Don't diagnose services, structural, or building-physics faults. Report the finding and refer to the relevant engineer.
- Don't identify individual respondents in findings.
