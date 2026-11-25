---
name: antitextai
description: Strip AI and LLM tells from text, Markdown, and source code.
license: MIT
compatibility: any agent that can run a shell command, or import Python directly
metadata:
  version: 1.0.0
  repository: https://github.com/satriazoid/antitextai
  tags: text-cleanup, unicode, de-ai, refactoring
---

# antitextai

Specification and executable ruleset for de-AI-ing generated text and code: invisible
Unicode, smart quotes, banner separators, end-of-block markers, narration comments,
conversational frames, NBSP indentation.

Use when the goal is text or code that does not read as machine-generated: humanizing LLM
output, anti-AI filters, preprocessing datasets, refactoring AI-written commits.

The deterministic half runs as a command. The judgment half is yours, and this document
says exactly which is which. Nothing here needs the network, and the tool has no
dependencies beyond the Python standard library.

## When to Use

- A file, diff, or document still carries LLM fingerprints: invisible characters, curly
  quotes, `# ====` banners, `# end function x`, NBSP indentation.
- Preparing LLM output for publication: commits, PRs, docs, datasets.
- Wiring a cleanup step into CI or a pre-commit hook.
- Checking CSS/HTML for AI-generated font-family declarations (non-standard fonts).
- Detecting AI-style linguistic tells in prose (hedging, fluff openers, sign-offs, bold-keyword lists, emoji headings).

## Font Detection

The `scan-fonts` subcommand detects non-standard font-family declarations in CSS and HTML files.
Only five Google-sourced sans-serif fonts are considered human-curated:

1. **Roboto** - Font sans-serif modern dari Google, clean dan mudah dibaca, cocok untuk UI/web design.
2. **Open Sans** - Font humanist sans-serif yang netral dan friendly, sangat versatile untuk berbagai keperluan.
3. **Montserrat** - Font geometric sans-serif dengan karakter elegan, sering digunakan untuk heading dan branding.
4. **Lato** - Font sans-serif semi-rounded yang hangat namun profesional, bagus untuk body text.
5. **Poppins** - Font geometric sans-serif dengan bentuk bulat dan modern, populer untuk desain contemporary.

If any other font is detected in `font-family` declarations or Google Fonts `<link>` tags,
it is flagged as an AI tell and the scanner recommends one of the five allowed fonts.

```bash
python -m antitextai scan-fonts .                           # detect non-standard fonts
python -m antitextai scan-fonts src --strict                # fail if any non-allowed font is found
python -m antitextai scan-fonts . --json > fonts.json       # machine-readable report
```

## Style Detection

The `scan-styles` subcommand detects AI-generated prose patterns in text files:

| Rule | Pattern | Action |
| --- | --- | --- |
| `HEDGING` | generally, typically, often, usually, somewhat, fairly, rather, pretty, quite, more or less, in general, on the whole | remove hedge or replace with direct statement |
| `TRANSITION` | furthermore, additionally, moreover, consequently, nevertheless, hence, thus, accordingly, meanwhile, subsequently, alternatively, specifically, notably, essentially, ultimately, therefore, similarly, however, although | consider removing or replacing with simpler link |
| `AI_OPENER` | Certainly!, Sure thing!, Of course!, Great question!, Happy to help!, etc. | delete entire line; AI filler |
| `AI_SIGNOFF` | Hope this helps!, Let me know if..., Feel free to ask..., Don't hesitate to reach out... | delete entire line; AI filler |
| `MID_GESTURE` | It's important to note that..., Please note that..., Needless to say..., In fact, Indeed... | delete the gesture clause |
| `BOLD_KEYWORD_LIST` | `- **Security:** value`, `* **Key:** value` | drop the bold keyword prefix, write as plain prose |
| `EMOJI_HEADING` | `## 🚀 Overview`, `### ✅ Summary` | remove emoji from heading |
| `FILLER_SECTION` | `## Overview`, `## Conclusion`, `## Summary` (empty sections) | delete empty filler section |

```bash
python -m antitextai scan-styles .                          # detect AI-style tells
python -m antitextai scan-styles src --strict               # fail if any tell is found
python -m antitextai scan-styles . --json > styles.json     # machine-readable report
```

