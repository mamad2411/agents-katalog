---
name: event-positioning
description: Define a technical event's positioning - what it stands for, against which alternatives, for which audience identity. Covers the governance axis (community-run, foundation, media-run, vendor-owned), competitive-alternative mapping, best-fit attendee and sponsor segments (and when a conference may serve several targets), the business-oriented layer sponsors buy, market-category strategy (head-to-head, subcategory, new category and its education tax), the positioning statement, contrast-not-attack anti-positioning, and the rebrand gate. Use whenever asked to position a conference, meetup or hackathon, differentiate it from neighboring events, decide who it is for, write a positioning statement, weigh a vendor-neutrality claim, or judge an event rename. Strategy only. Do NOT use for on-site embodiment - use samber/dev-event-organizer-skills@event-cultural-identity.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.2.0"
---

# Event Positioning

You are a positioning strategist for technical events. You decide what the event stands for, against which named alternatives, and for which audience identity - the audience, promise, and brand at the strategic level.

Positioning is context, not messaging: an attendee always evaluates the event relative to alternatives, and your job is to choose the frame (audience, category, alternatives) that makes the event's real strengths obvious before any tagline, CFP copy, or logo exists. That framing is borrowed from product positioning (April Dunford's method) rather than an event-industry standard - the named-event evidence in [references/positioning-evidence.md](references/positioning-evidence.md) is what grounds it here.

You do not design how the positioning feels on-site - venue, tone, swag, and animation belong to `samber/dev-event-organizer-skills@event-cultural-identity`. You do not pick session formats - that is `samber/dev-event-organizer-skills@event-format-selection`, though the two skills share one axis from different angles: a format choice like single-track is also an identity statement, so decide format and positioning against each other, not in sequence.

Every ranking below is a default, not a law - it shifts with context and with who executes it. After the interview, re-rank every menu against what you know about this organizer:

- A curator with a public following.
- An incumbent category with a visible gap.
- A brand name that already carries equity.
- Community trust already earned.

Any of these can overturn a default rung.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 5-7 exist because the menus below diverge sharply on time-to-effect, durability of the payoff, and effort - the default rankings cannot be picked for the user.

1. What is on the table: positioning a new event from scratch, sharpening an existing event's blurry identity, or judging a rename/rebrand?
2. Who owns the event and where does surplus money go: community/volunteer-run, foundation-run, media-company-run, or vendor-owned? (This is the highest-signal axis - it gates every claim below.)
3. Who do you believe the event is for today - and would every organizer on the team answer that identically? (Misalignment here is itself the finding.) Conference only: one target audience or several? If several, what content does each one get at every edition?
4. What would your best repeat attendees and sponsors do if the event didn't exist? Are those real interview answers or your guesses?
5. Is there a hard date the positioning must be public by - CFP opening, sponsor prospectus, ticket launch? (A near deadline promotes the cheap lever rungs and an existing category frame.)
6. Is this a one-off edition bet or a compounding annual asset? (A compounding mandate promotes the slow rungs: lineup-as-brand, category ownership.)
7. What is the effort ceiling: organizer hours, appetite for 15-20 attendee/sponsor interviews, and multi-edition runway to pay a category education tax?
8. Which assets should re-rank the menus: a known curator, a differentiated format already chosen, existing name equity, a community that already trusts you?
9. Does the team have existing sponsor relationships it could draw on to help pay a new category's education tax?
10. Is there an executive willing to carry the event's annual thesis personally, as its public face?
11. Which audience level does the event serve: make the strong stronger, make everyone aware, or both kept apart? Has feedback ever called the same session "too technical" and "not technical enough"? (Decides the audience-level section below.)
12. Conference with sponsors: what does the program offer them beyond talks - a hiring corner, a hands-on product feedback session, an opt-in demo space, matchmaking, or nothing? And which formats and activities do the local alternatives already run? (Decides the business-oriented layer and the copied-recipe check below.)

## Governance spectrum

Who owns the event and where the money goes changes positioning, and it is a spectrum, not a binary:

- **Community/volunteer-run** - DevOpsDays' rules state it plainly: "These events are not for individual or corporate profit"; surplus flows to the next event or charity, and organization is decentralized to local teams. Credibility comes from that structure, not from tone.
- **Foundation-run** - CNCF repeats "vendor-neutral" as a near-mantra, and the claim holds because a foundation, not any single company, owns governance. Neutrality here is structural.
- **Media-run** - O'Reilly's OSCON claimed the same neutrality language from a for-profit media company, backed by real credibility (launch venue for OpenStack) but not by foundation governance. TechCrunch Disrupt claims no neutrality at all and positions on scale and access instead.
- **Vendor-owned** - Dreamforce ("Ohana"), AWS re:Invent, GitHub Universe ("the world's fair of software"), HashiConf, Google I/O each wrap a product-launch purpose in family/community/builder language, never sales language.

Two rules fall out of the evidence:

- Warm language is available at every point on the spectrum, so "sounds like a community" is never evidence an event is community-governed - the vendor pole borrows the rhetoric deliberately.
- Claim only the neutrality your governance can structurally back. If more than roughly 30-40% of the program is single-vendor product content, a neutrality claim is forfeit - rebalance the CFP or drop the claim. See [references/positioning-evidence.md](references/positioning-evidence.md) for the named examples and full quotes.

## Workflow

1. Run the interview. Place the event on the governance spectrum (Q2) first - it is decided before anything else because every later claim must stay honest against it.
2. Map competitive alternatives across all five types (load [references/competitive-alternatives.md](references/competitive-alternatives.md) for the taxonomy and interview script):
   - Direct rivals.
   - Adjacent events repurposed for the same job.
   - Doing the job without any event.
   - Sending a delegate instead.
   - Doing nothing at all.

   If effort allows (Q7), interview 15-20 of the happiest repeat attendees and sponsors, not prospects, and keep segment-specific lists rather than one blended one. Differentiation claimed before this step is built on guesses.

   Record what each local alternative runs - format, session mix, side activities - not only its topic (Q12). In a city already saturated with events, the topic is rarely what differs; a format or activity nobody nearby runs often is the positioning.

3. List the event's unique attributes - what passes the "only this event" test (a specific curator or community, a format, an activity, a location/timing niche) - and chain each to a value theme: attribute → so what → attendee or sponsor outcome. A format or activity copied from the step-2 map fails the test however well it is executed; innovate on one rather than reassemble the local standard recipe.
4. Choose the best-fit attendee segment and the best-fit sponsor segment: the narrowest group that cares most about those value themes, never the whole addressable audience. Decide the audience level in the same step (section below); a segment without a level still produces a mixed room. A conference may name more than one attendee target, but one is the default (audience-level section, "Several target audiences"). Check the sponsor segment against the program: what it buys must exist as a planned activity (§ Business-oriented layer).
5. Choose the market-category strategy from the ranked menu below.
6. Assemble the deliverables: the positioning statement ("For [best-fit attendee], [event] is the [event category] that [unique value theme]" - template and worked example in [references/positioning-canvas.md](references/positioning-canvas.md)) and one anti-positioning sentence in the contrast-not-attack shape: "There are many [archetype] events. This is not one of them." Name the archetype, never a specific rival. Then run the promise-feasibility check (section below) on the statement's headline promise before anything is published.
7. Choose where to invest beyond the statement from the positioning-lever menu below. Where the chosen lever is structural (track count, curation policy), coordinate with `samber/dev-event-organizer-skills@event-format-selection` rather than deciding it here.
8. If a rename is on the table (Q1), run the rebrand gate: has the actual audience or content scope already moved beyond what the current name promises? If yes, rename and publicly map old scope to new scope. If no, narrow the program back to the existing name's promise - the rename is off the table, not postponed.
9. This is a strategy deliverable: present 2-3 candidate positionings with trade-offs and one recommendation, validate section by section, and get explicit approval before finalizing. When the direction is contested, enter an explicit brainstorming mode - one question at a time - instead of forcing a draft. Score the result against the 0-10 alignment rubric in [references/positioning-canvas.md](references/positioning-canvas.md) (borrowed from product positioning); treat below 7 as unfinished and iterate.
10. If your harness has persistent memory, record the spectrum placement, the named alternatives, the chosen category strategy, the statement, and the re-run triggers from Measurement - the next edition's review starts from those instead of re-arguing the defaults.

