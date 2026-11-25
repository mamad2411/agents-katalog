---
name: event-sponsor-renewal
description: "Wins back last edition's tech event sponsors after the post-event report: the sponsor debrief call and renewal ask timed to budget locks, non-discount early-renewal offers, telling returning sponsors about a price increase, tier changes, rescuing an at-risk sponsor or one whose champion left after the event, and renewal rate. Use whenever an organizer mentions renewing sponsors, a renewal pitch, a lapsing sponsor, or sponsor retention. Do NOT use for the report itself - use samber/dev-event-organizer-skills@event-sponsor-fulfillment; use samber/dev-event-organizer-skills@event-sponsor-pricing to set prices; use samber/dev-event-organizer-skills@event-sponsor-outreach for new sponsors; use samber/developer-relations-skills@developer-event-sponsorship when the user is the sponsor."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Sponsor Renewal

You turn last edition's sponsors into next edition's: the renewal conversation the post-event report earns, the offer, the price, the rescue and the rate.

The report is the evidence, and the renewal is won or lost on it. A sponsor's champion carries it into an internal budget review you never attend. Sponsors under-measure (ANA/MASB 2018 survey: only 37% had a standardized sponsorship-ROI process), so many champions likely arrive with no method of their own (judged); a report whose numbers they can re-derive is what they defend you with.

Inputs and outputs:

- **In** - each sponsor's post-event report and your renew / renegotiate / drop read, from `samber/dev-event-organizer-skills@event-sponsor-fulfillment`, which writes the report.
- **In** - each sponsor's own survey verdict (a "no" to sponsoring again triggers the rescue path), from `samber/dev-event-organizer-skills@event-feedback`.
- **Out** - a renewal decision per sponsor, a re-signed yes handed to `samber/dev-event-organizer-skills@event-sponsor-agreement`, and the edition's renewal rate.

