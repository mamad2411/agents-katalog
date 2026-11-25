---
name: fusion-writing
description: Draft, restructure, or plan fusion-domain (magnetic/inertial confinement fusion, tokamak/stellarator/spherical-tokamak physics, diagnostics, simulation, materials, and engineering) manuscript sections and initial-submission materials from author-provided claims, results, figures, notes, or Chinese drafts. Use when the user wants to write or rebuild an abstract, introduction, related-work, method, experiments, discussion, conclusion, title, full manuscript argument, pre-submission cover letter, title page, highlights, author-contribution statement, availability/declaration text, reviewer suggestions, or a complete initial submission package rather than only polish finished prose. Specialized fusion paper types include experimental (实验论文/装置放电), simulation (模拟论文/数值模拟), diagnostic (诊断论文/诊断开发), and material (材料论文/聚变材料/等离子体-壁相互作用). Also trigger on general academic-writing and first-submission requests such as writing a paper from scratch, drafting a manuscript/section, structuring a paper, submission package, 投稿材料、首次投稿、投稿前 cover letter、投稿信、标题页、亮点、作者贡献、数据可用性声明、推荐审稿人, and fusion-domain triggers such as 聚变论文、托卡马克、等离子体、H-mode、ELM、偏滤器、中子、氚、包层、磁约束、惯性约束、装置实验、放电、平衡重建、剖面、输运、MHD 稳定性.
---

# Fusion Scientific Writing — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (core stance + workflow, paper-type playbooks including the four fusion paper types, per-section drafting guidance including the experimental method template, initial-submission guidance, language-specific rules, per-journal style).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's axes and loads only the fragments needed for the current job.

Do not try to apply the drafting logic from memory or from this router. Always load fragments from disk as described below.

## Routing protocol

Follow these five steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the axes (`task`, `paper_type`, `section`, `language`, `journal`), the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`. These hold the default stance, writing workflow, output format, and the shared fusion terminology ledger that apply to every drafting job.

### 2. Detect the axis values for this request

For each axis in the manifest, decide the value using the manifest's `detect:` hint and the user's input:

- `task` — manuscript / submission-package. Use `submission-package` for first-submission materials, never for revision correspondence.
- `paper_type` — research / methods / hypothesis / algorithmic / review, plus the fusion types experimental / simulation / diagnostic / material. Default: research. Use `experimental` for discharge/experiment papers, `simulation` for code/model papers, `diagnostic` for diagnostic development, `material` for fusion materials / plasma-surface interaction / tritium.
- `section` — abstract / intro / related-work / method / method-experimental / experiments / discussion / conclusion / title. May be multiple. Prefer `method-experimental` for an experimental fusion setup/method section (装置→诊断→放电选取→分析方法). Ask the user if it is ambiguous and matters for the draft.
- `language` — en or zh-to-en. Detect from the user's notes themselves.
- `journal` — nuclear-fusion / ppcf / pop / fed / pst / nme / fst (fusion journals) or nature / nature-family / nat-comms / generic. Default: generic.
  Use the fusion journal value the user names; use `nature` only for the flagship
  journal Nature, `nat-comms` for Nature Communications, and `nature-family` for
  other Nature Portfolio titles.

State the detected axis values in one short line to the user before drafting, so they can correct you cheaply.

### 3. Load the matching fragments

For each axis value, Read the file mapped in the manifest. Skip the `section` axis when the task is `submission-package` or when the user explicitly asks for a free-floating argument paragraph with no section context.

Do **not** read every fragment in `static/`. Load only what step 2 selected.

### 4. Draft using the loaded material

Apply the loaded fragments in this priority order:

1. Core stance + intake (`core/stance.md`) — surface missing claim / evidence / boundary before drafting.
2. Paper-type playbook — argument chain, drafting order (fusion types carry device/shot-selection/model-validation/calibration/characterization rules).
3. Section-specific drafting rules and structure (use `method-experimental` for the experimental method chain).
4. Task-specific submission rules when `task=submission-package`.
5. Journal-specific framing and constraints (fusion journal formats live in `../fusion-shared/journal-formats/`).
6. Language-specific sentence and paragraph rules (apply last).

For `task=manuscript`, run the workflow in `core/workflow.md` end-to-end. Do not skip planning just because the user asked for prose immediately. The Terminology Ledger in step 1b must lock canonical fusion symbols (`q_95`, `β_N`, `T_e`, `λ_q`, `H-mode`, `ELMs`, `SOL`) from `../fusion-shared/core/terminology-ledger.md` before prose is written.

For `task=submission-package`, follow `static/fragments/task/submission-package.md` and `references/submission-package.md` instead. Build the deliverable matrix and readiness audit; do not force manuscript paragraph architecture onto administrative submission materials.

If essential evidence or boundary is missing, write a placeholder and list it under `Assumptions or missing inputs:` instead of inventing content.

### 5. Reach for references only when needed

The files under `references/` are deep references and the example library, not defaults. Open them on demand per the `references.on_demand` table in the manifest. Typical triggers:

- The user asks for a concrete example or template → `references/examples/index.md`.
- A section's draft has structural problems that the section fragment alone does not explain → the matching `references/<section>.md`.
- The user needs a broad-audience `Nature` abstract opening or asks about a `summary paragraph` → `references/nature-summary-paragraph.md`.
- The user asks "does this paragraph flow?" → `references/paragraph-flow.md`.
- The user asks for a self-review or rejection-risk audit → `references/paper-review.md`.
- The user requests a complete first-submission package, templates, or a submission-readiness audit → `references/submission-package.md`.
- The manuscript needs a terminology/unit/number drift audit → `../fusion-shared/core/consistency-sweep.md`.
- The target is a fusion journal and exact formatting matters → the matching `../fusion-shared/journal-formats/<name>.md` (nuclear-fusion, ppcf, pop, fed, pst, nme, fst).
- Physics constants, unit conventions, or a standard parameter definition must be pinned down → `../fusion-shared/core/physics-constants.md` / `parameter-definitions.md` (loaded on demand, not preloaded).

## Submission boundary

- `fusion-writing` owns **initial submission** materials prepared before peer review.
- `fusion-response` owns revision cover letters, rebuttals, point-by-point responses, marked manuscripts, appeals, and other post-decision correspondence.
- Route graphical abstracts and TOC graphics to `fusion-figure`; route simulated pre-submission peer review to `fusion-reviewer`.

## Why this split

- The static layer is versioned and reviewable. Adding a new journal style, paper type, or section is one new file plus one manifest line.
- The dynamic layer keeps each invocation cheap: only the fragments relevant to this draft enter context, instead of the full multi-thousand-line reference set.
- The router itself is short on purpose. Update fragments, not this file, when adding scope.
- Fusion domain knowledge lives in `fusion-shared/` (terminology, parameters, constants, journal formats) so it is loaded once and reused by `fusion-writing`, `fusion-polishing`, and the rest of the fusion skill family.
