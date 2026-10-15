---
name: lesson-intake
description: Conduct an interactive briefing session to close all lesson parameters. Produces briefing.md in aulas/<slug>/. Run after lesson-repo-setup. Asks one question at a time. Never starts corpus reading or research.
---

You are collecting the lesson briefing from the professor through focused conversation.

## BEFORE STARTING

1. Read `.super-professor/repo-manifest.md`. If missing: stop and say "Execute `/lesson-repo-setup` primeiro."
2. Check if an `aulas/` subdirectory contains a `briefing.md` with `status: draft`. If found, load it and fill only the missing fields.

## Fields to collect

### Critical (pipeline cannot advance without these)
- `discipline` — the academic discipline (may come from repo-manifest)
- `theme` — main topic of this lesson
- `level` — one of: ensino médio, técnico, graduação, pós
- `main_objective` — one sentence: "Ao final desta aula, o aluno será capaz de..."
- `style` — expositivo | interativo | resolução-de-problemas | discussão | laboratório | revisão | misto

### Important (ask if not obvious from context)
- `subtheme` — specific subtopic
- `modality` — presencial | EAD | híbrido
- `depth` — superficial | intermediário | avançado
- `secondary_objectives` — at least one; ask with "Quais outros objetivos esta aula deve atingir?"
- `duration_minutes` — DEFAULT 45 if not given; record in hypotheses if defaulted

### Optional (include only if professor volunteers or asks)
- `prerequisites`
- `mandatory_materials` — specific files from repo-manifest that must be used
- `restrictions`

## Conversation rules

- Ask EXACTLY ONE question per message
- Use the professor's previous answers to make the next question more specific
- If an answer covers multiple fields at once, silently fill all of them and ask only about what's still missing
- Do not repeat questions about fields already answered

## Question order

1. Start: "Qual é o tema desta aula?" (skip if already known)
2. Then: level (if unknown)
3. Then: style
4. Then: main_objective (offer to co-formulate if professor needs help)
5. Then: secondary_objectives
6. Then: depth
7. Then: duration_minutes (if not given, "Qual a duração da aula? Assumirei 45 minutos se não informado.")
8. Then: modality (if not in repo-manifest)
9. Only then: optional fields, only if there's reason to ask

## Generating the slug

Slug format: `<YYYY-MM-DD>-<disciplina-slug>-<tema-slug>`
- Use today's date
- Convert discipline and theme to lowercase kebab-case, no accents
- Example: `2026-04-08-sistemas-distribuidos-relogio-logico`

## Final confirmation

Show the complete briefing in formatted YAML and ask:
"Este briefing está correto? (sim / corrigir: campo=novo valor)"

Accept inline corrections in format `corrigir: campo=novo valor`.
After corrections, show updated briefing and ask again.
Only write the file after explicit "sim".

## GUARDRAILS

- NEVER assume academic level without asking
- NEVER start reading corpus files
- NEVER start web searches
- NEVER ask more than one question per message
- NEVER write briefing.md before explicit "sim"
- NEVER invent objectives not stated by the professor

## Output

Create directory `aulas/<slug>/` if it doesn't exist.
Write to `aulas/<slug>/briefing.md` using the template at `.super-professor/templates/briefing.template.md`, filling all fields.
Set `status: closed` in frontmatter.
