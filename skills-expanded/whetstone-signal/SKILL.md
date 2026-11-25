---
name: whetstone-signal
description: >-
  Use this when ad campaigns that let the platform pick the audience (Meta
  Advantage+, Google Performance Max, Google Demand Gen, or similar) bring
  plenty of cheap leads, signups, or clicks that rarely turn into revenue.
  Helps you choose the conversion event the algorithm should chase, score
  and send back higher quality conversions, and check the results against
  your own backend numbers. Also use it when setting up a new automated
  campaign and deciding what to optimize for.
---

# Whetstone Signal

Automated ad campaigns pick the audience for you. They look for people
similar to the ones who already converted. The setting still in your hands
is what counts as a conversion. If that is "filled in a form," the system
gets very good at finding form fillers, including the ones who never pick
up the phone.

This skill sharpens that target. You pick an event closer to revenue, make
sure it happens often enough for the platform to learn, and send it back
with a value attached. Then you check your own sales numbers to confirm the
change helped.

## When to use

- Cost per lead looks good but sales says most leads are junk.
- A new Advantage+, Performance Max, or Demand Gen campaign needs an
  optimization goal.
- The platform reports more conversions than your CRM or database can find.
- You want value-based bidding but have no honest values to send.
- Retargeting or prospecting keeps reaching existing customers or staff.

Skip it when the account has fewer than about 10 conversions a week of any
kind. Fix traffic or offer first.

## Inputs to ask for

Ask for these before you recommend anything. If the user cannot answer one,
note the gap and continue with the safest default.

1. Platforms and campaign types in use, and current bid strategy.
2. Funnel stages with weekly counts for the last 4 to 8 weeks
   (for example: visit, lead, booked call, showed up, paid).
3. Where truth lives: CRM, billing system, database, spreadsheet.
4. How long it takes a typical lead to reach a paid or high value outcome.
5. Average deal or customer value, and how much it varies.
6. Tracking already in place: pixel or tag, server-side events (Meta
   Conversions API), Google enhanced conversions, offline conversion
   imports.
7. Consent setup: cookie banner, privacy policy, and whether form users
   agree to their data being used for ad measurement.
8. Who the product is for, and whether any of it is aimed at children.

## Procedure

### 1. Map the funnel and count it

Write each stage with its weekly count and the median days from click to
that stage. Ask the user to confirm the counts from their own system, not
from the ad platform.

### 2. Run the volume check

