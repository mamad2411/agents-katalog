---
name: keiko-issue
description: Drive a single GitHub issue (task / feature / bug / user-finding) end-to-end from origin/dev to a green PR, the standard Keiko way — Definition-of-Ready gate, task-shaped execution, quality bars, mandatory keiko-issue-audit, target-authorized delivery. Use when the operator selects one issue to work on. Takes an issue number.
---

# keiko-issue

Canonical, parameterized single-issue workflow for both harnesses. Replaces the
old `codex-task-prompt.md` / `claude-issue-prompt.md` run-cards. **Selects relevant
canonical roles** (`.agents/roles.yaml`), **defers to** `docs/workflow-contract.md`
for branching, gates, and target-owned delivery authority — follow them, do not
restate.

**Argument:** the issue number `#N` (optionally a mode: `feature` adds behavior,
`fix` repairs a defect/regression/finding).

## Role

You are the lead session — the sole orchestrator. You may implement small, clearly
scoped work directly. Delegate when independent execution, specialist judgment, or
safe parallelism materially helps; keep required audit independent of the author.

## 0. Select the product profile (before intake)

Select against the target checkout using [profile selection](../../../profiles/README.md).
State the profile on the first output line; explicit operator selection wins.
Load only the selected profile and its task-relevant authority docs, including the
target's `AGENTS.md` and `CONTEXT.md` when present. Take readiness, verification,
templates, evidence, exclusions, and merge authority from it; ambiguity requires
clarification. The accepted target contract governs product requirements.

Target `AGENTS.md`, scoped instructions, ADRs, and explicit user choices override
generic workflow defaults. For Keiko, ADR-0135 authorizes accepted, checked
`dev` delivery through native auto-merge; ADR-0145 retires `agent:pre-pr`.
An explicit final epic human-review hold overrides target-authorized final auto-merge
for that run and adds no per-child approval. Preserve it until the human explicitly
authorizes final delivery; a green PR or an approval from another agent does not
lift it. Otherwise retain the generic final human-review default where the target
and user have not authorized another path.

## 1. Intake (Definition-of-Ready gate)

Fetch `#N` (body, labels, comments, linked PRs/children). Apply the **active
profile's Definition of Ready**. **keiko-web:** the issue must have acceptance
criteria + a verification command; accepted `New`/`Triaged` work is executable
when those are complete. Actual `Blocked`/`Waiting for User` states require
resolution or the requested decision before resuming. **keiko-native:** it must be
a machine-validated accepted contract — a single `type:*` label, `status: ready` with a matching
readiness record (validated `Planning contract` version + fingerprint), and a
complete **Execution Authority** + **Quality Plan**; an instruction to consult the
private Fachkonzept or infer omitted requirements is a missing-requirement defect
(stop, return to planning). Follow the profile's **Issue lifecycle** rules
(`profiles/keiko-native.md`): **evaluate readiness independently of the `status:*`
label** (a label is not authority), treat **`triaged` as non-executable**, claim only
a genuinely **current-ready** claimable state, and **fail closed** on zero/multiple/
unknown labels or stale readiness. If missing/unready → triage first (comment the gap,
`status: new`), do not start. If it's an epic, use `keiko-epic`. If ambiguous or
conflicting with governance, stop and report.

**Collision check (do this first):** if `#N` already has a GitHub assignee other
than the operator, **do not start** — it's being worked by someone else. Skip and
report. (`gh issue view <N> --json assignees`.)

## 2. Claim on the delivery board

Claiming is mandatory before any implementation:

- **Assign the operator on GitHub** — `gh issue edit <N> --add-assignee @me`. The
  assignee is the cross-agent lock; never start an issue you haven't claimed. In
  **keiko-native** the assign **is** the claim (the claimable-state trigger).
- Board update. **keiko-web:** set `status: in progress`; `Workflow State`/`Status` =
  `In Progress`. **keiko-native:** **do not hand-write the derived `status: in
progress` label** — it is a reconciled effect the target owns; board / project fields
  are **one-way projections**, never authority. In both: `Owner / Agent` = active agent;
  `Human Review Required` reflects target requirements and explicit run holds;
  fill `Branch` once created.

