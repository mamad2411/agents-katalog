---
name: chinese-formal-document-format
description: 中文正式文档排版（Chinese formal-document formatting）。保守地整理中文正式 DOCX 的页面、字体、字号、固定行距、标题层级、落款、日期和表格，参照 GB/T 9704-2012，但不改写正文。当用户上传中文 DOCX 并说“排版、排一下、整理格式、调格式、公文格式排版、党政机关公文格式、按国企排版”，或要求整理报告、方案、函、通知、请示、会议纪要，或提到仿宋_GB2312、楷体_GB2312、方正小标宋简体、固定值28磅、一、（一）1.（1）层级时使用。输出格式化 DOCX 和核验报告，保留原文、数字、标点、段落、表格及页眉页脚。
compatibility: Requires python-docx 1.1.2 or later. A DOCX renderer is optional for visual checking.
---

# 中文正式文档排版

> 鼓翼成长星球 · 出品与持续维护

Apply the reference typography in `profiles/default.json`. The core promise is:

**Change typography. Preserve the document's textual content and structure.**

This skill is for Chinese formal documents and workplace materials that want a public-document-inspired layout. It covers official documents, reports, plans, letters, meeting minutes, notices, requests, summaries, and other structured drafts. It is not a legal-compliance certificate and does not replace the issuing organization's current document-control rules.

## Brand attribution

This share version is curated and maintained by 鼓翼成长星球. Apply the brand to this Skill's documentation, README, release notes, manual, and sharing materials. Keep the user's formatted DOCX content-identical unless the user explicitly requests a separately branded template.

## Runtime selection

Read `references/runtime-notes.md` if the current environment is not obvious.

- If Python and shell execution are available, use the bundled scripts. This is the deterministic path.
- If an in-app Word editing tool is available, use it only when it can preserve source text exactly and report the same page, font, spacing, and indent checks.
- If neither path is available, ask the user to open the file in an environment with DOCX file output. Do not approximate the formatting in chat.

## User-facing language

For Chinese documents and Chinese-speaking users, write explanations, warnings, questions, and final summaries in Chinese by default.

Keep code, CLI flags, file paths, JSON keys, profile keys, font names, and other machine-facing identifiers unchanged. The English `SKILL.md` and English reference files remain the executable source of truth; `*.zh-CN.md` files are user-facing Chinese guides. See `docs/localization-policy.md`.

## Workflow

### Step 1: Protect the source

Work on a copy. Never overwrite the user's source DOCX.

Completion criterion: the input file remains unchanged and the intended output path differs from it.

### Step 2: Identify the document

Inspect the title, recipient, hierarchical headings, metadata block, closing phrase, signature, and date.

Use the user's explicit document type when supplied. Otherwise run with `--doc-type auto`.

Do not classify a paragraph as a heading from its number alone. A short standalone label such as `1. 完成情况` may be a level-3 heading. A complete numbered sentence such as `1. 由市场部牵头，于10月25日前完成任务。` is body text and keeps the body font.

🔴 CHECKPOINT · ASK when:

- No title or date exists and the material appears to be a final outgoing document.
- A line could be either a heading or body data.
- Report and request-for-approval language are mixed.
- The document type changes the structure the user expects.

Ask one concrete question, such as: “标题‘关于XX的请示’带有报告式正文，文种按请示还是报告处理？”

Do not silently invent missing content or choose a materially different document type.

Completion criterion: the document type and any material structural ambiguity are resolved.

### Step 3: Format with the script

Run commands from the skill root, or replace `scripts/...` with the absolute path to the script:

```bash
cd /path/to/chinese-formal-document-format
```

Use the default reference profile:

```bash
python scripts/format_docx.py input.docx output.docx --strict
```

Use an organization override:

```bash
python scripts/format_docx.py input.docx output.docx \
  --profile profiles/example-org.json --strict
```

Override an uncertain type:

```bash
python scripts/format_docx.py input.docx output.docx --doc-type report --strict
```

If a multi-line title is stored as separate paragraphs rather than ordinary line wrapping, add `--title-lines N` to both the formatter and verifier.

The script writes the formatted DOCX and `<output>.format-report.json`. It compares the full textual structure before and after saving. If any paragraph, table cell, row, column, or header/footer text changes, it stops and does not produce a successful output.

Completion criterion: the command exits successfully, the output DOCX exists, and the report says `content_integrity.passed = true`.

### Step 4: Verify the typography

```bash
python scripts/verify_docx.py output.docx --reference input.docx
```

The verification checks:

