---
name: developer-event-followup
description: "Plans what a company does after an in-person developer event it exhibited at, spoke at, sponsored or ran a workshop at: sorting badge scans, booth notes, raffle entries, rosters and hackathon submissions, deciding who may be emailed and for what, writing the messages, routing contacts to product, community or sales, and measuring the cohort. Use whenever someone asks what to do with conference leads or badge scans, how to follow up after a hackathon or workshop, whether they can email the people they met, or why event leads never convert - even if they only say 'we got 400 scans at KubeCon, now what'. Do NOT use for working the booth (samber/developer-relations-skills@developer-booth-playbook) or webinar registrants (samber/developer-relations-skills@devrel-webinar-program)."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Event Follow-up

You turn the people a company met at a developer event into users, community members and, when they asked for it, sales conversations, without turning them into spam recipients.

A badge scan records presence, not intent. Every rule below protects two things: the promise staff made aloud when they took someone's details, and the reputation the company brings to the next edition. On Hacker News, developers name "people who scanned my badge at a conference" as a spam source their filters miss; a follow-up that ignores what was discussed costs more trust than silence.

Route elsewhere when this is the wrong table:

- Staffing the booth, grading conversations, the consent line said at capture → `samber/developer-relations-skills@developer-booth-playbook`. That skill hands its graded log here.
- Which event to buy, the cost-per-conversation threshold and the renew/drop verdict → `samber/developer-relations-skills@developer-event-sponsorship`. This skill supplies the outcome data that verdict reads.
- Webinar registrants and the webinar's sales handoff → `samber/developer-relations-skills@devrel-webinar-program`.
- Guests of a private dinner or roundtable you hosted → `samber/developer-relations-skills@devrel-field-events`.
- An organizer emailing its own attendees, including a meetup the company runs itself → `samber/dev-event-organizer-skills@event-attendee-email-sequences` (sibling collection).
- A newsletter that event contacts may opt into → `samber/developer-relations-skills@devrel-newsletter-growth`.

## Interview

Ask one question at a time, multiple-choice where possible, and skip what the user already gave. Q1-Q4 block the plan; draft with stated assumptions for the rest.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Which event, which type (booth at a conference, talk, workshop, hackathon, meetup), and when did it close?
2. What records exist, by source: graded conversation log, scanner export, raffle or draw entries, sign-up sheet, workshop roster, hackathon submissions, a list the organizer handed over? Roughly how many of each?
3. What did staff say when they took details? Paste the purpose line, the scanner screen text, the raffle form, the sign-up sheet header, and, for any organizer list, the organizer's notice about sharing with sponsors.
4. Where are the contacts based, or which jurisdictions does your privacy owner treat as in scope?
5. Who buys the product: a developer with a card, a developer who champions it to a buyer, or a buyer who never touches it?
6. What counts as activation in your product (API key, first successful call, first deploy)? Can you tag an event cohort in product data?
7. By what date must a result show (a sponsorship review, a quarter close)? One event, or a series you will repeat?
8. Effort ceiling: hours the staffers who met people can give this week, and who owns the follow-up after that?

Re-rank the track menu below against the answers, and say which answer moved which option:

- Q3 shows a purpose line narrower than marketing (or none at all) → delete the nurture track for those records; keep the sales handoff only where the attendee's own words asked for pricing, procurement or a buyer conversation.
- Q4 includes Germany, or any jurisdiction the gate's default treats as prior-consent → delete every marketing track for those records without a consent you can show.
- Q5 a buyer who never touches the product → promote the sales handoff for A records with a stated buying need, never for the rest.
- Q6 activation defined and a cohort tag possible → promote the activation path; without both, it cannot be measured, so ship the promised-item message instead.
- Q7 a series → promote the public recap and the community invitation, which compound into the next edition.
- Q8 under an hour per staffer → staffers write only the A messages; DevRel drafts the rest for their review.

In the memory file named above, keep per event: record counts by source and grade, the purpose lines, the jurisdiction gate result, the tracks chosen, and the 30/60/90 readings.

## Workflow

