---
name: eng-plan
description: Transform a feature request, user story, or frozen specification (specs/) into a comprehensive, context-rich, one-pass implementation plan. Use when planning new features, major refactorings, or preparing step-by-step tasks before coding.
---

# Plan Feature

Transform a feature request or frozen specification into a **comprehensive implementation plan** through systematic codebase analysis, context gathering, and dependency-ordered task breakdown.

## Core Rules & Guardrails

- **Zero-Code Phase**: Do NOT write or modify application source code during this phase. Only create the plan document.
- **Spec-First Ingestion**: If `specs/<feature-name>/` exists, treat `requirements.md` and `design.md` as the frozen single source of truth. Derive tasks and acceptance criteria directly from the spec's AC identifiers without re-inventing requirements.
- **Anti-Hallucination & Reality Check**:
  - Every referenced file, symbol, or pattern MUST exist in the codebase and be confirmed with tools (`grep`, `glob`, `read`).
  - Validation commands MUST match actual project tooling (e.g. detect `package.json`, `Cargo.toml`, `pytest.ini`).
  - Never invent URLs or unverified file paths in the delivered plan ,  cite only tool-confirmed artifacts.
- **No Full Code Dumps in Tasks**: Provide interface signatures, key logic outlines, and pattern references, NOT 100-line code blocks.

---

## 5-Phase Planning Workflow

```
[Phase 1: Spec / Scope Ingestion & Ambiguity Gate] ➔ [Phase 2: Codebase Intelligence] ➔ [Phase 3: Architecture & Contract Alignment] ➔ [Phase 4: Task Breakdown] ➔ [Phase 5: Plan Output & Verification Gate]
```

### Phase 1: Scope & Ambiguity Gate
1. **Check for Spec**: Inspect `specs/<feature-name>/`. If frozen, ingest `requirements.md` (ACs, scope) and `design.md` (contracts).
2. If no spec exists, extract user intent, determine category (`New Capability` | `Enhancement` | `Refactor` | `Bug Fix`), and assess complexity.
3. **Ambiguity Gate**: If requirements, core technical stack, or breaking changes are ambiguous (and no frozen spec exists), **stop and ask the user** (or suggest running `eng-spec`) before proceeding.

### Phase 2: Codebase Intelligence Gathering
1. **Locate Integrations**: Identify existing files that need modifications and new files to create.
2. **Extract Conventions**: Identify existing project patterns for naming, error handling, logging, and database access.
3. **Verify Build & Test Commands**: Discover exact test, lint, and build commands from project configs.
4. **Identify Gotchas**: Note deprecations, concurrency constraints, or edge cases.

### Phase 3: Architecture & Contract Alignment
1. Align component boundaries and API interfaces with codebase conventions (or frozen `design.md`).
2. Document architectural trade-offs and rationale.
3. Ensure backward compatibility and error recovery strategies.

### Phase 4: Atomic Task Breakdown
Break the work down into atomic, dependency-ordered tasks using the standardized format:
- **ACTION**: `CREATE` | `UPDATE` | `REMOVE` | `MIRROR`
- **TARGET**: relative file path
- **OBJECTIVE**: concise change description (mapped to AC when spec exists)
- **PATTERN REFERENCE**: existing file and line reference as blueprint
- **VALIDATION**: executable non-interactive command

### Phase 5: Output & Verification Gate
Generate the final plan file at `.agents/plans/<kebab-case-feature-name>.md` following the template below.

---

## Output Plan Template

```markdown
# Feature Plan: <feature-name>

## 1. Overview & Context
- **Problem Statement**: <what problem is being solved>
- **Proposed Solution**: <how the solution addresses the problem>
- **Spec Reference**: `specs/<feature-name>/` (or N/A)
- **Feature Type**: New Capability | Enhancement | Refactor | Bug Fix
- **Estimated Complexity**: Low | Medium | High

## 2. Context References & Existing Patterns
- `path/to/existing_file.ext` (lines X-Y) - Pattern to mirror
- `path/to/config.ext` - Integration target

## 3. Implementation Steps (Dependency-Ordered)

### Task 1: [ACTION] path/to/file.ext
- **OBJECTIVE**: <Goal of this task, mapped to AC-X if spec present>
- **PATTERN**: `<file:line_reference>`
- **KEY CHANGES**: <Specific function/type changes without dumping entire files>
- **GOTCHAS**: <Known constraints to avoid>
- **VALIDATE**: `<non-interactive CLI verification command>`

### Task 2: [ACTION] path/to/next_file.ext
...

## 4. Testing & Validation Matrix
- **Syntax / Lint**: `<command>`
- **Unit Tests**: `<command>`
- **Integration Tests**: `<command>`
- **Manual Verification Checklist**:
  - [ ] Verification step 1
  - [ ] Verification step 2

## 5. Acceptance Criteria
- [ ] AC-1: <from spec or requirements>
- [ ] AC-2: <from spec or requirements>
- [ ] All automated tests pass with zero regressions
- [ ] Conforms to existing codebase style and patterns
```

---

## Plan Quality Checklist (Pre-Flight Gate)

Before delivering the plan, ensure:
- [ ] If `specs/<feature-name>/` exists, all tasks map to frozen acceptance criteria.
- [ ] All referenced files and line numbers have been verified in the actual codebase.
- [ ] Tasks are strictly ordered by dependency (can be implemented top-to-bottom).
- [ ] Every task includes a working, executable validation command.
- [ ] Plan output path is `.agents/plans/<feature-name>.md`.

---

## Checkable Completion Criteria

- [ ] Plan file generated at `.agents/plans/<feature-name>.md` following the output template.
- [ ] Every task carries ACTION, TARGET, OBJECTIVE, PATTERN REFERENCE, and an executable VALIDATION command.
- [ ] All referenced files, symbols, and line numbers verified against the real codebase with tools.
- [ ] Tasks strictly dependency-ordered and mapped to spec acceptance criteria when a frozen spec exists.