The per-sponsor read used here is **renew / upgrade / swap / downgrade / release** (fulfillment's renegotiate = swap or downgrade, drop = release). The **hold date** is the date until which a package stays reserved for a returning sponsor.

Every ranking below is a default, not a law. Re-rank after the interview against what this organizer already has: a stable team that can sign multi-edition deals, a single anchor sponsor carrying most of the budget (it gets the strongest contact rung and the rescue path first), a next edition with no date yet.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 re-rank both menus.

1. Has the post-event report gone out, and does each one carry the five things below? Missing report: route to `samber/dev-event-organizer-skills@event-sponsor-fulfillment` first.
2. Which pole: community-run (volunteers, no attendee contact lists, talk slots not for sale) or company/foundation-run (paid team, consented scans, sponsored talks)?
3. Per sponsor: champion, budget owner, budget-lock month, every invoice paid, and the read from the report?
4. What is known about next edition: date, venue, rate-card changes, a price increase and its reason?
5. Which sponsors show red flags: silence on the report, unused perks, a changed champion, a "no" on the survey?
6. By when must renewals close? (A near deadline demotes the multi-edition agreement and the executive meeting, whose reviews will not finish in time.)
7. Is each sponsor a one-off or a multi-edition relationship? (A compounding mandate promotes the multi-edition agreement and the executive meeting.)
8. What is the effort ceiling: one volunteer or a volunteer team with a few evenings each, or a dedicated sponsorship lead? (A few evenings demotes the debrief call to the proposal email for every sponsor below the two highest-priced tiers.)

## How the report sets up the renewal

Check each stage-2 report (the short form or full metrics report fulfillment sends within 10 business days) for these five before any ask. Cannot see it: ask the user to paste it or confirm each item. A report missing one goes back to fulfillment; never patch it inside the renewal email.

1. **Their objective and a verdict against it** - the ask is "the package that hits your objective again", so the objective must be on the page.
2. **Every miss named with its make-good** - a sponsor who found a miss first reads the ask as spin.
3. **What went wrong and the fix** - the fix is the "what changes for you" line of the ask.
4. **A method line under every number** - the champion's analyst re-derives it before the budget meeting.
5. **Next edition, lightly** - dates and the fixes, no price and no pitch; the ask happens on the call.

## Community-run vs company-run

- **Community-run** - never offer a talk slot, attendee contacts or category exclusivity as a renewal incentive: the community pole does not sell them. Two-edition cap on any multi-edition deal; organizing teams turn over.
- **Company/foundation-run** - sponsored talks, consented scan hand-offs and category exclusivity are legitimate renewal currency. A paid team can call every sponsor and price multi-year terms through counsel.

## Workflow

1. Run the interview. Check every report against the five items above.
2. Triage first: a sponsor with two or more observed red flags, a champion who left, or a "no" on the survey skips the standard ask and enters the rescue path ([references/at-risk-sponsors.md](references/at-risk-sponsors.md)); it rejoins at step 4 once the reason is known and answered, and hears any price change only after that. A sponsor with a delivery miss but no flags stays on the standard path, gated on the make-good being delivered, not just promised.
3. Within days of the stage-2 report, book the renewal conversation at the contact rung the menu picks. A sponsor whose budget locks before the report date got the soft ask on site or before the event; pick up from there.
4. Read each sponsor: renew, upgrade, swap, downgrade or release, from the report's results against the tier bought ([references/renewal-offer-and-pricing.md](references/renewal-offer-and-pricing.md) § Tier read).
5. On the call: their internal reporting first ("what did your team have to report, and to whom?"), then the report, then the soft ask with one package and a hold date 30-60 days out (a judged window). Ask who else signs off and when the budget locks. A report row reading "pending, sent by [date]" (usually recording views): bring that figure to the call, or confirm its date on the call.
6. Communicate any price increase privately at this call, tied to a documented change, with the published price-change date. Next edition's list price comes from `samber/dev-event-organizer-skills@event-sponsor-pricing`; until it exists, quote it as indicative with its confirmation date.
7. Send the formal ask before the sponsor's budget locks, with the incentive the menu picks. Hold any ask while an invoice is unpaid. A yes goes to `samber/dev-event-organizer-skills@event-sponsor-agreement`.
8. Release honestly where the audience does not fit; released sponsors, sponsors still unsigned when the next edition takes place, and a departed champion's new employer, go to `samber/dev-event-organizer-skills@event-sponsor-outreach` as net-new.
9. When the renewal window closes (the later of the cohort's last budget-lock date and the last hold date, capped at the event date), compute the edition's renewal rate (see Measurement) and hand it to `samber/dev-event-organizer-skills@event-market-fit`. Sponsors still undecided at close are reported as open, never as lost.

If your harness has persistent memory, record per sponsor: champion and budget owner, budget-lock month, call notes, red flags, offer, hold date, outcome and release reason. Never store attendee personal data there.

## Renewal contact

How the renewal conversation happens after the report. Ranking (default, not a law - Q6, Q7 and Q8 re-rank):

- effort: `executive meeting > debrief call > proposal email == on-site ask`
- value (renewals closed before budget lock): `executive meeting > debrief call > on-site ask > proposal email`
- efficiency: `debrief call > on-site ask > proposal email > executive meeting`

The effort tie is argued: both ride a moment already happening, the email after the report and the day you are already on the floor together. The debrief wins efficiency because thirty minutes buys what the email cannot: what their boss measures, who signs, and when the budget locks.

- **Debrief call** - the default for every sponsor you want back: 30 minutes, booked when the stage-2 report lands.
- **On-site ask** - conditional: only for a sponsor whose budget locks before the report date, with last edition's report or, for a first-time sponsor, the on-site headline numbers as evidence.
- **Proposal email** - when the champion declines a call. Ask in writing what the call would have asked.
- **Executive meeting** - the starved option: highest value, highest effort. Promotion: the anchor sponsor, a top tier whose champion left, or a multi-edition deal on the table. A budget lock under about a month away overrides the promotion: hold the debrief call with the new budget owner instead.
- **Deleted, not demoted: the "are you coming back?" chase.** It confirms the suspicion that you only want the money (Sponsorship Collective). Every touch opens with a specific result plus one new idea.

## Renewal incentive

What makes signing before the hold date worth it. `event-sponsor-pricing` deletes the returning-sponsor discount, so every rung here is non-price or open to every sponsor on the same terms. Ranking (default, not a law - Q6 and Q7 re-rank):

- effort: `multi-edition agreement > published price-change date > first pick of capped surfaces == rate-card early-bird`
- value (renewals closed before budget lock): `multi-edition agreement > first pick of capped surfaces > published price-change date > rate-card early-bird`
- efficiency: `first pick of capped surfaces > published price-change date > rate-card early-bird > multi-edition agreement`
- compliance cost (the review it triggers): `multi-edition agreement > first pick == published price-change date == rate-card early-bird`

The effort tie is argued: first pick and the early-bird both sit on documents that already exist (the floor plan, the card), while a price-change date needs a pricing decision first. The compliance tie is argued: the three cheap rungs sit in a hold letter or on the published card and bind no future edition; a multi-edition agreement commits next year's organizers and needs counsel.

- **First pick of capped surfaces** - the default. Community-run: booth location, workshop room, prize track. Company-run adds a sponsored talk slot, and first pick of category exclusivity at its card premium and within the published cap. A returning sponsor gets the pick before the prospectus is public; the pick itself costs nothing.
- **Published price-change date** - when a real increase exists, pricing publishes the date it takes effect; anyone signing before it pays the current price. Returning sponsors hear the date first, privately. Set it at least 30 days (a judged floor) after the prospectus is public, or it becomes a returning-only discount by calendar.
- **Rate-card early-bird** - only where the card has one; mention it, never dress it as loyalty.
- **Multi-edition agreement** - the starved option. Promotion: a company or foundation-run event, a sponsor who asks, or an organizing team stable across both editions.
- **Deleted, not demoted:** a loyalty discount (pricing's deleted rung), and a matching-rights right of first refusal, which one organizer-side law firm advises dropping because it chills competing bids. Offer a time-boxed hold instead.

## Failure modes

- **Asking before the evidence lands.** A renewal email with no report attached is a cold email to someone who happens to know you. Fix: workflow step 1; route a missing report back to fulfillment.
- **A surprise price increase.** A new price on renewal day reads as punishing loyalty. Fix: announce it privately at the call, tied to a documented change, with the published price-change date.
- **A single-threaded relationship.** The champion leaves and the successor inherits a line item with no story. Fix: two named contacts per sponsor; the report doubles as the handover document.
- **Asking after the budget locked.** The sponsor liked the report and has no money left. Fix: Q3's budget-lock month sets the formal-ask deadline, not your event date.
- **Renewal rate as one number.** High logo retention can hide downgrades. Fix: report logo, gross and net revenue retention together.

## Measurement

- **Logo retention** = sponsors of edition N who sponsor N+1 / sponsors of N.
- **Gross revenue retention** = sum of min(N+1 spend, N spend) over the N cohort / the cohort's N spend. Excludes upgrades, so it shows leakage.
- **Net revenue retention** = the N cohort's total N+1 spend including upgrades / the cohort's N spend. Report it once more at constant prices when a price increase applied, so the increase does not pass for growth.
- **First-time sponsor retention** - the cohort practitioners report churns most (exhibitor data, not measured for tech-event sponsors).
- **Contracted carry-overs** - sponsors already signed for N+1 under a multi-edition agreement are reported apart; logo retention counts only sponsors who decided this cycle.
- **Annual series** - one cohort per series year, against the renewal date `samber/dev-event-organizer-skills@event-sponsor-pricing` fixes.
- **Ask timeliness** (self-set): 100% of formal asks sent before each sponsor's budget lock.

Cohort by legal entity (a group with no legal entity counts as one), report in-kind as a count outside the revenue rates, count releases as lost, and track your own trend. No measured benchmark exists for tech-event sponsor renewal. The nearest measured figure is trade-show exhibitor company retention (CEIR 2026 organizer survey, sample size not published: 73% small shows, 78% midsize, 69% largest), a proxy at best. The "62% average sponsor renewal" figure that circulates traces to no published study. Never quote a benchmark at a sponsor.

## Invocation examples

- "The sponsor reports went out last week. Plan the renewals for our 6 sponsors."
- "Our Gold sponsor's DevRel lead left in March. How do we keep them for next year?"
- "We're raising sponsor prices 15% next year. How do we tell returning sponsors?"
- "What was our sponsor renewal rate, and is it any good?"

Expected output:

- A per-sponsor read with red-flag count, the contact rung, the proposed package, the incentive and the hold date.
- The formal-ask schedule keyed to each sponsor's budget-lock month.
- Price-change messaging where an increase applies.
- The edition's logo, gross and net revenue retention once the window closes.

## References

- [references/renewal-offer-and-pricing.md](references/renewal-offer-and-pricing.md) - the two asks, hold dates, incentives, multi-edition terms, price-increase steps, tier read, ask templates.
- [references/at-risk-sponsors.md](references/at-risk-sponsors.md) - seven red flags, reason-matched responses, champion change, releasing a sponsor.

Cross-repo (recommendation, not a dependency): `samber/developer-relations-skills@developer-event-sponsorship` is the buyer's side; its renew/renegotiate/drop verdict is the decision this conversation meets.
