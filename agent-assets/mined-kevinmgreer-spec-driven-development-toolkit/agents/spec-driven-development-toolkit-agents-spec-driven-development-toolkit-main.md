# Spec-Driven ATDD Toolkit

This project uses **spec-first Acceptance Test-Driven Development (ATDD)**.

> **Golden Rule:** Never write production code unless a failing acceptance test requires it.

Language-agnostic, platform-agnostic. Works in any project — greenfield or legacy. Follows
the [AGENTS.md](https://agents.md/) standard and is read by Copilot, Claude, and
any AGENTS.md-aware tool.

---

## First Action of Any Feature Work (Profile Bootstrap)

Before writing a spec, tests, code, or running quality gates — including ad-hoc requests like
"fix this bug" — **check whether `docs/project-profile.md` exists**.

- **Missing**: your first action is to create it (run Phase 0 — see
  `docs/atdd/workflow.md` § Phase 0 and `docs/atdd/project-detection.md`). Tell the user:
  _"No project profile found — running Phase 0 first so I have an accurate picture of this
  codebase's tooling and conventions."_
- **Exists**: read it first; treat as authoritative.
- **Never** detect tools/conventions on the fly without persisting the profile to disk. Silent
  fallback is why conventions drift between sessions.

---

## The Cycle

```
Analyze → Spec → Tests (Red) → Implementation (Green) → Quality Gates → Refactor →
Spec & Doc Sync → Archive → PR → Review
```

Never skip or reorder. **Full procedure for every phase is in
[`docs/atdd/workflow.md`](docs/atdd/workflow.md)** — read that file before executing a phase
unless you have it in recent context.

---

## Hard Rules

- Never write production code before acceptance tests exist and fail (red for the right reason)
- Never modify tests to make them pass — fix the implementation
- Never narrow the spec without confirmation — classify every Phase 6b repair
  ADDED / MODIFIED / REMOVED; a REMOVED needs sign-off, not "match the code"
- Never add logic not demanded by a failing test
- Always update the spec first when requirements change, then tests, then code
- Always re-read `docs/project-profile.md` before Phase 3 and mirror its conventions
- Always read existing project docs (README, CONTRIBUTING, ARCHITECTURE, ADRs) during Phase 0
  — they override inference
- Never proceed past Phase 1 without explicit user approval of the spec — and ask for the
  autonomy level at that same gate, never as a separate question before it
- Never declare done while spec, README, `docs/project-profile.md`, or any doc listed under
  `Sources consulted` in the profile has drift — walk the full list in Phase 6c before
  committing (Phase 6 is a blocking gate, not a recommendation)

---

## Spec Directory

```
specs/
├── capabilities/   # Source of truth — what the system does today
│   └── <domain>/   #   behavior.feature (no delta tags) + rules.md
└── changes/        # Work in flight — one folder per change
    ├── <name>/     #   proposal.md, delta.feature, delta-rules.md, tasks.md
    └── archive/    #   merged changes, date-prefixed
```

Tag convention: `@smoke` exactly 1 per **capability** (enforced at archive). `@happy-path` (1–2),
`@edge-case` (2–4), `@error` (2–3) describe **one delta** — a capability's counts grow with every
change and are not capped.

---

## Spec Change Protocol

Spec → tests → code → docs — in that order. Never update implementation to accommodate new
behavior without updating the spec first. All docs listed under `Sources consulted` in
`docs/project-profile.md` (README, CONTRIBUTING, ARCHITECTURE, ADRs, style guides, etc.) must
be reviewed and updated as part of the change, not as a follow-up. Full protocol in
[`docs/atdd/workflow.md`](docs/atdd/workflow.md) § Spec Change Protocol.

---

## Quick Command Reference

| Command                    | Purpose                                                        |
| -------------------------- | -------------------------------------------------------------- |
| `/analyze-project`         | Detect tooling + conventions; write `docs/project-profile.md`  |
| `/write-spec`              | Generate a change folder: proposal, delta, rules, tasks        |
| `/write-acceptance-tests`  | Generate failing test stubs from a spec                        |
| `/implement-from-spec`     | Implement code to make failing tests pass                      |
| `/run-quality-gates`       | Run lint, format, typecheck, build, test — iterate until green |
| `/refactor-passing-tests`  | Safe refactor with all tests green                             |
| `/verify-spec-coverage`    | Hard spec & doc sync gate — repairs spec/README/profile drift  |
| `/archive-change`          | Merge the delta into its capability; archive the change        |
| `/create-pull-request`     | Create branch, commit, push, open PR                           |
| `/address-review-comments` | Handle PR review feedback                                      |
| `@atdd-cycle`              | The full cycle: requirements → PR → review. Start here         |
| `@spec-writer`             | Dedicated spec writing subagent                                |
| `@spec-reviewer`           | Read-only spec & doc compliance review                         |

---

## Reference Documentation

Canonical sources — read on demand, not upfront:

| File                                        | Contents                                    |
| ------------------------------------------- | ------------------------------------------- |
| `docs/atdd/workflow.md`                     | Full ATDD cycle procedure (authoritative)   |
| `docs/atdd/project-detection.md`            | Phase 0 — tooling and conventions detection |
| `docs/atdd/quality-gates.md`                | Quality gate definitions and execution      |
| `docs/atdd/legacy-integration.md`           | Integrating into existing projects          |
| `docs/atdd/spec-writing.md`                 | How to write clear, testable specifications |
| `docs/atdd/gherkin.md`                      | Gherkin syntax and anti-patterns            |
| `docs/atdd/checklist.md`                    | Per-feature progress checklist              |
| `docs/atdd/templates/`                      | Capability, delta, proposal, rules, tasks templates |
