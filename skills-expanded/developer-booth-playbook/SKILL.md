---
name: developer-booth-playbook
description: "Writes an exhibiting company's own playbook for an in-person booth at a developer conference: who works it and how many per shift, roles, how staff open and qualify a conversation, how each lead is captured and graded, swag and giveaway policy, and the exhibitor rules to obey. Use whenever a team is sending people to work a booth at KubeCon, re:Invent, PyCon, DevOpsDays or any developer event and asks about booth staffing, shifts, badge scanning, booth lead qualification, booth swag, a booth raffle or booth etiquette - even if they only say 'we got a booth, now what'. Do NOT use for choosing the event or tier (samber/developer-relations-skills@developer-event-sponsorship) or the demo itself (samber/developer-relations-skills@developer-live-demo-design)."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Booth Playbook

You write the floor plan for a booth a company already bought: who stands in it, when, what they say, what they write down, and what they hand out.

A developer audience judges the company by the person in the booth. Every rule below protects one unit: the **qualified conversation** (grade A below) - someone with the problem, who agrees to a named next step. Badge scans, swag handed out and foot traffic are activity counts, never the goal.

Route elsewhere when this is the wrong table:

- Which event, which tier, which activation, the ROI threshold → `samber/developer-relations-skills@developer-event-sponsorship`. This skill starts once the booth is bought.
- The demo loop, its restore points and failure plan → `samber/developer-relations-skills@developer-live-demo-design`.
- Everything after the hall closes: sequences, nurture, conversion → `samber/developer-relations-skills@developer-event-followup`.
- Dinners and invite-only side events → `samber/developer-relations-skills@devrel-field-events`.
- A recruiting table at a job fair → `samber/developer-relations-skills@tech-employer-branding`. A virtual booth on an online event platform has no floor, shifts or swag shipping; this skill does not fit it.
- Designing the whole expo floor as the organizer → `samber/dev-event-organizer-skills@event-booth-experience` (sibling collection).

## Interview

Ask one question at a time, multiple-choice where possible, and skip any the user's brief already answered. Q1, Q2, Q5 and Q6 block the plan; draft with stated assumptions for the rest and confirm them in the draft.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Which event, which dates, and what kind: community or volunteer-run, foundation or large vendor conference, or a vendor's own show?
2. What did the package buy: booth size, staff passes, lead retrieval or none, a demo station, power?
3. What is the booth's one objective, and the qualified-conversation bar plus minimum count set when it was bought? If none exists, step 2 sets one.
4. Who buys the product: a developer with a card, a developer who champions it to a buyer, or a buyer who never touches it?
5. Who can you send: names or roles, and how many can debug a stranger's code in your product?
6. What are the hall hours per day, and when do keynotes and breaks fall?
7. What do you already own: swag stock, a demo, last event's booth notes, a brief?
8. By what date must the swag order and the travel be locked? Work back from that, not the event date.
9. One event, or a booth you will run again at the next edition?
10. Effort ceiling: engineer-days you can pull off the roadmap, and who owns the conversation log after the event?

Re-rank the menus below against the answers, and say which answer moved which option:

- Q2 decides capture: no lead retrieval in the package (usual at community events, always at DevOpsDays) deletes the scanner rung in step 7.
- Q4 decides the crew: a buyer who never touches the product promotes the DevRel and account-executive pair in step 3.
- Q5 short on engineers: apply the coverage rule in How many per shift, item 6.
- Q7 swag already bought: keep it, and move it to the ambient or earned rung; never gate it behind a scan.
- Q8 inside an item's production and shipping time: delete that item; stock already owned wins.
- Q9 recurring: promote the hand-written conversation log and the earned swag item, since both compound into next edition's notes and recognition.
- Q10 low: cap the crew at two per shift, delete the rotating volunteer model, and apply the crew-of-two rule in How many per shift, item 7.

In the memory file named above, keep per event: the rules table, the shift grid, the A count against the minimum, and what the debrief said to change.

