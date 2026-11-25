---
name: qa-test-generation
description: Heuristics for generating comprehensive test checklists by change type. Used by /task-complete Etapa 1.7 to auto-create test steps.
---

# QA Test Generation

> Generate structured test checklists from acceptance criteria + modified files.
> Output: `TestStep[]` for `task.meta.test_checklist`.

---

## 🎯 PURPOSE

Automatically produce a comprehensive, multi-path test checklist when a task is being completed. The checklist covers **happy path, error cases, edge cases, boundary values, empty states, and permissions** — never just the happy path.

---

## 🔍 HEURISTICS BY CHANGE TYPE

### 1. UI Component Changes

**Detect:** Files matching `*.tsx`, `*.css`, `*.module.css` in `components/`, `features/`, `pages/`

| # | Test Step Template | Type | Category |
|---|-------------------|------|----------|
| 1 | Component renders without errors | auto | unit |
| 2 | All interactive elements are clickable (cursor: pointer) | manual | visual |
| 3 | Responsive: renders correctly on mobile (≤640px) | manual | visual |
| 4 | Responsive: renders correctly on tablet (641–1024px) | manual | visual |
| 5 | Dark mode: colors adapt correctly | manual | visual |
| 6 | Empty state: shows fallback when no data | manual | e2e |
| 7 | Loading state: shows skeleton/spinner during fetch | manual | visual |
| 8 | Error state: shows error message on API failure | manual | e2e |
| 9 | Hover/focus states match DS tokens | manual | visual |
| 10 | Accessibility: keyboard navigable (Tab/Enter/Escape) | manual | manual |
| 11 | Text content does not overflow containers | manual | visual |

### 2. API Endpoint Changes

**Detect:** Files matching `api/*.py`, `routes/*.ts`

| # | Test Step Template | Type | Category |
|---|-------------------|------|----------|
| 1 | Returns 200 with valid input | auto | integration |
| 2 | Returns 400 with invalid/missing fields | auto | integration |
| 3 | Returns 404 for non-existent resource | auto | integration |
| 4 | Returns 401/403 without authentication | auto | integration |
| 5 | Handles empty request body | auto | integration |
| 6 | Handles duplicate/conflict data (409) | auto | integration |
| 7 | Response schema matches TypeScript types | auto | unit |
| 8 | Pagination works correctly (if applicable) | auto | integration |
| 9 | Large payload doesn't timeout | manual | integration |

### 3. Backend Logic Changes

**Detect:** Files matching `crud/*.py`, `services/*.py`, `utils/*.py`, `schemas/*.py`

| # | Test Step Template | Type | Category |
|---|-------------------|------|----------|
| 1 | Function returns expected result for valid input | auto | unit |
| 2 | Function raises/returns error for invalid input | auto | unit |
| 3 | Edge case: empty/null/zero values handled | auto | unit |
| 4 | Edge case: boundary values (max int, empty string) | auto | unit |
| 5 | Concurrent operations don't corrupt data | manual | integration |
| 6 | Database constraints enforced (unique, foreign key) | auto | integration |

### 4. Styling Changes

**Detect:** Files matching `*.css`, `*.module.css`, `tokens.*`

| # | Test Step Template | Type | Category |
|---|-------------------|------|----------|
| 1 | Uses DS tokens (not hardcoded values) | auto | unit |
| 2 | Color contrast ratio ≥ 4.5:1 (AA) | manual | visual |
| 3 | Animations are smooth (no jank) | manual | visual |
| 4 | No layout shifts on load | manual | visual |

### 5. SDK/Type Changes

**Detect:** Files matching `sdk/*.ts`, `types.ts`, `domain/*.ts`

| # | Test Step Template | Type | Category |
|---|-------------------|------|----------|
| 1 | TypeScript build passes (`tsc --noEmit`) | auto | unit |
| 2 | New types are exported from index | auto | unit |
| 3 | SDK method calls correct API endpoint | auto | integration |
| 4 | Response type matches API schema | auto | unit |

### 6. Workflow/Skill Changes

**Detect:** Files matching `workflows/*.md`, `skills/*/SKILL.md`

| # | Test Step Template | Type | Category |
|---|-------------------|------|----------|
| 1 | Markdown syntax is valid | auto | unit |
| 2 | Referenced files/paths exist | auto | unit |
| 3 | Referenced commands run without error | manual | integration |
| 4 | Workflow steps are in logical order | manual | manual |

---

## 📋 GENERATION PROCESS

```
1. Read acceptance criteria from task body/meta
2. Read list of modified files from Resumo de Execução
3. For each file:
   a. Classify by change type (UI/API/Backend/Styling/SDK/Workflow)
   b. Select applicable heuristic table
   c. Generate TestStep for each row, customizing description to actual change
4. Add acceptance-criteria-specific steps (from task body)
5. Deduplicate (same test from different files → keep one)
6. Assign IDs: ts-1, ts-2, ...
7. Save via bridge.py --generate-tests OR direct API
```

---

## ⚙️ OUTPUT FORMAT

Each generated step follows this schema:

```json
{
  "id": "ts-1",
  "description": "OKR card renders without errors when key_results is empty",
  "type": "auto",
  "category": "unit",
  "status": "pending",
  "result_comment": null,
  "tested_by": null,
  "tested_at": null
}
```

---

## 🚫 ANTI-PATTERNS

| ❌ Don't | ✅ Do |
|----------|-------|
| Generate only happy path tests | Cover error, edge, boundary, empty states |
| Generic descriptions ("test UI") | Specific ("OKRCardExpanded shows 0% when no KRs") |
| All tests as `manual` | Classify auto vs manual based on tooling |
| Skip styling/visual tests | Include visual checks even if manual |
| Over-generate for trivial changes | Scale tests proportionally to change complexity |

---

## 🔗 USED BY

| Workflow | Step |
|----------|------|
| `/task-complete` | Etapa 1.7 (QA Test Checklist Gate) |
| `/fix-tests` | Step 2 (Analyze + regenerate if needed) |
