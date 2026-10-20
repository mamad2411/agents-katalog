---
name: temporal-configuration-validation
description: >
  Validates Temporal worker task queue configuration, activity
  timeout/retry policy settings, and namespace configuration (retention,
  visibility archival) before a workflow goes to production. Use when the
  user asks to "review this Temporal worker config before deploy," "check
  our activity timeout/retry settings," "validate a Temporal namespace
  before go-live," "why are workflows stuck with no worker picking them
  up," or is preparing a Temporal-based service for a production
  readiness review.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# Temporal Configuration Validation

## Purpose

A Temporal workflow can be authored correctly — deterministic, with
sensible activities and compensation logic as covered in
[temporal-durable-workflow-orchestration](../temporal-durable-workflow-orchestration/SKILL.md)
— and still fail in production because of configuration sitting outside
the workflow code itself: a worker polling the wrong (or no) task queue,
an activity timeout too tight for its real-world latency distribution, a
retry policy that never gives up on a permanently failing call, or a
namespace whose retention period silently discards the event history an
operator needed to debug an incident. These are the kind of mistakes
that pass every unit test against a mocked activity and only surface
under real production load or after the first workflow needs
investigating weeks later. This skill covers validating exactly that
configuration surface — task queues, timeouts/retries, and namespace
settings — before a Temporal-backed service goes live, as a
complement to (not a replacement for) the workflow/activity authoring
guidance in
[temporal-durable-workflow-orchestration](../temporal-durable-workflow-orchestration/SKILL.md).

## When to use

- Reviewing a Temporal-based service before a production launch or a
  significant workflow change, specifically for task queue, timeout,
  retry, and namespace configuration correctness.
- Diagnosing workflows or activities that appear "stuck" with no
  progress and no obvious error.
- Auditing activity timeout and retry policy settings across a codebase
  for values that are either dangerously loose (retrying forever) or
  dangerously tight (failing fast on normal latency variance).
- Setting up a new Temporal namespace and deciding retention,
  archival, and multi-tenancy boundaries before workflows start
  running in it.
- Adding a CI check that catches a missing timeout, an unset retry
  policy, or a task queue name mismatch before merge, rather than
  relying on someone noticing in a staging environment.

## Prerequisites & environment

- Access to the Temporal Server's admin/operator surface — the
  `temporal` CLI (v2, the current `temporal` binary, not the older
  deprecated `tctl`) configured against the target namespace, or
  equivalent SDK-based admin calls.
- The worker fleet's actual startup configuration (task queue names,
  concurrent execution limits, build ID/versioning settings) available
  for review — pulled from the deployment manifests/Helm values, not
  just source code defaults, since the two can drift.
- Familiarity with the workflow/activity code being validated (or the
  ability to grep it) to cross-check declared timeouts/retry policies
  against what
  [temporal-durable-workflow-orchestration](../temporal-durable-workflow-orchestration/SKILL.md)
  recommends per activity.
- For namespace validation: awareness of the organization's actual
  operational/compliance requirement for how long workflow history must
  remain queryable (debugging an incident from three weeks ago requires
  retention to still cover that window).
- Temporal Server 1.20+ recommended if validating worker versioning /
  Build ID-based safe-deploy features — the exact versioning API
  surface has evolved across releases, so confirm the deployed server
  version's supported versioning mode before relying on a specific flag.

## Step-by-step guidance

1. **Confirm every task queue referenced by workflow/activity code has
   at least one active poller**, and that the name matches exactly
   (case-sensitive, no incidental whitespace) between the
   workflow-starter code, the activity options, and the worker's
   registration:
   ```bash
   temporal task-queue describe \
     --task-queue order-fulfillment-tq \
     --namespace production
   ```
   Zero pollers listed for a task queue that workflows are actively being
   started against is the single most common "workflow is stuck" root
   cause — validate this *before* looking for a code-level bug in the
   workflow itself.

