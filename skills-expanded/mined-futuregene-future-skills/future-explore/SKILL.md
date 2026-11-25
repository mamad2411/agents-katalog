---
version: 3.5.0
name: future-explore
description: Evidence-driven exploration, method comparison, experimentation, optimization and feasibility assessment when the answer is not yet known. Use for scientific/engineering exploration or explicitly requested multi-worker reflection. Not for routine factual lookup, a code change with known implementation steps, or editing this skill itself.
allowed-tools: Bash(future:*)
category: tools
---

# Future Explore — Explore, Experiment, Verify

Reduce decision-critical uncertainty within the authorized resources. Separate
execution status, delivery acceptance and scientific conclusions; none is a
substitute for the others. Use evidence rather than a larger collection of rules.

## Scope, roles and budget

Clarify the objective, available material, deliverables, acceptance semantics,
permissions, resource limits and irreversible actions. Reuse explicit existing
authorization; ask once about missing or changed decisions, not unchanged fields.

Choose the smallest sufficient mode:

| Mode | Suitable work | Process |
|---|---|---|
| Light | Bounded mechanism review or targeted comparison | Inspect primary evidence and run targeted checks; usually one agent, no mandatory workspace bureaucracy |
| Standard | Uncertain implementation or consequential decision | Method map, exploratory iteration and an agreed verification plan |
| Heavy | Broad frontier or expensive/high-stakes experiments | Branch on consequential assumptions, discriminate between routes, synthesize and independently validate |

Before paid dispatch, agree on model/thinking settings and resource limits. Default
to the current session model, not a hard-coded roster. A preauthorized model pool
may specify roles, switch conditions and sub-budgets; record justified switches
within that authority without repeating approval. User-pinned configurations remain
binding. Request approval for changes outside the authorized pool/scope/budget.

Assign by capability: routine workers handle explicit implementation and bounded
experiments; the supervisor audits decisive evidence and selects methods; a strong
solver handles demonstrated reasoning/modeling/visual bottlenecks when authorized.
First distinguish missing inputs, infrastructure, implementation, measurement,
method and capability failures. Do not upgrade solely after a fixed retry count.
Within its user-authorized role, the supervisor may derive, implement and correct
work, but must preserve its actual contribution and cannot claim to independently
validate its own candidate.

For concurrent work, maintain one resource ledger. For each additive budget unit,
require `C + R + V + N <= B` before dispatch: authorized total B, consumed C,
outstanding reservations R, undispatched verification/delivery reserve V, and new
allocation N. Reserve before starting; settle consumption from R into C once.
A worker's sub-budget is not the whole parent's budget. Stop requests, query
timeouts or lost processes do not release reservations until termination and
unreported costs are checked. Wall-clock deadlines are checked separately along
dependency chains. State estimation uncertainty and actual enforcement limits;
never promise a hard money cap from a prompt or a turn count.

## Method map and anchors

1. Inspect task contracts, assets and existing evidence before choosing a route.
   Distinguish user requirements from supervisor proposals and historical guesses.
2. Identify plausible methods, assumptions, evidence, costs and discriminating
   tests. Never invent method families or citations to reach an arbitrary count.
3. Separate acceptance criteria, measured baselines, theoretical bounds and
   exploration targets. Unknown bounds stay unknown. Revising an exploration
   target does not make an unmet acceptance criterion pass.
4. Build only the necessary evaluation harness. Record input/submitted/runtime
   semantics, isolation, permissions, versions and unknown interpretations. Test
   both expected-pass and expected-fail cases; report extra robustness conditions
   separately from formal acceptance. Revalidate affected candidates after changes.

