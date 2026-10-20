---
name: laravel-ai-features
description: Build AI features in Laravel with the laravel/ai SDK - agent and tool design, structured output, conversation storage, queued AI work, testing with fakes, and cost control. Use when adding AI functionality to a Laravel app, designing agents or tools with laravel/ai, reviewing AI integration code, or wiring LLM calls into jobs and Livewire components.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit, write
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [laravel, ai, llm, agents, laravel-ai]
---

# Laravel AI Features

Wire LLM calls into Laravel **the Laravel way**: agents as small focused classes, side effects through tools, slow work on queues, and everything testable with fakes.

For model-agnostic design (evals, fallbacks, prompt contracts) see `llm-feature-design` — this skill is the Laravel-specific layer on top.

## When to use

- Adding AI features to a Laravel app (chat, summarization, extraction, agents)
- Designing agents/tools with the `laravel/ai` SDK
- Reviewing AI integration: error handling, cost, queueing, testing
- "Where does the LLM call go?" in a Laravel architecture

## Principles

- **Agents are classes, not config.** One agent = one job-to-be-done with a tight instruction set. Five vague agents lose to one sharp one per task.
- **Side effects go through tools.** The model proposes; your tool code validates and executes — with the same authorization you'd demand from a controller.
- **LLM calls are slow I/O.** Anything non-interactive belongs in a queued job; anything interactive should stream.
- **Untrusted in, validated out.** User input can steer the model (prompt injection); model output is parsed and schema-checked before anything acts on it.

## Process

### 1. Place the call correctly

| Use case | Placement |
|---|---|
| Chat / interactive | Controller or Livewire action, **streamed** to the UI |
| Enrichment (summarize, classify, tag) | Queued job (see `laravel-queue-design`) |
| Bulk processing | Batched queued jobs, rate-limited queue |
| Inline in a web request, blocking | Almost never — only sub-second, cached, or trivial calls |

### 2. Design the agent

- One agent class per task, instructions versioned in code (review like any other code)
- Inject runtime context (user, tenant, locale) explicitly — never let the model guess
- Pick the smallest model that passes your eval set; make the model a constructor/config concern so it's swappable

### 3. Design the tools

- Tool = capability boundary. Validate parameters like a FormRequest; authorize against the *acting user*, not "the agent"
- Destructive operations: tool creates a pending action requiring confirmation, or is simply not exposed
- Return small, structured results — the tool result is prompt context and costs tokens
- Log every tool invocation with arguments (audit trail for "why did the AI do that?")

### 4. Demand structured output

- Schema-constrained responses for anything programmatic; map to DTOs/enums at the boundary
- Validate before use; one retry with the validation error fed back, then fallback (default value, human queue, degraded UX)
- Give the model an explicit out (`null` / `"unknown"`) — or it will invent one

### 5. Handle conversation state

- Use the SDK's conversation storage for chat history; cap context (last N messages or a rolling summary) — unbounded history is unbounded cost
- Multi-tenant: conversations scoped by tenant/user like any other model, in queries **and** policies

### 6. Test it

- **Fake at the SDK boundary** in feature tests: assert your code's behavior given a canned AI response — including a *malformed* one
- Tools: plain unit tests (they're just classes)
- Keep a small real-call eval suite (`@group ai-evals`), run on prompt/model changes, **not** in CI's hot path
- Never let CI depend on a live LLM API for correctness

### 7. Control cost and failure

- Token/request budgets per user or tenant (rate limiter); track cost per feature in logs/metrics
- Timeouts + retry-with-backoff on provider errors; circuit-break to fallback behavior on provider outage (see `resilience-patterns`)
- Cache deterministic calls (same input → same enrichment) keyed on a content hash + prompt version

## Output format

```markdown
## AI feature: <name>

**Agent:** <class> — task, model, instruction version.
**Placement:** streamed controller / queued job / batch.

### Tools
| Tool | Validates | Authorizes | Destructive? |
|------|-----------|------------|--------------|
| …    | …         | policy X   | no / confirm-gated |

### Output contract
Schema: … → on invalid: retry ×1 → fallback: …

### Tests
Faked: … | Evals: N cases (manual trigger)

### Cost guards
Budget: …/user/day, cache: …, circuit breaker: …
```

## Anti-patterns

- ❌ Synchronous LLM call in a web request with no timeout, spinner, or fallback
- ❌ Tools that execute without authorization because "the agent decided"
- ❌ Parsing free-text model output with regex instead of structured output
- ❌ CI that calls a real LLM API — slow, flaky, expensive, nondeterministic
- ❌ Unbounded conversation history shipped to the model on every message
- ❌ Prompt instructions edited ad hoc with no version trail
- ❌ One mega-agent with twenty tools instead of focused agents per task
