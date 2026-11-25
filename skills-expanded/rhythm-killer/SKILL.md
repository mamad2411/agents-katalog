---
name: rhythm-killer
description: Fixes two sentence-rhythm tells that mark prose as AI-generated. Two targets behind one skill, picked via the --target arg. fragment-chain (three or more short sentences back-to-back) and uniform-length (two or more consecutive sentences within ~2 words of each other, especially with parallel structure). Use when the user says "reads like AI," "too choppy," "same length sentences back to back," "staccato," "fragments piled up," "rhythm is off," "uniform pacing." Pass --target fragment-chain|uniform-length|all (default all).
---

# Rhythm killer

Source: `points/ai-writing-rules.md` (the "Choppy short-sentence stacks" entry) and live critiques on cold-email and personal-essay drafts where the model's rhythm gave it away even after surface tells were scrubbed.

## What this skill does

Two passes behind one skill. Each pass fixes a different sentence-rhythm tell:

| Target | What it flags | When to run alone |
|---|---|---|
| **fragment-chain** | three or more short sentences/fragments back-to-back (each under ~6 words) | When the draft has a visible staccato run ("Same apartment. Finally. Tax law travels.") |
| **uniform-length** | two or more consecutive sentences within ~2 words of each other in length, especially with parallel syntactic structure ("You X. You Y. You Z.") | When sentences are different in content but march at the same tempo |

Default `--target all` runs both passes in order: fragment-chain first (more obvious), then uniform-length (subtler, often surfaces after the chain is fixed).

## How to invoke

```
/rhythm-killer "draft text"
/rhythm-killer --target fragment-chain "draft text"
/rhythm-killer --target uniform-length "draft text"
/rhythm-killer --target all "draft text"
```

Without `--target`, default to `all`.

---

## Target 1 — fragment-chain

Three or more short sentences (under ~6 words each) in a row read as AI rhythm. The model defaults to staccato when it doesn't know how to develop a thought, so it chops the thought into fragments that look "punchy" but pattern-match to LLM output.

**The trigger pattern (verbatim from a live draft):**

> Next year I want you here. California. Same apartment, finally. Tax law works from anywhere.

Four short sentences. Each lands. The chain doesn't — it reads as a list of beats, not a thought.

### How to fix

| Pattern | Rewrite move |
|---|---|
| 3+ shorts in a row | Keep one short (the strongest, usually first or last). Absorb the others into a longer surrounding sentence. |
| Opening with a fragment + immediate restatement | Cut the restatement; the fragment carries. |
| Closing with three short summary beats | Combine into one sentence with the final beat punching. |

**Before / after on the trigger pattern:**

| Before | After |
|---|---|
| Next year I want you here. California. Same apartment, finally. Tax law works from anywhere. | California, finally. Next year I want you here with me, in the same apartment for the first time in over a year. Tax law works from anywhere. |

The "California, finally." opener stays as a fragment for punch. The next two beats fold into a longer sentence that carries the substance. The rhythm is now short-long-medium instead of short-short-short-short.

### When NOT to flag

- Dialogue. Real people speak in clipped fragments. ("Wait. What? You're kidding.")
- Lists rendered as sentences for emphasis. ("Vendors. Families. Dietary requirements. Dress fittings.") — if it's clearly an enumeration, the chain is doing list work, not rhythm work.
- Poetry, song lyrics, deliberate rhythm-driven prose.
- A chain of exactly 2 shorts (a setup-payoff pair) — that's the `uniform-length` target's job, only if they're also similar length.

---

## Target 2 — uniform-length

Two or more consecutive sentences within ~2 words of each other in length, *especially* when their syntactic structure is parallel. The model defaults to uniform sentence length even when each individual sentence is fine — the cumulative effect reads as machine pacing.

**The trigger patterns (verbatim from live drafts):**

> Thank you for being the steady one. You married me when I was unemployable on paper. You book the next flight before I have to ask.
> *(7 / 9 / 10 words, three sentences with parallel "You X" structure — a triplet)*

> Through the long job search, you never once said "maybe come back early." Every late call when I was anxious about another rejection, you said: keep going.
> *(13 / 14 words, both with parallel "you ... said ..." structure)*

> One thing for next year. Tell me earlier. You sat on the photographer cancellation for three days. I know you didn't want me panicking from California. I'd rather panic with you. Call me when it's still small.
> *(6 sentences, all between 3 and 10 words — the whole paragraph marches at one tempo)*

### How to fix

| Pattern | Rewrite move |
|---|---|
| Parallel triplet ("You X. You Y. You Z.") | Combine the last two into one sentence with a conjunction. ("You X. You Y, and you Z.") |
| Two similar-length sentences with parallel verbs | Fold the second into the first as a subordinate clause. |
| Whole-paragraph march at one tempo | Pick the strongest beat to stay short; absorb the surrounding sentences into longer ones. Aim for at least one VL (>20 words) and one S (<8 words) per paragraph. |

