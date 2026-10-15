---
name: kf-verify-change
description: Verify existing changes without modifying them. Use when the user asks to review a diff or artifact, run checks, confirm readiness, or validate an existing implementation or design. Report evidence, actionable findings, and residual risk. Do not fix findings or act as the primary feature, bug, investigation, refactor, or design workflow.
---

# Verify Change

Determine whether an existing change satisfies its intended outcome and is ready to
hand off. Verification measures and reports; it does not correct.

## Workflow

1. Establish the verification target: requested outcome, observable acceptance
   criteria, artifact or diff scope, compatibility constraints, and relevant
   baseline. Separate verified facts, assumptions, and unknowns.
2. When a design contract exists, use its target, decisions, constraints,
   non-goals, acceptance evidence, unresolved assumptions, and affected boundaries
   as inputs. Revalidate them against the current repository rather than treating
   the design as proof.
3. Read applicable repository guidance, current status, the complete in-scope diff
   or artifact, and affected code paths before selecting checks.
4. Assess impact and risk. Choose the smallest meaningful combination of focused
   tests, type checking, linting, formatting checks, builds, schema or migration
   validation, compatibility checks, and broader suites supported by actual
   tooling.
5. Review the change against its acceptance criteria, repeated repository patterns,
   public contracts, and unaffected behavior. Trace important boundaries rather
   than validating filenames or exit codes alone.
6. Run the selected checks and inspect their complete relevant results. Prefer
   check, dry-run, or non-mutating modes when available, and inspect status again
   for artifacts produced by verification commands.
7. Classify each failure as change-caused, pre-existing, environmental, or
   unresolved only when evidence supports that classification. Do not attribute a
   failure by timing or proximity alone.
8. Report only actionable findings, ordered by severity. For each finding, state
   the evidence, violated outcome or invariant, impact, confidence, and the
   execution workflow that should own correction.
9. Give a readiness result of **ready**, **not ready**, or **indeterminate**. Report
   checks run and their results, critical checks not run, produced artifacts,
   assumptions, and residual risk.

## Correction routing

- Missing or incorrect requested behavior returns to `kf-implement-feature`.
- A demonstrated violation of an existing contract returns to `kf-fix-bug`.
- A structural problem whose correction must preserve behavior returns to
  `kf-refactor-code`.
- An unexplained failure or uncertain cause returns to `kf-investigate-issue`.
- An unresolved acceptance contract, interface, migration, or architecture decision
  returns to `kf-design-change`.
- A verified recurring contradiction in workflow method, routing, or guidance is
  reported as a learning signal for `kf-learn-from-evidence`; verification does
  not persist the lesson.

If the user asks to verify and repair in one request, complete and report the
verification first, then hand the findings to the applicable execution workflow.
Do not perform the repair while operating under this skill.

After the execution workflow reports correction complete, re-enter verification
with the original target and the current artifact. Reassess the affected checks and
publish a new readiness result; do not reuse the earlier verdict. Continue only
while evidence shows progress and the requested authorization still covers the
next correction. Stop when the result is ready, a blocker makes it indeterminate,
the same unresolved failure repeats without new evidence, or another correction
would require broader authority.

## Constraints

- Do not edit source, tests, documentation, configuration, snapshots, generated
  artifacts, or the reviewed design. Running checks is allowed; intentional
  correction is not.
- Do not weaken, disable, update, or reinterpret a check to make the result pass.
- Do not hide contradictory evidence, existing failures, incomplete coverage, or
  commands that could not run.
- Do not claim readiness while a blocking finding remains or a critical risk lacks
  meaningful evidence.
- Do not run every expensive check by default. Match verification depth to the
  change's impact, reversibility, and repository practice.

## Completion questions

- Does the change solve the requested task?
- Does it follow repeated repository patterns?
- Does it preserve unrelated behavior?
- Did it introduce unnecessary abstractions or dependencies?
- Does it touch unrelated code or formatting?
- Is a simpler complete implementation available?
- Were the relevant checks actually run?
- Is every failure classification supported by evidence?
- Are correction and verification still owned by separate workflows?
- When repair was requested, was the corrected artifact re-verified against the
  original target?

Verification is complete when the readiness result, material findings, supporting
evidence, unrun critical checks, and residual risk are explicit.