## When NOT to use

- Inside string literals, fixtures, or test data where a character is **data** (Unicode
  compatibility tables, i18n corpora, encoding tests). Cleaning there breaks the program.
- Quoted third-party material, license headers, transcripts, cited text.
- Files that must stay non-UTF-8 or carry a BOM for a legacy consumer.
- A BOM anywhere except byte 0 of a file: never delete a mid-file BOM to "clean" it.

## Prerequisites

- Python 3.9 or newer. No packages to install.
- The tool, which is either this repository cloned locally (then `python -m antitextai`
  works from the repo root) or installed with
  `pipx install "git+https://github.com/satriazoid/antitextai"` (then `antitextai`).

## How to Run

Run these through `terminal`. Order matters: inventory, transform, prove.

```bash
python -m antitextai scan .                        # 1. what is in there, change nothing
python -m antitextai clean --write PATH...         # 2. rewrite the deterministic half
python -m antitextai verify PATH... --strict       # 3. prove it, exit 1 when still dirty
```

- `scan` reports every non-ASCII codepoint with count and first line:column, classified as
  `mapped` (the tool will fix it), `review` (a human must decide), `decorative` (likely
  formatting, check it), `keep` (real content: accented Latin, Greek, CJK), plus every rule
  hit with sample line numbers. `--json` for machine-readable output.
- `clean` prints to stdout by default and only rewrites with `--write`. `-` reads stdin.
- `verify` re-runs the cleaner's own assertions and exits 1 on a residual with `--strict`.
- Both walk directories recursively over known text extensions, skip `.git`, `node_modules`,
  `__pycache__`, `.venv`, `dist`, `build`, `target`, and drop binary or non-UTF-8 files.

As a library, when a single file or an in-memory string is in play:

```python
from antitextai import clean, assert_no_artifacts, scan_text
assert_no_artifacts(clean(open("draft.md", encoding="utf-8").read()))
```

## Quick Reference

### Characters: mapped automatically

| Character | Codepoint | Becomes |
| --- | --- | --- |
| Zero-width space / non-joiner / joiner, word joiner, invisible operators | `U+200B` `U+200C` `U+200D` `U+2060`-`U+2064` | deleted |
| Bidi embeddings, overrides, isolates, deprecated format controls | `U+202A`-`U+202E` `U+2066`-`U+206F` | deleted |
| Tag characters (a hidden copy of ASCII, used to smuggle instructions) | `U+E0000`-`U+E007F` | deleted |
| Interlinear annotation anchors, Mongolian vowel separator | `U+FFF9`-`U+FFFB` `U+180E` | deleted |
| BOM at byte 0 | `U+FEFF` | deleted (a mid-file `U+FEFF` goes with the class below) |
| Soft hyphen, LRM, RLM | `U+00AD` `U+200E` `U+200F` | deleted |
| Wide and non-breaking spaces | `U+00A0` `U+1680` `U+2000`-`U+200A` `U+202F` `U+205F` `U+3000` | space |
| Line / paragraph separator | `U+2028` `U+2029` | newline |
| Smart quotes, primes | `U+201C` `U+201D` `U+2018` `U+2019` `U+2032` `U+2033` | `"` and `'` |
| Ellipsis token | `U+2026` | `...` |
| Multiplication sign, minus sign | `U+00D7` `U+2212` | `x`, `-` |
| Hyphens, dot leaders | `U+2010` `U+2011` `U+2024` `U+2025` | `-`, `.`, `..` |
| Variation selectors glued to ASCII, or stacked in runs of 2+ | `U+FE00`-`U+FE0F` `U+E0100`-`U+E01EF` | deleted |
| Bullet | `U+2022` | `-` (`- ` at line start) |

### Characters: reported, never replaced