2. **Check for task queue fan-out mistakes** — a common misconfiguration
   is starting a workflow on one task queue while its activities are
   registered (via `ActivityOptions.TaskQueue`, if set) to route to a
   *different* queue that has no workers polling it:
   ```go
   // if an activity's options override TaskQueue, confirm a worker
   // actually polls that specific queue, not just the workflow's queue
   ao := workflow.ActivityOptions{
       TaskQueue:           "order-fulfillment-activities-tq", // separate from the workflow's queue
       StartToCloseTimeout: 30 * time.Second,
   }
   ```
   If activities are deliberately routed to a dedicated queue (e.g. to
   isolate a GPU-bound or third-party-rate-limited activity onto its own
   worker pool), verify a worker is registered specifically for that
   queue — don't assume the workflow's own worker also covers it.

3. **Audit every activity for an explicit timeout appropriate to its
   real latency**, treating a missing or default-only timeout as a
   finding, not an acceptable gap:
   ```go
   // FLAG: no StartToCloseTimeout set — relies entirely on the SDK/
   // server default, which may not match this specific call's real
   // latency profile (e.g. a call to a third-party API with its own
   // multi-second p99).
   ao := workflow.ActivityOptions{}

   // BETTER: explicit timeout sized to the call's actual measured
   // latency distribution, with headroom, not a copy-pasted default.
   ao := workflow.ActivityOptions{
       StartToCloseTimeout: 20 * time.Second, // p99 of the downstream call is ~8s
       ScheduleToCloseTimeout: 5 * time.Minute, // total budget across retries
   }
   ```
   Distinguish `StartToCloseTimeout` (one execution attempt) from
   `ScheduleToCloseTimeout` (the whole activity's total time budget
   including all retries and queueing) — an activity with a generous
   per-attempt timeout but no `ScheduleToCloseTimeout` can retry for an
   effectively unbounded total duration if `MaximumAttempts` is also
   unset.

4. **Audit every retry policy for a bounded `MaximumAttempts` or a
   sane `MaximumInterval`**, and confirm genuinely non-retryable error
   types are actually listed:
   ```go
   // FLAG: unbounded retries with no non-retryable error classification
   // — a permanently failing call (bad request, auth failure, business
   // rejection) retries indefinitely, burning worker capacity and
   // delaying the workflow's own failure/compensation path.
   RetryPolicy: &temporal.RetryPolicy{
       InitialInterval: time.Second,
       BackoffCoefficient: 2.0,
   }

   // BETTER
   RetryPolicy: &temporal.RetryPolicy{
       InitialInterval:        time.Second,
       BackoffCoefficient:     2.0,
       MaximumInterval:        time.Minute,
       MaximumAttempts:        5,
       NonRetryableErrorTypes: []string{"InvalidOrderError", "CardDeclinedError"},
   }
   ```
   Cross-check the `NonRetryableErrorTypes` list against the actual
   error types the activity can return — an error type added to the
   activity's code later but never added to this list silently starts
   retrying an error that was meant to fail fast.

5. **Validate heartbeat timeout is present for any activity expected to
   run longer than a few seconds**, and that it's shorter than
   `StartToCloseTimeout`:
   ```go
   ao := workflow.ActivityOptions{
       StartToCloseTimeout: 10 * time.Minute,
       HeartbeatTimeout:    30 * time.Second, // must be < StartToCloseTimeout
   }
   ```
   An activity with a long `StartToCloseTimeout` and no
   `HeartbeatTimeout` means a genuinely crashed/hung worker isn't
   detected until the full timeout elapses — validate that any
   long-running activity's code actually calls `RecordHeartbeat` at an
   interval shorter than the configured `HeartbeatTimeout`, not just
   that the timeout value exists.

6. **Check the namespace's retention period against the organization's
   actual debugging/compliance window**, before assuming the default is
   sufficient:
   ```bash
   temporal operator namespace describe --namespace production
   ```
   ```bash
   # set/update retention explicitly rather than relying on server defaults
   temporal operator namespace update \
     --namespace production \
     --retention 30d
   ```
   A retention period shorter than how long an operator might reasonably
   need to look back at a workflow's event history (an incident
   investigation, a customer support escalation) means the history is
   already gone by the time someone asks — validate this against a real
   organizational requirement, not the server's out-of-the-box default.

