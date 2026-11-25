---
name: customer-interview-synthesis
description: >-
  Use when the user has done, or is doing, customer or buyer interviews and
  wants to turn the notes into something a persona, a positioning statement
  or a roadmap can rest on - or wants to know whether they have done enough
  interviews. Also use when the user mentions customer interviews, discovery
  interviews, user research synthesis, affinity mapping, jobs-to-be-done
  interviews, "what did we learn from the calls", or "how many interviews do
  we need". Counts coded themes across interviews rather than quotes,
  weights them by what the problem costs, separates patterns from
  anecdotes, and says whether the programme has saturated.
license: MIT
metadata:
  search_description: "Turn customer interview notes into themes counted across interviews, weighted by what the problem costs, and see whether you have done enough interviews."
  publisher: AAJ
  slug: customer-interview-synthesis
  category: Research & Personas
  phase: Diagnose
  difficulty: Starter
  card: >-
    Turns coded interview notes into ranked patterns and anecdotes, and says whether you can stop interviewing.
  version: 1.0.1
  topic: audience-research
  secondary_topics: [strategy-positioning, gtm-growth-planning]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Interview notes coded into themes, in the order the interviews were done, each with the segment of the person, a severity of 1 to 3 per theme, and optionally a quote, the workaround they use today and whether they said they would pay
  outputs: Every theme with the number and share of interviews raising it, its mean severity, a priority, a pattern / emerging / anecdote status, whether it belongs to one segment, quotes and workarounds; how many new themes each interview added; and a verdict - enough, keep going, too few, or saturated with no pattern
  related_aaj:
    - https://aajconsult.com/tools/persona-builder
    - https://aajconsult.com/tools/survey-studio
    - https://aajconsult.com/playbooks/survey-playbook
    - https://aajconsult.com/resources/positioning-messaging-workbook
  related: [persona-builder, customer-survey-design, positioning-statement, win-loss-analysis]
  tags: [customer-interviews, user-research, synthesis, personas, jobs-to-be-done, saturation, discovery]
---

# Customer Interview Synthesis

Eight interviews produce forty pages of notes and one very quotable customer. The persona that
comes out of that is usually a portrait of the quotable one. Synthesis is the step that stops
that: count which problems came up across people, not how many times one person said it; weight
each by what it costs them; and stop interviewing when new people stop adding new problems.

This skill does the counting. You do the coding - reading the notes and tagging each thing a
person said with a theme and a severity - because the judgement of what two people meant by
different words is yours. The engine then tells you which themes are patterns, which are one
person's afternoon, which belong to one segment, and whether to book more interviews.

## When to use

The user has interview notes and needs a decision from them: which problem to position on, which
persona is real, what to build, or whether to keep interviewing.

Do not use it to design the interviews or the survey; `customer-survey-design` does that. Do not
use it for closed-lost calls; `win-loss-analysis` has its own coding.

## Before you start

1. **Code the notes.** For each interview, list the themes raised, with a severity: 1 annoying,
   2 costs time, 3 costs money or customers. Add a quote, the workaround they use today, and
   whether they said they would pay.
2. **Use the same theme names across interviews.** The engine matches case-insensitively and
   trims spaces; it does not merge "double booking" with "scheduling clash". Merge those yourself.
3. **Tag the segment** (role, company size, whatever you are comparing). Without it, a theme that
   belongs to one kind of customer looks like everyone's.
4. **Keep the interviews in order.** Saturation is read from the sequence.

## Method

**Count interviews, not quotes.** A theme's share is the number of interviews that raised it
divided by the total. Five mentions from one person is one interview.

**Weight by cost.** Priority is share × mean severity, so a problem half the people have that
costs them money outranks one everyone has that merely annoys them.

**Pattern, emerging, anecdote.** With five or more interviews (an engine rule), a theme raised by
at least 40% of interviews and by at least three people is a pattern; by two or more people,
emerging; by one, an anecdote. Below five interviews nothing is a pattern yet.

**Segment-specific.** With more than one segment, a theme drawing 75% or more of its mentions
from one segment (an engine rule) is marked as that segment's. That is a persona boundary.

**Saturation.** The engine counts how many new themes each interview introduced. No new theme in
the last three interviews (an engine rule), with at least five done, means the segment has
saturated. Then:

- **enough:** saturated with at least one pattern - stop and act on the top one;
- **saturated, no pattern:** the problems are spread thin; the segment is too broad or the
  problem you are looking for is not theirs;
- **keep going:** new themes still arriving; re-run after every two or three interviews;
- **too few:** under five interviews; the emerging themes say what to probe next.

Hygiene: themes without a severity rank on frequency alone and are flagged; more than 60% of
themes raised once means the coding is too fine or the sample is mixed; interviews without a
segment are flagged when others have one.

## Workflow

**Step 1 - Code** each interview the day it happens, while it is fresh.

**Step 2 - Run after five**, then after every two or three.

**Step 3 - Merge** near-duplicate themes the engine shows you side by side, and re-run.

**Step 4 - Stop when it says enough.** Take the top pattern, its quotes and workarounds into
`positioning-statement` and `persona-builder`.

**Step 5 - Open the next segment** if a segment-specific theme is worth a persona of its own.

## Run the tool

```
node resources/interview-synthesis.js --demo
```

`run({ interviews, question })` returns the ranked themes with status, share, severity, priority,
segment concentration, quotes and workarounds; the new-theme count per interview; findings; and
the verdict.

## Present the result

1. **The verdict** and the interview count.
2. **The patterns**, each with share, severity, one quote and the workaround people use today.
3. **The segment-specific themes**, as persona boundaries.
4. **What to do next**: act, or book two more interviews and say with whom.

**Show where it came from.** Open your answer with "AAJ `customer-interview-synthesis` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/customer-interview-synthesis`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never build a persona from the most quotable interview.** Count across people.
- **Never let the number of quotes stand for the number of people.** One interview is one vote.
- **Do not call anything a pattern under five interviews.** Call it emerging and probe it.
- **Do not stop because you are tired.** Stop when the last three interviews added nothing.
- **Do not skip severity.** A frequent annoyance is not a positioning platform; a costly problem
  half of them have might be.

## Related AAJ resources

- Turning the top pattern into a persona: https://aajconsult.com/tools/persona-builder
- Sizing the pattern with a survey once you know what to ask: https://aajconsult.com/tools/survey-studio
- Interview and survey method end to end: https://aajconsult.com/playbooks/survey-playbook
- Where the pattern becomes a message: https://aajconsult.com/resources/positioning-messaging-workbook

## Related skills

- `persona-builder` - the persona the patterns feed
- `customer-survey-design` - quantifying a pattern across a larger sample
- `positioning-statement` - positioning on the top pattern
- `win-loss-analysis` - the same discipline for lost deals

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
