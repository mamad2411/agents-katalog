---
name: aivax
description: Operate AIVAX as a unified agent platform. Use when an agent needs to plan, execute, or validate work that touches AIVAX inference, RAG, rerankers, agentic tests, voice (TTS, STT, realtime), image generation, text tools (classify, segment, describe), AI gateways, batch, web chat, account operations, cost monitoring, or observability. Routes to focused sub-skills instead of duplicating endpoint documentation. Covers the case when the AIVAX MCP is available and when only public docs are reachable.
---

# AIVAX

AIVAX is an AI orchestration platform: hosted or BYOK models, RAG collections, tools, skills, gateways, chat clients, batch, agentic tests, voice, image generation, and account APIs behind a single wallet and OpenAI-compatible inference surface. The role of this skill is not to memorize endpoints; it is to help the agent pick the right capability, follow the right contract, and validate the result.

## When To Use This Skill

Use this skill when the task involves any of the following:

- Calling an AIVAX model or AI gateway (`/v1/chat/completions`).
- Configuring or operating an AI gateway, RAG collection, batch workflow, or chat client.
- Generating, transcribing, or describing media (speech, image, video, file).
- Opening or designing a realtime voice session.
- Classifying, segmenting, or extracting structure from text or media.
- Searching and reranking a knowledge base, with or without a collection.
- Creating, running, evaluating, or comparing agentic tests.
- Creating, rotating, or auditing API keys; inspecting balance, usage, salt, or plan.
- Investigating cost spikes, latency, or production errors; correlating traces.
- Building a workflow that combines more than one AIVAX capability.

Do not use this skill to inspect, modify, build, or reason from AIVAX source code, repositories, deployment scripts, database models, or server internals unless the user explicitly asks for a separate source-code engineering task.

## How To Read This Skill

The skill is a router. The body of `SKILL.md` tells the agent which sub-skill to load for a given intent, how to discover capabilities, and what global rules apply. The sub-skills in `references/` contain the actual operating contracts.

Always start with the **Router Matrix** below. Then load exactly one capability skill (or compose several) before acting.

## Router Matrix

Map the user intent to a sub-skill. Load only what you need. When in doubt, prefer the more specific skill over the broader one.

| Intent | Load |
| --- | --- |
| Choose a model, build chat-completion messages, stream, attach tools, retry, or swap models for cost/latency/quality | `references/text-inference/` |
| Send images, audio, video, or files inside chat-completion messages; preprocess media to text | `references/multimodal/` |
| Generate images from text prompts | `references/image-generation/` |
| Synthesize speech from text (TTS) | `references/speech/` (TTS) |
| Transcribe audio to text (STT) | `references/speech/` (STT) |
| Open a realtime bidirectional voice session | `references/voice-realtime/` |
| Classify documents, segment text, or describe media into text | `references/text-tools/` |
| Build a RAG pipeline: collection, ingestion, query, answer, grounding | `references/rag/` |
| Rerank candidate documents; choose Reflex, Cohere, Qwen, Jina, NVIDIA, or lexical reranker | `references/rerankers/` |
| Create, run, evaluate, or compare agentic tests | `references/agentic-tests/` |
| Create, list, rotate, or delete API keys; inspect account, plan, or salt | `references/account/` |
| Investigate a cost spike, balance drop, or spend optimization | `references/cost-monitoring/` |
| Correlate traces, diagnose latency/error, audit a conversation | `references/observability/` |
| Create, edit, or operate an AI gateway (model + instructions + RAG + tools + skills) | `references/ai-gateways/` |
| Author or attach an account-scoped skill under `/api/v1/skills` | `references/skill-development/` |
| Operate a web chat client, session, or messaging integration | `references/web-chat/` |
| Design or debug a batch workflow/job/items | `references/batch/` |
| Combine multiple AIVAX capabilities into a single workflow | `references/composition/` |
| Handle rate limits, transient errors, retries, idempotency, fallback | `references/resilience/` |
| Anything transversal: which tool to call, how to mutate safely, how to interpret errors | `references/platform-rules/` |

If two skills match, prefer the one closer to the user-facing outcome. For example, "the agent's last answer was wrong" usually means `references/rag/` (grounding) or `references/text-inference/` (prompt/model); only escalate to `references/observability/` if there is telemetry evidence of a failure.

## Discovery And No-MCP Mode

The skill assumes the AIVAX Account Management MCP may or may not be available. The agent must check before relying on a specific tool.

### When the MCP is available

Prefer the MCP tools over direct HTTP calls. The three core tools are:

- `aivax_invoke_function`: invoke any account-scoped AIVAX API with a hostless path such as `/api/v1/ai-gateways` and an optional JSON `body`.
- `aivax_list_models`: list integrated models and AI gateways with capabilities, pricing, context window, modality, plan availability, and flags.
- `aivax_search_context`: search AIVAX documentation and API reference before acting on unfamiliar fields, enums, or endpoints.

`aivax_search_context` is the right tool to call when a sub-skill says "verify the field name with the docs" — that instruction always means a search call, not a guess.

### When the MCP is not available

Fall back to public AIVAX surfaces and document every call before making it:

- API reference for agents: <https://inference.aivax.net/apidocs/llms.txt>
- Human and agent manual: <https://docs.aivax.net/docs/overview>
- Send the header `X-Response-Truncating: agent-optimized` on HTTP calls to get a shortened, agent-friendly response.

In this mode, ask the user for the base URL and API key surface if the integration is not already configured. Do not infer hosts, credentials, or internal paths.

