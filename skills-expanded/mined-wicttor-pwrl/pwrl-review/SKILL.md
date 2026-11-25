---
name: pwrl-review
description: Review code changes through 4-phase micro-skill pipeline (scope, prepare, analyze, report)
argument-hint: "[branch, PR number, or empty for current branch]"
---

# PWRL Review

Review code changes through a deterministic 4-phase pipeline: validate scope, prepare for review, analyze code quality/security/tests, and generate approval decision.

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "What code would you like to review? Provide a branch name, PR number, or leave blank for the current branch."
- Provide clear recovery suggestions when errors occur

## Purpose

Provide comprehensive code review through systematic analysis:

- **Validate Scope** — Ensure changes match requirements, detect scope creep
- **Prepare Review** — Gather artifacts, establish baselines, configure analysis
- **Analyze Code** — Review quality, security, tests, documentation, integration
- **Generate Report** — Compile findings, determine approval status

## Usage

```bash
/pwrl-review
/pwrl-review feature/U2-email-validation
/pwrl-review origin/dev
```

## Architecture

**Pure Skill Pipeline** — Direct sequence of 4 micro-skills:

```
Input (branch/PR)
  ↓
Phase 1: pwrl-review-scope
  ├ Input: Source branch, requirements
  ├ Output: Scope artifact (scope_verdict, files_analyzed)
  ↓
Phase 2: pwrl-review-prepare
  ├ Input: Scope artifact
  ├ Processing: Diff gathering, baseline setup, tool configuration
  ├ Output: Prepare artifact (review_scope, tools_configured)
  ↓
Phase 3: pwrl-review-analyze
  ├ Input: Prepare artifact
  ├ Processing: Code quality, security, tests, docs, integration checks
  ├ Output: Analyze artifact (findings, issues_found by severity, integration_check)
  ↓
Phase 4: pwrl-review-report
  ├ Input: Analyze artifact
  ├ Processing: Format report, calculate verdict, get user approval
  ├ Output: Report artifact (verdict: approved/request-changes/rejected)
  ↓
COMPLETE
```

## Phase Summary

Each phase is orchestrated sequentially. The orchestrator calls the micro-skill, receives the output artifact, validates it with a quality gate, and passes it to the next phase.

**Phase 1: Scope** ([pwrl-review-scope](../pwrl-review-scope/SKILL.md)) — Validate branch scope and file categorization. Output: Scope artifact.

**Phase 2: Prepare** ([pwrl-review-prepare](../pwrl-review-prepare/SKILL.md)) — Setup review environment and configure analysis tools. Output: Prepare artifact.

**Phase 3: Analyze** ([pwrl-review-analyze](../pwrl-review-analyze/SKILL.md)) — Review code quality, security, tests, docs, integration. Output: Analyze artifact.

**Phase 4: Report** ([pwrl-review-report](../pwrl-review-report/SKILL.md)) — Compile findings and determine approval verdict. Output: Report artifact.

**Phase 5: Sync Status** ([pwrl-review-sync-status](../pwrl-review-sync-status/SKILL.md)) — Post findings to GitHub PR with comment, formal review, and labels. Output: Sync confirmation.

**Quality Gates:** Run `/pwrl-phase-checkpoint review N [artifact-path]` to validate each phase. See [pwrl-phase-checkpoint](../pwrl-phase-checkpoint/SKILL.md) for validation rules.

### Interaction Mode Propagation

Interaction mode (`detailed | smart | yolo`) is set in Phase 1 (via `pwrl-review-scope` Step 0) and read at the start of each subsequent phase. The mode is stored in the scope artifact's `interactionMode` field and propagated through every downstream phase.

- **`detailed`** — Pause at every phase transition (Scope → Prepare → Analyze → Report → Sync); show generated artifacts; require explicit approval to proceed. Best for complex reviews, unfamiliar code, and high-stakes changes.
- **`smart`** — Phases run automatically; pause only when the next phase produces a HIGH-risk operation (e.g., posting a formal GitHub review, labeling a PR with a release-blocker). v1 simplification: behaves like Yolo with a single confirmation prompt at workflow start.
- **`yolo`** — Every phase runs automatically; only the final report is shown. Fastest. Best for routine, well-understood reviews.

**Future refinement:** In Yolo mode, `pwrl-review-report` should auto-approve the review unless CRITICAL issues are found (currently it always asks). This behavior change is out of scope for plan 2026-06-29-001; see `docs/learnings/pattern/interaction-mode-three-mode-propagation-2026-06-29.md` §"Future Refinements".

**Exception:** Error recovery steps always pause the pipeline, regardless of mode.

## Verdict Criteria

See [verdict-criteria.md](references/verdict-criteria.md) for comprehensive approval matrices, quality score calculations, and decision logic for all verdicts (APPROVED, REQUEST CHANGES, REJECTED).

## Review Lenses

- **Correctness** — Logic errors, edge cases, error handling
- **Security** — Input validation, injection, auth, secrets
- **Maintainability** — Clarity, complexity, duplication, abstraction
- **Testing** — Coverage, scenarios, assertions, isolation
- **Performance** — Efficiency, resource usage, slow operations
- **Integration** — No broken imports, circular deps, regressions

## Support Files

- `pwrl-review-scope/references/scope-validation-protocol.md` — Phase 1 specification
- `pwrl-review-prepare/references/prepare-review-protocol.md` — Phase 2 specification
- `pwrl-review-analyze/references/analyze-code-protocol.md` — Phase 3 specification
- `pwrl-review-report/references/report-generation-protocol.md` — Phase 4 specification

## When to Use

- After completing implementation work
- Before creating a pull request
- To review someone else's code changes
- When you need confidence before merging
- After completing a task from pwrl-work

## Control Tokens

Optional tokens control review depth and execution mode:

- `depth:fast` — Quick scan, minimal findings, no artifacts
- `depth:standard` — Balanced review (default), prefer subagents if available
- `depth:deep` — Thorough audit with parallel subagents and artifacts
- `subagents:on|off` — Force subagent mode (default: auto)

Tokens are stripped before interpreting remainder as branch/PR/commit/URL. Error if conflicting depth tokens provided.

## Micro-Skill References

For detailed implementation and workflow specifications for each phase, see:

- [pwrl-review-scope](../pwrl-review-scope/SKILL.md) — Phase 1: Scope validation
- [pwrl-review-prepare](../pwrl-review-prepare/SKILL.md) — Phase 2: Environment preparation
- [pwrl-review-analyze](../pwrl-review-analyze/SKILL.md) — Phase 3: Code analysis
- [pwrl-review-report](../pwrl-review-report/SKILL.md) — Phase 4: Report generation

Each micro-skill is complete and self-contained with its own workflow, error handling, and testing coverage.

## Output

- Code review report with findings grouped by severity
- Verdict: APPROVED | REQUEST CHANGES | REJECTED
- Artifacts from each phase (scope, prepare, analyze, report)
