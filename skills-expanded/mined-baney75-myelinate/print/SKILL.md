---
name: print
description: "Use when someone asks for a printable study guide, paper practice test, worksheet, formula sheet, or blank diagram. Not generic PDF conversion or screen-only quizzes."
---

# Print

Paper practice is a **rehearsal of the real exam and of the hand's work**: closed book, timed, written, drawn. A printable is worth making when it makes the learner retrieve, draw or reason without help, and when its key tells them exactly what they got wrong and why. A handsome PDF that the learner reads like notes is a handout, not practice.

Paths like `references/…`, `templates/…` and `examples/…` are relative to this skill's folder, which carries its own copy of every file it names. Other Myelinate skills are siblings (`../tutor/SKILL.md`) and are installed as their own skills too. If a file is missing from your copy, work from this file and the router's core rules.

Templates: `templates/practice-test.html`, `templates/diagram-worksheet.html`. Renderer: `scripts/make_pdf.py`. Reference: `examples/practice-test-oxygen.html` and its PDF. Copy their structure, not their content.

Evidence tags: **Strong** (replicated, meta-analytic or classroom-relevant), **Moderate** (consistent evidence, limited transfer or delay data), **Weak** (thin or mixed), **Craft** (expert practice, not tested as such).

## 0. Rules that override everything else

1. **Every answer is re-derived before it ships.** Work the test yourself, independently, before writing the key; compute every number with code; run `verify` on the key. A wrong key teaches the error with authority.
2. **The key never shares a page with the questions.** Page break before it, every key page marked ANSWER KEY. Nothing on the test pages gives an answer away: not label text, alt text, `aria-label`, `<title>`, ids, file names, or a later item's stem.
3. **Match the intended use.** For exam practice, match its format, length, timing, point weights and allowed materials. For a child, self-learner or work trainee with no exam, match their objective and level instead of inventing exam conditions. Practice that differs from a real test transfers less (transfer-appropriate processing; Morris, Bransford & Franks 1977). **Moderate**
4. **Unaided work is the score.** Anything done with notes, a word bank or a hint is recorded separately, on paper and when you grade it (Bastani et al., PNAS 2025: performance with help overstated performance without it). **Moderate** (one large RCT)
5. **Look at every page before delivering.** Render the PDF to images and inspect each one. A test with a clipped graph or a key bleeding onto the last question page is broken.

## 1. When paper helps

Make a printable when the learner needs:
- **Closed-book exam simulation.** Practice tests beat restudy for later retention (Roediger & Karpicke 2006; meta-analysis g ≈ 0.61, Adesope, Trevisan & Sundararajan 2017). **Strong**. Paper and a clock make "closed-book" real in a way a chat window does not. **Craft**
- **Handwritten mechanisms, derivations and diagrams**: arrow-pushing, free-body diagrams, pathways, labeled anatomy, curves. Drawing to-be-learned material aids memory (Fernandes, Wammes & Meade 2018) and learner-generated drawing can aid science learning when guided (Van Meter & Garner 2005). **Moderate**
- **Timed conditions** that rehearse pacing for a written or proctored exam. **Craft**
- **Time away from screens**, or a format their exam uses. Paper reading shows a small comprehension edge over screens, larger under time pressure (Delgado et al. 2018 meta-analysis); that is reading, not testing, so don't oversell it. **Moderate**

Stay in chat or a `lab` when the learner needs fast feedback per item, a simulation, or a drill. Print is the dress rehearsal, not the first lesson.

## 2. Practice tests

### Blueprint first
1. Get the **study guide** (or syllabus objectives) and the **exam format**: item types, count, minutes, point weights, allowed materials. If they are missing, ask once; label the test "format inferred" until confirmed (`tutor` §1a).
2. List objectives O1…On. **Every objective is sampled**; points are **proportional to its weight** in the guide, not to how easy it is to write items for.
3. Fill a blueprint table, objective → items → points → share, and put it in the key. Check sums with code.

### Item writing (NBME Item-Writing Guide, 6th ed.; Haladyna, Downing & Rodriguez 2002) **Craft, consensus guidelines**
- **Single best answer.** One option is defensibly best; the others are wrong for a named reason.
- **Cover-the-options rule.** The stem is a complete question a prepared learner could answer with the options hidden.
- No "all of the above", "none of the above", "both A and C", or true/false in MCQ clothing.
- **No cues.** Grammar agrees with every option; no longest-is-right; no word repeated from stem to key only; no absolutes ("always", "never") marking the wrong options.
- **Homogeneous options**: same kind of thing, similar length and structure (all mechanisms, or all directions of change).
- **Distractors come from named misconceptions**: concept inventories, the learner's own past errors, common exam traps, and the key names each one. Filler distractors make easy items, not diagnostic ones.
- Vignettes when the exam uses them: patient or experiment first, question last.
- Balance the key's letters; no runs or patterns. Order options logically (numeric ascending, or short to long).

