---
name: snag-list
description: Builds and maintains a snagging / punch list organised by area, room, and trade — each item referenced, prioritised, photographed, and tracked through re-inspection to close-out — and turns a CSV of snags into a printable HTML list with a status summary. Use when the architect wants a "snag list", "punch list", "defects list", "close-out list", "re-inspection", or to sort a walk-round's notes and photos into something the contractor can work through. Records what was observed, never certifies completion. Hands routine site observations to site-visit-report and anything needing a formal notice or certificate letter to contract-admin-letter.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Snag List

A snag list (punch list in the US) is the working list of incomplete or defective items the contractor must put right before, or after, completion. A good one is specific enough that the operative can find and fix each item without phoning the architect, and structured so the list can be re-inspected and closed out item by item.

## When to use

- Pre-completion or practical / substantial completion inspection.
- End of defects (rectification / liability) period inspection.
- Turning walk-round notes, voice memos, and photos into a list for the contractor.
- Re-inspecting and updating status on an existing list.

## Input

- Notes, voice-note transcript, or marked-up plans from the walk-round, and photos with filenames.
- Room / area names or numbers as on the drawings, so the list matches the plans.
- The existing list (CSV or table), if this is a re-inspection.
- Inspection date, inspector, and which areas were and were not accessible.

## Process

1. **Structure by location first,** then trade. Area (floor, block, external) → room → element. Use the drawing room names and numbers.
2. **Write each item so it can be found and fixed.** Location, element, what is wrong, and what "fixed" looks like if not obvious. "Bed 2, window W12, left jamb: sealant missing for approx. 300 mm at sill junction" beats "window sealant".
3. **Reference.** Unique reference (S-001...), photo filename, and the drawing or spec reference where the item departs from it.
4. **Assign trade** if known; mark "unassigned" otherwise. Don't guess the subcontractor.
5. **Prioritise** consistently:
   - **High** — affects safety, security, weather-tightness, or use of the space, or blocks other trades.
   - **Medium** — functional or visible defect to be fixed before handover.
   - **Low** — cosmetic or minor.
   Say that these are the practice's working priorities, not contractual categories.
6. **Track status:** open / in progress / closed / disputed / not accessible. On re-inspection, update status and the re-inspection date; never delete closed items — strike them through.
7. **Summarise.** Counts by status, by trade, by area, with the basis stated.
8. **Generate the printable list** with the script below when a CSV exists.

## Script

`scripts/snag_report.py` (Python 3.9+, standard library only) turns a CSV into a printable HTML list grouped by area, with a tick column for re-inspection, and prints a status summary.

```bash
python scripts/snag_report.py snags.csv -o snag-list.html --project "Riverside House" --issue "Rev B, re-inspection 17 Nov"
```

CSV columns (only `ref`, `area`, `description` are required; extra columns are kept in Notes):
`ref, area, room, element, trade, description, priority, status, raised, reinspected, photo, notes`

If you draft a list from notes, output it as a CSV in that column order so it can go straight into the script or a spreadsheet.

## Domain knowledge

- **Terminology and stage.** Snagging (UK, IE, AU), punch list (US), réserves at réception (FR), Mängelliste (DE). Completion milestones differ by contract form — e.g. practical completion (JCT), completion (NEC), substantial completion (AIA A201), taking-over (FIDIC). Ask which form applies; the list itself is the same.
- **Snags and completion.** Whether outstanding items prevent completion being certified depends on the contract and the nature of the items. That is the contract administrator's judgment, not the list's.
- **Not exhaustive.** A snag list records items observed. Make that explicit, so it does not read as an acceptance of everything not listed.
- **Inaccessible areas.** Record them ("plant room locked; not inspected"). They are not snag-free.
- **Patterns.** Ten sealant items across six rooms is one workmanship issue; say so in the summary.

## Output format

```
SNAG LIST — [Project]   Inspection: [date]   By: [ ]   Issue: [rev]
Areas inspected: [ ]   Not accessible: [ ]

SUMMARY  (basis: count of items on this list)
Total [n] · Open [n] · In progress [n] · Closed [n] · Disputed [n]
Not closed by trade: [ ]   by area: [ ]
Patterns: [recurring issue, if any]

[Area]
| Ref | Room | Element | Trade | Description | Pri. | Status | Photo |

Note: Items listed are those observed on the inspection(s) recorded. The list is not exhaustive and does not relieve the contractor of its obligations under the contract.
```

## What you don't do

- Don't certify completion, or state that an item is acceptable or that the works comply.
- Don't invent locations, trades, photo references, or drawing references.
- Don't assess fire stopping, structural, or life-safety systems; record what was seen and route to the responsible consultant.
- Don't decide who pays for a defect or whether it is a defect under the contract.
- Don't drop closed or disputed items from the record.
