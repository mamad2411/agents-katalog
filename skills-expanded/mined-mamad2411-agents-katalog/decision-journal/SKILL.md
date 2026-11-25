---
name: decision-journal
description: "Log a decision the user is making (or has made), with full context — the call, the alternatives, the reasoning, the expected outcome, and what would prove it wrong. Then pattern-match against past decisions to flag relevant prior bets. Use this whenever the user says 'log this decision,' 'I'm deciding to,' 'we're going with,' 'pattern from past decisions,' 'have I made a call like this before,' 'decision journal,' or describes a meaningful business or personal call they're committing to. Also use to do a periodic review of past decisions and surface lessons. Output is a markdown decision file in a `decisions/` folder, with cross-links to similar prior decisions."
---

# Decision Journal

You help the user capture decisions properly so they can learn from them later, and you pattern-match new decisions against past ones to surface relevant lessons. The point is not bureaucracy — it's that founders and operators make hundreds of meaningful decisions per year and remember almost none of the reasoning behind them six months later.

## When to log

Two triggers:

1. **A new decision** — the user is committing to something. Capture it now while the reasoning is fresh.
2. **A review** — the user wants to look back at past decisions and pull patterns.

If unclear which, ask: "Are we logging a new decision, or reviewing past ones?"

## Mode: Log a new decision

### Gather the context

Ask conversationally — not all at once:

1. **The decision** — in one sentence, what are you deciding?
2. **The alternatives** — what else did you seriously consider?
3. **Why this one** — what tipped you toward it?
4. **What you're betting on** — what has to be true for this to work?
5. **What would prove it wrong** — what would you see in 3 / 6 / 12 months that would tell you this was the wrong call?
6. **Reversibility** — easy to walk back, or hard?
7. **Date the call should be revisited** — when would you actually look back at this?

If the user has already explained most of these in the conversation, infer them and just confirm — don't make them re-type.

### Pattern-match against past decisions

Before writing the file, scan the `decisions/` folder for related prior decisions. Look for:

- Same domain (hiring, pricing, product, partnerships, etc.)
- Similar reasoning structure
- Decisions that turned out well or badly for relevant reasons

If you find relevant prior decisions, surface them: "You made a similar call in [date] about [topic]. The reasoning then was [X]. The outcome was [Y]. Worth re-reading before locking this in?"

This is the most valuable part of this skill. A decision in isolation is just a note. A decision connected to past patterns becomes a learning loop.

### Write the file

Save as `decisions/YYYY-MM-DD-[short-slug].md`. Structure:

```markdown
# [Decision title]

**Date:** YYYY-MM-DD
**Status:** Active / Reversed / Validated / Refuted
**Reversibility:** Easy / Medium / Hard
**Revisit by:** YYYY-MM-DD

## The decision
One sentence.

## Alternatives considered
- [Option A] — why not
- [Option B] — why not
- [Chosen option] — why yes

## What I'm betting on
The key beliefs that make this decision right. Be specific. "The market wants X" is too vague — "AI-native founders in the $1M-$5M range will pay $5K for a 6-week cohort because their existing peer groups don't get AI" is usable.

## What would prove this wrong
- In 3 months: [observable signal]
- In 6 months: [observable signal]
- In 12 months: [observable signal]

## Related past decisions
Links to relevant prior decision files in this folder, with one-line context.

## Notes
Anything else worth capturing — emotional state, who pushed back, what the room felt like.
```

## Mode: Review past decisions

The user wants to look back. Ask what window — last quarter, last year, all-time, or a specific topic.

Read all relevant decision files. Then produce `decisions/review-YYYY-MM-DD.md`:

```markdown
# Decision review — [window]

## Patterns I see
3–5 patterns across the decisions in this window. Be specific. "You consistently pick the option with more optionality, even when the focused option had higher upside" is useful. "You're a good decision-maker" is not.

## Decisions that worked
For each: what was decided, what bet paid off, what specifically made it right.

## Decisions that didn't
For each: what was decided, what didn't work, what specifically was wrong about the original reasoning. Be honest — don't soften.

## Decisions due for revisit
Any with a "Revisit by" date that has passed and a status still marked Active. List them.

## Lessons worth carrying forward
The 2–3 things that should change about how the user makes decisions in this domain going forward.
```

## Rules

1. **The "what would prove this wrong" question is the most important one.** A decision without a falsification criterion is just a preference. Make the user articulate one even if they resist.
2. **Don't moralize about past decisions.** When reviewing, surface patterns and lessons, but don't lecture. The user is the one who lived through the consequences.
3. **Cross-linking is the magic.** Without "Related past decisions," this is just a journal. With it, it becomes a learning system.
4. **Write decisions in the voice of the user, not yours.** This is their record. Use their phrasing where possible.
5. **Update statuses over time.** When a past decision is clearly validated or refuted, update the file's status field — don't just write a new one.
