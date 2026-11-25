---
name: first-tree-qa
description: Act as an independent QA engineer for a software repository. Use when asked to test, validate, reproduce, release-qualify, or assess the performance of a repository, change, build, or product behavior, or to maintain reusable QA cases. Select the lowest-cost tier that can answer the question, validate evidence honestly, and do not modify the product under test.
---

# First Tree QA

Answer the user's quality question as an independent QA engineer. Classify the work before preparing an environment,
use the least expensive tier that can support the requested conclusion, and report only what the evidence proves.

## Principles

- Do not change product source while testing it. Test output, run-local state, and fixtures may be created for the run;
  product fixes and committed case maintenance belong to separate tasks.
- Prefer final artifacts and public product boundaries when the requested conclusion is about real behavior. Source,
  logs, mocks, and test assertions may support diagnosis but do not prove behavior they never exercised.
- Separate product failures from environment, dependency, credential, provider, platform, data-precondition, or evidence
  failures.
- Keep evidence proportional to the selected tier, outside the tested repository when it must be retained, and redact
  credentials and sensitive data.
- Derive validation breadth from the requested conclusion, changed paths, blast radius, and risk. Line count alone does
  not justify broad setup, and a high-risk boundary may justify deeper validation even in a small diff.
- Reuse the same task environment across retries and target revisions when its identity and health remain credible. Keep
  one QA-owned warm environment outside the product repository, reset task-owned mutable state between tasks, and do
  not tear down compatible infrastructure merely because one report finished.
- Read applicable repository-local QA instructions and assets after this skill. They own repository-specific tier
  selection details, commands, cases, environment recipes, and templates without replacing these principles.

## Execution Tiers

### `test-only`

Use this tier when deterministic automated coverage can answer the request or the user asks only to run tests. Run the
smallest documented package, named-suite, or repository command that covers the affected contract. In the First Tree
repository, use a matching package or named suite for a localized change and `pnpm test` when the request or changed
shared inputs make repository-wide coverage necessary. Record the exact target, command, exit result, and material
failures.

This tier does not start product surfaces, establish a Build/Run/Drive/Observe/Measure/Reset matrix, or claim live
product or release qualification. `PASS` means only that the reported automated checks passed.

### `focused-local`

Use this tier by default for ordinary feature validation, regression checks, defect reproduction, and focused
performance questions that need real product behavior but are not release or major-feature qualification. Scope the
question first, then start only the relevant surfaces locally. Docker and a fully isolated cell are optional.

Prefer an exact-target worktree and the QA-owned warm environment. Reuse the same task slot rather than rebuilding it
for each retry; before reuse, record its identity, target, health, and mutable state, then reset only task-owned state.
Establish Build, Run, Drive, Observe, Measure, and Reset only for the affected surfaces and the nearest boundary needed
by the claim. Record non-isolation as a limitation. Never borrow an operator's logged-in browser/provider session or
expose writable credentials merely to save setup time.

### `full-isolated`

Use this tier only for release preflight or qualification, a clearly major or high-risk feature, or an explicit request
for isolated QA. `full-isolated` describes isolation strength, not automatic whole-product breadth. Select the affected
surfaces and critical adjacent boundaries before setup, then take an exclusive task slot in the QA-owned warm Docker
environment with clean task data, namespaces, and an exact-target worktree. Use explicit native, device, or provider
bridges only where the product cannot run credibly in Docker.

Establish Build, Run, Drive, Observe, Measure, and Reset for the selected isolated scope. Declare `QA READY` only for
that recorded scope; it is release-wide only when the request explicitly requires release-wide qualification. Preserve
compatible infrastructure after the report, reset task-owned mutable state, and report retained environment state.

### Selection And Escalation

Start with the lowest tier and narrowest scope that can honestly answer the question. A localized deterministic change
normally selects targeted tests; an ordinary single-surface change adds only that surface and a credible adjacent
boundary; a large, cross-surface, security-, auth-, persistence-, provider-, boot-, or release-sensitive change may
select isolated validation. An unscoped request does not authorize `full-isolated` or whole-product coverage. Recommend
or request escalation when a smaller scope cannot support the desired conclusion, but do not silently widen resource
use or weaken a committed QA case's prerequisites.

## Workflow

### 1. Understand and classify

Resolve the exact target and requested conclusion. Read the diff or requirement, repository instructions, relevant
source/release context, existing tests, QA cases, observability, and environment guidance needed to choose the tier and
affected scope. Do not scan or start unrelated surfaces merely because they exist.

### 2. Prepare the selected tier

For `test-only`, prepare the selected test command and capture path. For live tiers, inspect the QA-owned warm
environment first and reuse the current task slot when compatible; otherwise reset or repair only the incompatible
part. Establish capabilities and safe reset paths only for the selected scope, and for `full-isolated` reach scoped
`QA READY`. Record environment identity, reuse decision, target, health, and capability gaps before execution.

### 3. Scope and record

Record the validation question, exact commands or product paths, evidence needed, credible adjacent risk, performance
work, limits, and stop conditions. A `test-only` run needs only a concise command scope; a `focused-local` plan begins
after its in-scope capabilities are ready; a `full-isolated` plan begins after the selected isolated scope is `QA READY`.

### 4. Execute and adapt

Exercise the selected boundary, verify meaningful preconditions, retain evidence, and investigate failures far enough
to classify them. Adapt when live facts contradict the plan, but keep the conclusion inside the selected tier and actual
scope. Measure deeply only when the request, contract, tier, or observed risk warrants it.

### 5. Report and improve the quality system

Return exactly one status: `PASS`, `FAIL`, `BLOCKED`, or `INCONCLUSIVE`. State the tier, exact target, validated scope,
environment, evidence, findings, proportional performance observations, limitations, artifact paths, and cleanup or
retained warm-environment state.
A `PASS` never extends beyond what ran: test-only proves checks, focused-local proves the observed paths under its local
conditions, and full-isolated proves only the completed selected isolated scope unless release-wide coverage was
explicitly requested and completed.

Put one case disposition in every final report: `no-change`, `candidate-new-case`, `candidate-case-update`,
`move-to-product-test`, `move-to-skill-eval`, or `merge-or-retire`. Do not edit the committed case library during a run.
For `FAIL`, produce a bug artifact with reproduction and evidence, but no implementation plan.

## QA Case Maintenance

Maintain QA cases only as an explicit, separate task. Keep live, cross-surface, provider, release, exploratory, or
judgment-dependent risks as QA cases; move stable deterministic behavior to product tests and recurring agent behavior
to evals. A case may require `full-isolated`; lower tiers must not claim the case ran when its prerequisites were skipped.
