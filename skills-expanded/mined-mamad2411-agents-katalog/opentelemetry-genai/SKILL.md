---
name: opentelemetry-genai
description: "OpenTelemetry GenAI semantic conventions: instrument LLM inference, embeddings, tool calls and agents with gen_ai.* spans, attributes, events and metrics. Use when tracing calls to a model provider, adding telemetry to an agent or tool loop, recording token usage and latency, deciding whether to capture prompts and completions, instrumenting MCP clients or servers, or upgrading an instrumentation from semantic conventions v1.36.0 or earlier to the GenAI conventions (development, current; no preview) with OTEL_SEMCONV_STABILITY_OPT_IN. Triggers: OpenTelemetry, OTel, semantic conventions, semconv, GenAI, LLM observability, gen_ai.operation.name, gen_ai.provider.name, gen_ai.request.model, gen_ai.usage.input_tokens, gen_ai.input.messages, invoke_agent, execute_tool, create_agent, gen_ai.client.operation.duration, gen_ai.client.inference.usage, gen_ai_latest_experimental, mcp.method.name."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.1"
  kind: standard
---

# OpenTelemetry GenAI semantic conventions

The OpenTelemetry semantic conventions for generative AI define the span names, span kinds, `gen_ai.*` attributes, events and metrics for model inference, embeddings, tool execution, agents and the Model Context Protocol. They are maintained in the `open-telemetry/semantic-conventions-genai` repository and have **Development** status. With this skill the agent instruments GenAI calls so that any OpenTelemetry backend can read them.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: instrumentation author (library or framework), application developer adding manual spans, or backend consumer reading the data.
- Target version: GenAI conventions (development) (default, draft posture build). Semantic conventions v1.36.0 or earlier is legacy: existing instrumentations keep emitting it by default and switch only through the opt-in; never add new signals in it. There is no supported line and no preview. See [`references/versions.md`](references/versions.md).
- Revision: Draft posture: build. The pin is commit `b31e9e8ea26ac1c086d3313d474e31d7c3f391ae` (2026-09-30) of `semantic-conventions-genai`, schema URL `https://opentelemetry.io/schemas/gen-ai-dev/1.42.0-dev`, built on semantic conventions v1.44.0. The repository has no releases or tags, so pin the commit and the schema URL.
- Content capture: whether prompts, completions, system instructions and tool arguments may be recorded, and where (spans, events, or external storage).
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources), check the repository for a tag or a new `schema_url` in `model/manifest.yaml`, and update the pins.

## Invariants

1. **Everything here is Development.** The conventions, spans, attributes, events and metrics carry Development status (GenAI README; manifest `stability: development`). Names can change between commits; record the schema URL you implemented.
2. **Existing instrumentations do not switch conventions silently.** Instrumentations that emit v1.36.0 or earlier keep emitting it by default, and add `OTEL_SEMCONV_STABILITY_OPT_IN` with the value `gen_ai_latest_experimental` to emit the latest experimental conventions instead of the old ones (semantic conventions v1.41.1 GenAI README).
3. **`gen_ai.operation.name` is Required on every GenAI span, and `gen_ai.provider.name` on inference, embeddings, `create_agent` and client `invoke_agent` spans.** Use a well-known value when one applies; otherwise a custom value is allowed (spans, agent spans, registry).
4. **Span names are low-cardinality**: `{gen_ai.operation.name} {gen_ai.request.model}` for inference and embeddings, `execute_tool {gen_ai.tool.name}`, `invoke_agent {gen_ai.agent.name}`, `create_agent {gen_ai.agent.name}` (spans, agent spans).
5. **Span kind follows the call**: `CLIENT` for remote model, embeddings and agent-service calls (`INTERNAL` allowed for in-process models); `INTERNAL` for `execute_tool` and in-process `invoke_agent` (spans, agent spans).
6. **A span covers the whole logical operation**, including automatic retries, until the response is fully received or the operation ends in an error or cancellation (spans, Spans).
7. **Content is not captured by default.** `gen_ai.system_instructions`, `gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.tool.definitions`, `gen_ai.tool.call.arguments` and `gen_ai.tool.call.result` are Opt-In; offer an option to enable them (spans, Capturing instructions, inputs, and outputs).
8. **Errors set `error.type`**, and span status follows the Recording Errors document (spans).
9. **Token counts report billable tokens** when a system reports both used and billable tokens, and the per-operation histograms are never used for totals or cost (token metrics).

## Workflow

1. **Pick the version.** Emit the GenAI conventions (development) in a new instrumentation; in an existing one that emits semantic conventions v1.36.0 or earlier, keep that default and plan the opt-in.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target conventions and schema URL are recorded, and the opt-in behaviour is decided.
2. **Choose the spans.** Map each GenAI call in the code to an inference, embeddings, retrieval, execute_tool, create_agent, invoke_agent, invoke_workflow or MCP span.
   -> [`references/spans.md`](references/spans.md)
   ✓ Each call site has a span type, a name pattern and a span kind.
3. **Set the attributes.** Fill the Required and Conditionally Required attributes, then the Recommended ones the response provides, such as usage and finish reasons.
   -> [`references/attributes.md`](references/attributes.md)
   ✓ No span lacks `gen_ai.operation.name` or (where required) `gen_ai.provider.name`.
4. **Decide on content capture.** Default off; if enabled, choose span attributes or external storage, and apply truncation.
   -> [`references/attributes.md`](references/attributes.md)
   ✓ A configuration flag controls capture and is off by default.
