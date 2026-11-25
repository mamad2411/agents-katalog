---
name: article-translation
description: Translate a completed article into target languages specified in the brief. Supports bidirectional zh↔en translation with automated review. Use when an article has status "review" or "published" and the brief specifies target languages.
---

# Article Translation

You translate completed articles into target languages. You work from a finished, author-approved article and produce a natural translation that preserves the author's voice, tone, and specificity.

## Prerequisites

- Read `writing.config.md` first (see your workspace configuration for its location)
- Read the `workspace` field from `writing.config.md` frontmatter (default: `.`). If the value starts with `/`, use it as an absolute path; otherwise resolve it relative to the directory containing `writing.config.md`. The article directory containing `brief.md` is inside `{workspace}/articles/`.
- `brief.md` must have status `review` or `published`
- `brief.md` must have a non-empty `Translations` field
- `article.{original_lang}.md` must exist, where `{original_lang}` comes from `brief.md`'s `Original language` field

If any prerequisite is missing, inform the user what needs to be done first.

## Supported Languages

- `zh` — Traditional Chinese (繁體中文)
- `en` — English

If `Translations` contains unsupported language codes, inform the user and skip those.

## Your Responsibilities

### Step 1: Read Context

Read and understand:
1. `writing.config.md` — resolve workspace path
2. `brief.md` — article info, target audience, goals, original language, target languages
3. `article.{original_lang}.md` — the source text to translate
4. Translation rules — see [translation rules](references/translation-rules.md)
5. Writing rules — see [writing rules](${CLAUDE_SKILL_DIR}/../article-writing/references/writing-rules.md)

Determine the translation direction from `brief.md`:
- `Original language` field → source language
- `Translations` field → target language(s)

Verify the article status is `review` or `published`. If not, inform the user and stop.

### Step 2: Translate

Translate the article into each target language with a professional, rational tone.

Follow the content element rules in [translation rules](references/translation-rules.md):
- Convert punctuation to target language conventions
- Translate source language comments in code blocks; keep target language comments and all code as-is
- Translate image alt text and link text; keep paths and URLs unchanged
- Keep technical terms in their original form (Redis, Claude, Astro, etc.)
- Preserve all markdown formatting exactly

**Quality constraints:**
- Apply the prohibited patterns from `writing-rules.md` in spirit — a translation must not introduce AI writing patterns that the original article avoided
- For English output: no dash-connected contrasts, hollow questions, filler phrases, summary sentences, transition filler
- For Chinese output: no translationese, no excessive 「的」, no unnatural passive voice
- All Chinese output must be Traditional Chinese (繁體中文) — no Simplified Chinese characters

Write the translation to `article.{target_lang}.md` in the same article directory.

### Step 3: Automated Review Loop

Run an automated review loop (max 3 rounds) to catch common AI translation errors.

**Timeout:** Each review round reads multiple files (original article, translated article, translation rules, writing rules) and performs detailed comparison. If your tool supports configuring a timeout for subagent tasks, set it to at least 5 minutes per round. The default timeout of many tools is too short for this workload.

See [translation-review-prompt.md](references/translation-review-prompt.md) for the dispatch template.

**3a.** Dispatch the translation review subagent with paths to the original article, the translated article, `references/translation-rules.md`, `writing-rules.md`, the target language, and the current round number.

**3b.** If the subagent returns "PASS": proceed to Step 4.

**3c.** If the subagent returns "FIXED": increment the round counter. If round < 3, go back to 3a. If round = 3, proceed to Step 4.

### Step 4: Wrap Up

1. Check "Translations completed" in the `brief.md` checklist
2. Git commit with message: `content: add {target_lang} translation for {slug}`
   - Include `article.{target_lang}.md` and `brief.md`
   - If the workspace is an absolute path, run git commands from the workspace directory. Skip if not a git repository.

## Output

- `article.{target_lang}.md` — translated article for each target language
- `brief.md` — "Translations completed" checklist item checked

## You Do NOT

- Modify the original article
- Change the article's status field
- Publish translated files to a CMS (future publishing skill)
- Fabricate content not present in the original article
- Translate technical terms (keep them in original form)

## Behavior Principles

- **Voice preservation**: The translation should read as if the author wrote it in the target language. Don't flatten distinctive phrasing into generic prose.
- **Materials are sacred**: The translation conveys what the author said — no additions, no omissions, no editorial changes.
- **Professional tone**: All translations use a rational, professional style appropriate for a technical blog.
