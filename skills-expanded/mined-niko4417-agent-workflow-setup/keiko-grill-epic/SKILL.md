---
name: keiko-grill-epic
description: Turn a rough Keiko feature idea (or an existing epic) into an implementation-ready GitHub epic with scoped child issues, through one evidence-first grilling session. Use when planning a Keiko epic, stress-testing feature scope, converting a product idea into child issues, or hardening an epic before implementation. Inspects current dev, ADRs, templates, styleguide, security guardrails, code, and GitHub metadata before asking; asks only product, UX, policy, risk, or scope questions that project evidence cannot answer.
---

# keiko-grill-epic

Turn a rough Keiko feature idea into an implementation-ready parent epic plus scoped child issues, through one evidence-first grilling session. **Upstream of `keiko-epic`**: this skill _creates or hardens_ the epic package; `keiko-epic` later _executes_ a ready epic. **Defers to** `docs/workflow-contract.md` for the delivery model, quality bars, and guardrails — do not restate contract rules.

**Input:** a rough feature idea (→ new epic), or an existing epic number `#E` to harden.

## 0. Select the product profile (before anything else)

Select against the target checkout using [profile selection](../../../profiles/README.md).
State the profile on the first output line; explicit operator selection wins.
Load only the selected profile and its task-relevant authority docs, including the
target's `AGENTS.md` and `CONTEXT.md` when present. Take readiness, verification,
templates, evidence, exclusions, and merge authority from it; ambiguity requires
clarification. The accepted target contract governs product requirements.

In `keiko-native`, also read [Native planning](references/native-planning.md).

## Core rule

No question cap. Unlimited useful questions, zero self-answerable ones. Classify every question before asking:

- `ask user` — product, UX, policy, business priority, scope, risk acceptance, rollout
- `inspect` — answerable from code, ADRs, templates, styleguide, GitHub metadata, or behavior
- `defer to issue` — implementation detail that belongs in a child issue; no scope/risk change
- `out of scope` — belongs in a follow-up epic or an explicit non-goal

Ask the user only `ask user` questions. `inspect` → examine and decide. `defer to issue` → write the constraint into the child issue. `out of scope` → preserve it on the parent epic as a deferred follow-up. If the user keeps answering "yes", stop and audit the line of questioning; continue only if the next answer changes scope, UX, policy, trust, rollout, or slicing.

## Evidence pass (before grilling)

Sync first: ensure the local checkout reflects the latest `origin/dev` (fetch/sync) so all evidence is current — never reason from a stale base or from memory. Then inspect, treating current code/templates/ADRs/styleguide as higher authority than older examples or chat memory:

1. `.github/ISSUE_TEMPLATE/` and `pull_request_template.md` — current templates override older examples.
2. Relevant ADRs, guardrail/security/product docs, design-system guidance, existing feature patterns.
3. Relevant code paths on current `dev`.
4. Strong completed epics/child issues for the quality bar — reconciled against current templates and behavior.
5. GitHub metadata when hardening an existing epic: parent-child links, labels, project fields, comments, body.

## Grilling discipline

Apply `grill-me` principles inside Keiko guardrails:

- Ask small rounds of independent unresolved decisions (usually 2–3), each with a
  recommended answer and its consequence. Ask prerequisites first; dependent
  questions wait for their answers. A single decision can stand alone. When the
  user accepts a recommendation, record it and continue without reconfirming it.
- Walk the decision tree to shared understanding.
- Never ask what inspection can answer; never ask confirmations the contract/ADRs already imply.
- Resolve scope tradeoffs against user value, risk, and the selected delivery unit. Respect explicit user decisions; preserve deferred ideas as follow-ups.

Good: "Should v1 include text selection/copy, given governance implications?" · "Should a recoverable citation failure open an in-viewer recovery state, or only an inline chat error?" · "Is this follow-up part of v1, or a later epic?"

Bad: "Should the API accept `chatId + assistantMessageId + marker`?" · "Should we reuse the window config sanitizer?" · "Should the issue use the current template?" → inspect and encode the answer into the epic or child issue.

