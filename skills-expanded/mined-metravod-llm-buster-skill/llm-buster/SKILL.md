---
name: llm-buster
description: "Use this skill when the user asks to audit a codebase for LLM API calls (OpenAI, Anthropic — Python and TS/JS SDKs plus equivalent raw HTTP) and decide which calls can be replaced with deterministic logic. Activates on phrases like 'audit LLM usage', 'bust LLM calls', 'bust the LLM here', 'llm-bust this', 'do I actually need an LLM here', 'replace LLM with deterministic', 'de-LLM this', 'find LLM calls', 'cut LLM costs', 'is this prompt necessary'; on grep hits for `openai.`, `client.chat.completions.create`, `from anthropic import`, `client.messages.create`, `api.openai.com/v1/chat/completions`, `api.anthropic.com/v1/messages`; and on questions about whether a specific LLM call could be a regex, parser, classifier, lookup, or rule. Produces a per-call audit report with 🟢/🟡/🔴 verdicts and concrete deterministic alternatives. Does NOT rewrite code unless the user explicitly asks after seeing the report."
metadata:
  version: "1.0.0"
  scope: "openai-anthropic-audit"
  file_policy: "markdown-only"
---

# llm-buster skill

Use this skill when the user wants to know **which LLM calls in an existing codebase are doing work a regex, parser, classifier, or lookup table could do for free**. The skill is an audit tool, not a refactoring tool — it surfaces call sites, classifies the task, applies a rubric, proposes a deterministic replacement, and estimates impact. The user decides what to actually swap.

## Core stance

LLMs are paid wizards. They earn their keep when the input is open-ended, the output requires reasoning or generation, or the task surface is too broad to specify. They are wildly overused for tasks a 20-line parser would nail.

Three load-bearing consequences:

1. **The prompt is the spec.** If the prompt names a fixed set of fields, a finite set of categories, or a format conversion — that spec can usually be written in code. Read the prompt before reading the SDK call.
2. **Variability of input is the deciding factor.** A "classify support ticket" call over emails from 12 known templates is different from the same call over free-form user chat. Same SDK, opposite verdicts.
3. **The LLM was probably right when added.** Do not assume the original author was lazy. Sometimes the LLM is absorbing edge-case complexity that a regex would silently corrupt. When in doubt, mark 🟡 and recommend a shadow-mode A/B, not a swap.

## What the report looks like

One block per call site, grouped 🟢 → 🟡 → 🔴. Example of a single finding (full template in [references/report.md](references/report.md)):

> **🟢 — `services/intent.py:42`**
>
> Task: classification (3 fixed labels: `refund` / `shipping` / `other`).
> Prompt is a system message listing the labels with 4 hardcoded few-shot examples; output is parsed with `label = resp.choices[0].message.content.strip().lower()`.
>
> **Replacement:** `rapidfuzz.process.extractOne(text, LABELS, scorer=fuzz.token_set_ratio)` with a 60-score floor, fallback to `"other"`. ~15 lines.
>
> **Risks:** loses ability to handle paraphrases the few-shots didn't cover ("money back" → `refund`). Mitigate by adding aliases to a dict, or shadow-mode for a week against the live LLM and grow the alias list from disagreements.
>
> **Per-call cost:** ~280 input + ~3 output tokens on `gpt-4o-mini` ≈ \$0.00005. `× requests/month = $TBD`.

The audit ends with one closing line: *"Want me to apply the 🟢 replacements?"*

## When to activate

Activate on any of:

- user asks to "audit / inventory / find / list" LLM calls in a project;
- user asks "do I need an LLM here", "can I drop this prompt", "is this overkill";
- user asks to "cut LLM costs" or "reduce token spend" via deterministic replacement;
- working directory has `import openai`, `from anthropic`, `@anthropic-ai/sdk`, `openai` (npm), or HTTP to `api.openai.com` / `api.anthropic.com`;
- working directory has imports of common multi-provider wrappers — `litellm`, `google.genai` / Vertex Gemini SDK, `boto3` with `bedrock-runtime`, `ollama`. The skill still activates here but operates in **detection-only** mode for those providers — see [references/detection.md](references/detection.md) § "Detection-only providers". Replacement recipes still target OpenAI/Anthropic call sites in the same repo;
- user explicitly invokes `/llm-buster` or names this skill.

Do **not** activate for:

- adding new LLM features (out of scope — this is removal-oriented);
- migrating between providers (OpenAI ↔ Anthropic);
- prompt engineering or quality improvement of an existing LLM call;
- generic "should I use AI for X" greenfield design questions.

