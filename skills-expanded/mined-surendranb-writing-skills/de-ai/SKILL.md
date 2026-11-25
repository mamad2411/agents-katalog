---
name: de-ai
description: Remove the patterns that mark text as AI-written, per Wikipedia's "Signs of AI writing" guide (WikiProject AI Cleanup). Use when the user says "de-AI this", "make it sound human", "remove the AI tells", or "this sounds like ChatGPT", and as the final pass after any other skill in this collection.
---

# De-AI

Say the specific thing, plainly, once.

## The core rule

**Replace every generic, important-sounding phrase with the specific fact, or cut it.** LLMs regress to the mean: they swap rare, concrete details for safe filler that could describe anything. This pass removes that filler without changing the facts, the meaning, or the style another skill set.

Workflow: `scan for the tells below` → `replace each with the plain fact, or delete it` → `re-check the upstream skill's rules` → `run the Verify checklist`.

## Mechanics

1. **Cut puffery.** Delete claims of significance the text does not prove: "stands as a testament", "plays a pivotal/crucial/vital role", "underscores its importance", "reflects broader trends", "enduring legacy", "has shaped discussions about".
2. **Use "is" and "has".** "The gallery is the exhibition space", not "serves as / stands as / functions as / represents". "It has six rooms", not "it boasts / features six rooms".
3. **Cut tacked-on "-ing" analysis.** Delete trailing clauses such as ", highlighting its importance", ", ensuring quality", ", reflecting its values", ", fostering community". If the point matters, give it its own sentence with evidence.
4. **No negative parallelisms.** Drop "not just X, but Y", "not X, but Y", and "Y rather than X" unless a reader really believed X. State Y.
5. **Break reflexive triples.** Use a list of three only when there are exactly three real items. Two or four are fine.
6. **Name the source or cut the claim.** No "experts argue", "observers note", "industry reports", or "several sources" when one source exists. Replace "associated with / connected to" with the actual relationship.
7. **Cut AI vocabulary.** Watch list, from the guide's per-model lists: delve, tapestry, testament, landscape (figurative), intricate, interplay, meticulous, pivotal, crucial, vibrant, boasts, bolstered, garner, underscore, showcase, highlighting, emphasizing, enhance, foster, align with, resonate, valuable insights, multifaceted, leverage, quietly, and "Additionally" to open a sentence. Use the plain word or nothing.
8. **No chatbot residue.** Strip "Certainly!", "Great question", "I hope this helps", "Let me know if", "Would you like", "Here is a", and "based on available information" hedges.
9. **No formula endings.** No "Despite these challenges..." wrap-up, no "future outlook" paragraph, no closing line that restates or moralizes.
10. **Fix formatting tells.** Sentence-case headings. No emoji on headings or bullets. Bold only what the reader must find. Vary punctuation as the sentence needs it: newer models that avoid em dashes overuse commas and periods, and that is also a tell.
11. **Never invent the fact.** Cut filler with no fact behind it. Flag a gap in brackets at the end only when the cut removes something the reader needs, such as an unnamed source for a claim the text depends on.
12. **The upstream skill wins.** If a rule here conflicts with the skill that wrote the draft, keep the upstream rule.

## Verify

- Zero literal hits from the puffery list (rule 1) and the vocabulary list (rule 7)
- Zero "serves as / stands as / boasts" where "is / has" works
- Zero sentence-final "-ing" clauses that add judgment, not fact
- Zero "not just X, but Y" and "not X, but Y" constructions
- Every opinion names who holds it, or it is gone
- Zero chatbot phrases
- The last sentence of the text (before any bracketed gap flags) adds information; it does not restate
- Facts, numbers, names, and meaning match the input; nothing new is invented
- The upstream skill's Verify checklist still passes

## Do not

- Override the upstream skill. Voice flourishes (Jack Sparrow's ornament, Yoda's inversions) and required shapes (a BLUF line, AP attribution) stay. Remove only the tells listed here.
- Swap a banned word for a synonym of the same weight ("crucial" to "essential"). Rewrite the sentence or cut it.
- Add typos, slang, or errors to "sound human". People write cleanly too.
- Treat perfect grammar, formal tone, or ordinary transitions as AI signs. The guide lists these as ineffective indicators.
- Aim to beat AI detectors. The goal is text a reader trusts.

## Example transformations

**Before:** "Nestled in the heart of the valley, the library stands as a testament to the town's enduring commitment to learning, serving as a vibrant hub that fosters community, creativity, and connection."

**After:** "The library is in the center of the valley. [Add what it offers and when it opened: the draft gives no facts.]"

**Before:** "Great question! Q3 revenue grew 18%, which wasn't just strong. It underscored our pivotal role in the evolving AI landscape, highlighting the team's dedication. Additionally, experts agree the outlook is bright. I hope this helps!"

**After:** "Q3 revenue grew 18%. [The outlook claim needs a named source: add one, or leave it out.]"

**Before:** "The new policy serves as a framework for remote work, ensuring flexibility, accountability, and alignment across teams. Core hours are 10:00 to 15:00, and managers approve schedules weekly."

**After:** "The new policy sets the rules for remote work. Core hours are 10:00 to 15:00, and managers approve schedules weekly."
