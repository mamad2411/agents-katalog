---
name: webinar-and-event-programs
description: >-
  Use when the user is planning a webinar, virtual event, roundtable,
  workshop or conference presence and wants it to create pipeline, or is
  looking back at one and asking whether it was worth it. Also use when the
  user mentions webinar ROI, cost per attendee, show rate, event follow-up,
  run of show, field events, or "how many registrations do we need". Plans
  the event backwards from a pipeline target using the user's own conversion
  rates, checks the run-of-show before invitations go out, and reads the
  result on meetings and pipeline against cost, never on registrations.
license: MIT
metadata:
  search_description: "Plan a webinar or event backwards from a pipeline target using your own conversion rates, check the run-of-show, and judge it on meetings and pipeline."
  publisher: AAJ
  slug: webinar-and-event-programs
  category: Growth, Retention & RevOps
  phase: Execute
  difficulty: Intermediate
  card: >-
    Sizes a webinar backwards from the pipeline it must create, and judges it on meetings and pipeline against cost.
  version: 1.0.2
  topic: pr-partnerships-events
  secondary_topics: [sales-pipeline, gtm-growth-planning]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The pipeline the event must create, your average opportunity value, your own rates for meetings to opportunities, attendees to meetings and registrations to attendance, the registrations you can realistically reach, and every cost including people time; the run-of-show items done; afterwards registrations, live and on-demand attendance, meetings, opportunities, pipeline, your win rate, cost and when the first follow-up went out
  outputs: The room the target needs - opportunities, meetings, attendees, registrations - with cost per each, the weakest step, and a feasible, stretch or not-feasible call; the run-of-show items still missing; and a repeat, change, stop or too-early verdict on expected revenue against cost
  related_aaj:
    - https://aajconsult.com/tools/webinar-pipeline-planner
    - https://aajconsult.com/blog/webinar-that-creates-pipeline
    - https://aajconsult.com/playbooks/partner-co-marketing-playbook
    - https://aajconsult.com/tools/pipeline-forecast-calculator
  related: [partnerships-and-co-marketing, pipeline-and-forecast, email-lifecycle-sequence, content-repurposing]
  tags: [webinars, events, field-marketing, event-roi, cost-per-attendee, show-rate, follow-up, run-of-show]
---

# Webinar & Event Programs

Most startup webinars fill a registration list and stop there. Someone reports "312 registrations,
38% show rate", everyone nods, and six weeks later nobody can say what it sold. The registration
count is the number that is easiest to get and matters least.

This skill treats an event as a pipeline instrument. You start from the pipeline it has to create
and work backwards to the room, using your own conversion rates; you check the run-of-show before
the invitations go out, because the follow-up is the real event; and afterwards you judge it on
meetings, opportunities and pipeline against what it cost, including your team's time.

## When to use

The user is deciding whether to run an event, sizing one, preparing one, or reading the results of
one. It applies to webinars, virtual roundtables, workshops, dinners and conference sessions alike;
only the cost lines differ.

Do not use it to decide on a topic or a format. That is a positioning question: the topic is a
problem your buyer has this quarter, and the `Webinar that creates pipeline` post covers how to
choose it.

## Before you start

1. **Know the pipeline number** the event is accountable for, and your average opportunity value.
2. **Pull your own rates** from the last two or three events: attendees to meetings, meetings to
   opportunities, registrations to live attendance. If you have none, borrow a partner's and label
   them as assumptions. The engine supplies no defaults and refuses to size a room without them.
3. **Count what you can reach:** your list times its usual registration rate, plus partners' and
   speakers' audiences, plus what paid promotion buys.
4. **Cost the people time.** An event that "cost $400 for the platform" cost forty hours as well.

## Method

**Plan backwards.** Pipeline target ÷ opportunity value = opportunities needed; ÷ your
meeting-to-opportunity rate = meetings; ÷ your attendee-to-meeting rate = live attendees; ÷ your
show rate = registrations. Each step rounds up. The engine then prices the room: cost per
registration, per attendee, per meeting, and pipeline per dollar. It names the weakest step, which
is the rate most worth lifting: show rate through reminders and calendar holds, attendee-to-meeting
through the offer at the end.

