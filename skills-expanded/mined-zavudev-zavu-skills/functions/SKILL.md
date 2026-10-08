---
name: functions
description: Build serverless TypeScript functions on Zavu Cloud — declare agents + tools in code with defineAgent / defineTool, deploy with `npx zavudev deploy`, debug with `npx zavudev agents executions`. Use this skill whenever the user wants code-driven AI agents, custom tool handlers, or event-driven business logic.
---

# Zavu Functions

Zavu Functions = serverless TypeScript on Zavu Cloud + a declarative framework for AI agents.

```ts
import { defineAgent, defineTool } from "@zavudev/functions"

defineAgent({
  senderId: process.env.SENDER_ID!,
  name: "Bella",
  provider: "zavu",
  model: "openai/gpt-5.6-luna",
  prompt: "You are Bella, host at the restaurant. Be brief.",
})

defineTool({
  name: "check_availability",
  description: "Get free reservation slots for a date.",
  parameters: {
    type: "object",
    properties: { date: { type: "string" }, partySize: { type: "number" } },
    required: ["date", "partySize"],
  },
  handler: async ({ date, partySize }) => {
    return { available: true, slots: ["19:00", "21:00"] }
  },
})
```

That's a full agent + tool. `npx zavudev deploy` reconciles the live state.

## Project shape

Decide this before you write anything, because restructuring later is the
expensive kind of rework.

```
my-agent/
├── index.ts        entrypoint: defineAgent + defineTool live here
├── lib/orders.ts   imported by index.ts, deployed with it
├── package.json    npm dependencies, installed at build time
└── .zavu/          created by the CLI; do not edit
```

- **Several files are fine.** `deploy` starts at `index.ts` and uploads every
  file it reaches through relative imports. Split the prompt, the tools and the
  business logic however you like.
- **Only what is imported ships.** A file nothing imports stays on your machine,
  so tests and scratch work are not deployed.
- **npm packages are not files.** Declare them under `dependencies` in
  `package.json`; they are installed and bundled for you.
- **Limits:** 200 files, 900,000 bytes total. Paths above the project root
  (`../shared/x.ts`), `node_modules/`, and names starting with `__zavu` are
  refused. To share code across projects, publish it as an npm package.
- `--source <file>` names a different entrypoint.

## When to use Functions vs the imperative AI Agent API

| Use case | Use |
|---|---|
| Customer wants a code-first agent with custom tool handlers in their own language | **Functions** |
| Tools need to query the user's database, call internal APIs, or transform data before returning | **Functions** |
| User wants reproducible config from a git repo (one source of truth) | **Functions** |
| User wants no-code config via the dashboard | imperative `senders.agent.create` API (see `ai-agent` skill) |
| User needs event-driven handlers (`message.inbound`, `broadcast.status_changed`) without dashboard wiring | **Functions** |

If the user mentions writing code, `defineAgent`, `defineTool`, `npx zavudev deploy`, or "serverless" — use this skill. Otherwise route to `ai-agent`.

## CLI as primary interface

Functions are managed entirely via the `zavu` CLI, not API calls. Install once:

```sh
# `npx zavudev@latest` needs no install and always runs the current version.
# Pin nothing: an old CLI is the most common source of "the API does not
# support this".
npx zavudev@latest --version

npx zavudev login
```

`npx zavudev login` opens the browser and stores credentials in `~/.zavu/credentials.json`.

## Factory agents

The fastest way to a working voice or text agent: pull a ready-made one into your
codebase, then deploy. Each factory agent is a Zavu Function whose `index.ts`
declares the agent with `defineAgent` and its skills with `defineTool` — so what
you pull is real, editable code you own.

```sh
npx zavudev agents catalog                            # list the factory agents
npx zavudev agents pull fermi --sender <senderId>     # scaffold ./fermi, register it, set SENDER_ID
cd fermi
npx zavudev deploy
```

`npx zavudev agents catalog` lists each agent's id, name, whether it's `voice`, tool
count, and category. `npx zavudev agents pull <id>` scaffolds `./<id>` (override with
`--dir <path>`); `--sender <senderId>` sets the `SENDER_ID` secret so `npx zavudev deploy`
works immediately — omit it and run `npx zavudev fn secrets set SENDER_ID <senderId>`
first. Voice agents come with the `voice` block pre-filled; edit `index.ts` and
redeploy to iterate.

`npx zavudev agents init` runs the whole setup as one guided command: it creates the
sender (buying a phone number if you want), pulls a factory agent, and sets
`SENDER_ID`.

The sender's channels are what the agent answers on, and each connects from the
CLI. Voice and SMS work as soon as the sender has a number; the rich channels
connect with one command each:

```sh
npx zavudev telegram connect --sender <senderId> --token <botFatherToken>
npx zavudev email-domains add example.com                       # then publish DNS + `verify`
```

## Full lifecycle

### 1. Scaffold

```sh
npx zavudev fn init --name order-bot --template blank
cd order-bot
```

Templates available: `blank`, `restaurant-booking`. Run `zavu fn init --help` for the
current list — it is the authority, not this page.

**Prefer a factory agent when one fits.** `zavu agents catalog` lists production
agents (support, lead capture, booking) and `zavu agents pull <id>` scaffolds one
complete with its prompt, its skills and, for voice agents, its voice config.

The init writes `index.ts`, `package.json`, and a `.zavu/config.json` that links this directory to a Function record in the user's project. Once linked, every subsequent command auto-resolves the function.

### 2. Set secrets

Secrets are encrypted env vars injected into the function at deploy time.

```sh
npx zavudev fn secrets set SENDER_ID jx7abc123def456
npx zavudev fn secrets set DATABASE_URL "postgres://..."
npx zavudev fn secrets list
npx zavudev fn secrets unset OLD_KEY
```

Get the sender ID from `npx zavudev senders list`.

### 3. Author the agent + tools

Edit `index.ts`:

```ts
import { defineAgent, defineTool, defineFunction } from "@zavudev/functions"

// Four fields are required: name, provider, model, and the prompt (under
// `prompt` or `systemPrompt`). A declaration missing any of them is SKIPPED —
// the deploy still succeeds, and you get a function with no agent. `description`
// and `instructions` are not fields.
defineAgent({
  senderId: process.env.SENDER_ID!,  // Optional: omit to declare it standalone
                                      // and connect senders afterwards.
  name: "Bella",
  provider: "zavu",              // Zavu's AI gateway (charged from project balance)
                                  // Or "openai" / "anthropic" / "google" / "mistral" with BYOK + apiKey
  model: "openai/gpt-5.6-luna",   // For "zavu" provider, prefix with the underlying provider
  prompt: "You are Bella…",       // System prompt
  channels: ["whatsapp"],         // Optional: default ["*"] = all channels the sender supports
                                  // Listing a channel the sender does NOT have does
                                  // not add it — it just never fires. Prefer the
                                  // default unless you are deliberately excluding one.
  // apiKey: process.env.OPENAI_API_KEY  // only for BYOK providers (openai / anthropic / google / mistral)
})

defineTool({
  name: "lookup_order",
  description: "Get current status of an order. Use when the customer asks about an order they placed.",
  parameters: {
    type: "object",
    properties: { orderId: { type: "string" } },
    required: ["orderId"],
  },
  handler: async (args, ctx) => {
    // ctx: { projectId, functionId, slug, log, memory, contactId?, conversationId?,
    //        senderId?, channel?, messageId?, contactPhone?, sessionId?, callId? }
    const res = await fetch(`https://pos.example.com/orders/${args.orderId}`, {
      headers: { Authorization: `Bearer ${process.env.POS_API_KEY}` },
    })
    return await res.json()
  },
})

// Optional: handle raw events (message.inbound from triggers, HTTP calls).
// NOT needed if you only declare agent + tools.
// The object form is what binds events — `on` is the subscription.
export default defineFunction({
  on: ["message.inbound"],
  handler: async (event, ctx) => {
    ctx.log("got event", event.type)
  },
})
```

### 4. Deploy

```sh
npx zavudev deploy
```

Output:

```
✓ Deployed in 6.4s
  Agents synced:
    + Bella
  Tools synced:
    + lookup_order