Create the source branch before implementation: web `issue/<N>-<short>` or
`codex/issue-<N>-<short>` from `dev` (epic children from their epic branch); Native a runner-managed branch
including the issue number, from its frozen accepted delivery target. Record the
branch on the board. For isolated workers, verify their actual base includes the
required parent commits before they write; a default-branch worktree is not enough.

## 3. Route (task-shaped)

Use the smallest effective shape; these routes are choices based on the actual
change, not a mandatory roster:

- Small, clearly scoped work → the lead may inspect, implement and test directly.
- `fix` with unclear root cause → execute the reproduction below; use competing
  hypotheses or debug fan-out when bounded investigation needs it.
- A delegated known/scoped fix → `implementor`; a delegated feature → `developer`.
  Cross-layer work needs production-wiring evidence, not automatically more agents.
- User-facing changes retain the active profile's UI standard and accepted journey.
  Use `ui-engineer` for material implementation work and an independent
  `a11y-auditor` where the target or accepted plan requires fidelity/accessibility
  review (Web design system; Native design baseline and Acceptance Journey).
- Select `security-triage`→`security-auditor`, `performance-engineer`, `architect`,
  `test-engineer` or `docs` for material risks or target-required role separation.
  An area label alone is not a reason to add every associated role.

Assign explicit, disjoint ownership to delegated writers. Run the independent
issue audit even when the lead implements; self-review is not that audit. An
accepted spec and implementation authority do not need another plan approval.
Ask only for an unresolved product decision or a change to scope/authority.

## 4. Implement

Apply the shared quality bar and the target's accepted Quality Plan. Issue-scoped only;
no unrelated refactors, TODOs, or placeholders. **User-facing components** conform
to the active profile's UI standard (keiko-web: Keiko Design System — semantic/
component tokens only, full `state-matrix.md` coverage, governance change-rules;
**keiko-native:** `native-design-baseline.md`, satisfying the issue's Acceptance
Journey). In **keiko-native** honor the issue's frozen **Execution Authority** (write
scope, delivery target, prohibitions) and **never** store/quote/request the private
Fachkonzept. Out-of-scope blockers → report up, the lead files a linked issue
(`status: new`); never expand scope.

**Bug reproduction (fix mode).** Before editing, run a command/test that asserts
the reported symptom on the current code; record expected vs actual behavior and
the command's result. A build failure or guessed explanation is not a reproduction
of a behavioral bug. Minimize the input while preserving the failure, then trace
the failing path. If the symptom cannot be reproduced, report the missing evidence
and continue bounded investigation; do not claim a proven fix. After the change,
rerun the original reproduction and relevant regressions. If using a temporary
mutation to prove a test detects the defect, inspect its diff against the pristine
version and prove it landed and caused the intended assertion failure; restore it
before continuing. Never manufacture a red result through a syntax/import error.

**Behavioral test plan.** In the existing test plan / Quality Plan, map accepted
requirements to observable public boundaries (API, adapter, component, CLI, or
production composition). For each seam state one line of what it **catches** and
**misses**, so a green unit test is not mistaken for wiring/platform evidence.
Implement one meaningful red → green slice at a time. Derive expected values from
the requirement or an independent oracle, not the same computation as production.
Use the accepted plan's authority; seek clarification only for unresolved scope
or product decisions, not routine test placement.

Commit scoped implementation with a Conventional Commit referencing `#N`.
Run applicable local checks before pushing; Native retains its frozen Execution
Authority and target-owned delivery contract.

## 5. Verify, audit, ship (per target contract)

