---
name: compression
description: Cuts a draft to a target word count without losing substance. Two modes behind one skill. target-count hits a specific number (200 for a cold email, 500 for an op-ed, 6 for a product summary). redundancy catches the specific failure where a phrase says what the verb or context already implied — "going forward" after a future-tense verb, "as I mentioned earlier," "reduce so they are smaller." Implements Kramon's "rewrite this in less than 100 words" exercise, the six-word summary drill, and the in-class redundancy exercise. Use when the user says "shorten this," "cut this," "tighten," "make it concise," "too many words," "going forward," "say it twice," "redundant." Pass --mode target-count|redundancy|both (default both) and --target-words N for target-count.
---

# Compression

Source: `points/core-rules.md` rule 5 (be shorter), `points/banned-jargon.md` (wordy phrases), `points/frameworks.md` (six-word summary), and the Kramon in-class redundancy exercise.

> *"Be shorter. Always. Cut without losing substance."* — Kramon

## What this skill does

Two modes behind one skill. They cut different things:

| Mode | Cuts | Use when |
|---|---|---|
| **target-count** | throat-clearing, hedges, weak sentences, anything between the draft and the word target | User has a length to hit (200 for cold email, 500 for op-ed, 6 for product summary) |
| **redundancy** | phrases where one half is implied by the other (`going forward`, `as I mentioned`, `reduce so they are smaller`, `free gift`, `definitely commit`) | Draft is wordy in a way that's hard to point at — long without obvious filler |

