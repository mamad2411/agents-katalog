---
name: generic-gate-pipeline
description: Apply whenever a substantive engineering task starts — a feature, bug fix, refactor, or anything else that should pass through the seven development gates. Defines the gate sequence, stack-conditional skipping, and the rules for justified skips.
metadata:
  stack: [generic]
  specificity: 90
---

# Seven-gate development pipeline

**STOP.** For every feature, bug fix, or change — work through these gates IN ORDER. Do not skip gates. Do not start coding before Gate 4. If a gate is incomplete, refuse to proceed and ask which gate output to produce first.

The orchestrator and any local skill that triggers process work should consult this skill before producing code or tests.

## The seven gates

### Gate 1 — Requirements

- Read the relevant `docs/requirements/*.md`. Use [`generic-docs-standards`](../generic-docs-standards/SKILL.md) for placement rules and `[FR-*]` / `[NFR-*]` IDs.
- Ignore anything under a `TBC` header — those sections are not authoritative.
- If the requirement is missing or unclear, **ask the user**. Do not guess.
- If the chat reveals requirement changes, **update the requirements file** in the same change set.

Delegates to `/dev-team:specs` when the four-artifact spec set (Intent / BDD / Architecture / Acceptance) is needed.

### Gate 2 — BDD specification

- Write or update Gherkin scenarios under `docs/bdd/*.feature`.
- Each scenario must map to a **testable** behaviour. No vague "system should be performant".
- Tag every scenario to its governing requirement ID.
- Get user confirmation before proceeding.

Delegates to `/dev-team:feature-file-validation` for syntax + scenario-quality checks.

### Gate 3 — Mocked UI (stack-conditional)

**Applies when:** `nextjs` ∈ active stacks OR `expo` ∈ active stacks. **Skip for pure-backend work.**

- Build the React (or React Native) component with **hardcoded / mock data**.
- No API calls yet — use static data matching the BDD scenarios.
- Show the user for feedback.

### Gate 4 — Failing tests

- Write tests that express the BDD scenarios.
  - **dotnet**: xUnit (domain unit tests for business logic; integration tests for API endpoints).
  - **nextjs**: Vitest (+ Playwright for UI flows when warranted).
  - **expo**: Jest / Expo test runner.
- **Test discipline.** Default for new features: write new tests only; do not modify existing tests. See `generic-code-quality` "Test discipline" for the matrix (new feature / bug fix / changing existing feature / refactor).
- Create skeleton implementation classes (entities, DTOs, validators, repositories, endpoints, components) that throw `NotImplementedException` / `throw new Error('not implemented')` — the solution **MUST compile**.
- ALL tests must FAIL at **runtime** (red), not at compile time, before implementation.
- Verify by running the test command from the manifest for each in-scope stack — e.g. `dotnet test <solution>.slnx` or `pnpm test` in the frontend root.
- **Self-review before handoff:** run `/dev-team:code-review --changed` against the Gate 4 changes and address findings before asking the user to review.

### Gate 5 — Implementation (stack-conditional, but usually applies)

**Applies when:** any stack is in scope (effectively always).

- Implement against the failing tests.
  - **dotnet**: domain logic, services, endpoints.
  - **nextjs**: real components, hooks, state, BFF integration.
  - **expo**: real screens, navigation, native modules.
- Run the test command for each in-scope stack — ALL tests must PASS (green).
- If a test fails, fix the **implementation**, not the test. If the test is genuinely wrong, fix it deliberately and document why in the commit message. **Never edit existing tests just to chase green** — see `generic-code-quality` "Test discipline".
- **Self-review before handoff:** run `/dev-team:code-review --changed` against every coding-gate output (Gate 4 tests + Gate 5 implementation). Address findings BEFORE presenting work for human approval. Only once the self-review is clean (or remaining findings are deliberately accepted with a stated reason) do you ask the user to review.

### Gate 6 — Connect UI to API (stack-conditional)

**Applies when:** Gate 3 applied (i.e. there's a frontend component). **Skip otherwise.**

- Replace mock data with real API calls.
  - **nextjs**: through the BFF proxy at `<frontend-root>/app/api/proxy/...` (see [`nextjs-frontend-standards`](../nextjs-frontend-standards/SKILL.md) and any project-local `vendor-*-bff` skill).
  - **expo**: direct HTTPS to the API; auth strategy is project-specific.
- Verify end-to-end flow works against a real backend (local or dev).
- Run `pnpm check-types` (or equivalent) in each in-scope frontend root for type safety.

### Gate 7 — Cleanup

- **Capture feedback.** Run the `generic-feedback-capture` skill against any corrections, surprises, or "prefer X over Y" decisions surfaced during this work. The skill's destination table routes each item to the right home (a stack-tagged skill, a rule file, the glossary, the stack manifest, user-level auto-memory, `memory/decisions.md`, or a proposed new skill) and updates `metrics/config-changelog.jsonl`. Do this in the same change set so the toolbox learns from this PR.
- If requirements changed, verify `docs/requirements/` and `docs/design/` are both updated and still consistent.
- If a new file exceeded 300 lines of meaningful code, consider whether to split (see `generic-code-quality`).

## Stack-conditional skipping (built-in)

| Gate | Skips when |
|---|---|
| Gate 3 (Mocked UI) | No `nextjs` and no `expo` in active stacks |
| Gate 5 (Implementation) | No code-bearing stack in scope (rare — usually applies) |
| Gate 6 (Connect UI to API) | Gate 3 was skipped |

The orchestrator should announce skipped gates explicitly so the user sees the routing decision.

## Justified gate skipping (`--skip-gate=N --reason=…`)

For genuine edge cases (typo fixes, doc-only changes, hot-fixes that bypass BDD), a gate may be skipped with an **explicit justification**. The justification is logged to `memory/decisions.md` as a `DEC-YYYY-MM-DD-NNN` entry by the orchestrator.

Examples:

- `--skip-gate=2 --reason="docs-only change to a guide, no behaviour"` — Gate 2 (BDD) skipped.
- `--skip-gate=3 --reason="API-only field rename, no UI"` — Gate 3 (Mocked UI) skipped.
- `--skip-gate=4 --reason="emergency hot-fix to prod outage; backfill tests in follow-up"` — Gate 4 (Failing tests) skipped, **only with explicit human approval and a follow-up commitment**.

Default = no skips. Justified skips = exception, not norm.

## Anti-patterns

- Skipping Gate 4 silently because "the change is small". Skill enforces RED-GREEN-REFACTOR — the discipline matters more than the size.
- Skipping the self-review (`/dev-team:code-review --changed`) between Gates 4 and 5, or between Gate 5 and human handoff. Self-review catches the cheap-to-fix issues before the human spends time.
- Editing tests to make them pass when the implementation is buggy. Fix the implementation.
- Letting Gate 1 conversations not flow back to the requirements file. If the chat reveals new constraints, update `docs/requirements/` in the same change set.
- Treating Gate 7 as a vestigial step. The Code-Standards-feedback-loop is how the toolbox stays sharp.
