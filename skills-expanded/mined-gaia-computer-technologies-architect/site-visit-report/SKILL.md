---
name: site-visit-report
description: Turns site photos, voice notes, and rough observations into a dated, numbered site visit report — weather, attendees, progress by area, observations, quality issues, actions, and a photo register — written as a record of what was seen, never as a certificate of quality or compliance. Use when the architect wants a "site report", "site visit notes", "write up my site visit", "inspection report", or "field report". Hands defects at completion to snag-list, contractor queries to rfi, and anything needing a formal instruction to contract-admin-letter.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Site Visit Report

The architect's site visit is periodic, not continuous. The report records what was observed on a given day, in the areas visited, and what follows from it. Its wording matters: it must never read as if the architect supervised, inspected everything, or approved the work.

## When to use

- After a site visit during construction, or a pre-start or pre-handover walk-round.
- When the architect has photos, voice memos, and scribbles and needs a clean, issued report.
- To keep a numbered series of reports consistent across a project.

## Input

- Photos (with filenames or timestamps) and any captions. If images can be viewed, describe what is visible; if not, use the architect's captions only.
- Voice-note transcript or written notes.
- Visit metadata: project, report number, date, time on site, weather, attendees, areas visited.
- Previous report's open items, if any.
- Programme position, if the architect knows it (e.g. "week 23 of 40, frame complete").

## Process

1. **Header.** Project, report number, date, time on and off site, weather and conditions as noted, attendees, areas visited. If weather or attendees were not given, mark "not recorded" rather than inventing.
2. **Scope statement.** One line: which areas were seen and which were not. "Visited: ground and first floor, east elevation scaffold. Not visited: roof, basement plant room." This protects the architect and is the most commonly omitted line.
3. **Previous items.** Status of open items from the last report: closed, ongoing, not inspected this visit.
4. **Progress by area.** Short factual description per area or trade: what stage it is at, as observed. No percentages unless the architect gives them; if given, say whose estimate it is.
5. **Observations.** Number each. For each: location, what was seen, photo reference, and the reason it matters (e.g. "does not appear to match detail A-521 rev B — insulation fixings at wider centres than shown"). Use "appears", "was observed", "not seen" language throughout.
6. **Classify.** Information / query / possible defect / health-and-safety observation. H&S items are reported to the contractor and principal contractor or equivalent; the architect does not manage site safety.
7. **Actions.** Owner and date for each. If an action requires the contractor to do work, flag that it may need a formal instruction (hand to `contract-admin-letter`) or an RFI response.
8. **Photo register.** Filename, observation number, short caption.

## Domain knowledge

- **Periodic visits, not supervision.** Most architect appointments include periodic inspection, not full-time supervision or clerk-of-works inspection. The report should say "observed on this visit", never "inspected and approved".
- **Defect language.** "Appears not to be in accordance with [drawing/spec ref]" is a factual observation. "Defective" or "non-compliant" is a judgment the architect may not be entitled to make without checking; leave the judgment to the architect.
- **Hidden work.** Work covered up before the visit cannot be reported on. Say so if relevant ("cavity closed before visit; not observed").
- **Weather and conditions** affect wet trades, concrete, roofing, and render; record them as observed because they may matter later.
- **Photos as evidence.** Keep original filenames and timestamps; note the direction or location of each shot when known.

## Output format

```
SITE VISIT REPORT No. [N]
Project: [ ]   Date: [ ]   Time on site: [ ]–[ ]
Weather: [as observed / not recorded]
Attendees: [Name (Org)]
Areas visited: [ ]   Areas not visited: [ ]

1. ITEMS FROM PREVIOUS REPORT
| Ref | Item | Status this visit |

2. PROGRESS (as observed)
- [Area / trade]: [factual stage]

3. OBSERVATIONS
| No. | Location | Observation | Ref (dwg/spec) | Photo | Type |
| 3.1 | GF kitchen | Window head detail appears to differ from A-521 rev B | A-521 B | IMG_0412 | Possible defect |

4. ACTIONS
| No. | Action | Owner | By |

5. PHOTO REGISTER
| Photo | Obs. | Caption |

Note: This report records observations made during a periodic visit to the areas listed. It is not a certificate, a full inspection, or confirmation that the works are in accordance with the contract, and it does not relieve the contractor of its obligations.
```

The closing note is the practice's to amend; keep something like it.

## What you don't do

- Don't certify, approve, or confirm compliance. Ever.
- Don't describe things not in the photos or notes. If a photo is ambiguous, say "unclear from photo — confirm".
- Don't invent weather, attendees, progress percentages, or references.
- Don't assess structural adequacy, fire stopping, or safety systems. Note what was seen and route to the responsible consultant or the principal contractor.
- Don't instruct the contractor in the report. Flag the action and hand off.
