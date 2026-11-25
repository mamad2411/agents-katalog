---
name: save-learning
description: Use when you learned something durable — a decision, a hard-won lesson, a useful reference. Captures it into the memory wiki so it compounds.
---

# Save a Learning

Turn a one-time insight into permanent, reusable knowledge. Without this,
agents are amnesiac — they re-learn and re-break the same things forever.

## When to use

- A non-obvious **decision** was made (and why, and the alternatives).
- A **lesson** was learned the hard way (a bug, an incident, a surprise).
- A useful **reference** surfaced (an external system, doc, dashboard).
- The human says "remember this", "save that", "don't forget".

## Before you save — the filter

Ask: **is this surprising or non-obvious?**

- ✅ Save: "Vendor's weekend data is unreliable until D+3" — non-obvious, costly to relearn.
- ❌ Don't save: "the auth code is in auth.py" — read the code instead.
- ❌ Don't save: secrets, personal data, ephemeral session state.

If it's derivable from the code, git history, or the docs — don't save it.

## Steps

1. **Pick the type:** decision · lesson · reference · person
   (rules/memory-system.md).

2. **Write the page** at `memory/wiki/<type>/<slug>.md` with frontmatter:
   ```yaml
   ---
   name: <title>
   description: <one line — how you'd recognize this is relevant later>
   type: lesson
   created: <date>
   confidence: HIGH | MED | LOW
   tags: [<topic>]
   ---
   ```
   Body: what it is, why it matters, what to do about it. Keep it short.

3. **Run the privacy filter** — strip any secret / personal data before saving.

4. **Add one line to `memory/INDEX.md`** pointing at the new page.

5. **Append one line to `memory/log.md`:**
   `## [<date> <time>] <type> | <summary> | <path>`

6. If this **supersedes** an older fact, link them both ways and banner the old
   page (rules/memory-system.md) — don't silently delete.

## Result

Next session, the agent reads the index, sees the lesson, and doesn't repeat
the mistake. That's the compounding.
