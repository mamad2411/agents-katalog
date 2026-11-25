---
name: wiki-generation
description: Generate or update formal wiki notes from one `.cache/source-id-analysis.md` handoff document.
---

# Wiki Generation

This skill reads one analysis handoff document and completes the note-compilation pass.

## Read First

- `references/generation-rules.md`

## Input And Output

- Input: one `.cache/<source-id>-analysis.md`
- Output:
  - created or updated notes under `wiki/`
  - processing report at `outputs/processing/<source-id>-report.md`
  - archived source under `archive/`
  - archived analysis under `archive/.cache/`

## Workflow

1. Load one handoff artifact.
   Treat `.cache/<source-id>-analysis.md` as the direct input. Reopen the raw source only if the handoff is clearly insufficient.

2. Decide the edit scope.
   Separate the work into:
   - permanent notes
   - reference notes
   - argument notes
   - structure notes

3. Write or update permanent notes.
   - One reusable claim, distinction, method, step, or question per note
   - Check whether each candidate repeats, extends, corrects, narrows, or challenges an existing permanent note before creating a new file
   - Update an existing permanent note when the source adds clearer wording, stronger evidence, a caveat, an example, a correction, or a source link for the same reusable claim
   - Create a new permanent note only when the candidate carries a distinct claim, method, distinction, question, or role in an argument chain
   - Keep `## Summary` and `## Note`
   - Preserve important links and needed images
   - Use Markdown emphasis when it materially improves readability
   - Turn raw candidate note units from the analysis file into formal permanent notes

4. Write or update reference notes.
   Create or update `wiki/reference-notes/` only for stable named items such as books, frameworks, methods, models, acronyms, or long-lived coined terms.
   Treat each reference note as a source-context anchor for a named object, not as an entrance note, argument container, or摘抄堆.
   Use it to preserve:
   - what the named object is
   - where it comes from
   - its core definition, components, and boundaries
   - which permanent notes are distilled from it

5. Place notes into argument notes.
   - Judge from argument fit first
   - Insert notes into existing chains when possible
   - Create a new argument note when needed
   - Use broad parent-question or meta-claim titles
   - Prefer short, natural parent-question titles; keep the title simpler than the summary
   - Keep titles natural but still conceptually precise; do not overcorrect into chatty or overly colloquial wording
   - Allow branches or `---` segmentation when the reasoning should not be forced
   - `argument-notes` only connect upward to `structure-notes` and downward to `permanent-notes`
   - Do not create `argument -> argument` links as a substitute for merging or insertion
   - In each evidence item, explain the note's role in the chain directly
   - Do not use filler transitions such as “上一条已经…”, “接着”, or “然后”
   - Write `argument-note` summaries as direct conclusions, not as self-referential introductions about what the note is doing
   - Do not begin summaries with low-information scaffolding such as “这条论点笔记回答的问题是：”, “回答：”, “这条链处理……”, or similar template phrasing
   - This step owns the final decision about insertion order, branch shape, and `supports` / `next` structure
   - Treat analysis-file argument matches as candidates, not as final placement
   - If no existing argument fits, create or revise an argument note in the same pass
   - Treat each argument note as one stable parent question or parent claim with a readable reasoning chain, not as a topic bucket or note container
   - Put scope qualifiers, edge cases, and narrowed conclusions into `## Summary` and `### 论据`, not into the title unless they are the irreducible core of the parent question
   - Title the note as a question a real person would naturally ask, not as an internal analysis label or compressed explanation
   - Prefer direct, human wording such as `如何提升编程能力？`, `如何沉淀经验？`, `创作如何发生？`, `如何提升作品的传播度？`
   - Avoid double-question titles such as `为什么要学X，以及X能力如何长出来？`; prefer the shorter parent question and move the other half into `## Summary`
   - Avoid definition-plus-comparison titles such as `什么是X，X与Y有何不同？`; prefer the core definition question and let the comparison become supporting evidence
   - Avoid explanatory endings such as `如何…真正长出来`, `如何…稳定沉淀`, `如何…并被约束`, `如何…并形成…`, `如何…并提高…` when the simpler question is still the same question
   - Avoid abstract mechanism names such as `飞轮`, `闭环`, `框架`, `模型`, `可操作性层级`, `系统设计与维护边界` as titles unless that mechanism name is itself the exact object under discussion
   - If the title sounds like a sentence written by the analyst rather than a question asked by the reader, rewrite it

6. Attach argument notes to structure notes.
   Every new or updated argument note must be linked from at least one relevant `wiki/structure-notes/`.
   `structure-notes` only collect `argument-notes`; do not link them to other `structure-notes` or `permanent-notes`.
   Decide structure placement only after the final argument shape is stable.
   Treat each structure note as a theme note: define the theme boundary, state what it covers and excludes, and list the few argument notes that are the correct entry paths.

7. Write the processing report.
   Write `outputs/processing/<source-id>-report.md`.
   Include review blocks only for issues that cannot be resolved stably.

8. Finalize archival state.
   - move the processed source into `archive/`
   - move `.cache/<source-id>-analysis.md` into `archive/.cache/`
   - create `archive/.cache/` when needed

## Hard Rules

- Do not create orphan permanent notes.
- Do not create a new permanent note when an existing note can be updated without losing a distinct claim or argument role.
- Do not leave new argument notes unattached to the structure layer.
- Do not attach `structure-notes` to other `structure-notes`.
- Do not attach `structure-notes` directly to `permanent-notes`.
- Do not leave any `permanent-note` without at least one `argument-note` target; if no fit exists, create or revise an argument note in the same pass.
- Do not treat `source-analysis` candidate links as final chain instructions.
- Do not use narrow process-description titles for argument notes.
- Do not use unnatural, over-explained, or analysis-jargon argument titles.
- Do not treat argument notes as topic buckets or unordered note piles.
- Do not treat structure notes as portal pages, cross-link hubs, maintenance scratchpads, or raw note indexes.
- Do not silently drop source links, citations, or useful images.
- Do not use `wiki/reference-notes/` as an entrance layer.
- Do not use natural-language reference labels such as `来源文件：`, `来源链接：`, or `主题来源：`; normalize to `from` / `references` / `url`.
- Do not use `related_pattern` or other pseudo-structural link labels inside `reference-notes`.

## Completion Test

The pass is complete only when:
- wiki notes are updated as needed across permanent / reference / argument / structure layers
- new notes are placed into argument chains
- affected argument notes are attached to structure notes
- source provenance remains visible
- `outputs/processing/<source-id>-report.md` exists
- the processed source has moved to `archive/`
- the completed analysis file has moved to `archive/.cache/`
