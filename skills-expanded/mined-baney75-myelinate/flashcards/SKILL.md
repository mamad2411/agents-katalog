---
name: flashcards
description: "Use when someone says make flashcards, a study deck, or Anki or Quizlet cards. Quick live drills belong to tutor; cards support recall after understanding."
---

# Flashcards

Cards exist for **durable recall of what the learner already understands**: fast, reliable access to facts, terms, relationships and steps so working memory is free for reasoning. A deck cannot create understanding, and a bad deck creates review debt and false confidence. Few, sharp cards beat many vague ones.

Paths like `references/…`, `templates/…` and `examples/…` are relative to this skill's folder, which carries its own copy of every file it names. Other Myelinate skills are siblings (`../tutor/SKILL.md`) and are installed as their own skills too. If a file is missing from your copy, work from this file and the router's core rules.

**Stand down when it isn't wanted.** If the person has said not to use Myelinate for this subject or kind of request, skip this skill's method and answer plainly; a slash command brings it back.

Evidence: retrieval practice and distributed practice are the two "high utility" study techniques (Dunlosky et al. 2013); repeated retrieval beats restudy at a week (Roediger & Karpicke 2006); successive relearning (3 correct recalls per item in the first session, then 1 correct recall in each of 3+ spaced sessions) raises college exam scores (Rawson & Dunlosky 2011; Rawson, Dunlosky & Sciartelli 2013). Card-writing rules below follow Matuschak ("How to write good prompts") and Wozniak ("20 rules of formulating knowledge").

## 0. Rules that override everything else

1. **Understand first, then card.** If the learner can't explain it, teach it (`tutor`) before carding it.
2. **One retrieval per card.** Atomic: one fact, one link, one step.
3. **Every back is checked** against the course source or a reliable reference before delivery.
4. **Course wording and notation** exactly as the course uses them; note where the textbook differs.
5. **Don't touch existing decks**: add new ones; never overwrite or merge without asking.
6. **Cards from their material point at it.** Each card names its passage in a source column or a small line on the back. Anything not in the material is marked *Outside your material:* or left out. If the material leaves something undefined, list that under the deck instead of inventing it. State the number of cards, and count them first. Add no units, conditions or derivations the material doesn't give; an application card is fine if the situation is marked as yours and the rule is theirs. In a learner's language other than English, keep every label in that language.

## 1. What makes a good prompt

- **Focused**: one detail. "Describe glycolysis" is twenty cards.
- **Precise**: one acceptable answer. Add context to rule out reasonable alternatives: "In the *proximal tubule*, roughly what fraction of filtered Na⁺ is reabsorbed?" → about two-thirds (~65%).
- **Consistent**: produces the same answer every review.
- **Tractable**: answerable ~90% of the time once learned; break hard items down or add cue words.
- **Effortful**: real retrieval. No yes/no. No front that gives the back away by pattern.
- **Short**: back ideally one line. A paragraph back is several cards.
- **No orphans**: each card serves an objective. Skip completionism.

## 2. Card types, mix them per concept

A concept deserves several angles; this is what turns cards into understanding scaffolds rather than trivia.

| Type | Front → Back example |
| --- | --- |
| Fact | On a topographic map, what does one contour line connect? → points of equal elevation |
| Mechanism / why | Why does adding a resistor in series lower current at fixed voltage? → total resistance rises, so I = V/R falls |
| Cause → effect | In a basic supply-demand model, if supply increases and demand stays fixed, what happens to equilibrium price? → it falls |
| Contrast | How does a primary eyewitness account differ from a later historical synthesis? → direct testimony from the event versus an interpretation drawing on sources |
| Application | A history essay quotes a 1910 speech. Is that speech a primary source for the speaker's stated view? → yes |
| Procedure step | After choosing a common denominator for fraction addition, what comes next? → rewrite both fractions as equivalents with that denominator |
| Cloze (closed list/sequence) | Water cycle: evaporation, {{c1::condensation}}, precipitation |
| Image occlusion | Masked structure on a diagram → its name (one mask per card) |
| Definition ↔ term | Reverse only when both directions are tested (vocab, drug ↔ class) |
| Hook-assisted | Target fact on the front/back; the mnemonic (`memory-hooks`) as an optional hint line on the back, never the answer itself |

**Interference control:** confusable pairs (primary/secondary sources, area/perimeter, mitosis/meiosis) get an explicit contrast card instead of two near-identical prompts.

**Image occlusion:** mask every instance of the label, image text, other labels that give it away by elimination, caption, alt text, filename. Use licensed or course-supplied images only (`find-media`).

## 3. How many and which

- Per lesson: typically 6 to 15 cards. Per exam: weight cards by the study guide, not by what's easy to card.
- Formula tiers and units: sort formulas into memorize, also know and provided, from the study guide itself, and give each its units. Mark units you worked out yourself as derived. With no study guide, label every formula as unsorted and ask; don't invent tiers. If they'll hand-write cards, show every formula inline, rendered as math, grouped by tier.
- Formulas: if the exam supplies an equation sheet, card what each term means, when the formula applies and which way the output moves, not the formula itself. If it doesn't, card the formula too. Don't know? Ask in one line while you build.
- Prioritize: high-yield facts the reasoning depends on, confusable distinctions, mechanisms' key "why"s, frequently tested values and steps.
- Leave out: things they'll look up, things they'll never be asked, anything they can derive in seconds.

## 4. Export formats

