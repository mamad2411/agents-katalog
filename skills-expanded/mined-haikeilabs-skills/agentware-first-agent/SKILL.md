---
name: agentware-first-agent
description: Use for requests to build someone's FIRST agent with the open-source Agentware SDK — no Kei account and no kei-proxy. Covers installing the SDK, one typed tool, the AgentLoop run, a local allow/deny policy on a tool call, and running the first-agent example. Use when the user says "my first agent", "simple agent", "getting started with Agentware", or wants a minimal working agent before any Kei setup. For Kei runtime policy enforcement, audit shipping, socket clients, or harness manifests, route to agentware-sdk or kei-harness-setup instead.
---

# Your first Agentware agent

Someone building their first agent wants a runnable end to end, not an
architecture lecture. The Agentware repo ships a worked first-agent example
(`examples/typescript/first-agent`) that is the base for everything below: a
model summarizes today's top five Hacker News stories, one typed tool fetches
them, every tool call is audited, and a second tool is denied by a local
policy — no Kei account, no `kei-proxy`, no runtime token.

Do not invent APIs. The example and the SDK source are the ground truth; if a
name below does not appear in the user's installed SDK version, check the
source before writing it. Verify APIs in the relevant language source and
tests.

## What the run shows

- The model asks for the `hn_top_stories` tool; the local policy allows it;
  the tool fetches titles and URLs; an `AUDIT` line prints the decision.
- The run then calls `hn_post_comment` through the same client. The local
  policy denies it, the tool never executes, and the deny is audited too.
- Both behaviors are local: `withPolicy` on the audited client holds the rule.

