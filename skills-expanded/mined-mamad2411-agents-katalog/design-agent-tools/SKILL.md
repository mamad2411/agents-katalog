---
name: design-agent-tools
description: Design or repair the tool surface an LLM agent acts through — one responsibility per tool, schema-constrained arguments, structured errors the model can recover from, capped and paginated results, an explicit side-effect class per tool with runtime enforcement, idempotency keys on irreversible effects, and the loop budgets and termination conditions that keep a run bounded. Use before giving an agent its first tool, when an agent loops, retries, misuses arguments or takes an action nobody authorised, or when adding a write capability to an existing agent.
allowed-tools: Read Grep Glob Bash Write Edit
argument-hint: "[agent-or-module-path]"
user-invocable: true
model: sonnet
effort: medium
metadata:
  foundry.vertical: ai
  foundry.io: "requirement.v1 -> plan.v1 + docs/agents/<agent>-tools.md"
license: Apache-2.0
---

# Design the agent's tool surface

Tools are the agent's API and its blast radius. Most agent reliability is won here, not in the
prompt: a well-shaped tool makes the wrong call impossible to express, while a vague one turns
every ambiguity into a production effect.

Work in this order: **inventory → contracts → errors → effects → budgets → tests**.

## When not to use this

- **There is no loop.** A single LLM call with function calling is not an agent; validate the
  output at the boundary (`prompt-engineer`) and stop.
- **The topology is the problem.** If the question is "one agent or three", start with
  `agent-architect` — tool design cannot rescue a wrong decomposition.
- **The tool is a retrieval endpoint whose quality is in doubt** → `build-rag-pipeline`. Here we
  design the interface; there you make it return the right things.
- **You are designing a public API for third parties** → `foundry-dev:design-api-contract`. An
  agent-facing tool is allowed to be narrower, more opinionated and less general than a public
  API, and conflating the two produces a bad version of both.

## Step 1 — inventory what the agent can already do

```bash
grep -rn "@tool\|StructuredTool\|tool(\|function_declarations\|tools=\[" \
  --include='*.py' --include='*.ts' --include='*.js' . | head -40
grep -rn '"name":' --include='*.json' . | grep -i "tool" | head -20
```

For each tool record: name, arguments, what it reads, what it changes, whether the change is
reversible, who it acts as (which credentials), and its worst-case result size. Any tool you
cannot fill that row for is the first finding.

**Count them.** Past roughly ten tools, selection accuracy degrades and the schemas alone consume
meaningful context in every call. Merge near-duplicates, split overloaded ones, or move to a
router topology.

## Step 2 — contracts

- **Verb-object names the model can choose between**: `search_orders`, `get_order`,
  `refund_order`. Not `data_api`, not `helper`, not `do_action`. Overlapping names cause
  oscillation between two tools that do nearly the same thing.
- **One responsibility each.** A tool with a `mode` argument that changes what it does is two
  tools wearing one schema, and the model will pick the wrong mode.
- **Constrain arguments**: enums instead of free strings, ids instead of names, explicit units in
  the field name (`amount_cents`, `timeout_ms`), dates in one stated format. Every free-text
  argument is a place the model invents a value.
- **Required only when knowable.** A required field the model cannot know forces a fabrication;
  make it optional and handle the absence server-side.
- **Never accept an unvalidated query language.** A tool taking raw SQL, a shell command, a
  JSONPath or a regex converts a model's syntax error into a production incident, and it hands an
  injected instruction a direct execution path. Expose parameters; validate server-side; reject
  rather than guess. Where a query interface is genuinely required, allow-list the tables,
  columns and operations, and run it as a least-privileged read-only principal.
- **Describe the tool for a caller who cannot see your code.** The description states what it
  does, when to use it, when *not* to use it, and what it returns. "When not to use it" is what
  stops the model reaching for it as a universal hammer.
- **Version the tool surface.** Changing an argument's meaning without a name change silently
  invalidates every stored trace and every eval baseline.

## Step 3 — errors the model can act on

Return errors as data, in-band, with a machine-readable code and an actionable hint:

```json
{"error": "not_found", "hint": "no order with id ORD-9; call search_orders with the customer email first"}
{"error": "invalid_argument", "field": "amount_cents", "hint": "integer cents, not a decimal string"}
{"error": "forbidden", "hint": "this order belongs to another tenant; do not retry"}
{"error": "rate_limited", "retry_after_ms": 2000}
```

Rules:

- An exception that aborts the loop teaches the model nothing and loses the run's progress.
- An opaque message (`"error occurred"`) produces blind retries — the single most common source
  of agent cost blowouts.
- Say explicitly whether a retry can help (`do not retry` vs `retry_after_ms`). Without that, the
  model guesses, and it guesses "retry".
- Validate arguments **before** side effects, and return every violation at once rather than one
  per round trip.

## Step 4 — result size

- **Cap every result** and paginate: return the top slice, the total count and a cursor. One
  oversized tool result poisons the remainder of the run: it crowds out the instructions, costs
  budget on every subsequent step, and buries the relevant fields.
- Return **fields the agent needs**, not the full record. Trimming a payload is the cheapest
  latency and cost win in most agent systems.
- For large artefacts, **write to a store and return a reference** (path plus a bounded summary).
  This is the same context-firewall discipline Foundry applies to its own agents
  (AUTHORING.md §2).
- State the cap in the tool description so the model knows the result is partial and can page.

## Step 5 — classify effects and enforce the class in the runtime

