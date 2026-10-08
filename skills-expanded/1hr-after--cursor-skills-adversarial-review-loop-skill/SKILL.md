---
name: adversarial-review-loop
description: Bounded build-then-independent-review loop for a meaningful code change. Plans, implements, verifies, and ships a pull request, then runs an INDEPENDENT adversarial reviewer (a different model family than the builder, Codex-class for general review) that returns severity-ranked findings; the builder fixes every finding at or above a configured severity threshold, pushes, and re-reviews. Persists plan, branch, PR, findings, verdict, and iteration so the run resumes safely. Stops only when the reviewer approves, only sub-threshold findings remain, or max-iter is reached — and NEVER reports a stalled, errored, or exhausted run as approved. Use for code changes that benefit from an independent reviewer and several structured review-and-fix rounds — e.g. "clodex", "adversarial review loop", "review and fix until approved", "independent code review loop".
---

# Adversarial Review Loop

A bounded development workflow that plans and ships a pull request, runs an
**independent** adversarial review, fixes blocking findings, and repeats until the
reviewer approves or the iteration budget runs out. It separates the *builder*
from the *reviewer* so review feedback drives a bounded repair loop instead of the
author grading their own work.

## The invariant (read this first)

1. **Builder ≠ reviewer.** The reviewer is a different model family than the
   builder (Codex-class for general review), and runs read-only against the diff.
2. **Threshold is a ceiling, not a floor.** It names the *highest acceptable*
   severity to leave unfixed. Inspect everything; fix everything at or above it.
3. **Resumable, honestly.** Persist plan/branch/PR/findings/verdict/iteration so an
   interrupted run continues — without ever pretending an interrupted run passed.
4. **Never launder a non-approval.** A stalled, errored, or budget-exhausted run is
   reported as exactly that. Only an actual reviewer approval is "approved".

## When to Use

- A meaningful code change (feature, refactor, migration, fix) that benefits from
  an independent reviewer and may need several review-and-fix rounds.
- Security-sensitive or production-critical changes — run with strict-approve.
- The user says "clodex", "adversarial review loop", "review until it approves",
  or "have an independent reviewer tear this apart and fix it".

## When NOT to Use

- Trivial or mechanical changes (formatting, copy, dependency bump) where an
  independent review round adds no signal.
- Changes with no verifiable build/test surface — establish that first.
- Pure research/optimization of a scoreable artifact — use
  [champion-challenger-loop](../champion-challenger-loop/SKILL.md).

## Parameters to define BEFORE starting

```yaml
task:            <what to build, in one or two sentences>
thinking:        <reasoning budget role for the builder, e.g. "think hard">
max_iter:        <N>          # hard ceiling on review-and-fix rounds
threshold:       <highest acceptable UNFIXED severity>   # e.g. low | medium | high | critical
strict_approve:  <true for security/prod-critical>       # require explicit reviewer APPROVE
```

`threshold` semantics — it is the highest severity allowed to remain **unfixed**,
so you fix everything **strictly above** it: with `threshold: medium`, you must fix
every `high` and `critical` finding, while `medium` and `low` may remain. With
`strict_approve: true`, "only at-or-below-threshold findings remain" is **not**
enough — the reviewer must explicitly approve.

## The loop

```text
plan(task, thinking)                 # builder: plan the change
implement()                          # builder: make the change
verify()                             # builder: tests/typecheck/lint/security gate
ship_pr()                            # builder: commit, push, open/update PR
iteration = 0
while iteration < max_iter:
    iteration += 1
    findings = independent_review(diff)          # reviewer: separate model family, read-only
    blocking = [f for f in findings if severity(f) > threshold]   # strictly above the ceiling
    if blocking is empty:
        if strict_approve and reviewer_verdict != "APPROVE":
            continue                             # keep going until explicit approve
        return APPROVED(pr, findings, verdict, iteration)
    fix(blocking)                                # builder: address every blocking finding
    verify(); push()                             # re-run gates, update the PR
    persist(plan, branch, pr, findings, verdict, iteration)
# budget exhausted
return NOT_APPROVED(reason="max_iter reached", pr, remaining=blocking, iteration)
```

Stop conditions, in order of precedence:

1. Reviewer **approves** (and, if `strict_approve`, says so explicitly) → APPROVED.
2. Only **at-or-below-threshold** findings remain and `strict_approve` is false → APPROVED.
3. **max_iter** reached → NOT_APPROVED (report remaining findings).
4. Reviewer errored or the run stalled → NOT_APPROVED (report the error/stall).

Cases 3 and 4 are never reported as approved.

## The independent reviewer

Resolve the reviewer by **role**, not a fixed slug (per `orchestration-kernel` §1):

- Role: `critic/auditor` — a capable model from a **different family than the
  builder**. For general code review this is a **Codex-class** model; for
  security/prod-critical changes prefer the strict, security-tuned path.
- The reviewer is **read-only** on the change under review (it inspects the diff,
  it does not author the fix). This is what keeps the review adversarial.

Delegate the actual review to our existing reviewer primitives rather than
hand-rolling one — see [reference.md](reference.md) for the exact subagent wiring
(`review-bugbot`, `review-security`, and the read-only `auditor`/`validator`
subagents), and use [babysit](../babysit/SKILL.md) to keep the PR green across
rounds (CI, conflicts, comment triage).

## Persisted state (resumable)

Persist after every round so the loop resumes safely (see evidence-bundle shape in
`orchestration-kernel` §3):

```yaml
task: <...>
branch: <name>
pr: <url|number>
plan_path: <path>
iteration: <k>
threshold: <...>
strict_approve: <bool>
findings: [ { id, severity, file, line, summary, status: open|fixed|wontfix-subthreshold } ]
verdict: <APPROVE | CHANGES_REQUESTED | ERROR | null>
checks: [ { command, exit_code } ]
```

On resume: re-read this state, re-run the reviewer on the current diff (findings
can change as code changes), and continue from `iteration`. Do not trust a stale
`verdict` — re-verify against the current diff.

## Completion contract

Report done only with:

- Final `verdict` (APPROVED or NOT_APPROVED + reason), never inferred.
- The PR link, the resolved reviewer role/identity, and `iteration` used.
- Every finding listed with final status; any `wontfix-subthreshold` justified
  against the threshold.
- Passing local gate evidence (`./scripts/wterm-preflight.sh --mode pre-push` in
  this repo; the repo-equivalent elsewhere) with exit codes.
- For `strict_approve` runs: explicit reviewer approval, not just "no blockers".

## Hard-stop conditions

```yaml
stop_if:
  reviewer_unavailable: true            # cannot get an independent review
  reviewer_same_family_as_builder: true # not actually independent
  threshold_or_max_iter_undefined: true
  pr_gate_red_after_fix: true           # fixes did not restore green
  asked_to_report_exhausted_as_approved: true   # refuse
```

Hard-stop shape: `stop_reason`, `loop: adversarial-review`, `attempt`,
`failed_checks[]`, `evidence_paths[]`, `next_action` (per `orchestration-kernel` §5).

## Additional resources

- Reviewer subagent wiring, severity mapping, per-repo gates: [reference.md](reference.md)
- Shared contracts (model roles, evidence bundle, hard-stop): [orchestration-kernel](../orchestration-kernel/SKILL.md)
- PR keep-green companion: [babysit](../babysit/SKILL.md)
- Reviewer primitives: [review-bugbot](../review-bugbot/SKILL.md), [review-security](../review-security/SKILL.md)
- Build/verify spines: [project-orchestrator](../project-orchestrator/SKILL.md), [autonomous-verifier](../autonomous-verifier/SKILL.md)
