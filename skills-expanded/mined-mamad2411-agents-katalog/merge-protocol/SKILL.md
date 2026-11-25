---
name: merge-protocol
description: "Collect, deduplicate, and resolve conflicts across parallel subagent results. Produces a consolidation report for Control Tower before SSOT sync. Triggers: 2+ subagents completed in one Work Block, Workflow tool finished all parallel tasks, or before Stage closeout when parallel agents were used. Auto-proceed if no conflicts; hard stop on unresolvable conflict."
user-invocable: true
argument-hint: "[work-block-id] [stage]"
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(rg *)
  - Bash(jq *)
---

# Skill: Merge Protocol

## Purpose

After parallel subagents complete, their results must be collected, deduplicated,
and reconciled before Control Tower can proceed to SSOT sync. The merge protocol
produces a single consolidation report from N independent subagent outputs.

## Position in SDLC

```
Parallel Dispatch
  └─→ [all agents completed]
        └─→ Merge Protocol (consolidation report) ← YOU ARE HERE
              └─→ SSOT Sync Closeout
                    └─→ Stage transition
```

## When to Use (Triggers)

Control Tower MUST run merge protocol when:

- **2+ subagents completed** in the same Work Block (parallel dispatch)
- **Workflow tool finished** all parallel/pipeline tasks
- **Before Stage closeout** when parallel subagents were used

Skip when:
- Single subagent (no merge needed — use subagent output directly)
- Sequential execution with no parallel branches
- Trivial Work Block with one agent

## Conflict Resolution Rules

Priority order for resolving verdict conflicts on the same file/artifact:

| Agent A | Agent B | Result | Rationale |
|---|---|---|---|
| PASS | ISSUES | **ISSUES wins** | Conservative — don't silence findings |
| PASS | BLOCKED | **BLOCKED wins** | BLOCKED is the strongest signal |
| ISSUES | BLOCKED | **BLOCKED wins** | Verifier authority overrides reviewer |
| ISSUES (type A) | ISSUES (type B) | **Both included** | Different findings are complementary |
| ISSUES (same) | ISSUES (same) | **One entry, both credited** | Same finding — deduplicate |

**Unresolvable conflicts:**
- Two agents produce contradictory evidence on the same file (e.g., verifier says PASS with evidence, reviewer says ISSUES with contradicting evidence)
- Control Tower cannot determine which is correct from the reports alone
- → **ESCALATE to Control Tower with both reports quoted.** Hard stop until resolution.

## Workflow

### Step 1 — Collect Results
- Read all subagent reports from `docs/reports/` or direct subagent outputs
- Read review-log.md for subagent verdicts
- Verify all expected agents completed — flag incomplete/failed agents

### Step 2 — Deduplicate Findings
- Group findings by `file:line` key
- Same finding from multiple agents → one merged entry, all discoverers credited
- Different findings on same file but different lines → separate entries

### Step 3 — Detect Conflicts
- Group findings by `file` (same file, different verdicts)
- Apply conflict resolution rules (see above)
- Unresolvable → escalate immediately, do not proceed

### Step 4 — Classify
- **Must fix (P0):** BLOCKED verdicts, HIGH severity security findings
- **Should fix (P1):** MEDIUM severity, maintainability issues
- **Might fix (P2):** LOW severity, style nits
- **Accepted:** findings Control Tower consciously accepts with rationale

### Step 5 — Produce Consolidation Report
- Fill in `docs/templates/consolidation-report-template.md`
- Save to `docs/reports/consolidation-[wb-id]-[stage]-[date].md`

### Step 6 — Update Logs
- `orchestrator-log.md`: add consolidation decision row
- `review-log.md`: add rows for any subagents not yet logged
- `progress.md`: no update yet — that's SSOT Sync Closeout's job

## Output

Consolidation report saved to `docs/reports/consolidation-[wb-id]-[stage]-[date].md`

Key sections:
1. Subagent results table (all agents, verdicts, findings)
2. Merged findings (deduplicated, with severity and discoverers)
3. Conflicts (if any — with resolution or escalation)
4. Accepted risks
5. Incomplete/failed agents
6. Follow-ups for backlog
7. Control Tower decision (PROCEED / ESCALATE / RERUN)

## Constraints

- **Auto-proceed** if no conflicts and no BLOCKED verdicts
- **Hard stop** on unresolvable conflict — escalate to Control Tower, await decision
- **Hard stop** on BLOCKED verdict — cannot proceed to closeout
- **Never discard findings** — even if accepted, document them
- **Traceability** — every merged finding references its source agent(s)
- Consolidation report is part of audit trail, never deleted

## Relationship with Other Skills

| Skill | Relationship |
|---|---|
| `context-snapshot` | Merge protocol references the pre-dispatch snapshot for baseline comparison |
| `ssot-sync-closeout` | Merge protocol runs BEFORE ssot-sync — provides cleaned input |
| `orchestrator-log` | Merge outcome is logged to orchestrator-log.md |
| `review-log` | Subagent results are logged to review-log.md during merge |
| `critic-review` | Critic may re-evaluate consolidation quality for complex merges |

## Anti-Patterns

- **Silent dedup:** merging two different findings because they "look similar" → Always check file:line. Different lines = different findings.
- **Rubber-stamp consolidation:** "all agents passed, nothing to see" → Check each report. Silent failures exist.
- **Merge without snapshot:** consolidating without the pre-dispatch snapshot → Cannot verify if agents saw the same state.
- **Deferring all conflicts:** "escalate everything" → Only escalate genuinely unresolvable conflicts. Control Tower can resolve most.

## Handoff

- **Success condition:** consolidation report written, all findings deduplicated, conflicts resolved or escalated, logs updated
- **Next:** SSOT Sync Closeout (if PROCEED) or corrective Work Block (if RERUN)
- **Auto-proceed:** YES — if no conflicts and no BLOCKED verdicts
- **Hard stop:** YES — on unresolvable conflict or BLOCKED verdict from verifier
