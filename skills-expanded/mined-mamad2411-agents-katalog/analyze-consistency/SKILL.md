---
name: analyze-consistency
description: Verify internal consistency of requirements.md and adherence to project rules before task generation. Use after scope confirmation, when the user asks to analyze or validate requirements, or after manual edits to requirements — automatically between Gate 2 and task generation. Produces consistency-report.md; does not modify requirements. Do NOT generate tasks.
depends:
  - nextstage-harness
---

# Analyze Consistency

Pre-execution validation: plan vs plan before coding.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md`. Load `{harness}/rules/*.mdc` when present for stack-specific checks.

## When to use

- After Gate 2 (`scope_confirmed`)
- User asks "analyze requirements" or "check consistency"
- After manual `requirements.md` edits

## Prerequisites

- `{product_root}/docs/versions/{version_san}/requirements.md` exists
- Create version directory if missing before writing report

## Workflow

### Step 1 — Index requirements

Read `requirements.md` and index:

- Main objective
- Features (title, precedence, acceptance criteria)
- NFRs
- Declared stack

### Step 2 — Run checks

Classify each as ✅ OK | ⚠️ Warning | ❌ Blocker:

**Feature integrity**

| Check | Failure level |
|-------|---------------|
| Every feature has title, description, acceptance criteria | ❌ Blocker |
| At least 2 acceptance criteria per feature | ⚠️ Warning |
| No circular precedence | ❌ Blocker |
| At least one root feature (no precedence) | ❌ Blocker |
| Frontend features mention test ids when E2E expected | ⚠️ Warning |

**Test coverage**

| Check | Failure level |
|-------|---------------|
| Backend features include unit test criteria | ⚠️ Warning |
| UI features include E2E criteria | ⚠️ Warning |
| Infra before domain on greenfield | ⚠️ Warning |

**Data model**

| Check | Failure level |
|-------|---------------|
| Clear "Data model and APIs" section | ❌ Blocker |
| All entities in features listed in data model | ❌ Blocker |
| FK creation order respected | ❌ Blocker |
| API endpoints for frontend consumption declared | ❌ Blocker |

**Alignment**

| Check | Failure level |
|-------|---------------|
| Features support stated objective | ⚠️ Warning |
| Out-of-scope features present | ⚠️ Warning |

Apply stack-specific checks from harness rules when they exist (Laravel/React checks are optional).

### Step 3 — Report

Save to `{product_root}/docs/versions/{version_san}/consistency-report.md`:

```markdown
# Consistency Report — {version_san}
**Date:** {date}
**Analyzed:** `{path}`

## Overall result
✅ 100% approved | ⚠️ Approved with reservations | ❌ Requires correction

## Blockers (❌)
...

## Warnings (⚠️)
...

## Passed (✅)
Count and summary

## Recommendations
Optional improvements
```

### Step 4 — Proceed decision

- **❌ Blockers:** Stop — ask user to fix requirements, then re-run
- **⚠️ Only warnings:** Ask fix now or proceed; user decides
- **100% ✅:** Inform auto-proceed to task generation; `execution_confirmed` implicit (skip Gate 3)

## Critical rules

- **Do not edit** `requirements.md` — report issues only
- Blockers prevent task generation without fix or explicit waiver
- If requirements missing → redirect to Gate 1 / `requirements-generator`

## Integration

```
Gate 2 → analyze-consistency → [100%] → task-generator
                            → [blockers] → fix requirements
```

Post-implementation: `code-reviewer` validates requirements × code — complementary, not a substitute.
