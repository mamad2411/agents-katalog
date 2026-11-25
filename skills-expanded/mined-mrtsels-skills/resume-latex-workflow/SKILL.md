---
name: resume-latex-workflow
description: "Use when adding/editing/compiling/polishing bilingual LaTeX resume entries: scan project → write entry → compile → tune bullets (+N -N) → commit."
version: 1.2.0
author: Hermes
platforms: [macos]
---

# Resume LaTeX Workflow — Iterative Editing Pipeline

Trigger: use this when the user wants to add, edit, compile, or polish a bilingual LaTeX resume entry — the pipeline is scan the source (docx/PDF/repo) → write the entry → compile → fine-tune bullets (+N -N) → commit and verify, typically in `/Users/minimx/Documents/resumes/resume-alex/`.

## Prerequisites

- XeLaTeX (TeX Live): `which xelatex`
- Git root at `~/Documents/resumes/` — the repo root, not a per-project subdir. `AGENTS.md` at the root enforces immediate commit+push after every change.
- Two entry classes: `resume-en.cls` (English, activates `\use_i:nn`) and `resume-zh.cls` (Chinese, activates `\use_ii:nn`).
- Entries are **bilingual**: a single `.tex` file holds both languages via `\resumeenif{EN content}{ZH content}`.
- All entries live under `entries/` and are included with `\input{entries/<prefix>-<name>}`.

## File Layout

| Artifact | Path |
|----------|------|
| Main .tex | `resume.tex` |
| Document classes | `resume-en.cls`, `resume-zh.cls` |
| Entries | `entries/<prefix>-<name>.tex` |
| Output PDF | `resume-en.pdf` / `resume-zh.pdf` |

Naming convention: `internships-company.tex`, `research-project.tex`, `education-school.tex`, `research-<shortname>.tex`.

## Entry Format

Each entry file is bilingual with `\resumeenif` — EN block in the first argument (shown by `resume-en.cls`), ZH block in the second (shown by `resume-zh.cls`):

```latex
\resumeenif{
  \ResumeItem{\textbf{\ResumeUrl{url}{Company or Project Name}}}
  [Role | Supervisor: Prof. Full Name]
  [MM/2026\textendash MM/2026]
  [City]

  \begin{itemize}
    \item Past-tense action verb, quantified results, no articles a/an/the.
  \end{itemize}
}{
  \ResumeItem{\ResumeUrl{url}{中文公司名}}
  [中文职位]
  [2026/07\textendash 2026/08]
  [城市]

  \begin{itemize}
    \item 中文bullet，强动词开头，量化结果。
  \end{itemize}
}
```

Date conventions: EN block uses `MM/YYYY`, ZH block uses `YYYY/MM`. Always `\textendash` (not `--`) between dates, no extra spaces. EN bullets: past-tense action verbs, quantified results, no articles; ZH bullets: strong verb openings, quantified results.

## 1. Scan the Source Project

When the user drops a source — a docx, PDF, or a code repo — extract accurate content before writing anything:

- **docx/PDF**: use `read_file` to auto-extract the text. Match the EN resume style (strong past-tense verbs, quantified results). **Cross-check every metric against the actual source repo or report — docx claims may be stale or inaccurate.** Prefer report data if they differ.
- **Code repo**: follow the deeper codebase workflow in section 4.

## 2. Verify Company / Institution Names

Before writing a name into `\ResumeUrl{url}{Company Name}`, visit the official website and confirm the full legal name. Examples: Oakcean Capital Limited (oakceancapital.com), xQuant (xquant.com), Excellence Information Technology Corp., Ltd. (excellence.com.cn). Check the footer, About page, or the English-language version of the site; cross-reference email signatures when available. Do not use shortened or assumed names.

## 3. Create the Entry File

a. Create `entries/<prefix>-<name>.tex` with 3 bullets: architecture/approach, key results with metrics, and ablation/insight.
b. Add `\input{entries/<prefix>-<name>}` to `resume.tex` in the correct section, keeping time-descending order.

## 4. Research Entry from a Codebase

When the source is a code repository (research code, course project, production repo) and the target is the Research & Projects section:

**Scan order** — read in this order:
- `README.md` — problem statement, motivation, key results, high-level architecture
- `TASK.md` / `plan.md` / `PHASES.md` — structured development plan with per-phase metrics (prioritize Phase summaries and Results tables over README prose when present)
- Core source files — architecture and key results: `model/model.py` (entry point, forward pass, loss), `model/encoder.py` (message-passing structure), `eval/metrics.py` (metric definitions), `graph/` or `data/` (data representation)
- Experiment results — `experiments/`, `results/`, benchmark files

**Extract**:

| Category | What to Extract |
|----------|-----------------|
| Problem | What gap or limitation does this address? |
| Approach | Model architecture, graph construction, loss formulation |
| Key Metrics | Accuracy, AUROC, F1 change (in pp), MSE, speedup, cross-domain transfer |
| Unique Contribution | Novel technique, ablation finding, architectural insight |

Prioritize **quantified results with baseline context** — "92% acc" without a baseline is weak; "92% acc (+3pp over baseline)" is strong.

