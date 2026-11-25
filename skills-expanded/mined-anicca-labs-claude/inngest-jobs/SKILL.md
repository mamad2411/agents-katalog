---
name: inngest-jobs
description: Inngest background jobs and cron conventions — function registration, step.run/step.sendEvent, the sweep-then-dispatch pattern for time-based work, typed event catalogs, and safe local dev via the Inngest MCP. Use when writing a cron job, a background task triggered by an event, or debugging a run in the Inngest dev server.
---

Apply the following conventions to Inngest functions in this project.

## The two trigger shapes

```ts
import { inngest } from '../client';

// Cron — runs on a schedule, no event payload
export const nightlyDigest = inngest.createFunction(
  { id: 'nightly-digest', name: 'Send nightly digest' },
  { cron: '0 6 * * *' },
  async ({ step }) => {
    /* ... */
  },
);

// Event-driven — runs when a named event is sent
export const sendWelcomeEmail = inngest.createFunction(
  { id: 'send-welcome-email', name: 'Send welcome email' },
  { event: 'user/created' },
  async ({ event, step }) => {
    /* ... */
  },
);
```

`id` is stable and used for dedup/concurrency config — never derive it from something that changes (a variable, a timestamp). `name` is the human label shown in the dev server / dashboard.

## Explicit function registry, not auto-discovery

Every function module is imported and flattened into one array served at the Inngest endpoint — there's no glob or filesystem convention scanning for functions:

```ts
// inngest/functions/index.ts
import { nightlyDigest } from './nightlyDigest';
import { sendWelcomeEmail } from './sendWelcomeEmail';
import { sweepExpiredTrials, handleTrialExpired } from './trialExpiry';

export const functions = [nightlyDigest, sendWelcomeEmail, sweepExpiredTrials, handleTrialExpired];
```

```ts
// inngest/serve.ts (mounted in the Express app, or as its own route)
import { serve } from 'inngest/express';
import { inngest } from './client';
import { functions } from './functions';

app.use('/api/inngest', serve({ client: inngest, functions }));
```

This is deliberate over auto-discovery: a missing function is a compile error or an obvious diff, not a silent no-op because a file didn't match a glob pattern.

## `step.run` / `step.sendEvent` — not one big function body

Wrap discrete sub-operations in `step.run` so each is independently retried, cached, and visible in the run timeline — a step that already succeeded isn't re-executed if a later step throws and the function retries:

```ts
export const sendWelcomeEmail = inngest.createFunction(
  { id: 'send-welcome-email', name: 'Send welcome email' },
  { event: 'user/created' },
  async ({ event, step }) => {
    const user = await step.run('fetch-user', () => userService.getById(event.data.userId));

    await step.run('send-email', () => emailService.sendWelcome(user.email));

    await step.sendEvent('emit-onboarding-started', {
      name: 'onboarding/started',
      data: { userId: user.id },
    });
  },
);
```

A function with no `step.run` calls loses retryability granularity — if it fails halfway, the whole body re-runs from the top on retry, including side effects that already succeeded (a duplicate email). Wrap anything with a side effect or a network call.

## Sweep-then-dispatch for time-based work

Don't put the actual work inside the cron function. A lightweight cron finds *candidates* and emits one event per candidate; a separate event-driven function does the work. This keeps each unit of work independently retryable and observable, instead of one long cron run where a single failure (or timeout) can drop the rest of the batch silently:

```ts
// Sweep: cron, finds candidates, only emits events
export const sweepExpiredTrials = inngest.createFunction(
  { id: 'sweep-expired-trials', name: 'Sweep expired trials' },
  { cron: '0 * * * *' },
  async ({ step }) => {
    const expired = await step.run('find-expired', () => trialService.findExpiredSince(1));

    await step.sendEvent(
      'emit-trial-expired',
      expired.map((trial) => ({ name: 'trial/expired', data: { trialId: trial.id } })),
    );
  },
);

// Dispatch: event-driven, does the actual work for one candidate
export const handleTrialExpired = inngest.createFunction(
  { id: 'handle-trial-expired', name: 'Handle trial expired', retries: 5 },
  { event: 'trial/expired' },
  async ({ event, step }) => {
    await step.run('downgrade-account', () => billingService.downgrade(event.data.trialId));
    await step.run('notify-user', () => emailService.sendTrialExpired(event.data.trialId));
  },
);
```

One candidate failing retries on its own; it never blocks or re-runs the sweep, and it never re-processes the other 999 candidates that already succeeded.

## Typed event catalog from shared schemas

Define the event catalog with `EventSchemas().fromSchema()`, sourced from the same zod schemas the API layer validates with (see the `contracts` skill) — event payloads get the same compile-time and runtime type safety as HTTP request bodies, and a typo in `event.data.userld` is a type error instead of `undefined` at 3am:

```ts
// inngest/client.ts
import { Inngest, EventSchemas } from 'inngest';
import { z } from 'zod';
import { userCreatedEventSchema, trialExpiredEventSchema } from '@repo/contracts';

const eventSchemas = new EventSchemas().fromSchema({
  'user/created': { data: userCreatedEventSchema },
  'trial/expired': { data: trialExpiredEventSchema },
});

export const inngest = new Inngest({ id: 'my-app', schemas: eventSchemas });
```

## Money and state-mutating work: transaction + idempotency

Retries can (and will) redeliver an event — Inngest guarantees at-least-once execution, not exactly-once. Anything that mutates money or other non-idempotent state must dedupe explicitly, not just rely on "it probably won't retry":

```ts
await step.run('apply-charge', async () => {
  return db.$transaction(async (tx) => {
    // row lock prevents a concurrent retry from double-processing the same invoice
    const invoice = await tx.invoice.findUniqueOrThrow({
      where: { id: invoiceId },
      // FOR UPDATE-equivalent row lock, e.g. Prisma's `select ... for update` raw query
    });

    // idempotency check — a sentinel record proves this charge already ran
    const existing = await tx.chargeAttempt.findUnique({ where: { idempotencyKey } });
    if (existing) return existing;

    const charge = await chargeCard(invoice, idempotencyKey);
    return tx.chargeAttempt.create({ data: { idempotencyKey, chargeId: charge.id } });
  });
});
```

The sentinel record (an `idempotency_key` unique column, or similar) is what makes a redelivered event a safe no-op instead of a second charge.

## Local dev

`inngest-cli dev` runs a local dev server (default `http://localhost:8288`) with a UI for inspecting registered functions, triggering test runs, and viewing run/event history. Point it at your app's serve endpoint (e.g. `http://localhost:3000/api/inngest`) so it can discover functions.

It also exposes an MCP endpoint at `http://localhost:8288/mcp`, registered as the `inngest` entry in the project's `.mcp.json` — this lets an agent inspect functions, runs, and events directly. It's **local-only and only reachable while `inngest-cli dev` is running**; if the MCP tools time out or come back empty, check the dev server is actually up before assuming a code bug.
