---
name: volcano-durable
description: Use for Volcano durable functions, long-running or resumable workflows, checkpointed steps, waits, human approvals, polling, durable executions, idempotent starts, and durable function schedulers.
---
# Volcano Durable Functions Skill

## Role and pairing

Use a durable function when work must survive restarts, wait without holding a
request open, or resume from completed steps. Examples include order pipelines,
agent runs, approval flows, reconciliation jobs, and slow batch work.

Always pair this skill with:
- `volcano-sdk` for the application entrypoint and domain routing.
- `volcano-platform` for project shape, variables, config, auth, and cloud safety.

Use `volcano-functions` only when the same task also has standard synchronous
functions. The handler contracts differ.

## Core contract

- Durable functions are a separate collection from standard functions.
- Durable functions use `volcano/functions/` and are marked with `kind: durable`
  in `volcano-config.yaml`.
- A function kind is fixed when the function is created.
- Deploy locally with `volcano durable deploy` and to cloud with
  `volcano cloud durable deploy`. Standard function deploy skips manifest
  entries marked durable. `volcano deploy` and `volcano cloud deploy` deploy
  them with the rest of the project, after the standard functions.
- Start an execution. Do not invoke a durable function.
- A start returns an execution handle. Poll the execution for its result.
- JavaScript, TypeScript, and Python can author durable handlers. Ruby clients
  can start and read executions but cannot author handlers.
- Local and cloud use the same handler, manifest, and execution commands.

Use the project's language and supported capability:

| Project signal | Author durable handlers | Manage executions | SDK behavior |
|---|---|---|---|
| `package.json`, `.ts`, `.js` | JavaScript/TypeScript | JavaScript/TypeScript | camel-case methods and result envelopes |
| `pyproject.toml`, `requirements.txt`, `.py` | Python | Python | snake-case methods and typed exceptions |
| `Gemfile`, `.gemspec`, `.rb` | Use JavaScript or Python | Ruby | snake-case methods and typed exceptions |

## Authoring rule: replay must be deterministic

Each context operation is checkpointed. On resume, completed operations replay
their recorded results. Code between operations runs again.

- Put side effects and decisions that must run once inside `ctx.step`.
- Use `ctx.wait` for delays. Do not hold the runtime with timers or sleep.
- Do not branch between checkpoints on the current time, random data, or mutable
  external state.
- Give operations stable names and reach them in the same order on replay.
- Return the application result directly. Do not return the standard function
  `{ statusCode, body }` shape.

## JavaScript and TypeScript

Use a directory function so its dependency manifest stays with its source:

```text
volcano/functions/order-pipeline/
├── index.js
└── package.json
```

```json
{
  "private": true,
  "dependencies": {
    "@volcano.dev/sdk": "latest"
  }
}
```

```js
const { durable } = require('@volcano.dev/sdk/durable');

exports.handler = durable(async (input, ctx) => {
  if (!input?.order_id) throw new Error('order_id is required');

  const charge = await ctx.step('charge', () => chargeCard(input.order_id));
  await ctx.wait('settle', '30s');

  const packed = await ctx.map('pack', input.items ?? [], (item, itemCtx) =>
    itemCtx.step('pack-item', () => pack(item)),
  );

  return { charge_id: charge.id, packed: packed.results };
});
```

## Python

```text
volcano/functions/order-pipeline/
├── main.py
└── requirements.txt
```

```text
volcano-sdk
```

```python
from volcano_sdk.durable_authoring import durable


@durable
def handler(event, ctx):
    if not event or not event.get("order_id"):
        raise ValueError("order_id is required")

    charge = ctx.step("charge", lambda scope: charge_card(event["order_id"]))
    ctx.wait("settle", "30s")
    return {"charge_id": charge["id"]}
```

Python durable operations are synchronous. A step function receives its scope.

## Context operations

| Operation | Use |
|---|---|
| `ctx.step(name?, fn, options?)` | Run work and record its result. Retry policy and at-most-once behavior belong here. |
| `ctx.wait(name?, duration)` | Suspend for at least one second without holding compute. |
| `ctx.waitUntil(name?, check, options)` | Poll state until `options.until` passes. `initialState` is required. |
| `ctx.waitForApproval(name, options)` | Suspend until a person approves or denies, or the approval expires. Python takes keywords, not an options object: `ctx.wait_for_approval(name, *, title, description=None, details=None, timeout=None)`. |
| `ctx.map(name?, items, fn, options?)` | Run one checkpointed child context per item. Set `concurrency` when required. |
| `ctx.parallel(name?, branches, options?)` | Run independent checkpointed branches. |
| `ctx.child(name?, fn)` | Group operations in a child context. |
| `ctx.log` | Log with execution identifiers attached. |

