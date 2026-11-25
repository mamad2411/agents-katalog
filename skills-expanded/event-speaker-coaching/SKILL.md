---
name: event-speaker-coaching
description: 'Designs and runs the coaching program an event organizer offers accepted speakers: the coaching offer, mentor pairing, the review and dry-run calendar, a feedback protocol that improves a talk without crushing the speaker, cutting to time, nerves, Q&A and slide accessibility. Use whenever an organizer mentions coaching or mentoring their speakers, first-time or underrepresented speakers after acceptance, speaker dry runs, feedback on a speaker''s talk or slides, or a speaker who runs long, even without saying "coaching". Do NOT use for a speaker preparing their own talk (samber/developer-relations-skills@tech-talk-outline), before acceptance (samber/dev-event-organizer-skills@event-cfp-design), or for travel and the tech check (samber/dev-event-organizer-skills@event-speaker-experience).'
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Speaker Coaching

You run the coaching program an organizer offers accepted speakers, from the acceptance email to the moment they walk on stage. Your output is a speaker who has said the talk out loud to a real listener early enough to change it, fits the slot, and walks on knowing what the room and the questions will be like.

What this skill does not do:

- **Write the talk.** The talk is the speaker's own work. You review it against the promise it made; a speaker builds it with `samber/developer-relations-skills@tech-talk-outline` (sibling collection, see-also).
- **Logistics and care.** Packet, materials ladder, travel, recording consent, green room and the on-site tech check stay with `samber/dev-event-organizer-skills@event-speaker-experience`.
- **Proposal mentorship.** Help before submission belongs to `samber/dev-event-organizer-skills@event-cfp-design`.
- **Select or gate.** Acceptance is decided. Coaching never re-opens it (see Blockers).

## Ground rules

Load-bearing. Every later section assumes them.

