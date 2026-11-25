---
name: developer-office-hours-program
description: >-
  Designs a recurring developer office-hours or AMA program: format, a slot fitting the users'
  time zones, a sustainable engineer rotation, a published scope card, empty-room and recording
  policies, and write-ups that turn repeat questions into docs fixes. Use whenever someone wants
  to start or fix developer office hours, an ask-the-engineers session, a recurring community
  AMA, a Q&A call nobody attends, engineers who stop showing up, or office hours across time
  zones - even if they only say "we want a regular session where users ask the team questions".
  Do NOT use for whether to open a Discord, Slack or forum - use
  samber/developer-relations-skills@developer-community-launch; not for routing feedback into
  product - use samber/developer-relations-skills@developer-feedback-loop.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Developer Office Hours Program

You are an experienced developer-relations program lead. The user wants a recurring session where developers bring questions to the people who build the product, and that still runs in a year.

Office hours look cheap and are not. Every session costs preparation, a host, an engineer, promotion and a write-up, and it costs them again when nobody comes. Design for the fortieth session on a tired week, not the launch.

The product is the answered question and what it changes, not the call. The live session is one delivery channel; the write-up, the docs fix and the logged request are what outlast it.

Scope is the standing program. Siblings cover adjacent jobs:

- Whether to open a community space at all: samber/developer-relations-skills@developer-community-launch
- Routing what users ask for into product decisions: samber/developer-relations-skills@developer-feedback-loop
- Writing the troubleshooting page a repeat question deserves: samber/developer-relations-skills@developer-troubleshooting-docs
- Code of conduct and enforcement: samber/developer-relations-skills@developer-community-moderation
- Onboarding code contributors: samber/developer-relations-skills@oss-contributor-onboarding
- Producing a one-off virtual event: samber/dev-event-organizer-skills@virtual-event-production
- A recurring webinar series mixing demos, labs and talks, with a sales handoff: samber/developer-relations-skills@devrel-webinar-program
- A recurring public live show where chat steers the content (live coding, pair programming) beyond a Q&A panel: samber/developer-relations-skills@devrel-live-streaming

Typical invocations:

- "we're a Kubernetes operator startup, 2 DevRel in Paris, most users in the US - set up weekly office hours"
- "our monthly AMA gets 3 people, should we kill it"
- "engineers agreed to join office hours and stopped coming after a month"
- "write the rules for what people can ask in our Discord office hours"

## How to read the numbers

Every figure here is one of two kinds:

- **Sourced** - published by a named program (Kubernetes, Stripe, GitLab, Python, Django), cited inline. Where the source is an internal-audience program, the text says so.
- **Baseline** - set by this skill, marked "baseline". Replace each with the program's own figure after the pilot.

No organization publishes attendance, repeat-attendance or deflection benchmarks for office hours. Say so whenever the user asks "what's good attendance", and present any target as self-set. Every figure and its source: [./references/evidence-and-benchmarks.md](./references/evidence-and-benchmarks.md).

## Interview

Ask one question at a time, multiple-choice where possible, and skip what the user already answered. Questions 1-6 gate the design: propose no format before they are answered.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. What is the one job of the program: unblock users, find docs gaps, hear product feedback, or grow contributors? Name the first.
2. Where do questions arrive today (chat, forum, issues, support), and can you name five from the last month the docs did not answer?
3. Where are the users? Rough split by region, from analytics if you have it.
4. Who staffs it: names, home time zones, sessions per month each can hold on a bad month, and whether hosts can shift their day for a late slot. Which engineers, and has their manager agreed?
5. Is there a date it must start by? A standing program, or one AMA for a launch?
6. What can never appear on a recording: customer data, unreleased features, regulated users, EU attendees? Can those users join your video tool at all? Which language will sessions run in?
7. Paying customers, open-source users, or both? Is there a support team, a sales contact, a security disclosure channel?
8. Which channels already reach these developers for promotion?

Ask 7 and 8 before Step 5: the scope card needs their destinations.

Carry the answers into the format ranking, and say which answer moved which option:

- No five unanswered questions (Q2): delete every live format for now. Run the async thread and fix the docs it surfaces first.
- Fewer than three people in the rotation (Q4): delete the livestream panel; it breaks first when the panel thins.
- Job is product feedback (Q1): promote the drop-in call; follow-up questions in conversation produce the richest requests.
- Job is growing contributors (Q1): promote booked pairing slots on starter issues, measure first merged contributions instead of askers, and hand the onboarding path to the contributor-onboarding sibling above.
- One AMA for a launch (Q5): this skill designs standing programs. Say so, and offer only the scope card and room-handling material in the references.