## First action: scope check, then inventory

### Scope sanity check (10 seconds)

Before running grep, confirm you're actually looking at a project and not a one-shot scratch file. Check three things:

```bash
ls -la             # is there a .git/ ? a pyproject.toml / package.json / Cargo.toml ?
find . -type f -not -path '*/\.*' | wc -l   # how many tracked files?
```

If the answer is "one loose .py file" or "no project metadata", abort the per-call report machinery and just inspect the file conversationally — a 200-line script doesn't need a verdict table, a per-file pivot, or a duplication pass. Tell the user: *"This looks like a single script, not a project — I'll skip the audit format and just walk through the LLM calls inline. OK?"*

### Inventory grep

From the project root. Two passes — the second is for the broader provider surface so the user sees their full LLM cost footprint (calls there enter **detection-only mode** — see next section).

```bash
# Pass 1 — in-scope: OpenAI + Anthropic SDKs and raw HTTP. Full replacement recipes apply.
rg -n --no-heading -e 'from openai' -e 'import openai' -e 'openai\.' \
   -e 'from anthropic' -e 'import anthropic' -e 'anthropic\.' \
   -e 'client\.chat\.completions\.create' -e 'client\.messages\.create' \
   -e 'api\.openai\.com' -e 'api\.anthropic\.com' \
   --glob '!**/node_modules/**' --glob '!**/.venv/**' --glob '!**/dist/**'

# TS/JS
rg -n --no-heading -e "from ['\"]openai['\"]" -e "from ['\"]@anthropic-ai/sdk['\"]" \
   -e 'new OpenAI\(' -e 'new Anthropic\(' \
   --glob '!**/node_modules/**' --glob '!**/dist/**'

# Pass 2 — detection-only: other providers and wrappers. Verdict rubric applies; no replacement recipes.
rg -n --no-heading \
   -e 'import ollama' -e 'from ollama' -e 'ollama\.(chat|generate)\(' \
   -e 'from litellm' -e 'litellm\.' \
   -e 'from google import genai' -e 'google\.generativeai' -e 'from vertexai' -e 'GenerativeModel\(' -e 'generate_content\(' \
   -e "boto3\.client\(['\"]bedrock-runtime" -e 'invoke_model\(' -e '\.converse\(' \
   -e 'from langchain_(google_genai|aws|ollama|mistralai|cohere)' \
   -e 'from llama_cpp' -e 'localhost:(11434|8000)/v1' \
   --glob '!**/node_modules/**' --glob '!**/.venv/**' --glob '!**/dist/**'
```

If `rg` is unavailable, `grep -rn` with the same patterns works. If pass 1 returns hits, you usually don't need to chase wrapper frameworks (LangChain `ChatOpenAI`, instructor, LiteLLM to OpenAI) — most projects also call the SDK directly somewhere. See [references/detection.md](references/detection.md) for AST queries and the full wrapper pattern list when grep misses.

This produces the call-site list. Everything downstream operates on that list.

## If only detection-only calls are found

When pass 1 is empty but pass 2 has hits, the project is non-OpenAI/Anthropic (Gemini, Bedrock, Ollama, etc.). The audit still runs — same scope check, same per-call loop, same verdict rubric — but each finding **omits the proposed replacement code block** and instead writes:

> *Replacement recipe out of scope for this skill version (provider: `<gemini|bedrock|ollama|...>`); the rubric still applies and this call is a candidate for deterministic replacement using the same task category.*

Also: do not report dollar savings for local runtimes (Ollama, vLLM, llama-cpp) — substitute "latency / GPU-time saved" qualitatively. See [references/detection.md](references/detection.md) § "Detection-only providers" for the per-provider grep patterns and edge cases.

## How to use this skill

Load references on demand, not all up front:

- **[references/detection.md](references/detection.md)** — grep patterns, AST queries, wrapper detection (LangChain, LiteLLM, instructor). Load when the basic inventory grep misses calls or returns false positives.
- **[references/taxonomy.md](references/taxonomy.md)** — the 10 task categories (extraction, classification, routing, validation, normalization, summarization, rephrasing, generation, reasoning, agentic). Load when classifying a specific call.
- **[references/rubric.md](references/rubric.md)** — the 🟢 / 🟡 / 🔴 decision rules with disqualifiers. Load when deciding the verdict for a call.
- **[references/replacements.md](references/replacements.md)** — concrete code recipes per task category (regex, `pydantic`, `dateutil`, `rapidfuzz`, sklearn TF-IDF + LogReg, `email-validator`, sentence-transformers). Load when writing the proposed replacement for a 🟢 or 🟡 call.
- **[references/report.md](references/report.md)** — the report template the audit emits. Load when assembling the final output.

