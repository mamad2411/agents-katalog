# Anthropic SDK for TypeScript — Reference

Official TypeScript/JavaScript client for the Claude API. Full async/await support with streaming, structured outputs, tool use, and the complete Managed Agents / Claude Agent SDK surface.

**Package:** `@anthropic-ai/sdk`
**Source:** `anthropics/anthropic-sdk-typescript` (public)
**Local clone:** `/home/user/anthropics/anthropic-sdk-typescript`
**Docs:** `platform.claude.com/docs/en/api/sdks/typescript`

---

## Installation & Setup

```sh
npm install @anthropic-ai/sdk
```

```ts
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env['ANTHROPIC_API_KEY'], // default; can omit
});
```

**Browser support** (disabled by default to avoid exposing the key):
```ts
const client = new Anthropic({ dangerouslyAllowBrowser: true });
```

---

## Runtime Requirements

- **Node.js** 20 LTS or later
- **Deno** v1.28.0+
- **Bun** 1.0+
- **Cloudflare Workers**
- **Vercel Edge Runtime**
- **Jest** 28+ with `"node"` environment
- **Nitro** v2.6+
- **TypeScript** >= 5.0
- React Native is **not** supported

---

## Core API Namespaces

### Messages (`client.messages`)

```ts
// Create a message
const msg = await client.messages.create({
  model: 'claude-opus-5',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello, Claude' }],
});
console.log(msg.content);

// Count tokens before sending
const count = await client.messages.countTokens({ model: 'claude-opus-5', messages: [...] });

// Parse with structured output (Zod)
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';
import { z } from 'zod';
const Schema = z.object({ answer: z.string() });
const parsed = await client.messages.parse({
  model: 'claude-opus-5',
  max_tokens: 512,
  messages: [{ role: 'user', content: 'Answer in JSON.' }],
  output_config: { format: zodOutputFormat(Schema) },
});
console.log(parsed.parsed_output?.answer);
```

### Message Batches (`client.messages.batches`)

```ts
const batch = await client.messages.batches.create({ requests: [...] });
const result = await client.messages.batches.retrieve(batch.id);
for await (const item of await client.messages.batches.results(batch.id)) { ... }
await client.messages.batches.cancel(batch.id);
```

Methods: `create`, `retrieve`, `list`, `delete`, `cancel`, `results`

### Models (`client.models`)

```ts
const model = await client.models.retrieve('claude-opus-5');
const list = await client.models.list();
```

### Files (`client.files`)

```ts
const file = await client.files.upload({ file: fs.createReadStream('data.pdf') });
const meta = await client.files.retrieveMetadata(file.id);
const content = await client.files.download(file.id);
await client.files.delete(file.id);
```

Methods: `list`, `delete`, `download`, `retrieveMetadata`, `upload`

### Skills (`client.skills`)

```ts
const skill = await client.skills.create({ name: 'my-skill', ... });
await client.skills.retrieve(skill.id);
await client.skills.list();
await client.skills.delete(skill.id);
```

#### Skill Versions (`client.skills.versions`)

```ts
await client.skills.versions.create(skillId, { ... });
await client.skills.versions.retrieve(version, { skill_id: skillId });
await client.skills.versions.list(skillId);
await client.skills.versions.delete(version, { skill_id: skillId });
```

---

## Streaming

```ts
// High-level stream with events and helpers
const stream = client.messages.stream({
  model: 'claude-opus-5',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Tell me a story.' }],
});

stream.on('text', (delta, snapshot) => process.stdout.write(delta));
stream.on('message', (msg) => console.log('\nFinal:', msg));

const finalMsg = await stream.finalMessage();
const text = await stream.finalText();

// Low-level async iterable (less memory)
const raw = await client.messages.create({ stream: true, ... });
for await (const chunk of raw) { ... }

// Cancel mid-stream
stream.abort();
// or: break from for await loop
```

### MessageStream Events

