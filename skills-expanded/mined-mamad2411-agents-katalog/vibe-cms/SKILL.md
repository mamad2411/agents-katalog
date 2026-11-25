---
name: vibe-cms
description: Generate and manage "CMS documents" — Markdown files that serve as a simple content management interface for non-technical collaborators in Vibecoding workflows. Use this skill whenever the user wants to inventory, review, or batch-update frontend copy (UI text, button labels, placeholder text, error messages, aria-labels, page titles, AI prompts, or any other user-facing strings hardcoded in source files). Also trigger when the user says things like "list all the text in my app", "I want to change the wording", "make a copy doc", "generate a content inventory", "let someone else edit the text", "backfill copy from the doc", or "apply the CMS document". This skill works with any frontend framework (React, Vue, Svelte, Next.js, plain HTML, etc.).
---

# Vibe CMS — Content Management through Markdown Documents

> *跨过代码，在 Vibecoding 中实现精确内容管理。*

## What this skill does

This skill turns a coding agent into a lightweight CMS engine. It has three modes:

1. **Scan & Generate (扫描生成)** — Crawl the project source code, extract every piece of hardcoded user-facing text, and produce a structured Markdown document (the "CMS document") that a non-technical person can edit directly.
2. **Backfill & Apply (回填执行)** — Read an edited CMS document, diff the "建议新文案" column against the "当前文案" column, and batch-replace the text in the source files.
3. **Incremental Update (增量同步)** — After new code is added, scan only for new strings and merge them into the existing CMS document without overwriting any edits already made.

The CMS document is the single source of truth that bridges the gap between developers and content editors (copywriters, product managers, domain experts). It requires zero coding knowledge to edit — just open the `.md` file and type in the table cells.

---

## Phase A: Scan & Generate

When the user asks you to generate a CMS document (or inventory the frontend copy, or make a content doc, etc.), follow these steps:

### A1. Identify the scan scope

Silently infer the scan scope from the project context. Default to typical source directories like `src/`, `app/`, `pages/`, `index.html`, and prompt config files (e.g., `prompts.js`, `i18n/`). 
Always exclude: `node_modules/`, `dist/`, `build/`, `.git/`, test files, and other non-source directories.

**Only ask the user** if the project structure is highly unusual, ambiguous, or if multiple distinct frontend apps exist in the workspace and you don't know which one they mean. Otherwise, proceed silently with your inferred defaults to save the user time, but briefly mention what directories you scanned when you present the results.

### A2. Extract text strings

Scan the source files and extract text that is **user-facing**. This includes:

| Category | Examples |
|---|---|
| UI Labels | button text, navigation items, page titles, section headings |
| Input UI | placeholder text, helper text, validation messages |
| Status Messages | loading states, empty states, success/error messages |
| Accessibility | aria-label, title attributes, alt text |
| Meta Content | `<title>`, meta descriptions, OG tags |
| AI Prompts | system prompts, prompt templates (the parts that shape what users see) |
| Static Content | about pages, onboarding text, tooltips, footer text |

What to **skip** (these are dynamic and not suitable for static CMS):
- Variable names, function names, code comments
- Text that comes from APIs, databases, or user input at runtime
- Import paths, URLs that aren't user-visible
- Console.log messages (unless they surface to users)

### A3. Produce the CMS document

Read the template at `references/template.md` for the exact format. The key principles:

1. **Group by page/feature** — Use `## Section` headings that match the app's information architecture so content editors can navigate by page name, not filename.
2. **Every row has a code location** — Format: `` `relative/path/to/file.jsx:lineNumber` ``. This is what makes backfill precise.
3. **The "建议新文案" column starts empty** — This is the editing interface for the content editor.
4. **Explain dynamic content** — After each table section, add notes explaining which text is dynamic (comes from user input, AI generation, databases) so editors don't waste time looking for text that isn't in the tables.
5. **Include AI prompts separately** — Put prompt content in its own section. Use fenced code blocks for multi-line prompts so editors can see the full prompt in context, with an empty code block below for the suggested replacement.
6. **Add a usage guide at the end** — Tell the editor how to use the document (what to fill in, what not to modify, how to signal they're done).

Save the CMS document to `docs/cms-copy-inventory.md` (or a name the user prefers).

### A4. Proactive Guidance & Explanation

After generating, you MUST actively guide the user. Output a friendly message containing:
- What the document contains, how it's organized, and provide a direct link to it.
- Clear instructions: "请直接打开该文档，在 **建议新文案** 这一列填入新文字。原文字和位置等列千万不要改。完成后只要告诉我：**按 CMS 文档回填代码** 即可。"
- **CRITICAL REMINDER**: Always add this reminder at the end: "⚠️ **温馨提示: 如果您接下来继续修改了代码或新增了功能，请务必记得说“更新文案文档” ，以保持文档与代码匹配！**"

---

## Phase B: Backfill & Apply

When the user asks you to apply/backfill the CMS document (or says "回填", "apply the CMS doc", "update copy from the doc", etc.):

### B0. Pre-execution Confirmation (执行前主动告知)

Before doing anything, read the CMS document and count all editable entries that already contain a suggested replacement. This includes:
- table rows where `建议新文案` is filled in
- prompt / long-text sections where the suggested content block is non-empty

Then proactively report the total to the user:

> "我已读取 CMS 文档，共找到 **X 处**已填写修改建议的条目（含表格文案与提示词/长文本块），将涉及以下文件：`[文件列表]`。确认后我将开始回填。是否现在执行？"

Wait for user confirmation ("yes", "确认", "go", "开始" etc.) before proceeding. This gives the user a final chance to catch mistakes before any code is changed.

### B1. Read and parse the CMS document

Read the CMS document (typically `docs/cms-copy-inventory.md`). Parse each Markdown table row and extract:
- `位置` (file path and line number)
- `当前文案` (current copy in code — used for verification)
- `建议新文案` (new copy to apply)

Also parse prompt / long-text sections. Do **not** treat them as a different class of operation just because they are not in tables. If a section clearly describes a multi-line editable block, extract the same essential information:
- `位置`
- content type hint when available (for example `prompt`, `long_text`, `长文本`)
- current content block
- suggested content block

Prefer semantic understanding over rigid string matching. Common labels may include:
- `当前提示词`, `当前内容`, `当前正文`
- `建议新版提示词`, `建议新内容`, `建议新版正文`
- `类型：prompt`, `类型：long_text`

If the structure is slightly inconsistent but the editor's intent is clear, use your generalization ability to recover the intended block boundaries and continue.

**Formatting Auto-Correction (自动修正):** Content editors might make syntax mistakes (e.g., breaking the Markdown table structure by missing a pipe `|`, adding extra line breaks, or messing up code blocks). **You must be resilient.** If you encounter malformed Markdown, intelligently deduce the user's intended text and parse it anyway. Do not crash or simply skip over slightly broken formatting.

**Only process entries where the suggested replacement is meaningfully non-empty.**
- For table rows, process rows where `建议新文案` is non-empty.
- For prompt / long-text sections, process blocks where the suggested content contains non-whitespace text.
- Skip blank suggestions — that means the editor wants to keep the current content unchanged.

### B2. Verification & Safety Dry-Run

Before replacing any code, you MUST perform these validations (Dry-Run) to prevent breaking the application:
1. **Locate & Match**: Navigate to the line (±3 lines tolerance). Verify the original current content exists. For table entries this means the `当前文案`; for prompt / long-text sections this means the current content block. If not found, search the file more broadly; if still not found, flag as error and skip. Do not guess.
2. **Variable Preservation Check**: If the original current content contains template variables (e.g., `{count}`, `${name}`), verify that the suggested replacement still includes them. If any variable is missing, flag an error ("缺少必要的变量占位符") and skip.
3. **Syntax Breakage Check**: Check if the suggested replacement will be inserted into a JS/JSX string literal context (i.e., surrounded by `'…'`, `"…"`, or `` `…` `` in the source). If so, only reject unescaped occurrences of the **same delimiter** used by the surrounding literal. For example, `'` is dangerous inside `'…'`, but is safe inside `"…"`. Likewise, `"` is dangerous inside `"…"`, but safe inside `'…'`. Note: CJK quotation marks (`“`, `”`, `‘`, `’`) are safe and must never be flagged as errors.
4. If a validation fails, record it and do not modify that specific entry.

### B3. Execute replacements

Apply replacements file by file. For multiple changes in the same file, apply them all in a single edit operation to avoid line number drift between changes.

For prompt / long-text sections, replace the entire current content block with the suggested content block provided in the CMS document. Preserve the surrounding code context and delimiters in the source file; only replace the actual content payload.

### B4. Report results

After all replacements are done, produce a summary:

```
## 回填结果

✅ 成功替换: X 处
⏭️ 跳过 (未填写新文案): Y 处
⚠️ 跳过 (原文不匹配/找不到): Z 处

### 详细变更:
| 文件 | 行 | 旧文案 | 新文案 |
|---|---|---|---|
| ... | ... | ... | ... |

### 未能匹配的条目 (需人工检查):
| 文件 | 行 | 期望找到 | 实际内容 |
|---|---|---|---|
| ... | ... | ... | ... |
```

### B5. Follow-up Operations & Reminders

1. **Offer to regenerate**: Offer to regenerate the CMS document to safely reflect the new state of the codebase and resolve any shifted line numbers.
2. **API Documentation Reminder**: Always conclude your successful backfill response with: "⚠️ **温馨提示: 代码与文案已顺利更新！如果此次产品迭代涉及了接口逻辑或字段的变更，请不要忘了同步更新相应的接口文档 (API Docs) 哦！**"

---

## Phase C: Incremental Update (增量同步)

Trigger this mode when the user says things like "更新文案文档", "新增了一些页面，帮我同步一下", "refresh the CMS doc", "我加了新功能，CMS 文档要同步", or "update the content inventory".

### C1. Proactive Guidance (执行前主动告知)

Before scanning, confirm the operation with the user:

> "我将扫描代码中**新增的文案**，并把它们追加到现有的 CMS 文档里。之前已填写的「建议新文案」**不会被覆盖**。现在开始吗？"

### C2. Scan for new strings only

- Re-scan the source directories (same scope as Phase A — ask the user if the scope has changed since last time).
- Compare results against entries already recorded in the existing CMS document.
- Use `位置` as the primary anchor for incremental sync.
- Do not treat `当前文案` alone as a unique identifier across the whole project.
- Classify changes as:
  - **New entries**: no reliable match in the document → append to the appropriate section.
  - **Moved entries**: same content, same file, line number shifted → update the `位置` column only.
- If matching is ambiguous, do not guess and do not auto-append. Record the ambiguous entry, list the candidate matches, and ask the user to decide how it should be resolved.

### C3. Merge into the existing document

- **Append** new entries to the appropriate section.
- **Update** line numbers only for confidently matched in-file moves.
- **Never overwrite** any row that already has `建议新文案` filled in — those belong to the editor.
- **Do not auto-process ambiguous entries** until the user confirms the intended resolution.

### C4. Report results

After the merge, tell the user:

> "增量同步完成！新增了 **X 条**文案，更新了 **Y 条**行号，保留了 **Z 条**已有修改建议。另有 **N 条**歧义条目未自动处理，请确认后我再继续。"

---

## Edge Cases & Best Practices

### Handling multi-line text
For text that spans multiple lines (like AI prompts), use fenced code blocks in the CMS document rather than table cells. Tables are for single-line strings.

### Handling template literals and interpolation
Text like `` `已完成 ${count} / ${total} 步` `` contains dynamic parts. In the CMS document, represent the dynamic parts with `{variableName}` placeholders and note them:
```
| 进度文案 | `TaskBreakdown.jsx:90` | `已完成 {completedCount} / {totalCount} 步` |  |
```
When backfilling, preserve the `{placeholder}` parts exactly as they appear — only replace the static text around them.

### Language and encoding
The CMS document should match the language of the project's UI. If the project uses Chinese, Japanese, or any non-Latin text, ensure the Markdown file is saved as UTF-8.

### Line number accuracy
Line numbers in the `位置` column are snapshots — they become stale as code changes. This is acceptable because:
1. The `当前文案` column serves as the verification anchor
2. Phase B uses fuzzy matching (±3 lines) and falls back to full-file search
3. The user can regenerate the document to refresh line numbers at any time
