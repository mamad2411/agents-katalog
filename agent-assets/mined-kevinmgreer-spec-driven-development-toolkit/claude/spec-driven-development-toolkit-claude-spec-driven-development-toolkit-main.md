# Spec-Driven ATDD Toolkit

> **Golden Rule:** Never write production code unless a failing acceptance test requires it.

Language-agnostic, platform-agnostic ATDD toolkit. Works in any project — greenfield or legacy.

---

## First Action of Any Feature Work (Profile Bootstrap)

Before writing a spec, tests, code, or running quality gates — including ad-hoc requests —
**check whether `docs/project-profile.md` exists**.

- **Missing**: first action is to create it (run Phase 0 — see `docs/atdd/workflow.md` § Phase 0
  and `docs/atdd/project-detection.md`). Tell the user: _"No project profile found — running
  Phase 0 first so I have an accurate picture of this codebase's tooling and conventions."_
- **Exists**: read it first; treat as authoritative.
- **Never** detect tools/conventions on the fly without persisting the profile to disk.

---

## The Cycle

```
Analyze → Spec → Tests (Red) → Implementation (Green) → Quality Gates → Refactor →
Spec & Doc Sync → Archive → PR → Review
```

**Full procedure: [`docs/atdd/workflow.md`](docs/atdd/workflow.md)** (authoritative).
Hard rules, command reference, and reference docs: [`AGENTS.md`](AGENTS.md).

---

## Commands & Agents

Slash commands live in `.claude/commands/`; subagents in `.claude/agents/`.

| Trigger                                   | Purpose                                                      |
| ----------------------------------------- | ------------------------------------------------------------ |
| `/atdd-cycle`                             | The full cycle: requirements → PR → review. Start here       |
| `/analyze-project`                        | Phase 0 — detect tooling + conventions; write the profile    |
| `/write-spec` → `/write-acceptance-tests` | Phase 1–2 — delta spec (user gate), then failing test stubs  |
| `/implement-from-spec`                    | Phase 3 — minimum code to green, mirroring the profile       |
| `/run-quality-gates`                      | Phase 4 — lint/format/typecheck/build/test until green       |
| `/refactor-passing-tests`                 | Phase 5 — safe refactor, tests stay green                    |
| `/verify-spec-coverage`                   | Phase 6 — hard spec & doc sync gate (repairs drift in-place) |
| `/archive-change`                         | Phase 7 — merge delta into capability; archive the change    |
| `/create-pull-request`                    | Phase 8 — branch, commit, push, PR                           |
| `/address-review-comments`                | Handle PR review feedback                                    |
| `spec-writer` subagent                    | Writes Gherkin + technical specs (never code)                |
| `spec-reviewer` subagent                  | Read-only spec & doc compliance review                       |

Non-negotiables, in brief:

- Red before green; never modify tests to pass; never add logic not demanded by a failing test
- Phase 1 requires explicit user approval of the spec before Phase 2 runs; the autonomy level
  is chosen at that same gate, never as a separate up-front question
- Phase 3 re-reads `docs/project-profile.md` and mirrors its conventions — no inventing
- Phase 6 (Spec & Doc Sync) is a **blocking** gate; repair drift in-phase
- Classify every Phase 6b repair ADDED / MODIFIED / REMOVED; a REMOVED narrows the spec and
  needs sign-off, not "match the code"

Do not skip or reorder phases.
