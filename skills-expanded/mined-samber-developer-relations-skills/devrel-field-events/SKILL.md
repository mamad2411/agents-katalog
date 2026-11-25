---
name: devrel-field-events
description: "Plans the private, invite-only events a developer-tool company hosts beside someone else's conference: executive dinners, practitioner roundtables, customer receptions. Use whenever someone mentions a VIP or exec dinner, a roundtable or customer happy hour at KubeCon, re:Invent or any developer conference, field events, a side-event guest list or invite count, a guest's hospitality limit, or whether a conference dinner paid off - even if they only say 'we want to do a dinner during the conference'. Do NOT use for the booth (samber/developer-relations-skills@developer-booth-playbook) or for choosing which events to sponsor (samber/developer-relations-skills@developer-event-sponsorship)."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# DevRel Field Events

You plan the small private event a company hosts beside a conference it does not run: who sits at the table, why each one, what happens in the room, and what the company may honestly claim afterwards.

A field event is judged by the twelve people in the room, not by the hundreds in the hall. Every rule below protects one unit: the **named guest who leaves with a next step they agreed to**. Seats filled, covers paid and photos posted are activity counts.

Route elsewhere when this is the wrong table:

- Staffing the booth, qualifying walk-up conversations → `samber/developer-relations-skills@developer-booth-playbook`.
- Which conferences to attend, at which tier, and whether a side event beats a booth as the activation → `samber/developer-relations-skills@developer-event-sponsorship`. This skill starts once a side event is on the plan.
- Badge scans, booth notes and bulk post-event sequences → `samber/developer-relations-skills@developer-event-followup`. Named guests of the event you host stay here.
- A public, recurring meetup you run → `samber/developer-relations-skills@developer-meetup-program`.
- A standalone dinner series or roadshow with no host conference, or the conference organizer's own VIP programme → `samber/dev-event-organizer-skills` (`business-event-formats`, `event-vip-social-program`), sibling collection.
- Booking one-to-one meetings with attendees, a customer advisory board, a press or analyst dinner, or a dinner for your own staff: not this skill. The first two are sales and product work; press goes to `samber/developer-relations-skills@tech-press-relations`.

## Interview

Ask one question at a time, multiple-choice where you can, and skip what the brief already answers. Questions 1-5 block the plan; draft the rest with stated assumptions.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Which conference, which dates, and is the company a sponsor, an exhibitor, a speaker, or only attending?
2. What should the evening change? Pick one primary: move open deals forward, open accounts that ignore outreach, expand or keep a customer, recruit customer advocates, or build ties with maintainers and community leaders.
3. Who must be at the table: engineers and maintainers, engineering managers, or executives who sign? How many such named people will attend the conference?
4. Who owns the accounts: account executives, customer success, founders, or nobody (DevRel only)?
5. Do any likely guests work in government, state-owned companies, healthcare or another regulated sector? Which countries?
6. Effort ceiling: who hosts in the room, how many hours can account owners give to nominations and follow-up, and what envelope covers venue, food and travel?
7. By what date must the result show (a quarter close, a board review)? One evening, or a series across several conferences this year?
8. Can the CRM tag invitees and attendees, and does a baseline exist from past side events?

Re-rank every menu below against the answers, and say which answer moved which option:

- A quarter-close deadline promotes formats that seat open opportunities next week; a series mandate promotes the format you can repeat at every conference with one guest-list method.
- An engineer audience deletes the executive dinner by default and promotes the roundtable and the reception.
- Guests from government or healthcare cap the format at the meal their rules allow (step 5) before any ranking applies.
- A DevRel-only team with no account owners deletes "move open deals" as an objective: nobody can carry a next step that needs a contract.
- Two teams asking for two audiences (sales wants executives, DevRel wants contributors) get two events, each with its own objective. One room serving both serves neither.
- Under three weeks before the conference, shrink the table, raise the invitation ratio, seat customers first, and keep "host nothing" on the table until the first reconfirmation.

In that memory, keep per event: the objective, the guest-list method, the show rate and the 90-day verdict. Conference weeks repeat; the next plan should start from last year's show rate, not from a vendor's.

## Step 1 - Decide whether to host at all, and what success means

Brainstorm before committing. Sketch **two or three plans** for this conference, each naming the audience, the format, the staff it consumes and what it gives up. Always include one plan that hosts nothing. Recommend one and get agreement before any venue is contacted.

Hosting nothing beats a half-filled room. Choose it when:

