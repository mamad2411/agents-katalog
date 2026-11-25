---
name: building-agents
description: Build the AI parts of a 3B workflow — any step that calls a language model. Use whenever a task calls a model (Anthropic, OpenAI, Gemini, …) or is model-shaped — summarize, extract, classify, generate, rewrite, answer, converse, or a tool-using agent — even if “AI” or “agent” is never said. Covers choosing the shape, the agent step, the mandatory self-loop for async agents, tools, model choice, conversations, chat UIs, and single-request calls. Pair with the claude-api skill for Anthropic-native features (Batches, the Files API).
license: Apache-2.0
compatibility: Tines 3B
---

# Building AI into a 3B workflow

An “AI step” is any step that calls a model. Pick the simplest shape that does the work, wire it the 3B way, and don’t hand-roll what the agent template already gives you.

## Choose the shape

Simpler shapes mean less latency, cost, and breakage — but under-powering is just as real a failure: a task that has to gather context or act, crammed into one call, gives a worse answer, not a simpler one. The deciding question isn’t how much fits in the prompt; it’s whether you can name every input up front.

1. **Single request** — one call in, one result out, no tools. Use it when you can assemble the complete input ahead of time and the job is to transform it: classify, extract, summarize, generate, rewrite, answer a self-contained question. If a regex or lookup would do, don’t call a model at all.
2. **Agent** — one model with tools, looping until it’s done. Use it the moment a good answer depends on context the model has to _choose to pull_, or on _doing_ something and reacting to the result: reading the files a diff touches, following a lead, searching, calling an API, then deciding what’s next. The tell: you can’t list the inputs up front, because they depend on what the model finds. Pre-fetching that context in code and pasting it into one call is the trap — it looks like it “puts everything in the prompt”, but it freezes what the model can consider to whatever you guessed and caps the quality of the answer. When the user asks for an “agent”, this is the shape they mean — and one pass is not an agent.

## The agent step

Copy the `agent` template — never hand-roll the model loop, in-process or as a chain of AI steps. The template is the canonical implementation of what a correct agent guarantees:

- **Loops until the model signals done** — a turn ending with no tool call.
- **Stops at its bounds** — step caps (per run, and across all of a conversation’s runs), token budget, and wall clock end the run with the transcript persisted and a terminal event, never a runaway loop or a mid-write kill.
- **Streams to a watching caller** — text, reasoning, tool calls and results, and usage flow as they happen, never one blob at the end. A headless run instead writes a single structured result — the stream is noise to downstream steps, and the full trail is in the transcript.
- **Persists the transcript durably every run** — messages, tool calls, results, and the whole usage object (cache and reasoning tokens are priced separately): the audit trail, debugging surface, and cost record.
- **Isolates conversations by the authenticated caller** — a client-supplied conversation id is never an access check.

You normally touch five things: `system.md` (who the agent is, its tools, and when to stop or ask before an irreversible action), `tools/` (one tool per file — see Tools), `model.json` (provider, model, effort, thinking, run limits), `config.toml` (connect the provider; add a `route` plus `output = true` only when a caller invokes the agent directly — without them it’s a headless node: the upstream step’s output in, one structured result out), and `buildInput` in `agent.ts` — the function **you** own that shapes this workflow’s trigger payload (the upstream step’s output, or the route’s request body) into the agent’s message, tool context, and, for chat, the conversation to continue. The template can’t know that shape, so always write `buildInput` for the workflow at hand rather than leaving the placeholder. The template’s files document themselves — read the comments in the file you’re changing rather than a manual here.

The step has two shapes, and its wiring decides which — the loop keys off how the run arrives, so there’s nothing else to configure. **Interactive** — the run arrived through the agent’s own `route`, so a caller holds the stream: the in-process loop answers the whole turn inside one step run. **Async** — the run arrived headless (from a webhook step, a cron step, or any upstream step): it makes exactly one model request and exits. So wire the shape you mean: a chat agent carries the `route` (plus `output = true`); an async agent NEVER does — its trigger is its own step linked in, and the agent MUST self-loop — see “Async agents”. This is a hard requirement, not a variant to consider.

Use the latest model generation — check the `claude-api` skill for current ids; most capable by default, a cheaper tier only for routing or classification.

Always put `(AI Agent)` in the step name (e.g. `Answer support ticket (AI Agent)`) so the loop is obvious at a glance — the counterpart to the `(AI)` tag on single-request steps.

## Editing the loop

