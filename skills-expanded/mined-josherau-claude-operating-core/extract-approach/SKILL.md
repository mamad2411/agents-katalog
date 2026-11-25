---
name: extract-approach
description: Reasoning recorder — fires automatically after cracking a HARD problem (multiple failed attempts, non-obvious insight, judgment call between viable options, or an invented quality bar). Captures HOW the problem was solved — problem shape, dead ends, the turning point, the transferable recipe — as one note in your learnings directory, so the reasoning survives the session and any model change. Do NOT invoke for routine work, mechanical fixes, or first-try solutions. Also use when the user says "extract that approach" or "write down how you did that."
---

# Extract Approach — the reasoning recorder

Every hard solve contains two products: the fix, and the *approach that found the fix*. The fix ships; the approach evaporates when the session ends. This skill saves the approach — the more valuable half — as a permanent note any future model reads before touching similar work.

**Why this exists:** frontier models get repriced and retired. An answer helps once; a written-down approach upgrades every answer after it, at any model tier. The recipe requires top-tier judgment to *author* but only ordinary intelligence to *follow*.

## Setup (one-time)

Pick a learnings directory in your knowledge base (e.g. `{KNOWLEDGE_BASE}/learnings/`) and keep a `## Learnings` index — one line per lesson — in a file your sessions always load (CLAUDE.md is the natural place). Everything below assumes those two locations exist; adjust paths to your setup.

## Trigger test (all three must hold)

1. **It was actually hard.** At least one of: multiple failed attempts before the solve; a non-obvious insight was the turning point; a judgment call between 2+ viable approaches; a quality bar or heuristic was invented on the spot.
2. **It will recur.** The problem *shape* (not the exact problem) will plausibly show up again in the user's work.
3. **The approach is transferable.** You can state a recipe someone else could follow without this session's context.

If any fail, don't write a note — noise kills the learnings system faster than gaps do. Routine bug fixes, config edits, and lookups never qualify.

**Timing:** capture immediately at solve time, while the dead ends are still in context — never batched to session end. Logging mistakes the moment they happen is the same discipline; batching loses the details that matter.

## What to capture

Write ONE file to `{KNOWLEDGE_BASE}/learnings/{kebab-case-slug}.md`. The format is: one-line summary, then **Problem shape**, **Why it mattered**, **How to apply**:

```markdown
{One-line summary: the transferable heuristic, stated so it stands alone in an index.}

**Problem shape:** {What class of problem this was — described abstractly enough that a future session pattern-matches it BEFORE knowing the solution. 1-2 sentences.}

**Why it mattered:** {What was at stake, what failed first and WHY each dead end failed — the dead ends are half the value; they prune a future model's search tree. Include the turning-point insight and what made it non-obvious.}

**How to apply:** {The recipe. Numbered steps a mid-tier model could follow cold: what to check first, what signal discriminates between causes, what order to try things, what to never do. If a quality bar was invented, state it as pass/fail criteria.}
```

Rules:
- **Recipe over narrative.** "Check X; if Y, the cause is Z" beats a story about the debugging session.
- **Dead ends are mandatory.** An approach note without what *didn't* work is a success story, not a map.
- **State the discriminating signal** — the observation that separated the winning hypothesis from the losers. That's usually the part only a strong model notices, and exactly what must be written down.
- **No session-specific residue.** A reader with zero conversation context must be able to follow it.

## Index it (not optional)

Add one line to the `## Learnings` index in the file your sessions always load, matching the existing style:

```markdown
- [{slug}](learnings/{slug}.md) — {one-line summary, compressed}
```

The index is what every future session actually loads; an unindexed note is invisible.

## Dedup check first

Before writing, grep the learnings directory for the topic. If an existing lesson covers the same problem shape, **update that file** (sharpen the recipe, add the new dead end) instead of creating a near-duplicate. Delete lessons this solve proved wrong, and remove their index lines.

## Scope notes

- Corrections and gotchas ("X doesn't work, do Y") still go through your normal learnings flow — this skill is specifically for *multi-step reasoning approaches* worth replaying.
- If the solve produced a reusable standard rather than a technique, put the checkable pass/fail criteria in a standards file and write a short learning that points at it.
- **Routing vs adjacent skills:** a whole-session retro skill reviews process; this skill is narrower — one hard solve → one recipe note, at solve time. They don't substitute for each other.
- **Enforcement is by CLAUDE.md instruction** (same class as review-panel) — there is no hook forcing it. Put the trigger text in your global CLAUDE.md; if it stops firing in practice, that's a compliance drift worth its own learning, not a config bug.
