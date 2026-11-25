---
name: engineering-calc-report
description: Turns engineering calculations, scripts, or notes into a formal, checkable calculation report — objective, inputs with sources, assumptions, method with equations, unit-checked results, margins, conclusions, and references — ready for review or sign-off. Use when the user asks for a calc report, calc package, design calculation document, or to write up an analysis formally.
---

# Engineering Calculation Report

## Workflow
1. **Collect the calculations.** Gather them from the conversation, attached scripts or spreadsheets, or outputs of other skills (`machine-element-sizing`, `quick-fea`, `thermal-fluids-calc`). Re-run every number in code. Never copy a figure without recomputing it.
2. **Unit-check** everything with `pint`, using `scripts/calc_template.py` as the pattern. Each equation's result should carry units, and the script fails on any dimensional mismatch.
3. **Write the report** in this structure (see `references/report_structure.md`):
   1. Header block: title, document number, revision, project, author, checker (blank), date
   2. Objective: one paragraph on what is being shown and against what criterion
   3. Summary of results: a table of each check with its value, allowable, margin, and PASS/FAIL. This is the first thing a reviewer reads.
   4. Inputs: a table with value, unit, and source (drawing number, datasheet, standard, assumption)
   5. Assumptions: numbered, each with a justification and a note on whether it's conservative
   6. Method and calculations: each step gives the equation in symbols (LaTeX), substituted values, result with units, and a reference (textbook eq. number or standard clause)
   7. Discussion: sensitivity to key assumptions, limitations
   8. Conclusions and recommendations
   9. References
   10. Appendix: the script or code used
4. **Margins.** Report MS = allowable / (applied × FoS) − 1. A negative MS fails. State the factor of safety basis (code, customer, or company standard).
5. **Format.** Use the Docs artifact type by default. If the user wants a file, produce docx (docx skill) or PDF/LaTeX (pdf skill). Equations go in LaTeX.
6. **Self-check before delivery**: every input has a source; every assumption is used somewhere; the summary-table numbers match the body; units appear on every number.