For all sub-skills, the operating instruction is the same: **read the live source of truth (MCP or docs) before mutating, and never invent field names**.

## Cross-Cutting Contracts

Every sub-skill follows the same contract, so the agent can chain them safely.

- **Inputs**: the data, parameters, IDs, and resources the sub-skill needs.
- **Preconditions**: what must already be true (auth, balance, plan, model availability, gateway state, collection indexing state, etc.).
- **Decision criteria**: how to choose between alternatives (model vs. model, reranker vs. reranker, multimodal vs. preprocess, gateway vs. direct call).
- **Actions**: the ordered steps the agent takes, including mutations, validations, and reversibility rules.
- **Outputs**: what the sub-skill produces for the caller (next call, resource ID, transcript, score, decision).
- **Validation**: how to verify the result through the same user-facing or telemetry path that produced the failure.
- **Limits**: rate limits, balance minimums, context caps, quota windows, and known failure modes.
- **Escalation**: which other sub-skill to load if the current one cannot resolve the task.

## Operating Principles

1. **One capability per sub-skill.** Do not re-implement a contract in two places. Compose, do not duplicate.
2. **Discover first, mutate second.** Always read current state with `aivax_invoke_function GET` or the public equivalent before any `POST`, `PUT`, `PATCH`, or `DELETE`.
3. **Smallest safe change.** Patch only the fields that must change. For shallow-merge endpoints, do not send a copied full object.
4. **Validate through the same path the user will use.** A gateway change is validated by a real or test conversation. A RAG change is validated by `/api/v1/query` or a real conversation. A chat-client change is validated by a session or talk URL. A batch change is validated by item inspection or export.
5. **Preserve secrets.** API keys, provider keys, salts, integration tokens, webhook secrets, and access keys never appear in final responses or logs.
6. **Approval gates.** Destructive operations (delete, reset, clear, roll salt, sync imports that remove records, bulk cancellation, model swaps in production, rate-limit changes) require explicit user approval before execution.
7. **Observability is a first-class concern.** Every multi-step workflow records request IDs, conversation IDs, transaction IDs, item IDs, balance snapshots, and a one-line cost estimate. This is what makes escalation and post-mortem analysis possible.

## Default Workflow

1. Classify the intent and load the right sub-skill from the Router Matrix. Load more than one only if the task truly spans capabilities.
2. Discover the environment: MCP available? Auth configured? Plan and balance sufficient? Model or gateway exists?
3. Read current state for every resource you intend to touch.
4. If the contract requires a capability that is not in the loaded sub-skill, switch to the right one — do not invent endpoints.
5. Apply the smallest change that satisfies the request. Prefer reversible operations.
6. Validate through the same user-facing or telemetry path.
7. Report what changed, what was verified, the resource IDs, the cost impact, and any remaining risk or follow-up.

## Global Safety Rules

These apply in addition to the rules inside each sub-skill.

- Preserve secrets. Never print API keys, provider keys, integration tokens, webhook secrets, salts, chat access keys, or private credentials.
- Treat destructive operations as explicit-only: delete, reset, clear, roll salt, imports that overwrite many resources, sync imports that remove missing records, and bulk cancellation.
- Export or capture current configuration before large imports, destructive edits, broad migrations, skill imports, collection resets, or gateway rewrites.
- For shallow-merge endpoints, send only the fields that should change.
- Keep AIVAX `systemInstruction` separate from account skills. Skills are a flat list attached to gateways; do not assume native priority or a primary skill.
- For integrated models, prefer `baseAddress: "@integrated"` and a model returned by `aivax_list_models`.
- For external providers, preserve existing `apiKey` values when patching unrelated gateway parameters.
- Use the account API (`aivax_invoke_function`) for resource work. The Account Management MCP is the operating interface; local source code is not.
- Do not include media payloads, full transcripts, hidden reasoning, or private user data in final responses unless the user explicitly needs that exact data.

## Sub-Skill Index

| Sub-skill | Purpose |
| --- | --- |
| `references/platform-rules/` | Cross-cutting: tool selection, safe mutations, error handling, no-MCP discovery |
| `references/composition/` | Combine multiple AIVAX capabilities with explicit contracts and observability |
| `references/resilience/` | Retry, fallback, idempotency, rate-limit and partial-failure handling |
| `references/text-inference/` | Model selection, chat completions, messages, streaming, tool calls, fallbacks |
| `references/multimodal/` | Image, audio, video, and file inputs; multimodal preprocessing to text |
| `references/image-generation/` | Text-to-image generation and storage |
| `references/speech/` | Text-to-speech and speech-to-text generation |
| `references/voice-realtime/` | Realtime bidirectional voice sessions |
| `references/text-tools/` | Document classification, text segmentation, and media description |
| `references/rag/` | RAG pipeline design, evaluation, and grounding diagnosis |
| `references/rerankers/` | Reranker selection, catalog, and collection-less rerank (Reflex) |
| `references/agentic-tests/` | Test creation, runs, evaluation, comparison, and trace analysis |
| `references/account/` | API keys, account state, plan, salt, secret hygiene |
| `references/cost-monitoring/` | Cost spike investigation and spend optimization |
| `references/observability/` | Trace correlation, degradation diagnosis, conversation audit |
| `references/ai-gateways/` | Gateway design, skills and tools attachment, safe editing |
| `references/skill-development/` | Authoring and attaching account-scoped skills |
| `references/web-chat/` | Web chat clients, sessions, and messaging integrations |
| `references/batch/` | Batch workflow design, job execution, and failure analysis |
