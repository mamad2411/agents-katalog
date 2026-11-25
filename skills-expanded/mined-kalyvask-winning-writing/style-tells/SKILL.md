---
name: style-tells
description: Scrubs the three surface tells that make prose feel AI-generated, padded, or jargon-heavy. Three targets behind one skill, picked via the --target arg. em-dashes (default off in cold email / memo / Slack, max one per page in op-eds), adverbs (the -ly and intensifier pile), jargon (the Silicon Valley / consultant kill-list plus AI-tell phrases). Use when the user says "kill the AI tells," "scrub jargon," "remove em-dashes," "cut the adverbs," "make this sound human," "less corporate," "sounds like ChatGPT," "—," "very," "really," "leverage," "synergy," "delve," "tapestry." Pass --target em-dashes|adverbs|jargon|all (default all).
---

# Style tells

Source: `points/ai-writing-rules.md` (em-dash rule), `points/core-rules.md` rule 5 (be shorter), `points/banned-jargon.md`, and Stephen King's *On Writing* (the adverb rule).

## What this skill does

Three passes behind one skill. Each pass removes a different surface tell that flags writing as AI-generated, padded, or jargon-heavy:

| Target | What it removes | When to run alone |
|---|---|---|
| **em-dashes** | em-dashes (—), double-hyphens (--), the "not just X — it's Y" construction | When the only problem is AI-flavored punctuation |
| **adverbs** | empty intensifiers, -ly adverbs the verb already implies, sentence-starting adverbs | When the draft is bloated with qualifiers |
| **jargon** | banned consultant words, AI-tell phrases, wordy substitutions | When the draft sounds corporate or AI-generated |

Default `--target all` runs all three in order: jargon → adverbs → em-dashes. The order matters: jargon and adverbs often expose dashes that were holding bloated clauses together.

## How to invoke

```
/style-tells "draft text"
/style-tells --target em-dashes "draft text"
/style-tells --target adverbs "draft text"
/style-tells --target jargon "draft text"
/style-tells --target all "draft text"
```

Without `--target`, default to `all`.

---

## Target 1 — em-dashes

In 2026 the em-dash is the **#1 AI tell**. Models love them. Humans use them sparingly. A draft with twelve em-dashes per page is a confession that an AI wrote it.

### Format limits

| Format | Em-dashes allowed |
|--------|-------------------|
| Cold email | **Zero** |
| Memo / status update | **Zero** |
| Slack message | **Zero** |
| LinkedIn post | One, max |
| Op-ed / essay | One per page (~250 words), max two |
| Substack post | One per major section break |

Over the limit → scrub.

### Substitution table

| Pattern | Rewrite options |
|---------|-----------------|
| `X — Y` (parenthetical aside) | `X (Y)` or `X, Y,` or `X: Y` |
| `X — and Y` (continuing thought) | `X. And Y.` or `X, and Y` |
| `X — Y — Z` (interrupted clause) | `X, Y, Z` (commas) or `X. Y. Z.` (sentences) |
| `If — and only if — Z` | `If, and only if, Z` |
| `I built X — A, B, C — from scratch` | `I built X from scratch: A, B, C.` |
| `She said — wait, did she?` | `She said. Wait, did she?` |
| `It's not just X — it's Y` (AI tic) | Cut entirely. Rewrite without the construction. |

The right substitution depends on what the em-dash was *doing*:

- **Aside / clarification** → parenthesis or colon
- **List or apposition** → colon
- **Tone shift / interruption** → period (start a new sentence)
- **Connective ("and so")** → "and," "so," or comma

### When NOT to remove

- Inside a direct quote from someone else (preserve their punctuation)
- Inside dialogue if the speaker would naturally pause that way
- Inside a code block, file path, or URL
- Inside a quoted citation (e.g., a book title rendered with em-dash)

If unsure, ask the user.

---

## Target 2 — adverbs

> *"The adverb is not your friend. The road to hell is paved with adverbs."* — Stephen King

Most adverbs are evidence the verb wasn't strong enough. *"She walked quickly"* → *"she rushed."* *"He smiled broadly"* → *"he grinned."* *"It is very important"* → *"it matters."*

Adverbs also leak the writer's anxiety: *"clearly,"* *"obviously,"* *"of course"* are tells that the writer is afraid the reader won't agree. Kill them; let the argument stand.

### Category A — empty intensifiers (cut on sight, ~95% of the time)

| Cut | Why |
|---|---|
| `very` | If "very" makes a difference, the adjective was wrong. *"Very tired"* → "exhausted." |
| `really` | Same problem. *"Really fast"* → "fast" or "blistering." |
| `actually` | Almost always pure throat-clearing. |
| `basically` | Filler. Cut. |
| `literally` | If metaphorical, cut. If literal, you don't need to say so. |
| `definitely` | Hedge dressed up as confidence. Just say it. |
| `clearly` | The reader decides what's clear. Don't tell them. |
| `obviously` | Same problem, plus condescending. |
| `essentially` | Filler. |
| `simply` | Often patronizing. Cut. |
| `quite` | British, weak. Cut. |
| `rather` | Hedge. Cut. |
| `somewhat` | Hedge. Cut or commit. |
| `pretty` (as in "pretty good") | Cut — softens the claim. |
| `truly`, `genuinely` | If you have to say it, they don't believe you. |
| `arguably` | Then make the argument. |

### Category B — adverbs the verb already implies (rewrite the verb)

