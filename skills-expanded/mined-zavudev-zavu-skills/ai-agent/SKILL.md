---
name: ai-agent
description: Configure AI agents via the imperative SDK / REST API — for no-code dashboard setups, webhook-based tools, and knowledge bases.
---

# AI Agent

## When to Use

Use this skill when the user wants to configure AI agents through **API calls** (no source files, no deploy step) — typically from a dashboard or a backend script that creates/updates the agent imperatively.

If the user wants a **code-first agent with custom tool handlers** in TypeScript, deployed via the `zavu` CLI, route them to the **`functions`** skill instead. That path is more ergonomic, version-controlled, and has built-in deployment + debugging.

**Quick routing:**

| User says… | Use |
|---|---|
| "I want my agent's tool to query my database" / "I want to write the tool handler in code" / `defineTool` / `npx zavudev deploy` | `functions` skill |
| "Set up an agent that calls a webhook on my server" / "Configure from the dashboard" / "Create an agent via API" | this skill |
| "I'm starting from scratch and want the simplest path" | `functions` skill (recommended default) |

The imperative API documented here is fully supported and won't be deprecated, but Functions is the recommended path for most new integrations.

## Senders vs accounts (one paragraph)

A **Sender** is the API handle you pass as `Zavu-Sender`; **accounts** (a WhatsApp Business Account, a Facebook Page, a Telegram bot, a phone number) are the connections it routes — and what bills. Senders are free. Connecting an account in the dashboard auto-creates its sender; find it with `GET /v1/senders` and trust its `channels` array for what it can send. See the `channel-setup` skill for the full model.

## Architecture

```
Inbound message -> Flow check (keyword match, or an `always` flow?)
                     -> YES: Execute flow steps
                     -> NO: LLM call with system prompt + context + KB
                -> Agent generates response -> Send reply
```

## Two ways to build one

**As code, with `defineAgent`.** The agent lives in a Zavu Function, next to the
tools it calls, and `npx zavudev deploy` reconciles it. Prefer this when the agent has
tools, when it should be reviewable in a pull request, or when it is part of an
app you already deploy. See the `functions` skill for the full shape.

```typescript
import { defineAgent, defineTool } from "@zavudev/functions"

export const support = defineAgent({
  name: "Customer Support",
  senderId: process.env.SENDER_ID!,
  provider: "zavu",
  model: "openai/gpt-5.6-luna",
  // `prompt` here, `systemPrompt` over the REST API. The two paths name this
  // field differently and only `prompt` compiles against @zavudev/functions.
  prompt: "You are a helpful support agent for Acme Corp. Be concise.",
  tools: [orderStatus],
})
```

Deploy it with `npx zavudev deploy`. The reconcile output names every agent and
tool it created or updated, so read it rather than assuming: a deploy can
succeed while the declarations fail to sync, and it says so when that happens.

**Through the API**, shown below. Prefer this for one-off setup, for agents
managed by a dashboard you are building, or when there is no function to attach
the agent to.

Whichever you pick, an agent is created **disabled**. It answers nothing until
you enable it.

## Create Agent

Each sender can have one agent:

```typescript
const result = await zavu.senders.agent.create({
  senderId: "snd_abc123",
  name: "Customer Support",
  provider: "openai",
  model: "gpt-4o-mini",
  systemPrompt: "You are a helpful customer support agent for Acme Corp. Be friendly, concise, and helpful. If you don't know the answer, say so.",
  apiKey: process.env.PROVIDER_API_KEY,
  contextWindowMessages: 10,
  includeContactMetadata: true,
  triggerOnChannels: ["*"],
  triggerOnMessageTypes: ["text"],
});
console.log(result.agent.id); // agent_xxx
```

**Python:**
```python
result = zavu.senders.agent.create(
    sender_id="snd_abc123",
    name="Customer Support",
    provider="openai",
    model="gpt-4o-mini",
    system_prompt="You are a helpful customer support agent...",
    api_key=os.environ["PROVIDER_API_KEY"],
)
```

**Go:**
```go
result, err := client.Senders.Agent.Create(context.TODO(), zavudev.AgentCreateParams{
    SenderID:     zavudev.String("snd_abc123"),
    Name:         zavudev.String("Customer Support"),
    Provider:     zavudev.String("openai"),
    Model:        zavudev.String("gpt-4o-mini"),
    SystemPrompt: zavudev.String("You are a helpful customer support agent..."),
    APIKey:       zavudev.String(os.Getenv("PROVIDER_API_KEY")),
})
```