## Scope control

Define the smallest useful shippable unit, its non-goals, and the tradeoffs for any
expansion. If the accepted idea needs multiple epics, explain the dependency and
split it with the user's scope decision preserved. Do not reopen a settled choice
unless new evidence changes its consequences.

## User journey & platform surface (user-facing / cross-platform epics)

For any epic that ships user-facing UI or runs cross-platform, pin these in the epic body **before** slicing — each is an acceptance anchor children verify against, not prose:

- **Primary user journey** — the single end-to-end path a user takes, bound to a **branch/SHA baseline** so "done" is measured against a known state, not a moving target.
- **Platform matrix** — the OSes/runtimes that must pass **per the active profile** (keiko-web: per the CI cross-platform smoke; **keiko-native: Windows + macOS only, Linux deferred — never add it to acceptance**); each becomes a verification target, not an afterthought.
- **UI surface** — the exact screens/components/states in scope, feeding the profile's evidence model (keiko-web: design-system `state-matrix.md` coverage; keiko-native: the issue's **Acceptance Journey** checkpoints).

Backend-only epics with no user-facing or platform surface may skip this. If a journey / platform / surface cannot be pinned by inspection, that is an `ask user` question — resolve it before the epic is Ready.

## Slicing into child issues

Use `to-tickets` for the slicing **method only** — thin tracer-bullet vertical slices (each a complete path through every layer, independently verifiable), created in dependency order (blockers first). Its "quiz the user" step is **subordinated to the Core-rule classify-gate**: derive dependencies and sequencing by inspection; ask the user only slicing questions that change scope, UX, policy, or risk.

**Stay scope-wary while slicing, too.** Each slice is the **thinnest** complete path that delivers observable value — resist padding it with "while we're here" extras. A slice that has grown fat is two slices; a slice that isn't independently verifiable is mis-cut. Keep every slice sized to a single fresh context window, and keep anything not required for _this_ slice's acceptance out of it.

For every cross-child dependency, define the **interface contract** (inputs, outputs, types, error/empty states) in both issues, so the dependent slice is built against a stable boundary.

**Wide refactors — the exception to vertical slicing.** A change whose blast radius fans across the whole codebase (rename a shared symbol/column, retype a shared type) can't land as one green vertical slice, and forcing it into one breaks thousands of call sites at once. Sequence it **expand → migrate → contract** instead:

1. **Expand** — add the new form _beside_ the old so nothing breaks (both exist).
2. **Migrate** — move call sites in blast-radius-sized batches (per package / per directory), **each batch its own child** blocked by the expand; CI stays green batch to batch because the old form still exists.
3. **Contract** — delete the old form once no caller remains, in a child blocked by every migrate batch.

If the batches can't stay green alone, keep the sequence but let them share an **integration branch** that all block a final integrate-and-verify child — green is promised only there. Never force a wide refactor into a single tracer bullet.

Author every issue with the **active profile's templates** (keiko-web: `epic.md` for the parent, `feature_task.md` for children; **keiko-native:** the typed templates `epic.md` / `feature_task.md` / `decision_evaluation.md` / `defect_finding.md`, exactly one `type:*` label each, and every implementation issue carrying its **Execution Authority** + **Quality Plan**). `to-tickets`' minimal body is _not_ compliant — it omits the reuse gate, board workflow, verification gates, stop conditions, and epic linking. One parent epic + child issues; declare dependencies; prefer one PR per child; children target the epic branch, not `dev` (see contract).

> `to-tickets` is optional. The method above is self-contained; no personal skill-store dependency is required.

For each child's test / Quality Plan, map requirements to public verification
seams. State what each **catches** and **misses** (one line each), and cover missing
wiring, recovery, and platform claims in the integrated gate. Do not copy the
implementation's calculation as the test's oracle or introduce another approval
ceremony for routine test structure.

## Release / enterprise-acceptance QA gate (mandatory, every epic)