| Event | Payload |
|-------|---------|
| `connect` | — |
| `streamEvent` | `(event, snapshot: Message)` |
| `text` | `(delta: string, snapshot: string)` |
| `inputJson` | `(partial: string, snapshot: unknown)` |
| `contentBlock` | `(block: ContentBlock)` |
| `message` | `(message: Message)` |
| `finalMessage` | `(message: Message)` |
| `error` | `(error: AnthropicError)` |
| `abort` | `(error: APIUserAbortError)` |
| `end` | — |

See: `examples/streaming.ts`, `examples/raw-streaming.ts`

---

## Structured Outputs

Three schema formats supported:

```ts
// Zod (recommended)
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod';
import { z } from 'zod';
const Schema = z.object({ primes: z.array(z.number()) });
const msg = await client.messages.parse({
  model: 'claude-sonnet-5',
  max_tokens: 512,
  messages: [{ role: 'user', content: 'List 3 primes.' }],
  output_config: { format: zodOutputFormat(Schema) },
});
console.log(msg.parsed_output?.primes); // [2, 3, 5]

// JSON Schema
import { jsonSchemaOutputFormat } from '@anthropic-ai/sdk/helpers/json-schema';
const format = jsonSchemaOutputFormat({ type: 'object', properties: { ... } });

// Standard Schema (Valibot, ArkType, ...) — beta namespace
import { betaStandardSchemaOutputFormat } from '@anthropic-ai/sdk/helpers/beta/standard-schema';
const msg = await client.beta.messages.parse({ ..., output_config: { format: betaStandardSchemaOutputFormat(schema) } });
```

See: `examples/structured-outputs-zod.ts`, `examples/structured-outputs-json-schema.ts`, `examples/structured-outputs-streaming.ts`

---

## Tool Use & Tool Runner

### Defining Tools

```ts
// Zod tool
import { betaZodTool } from '@anthropic-ai/sdk/helpers/beta/zod';
import { z } from 'zod';

const weatherTool = betaZodTool({
  name: 'get_weather',
  inputSchema: z.object({ location: z.string() }),
  description: 'Get current weather',
  run: async (input) => `Weather in ${input.location}: sunny, 72°F`,
});

// JSON Schema tool
import { betaTool } from '@anthropic-ai/sdk/helpers/beta/json-schema';
const calcTool = betaTool({
  name: 'calculator',
  input_schema: { type: 'object', properties: { a: { type: 'number' }, b: { type: 'number' } }, required: ['a','b'] },
  description: 'Add two numbers',
  run: (input) => String(input.a + input.b),
});

// Standard Schema tool (Valibot etc.)
import { betaStandardSchemaTool } from '@anthropic-ai/sdk/helpers/beta/standard-schema';
```

### Tool Runner

```ts
// One-shot — await the final result directly
const finalMsg = await client.beta.messages.toolRunner({
  model: 'claude-sonnet-5',
  max_tokens: 1000,
  messages: [{ role: 'user', content: 'What is the weather in SF?' }],
  tools: [weatherTool],
});

// Iterate — observe each intermediate message
const runner = client.beta.messages.toolRunner({ ..., tools: [weatherTool] });
for await (const msg of runner) { console.log(msg); }
const finalMsg = await runner;

// Streaming tool runner
const runner = client.beta.messages.toolRunner({ ..., stream: true, tools: [calcTool] });
for await (const msgStream of runner) {
  for await (const event of msgStream) { ... }
  const msg = await msgStream.finalMessage();
}
```

### BetaToolRunner Methods

| Method | Purpose |
|--------|---------|
| `done()` | Await completion, return final message |
| `runUntilDone()` | Eagerly read stream, return final message |
| `setMessagesParams(params\|fn)` | Update conversation params mid-run |
| `pushMessages(...msgs)` | Add messages to history |
| `compactBeforeNextTurn(config?)` | Schedule compaction after current turn |
| `setRequestOptions(opts\|fn)` | Update headers/abort signal |
| `generateToolResponse(signal?)` | Get tool response for last assistant message |
| `params` | Read-only current params |

