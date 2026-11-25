---
name: audit-orchestrator
description: "Orchestrates full SDLC audit across all phases. Use when running /audit:full or coordinating multiple audit phases. Manages depth control, scope, output artifacts, and final reporting."
sprint_required: true
sprint_workflow: phase-based
---

<!-- methodology:start -->
## Methodology checklist (for ai-scrum integration)

When ai-scrum plugin is installed, this skill triggers sprint cycle.
Below structure is parsed by ai-scrum's methodology-parser to generate sprint backlog.

### Phase 1: Setup & Discovery
- name: Detect project root and language stack
  mandatory: yes
  can_skip_if: never
  success_criteria: language-detection.json saved with at least one language detected
  effort: XS

- name: Read existing audit configuration
  mandatory: no
  can_skip_if: no audit.config.yaml exists
  success_criteria: thresholds and exclusions loaded if config exists
  effort: XS

### Phase 2: Architecture audit
- name: Architecture audit (apply architecture-audit skill)
  mandatory: yes
  can_skip_if: never
  success_criteria: architecture/findings.json valid against schema
  effort: M

### Phase 3: Domain audit
- name: Domain logic audit (apply domain-audit skill)
  mandatory: yes
  can_skip_if: never
  success_criteria: domain/findings.json valid against schema
  effort: M

### Phase 4: Code quality audit
- name: Code quality audit with SAST tools
  mandatory: yes
  can_skip_if: depth=quick (skip SAST tools, use Claude reading only)
  success_criteria: code/findings.json valid, hot files identified
  effort: L

### Phase 5: Test audit
- name: Test audit (coverage, quality, pyramid)
  mandatory: yes
  can_skip_if: never
  success_criteria: tests/findings.json valid, coverage gaps identified
  effort: M

### Phase 6: Security audit
- name: Security audit (SAST, secrets, CVEs, OWASP)
  mandatory: yes
  can_skip_if: never
  success_criteria: security/findings.json valid, secrets scan complete
  effort: M

### Phase 7: Docs audit
- name: Documentation drift detection
  mandatory: yes
  can_skip_if: never
  success_criteria: docs/findings.json valid, drift report generated
  effort: S

### Phase 8: Deploy audit
- name: Deployment configuration audit
  mandatory: yes
  can_skip_if: project has no CI/CD or deployment config
  success_criteria: deploy/findings.json valid
  effort: S

### Phase 9: Aggregation & Reporting
- name: Findings classification and deduplication
  mandatory: yes
  can_skip_if: never
  success_criteria: _findings-classified.json exists with all findings
  effort: S

- name: Backlog generation with priorities
  mandatory: yes
  can_skip_if: never
  success_criteria: BACKLOG.md generated with sorted findings and fix prompts
  effort: S

- name: Final report generation
  mandatory: yes
  can_skip_if: never
  success_criteria: INDEX.md, EXECUTIVE_SUMMARY.md, METRICS.md all present
  effort: XS
<!-- methodology:end -->

# Audit Orchestrator

Координирует выполнение полного SDLC аудита проекта.

## Когда применять

- Команда `/audit:full` запущена
- Нужно координировать несколько фаз аудита подряд
- Нужно управлять depth (quick/standard/deep) и scope для всех фаз

## Inputs

- `depth`: quick|standard|deep (default: standard)
- `scope`: путь относительно корня проекта (default: весь проект)
- `audit_timestamp`: для именования папки отчёта

## Workflow

### Phase 0: Setup

1. **Detect project root**: подняться по дереву до файла `.git`, `package.json`, `pyproject.toml`, `go.mod`, или подобного
2. **Read audit config** если есть `audit.config.yaml` в корне проекта - применить exclusions и custom thresholds
3. **Create output directory**: `docs/audit/<YYYY-MM-DD-HHmm>/`
4. **Detect languages** через skill `language-detector`
5. **Initialize tracking**: создать `docs/audit/<TS>/_progress.json` для отслеживания фаз

### Phase 1-7: Sequential audit phases

Запускать в строгом порядке (зависимости между фазами):

```
architecture → domain → code → tests → security → docs → deploy
```