## Workflow

1. **Read the event's exhibitor rules before planning anything.** Fill the rules table in [references/exhibitor-rules-checklist.md](./references/exhibitor-rules-checklist.md) from that event's own exhibitor manual or sponsor guide. Rules differ per event, sometimes in opposite directions: in the editions cited there, staff lanyards were allowed at one large show and banned at another. Never carry rules over from a different event.
2. **Fix the conversation bar.** Copy the qualified-conversation definition, the named next step and the minimum A count from the sponsorship plan. If none exists, ask the user what count of A conversations makes the trip worth the staff-days, label it self-set, and point to `samber/developer-relations-skills@developer-event-sponsorship` for the full threshold. Brief every staffer on the exact words.
3. **Pick who goes** from the crew menu below.
4. **Size the shifts** with the headcount method below, then draw the shift grid and role cards ([references/staffing-and-swag.md](./references/staffing-and-swag.md)).
5. **Write the floor scripts**: opener, three qualifying questions, the hand-off line, the polite exit, and the purpose line said before taking contact details. Templates in [references/floor-scripts-and-capture.md](./references/floor-scripts-and-capture.md).
6. **Fill the booth before doors open**: invite existing users and open evaluations to book a slot at the booth, and post where the community already gathers. Pre-booked conversations are the surest A grades on a busy floor.
7. **Pick the capture method** from the capture menu below, and fix the record every conversation leaves.
8. **Write the swag policy** from the swag menu below.
9. **Run the show loop**: log at the end of every shift, read the log at end of day one, adjust day two with the triggers in [references/floor-scripts-and-capture.md](./references/floor-scripts-and-capture.md).
10. **Close the floor**: debrief the same day the hall closes, then hand the graded log to its owner for `samber/developer-relations-skills@developer-event-followup`. Stop there: sequences and nurture are that skill's job, and they stay within the purpose staff said aloud at capture.

## Who works the booth

Value is qualified conversations that continue after the event. Effort is engineer-days off the roadmap, briefing and coordination.

- value: engineer crew with a DevRel captain > DevRel and account-executive pair > rotating company volunteers > sales-led with an engineer on call
- effort: engineer crew with a DevRel captain > rotating company volunteers > DevRel and account-executive pair > sales-led with an engineer on call
- efficiency: engineer crew with a DevRel captain > DevRel and account-executive pair > rotating company volunteers > sales-led with an engineer on call

- **Engineer crew with a DevRel captain** (default) - people who answer the second question, led by someone who owns the brief and the log. DevOpsDays organizers report sponsors "benefit the most when they bring engineers" instead of scanning badges. It tops efficiency despite top effort because a developer booth without an engineer produces conversations that end at the first follow-up question.
- **DevRel and account-executive pair** - DevRel talks first, the account executive takes pricing and procurement on a rehearsed hand-off. Promote to default when Q4 says buyers visit the booth themselves.
- **Rotating company volunteers** - product, support and engineering staff on single shifts. Nothing is starved on these axes: the top-value rung also tops efficiency. Volunteers win on a value these axes do not count, the product team hearing users first-hand; promote them when that is the booth's objective, or when Q9 says the booth recurs and you want a deep bench.
- **Sales-led with an engineer on call** - last on every line. Delete it at community events, whose sponsor guidance asks for people who can "tell your story and participate with the community".
- Delete hired booth talent at any developer event: they cannot answer the follow-up question and every event badge rule still applies to them.

## How many per shift

Derive headcount from conversations, never from floor area.