**Ruby:**
```ruby
result = client.senders.agent.create(
    sender_id: "snd_abc123",
    name: "Customer Support",
    provider: "openai",
    model: "gpt-4o-mini",
    system_prompt: "You are a helpful customer support agent...",
    api_key: ENV["PROVIDER_API_KEY"],
)
```

**PHP:**
```php
$result = $client->senders->agent->create([
    'senderId' => 'snd_abc123',
    'name' => 'Customer Support',
    'provider' => 'openai',
    'model' => 'gpt-4o-mini',
    'systemPrompt' => 'You are a helpful customer support agent...',
    'apiKey' => getenv('PROVIDER_API_KEY'),
]);
```

## Provider & Model Selection

| Provider | Models | API Key Required |
|----------|--------|-----------------|
| `openai` | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo` | Yes |
| `anthropic` | `claude-3-5-sonnet`, `claude-3-haiku` | Yes |
| `google` | `gemini-1.5-pro`, `gemini-1.5-flash` | Yes |
| `mistral` | `mistral-large`, `mistral-small` | Yes |
| `zavu` | Zavu-hosted models | No (included) |

## Update & Toggle Agent

```typescript
// Update configuration
await zavu.senders.agent.update({
  senderId: "snd_abc123",
  systemPrompt: "Updated prompt...",
  temperature: 0.7,
  maxTokens: 500,
});

// Enable/disable
await zavu.senders.agent.update({
  senderId: "snd_abc123",
  enabled: false,
});
```

## Voice

The agent can also answer and place **phone calls** through Zavu's co-located voice network (speech recognition, the agent's LLM, and speech synthesis, with real-time interruption handling). The `systemPrompt`, tools, and knowledge bases all apply on a call — voice just adds a spoken channel on top. For a code-first voice agent declared in TypeScript, use the `functions` skill instead.

**Requirements**

- The Voice Agents feature must be enabled for your team (call endpoints return `403` otherwise).
- The agent must have `voice.enabled: true`.
- **The sender must have the voice channel on.** An agent with a voice on a sender that cannot take calls looks configured and never rings. The sender needs a phone number your project owns, plus `enableVoice`:
  ```bash
  npx zavudev senders update snd_abc123 --enable-voice
  ```
  Confirm with `npx zavudev senders get snd_abc123`: `channels` must contain `voice`. That array is computed from the sender's real configuration, so it is the answer, not a stored flag.
- Not available with test-mode keys — use a live (`zv_live_...`) key.
- Calls are billed per connected minute plus telephony, deducted from your prepaid balance.

### Enable voice on an agent

Voice lives under the agent's `voice` object on `POST`/`PATCH /v1/senders/{senderId}/agent`. The SDK does not type the `voice` field yet, so set it over REST:

```bash
curl -X PATCH https://api.zavu.dev/v1/senders/snd_abc123/agent \
  -H "Authorization: Bearer $ZAVU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "voice": {
      "enabled": true,
      "greeting": "Hi, thanks for calling Acme. How can I help you today?",
      "language": "en",
      "ttsVoiceId": "aura-2-thalia-en",
      "interruptible": true,
      "maxCallDurationMinutes": 15,
      "maxIdleSeconds": 30,
      "voicemailAction": "hangup",
      "transferPhoneNumber": "+14155551234"
    }
  }'