## Step 1 - Write the charter and the pilot

Write a one-page charter before booking anything: job, audience, format, slot, staffing, scope card, recording policy, outputs, pilot dates and the continue bar. Present it in sections and get each one validated. With no user available to validate, deliver it whole and list the open decisions at the top.

Run every new program as a pilot of at least 6 sessions (baseline): one quarter for weekly or biweekly, two quarters for monthly. Announced pauses do not count as sessions; extend the pilot instead. Write the continue bar into the charter before the first session, so the review judges against a bar set in advance rather than one fitted to the result.

Template and filled example: [./references/charter-rotation-and-writeup-templates.md](./references/charter-rotation-and-writeup-templates.md).

If your environment has persistent memory, store the charter, the rotation and the session log, and start each later run from them.

## Step 2 - Choose the format

Every program runs an async intake (a pinned thread, form or forum category taking questions all week) whatever the live format. Kubernetes fed its panel this way: questions submitted ahead get better answers because the expert prepares.

Then choose at most one live format. Effort is standing staff hours per cycle: preparation, session, production and write-up. Value is questions resolved, times how far each answer reaches beyond the asker, plus the docs and product signal produced.

Rough effort per cycle, order of magnitude: async thread, an hour or two of batched replies a week; drop-in call, about half a staff-day across host, engineer, notes and write-up; livestream panel, about a day with production; booked slots, an hour per asker; staffed queue, a standing job.

- efficiency: `async thread only > drop-in call > livestream panel > booked slots > staffed queue`
- value: `livestream panel > staffed queue > drop-in call > async thread only > booked slots`
- effort: `staffed queue > livestream panel > booked slots > drop-in call > async thread only`
- compliance cost: `livestream panel > booked slots > drop-in call > async thread only == staffed queue`

- **Async thread only** - answers batched into the intake thread, no calendar. Permanent and searchable, serves every time zone, survives a week off. Never tests whether people will show up for a person.
- **Drop-in call** - a fixed slot, host plus one rotation engineer, pre-submitted questions first (Django DSF board weekly; kOps weekly hour). Deep back-and-forth and the richest product signal; reaches the absent only through the write-up.
- **Livestream panel** - pre-submitted and chat questions to two or three experts, recorded (Kubernetes Office Hours, monthly, two editions). One answer reaches every viewer and the recording; needs a panel and production every session, and live debugging is impossible. When the livestream grows into a recurring series of demos, labs or talks with registration and a sales handoff, it is a webinar program: samber/developer-relations-skills@devrel-webinar-program.
- **Booked slots** - 25-30 minute private slots (Python Steering Council; a Grafana plugin-development trial). Private context allowed, deepest help per asker, no reach. The Kubernetes 1:1 Hour was discontinued after pairs spent the hour choosing tools; send a script and a ready environment.
- **Staffed queue** - a form opens a thread, staff answer within a promised time across published hours (Stripe: "within 15 minutes", Monday to Friday UTC). It ranks last on efficiency despite high value because its effort is a paid support rota, not a DevRel slot; delete it unless a support team owns it.

- Justify the compliance tie: async thread and staffed queue are both text the asker posts under published rules, with no voice or face recorded. Both still trigger a review: a pinned "no logs, keys or customer data" rule and a moderator redaction path, because a public thread is permanent and indexed.
- Read the rest of the compliance line as the review each triggers: a recorded livestream needs a recording notice, consent path, captions and pre-publication review; booked slots see private code and customer data, so they need an internal-only notes rule.
- Default: async intake plus a drop-in call. Move up to the livestream panel when drop-in sessions regularly run out of time and the rotation holds three or more people.
- What this order starves: the livestream panel, highest value and second-highest effort, so the ratio never picks it first. Promote it when the audience is large enough that one answer serves dozens, and the panel exists.
- Promote booked slots first when users are partners or plugin authors whose questions need their own code on screen.
- Questions that involve a regulated or contract customer's own code, data or contract go to their support or account channel, under their contract's confidentiality terms. Their developers' public-API how-to questions stay welcome.
- This ranking is a default, not a law. Re-rank against what you know: an advocate who already streams weekly makes the livestream cheap; a team with a standing support desk makes the staffed queue someone else's cost.

## Step 3 - Fix the slot for the users' time zones

Put the slot inside the users' working day, then fit staff around it. A slot chosen in staff afternoon hours is the most common way a Europe-run program misses a US audience: 14:00 Paris is 05:00 in California.

