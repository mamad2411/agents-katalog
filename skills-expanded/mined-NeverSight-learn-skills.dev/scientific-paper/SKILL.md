---
name: scientific-paper
description: Writes and edits scientific and academic papers in LaTeX following rigorous research methodology. Use when the user asks to write, edit, expand, structure, or review any academic paper, research paper, technical report, or LaTeX document. Triggers on mentions of papers, LaTeX, .tex files, abstracts, literature reviews, methodology sections, theorems, proofs, citations, or BibTeX. Covers the full research lifecycle from problem formulation through publication-ready output.
---

# Scientific Paper Writing

## Core philosophy

Approach every paper as a PhD-level researcher would:

1. **Understand before writing.** Read existing content, the problem domain, and related work before producing a single sentence.
1. **Rigor over volume.** Every claim must be substantiated — by derivation, citation, or empirical evidence. Never pad.
1. **Precision in language.** Use exact terminology. Define terms on first use. Avoid weasel words ("very", "clearly", "obviously").
1. **Reproducibility.** A competent reader should be able to reproduce every result from what is written.
1. **Intellectual honesty.** State assumptions explicitly. Acknowledge limitations. Report negative results. Distinguish what is proven from what is conjectured.
1. **Write to communicate, not to impress.** The goal is transferring understanding to the reader. Prefer simple, direct prose over elaborate vocabulary. Complex ideas demand simple writing.

## Research methodology workflow

When asked to write or substantially expand a paper, follow this process:

```text
Phase 1: Problem Formulation
  - What is the precise research question?
  - Why does it matter? (motivation)
  - What would a solution look like? (success criteria)
  - What are the boundaries? (scope)

Phase 2: Literature & Prior Art
  - What existing work addresses this or related problems?
  - What are the gaps in existing approaches?
  - How does this work position itself relative to the field?

Phase 3: Methodology & Framework
  - What analytical/computational approach will be used?
  - Why is this approach appropriate? (justify the choice)
  - Define notation, assumptions, and formal setup

Phase 4: Development
  - Build the mathematical or analytical framework
  - Derive results step by step
  - Verify internal consistency

Phase 5: Analysis & Discussion
  - What do the results mean?
  - What are the limitations?
  - What are the practical implications?

Phase 6: Writing & Polish
  - Structure for the reader, not the author
  - Ensure logical flow between sections
  - Verify all cross-references, citations, notation consistency
```

For detailed guidance on each phase, see [references/scientific-method.md](./references/scientific-method.md).

## LaTeX standards

### Document setup

Always use these baseline packages unless there is a specific reason not to:

```latex
\usepackage[a4paper,margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm}    % Mathematics
\usepackage{hyperref}                   % Clickable references
\usepackage{cleveref}                   % Smart cross-refs (\cref)
\usepackage{booktabs}                   % Professional tables
\usepackage{graphicx}                   % Figures
\usepackage[backend=biber,style=numeric-comp]{biblatex}  % Citations
```

### Mathematical typesetting rules

- **Operators**: Use `\operatorname{}` or define with `\DeclareMathOperator` for multi-letter operators (e.g., `\operatorname{argmax}`, not `argmax` in math mode)
- **Variables**: Single italic letters for scalars ($x$), bold for vectors ($\mathbf{v}$), blackboard bold for sets ($\mathbb{R}$)
- **Subscripts/superscripts**: Use descriptive subscripts: $r_{\text{net}}$, not $r_n$ when $n$ is ambiguous
- **Equations**: Number all important equations. Use `align` for multi-line, `equation` for single-line. Never use `eqnarray`.
- **Definitions**: Use `\coloneqq` (`:=`) when defining a quantity, `=` for equality
- **Notation table**: Include a notation summary table when the paper uses more than 10 symbols

### Theorem environments

Define and use proper theorem environments:

```latex
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}
```

### Tables

Use `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`). Never use vertical lines. Example:

```latex
\begin{table}[htbp]
  \centering
  \caption{Description before the table.}
  \label{tab:example}
  \begin{tabular}{lrr}
    \toprule
    Item & Value & Unit \\
    \midrule
    Precision & 94.3 & \% \\
    Samples   & 1{,}000 & -- \\
    \bottomrule
  \end{tabular}
\end{table}
```

For complete LaTeX reference, see [references/latex-reference.md](references/latex-reference.md).

## Writing quality standards

- **Active voice** preferred over passive ("We derive..." not "It is derived...")
- **Present tense** for established facts and mathematical truths; **past tense** for describing what was done
- **One idea per paragraph.** Topic sentence first, then support.
- **Transitions** between sections and paragraphs — the reader should never wonder "why am I reading this now?"
- **Avoid**: "it is well known that", "trivially", "clearly", "the reader can easily verify". If it is clear, the reader does not need to be told; if it is not, saying so is condescending.
- **Define before use.** Every symbol, abbreviation, and technical term must be defined before or at first use.

For detailed style guidelines, see [references/writing-style.md](references/writing-style.md).

## Workflow for editing existing papers

When asked to work on an existing `.tex` file:

1. **Read the entire file first.** Understand structure, notation, and what exists.
1. **Identify what is needed.** Expand content? Fix errors? Add sections? Improve prose?
1. **Maintain consistency.** Match existing notation, style, and conventions. Do not introduce new packages or notation that conflicts with what exists.
1. **Build on what is there.** Extend, do not replace, unless explicitly asked to rewrite.
1. **Verify compilation.** Ensure no LaTeX errors are introduced.

## Workflow for new papers

1. **Clarify the research question** with the user before writing.
1. **Outline first.** Propose a section structure and get agreement before writing prose.
1. **Design figures and tables early.** Determine the key visuals before writing prose — let the figure sequence drive the narrative structure.
1. **Write non-linearly.** Start with Results/Methods (the most concrete sections), then Discussion, then Introduction, then Abstract. Few successful papers are written start-to-finish.
1. **Revise in order: content → structure → style.** First ensure correctness and completeness, then logical organization, then prose quality.
1. **Writing is iterative.** Drafting reveals gaps in reasoning. Expect to revisit earlier sections as later ones develop.

## Quality checklist

Before considering a paper section complete:

```text
- [ ] Every claim is substantiated (derivation, citation, or evidence)
- [ ] All notation is defined and used consistently
- [ ] All equations are numbered and referenced in the text
- [ ] Cross-references (\ref, \cref) are correct
- [ ] No undefined terms or unexplained abbreviations
- [ ] Assumptions are explicitly stated
- [ ] Limitations are acknowledged
- [ ] Alternative interpretations or counterarguments are addressed
- [ ] Results are reported separately from interpretation
- [ ] Figures and tables are self-explanatory through their captions
- [ ] Logical flow: each paragraph follows from the previous
- [ ] No filler text or unsupported generalizations
```