Default `--mode both` runs redundancy first (it's surgical, every cut is defensible), then target-count (which may need to cut substantive material). The order matters: redundancy cuts free words first, so target-count doesn't have to.

## How to invoke

```
/compression "draft text"
/compression --mode target-count --target-words 200 "draft text"
/compression --mode redundancy "draft text"
/compression --mode both --target-words 500 "draft text"
```

Without `--mode`, default to `both`. `--target-words` is required for `target-count` mode and optional for `both` (if omitted in `both`, run redundancy only).

---

## Mode 1 — target-count

Most drafts can lose 30% with no loss of meaning. Many can lose 50%. Forced compression is what reveals which sentences were actually carrying weight.

### Three drill levels

**Level 1 — Cut 30% (standard pass)**

Tactics:
- Remove every -ly adverb that isn't doing real work
- Replace wordy phrases (see [banned-jargon.md](../../points/banned-jargon.md))
- Combine sentences that share a subject
- Cut hedges: *"I think,"* *"perhaps,"* *"it might be the case that"*
- Cut throat-clearing: *"In this piece I'll argue that…"* — just argue it
- Replace passive with active

**Level 2 — Hit a target word count**

User gives a number (200 for cold email, 500 for op-ed, 100 for memo). Iterate:

1. Cut to 1.5× the target — easy passes only
2. Cut to 1.2× the target — harder; remove subordinate clauses
3. Cut to 1.0× the target — surgical; every word earns its place
4. Cut to 0.9× the target — leave room for one final addition

**Level 3 — Six-word summary**

The ultimate compression. One thing, six words, tells a story.

Run the user through:
1. What's the single most important thing about this?
2. Who is the protagonist?
3. What changed?
4. Draft. Score. Iterate.

Examples that work:
- *"For sale: baby shoes, never worn."* (Hemingway)
- *"Edited Pulitzer winners. Now teaching business leaders."* (Kramon)
- *"Immigrant's kid, chip on her shoulder."* (student)
- *"Soldier first, engineer always, educator next."* (student)

The rule: six words that tell a **story** — not six unrelated descriptors.

### What not to cut

Compression is not amputation. **Keep:**
- Specific sensory details (a date, a place, a sound, an image) — these make writing memorable
- "Like you" lines and personal hooks
- The one moment of warmth or humor
- Names and numbers

**Cut first:**
- Throat-clearing
- Hedges
- Adverbs
- Synonyms used for variety ("she said… she explained… she argued…")
- Unnecessary qualifiers
- Background the reader can infer

### The two-pass method

1. **First pass** — read aloud. Cross out any sentence you stumble over. Stumbles are usually sentences not earning their place.
2. **Second pass** — read again. For each surviving sentence, ask: *what changes if I delete this?* If nothing, delete.

---

## Mode 2 — redundancy

A specific failure: a phrase that *feels* like it adds information when in fact it adds nothing. The verb or the surrounding context already implies it. Cut.

### Pattern 1 — Verb-implied direction

*"Going forward"* and *"moving forward"* after a future-tense verb.

| Redundant | Fixed |
|---|---|
| We promise better security going forward. | We promise better security. |
| Moving forward, we'll offer encryption. | We'll offer encryption. |
| In the future, all our hires will be technical. | All our hires will be technical. |
| From this point onward, we'll improve. | We'll improve. |

The future tense already does the work. Add a tag only if you're contrasting with the past (*"unlike last quarter, we'll publish monthly going forward"* — fine).

### Pattern 2 — Self-referential meta-commentary

The reader is reading it; they know.

| Redundant | Fixed |
|---|---|
| I am currently writing this email to you. | (cut entirely) |
| As I said earlier, X. | X. |
| As I mentioned in my last email, X. | X. |
| The purpose of this memo is to argue that X. | X. (just argue it) |
| What I will demonstrate in this section is X. | X. (then demonstrate it) |

### Pattern 3 — Verb-implied result

The verb names the action; the result is implied.

| Redundant | Fixed |
|---|---|
| Reduce the size of teams so they are smaller. | Reduce the team. |
| Increase headcount so we have more people. | Increase headcount. |
| Lower the price so it costs less. | Lower the price. |
| Shorten the meeting so it's not as long. | Shorten the meeting. |
| Speed up the rollout so it's faster. | Speed up the rollout. |

### Pattern 4 — Tautological qualifiers

The adjective and the noun say the same thing.

| Redundant | Fixed |
|---|---|
| 9am in the morning | 9am |
| Free gift | Gift |
| New innovation | Innovation |
| Past history | History |
| Future plans | Plans |
| End result | Result |
| Final outcome | Outcome |
| Unexpected surprise | Surprise |
| Personal opinion | Opinion |
| Each individual person | Each person |
| Advance planning | Planning |
| Joint collaboration | Collaboration |
| Period of time | Period |

### Pattern 5 — Doubled qualification

If the noun or verb is absolute, the intensifier is redundant.

| Redundant | Fixed |
|---|---|
| I will definitely commit. | I will commit. |
| It's absolutely critical. | It's critical. |
| Completely unique. | Unique. |
| Totally finished. | Finished. |
| Fully comprehensive. | Comprehensive. |

### Pattern 6 — Restating the obvious

| Redundant | Fixed |
|---|---|
| Free of charge | Free |
| At a price of $100 | $100 |
| In the month of November | In November |
| The country of Greece | Greece |
| Despite the fact that | Although |
| In light of the fact that | Because |
| For the purpose of | To |

### Pattern 7 — Two weak words → one strong word

Kramon's Session 8 drill: nearly every adverb-plus-weak-verb pair has a single strong verb that does the work better. The strong verb is shorter, more vivid, and more memorable. Two weak words almost always lose to one strong one.

| Two weak words | One strong word |
|---|---|
| Incredibly important | Vital / crucial |
| Dramatically cut | Slashed |
| Mitigating the impact | Cushioning / softening |
| Grown up significantly | Matured |
| Make better | Improve |
| Make sure | Ensure |
| Walk fast | Stride / hurry / dash |
| Impact significantly | Reshape / overhaul |
| Extremely smart | Brilliant |
| Especially unusual | Singular / unique |
| Negatively affect | Harm / hurt |
| Look carefully at | Examine / inspect |
| Think hard about | Reckon with / weigh |
| Get bigger | Grow / swell |
| Get smaller | Shrink |
| Get worse | Decline / worsen |
| Get better | Improve / mend |
| Very angry | Furious |
| Very tired | Exhausted |
| Very happy | Thrilled |
| Very sad | Bereft / devastated |
| Very surprised | Astonished |
| Very scared | Terrified |
| Very small | Tiny / minute |
| Very big | Enormous / vast |
| Very fast | Rapid / sudden |
| Very slow | Glacial |
| Very old | Ancient |
| Very new | Novel / fresh |
| Looked at quickly | Glanced |
| Spoke loudly | Shouted / boomed |
| Spoke softly | Murmured / whispered |
| Held tightly | Gripped / clutched |
| I'll be able to do this | I can do this |
| Action item | Task / to-do |
| Make a decision | Decide |
| Reach a conclusion | Conclude |
| Conduct an investigation | Investigate |
| Give consideration to | Consider |

**Use the table as a sniff test, not gospel.** If the strong word changes the meaning (*"vital"* and *"important"* are not exact synonyms — *vital* means "essential to survival"), keep the weaker pair. The point is to notice when two weak words are doing the job of one, not to forcibly substitute.

### The two-question test (for any phrase)

1. **Does this phrase add information not already implied by the verb, the subject, or the surrounding sentence?**
2. **If I cut this phrase, what changes?**

If 1 is no and 2 is "nothing changes" — cut.

---

## How to run the pass

### Pass 1 — Redundancy scan
Search for direction tags (*going forward, moving forward, in the future, currently, as I mentioned, as I said, as we discussed*) — candidates to cut.

### Pass 2 — Verb-result restatements
For each verb, check the next clause: does it merely describe the result? *"Reduce X so Y is smaller"* — cut the *"so Y is smaller."*

### Pass 3 — Tautological adjectives and doubled qualifiers
*free gift, new innovation, past history, end result, definitely commit, absolutely critical* — cut the redundant half.

### Pass 4 — Two-weak-words → one-strong-word
Scan for adverb-plus-weak-verb pairs and "very + adjective" pairs. Substitute the strong single word from the Pattern 7 table when the meaning holds. Skip when the strong word shifts the meaning.

### Pass 5 — Target-count cuts (if a target is set)
Apply the three drill levels above. Stop when at target.

### Pass 6 — Read aloud
Anything that lands twice in your ear lands twice in the reader's ear. Cut the second landing.

## Output format

```
## Compression summary
Original: N words → Final: N words (X% reduction)
Target: N words [if set]

## Redundancy hits

| Line | Pattern | Original | Fixed |
|---|---|---|---|
| N | direction tag | "going forward, we'll improve" | "we'll improve" |
| N | self-referential | "as I said earlier, X" | "X" |
| N | verb-implied result | "reduce so they are smaller" | "reduce" |
| N | tautological | "free gift" | "gift" |

## Target-count cuts [if target set]

Categories of what was removed:
1. **Jargon and wordy substitutions:** [examples]
2. **Throat-clearing and hedges:** [examples]
3. **Substantive cuts:** [examples with one-line justification each]

## One flag
[If there's a sentence you might want to put back, with the tradeoff. Otherwise omit.]

## Clean draft
[The full text at the target length with all cuts applied.]
```

## When the user resists cutting

Common pushback: *"but that detail is important."*

Response: *"Then it should earn its place. Show me which other sentence we can cut to keep it. We can't keep both."*

Compression is zero-sum.

## When NOT to use

- **Legal writing** where tag-alongs may be load-bearing for precision. *"For the avoidance of doubt"* sometimes does work *"to be clear"* doesn't.
- **Poetry, song lyrics, deliberate rhetoric.** Repetition is the device.
- **Casual chat / Slack** where small redundancy reads warmer than terse. *"Just wanted to say"* in a thank-you note may earn its place.

## The Kramon rule

> *"Every sentence you write, ask yourself: am I being repetitive? That's the way to improve your writing."*

Most drafts have two to five redundancy hits per paragraph. The most over-written drafts have one every sentence. Run this skill after `style-tells` for the cleanest result.
