---
name: agent-observability
description: Trace agent reasoning chains, tool call sequences, context injections, and token costs to enable debugging, cost attribution, and continuous evaluation improvement. Use when deploying agents to production, diagnosing unexpected outputs, tracking costs across tenants, or building evaluation datasets from real-world failures.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, delegate_task, a2a_send_task, run_tests, execute_command]
version: "1.0.0"
---

# Agent Observability

Use this skill when agent behavior needs to be traceable, debuggable, and measurable beyond simple pass/fail checks.

## When to Use

- deploying agents to production
- diagnosing unexpected or wrong agent outputs
- attributing token/cost across tenants
- building evaluation datasets from real failures

## Core Rules

- trace every tool call, reasoning decision, and context injection using standard OpenTelemetry (OTel) GenAI semantic conventions
- enforce nested span hierarchy: `invoke_agent` (root) $\rightarrow$ `plan` $\rightarrow$ `chat` / `generate_content` $\rightarrow$ `execute_tool`
- track token usage with fine granularity: `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.usage.reasoning.output_tokens`, and `gen_ai.usage.cache_read.input_tokens`
- never log unredacted secrets, credentials, or PII in span payloads (opt-in sanitized message attributes only)
- feed production anomalies and validation failures back into evaluation golden datasets (the Virtuous Cycle)
- use tail-based sampling in high-volume environments (retain 100% of errors/anomalies, sample 1–5% of nominal traces)
- attribute costs down to tenant, task, model tier, and Cost per Successful Task Resolution (CPTR)

## Key Concepts

### Session-Level Tracing

Individual LLM call tracing is insufficient. Agent failures are causal chains — a mistake at step 3 may not manifest until step 7. Capture the full distributed trace tree:

- system prompt and context injected at each step
- tool calls with inputs and outputs
- reasoning decisions and branching logic
- memory reads and writes
- final output and user feedback

### The Virtuous Cycle

The most mature teams feed production failures back into their evaluation loop:

1. agent produces unexpected output in production
2. the trace is flagged (manually or by drift detection)
3. the input/output pair is sanitized and added to the golden dataset
4. the prompt or skill is updated via PromptOps
5. the eval suite runs against the expanded dataset
6. regression is prevented permanently

### OpenTelemetry For GenAI (2026 Semantic Conventions)

Use OpenTelemetry GenAI semantic conventions (`open-telemetry/semantic-conventions-genai`) to ensure portability across observability backends. Core attributes:

- `gen_ai.operation.name`: operation type enum (`invoke_agent`, `plan`, `chat`, `generate_content`, `execute_tool`, `search_memory`, `upsert_memory`)
- `gen_ai.provider.name`: provider flavor (`anthropic`, `openai`, `gcp.vertex_ai`, `aws.bedrock`)
- `gen_ai.request.model` / `gen_ai.response.model`: requested and responding model IDs
- `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens`: gross token volume
- `gen_ai.usage.reasoning.output_tokens`: thinking tokens (o1, o3, Sonnet 3.7)
- `gen_ai.usage.cache_read.input_tokens`: cached prompt tokens (discounted pricing)
- `gen_ai.usage.cache_creation.input_tokens`: prompt cache write tokens
- `gen_ai.response.finish_reasons`: array of strings (`["stop"]`, `["tool_calls"]`)
- `gen_ai.conversation.id`: session correlation ID
- OTel Collector template: `core/observability/otel-collector-config.template.yaml` (tail sampling & redaction)

### FinOps Cost Attribution

Track costs at multiple dimensions:

- per-user or per-tenant
- per-feature, per-workflow, or per-role
- per-model tier (lightweight vs mid-tier vs premium)
- Cost per Successful Task Resolution (CPTR)

## Suggested Process

### 1. Instrument The Session

At session start:

- assign a unique session/trace ID
- record the initial context (role, rules, skills loaded)
- record the model and routing decision

### 2. Trace Each Step

For every action:

- log the tool or operation name
- log inputs (sanitized of secrets)
- log outputs and status
- log token usage
- log elapsed time
- log any context injected from memory or RAG

### 3. Detect Anomalies

Flag sessions where:

- total token usage exceeds expected budget by 2x
- the agent called the same tool more than 3 times in a loop
- the agent changed its plan mid-execution more than twice
- the final output contradicts intermediate reasoning
- user required a re-prompt or correction