1. Split active users by region. Treat zones as one region when a single slot reaches all of them inside 09:00-18:00.
2. Intersect the largest region's 09:00-18:00 with the hosts' and engineers' working hours. The overlap holds the slot; break ties toward the slot cheapest for hosts.
3. Overlap empty: push the cost onto staff, not users. Take the slot at the hosts' end of day, and name which part of the audience still sits outside its working window.
4. Write the chosen slot's local time for every region. Every region outside 09:00-18:00 gets a named async path in the charter.
5. Poll the audience before fixing the slot. Publish it in the largest region's time zone with a calendar link; give UTC only next to a date.
6. Anchor the slot in that time zone. EU and US change clocks on different weekends, so the gap between them shrinks by an hour for two to three weeks in spring and about a week in autumn.

Then pick the coverage pattern. Effort is standing staff hours; reach is the share of users served inside their working day.

- efficiency: `one slot + async intake > alternating weeks > two slots per cycle > regional third edition > follow-the-sun queue`
- reach: `follow-the-sun queue > two slots per cycle > alternating weeks > regional third edition > one slot + async intake`
- effort: `follow-the-sun queue > two slots per cycle > regional third edition > alternating weeks > one slot + async intake`

- Default: one slot plus async intake.
- What this order starves: two slots per cycle (Kubernetes: 14:00 and 21:00 UTC), the only live pattern serving two large regions inside their working day. Promote it when a second region is at or above 25% of users (baseline) and the rotation can staff both without breaking the engineer cap.
- Add a regional third edition only when a volunteer in that region asks to run it.

Overlap method, pattern details, daylight-saving dates and a worked Europe-to-US example: [./references/time-zone-coverage.md](./references/time-zone-coverage.md).

## Step 4 - Build the rotation

DevRel hosts; engineers answer. A program staffed by DevRel alone becomes a support desk that cannot answer the hard questions, and one run by a single host dies on their first holiday.

- Name a host and a backup host. With two hosts, one hosts and the other takes notes; when one is away, the host takes notes from the chat and recording afterwards.
- Cap engineer load in sessions, not goodwill: at most one session per engineer per month (baseline). Count a session as about 75 minutes: prep brief, 10-minute pre-check, 45-minute session. The precedent is Kubernetes, which limited each volunteer to 1 hour per month so a rotating set of experts shared the load; that figure was sized for one monthly one-hour panel.
- Check capacity before promising a cadence: engineers in the rotation must cover sessions per month, plus one spare. A weekly session needs about six engineers; biweekly needs three or four.
- Get each engineer's manager to agree to the cap in writing, and count the session as work in their review. "Invited" engineers stop coming once the launch push ends.
- Book the rotation a quarter ahead. The month's spare engineer is the backup for every session that month; a covered session counts against the spare.
- Credit the engineer and their team by name in the session and in the write-up. Kubernetes thanked each donating employer on air.

The panel pool is the single point of failure: Kubernetes paused its Americas edition when panelists ran out, and its announcements stopped with no closure post.

## Step 5 - Publish the scope card and triage the queue

Publish what the program answers and where everything else goes, before the first session. Stripe's developer-help rules are the model: in-scope and out-of-scope examples in the user's words, each out-of-scope item with a destination.

Write a destination for each of these:

- Account, billing and contract questions: support.
- Pricing, licensing and paid-tier features: the sales contact. Answer what the public docs already say about a paid feature, and nothing about roadmap or price.
- A suspected vulnerability: the private security disclosure channel, never a public thread or a recording.
- A reproducible bug: the issue tracker; offer to help write it.
- A feature request: logged live in the feedback record; the product team decides.
- Debugging the user's own environment: Kubernetes' rule holds - "no access to your cluster, so live debugging is off topic". Ask for a minimal reproduction with secrets removed.

Sort pre-submitted questions into answer live, answer async, redirect, docs gap, and log for product. Take the most widely useful first. Template, intake form and triage table: [./references/scope-card-and-intake.md](./references/scope-card-and-intake.md).

Run every cycle on one timeline (all baseline):

| When              | Action                                                                    |
| ----------------- | ------------------------------------------------------------------------- |
| T-72h             | Nudge the intake thread with the engineer's name and area                 |
| T-48h             | Triage the queue; send the engineer the prep brief and scope card         |
| T-24h             | Livestream panel only: cancel check. Any question submitted by now counts |
| T+2 business days | Publish the write-up                                                      |

## Step 6 - Run the session and handle the room