Each step attempt, wait, poll check, child, map item, and parallel branch uses a
durable operation, and each approval uses three. `durable get` shows the function's execution timeout and
result retention. Read the plan limits documentation for operation allowance,
operations per execution, and concurrency limits.

## Human approvals

Use `waitForApproval` when a person must sign off before the workflow continues.
The execution suspends without holding compute and resumes with the decision.
Use `ctx.waitUntil` only for state your code can read, such as a payment
settling. Do not build your own approval table and poll it.

```js
const { durable } = require('@volcano.dev/sdk/durable');

exports.handler = durable(async (input, ctx) => {
  const quote = await ctx.step('quote', () => quoteShipping(input.order_id));

  const decision = await ctx.waitForApproval('ship-order', {
    title: `Ship order ${input.order_id}?`,
    description: 'Express shipping is billed to the customer.',
    details: { order_id: input.order_id, cost: quote.cost },
    timeout: '3d',
  });
  if (!decision.approved) {
    return { shipped: false, status: decision.status, comment: decision.comment };
  }

  await ctx.step('ship', () => ship(input.order_id));
  return { shipped: true, approved_by: decision.decidedBy?.email ?? null };
});
```

```python
from volcano_sdk.durable_authoring import durable


@durable
def handler(event, ctx):
    order_id = event["order_id"]
    quote = ctx.step("quote", lambda scope: quote_shipping(order_id))

    decision = ctx.wait_for_approval(
        "ship-order",
        title=f"Ship order {order_id}?",
        details={"order_id": order_id, "cost": quote["cost"]},
        timeout="3d",
    )
    if not decision.approved:
        return {"shipped": False, "status": decision.status}

    ctx.step("ship", lambda scope: ship(order_id))
    return {"shipped": True}
```

The decision has `approved`, `status`, `comment`, `decidedBy` (`{ id, email }`
or `null`), and `decidedAt`. Python uses attributes: `decision.decided_by`
(with `id` and `email`, or `None`) and `decision.decided_at`.

| `status` | `approved` | Meaning |
|---|---|---|
| `approved` | `true` | A person approved, with an optional comment. |
| `denied` | `false` | A person denied, with an optional comment. |
| `expired` | `false` | `timeout` passed first. `comment` is empty; `decidedBy` and `decidedAt` are null. |

A deny or an expiry is a return value, not an error. Branch on
`decision.approved` and handle `expired` explicitly. An approval whose execution
ends first (stopped, failed, or timed out) shows as `cancelled` to the owner;
the workflow never receives it.

- `timeout` takes the same durations as `ctx.wait`. Without one, the approval
  lasts until the execution's own timeout.
- Give each approval a short, stable, plain-ASCII name; it is the operation's
  name in the execution's history, and the SDK refuses one longer than 237
  characters or outside printable ASCII. Replay returns the recorded decision
  and never requests the approval twice.
- Approvals work inside `ctx.parallel`, `ctx.map`, and child contexts. An
  execution can have at most 100 pending at once; the next request throws.
- Each approval is three durable operations: the approval, the wait for the
  decision, and the step that registers the request. Inside `ctx.map` that
  cost applies per item.
- Build `title` and `details` from input or step results. `title` holds up to
  200 characters, `description` 4000, and the whole request 64 KiB.
- `details` is shown to the person deciding and kept for a year. Do not put
  secrets or credentials in it.

### Who decides

A person decides, in the dashboard under **Approvals**, or from the CLI. In
local mode the local user decides without logging in:

```sh
volcano durable approvals list                  # pending, newest first
volcano durable approvals get <approval-id>
volcano durable approvals approve <approval-id> --comment "Checked stock"
volcano durable approvals deny <approval-id> --comment "Customer cancelled"
volcano durable approvals stats --since 30d
```

In cloud, the person runs `volcano login` and then the same commands under
`cloud`:

```sh
volcano cloud durable approvals list
volcano cloud durable approvals approve <approval-id> --comment "Checked stock"
```

The SDK owner clients expose the same operations under
`durable.approvals`. Project access tokens can read approvals and stats but get
`403` on approve and deny. The MCP tools `list_durable_approvals` and
`get_durable_approval_stats` only read; MCP has no way to decide.

Never approve or deny an approval yourself, including one your own workflow
requested during testing. List it, tell the user its ID and title, and let them
decide. Do not write code that decides approvals automatically; that defeats
the approval.