```

| Field | Description |
|-------|-------------|
| `enabled` | Whether the agent handles calls. Required. When false, its number is not answered and outbound calls are rejected. |
| `greeting` | Opening line spoken when the call connects (max 1000). If omitted, the agent waits for the caller to speak first. |
| `language` | BCP-47 code for recognition and synthesis (e.g. `en`, `es`, `pt-BR`). Auto-detected from the recipient when omitted. |
| `ttsVoiceId` | Voice used for synthesis. List the ids with `npx zavudev agents voices` (or `GET /v1/agents/voices`); a name that is not in that list is ignored. Neutral default when omitted. |
| `interruptible` | Caller can barge in while the agent is speaking. Default `true`. |
| `maxCallDurationMinutes` | Hard call-length cap, 1-120. Default 15. |
| `maxIdleSeconds` | Silence before the agent ends the call, 5-300. Default 30. |
| `voicemailAction` | On an answering machine (outbound): `hangup` or `leave_message`. Default `hangup`. |
| `voicemailMessage` | Spoken when `voicemailAction` is `leave_message` (max 1000). Falls back to `greeting`. |
| `transferPhoneNumber` | E.164 number the agent can transfer the call to. Setting it gives the agent a transfer tool. |

Once enabled, the sender's number answers inbound calls automatically.

### Place an outbound call

The SDK has a `calls` resource since `@zavudev/sdk` 0.56.0. `to` is the only required field; `senderId` defaults to the project's default sender (whose agent must have voice enabled).

```ts
const { call } = await zavu.calls.create({
  to: "+56912345678",
  senderId: "snd_abc123",
  greeting: "Hi, this is Acme calling about your appointment.",
  maxDurationMinutes: 10,
  metadata: { campaign: "appointment_reminders" },
})
```

Over REST (or on an older SDK):

```bash
curl -X POST https://api.zavu.dev/v1/calls \
  -H "Authorization: Bearer $ZAVU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+56912345678",
    "senderId": "snd_abc123",
    "greeting": "Hi, this is Acme calling about your appointment.",
    "maxDurationMinutes": 10,
    "metadata": { "campaign": "appointment_reminders" }
  }'
```

Returns `202` with the call object as it starts dialing. `greeting` and `maxDurationMinutes` override the agent's config for this call only.

### Fetch a call and its transcript

SDK: `zavu.calls.retrieve(callId)` (includes the transcript), `zavu.calls.list({ status, direction })` (auto-paginating), `zavu.calls.hangup(callId)`. Over REST:

```bash
# Single call, including the ordered transcript
curl https://api.zavu.dev/v1/calls/call_abc123 \
  -H "Authorization: Bearer $ZAVU_API_KEY"

# List recent calls (filter by status / direction)
curl "https://api.zavu.dev/v1/calls?direction=outbound&status=completed&limit=50" \
  -H "Authorization: Bearer $ZAVU_API_KEY"

# Hang up an active (ringing or in-progress) call
curl -X POST https://api.zavu.dev/v1/calls/call_abc123/hangup \
  -H "Authorization: Bearer $ZAVU_API_KEY"
```

The transcript is a list of turns, each `{ seq, role, text }` where `role` is `user`, `assistant`, or `tool`. It is included when fetching a single call and omitted from the list. `durationSeconds`, `endReason`, `turnCount`, and `cost` populate once the call ends.

## Addressing an agent

Tools, flows and knowledge bases are reachable two ways, and they are the same
resource:

```
/v1/senders/{senderId}/agent/tools     via the sender that answers with it
/v1/agents/{agentId}/tools             via the agent itself
```

Use the agent-scoped form when the agent has no sender yet, which is what
`POST /v1/agents` creates. The sender-scoped form cannot address it, so an
agent you were told to assemble standalone used to be un-assemblable.

```bash
AGENT=$(curl -s -X POST https://api.zavu.dev/v1/agents \
  -H "Authorization: Bearer $ZAVUDEV_API_KEY" \
  -d '{"name":"Ada","provider":"zavu","model":"openai/gpt-5.6-luna","systemPrompt":"..."}' \
  | jq -r .agent.id)

