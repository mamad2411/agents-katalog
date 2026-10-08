---
name: russian-text-quality
description: Use when reviewing or writing code that contains Russian-language UI strings, i18n locale files (ru.json, ru.yml, ru.po), Russian comments, or transliterated identifiers (polzovatel, tovar, kolichestvo). Triggers on mixed English-code + Russian-content projects. Does not cover typography, spelling, or ё/е.
---

# Russian Text Quality Review

## Overview

Detects Russian-language quality bugs that general linters and LLMs consistently miss in code: broken pluralization in i18n locale files, case-agreement bugs in string concatenation, terminology drift across files, transliterated identifiers, and inconsistent language mixing. Code-aware, not prose-focused.

**Core principle:** structural Russian mistakes that survive `eslint` and type-checks but break production UIs. Prose quality is delegated to other tools.

## Activation

Run this skill ONLY if BOTH conditions hold:

1. The project contains **≥10 total Cyrillic characters** across code and locale files (excluding `node_modules`, `.git`, `dist`, `build`, and `.gitignore`d paths).
2. At least one file contains **≥5 consecutive Cyrillic characters** (rules out single stray tokens).

If either condition fails, respond with `Not activated — no Russian content detected` and stop. Never run on English-only projects.

Full activation pseudo-code: `references/activation-logic.md`.

## What this skill checks

| # | Check | Detection | Severity | Confidence |
|---|---|---|---|---|
| 1 | **Plural structure** — i18next/ICU/vue-i18n Russian plurals missing CLDR categories (`one`/`few`/`many`/`other`) | Deterministic parse of locale files + call sites | **Error** | High |
| 2 | **Terminology drift** — same source key translated to different Russian terms across files, or known-synonym variance | Normalized value comparison | Warning | Medium |
| 3 | **Concatenation case bug** — Russian preposition/verb governing non-nominative case followed by string interpolation | Heuristic regex + closed trigger list | Warning | Medium |
| 4 | **Language mixing** — inconsistent comment language in a single file, or inline Russian literals outside i18n | Per-file line-language ratios | Warning | Medium |
| 5 | **Transliterated identifiers** — `polzovatel`, `tovar`, `kolichestvo` etc. | Dictionary + phonotactic + file-context (3-tier) | Info | Low |

Full detection algorithms live in `references/plural-rules.md` (check #1), `references/concatenation-triggers.md` (check #3), and `references/mixing-and-transliteration.md` (checks #4 and #5). Check #2 terminology detection is described in the workflow below and in `.claude/russian-glossary.example.yml`.

## What this skill does NOT check

Delegate these to purpose-built tools:

| Out of scope | Recommended tool |
|---|---|
| Typography (« », em-dash —, non-breaking spaces) | [talkstream/ru-text](https://github.com/talkstream/ru-text) |
| Spelling | [yaspeller](https://github.com/hcodes/yaspeller) |
| ё/е restoration | [eyo / eyo-kernel](https://github.com/e2yo/eyo) |
| UX writing quality, translationese | [talkstream/ru-text](https://github.com/talkstream/ru-text) |

## Review workflow

1. **Check activation.** If conditions not met, stop.
2. **Detect i18n framework** from `package.json`: `i18next`, `react-intl`/`@formatjs/*`, `vue-i18n`/`@intlify/*`, or none. If multiple, run all applicable detection strategies.
3. **Run checks** against matching file targets. Skip checks whose file types are absent.
4. **Emit the Markdown report** in the format below.
5. **Do NOT modify files** without explicit user approval. Findings are suggestions except for `#1` plural scaffolding, which may be auto-applied only when the user approves.

## Output format

```
# Russian Text Review — <project name>

## Summary
- Files scanned: N
- Russian content detected in: M files
- Findings: X errors, Y warnings, Z info

## Findings

### Errors (must fix)
#### #1 Plural structure
- [HIGH] path/to/ru.json:L — key `items.count` missing `_few`, `_many` siblings
  - **Why:** Russian CLDR requires `one/few/many/other`. Missing `_few` produces wrong form for n=2,3,4.
  - **Fix:** add `items.count_few`, `items.count_many` entries (scaffolded below).

### Warnings
#### #5 Terminology drift
- [MEDIUM] locales/ru.json vs locales/admin/ru.json — key `user` translates to `пользователь` and `юзер`
  - **Why:** inconsistent terminology confuses users and breaks search.
  - **Fix:** pick one; lock via `.claude/russian-glossary.yml`.

### Info
#### #1 Transliterated identifiers
- [LOW] src/order.ts:12 — identifier `kolichestvo_tovarov` looks like transliterated Russian
  - **Suggestion:** `product_quantity` or keep Cyrillic if that is your project convention.

## External tools we recommend
- Typography / UX writing → talkstream/ru-text
- Spelling → yaspeller
- ё/е → eyo
```

The "External tools we recommend" block appears only when the scan finds Russian content. On English-only projects, the skill does not run at all.

## Common mistakes when using this skill

- **Running on English-only projects.** Honor the activation guard. Do not bypass it to "check anyway".
- **Flagging typography, spelling, or ё/е.** These are explicit non-goals — delegate, do not duplicate.
- **Treating medium-confidence heuristics as errors.** Checks #3, #4, #5 emit warnings or info; never promote them to errors.
- **Auto-fixing without approval.** Only `#1` plural scaffolding can be offered as an auto-fix, and only after the user approves the suggested diff.
- **Matching `key_plural` suffixes.** This skill targets i18next v4 format only. Old v3 projects using `key_plural` are out of scope in v1: when detected, emit a single `Info` finding noting the v3 file was skipped, then stop plural checks for that file.

## References

- `references/plural-rules.md` — CLDR Russian rules + per-framework detection algorithms (i18next, ICU, vue-i18n) with test cases. Includes Step 2.5 for locale values with count-placeholders but no plural siblings.
- `references/concatenation-triggers.md` — closed list of triggers for check #3 with exclusions
- `references/mixing-and-transliteration.md` — detection pseudo-code and thresholds for checks #4 and #5
- `references/transliteration-dict.yml` — seed dictionary used by check #5
- `references/activation-logic.md` — activation pseudo-code + test cases
- `references/examples.md` — 16 before/after cases sourced from real projects
- `.claude/russian-glossary.example.yml` — template for user-provided terminology glossary
