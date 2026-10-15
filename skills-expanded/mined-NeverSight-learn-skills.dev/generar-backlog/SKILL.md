---
name: generar-backlog
description: Despieza un PRD + Technical Design Document en un backlog ordenado de specs implementables, cada una lista para arrancar un ciclo de Spec-Driven Development (SDD). Use when the user asks to break down, decompose, or turn a PRD/technical design into a backlog, roadmap, list of features, or list of specs to implement.
---

# PRD + Tech Design → Backlog Decomposer

## Goal

Turn an approved `PRD.md` and `TECH-DESIGN.md` (with its ADRs) into an ordered backlog of
implementable specs — the missing bridge between "I have a product and an architecture" and
"I know what to build first." Each backlog item should be scoped so it can become a single SDD
change (one `sdd-new`/spec-driven cycle), not a whole feature area and not a single button.

This skill does not run SDD itself and does not write code — it produces the map that the SDD
cycle will consume one item at a time.

## Required Input

- `PRD.md` — required.
- `TECH-DESIGN.md` and its `adrs/*.md` — required. Decomposition without the architecture produces
  backlog items that don't respect component boundaries.

If either is missing, stop and ask for it.

## Workflow

1. Read `PRD.md` and `TECH-DESIGN.md` (+ ADRs) fully.
2. Identify natural implementation units from what both documents already establish: the flows and
   acceptance criteria in the PRD, and the component/data boundaries in the TDD. Do not invent
   scope that isn't traceable to one of these two documents.
3. Size each unit so it is realistically a single SDD cycle: big enough to be a coherent slice of
   value, small enough to specify, design, and implement without becoming its own mini-project. A
   backlog item titled "el sistema" is too big; one titled "cambiar el color de un botón" is too
   small — flag either extreme instead of accepting it silently.
4. Order the backlog by dependency, not by guessed priority: an item that other items require
   (e.g., the data model or auth before anything that uses them) goes first, regardless of how
   interesting it is.
5. For each item, flag whether it likely needs **domain-specific business rules as context** —
   heuristic: the item touches specialized calculations, regulated logic, or terminology that
   goes beyond what a generic PRD/TDD would define (e.g., an accounting module's chart-of-accounts
   rules). Do not assume every project has this — most won't. When flagged, note explicitly: "antes
   de generar la spec de este ítem, comparte tu documentación de reglas de negocio de este dominio
   como contexto, si la tienes" — the skill does not generate or ask for that documentation itself,
   it only flags where it will matter.
6. Present the draft backlog to the user before finalizing. Ask explicitly: does the order make
   sense, does any item need splitting or merging, and for the flagged items — do they already have
   domain rules documented that should be noted here? Wait for the answer before writing the file.
7. Write `BACKLOG.md` at the project root.

## Output Format (`BACKLOG.md`)

```markdown
# Backlog: {Nombre del proyecto}

| # | Item | Alcance | Depende de | Contexto extra requerido |
|---|---|---|---|---|
| 1 | {Nombre} | {1 línea} | — | — |
| 2 | {Nombre} | {1 línea} | #1 | Reglas de negocio de {dominio} |

## Cómo usar este backlog

Cada ítem es una spec independiente. Al implementarlo, arrancá un ciclo de Spec-Driven
Development (`sdd-new` o el flujo equivalente de tu harness) usando este ítem como el
"change" — no el proyecto completo. Si la columna "Contexto extra requerido" tiene algo,
compartilo como contexto al generar la spec de ese ítem.
```

## Quality Gate

Before returning, silently check:

- Every backlog item traces back to something explicit in the PRD or TDD — nothing invented.
- No item is sized as "the whole project" or as a single trivial change.
- Dependencies are acyclic and foundational items precede what depends on them.
- Domain-heavy items are flagged for extra context — not silently assumed to need it, and not
  silently skipped either.