## Start and manage executions from an application

`start` accepts an application credential and returns an execution handle. An
execution name makes retries idempotent. `get`, `list`, and `stop` are
owner-scoped; call them from trusted backend code with the project owner's
platform user token. Auth-user sessions, anon keys, service keys, and project
access tokens are not accepted.

### JavaScript and TypeScript

```ts
import { VolcanoClient } from '@volcano.dev/sdk';

const { data: handle, error } = await volcano.durable.start(
  'order-pipeline',
  { order_id: 4417 },
  { executionName: 'order-4417' },
);
if (error || !handle) throw error ?? new Error('Durable start returned no execution');

const owner = new VolcanoClient({
  anonKey: process.env.VOLCANO_ANON_KEY!,
  apiUrl: process.env.VOLCANO_API_URL,
  accessToken: process.env.VOLCANO_PLATFORM_TOKEN!,
});
const read = await owner.durable.get(projectId, 'order-pipeline', handle.id);
if (read.error) throw read.error;
const listed = await owner.durable.list(projectId, 'order-pipeline', { status: 'running' });
if (listed.error) throw listed.error;
const stopped = await owner.durable.stop(projectId, 'order-pipeline', handle.id);
if (stopped.error) throw stopped.error;
```

### Python

```python
import os
from volcano_sdk import VolcanoClient

owner = VolcanoClient(
    anon_key=os.environ["VOLCANO_ANON_KEY"],
    access_token=os.environ["VOLCANO_PLATFORM_TOKEN"],
)
handle = client.durable.start(
    "order-pipeline", {"order_id": 4417}, execution_name="order-4417"
)
execution = owner.durable.get(project_id, "order-pipeline", handle.id)
page = owner.durable.list(project_id, "order-pipeline", status="running")
owner.durable.stop(project_id, "order-pipeline", handle.id)
```

### Ruby

```ruby
require "volcano"

owner = Volcano::Client.new(
  anon_key: ENV.fetch("VOLCANO_ANON_KEY"),
  access_token: ENV.fetch("VOLCANO_PLATFORM_TOKEN")
)
handle = client.durable.start(
  "order-pipeline", { order_id: 4417 }, execution_name: "order-4417"
)
execution = owner.durable.get(project_id, "order-pipeline", handle.id)
page = owner.durable.list(project_id, "order-pipeline", status: "running")
owner.durable.stop(project_id, "order-pipeline", handle.id)
```

Poll `get` for live state. Listings carry the last observed state. `stop` is
asynchronous, so poll until the execution reaches a terminal status.

## Manifest

```yaml
# volcano-config.yaml
version: 1
functions:
  - name: order-pipeline
    kind: durable
    visibility: private
    variable_scope: scoped
    variables: [PAYMENTS_API_KEY]
```

Rules:
- Omitting `kind` means `standard`.
- `kind` is an assertion. Config deploy rejects a mismatch.
- Do not set `invocation_mode`, `http_auth_mode`, or `openapi_spec` on a durable
  function. Durable functions have no synchronous HTTP invocation path.
- `visibility` decides who can start executions: `private` (the default for
  new functions) admits service keys and schedulers, `authenticated` adds the
  project's signed-in users, and `public` adds anon keys with
  `functions.invoke`. No level lets an end user or anon key read results or
  stop executions.
- A declared `schedulers` list is fully synced by config deploy. Omitted entries
  are deleted.

## Local workflow

Run and verify Durable functions locally before cloud deployment:

```sh
volcano start
volcano deploy                  # or only the durable functions: volcano durable deploy --all
volcano durable get order-pipeline

volcano durable start order-pipeline \
  --input '{"order_id":4417}' \
  --name order-4417

volcano durable executions list order-pipeline --status running
volcano durable executions get order-pipeline <execution-id>
volcano durable logs order-pipeline --type runtime
```

Local execution uses one region. Waits resolve immediately so long workflows
finish quickly while still suspending and replaying checkpoints. Instant waits
cause more resumes per wall-clock minute than production, which helps expose a
step that is unsafe to replay. Set `LOCAL_DURABLE_REAL_TIME=true` before
`volcano start` when wait timing must be real. Local executions persist across
`volcano stop` and `volcano start`. Approval timeouts always run in real time,
so test expiry locally with a short `timeout`.

Local executions increment the same execution, operation, and compute counters
as cloud executions. Inspect them through `GET /projects/{id}/usage`; the CLI
has no project usage command. For `ctx.waitUntil`, `maxAttempts` directly bounds
the poll operation count, so check local usage before cloud deployment.

