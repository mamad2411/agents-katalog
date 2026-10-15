---
name: stackbone
description: >-
  Use this skill when writing the inside of a Stackbone workspace with @stackbone/sdk and eve:
  the workspace is discovered by convention from the files on disk (agents/<name>/agent.yaml +
  workflows/<name>.workflow.ts), with an optional stackbone.config.ts override via
  defineWorkspace({ agents, workflows }) that wins when present,
  authoring a durable eve agent (agent.ts with a model + build.externalDependencies, instructions.md,
  tools under tools/ via defineTool from 'eve/tools'), writing durable workflows as 'use workflow' /
  'use step' functions with sibling inputSchema/outputSchema, and reaching the ambient `stackbone` client
  from inside a tool's execute() or a workflow step — stackbone.database (Drizzle over Neon Postgres),
  stackbone.storage (file uploads), stackbone.ai (LLM chat / embeddings via OpenRouter), stackbone.rag
  (ingest + hybrid search), stackbone.config / stackbone.secrets / stackbone.prompts, stackbone.agent(id)
  to call a sibling agent, and stackbone.connection(id) to call a third-party connector — plus
  human-in-the-loop pauses via requestApproval() from @stackbone/sdk/workflow.
  Trigger on requests like: build an agent, add a tool, write a workflow, store user data, upload a file,
  call an LLM, ingest docs for RAG, pause until a human approves, call another agent, call a connector,
  read dynamic config, or add an optional stackbone.config.ts override on top of convention discovery.
  For CLI tasks (init, dev, publish, db migrate, runs, hitl, trigger), use the stackbone-cli skill instead.
  For triage of errors and stuck runs, use the stackbone-debug skill.
license: MIT
metadata:
  author: stackbone
  version: '0.4.1'
  organization: Stackbone
  date: June 2026
---

# Stackbone SDK skill

This skill covers writing code **inside** a Stackbone workspace — what the creator authors with `@stackbone/sdk` and `eve`. The workspace is discovered by convention from the files on disk (`agents/<name>/agent.yaml` + `workflows/<name>.workflow.ts`); an optional `stackbone.config.ts` is an override that wins when present. For everything around the workspace (scaffolding, the dev emulator, publishing, db migrations, triggering runs) use the **stackbone-cli** skill.

## The mental model in four sentences

