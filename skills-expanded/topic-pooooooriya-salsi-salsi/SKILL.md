---
name: salsi
description: Write Persian with Persian words. Use when writing, editing, translating or reviewing Persian (Farsi) prose — articles, documentation, posts, essays, UI copy — to replace loanwords with Persian equivalents while leaving technical terminology, proper nouns and code untouched. Also use when the user asks for پارسی سره, سره‌نویسی, فارسی‌سازی, or "make this text more Persian".
license: MIT
---

# سالسی — Write Persian with Persian words

Persian prose is full of borrowed words that have perfectly good Persian
equivalents. Replacing them makes writing clearer and more native. Replacing
them *carelessly* makes writing wrong — it mangles technical terms, changes
meaning, and produces words no reader recognises.

This skill is about the difference.

## The one rule that matters

**A loanword is only worth replacing when the replacement is at least as clear
to the reader.** Purity is never worth clarity. If you are unsure whether a
reader would recognise the Persian equivalent, keep the original.

## Workflow

1. **Scan** the text to find candidates:

   ```bash
   salsi scan article.md --format json
   ```

   If `salsi` is not on PATH, this skill ships its own copy — run
   `./bin/salsi` from this skill's directory instead. It needs nothing
   installed beyond Python 3.10 and carries the full 20,129-word lexicon.

   Add `--domain tech` (or `medical`, `legal`, `science`, `business`) so the
   terminology of that field is protected. Add `--topic <subject>` to help the
   scanner pick the right sense of an ambiguous word.

2. **Read each finding.** Every one carries `level`, `ambiguous`, and a `sense`
   label per suggestion. Apply the judgement rules below. Most findings will be
   *rejected* in a technical document — that is the expected outcome, not a
   failure.

3. **Apply** with your normal editing tools, one considered change at a time.
   For the settled subset only, `salsi apply article.md` does it mechanically.

4. **Show the user a diff and the reasoning** before finalising. Never rewrite
   someone's text wholesale without showing what changed.

Only if you cannot run commands at all — no shell available — work from
`reference/core-words.md`, which holds the settled replacements as a plain
table. It is ~119 words against the lexicon's 20,129, so say plainly that you
are working without the full dictionary and be correspondingly conservative.

## Judgement rules

### Never touch

- Anything inside code fences, inline code, URLs, file paths, commands,
  identifiers, or configuration keys. (`salsi` already excludes these; if you
  are working by hand, you must too.)
- Quoted text from another author, or a cited title. Quotations are evidence,
  not drafts.
- Proper nouns: people, places, companies, products, brands, standards bodies.
- Numbers, units, and formulas.

### Technical terms — the part people get wrong

Ask **what the field itself writes**, not what a dictionary offers.

- Use the Persian term when the field already uses it: `کامپیوتر`→`رایانه`,
  `دیتابیس`→`پایگاه داده`, `دانلود`→`بارگیری`, `فایل`→`پرونده`. These read as
  normal technical Persian.
- Keep the loanword when it *is* the term of art: `الگوریتم`, `پروتکل`,
  `کامپایلر`, `ای‌پی‌آی`, `توکن`, `کرنل`. Translating these makes the text
  harder for its own audience.
- Never invent a term. If the lexicon offers something you have not seen used
  in that field, do not be the first to use it in someone else's document.
- In medicine, law and standards, a term can have a *defined* meaning. Changing
  it changes the content. Leave it.

### Meaning first

The lexicon is keyed by spelling, not sense. Check the `sense` label on each
suggestion before using it.

- `سرور` in a systems document is *server*, not `سُرور` "joy".
- `استرس` is `تنش` in mechanics but `دلهره` in psychology.
- `تست` is `آزمون` in science, but a `تُست` is bread.

When `ambiguous` is true, either pick the sense the context demands or leave the
word alone. Never take the first suggestion because it is first.

### Register and audience

- Formal, literary and cultural writing tolerates more purism.
- Technical documentation, legal text and UI copy tolerate much less: the reader
  is there to accomplish something, not to admire the prose.
- Casual and conversational text should stay casual. `سلام، فایلو فرستادم`
  should not become a treatise.

### Craft

- **Be consistent.** Once you choose `پرونده` for `فایل`, use it everywhere in
  the document, including headings.
- **Introduce once.** When an unfamiliar equivalent genuinely earns its place,
  the first occurrence may carry the original: `بارگیری (دانلود)`. Once.
- **Fix the grammar around the change.** Persian suffixes change shape:
  `فایل‌ها`→`پرونده‌ها`, `خانه‌ای` patterns, ezafe. Re-read the sentence after
  each edit.
- **Do not increase word count much.** A three-word phrase replacing one word is
  usually a bad trade.

### When the user asks for سره‌نویسی

Full purism (`--level pure`) also targets Arabic loanwords that are ordinary
modern Persian — `کتاب`, `علم`, `قانون`. Only do this when the user explicitly
asks for it, and warn that the result reads as a deliberate literary style, not
as neutral Persian.

## Levels

| Level | What it offers | Use it for |
| --- | --- | --- |
| `safe` | Only the curated, settled replacements | Automation, first pass, anything you cannot review |
| `standard` (default) | Everything except naturalised and protected words | Normal editing with review |
| `pure` | The full lexicon | سره‌نویسی, only on request |

## Commands

```bash
salsi scan FILE [FILE...]        # --format text|json|markdown
salsi apply FILE                 # settled replacements only; --diff to preview
salsi lookup WORD                # what does the lexicon offer, and in which sense
salsi domains                    # protection profiles available
salsi info                       # lexicon size and provenance

# useful flags
--level safe|standard|pure
--domain tech|medical|legal|science|business    # repeatable
--topic "زبان‌شناسی"                            # disambiguates senses
--protect WORD / --protect-file FILE            # your own exceptions
```

Exit code with `--strict` is non-zero when anything is found, which makes
`salsi scan --level safe --strict` usable as a CI or pre-commit check.

## Reference

- `reference/judgement.md` — worked examples of accepting and rejecting findings
- `reference/core-words.md` — the settled replacements, usable without the CLI
- `reference/install.md` — installing `salsi` and this skill elsewhere

## Credit

The word list and every Persian equivalent come from **پاسبان (Pasban)** —
<https://pasbans.ir>. This skill is a way of using their work; it is not a
substitute for it. Keep the attribution when you redistribute.
