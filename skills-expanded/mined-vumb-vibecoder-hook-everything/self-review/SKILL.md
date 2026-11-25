---
name: self-review
description: After drafting, reread the text as a native reader in its own language. If it still reads as machine-written, rewrite it. Works in any language. Sub-skill: load only when routed from the hook-everything entry skill, not for general writing or editing.
---
# Self-Review Loop (Read It Cold, Rewrite If It Still Smells)

A draft that passes a word list can still read as machine-written. This skill adds a reader's pass at the end: read the text as a skeptical native speaker, say whether it still reads as AI, and fix it until it doesn't. It works in any language.

Be honest about the limit. A model judging its own text is an unreliable detector, so this pass never relies on a feeling alone. Every verdict needs quoted evidence, and the scanner has the last word on score.

---

## The Loop (maximum 3 rounds)

1. **Switch to the reader's language and register.** Judge the text in the language it is written in. Never translate it to English to judge it, because translation hides the calques and register slips you are looking for. Picture one real reader: a native speaker of that language who reads a lot and distrusts polished copy.
2. **Read it cold, start to finish, without editing.** Then give one verdict: `reads human`, `unsure`, or `reads machine-made`.
3. **Back the verdict with evidence.** Quote the 3 spans that feel most machine-made and name the tell for each (`uniform sentence weight`, `abstract noun as subject`, `see-saw concession`, `claim-example-moral paragraph`, `calque from English`, `no concrete anchor in 35 words`). If you cannot quote a span, you have no verdict, so run the scan.
4. **Run `python3 tools/slop_scan.py <file> --fix-hints --hidden`** when a shell is available. Treat a score above 15 or any hidden-character hit as a failed round, whatever the verdict was.
5. **Rewrite the flagged spans from scratch.** Change the subject, the verb and the sentence shape. Swapping a synonym into the same skeleton fixes nothing (`anti-slop` Rule 72).
6. **Repeat from step 2.** Stop when the verdict is `reads human` and the score is `<= 15/100`, or after 3 rounds. After round 3, list what still bothers you and hand it over instead of looping again.

---

## What Never Changes in a Rewrite

- **Facts, numbers, names and dates stay exactly as they were.** A rewrite that changes a figure is a new claim.
- **Quoted text stays word for word** (`anti-slop` Rule 42).
- **Do not invent personal detail to sound human.** No fake anecdotes, no made-up "last Tuesday" stories, no deliberate typos. `value-check` item 2 forbids fabricated receipts, and made-up texture counts. When a piece needs lived detail, leave a bracket for the person to fill: `[your own example here]`.
- **Keep the author's register.** A formal legal memo should come back formal and plain, not chatty.

---

## Per-Language Reader Checks

Run the checks for the language of the text. For languages not listed, use the Universal block.

| Language | Extra tells a native reader notices |
|---|---|
| English | Em-dash glue, "not just X, it's Y", two-word rhetorical questions, three-adjective stacks, a closing summary paragraph. |
| Vietnamese | Pronoun stuffing (`bạn`, `của bạn`, `chúng tôi` in every clause), `việc + động từ` nominalizations, `không chỉ... mà còn...` openers, stock phrases like `trong bối cảnh`. |
| Spanish | `en el mundo actual` openers, `juega un papel fundamental`, calques of English passive voice, subject pronouns where Spanish drops them. |
| French | `dans un monde en constante évolution`, `il est important de noter que`, English-style noun stacks, `vous` and `nous` repeated where French drops them. |
| German | `in der heutigen schnelllebigen Welt`, long nominal chains with `-ung` nouns, English word order in subordinate clauses. |
| Chinese / Japanese / Korean | Stock frames (`在当今...`, `〜において重要な役割を果たします`, `오늘날...`), literal translation of English connectors, stiff register that no one speaks, over-explicit subjects in Japanese and Korean. |
| **Universal (any language)** | See below. |

**Universal block, for any language**

- Every sentence has about the same length and the same temperature.
- Paragraphs share one shape: claim, two examples, a moral.
- Syntax follows English even though the words are not English (a calque of structure, not of vocabulary).
- Register is flat and over-polite from the first line to the last, with no slang, no shorthand, no mid-thought correction.
- Abstract nouns stand in for people and actions, and nothing in a 35-word stretch is concrete.
- Every point is hedged on both sides, and the text never takes a position.
- A list or heading structure imposed on something a person would have just said.

---

## Quick Self-Test Questions

Ask them in the text's own language, then answer with a quoted span.

1. Which sentence would a native speaker never say out loud to a colleague?
2. Where does the text explain something nobody asked about?
3. Which paragraph could be moved to a different article without anyone noticing?
4. Where does the writer sound more careful than a person would be?
5. If I deleted the first and last sentences, would any fact be lost? (`anti-slop` Rule 73)

---

## Hand-Off

End the loop with one line for the user: the final verdict, the scanner score if it ran, and anything left unresolved. Then run `skills/value-check`.
