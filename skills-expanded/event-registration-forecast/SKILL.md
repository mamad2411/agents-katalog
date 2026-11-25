---
name: event-registration-forecast
description: "Forecast final registrations for a technical event from its sign-up pace curve, with a bundled Python 3 script, while registration is still open - prior-edition or generic reference curves aligned on days-out, a low/mid/high band, milestone tripwires declared in advance, the commit figure at each contract lock date, when the forecast crosses capacity, and attendance by ticket type. Use whenever asked how many people will end up registering or attending, to project this year from last year's curve, what headcount to commit before sign-ups close, or when registration will hit its cap. Do NOT use for the demand verdict - use samber/dev-event-organizer-skills@event-market-fit - or overbooking ratios and food counts once sign-ups close - use samber/dev-event-organizer-skills@event-no-show-management."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Registration Forecast

You forecast how many people will register for a technical event, and how many will attend, from the registrations already in. The forecast exists for the dates where money locks: a catering guarantee, a hotel-block cutoff, a venue cancellation-fee step. Doors day is too late to be useful.

**You produce:**

- A projected final registration count as a low / mid / high band, net of comps.
- Expected registrations on hand at each milestone, declared before the milestone arrives.
- A commit figure for each lock date, chosen from the band, never the midpoint by default.
- Expected attendance by ticket type.

The order: clean the readings, pick references, run the script, then read the band at each milestone, lock date and capacity (§ Workflow).

**You do not decide:**

- Whether the event has demand. `samber/dev-event-organizer-skills@event-market-fit` reads the same pace as a demand signal and issues go, hold, pivot or stop. Hand it your band; never issue that verdict here.
- The per-phase targets or the push itself. `samber/dev-event-organizer-skills@event-marketing-plan` owns both; you fire a tripwire and hand it a brief.
- Prices or price dates. `samber/dev-event-organizer-skills@event-ticket-pricing` owns them; you only say when a ticket-count gate will trip.
- Show-up ratios, the overbooking ceiling, the waitlist and the walk-in lane. `samber/dev-event-organizer-skills@event-no-show-management` owns those; you apply its ratios per ticket type. Once registration has closed, the count is known and the food number is its job alone.
- The go/no-go poll. `samber/dev-event-organizer-skills@event-risk-management` runs it; you deliver the registration criterion to it.

The method is booking-curve pickup forecasting from hotel and airline revenue management: a fixed-date, perishable inventory forecast from bookings on hand plus expected pickup. No event-specific forecasting method is established, so name that origin when presenting the forecast. Every ranking below is a default, not a law. Re-rank against what you know about this organizer: a prior edition's export on disk, a free event, a hackathon closing registration a week out, a peer organizer willing to share a curve.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 8-10 exist because the menus below diverge on time-to-effect and effort; their defaults cannot be picked for the user. When the user cannot answer, proceed on stated assumptions and list every one in the deliverable's first section.

