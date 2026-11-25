---
name: family-custody-schedule-builder
description: Turn negotiated custody/parenting-time terms (described in plain language or notes) into a formatted parenting time schedule document, including holiday rotation and exchange logistics. Use whenever the user describes custody arrangement terms and wants a formatted schedule, parenting plan document, or calendar-style breakdown, or wants to compare/redline a proposed schedule against a counter-proposal.
---

# Custody Schedule Builder

Converts negotiated or proposed custody terms into a clear, formatted parenting time schedule that can go straight into a parenting plan or settlement document.

## Workflow

1. **Extract the terms.** From the user's description, identify: the base rotation (e.g., week-on/week-off, 2-2-3, alternating weekends), exchange day/time, exchange location, holiday schedule, and any school-break provisions.
2. **Ask only if genuinely missing** something load-bearing (e.g., no exchange time specified at all) — don't ask about details the user didn't mention if a standard default is reasonable and can be flagged as an assumption.
3. **Build the schedule** in two views:
   - A plain-language week-by-week description
   - A holiday/school-break table showing which parent has the child each year (alternating, fixed, or split)
4. **Flag ambiguities or conflicts** — e.g., if the base rotation and a stated holiday provision would overlap or contradict, surface it rather than silently resolving it one way.
5. **If comparing two proposals**, produce a side-by-side diff highlighting exactly where they differ (which weekends, which holidays, exchange logistics) rather than restating both in full.

## Output format

```
## Parenting Time Schedule — [Case name]

**Regular schedule:** [plain-language rotation]
**Exchanges:** [day/time/location]

### Holiday & School Break Rotation
| Holiday/Break | Odd Years | Even Years |
|---|---|---|
| Thanksgiving | Parent A | Parent B |
| ... | | |

**Assumptions made:** [list anything defaulted, e.g., "assumed exchanges at 6pm absent a stated time"]
```

## Document Output Format

When the schedule is wanted as a document (for the parenting plan, or to send to opposing counsel/client), use the `docx` skill:

- **Header:** firm name/logo placeholder, case caption (parties' names, case number if known), title ("Parenting Time Schedule" or "Proposed Parenting Plan Schedule").
- **Regular schedule:** clean, readable paragraph or simple table — avoid cramming a full calendar grid into Word; a table with day-of-week columns and a short description works better than trying to replicate a calendar visually.
- **Holiday table:** real Word table with header row (light gray shading via `ShadingType.CLEAR`, never solid black), consistent column widths.
- **Assumptions section:** set apart clearly (e.g., italicized or in a bordered box) so it doesn't get mistaken for an agreed term if the document is shared before final review.
- **Typography:** 11-12pt serif or sans-serif consistent with firm preference, 1" margins, page numbers in the footer if more than one page.
- If comparing two proposals, use a two-column side-by-side table rather than two separate documents.

## Notes

- This produces a drafting aid, not a filed court document — note that it should be reviewed against jurisdiction-specific parenting plan requirements before filing.
- Never silently resolve a scheduling conflict in either parent's favor — flag it for the attorney to decide.
