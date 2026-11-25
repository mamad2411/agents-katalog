---
name: latex-templates-collection
description: "Use when starting a LaTeX document (paper, presentation, CV): pick a fitting template, adapt it, and compile with best practices."
version: 1.0.0
author: wentor-community
source: https://github.com/deedydas/latex-templates
metadata:
  openclaw:
    category: "writing"
    subcategory: "latex"
    emoji: "📋"
    keywords:
      - latex-templates
      - paper-templates
      - presentation-templates
      - cv-templates
      - academic-formatting
      - beamer
      - arxiv
---

# LaTeX Templates Collection

**Trigger:** You are starting a new LaTeX document — paper, slides, CV, thesis, grant, or poster — and need a proven template plus a reliable path from scaffold to compiled output, including arXiv submissions.

## 1. Choose a Template by Document Type

Match the template to the target venue and document type before writing anything. Prefer a venue's official template when one exists; otherwise start from the closest generic style and adapt it (see Section 7). The typical workflow is: select the template → scaffold the document → pre-populate title, author, and affiliation metadata → draft content (pair with writing composition skills) → manage references (pair with bibliography skills) → compile and verify → package for submission.

| Template | Best for |
|----------|----------|
| arxiv-style (NIPS/NeurIPS look) | General ML/CS preprints |
| NeurIPS / ICML / ICLR official | Machine learning conference submissions |
| ACL / EMNLP | NLP conference submissions |
| CVPR / ICCV | Computer vision conference submissions |
| CHI / CSCW | HCI conference submissions |
| IEEE / ACM / Elsevier two-column | Journal articles |
| Beamer | Talks, lectures, thesis defense |
| Academic CV | Faculty and postdoc applications |
| Resume | Industry applications |
| ElegantPaper | Working papers and tech reports |
| A0 poster | Conference poster sessions |

## 2. Paper Templates (Journals & Conferences)

### Journal Article Templates

- Two-column formats for IEEE, ACM, and Elsevier journals
- Single-column formats for Nature, Science, and PNAS style submissions
- APA-formatted manuscripts for social science journals
- Generic `article`-class templates adaptable to any journal's requirements
- Preprint templates optimized for arXiv and other preprint servers (see Section 3)

### Conference Paper Templates

- NeurIPS, ICML, and ICLR for machine learning conferences
- ACL and EMNLP for NLP conferences
- CVPR and ICCV for computer vision conferences
- CHI and CSCW for HCI conferences
- Generic conference templates following common two-column layouts

### Shared Paper Structure

Every paper template provides the same core skeleton: title page configuration, an abstract environment, section hierarchy, bibliography setup, and appendix formatting. Figure and table environments ship with proper captioning and numbering; algorithm and code listing environments support technical papers; theorem, proof, and definition environments cover math-heavy content; and author metadata fields handle name, affiliation, email, and ORCID.

## 3. arXiv Preprint Template (NIPS/NeurIPS Style)

For arXiv preprints, the clean minimal arxiv-style template gives professional CS/ML formatting without the overhead of a full conference submission kit. It is based on the NIPS/NeurIPS conference look, includes proper bibliography and math support, and supports single or double column layouts.

### Quick Start

```bash
git clone https://github.com/kourgeorge/arxiv-style.git
cd arxiv-style
# Edit main.tex, then compile in this order:
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

### main.tex Structure

```latex
\documentclass{article}
\usepackage{arxiv}

\title{Your Paper Title: A Descriptive Subtitle}

\author{
  First Author\thanks{Equal contribution.} \\
  Department of Computer Science\\
  University Name\\
  \texttt{first@university.edu} \\
  \And
  Second Author \\
  Research Lab\\
  Institution Name\\
  \texttt{second@institution.org}
}

\begin{document}
\maketitle

\begin{abstract}
  Your abstract here. Keep it under 200 words for arXiv.
  State the problem, approach, key results, and implications.
\end{abstract}

\keywords{keyword1, keyword2, keyword3}

\section{Introduction}
% Background, motivation, contribution summary

\section{Related Work}
% Position relative to existing literature

\section{Method}
% Technical approach, algorithms, models

\section{Experiments}
% Setup, datasets, baselines, results

\section{Conclusion}
% Summary, limitations, future work

\bibliographystyle{unsrtnat}
\bibliography{references}

\appendix
\section{Supplementary Material}
% Proofs, additional results, hyperparameters

\end{document}
```

### Math, Tables, and Figures

```latex
% Theorem environments
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}

\begin{theorem}
For any $\epsilon > 0$, there exists $\delta > 0$ such that...
\end{theorem}

% Algorithm
\usepackage{algorithm}
\usepackage{algorithmic}

\begin{algorithm}
\caption{Training procedure}
\begin{algorithmic}[1]
\REQUIRE Dataset $\mathcal{D}$, learning rate $\eta$
\FOR{$t = 1$ to $T$}
  \STATE Sample batch $B \sim \mathcal{D}$
  \STATE $\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}(B)$
\ENDFOR
\RETURN $\theta$
\end{algorithmic}
\end{algorithm}
```

```latex
% Results table (booktabs style)
\begin{table}[t]
\centering
\caption{Comparison with baselines on benchmark datasets.}
\begin{tabular}{lccc}
\toprule
Method & Accuracy & F1 & Time (s) \\
\midrule
Baseline & 85.2 & 83.1 & 12.4 \\
Ours & \textbf{91.7} & \textbf{90.3} & 8.2 \\
\bottomrule
\end{tabular}
\end{table}