curl -X POST https://api.zavu.dev/v1/agents/$AGENT/tools -d '{...}'
curl -X POST https://api.zavu.dev/v1/agents/$AGENT/knowledge-bases -d '{...}'
curl -X POST https://api.zavu.dev/v1/agents/$AGENT/senders -d "{\"senderId\":\"$SENDER_ID\"}"
curl -X PATCH https://api.zavu.dev/v1/agents/$AGENT -d '{"enabled":true}'
```

## Conversational Flows

Flows handle structured conversations (keyword triggers, data collection):

```typescript
const result = await zavu.senders.agent.flows.create({
  senderId: "snd_abc123",
  name: "Lead Capture",
  description: "Capture lead information from interested prospects",
  trigger: {
    type: "keyword",
    keywords: ["info", "pricing", "demo"],
  },
  steps: [
    {
      id: "welcome",
      type: "message",
      config: { text: "Thanks for your interest! Let me get some info." },
      nextStepId: "ask_name",
    },
    {
      id: "ask_name",
      type: "collect",
      config: { variable: "name", prompt: "What's your name?" },
      nextStepId: "ask_email",
    },
    {
      id: "ask_email",
      type: "collect",
      config: { variable: "email", prompt: "What's your email?" },
      nextStepId: "confirm",
    },
    {
      id: "confirm",
      type: "message",
      config: { text: "Thanks {{name}}! We'll reach out at {{email}}." },
    },
  ],
  enabled: true,
  priority: 10,
});
```

### Trigger Types

| Type | Description |
|------|-------------|
| `keyword` | Matches specific keywords in message (case-insensitive substring) |
| `intent` | Message expresses the intent described in `trigger.intent`, judged for meaning rather than words |
| `always` | Runs on every inbound message not already inside a flow |

For `intent`, write one plain sentence describing what the contact wants, in any
language: `{ type: "intent", intent: "asks where their order is" }`. Rules that
decide which flow starts:

- A `keyword` or `always` flow with a higher `priority` wins without the intent
  being considered. Give intent flows the higher number, or an `always` flow
  above them means they never start.
- An intent flow starts only on a clear match. Otherwise the next `keyword` or
  `always` flow in priority order starts, and if there is none the agent answers.
- At most 12 intent flows are considered per message (the 12 highest-priority).
  An intent is cut at 300 characters.
- If the classifier is unavailable, the message is handled as if no intent
  matched: the contact is still answered, the flow does not start.
- Exact tokens such as "STOP" or an order number carry no intent. Use `keyword`.

`manual` is accepted by the API and stored on the flow, and nothing starts it: a
flow created with it never triggers, and nothing reports that.

A `transfer` step sends its message, marks the session transferred, and
**silences the agent for that contact** until a person answers. Their messages
still arrive and show in the inbox; the agent just stops replying. Any outbound
message you send them ends the handoff and the agent resumes. Nobody is notified
for you, though: `notifyWebhook` and `reason` are accepted and never read, so put
a `tool` step before the transfer if your team needs a ping.

A `collect` step's `date` validation accepts any text including `tomorrow`. Constrain a date with `choice`, or
validate it in your own tool.

Flow sessions do not expire. A contact who stops answering halfway resumes at
the same step whenever they write again, with the variables they had.

### Step Types

| Type | Description |
|------|-------------|
| `message` | Send a message |
| `collect` | Collect user input into a variable |
| `condition` | Branch based on conditions |
| `tool` | Call a webhook tool |
| `llm` | Make an LLM call |
| `transfer` | Transfer to human agent |

### The `tool` step, and the field that looks like an id

```typescript
{
  id: "save_lead",
  type: "tool",
  config: {
    toolName: "create_lead",   // the tool's name, or its id
    action: "call",
    params: { email: "{{email}}", source: "whatsapp" },
    storeResultAs: "lead",
  },
  nextStepId: "confirm",
}
```

`config.toolId` is the original spelling and still works. Either field is
accepted, and either one may hold the tool's name or its id: `toolId` was read
as a name for a long time while the dashboard wrote real ids into it, so both
shapes exist in the wild and both resolve.

Values wrapped in `{{ }}` are replaced with data collected earlier in the flow;
anything else is passed through literally. Omit `params` for a tool that takes
none. The tool must already exist on the agent before the flow runs.

A step pointing at a tool the agent does not have ends the session as
**abandoned** and logs the misconfiguration. It is not counted as a completed
flow, and nothing is said to the contact: the plain agent picks the conversation
up from their next message.

### Flow Operations

```typescript
// List flows
const flows = await zavu.senders.agent.flows.list({ senderId: "snd_abc123" });

// Update flow
await zavu.senders.agent.flows.update({
  senderId: "snd_abc123",
  flowId: "flow_abc123",
  enabled: false,
});

// Duplicate flow
await zavu.senders.agent.flows.duplicate({
  senderId: "snd_abc123",
  flowId: "flow_abc123",
  newName: "Lead Capture (Copy)",
});

