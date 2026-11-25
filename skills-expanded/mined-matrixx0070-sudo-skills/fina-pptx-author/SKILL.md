---
name: fina-pptx-author
version: 1.0.0
description: Authors a finance presentation from scratch, building the storyline (SCQA / pyramid), writing action-titles that state each slide's takeaway, selecting the right exhibit per message, and sourcing every exhibit into a clean, defensible deck.
author: matrixx0070
tags: [finance, investment-banking, presentation, storyline, action-titles, exhibits, pptx-author]
capabilities: []
---

# Finance Presentation Author

## When to use
Use this to build a new finance deck from a blank file: pitch, board, strategy, or committee materials where you need to construct the storyline, write the slides, choose the exhibits, and source them. This is the authoring workflow that turns finished analysis into a persuasive, defensible deck.

**Not for:** creating the reusable template/master (use fina-ppt-template-creator first), refreshing an existing deck to current data (use fina-deck-refresh), or the final proofing pass (use fina-ib-check-deck). The numbers must already exist — build them in fina-comps-analysis, fina-dcf-model, or fina-3-statement-model, and their tables in fina-xlsx-author, before you author slides on top.

## Method
1. **Start from the template, not a blank slide.** You open the fina-ppt-template-creator master so every slide inherits layouts, styles, and the source band before you write a word.
2. **Write the storyline before any slide.** You draft the argument as SCQA (Situation, Complication, Question, Answer) and lay the supporting points out as a pyramid — the answer on top, grouped MECE arguments beneath. Decision point: if you cannot state the deck's single governing answer in one sentence, you stop and resolve the thesis before building slides.
3. **Convert the pyramid to a slide flow.** You map each pyramid node to one slide so the horizontal logic (reading only the titles top to bottom) already tells the story.
4. **Write action titles.** You title each slide with its takeaway, not its topic — "Margin expansion drives 60% of value creation," not "Margins." Each title is a full assertion the exhibit below proves.
5. **Enforce one message per slide.** You keep each slide to a single argument; if a slide carries two messages, you split it. Decision point: if an exhibit needs more than one takeaway to explain, you either split the slide or demote the detail to the appendix.
6. **Select the right exhibit.** You choose the visual that fits the message — table for precise values and comparisons across many metrics, chart for trends, composition, or distribution — matching message type to exhibit type deliberately.
7. **Source every exhibit.** You add a source footnote with provider and as-of date to every data slide as you build it, so the deck is defensible before it reaches fina-ib-check-deck.
8. **Write the executive summary last.** You distill the pyramid's top level into a one-page executive summary that stands alone.
9. **Impose appendix discipline.** You move supporting detail, methodology, and backup exhibits to a clearly separated appendix, keeping the main body tight.
10. **Hand off for QC.** You pass the completed deck to fina-ib-check-deck for the deck-check before it goes out.

## Example
You author a sell-side pitch. SCQA: Situation — the target holds #2 share in a growing niche; Complication — organic growth is decelerating; Question — how does it re-rate and who pays for it; Answer — a strategic acquirer captures $180mm of synergies justifying a 30% premium. The one-sentence answer passes the decision-point gate. The pyramid's three groups (market position, synergy case, valuation) become three sections. A slide arguing peers trade up on scale gets the action title "Scale leaders command a 3x turn premium" over an EV/EBITDA-vs-revenue scatter (trend + relationship → chart, not table). The valuation slide uses a football-field bar (range comparison → chart), while the synergy build uses a table (precise, multi-line values). Every exhibit gets a source line as built. You write the one-page exec summary last, push the sensitivity detail to the appendix, and hand off to fina-ib-check-deck.

## Pitfalls
- **Topic titles.** "Revenue" as a title makes the reader do the work; state the takeaway so the title flow alone tells the story.
- **Two messages per slide.** Cramming two arguments onto one slide buries both; split or demote to appendix.
- **Slides before storyline.** Building slides before the SCQA/pyramid produces a deck that lists facts instead of arguing; write the logic first.
- **Wrong exhibit type.** A table where a trend chart belongs (or vice versa) hides the message; match exhibit to message type.
- **Unsourced exhibits.** Skipping the source line at authoring time guarantees a scramble later; source as you build.
- **Bloated body.** Leaving backup detail in the main flow dilutes the argument; enforce appendix discipline.
- **Non-MECE grouping.** Overlapping or gappy argument groups weaken the pyramid; make groups mutually exclusive and collectively exhaustive.

## Output format
```
DECK PLAN — Project Vantage Sell-Side Pitch
STORYLINE (SCQA)
  S: Target holds #2 share in a growing niche
  C: Organic growth is decelerating
  Q: How does it re-rate, and who pays?
  A: Strategic acquirer captures $180mm synergies -> 30% premium justified

PYRAMID -> SLIDE FLOW (action titles)
  Sec 1  Market position
    1  "Target owns #2 share of a market growing 12% p.a."   [chart: share trend]
  Sec 2  Synergy case
    2  "$180mm of run-rate synergies are actionable in 24 months" [table: synergy build]
  Sec 3  Valuation
    3  "Scale leaders command a 3x turn premium"             [chart: EV/EBITDA scatter]
    4  "Precedents support a 30% control premium"            [chart: football field]

EXEC SUMMARY: one page, top of pyramid, stands alone (written last)
APPENDIX: sensitivity tables, methodology, detailed comps
SOURCING: every exhibit carries provider + as-of date
NEXT: hand to fina-ib-check-deck
```

## Reference

### Storyline frameworks
| Framework | Structure | Use |
| --- | --- | --- |
| SCQA | Situation, Complication, Question, Answer | Opening / setting up the argument |
| Pyramid (Minto) | Answer on top, MECE groups beneath, data at base | Organizing the whole deck's logic |
| Governing thought | One sentence the deck exists to prove | Gate before building any slide |
| Horizontal logic | Titles read top-to-bottom tell the story alone | QC the flow |
| Vertical logic | Each slide's exhibit proves its own title | QC each slide |

### Action-title rules
| Rule | Detail |
| --- | --- |
| Assertion not topic | Title states the takeaway, not the subject |
| One claim | Exactly one message per title |
| Provable | The exhibit below proves the title |
| Specific | Prefer numbers ("3x turn premium") over adjectives |
| Consistent tense | Present tense, parallel structure across the deck |

### Exhibit choice by message
| Message | Exhibit |
| --- | --- |
| Trend over time | Line chart |
| Composition / mix | Stacked bar or 100% stacked |
| Ranking / comparison | Bar chart |
| Relationship / two variables | Scatter |
| Valuation range | Football field (floating bars) |
| Precise multi-metric values | Table |
| Bridge / driver decomposition | Waterfall |
| Single headline figure | Big number / callout |

### Slide-anatomy checklist
| Element | Requirement |
| --- | --- |
| Action title | One provable takeaway |
| Exhibit | Right type for the message |
| Source line | Provider + as-of date |
| One message | No second argument on the slide |
| Page number | Present and correct |
| Template fidelity | Uses fina-ppt-template-creator layouts |

### Sourcing conventions
| Item | Convention |
| --- | --- |
| Format | "Source: <provider>, as of <date>" on every exhibit |
| Financials | Cite the model and period |
| Market data | Cite provider and single close date |
| Comps | Cite fina-comps-analysis and peer set date |
| Estimates | Label as estimates and cite basis |
