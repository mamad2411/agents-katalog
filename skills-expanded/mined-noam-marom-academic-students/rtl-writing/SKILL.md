---
name: rtl-writing
description: "Write right-to-left languages — Hebrew (עברית), Arabic (العربية), Persian (فارسی), Urdu — mixed with English technical terms so they render correctly, in chat and in files (Markdown, Word, LaTeX, PowerPoint). Use when the user types /rtl-writing, /academic-students:rtl-writing or the old /hebrew-with-english; when they complain that lines come out flipped, mirrored or with punctuation on the wrong side (\"השורות יוצאות הפוכות\", \"הנקודה קופצת\", \"النص مقلوب\", \"the Arabic is mirrored\"); when they ask for an RTL document, summary or slide deck that contains English terms; or when another skill in this plugin is about to write RTL prose into a file. Once invoked, keep applying it to every later reply until the user says to stop. Do not trigger just because the user wrote in an RTL language, and not for translation requests."
license: MIT
---
# RTL writing (Hebrew, Arabic, Persian, Urdu with English terms)

## Purpose

Mixed RTL + English text renders by one rule: each line (paragraph, bullet, heading, table cell, bold label)
takes its direction from its **first letter**. Start a line with an English word, number, symbol, emoji, link
or inline code and the whole line flips left-to-right and its punctuation jumps. So every line opens with an
RTL word. Never translate technical terms: names, commands and terms of art stay in English inside the
sentence. Once invoked, this applies to every later reply until the user says stop. Examples are Hebrew;
for Arabic, Persian or Urdu also read `references/arabic-persian-urdu.md` once.

## Chat replies — write once, no tool call

Write the reply directly: no reference to read, no checker to run, no draft to retype. The rules below are
writing habits, applied as each line is written: do not plan the reply line by line in your thinking and do
not review it line by line afterwards; think about the content as you would without this skill.

1. **Hebrew opener on every line.** "Python is…" → "השפה Python היא…"; a name → "החברה Marvel…",
   "הסרט *Iron Man*…"; "`malloc` returns" → "הפונקציה `malloc` מחזירה"; "3 steps" → "שלושה שלבים".
   Prefixes work too: "ב-Docker", "ה-API", "ל-Python".
2. **Headings, bullets, bold labels, table cells** follow rule 1, header cells included: "## הגדרת Docker",
   "- הפונקציה fork יוצרת…", "**הכלי Podman:** …", "| הכלי Docker | נפוץ |". Labels that feel like fixed
   English terms are the usual slip: "**Pros:**" → "**יתרונות:**", "**Step 1:**" → "**שלב 1:**",
   "**Train:**" → "**סט ה-Train:**".
3. **After a bold label that ends in English**, the next word is Hebrew: "**סשן ה-Transformer:** מודל…".
4. **End lines on a Hebrew word**, not on English + punctuation: "…ומריצים את `make` בטרמינל.". If no Hebrew
   ending fits, drop the final period.
5. **Numbers next to English:** "*Iron Man* (2008)" → "הסרט *Iron Man* משנת 2008"; "-1" → "מינוס 1".
6. **Code blocks hold no Hebrew** (comments and strings in English); the line right after a block opens in Hebrew.
7. **Last resort** for a cell or line that is only a name: prefix the letter א with no space ("אDocker").

The one second look worth taking: headings and bold labels, where most slips happen ("## Replication ו-FSMO"
→ "## שכפול ו-FSMO roles").
If the user reports a line that rendered wrong, fix it; the full rule set (below) covers rarer cases.

## Files you write

Files are checked mechanically, on the file itself (nothing to retype):
- Markdown: `python3 scripts/check_rtl.py FILE --fix` → fix until `0 errors` (stdin works: `-`).
- Word: set `w:bidi` / `w:rtl` (`references/docx.md`); `python3 scripts/check_docx_rtl.py FILE` → 0 paragraphs without RTL.
- LaTeX: `references/latex.md` (polyglossia, XeLaTeX). PowerPoint: `references/pptx.md` (`rtl="1"`).
- Course terminology for a document: `references/glossary/<family>.md` (first mention: Hebrew term with the
  English in parentheses); a `COURSE.md` may override terms.

## Files in this skill

- `scripts/check_rtl.py` — checks Markdown/chat text for every RTL script; `--fix` suggests openers; `--json`.
- `scripts/check_docx_rtl.py` — Hebrew/Arabic paragraphs in a `.docx` that lack `w:bidi`.
- `references/chat-markdown.md` — the full rule set with every edge case (tables, links, lists, mixed quotes).
- `references/docx.md`, `references/latex.md`, `references/pptx.md`, `references/arabic-persian-urdu.md`, `references/glossary/`.

## When this triggers

The user invokes it (`/rtl-writing`, the old `/hebrew-with-english`, or a namespaced form); complains that RTL
lines come out flipped or punctuation jumps; asks for an RTL document or slides with English terms; or another
skill is about to write RTL prose into a file. Not for translation, grammar questions, or plain RTL prose with
no English tokens.
