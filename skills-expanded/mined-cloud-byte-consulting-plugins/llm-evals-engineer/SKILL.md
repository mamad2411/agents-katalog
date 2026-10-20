---
name: llm-evals-engineer
description: >-
  Evaluate and production-harden LLM applications end to end. Use when the user
  says "evaluate my LLM app", "add evals", "is my RAG hallucinating", "RAG
  quality metrics", "LLM-as-judge", "add tracing for my chatbot", "guardrails",
  "prompt versioning", "rate-limit my LLM spend", "LLM budgets", or "make my
  LLM app production-ready". Covers tracing architecture (callback handler plus
  decorator instrumentation, trace-per-query spans, session/user propagation),
  the score data model, Ragas-style metrics (context precision/recall, context
  entities recall, noise sensitivity, faithfulness, response relevancy, tool call
  accuracy), LLM-as-judge pipelines, prompt versioning, chat-history trimming,
  input guardrails, and gateway controls. Langfuse, Ragas, NeMo Guardrails,
  LiteLLM, and Redis are example capability fills. For trust auditing of
  autonomous agent actions and delegation gates, use agent-trust-auditor.
---

# LLM Evals Engineer

## Purpose

Take an LLM application from "it seems to work" to measured, gated, and production-hardened. This skill covers the full arc: instrumenting tracing, defining a score model, building an offline eval set from real traffic, wiring a metric suite that separates retrieval failures from generation failures, adding an LLM judge for dimensions humans can't score at volume, gating deploys on eval thresholds, and enforcing production controls (prompt versioning, bounded chat history, input guardrails, gateway budgets).

The stack is described as **capability slots**, each with a concrete reference tool. Substitute freely — the architecture, not the vendor, is the deliverable:

| Slot | Capability | Reference tool |
|---|---|---|
| Tracing platform | traces, spans, sessions, scores, prompt registry, datasets | Langfuse |
| Metric suite | reference-implemented RAG/agent metrics | Ragas |
| Rails engine | input/output validation flows | NeMo Guardrails |
| Gateway | unified API, keys, budgets, rate limits | LiteLLM proxy |
| History store | TTL-capable chat message persistence | Redis |

Cross-references: after the eval gate passes, hand off to **llm-app-deployer** (same pack) for shipping. For judging *autonomous agent* outputs — multi-step plans, tool-use trajectories, trust/safety verification of agent actions — route to **agent-trust-auditor**; this skill evaluates the *application* layer (retrieval + generation quality), not agent-level output trustworthiness.

## Core model

### Tracing architecture

Use **dual instrumentation** — the two mechanisms cover different code:

1. **Callback handler** for framework-managed calls: create ONE handler instance before the conversation loop and pass it on every invoke — `config={"callbacks": [handler], "run_name": "context"}`. Works with `.invoke()`, `.batch()`, and streaming. Do not construct a new handler per call.
2. **Decorator** (`@observe(name="generate-context")`) for arbitrary non-framework functions: data loaders, tool executors, embedding jobs — anything the framework's callbacks can't see.

**Trace-per-query, grouped by session** is the target shape:

```python
session_id = f"session-{uuid.uuid4().hex[:8]}"   # once at startup, with user_id

while True:  # conversation loop
    with langfuse.start_as_current_observation(
        as_type="span", name="user-query", input=user_input
    ) as span:
        with propagate_attributes(session_id=session_id, user_id=user_id):
            # named child runs: "context", "final-response", "goodbye-message"
            ...
        span.update(output=final_answer)
```

`propagate_attributes` stamps session/user (and tags) on all child observations; for one-off attribution, pass `metadata={"langfuse_session_id": ..., "langfuse_user_id": ...}` in the invoke config instead. Result: every query is one trace with named spans, tokens, cost, and latency; the session filter reconstructs whole conversations.

### Score data model

All evaluation results — human, heuristic, or model-based — are stored as **scores**: numeric, categorical, or boolean, with optional comments, attachable at **trace**, **observation**, or **session** level.

**Session-level-scoring rule:** for conversational apps, attach satisfaction-style feedback at the *session* level, because satisfaction spans turns — a great turn 3 doesn't redeem a useless conversation. Individual traces stay visible under the session for debugging.

```python
langfuse.create_score(
    session_id=session_id, name="conversation_usefulness",
    value=feedback, data_type="CATEGORICAL", comment=reason,
)
```

