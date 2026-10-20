# CLAUDE.MD — {{PAPER SHORT TITLE}}

**Working Title:** "{{Full Paper Title}}"
**Phase:** {{Setup / Data / Analysis / Writing}}
**Sync:** Dropbox (no git)

---

## Core Principles

- **Plan first** — enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** — compile/render and confirm output at the end of every task
- **Additive only** — never delete or overwrite existing work without explicit permission
- **Stata + R interchangeable** — Stata primary for do-files; R secondary; Quarto for compilation
- **Quality gates** — nothing ships below 80/100 (details in `.claude/rules/quality-gates.md`)
- **Session logging** — update backmatter chapters (91-95) with decisions, problems, changes
- **[LEARN] tags** — when corrected, save `[LEARN:category] wrong → right` to MEMORY.md

---

## Shorthand Paths (★ EDIT THESE FIRST — everything else resolves from them)

- `$RB` = `{{path/to/quarto/project/root}}`
- `$OL` = `{{path/to/Overleaf/project/via/Dropbox}}`
- `$PAPERS` = `{{path/to/source/PDFs}}`

> Full path reference: `.claude/rules/path-config.md`. Mirror in `code/master/paths.do` and `scripts/config.R`.

## Folder Structure

```
project_root/                               # PROJECT ROOT
├── .claude/                                # Rules, skills, agents
├── $RB/                                    # ★ PRIMARY WORKSPACE
│   ├── replication_book/*.qmd              # Quarto chapters (internal docs)
│   │   └── 91-95_*.qmd                     # Backmatter: reviewer audit trail
│   ├── code/                               # Stata do-files / R scripts
│   ├── data_raw/ → data_final/             # Data pipeline
│   ├── output/results/                     # Regression results CSV
│   ├── quality_reports/                    # Plans, logs, specs
│   └── explorations/                       # Research sandbox
├── $OL/                                    # OVERLEAF (paper + slides)
│   ├── main.tex + Sections/1-8            # Paper (natbib/apalike)
│   ├── presentation.tex                    # Beamer slides
│   ├── bibliography.bib                   # Bibliography
│   └── files/tab/                         # LaTeX tables from Stata
└── $PAPERS/                               # Source PDFs
```

---

## Commands

```bash
stata-mp -b do "$RB/code/07_regressions.do"   # Run Stata
Rscript "$RB/scripts/analysis.R"                # Run R
cd "$RB" && quarto render                       # Render Quarto book
# Overleaf compiles via cloud — tables sync via Dropbox
```

---

## Agents (16 — narrow reviewers, one quality dimension each)

**Core:**
`domain-reviewer` (opus) · `proofreader` (sonnet) · `verifier` (sonnet) · `slide-auditor` (sonnet) · `narrative-reviewer` (sonnet) · `r-reviewer` (sonnet) · `quarto-auditor` (sonnet) · `quarto-fixer` (sonnet)

**Project-specific additions:**
`stata-reviewer` (sonnet) · `table-auditor` (sonnet) · `tikz-reviewer` (sonnet) · `bib-checker` (haiku) · `bib-fixer` (sonnet) · `pdf-auditor` (sonnet) · `pdf-fixer` (sonnet) · `session-logger` (haiku)

> Agents are READ-ONLY critics (except quarto-fixer, bib-fixer, pdf-fixer). Skills orchestrate them. See `.claude/rules/model-assignment.md` for selection logic.

## Skills (22 total — run with `/skill-name`)

**Code:** `/stata-code` · `/r-quarto` · `/translate-code` · `/data-analysis`
**Writing:** `/condense-to-overleaf` · `/proofread` · `/lit-review` · `/research-ideation`
**Review:** `/review-paper` · `/review-r` · `/devils-advocate` · `/interview-me`
**Overleaf:** `/overleaf-check` · `/compile-latex` · `/insert-tables` · `/validate-bib`
**Slides:** `/build-slides` · `/visual-audit` · `/slide-excellence`
**Quarto:** `/qa-quarto` · `/render-pdf` · `/quarto-warnings`
**Meta:** `/verify` · `/context-status` · `/learn` · `/commit` · `/session-log`

---

## Current State

| Component | Status |
|-----------|--------|
| Data pipeline | {{Not started / In progress / Complete}} |
| Regressions | {{Not started / In progress / Complete}} |
| Tables (.tex) | {{Not started / In progress / Complete}} |
| Quarto book | {{Not started / In progress / Complete}} |
| Literature review | {{Not started / In progress / Complete}} |
| Bibliography (.bib) | {{Not started / In progress / Complete}} |
| Paper sections 1-6 | {{Not started / In progress / Complete}} |
| Presentation slides | {{Not started / In progress / Complete}} |

---

## Non-Negotiables

- Never overwrite existing do-files without permission
- {{Clustering specification, e.g., "County-clustered SEs (83 clusters)"}}
- {{Sample restrictions, e.g., "COVID 2020-2021 always excluded"}}
- BibTeX keys: `authorYYYYdescriptor`
- Tables → `$OL/files/tab/{{subfolder}}/`
- Quarto renders from `$RB/`

---

## Detailed Standards (loaded on demand from `.claude/rules/`)

| Rule | What It Covers |
|------|---------------|
| `stata-r-conventions.md` | Code style for both languages |
| `quality-gates.md` | Scoring rubrics by file type |
| `overleaf-workflow.md` | Two-layer architecture, table pipeline, section status |
| `study-parameters.md` | Treatment vars, headline results, panel definitions |
| `replication-protocol.md` | Do-file pipeline, cross-verification |
| `session-logging.md` | When/how to log, backmatter updates |
| `verification-protocol.md` | Checklists for Stata, R, Quarto, LaTeX, BibTeX |
| `model-assignment.md` | Agent model selection, orchestrator routing, cost optimization |
| `single-source-of-truth.md` | Authority chain: do-files → CSV → tables → paper |
| `path-config.md` | Central path variables, derived paths, Stata/R integration |