Ask which tool they use if unknown, but make the deck first. Default: a readable table plus an Anki-ready tab-separated block (question, answer, source), which also imports into Quizlet. If your host renders HTML inline, offer to run the cards right here with the flashcard view in `templates/inline-widgets.html`. Sets over ~20 cards: also deliver a file (`.txt`/`.tsv`/`.md`) and state the count.

**Study deck page** (they ask for a deck file or page, an exam deck they'll come back to, or no SRS app): copy `templates/flashcards-deck.html` and replace only the JSON in `<script type="application/json" id="deck">`: title, course, source, and the cards (`id`, `front`, `back`, optional `hint`, `tag`, `type`). Give every card a short stable `id` and keep it when you edit the deck: saved review dates follow the id. Build the JSON with a serializer (`json.dumps`, `JSON.stringify`) and write `<` as `\u003c`; by hand, every TeX backslash is doubled (`"\\(\\frac{a}{b}\\)"`), since JSON reads a single `\f`, `\n`, `\t`, `\b` or `\r` as a control character. The deck refuses a card only for `\f` or `\b`; a tab, carriage return or line break that looks like a swallowed backslash (`\theta`, `\rho`, `\nabla`) loads and appears in `deckAudit()` under `possibleLostBackslash`. The engine does the rest offline: commit before reveal, again/hard/good/easy with misses requeued, three correct recalls in the first session, a saved review ladder, a tag filter, a print-ready browse list, and Quizlet and Anki exports. Don't rewrite the engine or hand-build a deck page. If you can run a headless browser, call `deckAudit()` on the page before delivering: fix every `mathErrors` and `skipped` entry, and check each `rawTeX` (likely missing delimiters) and `possibleLostBackslash` entry against what you meant.

**Formulas.** Write math in TeX between `\( \)` (inline) or `\[ \]` (display): `\(p^2 + 2pq + q^2 = 1\)`, `\(\frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right)\)`. The deck page renders it as native math with no network, and its Quizlet export turns it into plain Unicode. In a Quizlet block you write yourself, use Unicode (p² + 2pq + q² = 1, Nₜ, Δ, →), never TeX. In an Anki file, set `#html:true` and keep `\( \)`; Anki renders it. In chat, use whatever the host renders; if raw `$`, `\frac` or `^{` would show, write Unicode instead. It renders fractions, roots, scripts, Greek, common operators and arrows, `\text`, `\mathrm`, `\mathbf`, `\vec`, accents, `\lim`, `\sum`, `\int` and `\binom`; write chemistry as `\mathrm{H_2O}`, not `\ce`, and write matrices and other environments in Unicode or as text, since they are not supported. Before delivering, open the deck's browse list: any formula shown as source or boxed in red as unsupported is a bug to fix, not a style.

**Quizlet** (Import → "Between term and definition: Tab", "Between cards: New line"):
```
Rate-limiting enzyme of glycolysis	PFK-1
Effect of ↓pH on O₂-Hb curve	Shifts right; more O₂ unloaded to tissue
```
No tabs or line breaks inside a card. If a back needs a line break, use a custom card separator (e.g., `;;`) and say so.

**Anki** (File → Import; a plain-text file):
```
#separator:tab
#html:false
#tags column:3
Rate-limiting enzyme of glycolysis	PFK-1	BIOL126::Exam2::Metabolism
```
Cloze cards go in a separate file with `#notetype:Cloze` and text like `Hemoglobin's Hill coefficient is about {{c1::2.7}}`. Hierarchical tags `Course::Exam::Topic`.

**Obsidian Spaced Repetition plugin**: `Question::Answer` (one line), `Question:::Answer` (also reversed), multi-line cards with a `?` line between front and back, `==highlight==` cloze; **separate every card with a blank line** (a multi-line card ends at a blank line); tag the note `#flashcards/<course>`.

**In-chat drill**: show fronts one at a time; learner answers; reveal and rate (again / hard / good / easy); misses requeue at the end of the round; finish with the miss list as a mini deck.

**Inside a lab** (`lab`): built-in review with a stored schedule (e.g., 1 → 3 → 7 → 14 → 30 days on "good", 10 minutes on "again"), plus Quizlet and Anki export buttons.

## 5. Scheduling and use

- Encourage an SRS (Anki/FSRS, Quizlet's spaced mode, Obsidian SR) over massed review.
- First session: 3 correct recalls per card. Then relearn to 1 correct in each of 3+ later sessions, days apart; adjust spacing to the exam date (`study-plan`).
- Say aloud or write the answer before flipping. Do not self-grade with "I knew that."
- Pair cards with application practice; cards alone don't produce transfer.
- Retire or rewrite cards that fail repeatedly (usually too big, ambiguous, or not understood). A leech is a teaching problem, not a discipline problem.

## 6. Quality check before delivering

- [ ] Every back verified against source; numbers and units correct
- [ ] Each card has exactly one answer; no yes/no; no giveaway fronts
- [ ] Mix includes why/contrast/application, not only facts
- [ ] No duplicates or near-duplicates; confusable pairs have contrast cards
- [ ] Format imports cleanly (one tab per line for Quizlet; headers for Anki)
- [ ] Every formula renders as math: no raw `$`, `\frac` or `^{` on screen, nothing flagged unsupported in the deck page
- [ ] Count stated; tags/course labels applied

## Anti-patterns

Paragraph backs · yes/no cards · cards before understanding · copying slide bullets verbatim as cards · 300-card decks for a 4-chapter exam · mnemonic as the answer · ambiguous prompts that accept several answers · reverse cards by default · overwriting the learner's existing decks.
