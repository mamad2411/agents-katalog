---
name: no-slop
description: MANDATORY before declaring prose "done" or ending a turn after writing a README, doc, blog post, comment, or any .md/.mdx/.txt/.rst. Use whenever you write or edit prose and are tempted to reach for an AI-tell cliché — "delve into", "it's worth noting that", "a testament to", "navigate the complexities", "rich tapestry", "in today's fast-paced world", "unlock the full potential", "seamlessly integrate", "elevate your", or a pile-up of decorative em-dashes. Forces you to cut the tell and say the thing plainly. Triggers on "make it sound better", "polish this copy", "write the intro", "draft the README", "punch up the wording", "add a conclusion".
---

# No Slop

**"Delve into" is not writing. It's the smell of a model trying to sound like it wrote something.**

The clichés below are AI tells: phrases that almost never appear in good human prose but show up constantly in generated text. They add no information. They cost the reader trust the moment they're spotted. Cutting them is free — the sentence underneath is always shorter and clearer.

## The rule

> **Say the thing plainly.** If a phrase decorates rather than informs, delete it. One idea per sentence. No throat-clearing.

## The tells (cut on sight)

- **Throat-clearing:** "it's worth noting that", "needless to say", "it goes without saying", "first and foremost", "when it comes to", "at the end of the day", "in conclusion,"
- **Stock openers:** "in today's fast-paced world", "in today's digital age", "in the modern era", "in the realm of", "the world of"
- **Decorative verbs:** "delve into", "dive deep into", "let's dive in", "navigate the complexities", "navigating the landscape", "embark on a journey"
- **Marketing slop:** "unlock the full potential", "unleash the power", "a game-changer", "elevate your", "seamlessly integrate", "seamless experience", "robust and scalable", "ever-evolving"
- **Faux-literary:** "rich tapestry", "a testament to", "underscores the importance of"
- **Transition-word soup:** "furthermore" *and* "moreover" stacked in the same passage
- **Em-dash pile-ups:** three or more em-dashes crammed into one short paragraph — a model tic, not emphasis

## Step 1 — Find the tell

When a phrase feels like it's there to sound impressive rather than to carry meaning, it's a tell. Read the sentence and ask: *what is this actually saying?* Usually the decoration wraps a single plain claim.

## Step 2 — Cut it, keep the meaning

Replace the cliché with the plain thing underneath. The rewrite is almost always shorter:

- "It's worth noting that the API is rate-limited." → "The API is rate-limited."
- "This library lets you seamlessly integrate payments." → "This library adds payments."
- "Let's delve into how the cache works." → "Here's how the cache works."
- "In today's fast-paced world, speed matters." → "Speed matters." (or cut entirely)
- "The result is a testament to careful design." → "The design is careful." (or show the result and let it speak)

Don't swap one cliché for another. Don't pad to hit a length. If a sentence carries no idea after you strip the decoration, delete the whole sentence.

## Step 3 — One idea per sentence, no transitions for their own sake

Good prose doesn't need "furthermore" and "moreover" to glue thoughts together — if two sentences belong next to each other, the reader already sees it. Use a transition only when the logical turn is real.

## Intentional slop is allowed, but only out loud

Sometimes you *need* the cliché in the text — quoting it as an example of bad writing, documenting the phrases this very gate catches, or reproducing a source verbatim. That's fine, but it must be a decision, not a leftover. Declare it:

```
NO-SLOP: INTENTIONAL — quoting "delve into" as an example of an AI tell
NO-SLOP: INTENTIONAL — reproducing the client's marketing copy verbatim
```

The Stop hook scans prose you edited this turn and blocks the turn when it finds 2+ distinct tells, unless it's clean or you've recorded that line.

## Avoiding false alarms

The gate is built tight: it only fires on the multi-word clichés above, never on common-but-fine words alone (leverage, robust, utilize). One stray tell never blocks — it takes two distinct ones. The em-dash signal only counts true em-dashes (—) in short paragraphs, so a long legitimate passage won't trip it.

## Kill switch

False positive (a doc that legitimately discusses these phrases): `touch .no-slop-off` in the project root, or `export NO_SLOP_GATE=off`.

## Pairs with

- **`no-stub`** — the same forcing function for code: don't ship half-written work.
- **`verify-before-done`** — once the prose is clean, the code behind it should be proven too.
