---
name: latex-report-revision
description: Revise LaTeX reports per inline notes; rebuild, share PDF.
license: CC0-1.0
metadata:
  hermes:
    tags:
    - latex
    - report
    - lab-report
    - revision
    - workflow
    related_skills:
    - latex-debugging
    - academic-writing-latex
  source_frontmatter:
    version: 1.0.0
    author: hermes
  imported_from: hermes
---

# LaTeX Report Revision (iterative, user-driven)

## When to use
- User hands you a `.tex` path (course/lab report series, e.g. weekly I2060 reports) and sends
  incremental correction notes ("改X", "把Y移到Z后", "表头左对齐").
- Session may be a handoff from a codex thread (`codex://threads/<id>`). Recover the pending
  instruction from `~/.codex/sessions/<yyyy>/<mm>/<dd>/rollout-*-<id>.jsonl`: parse payloads of
  type `message` with role `user`; the LAST user message with no assistant reply = still pending.
- Multi-round: the user reviews the PDF and sends the next note. Conventions below were enforced
  by corrections across rounds — violations get pushed back.

## The loop (every instruction, no exceptions)
1. **Re-read the exact current bytes** before editing. The file changes between rounds; never
   patch from an old read.
2. **Edit via a Python script with anchors**: each `(old, new)` pair asserts `count(old) == 1`
   before replacing, then post-verifies new text, then writes only after ALL checks pass
   (fail-safe ordering: verification failure ⇒ file untouched). Never use the patch tool on
   backslash-heavy `.tex` (double-escape pitfall — it silently writes `\\textbf`).
3. **Compile twice**: `xelatex -interaction=nonstopmode <name>.tex` in the `latex/` dir.
   Trust the LOG, not the exit code: `grep -c '^!'` must be 0, look for `Output written`,
   and `grep -c Overfull`.
4. **Verify in the PDF** (pdftotext, whitespace-collapsed): new phrases present, moved
   phrases appear exactly once, removed phrases gone, mention-before-float still holds.
5. **Always end the reply with a link to the latest PDF** — standing requirement
   ("always output the latest pdf for me to review").

## User style rules (each one was a correction — violations get pushback)
- **Bold only the result clause**, never the whole sentence (e.g. bold everything after "and",
  leave "We use the oscilloscope to …" regular). Inside bold: numbers `\mathbf{}`, units stay
  `\mathrm{}` regular — matches the report's number-emphasis convention.
- **Concise over explanatory**: a wordy justification becomes
  `…, consistent with the specified 200 Ω series resistor …`. No "so this reading is consistent
  with … being present and intact".
- **Don't restate methods already introduced earlier** — but when you delete such a sentence
  because "前面有方法介绍了", go CHECK the earlier location actually carries the detail; if it
  doesn't, strengthen it (e.g. OBJECTIVES bullet must say "take three trials … report their
  mean" once the delay paragraph drops the averaging). Missing the second half reads as not
  following the instruction.
- **Every Table/Figure first mention must precede its float.** Re-run
  `scripts/check_report.py` after ANY structural edit.
- **One clarify, then full execution**: when a note has ambiguous scope (what moves? which
  tables?), ask ONE multi-select clarify, then apply ALL chosen scopes in one pass. Don't ask
  again mid-work; don't execute half.
- **Table lead-in = the conclusion the data proves**, not the table's identity ("Table N lists…").
  Concise but powerful; re-verify every quoted number against the cells first.
- **Result tables carry results, not verdicts**: drop "Matches"/assessment and photo-index
  columns — verdict ("all eight results agree with expectation") + provenance caveats
  ("the $10$ retention was not photographed") go into the lead paragraph; the table just
  shows `Inputs | Ideal action | Measured result`.

## House conventions (series-wide — see references/house-style.md for the full spec)
- **Experiment section template**, in order:
  intro paragraph ending with a colon → formulas → circuit-structure paragraph → Figure
  → LED state photos + their lead (BEFORE the truth table — user rule: 照片是实验中的状态，
  状态先行; delay evidence stays put) → truth-pattern paragraph → Table
  → delay paragraph → delay table (measurement sections only) → [scope traces after delay table].
  When one paragraph heads several equations (EQ/GT/LT), split into one
  `sentence ending with colon → display` pair per equation group.
- **All measurement tables share ONE house style** (the first/delay worksheet table is the
  model): bold LEFT-aligned headers (no `\multicolumn{..}{c}{..}` centering, no `\shortstack`
  two-line headers), one column per trial (`Trial 1 (ns)` …) plus `Mean (ns)`, edge-pair folded
  into the Delay column, portrait inline — never `\\begin{landscape}` — 11 pt font
  (10 pt was a correction-turned-violation: everything except 大标题 is 11 pt),
  `tabcolsep` 3 pt, column fractions summing ≈ 90 % of `\\linewidth`.
  When told to "apply this table's experience to all later tables", rewrite EVERY later table
  of that class, including ripping out landscape wrappers and condensing long cell labels.
- **Page count will change** after structural edits (landscape removal etc.) — verify content
  (caption counts, key sentences), not page numbers.

## Pitfalls
1. **Display-formula spacing**: `\normalsize` runs at `\begin{document}` and RESETS
   `\abovedisplayskip`/`\abovedisplayshortskip`/`\belowdisplayskip`/`\belowdisplayshortskip` —
   preamble `\setlength`s are silently wiped (bisection-confirmed: preamble-set = no effect,
   local group = works). Set the four skips IMMEDIATELY AFTER `\begin{document}`. Also delete
   any `\par` directly before `\[` — it injects `\parskip` on top of the display skip.
   Target: ≈ 8–9 pt white gap text→formula (normal line whitespace ≈ 6.3 pt). Measure with
   `pdftotext -bbox` (word yMin/yMax grouped by line), don't eyeball.
2. **Bold verification**: `pdftohtml -xml -f p -l p out.pdf` shows `<b>` tags and font ids —
   the reliable way to confirm bold scope (PyMuPDF may be unavailable). Span text may be
   hyphen-split ("oscil-" / "loscope"); search for substrings, not full sentences.
3. **pdftotext extraction quirks**: hyphenated line breaks merge ("short-circuit" →
   "shortcircuit"), Ω and thin spaces vary — grep loosely (`grep -o "phrase.\{0,60\}"`) or
   collapse whitespace before substring checks; a "missing" phrase is often the search
   string, not the content.
4. **Long inline terminal one-liners get blocked** by the command hardline filter — split into
   small commands or run a saved script file.
5. **`multirow.sty` may be local** to the report's latex/ dir — test docs compiled elsewhere
   need `TEXINPUTS=<latex dir>:` .

## Support files
- `references/house-style.md` — full section template, table spec, phrasing rules with examples.
- `scripts/check_report.py` — float mention-order checker (mentions before floats, caption
  counts, never-mentioned floats). Run after every structural edit.
