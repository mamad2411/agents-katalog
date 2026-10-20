# Spec-Driven ATDD

Language-agnostic, platform-agnostic spec-first ATDD toolkit.

> **Golden Rule:** Never write production code unless a failing acceptance test requires it.

## First Action of Any Feature Work (Profile Bootstrap)

Before writing a spec, tests, code, or running quality gates — including ad-hoc requests like
"fix this bug" — **check whether `docs/project-profile.md` exists**.

- **Missing**: first action is `/analyze-project` (or Phase 0 of `@atdd-cycle`). Tell the user:
  _"No project profile found — running Phase 0 first so I have an accurate picture of this
  codebase's tooling and conventions."_
- **Exists**: read it first; treat as authoritative.
- **Never** detect on the fly without persisting the profile to disk.

## Directory Structure

```
specs/
├── capabilities/   # Source of truth — what the system does today
│   └── <domain>/   #   behavior.feature (no delta tags) + rules.md
└── changes/        # Work in flight — one folder per change
    ├── <name>/     #   proposal.md, delta.feature, delta-rules.md, tasks.md
    └── archive/    #   merged changes, date-prefixed
```

## The ATDD Cycle

```
Analyze → Spec → Tests (Red) → Implement (Green) → Quality Gates → Refactor →
Spec & Doc Sync → Archive → PR → Review
```

Full procedure: **[`docs/atdd/workflow.md`](../docs/atdd/workflow.md)** (read on demand).

## Hard Rules

- Red before green; never modify tests to make them pass
- Never add logic not demanded by a failing test
- Update spec first when requirements change, then tests, then code
- Phase 1 requires explicit user approval before tests are generated
- Phase 3 re-reads `docs/project-profile.md` and mirrors its conventions — no inventing
- Phase 0 reads existing docs (README, CONTRIBUTING, ARCHITECTURE, ADRs) before drawing
  conclusions — they override inference
- Phase 6 (Spec & Doc Sync) is a **blocking** gate that repairs drift in-phase —
  includes `README.md` and `docs/project-profile.md` updates
- Phase 6b classifies every repair ADDED / MODIFIED / REMOVED; a REMOVED narrows the spec and
  needs sign-off, not "match the code"

## Commands & Agents

| Trigger                    | Purpose                                                          |
| -------------------------- | ---------------------------------------------------------------- |
| `@atdd-cycle`              | The full cycle: requirements → PR → review. Start here            |
| `@spec-writer`             | Write Gherkin + technical spec                                   |
| `@spec-reviewer`           | Read-only spec & doc compliance review                           |
| `/analyze-project`         | Detect tooling + conventions; write `docs/project-profile.md`    |
| `/write-spec`              | Generate spec from requirements                                  |
| `/write-acceptance-tests`  | Generate failing test stubs from a spec                          |
| `/implement-from-spec`     | Implement code to make failing tests pass                        |
| `/run-quality-gates`       | Run lint/format/typecheck/build/test until green                 |
| `/refactor-passing-tests`  | Safe refactor after green                                        |
| `/verify-spec-coverage`    | Hard spec & doc sync gate (repairs drift in-place)               |
| `/archive-change`          | Merge the delta into its capability; archive the change         |
| `/create-pull-request`     | Create branch, commit, push, open PR                             |
| `/address-review-comments` | Handle PR review feedback                                        |

## Reference Documentation

All detail lives in `docs/atdd/` — read on demand:
`workflow.md`, `project-detection.md`, `quality-gates.md`, `legacy-integration.md`,
`spec-writing.md`, `gherkin.md`, `checklist.md`, `templates/`.
