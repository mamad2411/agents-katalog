---
name: requirements-clarification
description: Turns a vague request into a few pointed questions and written acceptance criteria before any code is written.
---

# Requirements clarification

Clarify before building. Write no production code in this skill.

## Steps

1. Read the request twice. Underline words that can mean two things: "fast", "users", "export", "better", "soon".
2. Look in the code and docs for answers first: existing behavior, similar features, roles and permissions, limits, and data that already exists. Do not ask a question the repository can answer.
3. Sort what is unknown into three bins. Blocks the design: ask. Changes effort but not the design: ask if cheap, otherwise assume. Detail that can be changed later: assume.
4. Ask at most five questions, most important first. Make each one concrete and answerable in a line, offer your best guess as the default, and show what each answer changes. Prefer "Should export include archived projects? Default: no, because the list view hides them" over "What should export include?".
5. Cover these areas: who does it and with which permission, the trigger and the inputs, the result and where it appears, edge cases (empty, huge, duplicate, concurrent, failed), what must not change, and scale or time limits.
6. When answers arrive, write acceptance criteria in plain Given, When, Then lines, each testable by a person or an automated test. Add explicit non-goals.
7. List remaining assumptions and who should confirm each.

## Rules

- Never invent business rules and present them as facts.
- Never exceed five questions in one round.
- Do not propose technology unless a requirement forces it.

## Report

Questions with defaults, then after answers: acceptance criteria, non-goals and assumptions.
