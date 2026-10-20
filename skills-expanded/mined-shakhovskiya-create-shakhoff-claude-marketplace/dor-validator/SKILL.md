---
name: dor-validator
description: "Validates Definition of Ready for tasks before sprint execution. Checks mandatory criteria (title, description, AC, test approach, dependencies) and conditional criteria (PRD link, design link, expected ADR). Used by sprint-orchestrator before each sprint starts."
---

# DoR Validator

Definition of Ready gate перед стартом sprint.

## Когда применять

- Phase 5.2 каждого sprint
- Запускается sprint-orchestrator'ом перед началом sprint execution
- Применяется к каждой task в sprint

## Mandatory criteria

Эти проверки ВСЕГДА:

### 1. Title clear

- Task имеет non-empty title
- Title imperative form ("Implement X", "Refactor Y", не "Maybe consider...")
- Title <= 100 chars

### 2. Description present

- Task имеет description >= 50 chars
- Description explains WHAT и WHY
- Не just "fix bug" - нужно more context

### 3. AC defined and testable

- Минимум 1 AC присутствует
- Each AC:
  - Specific (не vague "make it work")
  - Testable (clear pass/fail)
  - User-focused или behavior-focused (не implementation detail)
  - Verifiable without subjective interpretation

### 4. Test approach defined

- Test approach field non-empty
- Specifies type of tests (unit/integration/e2e/property-based)
- Specifies what будет тестироваться
- Specifies hopw will verify

### 5. Dependencies known

- Dependencies field present (может быть "None")
- If dependencies listed - all referenced tasks exist
- No circular dependencies

## Conditional criteria

Применяются если condition met:

### 6. PRD link (when user-facing)

**Condition**: Task affects user-visible functionality (определяется по описанию)

**Requirement**:
- Link к PRD document, OR
- Explicit "no PRD needed - reason" (например для internal refactoring без UX impact)

**Detection heuristics**:
- Description mentions "user", "UI", "interface", "feature", "experience"
- Task title imperative для user-visible action ("User can register")
- Increment includes UI/UX deliverables

### 7. Design link (when UI changes)

**Condition**: Task includes UI changes

**Requirement**:
- Link to design (Figma, Sketch, attached image)
- OR explicit "no UI mockup needed - reason"

**Detection**:
- Description mentions "screen", "page", "form", "modal", "component"
- Increment includes frontend files (`*.tsx`, `*.vue`, etc.)

### 8. Expected ADR (when arch decisions)

**Condition**: Task involves architectural decisions

**Requirement**:
- Expected ADR title or number, OR
- Statement "design within task" если decision will be ad-hoc

**Detection**:
- Description mentions "architecture", "design", "approach", "framework choice"
- New module/service introduction
- Significant cross-cutting concern

### 9. API contract (when API changes)

**Condition**: Task changes API surface

**Requirement**:
- Link к API specification (OpenAPI, GraphQL schema), OR
- Statement "designed in task with documentation" если new API

**Detection**:
- Description mentions "endpoint", "API", "route"
- Increment includes API definition files

## Workflow

### 1. Read task

```bash
cat .sprints/active/tasks/T-{N}.md
```

### 2. Check each mandatory criterion

For each: PASS / FAIL with reason.

### 3. Detect applicable conditional criteria

Apply heuristics на task description, AC, increment.

### 4. Check applicable conditionals

For each detected: PASS / FAIL.

### 5. Generate validation report

Save `.sprints/active/dor-validation-T-{N}.md` через `dor.template.md`.

### 6. Verdict

**PASS**:
- All mandatory: PASS
- All applicable conditional: PASS or explicit "not required"
- Task can proceed

**FAIL**:
- Any mandatory: FAIL → BLOCK task
- In strict mode: any conditional FAIL → BLOCK
- In lenient mode: conditional FAIL → WARN

### 7. Resolution

If FAIL - block sprint start, return error to caller:

```
DoR validation FAILED for T-2:
  ✓ Title clear
  ✓ Description present
  ✗ AC defined and testable: AC #2 vague "should be fast" - needs specific threshold
  ✓ Test approach defined  
  ✓ Dependencies known
  
  Conditional:
  ✗ PRD link: detected user-facing change but no PRD link or "not needed" statement

Resolution required:
  1. Reformulate AC #2 with specific performance threshold
  2. Add PRD link or explicit "no PRD needed - reason"

Task cannot enter sprint until DoR validation passes.
```

## Integration с claude-solo-factory kit (если установлен)

Kit имеет skills для creating PRD и ADR (`prd-writer`, `adr-writer`). DoR validator может **detect kit presence** и give actionable suggestions.

### Detection

```bash
KIT_PRD=false
KIT_ADR=false
test -f .claude/skills/prd-writer/SKILL.md && KIT_PRD=true
test -f .claude/skills/adr-writer/SKILL.md && KIT_ADR=true
```

### Если PRD link required но missing

**Standard error message**:
```
DoR FAIL: PRD link required for user-facing functionality but not provided.
```

**Augmented с kit detection**:
```
DoR FAIL: PRD link required for user-facing functionality but not provided.

Kit available - you can create PRD using:
  Apply skill `prd-writer` (in claude-solo-factory kit)
  
Workflow:
  1. Run kit's `interview` skill для discovery если brief absent
  2. Run kit's `prd-writer` для PRD generation
  3. Save to docs/specs/<feature>/prd.md
  4. Re-run DoR validation with --prd-link=docs/specs/<feature>/prd.md
```

Suggestion - не enforcement. User может accept "no PRD - reason" если действительно не нужно.

### Если ADR expected но missing

**Standard**:
```
DoR FAIL: Architectural decision detected but no ADR reference provided.
```

**Augmented**:
```
DoR FAIL: Architectural decision detected but no ADR reference provided.

Kit available - create ADR using:
  Apply skill `adr-writer` (in claude-solo-factory kit)
  
Format:
  docs/architecture/adr/NNNN-decision-slug.md
  
Run kit's adr-writer skill - it will:
  - Auto-number (next available NNNN)
  - Apply ADR template (Status/Context/Decision/Consequences)
  - Document alternatives considered
```

### `code-discipline` skill

If `.claude/skills/code-discipline/SKILL.md` exists - DoR validation учитывает Karpathy rules:

- Task description должен specify **success criteria** (Karpathy rule 4 - goal-driven)
- Description should not имеет vague terms ("improve", "make better")
- Should surface assumptions explicitly (не "Smith's algorithm" без ссылки)

These checks added to DoR mandatory criteria when kit present.

## Strictness handling

**strict** (default):
- All FAILs block
- Both mandatory and applicable conditional must PASS

**lenient**:
- Mandatory FAILs block
- Conditional FAILs WARN, allow proceed

**permissive**:
- Only most critical mandatory checked (title, AC presence)
- All else WARN

## Special cases

### Audit/research tasks

For audit caller skills (sdlc-audit etc.):
- Test approach: typically "verify findings.json valid against schema"
- AC: typically "all checklist items addressed or skipped with justification"
- PRD/design: usually N/A
- ADR: not applicable

These conditional criteria smartly не apply для audit tasks.

### Documentation tasks

For docs-only tasks:
- Test approach: "verify links, examples run, format validates"
- PRD: usually N/A unless docs are part of feature spec
- Design: N/A

### Migration tasks

For data migrations:
- AC must include rollback verification
- Risk section mandatory (not just "low risk")
- Test approach: dry-run + small batch + full

## Output

Per task: `.sprints/active/dor-validation-T-{N}.md`

Summary in `.sprints/active/_state.json`:
- DoR validation status per task
- Block reasons if any