Зачем такой порядок:
- Architecture первая - её результаты важны для понимания остальных
- Domain после architecture - бизнес-логика часто видна через архитектурный объектив
- Code после domain - чтобы понимать что есть hot path а что edge
- Tests после code - чтобы знать что должны защищать тесты
- Security в середине - может найти как design flaws так и code-level issues
- Docs ближе к концу - мы уже знаем что должно быть задокументировано
- Deploy последний - результаты предыдущих фаз могут указать на missing CI gates

### Per-phase execution

Для каждой фазы:

1. Update progress: `<phase>: in-progress`
2. Invoke соответствующий subagent (`architecture-auditor`, `domain-auditor` и т.д.)
3. Subagent выполняет фазу, пишет `findings.json` + supporting файлы в `docs/audit/<TS>/<phase>/`
4. Update progress: `<phase>: complete` или `<phase>: failed` с reason
5. **Continue к следующей фазе даже если текущая failed** - не блокируй весь аудит из-за одной проблемной фазы

### Phase 8: Aggregation

После всех фаз:

1. **Collect all findings** из `docs/audit/<TS>/*/findings.json`
2. Apply skill `findings-classifier`:
   - Дедупликация (одна и та же проблема может появиться в разных фазах)
   - Финальная severity assignment
   - Cross-phase correlation (например finding в `tests` который усиливает finding в `code`)
3. Apply skill `backlog-generator`:
   - Сортировка по `severity × business_impact / effort`
   - Назначение sequential IDs (`BLOCKER-001`, `CRITICAL-001` и т.д.)
   - Генерация `BACKLOG.md` с готовыми fix prompts

### Phase 9: Final artifacts

Создать:

- **INDEX.md** - точка входа со ссылками на все файлы
- **EXECUTIVE_SUMMARY.md** - 1 страница для не-разработчика
- **METRICS.md** - numerical health (coverage %, mutation %, complexity P95, dependency CVE count, и т.д.)
- **BACKLOG.md** - already created by backlog-generator

Использовать template `templates/audit-report.template.md`.

## Depth handling

Передавать `depth` параметр всем skills и subagents. Они должны respect его:

| Depth | Architecture | Domain | Code | Tests | Security | Docs | Deploy |
|-------|--------------|--------|------|-------|----------|------|--------|
| quick | Структурный анализ только | Базовый review | Без SAST tools | Без mutation | Без external tools | Только README check | CI/CD review |
| standard | + SAST tools | + DDD анализ | + ruff/mypy/eslint и т.д. | Coverage tools | + bandit/eslint-plugin-security | + drift detection | + IaC review |
| deep | + reverse-engineered C4 diagrams | + bounded contexts mapping | + manual review топ-5 hot files | + mutation testing | + git history scan + dependency CVE check | + setup verification | + container security review |

## Failure handling

Если фаза падает (subagent error, tool not available):

1. **Не останавливать audit** - продолжать с следующей фазы
2. Записать в `_progress.json`: phase failed, reason
3. В final INDEX.md - явно показать какие фазы incomplete и почему
4. Эти фазы можно перезапустить отдельно через `/audit:<phase>` после фикса корневой причины

## Output

Полный отчёт в `docs/audit/<YYYY-MM-DD-HHmm>/`. Чат-output:

```
SDLC Audit Complete: 2026-04-29-1430
Depth: standard
Scope: <project root>
Languages: python, typescript

Findings: 47
  BLOCKER:  2
  CRITICAL: 8
  HIGH:    15
  MEDIUM:  16
  LOW:      6

Top 3 critical:
  [BLOCKER-001] ... 
  [BLOCKER-002] ...
  [CRITICAL-001] ...

Report: docs/audit/2026-04-29-1430/INDEX.md
Backlog: docs/audit/2026-04-29-1430/BACKLOG.md

Next: /audit:fix next
```

## Принципы

1. **Sequential, не parallel** - subagent quota ограничена, и phases имеют зависимости
2. **Resilient** - один failed phase не должен валить весь audit
3. **Observable** - `_progress.json` показывает текущее состояние, можно мониторить из другой сессии
4. **Reproducible** - при том же commit и том же depth должен давать тот же набор findings (с точностью до недетерминизма LLM tools)
