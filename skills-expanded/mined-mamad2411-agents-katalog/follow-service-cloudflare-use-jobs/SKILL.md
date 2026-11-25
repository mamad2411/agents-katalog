---
name: follow-service-cloudflare-use-jobs
description: Use Cloudflare Queues, Cron Triggers, Workflows, Durable Objects — async jobs, scheduling
argument-hint: "[queue|cron|workflow|do]"
related:
  - follow-service-cloudflare
  - run-test
  - resolve-errors
---

## Goal

Use the async/scheduled features of Workers — Queues (producer/consumer), Cron Triggers, Workflows (durable multi-step), Durable Objects (stateful coordination)

## Scope

Background jobs and scheduling — pick correctly: Queue = fire-and-forget/async offload, Cron = scheduled runs, Workflow = multi-step durable execution, DO = strongly-consistent per-key state; details in `references/triggers-and-cron.md`

## Execute

### 1. Queues

```bash
wrangler queues create my-queue
```

```ts
// wrangler.jsonc: queues.producers + queues.consumers
// producer
await env.MY_QUEUE.send({ job: 'resize', id })   // sendBatch for multiple messages

// consumer — exported in the Worker
export default {
  async queue(batch: MessageBatch, env: Env) {
    for (const msg of batch.messages) { await process(msg.body); msg.ack() }
    // batch.retryAll() when the whole batch fails; dead letter queue is set in config
  },
}
```

### 2. Cron Triggers

1. `wrangler.jsonc`: `triggers: { crons: ["*/5 * * * *"] }`
2. Handler: `export default { async scheduled(event, env, ctx) { ctx.waitUntil(job()) } }`
3. Test local: `wrangler dev --test-scheduled` + `curl "http://localhost:8787/__scheduled?cron=*+*+*+*+*"`
4. `wrangler triggers deploy` when only triggers need deploying

### 3. Workflows (multi-step durable)

```ts
export class MyWorkflow extends WorkflowEntrypoint {
  async run(event, step) {
    const a = await step.do('step-1', async () => fetchA())
    await step.sleep('wait', '10 minutes')
    return await step.do('step-2', async () => fetchB(a))
  }
}
// trigger: await env.MY_WORKFLOW.create({ params })
```

- `step.do`/`step.sleep`/`step.waitForEvent` — retry + persist automatically per step

### 4. Durable Objects (when coordination is needed)

- `class` extends `DurableObject` + binding + `[[migrations]]` tag — per-object strong consistency, websockets, alarms
- Use only when KV/Queue is not enough (per-entity locks, realtime rooms)

### 5. Verify

1. `wrangler dev` — really test the queue consumer, scheduled handler, and workflow steps
2. `/run-test`; fail → `/resolve-errors`

## Rules

- Consumer handlers must `ack()` or `retry()` every message — never swallow errors
- Use `ctx.waitUntil` for work that extends past the response in fetch/scheduled
- Workflow steps must be idempotent — a step may retry
- DOs need a new `[[migrations]]` entry for every added class

## Expected Outcome

- Chosen jobs/schedule working both locally and deployed
- Dead-letter/retry semantics correct
