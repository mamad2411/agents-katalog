---
name: explore
description: Use when a task modifies or references existing code — refactors, legacy rework, reusing a pattern, or when the prompt names specific methods/classes/tables. Harvests repo facts and verifies the user's technical claims before any design or code, so grill only asks judgment calls.
---

# Explore

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

Turn a task's code references into a **fact checklist** the main agent can act on without re-reading the repo.

**Core principle: the repo owns facts; the user owns decisions. Read everything the task names; verify everything the user asserts; deliver a checklist, not an opinion.**

## Who reads

The main agent dispatches a background **explore subagent** and tells it to load this skill. The subagent is read-only: no design, no questions to the user, no code. If you are that subagent, this skill is your entire task — follow it exactly.

## When to Use

- Task names code to change or reference: "refactor X", "model after Y", "reuse Z's pattern"
- The prompt contains technical assertions to verify (signatures, fields, SQL, types, "try not to update" style constraints)
- Refactor / legacy rework / reuse, where guessing the code shape would waste grill questions

**When NOT to use:** brand-new code with no anchors; bugfix with known root cause (debug); mechanical rename.

## Trigger threshold (anchors trigger, width decides dispatch)

- **Trigger:** any task that names existing code — a method/class to change, a table/SQL, or a "reuse / model-after" pointer — gets an explore pass. No threshold below that.
- **Dispatch width:** one anchor, obvious chain (≤ 1 method + 1 table) → the main agent reads inline. Wide chain (multiple tables + referenced classes + data consumers) → dispatch a background subagent.
- The threshold is a rule, not a judgment call — decide by counting anchors, then dispatch.

## The Iron Law (non-negotiable)

```
READ EVERYTHING THE TASK NAMES. VERIFY EVERYTHING THE USER ASSERTS.
Deliver facts only. If the repo can't answer it, it's a blocker — never guess.
```

## Workflow

1. **Parse anchors** — every named method/class/table/config/SQL + every "reuse / model-after" pointer.
2. **Read the full chain** — target method → referenced classes → Mappers/entities/XML → the data's consumers (e.g., existing Redis retry consumers) → relevant config. Read implementations, not just signatures, when behavior matters.
3. **Verify assertions** — each technical claim in the prompt → ✓ consistent / ✗ contradicts, with file:line evidence.
4. **Map conflicts** — constraint vs repo reality (e.g., "try not to update" vs no status field → re-run duplicates).
5. **Deliver the fact checklist** — the format below, nothing else. Compact: it lives in session history, grill consumes it directly, and write-spec folds it into the Current state section.

## Deliverable: Fact Checklist

```
### 1. Anchors
- <method>: exists ✓ — current behavior: <2 lines>
- <referenced class>: <signature/usage, 2 lines>
- <table> → Entity X; fields: <relevant fields>

### 2. Assertion check
- "<user's claim>": ✗ actual <thing> returns <X> (file:line)

### 3. Conflicts
- "<soft constraint>" ↔ <repo reality> → <consequence> → grill Q<#>

### 4. Judgment calls for grill  (one line each: question + why the repo can't answer)
- <idempotency / redis fallback / acceptance …>

### 5. Blockers
- <not found in repo; main agent decides whether to ask the user>
```

Rules: no design opinions (grill's job); no user-directed questions; missing anchor = blocker.

## Small-task fallback (main agent)

One anchor, obvious chain → read inline. Dispatch the subagent when the chain is wide (multiple tables + referenced classes + consumers).

## Rationalization Table

| Excuse | Reality |
|---|---|
| "I know what <referenced class> does" | You know what you assume. Read it. |
| "I'll ask the user if this field exists" | Facts → explore. Decisions → ask. Blockers only for what the repo truly lacks. |
| "I'll add a design note here" | Facts and opinions mix → grill trusts the wrong thing. |
| "This task is small, skip exploring" | The trigger threshold is a rule — anchors present = explore. Inline reading still costs almost nothing. |

## Red Flags

- Checklist contains recommendations or "should we…?" questions (that's grill's output channel)
- Assertion check empty despite claims in the prompt
- Anchor listed but not read (no evidence lines)
- User asked a question; subagent answered — subagents deliver facts, never decisions

## Checklist

- [ ] All anchors read (target + references + tables + consumers)
- [ ] Every user assertion marked ✓/✗ with evidence
- [ ] Conflicts surfaced (constraint vs repo fact)
- [ ] Judgment calls framed for grill to ask one at a time
- [ ] No opinions, no user questions, no code
