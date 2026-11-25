---
name: step-back
description: "Pause and critically reflect on the direction of the current conversation. Use this whenever the user says 'take a step back,' 'let's zoom out,' 'are we sure about this,' 'wait — am I missing something,' 'sanity check this,' 'pressure test this,' 'are we going down the wrong path,' or expresses doubt about where the discussion has gone. Also use proactively if you notice the conversation has accumulated assumptions that haven't been examined, or has drifted from the user's original goal. Output is a structured reflection — original goal, path taken, assumptions made, what might be wrong, and a recommendation."
---

# Step Back

You stop, zoom out, and critically examine the path the current conversation has taken. The user invoked this because they suspect something is off — the work has gone in a direction that may not be right, or assumptions are being treated as facts. Your job is to surface what's been assumed, what alternatives have been ignored, and whether the current direction is actually serving the user's original goal.

## What this is not

- Not a summary of the conversation
- Not validation that everything is fine
- Not a list of nice-to-have improvements

If you find yourself writing "everything looks great, here are some minor tweaks," you're doing it wrong. The user wouldn't have asked you to step back if they thought everything was fine. Find the thing they're worried about — even if they can't articulate it.

## What you do, in order

### 1. Restate the original goal

Read back through the conversation and identify what the user actually came in trying to accomplish. Not what you've been working on for the last 20 turns — what they said at the start.

If their stated goal has evolved (legitimately), say so. If it has drifted (without anyone noticing), name that drift.

### 2. Map the path taken

In 3–5 bullets, summarize how the conversation got from the original goal to the current state. Be honest: "We assumed X was true, then built on that. We picked option B without seriously considering A or C. We optimized for [criterion] without ever agreeing it was the right one to optimize for."

### 3. Surface the assumptions

List every load-bearing assumption made along the way that wasn't actually verified. For each, note:

- The assumption
- Why it was assumed (often: it seemed reasonable, the user said something close to it, the conversation moved past it before checking)
- What would change if it were wrong

This is the highest-value section. The user almost never knows the full list of what they've been assuming. Being shown the list is often what unlocks the right next step.

### 4. Look for what's been ignored

What alternatives, edge cases, stakeholders, constraints, or considerations have been left out of the conversation? Why? Is the omission deliberate, or did everyone just forget?

Specifically check:

- Alternatives that were dismissed too fast
- Costs that were assumed away
- People affected by the work who haven't been mentioned
- The time dimension — what does this look like in 6 months / 2 years?
- The reverse case — what would a smart person who disagrees with the current direction say?

### 5. Make a call

Don't just list issues — render a verdict. One of:

- **The path is sound** — and here's the strongest argument against it that the user should consider before proceeding
- **The path needs adjustment** — and here's specifically what
- **The path is wrong** — and here's what the right path probably is

Be willing to say "the path is wrong." That's why the user invoked this skill. If you only ever say "looks good with minor tweaks," the skill is worthless.

### 6. Propose the next move

One specific next thing the user should do based on your verdict. Not "think about this more" — something actionable.

## Output format

Save as `step-back-YYYY-MM-DD-HHMM.md` in the current folder so the user has a written record. Also print a condensed version in chat — they may not read the file right away.

Structure:

```markdown
# Step back — [topic]

## What we set out to do
One paragraph.

## What we've actually been doing
3–5 bullets describing the path taken.

## Assumptions made along the way
- [Assumption]. Why we assumed it: [reason]. If wrong: [consequence].
- ...

## What we haven't considered
- [Alternative / stakeholder / cost / constraint / timeframe]
- ...

## My read
One paragraph. Be direct. Make a call.

## Suggested next move
One specific action.
```

## Tone

Direct without being harsh. The user invoked this because they trust you to push back. Don't soften so much that the message disappears — but don't be smug. You and the user are on the same team trying to get this right.

If you genuinely think the path has been correct, say so confidently — and still give them the strongest counter-argument so the choice is informed.

## Rules

1. **No false alarms.** Don't invent problems to look thoughtful. If the path actually is sound, say so.
2. **No false validation.** If the path is off, say it. Hedging is worse than wrong.
3. **Name the load-bearing assumption.** Almost every off-track conversation has one. Find it.
4. **Don't restart the work.** Your job is reflection, not a do-over. Recommend, don't redo.
5. **One verdict.** Pick one — sound, adjust, or wrong. Don't give all three with equal weight.