1. **Inventory the records** by source and grade, dedupe on email, and match against the CRM: an existing customer goes to the account owner, an open deal to the deal owner, and an earlier unsubscribe or objection wins over anything the event produced. Copy grades A/B/C from the booth log when one exists (A = has the problem now, builds or influences, agreed a named next step; B = has the problem, no next step; C = curious, learning, or here for swag). When notes exist without grades, grade them with these definitions and grade a doubtful one B. Grade raffle-only, scan-only and sign-up-sheet records C unless a note proves more. A scan with no note stays C: nothing in it can be personalized.
2. **Gate every source on purpose and basis.** Write down, per source, what the attendee heard and which jurisdiction applies, then fill the gate table in [references/consent-and-jurisdiction.md](./references/consent-and-jurisdiction.md). Gate the A rows first: it takes minutes and must not delay them. Agree the basis with the user's privacy owner; this skill frames the questions, it does not give legal advice.
3. **Send the A messages before the rest of the log is clean**, within two working days of the event closing, from the notes as they stand. That window is practitioner convention plus the fact that both sides still remember the conversation; no study measured event contacts (see the speed note below). Already past it: send anyway, say plainly when you met, never skip the note.
4. **Route each record to one destination** with the routing table below, and name an owner per A record.
5. **Pick the tracks** from the track menu below, per segment.
6. **Write the messages** from the templates in [references/followup-messages.md](./references/followup-messages.md), then run them through your preferred humanizer skill. Each one comes from the person the attendee met, quotes the problem in their words, delivers what was promised, and offers one next step.
7. **Set stop rules and suppression** before the first send (see Stop rules).
8. **Measure the event cohort** at 30, 60 and 90 days and hand the readings to the sponsorship review (see Measurement).

### What the speed evidence measured

The "respond within the hour" and "within 5 minutes" figures (Oldroyd, McElheran and Elkington, HBR 2011; the InsideSales/MIT study of 2007) measured inbound web leads, in research co-authored by a lead-response software vendor. Neither sampled booth, hackathon or meetup contacts. Never cite them, or "80% of trade-show leads are never followed up" (no published study supports it; industry write-ups report CEIR disowning it), as evidence for an event sequence. Act fast on A records because memory fades, and say that is the reason.

## Two kinds of message

- **The requested reply** delivers exactly what the attendee asked for: the config, the slides, the credit, the answer to their question. It answers a request, so keep it free of promotion and it stays outside direct marketing.
- **Direct marketing** is everything beyond the request: newsletter, nurture, product announcements, a sales sequence. It needs the basis the gate in step 2 found.

Most event follow-up goes wrong by dressing the second as the first: a "here are the slides" email that subscribes the reader to a nurture.

Apply four rules when reading the gate:

- **The requested reply is owed at every grade.** A scanner screen that promised "the config emailed to you" owes the config to every scan, C included.
- **Marketing needs two yeses**: the jurisdiction allows it, and the purpose line covers it. A UK corporate address or a US contact told "scan for the config" still gets no nurture, because the promise was narrower than the law. In the EU and UK the second yes is purpose limitation in law; in the US it is a trust rule, so say so: the law allows it, the promise does not.
- **Judge each message against the source that covers it.** An A conversation's own promise governs the personal note even when the same person also entered the draw. A separately ticked opt-in (an updates box on the draw form) counts on its own; a draw entry without that tick never widens anything.
- **Default to prior consent.** Treat Germany, every other EU or EEA country, and any jurisdiction the reference table does not list as requiring consent for marketing email, until the privacy owner names the local rule (France, for example, allows business prospecting under conditions).

## Routing

Route each contact to the team that can act on it, not only to sales, following Mary Thengvall's DevRel Qualified Leads (2019).

| Signal in the record                               | Destination                                                                    | Owner                       |
| -------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------- |
| stated buying need, budget or procurement question | Sales                                                                          | named account owner         |
| building with the product, blocked or evaluating   | Product path                                                                   | the staffer who met them    |
| bug or missing feature                             | Engineering                                                                    | triage owner, link the note |
| wants to contribute, speak, or host                | Community                                                                      | community lead              |
| integration or reseller interest                   | Partnerships                                                                   | partner manager             |
| existing customer or open deal                     | Account or deal owner                                                          | account or deal owner       |
| student, job seeker                                | Community; recruiting only where the capture or a reply covers it; never sales | community lead              |
| C with no note                                     | Public recap, plus any item the capture promised                               | DevRel                      |

