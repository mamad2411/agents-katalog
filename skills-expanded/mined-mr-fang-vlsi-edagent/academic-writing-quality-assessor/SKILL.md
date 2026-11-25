---
name: academic-writing-quality-assessor
description: Audit and refine academic manuscripts for structure, terminology consistency, LaTeX hygiene, and high-signal grammar fixes. Use this skill for theses, papers, proposals, and technical reports when the task is manuscript writing rather than experiment execution.
---

# Academic Writing Quality Assessor

## When to use

Use this skill when the user asks to:
1. check thesis/paper/proposal formatting and manuscript consistency,
2. run grammar review with minimal false positives,
3. unify terminology, equation/citation style, or figure/table conventions,
4. clean LaTeX hygiene issues such as case-mismatched graphics paths, stale chapters, or front-matter drift.

Do not use this skill for slide drafting/refinement; use `academic-presentation-crafter` or `academic-slide-refiner` instead.

## Scope Boundary

This skill owns manuscript quality assurance and writing-side consistency.
It does not own domain experiment execution, paper search, or physical-design conclusions.

## Knowledge And Tool Interaction

1. Treat the active manuscript source tree as the primary evidence source.
2. Use `scripts/common/latex_writing_audit.py` before large cleanup or when active-file boundaries are unclear.
3. When the manuscript task also requires shared KB/tool retrieval, delegate lookup to `eda-context-accessor`.
4. Prefer minimal-intrusion edits: fix correctness and consistency first, then style.
5. Archive or remove stale chapters/assets only after confirming they are outside the active include/input closure.

## Workflow

1. Build or inspect the current LaTeX project state.
2. Determine the active chapter/input/bibliography/graphics closure.
3. Review in this order:
   - build blockers and references,
   - front matter correctness,
   - chapter naming/structure consistency,
   - terminology consistency,
   - must-fix grammar errors,
   - low-risk style cleanup.
4. Only after active assets are known, clean stale chapters or duplicate figures.

## Operational References

1. Load `references/writing-qa-playbook.md` for the full manuscript QA checklist and review order.
2. Load `references/thesis-writing-onboarding.md` when the task is dissertation/thesis assembly from proposal + papers.
3. Load `references/scripts/scripts__common__latex_writing_audit.py` when you need exact behavior of the audit script or want to mirror/patch it.