### Mix, order and transfer
- **Item types** in the exam's proportions: MCQ, short answer, draw-and-label, mechanism/arrow-pushing, calculation with work shown. Free recall and drawing are harder and more diagnostic than recognition. **Moderate**
- **Interleave topics** within each section; don't block them. Interleaving confusable types helps learners pick the right approach (Brunmair & Richter 2019). **Strong**
- **Difficulty ramp** within each section: a confidence-building first item, then harder. **Craft**
- **Transfer items**: same principle, new surface (a drug in the stomach, a climber, stored blood). Mark them in the key.
- **Cross-item leaks**: a later stem must not state an earlier answer (if item 11 asks for S at 100 mmHg, item 12 must not say "97% saturated").

### Pages, in order
1. **Cover and instructions**: name, date, start and end time, time limit, total points by section, allowed materials, the rule for marking items done with notes, and "the key starts on a page marked ANSWER KEY; remove it first."
2. **Sections** with item and section point values. Answer space sized to the expected answer: about one ruled line per 10 to 12 words; work boxes sized to the steps; blanks with units for numeric answers.
3. **Answer key** after a page break: blueprint; sources list; per item: answer, why it is right, why each distractor tempts (the misconception by name), objective, source (study-guide line, slide or page). Open items get a **model answer and point rubric**; drawings get a model figure and a rubric of features.
4. **Scoring sheet**: item · objective · points · unaided / with notes / missed · points earned · error type. Totals for all points and for **unaided only**; time used.
5. **Error-analysis page**: every lost point gets one cause: **K**nowledge (didn't know), **M**isread (stem, option, units, NOT/EXCEPT), **R**easoning (pieces known, chained wrong, or a tempting distractor), or **T**ime. Then include points lost by objective, a next action, and a retest list for 2 to 3 days later. Bring it to `study-plan`, which re-ranks by these results. Reflection wrappers after exams have modest support (Lovett 2013). **Weak**, cheap enough to keep.

## 2b. Study guides that make them retrieve

The best study guide is a set of questions, not a summary. Rereading and summarizing rated low utility; practice testing and spaced practice rated high (Dunlosky et al. 2013, *Psychol Sci Public Interest* 14:4 to 58). **Strong.** Retrieval practice beat elaborative concept mapping on a later test, including on concept-map tests (Karpicke & Blunt 2011, *Science* 331:772 to 775). **Moderate-Strong.** Students rated bolded key terms most helpful, yet that rating was negatively related to exam scores (Gurung 2004, *Teaching of Psychology*). **Moderate.**

Build it this way:
1. **Scope from the official study guide or objectives,** one section per objective, in the course's notation and order (`tutor` §1a). Pull in the learner's own notes where they help (`notes`), and the gaps the notes reveal.
2. **Each section leads with questions,** answers hidden at the back: recall ("define"), explain ("why does…"), compare ("A versus B: what's the one deciding feature?"), apply (a new case), draw ("sketch the… from memory").
3. **One compact model per section:** the key diagram, comparison table or worked example, labeled, after the questions, so the learner tries before they look.
4. **Blank and masked versions** of each key diagram for redrawing (§3).
5. **Contrast tables for confusables** (SN1 vs SN2, DI vs SIADH), with the deciding feature named.
6. **A mixed self-test at the end,** interleaved across sections, exam format, with a key on separate pages.
7. **A one-page review plan:** which sections to retrieve on which days before the exam (`study-plan`).

Keep it short enough to use: one or two pages per lecture's worth of objectives. Encourage them to write their own answers before checking; a guide they complete themselves does more than one they read.

## 3. Diagram worksheets

- **Blank version**: the figure with **numbered leader lines** ending clearly on one structure each, and a numbered answer table. Optional **word bank** with decoys so it cannot be solved by elimination; using it marks the item "with help."
- **Masks are complete**: no label text in the image, `<text>`, `<title>`, `<desc>`, `aria-label`, ids, class names, comments, captions or file names. Neutral alt text: "structures numbered 1 to 6." (`find-media` §4.)
- **Labeled answer version** on a separate page marked as the answer page: the same figure, each name beside its number, plus a one-line function or identifying feature and source.
- Figures: hand-authored **vector SVG** preferred (crisp at any size, maskable, editable). Sourced images only with a recorded license (TASL) via `find-media`; course figures stay private.
- Add an optional **draw it from memory** page for a later day.

## 4. Formula sheets

Make one only if the exam allows one; then mirror the allowed size and rules (one side, handwritten, provided by the instructor). If the exam provides a sheet, use that exact sheet in practice. A self-made sheet is a summary to build, not to lean on: have the learner write it from memory first, then correct it. If no sheet is allowed, put needed constants in stems the way the exam does, and quiz the rest with `flashcards`.

When the learner wants formulas to copy onto cards or a sheet by hand, show every formula inline in the chat as rendered math (`show_widget` or the host's equivalent), not as bold plain text or a Markdown table of typed symbols. Group them by tier (memorize, know, provided) from the study guide, with units beside each and units you worked out yourself marked derived.

## 5. Print layout rules

- Paper: **Letter default**, A4 on request (`@page { size: A4 }` or `make_pdf.py --format A4`). Layout must fit both widths.
- Body **≥ 11pt**; Newsreader headings, Inter body with fallbacks (`assets/brand.md`). White paper, ink `#16313b`, rust `#a54320` only for item numbers and key markers.
- `break-inside: avoid` on every question, key entry, figure and table row; headings `break-after: avoid`.
- Footer on every page: **title + Page X of Y** (CSS `@page` margin boxes in the templates; `make_pdf.py` adds a footer if a page lacks them).
- **Grayscale-safe**: never carry meaning in color alone. Distinguish curves by solid/dashed/dotted, mark points with shapes and labels (WCAG 1.4.1).
- **No ink-wasting backgrounds**: no fills, gradients, or dark blocks. Ruled lines and boxes are borders, so they print even with background graphics off.
- Vector SVG figures; text inside SVG stays real `<text>` and fits with fallback fonts.

## 6. Making the PDF

1. Work in the learner's project folder or a scratch folder (`$TMPDIR/myelinate-print`), never inside this skill's folder: an installed skill is shared and gets replaced on update, and some hosts bundle every file in it. Copy the template there and replace content between the `<!-- CONTENT: -->` markers.
2. Render with headless Chromium, from that folder, calling the script by its path in this skill:
   `python3 <this skill's folder>/scripts/make_pdf.py test.html test.pdf --png-preview previews/`
   It waits for web fonts, prints backgrounds, honors CSS `@page` size (unless `--format` is given), adds page numbers when the page has none, and writes `previews/page-NN.png` (pdftoppm, else PyMuPDF). It never downloads a browser; set `MYELINATE_CHROMIUM` to a Chromium executable if needed.
3. Fallbacks: a Chromium browser → Print → Save as PDF (margins Default; headers and footers off, since the template has its own). Firefox and Safari ignore `@page` margin boxes, so footers drop there. ReportLab or LaTeX (`exam` class) are fine when the environment has them and HTML is not available.
4. **Chat-only, no code execution**: deliver the print-ready HTML file and say: "Open it in Chrome or Edge, choose Print → Save as PDF, paper Letter (or A4), margins Default." Do not claim you checked the layout.

## 7. Grading completed paper

The learner photographs each page, flat, in good light, whole page in frame, and uploads the photos.
- **Read before grading.** Transcribe what you can read; say exactly what you can't ("item 9, line 3 is illegible") and ask, rather than guess in their favor or against them.
- **Grade against the key and rubric**, point by point, quoting what earned or missed each point. Rubric points, not impressions; no keyword matching.
- **Record assistance honestly**: circled or word-bank items are "with notes," whatever the answer. Report the unaided total separately.
- **Feedback follows `tutor` §3a**: what's right, the one specific gap, why the tempting option tempted, what to do next. Then make them fix one missed item themselves before you show the full worked answer.
- **No sycophantic grading.** Don't round up, don't award half points the rubric doesn't give, don't soften a wrong answer to "almost." If they push back, recheck against the source; change the grade only for a real reason, and say which.
- Fill the error-analysis page with them, then hand results to `study-plan` and mark targets with honest states (Not checked / Needs support / Independent this session / Retrieved after delay / Transferred).

## 8. Verify before you deliver

Report each check with its result; never "verified" without saying by what.
1. **Key**: re-derive every answer independently, then compare; recompute every number with code; run `verify` (adversarial review) on the key for anything graded or high-stakes.
2. **Items**: one defensible answer each; cover-the-options passes; distractors each named; no cues or cross-item leaks; letters balanced.
3. **Blueprint**: every objective sampled; points sum; shares match the guide.
4. **Render** in the working folder (§6), `make_pdf.py --png-preview`, then **look at every page**: page breaks, nothing split or clipped, answer spaces intact, figures legible, footer and page count right, key starting on its own page with the ANSWER KEY mark.
5. **Leaks**: search the test pages' HTML for answer strings (label names, key values) before the key section.
6. **Grayscale**: meaning survives without color (check a grayscale preview when color is used).

## 9. Delivery

Deliver the PDF and the HTML source. One sentence on what it is (items, minutes, points) and how to use it: print, remove the key, take it timed and closed-book, then score with the sheet or upload photos. State scope (confirmed from the study guide or inferred), what was checked and how, and what is approximate.

## Anti-patterns

Key on the last question page · answers in alt text or file names · a later stem giving away an earlier answer · "all of the above" · filler distractors · blocked topics in exam order · a 10-minute test for a 2-hour exam, or the reverse · equal points regardless of the guide · answer lines too short to answer in · color-only legends · dark backgrounds · fonts under 11pt · un-inspected PDFs · lenient or rounded-up grading · counting with-notes points as mastery · formula sheets the exam doesn't allow.
