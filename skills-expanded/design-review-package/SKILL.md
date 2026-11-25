---
name: design-review-package
description: Assembles a design-review package for a mechanical product — requirements traceability matrix, design FMEA with RPN and action priority, costed multi-level BOM with Pareto and lead-time critical path, risk register, and a PDR/CDR checklist — as one consistent document. Use when the user is preparing a design review, PDR, CDR, gate review, or asks for an FMEA, BOM roll-up, or requirements matrix.
---

# Design Review Package

## Workflow
1. **Scope.** Find out the review type (concept / PDR / CDR / production-readiness), the audience, and what already exists. Use what the user has. Generate only the missing pieces, and mark anything generated as a draft for the team to validate.
2. **Requirements matrix.** Columns: ID | Requirement (shall-statement, measurable) | Source | Verification method (Analysis / Inspection / Demonstration / Test) | Evidence | Status. Rewrite vague requirements into measurable ones and show the original next to the rewrite.
3. **DFMEA.** Build `fmea.csv` (see `scripts/example_fmea.csv`). Rate severity, occurrence, and detection on the AIAG-VDA 1–10 scales in `references/fmea_scales.md`. Then rank:
   ```bash
   python scripts/review_tables.py fmea fmea.csv --rpn-threshold 100 --out fmea_ranked
   ```
   Every High action-priority row needs an action, an owner, and a due date.
4. **BOM roll-up:**
   ```bash
   python scripts/review_tables.py bom bom.csv --qty 500 --out bom_rollup
   ```
   Report unit cost, the parts that make up 80% of cost, and the longest-lead item (the critical path).
5. **Risk register.** Top 5–10 technical, schedule, and supply risks: likelihood × consequence (5×5), mitigation, owner, and the trigger that would escalate each one.
6. **Checklist.** Score the design against `references/review_checklist.md` for the review type. Mark each item Ready / Gap / N/A, with evidence.
7. **Assemble the document.** Use the Docs artifact type, or docx/pdf if the user asks for a file. Order: summary and decision requested → requirements → analysis evidence (link calc reports) → DFMEA → BOM → risks → checklist → action items. Keep numbers consistent: one source CSV feeds every table.

## Quality bar
Each requirement traces to verification evidence or to an open action. Each High-severity failure mode traces to a design control. The summary states the decision the board is being asked to make.
