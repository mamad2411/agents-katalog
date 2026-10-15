---
name: final-response
description: Use after code edits, config changes, refactors, bug fixes, test or
  command runs, or non-trivial analysis with decisions. Apply on the same turn, right
  before sending the final answer. Adds a short note on what changed and why. Skip
  pure Q&A and one-line status replies.
---

# Final Response

If you opened this skill, apply it on this turn — do not read it and defer. Run a
completion check, then attach a short note: what changed, the path taken, and why.
This is a finishing step, not optional prose polish. It runs *after* implementation
and verification — it does not replace them.

## When To Apply

Before sending a final response, check:

- Did files change?
- Did commands or tests run?
- Did I make an architecture, design, or implementation decision?
- Did I finish a bug fix, refactor, config change, or review?

If **yes** to any, add the note.

## Order With Other Skills

Use implementation, TDD, and verification skills **first**. Use this skill **last**,
immediately before the final answer.

## Skip Only When

- Pure Q&A — no change and no decision
- User explicitly asks for code-only or no summary
- The final answer is a one-line status response

## What To Cover

Drop any section with nothing to say.

- **Approach** — the route taken and why this one (1-2 sentences)
- **Changes** — concrete: files, functions, behaviors touched. Many changes -> bullet
  list; group by area if it helps the reader.
- **Reason** — the root cause or tradeoff behind the change
- **Notes** *(optional)* — risk, follow-up, known limitation

## How To Write It

Write like a person, not like an AI summary.

- Short sentences. State facts.
- Say what changed and why, directly. No padding.
- Drop empty adjectives — comprehensive, robust, seamless, deep, powerful.
- No filler openers — First, Moreover, In conclusion, It's worth noting.
- No rule-of-three lists unless each item earns its place.
- No em-dash chains. Don't symbolize what a simple change "represents".
- Keep code, terms, and proper nouns in their original form.

## Length

Length follows the work, not a fixed number.

- Small change -> one or two lines.
- Big refactor -> name every file and function you touched.
- The cap is on padding, not on lines. Every line must carry information.
- Don't collapse real changes to look terse. Don't pad to look thorough.

## Example

> Approach: reuse open DB connections via a pool instead of one per request.
> Changes: `db.ts` adds `Pool`; `handler.ts` switches to `pool.query`.
> Reason: connection handshake was the bottleneck under load. Pooling removes it.
> Notes: pool size fixed at 10 for now — revisit if we see waits.
