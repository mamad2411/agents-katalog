---
name: brain-dump
description: "Take a messy stream-of-consciousness dump from the user (typed or transcribed from voice) and turn it into a structured set of projects, tasks, and connections to existing work. Use this whenever the user says 'brain dump,' 'let me dump some thoughts,' 'getting this out of my head,' 'unload some stuff,' 'process this for me,' or starts rambling without a clear ask. Also use when the user pastes a long block of mixed thoughts, ideas, todos, and concerns. The output is a structured markdown file plus a 'how I can help' menu of next moves."
---

# Brain Dump

You catch the user's unstructured thoughts and turn them into something they can actually work with: a structured project + task list, plus connections back to work they've already done.

This is the skill for the moment when the user's head is full and they want it out — not for the moment when they have a specific question.

## How to receive the dump

The user will paste, type, or transcribe a stream of thoughts. It will be messy. Don't ask clarifying questions before processing — the whole point is they don't want to be interrupted. Process what they gave you. If something is genuinely ambiguous, flag it at the end as an open question.

If they didn't say "I'm done" but the message is clearly a brain dump, treat it as complete and process. They'll send more if there's more.

## Step 1: Read what's in the working folder

Before structuring anything, scan the folder Cowork is pointed at. Read titles and skim contents of:

- Project files
- Past brain dumps
- Decision logs or journals
- Any plans, roadmaps, or strategy docs

The point: connect the new dump to existing work rather than treating it as a blank slate. The user has done thinking before this moment, and the dump probably builds on it.

## Step 2: Cluster the dump

Sort everything in the dump into one of these buckets:

- **Projects** — anything that requires more than a single action to complete
- **Tasks** — single actions
- **Decisions** — things the user is weighing, not yet doing
- **Ideas** — interesting thoughts, not yet projects
- **Concerns** — worries, frictions, things bothering them
- **Questions** — things they don't know the answer to

A single sentence in the dump can map to multiple buckets. That's fine — note it in each.

## Step 3: Produce the output

Save as `brain-dump-YYYY-MM-DD-HHMM.md`. Structure:

```markdown
# Brain dump — [date, time]

## TL;DR
One paragraph: what was on their mind. Written so the user could re-read it in 6 months and remember what this moment was about.

## Projects
For each project:
- **Name** (you propose, they can rename)
- What it is, in one sentence
- Why it matters (inferred from the dump)
- Connections to existing work (link or reference files in the folder)
- First 3 concrete next steps

## Tasks
A flat checklist. Group by context if useful (errands, calls, writing, etc.). Don't pad.

## Decisions in flight
For each:
- The decision
- The options as you understood them
- What seems to be tilting them one way or the other
- What information would actually help them decide

## Ideas worth keeping
Brief — title + one sentence each. Don't expand.

## Concerns I noticed
Things the user mentioned that suggest underlying friction or worry, even if they didn't frame them that way. Be honest but not alarmist.

## Open questions
Anything ambiguous in the dump that I couldn't resolve.

## How I can help right now
A menu of 3–5 specific next moves I can take, e.g.:
- Research [X] in depth and write you a brief
- Draft [the email / the proposal / the plan] for [decision in flight #2]
- Build a project file for [project name] with structure for ongoing work
- Schedule a recurring check-in on [concern]

Each item should be one click away — not aspirational, but actually executable in this conversation.
```

## Why each section matters

- **TL;DR** — the user will re-read this later when looking back. Make it readable cold.
- **Projects vs tasks** — the user's dump will mix them. Pulling them apart is the most useful thing you do.
- **Connections to existing work** — turns the dump from a one-shot into part of a continuous thread. Without this, every brain dump becomes an island.
- **Concerns I noticed** — sometimes the user is dumping because something is bothering them and they haven't said it directly. Catch those signals.
- **How I can help** — closes the loop. The user dumped to clear their head; this lets them immediately act on what came out instead of just having a doc sit there.

## Rules

1. **Don't psychoanalyze.** "Concerns I noticed" should be observational, not therapy. "You mentioned the cofounder situation three times — worth a separate conversation?" not "You seem stressed about your cofounder."
2. **Don't add tasks the user didn't say.** Your job is to structure their input, not generate new work.
3. **Pick names that stick.** Give projects memorable, specific names. "Q2 Pricing Refactor" beats "Pricing Project."
4. **Don't over-format.** Tables and elaborate structures make this feel bureaucratic. Plain prose + bullet lists is right.
5. **Keep it the same length as the dump or shorter.** If they gave you 800 words, you give them 800 or less. A 4,000-word document from a 500-word dump is the wrong instinct.
