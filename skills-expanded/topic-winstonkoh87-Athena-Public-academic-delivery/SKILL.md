---
name: academic-delivery
description: 8-step pipeline for academic deliverables — essays, reports, analysis, capstones. Encodes the full intake-to-delivery workflow with automatic red-team triggering.
version: 1.0.0
created: 2026-03-06
cluster: 13 (Build Lifecycle) + 8 (Adversarial QA)
triggers:
  - assignment
  - essay
  - report
  - capstone
  - academic
  - TMA
  - deliverable
  - submission
context_trigger: "*.docx, *.pdf, essay, report, assignment, capstone, coursework, academic, university, grade, APA, Harvard, MLA, literature review, methodology, research paper"
---

# Academic Delivery Skill

> **Purpose**: Structured pipeline for academic/knowledge deliverables. Prevents the V1-is-weak failure mode by auto-triggering adversarial review.
> **Origin**: Extracted from real-world execution of client assignments. Every assignment manually reconstructed this pipeline — now it's codified.

## The 8-Step Pipeline

### Step 1: INTAKE

- Parse brief/requirements document
- Extract: word count, format (essay/report/problem set), rubric criteria, deadline, client name
- Identify prescribed frameworks or sources (e.g., "use Hirshfield as critical lens")
- Log to `.context/client_work/pricing_log.md` if commercial

### Step 2: SCOPE

- Classify deliverable type:
  - **Essay** (argumentative, comparative, reflective)
  - **Report** (technical, research, capstone)
  - **Problem Set** (calculations, code, SPSS)
  - **Presentation** (slides, pitch deck)
- Estimate complexity (Λ score)
- If commercial: trigger `client-pricing` skill for quote generation

### Step 3: RESEARCH

- Load domain context via Exocortex (`smart_search.py`)
- If external research needed: trigger `deep-research-loop` (Cluster #12)
- Extract key frameworks, models, citations
- Build a reference spine (3–7 sources minimum for essays)

### Step 4: DRAFT (V1)

- Write full first draft to spec
- Embed citations inline
- Target 90–95% of word count (leave room for red-team additions)
- **DO NOT deliver V1.** V1 is always a working draft, never the output.

### Step 5: RED-TEAM (Mandatory — Auto-Triggered)

> [!IMPORTANT]
> This step is **non-negotiable**. It fires automatically after Step 4. Shipping V1 with zero counter-readings and zero formal analysis is the canonical failure mode.

- Feed V1 through adversarial review (Cluster #8 — `red-team-review`)
- Evaluate against:
  1. **Counter-reading**: Does the draft contain at least one steelmanned opposing interpretation + rebuttal? (~80 words, non-negotiable)
  2. **Formal analysis**: For literary/theoretical work — does it engage with the *form* (enjambment, structure, methodology), not just content?
  3. **Evidence density**: Every claim backed by textual evidence or citation?
  4. **Rubric alignment**: Does the draft hit every criterion in the brief?
  5. **Genre compliance**: Is the output in the correct academic register? (MLA vs APA vs report format)
- Generate a fix list with accept/reject decisions for each criticism
- **Reject invalid criticisms** (category errors, phantom rubric scoring, n=1 methodology applied to literary analysis)

### Step 6: REVISE (V2+)

- Incorporate accepted fixes from red-team
- If >3 structural issues found, produce V3 (rare — V2 is usually sufficient)
- Re-check word count against target
- Verify counter-reading and formal analysis are present

### Step 7: COMPILE

- Format per submission requirements:
  - Cover page (if required)
  - Table of Contents (forces a structural audit — per Session 06 learning)
  - Section headers (topic-based, not numbered, for MLA essays)
  - Works Cited / References (MLA, APA, or Harvard as specified)
  - Appendices (if applicable)
- **Compaction triage**: If over word count, cut from infrastructure (setup/transition/repetition) first, analytical core last. Ratio: 70% infrastructure cuts, 30% analysis cuts.
- Paragraphing pass — wall-of-text paragraphs are a delivery failure, not a content failure.

### Step 7.5: DELIVERABLE AUDIT (Mandatory — on the compiled file)

> Step 5 reviews the *draft's reasoning*. This step audits the *file the marker opens*. A deliverable can pass multiple draft-level red-team rounds and still ship mislabelled headings, broken renders, or stale handoff guides.

- Run `red-team-review` in **Deliverable Audit** mode ([deliverable-audit.md](../../quality/red-team-review/deliverable-audit.md)) on the compiled output.
- The auditor gets the isolation packet only: brief, rubric, template, course notes, raw data, the final file and a folder listing. **No answer key, changelog, earlier audits or "verified" claims.** Where possible, use a different model family from the builder.
- Minimum lenses on round 1: **L1** (every brief instruction mapped), **L2** (built file opened and parsed), **L5** (handoff docs vs the actual folder).
- Triage with evidence. Fix through the pipeline with a red run. Re-audit with a new lens until a round finds only LOW items.

### Step 8: DELIVER

- Final proofread (grammar, citation format, page numbers)
- Export to required format (Markdown → Google Doc → DOCX)
- If commercial: send to client with scope confirmation
- Log completion to activeContext / quicksave

## Exit Gate

No deliverable leaves Step 8 without:

- [x] Counter-reading present (if argumentative/analytical)
- [x] Formal analysis present (if literary/theoretical)
- [x] Word count within ±5% of target
- [x] All rubric criteria addressed
- [x] Format compliant (citations, headers, cover page)
- [x] Step 7.5 Deliverable Audit executed on the compiled file with 0 unaddressed HIGH/MED findings

## Reflexion Archive

> [REFLEXION] What failed: V1 shipped with zero counter-readings and zero formal analysis. Why: Over-optimised for clean thesis confirmation. Lesson: Auto-trigger red-team after V1. 80 words for a counter-reading is non-negotiable.

> [REFLEXION] What failed: A capstone delivered at $83/hr effective rate (73% rate collapse vs benchmark). Why: No pricing skill fired during intake. Lesson: Step 2 (SCOPE) must trigger pricing evaluation for commercial work.
