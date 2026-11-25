---
name: event-sponsor-value-proposition
description: Discover what each sponsor of a technical conference actually needs, then articulate what it genuinely gets and why each sponsor segment buys - brand exposure, product feedback, recruiting, community goodwill, and (vendor-run events only) pipeline - one segment at a time through a six-part jobs-to-be-done template, bounded by what the event type can honestly promise and backed by proof points a diligent sponsor will check. Use whenever the user mentions why a company should sponsor an event, sponsor benefits or motivations, or building the value story before a prospectus or rate card exists - even if they never say "value proposition". Sponsorship never buys talks, judging results, or roadmap influence. Do NOT use to package or price it - use samber/dev-event-organizer-skills@event-sponsor-prospectus instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.2.2"
---

# Event Sponsor Value Proposition

You discover what each sponsor needs and articulate the value a technical event can genuinely offer it, before anything is packaged, priced, or pitched. Sponsors often cannot see an event's value by themselves; the fit between event and sponsor is found in discovery, not assumed in a deck.

- **Deliverable**: one value-proposition statement per sponsor segment, every claim backed by a proof point, feeding `samber/dev-event-organizer-skills@event-sponsor-prospectus` (the deck) and `samber/dev-event-organizer-skills@event-sponsor-pricing` (the rate card).
- **Out of scope**: packaging tiers, setting prices, running outreach, drafting contracts, tracking delivery - those are sibling skills.
- **Scope**: mainly one-day and multi-day conferences; other formats reuse the logic only where they sell sponsorship the same way.
- **What the sponsor buys**: for a sponsor, the attendees are in effect the product - it buys access to a qualified audience. Access means presence and conversations, never an attendee list; contact data moves only when an attendee volunteers it, and at a community-run event never as a list (see Community-run vs vendor-run).
- **Boundary**: sponsorship buys placement and access, never a talk slot, a judging result, or influence over the program or roadmap ("No sponsor should be able to buy their way into the program" - DevOpsDays organizing guide).

Every ranking below is a default, not a law: it shifts with context and with who executes it. After the interview, re-rank against what you know about this organizer - each of the following overturns a default rung:

- an existing attendee-data pipeline
- a returning anchor sponsor
- a first edition with no track record
- a vendor-run event with consented lead retrieval
- a cooling local hiring market (Q11)

## Interview

Ask one question at a time, multiple-choice where possible. Questions 7-9 exist because the menus below diverge sharply on time-to-payoff, durability, and effort - the default rankings cannot be picked for the user.

1. Which pole does the event sit on: community-run (independent, CFP-driven, sponsors as cost recovery) or vendor/foundation-run (vendor-owned, marketing budget, sponsors as pipeline)? This bounds which value categories can honestly be promised - settle it before drafting any benefit claim.
2. Which sponsor segment is this proposition for, one at a time: product-feedback buyer (DevRel/developer-advocate titles), recruiting buyer (talent-acquisition/HR titles), brand buyer (marketing/PR titles), or community-member sponsor (a practitioner or founder inside the community)? Segment taxonomy and title signals: [references/sponsor-segment-jtbd-worksheets.md](references/sponsor-segment-jtbd-worksheets.md).
3. What does this specific partner actually need from the event? Ask before proposing; many sponsors cannot name it unprompted. Probe each typical need and map it onto a value category below: employer brand or hiring (recruiting), selling to the audience (pipeline at the vendor pole only; at the community pole, brand exposure plus attendee-chosen product conversations), product feedback (product feedback), brand awareness (brand exposure), community goodwill (community goodwill). A need no category can carry honestly goes on the not-offered list.
4. What audience evidence exists: aggregate role/seniority/company-size mix, geography, from past editions or registration forms? Numbers, not impressions. ("What audience will attend?" - first of the three questions sponsors always ask, DevOpsDays guide.)
5. What track record exists: editions run, returning-sponsor rate, a real post-event sponsor report? A first edition has none - flag it and use the substitutes in the proof-point reference, never invented figures.
6. What does this segment do today without the event - a booth at a bigger vendor conference, job-board ads, a brand campaign, cold outreach to the same audience? The status quo is what makes the event's value legible instead of assumed.
7. When must sponsorship revenue close? (A near deadline promotes categories that pay off on-site - recruiting conversations, product feedback - over the compounding ones.)
8. Is this sponsor relationship a one-off sale or a compounding multi-edition asset? (A compounding mandate promotes the slow categories: brand, community goodwill.)
9. What is the effort ceiling for evidence collection: data already held, survey capacity, organizer hours available?
10. Which specific sponsor or tier is this proposition being drafted for, and does that prospect's own diligence checklist ask about buying influence or seniority mix?
11. What is this segment's current hiring pressure: are the target companies recruiting tech staff now, holding, or cutting? Sponsors mostly pay to recruit or to sell to tech teams, and recruiting sponsors leave first when hiring slows. A cooling market demotes recruiting as co-lead and promotes staff-free visibility. Signals to check: [references/value-category-evidence.md](references/value-category-evidence.md).

