---
name: overleaf-section-workflow
description: >
  Bilingual section-by-section workflow for Overleaf physics-paper drafts:
  Korean draft, user iteration, Opus-direct English LaTeX translation,
  out-of-tree build, and sync hygiene. Use when starting, iterating,
  translating, or finalizing an Overleaf paper section; merging Korean drafts
  into main.tex; verifying citations; enforcing no em/en dashes, no unsupported
  novelty claims, and no forward references in background sections; or building
  JCAP/PRD-style sections with figures and BibTeX.
---

# Overleaf section workflow

A disciplined, section-by-section workflow for drafting a physics paper that lives on Overleaf, with a Korean intermediate draft and Opus-direct English translation. Designed to enforce paper-quality discipline learned from real JCAP-style drafting sessions.

## When to use

Use this skill whenever the user:
- Starts a new section of a paper drafted on Overleaf
- Iterates a Korean draft toward an English LaTeX section
- Translates a confirmed Korean draft directly into a `.tex` file
- Sets up out-of-tree builds in a `*_build` directory
- Asks for "section-by-section paper writing", "한글 초안 영어로 병합", "Overleaf 섹션 작성", or similar

Do **not** use this skill for one-shot full-paper writes; this workflow is *per-section*.

## Three-directory contract

The workflow assumes the user maintains three sibling directories under `~/zbin/OverLeaf/` (or wherever the project lives):

| Directory | Role |
|---|---|
| `~/zbin/OverLeaf/<PROJECT>/` | **Sync folder** mirrored to Overleaf via the `overleap` skill. `.tex`, `ref.bib`, `figs/` live here. **Never build here** — build artefacts would sync back to Overleaf. |
| `~/zbin/OverLeaf/<PROJECT>_draft/` | **Korean drafts** as `section<N>_ko.md` (one file per section). Plots embedded as markdown images. Iterated with the user before translation. |
| `~/zbin/OverLeaf/<PROJECT>_build/` | **Out-of-tree build**. Contains `build_<jobname>.sh` and all build artefacts (`.aux`, `.log`, `.pdf`, `.bbl`). Style files (`.bst`, `.sty`) and `ref.bib` are copied here at build time. |

If any of these directories does not exist, surface the gap before proceeding.

## Workflow loop (per section)

1. **Sync** the Overleaf project via `overleap` if not already mirrored.
2. **Draft the section in Korean** at `<PROJECT>_draft/section<N>_ko.md`:
   - Use markdown headings (`## §X.Y`), markdown bold paragraph leads (`**X.**`).
   - Math inline as `$...$`, display as `$$...$$` with explicit `\tag{X.Y}` for cross-reference.
   - Embed plots as markdown images: `![caption](figs_<topic>/foo.png)`.
   - Use `\cite{key}` exactly as it will appear in LaTeX (preserves verbatim).
   - Build up narrative as: motivation → introduce families → unify → identify limitation → contribution (see `references/06_section_narrative.md`).
3. **Iterate with the user**. Specifically watch for:
   - Em-dashes (`—`, U+2014) or en-dashes (`–`, U+2013) — both are AI-style markers; replace with periods, commas, parens.
   - Forward references (`§\ref{...}`, "본 연구의 §5 에서 다룬다") in background sections.
   - Absolute language ("표준이다", "확실하다") that should be softened.
   - Novelty claims without hedging.
   - Citations whose attribution doesn't match the cited paper's actual content.
   - Plot layout issues (legend on top of curves, xlim/ylim wasting empty space).
4. **User confirms** the Korean draft is paper-grade.
5. **Translate Opus-direct into English LaTeX** at `<PROJECT>/<jobname>.tex`. **NEVER use a Sonnet subagent for translation in this skill** — the user has explicitly required Opus-only. Conversion rules in `references/05_translation_rules.md`.
6. **Copy figure PDFs** from `~/Documents/Project/Research/.../outputs/<YYYYMMDD>_<topic>/plots/` to `<PROJECT>/figs/`.
7. **Verify the build** via `bash <PROJECT>_build/build_<jobname>.sh`. Build must produce zero `undefined` warnings.
8. **Commit-triage** the working tree at session boundaries (use the `commit-triage` skill).

## Core rules (non-negotiable)

These come from real session pain points. Do not skip.

1. **Build hygiene**: Never run `pdflatex`, `bibtex`, or any TeX command inside the Overleaf sync folder. Always build in `<PROJECT>_build/` via the supplied `build_<jobname>.sh`. If the user sees `*.aux`, `*.log`, `*.pdf` inside the sync folder, treat that as an emergency and clean it up.
2. **No em-dashes or en-dashes** in any draft or final LaTeX. They are AI-style markers; verify after every edit with `grep -cP "[\x{2013}\x{2014}]" <file>` (must return 0).
3. **No forward references** in background sections (§Background / §Setup). Subsequent sections may forward-reference earlier ones; earlier sections must stand alone.
4. **No "본 연구" preview** outside design statements. "본 연구는 GBP 를 채택한다" is fine. "본 연구의 §5 에서 다루는 DeCLA" is not.
5. **Citation must support the actual claim**, not just be metadata-correct. After bibtex generation, verify that the cited paper says what the body claims it says.
6. **Translation is Opus-only**. Do not delegate to Sonnet subagents in this skill, even when normal lab convention says to delegate translation. The user explicitly forbids this because translation goes directly into the paper.
7. **Plots use scienceplots `["science", "nature"]` with dpi=300, no title, no font override, no `no-latex` flag**. Save both PNG and PDF: PNG into the Korean draft, PDF into `<PROJECT>/figs/`. Legend placement uses `bbox_to_anchor=(1.02, 0.5)` with `loc="center left"` whenever data would overlap the legend.

## Resources

- `references/00_workflow_overview.md` — sequential workflow steps with checkpoints.
- `references/01_writing_style.md` — Korean / English style rules (em-dash ban, forward-ref ban, hedged claims, paper-grade tone).
- `references/02_citation_verification.md` — three-source verification (InspireHEP / CrossRef / Scholar) and content-vs-metadata distinction.
- `references/03_plotting_conventions.md` — scienceplots conventions, legend placement, xlim/ylim tuning, plot-script directory layout.
- `references/04_build_hygiene.md` — out-of-tree build pattern, build.sh template, what to do when sync folder is contaminated.
- `references/05_translation_rules.md` — Korean markdown → English LaTeX conversion rules (with worked examples).
- `references/06_section_narrative.md` — narrative structure (motivation → introduce → unify → limitation → contribution) and how to slot a contribution claim safely.
- `references/07_lessons_log.md` — incidents and lessons from prior sessions, grouped by category.
- `templates/build_template.sh` — copy-and-rename build script (set `JOBNAME`).

## Companion skills

The workflow orchestrates several existing skills. Invoke them in turn:

| Stage | Skill |
|---|---|
| Sync | `overleap` |
| Plot generation | `scienceplot-py` (or write inline if scope is small) |
| Plot regeneration / legend fix | direct Bash + `uv run` |
| Reference search | `reference-search` (broad lit) |
| Novelty verification | `deep-research` in lit-review / fact-check mode |
| BibTeX generation | `bibtex-gen` |
| Commit | `commit-triage` |

Do not invoke these companions silently — surface what you are doing so the user can intervene.