Three evaluation methods, in maturity order: (1) **user feedback** — implicit experts, cheap, coarse; (2) **manual annotation** — explicit experts scoring faithfulness / answer relevancy / context recall against score configs; high quality, slow at volume, and the source of your golden dataset; (3) **LLM-as-judge** — scales annotation; needed because lexical-overlap metrics (BLEU/ROUGE) cannot distinguish a factually correct answer from a similarly-worded wrong one.

### Metric taxonomy (diagnose retrieval and generation separately)

A two-chain RAG app (retrieve context → generate answer) fails in two independent places; metrics must isolate which.

**Retriever metrics** — is the right context arriving?
- *Context precision*: fraction of retrieved passages that are relevant. Catches noisy retrieval / bad ranking.
- *Context recall*: was all necessary information fetched? Catches missing chunks, bad k, index gaps.
- *Context entities recall*: entity-level drill-down — did retrieval surface the specific names/specs/numbers the answer needs? Use for fact-heavy domains.
- *Noise sensitivity*: how often irrelevant retrieved context induces errors in the answer. Catches a generator that gets distracted.

**Generation metrics** — given the context, is the answer right?
- *Faithfulness*: every claim in the answer must be supported by the provided context. This is the anti-hallucination metric.
- *Response relevancy*: on-topic and actually answers the question asked.

**Agentic metrics** — *tool call accuracy*: right tool selected, correct parameters supplied. Add as soon as the app makes tool calls; expand as it becomes more agentic (and see agent-trust-auditor for full trajectory judging).

#### Metric-selection decision guide (symptom → metric)

| Symptom | Check first |
|---|---|
| Answers invent facts not in the docs | Faithfulness; if low, then context recall (maybe the facts were never retrieved) |
| Answers are correct but off-topic / don't address the question | Response relevancy |
| Retrieval returns lots of junk alongside the right chunk | Context precision |
| Answers miss information that exists in the corpus | Context recall |
| Specific entities (model names, prices, dates) are wrong or missing | Context entities recall |
| Answer quality degrades when k is raised or corpus grows | Noise sensitivity |
| Wrong tool invoked, or right tool with wrong arguments | Tool call accuracy |

Rule of thumb: **low faithfulness + high context recall = generation problem; low faithfulness + low context recall = retrieval problem.** Fix retrieval first — a generator cannot be faithful to context it never received.

### LLM-as-judge pipeline mechanics

Judges run either from the tracing platform's UI (add an LLM connection, create an evaluator, execute over traces or datasets) or programmatically (run the metric suite, push results via `create_score`).

**The variable-mapping pitfall:** every judge metric expects specific inputs (user query, retrieved context, generated answer, sometimes reference answer). When wiring an evaluator you map your trace fields to those inputs. **Mis-mapping does not error — it silently produces plausible-looking false scores** (e.g., judging faithfulness of the answer against the *query* instead of the *context*). After wiring any evaluator, spot-check 3–5 judged traces by hand and confirm the judge's written reasoning references the right text before trusting a single aggregate number.

### Eval-maturity ladder

1. **Tracing only** — you can see what happened, but nothing is scored.
2. **Offline metric suite** — a curated dataset from real traces, retriever + generation metrics run on demand.
3. **LLM-as-judge in CI** — metrics run automatically; deploys gate on thresholds.
4. **Production scoring loop** — live traffic sampled and judged continuously; user feedback, budgets, and guardrails feed back into the dataset.

Place the app on this ladder first; build the next rung, not the top one.

## Workflow

1. **Instrument tracing.** Dual instrumentation (callback handler + decorator), trace-per-query with named spans (`context`, `final-response`, ...), session/user propagation from startup. Verify traces show tokens, cost, latency, and full inputs/outputs before proceeding — everything downstream consumes traces.
2. **Define the score model.** Decide names, data types, and attachment levels up front. Conversational satisfaction → session level. Per-answer quality → trace level. Per-retrieval quality → observation level. Add an end-of-session user-feedback prompt.
3. **Build an offline eval set from real traces.** Manually annotate a sample of production/dev traces on faithfulness, answer relevancy, and context recall; promote annotated traces into a curated dataset. Aim for [50–200] examples covering your main intents and known failure modes before trusting aggregates.
4. **Wire the metric suite with the retriever/generation split.** Run context precision + context recall (add entities recall and noise sensitivity for fact-heavy domains) and faithfulness + response relevancy over the dataset. Record baselines per metric.
5. **Add a judge for unscorable dimensions.** Tone, scope compliance (e.g., "never recommend a product not in context"), policy adherence — anything without a reference answer. Map variables, then hand-verify judged samples (see pitfall above).
6. **Gate deploys on eval thresholds.** Run the suite in CI against the dataset; block merge/deploy if any metric drops more than [5]% below baseline or faithfulness falls below [0.8]. Prompt changes go through the same gate — that's what versioned prompts (below) make cheap.
7. **Production scoring + enforcement.** Sample live traces for continuous judging, keep the user-feedback loop writing session scores, and turn on the production controls in Guardrails below. New failure modes discovered in production get added to the offline dataset — the loop closes.