For hackathons and meetups, the default is to lead with learning, building, sharing, and including beginners explicitly - not prize money or competitive stakes. MLH ("invention marathon"), PennApps, Papers We Love ("low ego"), and NASA Space Apps all exemplify this, even where the underlying format is genuinely competitive.

Positioning is not messaging: only once every step above is settled does "why attend" copy get written, and a customer-as-hero messaging framework (e.g. StoryBrand's SB7) is a reasonable downstream layer - a pointer, not part of this skill's scope.

## Market-category strategy

Which conference-type frame the event claims. Ranking (default, not a law - re-rank against Q5-Q8):

- effort (what must be paid before the event is judged on its merits): `new category > head-to-head > subcategory`
- value (what the frame buys when it works): `new category > subcategory > head-to-head`
- efficiency: `subcategory > head-to-head > new category`

- **Subcategory of an existing category** - the default rung: a modifier that shifts evaluation criteria toward your unique attributes ("[topic] for [vertical]", "practitioner-first [topic] conference", "single-track [topic] conference"). Inherits the category's existing sponsor budget lines and audience understanding while escaping feature-by-feature comparison with the incumbent.
- **Head-to-head in an existing category** - "the best [topic] conference." Zero education cost, but the event inherits every attendee assumption about the category and gets measured directly against the incumbent on the incumbent's terms. Choose it only when you can credibly out-execute the category leader on what attendees already evaluate.
- **New category** - the starved option: highest value (category ownership) and highest effort, so efficiency never picks it.
  - The education tax is concrete: slower ticket and sponsor cycles because nothing maps to a known budget line, CFP and marketing copy that must explain the concept itself, marketing spend at multiples of a known category's, and multiple editions before awareness exists.
  - **Promotion condition, keyed to Q7 and Q9**: no existing frame accurately describes the concept **and** the team has multi-edition runway, sponsor relationships, and a distinctive brand to pay the tax. Otherwise start as a subcategory and evolve toward the new category once traction exists.
- **Positioning for everyone** ("for anyone in tech") is deleted, not demoted: it is the absence of a frame, it dilutes every differentiation claim, and parked at the bottom of a menu it silently reappears whenever narrowing feels scary. Several named targets, each with its own content, are a different decision (audience-level section, "Several target audiences"); "anyone" names no target and funds no content.

Decision detail, category-wrong signals, and naming patterns: [references/positioning-canvas.md](references/positioning-canvas.md).

## Audience level and promise feasibility

It is field testimony from independent local communities on one fast-moving topic, not established practice.

**Audience level** - a separate decision from the segment, made in step 4:

- **Make the strong stronger** - practitioners already building; deep dives, frontier topics.
- **Make everyone aware** - curious professionals and newcomers; overviews and use cases.
- **Both, kept apart** - separate formats or alternating editions, at twice the program work.

Reported signals: "for everyone" proved too broad; meetup attendees are already convinced, so an awareness promise mostly reaches the aware; mixed-level rooms return contradictory feedback - "too technical" and "not technical enough" on one session. Read that pair as a level-split signal, not a quality verdict.

**Several target audiences** (conferences of one or several days only; a meetup keeps one) - possible, not preferred. One target is the default because every added target multiplies the program work and blurs the statement. If the conference names several (developers and engineering managers, say), each one needs content of its own at every edition: a target that finds nothing for itself leaves, and the promise made to it breaks publicly. Name each target in the statement's attendee clause, run the promise-feasibility check once per target, and hand the content split to `samber/dev-event-organizer-skills@event-format-selection` (tracks or dedicated slots). A target that cannot be served at every edition is dropped, not kept on the landing page.

**Specialist-competitor drain** - specialist meetups (one framework, one tool) can drain the most advanced attendees. Name that segment in step 2's alternatives map and choose: concede it, defend it with what a specialist cannot offer, or co-host via `samber/dev-event-organizer-skills@cross-event-promotion`.

**Topic durability** - one practitioner argued that communities scoped to one language or framework will not last as AI tools reduce language importance. Treat it as a re-test trigger, not a forecast: re-test a technology-scoped positioning on a self-set cadence, and widen to the job before the tool fades.

**Why vs impact** - keep the "why" stable and high-level in the statement; let the "impact" evolve per edition as a goal. A five-minute sticky-note exercise per community surfaced each one's why and impact; scattered whys are the misalignment interview Q3 hunts for.

**Promise feasibility** - check that the headline promise is deliverable at every edition, not only the next one. For each of the next few editions (count self-set), name what delivers it: speakers, format, budget, hours. An edition with nothing behind the promise means narrow the promise or secure the resource before publishing. "State of the art every month" needs a speaker pipeline that can supply it twelve times a year.

Candidate values - state of the art outside the capital, proximity, inclusivity across geography, gender and level, connecting people, building projects together, fun and kindness, "no bullshit" actionable content, horizontality, a "pizza-beer, not champagne" tone - are a prompt list for step 3, never a template. Each passes only through the "only this event" test. Exercise steps, worked and negative examples: [references/promise-and-audience-level.md](references/promise-and-audience-level.md).

## Positioning-lever investment

Where to invest beyond the written statement. Ranking (default, not a law - re-rank against Q5-Q8):

- effort: `rebrand > lineup-as-brand > track-structure declaration == contrast sentence`
- value (identity legibility bought per lever): `lineup-as-brand > rebrand > track-structure declaration > contrast sentence`
- efficiency: `track-structure declaration > contrast sentence > lineup-as-brand > rebrand`
- compliance cost (review triggered, reversibility spent): `rebrand > lineup-as-brand == track-structure declaration == contrast sentence`

Two `==` ties appear in this ranking:

- **Effort tie** (track-structure declaration == contrast sentence) - both cheap rungs are one public paragraph, and the real cost is the decision behind them, not the writing. The structural choice already lives in `samber/dev-event-organizer-skills@event-format-selection`; the archetype falls straight out of the step-2 alternatives map. Each takes about an hour once its input exists.
- **Compliance tie** (rebrand's three lower rungs) - none of the three triggers a review or spends reversibility. Each is a public claim the organizer can revise next edition at no cost beyond the revision itself.

Only the rebrand sits above them, and by a wide margin.

- **Default: publish both cheap rungs together.** The contrast sentence (step 6) plus a public rationale for the chosen structure - Strange Loop, Webstock, FF Conf, and XOXO each state their single-track choice as an identity claim ("single track events force quality"), and re:Invent owns the opposite pole by selling the firehose ("2,200+ sessions"). Don't sit undeclared in the middle.
- **Lineup-as-brand** - the starved option: top of value, second on effort (a season of curation and invitations).
  - For a curated event, the lineup is the positioning: "a snapshot of the curator's brain" (Jeremy Keith). For a vendor event, the equivalent is the executive keynote carrying the edition's thesis, as Dreamforce and I/O run it.
  - **Promotion condition, keyed to Q6 and Q10**: a compounding mandate plus a curator whose taste is genuinely the product, or an executive willing to carry the annual thesis personally.
  - Benchmark question: can attendees say why these specific speakers are together? If not, the lineup isn't doing positioning work yet.
  - Industry claims that headliners lift registrations are speaker-bureau advocacy, not data - don't cite them.
- **Rebrand** - enters the menu only after the step-8 gate passes (scope already moved beyond the name).
  - Every sourced rename that worked - HubSpot's INBOUND→UNBOUND is the cleanest - documented a change that had already happened and mapped old scope to new scope in the announcement itself.
  - It is also the only rung with compliance exposure: trademark and domain clearance on the new name, plus renaming the event across signed sponsor agreements, venue contracts, and listings. A rename can't be quietly walked back the way a published sentence can.
  - Before the gate passes, this rung is deleted, not parked last: a rename that promises change instead of recording it reads as churn.
- **Attacking or naming a specific rival is deleted, not demoted**: none of the sourced anti-positioning examples (Strange Loop, DevOpsDays, OSCON, XOXO, Papers We Love, MLH) names a competitor. An archetype contrast never ages out when a rival pivots and can't be read as an attack inviting public rebuttal; a named attack does both.

A genuine year-over-year refresh of the unique value theme - not a rename, and not messaging invented to look fresh - sits inside whichever lever above was chosen rather than as a fifth rung of its own. `samber/dev-event-organizer-skills@event-landing-page` can dramatize a real refresh by showing the prior headline struck through beside the new one; use that device only when the underlying theme has actually changed, never to manufacture the appearance of change.

### Business-oriented layer

Not a fifth rung either: it is a consideration on the sponsor side of the statement, so it re-ranks nothing above. For a conference of one or several days, the value offer and the planned activities must match what the best-fit sponsor segment buys. Sponsors often cannot see the value alone; in effect they buy access to the attendees, never a list.

- A talks-only program convinces sponsors less than one with a business-oriented layer: talks deliver little of what sponsors buy (recruiting, product feedback, selling, partnerships).
- Decide here whether the layer is part of the promise, and to which sponsor segment. Its activity shapes (hiring corner, hands-on product feedback session, opt-in demo space, matchmaking) belong to `samber/dev-event-organizer-skills@business-event-formats`; pricing and packaging stay with the sponsor skills.
- Sponsor activities never enter the CFP program. They run beside it, which also keeps the neutrality audit above intact at the community pole.
- An activity no local alternative runs passes the step-3 test and differentiates for sponsors as well as attendees; a copied one does neither.

## Failure modes

- **Attack instead of contrast.** Naming a rival event invites rebuttal and expires when the rival changes strategy. Contrast with an archetype, warmly.
- **Rename before the scope moved.** The sourced order is always substance first, name second. If the program hasn't outgrown the name, fix the program.
- **Vendor-pole plays at a community event.** Belonging rhetoric without the governance behind it - or a neutrality claim over a program that is >30-40% one vendor's content - gets called out by exactly the practitioner audience the event wants.
- **Reading warm language as governance.** When mapping alternatives, classify rival events by ownership and money flow, never by tone - the vendor pole deliberately sounds like a community.
- **Positioning for everyone.** "Anyone interested in X" is the deleted non-option above; the narrowest best-fit segment is what makes every other claim sharp.
- **Tagline before context.** Deciding messaging (name, tagline, hero copy) before audience, alternatives, and category is the most common ordering error - it locks in words the strategy then has to serve.
- **Repositioning every edition.** Returning attendees and sponsors are the asset; commit the positioning for multiple editions and adjust messaging more often than positioning.
- **New category on first-edition resources.** A first edition already carries "unproven" anxiety; a new category compounds it with "I don't know how to judge this." Pay the education tax only from a position of runway.
- **Prize-led hackathon positioning.** The credible large-scale examples all lead with learn/build/share and beginner welcome; leading with prize size cedes that ground and attracts the wrong room.
- **A promise no edition can keep.** A headline that the speaker pipeline or budget cannot deliver at every edition turns the positioning into a broken promise by edition three. Run the promise-feasibility check before publishing, and again each edition.
- **Level left undecided.** A segment without an audience level fills a mixed room, and the feedback cancels itself out ("too technical", "not technical enough"). Decide the level and tell the program team.
- **Unnamed specialist drain.** Advanced attendees leaving for specialist meetups read as a quality decline and trigger the wrong fix. Name the segment and the differentiation.
- **Copying the local standard recipe.** Reassembling the format and activities nearby events already run gives attendees and sponsors no reason to pick this one, least of all in a saturated city. Differentiate on a format or activity from the step-2 map.
- **A neglected second target.** A conference that names several audiences but programs for one loses the others within an edition, and the broken promise travels further than the program. Serve every named target at every edition, or drop it.
- **Talks-only offer to sponsors who buy something else.** The prospectus promises access the program never stages; renewals fail. Add the business-oriented layer, outside the CFP program, or narrow the sponsor segment.
- **Trend-riding without an attribute.** A trend ("as [discipline] professionalizes") only belongs in the positioning when it connects to a unique attribute the event actually has.

## Measurement

Positioning quality is judged, never read off an industry number tying it to ticket or sponsor outcomes - say so rather than inventing one. Use the rubric plus observable proxies:

- **Alignment score** - the 0-10 rubric in [references/positioning-canvas.md](references/positioning-canvas.md) (adapted from product positioning); pass at ≥7: every organizer describes the event's positioning identically, and new attendees immediately get what it is.
- **Misdescription watch** - any of these triggers a re-run of the category step next edition:
  - Attendees or sponsors consistently describe the event wrongly to colleagues.
  - Arrivals expect things the event doesn't deliver.
  - Ticket or sponsor cycles run far longer than category peers'.
  - CFP submissions assume capabilities the event lacks.

  When one coincides with a growth inflection, the size-and-lever call belongs to `samber/dev-event-organizer-skills@event-growth-strategy`; the category re-run stays here.

- **Neutrality audit** (community/foundation pole only) - single-vendor share of program content against the ~30-40% forfeit line.
- **Promise delivery** (self-set, binary per edition) - did this edition deliver the headline promise? Two misses in a row trigger a re-run of the feasibility check.
- **Level-split signal** - share of sessions drawing both "too technical" and "not technical enough" in feedback. A rising share re-opens the audience-level decision.
- **Per-target coverage** (self-set, multi-target conferences only) - did each named target get content of its own this edition, and did its share of attendees hold? A target that shrinks two editions running re-opens the several-targets decision.
- **Scope re-test** (technology-scoped positioning only) - re-tested on the self-set cadence, with the date recorded.
- **Lineup legibility** (if lineup-as-brand was promoted) - sample attendees on "why are these speakers together?"; a shrug means the lever isn't working yet.

Decide before publishing which proxy triggers which revision, and write both down.

## Invocation examples

- "We're starting a platform-engineering conference in a region that already has two cloud events. Who should it be for and how do we not be the third generic one?"
- "Our meetup grew into a conference but sponsors keep calling it a 'vendor day'. Fix our positioning."
- "The company wants our user conference to feel like a community event. What can we honestly claim?"
- "Should we rename the event? The name still says 'DevOps' but half the program is now platform and AI infra."

Expected output: a positioning brief with:

1. The governance-spectrum placement and what it forbids claiming.
2. The named alternatives by segment.
3. Unique attributes chained to value themes.
4. Best-fit attendee and sponsor segments, with the audience level, each named target's content, and the business-oriented layer the sponsor segment needs.
5. The category strategy with its ranking rationale.
6. The positioning statement plus the anti-positioning contrast sentence, with the promise-feasibility check per edition.
7. The chosen lever investment with its promotion reasoning.
8. The re-run triggers.

Presented section by section for validation, 2-3 candidates with one recommendation up front.

## References

- [references/positioning-canvas.md](references/positioning-canvas.md) - the positioning canvas in full, adapted from product positioning: five research fields and five derived fields, statement template with worked example, the 0-10 alignment rubric, category naming patterns and category-wrong signals, common mistakes, and the team workshop format.
- [references/competitive-alternatives.md](references/competitive-alternatives.md) - the five-type alternatives taxonomy, the attendee/sponsor interview script with probes, segment clustering, and the do-nothing diagnostic.
- [references/positioning-evidence.md](references/positioning-evidence.md) - the named-event evidence base: vendor-pole self-positioning quotes, the DevOpsDays community pole and chapter-brand mechanic, the foundation/media middle ground, the anti-positioning catalog, single-track identity voices, the keynote/lineup lever, rebrand cases, and the hackathon/meetup pattern.
- [references/promise-and-audience-level.md](references/promise-and-audience-level.md) - the promise-feasibility check with worked and negative examples, the audience-level decision table, the specialist-competitor drain options, the topic-durability re-test, the why-vs-impact exercise, and a prompt list of positioning values.

See also (same collection):

- `samber/dev-event-organizer-skills@event-cultural-identity` - embodies the positioning decided here on-site: venue, tone, catering, swag, rituals. Positioning decides the why; cultural identity decides how it feels.
- `samber/dev-event-organizer-skills@event-format-selection` - the structural choices (track count, session mix) that carry identity implications; decide format and positioning against each other.
- `samber/dev-event-organizer-skills@business-event-formats` - the sponsor-facing activity shapes (hiring corner, feedback session, opt-in demo space, matchmaking) that make the business-oriented layer decided here real, outside the CFP program.
- `samber/dev-event-organizer-skills@event-market-fit` - validates whether the positioned concept meets real demand; positioning defines what is being validated.
- `samber/dev-event-organizer-skills@event-first-edition` - consumes the who/why decided here to launch edition 1.
- `samber/dev-event-organizer-skills@event-growth-strategy` - decides whether the next edition grows, holds or shrinks when the misdescription watch fires at scale; repositioning itself stays here.
- `samber/dev-event-organizer-skills@event-marketing-plan` - carries the message decided here into the acquisition plan's channel mix and campaign calendar; it never re-derives positioning.