| Character | Why it needs you |
| --- | --- |
| Horizontal bar `U+2015` | A dash variant that joins clauses like an em dash. Same review as the dashes below. |
| Variation selectors | A single selector after a non-ASCII character is presentation data (an emoji presentation selector, a CJK variation sequence) and `clean` keeps it; selectors attached to ASCII or stacked in runs are mapped, because there they carry hidden bytes. |
| Em dash `U+2014`, en dash `U+2013` | A dash can join a numeric range (`2019–2021`), a compound noun, a quotation, or a clause. Each has a different correct replacement, so every occurrence goes through review. Prefer splitting the sentence or a comma over a blind `-`, which is its own tic. |
| Box drawing `U+2500`-`U+257F`, arrows `U+2190`-`U+21FF`, dingbats `U+2600`-`U+27BF`, emoji `U+1F300`-`U+1FAFF` | Reported as `decorative`. Delete decorative banners and status glyphs on headings, but a real tree diagram or a checked checklist stays. |
| Anything classified `unclassified` | Look at it before deciding. Real content is classified `keep`. |

### Lines: whole-line rules

| Rule | Pattern shape | Action |
| --- | --- | --- |
| Separator / banner | a line that is only `=` `-` `*` `_` repeated 5+ times, optionally wrapped in comment markers | delete |
| End marker, standalone | `# end of loop`, `// end function f`, `-- end of block` | delete |
| End marker, trailing | code followed by `  # end function f` | delete the comment only, keep the code |
| Narration comment | `# Now we loop over the items`, `# Return the result` | delete |
| Step comment | `# Step 1: ...`, `# Step 2: ...` | delete unless the order is a protocol requirement |
| Pre-code meta-text | `Here is the complete Python script to achieve this:` alone before a fence | delete |
| Pure fluff line | `Certainly!`, `Hope this helps!`, `Thanks!` alone on a line | delete |
| Sign-off line or inline | `Let me know if ...`, `... is a solid choice. Hope this helps!` | delete the sign-off, keep the sentence before it |

### Frames: stripped, never deleted with their content

| Frame | Input becomes output |
| --- | --- |
| Interjection | `Certainly! The build passes.` to `The build passes.` |
| Adverbial opener | `In today's market, revenue grew 12%.` to `Revenue grew 12%.` |
| Complementizer | `It's important to note that the loop terminates.` to `The loop terminates.` |
| Mid-paragraph gesture | `Caching is essential. Please note that TTLs help.` to `Caching is essential. TTLs help.` |

Every frame rule consumes the following word character and recapitalizes it, so a stripped
frame never leaves a lowercase sentence start. Multi-word openers (`sure thing`,
`no problem`, `of course`, `great question`) are single alternatives, so nothing is orphaned.

## Procedure

1. **Inventory.** `python -m antitextai scan PATH`. Completion: you can name which files are
   dirty and which findings are `review` or `decorative` rather than `mapped`.
2. **Decide the exclusions** from "When NOT to use" per file. Completion: every file you are
   about to touch has a reason to be touched.
3. **Transform.** `python -m antitextai clean --write PATH...`. Completion: exit code 0 and
   no residual line on stderr.
4. **Hand-edit the judgment rules.** Em/en dashes, docstrings, banners that mark a real module
   boundary, WHAT-comments, hyper-descriptive identifiers, hedging stacks, emoji headings.
   Completion: no `review` finding left unexplained.
5. **Review the diff.** Every touched line must still say the same thing. A transformation
   that changed meaning is a bug, not a cleanup. Completion: encoding still UTF-8, no string
   literal changed, line endings unchanged, frontmatter byte-identical.
6. **Prove zero.** `python -m antitextai verify PATH --strict`. Completion: exit 0. Keep
   `--allow-dashes` only when the remaining dashes were individually reviewed.
7. **Build and test.** Run the project's own build and test command. Whitespace and identifier
   edits fail at runtime, not at parse time.

## Judgment work the tool refuses to do

- **Docstrings.** Strip them on internal, trivial helpers. Keep any docstring carrying contract
  information a signature cannot express (units, ranges, raises, side effects, ownership) and
  keep public or exported API docs; removing those is an API regression.
- **WHAT-comments vs WHY-comments.** Delete comments restating the syntax. Keep constraints,
  workarounds, bug references, invariants.
- **Banner labels.** Delete the decorative lines. Keep the label only if it names a real module
  boundary, then express it as a normal one-line comment or split the module.
- **Identifiers.** `processed_user_data_response_object` becomes `data` or `user_res`. Match the
  surrounding file's naming style exactly; a second convention in one file is worse.
