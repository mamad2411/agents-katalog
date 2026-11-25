---
name: literature-guide-read
description: Guided reading page for a course PDF, paper or textbook chapter (English/Chinese). Use when the user gives a reading and wants a reading guide, close reading or study help. 导读、精读。
---

# Reading guide

Builds a reading page for one reading (a PDF or plain text). The page helps the reader read the original and gives a summary of each paragraph, so a reader short on time still gets the argument:

- a title, a source line, a one-sentence conclusion, and a mind map under it that stops at the parts (dashed lines for qualifications);
- a left margin that follows the reader, in three boxes: the current part's claim, its numbered reasoning steps (one sentence each on the move and why it follows; click to jump) and the terms first defined there, with a Terms button for the full index;
- the reader's questions and the "guess the relations" switch below the conclusion;
- the original text in order, in a serif, while the guide's own text is in a sans on a tinted block with a coloured bar and a label: close-read paragraphs with a "read for" prompt and a folded after-reading summary, skim paragraphs led by a restatement with the original folded, skip paragraphs on one line;
- one highlight style for definitions and key claims, simple inline formulas set as text, complex ones in KaTeX with the PDF crop, explanation and symbol table folded under them;
- figures and tables on the paragraph that first cites them, recall questions at the end of each part, a full-text or summaries-only switch, term definitions on hover.

Read `references/method.md`, `references/elements.md` and `references/schema.md` before writing any guide data.

`SKILL_DIR` is the folder holding this file. `WORK` is any writable folder, such as `./guide-<slug>/`. `OUT` is where the user collects files: `/mnt/user-data/outputs/` on claude.ai, otherwise `WORK`. Requirements are in `requirements.txt`: Python 3.9+, pdfplumber and fonttools (embedded font styles); scanned PDFs need MinerU; open versions need network access and beautifulsoup4.

## Language

- Write the notes in the user's language, Chinese or English. Write both only when the user asks, and list them in `meta.notes_lang` (the first one is the default; the page then offers a language switch).
- Never translate or edit the original text. Anchors are copied from it verbatim.

## Workflow

0. **Brief the reader first.** Before writing anything, ask one round of questions in the user's language, numbered, each with a recommended answer so that "yes" accepts it (the grill-me format). Required: the language of the notes; what they are reading for (whole argument / core claims only / method and design only / evidence to cite / exam revision / something else). Optional: how familiar they are with the field and this text; questions they want answered or things they are curious about. Segmentation can run while you wait; do not write guide data before the answers. If the user says "you decide", use whole argument, medium density, and say so. Record the answers in `meta.purpose`, `meta.familiarity` and `questions` (schema.md); the purpose changes which paragraphs are close reads (method.md section 3a).
   **MinerU offer.** Check first: `python -c "import sys; sys.path.insert(0, 'SKILL_DIR/scripts'); import mineru_backend; print(mineru_backend.available())"` (it prints the Python that has MinerU, or `None` when MinerU is not installed). Inspect the text layer: with no text layer or most pages image-only, the basic tier cannot read the PDF and MinerU is needed. If MinerU is installed, use it without asking. Otherwise add one optional question to the same round: "Install MinerU, the layout engine? Pros: reads scans, more reliable on unusual layouts, tables kept as tables, formulas turned into LaTeX. Cons: about 0.8 GB download, 1 to 3 minutes per paper, not available on claude.ai." Recommend yes for a scan, many formulas or unusual layouts; otherwise recommend the basic tier. On yes, install it yourself (`pip install "mineru>=4,<5" && mineru-kit models download --tier basic`) and segment with it. Diagnose installation failures yourself; text PDFs can fall back to the basic tier. On claude.ai, skip the offer; for a scan say in one line that a scanned PDF cannot be read there and suggest running the skill in a local agent.