## Per-call analysis loop

For each call site found in inventory, run these five steps in order. Do not skip step 2.

1. **Read the prompt template, not just the SDK call.** The classification depends almost entirely on what the prompt asks the model to do. Resolve f-strings, template literals, message arrays — find the actual instruction text. If the prompt is dynamically assembled from a database or config, note that and ask the user for a sample.
2. **Identify the output contract.** Is `response_format={"type":"json_object"}` set? Is there a `tools=` / `tool_choice=` argument forcing a function call? Is the assistant text parsed with `json.loads`, a regex, or fed verbatim to a user? The contract tells you whether the call is structured (replaceable candidate) or freeform (probably not).
3. **Classify the task.** Map to one of the 10 categories in [references/taxonomy.md](references/taxonomy.md). If two fit, pick the dominant one; note the secondary.
4. **Apply the rubric.** From [references/rubric.md](references/rubric.md): 🟢 / 🟡 / 🔴. Apply disqualifiers (free-form input, open-ended output, multi-step reasoning, unbounded category space) — any one disqualifier downgrades the verdict.
5. **For 🟢 and 🟡 only — propose a replacement.** Pull the recipe from [references/replacements.md](references/replacements.md), adapt to the call's actual inputs/outputs, and write the snippet inline in the report. For 🔴, write one sentence on _why_ it stays.

## Verdict rubric — short version

Full table in [references/rubric.md](references/rubric.md). Five verdict modes:

- 🟢 / 🟡 / 🔴 — standard colour rubric for in-scope local calls.
- ❌ Out of scope — call exists for benchmarking, training-data generation, or as a baseline being evaluated. Replacing it defeats the purpose of the code.
- 🔵 Delegated — repo is a thin client to a remote service; all LLM work runs server-side. Audit pivots to architecture-level recommendations.

Decision shortcut for the colour rubric:

| Signal | Verdict |
|---|---|
| Fixed output schema + structured/semi-structured input + finite domain | 🟢 |
| Fixed schema but messy input (OCR, free-form chat, mixed languages) | 🟡 |
| Finite category set (≤ ~20 labels) + ≥100 labeled examples available | 🟡 |
| **Deterministic sub-task buried inside an otherwise-LLM prompt** (heuristic, pick-from-list, ratio bucketing) | 🟡 (sub-task extraction) |
| Prompt contains "explain", "summarize", "rephrase", "write", "answer the user's question" | 🔴 |
| Output is shown verbatim to a human end-user as natural language | 🔴 |
| Multi-step reasoning, chain-of-thought, or agentic tool-loop | 🔴 |
| Stateful conversation context required | 🔴 |
| Reasoning over free-form prose produced by another LLM upstream | 🔴 (hard — see H3 in [references/rubric.md](references/rubric.md)) |

When two rows fight, the **harder** verdict wins (i.e. 🔴 trumps 🟢). Structural verdicts (❌, 🔵) replace the colour, not extend it.

## Non-negotiables

- **Do not rewrite code on a first pass.** Output is the audit report. Only swap code when the user explicitly says "apply the 🟢 replacements" or names specific call sites after reading the report.
- **Do not downgrade an LLM call without reading the prompt.** SDK call detection is not classification. Two `client.chat.completions.create` calls can be 🟢 and 🔴 sitting in adjacent files.
- **Do not propose regex for free-form natural language.** Regex against user-generated content is a footgun. If the prompt's input includes "user's message", "support ticket body", "tweet", "chat history" — that's a disqualifier toward 🔴 unless the task is hard validation (length, format).
- **Do not estimate dollar savings without call volume.** If the user hasn't provided traffic numbers, show the per-call token cost only (input tokens × price + output tokens × price), and label the monthly figure as `× requests/month = $TBD`. Do not invent traffic.
- **Do not claim a replacement is "drop-in" without listing what changes.** Latency profile, error modes, and edge-case coverage all shift when you replace an LLM with a parser. The report's "Risks" field is mandatory for 🟢 and 🟡.
- **Do not count tokens by character length.** Use this fallback order, in order, and stop at the first that works:
  1. `tiktoken` for OpenAI models (`pip install tiktoken`, then `encoding_for_model("gpt-4o-mini").encode(text)`).
  2. Anthropic's `client.messages.count_tokens(...)` API for Anthropic models — costs nothing and returns exact counts.
  3. `anthropic-tokenizer` (TS) / `gpt-tokenizer` (TS) for JS projects without Python tooling.
  4. If none of the above is reachable in the audit environment, mark the per-call savings as `tokens: estimate pending — install tiktoken` and proceed. Do **not** substitute `len(text) / 4` or any other char-based heuristic; it's off by 30–60% on code and structured data and silently inflates the savings table.
