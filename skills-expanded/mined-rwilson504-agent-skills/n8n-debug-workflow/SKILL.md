---
name: n8n-debug-workflow
description: Diagnose and fix failing n8n workflow executions. Use when user says "my n8n workflow is failing", "execution errored", "this node returns an error", "rate limited", "Could not find paired item", "workflow is stuck", "webhook isn't firing", "Schedule trigger isn't running", "memory leak", "execution timeout", "data is empty in next node", "wrong data shape downstream", "items got duplicated", "binary data missing", or pastes an n8n execution error. Walks through reading the execution log, common-error catalog, item-linking forensics, rate-limit recovery, webhook/schedule debugging, and recovery patterns (retryOnFail, continueOnFail, Error Trigger). Do NOT use for designing new workflows (use n8n-build-workflow), writing Code nodes (use n8n-code-node), or hosting/Docker-level issues (use n8n-self-host).
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["n8n", "debugging", "troubleshooting", "execution-errors", "rate-limits", "item-linking"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/n8n", "emoji": "🟧" } }
---

# n8n Debug Workflow

Diagnose failing n8n executions. Most n8n bugs fall into a handful of
categories — recognize the category, then apply the matching fix.

**References:** [ERROR_CATALOG.md](references/ERROR_CATALOG.md) | [EXECUTION_DEBUGGING.md](references/EXECUTION_DEBUGGING.md) | [ITEM_LINKING_ERRORS.md](references/ITEM_LINKING_ERRORS.md) | [RATE_LIMITS.md](references/RATE_LIMITS.md) | [TRIGGER_PROBLEMS.md](references/TRIGGER_PROBLEMS.md)

**Lessons:** [LESSONS_LEARNED.md](LESSONS_LEARNED.md) — read before non-trivial work.

**Authoritative docs:** <https://docs.n8n.io/courses/level-two/chapter-4/> (debugging chapter) and <https://docs.n8n.io/flow-logic/error-handling/>.

---

## Triage in three questions

Before opening logs, get the user to answer three questions. They short-circuit
80% of debugging:

1. **Which node fails?** Open the execution in the Editor → Executions tab.
   Look for the red node. Errors propagate upstream visually — the actual
   failure is the FIRST red node from the trigger.
2. **What's the exact error message?** Copy it verbatim. n8n error messages
   are usually accurate; the model + free-text reasoning is almost always
   in the message.
3. **Did this work before?** If yes — what changed? (Workflow edits, n8n
   version upgrade, credential rotation, API change upstream, schedule
   timezone shift.)

If the user can't answer #1 because no execution log exists (workflow
never fires), jump to [Trigger never fires](#trigger-never-fires).

---

## Error categories (load the matching reference)

| Symptom | Category | Reference |
|---|---|---|
| Node throws with API/transport error | API errors | [ERROR_CATALOG.md](references/ERROR_CATALOG.md#api--transport) |
| "Could not find paired item" / `$('X').item` throws | Item linking | [ITEM_LINKING_ERRORS.md](references/ITEM_LINKING_ERRORS.md) |
| HTTP 429, ETIMEDOUT, ECONNRESET storms | Rate limits | [RATE_LIMITS.md](references/RATE_LIMITS.md) |
| "Cannot read properties of undefined" in expression | Expression errors | [ERROR_CATALOG.md](references/ERROR_CATALOG.md#expression-errors) |
| Trigger doesn't fire / fires twice / fires late | Trigger problems | [TRIGGER_PROBLEMS.md](references/TRIGGER_PROBLEMS.md) |
| Execution stalls or times out | Execution problems | [EXECUTION_DEBUGGING.md](references/EXECUTION_DEBUGGING.md#stalled-executions) |
| Memory/disk usage spikes during execution | Execution problems | [EXECUTION_DEBUGGING.md](references/EXECUTION_DEBUGGING.md#resource-issues) |
| Webhook returns wrong status/body | Webhook problems | [TRIGGER_PROBLEMS.md](references/TRIGGER_PROBLEMS.md#webhook-response-issues) |
| Data is "missing" in a downstream node | Item linking OR run-mode | [ITEM_LINKING_ERRORS.md](references/ITEM_LINKING_ERRORS.md), then [EXECUTION_DEBUGGING.md](references/EXECUTION_DEBUGGING.md#run-modes) |

---

## Procedure (any debugging request)

### Step 1 — Read the execution log

In the Editor:

1. Open the workflow.
2. Click the **Executions** tab.
3. Open the failed execution.
4. Click on the red (failed) node — the right panel shows input data,
   output data, and the error.
5. Click upstream nodes to verify they actually produced the data the
   failed node expected.

**Three things to extract:**

- **Error message** (exact text, including the "On node X" prefix).
- **Input data to the failing node** — is it empty? Wrong shape?
- **Output data of the immediately-upstream node** — does it match what the
  failing node was expecting?

### Step 2 — Reproduce locally if possible

- Use **Pin Data** on the failing node: right-click → Pin (or set
  `pinData` in workflow JSON). This lets you re-run downstream without
  re-firing the trigger.
- Use the **Run from this Node** option (right-click on a node) to start
  execution from a specific node using its pinned data.
- For Webhook-triggered workflows, replay the original request using the
  Webhook node's **"Listen for Test Event"** button + a tool like
  `curl`/`httpie` aimed at the test URL.

### Step 3 — Classify the error

Pick the matching category from the table above and load that reference
doc. Most categories have a checklist.

### Step 4 — Apply the fix

Common fix levers (least invasive first):

1. **Change node parameters** — fix expressions, set headers, adjust
   pagination.
2. **Add node-level resilience** — `retryOnFail: true`, `maxTries: 3`,
   `waitBetweenTries: 5000`, `continueOnFail: true`,
   `onError: "continueErrorOutput"`.
3. **Add flow-level resilience** — Wait node, Loop Over Items batching,
   Stop and Error with a useful message.
4. **Change the workflow structure** — add an error branch, extract a
   sub-workflow, add an idempotency check.
5. **Add an Error Workflow** at the instance level so future failures
   notify someone.

### Step 5 — Verify

- Manually re-execute with the failing input (use Pin Data or replay).
- Check the Executions tab to confirm the new run is green.
- For schedule/webhook workflows, monitor the next 1–3 production
  executions before declaring victory.

### Step 6 — Capture the lesson

If the root cause was non-obvious (most debugging is), append a dated entry
to [LESSONS_LEARNED.md](LESSONS_LEARNED.md). Future-you will thank past-you.

---

## Trigger never fires

If the workflow has no execution history and never fires:

- **Manual Trigger** — fires only when user clicks Execute Workflow. Won't
  fire on a schedule.
- **Workflow not activated** — toggle is "Inactive" in the top bar. Webhook,
  Schedule, App, and Form triggers only fire on production URLs when active.
- **Webhook URL confusion** — there are TWO URLs per Webhook node:
  - **Test URL** (`/webhook-test/<path>`) — works only when the editor is
    open and the node has "Listen for Test Event" running.
  - **Production URL** (`/webhook/<path>`) — works whenever the workflow is
    active.
- **Schedule mode mismatch** — "Interval" mode anchors to instance restart.
  "Cron Expression" mode anchors to wall-clock. Switch to Cron Expression
  for predictable schedules.
- **Timezone mismatch** — Schedule respects `settings.timezone` on the
  workflow, falling back to instance `GENERIC_TIMEZONE`. Verify both.
- **Trigger node deleted from active workflow** — n8n keeps the workflow
  active and shows no error, but no triggers fire. Re-add the trigger and
  toggle inactive → active to re-register.
- **App trigger credential expired** — Slack/Gmail/etc. OAuth tokens
  expire. Re-authenticate.
- **Queue mode worker not running** — if the instance is in queue mode and
  no worker is up, executions queue indefinitely. See
  [n8n-self-host](../n8n-self-host/SKILL.md).

See [TRIGGER_PROBLEMS.md](references/TRIGGER_PROBLEMS.md) for deeper coverage.

---

## Quick reference: node-level resilience flags

Set these on a node via the editor's "Settings" gear or in workflow JSON
under the node:

| Flag | Effect |
|---|---|
| `retryOnFail: true` | Auto-retry on any thrown error |
| `maxTries: 3` | Number of attempts (default 3) |
| `waitBetweenTries: 5000` | Milliseconds between retries (default 1000) |
| `continueOnFail: true` | (legacy) On error, output a "fail item" to the regular output and continue |
| `onError: "continueRegularOutput"` | Modern: on error, output `{ error: {...} }` to regular output |
| `onError: "continueErrorOutput"` | Modern: on error, output the error item to a SECOND output port (red dot in editor) |
| `onError: "stopWorkflow"` | Default: throw |
| `alwaysOutputData: true` | When input is empty OR node errors, still output one item (often `{}`) so downstream runs |
| `executeOnce: true` | Force node to run a single time even if multiple input items |

Don't blanket-apply `continueOnFail` — silent failures are worse than loud
ones. Use it deliberately where you have a recovery branch.

---

## Best practices

**Do:**
- Pin data on the failing node BEFORE making fix attempts so you can
  re-test deterministically.
- Add an Error Workflow at the instance level for any production workflow.
  Pick one — Slack, PagerDuty, email — and wire it once.
- Use `onError: "continueErrorOutput"` + a Set/Slack node on the error
  branch to log structured failure data instead of silently dropping items.
- Add a unique correlation ID early in the workflow (Set node, UUID
  expression) so you can grep logs/Slack alerts/database rows to one
  execution.
- Set `EXECUTIONS_TIMEOUT` (instance) and `executionTimeout` (workflow) to
  realistic ceilings — runaway workflows are common.
- Use **Workflow Insights** (Enterprise) or query the `execution_entity`
  table directly for trend analysis.

**Don't:**
- Don't disable a failing node to "fix" it. Find the root cause; the
  workflow only ran because the disabled node WAS doing work.
- Don't silently swallow errors with `continueOnFail` and no downstream
  handling. At minimum, log to an error branch.
- Don't keep increasing `maxTries` on a node that's failing every time.
  Retries are for transient errors; a persistent error needs a real fix.
- Don't debug by editing production. Duplicate the workflow ("Duplicate" in
  the Workflows list), debug the copy, then port the fix back.

---

## Continuous learning

After every non-trivial debugging session, append an entry to
[LESSONS_LEARNED.md](LESSONS_LEARNED.md). The lesson is most valuable when
the error was misleading, the cause was non-obvious, or the fix surprised
you. Follow the [Lesson entry template](../../agents/n8n.agent.md#lesson-entry-template)
in the agent file.