### Cancellation

```ts
const controller = new AbortController();
const runner = client.beta.messages.toolRunner({ ..., tools }, { signal: controller.signal });
setTimeout(() => controller.abort(), 5000);
const result = await runner;
```

### Context Compaction in Tool Runner

```ts
const runner = client.beta.messages.toolRunner({
  model: 'claude-sonnet-5',
  max_tokens: 1000,
  betas: ['compact-2026-09-04'],
  messages: [...],
  tools: [searchTool],
});
for await (const msg of runner) {
  if (msg.usage.input_tokens > 100_000) runner.compactBeforeNextTurn();
}
```

### ToolError

```ts
import { ToolError } from '@anthropic-ai/sdk/resources/beta/messages';
throw new ToolError('Something went wrong');
throw new ToolError([{ type: 'text', text: 'Error details' }, { type: 'image', ... }]);
```

See: `examples/tools.ts`, `examples/tools-helpers-zod.ts`, `examples/tools-helpers-advanced.ts`, `examples/tools-helpers-advanced-streaming.ts`

---

## Beta API Namespaces

All beta resources are under `client.beta.*` and require `?beta=true`.

### Beta Messages

```ts
// Extended message create with beta features
const msg = await client.beta.messages.create({ model: 'claude-opus-5', max_tokens: 1024, messages: [...] });
const count = await client.beta.messages.countTokens({ ... });
const parsed = await client.beta.messages.parse({ ..., output_config: { format: betaStandardSchemaOutputFormat(schema) } });
```

### Beta Message Batches (`client.beta.messages.batches`)

Same interface as `client.messages.batches`.

### Agents (`client.beta.agents`)

```ts
const agent = await client.beta.agents.create({ name: 'my-agent', ... });
await client.beta.agents.retrieve(agent.id);
await client.beta.agents.update(agent.id, { ... });
await client.beta.agents.list();
await client.beta.agents.archive(agent.id);
await client.beta.agents.versions.list(agent.id);
```

### Environments (`client.beta.environments`)

```ts
const env = await client.beta.environments.create({ ... });
await client.beta.environments.retrieve(env.id);
await client.beta.environments.update(env.id, { ... });
await client.beta.environments.list();
await client.beta.environments.delete(env.id);
await client.beta.environments.archive(env.id);
```

#### Environment Work (`client.beta.environments.work`)

```ts
const work = await client.beta.environments.work.retrieve(envId);
await client.beta.environments.work.update(envId, { ... });
await client.beta.environments.work.list(envId);
await client.beta.environments.work.ack(envId, workId);
await client.beta.environments.work.heartbeat(envId, workId);
await client.beta.environments.work.poll(envId);
await client.beta.environments.work.stats(envId);
await client.beta.environments.work.stop(envId, workId);
```

### Sessions (`client.beta.sessions`)

```ts
const session = await client.beta.sessions.create({ ... });
await client.beta.sessions.retrieve(session.id);
await client.beta.sessions.update(session.id, { ... });
await client.beta.sessions.list();
await client.beta.sessions.delete(session.id);
await client.beta.sessions.archive(session.id);
```

#### Session Events (`client.beta.sessions.events`)

```ts
await client.beta.sessions.events.list(sessionId);
await client.beta.sessions.events.send(sessionId, { ... });
await client.beta.sessions.events.stream(sessionId);
const runner = client.beta.sessions.events.toolRunner(sessionId, { tools: [...] });
for await (const call of runner) { console.log(call.name, call.isError ? 'error' : 'ok'); }
```

#### Session Resources (`client.beta.sessions.resources`)

Methods: `retrieve`, `update`, `list`, `delete`, `add`

#### Session Threads (`client.beta.sessions.threads`)

```ts
await client.beta.sessions.threads.retrieve(threadId, { session_id: sessionId });
await client.beta.sessions.threads.list(sessionId);
await client.beta.sessions.threads.archive(threadId, { session_id: sessionId });
await client.beta.sessions.threads.events.list(threadId, { session_id: sessionId });
await client.beta.sessions.threads.events.stream(threadId, { session_id: sessionId });
```