- **Do not treat `tools=`/`tool_choice=` calls as freeform.** A forced function call with a fixed JSON schema is structured output — it is a 🟢/🟡 candidate, not 🔴.
- **Do not skip the prompt because it's long.** Long system prompts often encode the entire deterministic spec verbatim (a 2000-token system message describing 8 fields is screaming "I am a parser"). Read it.

## Default output structure

When the user asks "audit this project" or "is this LLM call necessary", produce the report from [references/report.md](references/report.md):

1. **Header line** — `N calls found across M files`.
2. **Verdict table** — counts per 🟢 / 🟡 / 🔴 with estimated savings.
3. **One block per call**, ordered 🟢 → 🟡 → 🔴, each with:
   - location (`file:line`);
   - current snippet (the SDK call + the prompt template);
   - detected task category;
   - verdict + one-line justification;
   - proposed replacement code (🟢 / 🟡 only);
   - risks / edge cases the LLM was likely catching;
   - per-call token cost estimate.
4. **Closing line** — what to do next: "Want me to apply the 🟢 replacements?" or "Sample real inputs for the 🟡 calls before deciding."

If the project has > ~15 call sites, group by file rather than listing all inline, and offer to deep-dive a subset.

## Gotchas

- **Wrapper frameworks hide the prompt.** LangChain's `LLMChain(prompt=PromptTemplate(...))` and instructor's `client.chat.completions.create(response_model=MyModel)` both wrap the underlying call. Find the template / pydantic model — that's the spec. See [references/detection.md](references/detection.md).
- **Jupyter notebooks need cell extraction first.** Naive `rg` over `.ipynb` returns JSON-escaped fragments (`"    response = requests.post(...)\n"`). Convert with `jupyter nbconvert --to script` or the stdlib snippet in [references/detection.md](references/detection.md) before classifying.
- **Umbrella / multi-subproject repos blow up per-call mode.** When the repo has ≥ 3 subprojects, lead with a per-subproject table and deep-dive only the top 2–3 with actionable findings. See [references/report.md](references/report.md) § "Umbrella-repo mode".
- **Same call in N files is one finding, not N.** Five sites running the same FinBERT-replaceable sentiment call should be reported as one consolidated 🟡 with a cross-reference table — see [references/report.md](references/report.md) § "Duplication pass".
- **Research/benchmark code is ❌, not 🔴.** Calls inside `Evaluation_methods/`, `data_gen/`, `prepare_data/`, or LLM-as-judge harnesses cannot be replaced with deterministic code by definition. Tag as ❌ and skip the colour rubric — see [references/rubric.md](references/rubric.md) § "❌ Out of scope".
- **Thin clients to remote agentic services are 🔵.** When the standard grep returns zero direct LLM calls but the README describes an LLM product, the LLMs are server-side. Pivot to architecture-level recommendations — see [references/rubric.md](references/rubric.md) § "🔵 Delegated".
- **A `temperature=0` call is not automatically deterministic-replaceable.** Temperature 0 means low randomness, not low complexity. The task might still be open-ended.
- **`response_format={"type":"json_object"}` ≠ schema-bound.** Without a JSON Schema (via `tools=` or `response_format={"type":"json_schema",...}`), the model can return any JSON shape. Calls with a true schema are stronger 🟢 candidates than calls with just `json_object`.
- **Few-shot prompts are red herrings.** A prompt with 5 hardcoded `input → output` examples is usually 🟢 — those examples _are_ the lookup table. Build a dict from the examples and pattern-match.
- **`gpt-4o-mini` / `claude-haiku` calls feel cheap, so people don't audit them.** Volume × cheap-per-call still adds up; cheap models also have worse JSON adherence, meaning a deterministic replacement often _improves_ reliability while cutting cost. Include cheap-model calls in the audit.
- **Streaming calls (`stream=True`) are usually generation.** If output is streamed to a UI, it's almost always 🔴 — the user is reading text as it arrives. Don't propose replacing those.