% Figure
\begin{figure}[t]
\centering
\includegraphics[width=0.8\columnwidth]{figures/architecture.pdf}
\caption{Model architecture overview.}
\end{figure}
```

### Prepare the Submission Package

Include in the arXiv upload: all `.tex`, `.bib`, and `.bbl` files; all figures (PDF preferred over PNG); and `arxiv.sty`. Exclude build artifacts such as `.aux`, `.log`, and `.out` files.

```bash
# Create the submission archive
tar -czf submission.tar.gz \
  main.tex arxiv.sty references.bbl figures/
```

## 4. Presentation Templates (Beamer)

### Beamer Themes

- Clean, minimal themes suitable for academic talks
- Conference presentation templates with progress indicators
- Lecture slide templates with note support for teaching
- Thesis defense templates with structured slide sequences
- Poster session lightning talk templates

### Content Best Practices

- Use large fonts: minimum 24pt for body text, 32pt for titles
- Limit content to one main idea per slide
- Prefer figures and diagrams over dense text
- Include slide numbers and the total count for audience orientation
- Provide a handout version with multiple slides per page

### Animation and Overlays

- Use overlay specifications for progressive content reveal
- Build complex diagrams step by step across overlay frames
- Highlight key terms or equations when first introduced
- Use `\pause` commands for natural presentation flow
- Export animated PDFs for self-running presentations

## 5. CV, Resume & Cover Letter Templates

### Academic CV Templates

- Comprehensive sections: education, positions, publications, grants, teaching, service, talks
- Publication list formatting with citation counts and impact metrics
- Grant history with amounts, agencies, and roles
- Teaching portfolio with course descriptions and evaluations
- Awards and honors with dates and descriptions

### Resume Templates

- Concise one-page or two-page formats for industry applications
- Skills-focused layouts for technical positions
- Research summary formats for postdoc applications
- Clean, ATS-friendly designs that parse correctly in application systems
- Customizable color accents and section ordering

### Cover Letter Templates

- Academic job application letters with structured paragraphs
- Grant application letters with project summary integration
- Journal submission letters aligned to the editorial board
- Postdoc application letters emphasizing research vision
- Industry transition letters highlighting transferable skills

## 6. Thesis, Grant & Poster Templates

### Thesis and Dissertation

- Chapter-based templates with front matter, back matter, and appendices
- University-specific formatting packages for common institutions
- Proposal templates for thesis committee submissions
- Progress report templates for annual reviews

### Grant Proposals

- NSF-style proposal templates with required sections
- NIH grant format with a specific aims structure
- EU Horizon-style templates with work package organization
- Internal funding application templates

### Posters

- Conference poster templates in A0 and standard sizes
- Multi-column layouts with figures and results sections
- QR code integration for linking to preprints and code
- Print-ready templates with correct DPI and bleed settings

## 7. Customize Any Template

### Font Selection

- Default Computer Modern works for most applications
- Times-like fonts: `mathptmx` or `newtxtext`/`newtxmath`
- Sans-serif: `helvet` or `sourcesanspro` for a modern appearance
- Monospace: `inconsolata` for code listings
- Always ensure math fonts are compatible with text fonts

### Color Schemes

- Define institutional colors in the preamble for consistent branding
- Use `xcolor` named colors for maintainability
- Limit the palette to 3-4 colors for a professional look
- Ensure sufficient contrast for accessibility (WCAG AA minimum)
- Provide grayscale fallbacks for print compatibility

### Page Layout

- Use `geometry` for margin and page size configuration
- Set line spacing with `setspace` (single, 1.5, double)
- Configure headers and footers with `fancyhdr`
- Control paragraph spacing and indentation with `parskip`
- Set column separation and rules for multi-column layouts

### Review and Submission Options

```latex
% Two-column layout (the arXiv template defaults to single column)
\documentclass[twocolumn]{article}

% Line numbers (for review)
\usepackage{lineno}
\linenumbers

% Hyperlinks (recommended)
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue}
```

## Pitfalls

- Read the venue's author guidelines even when using its official template — guidelines change between submission cycles.
- Never include build artifacts (`.aux`, `.log`, `.out`) in an arXiv upload; strip them before packing.
- Test-compile a minimal document with any new template before starting the full manuscript.
- Don't mix text and math fonts carelessly — verify compatibility (e.g., `helvet` with default math).
- Keep color palettes to 3-4 colors and check grayscale/print output.
- Don't rely on overlays in handouts — provide a static multiple-slides-per-page version.
- Keep custom commands backward compatible when updating templates; removing them breaks documents that depend on them.
- Refresh templates before each new submission to catch guideline changes.
- Version-control templates alongside your documents.
- Maintain a personal template library with your preferred customizations pre-applied.

## References

- [latex-templates repository](https://github.com/deedydas/latex-templates)
- [arxiv-style GitHub](https://github.com/kourgeorge/arxiv-style)
- [arXiv Submission Guide](https://info.arxiv.org/help/submit/index.html)
- [arXiv LaTeX Cleaner](https://github.com/google-research/arxiv-latex-cleaner)