For literature-dependent method research, delegate through `future-deep-research`:
use `entry=delegated`, normally `deliverable=methods`, or `delta` for a specific gap
in identified prior work. Preserve `report` when a full report is requested. Inherit
approved depth and sub-allocation, verify key claims and reuse adequate evidence.
These are handoff fields, not invented CLI flags. Check the installed dependency's
actual contract. Repository code/specs may themselves suffice for a light software
investigation; do not require ceremonial web research. Authorized asset checks,
environment smoke tests and cheap baselines independent of unresolved methods can
proceed in parallel; method-dependent heavy work still needs an evidential basis.

## Hypothesis-led branching

Parallel implementation is not independent exploration. Splitting theory, data,
optimization and sampling among workers can propagate one untested assumption to
all outputs. Different agents, models or libraries alone do not establish distinct
routes. When the user requests multi-direction exploration, branch on consequential
assumptions or methods, not merely on deliverable components.

Before committing substantial method-dependent work, identify the assumptions
whose failure could invalidate acceptance. Prioritize by consequence, uncertainty
and cost of the cheapest discriminating check. Record compactly in the existing
method map, not a new bureaucracy:

- The assumption, affected requirement and current evidence or uncertainty.
- A credible alternative or independent challenge, and a check that could separate
  the explanations. State what result would change the method or allocation.
- An owner, shared dependencies, bounded cost/checkpoint and downstream work that
  depends on the assumption. Label an untested default as provisional.

Choose the smallest useful set of branches. A baseline plus a targeted challenge
may be enough; one worker can compare variants for a light task. If alternatives
are unclear, ask for independent assumption critiques before converging on a shared
implementation. Do not invent alternatives, require a fixed branch count or launch
extra workers simply to look diverse. Explain when no worthwhile fork is available.
Implementation-only splits are useful, but describe them as such, not corroboration.

Branch briefs must say what is being challenged, what may be shared, and which
independent evidence is needed. Give challengers the task contract and permitted
primary inputs, not the baseline's assumptions as settled facts. Cross-branch
agreement counts only within the dependencies actually tested: two validators
using the same theory may verify algebra but not the theory. Numerical refinement
inside a fixed approximation does not validate that approximation's adequacy.

Run cheap, high-impact challenges early, before expensive downstream tuning or
sampling. Preserve a working baseline and allow independent preparation to proceed;
do not serialize unrelated work. Method-dependent results remain conditional until
their critical assumptions have adequate evidence. Early collaborators who help
tune the candidate do not thereby become its independent final reviewers.

## Evidence-driven supervision and correction

Before declaring data inaccessible, an interface broken, a worker wrong, a route
exhausted, or a task complete, inspect the decisive original evidence. Record in
the existing report: observed fact, candidate explanation, counterevidence,
cheapest discriminating check and resulting decision. Do this for consequential
decisions, not every trivial action. Missing fields or a transient error do not
establish a permanent failure; several simultaneous changes do not isolate one
cause of improvement.

Bind key evidence to its task, run/session or external receipt ID, observation
and retrieval time, input/candidate/validator versions and original record path.
Read IDs from actual records, not latest file mtime. A report is an evidence index;
execution logs prove execution, not scientific truth. Do not use another task's
old log to explain the current outcome or silently rank incomparable measurements.

Treat suggested worker routes as challengeable hypotheses, not axioms. When
counterevidence invalidates a supervisor assumption, preserve the old record,
mark dependent conclusions/rankings/stopping decisions/briefs for review, notify
affected workers and selectively revalidate. Prevent further dependence on invalid
inputs or evaluation without restarting unrelated work. Keep unaffected baselines.
Conflicts stay unresolved until evidence discriminates; majority agreement among
workers sharing one implementation is not independent corroboration. None of this
authorizes changing user constraints or accessing prohibited answers/test data.

An unresolved acceptance-critical risk also requires a decision; do not wait for a
proven defect before investigating. At a checkpoint, connect new evidence to a
concrete action: retain a supported assumption, schedule the next discriminating
check, redirect affected work, or pause it with a stated reason. When a useful check
fits the remaining authorized budget, assign its owner, artifact and time allowance
while preserving final-review resources. If deferred, state what remains conditional
and why; listing a risk in a report is not resolving it. A partial test at one point
or range cannot clear a requirement over an untested domain.

