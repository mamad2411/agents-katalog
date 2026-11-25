---
name: llm-integration
description: Checklist for code that calls a language model or exposes a system to one. Use when writing or reviewing code that calls a model API (Anthropic, OpenAI, Bedrock, Gemini, Perplexity), a prompt or prompt template, structured model output, an MCP server or tools an agent will call, or a surface that carries user- or web-controlled text to a model without calling one (a tool result, a chat card, a ticket). Also use when choosing which model a product's code calls, or pricing those API requests.
---

# Model calls

A model appears in a system in one of three roles, and the checklist applies to each:

- **Component**: the feature calls a model to summarize, classify, extract or draft. Its output
  feeds your code.
- **Subject**: you measure what a model says (which sources an answer engine cites, how a
  chatbot answers a customer question). The answer is the data, so it must not be smoothed over.
- **Caller**: an agent calls your system through tools (an MCP server, a function-calling API).
  Your system is the component, and the model is the client.

Keep deterministic parts deterministic: a pass/fail gate, a score or a compliance verdict does
not take a model's word as its input unless the design says so explicitly.

## Prompts are source code

- A prompt lives in a versioned file or a config entry with an `id`, never inline in a call
  site. Rewording is a reviewed change; changing the `id` means it is a different question and
  any trend over its answers restarts.
- Changing a prompt or a model is a behavior change: run it against a fixed set of recorded
  cases (an eval set) before it ships, and compare with the previous version.
- Anything interpolated into a prompt is validated by a schema first (zod, pydantic, JSON
  Schema). Text a third party controls (web pages, uploaded documents, emails, tickets, user
  profiles) goes in only as quoted, delimited data, never spliced into an instruction. Prompt
  injection is the SQL injection of this layer: a page can carry "ignore previous instructions".
- Keep the static part of the prompt first and the variable part last, so provider prompt
  caching applies to the prefix.

## Outputs are untrusted input

- Ask for structure (tool use or a JSON schema) and parse it with a schema validator. Never
  regex free text for a URL, a number or a verdict.
- A URL, citation, ID or quote a model returns is a claim. Normalize it (strip tracking and
  credential parameters, fragment, user info) and verify it before storing it as a fact: check
  it against what the model was actually given or searched, or fetch it through an
  SSRF-guarded client. A hallucinated citation reported as a success is worse than a miss.
- Keep the raw response next to the parsed one. A model answer cannot be reproduced later.
- Redact keys and anything shaped like a key from every provider message that reaches a log, a
  report or an error: providers echo rejected keys back in error bodies.

## Cost, models and fallbacks

- Take model IDs and prices from the provider's current docs, not from memory. Price every call
  from the published rates and stop the run at a configured spend cap; report measured cost
  where the provider returns usage.
- For a component, use the cheapest model that passes a verification step, and escalate one tier
  only when it fails (cascading). For a subject, the model is fixed by the study design: no
  cascading, since switching models mid-series changes the thing being measured.
- Retry a rate limit after `retry-after`, with a cap. A 401, 403 or 402, or an exhausted quota,
  is fatal for that provider, and the run says so in its status. A provider outage is reported
  as "not run", never as a zero or a pass.
- Do not cache answers when the answer is the measurement. Where an answer cache is legitimate,
  key it per tenant and per input, give it a TTL, and never serve one tenant's answer to another.

## Exposing a system to an agent (MCP, tools)

- A few tools with full descriptions beat many thin ones. The description is the agent's only
  documentation: say what the tool does, when to call it, and what it returns.
- Every tool input goes through a schema. Targets (hosts, repositories, accounts) are
  allowlisted. Long work is an asynchronous job, with a start tool and a status tool, because a
  tool call should return in seconds.
- Grant the least that the task needs: read and run, not deploy or delete. An agent that fixes
  what it finds opens a pull request for a human to merge.
- The server stops when told to. In Node, a signal handler replaces the default exit, so a
  handler that only tidies up leaves the process running, and the MCP SDK's stdio transport does
  not notice stdin closing. On SIGINT, SIGTERM or stdin end: close the transport, stop any
  running job (kill its process group, so a child browser or shell goes too), then exit 130, 143
  or 0, with a deadline in case cleanup hangs. Hold this with a test that sends the signal and
  closes stdin.

## Untrusted text that reaches a model through your system

Some surfaces carry third-party text to a model without your code calling one: a tool result an
agent reads, a chat card that an assistant summarizes, a ticket an assistant triages. That
text can carry instructions too (indirect prompt injection).

- Return third-party text as data, under its own field name (`evidence`, `excerpt`, `body`),
  quoted or fenced, and cut to a length cap. A tool description, a card heading or a status line
  is in your system's words only, never concatenated with third-party text.
- Keep what a planted instruction could achieve small: if the tools grant read and run, the most
  it can do is ask for another read or run.
- An inbound webhook or API that triggers work is an input boundary: verify the signature with a
  constant-time comparison before anything else, parse the payload with a schema, and apply the
  same allowlist as the tools.

## Review focus

When a change touches a model SDK, a `fetch` to an AI provider, a prompt file, an MCP server or
tool definitions, or a surface that carries third-party text to a model, say so at the top of the
review and check, in this order: inputs validated, outputs parsed by schema and verified, raw kept,
keys redacted, cost capped, failures reported as not-run. For an MCP server, also check that it
still stops on a signal and on a closed stdin, and stops its running job first.