## Community-run vs vendor-run

Who owns the event decides what can honestly be promised, the same axis `samber/dev-event-organizer-skills@event-first-edition` and `samber/dev-event-organizer-skills@event-format-selection` argue:

- **Community-run** - no attendee contact list is ever given or sold, and no speaking slot is purchasable (DevOpsDays organizing guide states both rules twice). Lead capture happens only when an attendee volunteers it. Aggregate demographics are the honest substitute for lead data; the honest category mix is brand exposure, recruiting via real conversations, product feedback from a technical opinionated audience, and community goodwill.
- **Vendor/foundation-run** - pipeline and consented lead-retrieval value (badge scanning that returns contact details) are honestly on the table, bounded by attendee consent. The pipeline category exists only at this pole.

Say which pole each claim assumes. A value proposition that promises lead lists at a community-run event oversells a benefit the event structurally cannot deliver - and a sponsor who has read the organizer's own published rules catches the mismatch immediately.

## Workflow

1. Run the interview; fix the pole (Q1) and one segment (Q2).
2. **Discovery**: run Q3 with the actual prospect - a call or a short exchange, not a guess from its job ads. Write down its stated need in its own words and the category it maps to; that pairing is the event-sponsor fit the statement must serve.
3. **Honesty gate first**: write down what this event will _not_ offer before drafting what it will - the published organizer pattern (DevOpsDays tells sponsors "no attendee lists, no purchased slots" before describing packages). Delete unavailable categories now; a category parked "for later" silently reappears in the deck.
4. Choose the lead category from the value-category menu below; the need found in discovery picks the co-lead.
5. **Offer-activity coherence**: check that the planned program carries an activity for every category claimed - a hiring corner for recruiting, a hands-on feedback session for product feedback, a staffed demo space attendees opt into for selling. A talks-only program convinces sponsors less than one with a business-oriented layer, because talks deliver little of what they buy. Design that layer rather than copying another event's recipe; in a city already saturated with events, a sponsor activity nobody else runs is itself the differentiator. Positioning: `samber/dev-event-organizer-skills@event-positioning`; activity shapes: `samber/dev-event-organizer-skills@business-event-formats`. Sponsor activities stay outside the CFP program (see Boundary).
6. Fill the six-part JTBD template for this one segment - Who / Why / What Before / How / What After / Alternatives - using [references/sponsor-segment-jtbd-worksheets.md](references/sponsor-segment-jtbd-worksheets.md). Never blend segments into one statement.
7. Attach a proof point to every claim in the How, chosen from the instruments menu below (collection detail: [references/proof-point-instruments.md](references/proof-point-instruments.md)). Label every claim evidenced or aspirational - an unlabeled claim reads as evidenced and fails diligence as invented.
8. Score the draft with the value-equation check in [references/proof-point-instruments.md](references/proof-point-instruments.md) - a post-draft scoring lens, never the structure to fill in.
9. Validate section by section with the user - this is a strategy deliverable; get explicit approval per section, never as one block. Repeat steps 2 and 4-8 per additional segment.
10. Hand off the statements plus proof-point inventory to `samber/dev-event-organizer-skills@event-sponsor-prospectus` and `samber/dev-event-organizer-skills@event-sponsor-pricing`.

