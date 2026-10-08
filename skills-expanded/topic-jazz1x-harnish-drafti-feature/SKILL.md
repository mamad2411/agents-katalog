---
name: drafti-feature
version: 0.4.0
description: >
  Planning-based implementation spec PRD generator. Converts planning requirements into an implementation-ready spec.
  Triggers: "drafti-feature", "drafti", "drafti 피쳐", "이 기획서로 PRD 만들어", "create PRD from this planning doc",
  "피쳐 PRD", "feature PRD", "기획서 기반 구현 명세", "implementation spec from planning doc",
  "피쳐 설계", "feature design", or when a planning document is attached/referenced.
  Distinction from drafti-architect: planning document exists → feature, does not exist → architect.
ssl:
  logical:
    writes: ["docs/prd-{slug}.md", ".harnish/assets/*.jsonl"]
    idempotent: false
    rollback: "Step 7 HITL gate; 'overwrite' is explicit destructive — no auto backup"
---

# drafti-feature — Planning to Implementation Spec PRD

> Takes planning requirements and produces an implementation spec PRD focused on "how to build it."

## Bash Convention

Each Bash tool invocation is a fresh subshell. Every bash block re-declares `HARNISH_ROOT="${CLAUDE_PLUGIN_ROOT}"` inline; no persistent variables.

## Skill Chain

Can be invoked independently (planning doc required). Follow-up: "start implementation after review" → impl, or "/galmuri:ralphi to verify PRD consistency" → galmuri:ralphi (sibling plugin).

## Step 1: Requirement Parsing

Extract 4 items from the planning document:

| Item | Content |
|-----|------|
| Core Feature | User-visible changes (1~3 lines) |
| Success Metrics | KPI/goals (numeric or conditional) |
| User Flow | Happy path + branches |
| Non-Functional Requirements | Performance, security, accessibility |

**Gate**: all 4 items must be present before proceeding.
- 0 missing → proceed to Step 2.
- 1+ missing → ask the user for the missing items. Do not assume defaults. Re-evaluate after the user replies; if still missing → re-ask.

## Step 2: Existing Asset Query

Extract 3~5 core keywords, then:

```bash
HARNISH_ROOT="${CLAUDE_PLUGIN_ROOT}"
if [[ -n "$HARNISH_ROOT" ]]; then
  bash "$HARNISH_ROOT/scripts/query-assets.sh" \
    --tags "{keywords}" --format inject \
    --base-dir "$(pwd)/.harnish"
fi
```

If assets found, use as reference; if none, proceed anyway.

## Step 3: Codebase Exploration

Detect the language from project config files (`package.json`, `pyproject.toml`, `go.mod`, etc.), then explore affected files using core keywords.

1. **Keyword search**: Find related code files
2. **Filename patterns**: Find related components/modules
3. **Data models**: Find type definitions/interfaces/classes

Result: Affected file list + whether data model changes are needed → reflect in PRD §4.

## Step 4: Feature Flag Assessment (Optional)

**Not all features need a flag.** Design one only when the conditions below apply.

| Condition | Flag Needed | Not Needed |
|------|-----------|--------|
| User-facing service, gradual rollout needed | ✓ | |
| High-risk features such as payments/finance | ✓ | |
| Internal tools, CLI, libraries, infrastructure | | ✓ |
| Simple bug fixes, refactoring | | ✓ |

If flag needed → read `references/feature-flag-patterns.md` and:
- Flag key: `{feature_name}_enabled`
- Select rollout strategy (percentage/segment/manual)
- Kill switch conditions (error rate > 1%, p99 > 500ms, etc.)
- Rollback plan

If not needed → §2 (Flag design) is **omitted** from the output PRD. Section numbers `§1, §3, §4, ...` remain unchanged (do not renumber). Proceed to Step 5.

## Step 5: Implementation Spec Writing

**Foundation for task decomposition. Be specific about file paths, functions, and branch locations.**

§4.1 Affected files:
```
| File Path | Change Type | Description | Flag Branch |
```

