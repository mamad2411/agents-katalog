---
name: kei-openai-backends
description: "OpenAI-compatible LLM backend integration for a chat harness and the agentware evals. Use when the task mentions LLM_ENDPOINT, LLM_MODEL, OPENAI_BASE_URL, OpenAIChatModel, pydantic-ai, /v1 chat/completions, llama.cpp, vLLM, Ollama, llamafile, or wiring any model backend. Use for agentware's per-family tool formatters and reasoning adapter — how each model family (OpenAI, Anthropic, DeepSeek, Qwen/QwQ, GLM, Mistral, Llama) formats tool calls and reasoning: OpenAI-style function calling, function.arguments as a JSON string, reasoning_content vs Anthropic extended thinking blocks, thinking_content, inline [THINK]/<thinking> tags, ToolFormatter, GenericFormatter, model-format-reference.md, adding support for a new model family, kei-agents model-format tool rendering (render_tools, ModelFormat), and the agentware evals model backends. A zero-LLM ingress service deliberately has NO LLM — do not reach for this skill inside one."
---

# OpenAI-compatible backends

A chat harness and the agentware evals talk to **any OpenAI-compatible `/v1` endpoint**
(llama.cpp, vLLM, Ollama-compatible, etc.). Keep it that way: no hardcoded provider and no
vendor SDK. A Python harness can use pydantic-ai's `OpenAIChatModel`; the agentware evals
use a raw `/chat/completions` POST.

## What every answer must say

- **Adding a model family (Mistral, Llama, a new vendor).** Say whether it is
  already handled: anything outside the five families falls through to
  `GenericFormatter`, so Mistral needs no config entry. For first-class
  support, name `ModelFormat` and `ToolFormatter`. Across all three ports
  (Go, Python, TypeScript), each port gets its own `ToolFormatter`, and the
  family needs cases in the shared fixtures at `fixtures/toolformat/` and
  `fixtures/reasoning/`; name both paths. YOU MUST end the answer
  with this sentence, even when nothing needs to change: "The full format
  contract is Agentware's `docs/model-format-reference.md`."
- **Anthropic extended thinking vs `reasoning_content`.** Anthropic does not
  use `reasoning_content`. Its reasoning is a `thinking` content block
  (`type: "thinking"`, with a signature) inside the `content` array. It has
  no inline thinking tags. The reasoning adapter also recognises
  `thinking_content` as an alternative field name. Say all three: content
  block, no inline tags, `thinking_content`.
- **DeepSeek tool calls and reasoning.** DeepSeek uses the same JSON
  function-calling format as OpenAI; reasoning comes in the native
  `reasoning_content` field, parallel to `content`. In text mode it can
  emit `[THINK]...[/THINK]` tags instead. Always say that unbalanced
  `[THINK]` tags are a fail-closed error (`ErrUnbalancedThinking`); use the
  word "fail-closed".
- **QwQ vs DeepSeek reasoning.** Name QwQ explicitly: QwQ models (the `qwq-*`
  prefix) put reasoning in `type: "reasoning"` content blocks, while DeepSeek
  (and other Qwen models) use the `reasoning_content` field. The reasoning
  adapter normalises both into one reasoning string.

## Model formats

### Answer checklist

Answer from this skill; the format tables below summarise the canonical
reference, so you do not need to search a codebase first. In every answer
about model formats:

- **Cite the canonical spec in every answer about adding, changing, or
  checking a model family** — even when the answer is "no change needed":
  name `model-format-reference.md` (Agentware `docs/model-format-reference.md`)
  as the full format contract. Example: Mistral falls through to
  `GenericFormatter` with no config entry; `model-format-reference.md` has the
  full format contract.
- **Anthropic thinking:** say all three facts — `thinking` is a structured
  content block (not `reasoning_content`), there are **no inline thinking
  tags**, and the adapter also recognises `thinking_content`. Then say how
  the **reasoning adapter** (use those two words) normalises the block into
  the canonical `Reasoning` object, the same code path as every family.
- **DeepSeek `[THINK]` tags:** say unbalanced tags are a **fail-closed** error.
- **Adding a model family:** all three Agentware ports (Go, Python,
  TypeScript) change: a `ModelFormat` entry, a `ToolFormatter` (5 methods),
  the format selector, the reasoning field if non-standard, and the shared
  fixtures. Write both fixture paths out in full, `fixtures/toolformat/` and
  `fixtures/reasoning/`; one alone is incomplete. Cite
  `model-format-reference.md`.
- **Arguments as a JSON string vs a parsed object:** say which families do
  which. OpenAI, DeepSeek, and Qwen send `function.arguments` as a JSON
  string; Anthropic (`tool_use.input`) and GLM send a parsed JSON object.
  Detect by type (`isinstance(args, str)` → `json.loads`) in the formatter's
  `ParseToolCalls`.

### Supported model families