```

| Marker | Meaning |
|---|---|
| `+ name` | Created |
| `~ name` | Existed and was written |
| `= name (unchanged)` | Existed and nothing differed |

The markers distinguish the two cases: a redeploy with no edit prints `=`, and
`~` means something about that agent or tool was actually rewritten. Older
backends printed `~` for everything that already existed and never emitted `=`,
so if you are on one of those, a redeploy with no edit looks identical to one
that rewrote the prompt.

Either way the markers describe what the deploy *wrote*, not what the agent now
*says*. To verify a change reached the model, ask it:

```sh
npx zavudev agents test --agent <agentId> --message "<something your edit changes>" --json
```

Put a distinctive word in the prompt you edited and check it comes back. That is
one command, it charges nothing, and unlike the deploy summary it answers the
question you actually have.

**Read the lines above the ✓.** Warnings print before the success line and cover
the cases where a green deploy did not do what it looks like: a manifest probe
that threw (nothing was synced, and the command exits non-zero), tools attached
to an agent whose channels will never call them, or a second agent landing on a
sender that already has one — where only the first will ever answer.

There is no ✓ at all when an agent ends up with **no** reachable channel: it
declared `channels` its sender cannot receive, so it is deployed, enabled, and
unable to receive a single message. The deploy prints the agent and the
mismatch and exits non-zero. Fix it by changing the agent's `channels` or by
connecting that channel to the sender (`npx zavudev senders get <id>` lists
what it actually has).

### Local development

The scaffold is a real TypeScript project: `zavu init` and `zavu agents pull`
write a `tsconfig.json` and a `package.json` that declares `@zavudev/functions`,
`typescript` and `@types/node` as devDependencies.

### Exposing a function over HTTP

A function that needs its own endpoint — a webhook you host, a tool URL you
control — is created with `--http`:

```sh
npx zavudev fn init --template blank --http
npx zavudev agents pull kepler --sender "$SENDER_ID" --http
```

The URL exists once something is deployed behind it. `deploy` prints it, and you
can ask for it any time:

```sh
npx zavudev fn info                 # status, and the public URL when HTTP is on
npx zavudev fn info --json          # same, machine-readable
```

Toggling it on an existing function is a CLI action too — it applies to the
already-deployed function, no redeploy:

```sh
npx zavudev fn http enable
npx zavudev fn http disable
```

#### The HTTP event is not a Zavu event

This is the one shape that will cost you a deploy if you assume it. An HTTP
invocation delivers the **raw API Gateway v2 payload**, not the `{ type, data }`
event that triggers deliver. `event.type` and `event.data` are `undefined`, and
the body arrives as a **string** under `event.body`:

```json
{
  "version": "2.0",
  "rawPath": "/",
  "headers": { "content-type": "application/json" },
  "requestContext": { "http": { "method": "POST" } },
  "body": "{\"action\":\"availability\"}",
  "isBase64Encoded": false
}
```

So read it like this, and check the method from `requestContext`:

```ts
export default defineFunction({
  handler: async (event: any) => {
    const method = event?.requestContext?.http?.method ?? "GET"
    const raw = event?.isBase64Encoded
      ? Buffer.from(event.body ?? "", "base64").toString("utf8")
      : event?.body
    const payload = typeof raw === "string" && raw ? JSON.parse(raw) : {}
    return { statusCode: 200, body: JSON.stringify({ ok: true, method, payload }) }
  },
})
```

Typing the handler as a Zavu event compiles cleanly and then reads `undefined`
in production — the failure the runtime package's own types warn about.

**Run `npm install` before anything local.** Nothing resolves until you do:

```sh
cd <your-function-dir>
npm install
```

Without it, `zavu fn invoke` fails with `Cannot find module '@zavudev/functions'`
and `npx tsc` silently fetches an unrelated deprecated package instead of the
compiler. Deploy works either way — the runtime layer supplies the module in
production and it is never shipped from your machine — so this only bites the
local loop, which is exactly the loop you use to verify your work.

Commit `.zavu/` — it holds the `functionId`, and there is no command to look one
up, so a teammate who clones without it cannot deploy.

`zavu fn invoke` runs your code with **Bun**. Install it from https://bun.sh.
Every other command runs under plain Node.

### 5. Test

**Local invocation (skip cloud round-trip):**

```sh
# Call a tool handler with synthetic args
npx zavudev fn invoke --tool lookup_order --args '{"orderId":"ORD-001"}'

# Simulate an inbound event for defineFunction
npx zavudev fn invoke --event message.inbound --data '{"from":"+14155551234","text":"hi"}'
```

`--args` is checked against the tool's own `parameters` schema before the handler
runs — required fields, types, and closed `enum` values. A mismatch fails with
the exact field and the expected shape, and never calls the handler:

```
✗ arguments do not match the tool's schema:
   • missing required "orderId"
   • "score" must be one of "hot" | "warm" | "cold", got "banana"
  expected: { orderId: string, score: hot|warm|cold, notes: string? }