- every body paragraph and table cell text remains identical;
- paragraph order, table dimensions, merged-cell layout, and header/footer text remain identical;
- A4 page size and the configured margins;
- expected Chinese font names and point sizes;
- exact line spacing;
- alignment and first-line/right-side character indents;
- table header/body fonts.

Completion criterion: `status = passed` and every check in the report is true.

### Step 5: Visual check when a renderer is available

Prefer the bundled font-aware previewer:

```bash
python scripts/render_preview.py output.docx preview/
```

This command creates a temporary `fontconfig` that includes macOS, Windows, or Linux font directories, then converts through LibreOffice when available. On macOS it falls back to Quick Look for a first-page thumbnail.

Inspect the pages at readable zoom. Check Chinese glyphs, clipping, table wrapping, page breaks, and unexpected font substitution.

If the previewer still shows tofu, use Word or WPS on a machine with the configured fonts. Keep the correct font names in the DOCX; changing them to the renderer's fallback would make the deliverable wrong. Record the visual-check limitation and finish with structural verification.

Completion criterion: pages are visually clean, or the renderer limitation is explicitly reported.

### Step 6: Report the result

Return:

1. the formatted DOCX;
2. the JSON verification report;
3. a short note covering document type, page setup, heading levels, content-integrity status, warnings, and any visual-check limitation.

List content problems separately. Do not fix them:

- date format deviations;
- report containing request language;
- inconsistent names or numbers;
- ambiguous heading levels;
- missing signature or date.

## Character-indent implementation

Write both attributes when applying a character indent:

```xml
<w:ind w:firstLineChars="200" w:firstLine="640"/>
```

`firstLineChars` expresses the Chinese character intent; `firstLine` is the physical renderer fallback. For right indents, use `rightChars` plus `right`.

## Profiles and organization variants

Read `references/customization.md` when a unit has its own font, margin, line-spacing, or indent requirements.

The default profile is a reference, not a claim of universal compliance. Name a custom profile after the organization and record who approved it.

## Failure handling

| Trigger | First response | If still blocked |
|---|---|---|
| `python-docx` missing | Install from `requirements.txt` | Run in a runtime that provides document dependencies |
| `.doc`, PDF, or scanned image | Ask for an editable DOCX | Convert first, then verify extracted text against the source |
| Password-protected or corrupt file | Ask the user to unlock and resend | Stop; do not manufacture a replacement |
| Tracked changes, content controls, or text boxes detected | Format a clean copy and report the affected regions | Ask the user to accept changes or flatten controls before final use |
| Complex merged table changes unexpectedly | Stop before saving | Preserve the original table and hand-format only safe cells |
| Font unavailable on the target device | Keep the configured font name in the DOCX | Report substitution risk; never silently change to a different typeface |
| Renderer shows Chinese tofu | Keep correct font names and use structural verification | Ask the user to inspect in Word or WPS |
| Same-line level-2 heading contains a hyperlink, field, or comment | Keep the paragraph intact and report the mixed-format limitation | Ask whether preserving the field or splitting the paragraph is more important |
| Numbered line could be a heading or body | Treat complete sentence-like items as body; ask only when the visual hierarchy is still unclear | Preserve the numbered text and report the chosen role |
| Content-integrity check fails | Stop | Diff the affected blocks; never ship the compromised output |

## Blacklist

Reverse these failure modes into positive behaviour:

- Keep the author's prose, punctuation, numbering, dates, names, and paragraph breaks exactly as written.
- Treat ambiguous content as a question for the user.
- Put the formatted copy in a new file.
- Use the configured organization profile instead of universal assumptions.
- Report missing fonts and unsupported document structures.
- Preserve fields, hyperlinks, tracked changes, comments, and table merges unless the user explicitly authorizes a structural change.
- Deliver a DOCX only after content and structure checks pass.

Do not:

- rewrite, shorten, polish, translate, or standardize the text;
- change `1、` to `1.`, zero-padded dates, organization names, or terminology;
- add `特此报告`, recipients, signatures, red headers, page numbers, or attachments;
- merge or split paragraphs to make the layout easier;
- replace an unavailable font silently;
- claim legal or formal-document compliance from a successful script run;
- overwrite the source file.

## References

- `references/format-spec.md` — exact reference typography.
- `references/document-structures.md` — structural expectations and fallback for other document types.
- `references/conservative-rules.md` — content-preservation boundary.
- `references/customization.md` — organization profiles.
- `references/runtime-notes.md` — Codex, Claude, Word add-in, and chat upload notes.