// Delete flow
await zavu.senders.agent.flows.delete({
  senderId: "snd_abc123",
  flowId: "flow_abc123",
});
```

## Booking skills you do not have to build

`check_availability` and `book_meeting` are hosted by Zavu: no endpoint, no
hosting, no secret. They read and write one calendar per project (Cal.com or
Google Calendar), and they behave identically on a call and in a thread.

They are added from the dashboard, in the agent's **Tools** tab under
**Library**, along with the calendar connection itself. There is no REST or SDK
surface for them yet, so do not tell a user to add one with the API.

What matters when a booking agent uses them: `book_meeting` only reports a
booking when the calendar accepted it. A Cal.com event type that requires
confirmation answers `pending`, and the skill tells the agent to say the time is
held but not confirmed. Never write a prompt that instructs the agent to
announce a confirmation before the tool result says so.

## Webhook Tools

Tools let the agent call your backend during conversations.

> **Which channels call them: all of them.** Tools are offered to the model on
> voice, on plain text (WhatsApp, SMS, Telegram, email), and inside a flow's
> `tool` step. All three dispatch through the same executor, so a tool cannot
> behave differently per channel. The model may chain up to five tool rounds in
> one reply, and you are billed for the tokens the whole loop uses.
>
> Reach for a flow when the sequence must be deterministic, not because text
> cannot call tools. It can.
>
> Verify per execution rather than assuming: `toolCalls: 0` on an agent that has
> tools means it answered without calling any, which is the case where the reply
> says "let me check that" and nothing happened.

```typescript
const result = await zavu.senders.agent.tools.create({
  senderId: "snd_abc123",
  name: "get_order_status",
  description: "Get the current status of a customer order",
  webhookUrl: "https://api.example.com/webhooks/order-status",
  webhookSecret: process.env.WEBHOOK_SECRET,
  parameters: {
    type: "object",
    properties: {
      order_id: { type: "string", description: "The order ID to look up" },
    },
    required: ["order_id"],
  },
});

// Test tool
await zavu.senders.agent.tools.test({
  senderId: "snd_abc123",
  toolId: "tool_abc123",
  testParams: { order_id: "ORD-12345" },
});
```

## Knowledge Bases (RAG)

A prompt that says "only state what the documentation returns" with no documents
attached does not refuse — it invents. Attach the documents, then verify with
`agents test`, which reports how many chunks it actually retrieved.

From the CLI:

```bash
npx zavudev agents knowledge-bases create --sender snd_abc123 --name "Product docs"
npx zavudev agents knowledge-bases documents add --sender snd_abc123 --kb <kbId> \
  --title "Pricing" --content-file ./pricing.md
npx zavudev agents knowledge-bases documents list --sender snd_abc123 --kb <kbId>
```

Processing takes a few seconds; `isProcessed` flips to true and `chunkCount`
fills in.


Add documents for the agent to reference via retrieval-augmented generation:

```typescript
// Create knowledge base
const kb = await zavu.senders.agent.knowledgeBases.create({
  senderId: "snd_abc123",
  name: "Product FAQ",
  description: "Frequently asked questions about our products",
});

// Add document
await zavu.senders.agent.knowledgeBases.documents.create({
  senderId: "snd_abc123",
  kbId: kb.knowledgeBase.id,
  title: "Return Policy",
  content: "Our return policy allows returns within 30 days of purchase...",
});

// List documents
const docs = await zavu.senders.agent.knowledgeBases.documents.list({
  senderId: "snd_abc123",
  kbId: kb.knowledgeBase.id,
});
```

## Monitoring

```typescript
// Get agent stats
const stats = await zavu.senders.agent.stats({ senderId: "snd_abc123" });
console.log(`Invocations: ${stats.totalInvocations}`);
console.log(`Tokens: ${stats.totalTokensUsed}`);
console.log(`Cost: $${stats.totalCost}`);