### Deployments (`client.beta.deployments`)

```ts
const dep = await client.beta.deployments.create({ ... });
await client.beta.deployments.update(dep.id, { ... });
await client.beta.deployments.list();
await client.beta.deployments.archive(dep.id);
await client.beta.deployments.pause(dep.id);
await client.beta.deployments.run(dep.id, { ... });
await client.beta.deployments.unpause(dep.id);
```

### Deployment Runs (`client.beta.deploymentRuns`)

```ts
await client.beta.deploymentRuns.retrieve(runId);
await client.beta.deploymentRuns.list();
```

### Vaults (`client.beta.vaults`)

```ts
const vault = await client.beta.vaults.create({ ... });
await client.beta.vaults.update(vault.id, { ... });
await client.beta.vaults.list();
await client.beta.vaults.archive(vault.id);
```

#### Vault Credentials (`client.beta.vaults.credentials`)

```ts
const cred = await client.beta.vaults.credentials.create(vaultId, { ... });
await client.beta.vaults.credentials.retrieve(credId, { vault_id: vaultId });
await client.beta.vaults.credentials.update(credId, { vault_id: vaultId, ... });
await client.beta.vaults.credentials.list(vaultId);
await client.beta.vaults.credentials.delete(credId, { vault_id: vaultId });
await client.beta.vaults.credentials.archive(credId, { vault_id: vaultId });
await client.beta.vaults.credentials.mcpOAuthValidate(credId, { vault_id: vaultId, ... });
```

### Memory Stores (`client.beta.memoryStores`)

```ts
const store = await client.beta.memoryStores.create({ ... });
await client.beta.memoryStores.update(store.id, { ... });
await client.beta.memoryStores.archive(store.id);
```

#### Memories (`client.beta.memoryStores.memories`)

```ts
const mem = await client.beta.memoryStores.memories.create(storeId, { ... });
await client.beta.memoryStores.memories.retrieve(memId, { memory_store_id: storeId });
await client.beta.memoryStores.memories.update(memId, { memory_store_id: storeId, ... });
await client.beta.memoryStores.memories.list(storeId);
await client.beta.memoryStores.memories.delete(memId, { memory_store_id: storeId });
```

#### Memory Versions (`client.beta.memoryStores.memoryVersions`)

Methods: `retrieve`, `list`, `redact`

### Beta Files (`client.beta.files`)

Same interface as `client.files` but via beta endpoint.

### Beta Skills (`client.beta.skills`)

```ts
const skill = await client.beta.skills.create({ ... });
await client.beta.skills.retrieve(skill.id);
await client.beta.skills.list();
await client.beta.skills.delete(skill.id);
```

#### Beta Skill Versions (`client.beta.skills.versions`)

```ts
await client.beta.skills.versions.create(skillId, { ... });
await client.beta.skills.versions.retrieve(version, { skill_id: skillId });
await client.beta.skills.versions.list(skillId);
await client.beta.skills.versions.delete(version, { skill_id: skillId });
await client.beta.skills.versions.download(version, { skill_id: skillId }); // -> Response
```

### Webhooks (`client.beta.webhooks`)

Parse and verify incoming webhook payloads. Covers events for agents, deployments, environments, memory stores, sessions (including status, threads), and vaults/credentials.

```ts
const event = client.beta.webhooks.parseUnverified(body);
const verified = client.beta.webhooks.unwrap(body);
```

Types include: `BetaWebhookEvent`, `BetaWebhookEventData`, `BetaWebhookSessionCreatedEventData`, `BetaWebhookDeploymentRunSucceededEventData`, etc.

### User Profiles (`client.beta.userProfiles`)

```ts
const profile = await client.beta.userProfiles.create({ ... });
await client.beta.userProfiles.retrieve(profileId);
await client.beta.userProfiles.update(profileId, { ... });
await client.beta.userProfiles.list();
const url = await client.beta.userProfiles.createEnrollmentURL(profileId, { ... });
```

