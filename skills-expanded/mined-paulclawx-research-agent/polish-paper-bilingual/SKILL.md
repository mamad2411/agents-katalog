---
name: polish-paper-bilingual
description: Use this skill when the user wants to polish Chinese academic writing, convert Chinese research drafts into fluent English paper prose, rewrite English sections into clearer Chinese, or perform bilingual academic rewriting for abstracts, introductions, methods, experiments, conclusions, and rebuttals while preserving the original technical claims.
---

# Polish Paper Bilingual

## Overview

This skill is for Chinese-first academic writing and bilingual paper revision. It improves clarity, structure, formality, and readability in Chinese, and it also supports high-fidelity Chinese-to-English or English-to-Chinese academic rewriting.

Use it when the user needs polished research prose across both languages without changing the science, claims, notation, or evidence.

## When To Use

Use this skill when the user asks for any of the following:

- Polish a Chinese paper draft
- Rewrite Chinese academic text to sound more natural and publishable
- Translate Chinese draft text into conference-style English
- Translate English paper text into precise Chinese
- Perform side-by-side bilingual rewriting
- Improve a Chinese or bilingual rebuttal response
- Turn mixed Chinese and English notes into coherent academic prose

Prefer `polish-paper` instead when the draft is already fully in English and the user only needs English-language polishing.

## Inputs

Gather as many of these as available:

- Source text
- Source language and target language
- Paper title or topic
- Section type such as abstract, intro, method, experiments, conclusion, or rebuttal
- Venue or target style such as NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR, or journal style
- Constraints on length, tone, literalness, or editing strength
- Terms, notation, dataset names, and model names that must stay unchanged
- Whether the user wants polished Chinese only, translation only, or bilingual output

If the source is rough, fragmentary, or mixed-language, normalize it conservatively rather than inventing missing scientific content.

## Default Workflow

Follow this sequence unless the user asks for only one part:

1. `Language Lock`
   Identify source language, target language, audience, and terms that must remain unchanged.
2. `Meaning Extraction`
   Separate the real technical content from rough phrasing, direct translation artifacts, and spoken-style filler.
3. `Academic Rewrite`
   Rewrite in the target language with cleaner structure, stronger flow, and venue-appropriate tone.
4. `Terminology Check`
   Verify that notation, method names, datasets, metrics, and claims remain faithful and consistent across languages.
5. `Bilingual Alignment`
   If bilingual output is requested, ensure the Chinese and English versions match in meaning and emphasis.

## Working Rules

- Preserve scientific fidelity. Do not add claims, results, baselines, citations, or limitations not present in the source.
- Do not translate technical names mechanically when standard academic usage prefers the original English term.
- Keep equations, symbols, model names, dataset names, and metric names unchanged unless the user asks otherwise.
- Prefer natural academic prose over literal sentence-by-sentence translation.
- Remove Chinglish, spoken phrasing, redundancy, and weak connective language.
- When translating into English, prefer concise conference-style wording over textbook or overly ornate phrasing.
- When translating into Chinese, prefer precise written academic Chinese over colloquial or over-literal wording.
- If a phrase is ambiguous in the source, rewrite conservatively and avoid inventing intent.

## Output Modes

- `zh-polish`: polish Chinese academic writing only
- `zh-to-en`: convert Chinese draft text into polished English paper prose
- `en-to-zh`: convert English academic text into precise Chinese
- `bilingual-side-by-side`: provide aligned Chinese and English versions
- `rebuttal-bilingual`: professional bilingual author-response style
- `with-rationale`: revised text plus short notes on major wording choices

## Reference File

When you need reusable prompt patterns, read:

- [references/prompt-templates.md](./references/prompt-templates.md)

Use that file for Chinese-only polishing, Chinese-to-English rewriting, English-to-Chinese rewriting, and bilingual rebuttal templates.