- **Hedging stacks.** `generally typically often usually` loses all but one hedge.
- **Bold keyword prefixes** on every list item (`- **Security:** ...`): drop the forced bold term
  or rewrite as prose. Keep bold in a genuine definition list.
- **Subheading fragmentation.** Merge one-sentence sections under one heading.
- **Emoji section markers** (a rocket or chart glyph on a heading): delete unless the document's own
  style needs them.

## Clean code: let the code carry the meaning

Cleaned text is only half the job. Code written or edited under this skill must read like a
person wrote it and a person can maintain it. The test is simple: a reader who has never seen
the file follows what happens, in order, without a comment narrating each step.

### Names replace comments

- A comment that says what the next line does is a failed name. Rename the function, variable,
  or constant until the comment has nothing left to say, then delete the comment. A caption
  above `retries += 1` that reads "increment the retry counter" is noise; a docstring on
  `def add(a, b)` that says it adds two numbers is noise with better formatting.
- No docstring or comment block per function by default. A short function with a clear name
  needs no introduction. Write one only when the signature cannot carry a real contract:
  units, valid ranges, what it raises, side effects, ownership, thread safety.
- No banner or section-divider comments inside a file, no end-of-block markers, no step
  narration, no commented-out code. Dead code belongs in git history, not in a comment block.
- Keep a comment only when it answers why, not what: a business rule, an external constraint,
  a workaround with its bug reference, an invariant the types cannot express, a warning about
  a non-obvious order of operations. One or two lines. If a reader gets it from the code in
  five seconds, delete it.

### Shape of a function

- One function, one job, one level of abstraction. If a blank line and a comment are needed to
  mark a new phase inside a function, that phase is a second function waiting for a name.
- Keep functions short enough to see whole on one screen. Long is a smell, not a sin: a flat
  list of assignments or a long data table reads fine and must not be chopped into one-line
  helpers that force the reader to jump around the file.
- Prefer guard clauses and early returns over nested pyramids, so the main path reads top to
  bottom and the unhappy paths leave early.
- No clever one-liners, nested ternaries, or comprehension puzzles when a plain loop or two
  plain statements say the same thing. Boring code is maintainable code.
- Do not abstract on the second use. Wait for the third, and even then only when the copies
  must change together. A wrong abstraction costs more than a small duplication.

### Write it the way a person writes it

1. Solve the problem in the plainest order first: read the input, validate it, do the work,
   return the result. Refactor only after it works and the tests pass.
2. Follow the file that is already there: its naming, its error handling, its layout. New
   code must not look imported from another project or generated from a template.
3. Leave small human variation in place. Uniform perfection is a tell in code too: every
   function the same length, every docstring the same shape, every error message the same
   template. Match the unevenness of the surrounding code.
4. Change one thing at a time and keep the diff reviewable. A pass that renames, moves, and
   rewrites at once cannot be reviewed, and code that cannot be reviewed cannot be maintained.
5. Delete what your change made unused: imports, helpers, flags, and the comments that
   described the old shape. An explanation of code that no longer exists is the fastest way
   to mislead the next reader.

### Maintenance check

- Read each function name aloud. If the honest description of what it does needs the word
  "and", the function does two jobs: split it.
- Search your own diff for comments you added. For each one ask whether it says why or only
  what. Delete the what ones, and rename until they have nothing left to explain.
- Read the diff as the next maintainer, six months from now, with no memory of this change.
  Everything they need is in the names, the order, and the tests, or the code is not done.

## Comment spam in code

The line rules catch narration they can recognize. They cannot judge bulk: a
forty-line comment wall over a ten-line function, or a file that is mostly
comments. That shape has its own pair of subcommands.

```bash
python -m antitextai scan-comments src/            # measure it, change nothing
python -m antitextai clean-comments src/ --write   # remove long comment blocks
```

- `scan-comments` reports, per code file: the comment-to-code ratio
  (`COMMENT_HEAVY` when comments and docstrings are at least half of the
  non-blank lines), every comment block of 5 or more lines
  (`LONG_COMMENT_BLOCK`), single comment lines over 160 characters
  (`LONG_COMMENT_LINE`), and docstrings of 8 or more lines on functions and
  classes (`DOCSTRING_SPAM`; a module docstring gets 16 lines of room,
  because in this ruleset it carries the module rationale).