Hand a record to sales only when the note shows the buying signal in the attendee's words; company size or cluster count alone is not one. Sales calls to students and hobbyists come back to DevRel as complaints, and the next booth pays for them. A participant under 18, common at high-school hackathons, gets no marketing at all without the privacy owner's sign-off.

## Follow-up tracks

Value is continued conversations and activations. Effort is staffer hours that cannot be delegated, plus build time. Compliance cost is the review a track triggers and how hard it is to undo once sent.

- efficiency: public recap > promised-item message > personal note > community invitation > activation path > sales handoff > nurture sequence
- value: personal note > activation path > sales handoff > promised-item message > community invitation > public recap > nurture sequence
- effort: personal note > activation path > sales handoff > nurture sequence > promised-item message > community invitation > public recap
- compliance cost: nurture sequence > sales handoff > community invitation > activation path > personal note == promised-item message > public recap

- **Public recap** (default for C) - one post or page: slides, repo, recording, answers to the questions the booth heard most. Reaches every attendee, needs no contact data, triggers no review. Send the link to nobody; publish it where the community already reads.
- **Promised-item message** (default for B, and owed to any grade whose capture promised an item) - one email delivering what was promised. Add a single opt-in link only where the gate's marketing column says yes; elsewhere put the opt-in on the public recap page instead, since an email asking for consent can itself count as advertising under prior-consent rules. No second email unless they click.
- **Personal note** (default for A) - written or reviewed by the staffer who had the conversation, from their own address, quoting the problem, delivering the next step agreed at the booth. Highest value, and the one track nobody else can write.
- **Community invitation** - an invitation to the forum, chat or next meetup, sent once, to people whose basis covers it.
- **Activation path** - what the order starves: top value after the personal note, but it needs a build (a "finish the exercise" page, an event credit, a guided first call) and a cohort tag. Promote it to default for workshop and hackathon cohorts, where everyone already started building, and whenever Q6 says activation is measurable.
- **Sales handoff** - an introduction from the staffer to the account owner, in the same thread, never a cold sequence. Only for A records whose own words asked for pricing, procurement or a buyer conversation: that request is what the handoff answers.
- **Nurture sequence** - last on efficiency, top on compliance cost. Allowed only for records whose capture said "updates" or whose consent you can show. In Germany, an updates-purpose scan becomes a consent you can show through one confirmation email with no promotion, enrolled only on the click (double opt-in). Use it only where the capture already said updates; on any narrower purpose the confirmation email is a cold consent request, itself advertising. Delete the track for a raffle entry alone, scan-only records with a narrower purpose, and prior-consent jurisdictions without consent, rather than ranking it last.

The tie: a personal note and a promised-item message each answer the attendee's own request, reviewed once against the purpose line, and add no new purpose.

This order is a default. Re-rank against what the user already owns: an existing tutorial collapses the activation path to an hour of linking; a community that already runs monthly meetups makes the invitation the strongest track for B.

## Event-type variants

| Event type                      | A track                                                                                                 | Everyone else                                                                        | Watch for                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------- |
| Booth                           | personal note within two working days                                                                   | promised item to every record the capture promised it to; recap                      | scanner text promised one purpose; honour it                    |
| Talk (people who came up after) | personal note with the answer you owed                                                                  | recap with slides and recording                                                      | no list exists; do not build one from the room                  |
| Workshop                        | activation path with their half-finished exercise                                                       | same path, to every roster member whose sign-up line covered the materials           | slides alone end the journey at the slides                      |
| Hackathon                       | personal note to teams that built on your API, referencing their project; feature offer with permission | public showcase of all submissions; 30-day project check-in for teams still building | many participants are students: route to community, never sales |
| Meetup                          | invitation to the next one or to co-host                                                                | recap                                                                                | RSVP platforms share emails only when members chose to          |

## Stop rules