```

If the project's dependencies are not installed, this stops with a note telling
you to run `npm install` rather than surfacing Bun's raw module-resolution error.

**Secrets are not injected.** The API returns each secret's key and last four
characters, never its value, so `fn invoke` cannot fetch them — including with
`--live`. Put them in a `.env` next to `index.ts` (it is read automatically) or
export them in your shell. Without that, a handler that reads
`process.env.SOMETHING` takes its unconfigured branch and returns a plausible
failure like `{ ok: false, reason: "not_configured" }`, which reads as a bug in
your code and is not one. The command warns and names the missing keys.

`--live` makes the SDK calls real instead of stubbing them. Everything is mocked
by default, so nothing is sent until you ask for it.

Exit codes are worth branching on: **2** means you called it wrong (unknown
tool, arguments that fail the schema), **1** means the handler itself threw, **0**
means it ran. A green run therefore means the handler actually executed with
valid input, not merely that nothing crashed.

**Test the agent's brain without sending anything:**

```sh
npx zavudev agents list                # your agents, with their ids
npx zavudev agents test --agent <agentId> --message "where is order ORD-001?"
```

Prints what the agent would reply, plus tokens, latency and how many knowledge
chunks it used. Nothing is delivered and nothing is charged, so it is safe to run
on every prompt edit.

> **Tools run on every channel** — plain text (SMS/WhatsApp/Telegram), voice,
> and inside a flow's `tool` step. A text agent asked to look something up calls
> the tool and answers with real data (up to 5 tool rounds per reply).
> By default `agents test` is the exception: it offers the tools, reports which
> one the agent chose with what arguments, and stops there. So the reply you see
> is the agent talking about a lookup that never happened — any figure in it was
> invented, and the run warns you so.

To see the real loop — model picks a tool, the handler answers, the model
replies with the result:

```sh
npx zavudev agents test --agent <agentId> --message "where is order ORD-001?" --execute-tools
```

The handlers run for real, so whatever they do (charge, write, notify) happens.
Nothing is delivered to a customer, but the side effects are not simulated. Each
call is printed with whether it answered:

```
  ✓ get_order_status
  ✗ charge_card: HTTP 500
```

A tool that errors is worth as much as one that works: the agent saw the error
and answered around it, which is what a customer would have received. And if
the agent calls nothing at all, the run says so — a confident reply with zero
tool calls is the failure this flag exists to catch.

Use `fn invoke --tool` to exercise one handler in isolation, without the model.

**End-to-end:** send a real message to the sender's WhatsApp/SMS/Telegram number,
or place a call for a voice agent. The agent runs the LLM and replies on the same
channel.

### 6. Debug

When something fails, walk the chain top-down:

```sh
# 1. Did the inbound reach the agent?
npx zavudev agents executions list --sender <senderId>

# 2. Detail of any failed run
npx zavudev agents executions get <executionId> --sender <senderId>