- `clean-comments` removes comment blocks of 4 or more lines (`--min-block N`
  to change it). That covers prose walls and commented-out code alike; both
  belong in a docs file or in git history, not above the function.
- Never removed: a block carrying a license or copyright header, a tool
  directive (`noqa`, `type: ignore`, `eslint`, a shebang, a coding line), or
  a TODO/FIXME marker, and every docstring. Docstrings are reported, not cut:
  one can hold a contract the signature cannot state, so stripping them stays
  judgment work (see the Clean code section).
- Trailing comments on code lines are never touched by the scrub. Short blocks
  of 3 lines or fewer stay when they stand on their own; unmarked lines inside a
  block that is mostly removed go with it, so a note glued to a spam wall needs
  a blank line or a marker to survive.

## Word documents (.docx)

A .docx is a zip of XML, so the walkers used to skip it as binary while
AI-written prose sat inside untouched. `scan-word` extracts the text from
`word/document.xml` with the standard library and reports the usual tells in
it: mapped and review characters, frame and line rule hits, and the
`scan-styles` prose patterns, located by paragraph.

```bash
python -m antitextai scan-word .                   # inventory .docx files
python -m antitextai scan-word report.docx --strict
```

Report-only, on purpose: rewriting a .docx means owning its formatting.
The workflow is scan here, export or copy the text out, clean it as plain
text with the normal procedure, and paste it back.

Spacing gets its own findings, because pasted AI text often spreads out in
Word with gaps that are not in the words: `WIDE_SPACES` counts the wide
and non-breaking spaces in the text (cleaning the exported text turns
them into plain spaces), `WORD_JUSTIFY` fires when full justification
meets those spaces (justification stretches them into the visible gaps),
and `WORD_CHAR_SPACING` reports runs whose character spacing is expanded
in the XML, which makes text look stretched letter by letter.

## Pitfalls

1. **Deleting a frame's line destroys content.** `In today's market, revenue grew 12%.` must
   become `Revenue grew 12%.`, not vanish. This was the most damaging bug in the tool's history.
2. **Comment prefixes are anchored on purpose.** `x = "# end of loop"` and `url = 'http://x--y/z'`
   survive because a prefix counts as a comment only at line start or after whitespace. Regex
   cannot parse strings, so eyeball any file with comment-looking literals, then verify.
3. **Setext headings look like separators.** `Heading` over `------` is a heading. The tool masks
   those lines; if you hand-roll a pass, you will silently demote headings to body text.
4. **Order is the contract:** characters, then frames, then whole-line deletions, then whitespace
   collapse. Normalize NBSP after the line rules and every `^`-anchored pattern mis-anchors.
5. **Frontmatter is split off first.** YAML and `---` delimiters never see a line rule.
6. **Line endings are preserved.** CRLF in, CRLF out. Writing files with a text-mode newline
   translation on Windows will silently convert them; use `newline=""`.
7. **Binary files are skipped by content, not by extension.** Any NUL byte or non-UTF-8 means
   hands off. Non-ASCII inside a binary is normal.
8. **Font recommendations are heuristic.** The `scan-fonts` command suggests replacements based
   on keyword overlap (e.g., "geometric" → Montserrat, "humanist" → Open Sans). Review the output
   and adjust manually if the suggestion doesn't fit the context.
9. **Style detection is additive only.** `scan-styles` reports finds but does not auto-fix.
   Some patterns (like `HEDGING`, `TRANSITION`) are debatable — review before removing.
10. **Emoji detection uses Unicode ranges.** Some uncommon emoji outside the scanned ranges may slip through.

## Verification

- `python -m antitextai verify PATH --strict` exits 0.
- `python -m antitextai scan . --strict` finds nothing you did not expect, and every remaining
  finding is a reviewed em/en dash or a legitimate decorative glyph.
- `clean(clean(x)) == clean(x)` for any file you touched.
- The project's own test suite passes.
- `python -m unittest discover -s tests -t .` passes when you are working on this tool itself.
