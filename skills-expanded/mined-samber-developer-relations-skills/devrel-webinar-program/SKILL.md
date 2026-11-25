---
name: devrel-webinar-program
description: >-
  Designs a recurring technical webinar series for a developer audience and ships its
  charter, season plan and lead-handoff contract with sales. Use whenever someone runs or
  plans a monthly or bi-weekly webinar series for developers, or, for that series, sees low
  live attendance or replays nobody watches, asks whether to gate recordings, picks topics or
  speakers, co-hosts with a partner who wants the registrant list, or hears from sales that
  every attendee should be an MQL - even if they only say "our developer webinars aren't
  working". Do NOT use for platform, streaming or moderation mechanics - use
  samber/dev-event-organizer-skills@virtual-event-production - or a Q&A-only series - use
  samber/developer-relations-skills@developer-office-hours-program.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.2"
---

# DevRel Webinar Program

You are an experienced developer-relations program lead. The user runs, or wants to run, a recurring technical webinar series for developers, and needs it to still earn its slot a year from now.

Treat the series as a program, not an event. The live hour is one delivery channel; the replay, the clips and what attendees do afterwards outlast it. Design for episode twelve on a tired month, not for the launch episode.

Two teams usually claim the same series for different jobs: DevRel wants developers to learn and activate, sales wants leads. A series that never settles which job comes first gets judged on registrations, the one number neither team needs.

Scope is the recurring series for developers. Siblings cover adjacent jobs:

- Platform choice, streaming, remote-speaker connectivity, chat and Q&A moderation: samber/dev-event-organizer-skills@virtual-event-production
- Reminder emails and no-show handling for a single event: samber/dev-event-organizer-skills@event-attendee-email-sequences
- Making the demo inside an episode survive: samber/developer-relations-skills@developer-live-demo-design
- Scripting a recorded video or the clips cut from a replay: samber/developer-relations-skills@technical-video-script
- Which replays and cut-downs the company YouTube channel carries: samber/developer-relations-skills@devrel-youtube-channel
- Fitting episodes into the quarter's content plan: samber/developer-relations-skills@devrel-content-calendar
- A private hands-on workshop for one customer or prospect account: samber/developer-relations-skills@developer-workshop-program
- An open, chat-led live show with no registration on Twitch, YouTube Live, LinkedIn Live or X: samber/developer-relations-skills@devrel-live-streaming

Typical invocations:

- "observability startup, monthly webinars, 300 registrants, 22% show up live, sales wants every attendee as an MQL"
- "we want to start a bi-weekly technical webinar series for our API, where do we begin"
- "should we gate our webinar replays"
- "a partner wants to co-host and get the registrant list"

## Deliverable

Produce, in this order:

1. **Diagnosis** - only when the user brought numbers: denominators, population comparison, the pattern read in Step 6, the first fix.
2. **Charter** - one page: job, audience, format mix, cadence, slot, speaker pool, replay policy, budget, data retention, season dates, continue bar.
3. **Season plan** - episodes with format, topic, speaker, backup, slot and replay type.
4. **Topic backlog** - scored, a season ahead.
5. **Handoff contract** - tiers, timing, lawful basis, named sales owner. Route marketing email only to registrants who ticked an unticked opt-in box (Step 8).
6. **Episode log** - columns from the measurement table, past episodes entered as the pilot baseline, future rows empty.

Mark everything past the first season as provisional. Templates for every item and a filled charter: [./references/charter-and-season-templates.md](./references/charter-and-season-templates.md).

## How to read the numbers

Every figure in this skill is one of three kinds:

- **Sourced** - from a named vendor report or developer survey, cited inline, with its sample where the report discloses one.
- **Baseline** - set by this skill, marked "baseline". Replace it with the series' own figure after the first season.
- **Refused** - widely repeated, traceable to no study. Never quote it, even when the user does.

Every attendance benchmark comes from a webinar platform measuring its own customers, and none isolates developer audiences. Published live attendance runs from 22% (Demio, small hosts) to 60% (ON24), and Goldcast 2025's own averages divide to 21%; the spread follows who registered (owned list or cold, large brand or small host). Compare a series with its own baseline first and a population-matched figure second.

Refuse these on sight: "38% of attendees become MQLs", "median 41.6% live attend rate across 12,400 webinars", "average attendance 35-45%", "20-40% of attendees become qualified leads", "3+ reminders lift attendance 20%". Treat any attendee-to-MQL rate as unverified unless it states its sample and its MQL definition.