§4.2 Functions/Components: Input → Behavior → Output

§4.3 Flag branch locations (only when flag exists): File | Function | Location | Condition

§4.4 Data model (only when DB changes exist): Added fields + migration + rollback safety

Read `references/prd-template.md` and write accordingly.

## Step 6: Edge Cases + Tests

**When flag exists**: Separate into ON/OFF/partial rollout cases
**When no flag**: Separate into normal/error/boundary value cases

§6 Test Criteria (Acceptance Criteria):
- Verify new feature behavior
- Verify existing feature regression
- (When flag exists) 100% restoration of existing behavior after rollback

## Step 7: Save + Asset Recording

**HITL** (before any file write):
> "PRD draft ready: §{sections present} ({with/without} flag). Save to `docs/prd-{slug}.md`? (y / n / edit-slug)"
>
> **If `docs/prd-{slug}.md` already exists**, the prompt becomes: *"`docs/prd-{slug}.md` already exists. (overwrite / n / new-slug)"* — `y` is **not** offered. Treat `overwrite` as explicit destructive confirmation.

- `n` → end. PRD not saved.
- `edit-slug` → ask for slug, then `y` (re-check existence after slug change).
- `y` → proceed with save below.
- `overwrite` → existing file is replaced without backup (user has explicitly confirmed destructive write).
- `new-slug` → ask for a different slug, then re-check existence; repeat until a free slug is chosen or user picks `n`/`overwrite`.

Save PRD (only after `y` or `overwrite`):
```bash
mkdir -p docs/
# Write PRD content to docs/prd-{slug}.md
```

PRD section structure:
| Section | Content |
|------|------|
| §1 | Planning summary |
| §2 | Flag design ← **omitted when flag is not needed; numbering of §3+ unchanged** |
| §3 | Technical design (affected files) |
| §4 | Implementation spec |
| §5 | Edge cases |
| §6 | Test criteria |
| §7 | Guardrails |
| §8 | Asset references |

Asset recording:
```bash
HARNISH_ROOT="${CLAUDE_PLUGIN_ROOT}"
if [[ -n "$HARNISH_ROOT" ]]; then
  bash "$HARNISH_ROOT/scripts/record-asset.sh" \
    --type pattern --tags "{keywords}" \
    --title "{feature name} implementation pattern" --content "{summary}" \
    --base-dir "$(pwd)/.harnish"
fi
```

## Step 8: Completion

```
✅ PRD generated: docs/prd-{slug}.md
Includes: §4 Implementation spec / §6 Test criteria / §7 Guardrails
Next: "start implementation" after review, or /galmuri:ralphi for consistency check.
```

## Distinction from drafti-architect

| User Request | Judgment | Skill |
|-----------|------|------|
| "Create PRD based on this planning doc" | Planning document exists | → drafti-feature |
| "How should I design this problem" | No planning doc | → drafti-architect |

## Context Budget

| When | Reads |
|---|---|
| Step 1 (Parsing) | Planning document, project config files (`package.json`, `pyproject.toml`, etc.) |
| Step 2 (Asset query) | `.harnish/assets/*.jsonl` filtered by tags. Skip if `.harnish/` absent. |
| Step 3 (Codebase) | Keyword-matched files only. No full project tree read. |
| Step 4 (Flag) | `references/feature-flag-patterns.md` (only if flag needed) |
| Step 5 (Spec) | `references/prd-template.md` |
| Step 6 (Tests) | None |
| Step 7 (Save + record) | None (writes only — `docs/prd-*.md` and `.harnish/assets/*.jsonl`) |

Load **at most 1** reference at a time; switch when moving phase.

## Prohibited

- Guessing requirements without a planning doc (use drafti-architect instead)
- Forcing unnecessary feature flags (follow the Step 4 assessment table)
- Saving PRD without explicit user confirmation in Step 7
- Saving over an existing `docs/prd-*.md` without explicit `overwrite` confirmation
- Proceeding past Step 1 with any of the 4 required items missing
- Loading 2 references simultaneously
