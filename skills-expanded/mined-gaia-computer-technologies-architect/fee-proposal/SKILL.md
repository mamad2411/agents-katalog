---
name: fee-proposal
description: Build an architect's fee proposal — scope of services by work stage, a deliverables matrix, a fee basis with every number shown (percentage, lump sum, or time-charge built up from hours x rates), assumptions, exclusions, and a note on the appointment form. Works with RIBA Plan of Work, AIA phases, HOAI Leistungsphasen, or any stage framework the architect names. Use when the architect wants a "fee proposal", "fee letter", "quote for services", "scope of services", "how much should I charge", or to check a fee against the effort it implies. Never invents fee scales or rates; uses the practice's own rates or a cited survey. Hands to bid-response for formal tenders and client-pushback when the fee is contested.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Fee Proposal

Turn a project enquiry into a fee proposal a client can sign and the practice can deliver without losing money. The fee is a consequence of scope and effort, so build it from both, and show every step.

## When to use

- A new enquiry needs a fee letter or proposal.
- The architect has a number in mind and wants to test it against the hours it buys.
- Scope is fuzzy and the proposal needs to define what is, and is not, included.
- A client has asked for a breakdown by stage.

## Input

Ask for what's missing; never fill a gap with an assumed figure.

- **Project:** type, location (jurisdiction), size (GIA/GFA or units), construction budget if known, procurement route if known.
- **Stage framework:** RIBA Plan of Work 2020 (0–7), AIA phases (SD/DD/CD/Bidding/CA), HOAI Leistungsphasen 1–9 (Germany), or another. Ask which; don't default.
- **Stages in scope:** e.g. "to planning only" or "full service to completion".
- **Practice rates:** hourly or daily rates by grade (principal, associate, architect, assistant). These must come from the practice.
- **Fee basis preferred:** percentage of construction cost, lump sum per stage, time-charge, or a hybrid.
- **Reference fee data (optional):** a fee survey or benchmark the practice uses, named with its edition and date.
- **Known consultants:** who else is appointed, so exclusions are clear.

## Process

1. **Fix the stages and scope.** List the stages in scope in the client's framework. For each, write the services in plain language (what the client gets), not a code ("Stage 3").
2. **Build the deliverables matrix.** For each stage: drawings, reports, models, meetings, applications. Count meetings and site visits explicitly. They are where fees leak.
3. **Resource it.** Estimate hours per stage per grade. Show the build-up as a table: hours x rate = cost. Mark every hour figure as the practice's estimate to confirm. Ask for their timesheet history on similar jobs and use it if given.
4. **Set the fee basis.**
   - *Time-charge:* the resourced total, with a cap or estimate if the client wants certainty.
   - *Lump sum:* the resourced total plus risk and margin, stated as separate lines.
   - *Percentage:* convert to a percentage of construction cost only if the construction cost is given. Show the arithmetic, then compare it with the resourced total. If they diverge by more than about 15%, say so; one of them is wrong.
   - If the practice cites a fee survey, quote the figure with its source and date. Never supply a "typical percentage" from memory.
5. **Write assumptions and exclusions.** Assumptions: number of design iterations, meetings, planning route, drawing scales, information the client supplies. Exclusions: other consultants' work, surveys, statutory fees, specialist reports, additional services. Then define how variations are charged.
6. **Payment terms and appointment.** Stage-based or monthly invoicing; the appointment form the practice uses (RIBA Professional Services Contract, AIA B101, a national standard form, or a bespoke letter of appointment). Flag that the appointment terms, liability cap, and PI requirements need the practice's own review.

## Domain knowledge

- **Fee leakage lives in meetings, iterations, and planning.** Cap design iterations per stage and price extra rounds. Define the planning route (pre-application, full application, conditions discharge) and price each.
- **Construction-phase services are the most underpriced.** Site visit frequency drives cost: price visits as a number, not "as required".
- **Percentage fees float with cost.** If the budget is uncertain, a percentage fee is uncertain too. Say whether the percentage applies to the budget, the tender sum, or the final account.
- **Statutory and third-party fees are pass-through.** Planning application fees, building control fees, and survey costs are the client's, not part of the architect's fee.
- **Stage frameworks differ.** HOAI Leistungsphasen carry statutory fee tables in Germany (check current status and applicability). RIBA and AIA frameworks do not set fees. Never present any framework's fee as mandatory without a current source.

## Output format

```
## Fee Proposal — [Project], [Location]

**Scope in one line:** [stages and services, e.g. "Concept to planning approval, RIBA Stages 0–3"]

### Services by stage
| Stage | Services | Key deliverables | Meetings / visits |
|---|---|---|---|

### Resource build-up (practice estimate — confirm)
| Stage | Grade | Hours | Rate | Cost |
|---|---|---|---|---|
| | | | **Total** | |

### Fee
- Basis: [time-charge / lump sum / percentage / hybrid]
- Fee: [amount, with arithmetic shown]
- Cross-check: [percentage vs resourced total, and the variance]
- Expenses: [included / charged at cost / fixed allowance]

### Assumptions
- ...

### Exclusions
- ...

### Additional services and variations
[How extra work is charged: rates, notice, written instruction.]

### Payment and appointment
[Invoicing schedule; proposed appointment form; liability and PI to be confirmed by the practice.]

**To confirm before issue:** [every figure or assumption that is the practice's estimate]

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't invent fee scales, "industry standard" percentages, or hourly rates. Use the practice's own numbers, or a named and dated survey they supply.
- Don't give legal advice on appointment terms, liability caps, or insurance. Flag them for the practice's own review.
- Don't hide margin or risk inside hours. Show them as lines so the practice can see what it is betting.
- Don't let "as required" stand anywhere in a scope. Count it or cap it.