**Format** — save as `entries/research-<shortname>.tex`, matching existing conventions:

```latex
\ResumeItem{\textbf{Project Title}}
[Role | Supervisor: Prof. Name]
[MM/YYYY\textendash MM/YYYY]
[Location]

\begin{itemize}
  \item Architecture/approach description with \LaTeX math notation —
        graph definition $G = (V, E)$, loss $\mathcal{L}$, key parameters
  \item Key metric-driven result with baseline comparison and specific numbers
  \item Additional contribution — ablation study, cross-domain transfer,
        architectural innovation
  \item (optional) Advanced feature — multi-modal fusion, self-supervised pretraining
\end{itemize}
```

**Tone guidelines**:
- Role line always says "Supervisor: Prof. Name" — never "Advisor". If no supervisor is known, use "Independent Research". Never fabricate a name.
- Each bullet: dense, single sentence, starts with an action verb (Designed / Built / Introduced / Achieved).
- Use \LaTeX math for formulas and variables: $\to$, $\Delta$, $\mathcal{L}$, $O(N^{2.807})$.
- Specific percentages over vague adjectives. 4 bullets max — pick the highest-impact contributions; the user may request fewer after trimming.

**Valid bullet content** — draw from (pick 3–4 highest impact): architecture (graph design, message passing, loss formulation); key metrics (always with baseline comparison); cross-modal fusion (attention-based fusion, pre- vs post-encoder decisions, ablations); cross-domain transfer (zero-shot / fine-tuned OOD performance); real-world validation (metrics on real rather than synthetic data).

**Post-draft polishing** (when the user requests):
- Trim each line by ~3 words — remove filler (various, several, very, significant, comprehensive), keep metrics and technical specifics.
- Merge related bullets when they share a logical thread (e.g. graph construction + the pipeline that consumes the graph).
- Remove "(expected)" from EVERY entry whose end date has passed — check globally.
- Drop projects the user deems unrealistic (e.g. "不现实").
- Apply per-bullet word-count adjustments with exact syntax like `+2 +2 +2` or `-1 0 0` (see section 6).

## 5. Compile

Compile both EN and ZH versions, always two passes each (the second pass resolves hyperref outlines and cross-references):

```bash
cd /Users/minimx/Documents/resumes/resume-alex
xelatex -interaction=nonstopmode resume-en.tex
xelatex -interaction=nonstopmode resume-en.tex
xelatex -interaction=nonstopmode resume-zh.tex
xelatex -interaction=nonstopmode resume-zh.tex
```

Show the PDF after every compile with `MEDIA:resume-en.pdf` — never skip presenting the compiled output.

## 6. Iterative Bullet Tuning

The user gives shorthand for word-count adjustments; each number = words to add/remove on that bullet index (1-indexed). Apply exactly — do not round:

| Input | Meaning |
|-------|---------|
| `#1 +2 \|` | Bullet 1: +2 words |
| `#3 -1 \|` | Bullet 3: -1 word |
| `+2 0 +3` | Bullet 1: +2, Bullet 2: 0, Bullet 3: +3 |
| `-1 0 0` | Bullet 1: -1 word, Bullets 2-3: no change |

**Balancing technique:** when two bullets in a section have uneven lengths (one wraps mid-line while the other fits cleanly), the user may say "选两行做减法 两行做加法 你取舍一下" — subtract from one bullet and add to the other, using judgment. Prioritize keeping the more substantive/technical bullet and trimming redundant filler from the other. Common cuttable ZH filler: `的`, `了`, `进行`, `实现`, `使用`, `完成`, `通过`, `以`, `与`, `在`, `来`, `于`, `覆盖`, `算法`, `模型`. Common additions: qualifiers, context phrases, domain terms that were previously trimmed. Balance so both bullets render to approximately the same line count.

## 7. Hide / Show Entries

To hide a project without deleting its file, comment out the `\input{}` line in `resume.tex`; to restore, remove the `%`:

```latex
%\input{entries/research-numerical-hierarchy}
```

## 8. Commit and Push (Immediate)

Per AGENTS.md: **every file change must be committed and pushed immediately**, including word-count micro-tweaks. No batching.

```bash
git add entries/<changed-entry>.tex   # explicit paths only — no git add .
git commit -m "<type>: <description>"   # feat/fix/docs/chore/reorg
git push origin main
```

⚠️ The git root is `/Users/minimx/Documents/resumes/`, not the per-project subdir — cd to the root before git commands. Never `git add .` or `git add -A`; use explicit file paths. Never force push.

## 9. Reorder Sections

Each section lists entries by time descending (most recent end date first); same end date → later start date first.

**Date-change rule:** whenever a date on any entry is modified, immediately re-check that section's ordering, move the entry to its correct position, and recompile. Never leave a date-changed entry in its old position.

## 10. Skills Section Maintenance

Skills should list only tools/languages actually used in the resume's projects. Four lines: Languages, Programming, AI/ML, Infrastructure. If the user says "tech超字数了" or "ML/AI也是", simplify to bare language names without parentheses/framework details.