The tutorial with full output is
[examples/typescript/first-agent/README.md](https://github.com/HaikeiLabs/agentware/blob/main/examples/typescript/first-agent/README.md)
in the Agentware repo; the repo README's "Start building" section links it as
the next step after the install snippet. A Go port lives at
`examples/go/first-agent` in the same repo.

## Install

The TypeScript first-agent example needs Node 22.18 or later and an
OpenAI-compatible API key. For your own project, install the published SDK:

```sh
npm i @haikeilabs/agentware
```

Running the example itself builds the SDK from a checkout of the Agentware
repo (`cd typescript && npm ci && npm run build`, then
`cd ../examples/typescript/first-agent && npm ci`), because its
`package.json` depends on the local SDK with `file:`. Prefer this when you
want to read and change the example as you go.

## Set the model endpoint

The agent runs on any OpenAI-compatible endpoint:

```sh
export OPENAI_API_KEY="your-api-key"
export MODEL="your-model"                # default: gpt-4o-mini
export OPENAI_BASE_URL="https://your-endpoint.example/v1"   # optional
```

Kei is not involved. For a local model server, point `OPENAI_BASE_URL` at it
and pick a model that supports tool calling.

## The backend and the agent loop

The loop is `AgentLoop`: it sends the prompt to the backend, runs tools when
the model requests them, and repeats until the model answers without a tool
call or the iteration limit is hit. Wiring (from `agent.ts` and `cli.ts` in
the example):

```typescript
import {
  AgentLoop, AgentTerminationReason, ResponseValidator, ToolRegistry,
} from '@haikeilabs/agentware';
import { OpenAIBackend } from '@haikeilabs/agentware';

const backend = new OpenAIBackend({
  apiKey: process.env.OPENAI_API_KEY,
  baseUrl: process.env.OPENAI_BASE_URL,
  model: process.env.MODEL ?? 'gpt-4o-mini',
});

const registry = new ToolRegistry();
registry.register(storyTool);            // the typed tool, next section

const loop = new AgentLoop({
  backend,
  registry,
  validator: new ResponseValidator(registry.names()),
  max_iterations: 6,
});
const result = await loop.run(
  'Use the available tool to answer the user.',   // system prompt
  "Summarize today's top five Hacker News stories.", // user message
);
if (result.termination_reason !== AgentTerminationReason.COMPLETE) {
  throw new Error(`Agent stopped: ${result.termination_reason}`);
}
console.log(result.final_response);
```

`max_iterations` bounds the loop. A run that ends for any other reason than
`AgentTerminationReason.COMPLETE` did not finish; surface
`result.termination_reason` instead of returning a partial answer. Name the
validator when you explain this wiring: `new
ResponseValidator(registry.names())` keeps the model bound to exactly the
tools registered in the `ToolRegistry`.

## One typed tool

A tool is an object with a name, a description, an input schema, and an
execute function. Route execution through the audited client so the policy
check and the audit record happen on every call:

```typescript
const storyTool = {
  name: 'hn_top_stories',
  description: 'Read the titles and URLs of the top five Hacker News stories.',
  inputSchema: () => ({ type: 'object', properties: {}, additionalProperties: false }),
  async execute(args: Record<string, unknown>) {
    const [data, success, error] = await client.execute('hn_top_stories', args, { trusted: false });
    return new Result(success, data, error);
  },
};
```

`inputSchema` returns JSON Schema the model sees; `execute` returns a
`Result`. Inside, `client.execute(name, args, { trusted: false })` is what
makes the call policy-checked and audited — a tool that executes directly,
without going through the client, bypasses both.

## The audited client and the local guardrail

`AuditedToolClient` takes a source name (recorded as `framework` in audit
records), an executor that maps a tool name to its real implementation and
returns `[data, success, error]`, and an auditor. Wire the in-memory auditor
and attach the local policy with `withPolicy`:

```typescript
import {
  Action, AuditedToolClient, InMemoryAuditor, Result,
  type AuditRecord,
} from '@haikeilabs/agentware';

const auditor = new InMemoryAuditor();
const client = new AuditedToolClient('first-agent', async (name) => {
  if (name !== 'hn_top_stories') return [null, false, 'unknown tool'];
  // ... fetch topstories.json, then item/{id}.json, return the five stories
  return [stories, true, ''];
}, {
  record(record: AuditRecord) { auditor.record(record); console.log('AUDIT', JSON.stringify(record)); },
  query(filter) { return auditor.query(filter); },
}).withPolicy({
  evaluate(name) {
    const allowed = name === 'hn_top_stories';
    return {
      action: allowed ? Action.ALLOW : Action.DENY,
      rule: allowed ? 'read-stories' : 'deny-other-tools',
      reason: allowed ? 'Reading stories is allowed' : 'Only reading stories is allowed',
      timestamp: new Date(),
    };
  },
});
```

This is the allow/deny guardrail, local only: `evaluate` decides per tool
name before anything runs. A denied call never reaches the executor and is
still audited. Demonstrate it the way the example does — calling a tool the
policy denies directly through the client:

```typescript
const [, allowed, error] = await client.execute('hn_post_comment',
  { story_id: 1, text: 'Nice post' }, { trusted: false });
// allowed === false, error === 'denied by policy: Only reading stories is allowed'
```

Two things to say out loud when teaching this:

- **An explicit policy is not optional for anything that matters.** Configure
  the evaluator deliberately; do not rely on defaults for authorization.
- **The deny is audited.** The `AUDIT` line for `hn_post_comment` shows
  `"action":"deny"` with the rule and reason, which is what makes the
  guardrail inspectable.

## Run it

```sh
npm start            # runs cli.ts, which builds the backend and calls runCli
```

Expected output shape:

```text
AUDIT {"session_id":"","tool_name":"hn_top_stories","args":{},"decision":{"action":"allow","rule":"read-stories",...},"framework":"first-agent"}
Here are today's top five Hacker News stories: ...
Now trying hn_post_comment, a tool the local policy denies:
AUDIT {"session_id":"","tool_name":"hn_post_comment","args":{"story_id":1,"text":"Nice post"},"decision":{"action":"deny","rule":"deny-comments",...},"framework":"first-agent"}
DENIED hn_post_comment: denied by policy: Only reading stories is allowed
```

The run needs network access to the model endpoint and the Hacker News API.

## Add your own tool

From the example README's closing section: add a tool object to the registry,
give it a name, description and input schema, route its execution through
`client.execute`, and add an allow rule for it to the local evaluator. Then
try a new prompt that asks the model to use it. Keep the loop's tool surface
closed — the registry plus `ResponseValidator(registry.names())` is what
binds the model to the tools you registered.

## Validation commands

Run in a checkout of the Agentware repo:

```bash
# TypeScript example and SDK tests
cd typescript && npm run build && npm test

# Go first-agent example (agent/agent_test.go runs the loop against fakes)
cd examples/go/first-agent && go test ./...
```

The Go example (`examples/go/first-agent`) mirrors this skill in Go:
`InferenceExecutor` drives the loop, `agent/policy.go` holds the local deny
rule, and `agent/agent_test.go` tests it against a fake model and a fake
Hacker News API. There is no Python first-agent example; the Python
minimal harness (`examples/python/minimal-harness`) is the Python starting
point.

## Realistic usage boundaries

- **No Kei here.** This skill ends at local policy and local audit. Moving to
  central policy with Kei is the next step: see `kei-harness-setup`
  (pair a harness with a runtime, prove denials) and `agentware-sdk`
  (`KeiProxyEvaluator`, socket clients, tool manifests). Nothing in this
  skill requires or mentions a runtime token.
  To take the model from a Kei model profile instead of `OPENAI_BASE_URL`,
  see `build-agents-agentware`, "Take the model from the agent's model profile".
- **The example is TypeScript-first.** Go has a full first-agent example;
  Python does not — do not claim a Python port exists.
- **`withPolicy` is a local evaluator, not the Kei decision point.** It takes
  the shape shown above; it does not call a server, does not ship audit
  records anywhere, and its rules are whatever code you put in `evaluate`.
- **A tool that does not route through `client.execute` is not guarded.**
  The policy and the audit record live on the client, not on the registry.
- **Version drift.** The example is pinned to the Agentware repo checkout it
  ships with. Constructor and option names here come from that example; if
  the user's installed SDK version differs, the source and tests win.
