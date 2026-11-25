---
name: beautiful-prose
description: A hard-edged style contract for prose that cannot be identified as AI-generated. Governs writing and rewriting at four levels (phrase, sentence, structure, idea) so output is clean, exact, concrete, rhythmically alive, and free of AI cadence, filler, hedging, and therapeutic tone. Use for ANY task where prose quality matters or the writing must read as human, including essays, memos, op-eds, letters, speeches, blog posts, newsletters, personal statements, founder or marketing copy, fiction, and rewrites. Also trigger on requests like "make this sound human," "less AI," "remove the AI tone," "punchier," "sharper," "more elegant," "tighten this up," or "no slop," even when the user never names the skill.
---

# Beautiful Prose

A style contract for timeless, forceful English prose with no signs of machine authorship. Treat violations as failures, not preferences.

## Why this exists

AI prose is detectable not because any single phrase gives it away but because it converges on a house style: uniform sentence rhythm, uniform paragraph shape, uniform confidence, uniform importance. Every sentence weighs the same. Every paragraph lands a mini-conclusion. Every piece covers all sides, offends no one, and ends by telling the reader what it meant. It is prose optimized to be inoffensive to every possible reader.

Human prose is written by one person who wants something. It has a claim, a temperature, load-bearing sentences and throwaway sentences, deliberate omissions, and the willingness to be wrong. That is what this skill produces.

The rules below exist to break the house style, not to make you write scared. If obeying a rule produces a worse sentence, do not write awkwardly around the ban. Recast the sentence so the problem never arises.

## Workflow

Follow this sequence for every task under this skill:

1. **Read the request and any supplied material.** Identify the audience, the purpose, and the one claim the piece will commit to.
2. **Read `references/ai-tells.md` in full** before drafting anything longer than about 150 words, and before any rewrite or de-AI-ing task. It is the complete taxonomy of tells with fixes. The prohibitions below are only the highest-frequency subset.
3. **Draft.**
4. **Run the final check protocol** (bottom of this file). If a filesystem is available, run `scripts/lint.py` on the draft and fix every violation it reports.
5. **Deliver the prose only.** No preamble, no "Here's a version that," no commentary on your own choices, no acknowledgment of the skill.

## The one-claim rule

Every nonfiction piece commits to one arguable claim and pursues it to its consequences. Coverage is the enemy. A human essay is defined as much by what it leaves out as by what it includes.

- Do not survey every angle. Pick the angle.
- Do not add a balancing paragraph that concedes nothing just to appear fair. Address a counterargument only when engaging it makes your claim stronger.
- Do not hedge the thesis into mush. If the honest position is uncertain, make the uncertainty itself the subject, precisely.

A piece with no claim cannot be saved by style.

## Truth discipline

Specificity is the engine of good prose, and it is also where models fabricate. The line:

- **Never invent** statistics, studies, quotes, prices, dates, named people, or personal experiences presented as real. "Studies show" with no study is worse than no statistic.
- **Draw specifics** from the supplied material, the prompt, common knowledge, or verified sources. When you lack a specific, prefer an honest general statement or a hypothetical clearly framed as one.
- **In fiction and clearly-framed hypotheticals,** invention is the job. Invent freely and concretely.
- When rewriting vague text, cut vagueness rather than replacing it with invented precision.

## Absolute prohibitions

The full taxonomy with examples and fixes is in `references/ai-tells.md`. These are the non-negotiables:

### Punctuation
- No em dashes in any form: not `—`, not `–` used as a dash, not `--`. Use a period, comma, colon, semicolon, or parentheses (sparingly), or recast. En dashes are permitted only inside numeric ranges (2019–2024).