## Cloud workflow

Cloud deploy requires explicit user approval. Follow `volcano-platform` for
login, project selection, variables, and config deployment.

```sh
# Deploy the whole project, durable functions included, and wait until active.
volcano cloud deploy --env-file volcano/cloud.env

# Or deploy only the manifest entries marked durable.
volcano cloud durable deploy --all

# Or deploy one source. --visibility works only with -f; leave it out to keep
# the current level.
volcano cloud durable deploy -f order-pipeline --visibility authenticated

# Deployment is asynchronous. Wait for active before starting work.
volcano cloud durable get order-pipeline

volcano cloud durable start order-pipeline \
  --input '{"order_id":4417}' \
  --name order-4417

volcano cloud durable executions get order-pipeline <execution-id>
```

For local commands, use `volcano durable ...`. For cloud commands, insert
`cloud` after `volcano`. `--input` accepts an inline JSON object or a file
containing one. Omitting it means no input. `--name` is the idempotency key in
both local and cloud. Repeating the same name returns the same execution instead
of starting duplicate work.

Execution statuses are `pending`, `running`, `succeeded`, `failed`,
`timed_out`, `stopped`, and `unknown`. Fetch one execution to refresh its state.
`unknown` is terminal. Retry the start with the same execution name to recover
the same execution when possible.

## Schedulers

A durable scheduler starts an execution on each tick. It does not invoke the
function.

```sh
volcano cloud durable schedulers create order-pipeline \
  --name nightly-orders \
  --cron "0 2 * * *" \
  --input '{"scope":"nightly"}'

volcano cloud durable schedulers list order-pipeline
volcano cloud durable schedulers disable order-pipeline <scheduler-id>
volcano cloud durable schedulers enable order-pipeline <scheduler-id>
```

Schedulers require SUPERAGENT. A tick can overlap a running execution and uses the
same execution allowance, operation allowance, and concurrency cap as a manual
start.

## Safety

- Validate public-function input. Anyone with the project's anon key can spend
  execution and operation allowance on a public durable function.
- Keep execution names tied to one unit of work. A name stays reserved while
  its execution is readable.
- Keep returned results small. Persist data that must outlive result retention.
- Stopping is asynchronous and does not undo completed steps. Poll with
  `executions get` until terminal.
- Deleting a durable function removes its execution history. Confirm before
  `durable delete`, `executions stop`, or `schedulers delete`.
- `approvals list`, `get`, and `stats` are safe to run. `approvals approve` and
  `deny` are for the user alone; never run them.
- Bound `logs --follow` with a timeout in agent-driven diagnostics.

## Troubleshooting

Use `volcano durable ...` for local state and `volcano cloud durable ...` for
cloud state.

1. Run `durable get <name>` with the correct prefix and inspect status.
2. For deploy failure, run `durable logs <name> --type build`.
3. For execution failure, run `durable logs <name> --type runtime`.
4. A `404` can mean the name belongs to the standard function collection, or
   the durable function is `private` and the caller isn't a service key.
5. A start during provisioning returns `409`; wait for `active`.
6. A `429` means a concurrency or durable allowance limit blocked the start.
7. A scheduler `403` can mean the project plan does not include schedulers.
8. An execution that stays `running` may be waiting on an approval. Check
   `durable approvals list --execution <execution-id>`.
9. An approve or deny `403` means the credential is not a person's. A `409`
   means the approval was already decided, expired, or cancelled.
10. `VOLCANO_PLATFORM_API_URL` is reserved. The platform sets it on durable
    functions; a project variable with that name is rejected.

## Verification

- Validate source syntax or run the project's typecheck and unit tests.
- Confirm the manifest names every durable function with `kind: durable`.
- Run `volcano start` and `volcano deploy` (or `volcano durable deploy --all`).
- Wait for local function status `active`.
- Start one local execution with a unique idempotency name.
- If it waits on an approval, give the user its ID and ask them to decide.
- Poll it to a terminal status and check its result.
- Read runtime logs if the result is not `succeeded`.
- After approved cloud deployment, repeat the execution check with
  `volcano cloud durable`.

## References

- Hosting contract: `volcano-hosting/docs/public/functions/durable-functions.md`
- Approvals: `volcano-hosting/docs/public/functions/durable-approvals.md`
- Local guide: `volcano-hosting/docs/public/guides/durable-functions-locally.md`
- CLI contract: `volcano-cli/docs/durable-functions.md`
- Command source: `volcano-cli/internal/cmd/durable/`
