---
name: wiki-rank
description: Reduce one theme or domain concept to its irreducible generators, then use that explanation to distinguish it from adjacent concepts and infer natural theme boundaries. Use when the user asks for 降秩, 秩是什么, 背后是什么, or when reviewing an old theme concept or proposing a new theme concept before deciding theme boundaries and argument scope.
---

# Wiki Rank

Use this skill for concept-level reduction.
Do not use it for routine source extraction, ordinary unresolved generation leftovers, or repository-wide auditing.

## Input And Output

- Input: one theme concept, domain concept, or proposed parent-question concept
- Optional context: the minimum neighboring theme notes, argument notes, or permanent notes needed to distinguish the concept
- Output: a concise analysis file in `outputs/analysis/` unless the user asks for a different path

## Core Question

The task is not to list key points.
The task is to find the smallest set of independent generators that can regenerate the observed phenomena of the concept.

## Four Tests

All four must pass:

1. `generation`
   The generators can explain the major observed phenomena of the concept.
2. `minimality`
   Remove any one generator and something important becomes unexplained.
3. `independence`
   The generators can vary independently in real cases.
4. `predictive coverage`
   The generators can explain likely phenomena beyond the initial list.

## Workflow

1. Name the concept.
   State what concept is being reduced and what is not being judged yet.

2. List the main phenomena.
   Keep this short. Only include the recurring phenomena that the concept must explain.

3. Propose candidate generators.
   Compress the concept until the remaining generators still explain the phenomena.

4. Run the four tests.
   If one fails, revise the generators.

5. Distinguish the concept from adjacent concepts.
   Explain where the nearest existing themes or parent questions differ at the generator level.

6. Derive boundary implications.
   State what naturally belongs inside the concept boundary and what should stay outside.

## Use Order In This Repository

Use `wiki-rank` before structural decisions when the concept itself is unclear.

1. `wiki-rank`
   Use first when reviewing an old theme concept, proposing a new theme concept, or deciding whether two neighboring themes are actually different concepts.
2. `wiki-review`
   Use second to convert the rank result into a concrete decision: merge, split, rename, defer, or define argument range.
3. `wiki-generation` or direct wiki edits
   Use last only after the concept boundary is clear.

Do not insert `wiki-rank` into the normal `source-analysis -> wiki-generation` path unless the source is explicitly forcing a theme-concept review.

## Output Style

- Prefer short markdown prose over templates unless the user asks otherwise.
- Keep the analysis concept-first, not file-first.
- Do not drift into a long essay if a tighter explanation is enough.
- If the result is being used for theme review, end with:
  - the concept's generators
  - the nearest contrasting concept
  - the implied boundary
  - the likely argument range
