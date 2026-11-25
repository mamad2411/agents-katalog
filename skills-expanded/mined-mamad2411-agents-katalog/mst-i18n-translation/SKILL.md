---
name: mst-i18n-translation
description: Detect i18n key changes (t(), <Trans i18nKey>) and potential untranslated strings in the current git branch diff for react-i18next projects. Outputs a structured JSON with added keys (with AI-translated values for each locale) and removed keys. Use when the user asks to collect i18n translations, run translation diff, check for missing i18n keys, or mentions "mst-i18n-translation".
---

# i18n Translation Collect

Detect i18n key changes in the current git branch and generate a translation report JSON with AI-powered translations for all configured locales.

## Prerequisites

- **Git** repository with a clean HEAD (uses `git diff` to detect changes)
- **Node.js** 18+
- **TypeScript** npm package installed in the project (`import * as ts from 'typescript'`)
- **ripgrep** (`rg`) installed on the system
- **react-i18next** project structure with `src/locales/<lang>/*.json` locale files

## Modes

### Default Mode (collect + translate only)

Trigger: user runs the skill without extra arguments.

1. Execute: `node "<skill-dir>/scripts/run.mjs"`
2. Read the generated `.runtime/translation-collect.json`
3. For every non-`en` language in `add`, translate the English values into the target language and write back to the JSON
4. Validate no empty values remain, then open the result file in the editor

### Apply Mode (collect + translate + write to locale files)

Trigger: user provides a target JSON filename (e.g. `account.json`).

1. Execute: `node "<skill-dir>/scripts/run.mjs" --no-open`
2. Read `.runtime/translation-collect.json`
3. Translate all non-`en` empty values and write back
4. Execute: `node "<skill-dir>/scripts/apply-locale-updates.mjs" "<target-filename>"`
   - Matches `<target-filename>` under `src/locales/<lang>/` (recursive)
   - `add`: inserts or overwrites keys in matched files
   - `removed`: deletes keys present in the matched files
   - If no matching file exists, creates `src/locales/<lang>/<target-filename>` for each language

## Output JSON Structure

```json
{
  "add": {
    "en": { "key1": "English text", "key2": "Another text" },
    "de": { "key1": "", "key2": "" },
    "ja": { "key1": "", "key2": "" }
  },
  "removed": ["obsolete.key1", "obsolete.key2"]
}
```

- `add` — new keys per locale; `en` carries the original text, other languages are empty placeholders for the agent to fill via translation
- `removed` — keys that no longer appear in source and can be pruned from locale files

The `.runtime/` directory is ephemeral (gitignored) and should not be committed.

## Translation Quality Requirements

### Core Translation Principles

- Translate accurately, naturally, and fluently into the target language.
- The translation must sound native to the target market, not like a literal English translation.
- Preserve the original meaning, intent, tone, and marketing purpose.
- Use clear, professional, website-ready language suitable for a PDF software company.
- Prefer concise, benefit-oriented wording for headings, buttons, CTAs, and UI labels.
- Avoid overly formal, awkward, or machine-translated phrasing.

### Terminology

- Keep `Foxit` unchanged.
- Keep official product names such as `Foxit PDF Editor` unchanged unless the target locale has an approved official translation:
  `Foxit PDF Editor`, `Foxit PDF Editor+`, `Foxit PDF Reader`, `Foxit eSign`, `Foxit PDF SDK`, `Foxit AI Assistant`, `PDF Editor`, `PDF Editor+`, `PDF Editor Suite`, `PDF Editor Pro`, `PDF Editor Pro+`, `PDF SDK`, `PDF IFilter`, `PDF Compressor`, `eSign`, `eSign Business`, `eSign Essentials`, `AI Assistant`, `Smart Redact`, `Maestro Server OCR`
- Keep common file format names unchanged: `PDF`, `JPG`, `PPT`, `Excel`, `Word`, `PowerPoint`, `HTML`, `RTF`, `OCR`.
- Use consistent translations for repeated content (or similar content) within the same file or across different files.
- Maintain a professional software/SaaS terminology style.

### Website and Marketing Style

- Headings should be natural, clear, and compelling in the target language.
- CTAs should be short and action-oriented.
- FAQ answers should be clear, direct, and helpful.
- Feature descriptions should emphasize user benefits, not just literal functions.
- Keep SEO intent where possible, especially terms related to PDF compression, conversion, editing, security, online tools, and file size reduction.
- Avoid keyword stuffing; SEO terms should read naturally.

### Locale Quality

- Adapt grammar, punctuation, capitalization, spacing, and quotation marks to the target language.
- Use native punctuation conventions where appropriate.
- For German, French, Italian, Spanish, etc., avoid English sentence structure when it sounds unnatural.
- For UI labels, keep translations compact enough for buttons, tabs, menus, and cards.
- Preserve measurements, numbers, product trial periods, and limits exactly unless localization is explicitly requested.

### Accuracy and Safety