// List executions
const executions = await zavu.senders.agent.executions.list({
  senderId: "snd_abc123",
  status: "error",
  limit: 20,
});
for (const exec of executions.items) {
  console.log(exec.id, exec.status, exec.errorMessage);
}
```

### Execution Statuses

| Status | Description |
|--------|-------------|
| `success` | Agent generated response successfully |
| `error` | Execution failed (LLM error, tool error, etc.) |
| `filtered` | Response blocked by safety filters |
| `rate_limited` | Provider rate limit exceeded |
| `balance_insufficient` | Account balance too low to process |

## Agents are addressed by their own id

An agent is a standalone object. It can answer on several senders, and it can
exist with none while you build it.

```bash
npx zavudev agents list                 # every agent in the project, with ids
npx zavudev agents list --json
```

```
id                                name        kind   enabled  senders  model
qd75detym58c6has4sfrye3vws8b6ygt  Atlas       voice  yes      1        openai/gpt-5.6-luna
qd7ck28evcskdc3xx4wzevtmeh8b6bcm  Pizza Desk  text   no       0        gpt-4o-mini
```

Over REST:

| | |
|---|---|
| `GET /v1/agents` | List, including agents with no sender |
| `POST /v1/agents` | Create standalone — no sender required |
| `GET /v1/agents/{agentId}` | Fetch one |
| `PATCH /v1/agents/{agentId}` | Update |
| `DELETE /v1/agents/{agentId}` | Delete |
| `POST /v1/agents/{agentId}/test` | Run it, return the reply, deliver nothing |

The older `/v1/senders/{senderId}/agent` routes still work, but they resolve a
sender to exactly ONE agent — so they cannot reach an agent that has no sender,
or the second agent on a shared one.

To exercise one tool rather than the whole agent:

| | |
|---|---|
| `POST /v1/senders/{senderId}/agent/tools/{toolId}/test` | Call the tool with your params, return what it answered |
| `GET /v1/senders/{senderId}/agent/tools/{toolId}/test-runs` | The recent runs, newest first |

From the CLI:

```bash
npx zavudev agents tools test <toolId> --sender <senderId> --params '{"orderId":"ORD-4417"}'
npx zavudev agents tools test-runs <toolId> --sender <senderId>
```

The test is synchronous and returns the tool's status, body, and duration, so a
result is evidence the tool ran. A tool that answers with an error comes back as
`run.success: false` and the endpoint still returns 200 — read the field, not the
status. It fires the real webhook, so it has whatever side effects the tool has.

`test-runs` covers manual tests only. A tool called by the agent during a real
conversation is not listed there; for that, `agents executions` shows how many
tools each reply called.

### Connecting senders

```bash
npx zavudev agents senders connect    --agent <agentId> --sender <senderId>
npx zavudev agents senders disconnect --agent <agentId> --sender <senderId>
```

`POST /v1/agents/{agentId}/senders` with `{"senderId": "..."}`, and
`DELETE /v1/agents/{agentId}/senders/{senderId}`.

**A sender answers with at most one agent.** Connecting one that is already in
use returns `400` naming the agent that holds it — the alternative would be an
agent that looks connected and never receives a message.

## Test an agent without sending anything

```bash
npx zavudev agents test --agent <agentId> --message "where is order ORD-001?"
```

Runs the real prompt, model and knowledge base and prints what the agent
*would* reply, plus tokens, latency and how many knowledge chunks were used.
Nothing is delivered, nothing is charged, no execution is logged — safe to run
in a loop while iterating on a prompt.

It also warns about what a dry run cannot prove: an agent that is disabled,
tools its channels will never call, and contact metadata that will exist live
but not here. Treat those warnings as part of the result.

Multi-turn and isolating the prompt from retrieval:

```bash
npx zavudev agents test --agent <agentId> \
  --turn "I need to change my booking" --turn "Sure — which one?" \
  --message "the one on Friday"

npx zavudev agents test --agent <agentId> --message "what do you cost?" --no-knowledge
```

## Delete Agent

```typescript
await zavu.senders.agent.delete({ senderId: "snd_abc123" });
```

## Channels an agent answers on

`triggerOnChannels` is a whitelist, and it is the most common way to end up with
an agent that looks finished and is silent. An inbound message whose channel is
not in the list is dropped before the agent runs: no reply and no error, while
the dashboard Playground keeps answering, because it bypasses the filter. Look
for it in `GET /v1/senders/{senderId}/agent/executions`, where the drop appears
with `status: "filtered"` and an `errorMessage` naming the channel that arrived
and the channels the agent listens on.

`["*"]` means every channel the sender carries, and is the right default. Narrow
it only to deliberately exclude a channel, and remember that adding a channel to
the sender later does NOT add it here. Unknown strings are accepted and match
nothing, so a typo behaves exactly like a channel you meant to exclude.

## Constraints

- **One agent per sender.** Writes do not enforce it — a second agent can be
  created on a sender — but every read resolves a sender to exactly ONE agent,
  so the extra one answers nothing and is invisible to `agents get`. `zavu
  deploy` warns when it happens.
- System prompt: max 10,000 characters
- Context window: 1-50 messages
- Temperature: 0-2
- Max tokens: 1-4,096
- Tool name: max 100 characters
- Tool description: max 500 characters
- Document content: max 100,000 characters
- Knowledge base name: max 100 characters
- Provider `zavu` doesn't require an API key (uses Zavu-hosted models)
- All other providers require your own API key