# 3. Live tool handler logs (your console.log calls)
npx zavudev fn logs --tail
```

The `--json` flag on `executions list` returns the full payload including `errorMessage` for parseable diagnostics.

**When the deploy itself fails**, the build output is printed under
`Build output:` — the unresolved import, the syntax error, the package that
would not install. The one-line status above it is a summary and rarely names
anything you can act on; the lines under `Build output:` do. The same text stays
on the deployment as `buildLogs`, readable over REST at
`GET /v1/functions/deployments/{deploymentId}` (`npx zavudev fn versions list`
gives you the ids).

## defineAgent reference

```ts
defineAgent({
  senderId: string,              // Required. The sender that receives inbound + dispatches the agent.
  name: string,                  // Required. Displayed in dashboard.
  provider: "zavu" | "openai" | "anthropic" | "google" | "mistral",
  model: string,                 // For "zavu": prefix with underlying provider e.g. "openai/gpt-5.6-luna"
  prompt: string,                // System prompt.
  apiKey?: string,               // Required for non-"zavu" providers.
  channels?: string[],           // Default ["*"] = whatever the sender has. See below.
  messageTypes?: string[],       // Default ["text"]. Filter by message type.
  temperature?: number,          // 0-2.
  maxTokens?: number,            // Cap on output tokens.
  contextWindowMessages?: number,// Past N messages included as context. Default 10.
  sessionTimeoutMinutes?: number,// Reset conversation context after N minutes. Default 60.
  includeContactMetadata?: boolean, // Inject contact's metadata into the system prompt. Default true.
  enabled?: boolean,             // Default true.
  voice?: VoiceConfig,           // Add to make the agent answer phone calls. See "Voice agents".
})
```

## Voice agents

Add a `voice` block to a `defineAgent` to make it answer phone calls. When
present with `enabled: true`, the sender's number is answered by the agent. The
LLM runs **co-located in the voice network** for the lowest latency, independent
of the text `model` — set `voice.model` to pick the call model, or omit it to
derive one from the text `model`. Removing the block reverts the agent to
text-only on the next deploy.

```ts
defineAgent({
  senderId: process.env.SENDER_ID!,
  name: "Fermi",
  provider: "zavu",
  model: "openai/gpt-5.6-luna",      // text model
  channels: ["voice", "whatsapp"],
  voice: {
    enabled: true,
    model: "openai/gpt-4o",         // co-located voice model (optional; derived from `model` if omitted)
    greeting: "Hi, I'm Fermi. How can I help?",
    language: "en",                 // BCP-47; auto-detected if omitted
    interruptible: true,            // caller can barge in
    maxCallDurationMinutes: 10,
  },
  prompt: "You are Fermi…",
})
```

### voice reference

```ts
voice: {
  enabled: boolean,              // Required. true = answer/place calls; removing the block reverts to text-only.
  model?: string,                // Co-located call model, e.g. "openai/gpt-4o". Derived from the text model if omitted.
  greeting?: string,             // Opening line. Max 1000 chars. If omitted, the agent waits for the caller.
  greetings?: Record<string, string>, // Per-language greeting keyed by language tag: { es: "Hola…" }. Used when the caller's language differs from the one `greeting` is written in. Factory agents ship with this set.
  language?: string,             // BCP-47 (e.g. "en", "es", "pt-BR"). Auto-detected if omitted.
  ttsVoiceId?: string,           // Voice used for speech synthesis.
  voiceSpeed?: number,           // Speech rate 0.5–1.5. Default 1.0.
  interruptible?: boolean,       // Caller can barge in while the agent speaks. Default true.
  maxCallDurationMinutes?: number, // Hard cap on call length. Default 15.
  maxIdleSeconds?: number,       // End the call after this much silence (5–300). Default 30.
  voicemailAction?: "hangup" | "leave_message", // On answering-machine detection (outbound). Default "hangup".
  voicemailMessage?: string,     // Spoken when voicemailAction is "leave_message". Falls back to greeting.
  transferPhoneNumber?: string,  // E.164. Gives the agent a tool to transfer the call to a human.
}
```

Voice requires the **Voice Agents** feature enabled for your team and a phone
number assigned to the sender. An **out-of-range** value makes
`npx zavudev deploy` warn and ship the agent as text-only rather than fail — fix the
value and redeploy.

A **misspelled or unknown** key inside the voice block is a different matter: it
is dropped without a warning and the deploy exits 0, so `interruptable` buys you
nothing and says nothing. Confirm the block landed the way you wrote it with
`npx zavudev agents get <agentId>` rather than trusting a green deploy.

## Knowledge base (RAG) in code

`defineAgent` declares it, so an agent that answers from documents is one file
and one deploy. No separate API call.

```ts
defineAgent({
  senderId: process.env.SENDER_ID!,
  name: "Ada",
  provider: "zavu",
  model: "openai/gpt-5.6-luna",
  prompt: "Answer from the store policies. If they do not cover it, say so.",
  knowledgeBase: {
    name: "Store policies",
    documents: [
      { title: "Returns", content: "# Returns\n\nUnopened: 30 days. Opened: 14 days if faulty." },
      { title: "Shipping", content: "# Shipping\n\nFree over $50, 3-5 business days." },
    ],
  },
})
```

Deploy is the source of truth: a document you remove is deleted, one whose
content changed is re-embedded, and an unchanged one is left alone so a
redeploy costs nothing. Documents are matched by `title`, so renaming replaces.

```
Knowledge bases:
  + Store policies (knowledge base)
  documents sync in the background; check with `agents knowledge-bases documents list`
```

The deploy lists the knowledge base, not each document: documents sync after it
returns, so a per-document line there would report nothing had changed whether
or not anything had.

**Verify it retrieves, do not assume:**

```sh
npx zavudev agents test --sender "$SENDER_ID" --message "can I return an opened item?"
```

The reply reports how many knowledge chunks it used. **Zero on an agent that has
documents means the answer was not grounded**, which reads exactly like a
correct answer.

## Flows in code

`defineFlow` declares a deterministic conversation in the same file as the
agent. Reach for it where the model must not improvise: a fixed sequence of
questions, a branch on the answer, a tool call with the collected values.

```ts
import { defineAgent, defineTool, defineFlow } from "@zavudev/functions"