1. **Segment.** `python SKILL_DIR/scripts/segment.py <file> --out WORK`
   The basic tier reads text layers, keeps blank pages and skips image-only pages with one agent-addressed line naming them. A scan-only PDF stops with instructions for the agent to use installed MinerU or make the step 0 offer.
   Read the printed counts and the `自检` (self-check) line (the basic tier prints it; MinerU output has none, so read its part files with the same checks), then spot-check the first and last `WORK/paragraphs_partNN.txt` for merged columns, running heads in the text, or paragraphs cut in two. The default tier finds the columns of every page (one to three or more, with full-width titles and tables in place) and, when the result looks wrong, retries the other settings itself. Options: `--pages 3-28` to skip a cover or contents; `--columns auto|1|2|3` (default auto); `--engine mineru` to force the optional MinerU layout engine (used automatically when it is installed; see requirements.txt); `--text` for plain text (see the format below). Do not re-segment once you have started writing: it renumbers everything.
   **If the counts or the self-check look wrong** (many unnumbered headings, pages dominated by prose fragments or misplaced notes outside a notes section, unusually long merged paragraphs, text from two columns in one paragraph, references among the paragraphs, running heads inside paragraphs), fix it yourself, in this order, and never ask the user to install or fix anything:
   1. Read the self-check line; it names what looks wrong and which setting won.
   2. Re-run with `--columns 1`, `2` or `3`, or `--pages` to leave out a cover, contents or appendix.
   3. If MinerU is installed (the check in step 0), re-run with `--engine mineru`.
   4. Last resort: extract the text yourself with pdfplumber, column by column, dropping running heads, page numbers and the reference list. Write it in the `--text` format, run `python SKILL_DIR/scripts/segment.py WORK/text.txt --text --out WORK`, and later pass `--pdf <file>` to **render.py** (not segment.py) so the page images survive.
   The `--text` format: paragraphs separated by blank lines; `#`, `##`, `###` lines are headings; a line `[[p.12]]` says the following text is on page 12; put a figure or table caption in its own paragraph starting `Figure 2.` or `Table 1.` (it becomes a caption); leave table bodies out.
   `WORK/crops/` holds a PNG for every display equation and table region. Open the ones for formulas you will tag and transcribe them into `tex` (LaTeX, no `$`); when the engine already supplied `tex` (MinerU with its formula model, or an open version), check it against the crop.
1b. **Look and fix.** Run `python SKILL_DIR/scripts/fix.py overlay WORK/paragraphs.json --pages 1,<last-body-page>,<pages-to-check>` for page 1, the last body page, self-check pages and odd part text. Overlay needs a PDF and bboxes; `pages/pNNN.png` uses PDF pages (the first number in `[p4/印3]`). Write `WORK/fixes.json` as an array, e.g. `{"op":"type","ids":["P1"],"to":"frag","why":"..."}`; every op needs `why`. Operations: `type` (`ids`, `to`, heading `level`), `join` (`ids`), `split` (`id`, verbatim `at`), `move` (`id`, `after`), `region` (`page`, normalized `bbox`, `to`, `after` ID or null, heading `level`). Type targets: para, heading, caption, note, frag; title level is 0. Check front matter, headings and broken paragraphs; open every figure/table caption's crop. Frag hides masthead, licence, contact lines, chart labels, table cells and page furniture; lists/definitions stay para, captions stay caption. Inspect self-check list items in fragments and restore real items. Joined items must share a type (`type` a fragment to note or para first); joins cross notes/frags/captions, and pieces separated by other paragraphs need `move` before `join`. To remove running heads inside a paragraph, split around them, type the middle frag and join the outer pieces; a second split of a tail uses its name (`P9#2`), creating `P9#3`. Region needs a readable PDF; para/heading/caption/note targets extract words. A caption without a crop, a notes-strip crop, or a partial table/figure/code/display needs a `region` to table/figure/display covering all of it; list partial pieces in `replaces`. Run `python SKILL_DIR/scripts/fix.py apply WORK/fixes.json --paras WORK/paragraphs.json`; review parts/crops before guide data. Ops use first-segmentation IDs: after apply, find them with `overlay --orig`, paragraphs.orig.json or `fix.py ids WORK/paragraphs.json`; confirm echoed targets. Guides use new IDs; applies replay originals and log mappings. Do not re-segment or apply fixes after guide writing starts.
2. **Open version (optional).** `python SKILL_DIR/scripts/sources.py detect WORK/paragraphs.json`. If it finds an arXiv id, run `sources.py fetch <id> --out WORK`, then the `parse` or `parse-tex` command it prints. If the network is blocked, say so in one line and carry on without it. The PDF stays the source of the text and the page numbers; the open version only adds figures, tables, formulas and a report of words the PDF's text layer dropped.
3. **Read.** Read every part file in full. Use `references/genres.md` to set the genre.
4. **Write the guide.** Format in `references/schema.md`: `WORK/guide.json` with meta, thesis, overview and parts (each part with its claim, its relations `rel` and its reasoning steps `flow`, see method.md section 10), and `WORK/paras_01.json`, `paras_02.json`, ... with about 40 paragraph entries each.
5. **Check.** `python SKILL_DIR/scripts/check.py WORK/paragraphs.json WORK/guide.json WORK/paras_*.json`
   Fix every error. Judge each warning: change it or have a reason. When an anchor is not found, copy from the closest sentence the checker prints. When a number is not in the source, use the author's figure or wording.