For aligned labels use `\makebox[7em][l]{\textbf{Label:}} content` inside itemize:

```latex
  \item \makebox[7em][l]{\textbf{Languages:}} English (TOEFL 109), Mandarin (native), Cantonese (fluent)
  \item \makebox[7em][l]{\textbf{Programming:}} Python, Java, JavaScript, SQL, Bash, \LaTeX, Git
  \item \makebox[7em][l]{\textbf{AI/ML:}} PyTorch, HuggingFace, Transformers/LLMs, GNN, Bayesian inference
  \item \makebox[7em][l]{\textbf{Infrastructure:}} Docker, Linux, MongoDB, DuckDB, FastAPI, Flask, Nginx
```

Note: `pdfminer` extraction of PDFs with `\makebox` may report content in the wrong reading order despite correct visual rendering. Use `vision_analyze` on a screenshot thumbnail (generated via `qlmanage -t`) to verify visual layout when in doubt.

## 11. Justification

For better text alignment, add to `resume.cls`:

```latex
\usepackage{microtype}
\usepackage{ragged2e}
```

and `\justifying` after `\begin{document}` in `resume.tex`.

## 12. Education Entry Linking

The university name in `education-*.tex` can link to the specific programme page:

```latex
\ResumeItem{\ResumeUrl{https://www.ie.cuhk.edu.hk/programmes/bsc-in-mieg/}{Chinese University of Hong Kong}}
```

Find the programme page by navigating from the department website (e.g. ie.cuhk.edu.hk → Programmes → Undergraduate → MIEG), not from the central admissions site, which often returns 404 on sub-pages.

## Version Management

Use when the user maintains multiple resume versions for different applications alongside the master.

**Master resume** — the complete, unedited version:
- Contains ALL experience (no length limit), both current and past roles, all projects and achievements.
- Acts as the single source of truth; updated only when new experience is gained.
- Never let a tailored edit leak back into the master.

**Tailored versions** — one per job application, derived from the master:
1. Copy the master for each application.
2. Reorder or rephrase bullets for relevance.
3. Add missing keywords from the job description.
4. Delete irrelevant bullets.
5. Save with the naming convention `LastName_Role_Company_Date`.
6. Log the changes in the version tracking document.

**Version tracking template:**

| Date | Version | Target | Changes Made |
|------|---------|--------|-------------|
| 2024-01-15 | v1 | Master | Initial |
| 2024-01-20 | v2 | Google PM | Reordered bullets, added product keywords |

## Pitfalls

- **Never force push or initialize a repo without explicit user permission.** `git status` showing "No commits yet" may indicate a stale branch reference, not an empty repo — check `git reflog` for existing history before creating any root commit. A force push destroys the entire remote history, irreversibly without a local reflog.
- **One page limit**: too much text overflows to page 2. Default to 1 page unless the user accepts 2.
- **"(expected)" dates**: remove once the month has passed. Current date is July 2026 — check globally.
- **Supervisor NOT Advisor**: always use "Supervisor" in the role line, consistently across all entries.
- **Verify source metrics**: docx numbers may differ from actual report data — always verify against the source repo.
- **Single-pass compile**: always run xelatex twice; the second pass resolves hyperref outlines and cross-refs.
- **Entry not in resume.tex**: creating an entry file alone is not enough — it must be `\input{}`-ed.
- **`\ResumeItem` location**: location #5 uses `[]` brackets, not `{}`.
- **Bare `%` in LaTeX**: every `%` outside math mode in entry files must be `\%` — a bare `%` silently comments out the rest of the line. Always escape in ZH bullets (`60%` → `60\%`).
- **Don't list all features**: pick 3–4 most impressive contributions per entry.
- **Baseline context required**: "93.2% acc" without a baseline is weak; "93.2% acc, AUROC 0.989" is acceptable when the metric is standard.
- **Don't guess a supervisor**: without explicit mention, use "Independent Research"; never fabricate a name.
- **Date formatting**: use `\textendash` (not `--`) for date ranges; no extra spaces around it.
- **File path convention**: save entries as `entries/research-<shortname>.tex` matching existing entries.
- **Verify format**: read back the file to ensure no broken LaTeX, and check bullet length against existing entries for consistency.
- **TASK.md over README**: when a repo has structured phases, prioritize Phase summaries and Results tables over README prose.
- **Master is sacred**: never edit the master resume into a tailored state — derive copies instead, and log every change (what and why) in the tracking table.

## Verification

```bash
cd /Users/minimx/Documents/resumes/resume-alex && xelatex -interaction=nonstopmode resume-en.tex | grep "Output written"
```

Should show `resume-en.pdf (1 page)`. Check both EN and ZH outputs:
- The new/edited entry renders in the PDF at the correct position (use `vision_analyze` on a thumbnail if layout is in doubt).
- Section ordering is time-descending after any date change.
- Git repo is clean after push (`git status` shows no uncommitted changes).

## References

- `references/post-investment-bullets.md` — domain-specific bullet templates for FOF post-investment / compliance roles.
- `references/absorbed-*.md` — full original texts of the skills merged into this one (kept for history; this SKILL.md is the live copy).
