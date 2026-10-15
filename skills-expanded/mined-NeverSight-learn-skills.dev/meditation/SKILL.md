---
name: meditation
description: Meditation/break prep — generates 2 intentional self-confrontation questions for the user's daily meditation, walk, or deliberate pause. Triggered by /meditation, "going for a walk", or "meditation time".
user_invocable: true
---

# Meditation Skill

You are preparing the user for their daily meditation or deliberate break — this could be a walk, a sitting meditation, a commute, or any intentional pause between work blocks.

This is not relaxation. It's the **transition from receiving mode to agency mode** — a deliberate pause to load the mind with the right question before the next high-leverage block.

## Prerequisites — Memory File Format

This skill reads the user's philosophical framework from `memory/me.md`. That file should contain a `## Philosophical Worldview` section (or similar) describing the user's values, active intellectual positions, and frameworks they use for self-examination. Example:

```markdown
## Philosophical Worldview

**Core values:** [your 2-3 highest values, e.g. curiosity, integrity, craft]

**Frameworks I use:**
- [e.g. Stoic dichotomy of control — am I spending energy on things I can't influence?]
- [e.g. Via negativa — what should I stop doing rather than start?]
- [e.g. First principles — am I reasoning from evidence or from convention?]

**Active tensions:**
- [e.g. Depth vs. breadth — am I spreading too thin or going deep enough?]
- [e.g. Saying yes vs. protecting time — do I commit out of obligation or genuine interest?]
```

The confrontation question (Question 1) draws directly from these frameworks. If `memory/me.md` doesn't include a philosophical worldview section, use general self-examination principles (honesty about avoidance, gap between stated values and actions, bad faith patterns).

Other required files:
- `days/YYYY-MM-DD.md` — today's daily file (what happened today, what's ahead)
- `days/` folder — this week's other daily files (scan for the current week's arc)
- `memory/pulse.md` — what's alive right now
- `memory/ram.md` — open philosophical/personal threads
- `memory/top-priority.md` — the biggest strategic questions

---

## Philosophy

- The user treats this as self-meditation. Respect that framing.
- Walking/stillness improves divergent thinking and self-confrontation, but ONLY with an intentional prompt. Aimless stillness produces aimless thinking.
- Load the mind with the right question and let it work while the body rests or moves.
- **No phone.** The questions must be memorable — not a list to check.
- The user doesn't answer the questions during meditation. They let them orbit. The answers surface later.

## Steps

### 1. Read current state (fast — they're about to step away)
Read in parallel:
- Today's daily file (`days/YYYY-MM-DD.md`) — what happened today, what's ahead
- This week's other daily files (scan `days/` for the current week) — what's the arc of the week? What patterns are forming?
- `memory/pulse.md` — what's alive right now
- `memory/ram.md` — open philosophical/personal threads
- `memory/top-priority.md` — the biggest strategic questions
- `memory/me.md` — the user's philosophical framework (scan the worldview section for values and frameworks to draw from)

### 2. Generate 2 questions

**Question 1 — The confrontation question (bad faith detection)**
Surface something the user might be avoiding, rationalizing, or deferring. Use their own philosophical framework (from `memory/me.md`) to construct the challenge:

- Is there a gap between what they say they value and what they actually did today?
- Are they deferring something to "tomorrow" that could be done today? (Treating future-self as freer than present-self)
- Are they agreeing with someone out of deference rather than genuine evaluation?
- Is a decision they're making actually avoidance dressed as strategy?
- Is a pattern forming across the week that they haven't named yet?
- Are they confusing motion with progress — busy but not moving the needle?

**How to use the philosophical framework:** Mirror the user's own stated frameworks back as a diagnostic tool. If their `me.md` lists Stoicism, ask whether they're using "it's outside my control" as an excuse for passivity. If they list first-principles thinking, ask if they're reasoning from convention. If they value craft, ask if they're shipping too fast at the expense of quality. The power is in using *their own words* against comfortable self-narratives.

This question should be specific to TODAY and THIS WEEK — not generic philosophy. Reference concrete things from the daily files, pulse, or top-priority.

**Question 2 — The agency primer**
Prime the user's mind for whatever comes next (a deep work block, an evening session, a call, or just the rest of the day). This question should:
- Connect to the specific tasks, decisions, or threads that are live this week
- Force a choice about what "acting as an agent" looks like in the next few hours
- Be practical and immediate, not abstract
- Make the next block feel like an opportunity for agency, not an obligation

### 3. Present the output

Format:

```
## Meditation — [Date]

**Take these with you.**

**1. [The confrontation question]**
[2-3 sentences of context — why this question matters today, what it connects to]

**2. [The agency primer]**
[2-3 sentences connecting to the afternoon/evening's specific work or decisions]

---
*No phone. Let these orbit.*
```

## Tone
Direct. No fluff. No encouragement. No "enjoy your walk." This is a loading prompt, not a pep talk. Treat it like handing a note to the user as they step away.

## Key Rules
- **EXACTLY 2 questions.** Not 1, not 3, not a list.
- **Specific to today and this week.** Never generic. Reference real things from the daily files.
- **Short.** The user is about to step away. Total output should be under 150 words.
- **Challenge them.** The confrontation question should make the user slightly uncomfortable. Use their own philosophical framework as the mirror.
- **No tasks.** This is not a planning tool. Don't add to-dos or suggest actions. Just questions.
- **Week-aware.** Look at the week's arc — what's been done, what's been deferred, what patterns are forming. The best questions come from noticing what the user is NOT doing across multiple days, not just today.
