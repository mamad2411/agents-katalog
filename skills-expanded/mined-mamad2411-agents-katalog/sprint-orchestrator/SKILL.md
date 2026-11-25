---
name: sprint-orchestrator
description: "Central coordinator for ai-scrum sprint cycles. Manages full lifecycle from /sprint:start through task decomposition, sprint execution, reviews, and HTML report generation. Activated when user invokes /sprint:start or when caller skill declares sprint_required: true."
---

# Sprint Orchestrator

Центральный координатор всего lifecycle ai-scrum sprint cycle.

## Когда применять

- Команда `/sprint:start` запущена (явный пользовательский trigger)
- Skill из другого плагина имеет `sprint_required: true` в frontmatter (auto-activation)
- Любая команда требующая sprint discipline

## Lifecycle phases

Orchestrator управляет 9 phases в строгом порядке:

### Phase 0: Pre-flight

1. **Detect project root**: подняться по дереву до `.git`, `package.json`, `pyproject.toml`, `go.mod`
2. **Read config**: 
   - Default из `config/default.config.yaml`
   - Overlay из `.sprints/config.yaml` если есть
3. **Parse arguments**:
   - `--plan=<path>` if specified - mark for Phase 0.5
   - `--size=<small|medium|large|auto>` - size mode
   - `--strict|--lenient|--permissive` - strictness override
4. **Initialize storage**: создать `.sprints/active/` если нет
5. **Auto-add to .gitignore** если `git.auto_gitignore: true`:
   - Добавить `.sprints/active/` в `.gitignore` если не там
   - НЕ добавлять `.sprints/archive/` (коммитится в git)
6. **Generate task UUID**: для уникальной идентификации этого sprint cycle
7. **Load strictness level** из config (с применением CLI override если был)

### Phase 0.5: Plan import (NEW в v0.1.1)

Если `/sprint:start` был вызван с `--plan=<path>` argument:

1. Apply skill `plan-importer`:
   - Read plan file
   - Detect format (superpowers, prd-writer, manual, etc.)
   - Extract structured info (scope, mentioned tasks, ACs, references, dependencies)
   - Save normalized output в `.sprints/active/imported-plan.md`

2. Update `_state.json`:
   - `plan_imported: true`
   - `plan_source: <path>`
   - `plan_format: <detected>`
   - `plan_confidence: <HIGH|MEDIUM|LOW>`

3. Continue к Phase 1 (context investigation) - imported plan дополняет, не заменяет context

Если `--plan` не указан - skip Phase 0.5, переход к Phase 1.

**Важно**: Imported plan **не used as final decomposition**. Это input information для task-decomposer's Mode B (enrichment). Наш алгоритм декомпозиции применяется независимо от формата source.

### Phase 1: Context investigation

Применить skill `context-investigator`. Output:
- `.sprints/active/context-snapshot.md` - что узнали о проекте

Если context-investigator не может определить domain (нет brief, glossary, README):
- В strict/lenient mode - **спросить пользователя** о domain
- В permissive mode - продолжать с generic assumptions

### Phase 2: Task decomposition

Применить skill `task-decomposer`. Input:
- Scope description (от user или caller skill)
- context-snapshot.md
- Methodology section из caller skill (если есть, парсится через `methodology-parser`)

Output:
- `.sprints/active/plan.md` с tasks (T1, T2, ...) и proposed sprints

### Phase 3: Decomposition review (до полного PASS)

Запустить subagent `decomposition-reviewer` (fresh context).

Iterations:
- Iteration 1: review initial decomposition
- If REVISE: task-decomposer пересматривает, iteration 2
- If REVISE again: iteration 3
- Limit: `decomposition_review_max_iterations` из config (default 5)

После 5 iterations без APPROVED - **escalate to user** с явным выбором:
1. Accept current decomposition with warnings
2. Cancel task and re-plan from scratch
3. Provide manual decomposition

### Phase 4: Plan lock

После APPROVED:
- Plan фиксируется
- Tasks нельзя кардинально менять без `/sprint:replan`
- Active sprint = Sprint 1

### Phase 5-N: Sprint execution loop

Для каждого sprint в plan:

#### 5.1: Pre-sprint
- Прочитать HANDOFF.md (handoff-keeper) для context handoff
- Установить sprint goal
- Locked DoD criteria (default + applicable conditional + custom)

#### 5.2: DoR validation для всех tasks в sprint
- Для каждой task в sprint - запустить `dor-validator`
- Если any task fails DoR - blocker, нельзя стартовать sprint
- Resolution: caller updates tasks, re-validate

#### 5.3: Task execution loop
- Для каждой task - применить `sprint-executor`
- Hooks active:
  - `pre-tool-use-checkin` (warns/blocks if no recent checkin)
  - `pre-tool-use-test-first` (blocks production code without test)
  - `post-tool-use-tracker` (tracks tool history silently)
- After each task: AC verification