If your harness has persistent memory, record per segment:

- the need stated in discovery and the category it maps to
- the chosen lead category
- the not-offered list
- each claim's proof-point status (evidenced vs aspirational)
- the evidence still to collect before next edition

The prospectus, pricing, and outreach runs start from that record instead of re-deriving the value story.

## Value-category lead

Which category anchors the proposition for a given segment. Ranking (default, not a law - re-rank against Q7-Q9 and the pole):

- effort (evidence + delivery mechanics to claim it honestly): `pipeline > recruiting > product feedback > brand exposure == community goodwill`
- value (payoff to the typical sponsor when genuinely delivered): `pipeline > recruiting == product feedback > brand exposure > community goodwill`
- efficiency: `brand exposure > product feedback > recruiting > community goodwill > pipeline`
- compliance cost (the review it triggers, and how little of it can be undone): `pipeline > recruiting > product feedback == brand exposure == community goodwill`

All three ties are argued:

- **Effort**: brand exposure and community goodwill are each claimable from evidence the organizer already holds - aggregate demographics and visibility inventory for one, the community's track record and values for the other - while every higher rung pays for new machinery (composition data, conversation formats, consented capture).
- **Value**: a filled req and a validated product decision are comparably concrete single-quarter payoffs; MLH's organizer guide names recruiting and product feedback side by side among its three primary sponsor motivations without ranking them.
- **Compliance cost**: pipeline is the only category that hands a sponsor personal data, so it triggers a consent-flow and data-protection review plus a contractual limit on the sponsor's reuse, and it is irreversible - an attendee's contact details cannot be recalled once they leave. Recruiting inherits a lighter version of that review at the vendor pole only.
- **Bottom three**: tie at near-zero because none of them moves a name off the organizer's systems, which is what makes them genuinely equal rather than merely unseparated.

- **Brand exposure** - the default anchor. Events sit in the awareness family by default (Phil Leggetter's AAARRRP mapping) - that is a corrective, not a consolation: pitching every sponsorship as pipeline when the honest primary payoff is visibility is the dishonest default this menu exists to fix. Pair it with the segment's JTBD category as co-lead.
- **Product feedback** - co-lead for DevRel/advocate buyers: real-time reactions from a technical, opinionated audience (MLH). Pays off on-site - promote it under a near deadline (Q7).
- **Recruiting** - co-lead for talent buyers; at community-run events it is conversation-based (office hours, a staffed table), never scanned-data-based. Say so explicitly. Demotion condition, keyed to Q11: when the segment's hiring has slowed, recruiting budgets are the first cut, so lead with brand exposure and keep recruiting as an optional co-lead rather than the anchor.
- **Community goodwill** - low on the typical-sponsor value axis, but a real renewal driver distinct from pipeline: JetBrains' stated reason for sponsoring PyCon US is supporting the community, meeting existing users, and market intelligence - not leads (PSF prospectus testimonial; one vendor's stated logic, not a benchmark). Promotion condition: the sponsor is drawn from the community's own membership or strategically depends on the ecosystem - common, since many sponsor contacts are themselves practitioners (DevOpsDays). Then it leads.
- **Pipeline** - the starved option: tops the value axis, tops the effort axis (consented capture mechanics, attribution, booth staffing), so efficiency never picks it. Promotion condition: a vendor/foundation-run event with consented lead retrieval in place _and_ a sponsor whose stated job is pipeline.
- **At a community-run event, delete pipeline, don't demote it**: a demoted pipeline promise parked at the bottom of the menu reappears in the prospectus as scope.

## Proof-point instruments