7. **Validate namespace-level multi-tenancy boundaries** — confirm
   distinct environments (staging, production) and, where relevant,
   distinct customer-facing tenants use separate namespaces rather than
   sharing one namespace distinguished only by a naming convention in
   workflow IDs:
   ```bash
   temporal operator namespace create --namespace staging
   temporal operator namespace create --namespace production
   ```
   A shared namespace across environments means a staging load test or a
   buggy staging workflow can consume the same task-queue capacity,
   visibility store, and retention budget as production — validate that
   this separation actually exists rather than assuming it from naming
   alone.

8. **For worker deploys, validate Build ID-based versioning (or
   equivalent safe-deploy configuration) is in place** before assuming a
   rolling worker deploy is safe for in-flight workflows:
   ```bash
   temporal task-queue update-build-ids add-new-default \
     --task-queue order-fulfillment-tq \
     --namespace production \
     --build-id "order-fulfillment-v2.14.0"
   ```
   Confirm new workflow executions pin to the new Build ID while
   existing in-flight executions continue on the Build ID they started
   with (or are explicitly migrated), rather than a bare rolling
   deployment that lets old-code and new-code workers race to pick up
   the same task queue with no compatibility guarantee — this is the
   configuration-level complement to the code-level `GetVersion`
   patching discipline in
   [temporal-durable-workflow-orchestration](../temporal-durable-workflow-orchestration/SKILL.md).

9. **Run a replay test against real production history as a pre-deploy
   CI gate**, not just unit tests against mocked activities — this is
   the single strongest check that a proposed code change won't break
   currently in-flight executions:
   ```bash
   # fetch a sample of real, currently-running workflow histories and
   # replay them against the new worker binary before it's deployed
   temporal workflow show --workflow-id order-fulfillment-ORD-48213 \
     --namespace production --output json > sample_history.json
   ```
   ```go
   // Go SDK replay test
   replayer := worker.NewWorkflowReplayer()
   replayer.RegisterWorkflow(OrderFulfillmentWorkflow)
   err := replayer.ReplayWorkflowHistoryFromJSONFile(nil, "sample_history.json")
   // a non-nil err here means this code change would break replay for
   // any execution whose history looks like this sample
   ```

## Best practices

- Treat "zero pollers on a task queue" as the first thing to check for
  any stuck-workflow report — it's the most common root cause and the
  fastest to rule in or out.
- Require every activity to declare an explicit `StartToCloseTimeout`
  and retry policy in code review — no activity should rely silently on
  SDK/server defaults for either.
- Distinguish and set both `StartToCloseTimeout` (per attempt) and
  `ScheduleToCloseTimeout` (total budget) deliberately, rather than only
  the former, for any activity with retries enabled.
- Keep `NonRetryableErrorTypes` lists in sync with the activity's actual
  error types as part of code review — an out-of-date list is a silent
  correctness regression, not a cosmetic gap.
- Set namespace retention from an explicit organizational requirement
  (compliance, typical incident-investigation lookback), and document
  the reasoning next to the `temporal operator namespace update` command
  that set it.
- Run replay tests against sampled real production history in CI before
  any worker deploy that touches workflow code — this catches
  non-determinism that unit tests against mocks structurally cannot.
- Use Build ID-based worker versioning for any workflow type expected to
  have long-running in-flight executions across a deploy, rather than a
  bare rolling deployment.

## Common pitfalls

- **Symptom:** Workflows start successfully (visible via `temporal
  workflow list`) but never progress past their first activity, with no
  error surfaced anywhere.
  **Fix:** Run `temporal task-queue describe --task-queue <queue>` and
  check the poller count — zero pollers means no worker is actually
  processing this queue's tasks, most often from a worker deployment
  pointed at the wrong task queue name or a worker that crashed on
  startup without anyone noticing. Confirm the exact task queue string
  matches between workflow start options, activity options, and worker
  registration.

- **Symptom:** An activity that calls a flaky third-party API retries
  for hours, and the workflow the on-call team actually cares about
  never reaches its failure/compensation path.
  **Fix:** No `MaximumAttempts` or `ScheduleToCloseTimeout` bounds the
  retry policy's total duration. Add an explicit bound (step 3-4) so the
  activity fails and hands control back to the workflow's own
  compensation logic within a reasonable, known time budget instead of
  retrying indefinitely.

