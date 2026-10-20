---
description: Level 2 — Full Mode C pipeline for standard features (3-50 TCs)
agent: lead
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the Lead QA Architect. Execute the **full Mode C pipeline** for standard features.

## Prerequisites

- [ ] Triage completed: `/triage` run first, level = standard
- [ ] User approved: received "Lanjutkan" after implementation plan review

## Pipeline Phases

### Phase 1: Parallel Research

**Research before planning.** Learn codebase before writing plan.

Dispatch 4 researchers CONCURRENTLY in a single message with 4 separate `task()` calls (all 4 in one message). They run in parallel — wall-time = single longest call. Each call is independent (different domain, different output file, different TC ownership) — no race conditions.

| Letter | Agent                   | Domain                          | Output File                                           |
| ------ | ----------------------- | ------------------------------- | ----------------------------------------------------- |
| **A**  | researcher-routes       | Routes, navigation, guards      | `researcher-routes-{YYYYMMDDHHMMSS}-{seq}.json`       |
| **B**  | researcher-components   | Selectors, UI elements, testids | `researcher-components-{YYYYMMDDHHMMSS}-{seq}.json`   |
| **C**  | researcher-validators   | Validation rules, error states  | `researcher-validators-{YYYYMMDDHHMMSS}-{seq}.json`   |
| **D**  | researcher-pom-patterns | Existing POM patterns, BasePage | `researcher-pom-patterns-{YYYYMMDDHHMMSS}-{seq}.json` |

### Phase 2: Planning (After Research Complete)

1. Read `docs/workflows/002-multi-agent-orchestration.md` — Mode C SOP
2. Read `docs/workflows/000-triage.md` — confirm Level 2 routing
3. Read user story / PRD / AC
4. **Merge:** glob `.agent/tasks/researcher-*.json`
5. Write `.agent/plans/implementation-plan-{feature}.md` using template (based on research)
6. Create per-TC todo files `.agent/plans/todos/tc-*.md` with ownership assigned

### Phase 3: Human Gate (MANDATORY HALT)

```text
⏳ *Implementation Plan dan Todos berhasil dibuat. Silakan tinjau file tersebut.
Apakah ada yang perlu disesuaikan, atau ketik 'Lanjutkan' untuk mengeksekusi script testing?*
```

**Do NOT proceed to Phase 4 until user approves.**

### Phase 4: Implementation (SEQUENTIAL — POM first, then Spec)

1. **Builder-POM** → `src/tests/pages/**`, `src/tests/components/**` (dispatch first, wait for completion)
2. **Builder-Spec** → `src/tests/specs/**`, `src/tests/data/**` (dispatch after POM files exist)

⚠️ **Race condition:** Builder-Spec reads POM files from Builder-POM. Do NOT dispatch both at once.

### Phase 5: Verification + Reflection (SEQUENTIAL sub-phases)

Dispatch 3 agents ONE AT A TIME in this order:

1. **REFLECTOR-POM** → critiques POM structure (wait for verdict)
2. **REFLECTOR-SPEC** → critiques spec quality (wait for verdict)
3. **QA-GATEKEEPER** → runs `.agent/hooks/test.sh test --grep "{feature}" --reporter=list`

4. Reflector-POM first → if revise → Builder-POM fixes → re-dispatch
5. Reflector-Spec after POM pass → if revise → Builder-Spec fixes → re-dispatch
6. QA-Gatekeeper after both pass
7. Max 3 full cycles before BLOCK

### Phase 6: Teardown

1. Finalize summary with actual test counts
2. Write `.agent/state.json` ONCE
3. Write `.agent/memory/entities/relations.json`
4. Ask user: keep or delete `implementation-plan-{feature}.md`

## Rules

- Each researcher writes to its **own TC files only**
- Builders run SEQUENTIALLY: POM first, Spec second (Spec reads POM files)
- Memory writes: builders append, reflector annotates, Lead persists relations
- Never overwrite another's in-progress [/] row