Every figure, its source and the refused list with origins: [./references/evidence-and-benchmarks.md](./references/evidence-and-benchmarks.md).

## Interview

Ask one question at a time, multiple-choice where possible, and skip what the user already answered. Questions 1-5 gate the design: propose no format before they are answered. Question 7 gates the registration form.

When no user can answer (a one-shot request, an unattended run), infer each missing answer from the request, mark it "assumed", and list every assumption at the top of the deliverable as an open decision. Assume activation as the job when the request names a free tier or trial, deal acceleration when it names open deals, and feature depth otherwise.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. What is the series' one job: activate new developers, deepen use of existing features, accelerate deals already open, or grow community voices? Name the first; the others become secondary.
2. Who registers today, and from where: your own users, your newsletter, a partner's list, paid ads, a community? Rough split if known.
3. What exists already: past episodes with registrants, live attendees, on-demand views (platform and any public video copy), the slot used.
4. Who can speak and prepare, and how many hours per month each, on a bad month? Is there a free tier or sandbox an attendee could build on during a session?
5. What does sales want from the series, in their words, and who on the sales side will agree a written handoff rule?
6. Where are the developers, by region? Is there a date or launch the series must hit? What budget exists for platform, promotion and lab infrastructure?
7. Will partners co-host or sponsor? Which countries do registrants come from (EU member states, UK, Canada, US)?

Carry 1, 4 and 5 into the format ranking, and say which answer moved which option:

- Job is activation and a free tier or sandbox exists (Q1, Q4): put one or two follow-along labs in each season (baseline).
- Job is deal acceleration (Q1): promote the customer story and the live demo; sales co-owns the topic backlog.
- No one can moderate with prep time (Q4): delete the panel.
- Sales refuses any written handoff rule (Q5): ship the series without a sales route, route attendee data to product nurture only, and log the open decision.

## Step 1 - Write the charter and the first season

Write the charter before booking a slot. Present it in sections and get each validated. With no user available, deliver it whole with the open decisions at the top.

- Run the series in seasons of 4-6 episodes. Goldcast's 2026 benchmark puts the median B2B series at 4 episodes and advises committing to at least four; the upper bound is a baseline. A season gives a fixed review point and an honest exit.
- Write the continue bar into the charter before episode one, so the season review judges against a bar set in advance. Default bar (see Pass threshold): fail when total reach, live attendance or returning share drops below baseline (season one, on two later episodes; then three in a row), or the job metric stays flat; stop after two seasons failing the job metric.
- Price the season: platform, paid promotion, lab infrastructure, captioning, any speaker honorarium. Step 3 counts hours; this line counts money.
- Set a retention period for registrant and engagement data, and write it into the handoff contract.
- If your environment has persistent memory, store the charter, the topic backlog and the episode log, and start each later run from them.

## Step 2 - Choose the format mix

Effort is standing staff hours per episode: preparation, rehearsal, any lab environment, follow-up. Value is progress on the series' one job, plus how long the replay stays useful.

Rough effort per episode, order of magnitude (baseline): Q&A episode, a few hours; live demo, half a day when the demo exists; engineer conversation, about a day; panel, one to two days; customer story, one to two days plus weeks of approval wait; follow-along lab, about two days the first time, a day when re-run.

Rank by the series' job. For community voices, use the activation order with community speakers taking the engineer-conversation slots.

- efficiency (activation): `engineer conversation > live demo > Q&A episode > follow-along lab > customer story > panel`
- efficiency (deal acceleration): `live demo > customer story > engineer conversation > Q&A episode > panel > follow-along lab`
- efficiency (feature depth): `live demo > Q&A episode > engineer conversation > follow-along lab > customer story > panel`
- value (activation): `follow-along lab > engineer conversation > live demo > customer story > Q&A episode > panel`
- value (deal acceleration): `customer story > live demo > engineer conversation > follow-along lab > panel > Q&A episode`
- effort: `follow-along lab > customer story > panel > engineer conversation > live demo > Q&A episode`
- compliance cost: `customer story > panel > follow-along lab > engineer conversation == live demo == Q&A episode`

- **Engineer conversation** - an advocate interviews the engineer who built something (Datadog on...). Evergreen, clips well.
- **Live demo** - one developer problem solved live with the product, never a feature tour.
- **Q&A episode** - pre-collected questions answered by an engineer (AWS re:Post Live). Ranks below the demo despite lower effort because its value depends on a standing question backlog.
- **Follow-along lab** - attendees build on a free tier while the host builds (Snowflake hands-on labs, Postman Intergalactic). Needs a tested environment and a second staff member in chat.
- **Customer story** - a customer engineer explains a migration or architecture. One per season at most (baseline).
- **Panel** - three voices on one question; meanders without a prepared moderator.