1. Start at two people per shift, at least one able to debug a stranger's code: one stays free while the other is deep in a laptop.
2. Add one person per demo station, since a demo driver cannot qualify the person waiting. The driver needs the demo path, not engineering depth.
3. Plan one optional slot for peak blocks (breaks, opening reception, the first hour after lunch). Fill it once a shift log shows visitors leaving a queue. No measured conversations-per-hour benchmark exists; the "3 to 5 interactions per staffer per hour" in some organizer exhibitor kits is a trainer's planning target. Use its low end only to sanity-check that the crew can reach the step 2 minimum, then replace it with your own log.
4. Cap at what the space holds. The "50 square feet per staffer" figure is an exhibit trainer's rule of thumb repeated in organizer kits, not a study; use it only as a ceiling, since staff outnumbering visitors turn into a closed group nobody walks into.
5. Keep each floor block to two or three hours, agency advice rather than a measured fatigue limit, with a short overlap to hand over open conversations.
6. Cover every hall hour the event obliges: some shows make an unstaffed booth a contract breach or a fee. When engineers are fewer than blocks, put them on peak blocks, cap each at two blocks a day, and staff off-peak blocks with a trained non-engineer plus an engineer reachable within minutes. Say this trade-off in the plan.
7. Crew of two (overrides item 1 off-peak): both on the floor for peak blocks, alternating off-peak, nobody past two blocks in a row. At a single-track community event, staff the breaks together and attend talks while sessions run, unless the rules table obliges staffing then; the hall is empty anyway. Whoever can debug stays reachable within minutes while in a talk.

## Capture: what every conversation leaves behind

Every qualified conversation leaves one record: grade, problem in the attendee's words, stack, role, next step, owner, route, and the consent basis. Grade it at capture, not at the hotel: A = has the problem now, builds with or influences the decision, and agreed a named next step; B = has the problem, no next step yet; C = curious, learning, or here for swag. When a sponsorship plan defined the qualified conversation, copy its words into grade A verbatim so both count the same thing. Schema and examples: [references/floor-scripts-and-capture.md](./references/floor-scripts-and-capture.md).

Value is records that lead to a continued conversation. Effort is staff seconds per conversation plus clean-up. Compliance cost is the data review it triggers and the reversibility it spends.

- value: scanner with grade and note > hand-written conversation log > next-step QR code > consented prize draw
- effort: hand-written conversation log > consented prize draw > scanner with grade and note > next-step QR code
- compliance cost: consented prize draw > hand-written conversation log > scanner with grade and note == next-step QR code
- efficiency: scanner with grade and note > next-step QR code > hand-written conversation log > consented prize draw

- **Scanner with grade and note** (default where the event issues one) - scan A and B conversations only, after the conversation, then grade and note in the app or a paired sheet. A scan with no note is a name with no memory.
- **Next-step QR code** - one code per concrete next step (book a call, claim the event credit), tagged with the event. Captures only those who act, which is the point.
- **Hand-written conversation log** - what the order starves: the slowest rung and the only one that works everywhere. Promote it to default when Q2 says the package has no lead retrieval. Delete the scanner rung there.
- **Consented prize draw** - an opt-in draw, entry kept separate from marketing consent. Delete it when the rules table bans draws, or when entry requires a demo or a conversation.
- The tie: scanner data and a QR form both arrive with a privacy notice the attendee already saw, at registration or on your form, and need only your own basis for following up. A hand log makes you the collector at the table, so staff must hand over the privacy-notice link and keep the paper secure.

Never scan everyone who walks past.

| Rationalization                           | Why it is wrong                                                                                                                                                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "The scan costs nothing, sort later"      | Sorting later has no note to sort by; the follow-up writes to people who never talked to you.                                                                     |
| "Leadership counts leads"                 | Report scans as activity beside the qualified count; agree that split before the event.                                                                           |
| "They agreed to scanning at registration" | That covers the event sharing their data, not every use you make of it. Check with your privacy owner what basis covers what you send, and say the purpose aloud. |
| "Swag for a scan pulls traffic"           | It pulls swag collectors and grades every record C.                                                                                                               |

## Swag and giveaways

Value is conversations started or rewarded among the right people. Effort is procurement, sizing, shipping, storage and carrying home.

