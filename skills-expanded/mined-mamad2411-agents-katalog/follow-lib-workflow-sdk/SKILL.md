---
name: follow-lib-workflow-sdk
description: Use Workflow SDK (workflow-sdk.dev, Vercel) end to end — durable functions "use workflow"/"use step", sleep/hooks/webhooks, Worlds adapters, deploy + inspect
argument-hint: "[framework-or-world]"
allowed-tools:
  - exec
  - read
  - write
  - edit
  - grep
  - find_file_by_name
related:
  - follow-my-techstack
  - run-install
  - run-dev
  - run-test
  - follow-lib-tanstack-start
  - follow-service-vercel
---

## Goal

Use the Workflow SDK (package `workflow`, Vercel OSS) to build durable workflows — long-running stateful logic that persists progress through an event log and resumes after a restart/failure — running identically on local dev, Vercel, or other infra via World adapters

## Scope

Use when a feature needs long-running/multi-step logic that withstands failures: AI agents, pipelines, scheduled jobs, human-in-the-loop approvals — framework support: Next.js, Vite, React Router, Astro, Express, Fastify, Hono, Nitro, Nuxt, SvelteKit, TanStack Start, NestJS (beta), Python (beta)

- Catalog default → `/follow-my-techstack`; TanStack Start integration → `/follow-lib-tanstack-start`; Vercel deploy → `/follow-service-vercel`

## Execute

### 1. Install And Integrate

> Goal: integrate it into the framework in use

1. `bun add workflow` via `/run-install` + the framework integration per the docs (Next.js/Vite/Hono/Start, etc.)
2. Local dev uses the **Local World** automatically — state lives in `.workflow-data/` (gitignored), no config needed
3. Structure: `workflows/<name>/index.ts` (workflow fns) + `steps.ts` or a `steps/` folder + `workflows/shared/` — separate files help avoid bundler bugs

### 2. Write Workflows

> Goal: separate orchestration from work correctly

```ts
export async function processOrderWorkflow(orderId: string) {
  "use workflow";                    // sandboxed, deterministic, replayed
  const order = await fetchOrder(orderId);
  const payment = await chargePayment(order);
  return { orderId, status: "completed" };
}

async function chargePayment(order: Order) {
  "use step";                        // full Node.js, auto-retry (3x), persisted
  const stripe = new Stripe(process.env.STRIPE_KEY);
  return stripe.charges.create({ amount: order.total, currency: "usd", source: order.paymentToken });
}
```

- `"use workflow"` — orchestrate with conditionals/loops/try-catch/`Promise.all`; no Node.js runtime, npm is limited; must be deterministic (the framework freezes `Math.random`/`Date` for you — safe to use in a workflow)
- `"use step"` — real work, full npm, retry, the result is persisted; called outside a workflow = a normal fn (no retry/observability)

### 3. Suspension Primitives

> Goal: use wait/hook/webhook correctly

```ts
import { sleep, createWebhook } from "workflow";

await sleep("30d");                 // suspend without burning compute
const webhook = createWebhook();    // resume when an external system POSTs
await sendApprovalEmail(webhook.url);
const data = await webhook;
```

- Suspension happens at: a step hand-off, `sleep`, a webhook await — the state goes to the event log, resume continues from the same point
- Secrets/tokens that must be unguessable → generate them in a step (seeded random in a workflow is not a secret)

### 4. Deploy Via Worlds

> Goal: pick the backend matching the environment

1. **Local** — the dev default, `.workflow-data/`
2. **Vercel** — zero config; durable storage + a managed queue + dashboard observability + multi-region; **you must enable "Enable access to System Environment Variables"**, otherwise `VERCEL_DEPLOYMENT_ID` is missing → it falls back to the Local World → fails on a read-only FS
3. **Custom** — `WORKFLOW_TARGET_WORLD=@workflow/world-postgres` + `DATABASE_URL=...`, or build your own World

### 5. Inspect And Test

> Goal: observe and verify

1. `npx workflow inspect runs` (local) / `--backend @workflow/world-postgres` (remote)
2. `/run-dev` so the dev server runs real workflows → `/run-test` e2e through the workflow entry
3. v4 → v5: `npx skills add https://github.com/vercel/workflow --skill migrating-workflow-v4-to-v5`, then let the agent migrate (v5: inline steps, batched writes, compressed payloads — up to ~80% compute cost on Vercel)

## Rules

### 1. Determinism

- A workflow fn is replayed many times — no side effects outside steps; non-determinism (network, fs, real time) goes into `"use step"` only
- Always pass-by-value — mutating an object passed into a step has no effect back in the workflow; return data instead

### 2. Step Design

- A step should be idempotent at best — the default 3x retry may duplicate work; side-effects coming from outside must be deduped
- Long step → hand it to a queue if it exceeds the inline budget — avoid one super-long process

### 3. Deployment

- Production on Vercel = System Env Vars ON — check before every deploy
- `WORKFLOW_TARGET_WORLD` + world-specific env must be set for both build and runtime

- Use `/follow-my-techstack` to pick the orchestration tool
- Use `/run-dev` + `/run-test` to verify real runs

## Expected Outcome

- Workflow/step separated correctly: the orchestrator is deterministic, steps are idempotent + retryable
- Deploy works correctly on local/Vercel/custom World; runs are inspectable; resume after failure really works
