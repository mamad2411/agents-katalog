---
name: originality-guard
description: Use automatically whenever Claude writes or rewrites text that could overlap existing sources - articles, essays, thesis/proposal sections, literature reviews, reports, web content, summaries of papers or pages. Keeps writing original (own wording and structure), quotes and cites anything borrowed, and runs a self-check plus optional web search of distinctive sentences. Not a replacement for Turnitin/Copyscape, and not for code or facts that have only one correct wording.
---

# Originality Guard

## Purpose
Produce plagiarism-safe text: ideas credited, wording and structure original, quotations marked. Gives a practical first-pass check; it cannot guarantee a score from a commercial checker.

## When to use
Writing from sources, summarizing or paraphrasing papers/pages, academic writing (thesis, proposal, literature review), web articles, reports, any rewrite of user-supplied text.

## When NOT to use
- Code and standard formulas, legal clauses and definitions that must be quoted exactly (quote and cite them instead).
- Pure brainstorming with no sources.

## Inputs
The topic or draft, the sources the user gave (links, files, notes), citation style if academic (APA, IEEE, Harvard), allowed quote length.

## Core workflow
1. Collect sources first; keep a source log (author, title, year, URL/DOI, what was taken: idea, data, quote).
2. Read and understand the source, then write from your notes in your own structure, not sentence by sentence next to the source.
3. Paraphrase properly: change structure and vocabulary, not just synonyms; keep terms of art unchanged.
4. Quote only when the exact words matter: use quotation marks, keep short (under ~25 words), cite page/section.
5. Cite every borrowed idea, statistic or figure at the point of use; add a references list in the requested style.
6. Self-check: no run of 8+ identical words from any source unless quoted; no source structure copied paragraph by paragraph; claims are traceable to the log.
7. If web search is available, search 2-4 distinctive sentences in quotes; if matches appear, rewrite those passages or quote and cite them.
8. Report what was checked and what was not.

## Decision rules
- Common phrases and definitions are fine; distinctive phrasing, argument order and examples must be the user's own or cited.
- Never invent a citation, DOI, quote or statistic. If a source cannot be verified, say so and drop or flag the claim.
- Self-plagiarism: reusing the user's earlier work needs their permission and a citation if submitted elsewhere.
- Prefer the user's own data, experience and examples; they make text original by construction.

## Edge cases and failure handling
- Source is inaccessible (paywall) -> cite only what is verifiable from the abstract/metadata and mark the rest as unverified.
- Heavy overlap in a definition -> quote it with citation or restate once in own words with citation.
- Translated source text -> still a source; cite it and do not copy a translation word-for-word.
- User wants "zero similarity" -> explain that quotes, references and common terms always create some similarity; aim for original wording and correct attribution, not a number.
- Academic integrity rules (university, journal) apply; follow disclosure requirements for AI assistance.

## Validation
- Source log complete; every citation resolves to a real source.
- Spot-check passages against sources: no long verbatim runs outside quotes.
- References list matches in-text citations.

## Output requirements
Text with in-text citations and a references list; one short note listing checks done (self-check, web search yes/no) and any unverifiable claims.

## Example
```text
Source: "Federated learning enables training across decentralized devices without sharing raw data."
Own wording (cited): Models can be trained where the data lives, with only model updates leaving each device (McMahan et al., 2017).
Quote (only if exact words matter): the authors define it as "training across decentralized devices" (p. 2).
```

## Related skills
`citation-management`, `literature-review`, `peer-review`, `human-writing-mode`, `docs-pdf-clean-output`.
