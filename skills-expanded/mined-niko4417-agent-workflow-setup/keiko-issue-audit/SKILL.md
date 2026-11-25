---
name: keiko-issue-audit
description: Audit an implemented GitHub issue against its accepted requirements and repository standards, fix confirmed gaps, and write SHA-bound evidence. Use before PR-ready handoff or to recheck claimed completion. Takes an issue number; runs embedded in delivery or standalone.
---

# keiko-issue-audit

Canonical, parameterized issue-audit procedure for both harnesses (Codex primary,
Claude backup). Replaces the old copy-paste audit prompts. It **selects relevant
canonical roles** (`.agents/roles.yaml`) and **defers to the governance contract**
(`docs/workflow-contract.md`) for branching, gates, and the delivery model — do
not restate those rules here, follow them.

**Argument:** the GitHub issue number to audit (e.g. `178`). Below, `#N` = that issue.

## Role

You are the lead session (the sole orchestrator). Start with independent read-first
review, then scoped repairs. The lead may fix a small confirmed gap; a reviewer
who did not author that change must independently confirm the repaired head.

## 0. Select the product profile (before anything else)

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

## Source of truth

1. Fetch issue `#N`: body, labels, comments, linked PRs/commits, child issues.
2. Audit checklist = the **active profile's accepted contract**. **keiko-web:** the
   issue's **acceptance criteria**. **keiko-native:** the accepted issue contract —
   **acceptance criteria + the issue's Quality Plan** (and Acceptance Journey when
   user-facing) at its validated `Planning contract` version; refresh evidence after
   fixes, and do not invent acceptance beyond it.
3. Find the implementation (linked PR or the commits claiming to resolve `#N`).
   If none exists, stop and report the issue is not audit-ready.
4. If scope is ambiguous or conflicts with governance, stop and report the
   blocker — do not invent product scope. In keiko-native, an instruction to consult
   the private Fachkonzept is a missing-requirement defect: stop, return to planning.

## Audit wave (read-first, full)

Cover the entire accepted scope using the smallest relevant review wave. Select
specialists for the changed surface; an irrelevant review dimension is not a
reason to spawn another agent. At least one reviewer who did not author the
implementation covers requirements and repository standards. A single qualified
`verifier` or `pr-reviewer` may cover both axes for a small change; self-review and
green checks alone do not satisfy the independent audit. Add specialists for
material risks and any target-required separation of duties.

Keep two review axes distinct in the existing reviewers' findings:

- **Requirements/spec:** trace every accepted requirement to implementation and
  evidence, including omitted behavior, failure paths, and production wiring.
- **Repository standards:** discover the target's `AGENTS.md`, applicable scoped
  instructions, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, ADRs, and configured gates
  when present. Cite the exact rule and its applicable scope for a violation.

Each confirmed finding needs `file:line`, its requirement/rule, and the concrete
failure or missing obligation. Separate optional heuristics/preferences from
defects; they do not invent new acceptance or block delivery. Use the active
profile and accepted contract to resolve authority; unresolved conflicts are
blockers to surface, not rules to silently choose. These axes do not require two
additional agents.

Choose the roles needed for the changed surface, with explicit read scope:

- `verifier` or `pr-reviewer` — independent acceptance, correctness, regression and
  repository-standard review; one may cover a small change completely.
- `explorer` — when mapping unfamiliar production paths is needed.
- `architect` — material architecture, contracts, or ADR changes.
- `security-auditor` — material trust-boundary, secret, auth, model-access or unsafe
  data-flow risks; `security-triage` may handle an appropriate first pass.
- `performance-engineer` — measurable performance risk.
- `a11y-auditor` — target-required independent UI accessibility/fidelity review.
  User-facing changes always retain the active profile's required evidence:
  Web design-system fidelity and evidence under ADR-0049/0051; Native design
  baseline and Acceptance Journey. Missing required evidence blocks the audit.

Convert **only confirmed, evidence-cited findings** into fix slices. Speculative
findings are not blockers.

## Fix wave (scoped)

In standalone mode, create the profile's source branch **before fixes** (web:
`issue/<N>-audit` or `codex/issue-<N>-audit` from `dev`; Native: runner-managed issue branch from the frozen
accepted target). Embedded audits keep fixes on their parent's branch.

1. Fix a small scoped gap directly, or assign **disjoint** ownership to
   `implementor` / `developer` when delegated repairs materially help.
2. Add `test-engineer` when regression coverage needs specialist work; ordinary
   focused tests may be written by the repair author.
3. Preserve behavior unless the issue explicitly required a change. Preserve the
   deterministic-first architecture; keep model calls behind the Model Gateway;
   keep CI/tests/release-gates/CSP/security-scans/evidence at least as strict.

## Verify and record evidence

1. Run applicable target checks locally. The optional `.keiko-scripts/verify.sh`
   runner selects current required commands first (ADR-0145 individual commands);
   older accepted paths remain compatibility options. Verify required
   platform evidence on the authoritative runners named by the accepted plan.
2. The independent reviewer confirms every accepted checklist item with evidence
   and returns the proposed PR "Verification evidence" section to the lead for
   publication. The same reviewer may perform this confirmation without another
   mandatory handoff. For a **user-facing** change, the
   audit is not complete until the profile's evidence is captured (keiko-web:
   design-system fidelity + `docs/design-system/evidence/<N>/` — theme screenshots +
   `*-fidelity-proof.json` + `a11y-proof.json`, ADR-0049/0051; **keiko-native:** the
   Acceptance Journey's automated/a11y/visual/recovery/platform evidence, bound to
   the exact head).
3. Commit all scoped fixes with `#N` (`Refs #N`, or `Resolves #N` only when the
   accepted lifecycle should close on merge). Refresh evidence at this committed
   HEAD and report the actual results before opening/readying the PR.

## Publish audit evidence

After scoped fixes are committed, rerun the affected target checks and accepted
journeys, then independently confirm the corrected requirements at that head.
The lead publishes the inspected commit, actual commands/results, confirmed
findings and their fixes, remaining limitations, and required UI/platform results
in the PR body or a PR comment. A clean audit means no unresolved confirmed
findings; do not substitute an assertion of completion for executed evidence.
A changed head requires refreshed affected verification and audit evidence.

## Open/update and handoff

In embedded mode return the proposed evidence to the parent delivery skill.
Standalone mode follows `keiko-issue`'s target-authorized PR delivery and any
explicit final review hold. Use ordinary Git/GitHub commands in the chosen target
workdir. Required CI must pass on the exact current PR head and every review
finding must be settled before merge; missing or skipped required PR checks do
not qualify. Authorized Web auto-merge uses `gh pr merge <N> --auto --squash
--match-head-commit <exact-head-sha>`; Native retains its own delivery identity
and frozen authority. Do not add per-child human approvals.
The lead or delegated `pr-shepherd` handles bounded repairs; stop after three
materially distinct failed attempts and report the blocker. Refresh affected checks/audit/journeys after fixes
and update the PR evidence for the new head.

## Memory

Append to `.agents/memory/<role>/` **only a durable, generalizable lesson** — a
recurring finding, a repo gotcha, a workaround, a systemic gap. **Not** per-issue
facts (those live in the PR closure evidence) and **not** "audited #N, clean." If
this run taught nothing reusable, write nothing — silence beats noise. Keep
<25 KB/file; never store secrets, customer data, source dumps, or token-bearing
logs. (The epic-level `keiko-retro` pass aggregates across runs and prunes.)

## Final report

Issue audited · audit roles used + why · implementation inspected · findings
confirmed · findings fixed · files changed · tests/checks run · PR + `ci` status ·
residual risks / follow-ups.