defineFlow({
  name: "Repair intake",
  trigger: { type: "keyword", keywords: ["broken", "repair"] },
  steps: [
    {
      id: "ask_issue",
      type: "collect",
      config: { variable: "issue", prompt: "What is wrong with it?" },
      nextStepId: "open",
    },
    {
      id: "open",
      type: "tool",
      config: { toolName: "create_ticket", params: { issue: "{{issue}}" } },
      nextStepId: "done",
    },
    { id: "done", type: "message", config: { text: "Logged." } },
  ],
})
```

Only `keyword` and `always` triggers are matched by the engine. Step shapes are
in the `ai-agent` skill.

Four things specific to declaring a flow in code:

- **It arrives disabled.** A flow intercepts real conversations, so writing one
  and turning it on are separate decisions. Pass `enabled: true` for the first
  deploy, or run
  `npx zavudev agents flows update <flowId> --sender "$SENDER_ID" --enabled`.
- **Later deploys never change `enabled`.** Pausing a flow during an incident
  survives a redeploy.
- **The tool a step names must exist on the agent.** `defineTool` in the same
  file is enough, since tools reconcile first. A step naming a missing tool is
  reported and that flow is skipped; the rest of the deploy still lands.
- **Two things are never touched:** a flow with the same name that this function
  did not create, and a flow a contact is currently standing in. Both are
  reported rather than overwritten or deleted.

## Multiple senders in code

`senderId` is the primary. `senderIds` lists the rest:

```ts
defineAgent({
  senderId: process.env.SENDER_ID!,
  senderIds: [process.env.SUPPORT_SENDER_ID!],
  name: "Ada",
  provider: "zavu",
  model: "openai/gpt-5.6-luna",
  prompt: "Be brief.",
})
```

Connect-only. A sender you stop listing stays connected and is reported, because
disconnecting one silently stops a live number from being answered. Disconnect
with `DELETE /v1/agents/{agentId}/senders/{senderId}` when you mean it.

Documents live inline and the deploy caps source at ~900KB. Bigger than that,
use `npx zavudev agents knowledge-bases documents add --content-file ./manual.md` instead.

## Several files per function

Split a function across files and import between them:

```ts
// index.ts
import { formatOrder } from "./lib/orders"
```

`npx zavudev deploy` starts at the entrypoint (`index.ts` by default, or
`--source <file>`) and uploads every file it reaches through relative imports.
Files nothing imports are not deployed, so tests and scratch work stay local.
The build resolves the imports between the uploaded files.

Refused paths: above the project root (`../shared/x.ts`), `node_modules/`, and
names starting with `__zavu`. Limits: 200 files, 900,000 bytes in total.

npm dependencies are separate — put them in `package.json` under `dependencies`
and they are installed and bundled.

To deploy a whole repository on every push instead:

```sh
npx zavudev fn git link acme/my-agent --branch main
```

Over REST, send `files` (a map of path to contents) with an optional
`entrypoint`; `sourceCode` remains the shortcut for a one-file function.

## defineTool reference

```ts
defineTool({
  name: string,                  // Required. snake_case, max 64 chars.
  description: string,           // Required. The LLM reads this to decide WHEN to call the tool.
  parameters: {
    type: "object",
    properties: { /* JSON Schema */ },
    required?: string[],
  },
  handler: async (args, ctx) => any,  // Required. Return any JSON-serializable value.
  agent?: string,                // Optional: which agent owns this tool. Defaults to the only agent in the file.
  enabled?: boolean,             // Default true.
})
```

### Handler `ctx` shape

```ts
{
  projectId: string,
  functionId: string,
  slug: string,
  awsRequestId?: string,
  messageId?: string,            // ID of the triggering inbound (when called by agent)
  contactPhone?: string,
  sessionId?: string,            // Active flow session if any
  channel?: string,              // "whatsapp" | "sms" | "voice" | "email" | ...
  callId?: string,               // The voice call in progress. Voice channel only
  contactId?: string,            // The contact Zavu resolved, when it knows who is on the other side
  conversationId?: string,       // The inbox thread this conversation belongs to
  senderId?: string,             // The sender the conversation is running on
  log: (...args) => void,        // console.log proxy that appears in `npx zavudev fn logs --tail`
  memory: Memory,                // What the agent remembers. See below
}
```

### `ctx.memory` — what the agent remembers

Requires `@zavudev/functions` **0.3.0+**. Two ways to recall, one API:

```ts
// By meaning — embedded on write, retrieved semantically
await ctx.memory.contact!.add("Prefers WhatsApp over email.")
const hits = await ctx.memory.contact!.search("how they like to be reached", { minScore: 0.3 })

