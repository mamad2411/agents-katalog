---
name: paper-to-code
description: Implement an academic paper (arXiv or any quantitative source) as verifiable code without inventing unstated details. Use when asked to implement, reproduce, or prototype a method from a paper. Produces an ambiguity audit before code, citation-anchored decisions, and machine-checkable sanity verification.
---

# Paper-to-code: implementation without invention

BLUF: the paper is the only source of truth; every implementation decision is either anchored to it or explicitly flagged as our choice. The dominant failure mode is silent gap-filling — plausible defaults presented as the paper's content. That is neuroslop in code form, and this skill exists to make it structurally impossible.

## Stage 0 — acquire the full text

- Prefer arxiv-mcp tools (`download_paper` / `read_paper`) when available; otherwise WebFetch the abstract page and PDF.
- Appendices, footnotes, table captions, and figure captions are first-class sources — missing hyperparameters usually live there, not in the method section.
- If the authors published official code, locate it; it is a second, separately-tagged source — never a silent one.

## Stage 1 — ambiguity audit, before any code

Classify every implementation-relevant decision; the tags below are this skill's specialization of the harness claim-typing discipline (epistemic boundary: confirmed ≠ associative):

| Tag | Meaning | Obligation |
|---|---|---|
| `FACT §X.Y` / `Eq. N` | stated in the paper | anchor to the exact section/equation |
| `PARTIAL §X.Y` | mentioned but ambiguous | quote the passage verbatim, list the readings |
| `UNSPECIFIED` | paper is silent | our default + alternatives, never filled silently |
| `ASSUMPTION` | inference from context | reasoning stated next to it |
| `FROM-CODE` | taken from the authors' implementation | tagged as code-derived, not paper-derived |
| `QUESTION` | load-bearing gap that cannot be defaulted safely | ask the developer before coding — not a guess |

A `QUESTION` blocks its code path until answered (mental model gate).

## Stage 2 — implementation

- Non-trivial decisions carry their `§`/`Eq.` anchor in the audit table; inline flags (`[UNSPECIFIED]`, `[ASSUMPTION]`) appear only at load-bearing lines. These are constraint provenance the code cannot show by itself — not decoration, so they do not conflict with the no-decoration rule (invariant #9).
- Variable names follow paper notation where that stays readable.
- Standard components are imports: "standard transformer encoder" means a library call plus a dependency note, never a rewrite.
- Scope is the core contribution only, unless training / data / evaluation pipelines are explicitly requested. No baselines, no infrastructure beyond what the contribution needs.

## Stage 3 — verification, split by oracle class

- **Mechanizable class** (external validators): shape checks, conservation or sanity equations stated in the paper, a toy-dimension forward pass on CPU. Run them and paste outputs — claimed completion requires executed machine-checkable evidence (invariant #23).
- **Judgment class** ("did we implement what they meant"): present the audit table and every divergence to the developer; their sign-off closes it.
- Never claim correctness of the method itself. The implementation matches the text; if the paper is wrong, the code is faithfully wrong — say so in those words.

## Output contract

1. Ambiguity audit table. 2. Code. 3. Verification outputs. 4. Open QUESTIONs. BLUF at every step.

Counter: when the developer explicitly asks for a quick sketch, pseudocode, or intuition-level walkthrough, the full audit is overhead — state in one line what is being skipped and sketch.

---
Provenance: discipline distilled from the paper2code pattern (PrathamLearnsToCode/paper2code, surfaced via the ai-boost/awesome-prompts digest); this text is written from scratch for the neuro-matrix harness — no upstream text reused.
