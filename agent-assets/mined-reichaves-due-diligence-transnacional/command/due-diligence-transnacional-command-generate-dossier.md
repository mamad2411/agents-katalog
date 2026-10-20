---
description: >
  Generates the final PDF dossier from a findings-consolidated.json file.
  Uses the generate-dossier-pdf sub-skill with a ReportLab template.
  Requires human review of findings before executing.
argument-hint: "path/to/findings-consolidated.json"
---

You will generate the final PDF dossier from the consolidated findings file
in $ARGUMENTS.

Act as the sub-skill defined in `skills/generate-dossier-pdf/SKILL.md`.

All output must be in **English**.

## Before generating

1. Read the findings file provided.
2. Present a **findings summary** to the user:
   - Hit count per database
   - Highest-confidence findings (`confirmed`, `probable`)
   - Offshore flags (if any)
   - Identified gaps
3. **Ask the user** whether to confirm, remove any finding,
   or add context before generating the PDF.
4. Only generate the PDF after explicit confirmation.

## Dossier structure

The PDF must follow the structure defined in `skills/generate-dossier-pdf/SKILL.md`:

1. Cover page with metadata (target, date, investigator)
2. Executive summary
3. Methodology and databases consulted
4. Name variations tested
5. Findings by database (with source and confidence level)
6. Triangulations
7. Gaps and next investigative fronts
8. Applicable legal context
9. Appendix: timestamps of all queries

## Output

PDF saved to `cases/<target-slug>/dossier-<date>.pdf`

Confirm file location at the end.