- value: earned useful item > one large prize draw > ambient stickers > no swag or a donation per conversation
- effort: one large prize draw > earned useful item > ambient stickers > no swag or a donation per conversation
- compliance cost: one large prize draw > earned useful item == ambient stickers == no swag or a donation per conversation
- efficiency: ambient stickers > earned useful item > no swag or a donation per conversation > one large prize draw

- **Ambient stickers** (default) - on the table, ungated, designed so the logo is not the whole design.
- **Earned useful item** - handed after an A or B conversation, never for a scan; a C takes the ambient item. A T-shirt counts only with inclusive sizing, straight and fitted cuts.
- **No swag or a donation per conversation** - promote when the company's stated values or the event's sustainability stance call for it.
- **One large prize draw** - what the order starves: one prize can beat many small gifts, at the top compliance cost. Promote when the event allows draws in the booth and the capture menu needs an opt-in path. Run the prize-draw checklist in [references/staffing-and-swag.md](./references/staffing-and-swag.md) first: total prize value across all prizes can trigger state registration and a bond in the US, and rules differ outside it.
- The ties: none of the three non-draw rungs triggers a review beyond the rules table.
- Delete gating any item behind a form or a scan. A conversation is the only gate, with one exception: the prize draw's entry, which never doubles as marketing consent.
- Check the rules table before putting the event's logo on swag or giving away branded lanyards: some events ban both.

Policy template, sizing and stock math: [references/staffing-and-swag.md](./references/staffing-and-swag.md).

## Pass threshold

The playbook is ready when it carries:

- a filled rules table for this event
- the conversation bar and minimum count, in the exact words staff will log
- a shift grid with every hall hour covered, and an engineer on every shift or reachable within minutes, stated in the plan
- floor scripts, a capture method and a record schema
- a swag policy with nothing gated behind a scan

After the event, the booth passes when it met its minimum A count and every A carries a next step and an owner. Report B beside it as warm interest. A big scan count with a missed conversation count is a miss; say so.

## Failure modes

| Symptom                                | Cause                                        | Fix                                          |
| -------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| Staff huddled, visitors walk past      | too many staff for the space, closed group   | cap per How many per shift, item 4           |
| Nobody can answer "how does it scale?" | no engineer on that shift                    | How many per shift, items 1 and 6            |
| Notes say "great chat"                 | grading postponed to the evening             | grade and note at capture, end-of-shift log  |
| Booth fined or leads withheld          | rules carried over from another event        | rules table from this event's manual, step 1 |
| Staff in the aisle with flyers         | aisle soliciting, banned at many shows       | everything happens inside the booth          |
| Leftover boxes of shirts               | stock sized to attendance, not conversations | size earned stock to the conversation target |

## Output shape

One booth playbook, one page per section: rules table, conversation bar, crew and shift grid, role cards, floor scripts, capture method and record schema, swag policy, show-loop and debrief agenda. Label every figure as event-published, the user's own, convention, or assumed (confirm before the event).

## Invocation examples

- "We got a 10x20 at KubeCon, who do we send?" → steps 1, 3, 4.
- "First booth at a DevOpsDays, they don't do badge scanning" → hand-written log default, step 7.
- "Marketing wants 500 scans at re:Invent" → reset the unit in step 2, then the rationalization table.
- "What swag should we bring to PyCon?" → step 8 against the rules table.

## References

- [references/exhibitor-rules-checklist.md](./references/exhibitor-rules-checklist.md) - rules table to fill, sourced examples from re:Invent, PyCon US, KubeCon and DevOpsDays, and figures that circulate without a source.
- [references/staffing-and-swag.md](./references/staffing-and-swag.md) - worked headcount, shift grid, role cards, swag policy template, sizing and stock math.
- [references/floor-scripts-and-capture.md](./references/floor-scripts-and-capture.md) - opener, qualifying, hand-off and exit lines, consent line, record schema, graded examples, end-of-shift log and debrief agenda.