- Do not exaggerate claims beyond the English source.
- Do not weaken legal, privacy, security, or compliance statements.
- Preserve meaning for sensitive statements about encryption, deletion, privacy, compliance, file handling, and data security.
- Do not introduce new features, guarantees, prices, or availability information.

### Key Notes for Each Language

#### ar (Arabic)

- Use RTL writing. When embedding English product names, let the browser handle bidirectional text; do not manually reverse the character order of English text.
- Use Arabic punctuation marks: `،`, `؛`, `؟`. Avoid half-width `,;?`.
- Keep numerals consistent within the same file; do not mix ASCII digits with Arabic-Indic digits.

#### de (German)

- **Capitalize all nouns** (including common nouns and compound nouns); do not copy English lowercase usage.
- Use hyphens when combined with English abbreviations (`Cloud-Speicher`), but keep official Foxit product names fully in English without hyphens (`Foxit PDF Editor`, not `Foxit-PDF-Editor`).
- Use quotation marks `„…“`; use the formal pronoun `Sie` consistently.

#### es (Spanish)

- Questions and exclamations must use both opening and closing marks: `¿…?`, `¡…!`; never omit the opening mark.
- Use neutral international Spanish by default, with the formal pronoun `usted`.
- Use the infinitive form for UI buttons (`Descargar`, `Suscribirse`).

#### fr (French)

- Insert a **non-breaking space** (U+00A0 or U+202F) before `:`, `;`, `?`, `!`, and `»`, for example: `Ventes :`, `Continuer ?`.
- Use quotation marks `« … »` (with non-breaking spaces inside).
- Use the formal pronoun `vous`; use the infinitive form for UI buttons (`Télécharger`, `S'abonner`).
- Use a narrow non-breaking space for thousands separators in large numbers (`1 000`); prefer the ellipsis character `…` (U+2026).

#### it (Italian)

- Use the formal pronoun `Lei`; punctuation should be half-width, without French-style spacing rules.
- Keep UI button style consistent across the site (imperative or infinitive).

#### ja (Japanese)

- Use full-width punctuation `。、？！`; quotation marks should be `「」` / `『』`.
- Whether to insert a half-width space next to English text should follow the existing style; do not mix styles within the same file.
- Use polite style (`です・ます`) by default; for katakana loanwords, follow JIS conventions for long vowels (`エディター`, `ユーザー`, `サーバー`).

#### nl (Dutch)

- Use the formal pronoun `u`; common compound nouns tend to be written as one word or with hyphens (`PDF-bewerker`), while official Foxit product names remain in English.
- Use either `'…'` or `"…"` quotation marks, consistently with the rest of the site.

#### pt (Portuguese)

- This project uses **Brazilian Portuguese (pt-BR)**, so follow pt-BR conventions.
- Use the second-person pronoun `você`; use the infinitive form for UI buttons (`Baixar`, `Assinar`, `Inscrever-se`).

#### ru (Russian)

- Use quotation marks `« … »`; use the em dash `—`, distinct from the hyphen `-`.
- Translations are often 30-50% longer than the English source, so pay attention to UI space constraints; however, **do not omit key information just to shorten the text**.
- Keep usage of `вы` / `Вы` consistent with existing site terminology.

#### zh-TW (Traditional Chinese / Taiwan)

- **Traditional Chinese characters** must be used; Simplified Chinese is not allowed.
- Follow Taiwan terminology: `軟體`, `資訊`, `儲存`, `電子郵件`, `下載`, `影片`, `滑鼠`, `預設`, `範本`; avoid Mainland China terms such as `软件`, `信息`, `存储`, `邮箱`, `视频`, `鼠标`, `默认`, `模板`.
- Use full-width punctuation `，。；：？！`; quotation marks should be `「」` / `『』`.

## What the Scripts Detect

| Category                     | How                                                                                                                                                  |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **i18n keys**                | `t('...')` calls and `<Trans i18nKey="...">` JSX usage via TypeScript AST                                                                            |
| **Potential config strings** | String literals and JSX text not wrapped by `t`/`Trans`, filtered by heuristics (skips class names, URLs, routes, Tailwind utilities, imports, etc.) |
| **Removed keys**             | Keys present in HEAD but absent in the working tree; config strings confirmed unreferenced via `rg`                                                  |

## Scripts Reference

| Script                                 | Purpose                                                                                         |
| -------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `scripts/run.mjs`                      | Entry point — collects changed files, extracts keys, writes `.runtime/translation-collect.json` |
| `scripts/apply-locale-updates.mjs`     | Applies `add`/`removed` from the report into the project's `src/locales/**` JSON files          |
| `scripts/collect-changed-files.mjs`    | Lists `src/**/*.ts(x)` files changed vs HEAD (staged + unstaged + untracked)                    |
| `scripts/extract-i18n-keys.mjs`        | Extracts `t()` / `<Trans>` keys from TS/TSX via TypeScript compiler API                         |
| `scripts/extract-potential-config.mjs` | Extracts untranslated string literals with natural-language heuristics                          |
| `scripts/ar-lrm-postprocess.mjs`       | Inserts LRM marks for Arabic locale around LTR tokens (product names, phone numbers)            |