- Justify the compliance tie: engineer conversation, live demo and Q&A episode put only your staff and your public product on screen, so none triggers an outside approval.
- Read the compliance line as the review each triggers: customer approval for the story, outside-speaker releases for the panel, a privacy notice on the lab's trial sign-up.
- Default: alternate engineer conversations and live demos. Add the lab on the interview condition above, with one presenter and one person answering setup problems in chat.
- What this order starves: the follow-along lab, highest value for activation and highest effort, loses every efficiency round. One lab per season often carries the season's activation.
- Hand the series to samber/developer-relations-skills@developer-office-hours-program when every planned episode is a Q&A episode.
- Re-rank against what you know: an engineer who already streams makes the lab cheap; a customer who already presented at a conference makes the story cheap.

Episode skeletons and the exemplar table: [./references/formats-and-exemplars.md](./references/formats-and-exemplars.md).

## Step 3 - Size cadence from capacity, then fix the slot

Size cadence from preparation capacity, never from the marketing calendar.

1. Price one episode in staff hours per format from Step 2, including follow-up.
2. Multiply by episodes per month and check it against the hours named in Q4. If it does not fit, drop cadence before dropping preparation.
3. Default to monthly; go bi-weekly only when the backlog holds a full season and every slot has a backup speaker (baseline).
4. Book 30-45 minutes, and 45-60 for a lab (baseline). Technology webinars average 77 minutes on Goldcast while measured viewing runs about 29-49 minutes across reports.
5. Place the slot inside the working day of the largest developer region. With North America and Europe both large, 11:00 ET lands late afternoon in Central Europe; anchor in the larger region's time zone and announce the shifted local time in the weeks when US and EU clocks change on different dates.
6. Pick the day from your own data: Tuesday leads Goldcast's all-industry data by about a point. Goldcast's best tech-company slot, Friday afternoon ET (50.1%), is one segment's best hour and suits a North-America-only audience. Test a second slot only on two episodes of the same format.
7. Serve the second region with the replay, or repeat a lab in its time zone when it holds a quarter of users or more (baseline).

## Step 4 - Build the topic backlog

Hold a full season of topics before announcing the series. Sources, efficiency first: `repeated community questions > onboarding friction > engineering war stories > releases`. Questions and friction are already written down by developers; war stories need an engineer's time; releases date fast.

- Repeated community and forum questions (AWS re:Post Live answers top-voted questions).
- Onboarding friction: the step where trials stall, the docs search with no result.
- Engineering war stories from incidents and migrations.
- Launches and releases, as timely episodes, under a third of a season (baseline).

Score each candidate on job fit, developers affected, speaker available, and replay life past a quarter. Title by the developer's problem, never the product:

```
✓ Good - Tracing a slow Kafka consumer end to end in 30 minutes
✗ Bad - What's new in Acme Observability 4.2
```

## Step 5 - Source speakers a season ahead

DevRel hosts; engineers, customers and community members speak. A series where advocates are the only voice runs out of depth; one built on a single engineer dies with their next project.

Sources, efficiency first: `internal engineers > community members > partners > customers`. Engineers need only a manager's agreement; community members need coaching; partners trigger co-host rules; customers need weeks of approval.

- Internal engineers: agree the hours with their manager; credit them and their team by name.
- Community members: invite top contributors and forum answerers (AWS re:Post picks guests from top contributors; HashiTalks runs an open call and invites first-time speakers).
- Partners: a partner who touches registration data makes the episode co-hosted (Step 8).
- Customers: start approval 6-8 weeks before the slot (baseline).

Book a named backup per episode. Get a recording release from every speaker, staff included. Brief each with the episode's job, the audience's level, the no-pitch rule and the handoff wording they may say on air.

## Step 6 - Promote, then diagnose registration to attendance

Promotion order (baseline, ranked by registrant intent rather than volume): `own users and newsletter > community channels > speakers' own audiences > organic social > paid`. Livestorm's survey of go-to-market staff reports email driving registrations for 86% of respondents, organic social 43%, community and newsletter 33%, paid 20%; those are reported drivers, not measured lift, and social ranks lower here because its registrants show up less.

- Open registration 3-4 weeks ahead (baseline) and keep it open until the session starts. In Livestorm's data 49.6% of registrations arrive in the final 7 days and 15.3% on the day.
- Put most promotion effort into the final week.
- Reminder copy and timing belong to the email sibling listed at the top; this skill decides the window.

