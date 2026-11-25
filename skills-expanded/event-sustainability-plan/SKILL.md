---
name: event-sustainability-plan
description: "Plans, measures and reports the environmental footprint of a technical event the user organizes, and writes its public sustainability page without greenwashing, from a screening estimate of attendee travel (usually the dominant line) and ranked reduction levers to offset-free claim wording. Use whenever an organizer mentions a conference or meetup carbon footprint, a green or low-carbon event, conference waste, an event sustainability page or report, an event's carbon-neutral or offset claims, or ISO 20121 - even without saying 'sustainability'. Not for a company's own business-travel inventory or product claims. Do NOT use for financial or organizer-burnout sustainability - use samber/dev-event-organizer-skills@event-budget or samber/dev-event-organizer-skills@event-team-structure."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Sustainability Plan

You plan the environmental side of one technical event: how big its footprint is, which levers move it, what data proves it, and what the organizers may honestly say in public. Three artifacts come out:

- **The plan** - screening estimate, boundary, ranked levers, data-capture deadlines.
- **The public sustainability page** - what the event does and does not claim.
- **The post-event report skeleton** - the inventory the plan promised.

Attendee travel decides this subject. Published conference studies, all modelled or survey-extrapolated, put travel at roughly 80-97% of the total, most of it from the minority who fly long-haul. Catering, waste and swag are real but second-order on carbon, and they are exactly where greenwashing hides. Every output keeps that order visible.

## What you own and what you hand off

This skill sets targets, constraints and numbers. Siblings take the decisions those numbers inform:

| Sibling                                                           | The line                                                                                                                                     |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `samber/dev-event-organizer-skills@event-venue-sourcing`          | Runs the venue search and contract. You hand it criteria: rail access, metered energy data, waste-stream reporting. Never pick the venue.     |
| `samber/dev-event-organizer-skills@event-format-selection`        | Decides in-person, hybrid, virtual, hubs, cadence. You hand it the footprint delta of each option. Never decide format for carbon alone.     |
| `samber/dev-event-organizer-skills@hybrid-event-design`           | Designs the remote side once hybrid is chosen.                                                                                               |
| `samber/dev-event-organizer-skills@virtual-event-production`      | Runs a fully online event; its footprint is mostly the digital line.                                                                         |
| `samber/dev-event-organizer-skills@event-hospitality`             | Picks catering style and break content. You hand it a plant-based default and a food-waste measurement ask. Never write the menu.            |
| `samber/dev-event-organizer-skills@event-cultural-identity`       | Picks the swag rung. You report swag's waste line and forbid commodity swag under a green claim.                                             |
| `samber/dev-event-organizer-skills@event-vendor-sourcing`         | Briefs and contracts caterers, swag and print. Your asks (reusable lanyards, food donation, kg reporting) go into its brief.                  |
| `samber/dev-event-organizer-skills@event-sponsor-pricing`         | Owns sponsor-bought lanyards, swag-bag inserts and branded bottles. Cutting them is a pricing change you route there.                         |
| `samber/dev-event-organizer-skills@event-accessibility-inclusion` | Owns travel grants and access provisions. A travel cut never overrides an access commitment.                                                 |
| `samber/dev-event-organizer-skills@event-budget`                  | Holds the cost of any lever and any climate-contribution line.                                                                               |
| `samber/dev-event-organizer-skills@event-landing-page`            | Builds the site. You write the sustainability page text it publishes.                                                                        |
| `samber/dev-event-organizer-skills@event-debrief`                 | Runs the post-event review. Your report feeds it as one input.                                                                               |

## Interview

Ask one question at a time, multiple-choice where possible. When the request already answers a question, restate the answer in one line for confirmation and ask only the gaps. Questions 7-9 exist because the levers diverge sharply on time-to-effect and effort: nobody can pick those defaults for the user.

