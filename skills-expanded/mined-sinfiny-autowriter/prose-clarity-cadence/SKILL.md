---
name: prose-clarity-cadence
description: Use when editing, rewriting, diagnosing, or formatting nonfiction prose, essays, business writing, paragraphs, web copy, and AI-generated drafts for clarity, cadence, lexical specificity, paragraph breaks, and screen scannability. Based on David Perell's How I Write interviews with Steven Pinker, Ward Farnsworth, Robert Macfarlane, and Jason Fried; intended as an editorial workflow, not a style imitation skill.
---

# Prose Clarity Cadence

Use this skill to turn dense or bland prose into clear, memorable, screen-readable writing.

## Source Protocol

- Read `references/source-notes.md` when the user asks where the method came from, wants the video-by-video breakdown, or wants to modify the workflow.
- Treat the source videos as editing lenses, not as voices to imitate.
- Do not quote long transcript passages or mimic any living writer's prose style.

## Operating Loop

1. Identify the writing job: explain, persuade, narrate, announce, sell, summarize, or instruct.
2. Name the intended reader and what they already know.
3. Mark the core thesis or "aha" sentence.
4. Run the Pinker clarity pass.
5. Run the Farnsworth geometry pass.
6. Run the Macfarlane specificity pass.
7. Run the Perell/Fried screen pass.
8. Read once for breath and once for skim value before finalizing.

## Pinker Clarity Pass

Purpose: defeat the curse of knowledge.

- Replace unexplained jargon, acronyms, and insider shorthand with reader-facing language.
- Introduce the problem before the mechanism, method, or result.
- Convert weak nominalizations into verbs when the noun hides the actor or action.
- Prefer concrete examples over unsupported generalizations.
- Make the first sentence of an explanatory paragraph start from a person, object, scene, action, or observable problem.
- Split any sentence that makes the reader wait too long for the main verb.

Nominalization check:

```text
Flag abstract nouns ending in -tion, -ment, -ity, -ance, or -ence.
Keep precise terms of art when needed.
Rewrite only when the noun turns action into fog.
```

Breath test:

```text
If a sentence has more than 30 words, more than three clauses, or more than two stacked conditions before the main verb, split it.
```

## Farnsworth Geometry Pass

Purpose: make the paragraph move.

- Track sentence lengths as short, medium, and long.
- Never leave three medium sentences in a row if the paragraph should feel alive.
- Use short Saxon verbs and nouns for force: get, make, cut, hold, break, see, say, use.
- Use Latinate words when precision matters, but do not let them carry the emotional peak.
- Put the sentence's strongest word at the end whenever possible.
- Use anaphora, contrast, or inversion only for a line that deserves extra emphasis.
- Avoid decorative rhetoric. The device must clarify the thought.

Sentence length pattern:

```text
Short: 1-8 words.
Medium: 9-22 words.
Long: 23-35 words.

If the paragraph runs medium, medium, medium, revise the third sentence short or long.
```

Ending rule:

```text
Before finalizing a concluding sentence, ask:
What word should ring?
Move that noun or verb as close to the period as natural English allows.
```

## Macfarlane Specificity Pass

Purpose: remove statistical blandness.

- Delete empty modifiers: very, really, quite, just, literally, actually, basically, incredibly, extremely.
- Replace generic verbs with exact verbs that imply motion, pressure, or change.
- Hunt lazy forms of "to be" and "to have"; keep them only when they are the clearest choice.
- Upgrade generic nouns before upgrading adjectives.
- For descriptive or narrative prose, add one specific sensory detail that belongs to the subject.
- Let rhythm and punctuation serve the subject: clipped syntax for urgency, longer syntax for flow, clean stops for force.

Specificity ladder:

```text
Abstract claim -> concrete example -> specific noun -> active verb -> sensory detail.
```

One-detail rule:

```text
Every descriptive or narrative paragraph needs one non-obvious sensory detail.
Do not invent ornamental detail in technical, legal, or purely procedural prose.
```

## Perell/Fried Screen Pass

Purpose: make the reader want to keep reading on a screen.

- Keep paragraphs to four sentences or fewer. Use five only when the sentences are short.
- Break at the conceptual pivot, not at an arbitrary line count.
- Pull the core thesis into its own one-sentence paragraph when it carries the section.
- Use bold for the one full sentence a skimming reader must not miss.
- Prefer one clean heading over an explanatory preamble.
- Compress until each paragraph does one job.
- In business writing, make the next action, decision, or consequence unmistakable.

Whitespace rule:

```text
If the best sentence hides in the middle of a block, isolate it.
If two ideas share one paragraph, split them.
If a paragraph explains the same point twice, cut the weaker version.
```

## Output Contracts

For a rewrite:

```text
Revised draft:

Change notes:
- Clarity:
- Cadence:
- Specificity:
- Formatting:
```

For a diagnostic pass:

```text
Reader:
Core thesis:
Main clarity risks:
Cadence risks:
Bland words or verbs:
Scannability issues:
Recommended edit:
```

For an autonomous edit loop:

```text
Draft -> Pinker clarity -> Farnsworth geometry -> Macfarlane specificity -> Perell/Fried screen formatting -> final skim check
```

## Guardrails

- Preserve the user's meaning, claims, facts, and level of formality.
- Do not make precise technical prose chatty unless the user asks.
- Do not over-rhetoricize simple instructions.
- Do not add sensory detail to subjects that would make the writing less truthful.
- Do not bold more than one sentence per short section.
- Do not turn every paragraph into a single-sentence paragraph.
- If the user asks for a minimal edit, keep the edit radius small and explain what stayed unchanged.
