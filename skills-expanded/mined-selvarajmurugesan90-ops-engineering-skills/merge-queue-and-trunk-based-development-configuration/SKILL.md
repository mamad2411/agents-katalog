---
name: merge-queue-and-trunk-based-development-configuration
description: >
  Configures automated merge serialization — GitHub merge queue or a
  Mergify-style bot — and the trunk-based development discipline (short-
  lived branches, small PRs, feature flags over long-lived branches) it
  depends on, including how to avoid merge-train pileup. Use when a user
  asks to "set up a merge queue," "configure Mergify," "adopt trunk-based
  development," "our merge queue keeps stalling/piling up," "batch PRs
  before merging to main," or "avoid re-running CI on every rebase before
  merge."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Merge Queue and Trunk-Based Development Configuration

## Purpose

As a team's merge rate to a protected branch grows, a naive "require CI to
pass, then merge" workflow breaks down in a specific way: PR A and PR B
both pass CI independently against `main`, but merging A first can make B's
already-green CI result stale — B was tested against a `main` that no
longer reflects reality the moment A lands, so B can merge a change that
was never actually tested against the code it's landing on top of. A
**merge queue** (GitHub's native merge queue, or a bot like Mergify)
automates the fix: it serializes merges, re-testing each PR against the
*current* `main` (which may include changes from other PRs merged
moments earlier) immediately before it actually merges, batching several
queued PRs into one combined CI run where supported to avoid re-running a
full suite once per PR. This only works well, though, on top of **trunk-
based development** — short-lived branches, small PRs, and feature flags
used to hide incomplete work instead of long-lived feature branches — 
because a merge queue serializing a handful of large, long-lived,
merge-conflict-prone branches just moves the pileup problem from "which PR
merges first" to "the merge queue itself is now a bottleneck." This skill
covers configuring both pieces together: the merge queue mechanics and the
branching discipline that keeps it from becoming its own chokepoint.

## When to use

- A team's merge-to-`main` rate is high enough that "PR passed CI, but
  broke `main` after merging because another PR landed first" incidents
  are recurring.
- Setting up GitHub's native merge queue or a Mergify configuration for
  automated, serialized merging with re-validation against current `main`.
- A configured merge queue is stalling, piling up, or taking longer than
  expected to drain, and needs tuning (batch size, required checks, timeout
  handling).
- Adopting or reinforcing trunk-based development — moving a team off
  long-lived feature branches and toward small, frequent, flag-gated merges
  to `main`.
- Diagnosing why CI re-runs so often before a PR actually merges (e.g. a
  required "up to date with base branch" setting causing repeated
  re-triggers on every push to `main`).
- Deciding whether a merge queue is worth the added mechanism for a
  low-merge-volume team, versus simple branch protection with required
  status checks alone.

## Prerequisites & environment

- A CI pipeline with fast, reliable required status checks already in
  place — a merge queue amplifies, rather than fixes, a slow or flaky
  pipeline, since every queued PR gets re-validated through the same
  checks (see
  [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md) for pipeline
  speed/reliability fundamentals this depends on).
- For GitHub's native merge queue: a GitHub repository with branch
  protection enabled and at least one required status check configured;
  GitHub merge queue is available on GitHub Team/Enterprise plans for
  private repos (public repos on any plan) — confirm current plan
  eligibility before assuming availability.
- For Mergify: a Mergify GitHub App (or GitLab equivalent) installed on the
  repository/organization, plus a `.mergify.yml` configuration file
  committed to the repo.
- A feature-flag mechanism (a config-driven flag service, or even a simple
  environment-variable/config toggle for smaller teams) if adopting trunk-
  based development for work that can't be finished and merged within a
  single short-lived branch's lifetime — without this, trunk-based
  development pressures people into either merging incomplete work behind
  no flag (risky) or reverting to long-lived branches (the problem this
  discipline solves).
- Team agreement on a target PR/branch lifetime (commonly cited target:
  hours to a couple of days, not weeks) — the merge queue mechanics below
  assume this discipline is either already in place or being adopted
  alongside the tooling change.

## Step-by-step guidance

1. **Enable GitHub's native merge queue on the protected branch**, requiring
   PRs to enter the queue instead of merging directly once checks pass:
   ```
   Settings → Branches → Branch protection rule for "main"
     ✅ Require a pull request before merging
     ✅ Require status checks to pass before merging
         Required checks: build, test, lint
     ✅ Require merge queue
         Merge method: squash (recommended for trunk-based history clarity)
         Build concurrency: 5           # how many queue entries run CI in parallel
         Minimum group size: 1, Maximum group size: 5   # batch size per queue run
   ```
   When a PR is added to the queue, GitHub creates a temporary merge
   commit combining it with the current `main` (and, depending on batch
   size, other queued PRs) and runs required checks against *that*
   combination — not against the PR's original, possibly-stale branch
   state.

   > **Warning:** an admin "merge without waiting for requirements"
   > override bypasses both the merge queue and its re-validation against
   > current `main` entirely — this reintroduces the exact stale-CI-result
   > risk the queue exists to prevent. Restrict who can use admin merge
   > overrides on a protected branch with a merge queue enabled, and treat
   > routine use of that override as a process failure to investigate, not
   > a normal escape hatch.

2. **Configure Mergify as an equivalent (or GitHub Enterprise-independent)
   alternative**, with an explicit queue and merge conditions:
   ```yaml
   # .mergify.yml
   queue_rules:
     - name: default
       merge_method: squash
       batch_size: 5
       batch_max_wait_time: 5m
       checks_timeout: 60m

   pull_request_rules:
     - name: automatic merge via queue
       conditions:
         - "check-success=build"
         - "check-success=test"
         - "check-success=lint"
         - "#approved-reviews-by>=1"
         - "label=ready-to-merge"
       actions:
         queue:
           name: default
   ```
   `batch_size`/`batch_max_wait_time` control how many queued PRs Mergify
   groups into one combined validation run before merging the batch —
   larger batches drain the queue faster per CI run but mean a single
   failing PR in the batch can force the whole batch to be re-split and
   re-validated, so tune batch size against your actual CI duration and
   failure rate rather than maximizing it blindly.

3. **Keep required checks minimal and fast for the queue's own re-validation
   run**, separate from a fuller, slower suite that can run pre-merge on
   the original PR but doesn't need to re-run for every queue batch —
   mirrors the "keep fast checks first" staging guidance in
   [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md), applied
   specifically to what blocks queue throughput.

4. **Adopt short-lived branches as the actual prerequisite for a healthy
   queue** — a merge queue processing a handful of branches that have each
   been open for two weeks accumulates merge conflicts and large diffs that
   are slow to re-validate and prone to failing the queue's re-run. Target
   branch lifetimes of hours to a day or two:
   ```
   Team convention (documented, not just aspirational):
     - Branch from main, scope the PR to one reviewable change.
     - Open the PR within a day of starting work, even in draft.
     - Merge within 1-2 days; if the underlying task is bigger,
       split it into multiple merges behind a feature flag.
   ```

5. **Use feature flags to merge incomplete work safely**, rather than
   keeping a branch open until the feature is "done":
   ```python
   if feature_flags.is_enabled("new_checkout_flow", user=current_user):
       return new_checkout_handler(request)
   return legacy_checkout_handler(request)
   ```
   This is what makes small, frequent merges to `main` compatible with
   multi-week features — the code merges continuously and stays inert in
   production until the flag flips, decoupling "merged" from "released"
   the same way
   [blue-green-canary-deployments](../blue-green-canary-deployments/SKILL.md)
   decouples "deployed" from "serving live traffic."

6. **Set the merge queue's required "up to date with base" behavior
   correctly** — most merge-queue implementations handle re-validation
   against current `main` automatically as part of queue processing, so a
   separate branch-protection rule requiring the PR branch itself to be
   manually rebased/updated before merging is usually redundant with (and
   can conflict with) the queue's own mechanics; disable a manual
   "require branches to be up to date" rule once the merge queue is
   handling that re-validation itself, to avoid forcing redundant
   CI re-runs on every push to `main`.

7. **Monitor queue depth and drain time as an operational metric**, not just
   individual PR CI duration — a queue that's technically "working" but
   taking 45 minutes to drain under normal load is a throughput problem the
   same way a slow pipeline is, and should be tracked alongside pipeline
   duration metrics per
   [devops-delivery-metrics-and-dora-analysis](../devops-delivery-metrics-and-dora-analysis/SKILL.md).

8. **Set a queue timeout and a clear failure path** for a PR that fails
   validation inside the queue, so a failing PR doesn't block every PR
   behind it indefinitely:
   ```yaml
   # Mergify: checks_timeout caps how long a queued PR can occupy a slot
   queue_rules:
     - name: default
       checks_timeout: 60m
   ```
   A PR that times out or fails should be automatically removed from the
   queue (both GitHub's merge queue and Mergify do this by default) and the
   next queued PR re-validated without it, rather than the whole queue
   stalling on one bad entry.

## Best practices

- Keep required checks for merge-queue re-validation to the fast,
  high-signal set (build, unit tests, lint); route slow integration/e2e
  suites to run pre-merge on the original PR (or post-merge, non-blocking)
  rather than re-running them on every queue batch — this keeps queue
  drain time low.
- Enforce small PRs as a real team norm (a rough size guideline, code
  review culture, or a bot comment flagging oversized diffs), not just an
  aspiration — a merge queue's benefits degrade quickly once branches carry
  large, conflict-prone diffs.
- Prefer squash-merge for a clean, linear `main` history when using a merge
  queue — it keeps the trunk's commit history readable and avoids
  merge-commit noise from queue batching mechanics.
- Use feature flags (not long-lived branches) as the default answer to
  "this feature isn't finished yet" — this is the actual enabling practice
  behind trunk-based development, and skipping it is the most common
  reason a team's "trunk-based" workflow quietly reverts to long-lived
  branches under deadline pressure.
- Tune batch size empirically against your CI suite's duration and typical
  PR failure rate — a batch size that's too large means one bad PR forces
  re-validation of several good ones; too small loses the throughput
  benefit of batching entirely.
- Track queue depth/drain time as a first-class delivery metric alongside
  deploy frequency and lead time, per
  [devops-delivery-metrics-and-dora-analysis](../devops-delivery-metrics-and-dora-analysis/SKILL.md)
  — a stalling queue is a delivery-speed regression even if every
  individual PR's CI still passes.

## Common pitfalls

- **Symptom:** A PR passes CI on its own branch, merges, and breaks `main`
  because another PR merged moments earlier changed something it depended
  on — the exact "stale CI result" scenario a merge queue is meant to
  prevent.
  **Fix:** This means merges are still happening directly rather than
  through the queue (or the queue isn't actually re-validating against
  current `main`) — confirm `Require merge queue` is enabled and enforced
  on the branch protection rule (not just configured but optional), and
  that no bypass path (an admin merge override) is being used routinely to
  skip it.

- **Symptom:** The merge queue "pileup" — queue depth grows faster than it
  drains, and PRs sit queued for tens of minutes to hours during busy
  periods.
  **Fix:** Increase build concurrency/batch size if CI capacity allows, cut
  the set of required checks to the fastest high-signal subset, and check
  whether a small number of large, frequently-failing PRs are repeatedly
  forcing batch re-splits — those are usually the actual root cause, not
  queue configuration alone.

- **Symptom:** A single PR with a flaky test keeps failing inside the
  queue, forcing repeated re-validation of the PRs batched behind it and
  stalling the whole queue.
  **Fix:** Remove the flaky PR from the queue (most implementations do this
  automatically on a `checks_timeout` or repeated failure) and fix the
  flaky test at its root per the flaky-test guidance in
  [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md) — don't let a
  known-flaky check remain in the queue's required-checks list, since it
  will keep recreating this pileup.

- **Symptom:** A team adopts a merge queue but branches still commonly stay
  open for a week or more, and queue drain time doesn't improve despite the
  new tooling.
  **Fix:** The tooling isn't the bottleneck — long-lived, large-diff
  branches are inherently slower to validate and more prone to conflicts
  regardless of queue mechanics. Address the trunk-based development gap
  directly (smaller PRs, feature flags for incomplete work, a documented
  target branch lifetime) rather than expecting the merge queue alone to
  fix a branching-discipline problem.

- **Symptom:** CI re-runs on a PR every time `main` receives an unrelated
  merge, even though the PR hasn't been touched, well before it ever
  reaches the queue.
  **Fix:** Check for a redundant "require branches to be up to date before
  merging" branch-protection setting running independently of the merge
  queue's own re-validation — the queue already re-tests against current
  `main` at merge time, so a separate manual "must be up to date" rule
  forcing rebases on every unrelated push to `main` is usually redundant
  and should be disabled once the queue is handling that concern.

## Worked example

**Scenario:** A team of 25 engineers merging ~40 PRs/day to `main` is
seeing 2-3 "green PR broke main after merge" incidents a week, and separately
has several feature branches open for 2+ weeks. They adopt GitHub's merge
queue and formalize trunk-based development norms together.

Branch protection on `main`:
```
Require a pull request before merging: ✅
Require status checks to pass: ✅ (build, unit-test, lint — the fast set only)
Require merge queue: ✅
  Merge method: squash
  Build concurrency: 4
  Group size: 1–4
Require branches to be up to date before merging: ❌ (disabled — redundant
  with the queue's own re-validation against current main)
```

Slower integration/e2e suite moved to run on the original PR (required for
review approval) but explicitly excluded from the merge queue's own
required-checks list, keeping queue re-validation fast.

Trunk-based development norms documented and adopted:
```
- Target branch lifetime: under 2 days.
- PRs over ~400 changed lines get flagged by a bot comment suggesting a split.
- Multi-week features ship incrementally behind a feature flag
  (feature_flags.is_enabled("...")), merged to main continuously rather
  than developed on one long-lived branch.
```

Result after one month: queue drain time stays under 10 minutes at typical
load (tracked alongside existing DORA metrics per
[devops-delivery-metrics-and-dora-analysis](../devops-delivery-metrics-and-dora-analysis/SKILL.md)),
"green PR broke main" incidents drop to zero (every merge is now
re-validated against current `main` immediately before landing), and the
previously-common 2-week-old feature branch is retired as a pattern in
favor of flag-gated incremental merges.

## Cross-references

- [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md) — the pipeline speed/reliability and required-status-check fundamentals a merge queue depends on and amplifies; read this first if CI itself is slow or flaky before adding queue tooling on top.
- [blue-green-canary-deployments](../blue-green-canary-deployments/SKILL.md) — the deploy-side analogue of decoupling "merged" from "released," using feature flags and progressive rollout the same way trunk-based development decouples "merged" from "finished."
- [devops-delivery-metrics-and-dora-analysis](../devops-delivery-metrics-and-dora-analysis/SKILL.md) — tracking queue depth/drain time and merge frequency as delivery metrics alongside deploy frequency and lead time.
- [gitops-workflow](../gitops-workflow/SKILL.md) — a related git-driven-automation pattern for deployment reconciliation, distinct from but philosophically aligned with automating merge serialization here.