Every claim in the How needs evidence a diligent sponsor would accept - their due-diligence list (audience composition, geography, track record, sponsor density, program quality) is exactly what to gather answers for. Ranking (default, not a law - Q9's ceiling re-ranks):

- effort (collection + analysis hours): `deep attendee survey > post-event sponsor report > sponsor testimonials > registration-form demographics > returning-sponsor rate == program-content ratio`
- value (perceived-likelihood lift for a diligent sponsor): `deep attendee survey > registration-form demographics > post-event sponsor report > returning-sponsor rate > program-content ratio > sponsor testimonials`
- efficiency: `returning-sponsor rate > registration-form demographics > program-content ratio > sponsor testimonials > post-event sponsor report > deep attendee survey`
- compliance cost (the review it triggers, and how little of it can be undone): `deep attendee survey > registration-form demographics > sponsor testimonials > returning-sponsor rate == program-content ratio == post-event sponsor report`

Both ties are argued:

- **Effort**: returning-sponsor rate and program-content ratio are each an hour or so of counting records the organizer already keeps - the sponsor roster per edition and the published program - with no new collection.
- **Compliance cost**: the survey and the registration fields both collect personal data and need a privacy notice, a retention rule and a lawful basis, but the survey asks employment and buying-authority detail and cannot be un-asked, while a form field is dropped next edition. A named testimonial needs the sponsor's own sign-off on an attributed quote, withdrawable on request.
- **Bottom three**: tie at zero because each counts records the organizer already holds and reports them in aggregate - no new personal data, nothing to clear, nothing to undo.

- **Default rung**: compute the returning-sponsor rate and program-content ratio now (near-zero effort), and change the registration form this edition to capture role/seniority/company-size in aggregate. This is the one instrument that compounds: each edition's data feeds every future proposition, and it is the honest substitute for lead data at a community-run event.
- **Deep attendee survey** (buying influence, tool adoption, seniority detail) - the starved option: top of value, top of effort, so efficiency never picks it. Promotion condition, keyed to Q10: courting an anchor or presenting-tier sponsor whose diligence asks about buying influence, or a vendor-pole event where composition claims carry the price.
- **First edition**: no returning rate, no report, no prior demographics exist. Honest substitutes, flagged as such in the statement: the organizers' own track record, community size and engagement evidence (meetup attendance, CFP volume). Never a projection presented as history - see [references/proof-point-instruments.md](references/proof-point-instruments.md).

## Failure modes

- **Leading with qualified leads at a community-run event.** Structurally undeliverable - no lists, no scanning - and the organizer's own published rules say so. Substitute aggregate demographics plus conversation-based recruiting and feedback access.
- **Implying sponsorship buys a keynote, a judging result, or roadmap influence.** Not an aggressive pitch - a false claim that collapses the moment a sponsor tests it. Organizer guides state it as a hard rule, not a negotiable extra.
- **Skipping discovery and pitching a guessed need.** The sponsor rarely sees the event's value unprompted, so a statement built on an assumed job reads as generic and stalls. Run Q3 with the prospect first.
- **A business promise with a talks-only program.** Claiming recruiting, feedback, or selling value while the agenda holds only talks leaves the sponsor nothing to do on-site. Add the activity that carries each claim, or drop the claim.
- **Value proposition written as a perks list.** Booth size, logo placement, ticket counts are package contents - the prospectus's job. The value proposition answers why this segment buys, against its named alternatives.
- **One blended statement for all segments.** The multi-segment-canvas failure the one-at-a-time template exists to prevent; it dilutes into "great exposure to a great audience," which no budget holder can route internally.
- **Audience-quality claims with no composition data.** To a diligent sponsor, "great access to senior engineers" without evidence is indistinguishable from the buyer-side warning sign it matches (vague, unverifiable attendee numbers). Gather the proof point or drop the claim.
- **Invented ROI figures or conversion benchmarks.** This category has none to quote. DevOpsDays shows how to state confidence without one: "We believe the pricing is low compared to the value sponsors get" - conviction, no fabricated number attached.
- **Community goodwill treated as filler.** It is a named renewal driver distinct from pipeline; for practitioner-sponsors it is the lead category, not a residual paragraph.
- **Booth-first proposition with no staff-free route when budgets tighten.** A booth costs the sponsor staff days on top of the fee; when hiring slows, recruiting sponsors leave first and booth-led packages stall while logo and digital visibility still sells. Fix: read Q11 before choosing the co-lead, and state a staff-free brand-exposure route in every segment's How so `samber/dev-event-organizer-skills@event-sponsor-pricing` can price it.
- **Ignoring the sponsor's denominator.** Their fully loaded cost - fee, booth build, travel, staff days - is part of their mental math; naming it is more credible than silence.

## Measurement

Value-proposition framing cannot be measured against an industry conversion figure, so never quote one. What is observable is downstream and self-set - pick 2-3, and write down the revision each would trigger before outreach starts:

- **First-call coverage** (self-set): sponsor calls should open with the three known questions - what audience, why sponsor, what per level (DevOpsDays) - already answered by the proposition. Calls that stall on "what do we actually get" mean the How is vague. Calls that stall on "who attends" mean the composition proof point is missing.
- **Objection log** (self-set): have `samber/dev-event-organizer-skills@event-sponsor-outreach` tag objections by segment; a recurring objection is a defect in that segment's statement, not a sales problem.
- **Statement reuse** (self-set): the prospectus, pricing, and outreach runs should quote the statements near-verbatim; if they rewrite them, the statement wasn't concrete enough to survive contact.
- Sponsor renewal rate reads on the whole relationship - delivery, report quality, relationship - not on this skill alone; it belongs to `samber/dev-event-organizer-skills@event-market-fit` (signal) and `samber/dev-event-organizer-skills@event-sponsor-renewal` (tracking).

## Invocation examples

- "Why would anyone sponsor our 300-person community-run DevOps conference? Help me articulate it before I build the deck."
- "A dev-tools vendor asked what their DevRel team would actually get from sponsoring our hackathon - draft the value story."
- "We're courting a bank's early-talent team as an anchor sponsor. What's the recruiting value proposition, and what evidence do we need first?"
- "Sponsor renewals dropped this year - rebuild the value proposition for our existing practitioner sponsors."

Expected output: per segment, a six-part value-proposition statement (Who / Why / Before / How / After / Alternatives), a proof-point inventory labeling each claim evidenced or aspirational with the instrument behind it, and the not-offered list stated up front - presented section by section for validation.

## References

- [references/sponsor-segment-jtbd-worksheets.md](references/sponsor-segment-jtbd-worksheets.md) - the six-part JTBD template with per-segment worksheets (product-feedback, recruiting, brand, community-member buyers), the five-way sponsor-type taxonomy, and a worked positive/negative statement pair.
- [references/value-category-evidence.md](references/value-category-evidence.md) - the category set and the frameworks behind it (DQL routing, AAARRRP, the five ROI objectives), the sponsor-motivation and concern taxonomies, the honesty constraint in the organizers' own words, the goodwill testimonial evidence, and how sponsor demand follows the hiring market.
- [references/proof-point-instruments.md](references/proof-point-instruments.md) - the mirrored due-diligence checklist, per-instrument collection guidance, first-edition substitutes, and the value-equation scoring check.

See also, same collection:

- `samber/dev-event-organizer-skills@event-sponsor-prospectus` - packages this skill's statements into a deck with tiers and proof points.
- `samber/dev-event-organizer-skills@event-sponsor-pricing` - prices what this skill articulated; value claims justify the rate card, never the reverse.
- `samber/dev-event-organizer-skills@event-sponsor-outreach` - sells it; feeds the objection log back into this skill's measurement.
- `samber/dev-event-organizer-skills@event-sponsor-fulfillment` - delivers what was promised and writes the renewal-driving post-event report.
- `samber/dev-event-organizer-skills@event-positioning` - the community-vs-vendor pole this skill branches on, and how the event stands out among local alternatives, are positioning choices made there.
- `samber/dev-event-organizer-skills@business-event-formats` - business-oriented activity shapes that make the claimed categories deliverable on-site.
- `samber/dev-event-organizer-skills@event-first-edition` - the no-track-record case; its evidence gates feed this skill's first-edition substitutes.
