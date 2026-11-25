---
name: orchestration-kernel
description: "Define and keep the shared orchestration contracts aligned across project-researcher, project-orchestrator, and project-hardener: role-based model resolution, scope-lock ownership, evidence bundles, drift detectors, and hard-stop reporting. Use when creating or updating any of those spine contracts and their handoff/escalation edges."
---

# Orchestration Kernel

This skill is the shared contract for the three orchestration spines:

- `project-researcher` (pre-spec)
- `project-orchestrator` (spec + build)
- `project-hardener` (post-build convergence)

It is **not a direct execution skill**. Treat it as the canonical contract these
three skills reference and stay aligned to.

## When to Use

- You are adding or editing contract language in any spine skill.
- You are wiring handoff/escalation edges across the three spines.
- You need one source of truth for model-role resolution, scope-lock, drift
  detection, evidence shape, or hard-stop format.

## When NOT to Use

- You are executing an actual project phase. Use one of the spine skills.
- You are debugging product code directly.

## Shared Contract

### 1) Role-Based Model Resolution

All spines must name roles, never hardcoded model slugs.

| Role | Selection criteria | Typical responsibilities |
|---|---|---|
| planner | strongest available reasoning model with high thinking budget | strategy, decomposition, synthesis |
| builder | strongest available coding model at balanced speed/cost | implementation changes |
| mechanical | fastest low-cost model with stable tool execution | scaffolding, formatting, inventory updates |
| critic/auditor | capable model from a different family than builder | independent challenge and review |

Resolution order:
1. Use explicit project override file when present.
2. Otherwise resolve best-available-at-runtime by role criteria.
3. Show resolved mapping at the relevant human gate and freeze for that run.

Concrete model slugs may appear only in run-specific artifacts (approved specs,
override JSON), never in `SKILL.md` prose.

### 2) Scope-Lock Contract

Scope enforcement is mandatory for any phase or loop candidate that writes files.

- Canonical owner: `project-orchestrator/scripts/scope-check.sh`
- Inputs: `owns` globs, `forbidden` globs, changed file list
- Outcome:
  - out-of-owns edits fail
  - forbidden edits fail
  - only in-scope changes pass

Other skills should reference the canonical checker, not fork a second variant.

### 3) Evidence-Bundle Shape

Use this structure for project-level orchestration evidence:

```text
.orchestrator/<slug>/
├── SPEC.md
├── RESEARCH.md                 # optional, when researcher ran
├── Pk/                         # one directory per phase when applicable
│   ├── patch.diff
│   ├── NOTES.md
│   ├── commands.log
│   └── BLOCKER.md              # only if halted
├── integration/
│   ├── verify.log
│   └── success-criteria.md
└── REPORT.md
```

If escalation occurs from hardener, include the escalation payload in the
relevant phase or integration evidence directory.

### 4) Drift Detectors

All spines share these drift detector concepts:

- **scope drift**: edits outside declared ownership
- **plan drift**: implementation diverges from approved contract without update
- **evidence drift**: completion claim lacks passing command evidence

### 5) Hard-Stop Format

All hard stops halt execution and emit concrete evidence. Use this normalized
shape (or a strict superset):

```yaml
stop_reason: <machine-readable code>
phase_or_loop: <id>
attempt: <n>
failed_checks:
  - command: <exact command>
    exit_code: <code>
evidence_paths:
  - <path>
next_action: <explicit re-entry or escalation step>
```

### 6) Closed-Loop Edge Contract

The pipeline is closed, not linear:

1. `project-researcher` produces `RESEARCH.md` for orchestrator Stage 1 input.
2. `project-orchestrator` hands integration branch and evidence to
   `project-hardener`.
3. `project-hardener` escalates out-of-spec findings back to:
   - `project-orchestrator` for re-spec
   - `project-researcher` for re-research

## Additional Resources

- Full resolution and gate details: [reference.md](reference.md)
- Build spine: [project-orchestrator](../project-orchestrator/SKILL.md)
- Research spine: [project-researcher](../project-researcher/SKILL.md)
- Hardening spine: [project-hardener](../project-hardener/SKILL.md)