5b. **Second read.** Follow `references/review.md`: a reader that did not write the guide (a subagent with the brief there, or yourself field by field where no subagent can be started) checks the short fields, the notes that report results and the hidden text against the paragraphs and tables. Fix what it finds, have the reader confirm the changed fields, then run check.py again.
6. **Render.** `python SKILL_DIR/scripts/render.py WORK/paragraphs.json WORK/guide.json WORK/paras_*.json --out OUT/<slug>-guide.html` (add `--sources WORK/sources.json` if step 2 produced it). Deliver the page the way the environment delivers web pages: publish it as a link if you can, otherwise give the file. The page is a single offline HTML file.

In the chat reply, give how many findings the second read made and how many you fixed, the thesis in one sentence, the answers to the reader's questions with their paragraph ids, the close-read paragraphs grouped by part (with ranges and pages), and the page. Do not repeat the whole map.

## Rules that must hold

- Every paragraph has an entry; parts cover all paragraphs in order.
- Skim notes restate the content, with its numbers, definitions and conclusion; they never just say what the paragraph does.
- Close-read paragraphs get a "read for" line (no spoilers) and a `note` after-reading summary that restates the paragraph; the page shows it folded below the original.
- Anchors are verbatim. Every number in the guide appears in the source.
- The page is rendered only after the second read (step 5b) and a clean check.
- Keep close reads within `meta.density` (low, medium, high: 15%, 25%, 40%).
- Do not grade the authors or add information the text does not contain.
- A paragraph that introduces a formula the argument relies on is a close read; its formula element carries `tex`, `syms` and `x`, checked against the crop.
- Every part that is not skipped carries two or three `recall` questions answerable from the part; every reader question in `questions` names the paragraphs that answer it.

## While the user reads

- Questions about a paragraph ("what is P23 saying?"): point to the original first, then explain, and keep what the author says apart from your explanation.
- Corrections to a tier, a note or a highlight: edit the data, run check and render again, and update the same page.
- "Walk me through it": go part by part. State what the part must establish and what to watch for in its close reads, then wait until the user has read it.
- The working folder may not survive. To recover the data from a page: `python SKILL_DIR/scripts/render.py --dump OUT/<slug>-guide.html --out WORK`; afterwards pass only `paragraphs.json` and `guide.json`.

## Improving this skill

The rules are expected to change with use.

- Separate two kinds of feedback. About one reading ("P12 should be a close read"): fix that reading's data. About the method ("thought experiments should be close reads"): note it as a candidate rule and list it in the reply.
- When the user says they have finished a reading, ask once which close reads were wrong or missing.
- When the user asks to update the skill:
  1. Restate the rule change and wait for confirmation.
  2. `SKILL_DIR` may be read-only: copy it to a writable folder. Put method changes in `references/method.md`, genre rules in `genres.md`, element types in `elements.md`, workflow changes in this file, segmentation logic in `scripts/segment.py`, explicit segmentation corrections in `scripts/fix.py` / `scripts/fix_crops.py`, extraction engines in `scripts/mineru_backend.py`, and second-read rules in `references/review.md`.
  3. Add an entry at the top of `CHANGELOG.md`: version, date, what changed, and what prompted it (which reading, what went wrong). Rule changes bump the second number.
  4. Zip the folder (`zip -r literature-guide-read.zip literature-guide-read -x '*/.git' '*/.git/*' '*/__pycache__/*' '*/PLAN.md' '*/.claude/*' '*/.pytest_cache/*'`) and hand it over; README.md explains how each tool replaces the old version.
- Do not change the method halfway through a reading.