- **Offer coaching to every accepted speaker, in the same words.** Never pick who gets it by guessing from a name, a photo or a first-timer flag. A targeted offer tells the speaker the organizer expects them to struggle, and it is declined by exactly the people it was meant for. Make the default rung opt-out ("every speaker gets a dry run slot"), so taking it costs nothing socially.
- **When you already know who is new**, use it only to order the work, for example earlier dry-run dates. Every contact after the offer goes to every speaker in the same words: one reminder to everyone who has not answered, never a follow-up only to first-timers.
- **Coach the talk against its own promise**: the accepted abstract, the talk time and the room. **Talk time** = the slot minus any Q&A minutes the slot includes; when the programme lists Q&A separately ("30 min plus 5 Q&A"), talk time is the 30. Use the good-talk text the committee scored against in `samber/dev-event-organizer-skills@event-talk-selection`. Never coach toward a house style.
- **Comment on the talk, never the person.** Feedback aimed at the self rather than the task is the kind most likely to lower performance (Kluger & DeNisi's 1996 meta-analysis: over a third of feedback interventions made performance worse).
- **Cap each round at three changes** (self-set), Blocking notes included, plus what to keep. A first-timer handed fifteen notes fixes none and remembers the count.
- **Get the first out-loud run early.** Talks fail on the stage because nobody heard them before the week of the event, not because the speaker lacked tips. Content changes stop at the content freeze (calendar step); after it, only timing and delivery.
- **Never coach identity-coded traits**: accent, pitch, "sound more confident", "be more assertive", dress, how much the speaker smiles. These notes push underrepresented speakers toward one presenter type and carry no fix. Moment-anchored audibility and pace notes stay allowed: "at minute 12 the back row lost you; use the mic" points at the room, not the person.

## Interview

Ask one question at a time, multiple-choice where possible, and skip any the user already answered. Questions 4-6 re-rank the coaching-depth menu: its rungs differ sharply in effort and time-to-effect.

1. How many accepted speakers, in which formats (lightning, talk, keynote, co-presented, remote or pre-recorded), how long is each slot and does it include Q&A, and how many weeks remain to the event?
2. Is this a community-run event (volunteer coaches) or a vendor or user conference (paid coaches, mandatory content or legal review possible)?
3. What did the acceptance email or the call already promise about support? Deliver that; never shrink it.
4. By what date must every talk be final: the slide deadline, the captioner hand-off, the print date?
5. One-off edition, or a recurring event where coached first-timers become next year's speakers and mentors?
6. Effort ceiling: who coaches, how many hours a week, and is there any budget line for a professional coach?
7. Which assets exist: past speakers willing to mentor, a rehearsal room or the real stage before doors, a video-call account, an accessible slide template?
8. Is the audience mixed (developers and non-developers), multilingual, or remote? Each changes the review checklist.
9. What Q&A format does each slot have: open mic, moderated, written questions, none?

## Workflow

1. **Read the acceptance packet and the good-talk text** - the accepted abstract per speaker, slot length, Q&A minutes, format. A talk is coached against these, so collect them first.
2. **Pick the coaching depth** from the menu below, re-ranked against Q4-Q7. Write down what every speaker gets by default and what is opt-in.
3. **Send the coaching offer** to every speaker in one wording: what they get by default, what they can ask for, two or three dry-run date options, and that opting out changes nothing about their slot. Send it before any individual reply to a speaker's draft, so that reply does not read as targeted help. Template in [references/offer-intake-and-mentor-brief.md](references/offer-intake-and-mentor-brief.md).
4. **Run intake** with the offer, as optional questions for everyone and required for mentor requests: the talk in two sentences, what worries them, what feedback they want and what they do not, access needs, language, time zone. Ask, never infer, first-time status. Group the dry runs from the date answers.
5. **Pair mentors** where the depth includes them. Match on what the speaker asked for (topic, format, language, time zone, and a shared identity only when the speaker requests it). Brief every mentor before the first contact with the same brief.
6. **Set the calendar** by working back from Q4: outline check, first out-loud run, slide and accessibility review, timed dry run, content freeze, stage walk-through. Default dates and the minimum viable program are in [references/coaching-calendar-and-dry-runs.md](references/coaching-calendar-and-dry-runs.md).
7. **Run each review with the feedback protocol** below. Same protocol for organizers, mentors and peers.
8. **Run the timed dry run**: uninterrupted, with a listener, against a visible clock set to the talk time. Pass = the run ends by about 90% of the talk time (self-set; a room, an introduction and applause add the rest). A solo run counts as practice, not as the gate. Over time means a cut list, never "talk faster". After the gate run, re-time any small change solo and out loud against the same mark; a structural change needs another listener run. Protocol in [references/coaching-calendar-and-dry-runs.md](references/coaching-calendar-and-dry-runs.md).
9. **Review the deck for accessibility** before the slide deadline, with the checklist in [references/slide-accessibility-review.md](references/slide-accessibility-review.md). Its Blocking items are the only slide notes that count as blocking.
10. **Prepare nerves and Q&A**: rehearse two hard questions out loud, agree the Q&A format and the host's role, and offer the room before doors open. See [references/nerves-and-qa.md](references/nerves-and-qa.md).
11. **Hand the stage tech check to `samber/dev-event-organizer-skills@event-speaker-experience`** and the timing signals to `samber/dev-event-organizer-skills@event-run-of-show`. Rehearse the speaker with the same signals the room will use.
12. **Close the loop**: one short debrief after the talk (what worked, what to try next time), and the coaching measures below. Relay audience ratings from `samber/dev-event-organizer-skills@event-feedback` with the same protocol: keeps first, at most three themes, never a raw score dump.

Show the user the offer text and the calendar before anything goes out. An offer worded for "speakers who need help" cannot be unsent.

If your harness has persistent memory, record per edition: who opted in, which rung each used, overruns on the day, and which coached speakers return. That record re-ranks next edition's menu.

## Coaching depth

What the program gives speakers above whatever the call already promised. Every speaker gets the **rehearsal kit** with the offer: a one-page guide with their dates, how to time a run, the accessibility Blocking items and the Q&A format. It is the floor, not a rung; nobody learns from a checklist that their joke lands flat. Ranking of what sits above it (default, not a law):

- effort (coach hours, coordination, recruiting): `professional speaking coach > paired mentor across milestones > one-to-one timed dry run > group dry-run session`
- value (talks that fit the slot, survive the room, and speakers who come back): `paired mentor across milestones == professional speaking coach > group dry-run session == one-to-one timed dry run`
- efficiency: `group dry-run session > one-to-one timed dry run > paired mentor across milestones > professional speaking coach`

- **First value tie**: genuine - both put one experienced listener on the same talk across several milestones. They differ in who pays, not in what the speaker gets.
- **Second value tie**: genuine too - both buy one listened, timed run with capped notes. The group adds peers who struggle in the same places; one-to-one adds privacy.

Re-rank against the interview, and say which answer moved what:

- Q4 under three weeks to the final date: delete the paired mentor (no milestones left to see), promote one-to-one runs, which schedule faster than a group.
- Q5 recurring edition, or Q7 past speakers willing to mentor: promote the paired mentor.
- Q6 budget line: promote the professional coach for the headline keynote only.

- **Group dry-run session** - the default rung, offered opt-out to every speaker: one facilitator, an evening or a video call, each talk run uninterrupted then answered with the Critical Response Process. Budget talk time plus about 20 minutes of feedback (10 for a lightning talk) and 5 minutes of changeover per speaker, so a 3-hour session holds three 30-minute talks or about eight lightning talks. Highest value per hour because one sitting gives several speakers a real listener, a real clock and the discovery that everyone struggles in the same places.
- **One-to-one timed dry run** - an organizer or volunteer listens to one full run and gives capped notes: talk time plus about 20 minutes of the listener's time. Move a speaker here when the group session clashes with their schedule, or when they ask for privacy.
- **Paired mentor across milestones** - the starved option: one mentor sees the outline, the slides and a dry run, about four to six mentor hours per speaker (self-set). It tops value and effort together, so efficiency never picks it, and mentor supply runs short (PyCon US's proposal mentorship reports about twice as many mentee requests as mentors; expect the same direction after acceptance, not the same ratio). Promote it for every speaker who asks, for first-time keynotes, and whenever Q5 says the edition recurs: a coached first-timer is next year's mentor.
- **Professional speaking coach** - paid sessions, usually for keynotes at vendor or user conferences. Promote it when the talk carries the event's headline promise and Q6 shows a budget line.
- **Deleted, not demoted: coaching offered only to speakers the organizer has labelled first-time or underrepresented.** It looks like the inclusive rung. It singles people out, gets declined, and leaves the confident speaker who has never run their talk aloud uncoached.

Vendor or user conferences (Q2) often add a mandatory content review for product claims or legal approval. Keep it separate from coaching, run by a different person, so a speaker never wonders whether their coach is also their censor.

## Feedback protocol

Pick the format by setting. They do not compete, so they are not ranked:

| Setting                             | Format                                                                                                                               | Why                                                              |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Group dry run                       | Critical Response Process (Liz Lerman): what was meaningful, the speaker's questions, neutral questions, opinions only by permission | Keeps a room of listeners from piling on; the speaker steers     |
| One listener, right after a run     | Observation, impact, request or question (Lara Hogan's equation; SBI is the same shape minus the request)                            | Fast, specific, lets the speaker find the fix                    |
| Written review of outline or slides | Labelled notes: **Blocking** / **Change** / **Optional**, plus **Keep**                                                              | Survives translation; nobody mistakes a blocker for a suggestion |

Every note, in every format:

- Points at a moment ("slide 7", "minute 12", "the demo hand-off"), not a trait.
- Names the effect on the room, then one concrete suggestion or one question.
- Comes with what to keep, stated as specifically as the changes. "Great talk" is not a keep. If you have only a description, not the talk or the deck, write no keep and no style note: ask for the run or the file.
- Respects the cap: three changes per round, Blocking included. Park the rest for the next round or drop them.

Worked good and bad notes, and the post-run script, are in [references/feedback-protocol.md](references/feedback-protocol.md).

Rationalizations coaches reach for, and why each is wrong:

| Rationalization                                                 | Why it is wrong                                                                                                             |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| "They asked for honest feedback, so I gave them everything."    | Honesty is about accuracy, not volume. Fifteen accurate notes still produce no fixes.                                       |
| "I'll sandwich the criticism between two compliments."          | Speakers learn to discount the bread. Give specific keeps and specific changes, labelled.                                   |
| "Telling them to sound more confident is just delivery advice." | It names a trait with no action, and it lands hardest on speakers already judged by their voice. Point at a moment instead. |
| "It is faster if I just rewrite these slides."                  | The speaker then presents a talk they do not own and cannot recover when it goes off script.                                |
| "Experienced speakers don't need the dry run."                  | Experience predicts comfort, not timing. Offer the same default; let them opt out.                                          |
| "It's the week before; one more structural change won't hurt."  | After the content freeze, a structural change is an unrehearsed talk. Cut, do not rebuild.                                  |

## Blockers

Coaching supports; it does not approve. A coach labels a note **Blocking** only when it is one of these:

- The run still exceeds the full talk time after the agreed cuts. Missing the 90% mark alone is a strong Change note, not a Blocking one.
- The deck fails a Blocking item in the accessibility checklist.

A Blocking note goes to the speaker first. Escalate to the program chair only if the speaker declines, or cannot fix it by the content freeze, and tell the speaker before you do. Everything else is a note the speaker may decline.

Content rules are not the coach's to enforce, so the coach never becomes the censor:

- **Code of conduct or the commercial-content rule**: tell the speaker which rule the passage may cross; pass it to the program chair, who decides, only if the passage stays. Harassment-grade content goes to the chair at once.
- **Employer clearance**: ask "is this cleared?" once, and leave it with the speaker.

## Failure modes

- **Coaching starts in the last week.** Nothing structural can change. Hold the first out-loud run at least four weeks out (self-set) or say plainly that this edition offers polish only.
- **Coaching dropped under load.** Book coach hours as named tasks in the calendar; if the hours vanish, tell speakers the rung changed rather than going silent.
- **Over time fixed by speed.** A rushed talk loses the room faster than a shorter one. Cut whole sections from the cut list.
- **Mentor rewrites the talk.** The mentor brief forbids it; re-brief or re-pair.
- **Rehearsal recordings kept or shared.** Record only with the speaker's yes, share with nobody, delete after the event.
- **Coach plays therapist.** Offer practice and the room; refer clinical anxiety to a professional. Never suggest medication.
- **Q&A left as open mic for a speaker who dreads it.** Propose a moderated format to whoever owns the schedule (see nerves-and-qa).
- **The run is a different talk from the abstract.** Not a blocker. Tell the speaker, then the schedule owner, and update the published abstract with the speaker's agreement.
- **A workshop coached like a talk.** Exercise timing, setup and helper ratios belong to `samber/dev-event-organizer-skills@workshop-program-design`.
- **A remote or pre-recorded talk rehearsed like a stage talk.** Run the dry run on the event's own video tool, set the recording deadline before D, and see `samber/dev-event-organizer-skills@virtual-event-production` for the production side.
- **Intake answers kept forever.** Access needs go, with the speaker's agreement, to whoever delivers them (the speaker contact in `samber/dev-event-organizer-skills@event-speaker-experience`); worries go only to the mentor. Delete both after the event.

## Measurement

The two gates are this skill's objective; everything else is self-set and only means something across editions.

- **Timed-run gate**: every speaker who took a dry run ends their last listener run by about 90% of the talk time, and any later content change is re-timed against the same mark. Iterate cuts until it does. Speakers who opted out are covered only by the day's timing signals and live cut list.
- **Accessibility gate**: every deck clears every Blocking item in the accessibility checklist before the slide deadline.
- **Overruns on the day** (self-set): count them; the target is zero.
- **Coaching usefulness** (self-set): one question to each coached speaker after their talk - "What in the coaching changed your talk?" - read the answers, not a score.
- **Return rate** (self-set, recurring editions only): coached first-timers who speak or mentor again within two editions.

## Invocation examples

- "We accepted 14 talks, six from first-time speakers. How do we support them without being patronising?"
- "A speaker ran 38 minutes in a 25-minute dry run. What do I tell her?"
- "I'm mentoring a speaker for our conference next month. How do I give feedback on her slides?"
- "Can we set up rehearsals for our meetup speakers with just two volunteers?"

Expected output: the coaching offer text, a dated calendar, the depth chosen with what every speaker gets and what is opt-in, mentor pairings if any, and for review requests, capped labelled notes in the protocol's format.

## References

- `samber/dev-event-organizer-skills@event-accessibility-inclusion` - the event-wide access provisions the deck review checks against.
- See also `samber/developer-relations-skills@developer-live-demo-design` (sibling collection) - the demo fallback ladder a coach checks exists.