| Class | Examples | Required controls |
|---|---|---|
| `read` | search, get, list | tenant/ACL filter applied server-side from the session; rate limit |
| `write-reversible` | create draft, add tag, open ticket | audit log with run id; documented undo |
| `write-irreversible` | send email, charge, delete, deploy, post publicly | idempotency key from run+step+args; dry-run mode; explicit human confirmation; per-run cap |
| `external-untrusted` | fetch URL, read user file, read third-party record | result treated as data, never as instructions; provenance attached; no auto-follow of links |

Three rules that are not negotiable:

1. **Enforcement is in the runtime, not the prompt.** "Ask before sending email" in a system
   prompt is a request to a probabilistic system. The gate is code that will not execute without
   a confirmation token.
2. **Least tool.** The agent gets the smallest set that lets it finish the task at hand.
   Excessive agency and improper output handling are named risks in the OWASP Top 10 for LLM
   Applications — verify the current identifiers against the published list before citing them by
   number in a report — and both are mitigated by removing capability, not by better wording.
3. **The agent acts as a principal with its own credentials**, scoped to the session's user and
   auditable. Never a shared admin token. Coordinate with `foundry-dev:identity-engineer`.

## Step 6 — budgets and termination

Set all of these in the runtime, and make exceeding one a reported, non-silent outcome:

- `max_steps` per run, and a **repeat-state detector**: hash the last N (tool, arguments) pairs
  and abort on a cycle. Step caps alone let an agent burn the whole budget in a two-tool loop.
- `max_tokens` and `max_cost` per run, with a kill switch an operator can trigger mid-run.
- `max_wall_clock`, shorter than any upstream request timeout.
- Per-tool **retry budget** with backoff and a circuit breaker; one flaky dependency must not
  become hundreds of calls.
- Per-run cap on `write-irreversible` calls — a small integer, usually 1.
- An explicit **success predicate** and an explicit **give-up predicate**, plus the default
  outcome when neither is reached. An agent that cannot state how it knows it is done will not
  finish.
- A timeout with a defined default action on any human-gate wait, or the run deadlocks invisibly.

## Step 7 — test tools independently of the agent

- Unit tests per tool: happy path, every validation error, the permission denial, the pagination
  boundary, the idempotency replay (same key twice must not double-apply).
- A **cross-tenant test** per `read` tool: authenticated as A, ask for B's data, expect zero rows.
- A **loop provocation test**: a scripted environment that returns the state the agent just tried
  to change, asserting the repeat-state detector fires.
- A **dry-run test** for every irreversible tool, asserting nothing was applied.
- Trace assertions in the eval suite: correct tool selected, arguments schema-valid, no forbidden
  tool for the scenario (hand the task set to `build-eval-suite`).

Debugging a tool bug through a non-deterministic agent loop costs an order of magnitude more than
catching it in a unit test. This step is where the time is saved.

## Step 8 — write it down

`docs/agents/<agent>-tools.md`: the inventory table (name, arguments, effect class, credentials,
result cap), the error code catalogue, the budgets with their values, success and give-up
predicates, the human-gate policy, the trace fields recorded per step, and the review date.

Emit `plan.v1` to `.foundry/blackboard/<wave>/design-agent-tools.json`, with `outOfScope` naming
every capability deliberately withheld from the agent — that list is a security control and it
must be explicit.

## Exit criteria

1. Every tool has a filled inventory row, including its credentials and worst-case result size.
2. Tool count is justified; overlapping tools merged or routed.
3. All arguments schema-constrained; no unvalidated query language; no free-text argument without
   a stated reason.
4. Every tool returns structured errors with codes, hints and a retry indication.
5. Every result is capped and paginated; large artefacts returned by reference.
6. Every tool carries an effect class, enforced in the runtime.
7. Every `write-irreversible` tool has an idempotency key, a dry-run mode, a human gate and a
   per-run cap.
8. Step, token, cost and wall-clock budgets set; repeat-state detection implemented.
9. Success and give-up predicates written; human-gate timeout has a default action.
10. Unit tests per tool including permission denial, pagination boundary and idempotency replay;
    cross-tenant test passing; loop provocation test passing.
11. Per-step tracing records tool, arguments, outcome, tokens and cost.
12. `plan.v1` validates with a non-empty `outOfScope`; the doc exists.

## Degradation

- **Framework does not support tool-level permissions** → wrap the tools in your own dispatcher
  that enforces the effect class before delegating, and record the framework limitation as a
  finding rather than trusting the prompt.
- **No human channel for confirmation** → remove the irreversible tools from the set until there
  is one. Reduce capability rather than accept unreviewed effects.
- **No tracing backend** → write per-step JSONL to `.foundry/scratch/<session>/runs/<run-id>.jsonl`
  as an interim and raise a `high` finding: an untraceable agent cannot be operated.
- **Legacy tool cannot be reshaped** (third-party, frozen contract) → put an adapter in front of
  it that narrows arguments, caps results and normalises errors; the agent never sees the raw
  tool.
- **`superpowers` installed** → `superpowers:test-driven-development` for the tool unit tests, and
  `superpowers:systematic-debugging` when chasing a loop: form the hypothesis from the trace, not
  from the transcript.

## Deliberately not covered

Topology and state design (`agent-architect`), prompt wording and output schemas
(`prompt-engineer`), retrieval quality behind a search tool (`build-rag-pipeline`), measuring
task success (`build-eval-suite`), backend authorisation design
(`foundry-dev:identity-engineer`), public API contracts
(`foundry-dev:design-api-contract`), and spend forecasting
(`foundry-economics:ai-cost-controller`).

## Bundled references

- `references/tool-contract-patterns.md` — good and bad shapes for search, mutation, long-running,
  batch and human-gate tools, with the failure each shape prevents.
- `references/agent-failure-taxonomy.md` — fourteen agent failure modes, the trace signature that
  identifies each, and the runtime control that actually stops it.