### 4. Sample For Review

In production:

- keep 100% of failed or anomalous traces
- sample 1-5% of successful traces
- use tail-based sampling: decide whether to keep after the session completes, based on outcome

### 5. Close The Loop & Run 7-Dimension Session Forensics

Weekly or whenever a session stalls, repeats work, drifts from plan, or burns unexpected tokens:

- execute `python3 core/scripts/diagnose-session.py <transcript.jsonl|spans.jsonl> --scrub --format markdown` to audit all 7 forensic dimensions (`skill_timeline`, `plan_adherence`, `repeated_work`, `stumbles`, `quality_evidence`, `request_conflicts`, `cost_and_time`) per [`references/session-forensics-7-dimensions.md`](references/session-forensics-7-dimensions.md)
- discard any forensic claim lacking an exact `path:line` citation; extract verified failure pairs into the golden dataset and update prompts/skills

## Red Flags

| Rationalization Thought | Positive Corrective Action |
|---|---|
| "The session felt slow; I'll guess what went wrong." | Run `python3 core/scripts/diagnose-session.py` on the raw transcript or span log and cite exact `path:line` evidence. |
| "Share the raw transcript directly for debugging." | Pass `--scrub` and verify zero residual secrets or PII before sharing any diagnostic report. |
| "Token cost looks high, probably just a big prompt." | Inspect `repeated_work` and `stumbles` dimensions to separate retry loops from legitimate context size. |

## Checklist

- [ ] session trace ID assigned
- [ ] model and routing decision recorded
- [ ] every tool call traced with inputs, outputs, and token usage
- [ ] context injections (RAG, memory) traced
- [ ] secrets and PII excluded from traces
- [ ] anomalous sessions flagged
- [ ] sampling strategy applied (tail-based for production)
- [ ] production failures fed back to golden dataset
- [ ] cost attributed to appropriate dimensions
- [ ] weekly review cycle established

## Security Guardrails (OWASP ASI)

- **ASI06 Memory & Context Poisoning**: trace data may include poisoned tool outputs; validate the trace against the live system before drawing conclusions.
- **ASI07 Inter-Agent Communication**: traces consumed by other agents or by the audit system are untrusted inputs; require schema validation at every boundary.
- **ASI09 Human-Agent Trust Exploitation**: do not present a trace summary as definitive without surfacing the actual events; redacted traces lose signal.
- **ASI04 Supply Chain**: OTel collectors, tracing SDKs, and observability agents must be schema-validated against the expected manifest; treat unknown versions as untrusted.

## Failure Modes

- **Trace span drift from OTel GenAI convention**: a span attribute uses deprecated names (`prompt_tokens`, `completion_tokens`) instead of `gen_ai.usage.input_tokens` / `output_tokens`. **Mitigation:** validate every span attribute against `core/observability/otel-genai.md`; reject spans that use non-registered keys.
- **Span emitted without `trace_id`**: a tool call is logged without a trace context. **Mitigation:** require `AGENT_TRACE_ID` env var for every span emission; reject spans without a valid `trace_id`.
- **Cost attribution missing**: a tool call is logged without `team_id`, `project_id`, or `user_id`. **Mitigation:** reject tool calls missing the cost metadata; enforce at the gateway.
- **Retention policy drift**: a span is retained longer than the agreed 90 days. **Mitigation:** enforce the retention policy at the storage layer; surface the violation in the audit log; purge the over-retained spans.

## Output Contracts

When the observability data is consumed by another agent, an audit system,
or a downstream SRE/DevOps role, emit:

- **`contracts/schemas/agent-trace-span.json`** for each tool invocation, tag with the active role, the model tier, the tool name, the latency, the cost, and the exit status. The receiving agent can then correlate the trace with the live system.
- **`contracts/schemas/incident-report.json`** when an anomaly is detected; capture the trace span ids, the threshold, the detected value, and the recommended action.
- For human-readable reports, a markdown trace summary with the key spans and the cost breakdown.

Skip emission for read-only trace lookups that do not cross a role boundary.

## Related Skills

- **agent-tool-orchestration**: Provide trace data for every tool call
- **agent-quality-gate**: Use trajectory review as a quality gate
- **agent-prompt-lifecycle**: Feed production insights into prompt evaluation
- **agent-model-routing**: Record routing decisions for cost analysis
- **agent-context-management**: Trace what context was injected and from which source