- **Symptom:** A workflow's activity is repeatedly killed and retried
  even though the downstream call it's waiting on is still making real
  progress (e.g. a large file upload).
  **Fix:** `HeartbeatTimeout` is unset, or the activity code never calls
  `RecordHeartbeat`, so Temporal has no signal to distinguish "the
  worker died" from "this is just slow." Add heartbeating inside the
  activity at an interval comfortably shorter than the configured
  `HeartbeatTimeout` (step 5).

- **Symptom:** An operator investigating an incident from a month ago
  finds the relevant workflow's event history is simply gone.
  **Fix:** The namespace's retention period is shorter than the
  organization's actual investigation/compliance window. Check
  `temporal operator namespace describe` and set retention (step 6)
  from an explicit, agreed requirement rather than the server's default.

- **Symptom:** After a worker deploy that changed workflow code, a batch
  of in-flight executions all fail simultaneously with nondeterminism
  errors.
  **Fix:** The deploy wasn't validated with a replay test against real
  in-flight history first (step 9), and/or Build ID versioning (step 8)
  wasn't used to separate old and new code paths. Add a replay-test CI
  gate using sampled production histories before merging any workflow
  code change, and use Build ID-based worker versioning for any
  workflow type with meaningful in-flight volume across deploys.

## Worked example

**Scenario:** Pre-production readiness review for the
`order-fulfillment` workflow from
[temporal-durable-workflow-orchestration](../temporal-durable-workflow-orchestration/SKILL.md)
before it goes live for real customer orders.

1. Task queue check:
   ```bash
   $ temporal task-queue describe --task-queue order-fulfillment-tq --namespace production
   Pollers: 3 workers, all reporting healthy heartbeats within the last 10s
   ```
   Confirmed against the worker deployment's Helm values, which set
   `TASK_QUEUE=order-fulfillment-tq` matching the workflow-starter code
   exactly.

2. Timeout/retry audit of each activity (`ReserveInventory`,
   `ChargePayment`, `ReleaseInventory`, `ShipOrder`) confirms each has an
   explicit `StartToCloseTimeout`, a `MaximumAttempts` bound, and
   `ChargePayment` specifically lists `CardDeclinedError` under
   `NonRetryableErrorTypes` — cross-checked against the payment client
   library's actual exported error types to confirm the name still
   matches after a recent client library upgrade.

3. `ShipOrder` (which can take several minutes waiting on a carrier API)
   has `HeartbeatTimeout: 30s` configured and its implementation is
   confirmed to call `RecordHeartbeat` every 10 seconds while polling
   the carrier's status endpoint.

4. Namespace retention:
   ```bash
   $ temporal operator namespace describe --namespace production
   Retention: 30d
   ```
   Confirmed as meeting the support team's documented requirement to be
   able to investigate any order-related ticket within its 21-day SLA
   window.

5. A replay test is added to CI, replaying the three most recent
   real `order-fulfillment-*` workflow histories pulled from production
   against the candidate worker binary — this specific run catches that
   a proposed refactor reordered the `ReserveInventory` and a new
   proposed `ValidateAddress` activity call, which would have broken
   replay for any order fulfillment already past that point in its
   history; the change is revised to use `workflow.GetVersion` before
   merging.

6. Build ID versioning is confirmed configured so the next worker deploy
   pins new executions to the new Build ID while in-flight orders
   finish on the version they started with.

## Cross-references

- [temporal-durable-workflow-orchestration](../temporal-durable-workflow-orchestration/SKILL.md) — authoring the workflow/activity/signal code this skill validates the configuration around, including the `GetVersion` patching discipline this skill's Build ID checks complement.
- [kafka-configuration-validation](../kafka-configuration-validation/SKILL.md) — a comparable pre-production configuration-validation discipline (topic/consumer-group settings checked before go-live) for the messaging side of a system a Temporal workflow might integrate with.
- [airflow-scheduler-and-dag-troubleshooting](../airflow-scheduler-and-dag-troubleshooting/SKILL.md) — a comparable "diagnose a stuck orchestration unit" workflow for Airflow's scheduler, useful for contrasting how a stuck DAG run is diagnosed versus a stuck Temporal workflow (task queue pollers) covered here.