5. **Record metrics and events.** Emit `gen_ai.client.operation.duration` with the advised buckets, the token usage counters, and the exception and evaluation events where they apply.
   -> [`references/events-metrics.md`](references/events-metrics.md)
   ✓ Duration and token metrics carry the required attributes, including `gen_ai.token.modality` on token counters.
6. **Upgrade** (only when asked, or for an existing instrumentation). Map the v1.36.0 names to the current ones, pin the schema URL, and gate the new conventions behind `OTEL_SEMCONV_STABILITY_OPT_IN`.
   -> [`references/versions.md`](references/versions.md), [`references/versioning.md`](references/versioning.md)
   ✓ The emitted schema URL and the opt-in behaviour are documented for users, and users who did not opt in see unchanged telemetry.

## Verify before done

- [ ] Every GenAI span has `gen_ai.operation.name` with a well-known value where one applies.
- [ ] Inference, embeddings, `create_agent` and client `invoke_agent` spans have `gen_ai.provider.name`; `server.port` is set whenever `server.address` is.
- [ ] Span names follow the patterns above and contain no IDs or prompt text.
- [ ] Opt-In content attributes are off unless the user enabled them.
- [ ] A failed call sets `error.type` and ends the span.
- [ ] Token counters use `{token}`, durations use `s`, and the schema URL is recorded.

## Reference index

- **`references/versions.md`**: the development and v1.36.0 lines, which one to emit, what changed from v1.37.0 to the move into its own repository, the 1.36 to dev upgrade checklist, and why no preview is listed. Load for steps 1 and 6.
- **`references/spans.md`**: inference, embeddings, retrieval, execute_tool, agent and workflow spans, and MCP spans. Load for step 2.
- **`references/attributes.md`**: key `gen_ai.*` attributes, well-known values, usage attributes, and the content capture patterns. Load for steps 3 and 4.
- **`references/events-metrics.md`**: client, server, agent and tool metrics, token metrics, and the GenAI events. Load for step 5.
- **`references/versioning.md`**: Development status, the repository move, the schema URL pin, and `OTEL_SEMCONV_STABILITY_OPT_IN`. Load for step 6.

## Related skills

- `ocsf` to turn AI activity into security audit events: `npx skills add ScaleDockHQ/scaledock-skills --skill ocsf`.
- `cloudevents` to carry trace context on events with `traceparent`: `npx skills add ScaleDockHQ/scaledock-skills --skill cloudevents`.
- `opentelemetry` for the API, SDK, OTLP and general semantic conventions underneath the GenAI signals: `npx skills add ScaleDockHQ/scaledock-skills --skill opentelemetry`.
- `trace-context` for parsing and propagating `traceparent`, `tracestate` and `baggage`: `npx skills add ScaleDockHQ/scaledock-skills --skill trace-context`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Semantic conventions for generative AI systems](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/gen-ai/README.md): Development, commit b31e9e8 (2026-09-30), Draft posture: build, checked 2026-10-02.
- [Registry manifest](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/model/manifest.yaml): development, schema gen-ai-dev/1.42.0-dev on semantic conventions 1.44.0 at commit b31e9e8, checked 2026-10-05.
- [Generative client AI spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/gen-ai/gen-ai-spans.md): Development, commit b31e9e8, checked 2026-10-02.
- [GenAI agent and framework spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/gen-ai/gen-ai-agent-spans.md): Development, commit b31e9e8, checked 2026-10-02.
- [Generative AI events](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/gen-ai/gen-ai-events.md): Development, commit b31e9e8, checked 2026-10-02.
- [Generative AI exceptions](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/gen-ai/gen-ai-exceptions.md): Development, commit b31e9e8, checked 2026-10-02.
- [Generative AI metrics](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/gen-ai/gen-ai-metrics.md): Development, commit b31e9e8, checked 2026-10-02.
- [Generative AI inference token metrics](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/gen-ai/gen-ai-token-metrics.md): Development, commit b31e9e8, checked 2026-10-02.
- [Model Context Protocol semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/gen-ai/mcp.md): Development, commit b31e9e8, checked 2026-10-02.
- [Gen AI attribute registry](https://github.com/open-telemetry/semantic-conventions-genai/blob/b31e9e8ea26ac1c086d3313d474e31d7c3f391ae/docs/registry/attributes/gen-ai.md): Development, commit b31e9e8, checked 2026-10-02.
- [GenAI semantic conventions on opentelemetry.io](https://opentelemetry.io/docs/specs/semconv/gen-ai/): Moved, page as served on 2026-10-02, checked 2026-10-02.
- [GenAI conventions at semantic conventions v1.36.0](https://github.com/open-telemetry/semantic-conventions/blob/v1.36.0/docs/gen-ai/README.md): Development, v1.36.0 (2025-07-05), with its spans and events docs, checked 2026-10-05.
- [Semantic conventions CHANGELOG](https://github.com/open-telemetry/semantic-conventions/blob/main/CHANGELOG.md): changelog, main branch (GenAI entries v1.37.0 to v1.42.0), checked 2026-10-05.
- [semantic-conventions-genai commits](https://github.com/open-telemetry/semantic-conventions-genai/commits/main): no releases or tags, main at e07f4eb (2026-10-02, tooling only since b31e9e8), checked 2026-10-05.
- [GenAI README with the opt-in transition plan](https://github.com/open-telemetry/semantic-conventions/blob/v1.41.1/docs/gen-ai/README.md): Development, semantic conventions v1.41.1, checked 2026-10-02.
- [Semantic conventions v1.44.0 release](https://github.com/open-telemetry/semantic-conventions/releases/tag/v1.44.0): Released, v1.44.0 (2026-08-04), checked 2026-10-02.