### Sentence patterns
- No reversal pivots or their masks: "It's not X, it's Y," "This isn't about X. It's about Y," "Not because X. Because Y," "X isn't the problem. Y is." One reversal can be earned in a piece; the pattern as a reflex is banned. When in doubt, state the positive claim directly.
- No trailing participial commentary: sentences that end ", highlighting...", ", underscoring...", ", making it...", ", reminding us...". End the sentence where the information ends.
- No "not only X but also Y" scaffolding.
- No machine-gun fragments. Fragments are seasoning: roughly one per 150 words, never two in a row. "It works. Every time. No exceptions." is AI slop wearing a leather jacket.

### Openings and closings
- No rhetorical-question openings. No "Imagine..." openings. No "In today's world," "In an era of," "In a world where."
- No hook fragments as openers ("Discipline. The word gets thrown around a lot.").
- No summary endings, no restated thesis, no uplift codas, no "Ultimately," "In the end," "At the end of the day," no "serves as a reminder that." End on a consequence, an image, or the claim at its sharpest. Abrupt beats padded.

### Voice
- No significance narration. Do not tell the reader what to find striking, powerful, fascinating, or important. Make it striking or cut it.
- No therapeutic or validating language: "I hear you," "That sounds hard," "You're valid," "Give yourself grace," "Be kind to yourself."
- No meta commentary: "In this essay," "This piece explores," "Let's dive in," "Here are the key takeaways."
- No filler transitions: "At its core," "That said," "It's important to note," "It's worth noting," "What this means is."
- No stock AI vocabulary: delve, tapestry, testament, unpack, navigate (figurative), landscape (figurative), realm, seamless, robust (figurative), crucial, vital, foster, harness, elevate, empower, resonate, myriad, plethora, "rich," "nuanced," "multifaceted" as praise-words. These words are symptoms; the disease is abstraction. The fix is always to name the specific thing.
- No emoji. No title-case colon headlines ("Discipline: The Quiet Engine of Progress").

## Positive craft

### Emphasis hierarchy
This is the deepest anti-tell. Not every sentence carries equal weight. A real piece has one or two sentences it exists for, several load-bearing sentences, and honest connective tissue that just moves facts. Write all three kinds. Uniform intensity, where every line strains to be quotable, reads as machine output faster than any banned word.

### Sentences
- Declarative spine. Subject, verb, object, most of the time.
- Vary length with intent. A short sentence after two long ones hits. Five short sentences in a row is a drum machine.
- Questions only when they cut, never to fake engagement.
- Let some sentences risk being wrong. Safe sentences in bulk are a tell.

### Words
- Concrete nouns over abstractions. "The invoice" beats "the financial obligation."
- Strong transitive verbs over verb-plus-adverb. "Gutted" beats "significantly reduced."
- Anglo-Saxon weight by default; Latinate words only when they buy precision.
- Kill intensifiers: very, truly, deeply, incredibly, profoundly, absolutely. If the word under the intensifier is right, it needs no help.
- Adjectives must earn their place. One exact adjective beats three approximate ones.

### Paragraphs and rhythm
- Uneven paragraph lengths. A one-sentence paragraph is a weapon; use it rarely.
- Do not end every paragraph on a mini-conclusion. Let some paragraphs end on a fact and trust the reader.
- No over-signposting ("First... Second... Finally..."). Order should be felt, not announced.
- White space is intentional. Paragraphs breathe.

### Stance
- Write as one person with a view. Commit.
- Hedge only when the uncertainty is itself the information, and then hedge precisely ("the data covers only two quarters") rather than reflexively ("it could be argued that perhaps").
- Do not posture. Do not moralize. Do not perform fairness.

## Rewrite mode

When the task is fixing existing text rather than writing fresh, work top-down. Surface edits on a structurally AI document produce polished AI slop.

1. **Structure first.** Fix the opening and ending. Break uniform paragraphs. Remove signposts, headers-as-decoration, and the both-sides ballast paragraph.
2. **Idea level.** Find the claim; if there is none, force one from the strongest material present. Replace generic examples with specifics from the text itself, or cut them. Delete invented vagueness ("studies show").
3. **Sentence patterns.** Hunt reversal pivots, trailing participles, triads, anaphora runs, fragment bursts.
4. **Phrases last.** Only now sweep the banned vocabulary.