- Send each B and C record at most one message unless they reply or click the opt-in.
- Stop a batch and review the gate before sending more when either trigger fires (this skill's threshold, not a published one): the second spam complaint, or unsubscribes and "who are you, remove me" replies running above what the last event produced. Count every observable negative, not complaints alone: company-domain mailboxes rarely report complaints back to the sender. Protect the sending domain's daily Gmail rate (Google's 0.10% target and 0.30% ceiling in Postmaster Tools), but never wait for it to react: a few hundred event emails rarely show in it.
- Load records into the CRM as non-marketing contacts carrying source, grade, purpose line and capture date; enrolling in any marketing flow requires the gate's yes. Importing is not sending, and a bulk enrolment is how the nurture reaches people the gate excluded.
- Agree retention with the privacy owner: raffle data goes once the prize ships, unanswered scan-only records after the period they set.
- Honour unsubscribes and objections at once and add them to a permanent suppression list. The US legal floor is 10 business days and Yahoo expects bulk senders within 2 days; the right to object in the EU and UK is absolute.
- Never import a bought, scraped or rented list, and never re-use a raffle entry alone for marketing. An organizer-supplied list is usable only within what its notice told attendees about sharing with sponsors; in the EU and UK, marketing email to it needs consent that named your company, since "sponsors" or "partners" wording is not valid consent. A list handed over with no sharing notice gets no import: return or delete it and tell the organizer. In the EU you owe those people your own privacy notice no later than your first email, and within a month in any case.

| Rationalization                                  | Why it is wrong                                                                                                                                                                                                                                |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "They agreed to scanning at registration"        | that covers the organizer sharing data with you, not every message you send; check the gate                                                                                                                                                    |
| "Legitimate interest covers B2B email"           | in most of the EU, and always in Germany, unsolicited marketing email needs consent or soft opt-in; a few member states, France among them, allow business email on legitimate interest under conditions. Check the member state, never assume |
| "Leadership wants the whole list in the nurture" | every complaint lands on the sending domain's reputation, and the domain pays for every event after this one                                                                                                                                   |
| "It's just a thank-you"                          | a thank-you that links a newsletter signup is marketing; send it only where the basis covers it                                                                                                                                                |

## Measurement

The follow-up passes when the event cohort shows outcomes, not opens. Fix these before the first send:

- **Event cohort activation** - share of contacts from this event reaching the activation event (Q6) by day 30, 60 and 90, beside a non-event baseline. Track A, B and C separately.
- **Replies to A notes** and next steps completed, per owner.
- **Influenced versus sourced** - sourced means the event was the first touch on an opportunity, influenced means any event touch before close. Report both; developer events mostly influence, and claiming source for an influenced deal is the claim a CFO will test.
- **Complaint rate, unsubscribe count and time to suppression** - guardrails, never goals.

Read the 30-day numbers into the sponsorship review in `samber/developer-relations-skills@developer-event-sponsorship`; roll the program view into `samber/developer-relations-skills@devrel-metrics`. No published benchmark exists for event follow-up reply or activation rates; set the threshold from the company's own previous event or its blended acquisition cost, and label it self-set.

## Output shape

One follow-up plan per event:

1. Record inventory: counts by source and grade.
2. Gate table: source, purpose line heard, jurisdiction, allowed messages.
3. Routing list: A records with destination, owner and date.
4. Tracks per segment, with the ranking line and what moved it.
5. Message drafts, humanized, one per track.
6. Stop rules and suppression owner.
7. Measurement sheet: cohort tag, activation event, 30/60/90 dates, threshold labelled self-set or inherited.

## Invocation examples

- "We got 400 scans at KubeCon, marketing wants them in HubSpot by Monday" → steps 1-3, then the rationalization table.
- "Hackathon ended Sunday, 60 teams, how do we follow up?" → event-type variants, hackathon row, activation path.
- "The meetup organizer passed us their sign-up sheet, can we email them?" → step 2 with the jurisdiction reference.
- "Our event leads never convert" → inventory and gate first; capture without notes is a common cause, and more emails do not fix it.

## References

- [references/consent-and-jurisdiction.md](./references/consent-and-jurisdiction.md) - gate table to fill, rules by jurisdiction (EU, UK, France, Germany, US, Canada), purpose-limitation cases, deliverability limits.
- [references/followup-messages.md](./references/followup-messages.md) - templates per track, good and bad pairs, hackathon and workshop variants, the 30/60/90 measurement sheet.
- See `samber/developer-relations-skills@developer-community-launch` when no community exists yet to invite people into.
