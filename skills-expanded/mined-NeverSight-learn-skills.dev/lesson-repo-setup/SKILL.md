---
name: lesson-repo-setup
description: Analyze or initialize an academic repository for super-professor. ALWAYS run before any other lesson skill. Scans files, classifies them, proposes directory structure, and writes .super-professor/repo-manifest.md. Never moves or deletes files without confirmation.
---

You are setting up an academic repository for use with the super-professor lesson pipeline.

## BEFORE DOING ANYTHING: check for existing manifest

Check if `.super-professor/repo-manifest.md` exists.
- If YES: read it, compare against current files, show only what has changed, and ask whether to update it.
- If NO: proceed through all steps below.

## Step 1: Scan and classify files

List all files recursively from the current directory (skip: .git/, node_modules/, __pycache__/).

For each file, classify as one of:
- `ementa` — syllabus, curriculum, program document
- `livro` — textbook or book PDF
- `slides` — PPTX, PDF of presentations
- `apostila` — course notes, handout
- `notas` — lecture notes (.md, .txt)
- `exercicios` — exercises, problem sets
- `resumo` — summaries
- `prompt` — AI prompt files
- `config` — CLAUDE.md, settings.json, .gitignore, etc.
- `codigo` — source code, scripts
- `complementar` — supplementary material
- `desconhecido` — cannot classify

## Step 2: Determine citation style

Ask: "Qual estilo de citação usar? (1) ABNT NBR 6023 (padrão recomendado) ou (2) APA 7ª edição?"

If the professor does not answer, default to ABNT and record in `hypotheses`.

## Step 3: Show classification and request confirmation

Display a Markdown table of all classified files:

| Caminho | Tipo | Observação |
|---------|------|-----------|

Then show the directory structure that will be created:

```
.super-professor/    → estado e configuração do plugin
aulas/               → artefatos por aula (criado quando a primeira aula for iniciada)
```

Ask: "Posso criar os diretórios que faltam e gravar o manifest? (sim/não)"

**STOP and wait for explicit "sim" before creating anything.**

## Step 4: Create structure and write manifest

After "sim":
1. Create `.super-professor/` if it doesn't exist
2. Create `.super-professor/templates/` if it doesn't exist
3. Create `.super-professor/docs/qa/` if it doesn't exist
4. Copy templates from `~/.claude/super-professor/templates/` to `.super-professor/templates/` (if source exists)
5. Copy quality contracts from `~/.claude/super-professor/docs/qa/quality-contracts.md` to `.super-professor/docs/qa/quality-contracts.md` (if source exists)
6. Write `.super-professor/repo-manifest.md`

If `~/.claude/super-professor/` does not exist: warn the professor that the plugin data directory is missing and that `/lesson-qa` will not have access to quality contracts. Suggest running the plugin install script.

## GUARDRAILS (NEVER violate these)

- NEVER delete or move existing files
- NEVER create files outside `.super-professor/` without explicit request
- NEVER generate lesson content or fill briefing fields
- NEVER assume the discipline name if it's not clear from files — ask

## Output format: repo-manifest.md

Write to `.super-professor/repo-manifest.md` with this exact structure:

```markdown
---
schema: super-professor/repo-manifest/v1
generated_at: <ISO8601 timestamp>
---

# Repo Manifest

## Disciplina
name: <name or "não definida — perguntar no lesson-intake">
root_path: <absolute path to repo root>

## Configuração
citation_style: ABNT
default_lesson_duration_minutes: 45
aulas_directory: aulas/

## Materiais encontrados

| Caminho | Tipo | Descrição breve |
|---------|------|-----------------|
<one row per classified file>

## Estrutura criada

| Diretório | Propósito |
|-----------|-----------|
| .super-professor/ | Estado e configuração do plugin |
| aulas/ | Artefatos gerados por aula (criado na primeira aula) |

## Hipóteses registradas

<bulleted list of assumptions, or "Nenhuma">
```
