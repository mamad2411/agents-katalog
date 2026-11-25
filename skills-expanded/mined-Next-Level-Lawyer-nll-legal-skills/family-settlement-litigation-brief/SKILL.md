---
name: family-settlement-litigation-brief
description: Summarize the facts of a family law case into a one-page brief comparing likely outcomes and tradeoffs of settling versus litigating, to help a client make an informed decision. Use whenever the user wants a settle-vs-litigate comparison, a client-facing decision memo for a divorce/custody case, or a summary of risk/cost/timeline tradeoffs between the two paths.
---

# Settlement vs. Litigation Brief

Produces a one-page, client-readable comparison of settling versus litigating a family law matter, grounded in the specific facts of the case rather than generic pros/cons.

## Workflow

1. **Gather the case-specific facts** the user provides: contested issues (custody, support, property division), current settlement offer if any, strength of each side's position, and any time pressure (e.g., upcoming trial date, school year considerations).
2. **For each contested issue**, note the likely range of outcomes if litigated (based on what the user knows of local practice/precedent — don't invent case law), versus what's on the table in settlement.
3. **Build the comparison** across: likely outcome range, cost (attorney fees, time), timeline, emotional/relational cost (co-parenting relationship going forward), and certainty (settlement = certain, litigation = range with downside risk).
4. **State the tradeoff plainly** — this is a decision memo, not a neutral academic comparison. End with what the settlement offer would need to include, or what would need to be true, for each path to make sense.

## Output format

```
## Settle vs. Litigate — [Case name]

### Contested issues & current positions
- [Issue]: settlement offer = [X], likely litigated range = [Y-Z]

### If you settle
- Certainty: [what you'd get, guaranteed]
- Cost/timeline: [fast, lower cost]
- Tradeoff: [what you'd give up vs. best-case litigation outcome]

### If you litigate
- Best case / likely case / worst case: [range]
- Cost/timeline: [estimate]
- Risk: [what could go worse than the current offer]

### Bottom line
[1-2 sentence direct recommendation framing, not just "it depends"]
```

## Document Output Format

When this is wanted as a client-facing document rather than a chat answer, use the `docx` skill to produce a one-pager that actually reads like a firm memo:

- **Header:** firm name/logo placeholder, "To: [Client] / From: [Attorney] / Re: Settlement vs. Litigation — [Case] / Date" memo-style block.
- **Body:** real Word heading styles for each section (not bold body text pretending to be a heading), short paragraphs, and a comparison table for the contested-issues breakdown rather than a bulleted wall of text.
- **Bottom line:** visually set apart (bordered box, bold, or shaded background) at the end so the recommendation is the last thing the client's eye lands on — this document exists to drive a decision, and the layout should support that.
- **Typography:** 11-12pt, 1" margins, keep it to one page if at all possible per the brief's purpose.

## Notes

- Don't cite specific case law or statutes unless the user provides them — reason from the facts and general framework given, and flag where attorney judgment on local precedent is needed.
- This is meant to help a client decide, so end with a clear framing rather than hedging everything.