The platform needs roughly 50 optimization events per week per campaign
(or per ad set on Meta) to leave learning and stay stable. Find the deepest
stage that clears that bar, and that happens within about 7 days of the
click for Meta or about 30 to 90 days for Google offline imports (check the
platform's current window).

- Deepest stage clears 50 a week: optimize for it.
- It clears 20 to 50: use it if the campaign budget can be consolidated,
  or combine it with a scored version of a shallower stage (step 4).
- Under 20: optimize for a shallower stage, but send a value with it so the
  system can still tell good from weak.

### 3. Define a qualified event

Write one sentence that a salesperson and an engineer would both read the
same way. It needs:

- a name (for example `qualified_lead`)
- the exact rule that fires it, based on things the person did or told you
- where it is recorded and who owns it
- how long after the click it usually fires

Use behavior and stated answers. Never use guessed traits about the person
(see Guardrails).

### 4. Add an optional self-qualify question

If the form is the main event, add one short question whose answer splits
buyers from browsers. Examples: team size, timeline, budget band, service
area postcode, "Which of these describes you?" Keep it to one question.
Each extra field costs volume, so recheck step 2 after adding it.

### 5. Build a first-party engagement score

Score only actions you observed on your own properties with consent:

| Signal | Example points |
| --- | --- |
| Answered the qualifying question with a fit answer | +30 |
| Opened or clicked the follow-up email | +10 |
| Visited pricing or booking page twice or more | +15 |
| Booked a call or appointment | +40 |
| Used a disposable email or obvious fake details | -50 |

Start with 4 to 6 signals. Set the points so a score of 50 or more means
"the team would happily take this call." Tune after two weeks of data.

### 6. Send the qualified result back

Pick the route that fits the stack:

- **Meta**: send the qualified event or a value through the Conversions API
  from your server, deduplicated with the browser pixel by event ID. Use
  hashed contact fields only where the person gave consent.
- **Google**: upload offline conversions or use enhanced conversions for
  leads, keyed by click ID or hashed email. Value rules can raise or lower
  value by location, device, or audience list.
- **Values**: if you bid on value, send a number that tracks real worth.
  Expected value works: score band multiplied by average deal value and by
  that band's historical close rate.

Then switch the campaign goal to the new event or to value once it has
about a week of clean data. Change one campaign first.

### 7. Move the threshold each week

Once a week, compare score bands with real outcomes:

- If people scoring 50 to 60 almost never buy, raise the cutoff.
- If the qualified event drops under the volume bar, lower the cutoff or
  widen the date window.
- Log each change with the date so you can match it to performance shifts.

Avoid changing the cutoff more than once a week. Each change resets some
learning.

### 8. Add first-party exclusions

Upload consented lists of existing customers, current trial users, staff,
and known spam submitters as exclusions where the campaign type allows it.
Base exclusions on what people did with you, never on sensitive traits.

### 9. Hold out and compare

- Keep a holdout: a geo, a time block, or a platform conversion lift test
  where the new setup is off.
- Each week, compare platform-reported conversions with the same events in
  your backend. Track the ratio. A ratio that keeps climbing means the
  platform is claiming credit you cannot find.
- Judge success on backend numbers: qualified pipeline, revenue, cost per
  paying customer. Platform CPA alone does not count.

## Choosing the event

| Situation | Optimize for | Send back |
| --- | --- | --- |
| 50+ paid customers a week from ads, short cycle | Purchase or paid signup | Real revenue |
| Under 50 sales a week, 50+ booked calls | Booked call or qualified lead | Expected value by score band |
| Plenty of leads, few calls, long sales cycle | Lead with fit answer (step 4) | Score band value via CAPI or offline import |
| Leads under 50 a week | Lead, all of them | Value from score so the system still learns quality |
| Free product, revenue later (content, freemium) | An early action that predicts retention | Fixed value per action, adjusted by cohort data |
| Platform count far above backend count | Do not change the goal yet | Fix tracking and deduplication first |

## Worked examples

### B2B SaaS demo funnel

A project tool gets 400 demo requests a month from Performance Max. Sales
says a third are students or solo users. Counts per week: 95 demo requests,
30 demos held, 6 closed deals. Deals close in about 45 days.

- Closed deals (6 a week) are too few. Demos held (30) are short of 50.
- Add one form question: "How many people will use it?" Answers of 5 or
  more mark a fit lead. About 55 a week qualify.
- Score: fit answer +30, work email domain +15, booked a slot +40.
- Send `qualified_demo` through Google offline conversion import keyed by
  click ID, value = 0.2 close rate x 6,000 average deal = 1,200.
- Hold out two regions for four weeks. Compare demos held and pipeline per
  euro spent in test versus holdout.

### YouTube channel subscriber funnel

A cooking channel runs Demand Gen to grow subscribers. Subscribers are cheap
but many never watch a second video.

- The platform cannot see "watched three videos" directly, so define the
  qualified event on the channel's own site instead: joined the email list
  from the video description and opened the second email.
- About 70 a week qualify. That clears the bar.
- Send the event with a fixed value through enhanced conversions, using the
  email the person typed in with consent.
- Weekly guardrail: compare new subscribers who watched 2+ videos in
  YouTube Studio for test weeks against the prior four weeks.
- Content is aimed at adults. If a channel is made for kids, do not use
  this method for that audience at all.

### Local services lead form

A plumber runs Meta Advantage+ lead ads. Many leads live outside the service
area or want a quote for a job the business does not do.

- Add one question: postcode. Add a second only if volume allows: job type.
- Qualified lead = postcode inside the service area and a job type on the
  list. About 40 a week, under 50.
- Optimize for all leads, but send each lead's value through the Conversions
  API: 0 for out of area, 50 for in area, 150 for in area with a booked
  visit. Use value optimization once there is a week of data.
- Exclude existing customers using the consented customer list.
- Guardrail: booked jobs in the job system per week, compared with Meta's
  lead count.

## Guardrails: never do this

- Never buy data from data brokers or enrich leads with bought traits such
  as net worth, income, credit scores, marital status, or ethnicity.
- Never scrape, de-anonymize, or try to identify people who saw, liked,
  commented on, or clicked an ad beyond what the platform shares with you.
- Never score, target, or exclude people using sensitive or protected
  traits: race, ethnicity, religion, health, sexual orientation, gender
  identity, disability, age where restricted, political views, financial
  hardship, or close proxies for any of these.
- Never use personal data for ad measurement or targeting on content made
  for children.
- Use only first-party data that people gave you with consent, for a purpose
  they were told about. Honor deletion and opt-out requests in every list
  you upload.
- Follow each platform's terms, including special ad categories for
  housing, jobs, credit, and social issues, where many targeting and
  exclusion options are off by design.
- Never send a fake or inflated value to push the bidder. It teaches the
  system to find the wrong people and breaks your own reporting.

## Checklist

- [ ] Funnel counts come from the backend, for the last 4 to 8 weeks
- [ ] Chosen event clears about 50 a week, or a value is attached
- [ ] Qualified event is written as one unambiguous rule
- [ ] Score uses only consented first-party behavior and answers
- [ ] Events are deduplicated between browser and server
- [ ] One campaign changed first, with a holdout in place
- [ ] Weekly log of threshold, platform count, backend count, and ratio
- [ ] Exclusion lists are consented and current
- [ ] No sensitive traits, broker data, or kids content anywhere in the setup

## Template

Copy [qualified-event-spec.md](qualified-event-spec.md) to record the event
definition, scoring, send-back route, and weekly review in one place.
