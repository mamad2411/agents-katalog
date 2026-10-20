---
description: >
  Runs the full transnational due diligence pipeline for any person with U.S.
  ties. Searches FEC, LDA, FARA, state corporate registries (FL, DE, TX),
  OpenCorporates, and BR/US press archives. Produces a PDF dossier with
  explicit source citations and confidence levels. Supports any origin country
  via origin_country in target.yaml.
argument-hint: "Full Name of Target"
---

You will conduct a transnational due diligence investigation for the person
named in $ARGUMENTS.

Act as the orchestrator defined in `skills/due-diligence-transnacional/SKILL.md`.

All output and communication must be in **English** for this command invocation.
Set `investigation_language: en-US` in the target.yaml you create.

## Mandatory rules

1. **Follow all 5 stages** defined in SKILL.md — do not skip any.
2. **Stop at mandatory human review checkpoints** between stages 2→3 and 4→5.
   Show what will be done and wait for explicit confirmation before proceeding.
3. **Cite the source of every claim.** Use the format:
   `(Source: <database>, ID <id>, retrieved on MM/DD/YYYY)`
4. **Use confidence levels** from the scale in
   `skills/due-diligence-transnacional/references/confidence-levels.md`.
5. **"Not found" is a valid finding.** List the variations tested.

## Expected flow

```
Stage 1: Collect target context → save to cases/<slug>/target.yaml
Stage 2: Generate name variations → STOP → await approval
Stage 3: Parallel searches (FEC, LDA, FARA, state-corps, OC, press)
Stage 4: Triangulate findings → STOP → present consolidated results
Stage 5: Generate PDF dossier
```

## Ethical context

Before starting, confirm:
- Does the target have public relevance (executive, politician, donor, registered agent, etc.)?
- Is there a documented journalistic reason for the investigation?
- Does the target have any U.S. tie (registered company, lobbying activity, campaign donation, etc.)?

If not: inform the user that the pipeline is restricted to public-interest investigations with a U.S. connection.

## Origin country

Set `origin_country` to the target's home country (ISO 3166-1 alpha-2).
Works for any nationality — BR, US, PE, NG, CN, DE, and others.

> **Coverage note for non-Latin names:** The name-expansion algorithm handles
> accent removal and order inversions for any name. For Chinese, Arabic,
> Nigerian, or other non-Latin transliteration patterns, coverage is lower —
> review the generated variations carefully before running searches.
