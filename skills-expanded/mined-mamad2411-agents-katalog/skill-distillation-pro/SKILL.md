---
name: skill-distillation-pro
description: Distill books, articles, external repositories, expert workflows, team conventions, and repeated project experience into concise executable Codex skills. Inspired by kangarooking/cangjie-skill and adapted for Codex v4.3. Use when converting knowledge into SKILL.md files, improving skill packs, or extracting reusable methods from references.
---

# Skill Distillation Pro

## Purpose

Turn high-value knowledge into compact, executable skills.

Use this for:
- Books and long articles.
- External skill repositories.
- Team conventions.
- Repeated project workflows.
- Expert heuristics.
- Postmortems and lessons learned.

## Workflow

1. Define the target skill trigger: when should Codex use it?
2. Extract reusable principles, procedures, checklists, failure modes, and outputs.
3. Remove background explanation that does not guide action.
4. Convert knowledge into `SKILL.md` with `name`, `description`, workflow, rules, and output contract.
5. Add references only when details are too large for the main skill.
6. Validate that the skill is concise, triggerable, and not redundant with existing skills.

## Extraction Checklist

- What task does this knowledge improve?
- What inputs are required?
- What sequence should Codex follow?
- What mistakes should Codex avoid?
- What should the final output include?
- What evidence or verification is expected?
- Which existing skills overlap?

## Quality Rules

- Keep `description` trigger-rich and specific.
- Keep body procedural, not essay-like.
- Prefer checklists and workflows over theory.
- Do not copy large external text verbatim.
- Preserve licensing awareness for external content.
- If source quality is uncertain, mark the skill as experimental or adapt only the method.

## Output

Provide the distilled skill file, source inspiration, overlap analysis, and suggested install location.