## Explore, hand off and resume

For durable/multi-worker work, load `future-goal`, inspect existing goals, use
owner-scoped tasks and isolated output directories, and name relevant artifact
paths and versions in downstream briefs. Do not feed every worker the entire
cross-task ledger. At each checkpoint ask what new evidence changed the decision,
which hypotheses were weakened, what remains uncertain, and which next action is
worth its authorized cost. Read results, not just activity counters or summaries.

Put a concise receipt FIRST in each REPORT and repeat its pointer at handoff:

- Actual task/run/session identity and input/candidate version (unknown stays unknown).
- Result: what was supported, refuted or unresolved, and whether measured or inferred.
- Exact artifact paths, reproduction entry and original evidence references.
- Verification performed, validator version, failures and unverified conditions.
- External receipt ID, retrieval time and pending/final status, when applicable.
- Invalidated assumptions, affected dependencies, requested decisions and next action.
- Consumed/estimated resources, outstanding jobs and recovery conditions.

Follow with the detailed method, reasoning, negative results and limitations.
A truncated completion notification is a prompt to read the report, not permission
to guess an outcome. Verify relevant artifacts/receipts BEFORE recording verified.
One worker's completion or a `last todo` label never establishes global closure.

Each asynchronous experiment names a monitor owner, job/receipt ID, result endpoint,
next check, timeout handling, supported wakeup mechanism and reserved monitoring
budget. Read existing receipts; never resubmit an irreversible action just to find
its ID. The goal watchdog handles goal liveness/outbox, not arbitrary external
scores or resource allocation. If no persistent monitoring exists, disclose that
rather than promising automatic follow-up. On new results or unblocking events,
reassess within valid authorization; ask only for expired or changed permissions.
Avoid paid sleep/poll loops and gratuitous interrupts. A live process, tool usage
and changed files are activity signals, not evidence of scientific advancement.

## Verification and honest stopping

Agree on verification level, reviewer capability/independence and its allocation
before relevant exploration. Low-risk work may explicitly use self-checks; if
independent final review is promised, reserve and assign it before resources run
out. A reviewer who helped implement/tune/improve the candidate is not its
independent final reviewer merely because a new session/model is used. Disclose
shared dependencies and protect held-out data. Do not silently downgrade review.

Test the exact delivery version and the interpretation of its results, not just a
shared harness. Use alternative implementations, adversarial cases or randomized
tests according to risk, not a universal million-case quota. Zero observed failures
is not a proof. Do not overwrite a verified baseline with an unverified candidate.

Report three independent dimensions:

| Dimension | Report |
|---|---|
| Execution | Running/ended/paused, with the actual reason: completed work, budget, user stop, blocked input, no next idea or evidence-based low return |
| Acceptance | Met/partial/unmet/pending, with requirement-level evidence and actual verification level |
| Research conclusion | Result and scope: feasible, bounded infeasible, uncertain, conditional explanation or performance estimate |

A valid negative feasibility assessment can meet the user's acceptance contract.
Budget exhaustion or an empty idea queue is not a proof of global infeasibility.
When recommending low-return stopping with budget left, identify plausible untried
actions, what they could distinguish, cost/prerequisites and why not to pursue them.
If there is no next idea, say so; do not invent a proof or busywork. Completion of
the initial worker roster is not itself a stopping criterion or budget exhaustion.
Reallocate to useful unresolved checks within still-valid authorization rather than
requesting permission merely because an initial assignment ended. Respect explicit
worker/attempt limits and the resource ledger; never silently expand or relabel a
budget. Preserve useful partial artifacts, settle outstanding work and ask before
extending authorized resources.

Never fabricate execution, citations, cost, provenance or reviewer independence.
Record collaboration honestly and apply task-specific answer isolation. Changing
labels, acceptance thresholds or a progress file cannot manufacture success.