### Dreams (`client.beta.dreams`)

Async background processing jobs over sessions and memory stores.

```ts
const dream = await client.beta.dreams.create({ ... });
await client.beta.dreams.retrieve(dream.id);
await client.beta.dreams.list();
await client.beta.dreams.archive(dream.id);
await client.beta.dreams.cancel(dream.id);
```

### Tunnels (`client.beta.tunnels`)

```ts
const tunnel = await client.beta.tunnels.create({ ... });
await client.beta.tunnels.retrieve(tunnel.id);
await client.beta.tunnels.list();
await client.beta.tunnels.archive(tunnel.id);
const token = await client.beta.tunnels.revealToken(tunnel.id);
const newToken = await client.beta.tunnels.rotateToken(tunnel.id);
// Certificates
await client.beta.tunnels.certificates.create(tunnelId, { ... });
await client.beta.tunnels.certificates.retrieve(certId, { tunnel_id: tunnelId });
await client.beta.tunnels.certificates.list(tunnelId);
await client.beta.tunnels.certificates.archive(certId, { tunnel_id: tunnelId });
```

### Organization (`client.beta.organization`)

```ts
const org = await client.beta.organization.retrieve();

// API Keys
await client.beta.organization.apiKeys.retrieve(keyId);
await client.beta.organization.apiKeys.update(keyId, { ... });
await client.beta.organization.apiKeys.list();

// External Keys
await client.beta.organization.externalKeys.create({ ... });
await client.beta.organization.externalKeys.validate(keyId);

// Federation
await client.beta.organization.federation.issuers.create({ ... });
await client.beta.organization.federation.rules.create({ ... });
await client.beta.organization.federation.rules.workspaces.add(ruleId, { ... });

// Invites
await client.beta.organization.invites.create({ ... });
await client.beta.organization.invites.delete(inviteId);

// Service Accounts
await client.beta.organization.serviceAccounts.create({ ... });
await client.beta.organization.serviceAccounts.workspaces.add(accountId, { ... });

// Users
await client.beta.organization.users.retrieve(userId);
await client.beta.organization.users.update(userId, { role: 'admin' });
await client.beta.organization.users.list();
```

---

## Self-Hosted Environment Runner

Run managed-agent sessions locally (Node 22+ required for agent toolset).

```ts
import Anthropic from '@anthropic-ai/sdk';
import { betaAgentToolset20260401 } from '@anthropic-ai/sdk/tools/agent-toolset/node';

const client = new Anthropic();

// One-stop: poll → run toolset for each session → loop
await client.beta.environments.work
  .worker({
    environmentId: process.env.ANTHROPIC_ENVIRONMENT_ID!,
    environmentKey: process.env.ANTHROPIC_ENVIRONMENT_KEY!,
    workdir: '/workspace',
    tools: (ctx) => [...betaAgentToolset20260401(ctx), myCustomTool],
  })
  .run(AbortSignal.timeout(60 * 60_000));

// Handle single pre-claimed work item (e.g. from `ant worker poll --on-work`)
await client.beta.environments.work.worker({ workdir: '/workspace', tools }).handleItem();
```

**Agent Toolset** (`agent_toolset_20260401`): `bash`, `read`, `write`, `edit`, `glob`, `grep`

Individual tool factories: `betaBashTool`, `betaReadTool`, `betaWriteTool`, `betaEditTool`, `betaGlobTool`, `betaGrepTool`

```ts
// Extend or filter the standard toolset
const tools = [...betaAgentToolset20260401(ctx), myCustomTool];
const tools = betaAgentToolset20260401(ctx).filter((t) => t.name !== 'grep');
```

See: `examples/managed-agents-self-hosted-sandbox-worker.ts`, `examples/managed-agents-worker-dispatch.ts`

---

## Examples Index