- fewer qualifying named people will attend the conference than the invitation count step 4 needs (about three times the seats is this skill's default, not an industry figure);
- the conference forbids your company from hosting (step 2): re:Invent bars partners of the organizer who do not sponsor, and KubeCon reserves co-located events for sponsors;
- nobody in the company can host the conversation as a peer of the guests.

The no-host alternatives: pre-booked one-to-one meetings at the venue, buying into another company's dinner, or a seat at the organizer's own programme.

Write the success threshold now, before any venue is contacted, so the verdict is read rather than argued:

- a target share of seated guests with an agreed next step at 30 days (half is this skill's default);
- a show-rate target taken from your own past events; with no history, record this event's rate as the baseline and judge on next steps alone;
- for deal objectives, the stage movement expected at 90 days against a comparison group (step 7).

## Step 2 - Clear the host conference's rules first

Read the current edition's sponsor or exhibitor terms before you book a venue. Organizers publish the only hard constraints a field event has, and they change each edition. Large conferences restrict side events on five points:

- **Who may host** - some limit hosting to sponsors, and some bar non-sponsoring partners entirely during the week.
- **When** - windows that exclude the official programme and the official party night.
- **Approval** - some require approval before any venue contract, and force cancellation at your cost otherwise.
- **Branding** - most forbid the conference name or logo in your invitation; project marks such as "Kubernetes" follow their own trademark guide. Title the event by topic, city and date: "Stateful workloads dinner, Salt Lake City, 11 November".
- **Data** - KubeCon bans its lead-retrieval scanners at private sponsor events, and re:Invent keeps them for the expo floor. Take guest data from your own RSVP only.

Treat the common advice "you don't need the event's permission for a dinner across the street" as false until the terms say otherwise. Two recent examples show why:

- re:Invent: non-sponsoring partners of the organizer may not host during the week; every ancillary event needs written approval before any venue contract; reserving space within five miles of the venue needs prior written approval; a second sponsor or exhibitor in your event needs written approval too.
- KubeCon: co-located events are for sponsors only, inside published windows that exclude the programme and the official party night, with no conference branding. The guide is written for co-located events, so confirm in writing whether a private dinner counts, and plan as if it does.

Read [references/host-conference-rules.md](./references/host-conference-rules.md) whenever the conference is KubeCon or re:Invent, or publishes nothing: it holds the rule detail, what to ask an organizer that publishes nothing, and the competitor-exclusion etiquette.

Before paying a venue deposit, read its food-and-beverage minimum, attrition and cancellation clauses, and align the guaranteed-headcount deadline (typically a few days out) with your last reconfirmation in step 4.

## Step 3 - Choose the format

Value is named guests who leave with an agreed next step, per evening. Effort is host and account-owner hours before, during and after, plus the venue negotiation. Compliance cost is the hospitality review the format triggers and how much of it a guest's employer can refuse.

- efficiency: practitioner roundtable > seated dinner > co-hosted dinner > reception > activity outing
- value: seated dinner > practitioner roundtable > co-hosted dinner > reception > activity outing
- effort: seated dinner > activity outing > reception > co-hosted dinner == practitioner roundtable
- compliance cost: activity outing > reception > seated dinner > co-hosted dinner > practitioner roundtable

| Format                                                                     | Seats             | Wins when                                                                                           | Fails when                                                                                                             |
| -------------------------------------------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Practitioner roundtable (breakfast, lunch or early evening, 60-90 minutes) | 8-12              | one hard technical topic the guests own; engineers and managers                                     | the host conference windows forbid daytime events; the topic is your product                                           |
| Seated dinner                                                              | 10-14, 15 at most | executives or senior engineers who will talk for two hours; deals or accounts worth a whole evening | above 15 seats it splits into separate tables and stops being one conversation                                         |
| Co-hosted dinner with a partner                                            | 12-15             | a partner whose customers overlap yours halves list work and venue cost                             | the conference restricts co-hosts or their logos (step 2); the RSVP never told guests both companies get their details |
| Reception or happy hour                                                    | 30-80             | engineers and community; low pressure; recruiting advocates                                         | gatecrashers, alcohol-led tone, no conversation anyone remembers                                                       |
| Activity outing (a game, a tasting, a tour)                                | 10-30             | a customer thank-you with no commercial ask                                                         | public-sector or healthcare guests; anyone measuring pipeline                                                          |

- Justify the effort tie: the roundtable and the co-hosted dinner each cost one shared guest list and one short facilitation plan; the co-host splits a dinner's work in two, the roundtable never had a dinner's work.
- Default to the practitioner roundtable for developer audiences, and move to the seated dinner when the guests sign or veto purchases and the objective is deals or accounts.
- What this order starves: the seated dinner, the deepest format, loses to the roundtable on ratio every time. Promote it when the open opportunities named in the interview justify an evening each, or when the guests are executives who skip daytime sessions.
- Delete the activity outing whenever the objective is pipeline. When step 5 flags a regulated guest, delete every format whose meal exceeds that guest's limit; that guest gets a coffee meeting or pays their own way instead.
- Move the roundtable to an early-evening slot or the day before the conference when the windows forbid daytime events, as some editions do on core days. Delete it only when no window remains.

Developer guests reject sales theatre. Whatever the format: no slides, no stage, no product demo unless a guest asks, and a host who facilitates instead of presenting.

## Step 4 - Build the guest list

Build the list from accounts, not from whoever is free that night. Each name needs two things from the account owner at nomination:

- a one-line seat reason: open opportunity, stalled deal, new executive, expansion, advocate, or community anchor;
- a compliance flag for anyone from government, a public employer, healthcare or a regulated firm, read against step 5 before the invitation goes out.

Rank guest sources by seated value per hour of list work:

- efficiency: customer advocates in the same role as the prospects > account-owner nominations of open opportunities > named target accounts confirmed attending > one anchor guest (a respected maintainer or practitioner) > cold lists of attendees
- Delete cold lists entirely for dinners. They fill seats with "people who happen to be free", and a filler seat costs as much as a buyer's.
- What this order starves: the anchor guest, who takes the most persuading and alone makes the invitation worth accepting. Promote the anchor first when the guests are senior and the company is unknown to them.

Then do the invite math. Seats are not invitations:

1. Start from the seat count chosen in step 3 and reserve one internal seat per four or five external guests (three in a dinner of fourteen), so every guest has a host to talk to.
2. Invite about 2.5 times the external seats when most names are customers, 3 times for a mix of customers and warm accounts, and 4 times or more for prospects who have never met you. Vendor guidance spans 1.3x to 15x; the spread tracks list warmth, and no dataset settles it.
3. Accept yeses up to the external seats plus one. Later yeses go to a named waitlist; an executive who arrives to no chair is worse than an empty one. Overbook acceptances only for receptions.
4. Expect up to a third of accepted guests to drop out before the day. In one large event-software dataset, free events of 10-49 people had a median no-show near 37%; treat that as the ceiling for unreconfirmed RSVPs and replace it with your own history once you have one.
5. Send invitations from a named person's own address, peer to peer, three to five weeks out. Later invitations meet full calendars.
6. Reconfirm personally about a week out and again two days out, accept substitutes from the same account, and offer each released seat to the waitlist the same day it frees up. The day before is the last call, not the first: an executive rarely says yes on one day's notice in conference week.

For a co-hosted event, the RSVP names both companies and says both will receive the guest's details; agree before invitations go out who follows up which guest.

Write the seating plan: each prospect beside a customer in a similar role. An account owner may sit with their own account for continuity, never to pitch.

## Step 5 - Gate hospitality compliance at nomination

Read every flag from step 4 against these rules before the invitation goes out, never at the door. A guest who must refuse the dinner after accepting it costs the seat and the relationship.

- **US federal employees** may accept $20 per occasion and $50 per year from one source, and may not pay the difference to accept more. A dinner for a dozen is never a "widely attended gathering", and even a large reception counts as one only when the guest's agency authorizes it in writing; ask the guest to clear it. Otherwise offer coffee, or let them pay their own way. State and local rules differ.
- **Healthcare professionals** (clinicians and others who prescribe or buy medical products): pharmaceutical and medical-device industry codes cap their meals per country and bar sponsored entertainment. Those codes bind your company only if it sells health products; otherwise the guest's employer policy and anti-bribery law govern, and the industry caps make a sensible ceiling. Skip the activity outing either way.
- **Public hospitals, universities and other public employers** set their own gift rules; ask before inviting. **Employees of foreign governments and state-owned companies** fall under anti-bribery laws with no minimum amount, where proportionate, openly recorded hospitality is the defence.
- **Banks, insurers and other regulated private firms** often cap entertainment from vendors in their own policies; ask.
- **When two rules apply to one guest** (a federal health agency, a public hospital's clinicians), follow the stricter one. A host bound by a health-industry code applies that code's limit for the country where the event takes place.
- **Everyone**: ask the guest's own policy when in doubt, record the hospitality value per guest, and offer an alcohol-free option.

This step informs and never replaces the company's legal or compliance review; send any unclear guest there before inviting.

Two more rules bind every event:

- State photography in the invitation and get written consent before any named photo or quote is published.
- Name the attribution rule in the invitation. Under the Chatham House Rule, a recap may share themes but no guest list and no attributed quotes; "off the record" means no recap at all.

## Step 6 - Run the room

- Brief each internal host on every guest: role, account context, the one question worth asking them, and the next step that would make the evening a success.
- Open with two minutes from the host: who is in the room, the topic, the rule on attribution. Then facilitate questions between guests; the company speaks least.
- Assign each internal host four or five guests to talk to over the evening, matching the internal-seat ratio in step 4.
- Close with the topic, not a pitch. A guest who wants the product asks; someone answers then, briefly.

## Step 7 - Follow up each guest, then measure

Follow-up here is one person writing to one person:

- Within 48 hours, the internal host who spoke with the guest sends a personal note naming something the guest said and offering the next step agreed in the room. When the account owner was not at the table, the host writes, copies the owner, and the owner carries the step.
- A guest with no agreed next step gets a thank-you and nothing else.
- An RSVP is not consent to a newsletter or nurture sequence. Add a guest to one only when they ask.
- Route customers to their customer-success owner, and community guests to DevRel, rather than sending every guest to sales.

Read the verdict against the threshold written in step 1. Account owners nominate accounts already moving, so raw "influenced pipeline" credits the dinner with deals that were closing anyway. Compare attendees with accounts nominated but not seated before claiming acceleration:

- prefer waitlisted accounts as the comparison group, since accounts that declined self-select as less engaged and make the dinner look better than it was;
- when nominations exceed seats, choose among equally ranked nominations by lot, which gives a fair comparison for free.

With a few dozen accounts on each side, report counts, label the comparison directional, and pool it across events before calling a trend. Report meetings at 30 days, pipeline at 90 days, and velocity against that comparison after two quarters. The program-level metric set belongs to `samber/developer-relations-skills@devrel-metrics`.

## Pass threshold

The plan is ready when every event in it carries:

- one primary objective and the threshold written in step 1;
- the host conference's rules checked against the chosen date, time, venue and invitation wording;
- a seat count, an invitation count with its ratio, and a seat reason for every name;
- a compliance flag on every regulated guest;
- a named internal host and follow-up owner for every seat.

After the event, it passes when it met its own threshold on its primary objective. A miss means changing the guest-list method or dropping the format, never finding a friendlier metric.

## Failure modes

| Symptom                                                | Cause                                          | Fix                                      |
| ------------------------------------------------------ | ---------------------------------------------- | ---------------------------------------- |
| Six of fourteen seats empty                            | invitations equal to seats, no reconfirmation  | invite math and reconfirmation in step 4 |
| Executives arrive to no chair                          | more yeses accepted than seats                 | acceptance cap and waitlist in step 4    |
| Room full of people sales could not use                | list built from attendee lists, not accounts   | seat reasons from account owners         |
| Guests leave during the second course                  | pitch or demo from the host                    | facilitation plan in step 6              |
| Organizer cancels the event or bills the venue penalty | venue booked before approval, or not a sponsor | step 2 before any contract               |
| A government guest declines at the door                | no compliance flag at nomination               | step 5                                   |
| Dinner credited with pipeline that was already closing | no comparison group                            | step 7 comparison                        |

## Output shape

Produce one plan per event, in this order:

1. Objective and threshold.
2. Chosen format, and why the others lost.
3. The host-conference rule check.
4. Guest list table: name, account, seat reason, owner, compliance flag, status.
5. Invitation and reconfirmation schedule.
6. Run of show.
7. Follow-up owner per guest.
8. The 30/90-day review dates.

[references/field-event-plan-template.md](./references/field-event-plan-template.md) holds the template, an invitation and reconfirmation script, good and bad follow-up notes, and a worked invite-math example.

## Invocation examples

- "We're Gold at KubeCon, want a CTO dinner Tuesday night" → step 2 first (Tuesday is the official party night; confirm the window in writing), then steps 3-4.
- "Sales wants 40 prospects at a happy hour during re:Invent, we don't sponsor" → step 1 and step 2: hosting may be barred outright.
- "Who should we invite to our roundtable, and how many?" → step 4 with the interview's audience answer.
- "Was last year's dinner worth it?" → step 7; if no threshold was set, say the question cannot be answered honestly and set one for the next event.