| Adverb + weak verb | Stronger verb |
|---|---|
| walked quickly | rushed, sprinted, hurried |
| said loudly | shouted, barked |
| said quietly | whispered, murmured |
| smiled broadly | grinned, beamed |
| held tightly | clutched, gripped |
| ran very fast | sprinted |
| looked carefully | examined, scrutinized |
| ate quickly | wolfed down, devoured |

### Category C — sentence-starting adverbs (almost always cut)

| Cut | Why |
|---|---|
| `Importantly,` | If it's important, the sentence shows it |
| `Notably,` | Same |
| `Interestingly,` | Let the reader decide |
| `Surprisingly,` | Same |
| `Frankly,` | What were you being before? |
| `Honestly,` | Same |
| `Crucially,` | If it's crucial, write a stronger sentence |
| `Ultimately,` | Usually filler |
| `Fundamentally,` | Filler |

### Adverbs to keep (the 5% that earn their place)

- **They specify when, where, or how-much that the verb can't carry.** *"She arrived early"* — the adverb is the whole point.
- **They preserve a deliberate cadence.** *"He walked slowly, then faster, then ran"* — the contrast does work.
- **They are the joke.** *"She, very politely, told him to fuck off."*
- **In dialogue.** Real people say "really" and "actually."
- **In specifications.** *"The query runs roughly twice as fast"* — "roughly" carries epistemic weight.

If you can't articulate why the adverb earns its place, cut it.

---

## Target 3 — jargon

Two operations: **find** every banned word, AI tell, and wordy phrase, then **replace** with the shortest, plainest alternative. If a sentence collapses without the jargon, the sentence was empty; cut it.

### The kill list

**Silicon Valley / academic jargon (always)**
`currently`, `synergy`, `synergize`, `leverage`, `align`, `drive`, `strategize`, `empower`, `enable`, `deliverables`, `utilize`, `incentivize`, `facilitate`, `impact` (as a verb), `at the intersection of`, `driving innovation`, `building and scaling`, `passionate about complex problems`

**Grammar errors**
- `irregardless` → regardless
- `literally` (when used metaphorically)
- `ironic` (when you mean coincidental)

**Wordy phrases**
| Replace | With |
|---|---|
| In the event that | If |
| Concerning the matter of | About |
| I came to the realization that | I realized |
| We are investigating | We're investigating |
| Negative impacts | Harm |
| Positive impacts | Benefits |
| Sorry for the delay | Thanks for your patience |
| I think maybe we should | Let's |
| Utilize | Use |
| In today's fast-paced world | (delete) |
| I hope this email finds you well | (delete) |
| Just wanted to check in | (delete or replace with real content) |

**AI tells (scrub)**
- *"It's not just X — it's Y."* (most common AI tic)
- *"In today's [adjective] world"*
- *"Delve into"*
- *"Navigate the complexities of"*
- *"Tapestry of"*
- *"Robust solution"*
- *"Cutting-edge"*
- *"Game-changer"*
- Tricolons everywhere ("X, Y, and Z" three times in three sentences)
- Hedge-then-commit: *"While there are many considerations, ultimately…"*

**Cold-email-specific killers**
- *"I hope you are well"*
- *"My name is X"*
- *"Good morning"* / *"Good afternoon"* (timezone unknown)
- *"I'd love to pick your brain"*
- *"I'd love to grab coffee"*
- *"Just following up"*

---

## How to run the pass

### Pass 1 — Inventory
Scan the draft. For each target requested via `--target`, mark every hit. Count.

### Pass 2 — Categorize and rewrite
For each hit, decide:
- **Em-dash:** what was the dash doing? Aside / list / shift / connective → pick the right substitution.
- **Adverb:** empty intensifier (cut), verb-implied (rewrite verb), sentence-starter (cut), or earns its place (keep with one-line reason).
- **Jargon:** plain-English replacement, or cut the sentence if it collapses.

### Pass 3 — Read aloud
Did the prose get tighter, plainer, more human? If something now reads worse, the original word was doing real work. Put it back.

## Output format

```
## Inventory
em-dashes: N
adverbs: N
jargon hits: N
Total: N

## Hits (grouped by target)

### em-dashes
1. Line N: "the original sentence with the —"
   Function: aside | apposition | tone-shift | connective
   Rewrite: "the rewritten sentence"

### adverbs
1. Line N: "the original sentence"
   Removed: <word> (category: empty intensifier / verb-implied / sentence-starter)
   Rewrite: "the rewritten sentence"

### jargon
1. Line N: "the original sentence with the jargon"
   Banned: <word/phrase>
   Rewrite: "the rewritten sentence"
   Or cut entirely if: <reason>

## Kept with reason
- "she arrived early" — adverb is the point (specifies when)
- "the query runs roughly twice as fast" — epistemic hedge, earns its place

## Clean draft
[The full text with every requested target replaced. No commentary.]
```

## The litmus test

Read the rewrite aloud. Does the prose sound *more* like a human typing on a keyboard than the original? If yes, ship. If the rewrite reads jagged or robotic, back off — try a different substitution.

The goal is human prose, not purity.

## When the user pushes back on jargon cuts

Common: *"but my industry uses these words."*

Response: *"Your industry says them. Your readers tune them out. The people who get read are the ones who don't sound like everyone else."*

## When NOT to run

- **Direct quotes from someone else** — preserve their words verbatim.
- **Dialogue in fiction or scene-writing** — adverbs and em-dashes are how people actually talk and pause.
- **Legal or technical specs** where the adverb has precise meaning (`approximately`, `substantially`, `materially` can have legal weight).
- **Poetry, song lyrics, rhythm-driven prose** — sometimes a "softly" is doing musical work.