- A workspace is a project that contains **agents** and **workflows**, **discovered by convention from the files on disk**: every `agents/<name>/agent.yaml` is an agent and every `workflows/<name>.workflow.ts` is a workflow. An optional `stackbone.config.ts` (default-exporting `defineWorkspace({ agents, workflows })`) is an **override that wins when present** — most projects need none. Each agent is a directory under `agents/<name>/`; each workflow is a `*.workflow.ts` module.
- An **agent** is a durable [eve](https://eve.dev/docs/introduction) agent: a model + instructions + tools that hold a conversation across turns. You author it as files under `agents/<name>/agent/` — `agent.ts` (model + build config), `instructions.md` (the system prompt), and one tool per file under `tools/`. The runtime serves it over a signed `/eve/v1/*` session API; you never write HTTP code.
- A **workflow** is durable, replayable code: a plain async function marked `'use workflow'` whose individual side-effects are marked `'use step'`. Each step is a checkpoint — kill the runtime mid-run and it resumes from the last completed step. Workflows run on the [Workflow SDK](https://workflow-sdk.dev/docs).
- All persistence lives in the agent's own Postgres (Neon): relational data, vectors (`pgvector`), full-text (`tsvector`), the approvals inbox, the prompt catalog, dynamic config. From any tool's `execute()` or any workflow step you reach it through the **ambient `stackbone` client** — `import { stackbone } from '@stackbone/sdk'` — with no `createClient()` and no credential wiring.

## Quick setup

### 1. Scaffold (CLI)

Use the **stackbone-cli** skill. `stackbone init` is **workspace-first and offline by default** — it emits only the workspace shell (an `agents/` folder, a `workflows/` folder, `package.json`, `tsconfig.json`, an `.npmrc`, `.gitignore`, a README, and the coding-agent skills) with **no `stackbone.config.ts` and no agent**, and runs no network call. A first piece is opt-in via `--with`: `empty` (shell only — the default), `agent`, `workflow`, or `workflow-agent`. Only the agent-creating kinds (`agent`, `workflow-agent`) touch the network — they register the agent in the control plane, so you must be signed in; `empty` and `workflow` are fully offline. Once you have a workspace, add more pieces with `stackbone add agent|workflow|workflow-agent <name>` — see the **stackbone-cli** skill for the full command surface.

### 2. Install the SDK (and the eve peers you use)

```sh
npm install @stackbone/sdk
```

`@stackbone/sdk` declares `eve` and `workflow` as **optional peer dependencies**. Install the ones your workspace actually uses:

```sh
npm install eve                 # to author an agent (agent.ts / tools)
npm install workflow            # to author a workflow that pauses for approval
npm install @ai-sdk/openai-compatible   # to bind the OpenRouter-compatible model
```

A tool-only agent that never imports `@stackbone/sdk/workflow` or `@stackbone/sdk/connect` never loads those peers, so `import { stackbone } from '@stackbone/sdk'` stays peer-free.

### 3. Declare the workspace (optional)

You usually **do not** write this. The workspace is discovered by convention: every `agents/<name>/agent.yaml` (whose `name:` equals the folder basename) is an agent, and every `workflows/<name>.workflow.ts` (exporting `<camelCase(name)>Workflow`) is a workflow. Add a `stackbone.config.ts` only when you need to **override** that scan — when present it wins over the convention:

```ts
// stackbone.config.ts — OPTIONAL override; only needed when convention discovery isn't enough
import { defineWorkspace } from '@stackbone/sdk';

export default defineWorkspace({
  agents: [
    { name: 'support', dir: 'agents/support' },
    { name: 'billing', dir: 'agents/billing' },
  ],
  workflows: [
    {
      name: 'onboarding',
      module: 'workflows/onboarding.workflow.ts',
      export: 'onboardingWorkflow',
    },
  ],
});
```

- An **agent** entry is `{ name, dir }`. The `name` is the agent's folder under `agents/`; `dir` is the path to that folder.
- A **workflow** entry is `{ name, module, export }`. The `name` is how you address/trigger it (`stackbone workflows schema <name>`, `POST /api/workflows/<name>/start`); `module` is the `*.workflow.ts` path; `export` is the exported function name inside it.

## Authoring an eve agent

An agent lives under `agents/<name>/agent/`:

```
agents/support/
  package.json            ← name: "support"
  agent/
    agent.ts              ← model + build config (default export = defineAgent)
    instructions.md       ← the system prompt
    tools/
      read_config.ts      ← one tool per file (default export = defineTool)
      escalate.ts
```

### `agent.ts` — the model + build config

```ts
// agents/support/agent/agent.ts
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import { defineAgent } from 'eve';

// Stackbone injects the org's managed OpenRouter sub-key as OPENROUTER_API_KEY.
// OpenRouter exposes an OpenAI-compatible API, so bind it as a provider instance.
// eve routes a provider instance directly (a BARE model string would route
// through the Vercel AI Gateway, which Stackbone does not use).
const openrouter = createOpenAICompatible({
  name: 'openrouter',
  baseURL: process.env.OPENROUTER_BASE_URL ?? 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
});

export default defineAgent({
  model: openrouter('anthropic/claude-haiku-4.5'),
  // A custom provider carries no context-window metadata, so declare it.
  modelContextWindowTokens: 200_000,
  // Keep @stackbone/sdk (and eve) external so the agent shares ONE invocation
  // context. Inlining the SDK gives the agent a second copy of the SDK's
  // invocation-context AsyncLocalStorage and per-run logs arrive with no run id.
  // `stackbone publish` enforces this — an agent that omits it aborts the build.
  build: { externalDependencies: ['@stackbone/sdk', 'eve*'] },
});
```

> Import `defineAgent` from **`eve`** (the agent's model + build config) — not from `@stackbone/sdk`.

The agent's name comes from the `name:` field in **`agents/<name>/agent.yaml`** — and it **must equal the folder basename** (that match is the key the convention scan resolves agents by). You do not write the name in `agent.ts`. The system prompt lives in `agents/<name>/agent/instructions.md`.

### A tool — `agents/<name>/agent/tools/<tool>.ts`

One tool per file, default-exporting `defineTool` from `eve/tools`. The tool's `execute()` is where you reach the ambient `stackbone` client.

```ts
// agents/support/agent/tools/read_config.ts
import { defineTool } from 'eve/tools';
import { stackbone, z } from '@stackbone/sdk';

export default defineTool({
  description:
    "Return the agent's current dynamic configuration. Call to confirm how the " +
    'agent is configured before replying.',
  inputSchema: z.object({}),
  async execute() {
    const greeting = await stackbone.config.get('greeting');
    const all = await stackbone.config.getAll();
    return {
      greeting: greeting.error ? null : greeting.data,
      all: all.error ? null : all.data,
    };
  },
});
```

A tool with arguments destructures them from the `execute` parameter (validated against `inputSchema`):

```ts
export default defineTool({
  description: 'Escalate this lead to a human sales rep.',
  inputSchema: z.object({
    leadId: z.string().describe('CRM contact id'),
    reason: z.string().describe('Short reason for the hand-off'),
  }),
  async execute({ leadId, reason }) {
    await stackbone.database.insert(escalations).values({ leadId, reason });
    return { leadId, tagged: 'needs-human' };
  },
});
```

> **Deep dive:** [agents/authoring.md](agents/authoring.md) — full agent layout, the tool pattern, and the eve doc references.

## Authoring a durable workflow

A workflow is a plain async function in `workflows/<name>.workflow.ts`, marked `'use workflow'`, that declares its contract with **sibling `inputSchema` / `outputSchema` exports** (the build harvests them — there is no `defineWorkflow` wrapper). Side-effects live in helper functions marked `'use step'`.

```ts
// workflows/onboarding.workflow.ts
import { z } from '@stackbone/sdk';
import { stackbone } from '@stackbone/sdk';

// THE contract — sibling exports next to the bare function. The build harvests
// these into the manifest + a live validator. The input parameter type is
// DERIVED from inputSchema (z.infer), so there is no second type that can drift.
export const inputSchema = z.object({
  userId: z.string(),
  email: z.email(),
  plan: z.enum(['free', 'pro', 'scale']),
});

// Output is DECLARED (not inferred from the TS return type — that loses fields).
export const outputSchema = z.object({
  userId: z.string(),
  subject: z.string(),
  body: z.string(),
  tips: z.array(z.string()),
});

type OnboardingInput = z.infer<typeof inputSchema>;

export async function onboardingWorkflow(input: OnboardingInput) {
  'use workflow';

  const signup = await validateSignup(input); // step 1 — deterministic
  const tips = await askSupportForTips(signup.plan); // step 2 — calls the support AGENT
  const saved = await persistWelcome(signup.userId, tips); // step 3 — side effect (idempotent)
  return saved;
}

async function validateSignup(input: OnboardingInput) {
  'use step';
  if (!input.email.includes('@')) throw new Error(`Invalid email: ${input.email}`);
  return { userId: input.userId, plan: input.plan };
}

async function persistWelcome(userId: string, tips: { tips: string[] }) {
  'use step'; // deterministic side effect (DB / email). Keep it idempotent on userId.
  await stackbone.database.insert(welcomes).values({ userId, tips: tips.tips });
  return { userId, subject: 'Welcome', body: '...', tips: tips.tips };
}
```

Rules that matter for workflows:

- **`'use workflow'`** marks the durable orchestrator. The body should be cheap, deterministic glue — it replays on resume. Do the I/O in steps.
- **`'use step'`** marks a checkpoint that runs **once**, is persisted, and is retried on failure. Make every step **idempotent** — on retry it may run again.
- **Sibling `inputSchema` / `outputSchema`** are the workflow's public contract. The build extracts them so Studio renders an input form and the emulator validates `start` payloads. Derive the input parameter type with `z.infer<typeof inputSchema>`; declare `outputSchema` explicitly.
- See `/docs/concepts/workflows` (in the wiki) for the durable-execution model in depth.

> **Deep dive:** [workflows/authoring.md](workflows/authoring.md) — the directive rules, the typed contract, pauses, and every trigger path.

## Triggering and scheduling workflows

From inside a workflow, start another workflow **by name** through the `stackbone.workflows` surface on the ambient client (these bind on dispatch, so they run from a workflow body, not a tool):

```ts
import { stackbone } from '@stackbone/sdk';

const { runId } = await stackbone.workflows.start('reconcile', { invoiceId }); // fire-and-forget → its own run
const summary = await stackbone.workflows.startAndWait<Summary>('summarize', { docId }); // durably wait for the output
await stackbone.workflows.schedule('daily-digest', { scope: 'all' }, '0 9 * * *'); // dynamic cron, idempotent by name
```

- `stackbone.workflows.start(name, input)` enqueues an independent run and returns `{ runId }`; `stackbone.workflows.startAndWait(name, input)` suspends durably until it finishes and returns the validated output. `name` is the `*.workflow.ts` convention name (narrowed to the workspace's declared names once `stackbone dev` has generated `.stackbone/workflows.d.ts`); input is validated against the target's schema before anything is enqueued.
- `stackbone.workflows.schedule(name, input, cron)` / `.unschedule(name)` / `.listSchedules()` manage **dynamic** cron triggers (one per `name` — re-scheduling replaces it). For schedules that ship with the workspace, prefer the declarative form — `export const schedules = [{ cron, input }]` next to the workflow — which the build harvests and the runtime reconciles on deploy.
- `ingestDocuments({ collection, content, contentType })` is the durable RAG-ingest trigger (it stages the content, then runs the reserved `rag-ingest` workflow).
- The shell mirror is `stackbone workflows start <name>` (see the **stackbone-cli** skill).

## The ambient `stackbone` client

`import { stackbone } from '@stackbone/sdk'` — the single handle for every agent surface, reachable from any tool `execute()` or workflow step. It resolves config from the injected environment lazily on first use; there is no `createClient()` and you never pass connection strings.

| Surface                    | What it is                                                                                                  | Envelope                                 |
| -------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `stackbone.database`       | **Native Drizzle ORM** + `postgres-js` over the agent's Neon (vectors with `pgvector`, FTS with `tsvector`) | rows / **throws** (no `{ data, error }`) |
| `stackbone.storage`        | File uploads / downloads / signed URLs (R2 in prod, MinIO in dev)                                           | `{ data, error }`                        |
| `stackbone.ai`             | LLM chat / embeddings / vision via OpenRouter (300+ models). Stream long completions.                       | `{ data, error }`                        |
| `stackbone.rag`            | Ingest + hybrid (`pgvector` + `tsvector`) retrieval; tables are platform-provisioned                        | `{ data, error }`                        |
| `stackbone.config`         | Read dynamic config the operator edits in Studio: `get(key)` / `getAll()`                                   | `{ data, error }`                        |
| `stackbone.secrets`        | Read operator-managed encrypted secrets: `get(name)` / `getMany(names)`                                     | `{ data, error }`                        |
| `stackbone.prompts`        | Versioned prompt catalog: `get()` / `compile(key, vars)` / `list()` / `create()` / …                        | `{ data, error }`                        |
| `stackbone.approval`       | Agent-local HITL records (used by `requestApproval` under the hood — see below)                             | `{ data, error }`                        |
| `stackbone.agent(id)`      | Call a sibling agent by name — opens a session, sends a turn (see below)                                    | `result()` → `{ data, status }`          |
| `stackbone.connection(id)` | Call a third-party connector by id (Stackbone Connect — see below)                                          | `Promise<output>` / **throws** by code   |

The one rule across every surface: **destructure `{ data, error }` and handle both branches.** The sole exception is `stackbone.database` (native Drizzle — it returns rows and throws).

```ts
const { data, error } = await stackbone.storage
  .from('avatars')
  .upload(file, { contentType: 'image/png' });
if (error) throw new Error(error.message); // propagate the failure
// success: `data` is typed
```

`throw` to propagate a failure; branch on `error.code` to handle a known case and `return` instead. **Never swallow the `error` branch.** The error envelope is `{ code, message, meta? }` (`SdkError`).

> `stackbone.database` is native Drizzle: tables are `pgTable` objects from `agents/<name>/schema.ts`; helpers (`eq`, `and`, `sql`, …) come from `@stackbone/sdk/db`. Awaiting a query returns the typed rows and **throws** on error — there is no envelope.

### Calling a sibling agent — `stackbone.agent(id)`

From a workflow step (or another agent's tool), open a session and send a turn. The turn's structured reply is validated against the `outputSchema` you pass.

```ts
async function askSupportForTips(plan: string) {
  'use step';
  const session = stackbone.agent('support').session();
  const response = await session.send<{ tips: string[] }>({
    message: `A customer joined the "${plan}" plan. Give up to 3 onboarding tips.`,
    outputSchema: z.object({ tips: z.array(z.string()) }),
  });
  const result = await response.result(); // { data, status }
  return result.data ?? { tips: [] };
}
```

`session().send(...)` returns a response you collect with `result()` (`{ data, status }` where `status` is `'completed' | 'failed' | 'waiting'`) or iterate with `for await...of` for the live stream. `id` is an agent name resolved by the workspace convention scan — the `agents/<name>/` folder basename (its `agent.yaml` `name:`) — optionally overridden by a `stackbone.config.ts`.

> **Deep dive:** [workflow-agents/authoring.md](workflow-agents/authoring.md) — calling an agent from a workflow, with the structured (`result()`) and streaming (`for await`) reply forms.

### Calling a connector — `stackbone.connection(id)`

Call a third-party connector operation directly — no agent, no model in the loop. The credential is brokered by Stackbone Connect; you only pass the operation arguments.

```ts
async function sendMail(input: { to: string; subject: string; body: string }) {
  'use step';
  // Typed from the connector's schema (generated into .stackbone/connect.d.ts on
  // `stackbone dev`). Equivalent to .call('sendMail', input) at runtime.
  const output = await stackbone.connection('stub-mail').sendMail(input);
  return { sent: true, output };
}
```

- `stackbone.connection(id).<operation>(args)` is the typed form (once `.stackbone/connect.d.ts` is generated); `stackbone.connection(id).call('<operation>', args)` is the always-available dynamic escape hatch (use it for a dotted operation id like `'chat.postMessage'`).
- The call returns the operation output and **throws** a `ConnectorCallError` on failure — match `err.code` (the broker taxonomy: `invalid_args`, `credential_error`, `timeout`, …), never `instanceof`.
- See `/docs/concepts/connect` (in the wiki) for the broker model and how operators register connector credentials. To author a richer eve connection (e.g. an OpenAPI connection with brokered auth) use `connect(connectorId)` from `@stackbone/sdk/connect`.

## Human-in-the-loop — `requestApproval`

A workflow that needs a person to decide pauses **durably** with `requestApproval()` from `@stackbone/sdk/workflow` (NOT the main barrel — the subpath statically imports the `workflow` peer). It writes a row the Studio inbox shows, then races the human decision against a timeout.

```ts
// workflows/refund.workflow.ts — pause until a human decides.
// inputSchema / outputSchema are declared as usual (see the workflow example above).
import { requestApproval } from '@stackbone/sdk/workflow';

export async function refundWorkflow(input: z.infer<typeof inputSchema>) {
  'use workflow';

  const decision = await requestApproval({
    token: input.approvalToken, // resume key, unique per approval in a run
    topic: 'refund',
    payload: { orderId: input.orderId, amount: input.amount },
    title: 'Approve refund',
    timeout: '24h', // ISO duration or ms
    fallback: 'reject', // applied if the timeout wins the race
  });

  // Gate the side effect on a fresh approval; decision.timedOut means the fallback fired.
  if (decision.status !== 'approved') return { refunded: false, decision: decision.status };

  await performRefund(input.orderId, input.amount); // a 'use step' — never runs without a fresh decision
  return { refunded: true, decision: decision.status };
}
```

`requestApproval` returns `{ status: 'approved' | 'rejected', payload?, timedOut }`. **It must be called from the workflow body, never inside a `'use step'`** — pausing on a hook is a workflow primitive that suspends the run. The decision-resume path (`stackbone hitl approve/reject`, the Studio inbox) is in the **stackbone-cli** skill. For advanced cases the subpath also re-exports the raw `defineHook` + `sleep` from `workflow` as an escape hatch.

## Typed config — `config.schema.ts`

Declare your dynamic config once at the workspace root in `config.schema.ts` as a Zod object:

```ts
// config.schema.ts
import { z } from 'zod';

export const configSchema = z.object({
  greeting: z.string().min(1).describe('How the agent opens a conversation'),
  maxRetries: z.number().int().min(0).max(10).default(3),
  replyTone: z.enum(['formal', 'casual', 'friendly']).default('friendly'),
  rateLimit: z.object({ perMinute: z.number().int().min(1).default(60) }),
});
```

`stackbone dev` extracts ONE JSON Schema from it — which draws the Config editor form in Studio and validates writes — **and** generates `.stackbone/config.d.ts`, which augments `@stackbone/sdk`'s `ConfigRegistry`. As a result `stackbone.config.get('greeting')` is **key-checked and typed**: a typo is a compile error, `greeting` is `string`, `replyTone` is the enum union, and `rateLimit` is a navigable nested object.

## Injected environment (read by the runtime)

The runtime injects these at boot; **never hardcode them, never ask the user for them, never declare them in `agent.yaml`.** They are platform-managed.

| Category    | Variables                                                                       |
| ----------- | ------------------------------------------------------------------------------- |
| Identity    | `AGENT_ID`, `WORKSPACE_ID`, `STACKBONE_INSTALLATION_ID`                         |
| Persistence | `DATABASE_URL`, `STACKBONE_SECRET_KEY`                                          |
| Security    | `HMAC_SECRET` (signs the runtime's session/workflow/connector calls)            |
| Workflows   | `WORKFLOW_REDIS_URL` (durable step state), `AGENT_URLS` (sibling-agent routing) |
| LLM         | `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL` (managed sub-key, passthrough cost) |

> Observability needs **no env var from you**: the runtime auto-instruments outbound calls and correlates `console.*` output with the right run. There is no observability surface to configure.

## agent.yaml — the per-agent manifest

`stackbone.config.ts` is an **optional workspace-level override** — by default the workspace is discovered by convention from the files on disk, and the config only wins when present. Each agent carries its own per-agent `agent.yaml` (model engine, database paths, RAG embedding model, required connectors, seeded automations); this is the manifest the convention scan reads, and its `name:` must equal the folder basename. The schema is `.strict()` — an unknown key fails parse. See [agent-yaml.md](agent-yaml.md) for the full reference.

## Authoring guides

The full authoring reference for each workspace piece:

| Piece                                                | Doc                                                          |
| ---------------------------------------------------- | ------------------------------------------------------------ |
| An eve agent (model, instructions, tools)            | [agents/authoring.md](agents/authoring.md)                   |
| A durable workflow (`'use workflow'` / `'use step'`) | [workflows/authoring.md](workflows/authoring.md)             |
| A workflow that calls an agent (streaming or direct) | [workflow-agents/authoring.md](workflow-agents/authoring.md) |

## Per-surface deep dives

The full method shapes and worked examples for each ambient surface live in the leaf docs — read the one your task touches:

| Task                                                      | Doc                                                              |
| --------------------------------------------------------- | ---------------------------------------------------------------- |
| Drizzle queries, transactions, vectors, full-text, paging | [database/sdk-integration.md](database/sdk-integration.md)       |
| Uploads, the `key` handle, public/signed URLs             | [storage/sdk-integration.md](storage/sdk-integration.md)         |
| Chat/embeddings, **streaming** long completions, vision   | [ai/sdk-integration.md](ai/sdk-integration.md)                   |
| Ingest and hybrid retrieval                               | [rag/sdk-integration.md](rag/sdk-integration.md)                 |
| Durable HITL pauses (`requestApproval`)                   | [hitl/sdk-integration.md](hitl/sdk-integration.md)               |
| Versioned prompt catalog + `compile()`                    | [prompts/sdk-integration.md](prompts/sdk-integration.md)         |
| Connector operations (typed + `.call`)                    | [connections/sdk-integration.md](connections/sdk-integration.md) |
| Triggering & scheduling workflows, background work        | [scheduling/sdk-integration.md](scheduling/sdk-integration.md)   |

## Branch the backend for risky changes

If a change depends on a schema migration, a new RLS policy, a `rag.embeddingModel` change, or anything else that could leave a deployed agent broken — work on a `stackbone dev` session first (your local install, isolated Postgres + Redis + MinIO) before touching the cloud. See the **stackbone-cli** skill (`dev` reference) for the loop.

## Important notes

- **No HTTP framework choice, no Dockerfile.** The runtime serves the agent (`/eve/v1/*`) and the workflows (`/api/workflows/*`); you write neither HTTP routes nor a Dockerfile. The platform buildpack builds the container from your workspace.
- **Keep `@stackbone/sdk` (and eve) external in `build.externalDependencies`.** Inlining the SDK gives the agent a second copy of the invocation-context store and per-run logs lose their run id. `stackbone publish` enforces this.
- **Steps must be idempotent.** A `'use step'` is retried on failure and replayed on resume — code it so running twice is safe.
- **The agent owns its data.** Stackbone never reads or writes the agent's Neon directly.
- **`requestApproval` lives on `@stackbone/sdk/workflow`**, not the main barrel — importing it from `@stackbone/sdk` will not resolve.