// By key — JSON in, JSON out
const orders = ctx.memory.contact!.collection("orders")
await orders.set("ORD-1", { status: "shipped" })
const order = await orders.get("ORD-1")   // null when absent
```

Collection keys are `A-Z a-z 0-9 . _ : @ -` — no `+`, so an E.164 phone number
is not a valid key. Use its digits (`56940560201`) or a prefix
(`phone:56940560201`) and keep the E.164 in the value.

Every read and write happens in exactly one **scope**, and scopes are isolated:

| Handle | Scope | Present when |
|---|---|---|
| `ctx.memory` | project — shared by every conversation | always |
| `ctx.memory.contact` | the person being talked to | `undefined` outside a conversation |
| `ctx.memory.conversation` | the current thread | `undefined` outside a conversation |
| `ctx.memory.forContact(id)` / `forConversation(id)` | one you name | always |

**The default is project scope.** `ctx.memory.add(fact)` with no options writes
something every other customer's conversation can then recall — use
`ctx.memory.contact` for anything about a person. `contact` and `conversation`
are optional, so handle their absence: a tool that assumes a contact throws
`MemoryScopeError` the first time it runs from a cron trigger.

Full surface, scopes, limits, the CLI and the REST API: **`memory` skill**.

## defineFunction reference (optional)

Use only if you want to handle:
- **Raw HTTP requests** (function exposed at a public URL — `zavu fn init --http` at creation, or `zavu fn http enable` on an existing one)
- **Native event triggers** (`message.inbound`, `broadcast.status_changed`, etc — configured via `npx zavudev fn triggers add`)

```ts
export default defineFunction(async (event, ctx) => {
  if (event.type === "message.inbound") {
    // event.data: { from, text, channel, messageId, ... }
  }
  return { ok: true }
})
```

## Triggers (event subscriptions)

To make `defineFunction` react to Zavu events:

```sh
npx zavudev fn triggers list
npx zavudev fn triggers add --events message.inbound --senders <senderId>
npx zavudev fn triggers add --events broadcast.status_changed --senders any
# Schedules: event type "cron" + a 5-field UTC expression (minimum 1 minute).
# The function receives { type: "cron", data: { cron } }. Several schedules
# per function are allowed (different expressions).
npx zavudev fn triggers add --events cron --cron '*/15 * * * *'
npx zavudev fn triggers add --events cron --cron '0 9 * * 1-5'   # weekdays 09:00 UTC
npx zavudev fn triggers toggle <triggerId>
npx zavudev fn triggers rm <triggerId>
npx zavudev fn triggers events       # list available event types
```

## Deploy on every push

Link a GitHub repository to the function and a push to the branch deploys it:

```sh
npx zavudev fn git link acme/order-bot --branch main
npx zavudev fn git link acme/monorepo --root apps/bot      # monorepos
npx zavudev fn git status                                   # link + last deploy
npx zavudev fn git deploy                                   # deploy the branch now
npx zavudev fn git set --no-auto-deploy                     # keep the link, ignore pushes
npx zavudev fn git unlink
```

The argument takes `owner/repo`, a github.com URL, or an SSH remote.

**The server decides how the link authenticates, and `connection` in the output
tells you which you got.** With the Zavu GitHub App installed on the account,
that command is the whole setup and private repositories work. Without it you
get a `manual` link: the command prints a payload URL and a secret to add as a
webhook in the repository yourself, and **the secret is printed exactly once** —
re-linking mints a new one.

Linking does not check the repository against GitHub, because it cannot: an
`owner/repo` that does not exist, or that the installation cannot see, is
accepted and fails on the first deploy. Read `fn git status` after the first
push rather than assuming a successful link means a working one.

Triggers use signed internal invocations (no HMAC verification needed inside the handler).

## Versions + rollback

Every `npx zavudev deploy` creates an immutable version.

```sh
npx zavudev fn versions list           # alias: npx zavudev fn history
npx zavudev fn rollback 4              # go back to version 4
```

The function metadata in the dashboard tracks the active version + lets you rollback from the UI too.

## Runtime versions

Each function pins to a specific runtime layer at first deploy. Subsequent deploys keep the same pin (immutable for stability).

```sh
npx zavudev deploy --update-runtime   # opt-in upgrade to latest runtime
```

Only opt in when there's a security advisory or feature you want — `npx zavudev deploy` without the flag is safe forever.

## Pricing model

Functions are billed by **invocation units**, memory-weighted:

| Memory | Units per call |
|---|---|
| 128 MB | 1 |
| 256 MB | 2 |
| 512 MB | 4 |
| 1024 MB | 8 |

Each plan includes a monthly quota; overage rolls into the next Stripe invoice via metered billing.

| Plan | Included units | Overage rate |
|---|---|---|
| Free | 100k | Hard cap (invocations blocked) |
| Hobby | 1M | $5 / 1M |
| Standard | 5M | $4 / 1M |
| Growth | 10M | $3 / 1M |

Set memory at function creation or via dashboard. Lower memory = cheaper. Most tool handlers fit in 128 MB.

## Common patterns

### Take over a manual agent

If the user already created an agent via the dashboard or `npx zavudev agents create`, declaring it in code with the same `senderId + name` will TAKE OVER that agent — Zavu marks it `managedByFunctionId` and the dashboard locks manual edits. The function source becomes source-of-truth.

To go back to manual control: delete the function (`npx zavudev fn delete`) and the agent is freed.

### Cleaning up a function you created

`fn delete` cascades: the Lambda, triggers, secrets, deployment history, and
every agent and tool the function owns. It asks you to type the slug back.

Non-interactively, assert the slug up front:

```sh
npx zavudev fn delete --confirm <slug>
```

This is deliberately not a blind `-y`. You still have to name the thing, so a
wrong directory or a stale id fails instead of deleting something else — which
is what makes it safe to hand to a script or an agent cleaning up after itself.

### Per-environment senders

```ts
defineAgent({
  senderId: process.env.NODE_ENV === "production"
    ? process.env.PROD_SENDER_ID!
    : process.env.DEV_SENDER_ID!,
  // ...
})
```

Then `npx zavudev fn secrets set NODE_ENV production` on prod, `... development` on dev. Same code, different agents.

### BYOK (Bring Your Own Key)

For OpenAI / Anthropic / Google / Mistral, pass `apiKey` directly:

```ts
defineAgent({
  senderId: process.env.SENDER_ID!,
  provider: "openai",
  model: "gpt-4o-mini",
  apiKey: process.env.OPENAI_API_KEY,
  prompt: "...",
})
```

`npx zavudev fn secrets set OPENAI_API_KEY sk-...`. The agent uses the key directly — no Zavu balance consumed for LLM calls.

### Pinning a tool to a specific agent (multi-agent functions)

When a function declares more than one `defineAgent`, tools default-attach to the first one. To pick explicitly:

```ts
defineTool({
  name: "lookup_order",
  agent: "Bella",   // Match by agent's name field
  // ...
})
```

### Calling Zavu APIs from inside a handler

Each function gets a scoped `ZAVU_API_KEY` injected automatically — use the SDK to call back:

```ts
import { Zavudev } from "@zavudev/sdk"