| File | What it covers |
|------|----------------|
| `examples/demo.ts` | Basic message creation |
| `examples/streaming.ts` | MessageStream API with events |
| `examples/raw-streaming.ts` | Low-level async iterable streaming |
| `examples/thinking.ts` | Extended thinking |
| `examples/thinking-stream.ts` | Streaming with extended thinking |
| `examples/tools.ts` | Basic tool use |
| `examples/tools-streaming.ts` | Streaming with tools |
| `examples/tools-helpers-zod.ts` | Zod-based tool helpers |
| `examples/tools-helpers-json-schema.ts` | JSON Schema tool helpers |
| `examples/tools-helpers-standard-schema.ts` | Standard Schema (Valibot) tools |
| `examples/tools-helpers-advanced.ts` | BetaToolRunner advanced iteration |
| `examples/tools-helpers-advanced-streaming.ts` | Streaming tool runner |
| `examples/tools-helpers-memory.ts` | Tools with memory stores |
| `examples/structured-outputs-zod.ts` | Structured output with Zod |
| `examples/structured-outputs-json-schema.ts` | Structured output with JSON Schema |
| `examples/structured-outputs-standard-schema.ts` | Standard Schema structured output |
| `examples/structured-outputs-streaming.ts` | Streaming structured output |
| `examples/structured-outputs-raw.ts` | Raw structured output |
| `examples/count-tokens.ts` | Token counting |
| `examples/batch-results.ts` | Message Batches API |
| `examples/agents.ts` | Agents (managed) |
| `examples/agents-comprehensive.ts` | Comprehensive agent example |
| `examples/agents-with-files.ts` | Agents + file uploads |
| `examples/managed-agents-self-hosted-sandbox-worker.ts` | Full self-hosted environment worker |
| `examples/managed-agents-worker-dispatch.ts` | Worker dispatch pattern |
| `examples/managed-agents-observe-tool-calls.ts` | Observe tool calls |
| `examples/managed-agents-streaming-deltas-manual.ts` | Manual streaming deltas |
| `examples/autoCompaction.ts` | Auto context compaction |
| `examples/web-search.ts` | Web search tool |
| `examples/web-search-stream.ts` | Streaming web search |
| `examples/mcp.ts` | MCP integration |
| `examples/fallbacks.ts` | Error fallback patterns |
| `examples/middleware.ts` | Request middleware |
| `examples/cancellation.ts` | Request cancellation |

---

## Setup

```bash
cd /home/user/anthropics/anthropic-sdk-typescript
npm install
export ANTHROPIC_API_KEY=sk-ant-...
npx ts-node examples/demo.ts
```

---

## Prompts

### Build a streaming chatbot

```
Using /home/user/anthropics/anthropic-sdk-typescript/examples/streaming.ts and helpers.md:
Build a multi-turn chatbot with streaming output.
Implement clean text rendering and graceful abort on Ctrl+C.
```

### Implement tool use with agentic loop

```
Using /home/user/anthropics/anthropic-sdk-typescript/examples/tools-helpers-advanced.ts:
Build a [use case] agent that uses [tools].
Use betaZodTool for input validation, BetaToolRunner for the loop,
and handle ToolError for structured error responses.
```

### Structured output from Claude

```
Using /home/user/anthropics/anthropic-sdk-typescript/examples/structured-outputs-zod.ts:
Extract [schema] from [input] using client.messages.parse() with zodOutputFormat.
Show the full Zod schema definition and parsed output access.
```

### Set up a self-hosted environment worker

```
Using /home/user/anthropics/anthropic-sdk-typescript/examples/managed-agents-self-hosted-sandbox-worker.ts
and helpers.md (Self-Hosted Environment Runner section):
Set up a worker that polls [environment] and runs the agent toolset for each session.
Show how to extend the toolset with [custom tool] and handle cancellation.
```

### Query organization / admin data

```
Using the Organization beta namespace:
List all API keys in my organization and show their workspace scopes.
Also show how to manage service accounts and federation rules.
```
