---
name: deal-review-prep
description: "Prep an AE for a deal review or pipeline 1:1 with their manager — a crisp per-deal one-liner, anticipated probes, the help to ask for, and clean review notes. Use before a manager review or forecast call. Triggers on: deal review prep, prep for 1:1, manager review, pipeline 1:1, deal review."
---

# Deal Review Prep

## Purpose
Walk into a deal review or pipeline 1:1 with a tight story for each deal: where it
stands, what moves it next, the one real risk, and the specific help you need. Make
the manager's job confirming your plan — not extracting basics out of you.

## Inputs
- The deal set under review (which deals, which scope — committed, best-case, or all open)
- Current stage, close date, and amount for each
- The next step on each deal and who owns it
- What you actually want from the manager (an intro, air cover, a discount, a resource)

## Method
1. **One-liner per deal.** Force every deal into a single sentence the manager can
   absorb in five seconds:
   `<Account> — <stage>, <amount>, <close date>. Next: <next step + date>. Risk: <the one risk>. Ask: <specific help, or "none">.`
   If you can't write it, you don't understand the deal — that's the finding.

2. **Anticipate the three probes.** A good manager always presses on the same things.
   Have an evidence-backed answer ready for each:
   - **"Why this close date?"** Tie it to a buyer-stated event or commitment (budget
     cycle, contract end, project kickoff), not to your quarter. "They said X by Y" beats
     "I think it'll land."
   - **"Who's the economic buyer, and have you met them?"** Name the person, their role,
     and the date of last contact. "Champion only, EB unmet" is a valid honest answer —
     and itself becomes an ask.
   - **"What's the single biggest risk?"** One risk, not five. Name it, say what you're
     doing about it, and what would prove it resolved.

3. **Decide the ask before the meeting.** For each deal, classify the help you need so
   the manager can act, not just nod:
   - *Access* — exec sponsor intro, EB meeting, multi-thread support
   - *Authority* — discount/term approval, non-standard contract sign-off
   - *Air cover* — escalation, competitive pressure, "get our VP on a call"
   - *Resource* — SE deep-dive, security review, proof-of-concept help
   - *None* — explicitly say "on track, no help needed" so attention goes elsewhere

4. **Pressure-test the commit.** For any deal you're calling this period, sanity-check:
   is there a mutual next step on the calendar? Is the EB engaged? Are there open
   objections or active competitors? If two or more are shaky, downgrade it before the
   manager does.

5. **Sequence the review.** Lead with deals that need a decision/help, then committed
   deals, then the rest. Don't burn the slot narrating healthy deals.

**Review-notes output format:**
```
DEAL REVIEW — <date> — <your name>

COMMIT
- <Account> | <stage> | <amount> | <close date>
  Next: <step + owner + date>
  Risk: <one risk> → <mitigation>
  EB: <name/role, last contact | or "unmet">
  ASK: <specific help, or none>

BEST CASE
- <Account> | ... (same shape)

NEEDS DISCUSSION
- <Account> — <the open question for the manager>
```

**One-risk rule:** every deal gets exactly one named primary risk with a mitigation.
A deal with "no risks" hasn't been examined; a deal with five hasn't been prioritized.

## Tool binding
This skill works from a pasted deal list alone. It gets sharper when connected to your
stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, build the review from real deal
state instead of asking the user to reconstruct it:
- `ontology_list("deal", ...)` to pull the deal set in scope (stage, amount, close date,
  owner), and `ontology_aggregate` to summarize it — count and value by stage or by
  forecast category — so the review opens with the shape of the pipeline.
- Per deal, `ontology_resolve("deal", id, expand=["brief","risks","commitments"])` —
  use the `brief` for the one-liner narrative, `risks` for the evidence-backed primary
  risk, and `commitments` (both-sided, transcript-derived) for the real next step and
  for testing whether the close date is buyer-anchored.
Doris already derives risks and commitments from the actual calls — prefer those over
the AE's gut read so the answers survive the manager's probes.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull the deal list and fields (stage, amount, close
  date, next-step, owner) for the review set, and read activity history to anchor "why
  this close date" and "when did we last touch the EB."
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → confirm what the buyer
  actually committed to and surface open objections behind each risk.

### With nothing connected
Ask the user to paste their deal list (account, stage, amount, close date, next step).
Then, working only from that:
1. Write the one-liner for each deal; flag any deal where the user can't supply a next
   step, an EB, or a reason for the close date — those are the review's weak spots.
2. For each, draft answers to the three probes (close date / EB / biggest risk),
   marking gaps the user must fill before the meeting.
3. Classify the ask for each deal (Access / Authority / Air cover / Resource / None).
4. Output the full review-notes block above, ready to copy into the 1:1.

## Works without Doris
Fully functional from a pasted deal list — Doris only removes the reconstruction step
and supplies evidence-backed risks and commitments so the answers hold up under probing.

## Common mistakes
- One-liners that state the stage but bury the risk and the ask.
- A close date justified by the quarter instead of a buyer-stated event.
- Listing five risks instead of naming the one that actually decides the deal.
- Showing up with status but no specific ask — wasting the manager's leverage.
- Narrating healthy deals first and running out of time on the ones that need help.