1. **Verify.** Run the target's applicable minimum-loop and touched-area commands,
   including mandatory local Sonar where required. `.keiko-scripts/verify.sh` is
   an optional convenient runner; select semantic obligations from the target
   contract/Quality Plan using repeatable `--also <script>`. Package-surface
   assembly runs last because it prunes live dependencies. A fast smoke does not
   replace required checks. Fix confirmed failures and rerun, with at most three
   materially distinct repair attempts before escalation.
   **Cross-layer issue (≥2 layers/packages):** cover root typecheck, architecture,
   a non-test production-composition build, and a real request-path smoke. Unit
   tests alone cannot prove production wiring.
2. **Independent audit.** Run `keiko-issue-audit #N` before PR creation; repair
   confirmed findings and re-audit until clean, within the same bounded recovery.
   Accepted stages may be audited separately: name the audited stage and remaining
   stages. Stage evidence never authorizes closing the whole issue.
3. **UI evidence.** Execute the accepted user journey and report actual results
   at the exact head. Web uses runnable Playwright journeys and target-required
   design-system fidelity/a11y evidence under `docs/design-system/evidence/<N>/`
   (theme screenshots, fidelity/a11y proof files under ADR-0049/0051). Native uses
   its Acceptance Journey's automated/a11y/visual/recovery/platform evidence;
   a browser test cannot substitute for the desktop host.
4. **Publish evidence.** The lead records the exact current PR head, actual
   commands/results, independent audit findings/resolution, UI journey results,
   limitations, and CI links in the target PR template or a PR comment. After a
   new commit, refresh affected checks, audit and journeys and update that record.
   Cancel superseded verifier runs; never attribute old-head results to new code.
5. **Open and deliver.** Use ordinary `git`/`gh` commands from the deliberately
   chosen target workdir. An epic child targets its accepted epic branch and
   proceeds without per-child human approval. A standalone PR follows target/run
   authority. Every merge requires the full exact-head target required-check
   matrix and settled review findings; missing/skipped PR checks never qualify
   through integration-only evidence reuse. When authorized, arm native auto-merge
   with `gh pr merge <N> --auto --squash --match-head-commit <exact-head-sha>`.
   Native merge operations remain with its accepted automation identity.
   The lead or delegated `pr-shepherd` drives CI/review; reproduce failures locally,
   repair, rerun affected QA/audit/journeys, push, and update exact-head evidence. Never bypass
   checks, force-push or push directly to `dev`.
6. **Standalone → `dev`:** honor a target/run hold with `Ready for Human Review`;
   otherwise continue authorized delivery. Flush current state + next action to
   the issue/PR. Epic children continue their accepted integration loop.
7. **Close as done on merge.** When the issue's linked PR is **merged** — a child
   auto-merged into its **epic branch**, or an authorized standalone PR merged into
   `dev` — and **all accepted scope stages are complete with evidence**, transition
   the issue to the profile's **done** state and **close it**.
   **keiko-native:** the issue is closed with reason `completed` carrying exactly
   **`status: done`** (every other `status:*` removed), as a **projection** of the
   target's `docs/qa/issue-lifecycle.md` (done = closed + `status: done`; reopen →
   `new`) — read it at runtime and **fail closed** if labels/contract are missing/stale.
   **keiko-web:** close + `status: done` per the Keiko taxonomy. Only a **merged** PR
   closes an issue as done — never on `Ready for Human Review` alone. Follow the
   target's permitted merge path.

## Escalate (stop, report)

Escalate missing or contradictory acceptance criteria, unresolved product or
architecture decisions, authority conflicts, material scope expansion, overlapping
write ownership, prohibited sensitive artifacts, or exhaustion of 3 materially
distinct repair attempts. Accepted in-scope security, breaking public-API, and
migration work proceeds with the target-required audits and Quality Plan; its
category alone does not require another approval. Confirmed unsafe findings block
delivery until repaired and re-audited. A performance regression outside the
accepted budget must be repaired; escalate when safe resolution needs a missing
decision, additional authority, or exceeds the bounded recovery attempts.

## Final report

Issue · team used + why · files changed · tests/checks run · `keiko-issue-audit`
status · PR + `ci` status · board fields · residual risks/follow-ups.