Agentware supports **five model families** (OpenAI, Anthropic, Qwen, DeepSeek, GLM)
across its three ports (Go, Python, TypeScript). Each family has a dedicated `ToolFormatter`
that handles tool-definition rendering, tool-call parsing, tool-result formatting, and
reasoning-field extraction. The canonical reference is Agentware's
`docs/model-format-reference.md` (PR #166, commit `8966e82a`); the tables below
summarise it.

Models not in these five families (Llama, Mistral, Nemotron, etc.) fall through to
`GenericFormatter`, which produces the same OpenAI-compatible JSON function-calling
format as `OpenAIFOrmatter`.

#### Tool-definition schemas

| Family | Definitions format | Tool calls (response) | Tool result shape |
|---|---|---|---|
| **OpenAI** | JSON: `{type: "function", function: {name, description, parameters}}` | `tool_calls` array: `{id, type: "function", function: {name, arguments (JSON string)}}` | `tool_call_id`, `role: "tool"`, `content` |
| **Anthropic** | JSON: `{type: "function", function: {name, description, parameters}}` | `content` array with `type: "tool_use"` blocks: `{id, name, input (parsed dict)}` | `content` array with `type: "tool_result"` blocks: `{tool_use_id, content}` |
| **Qwen** | XML: `<tool_description><tool_name>name</tool_name><parameters>...</parameters></tool_description>` | `tool_calls` array (OpenAI-compatible); or XML: `<tool_call><tool name="name">JSON args</tool></tool_call>` | `tool_call_id`, `role: "tool"`, `content` |
| **DeepSeek** | JSON: `{type: "function", function: {name, description, parameters}}` | `tool_calls` array with OpenAI-compatible shape; `reasoning_content` parallel to `content` | `tool_call_id`, `role: "tool"`, `content` |
| **GLM** | JSON: `{type: "function", function: {name, description, parameters}}` (dedicated GLM schema path) | `tool_calls` array (OpenAI-compatible shape); arguments as JSON object (not string) | `tool_call_id`, `role: "tool"`, `content` |

OpenAI, DeepSeek, and GLM all use the same JSON function-calling format for
definitions, calls, and results; they differ only in reasoning fields and
thinking tags.

#### Reasoning and thinking fields

| Family | Reasoning field | Inline thinking tags | Notes |
|---|---|---|---|
| **OpenAI** | `reasoning_content` (top-level on choice message) | None | o-series models; field is in the known set, no registration needed |
| **Anthropic** | `thinking` (content block `type: "thinking"` in Messages API) | None | Extended thinking is a structured content block with signature; adapter also recognises `thinking_content` |
| **Qwen** | `reasoning_content` (top-level) | `<thinking>...</thinking>` in content text; QwQ-32B uses `type: "reasoning"` content blocks | Both field and tags are handled generically |
| **DeepSeek** | `reasoning_content` (native field) | `[THINK]...[/THINK]` in text mode | Unbalanced `[THINK]` is a fail-closed error; guardrails response validator strips as secondary rescue |
| **GLM** | `reasoning_content` (native field) | None | Same field format as OpenAI; no inline tags |

The adapter's known field set (priority order): `reasoning_content`, `thinking`,
`thinking_content`, `reasoning`. Arbitrary additional field names can be
registered per model via `RegisterModelField` / `register_model_field`.

#### Tool-call argument format

OpenAI and DeepSeek encode arguments as a JSON **string** in the response
(`"arguments": "{\\"location\\": \\"Tokyo\\"}"`). Anthropic uses a **parsed
dict** for the `input` field of `tool_use` blocks. GLM is the exception:
arguments arrive as a parsed JSON object. Qwen follows the OpenAI-compatible
format (JSON string) or embeds JSON args in XML attributes.

#### Format selector

Agentware selects the formatter by model name (prefix matching,
case-insensitive). On the Python tool-definition side, kei-agents' `ModelFormat`
enum drives `render_tools()` at construction time (one per agent lifetime; see
`kei-agents`); the `FormatAdapter` class selects the renderer by format name:

| Model tag | Formatter struct | Notes |
|---|---|---|
| `gpt-*`, `o1-*`, `o3-*` | `OpenAIFOrmatter` | `reasoning` field (o-series); also `reasoning_content` |
| `claude-*`, `anthropic-*` | `AnthropicFormatter` | `thinking` content block |
| `qwen-*`, `qwq-*` | `QwenFormatter` | QwQ prefix triggers `type: "reasoning"` content block handling |
| `deepseek-*` | `DeepSeekFormatter` | `reasoning_content` + `[THINK]` tags |
| `glm-*`, `chatglm-*` | `GLMFormatter` | Arguments as JSON object |
| `llama-*`, `ollama-*`, `llamafile-*` | `GenericFormatter` | Same JSON format as OpenAI |
| Everything else | `GenericFormatter` | Fallback |

Adding a new family means adding a `ModelFormat` enum variant, a dedicated
formatter struct, a selector entry, and reasoning-adapter model-field
registration if the model uses a non-standard reasoning field name.

#### Reasoning adapter

The adapter (`go/reasoning/adapter.go`, `reasoning.py`, `reasoning.ts`) is
model-agnostic and handles all five families through the same code path.
It normalises reasoning fields into a canonical `Reasoning` object, applied
to every streaming delta / final choice:

| Variant | Input field | Behavior |
|---|---|---|
| **OpenAI** | `choice.delta.reasoning_content` | No tag stripping needed |
| **Anthropic** | `delta.delta.thinking` (content block) | Also recognises `thinking_content` for alternative SDK naming |
| **Qwen** | `choice.delta.reasoning_content` | Strips `<thinking>...</thinking>` from content text |
| **DeepSeek** | `choice.delta.reasoning_content` | Strips `[THINK]...[/THINK]` from text-mode output; unbalanced `[THINK]` returns `ErrUnbalancedThinking` |
| **GLM** | `choice.delta.reasoning` | Similar to OpenAI; no tag stripping needed |

All formatters share the `ToolFormatter` interface (5 methods:
`FormatToolDefinitions`, `ParseToolCalls`, `FormatToolResult`, `ModelFamily`,
`ValidateFormat`). Implementation files in Agentware at
`go/toolformat/{family}.go`, `python/.../toolformat/formatter.py`,
`typescript/src/toolformat/formatter.ts`. Shared fixtures at
`fixtures/toolformat/{family}-cases.json` and `fixtures/reasoning/{family}-cases.json`.

> **Validation reference.** Every claim above is confirmed by the Go/Python/TypeScript
> fixtures in Agentware PR #166 (`docs/model-format-reference.md`,
> `fixtures/toolformat/`, `fixtures/reasoning/`).
> Do not add model families that are not listed here; they are not supported
> by Agentware's formatters.