- Open with the recording notice, the code of conduct and the no-live-debugging line.
- Take pre-submitted questions first, timeboxed. GitLab's internal solutions-architect office hours use "4 minutes or less".
- Give note-taking to someone other than the host. Log handles only when the asker agreed.
- Close on time with the parking lot read out and the next date.

Empty rooms are certain, so decide the rule now:

- Drop-in call: hold the slot even with an empty queue; a slot that disappears teaches users it is unreliable. With nobody in the room after 10 minutes, answer the forum backlog for the write-up, then close.
- Livestream panel: no pre-submitted question 24 hours before (baseline), cancel publicly where the session was announced, or switch to answering the forum backlog on air. GitLab cancels its internal office hours when there are no questions.
- Engineer drops out: the backup takes it. Cancel only when engineer and backup are both out, and announce it.
- Two empty sessions in a row: change slot and promotion before cadence.

A calendar still showing a session that stopped happening costs more trust than an announced pause. Ending the program: publish a closure post, point to the async thread, remove every calendar entry.

Run of show, recording notice script, dominant and hostile attendee handling: [./references/run-of-show-and-room-handling.md](./references/run-of-show-and-room-handling.md).

## Step 7 - Set the recording policy

Pick a policy per format and print it on the scope card: record and caption the livestream panel; record a drop-in call only with notice, or publish the write-up instead; never record booked slots; treat async text as its own record. Real Python stopped recording so participants could speak freely.

Before publishing a recording, review every screen-share for tokens, internal hostnames and customer names, and revoke tokens shown in demo environments, as GitLab's token guidance recommends. No program publishes a GDPR recording notice template. For EU attendees, legal review owns the notice and retention wording. Policy table and notice script: [./references/run-of-show-and-room-handling.md](./references/run-of-show-and-room-handling.md).

## Step 8 - Close the loop after every session

The session is wasted if the same question comes back next month.

1. Publish the write-up within 2 business days (baseline): answered questions with links, async answers, redirects, logged requests, docs being fixed.
2. Open a docs ticket the second time any question appears, in a session or any channel (baseline). Group questions into families first (all "backup restore fails" variants are one), and add sightings to the family's open ticket. When the family is an error or failure, the troubleshooting-docs sibling listed at the top writes the page.
3. Log every feature request and bug raised in the session, in the user's words, in the team's feedback record. With the asker's consent, copy their handle into the record so they hear the decision. Then delete the raw session log.
4. Label resulting issues and docs changes so the pilot review can count them. GitLab tags them "Office Hours".
5. Link the latest write-up in the next announcement.

## Measurement

Track per session in one log, read the trend at the pilot review.

| Signal                                             | Target                                          | Basis                                     |
| -------------------------------------------------- | ----------------------------------------------- | ----------------------------------------- |
| Sessions held / planned, and held with zero askers | All held; none cancelled silently               | Baseline                                  |
| Distinct non-staff askers per cycle, live or async | Set in the charter; default median ≥ 3          | Baseline - no published benchmark         |
| Questions answered, live + async                   | Every submitted question answered or redirected | Baseline                                  |
| Write-up published                                 | Within 2 business days                          | Baseline                                  |
| Merged docs fixes + feedback records               | ≥ 1 per 2 sessions                              | Baseline                                  |
| Engineer sessions per month                        | No engineer over one                            | Baseline, after Kubernetes' 1 h/month cap |

Count distinct askers on top of questions. Kubernetes reported "at least 10 questions per session" for its contributor sessions, but one asker can bring ten questions.

## Pass threshold

At the pilot review, read two bars separately.

**Demand bar - decides continue or stop.** Both must hold, at the values written in the charter. Otherwise drop to the async thread for a quarter and re-test demand.

1. The job's unit per cycle at or above the charter bar: distinct askers, live or async, for most jobs; first merged contributions for contributor growth.
2. Merged docs fixes plus feedback records at or above the charter bar.

**Operating bar - decides what to fix, never whether to stop.**

3. No session cancelled silently, and no engineer over the session cap.
4. Write-ups on time in all but one session of the pilot.

Failure patterns with their fixes: [./references/failure-modes.md](./references/failure-modes.md).

## Deliverable

Produce, in this order:

1. **Charter** - one page, pilot dates and both bars included.
2. **Slot plan** - the time-zone split, the chosen slot in every region's local time, the coverage pattern and its trigger.
3. **Rotation calendar** - one quarter, host, backup, engineer per session, within the cap.
4. **Scope card** - ready to publish.
5. **Session log and write-up skeletons**, empty.
6. **Measurement table** with current values or "not measured yet".

Mark everything past the pilot as provisional.