**Before / after on the trigger patterns:**

| Before | After |
|---|---|
| Thank you for being the steady one. You married me when I was unemployable on paper. You book the next flight before I have to ask. | Thank you for being the steady one. You married me when I was unemployable on paper, and you book the next flight before I have to ask. |
| Through the long job search, you never once said "maybe come back early." Every late call when I was anxious about another rejection, you said: keep going. | Through the long job search, on every late call when I was anxious about another rejection, you never once said "maybe come back early." You said: keep going. |
| One thing for next year. Tell me earlier. You sat on the photographer cancellation for three days. I know you didn't want me panicking from California. I'd rather panic with you. Call me when it's still small. | One thing for next year: tell me earlier. You sat on the photographer cancellation for three days because you didn't want me panicking from California. I'd rather panic with you, so call me when it's still small. |

### The length distribution test

In any paragraph over four sentences, check that sentence lengths span at least three distinct buckets:

- **VS / S** — under 8 words
- **M** — 8–15 words
- **L** — 16–25 words
- **VL** — over 25 words

A paragraph that lives entirely in one bucket is the failure mode. Two adjacent buckets is acceptable. Three or more is human.

### When NOT to flag

- Two short sentences in a row that serve as a rhetorical setup-payoff pair ("One thing. Tell me earlier.") — this is intentional structure, not rhythm drift.
- Two sentences of similar length but obviously different syntactic structures (a list-fragment followed by a subject-verb sentence). The rule fires hardest on *parallel* structure, not on mere length match.
- Aphoristic prose (Hemingway, Carver) where the rhythm is the point. Don't flag if the author is clearly choosing the cadence.

---

## How to run the pass

### Pass 1 — Inventory
Walk the draft sentence by sentence. Count words per sentence. For each requested target, mark every hit:
- **fragment-chain:** any run of 3+ consecutive sentences each under 6 words.
- **uniform-length:** any run of 2+ consecutive sentences within 2 words of each other in length, with the parallel-structure flag noted (parallel = same opening word/structure, e.g., "You X. You Y." or "I X. I Y.").

### Pass 2 — Diagnose
For each hit, decide which rewrite move applies (see the tables above). The first move is usually merging two sentences into one. The second is restructuring a longer surrounding sentence to absorb the chain.

### Pass 3 — Verify
Read aloud. Does the rhythm now feel like a human speaking? Or did the rewrite swing too far the other way (one giant 40-word sentence)? Aim for distinct buckets, not maximum length variance.

## Output format

```
## Inventory
Fragment chains found: N (locations: line A, line B)
Uniform-length runs found: N (locations: line C, line D)
Sentence-length distribution by paragraph: [buckets per para]
Total: N

## Hits (grouped by target)

### fragment-chain
1. Paragraph N: "the original chain"
   Lengths: [4, 1, 3, 4]
   Rewrite: "the rewritten paragraph"

### uniform-length
1. Paragraph N: "the original run"
   Lengths: [13, 14] | Parallel structure: yes ("you ... said ...")
   Rewrite: "the rewritten paragraph"

## Kept with reason
- "Vendors. Families. Dietary requirements." — list enumeration, doing list work
- "One thing. Tell me earlier." — setup-payoff pair, rhetorical

## Clean draft
[The full text with every flagged run rewritten. No commentary.]
```

## The litmus test

Read the rewrite aloud. Does the prose now have a heartbeat — slow, fast, slow — instead of marching at one tempo? If yes, ship. If the rewrite collapses into one breathless paragraph with no short beats, restore one or two short sentences for punch.

The goal is rhythm, not maximum length variance.

## When NOT to run

- **Dialogue, scene-writing, fiction.** Sentence rhythm is a deliberate craft choice in narrative prose; do not impose corporate-rhythm rules on it.
- **Poetry, song lyrics, slam.** Cadence is the medium.
- **Aphoristic prose by a writer who has chosen the cadence** (Hemingway, Joan Didion, Lydia Davis). If the user is deliberately writing in a short-sentence style, the skill's flags are noise.
- **Code blocks, lists, tables, or bullet points.** Each bullet is its own unit; cross-bullet rhythm rules do not apply.

If the user pushes back ("the staccato is the point"), trust them. Note the flag, output the original unchanged.

## Composes with

- `style-tells` — run after rhythm-killer. Once the rhythm is human, the surface tells (em-dashes, adverbs, jargon) are easier to spot.
- `humanize` — run after both. Humanize adds intentional irregularity on top of a draft that's already rhythmically varied.
- `compression` — if a draft is over its word target, run rhythm-killer first; merging sentences often cuts 5–10% before any deliberate compression pass.
