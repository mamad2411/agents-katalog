---
name: llm-feature-design
description: Design LLM-powered features that survive production - model choice, prompt structure, structured output, fallbacks, cost control, evals, and guardrails. Use when the user wants to add AI/LLM functionality to a product, asks about prompt design, RAG, agent features, handling model failures, or evaluating LLM output quality.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, write
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [llm, ai, prompts, evals, guardrails]
---

# LLM Feature Design

An LLM feature is a **probabilistic component inside a deterministic system**. Design for the 5% of calls that go wrong, not the demo that went right.

## When to use

- "Add an AI feature that…" (summarize, classify, extract, generate, chat)
- Choosing between models, or between LLM and non-LLM solutions
- "The prompt works sometimes" / output quality is inconsistent
- Reviewing an LLM integration before launch

## Principles

- **LLM last.** If regex, SQL, or a rules engine solves it, use that. LLMs buy flexibility at the cost of latency, money, and nondeterminism.
- **Structured in, structured out.** Free-text responses parsed with string-splitting is a production incident on a timer. Use schemas/tool calls.
- **The prompt is code.** Versioned, reviewed, tested — never edited live in a dashboard.
- **No evals, no iteration.** Without a measured baseline, every prompt "improvement" is a coin flip.

## Process

### 1. Frame the task

- What's the *exact* job? (classify into N labels ≠ summarize ≠ extract fields ≠ open generation)
- What does failure cost? Wrong label in an internal tool vs wrong refund amount to a customer → very different designs
- **Could this be done without an LLM?** Write down why not.

### 2. Choose the shape

| Task | Shape |
|---|---|
| Classification / extraction | Single call, structured output (JSON schema / tool call), low temperature |
| Summarization / rewriting | Single call, length + style constraints in prompt |
| Q&A over own data | RAG: retrieve → ground → answer with citations |
| Multi-step with side effects | Agent with tools — only if a fixed pipeline truly can't work |

Pick the **smallest model that passes your evals**; upgrade on evidence, not vibes.

### 3. Design the prompt

- Structure: role → task → constraints → examples (few-shot) → input
- Put variable user content in **clearly delimited** sections; treat it as untrusted (prompt injection)
- Specify the output schema and the *failure behavior*: "If the answer is not in the context, return `null`" — give the model an out, or it will invent one

### 4. Engineer the failure paths

- **Validation:** parse + schema-check every response; on failure → one retry with the error fed back, then fallback
- **Fallback:** deterministic default, cached previous result, degraded UX, or human handoff — never a raw stack trace
- **Timeouts + budgets:** max tokens, max retries, max $/request; rate-limit per user
- **Idempotency** for anything with side effects

### 5. Build evals before shipping

- Collect 20–100 representative inputs (include the ugly ones) with expected outputs
- Score automatically where possible (exact match, schema validity, contains-citation); LLM-as-judge for fuzzy quality, spot-checked by humans
- Run evals on every prompt/model change — this is your regression suite

### 6. Guardrails & ops

- Input: size limits, injection screening for high-stakes actions
- Output: PII/unsafe-content filtering where relevant; citations required for factual claims from RAG
- Log prompt version, model, latency, token cost per call; alert on error-rate and cost anomalies
- Plan for model deprecation: pinned model versions + eval suite = safe upgrades

## Output format

```markdown
## LLM feature: <name>

**Task:** … **Why LLM:** …
**Shape:** single call / RAG / agent. **Model:** … (smallest that passes evals)

### Prompt contract
Input: … → Output schema: … → On unanswerable: …

### Failure handling
| Failure | Behavior |
|---------|----------|
| Invalid output | retry ×1 w/ error → fallback: … |
| Timeout | … |

### Evals
Dataset: N cases. Metrics: … Baseline: …%

### Cost & limits
~$/request, max tokens, rate limit.
```

## Anti-patterns

- ❌ Shipping on "it worked in the playground" with zero evals
- ❌ Parsing free-text output with regex instead of demanding structured output
- ❌ No "I don't know" path — forcing the model to always answer manufactures hallucinations
- ❌ User input concatenated raw into the prompt for a feature with side effects
- ❌ Defaulting to the biggest model without testing a smaller one
- ❌ Prompt edited in production with no version history
- ❌ Unbounded loops in agents — no max iterations, no budget