Every epic carries a **release-acceptance QA gate** that qualifies the whole epic before its `-> dev` PR — as a **dedicated final child** (substantial epics) or an **epic-body acceptance section** (small epics). No epic is Ready without it. In **`keiko-native`** this gate **is** the epic's **Quality Envelope / Integrated verification** (`docs/engineering/code-quality-standard.md`); the two CORE rows below are exactly Native's two core obligations (verify the wired production composition; machine-evaluated evidence for every automatable claim). Generalizes the policy made explicit in epic #2384 (see child #2396). Acceptance **scales to the epic's surface** — include only applicable rows, but never drop the two CORE rows:

- **User-path matrix** — enumerate every top-level user/enterprise journey the epic touches; the rows below are asserted per path.
- **Contract + unit** coverage for every path.
- **Mocked integration tests** across the failure envelope: errors, races, cancellation, malformed responses, disconnects, recovery.
- **Real production-composition functional tests** — the actually-wired runtime/product, not fixtures. **(CORE — never dropped.)**
- **User-facing surface:** full **Playwright** per top-level journey; **packaged-product** coverage on the reference install (e.g. macOS arm64 via Computer Use); **cross-platform release-gate equivalents** (Windows x64, macOS x64) — packaged / native / functional / Playwright-equivalent.
- **NFR matrices** as the surface warrants: security, accessibility, responsive, visual, performance, memory, backpressure.
- **Machine enforcement** — the gate **rejects manual-only, mock-only, screenshot-only, or fixture-only** coverage; every claim is backed by a real reproducible run (actual command and journey results recorded at the inspected head). **(CORE — never dropped.)**

**Scale rule:** a backend-only epic omits Playwright / Computer-Use / responsive / visual but keeps contract + integration + real production-composition + performance/backpressure + security + machine enforcement. Match the matrix to the real surface; never force irrelevant rows, never drop the two CORE rows.

## Definition of Ready (exit criterion)

Every child issue must satisfy the **active profile's** Definition of Ready so `keiko-issue`/`keiko-epic` can pick it up. **keiko-web:** acceptance criteria + a verification command, and the issue claimable (unassigned). **keiko-native:** the body must pass the machine validator (`quality/issue-contract.mjs`) so the target's `issue-readiness` workflow grants `status: ready` — exact per-type sections, a `Planning contract` version, no placeholders, checked DoR, an observable acceptance criterion, and a `Required`/reasoned-`Not applicable` journey. Respect the lifecycle (`docs/qa/issue-lifecycle.md`): an issue moves `new → triaged → ready`; **`triaged`** (reviewed, classified, ordered) is **not yet executable** — request `status: ready` only when the contract is complete and accepted, and remember readiness is judged independently of the label (never treat a lingering `status: ready` as proof of current readiness). The planner requests ready; **the repository automation remains the readiness authority.** Encode each technical unknown as an inspected, answered fact or an explicit child-issue constraint — never leave it as an open user question the project could have answered. **The epic is not Ready until its release-acceptance QA gate exists** (dedicated final child or epic acceptance section, scaled to surface).

## GitHub hygiene

Use the current templates for the epic and every child. Link children as GitHub sub-issues (not just body links). Set labels, classification, project fields, and priority per current conventions. Use comments only for temporary planning; fold useful planning into the bodies and remove clutter before finishing. Verify final state: bodies, parent-child links, project fields, dependencies, readiness. If you draft locally first, mark it temporary and remove it once the GitHub bodies are the source of truth.

## Escalate (stop, report)

The idea needs splitting across multiple epics · a required product or architecture decision is missing and cannot be inspected · the idea contradicts an ADR or guardrail · scope cannot be made shippable without weakening architecture, security, evidence semantics, or deterministic verification.

## Final output

Parent epic link (or draft path) · child issue links + dependency order · major scope decisions · deferred follow-ups preserved on the epic · verification/audit expectations · remaining product decisions, if any · confirmation that technical unknowns were inspected or placed in the right child issue. Do not claim implementation readiness until the issue bodies themselves contain the decisions, acceptance criteria, verification expectations, and audit/closure requirements.
