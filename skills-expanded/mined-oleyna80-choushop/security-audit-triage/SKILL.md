---
name: security-audit-triage
description: "Map pentest reports and CVEs to real code. Classify each as confirmed/partial/not confirmed with file:line evidence. Assess API risk (injection, XSS, auth bypass), check OWASP Top 10 patterns, evaluate attack surface. Get prioritized P0/P1 fix scope. Read-only analysis — use before any security fix work."
user-invocable: true
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(head *)
  - Bash(tail *)
  - Bash(sort *)
  - Bash(uniq *)
  - Bash(wc *)
  - Bash(npm run *)
  - Bash(npm audit *)
  - Bash(npx vitest *)
  - Bash(npx tsc *)
  - Bash(npx eslint *)
  - Bash(curl *)
  - Bash(fuser *)
  - Bash(rg *)
  - Bash(jq *)
---

# Skill: Security Audit Triage

## Triggers
- "проверь security аудит"
- "валидация отчета"
- "подтверди findings"

## Objective
Отделить подтвержденные риски от гипотез и подготовить реалистичный backlog фиксов без over-engineering.

## Workflow
1. Собрать attack surface и точки входа (API, storage, proxy, deps).
2. Проверить каждый finding в коде и присвоить статус:
   - `confirmed`
   - `partially confirmed`
   - `not confirmed`
3. Пересчитать severity с учетом текущего runtime контекста проекта.
4. Сформировать минимальный safe remediation set (P0/P1) и deferred set (P2).
5. Зафиксировать результат в report + ссылками на файлы.

## Constraints
- Reviewer-mode: read-only до explicit подтверждения на implementation.
- Не копировать severity из внешнего отчета без проверки.
- Учитывать текущую архитектуру (`SQL-first`, reverse proxy, launch constraints).

## Output
- Findings matrix (`status`, `adjusted severity`, `evidence`)
- P0/P1 remediation scope
- Explicit list of risky changes that can break runtime

## Handoff
- **Success condition**: findings matrix готова, P0/P1 scope зафиксирован.
- **Next**: security-hardening-pass (при наличии confirmed P0/P1)
- **Auto-proceed**: 🟢 YES (переход к hardening без паузы)
- **Hard stop**: NO
