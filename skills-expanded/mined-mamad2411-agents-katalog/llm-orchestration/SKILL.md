---
name: llm-orchestration
version: 1.0.0
min_mindforge_version: 10.5.0
status: stable
triggers: LLM orchestration system, chain-of-thought routing, model cascading strategy, LLM fallback design, LLM context window optimization, LLM router design, model selection pipeline, LLM chain composition, prompt chaining, LLM gateway architecture, multi-model routing, LLM request planning
compose:
  - agent-orchestration-patterns
---

# LLM Orchestration & Routing

## When this skill activates

This skill activates when building systems that route requests across multiple LLMs, cascade from cheap to expensive models, implement fallback strategies, or manage context window limits. It applies to production AI systems where cost, latency, and reliability must be optimized across a fleet of models.

## Mandatory actions when this skill is active

### Before writing any code

1. **Map task to model capabilities** — Identify which tasks require which model capabilities: reasoning (Opus/GPT-4), speed (Haiku/GPT-3.5), cost-efficiency (Haiku/GPT-3.5), context length (Claude 200K, GPT-4 128K), multimodal (GPT-4V, Claude Sonnet with vision). Not all tasks need the most expensive model.
2. **Design cascading strategy** — Define fallback chain: start with fastest/cheapest model, escalate to more capable models if quality is insufficient. Example: Haiku → Sonnet → Opus. Measure escalation rate (% of requests that cascade) and optimize to minimize unnecessary escalations.
3. **Establish routing rules** — Define deterministic rules for model selection: route by task type (classification → Haiku, creative writing → Opus), by complexity (short prompts → small models, long prompts → large models), or by user tier (free users → Haiku, paid users → Sonnet). Document routing logic explicitly.
4. **Plan for context window management** — Measure typical prompt lengths and output lengths. If prompts exceed model limits, implement truncation (drop least important context), summarization (compress with smaller model), or chunking (split into multiple requests). Test that truncated prompts still produce useful outputs.

### During implementation

- **Implement request routing layer** — Build a central router that examines each request (task type, complexity, user tier, priority) and selects the appropriate model. Router must be fast (<10ms overhead) and deterministic (same input always routes to same model for consistency).
- **Add quality-based cascading** — After receiving a response from a cheap model, run a lightweight quality check (confidence score, length validation, keyword presence). If quality is below threshold, retry with a more expensive model. Log all escalations for analysis.
- **Design stateful prompt chaining** — When chaining multiple LLM calls (research → draft → critique → revision), maintain conversation state explicitly. Use structured context: {task: ..., previous_output: ..., next_instruction: ...}. Avoid relying on model memory (models are stateless between API calls).
- **Implement prompt compression** — For long contexts, compress aggressively: remove filler words, use abbreviations, reference external documents by ID instead of embedding full text. Test that compressed prompts produce equivalent outputs. Measure compression ratio (original tokens / compressed tokens).
- **Handle rate limits gracefully** — Implement exponential backoff and retry logic for rate limit errors. If one model is rate-limited, fail over to an alternative model (even if more expensive). Never return errors to users due to transient rate limits.
- **Track cost and latency per model** — Log every request: model used, input tokens, output tokens, latency, cost. Aggregate metrics by model and task type. Identify opportunities to downgrade expensive models to cheaper alternatives without quality loss.

### After implementation

- **Validate routing accuracy** — Test that requests route to the expected model based on your rules. Measure routing accuracy (% of requests routed correctly). Incorrect routing wastes cost (cheap task routed to expensive model) or produces poor quality (complex task routed to weak model).
- **Measure cascade efficiency** — Track escalation rate: % of requests that start with a cheap model but cascade to expensive models. Target: <10% escalation rate. Higher rates indicate routing rules are too aggressive (route to cheaper models upfront).
- **Benchmark end-to-end latency** — Measure latency including routing overhead, model inference, and cascading retries. Compare to single-model baseline. Orchestration should add <50ms overhead. If higher, optimize routing logic or reduce cascade depth.
- **Test fallback behavior** — Simulate model failures (rate limits, API downtime, timeouts) and validate that fallback logic activates. Ensure degraded mode still returns useful responses (even if lower quality or higher latency).

## Self-check before task completion

- [ ] Task-to-model mapping is documented with capability requirements (reasoning, speed, cost, context)
- [ ] Cascading strategy is defined with explicit escalation rules and thresholds
- [ ] Routing rules are deterministic and documented (by task type, complexity, user tier)
- [ ] Context window limits are handled via truncation, summarization, or chunking strategies
- [ ] Request router is implemented with <10ms overhead and deterministic behavior
- [ ] Quality-based cascading retries with more expensive models if quality is below threshold
- [ ] Prompt chaining maintains stateful context explicitly across LLM calls
- [ ] Prompt compression is implemented and tested for equivalence with uncompressed prompts
- [ ] Rate limit handling implements exponential backoff and model failover
- [ ] Cost and latency per model are logged and aggregated for optimization analysis
- [ ] Routing accuracy is validated (requests route to expected models)
- [ ] Escalation rate is measured and optimized to <10% of requests
- [ ] Fallback behavior is tested under simulated model failures (rate limits, downtime)