1. Event shape, size, days, and edition number? First edition or recurring?
2. What is still open: host city, venue contract, format, cadence, registration form, catering contract, swag order? Are talks streamed or recorded? A signed item closes its lever for this edition.
3. Where do attendees and speakers come from? Last edition's registration or billing countries, or the best guess by region. How many fly, how many long-haul, how many are local? How many speakers, volunteers, organizers and sponsor staff, and how many hotel nights on average?
4. What does the user need: an internal plan, a public page, a post-event report, a sponsor or funder requirement, ISO 20121?
5. Where is the event marketed and to whom: EU, UK, US (which states), elsewhere; tickets sold to individuals or only to companies? This sets the claim rules.
6. Which trips does the event book or pay for: keynotes, invited speakers, travel grants? Which access commitments are already published?
7. By what date must the result land: before the venue contract, before registration opens, before the page goes live, after the event?
8. One-off result for this edition, or a baseline the next editions improve on?
9. Effort ceiling: who owns this, how many hours per month, any budget for a rail deal, a measurement tool, or a contribution?

## Evidence rules

These hold in every output, because a single invented number discredits the whole page.

- **Never write an emission factor you cannot cite.** Tell the user to pull the current edition of a named public set (UK DESNZ GHG conversion factors, the ICAO calculator, ADEME Base Empreinte in France) and record set, edition year and unit. The screening estimate needs only a handful: one per flight band and travel mode, one hotel night, one grid factor. If you can browse the web, fetch them from the publisher's own page and cite it; otherwise leave named placeholders.
- **State the radiative-forcing choice for flights.** DESNZ multiplies flight CO2 by 1.7 for non-CO2 effects; other methods use higher multipliers. Pick once, say it on the page, keep it across editions.
- **Give ranges, not points.** Two published estimates of the same meeting (AGU 2019) differ by about 60%. Report low and high from the origin-data spread and the factor choice.
- **Label every line measured, surveyed or estimated.** A reader can act on that label without knowing how you built it.
- **Count all participant travel:** attendees, speakers, volunteers and sponsor staff, even though the organizer does not control it. Leaving out the dominant line is the most common way an event footprint misleads.
- **Name one owner per line.** Venue energy and a speaker's employer-paid flight are counted elsewhere too; say whose inventory each line belongs to. Trips the event pays for belong to the organizer.
- **Never promise neutrality on offsets, or a future target without a plan behind it.** Both shape the plan, not just the page: see Claims below.

## Workflow

1. **Write down what is closed.** Signed venue, closed format decision, live registration form, catering contract. A closed item removes its lever from this edition and moves to "next edition" in the plan.
2. **Build the screening estimate** before ranking anything. Bucket participants by origin band and likely mode, multiply by a cited factor, add accommodation nights, then sketch the smaller lines. Worksheet, factor sets, data-quality labels and double-counting owners: [references/footprint-screening-and-boundary.md](references/footprint-screening-and-boundary.md).
3. **Write the concentration line and place the audience centre:** what share of participants fly long-haul, what share of the travel line they produce, and whether the current city sits near the centre of the origin buckets. Together they pick the lever profile below.
4. **Set the boundary** on the 9 Net Zero Carbon Events categories, in or out with a reason and an owner for each.
5. **Rank the levers** with the profile the concentration line picks, then re-rank against the interview.
6. **Present 2-3 lever plans** with their trade-offs (for example "structural this edition", "quick rungs now, structural next edition", "remote-first for long-haul") and a recommendation. Get the user's choice before drafting anything public.
7. **Schedule the data capture.** Origin and mode go into the registration form before it opens; venue kWh, meals served and waste weights go into contracts before signature. A field missed here cannot be recovered. Field list and privacy handling: section 6 of the screening reference.
8. **Draft the public page** with the claim rules below, section by section, and validate each with the user.
9. **Hand off** each constraint to its sibling (table above) and record the cost of each lever for `event-budget`.
10. **After the event**, fill the report skeleton and compare with the screening estimate. Flag any boundary or factor change before comparing editions.

## The lever menu, ranked

Ranked by efficiency: emissions avoided per unit of organizer effort. Value is the share of the footprint a lever can move; effort is organizer time, coordination and reversibility. Food waste and swag avoid almost no emissions, so they sit outside the carbon ranking as waste rungs (end of this section).

**Pick the profile first.** Place the audience's centre from the origin buckets, then read the concentration line:

- **Off-centre override.** If the current city sits far from the audience's centre and a better-placed city exists, host-city relocation leads in every profile: one off-centre conference modelled a 45% cut from a central venue.
- **Long-haul profile:** long-haul flyers produce more than about 60% of the travel line.
- **Rail profile:** most flyers are short-haul and have a rail option under about a working day.
- **Domestic-flying profile:** most flyers are short- or medium-haul with no practical rail option, as at most North American events.
- Between about 40% and 60%, or when two profiles fit, show both in the plans of workflow step 6. The cut-offs are self-set.