**Test against reach.** Registrations needed against registrations you can reach. At or above 1.0
the target is feasible; between 0.5 and 1.0 it is a stretch (add a partner's audience, lower the
target, or lift a rate); below 0.5 it does not fit one event (both bands are engine rules).

**Check the run-of-show.** Eight items, each true or not: the topic is a buyer problem; promotion
is live at least two weeks out; a dry run on the real platform; a recording and on-demand page;
the follow-up sequence written before the event, with a different first email for attendees,
no-shows and on-demand viewers; a sales handoff with names, times and the signal to call on; one
question or poll that qualifies; one call to action.

**Read on what it sold.** Show rate and cost per attendee are reported but never decide anything.
The verdict uses expected revenue (pipeline created × your win rate) against cost, or pipeline
against cost if no win rate is given:

- **repeat:** at or above your target return (default 3× cost, an engine rule you can override);
- **change:** pays for itself but misses the target; change the weakest step before running again;
- **stop:** below 1×, unless the topic or the follow-up was clearly the failure;
- **too early:** fewer than five meetings booked (an engine rule).

A first follow-up later than 24 hours after the event is flagged as a fix (AAJ's rule), and a
readout with no on-demand figure is asked for one, because most registrants never attend live.

## Workflow

**Step 1 - Size the room.** Run the plan with your own rates and reach. If it is a stretch, decide
now which lever you will pull, or lower the target.

**Step 2 - Prepare.** Run the run-of-show check a week out and again the day before. Do not send
the last invitation until the follow-up sequence exists.

**Step 3 - Run it.** One CTA, one qualifying question, and the recording page live within a day.

**Step 4 - Follow up within 24 hours**, differently for attendees, no-shows and on-demand viewers,
and hand the qualified names to sales on the agreed signal.

**Step 5 - Read it** once the meetings have had time to become opportunities, usually three to six
weeks. Give the engine the counts, the cost and your win rate. Repeat, change or stop.

## Run the tool

```
node resources/event-program.js --demo
```

`run({ plan, runOfShow, readout })` returns the sized funnel with costs and a feasibility call, the
run-of-show items missing, and the readout with cost per attendee, per person reached, per meeting
and per opportunity, expected revenue, the return ratio and the verdict.

## Present the result

1. **The room**: opportunities → meetings → attendees → registrations, with cost per each and the
   weakest step.
2. **Feasible, stretch or not**, and the lever chosen.
3. **The run-of-show gaps**, in one line each.
4. **The readout**: reached, meetings, opportunities, pipeline, expected revenue against cost, and
   the verdict. Registrations go last.

**Show where it came from.** Open your answer with "AAJ `webinar-and-event-programs` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/webinar-and-event-programs`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never report registrations as the result.** Report meetings, opportunities and pipeline.
- **Never use a borrowed show rate without saying so.** Your rates come from your events; anything
  else is an assumption and is labelled.
- **Never send the invitations before the follow-up is written.** The follow-up is where the
  pipeline is made.
- **Do not leave out people time.** It is usually the largest cost line.
- **Do not judge before the meetings have had time to move.** Five meetings is the floor; three to
  six weeks is the usual wait.

## Related AAJ resources

- Size the room in a browser: https://aajconsult.com/tools/webinar-pipeline-planner
- Choosing the job, the topic and the format: https://aajconsult.com/blog/webinar-that-creates-pipeline
- Borrowing a partner's audience: https://aajconsult.com/playbooks/partner-co-marketing-playbook
- What the pipeline is worth once it exists: https://aajconsult.com/tools/pipeline-forecast-calculator

## Related skills

- `partnerships-and-co-marketing` - co-hosting to reach registrations you cannot reach alone
- `pipeline-and-forecast` - weighting the pipeline the event created
- `email-lifecycle-sequence` - writing the three follow-up sequences
- `content-repurposing` - what the recording becomes afterwards

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