1. Format and price posture: paid conference, nominal fee, free meetup, or free hackathon? Every reference curve and show-up figure splits on this.
2. What readings exist: cumulative registrations by date, exportable? Net of comps, or with speaker, sponsor and volunteer codes mixed in? How are refunds and cancellations counted?
3. Do you hold a prior edition's curve for this same event, same format, same posture? What moved between editions: the date, the early-bird close, the speaker announcement, the venue size?
4. What number matters: the planned final net of comps, the break-even registrations, the room's capacity?
5. Which commitments lock against a headcount, on what date, and can each one scale up or down afterwards (catering guarantee, hotel block, swag and badge print run, a second-room option, the venue's cancellation-fee steps)?
6. Which milestones are already fixed: early-bird close, speaker and agenda announcements, ticket-count price gates, registration close?
7. What is the ticket-type mix: paid tiers, students, scholarships, group orders, and comps for speakers, sponsors and volunteers?
8. When is the next lock date? A near one promotes the cheapest usable reference over a better one you would have to chase.
9. One edition, or a recurring event? A recurring one makes recording every milestone forecast worth the minutes, because next edition's band comes from this edition's errors.
10. Who reads the numbers each week, and how long can they spend?

## Readings

Clean the input before projecting anything; a wrong reading cannot be fixed by a better curve.

- Count cumulative registrations net of comps. Comps were never sold and enter the attendance forecast separately (§ Attendance by ticket type).
- Pick gross or net of refunds and hold it through every edition you compare. Mixing them bends the curve.
- Compute a prior edition's own show rate on the same basis: attended minus comps who attended, over registrations net of comps. Mixing comps into one side only inflates or deflates the rate.
- Annotate every reading with what happened that week: announcement, early-bird close, price gate, a push, a batch release. A spike is an event, not a new run rate.
- Flag batch releases. Releasing tickets in small batches manufactures an early sellout and flattens the real curve.
- Stop reading registrations as demand once a cap binds. From then on, count the waitlist; registrations only show the cap.

## Reference curve

Which curve supplies the expectation. Ranking (default; re-rank against Q3, Q8):

- effort (hours to obtain and align it): `comparable-event curve > own prior edition > generic sourced curve`
- value (how closely its shape matches this edition): `own prior edition > comparable-event curve > generic sourced curve`
- efficiency: `own prior edition > generic sourced curve > comparable-event curve`

- **Own prior edition** - the default whenever one exists: a past edition's daily or weekly export, aligned on days-out. Its shape already carries this audience, this price posture and this marketing rhythm.
- **Generic sourced curve** - the default for a first edition: a platform-wide lead-time distribution, a free-hackathon target timeline, or a published checkpoint ladder, each with its own population and its own label (observed or target). Shipped as CSV in `assets/`; scope and sources in [references/reference-curves.md](references/reference-curves.md). Never blend two generic curves into one; run each as its own reference.
- **Comparable-event curve** - the starved option: another organizer's export for a similar event, same format and posture. It beats a generic curve on shape and loses every efficiency round because it must be asked for. Promotion condition: a first edition (Q3) facing a large lock date (Q5) with a peer organizer reachable within the time Q8 leaves.

Run at least two references whenever two exist: the spread between them is your band. **Deleted, not demoted: the straight line** from today's count to doors. Every sourced curve is back-loaded; a free event's median registrant signs up about two weeks out. A straight line reads a healthy early curve as a shortfall and a front-loaded one as a sellout.

Align editions on days-out, never on calendar date. Two moves handle the common distortions; both are script options:

- **A milestone moved** (speaker announcement at 35 days this year, 42 last year): run the reference twice, as is and shifted (`last-edition.csv@-7`), and let the two form part of the band.
- **The latest reading follows a spike**: project with `--as-of` set to the last reading before the spike, and report it beside the latest. A spike projected forward overshoots; the lull after it then reads as collapse.

On a free event, the pooled generic curve forms the low end: free registrants sign up later than its pooled population, so it expects too much on hand early. Alignment rules and the booking-window drift caution are in [references/reference-curves.md](references/reference-curves.md).

## Projection

Run the script; do not do this arithmetic by hand. It needs Python 3 and nothing else, reads CSV, and writes nothing.

```
python3 scripts/forecast-registrations.py --actuals actuals.csv \
  --reference last-edition.csv --reference assets/curve-pooled-lead-time.csv \
  --target 550 --threshold 350 --capacity 500 --ceiling 900 \
  --checkpoint catering:7 --checkpoint hotel-block:30 --error-band 0.15 --types ticket-types.csv
```

The method choice is a rule, not a ranked menu: which projection is right depends only on how much of the curve is in, so a ranking would be false precision.

- **Multiplicative pickup** - registrations now divided by the share the reference had on hand at this days-out; the same arithmetic as the pace index. Used once at least 15% of the reference curve is in (self-set: below it, one stray registration swings the projection by six or more).
- **Additive pickup** - registrations now plus the reference edition's remaining pickup from this days-out. Used earlier, and needs a count reference. When the event runs under half or over double the reference at the same days-out (self-set range), the additive figure is only a bound: the script prints it on a bounds line and keeps it out of the band. So does an unstable multiplicative figure. With nothing left in the band, the script stops: say the forecast cannot be made yet.

**The band.** Two or more references: the low and high ends are the lowest and highest single-reference projections, never an average. Past forecast errors: widen by the error your own recorded forecasts showed at this days-out (`--error-band`). One usable reference and no history: the script prints no band; report a point guess, label it so, and add a second reference before any lock date. The mid is the median across references, so one edition run both as is and shifted counts twice; say so when it sets the mid.

Read the pace at week two, not on launch day: launch measures reach, not demand.

## Milestones and tripwires

Declare, before each milestone, the registrations you expect on hand: pass each milestone and lock date as a `--checkpoint` and read its range. A tripwire fires when a reading lands outside it, and only then. A threshold set after the reading can be argued into anything.

Response when the low end is running short. Ranking (default; re-rank against Q8, Q10):

- effort: `go/no-go escalation > budget-tier downgrade > push brief`
- value (money protected before the next lock): `go/no-go escalation > budget-tier downgrade > push brief`
- efficiency: `push brief > budget-tier downgrade > go/no-go escalation`

- **Push brief** - the default: hand `samber/dev-event-organizer-skills@event-marketing-plan` the gap in registrations, the milestone it must close by, and the segment furthest behind. Cheap and reversible, and it recovers registrations only when the gap is execution, not demand. Mark the push on the curve so next edition does not read it as organic.
- **Budget-tier downgrade** - commit the scalable lines at the tier the low end supports and hand that to `samber/dev-event-organizer-skills@event-budget`. It protects money for certain, at the price of a smaller event.
- **Go/no-go escalation** - the starved option: highest stakes, highest effort. Promotion condition: the mid projection misses the threshold (Q4) at the go/no-go review that precedes the next cancellation-fee step. Deliver the band and the threshold, fixed before the meeting, to `samber/dev-event-organizer-skills@event-risk-management`, and route the demand question to `samber/dev-event-organizer-skills@event-market-fit`.

**Deleted, not demoted: moving a published price date or adding an unannounced discount** to rescue a forecast. It trains buyers to wait for the next rescue, and the price calendar belongs to `samber/dev-event-organizer-skills@event-ticket-pricing`. What you may do is tell that skill when a published ticket-count gate will trip, so the tier flips on the date its own rule sets.

When a reading lands above the high end, run § Capacity instead.

## Lock dates

For every commitment from Q5, commit at the band end that its cheaper mistake points to, never at the midpoint by default. This is the newsvendor rule from inventory theory: when running short costs more than over-committing (food for people already in the room), commit toward the high end; when over-committing costs more (hotel room-nights with an attrition penalty), commit toward the low end, and grow the block later only where the hotel confirms in writing that rooms can be added at the group rate.

- Pick the band end the cost asymmetry points to, and write the reason next to the number.
- If the line can still grow after the lock (a caterer's +10% up to two days out, a hotel adding rooms), commit that end divided by one plus the flex, and keep the flex for a late surge.
- Before a lock date arrives, give a provisional figure and re-run the forecast on the lock date itself. The commitment is the figure made on that date.
- Hand headcount to catering in attendance terms (§ Attendance by ticket type), never as registrations.

The lock-date catalogue with typical timing, the newsvendor rule worked through, and the tier mapping are in [references/lock-dates-and-commit-rules.md](references/lock-dates-and-commit-rules.md). Read it before the first lock date.

## Capacity

Compare attendance, not registrations, against the room's limit.

1. Convert the band into attendance, comps included (§ Attendance by ticket type); the script compares that total with `--capacity`.
2. If high-end attendance crosses capacity before a bigger-room or second-room option expires, flag it to `samber/dev-event-organizer-skills@event-venue-sourcing` with the option's deadline.
3. "When do we close registration" is a ceiling question. A paid event closes at capacity minus the comps expected to attend (speakers, sponsor staff, volunteers take seats too); a free one closes at the registration ceiling `samber/dev-event-organizer-skills@event-no-show-management` sets from its show-up ratio. Pass that ceiling as `--ceiling`: the script gives the days-out at which each reference reaches it, which is the date the waitlist opens.
4. Once the cap binds, stop forecasting registrations. Forecast the waitlist instead, because registrations now measure the cap.

## Attendance by ticket type

Expected attendance is the sum over ticket types of registrations times that type's show rate. Run it through the script's `--types` file (`basis` is `share` for sold types, `count` for comps); never apply one blended rate to the whole list.

- Take paid and free show rates from `samber/dev-event-organizer-skills@event-no-show-management`, with their scope.
- Label every other type's rate sourced, own-data or self-set. Speakers, sponsor staff and volunteers carry no published rate; measure them once, then use your own.
- Never discount late registrants. Within the same event they turn up at practically the same rate as early ones; the apparent gap in pooled data comes from which events sell late.
- Forecast walk-ins and on-site registrations only from your own prior count. Without one, say the number is unknown; generic curves end at doors and leave them out.
- On a multi-day event, forecast each day separately for per-day catering: day two can draw fewer people than day one. Use your own per-day check-ins; without them, say day-two attendance is unknown rather than reusing day one.

Figures, scopes and the gaps are in [references/attendance-by-ticket-type.md](references/attendance-by-ticket-type.md).

## Workflow

1. Run the interview.
2. Clean the readings (§ Readings) and annotate each one.
3. Pick at least two references from the reference-curve menu and align them on days-out.
4. Run the script. Report which projection each reference used and why.
5. State the band and how it was built.
6. For each lock date from Q5, give the commit figure and the band end it came from, with the reason.
7. Declare the expected on-hand range for each upcoming milestone. Name the response each tripwire fires and its owner.
8. Run § Capacity against the high end.
9. Produce attendance by ticket type.
10. Deliver the forecast sheet section by section (output shape below), validating each with the user.
11. Re-run at every new reading, keeping earlier forecasts unedited, so each milestone keeps the forecast made before it.
12. After doors, compute the signed error at each milestone: forecast at that milestone against the final. That error is next edition's `--error-band`.

If your harness has persistent memory, record the reference set, each milestone forecast with its date, each commit figure with its band end, and the final count.

A worked forecast, with the script output read line by line and a straight-line negative example, is in [references/worked-forecast.md](references/worked-forecast.md).

## Failure modes

- **Extrapolating a spike.** An announcement week or an early-bird close projected forward overshoots, and the lull after it then reads as collapse. Project `--as-of` the last pre-spike reading as well, or shift the reference so its spike sits on this year's milestone.
- **Calendar-date comparison.** Comparing this October 1 with last October 1 when the event moved by a week shifts the whole curve. Align on days-out.
- **Comps inside the count.** A sponsor code batch of fifty looks like a sales week. Count comps once, in the type file.
- **Multiplicative pickup on a thin curve.** Twelve registrations against an expected six projects double the final. Below 15% in, use additive or say the read is unstable.
- **One number.** A point forecast hides the decision every lock date needs, which end of the band to commit at.
- **Blending posture curves.** A free event read against a paid curve looks behind for weeks and then surges; a free hackathon curve hits its total a week out on purpose.
- **Rescuing the forecast with a price move.** See the deletion under § Milestones and tripwires.
- **Issuing the demand verdict.** A short band is a capacity and money input. Whether the concept is wrong is `samber/dev-event-organizer-skills@event-market-fit`'s call.
- **Forecasting registrations past a sellout.** After the cap binds, the curve shows the cap, not demand. Forecast the waitlist.
- **Not recording the forecast.** Without each milestone's forecast kept as made, next edition has no error band and starts from a borrowed curve again.

## Measurement

- **Every lock-date commitment names its band end and reason** (gate, pass or fail): a commit figure with no stated end is a guess.
- **Forecasts are recorded at each milestone, unedited** (gate, pass or fail): the cheapest thing on this page, and the only route to an own error band.
- **Signed error at each milestone** (self-set): forecast at that milestone against the final. A consistent sign is bias, so fix the reference choice; a scattered sign is noise, so widen the band.
- **Band coverage** (self-set): how often the final landed inside the band declared at each milestone. A band that never misses is too wide to commit against.
- **Attendance by type against the count** (self-set): per type, so next edition's show rates are your own.

## Invocation examples

- "We've sold 165 tickets 45 days out; last year we finished at 500. What will we end up with, and what do I tell the caterer?"
- "First edition, free meetup-turned-conference, 90 signups 6 weeks out. How many will register, and when do we open a waitlist?"
- "Hotel block cutoff is in 10 days. How many room-nights should we keep?"

Expected output, delivered section by section:

1. Readings, cleaned and annotated.
2. References used, and the projection method each one took.
3. The band: low / mid / high, net of comps, and how it was built.
4. Lock-date table: commitment, date, commit figure, band end, reason.
5. Milestone table: date, expected on-hand range, tripwire response, owner.
6. Capacity read.
7. Attendance by ticket type, with each rate labelled.

## References

- samber/dev-event-organizer-skills@event-planning-timeline - puts each lock date and milestone on the work-back schedule.