## Guardrails

**Prompt versioning (registry slot).**
- Move every prompt out of code into the registry under **fixed names** (e.g., `context_system_prompt`, `review_system_prompt`); the app fetches by name at startup.
- **Link the prompt object to traces** (e.g., `prompt.metadata = {"langfuse_prompt": lf_prompt}`) so cost, latency, and scores accumulate per prompt *version* — this is what makes rollback and A/B comparison a dashboard read instead of an archaeology dig.
- No platform? Version prompts as YAML/JSON in git; never inline strings edited in place.

**Chat-history persistence (history store slot).**
- **Persist only the user message and the final assistant message per turn.** Auto-persist-everything wrappers store tool calls and intermediate AI messages too — bloating both storage and every future prompt. Tool traffic lives one turn only: load history, run chains on an in-memory copy, write back exactly two messages.
- Set a **TTL** on histories (e.g., 3600s) and add **token-based trimming** in the pipeline: `trim_messages(strategy="last", token_counter=llm, max_tokens=[500], start_on="human", include_system=True)` inserted between prompt and model. Tune max_tokens as cost-vs-context balance, not a constant.

**Input guardrails (rails slot).**
- Config pattern: a rails directory with (a) a config declaring the model, an `instructions` block describing the bot being protected, and `rails.input.flows: [self check input]`; (b) a prompts file whose `self_check_input` task lists the blocklist (harmful content, out-of-scope requests, impersonation, "forget your rules", system-prompt extraction, abusive language, sensitive personal info) and ends in a binary "Should the user message be blocked (Yes or No)?".
- **Validate before the chains, not piped into them.** Invoke the rail separately on the raw input; on block, return the canned response and `continue` — skip tool calls, skip generation, skip history persistence. Rationale: early exit before expensive LLM calls (blocked input never reaches the main model with full chat history), no message-serialization issues, explicit blocked/allowed control flow. Still log blocked requests to tracing so rules can be tuned.
- Guardrails complement good prompts; they do not replace them.

**Gateway controls (gateway slot).**
- **Pin an exact image version, never `:latest`.** Gateway images have been supply-chain-compromised in the wild, and `:latest` users were auto-affected while pinned users were not. Use signed, SemVer-tagged releases; read security advisories; test upgrades in staging.
- Per-deployment **rpm/tpm limits** in the model list; retries and model fallback at the gateway, not in app code.
- **Budgets with a duration**: a max budget means nothing without `budget_duration` (`1d`, `1h`, ...) — otherwise it's a lifetime cap that either never triggers or bricks the app permanently.
- **Virtual keys** per app/environment, each with its own model allowlist and budget; the app gets a virtual key and the gateway base URL, never a raw provider key.
- **Tiered end-user budgets**: register users against budget tiers at signup, and make the app pass the user id on every LLM call (e.g., `model_kwargs={"user": user_id}`) — the gateway can only meter what it can attribute.
- Route gateway-level LLM logs into the tracing platform (success callback) so proxy traffic and app traces reconcile.

**Evaluation-integrity guardrails.**
- Never report a judge metric you haven't spot-checked against hand-labeled examples.
- Don't tune prompts against the same dataset split you gate on — hold out.
- Session-level scores for conversation quality; trace-level scores for answer quality. Mixing levels corrupts both aggregates.

## Suggested effort

- **Add tracing to an existing app:** 1–2 hours. Callback handler + spans + session propagation; verify in the UI.
- **First offline eval set + metric suite:** half a day to a day, dominated by annotating [50+] traces well. Do not skimp — every later number inherits this dataset's quality.
- **LLM-as-judge in CI with deploy gates:** half a day, including the mandatory hand-verification of judge outputs.
- **Full production hardening** (prompt registry, history store, rails, gateway with budgets/keys): 1–2 days for the reference stack, mostly Docker plumbing and config; each slot is independently shippable, so land them in the Guardrails order above.
- When time is short: tracing and the retriever/generation metric split deliver the most diagnostic power per hour. Guardrails and budgets are the first thing to add once real users (and real money) touch the app.