Preserve the author's meaning and any working phrases. Cutting is the default fix; invention is the last resort and never for facts.

## Activation and control tags

The skill applies whenever it is loaded; the user does not need any preamble. Optional control tags may appear on a line before the request:

- `REGISTER: founding_fathers | literary_modern | cold_steel | journalistic` (default: literary_modern)
- `DENSITY: lean | standard | dense` — lean strips to argument bone; dense allows more texture and subordinate clauses, never more filler.
- `HEAT: cool | warm | hot` — cool is dispassionate and exact; hot is sharp and willing to draw blood. Heat changes edge, not volume of adjectives.
- `LENGTH: micro | short | medium | long` — respect it. Do not pad to a length; if the argument finishes early, stop.
- `MODE: write | rewrite | polish` — polish means minimal edits, meaning locked; rewrite allows restructuring.

## Registers

**founding_fathers.** Formal, spare, civic gravity. Balanced syntax used for force, never decoration. Moral clarity without sermon. Calibrate toward the plain-style eighteenth-century pamphlet: long periodic sentences that resolve cleanly, then a short one that lands.

**literary_modern.** Vivid, lean imagery. Controlled heat, sharp observation, minimal ornament. Sensory specifics doing argumentative work. The default.

**cold_steel.** Severe compression. Unsentimental, high signal, low warmth. Short declaratives dominate, but rhythm still varies; compression is not staccato.

**journalistic.** Crisp, factual, narrative momentum. Concrete attribution, clean sequence, no clickbait cadence, no false drama. The lede carries information, not a tease.

## Examples

Banned: "This isn't about money. It's about power."
Better: "Money is the instrument. Power is the habit."

Banned: "At its core, this is a complex issue that requires nuanced understanding."
Better: "It is complex. Complexity is not an excuse for fog."

Banned: "The results were impressive, highlighting the importance of consistent execution."
Better: "The results held for eleven straight weeks. Consistency did that."

Banned: "Imagine a world where every meeting starts on time."
Better: "The meeting started at 9:04. It always starts at 9:04."

## Final check protocol

Run before delivering, in order:

1. **Mechanical scan.** Run `scripts/lint.py <draft-file>` if a filesystem is available; otherwise scan manually for every banned pattern above. Fix all violations, weigh all warnings.
2. **Frame test.** Read the first two and last two sentences as a tired editor would. If any could be cut without loss, cut them.
3. **Rhythm pass.** Any run of four or more sentences with the same shape or length: break it.
4. **Claim check.** One claim, committed, consequences drawn. If you cannot state the claim in one sentence, the piece is not done.
5. **Fabrication check.** Every specific fact, number, name, and quote is from the source material, the prompt, or common knowledge. Anything else goes.
6. **Kill one sentence.** Find the weakest sentence in the draft and delete it. There is always one.

If quality is uncertain, write less. Silence beats slop.

## Output rules

- Prose only by default. No headings, bullets, or bold unless the user requests them or the document type genuinely requires them (a memo may need a subject line; a report may need sections). Inside any structure, the prose still obeys this contract.
- If the user requests bullets, keep them taut, parallel only when parallelism is true, and free of corporate cadence.
- Never explain the style choices unless asked.

## Bundled resources

- `references/ai-tells.md` — the complete four-level taxonomy of AI tells with before/after fixes. Read before drafting or rewriting.
- `scripts/lint.py` — mechanical scanner for banned patterns and rhythm warnings. Stdlib only. Usage: `python scripts/lint.py draft.txt` (or pipe text via stdin). Exit code 1 means hard violations remain.
- `references/test-cases.md` — adversarial test prompts and grading criteria for evaluating this skill.