Diagnose attendance against the right denominator before fixing anything:

1. Compute live attendance as live attendees / registrants, and total reach as live attendees + on-demand viewing within 30 days (baseline) on every surface. Use unique viewers where reported; otherwise views, labelled "upper bound".
2. Compare with the series' own earlier episodes first.
3. With no history, compare with the matching population (baselines derived from vendor cuts), keyed on host size and registrant source:
   - Small host, mostly paid or partner registrants: 20-35% (Demio: 22% under $1M revenue, 28% Internet Software & Services; BrightTALK: 34%).
   - Large host, mostly its own list: 45-60% (Demio: 46-48% above $10M revenue; Livestorm 47.7%; ON24 60%).
   - Any other mix: no vendor cut fits; use the first two episodes as the baseline.
4. Split registrants by source and compute attendance per source.
5. Check the gap between registration and session, and whether the slot sits inside registrants' working day.
6. Read the pattern:
   - Low registration and low attendance: a topic developers do not need. Fix the topic before the reminders.
   - Healthy registration, low live attendance, healthy replay reach: the audience prefers on demand. Invest in the replay and give live a reason.
   - Healthy registration, low live attendance, low replay reach: registrants bought by paid or partner promotion. Shift promotion to own users and community.
7. Tag every link in the replay description and follow-up email by episode, so sign-ups from anonymous replay viewers can be counted.

Give live a reason that more emails cannot: the lab environment, the engineer answering live, an optional unrecorded after-show for extra questions.

## Step 7 - Plan the replay

On-demand figures use different denominators: ON24 reports 43-52% of attendees watching on demand; Goldcast reports on-demand as 15.9% of viewing. Neither counts views of a public video copy. Measure replay reach per series instead of assuming it outdraws live.

Goldcast 2026 reports 91% on-demand completion against 74% live: read replay viewers who stay as intent-rich, not as worth more per head.

Gating options, efficiency first:

- efficiency: `ungated chaptered copy > ungated copy plus clips > gate the bundle only > gate everything`
- value (developer reach): `ungated copy plus clips > ungated chaptered copy > gate the bundle only > gate everything`

- **Ungated chaptered copy** - on the public video channel within 48 hours (baseline), chapters from the outline, code and tagged links in the description.
- **Ungated copy plus clips** - two or three clips per episode (baseline); the clip script belongs to the technical-video-script sibling.
- **Gate the bundle only** - recording ungated; gate what is worth a form: lab environment, badge, certificate (Snowflake and MongoDB tie sessions to credentials; Postman pairs recordings with forkable collections).
- **Gate everything** - developers learn from documentation (58.9%) and video (41.1%) per the Stack Overflow 2026 survey, and a form in front of a video cuts that path. Gating a recording already public means pulling it from the channel. Delete this option unless the charter's first job is deal acceleration.

- Caption every live session and publish captions and a transcript with every replay.
- Re-run evergreen labs as scheduled replays, labelled as recorded. Clip timely release episodes within days or not at all.

## Step 8 - Write the handoff contract with sales

Write who gets routed where before episode one, sign it with a named sales owner, and read sales acceptance back every episode. "Every attendee is an MQL" breaks three things: sales works leads that never wanted contact, developers who get a call after a technical session stop registering, and the series is judged on a volume its job never needed.

Route on behaviour, never on attendance alone:

| Tier | Signal | Route | Timing |
| --- | --- | --- | --- |
| A - hand-raise | Asked for a demo, pricing or contact; clicked a pricing or demo call to action | Sales, with the episode and the question asked | Within 1 business day (baseline) |
| B - engaged, open account | Engaged attendee or registered replay viewer at an account with an open opportunity | Account owner notified, no cold call | Next working day (baseline) |
| C - engaged | Engaged attendee who ticked the marketing box | Product activation nurture | Episode follow-up |
| D - registered | Registered, attended briefly or not at all | The replay email they registered for | Episode follow-up |

- Define "engaged" from the first two episodes so it holds roughly the top third of attendees (baseline): share watched, questions asked, resources clicked.
- Anonymous viewers of a public replay never enter a tier; count them through tagged links only.
- Route past registrants only under the notice they saw. Registrants never told sales may follow up get the replay and the new notice.

Lawful basis bounds every row. Legal review owns the wording; the structure is:

