---
name: orchestrator-log
description: "Session audit trail: log orchestrator decisions (tier, skips, topology, critic verdict, outcome) and subagent results (verdict, findings, evidence). Control Tower writes inline — not a separate stage. Triggers: after Stage 0 Preflight, after each subagent return, after Stage 3 closeout."
user-invocable: true
allowed-tools:
  - Read
  - Bash(cat *)
  - Bash(grep *)
  - Bash(date *)
---

# Skill: Orchestrator Log

## Purpose

Maintain an audit trail of Control Tower decisions and subagent results across
a session. Answers the question "why did the orchestrator make this choice?"
without requiring access to the original conversation transcript.

Two log files:
- `memory-bank/orchestrator-log.md` — Control Tower decisions (why)
- `memory-bank/review-log.md` — subagent results (what they found)

This applies to Codex and Claude Code runtimes. In the Codex layer, log
Stage 0.5 Codex critic mode (`READY`, `FALLBACK`, or `SKIPPED`) so the Owner
can see whether the Orchestrator was independently checked or used an explicit
fallback.

Related delegated-team log:
- `memory-bank/external-team-log.md` — external agent team execution trace
  for Claude Code handoff sessions (how the contractor team worked)

## When to Use (Triggers)

### Write to orchestrator-log

Control Tower writes to `memory-bank/orchestrator-log.md`:

- **After Stage 0 Preflight** — log tier selection, each skipped skill + reason, subagent topology
- **After Stage 0.5 Critic Review** — log critic mode, verdict, and action taken
- **After critic skip** — log valid skip condition or explicit Owner approval
- **On scope change** — log what changed + why + re-approval status
- **On Hard Stop trigger** — log which Hard Stop + Owner decision
- **After Stage 3 Closeout** — log final outcome (READY/BLOCKED/ESCALATED),
  residual risks, critic value, and any framework update produced by the
  retrospective

### Write to review-log

Control Tower writes to `memory-bank/review-log.md`:

- **After each subagent returns** — log agent, verdict, key findings, evidence summary
- **After same-session fallback critic** — log `codex-critic` with
  `FALLBACK` evidence so it is not mistaken for an independent subagent

### Read external-team-log

External Claude Code handoff sessions may write
`memory-bank/external-team-log.md` when the task contract explicitly requires
it. Control Tower reads that log during closeout and consolidates only the
verdict/findings into `review-log.md`.

## When to Skip

- Trivial fixes (single-file, no logic change) — no decision trail needed
- Routine documentation-only Work Blocks with no workflow, contract, release,
  safety, or governance impact — nothing to audit
- `orchestrator-log.md` and `review-log.md` are write-only for Control Tower;
  external Claude Code teams write only `external-team-log.md` when delegated
  through a handoff contract

## Workflow

### For orchestrator-log

1. After Stage 0 Preflight: add row with tier selection + skill skips + topology
2. After critic returns or fallback completes: update row with critic mode/verdict
3. On scope change or Hard Stop: add row immediately
4. After merge protocol (if parallel agents used): add row with consolidation decision
5. After Stage 3 Closeout: add row with final outcome, critic value, residual
   risks, and any follow-up framework update

### For review-log

1. Subagent returns with report
2. Control Tower reads report
3. Extract: agent name, verdict, 1-line key finding, evidence summary
4. Add row to review-log
5. If merge protocol runs: note consolidation report path in evidence column

## Format

### orchestrator-log.md

```markdown
| Date | Work Block | Decision | Rationale | Subagents Used | Critic Verdict | Outcome |
|---|---|---|---|---|---|---|
| 2026-06-12 | wb-001 | Standard tier | No auth/DB/payment touched | verifier | APPROVE | READY |
```

### review-log.md

```markdown
| Date | Work Block | Agent | Verdict | Key Findings | Evidence |
|---|---|---|---|---|---|
| 2026-06-12 | wb-001 | verifier | READY | Types pass, build OK | tsc --noEmit clean |
```

## Constraints

- **Never log secrets, tokens, or credentials.**
- Do not duplicate — check existing rows before adding.
- One row per decision, one row per subagent return.
- The log is an audit trail, not a task tracker. Task status goes to `progress.md`.
- Control Tower writes inline — no separate stage, subagent, or plan required.
- Keep entries under one line — details go to `docs/reports/`.

## Relationship with Other Files

| File | Purpose | This skill |
|---|---|---|
| `progress.md` | WHAT was done | Does NOT touch |
| `orchestrator-log.md` | WHY decisions were made | WRITES |
| `review-log.md` | WHAT subagents found | WRITES |
| `external-team-log.md` | HOW external teams worked | READS |
| `decisions.md` | Architecture decisions | Does NOT touch |
| `docs/reports/` | Full subagent reports | References |

## Handoff

- **Success condition**: log row added, no secrets leaked, no duplicates
- **Next**: continue with current stage — logging is inline, not blocking
- **Auto-proceed**: YES — logging never blocks the pipeline
- **Hard stop**: NO