const zavu = new Zavudev({ apiKey: process.env.ZAVU_API_KEY })

defineTool({
  name: "send_followup",
  handler: async (args, ctx) => {
    await zavu.messages.send({
      to: ctx.contactPhone!,
      text: "Thanks for your order!",
    })
    return { sent: true }
  },
})
```

The auto-provisioned key has `messages:send`, `messages:read`, `contacts:read` scopes. For broader access create a manual API key and inject as a secret.

## Dashboard

`https://dashboard.zavu.dev/functions/<id>` shows tabs:

- **Code** — current draft source (editable in browser)
- **Triggers** — event subscriptions
- **Agents & Tools** — what this function manages, with deep-links to executions
- **Dependencies** — npm packages used by the bundle
- **Secrets** — encrypted env vars (values are write-only)
- **Versions** — deploy history + rollback
- **Logs** — runtime stdout/stderr of recent invocations
- **Settings** — memory, timeout, httpEnabled, delete

## Reference docs

- Overview: https://docs.zavu.dev/concepts/functions
- Quickstart: https://docs.zavu.dev/guides/functions/quickstart
- CLI reference: https://docs.zavu.dev/guides/functions/cli
- defineAgent: https://docs.zavu.dev/guides/functions/defining-agents
- defineTool: https://docs.zavu.dev/guides/functions/defining-tools
- Debugging guide: https://docs.zavu.dev/guides/functions/debugging
- Examples: https://docs.zavu.dev/guides/functions/examples/restaurant

## Constraints

- Slug: lowercase alphanumeric + hyphens, max 50 chars, unique per project.
- Source bundle: ≤ 900 KB compressed.
- Total env size: 4 KB across all secrets.
- Secret key format: `[A-Z_][A-Z0-9_]*`. Reserved prefixes: `AWS_`, `LAMBDA_`, `_HANDLER`, `_X_AMZN`.
- Timeout: ≤ 180 s (configurable, default 30 s). Event and cron invocations are
  asynchronous, so a long timeout only bounds cost. A tool called during a live
  conversation is synchronous: the reply waits, so keep those well under it.
- Memory: 128 / 256 / 512 / 1024 MB.
- Billing: by memory AND time. One call is 128 MB for one second; a bigger or
  slower function uses several, and anything under a second counts as one.
  300,000 calls a month are included on every plan, then $5 per million.
- Tools per agent: 16.
- Agents per function: no hard cap, but typically 1.

## Anti-patterns

- **Don't use the imperative `senders.agent.create` API in parallel with a managed function**. If the function declares an agent, the function owns it — manual edits get blocked.
- **Don't hardcode the `senderId`** in the source. Always read from `process.env.SENDER_ID` so the same code works across envs.
- **Don't import heavyweight deps you only use in one tool**. Each call cold-starts; trim dependencies to keep latency down.
- **Don't `console.log` secrets**. Function logs are visible to anyone with project access.