**Long-haul profile**

- efficiency: `organizer-booked travel policy > remote speaking option > train-times page > plant-based default > venue energy ask > remote attendance tier > rail deal > rail-first host city > cadence > regional hub`
- value: `remote attendance tier > cadence > regional hub > remote speaking option > organizer-booked travel policy > rail-first host city > rail deal > train-times page > plant-based default > venue energy ask`

**Rail profile** (remote attendance tier and regional hub deleted: no distant cluster to serve)

- efficiency: `train-times page > plant-based default > organizer-booked travel policy > rail-first host city > rail deal > venue energy ask > remote speaking option > cadence`
- value: `rail-first host city > cadence > rail deal > train-times page > plant-based default > organizer-booked travel policy > remote speaking option > venue energy ask`

**Domestic-flying profile** (train-times page and rail deal deleted; regional hub deleted unless a second cluster exists)

- efficiency: `organizer-booked travel policy > remote speaking option > plant-based default > venue energy ask > host city near the audience centre with direct flights > remote attendance tier > cadence`
- value: `cadence > remote attendance tier > host city near the audience centre > remote speaking option > organizer-booked travel policy > plant-based default > venue energy ask`

**Effort, every profile, highest first:** `regional hub > cadence > remote attendance tier > host city > rail deal > remote speaking option > organizer-booked travel policy > venue energy ask > train-times page > plant-based default`

Table rows follow the long-haul efficiency line.

| Lever                          | Value (long-haul / rail / domestic) | Effort | Control   | Organizer effort, order of magnitude | Condition and guard                                                                                                                   |
| ------------------------------ | ----------------------------------- | ------ | --------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| Organizer-booked travel policy | `++` / `+` / `++`                   | `++`   | decide    | one written policy                   | Economy, direct flights, rail under a set journey time, regional keynotes; access exceptions owned by `event-accessibility-inclusion`. |
| Remote speaking option         | `++` / `+` / `++`                   | `+`    | influence | hours per speaker                    | Offer, never impose; same slot, same billing; never in place of a travel grant.                                                       |
| Train-times page               | `+` / `++` / deleted                | `+++`  | influence | an hour                              | Routes and times from the main origin cities. Moves only flyers who have a rail option.                                              |
| Plant-based catering default   | `+` / `+` / `+`                     | `+++`  | decide    | one line in the caterer brief        | About 1-3% of travel at one modelled conference: small, cheap, visible. Alternatives on request.                                      |
| Venue energy ask               | `-` / `-` / `-`                     | `++`   | influence | one request in the venue brief       | Separate a renewable supply contract from unbundled certificates.                                                                     |
| Remote attendance tier         | `+++` / deleted / `++`              | `--`   | influence | a standing job                       | Input to `event-format-selection`; remote engagement and cost evidence is poor. Offer, never steer one region to it.                  |
| Rail deal with an operator     | `+` / `++` / deleted                | `-`    | influence | weeks of back-and-forth              | Worth it once the host city is fixed and a large share can arrive by train.                                                           |
| Host city                      | `+` / `+++` / `++`                  | `-`    | decide    | a day of desk work, plus a new venue | Only while the venue is unsigned. Choose by attendee origin, not by the team's home city.                                             |
| Cadence                        | `+++` / `++` / `+++`                | `---`  | decide    | a community-wide decision            | Biennial, or alternating in-person and online years. Route to `event-format-selection` and `event-budget`.                            |
| Regional hub or edition        | `+++` / deleted / deleted           | `---`  | decide    | a quarter or more, a second team     | The starved option, see below.                                                                                                        |

**Recommended default rung:** take the matching profile's efficiency line in order, down to the effort ceiling from interview question 9. Structural rungs that miss the ceiling become next-edition commitments.