- Disclose on the form that attendance, watch time and clicks are recorded and used to decide follow-up, and that the host's sales team may contact them.
- Show every registrant an unticked opt-in box for marketing email, and route marketing email on the box alone; it is the only basis valid in every EU state and needs no country lookup. Looser regimes exist (France and UK B2B notice plus opt-out, US opt-out; Canada needs express or implied consent; Germany requires prior consent, B2B included), but the form rarely knows the country.
- Record a legitimate-interest assessment before sales calls or account notes based on webinar behaviour.
- Treat data as staying with one controller only inside one legal entity; a sales team in another group company is a disclosure.
- With a co-host deciding registration fields or follow-up, treat both as joint controllers (EDPB Guidelines 07/2020): sign an arrangement, name the partner on the form, and give partner marketing its own unticked box.
- Never hand a sponsor the full list; a sponsor using it for its own marketing is a separate controller with its own basis.
- Collect name, email and at most one qualifying field; ask for a work email only where Tier B account matching matters, since students and hobbyists have none.

Hold the contract under pressure:

| Rationalization | Why it fails |
| --- | --- |
| "Sales needs volume this quarter" | Tiers A and B carry every account with intent; the rest lowers acceptance and burns the audience the next episode needs |
| "They gave us their email, so they expect a call" | The form's notice and the region's email rules decide that, not the registration |
| "Benchmarks say 38% of attendees become MQLs" | That figure traces to no study |
| "Gate the replay to capture more leads" | Gate the bundle; a gated video loses the developers who learn from video |
| "The partner co-hosted, they get the list" | Only with the partner named on the form and its own basis |

Contract template, form wording, per-country notes and co-host checklist: [./references/handoff-and-consent.md](./references/handoff-and-consent.md).

## Measurement

Log every episode on one sheet; read the trend at the season review.

| Signal | Target | Basis |
| --- | --- | --- |
| Total reach (live + 30-day on-demand, all surfaces) | Flat or rising | Baseline |
| Live attendance / registrants | At or above the series' pilot median | Own baseline; population band with no history |
| Returning-attendee share | At or above the charter bar | Baseline, set from season one |
| Live and replay completion | Track the trend | Goldcast 2026: 74% live, 91% on demand |
| Questions per 10 live attendees | At or above the charter bar | Baseline |
| Job metric | Attendees ahead of matched non-attendees, pooled over the season | Directional; for a causal read with an eligible list in the thousands, hold back a random 10-20% of it from invitations for one season (baseline) |
| Tier A handoffs, sales acceptance | Acceptance at or above the contract bar | Contract |
| Replay within 48 h; next season's speakers booked | Every episode | Baseline |

Job metric by job: activation, 30-day first meaningful action (first API call, first trace); feature depth, feature adoption among attendee accounts; deal acceleration, stage progression of open opportunities with attendees; community voices, attendees who later speak, answer or contribute.

Never report registrations alone.

## Pass threshold

At each season review, continue unchanged only if all four hold, and apply the fix named for the one that fails:

1. No metric among total reach, live attendance and returning-attendee share falls below baseline: in season one, against the first two episodes' median, on two of the later episodes; from season two, against the prior season's median, for three consecutive episodes. Fix: topic and format first, slot second, cadence third.
2. The job metric moved in the attendees' favour. Fix: change the format mix toward the job's top-value format.
3. Every replay published within the deadline. Fix: cut cadence until production keeps up.
4. The topic backlog and speaker pool hold the next season. Fix: one season of community-question topics, or stop.

Stop the series, with an announced last episode, after two consecutive seasons failing criterion 2, or when the backlog cannot fill a season.

## Failure modes

| Failure | What it looks like | Fix |
| --- | --- | --- |
| Registration vanity | Report shows 300 registrants and nothing else | Live, total reach and the job metric beside it |
| Wrong benchmark | 22% judged against ON24's 60% | Own baseline; population-matched band |
| Calendar cadence | Weekly because marketing wants weekly | Cadence from capacity arithmetic |
| Product-tour topics | "What's new in 4.2" every month | Problem-titled backlog |
| Everyone is an MQL | Sales calls every attendee; registrations fall | Tiered contract, acceptance tracked |
| Gated library | Replays behind a form, few views | Ungated copy; gate the bundle only |
| List handed to partner | Co-host emails registrants who never heard of them | Named partner, separate box, joint arrangement |
| Endless series | Episode 30 runs on habit | Seasons with a written continue bar and stop rule |

## References

- DevRel-wide metric framework the series reports into: samber/developer-relations-skills@devrel-metrics
- Guest appearance on someone else's webinar or show: samber/developer-relations-skills@tech-podcast-interview-prep