#### 5.4: Sprint validation gate (DoD)
- Запустить `dod-validator`
- Если fails - BLOCK `/sprint:complete`
- Resolution: executor addresses blocking criteria

#### 5.5: Internal SE review
- Запустить subagent `senior-engineer` (fresh context)
- Apply provided SE prompt + extended test review
- Verdict: PASS / FAIL / WAIVE
- Findings logged

#### 5.6: External Codex review (if available)
- Detect codex-plugin-cc
- If available - запустить `codex-external-reviewer` через codex-bridge subagent
- If unavailable - graceful skip with logging

#### 5.7: Sprint retrospective
- Запустить subagent `retrospective-author` (fresh context)
- Generate retrospective.md

#### 5.8: HANDOFF.md update
- Запустить handoff-keeper subagent
- Validate update is meaningful (not just timestamp)
- Append to HANDOFF.md

#### 5.9: Sprint close
- Mark sprint as complete
- Move to next sprint

### Phase N+1: Final wrap-up

После всех sprints закрыты:

1. **Final retrospective** - macro level (cross-sprint trends)
2. **HTML report generation**:
   - Detect design system (skill `design-system-detector`)
   - Generate self-contained HTML (skill `html-report-generator`)
   - Save to `.sprints/active/report.html`
3. **Archive**:
   - Move `.sprints/active/*` to `.sprints/archive/<TS>-<task-uuid>/`
   - Clean active directory
4. **Final HANDOFF.md update** (executive summary всего cycle)

### Phase N+2: User notification

Output to user:
- Total time vs estimated
- Sprints summary
- Findings count (если applicable)
- Path к HTML report
- Suggested next steps

## State management

Active state в `.sprints/active/`:
- `_state.json` - current phase, active sprint, progress
- `plan.md` - locked plan
- `context-snapshot.md`
- `tasks/*.md`
- `sprint-{N}.md`
- `tool-history.log` (continuous)
- `reviews/*.md`

State persists между Claude Code sessions - можно continue после restart.

## Error handling

### LSP MCP unavailable
- Log "LSP integration unavailable, falling back to CLI tools"
- Continue with degraded functionality

### Codex unavailable
- Log "Codex review skipped: codex-plugin-cc not installed" or "API unreachable"
- Continue without external review (acceptable in `lenient`/`permissive`, BLOCK in `strict` if "external_review" was REQUIRED for this sprint)

### Tool failures (pydeps errored, etc.)
- Mark step as `failed` with reason
- Sprint executor должен либо use fallback либо declare insufficient coverage
- Failure не cancel'ит sprint - just affects DoD criteria

### Hook BLOCK
- HARD GATE - executor cannot bypass without explicit override commands
- Override commands logged for audit

### State corruption (unlikely)
- `_state.json` malformed → recover from latest sprint-{N}.md
- If unrecoverable → backup current state, prompt user to /sprint:cancel

## Configuration overrides

В `.sprints/config.yaml` пользователь может override:
- `strictness`: strict | lenient | permissive
- `discipline.test_first.enabled`: bool
- `reviews.external.required`: bool
- DoD custom additions (через `/sprint:dod-customize` wizard)

## Integration points

### With other plugins

Orchestrator detects и интегрируется:
- **codex-plugin-cc**: для external review (если установлен)
- **LSP MCPs**: для type checking, references analysis
- **Issue tracker MCPs**: для sync (если установлен и opted in)

### With caller skills

Caller skill могут declare:
- `sprint_required: true` (auto-activation)
- `sprint_workflow: phase-based | task-based`
- `<!-- methodology -->` секция с checkpoints

### With user

Direct invocation: `/sprint:start "<scope>"`

## Output specification

Финальный output user после complete sprint cycle:

```
✓ Sprint cycle complete: {{TASK_NAME}}

Summary:
  Sprints: {{N}} (all PASSED)
  Tasks: {{M}} ({{X}} done, {{Y}} skipped, {{Z}} failed)
  Total time: {{ACTUAL}} (estimated: {{ESTIMATED}}, variance: {{V}}%)
  
Reviews:
  Internal SE: {{COUNT}} reviews, {{ISSUES}} findings
  External Codex: {{STATUS}}

Reports:
  HTML report: .sprints/archive/{{TS}}/report.html
  Retrospective: .sprints/archive/{{TS}}/retrospective.md
  Updated HANDOFF.md: {{LINES_ADDED}} lines

Next steps:
  - Review HTML report for full details
  - Address findings in BACKLOG (if applicable)
  - Continue with /sprint:start "next task" or /audit:full --depth=...
```

## Принципы

1. **Sequential, не parallel** - sprints в order, dependencies respected
2. **Fail-secure**: при ошибках - block, не continue silently
3. **Honest reporting**: все skipped/failed steps documented с reason
4. **Discoverable**: state visible в `.sprints/`, можно inspect anytime
5. **Reproducible**: same input + same git state → similar outcome (с tolerance for LLM nondeterminism)
