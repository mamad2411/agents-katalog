---
name: write
description: "Use for rewriting and polishing prose in Chinese or English — removes AI-like wording, reviews product localization copy while preserving intent for drafts, docs, release notes, launch copy, and social posts. Not for code comments, commit messages, or inline docs. Trigger words: 帮我写, 改稿, 润色, 去AI味, 写一段, 审稿, 文档review, 本地化文案, 多语言文案, i18n copy, localization copy, check this document, 推特, twitter, X推文, tweet, social post, 连贯性, 段落连贯, draft, edit text, proofread, sound natural, polish, rewrite."
---

# Write: Cut the AI Taste

🥷 Strip AI patterns from prose and rewrite it to sound human.

## Outcome Contract

- **Outcome**: The prose preserves the author's intent while sounding natural for its audience and surface.
- **Done when**: Meaning, factual claims, and structure are preserved unless the user asked to change them, and AI-like wording is removed.
- **Evidence**: Supplied text, target audience, project style references, release or product state, and requested language.
- **Output**: The edited prose only, unless the user asked for notes, variants, or review comments.

## Core Stance

A catalog of smells, not a checklist. Use it to recognize AI taste, then make judgment calls.

- **Over-editing is failure.** If a sentence is natural, leave it. Most polish is subtraction, cutting repetition, summary-tone, restated conclusions.
- **The author's voice wins.** Keep colloquial words, cadence, and stance. When a rule conflicts with authorial or genre choice, the author wins.
- **Banned-phrase lists are examples, not find-and-replace.** Match the smell, not the string.
- **Prefer fewer, stronger edits.** Three changes that matter beat thirty mechanical swaps.

## Pre-flight

Three checks before editing. Detailed language-routing logic (which reference file to load per detected language/mode) is in [REFERENCE.md §Pre-flight](REFERENCE.md).

1. **Text present?** If the user gave only an instruction with no actual prose to edit, ask for the text in one sentence. Do not proceed.
2. **Audience locked?** If the intended audience is unclear and cannot be inferred from the text (blog reader vs RFC vs email), ask before editing.
3. **Language detected from the text being edited**, not the user's command. Follow the routing table in REFERENCE.md §Pre-flight to load the right reference file, then edit.

Read the loaded reference file. Then edit. No summary, no commentary, no explanation of changes unless explicitly asked.

## Context Setup

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate domain docs and identify project scope.

Voice and format constraints from durable context are `decision`, `preference`, and `principle` entries; editing checks are `pattern` and `learning`. The supplied text, audience, project docs, current release state, and source material override memory.

## Hard Rules

Five hard rules — meaning first, no silent restructuring, artifact-grounded claims, **no em-dash (U+2014) or en-dash (U+2013)** in output, stop after output. Full statements: [REFERENCE.md §Hard Rules](REFERENCE.md). Hard rules yield only to an explicit user instruction in the current turn; otherwise they override house style and catalog patterns.

## Modes

| Mode | Trigger | Reference File(s) |
|------|---------|-------------------|
| **Chinese prose** | Chinese text, general editing | `write-zh-prose.md` (always); `write-zh.md` only for deep rewrite / long-form |
| **English prose** | English text, general editing | `write-en.md` |
| **Bilingual review** | Mixed CN/EN, translation review | `write-zh-bilingual.md` |
| **Product localization** | "本地化文案", multi-locale review | `write-product-localization.md` |
| **Release notes** | "release", "changelog", "version" | Chinese → `write-zh-release-notes.md`; English → `write-en.md` §Release Notes & Social Posts |
| **Long-form article** | Multi-section Markdown, >300 lines | see REFERENCE.md |
| **Tweet / social post** | "推特", "tweet", "social post" | Chinese → `write-zh-release-notes.md`; English → `write-en.md` §Release Notes & Social Posts |
| **Public reply** | "回复 issue", "reply to PR" | see REFERENCE.md |
| **Document review** | "审稿", "check this document" | see REFERENCE.md |
| **Paragraph coherence** | "连贯性", "coherence" | see REFERENCE.md |

All mode procedures live in [REFERENCE.md §Mode Procedures](REFERENCE.md).

## Gotchas

| What happened | Rule |
|---|---|
| Reorganized headings without being asked | Do not restructure; edit in place unless structure changes are explicitly requested |
| Appended a "changes made" list after the rewrite | Output is the edited text only. No changelog, no commentary. |
| Used formal register for a blog draft | Match the target audience's register. Blog is conversational, not academic. |
| Applied Chinese/English spacing rules to a pure-English text | Bilingual spacing rules only apply when the text mixes Chinese and English |
| Polished the author's voice into generic launch copy | Preserve the author's cadence and stance |
| Drafted release or social copy from memory | Read the current release page, changelog, issue/PR before making factual claims |
| Polished a review report until it sounded timeless | Keep snapshots labeled as snapshots, or distill them into stable rules |

## Output

Return only the edited prose. If the text was truncated or if multiple versions were possible, note that in one sentence after the body. Otherwise, no wrapper, no preamble, no postscript.
