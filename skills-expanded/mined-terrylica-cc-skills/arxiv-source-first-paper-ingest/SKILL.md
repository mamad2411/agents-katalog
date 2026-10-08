---
name: arxiv-source-first-paper-ingest
description: Read an arXiv paper faithfully by fetching the authors' own LaTeX source instead of OCR-ing the PDF. Extracts every display equation with its label, environment and enclosing proposition, renders each to MathML, and proves usability by compiling each formula with a real TeX engine. Use when you need a paper's formulas exactly — to replicate a method, implement a loss function or custom objective, verify a quoted number, or check a claim against what the authors actually wrote. TRIGGERS - read this paper, get the paper, arxiv paper, extract formulas from a paper, replicate a method, implement the loss from, verify the paper's numbers, machine-readable paper, latex source, mathml, e-print.
---

# arXiv source-first paper ingest

> **Self-Evolving skill.** If a step here fails or the tooling drifts, fix this file in the same
> change. The Post-Execution Reflection at the bottom says what to check.

**The whole idea in one line: for an arXiv paper, the PDF is a rendering of something you can get
losslessly, so do not read the rendering.**

`arxiv.org/e-print/<id>` serves the authors' own LaTeX. It carries the exact formulas, their
`\label`s, and — critically — which formulas are _stated propositions_ rather than intermediate
steps inside a proof. None of that survives into a PDF, so no vision model can recover it.

Measured on one real paper, OCR of the PDF reached **0.958 mean token similarity** to the source and
**only 49 % of its formulas compiled**, against 98 % for the source. Full numbers, including a
systematic model defect that similarity cannot see, in
[`../../references/OCR-VERSUS-AUTHOR-LATEX-GROUND-TRUTH.md`](../../references/OCR-VERSUS-AUTHOR-LATEX-GROUND-TRUTH.md).

---

## Step 1 — fetch the source, not the PDF

Identify yourself; arXiv asks for it and rate-limits anonymous bulk access.

```bash
ID=2605.00501
UA="your-project/1.0 (mailto:you@example.com)"
mkdir -p /tmp/paper && cd /tmp/paper
curl -sSL -A "$UA" "https://export.arxiv.org/api/query?id_list=$ID" -o meta.xml
curl -sSL -A "$UA" "https://arxiv.org/e-print/$ID" -o eprint.tar.gz
mkdir -p src && tar xzf eprint.tar.gz -C src
```

If `tar` fails the e-print may be a single gzipped `.tex` — `gunzip -c eprint.tar.gz > src/main.tex`.
Papers withdrawn or submitted as PDF-only have no source; **that is when you OCR**, and the
`unlimited-ocr` plugin is the tool.

## Step 2 — extract every display equation, with the structure that gives it authority

The tools live beside this file, under `tools/` in this skill directory.

```bash
SKILL_DIR="$(dirname "$0")"   # or the directory containing this SKILL.md
cargo run --release \
  --manifest-path "$SKILL_DIR/tools/arxiv-latex-display-math-extractor/Cargo.toml" \
  -- /tmp/paper/src > /tmp/paper/equations.json
```

Each record carries `label`, `environment_name`, `enclosing_theorem_environment`,
`enclosing_theorem_title`, `is_boxed_by_authors`, the verbatim LaTeX, and MathML.

**Read `enclosing_theorem_environment` before you trust a formula.** A formula inside `proposition`
is a stated result; the same-looking formula inside `proof` is a step in an argument. Implementing
the second as though it were the first is a silent error. `is_boxed_by_authors` is a strong signal
too — authors box the result they want you to take away.

## Step 3 — prove the formulas are usable, not merely similar-looking

```bash
bun run "$SKILL_DIR/tools/compile_each_formula_with_real_tex_engine.ts"
```

Requires TeX Live. Every formula compiles as its own minimal document, so one failure cannot cascade.

**Do this even when the source is your only input.** It catches author macros your extraction
context lacks, and it is the only check that answers "can I use this" rather than "does this look
right".

---

## Why not the obvious alternatives

| Approach                                 | Why it loses to the source                                                                                             |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| OCR the PDF with a vision model          | Lossy by construction. Measured 49 % compile rate, and it invents fused commands like `\neqi` that read plausibly.     |
| `pdftotext` / PyMuPDF text layer         | Cannot express mathematics at all — a displayed equation is glyph positioning, not a string. Returns broken fragments. |
| Ask a language model to recall the paper | No provenance, and the failure mode is confident fabrication of specific numbers.                                      |
| `ar5iv.org/abs/<id>`                     | Genuinely good, and it is LaTeXML over this same source. Use it to READ; use this to EXTRACT machine-readable records. |

## Optional: whole-document conversion

For prose as well as formulas, `latexml` (the converter behind arXiv's own HTML) produces semantic
MathML, and `pandoc -f latex -t html --mathml` is far faster and usually sufficient. Both are
complements to step 2, not replacements: neither emits one record per equation with its proposition
context.

---

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the e-print unpack?** If arXiv served a shape not handled above (single `.tex`, PDF-only,
   withdrawn), record the shape and the branch taken here so the next run does not rediscover it.
2. **Did any formula fail to compile?** An author macro means the extraction context needs that
   preamble; a genuine failure in source LaTeX is rare and worth noting in the reference document.
3. **Did you fall back to OCR?** Record why the source was unavailable — that list is the real
   boundary between this skill and `unlimited-ocr`.