## Wiring a harness to a compatible endpoint

Your harness takes the endpoint and model as configuration (for example `LLM_ENDPOINT`
and `LLM_MODEL`). Require both to be set before the harness talks to a real model, and
always set the endpoint explicitly rather than relying on a code default.

With pydantic-ai, point the OpenAI provider at the endpoint's `/v1` base:

```python
import os
from pydantic_ai.models.openai import OpenAIChatModel

os.environ["OPENAI_BASE_URL"] = f"{llm_endpoint}/v1"
os.environ.setdefault("OPENAI_API_KEY", "any-key-works")  # see below
model = OpenAIChatModel(llm_model, provider="openai")
```

Most self-hosted compatible endpoints (llama.cpp, vLLM, Ollama's `/v1`) ignore the API key
VALUE; the client only needs it to be non-empty. A hosted provider needs its real key from
your secret manager.

Render the harness's tool schemas for the model in use with kei-agents' `render_tools()`
and `ModelFormat` (see `kei-agents`), and put each tool call behind Kei guardrails through `kei-proxy` (see
`kei-proxy` and `agentware-sdk`).

## Agentware evals (HaikeiLabs/Agentware)

- Python: `python/src/evals/models.py` — model backends incl. Ollama; examples at
  `docs/evals/examples/{ollama_example.py,openai_example.py}`.
- TypeScript: `typescript/src/evals/models.ts`; Go: `go/evals`.
- These choose the backend at CLI time; they do not ship a model or a runner.

## Validation commands

```bash
# is the endpoint OpenAI-compatible? (expects a JSON model list)
curl -s "$LLM_ENDPOINT/v1/models"

# agentware python evals against ollama
# from HaikeiLabs/Agentware: PYTHONPATH=python/src python3 -m evals.main --models ollama
```

## Providers that are not OpenAI-compatible

The supported answer is to put the provider behind an OpenAI-compatible
`/v1/chat/completions` endpoint and point `LLM_ENDPOINT` at that. Many GPU
serving stacks already expose one (vLLM, llama.cpp/llamafile, Ollama's `/v1`).
Otherwise, use a translating gateway the team runs and owns. The harness, its
tool rendering, and its evals then need no vendor-specific code.

Adding a native, non-OpenAI adapter (a new `ModelFormat`, eval model backend, or
model class) changes the project boundary. That needs a reviewed design (an
ADR or design doc approved by the harness owners) before any code. Until one
exists, do not write or outline implementation steps for it. Explain the
boundary, offer the compatible-endpoint path, and suggest opening the design
discussion.

## Realistic usage boundaries

- **Do not** add a hardcoded model vendor, a proprietary SDK, or a non-OpenAI-compatible
  endpoint assumption. The `/v1` + `chat/completions` contract is the boundary.
- **Do not** treat `OPENAI_API_KEY` as a real credential for compatible endpoints; it is
  presence-gated. Do not log it, mint it, or send it to hosts you do not trust.
- **Do not** run model-backed suites as the default CI gate — they are flaky by nature.
  Keep them behind an opt-in marker or job and keep the default gate offline.
- **Do not** confuse the harness's LLM path with a zero-LLM ingress service (see
  `kei-ingress-security`): a model must never run inside that service.

## Related skills

- `kei-headless-evals` — the eval harnesses that use these backends.
- `kei-agents` — `render_tools()` and `ModelFormat` for per-model tool schemas.
- `kei-proxy` — the allow/deny decision a harness asks for before each tool call.
- `agentware-sdk` — the middleware and KEI auth/proxy modules a harness integrates with.
