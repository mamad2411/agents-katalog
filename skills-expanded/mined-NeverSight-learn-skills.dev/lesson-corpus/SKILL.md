---
name: lesson-corpus
description: Read and audit all repository materials against the closed briefing. Produces corpus-inventory.md. Uses corpus-reader subagent per file. Never invents content not found in files.
---

You are auditing the academic repository materials for the lesson defined in briefing.md.

## BEFORE STARTING

1. Read `aulas/<slug>/briefing.md`. If `status` is not `closed`: stop and say "O briefing ainda não foi fechado. Execute `/lesson-intake` primeiro."
2. Read `.super-professor/repo-manifest.md` to get the list of materials.
3. Check that all files listed in `briefing.mandatory_materials` exist on disk.

## Step 1: Read each relevant file

For each file in repo-manifest (skip: config, codigo types unless briefing references them):
- Dispatch the `corpus-reader` subagent with:
  - file_path
  - theme from briefing
  - main_objective from briefing
  - level from briefing

Collect all subagent results.

## Step 2: Classify and assess

From the collected results:
- Mark each file as central / complementar / periférico
- Mark each file as obrigatório / opcional / descartar
  - `obrigatório`: in briefing.mandatory_materials OR has central relevance
  - `descartar`: periférico AND not referenced anywhere
  - `opcional`: everything else
- Identify conflicts between files (e.g., ementa says X, slides say Y)
- Identify gaps: topics needed for the lesson that aren't covered by any file

## Step 3: Show classification for validation

Present a summary table:

| Arquivo | Tipo | Relevância | Status |
|---------|------|------------|--------|

List gaps and conflicts separately.

Ask: "Esta classificação está correta? (sim / ajustar: arquivo=relevância)"

**STOP and wait for response. Accept inline adjustments. Only write after "sim".**

## GUARDRAILS

- NEVER add evidence entries that are not direct quotes from the files
- NEVER classify a file as central without at least one evidence entry
- NEVER invent content to fill gaps — document gaps explicitly
- NEVER skip files listed in briefing.mandatory_materials
- NEVER write corpus-inventory.md before explicit confirmation

## Output

Write to `aulas/<slug>/corpus-inventory.md` following the template at `.super-professor/templates/corpus-inventory.template.md`.

The `gaps_summary` field must list every topic needed for the lesson that was not found in any repository file. If no gaps: write "Nenhuma lacuna identificada."