**Waste rungs, added on top.** Food-waste weigh-and-donate (a contract clause; check the venue's catering exclusivity and food-safety rules allow donation) and swag, lanyards and single-use plastics (one decision plus a sponsor talk; keep bendable straws available without asking). Run them alongside the carbon rungs, never in place of one, and never as the headline.

**What this order starves:** cadence and the regional hub top value and lose every efficiency round, because they split or thin the community. Promote cadence when long-haul or domestic flying dominates, the event is recurring, and the community has said it would accept a gap year. Promote a hub when a strong second audience cluster sits on another continent with a partner team ready to host.

**Re-rank against the user.** Each of these overturns a default:

- Venue already signed: delete the host-city rung for this edition and carry it to the next.
- Audience mostly local and arriving by transit: travel shrinks, so catering and venue energy move up.
- Format closed as in-person: delete the remote attendance tier. Remote speaking moves up, since it keeps most of its value at a fraction of the effort.
- Hard deadline before the page goes live: a structural rung whose decision point falls inside the window still fires (comparing host cities before an unsigned venue is desk work); one whose decision point falls after it goes on the page as a next-edition commitment.
- Sponsors already bought swag bags or lanyards: that rung costs sponsor revenue, so route it to `event-sponsor-pricing`.
- Travel grants or access commitments: they win over any lever. Never rank speakers or attendees by their flight footprint, and say so in the plan when a commitment blocks a lever.

Evidence and precedents for every rung, including the hybrid engagement counterweight: [references/lever-evidence.md](references/lever-evidence.md).

## Claims the page may make

Offsets are not reductions. In the EU, since 27 September 2026, claiming that a product has a neutral, reduced or positive greenhouse-gas impact because of offsetting is a blacklisted commercial practice, whatever the credit quality; a conference ticket sold to individuals is such a product. Future targets ("net zero by 2030") need a detailed, realistic plan verified by an independent expert. The UK requires saying how far emissions were reduced versus offset. Not legal advice: flag the jurisdiction and suggest a review before publishing.

```
// ✓ Good - estimate, method, actions, contribution kept separate
We estimate [low]-[high] t CO2e ([factor set, edition], flights with radiative forcing).
About [share]% is travel. We chose a city with direct trains from most of our audience
and contributed EUR X to [named project]. This does not cancel our emissions.

// ✗ Bad - neutrality on offsets, generic label, hides the dominant source
A carbon-neutral, eco-friendly conference: zero plastic, all offset!
```

Rules by jurisdiction, banned wording, target wording, contribution criteria, ISO 20121 self-declaration, page and report templates: [references/claims-page-and-report.md](references/claims-page-and-report.md).

## Failure modes

| Rationalization                                            | Why it is wrong                                                                                              |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| "We'll offset everything and call it carbon neutral."      | Blacklisted in EU consumer communication, upheld against elsewhere (FIFA 2022), and reduces nothing.         |
| "Travel isn't our emissions, so we report venue and food." | It is most of the footprint. A page that omits it misleads by omission.                                      |
| "Let's start with the easy wins: no swag, no plastic."     | Fine as additions, wrong as the plan. Lead with what moves tonnes.                                           |
| "A typical flight is about X kg, I'll just use that."      | An uncited factor makes every figure on the page unverifiable. Name the set and edition.                     |
| "Moving to a central city is the big win."                 | Only when the current city is off-centre or the audience travels by rail. With a dispersed intercontinental audience and a well-placed city, the best alternative saves about a tenth; remote options and cadence move far more. |
| "Going hybrid fixes the footprint."                        | Remote engagement and cost evidence is poor; the format call belongs to `event-format-selection`.            |
| "We follow ISO 20121."                                     | It is a management-system standard, not a carbon method. Without a certification body, say "self-declared".  |

## Measuring success

- Origin and mode data for at least 80% of participants (self-set threshold: below it, the travel line stays an estimate band).
- Travel emissions per attendee, as a range, compared edition to edition on the same factor set and boundary. Per attendee-day only as a secondary figure: adding a day lowers it without avoiding a tonne.
- Share of trips by flight, and share of flights that are long-haul.
- Food waste in kg per meal served; kg donated.
- Every public claim traceable to a line in the report.

## Output shape

1. Closed-and-open list.
2. Screening estimate table with ranges, data-quality labels and the concentration line.
3. Boundary table: 9 categories, in or out, owner.
4. Two or three lever plans, the chosen one with this edition's actions and next edition's commitments.
5. Data-capture schedule tied to registration and contract dates.
6. Sibling hand-off list.
7. Draft public page.
8. Post-event report skeleton.