The loop is real code (`agent.ts`, `runtime/`), and editing it is normal — add a provider in `runtime/model.ts`, restructure the runtime. Whatever you change, the guarantees above must survive. Two mechanics to preserve:

- **stdout is the run’s output contract** — an interactive run streams one NDJSON `AgentEvent` per line; a headless run writes exactly one structured `AgentRunResult` object at the end. Nothing else; log to stderr. Anything stray on stdout corrupts the step’s output.
- **The transcript is written before the platform kills the step** — the loop stops itself under the step timeout to leave that margin. Keep the margin if you change the timing, the timeout, or the persistence.

## Async agents

Whenever no caller is waiting on the stream — the agent is triggered by a webhook, a cron, or an upstream step (e.g. `GitHub PR webhook → Review PR (AI Agent)`) — the agent MUST self-loop: **link the step back to itself** (its own name in `links` in its `config.toml`), and keep the trigger on its own step — never a `route` on the agent itself. Never let a headless agent run its whole loop inside one step run.

The template does the rest: each run resumes the conversation from the transcript, makes exactly one model request, and writes a single structured `AgentRunResult` whose `status` — `"running"`, `"done"`, or `"error"` — drives the loop; the contract is documented where it lives, in `runtime/events.ts`. One request per run is what makes the agent durable: a run never races the step timeout, and a failed run resumes from the last completed request instead of restarting the task. And since stdout fans out to every link, a consumer step downstream of the agent runs on every iteration — it acts on the terminal result (`status` no longer `"running"`) and exits with no output otherwise.

## Conversations

Continuity is server-side, keyed by `conversation_id`: the agent loads the thread’s transcript, appends each turn, and isolates it per authenticated user. A client sends only the new `message` plus the `conversation_id` — **never replay prior turns** (the agent already has them) — and `buildInput` implements that contract by returning the caller’s `conversationId` alongside the message. The same id continues a thread; a new or absent id starts one (the agent mints it and returns `{ type: "conversation", conversationId }` as the first event). Own the id on the client.

## Chat UIs

A custom chat UI talks to the route and never re-implements the loop — build it as a react step (`frontend-design` skill). The stream is NDJSON (one object per line; skip keepalives and unknown `type`s); events are `AgentEvent` in `runtime/events.ts`.

- **Own the `conversation_id` and put it in the URL** (`/chat/<id>`) so threads are linkable and reload-safe; adopt the id from the `conversation` event if you didn’t send one.
- **Restore on refresh from the server** — a small read route that returns the transcript from storage (keyed by authenticated user and `conversation_id`), not local state alone. Restore the **full trail** — reasoning, tool calls, and results, not just Q&A — since the point is watching the agent work. Stored records are AI-SDK `ModelMessage`s (assistant content is an array of `reasoning`/`text`/`tool-call` parts; tool results are a separate `role:"tool"` message); map them to the same blocks as `AgentEvent`, with the answer the last `text` part.
- **A mid-stream refresh loses only the live view** — the turn is still recorded; refetch and show the last completed turn.
- **Enforce isolation** — require auth and key any history you store or serve by the authenticated user.

## Tools

- One tool per file under `tools/`, default-exporting `tool({ … })`; the loop discovers each by filename.
- Return structured JSON, not prose; give each a clear name, a typed input schema, and a one-line description.
- Log to stderr — stdout is the event stream.
- Keep output small — it’s resent every turn.

Tools live inside the agent step by default — the file under `tools/` is the implementation, which means the agent step itself connects every connector its tools use. When that stops scaling — different tools need different connectors, the logic outgrows one file, or you want to test a tool on its own — promote the tool to its own step with a `route` and keep the `tools/` file as a thin `fetch` to it. Connector access stays isolated to the step that needs it, at the cost of an HTTP hop per call.

Load the `workflow-volume-design` skill when an agent reads or writes a named volume. The agent loop and all of its tool calls are one step execution, so apply the volume guidance to the whole loop rather than treating each tool call as a separate execution.

## Single-request steps (no agent)

One call in, one result out, no tools — when you can assemble the whole input up front. The agent loop does all of this for you; these apply to a plain step:

- Use the vercel AI SDK (`ai` + `@ai-sdk/<provider>`) so you can swap models.
- Latest, most capable model (see `claude-api`); a cheaper tier only for routing or classification.
- Credentials from a connector — pass the placeholder `"set-by-connector"`, never hardcode.
- Stream the call — a silent one trips request and idle timeouts.
- Reasoning and prompt caching on by default; off only for trivial routing or extraction.
- Name the step so the model call is obvious, e.g. `Classify email (AI)`.
