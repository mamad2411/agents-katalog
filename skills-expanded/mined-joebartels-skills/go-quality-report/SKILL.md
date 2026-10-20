---
name: go-quality-report
description: Orchestrate a comprehensive graded Go quality review of a changeset, codebase, package, or supplied code. Use when the user wants an overall report across relevant Go quality topics, delegated report cards, or a pre-merge quality assessment; use a single topic skill for a specifically limited topic review.
metadata:
  review-contract: "1"
---

# Go Quality Report

Coordinate the nine Go review skills and synthesize one evidence-backed overall result. Review only; fixes, installation, publication and merge actions require their own user request. This skill needs the applicable topic skills, discovered by name through the host or a local skill catalog. It does not contain substitutes for them.

## 1. Fix the target

Use the user's explicit target. For a changeset, record exact base/head or the supplied patch; for staged, unstaged or untracked work, record the actual snapshot and included paths. For a codebase/code-area review, record the revision/snapshot and named area. Ask a focused question only if plausible interpretations materially change what gets reviewed. Offer observed choices; do not guess a default branch or silently substitute the current checkout for a requested revision.

Inspect metadata and file inventory first: relevant instructions, changed paths/statistics, modules, project type, support versions and tests/build configuration. Delegate deeper discovery for a large tree. Track later source changes and invalidate affected cards. Non-Go files such as migrations, CI, schemas and manifests can affect Go quality. If nothing implicates the Go topics, return Not applicable with scope and reason.

## 2. Map coverage and bounded work

Read [orchestration](references/orchestration.md) to discover topic skills, route risks, size work and dispatch workers. Create a small manifest of the target, exclusions, chunks, important boundary contracts, topic applicability and owners. Every requested area must be accounted for. Assign cross-boundary and repository-wide obligations explicitly; local approvals alone do not verify integration.

Start with coherent domains or behavior boundaries; combine a small change into one packet and split large ones further. Select topic combinations per packet, not one agent per skill by default. Every topic is considered, but invoke only those with a relevant review question. Record why topics are not applicable; unavailable evidence or missing skills are coverage gaps, not irrelevance. Related files can be read to trace effects. Changeset grades include only introduced, worsened or newly exposed defects; code-area grades include existing in-scope defects.

## 3. Dispatch and collect

Use the host's available delegation API. Give each worker the precise target, bounded paths/contracts, resolved topic-skill locations, relevant context, read-only constraints and artifact destination. Workers must read/invoke each assigned skill and its relevant references, returning its standard report card for each topic, plus inspected coverage and a short handoff. Do not send expected findings or preselect grades.

Choose permitted model capabilities and reasoning effort for the task; respect user pins and actual host support. Use bounded queues within concurrency limits. If delegation is unavailable, review bounded packets sequentially with the same skills and disclose that limitation. Missing applicable skills stay explicitly unassessed.

Keep the orchestrator context to the manifest, compact card summaries, finding index and unresolved questions. Store full cards and evidence in artifacts; retrieve relevant portions for reconciliation. Follow [artifact and output contract](references/reporting.md). Do not paste entire files, logs or repeated cards into synthesis context.

## 4. Reconcile and close coverage

Read [grading and reconciliation](references/grading.md). Check card scope, skill invocation, evidence, counts and limits. Namespaced local finding IDs prevent collisions. Deduplicate the same causal defect across chunks/topics, retaining separate independently actionable defects. Resolve contradictions against evidence, not votes or the most alarming label. Return focused questions to workers or inspect the necessary code. Keep original cards and record accepted corrections.

Perform targeted boundary reviews and close remaining material obligations. Retry/reassign an incomplete packet only with a concrete recovery plan; repeated identical blocked attempts add no evidence. Respect user time/cost constraints and report residual gaps. Sampling or a completed subset must not become a full-codebase claim.

## 5. Grade and report

Grade unique confirmed root causes using the shared rubric, never averages of card grades, clean-chunk dilution or automatic worst-card selection. Recompute topic rollups from unique in-topic causes when useful. A+ safeguards must also be independent and verified. Changing packet boundaries alone must not change the result.

When Python is available, resolve [grade.py](scripts/grade.py) relative to this skill's `SKILL.md` and invoke its absolute path: `python3 /absolute/path/to/go-quality-report/scripts/grade.py /path/to/reconciled-ledger.json`. The ledger format is in the grading reference. Otherwise apply the same table manually. The calculator checks arithmetic, not evidence truth or omitted coverage.

Produce the report in [reporting](references/reporting.md): overall result, scope and coverage, topic breakdown, good/bad with why, prioritized linked changes with why and verification, and limits. Full-scope material coverage gaps mean overall Insufficient evidence; preserve confirmed findings and, when useful, show a separately labeled assessed-scope defect grade. Do not award A/A+ from incomplete material coverage. All topics genuinely irrelevant means Not applicable. Link the underlying cards so detail remains reviewable.
