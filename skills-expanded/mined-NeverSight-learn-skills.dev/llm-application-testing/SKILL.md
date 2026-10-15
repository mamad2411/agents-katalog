---
name: llm-application-testing
description: >-
  Test LLM / generative-AI application features — chatbots, RAG, agents, tool-use —
  where output is non-deterministic and open-ended. Covers correctness/faithfulness
  evaluation AND security/safety via the OWASP Top 10 for LLM Applications (2025). Use
  when: "test an LLM feature," "LLMのテスト," "RAG evaluation," "hallucination testing,"
  "prompt injection," "jailbreak," "LLM-as-judge," "evals," "red team the chatbot," or
  shipping any feature built on an LLM. Produces an eval plan + OWASP LLM Top 10
  coverage (design mode) and eval/red-team suites, e.g. promptfoo/DeepEval/Ragas/garak
  (implementation mode). Not for: non-LLM app/API pen-testing (auth bypass, SQLi,
  dependency scans) — use security-testing; or classical/predictive ML models — use
  ml-system-testing. Related: ml-system-testing, security-testing.
license: MIT
metadata:
  version: "1.0"
  istqb: "CT-AI v2.0 §4.2 (Testing Generative AI and LLMs)"
  iso25010: [functional-suitability, security]
  iso25059: [ai-robustness, transparency, ai-functional-correctness]
  mode: [design, implementation]
---

# LLM Application Testing

Evaluate LLM-powered features on **properties and rubrics**, not exact strings, and
red-team them against the OWASP LLM Top 10 — because output varies run-to-run and the
worst failures are adversarial, not incidental.

## Objective

A repeatable evaluation harness for the LLM feature covering three axes: **quality**
(is the output correct/faithful/relevant?), **safety & security** (does it resist the
OWASP Top 10 for LLM Applications 2025?), and **regression** (do curated evals hold in
CI over prompt/model changes?). The failure mode this prevents: a demo that looks great
once, then hallucinates, leaks its system prompt, or obeys an injected instruction in
production.

## Context Discovery

- **Feature shape**: plain generation, **RAG** (retrieval), **agent/tool-use**, or
  classification-via-LLM? Each has different failure modes and metrics.
- **Harm surface**: what's the damage if it hallucinates, leaks data, or is jailbroken?
  (Sets red-team depth and which OWASP categories are in scope.)
- **Determinism controls**: can you set `temperature=0`? Is the model version pinned?
- **Ground truth / golden data**: is there a reference dataset, or must you grade with
  rubrics / LLM-as-judge?
- **Guardrails present**: input/output filtering, allow-lists, tool-permission scoping.

## Instructions

1. **Handle non-determinism** (CT-AI §4.2): do NOT assert exact string equality. Assert
   on **properties** (schema/format valid, contains/regex, no PII), **semantic
   similarity** thresholds, or **rubric scores**. Run **N samples** and require a
   **pass rate**; pin the model version and use `temperature=0` where the platform
   allows to reduce variance.

2. **Build an eval dataset ("evals")**: a curated golden set of input → expected-
   property cases, run in CI/CD with a tracked pass rate to catch regressions. Include
   **guardrail tests** (safety/refusal/injection cases that must ALWAYS pass).

3. **Grade with LLM-as-judge where no ground truth exists**: a separate, carefully-
   prompted model scores outputs against an explicit rubric using reason-then-score
   (chain-of-thought). Treat the judge as a system under test itself — calibrate it
   against human labels and watch for position/verbosity bias.

4. **RAG evaluation — the RAG triad**: **Context Relevance** (are retrieved docs
   relevant?), **Groundedness/Faithfulness** (is the answer supported by the retrieved
   context — i.e. not hallucinated?), **Answer Relevance** (does it address the query?).
   Ungrounded output = hallucination (OWASP **LLM09 Misinformation**).

5. **Security & safety via OWASP LLM Top 10 (2025)** — cover the applicable categories
   with concrete tests, especially:
   - **LLM01 Prompt Injection** — direct (malicious user input) and **indirect**
     (malicious instructions hidden in retrieved/ingested content).
   - **LLM02 Sensitive Information Disclosure** — probe for PII/secret leakage.
   - **LLM05 Improper Output Handling** — LLM output flows into a sink (HTML/SQL/shell)
     without sanitization → XSS/SSRF/code exec.
   - **LLM06 Excessive Agency** and **LLM07 System Prompt Leakage** for agents.

6. **Red teaming** (CT-AI §4.2): adversarial probing for harmful, biased, unsafe, or
   policy-violating outputs — manual and automated (auto-generated adversarial cases) —
   before release.

7. **Enforce guardrails server-side and validate output**: input/output filtering,
   tool-permission scoping, structured-output validation.

## Output Format

### design mode

```
# LLM Eval Plan: {feature}
## Feature shape (gen / RAG / agent) + harm surface
## Determinism strategy (temp, model pin, N samples, pass-rate)
## Quality metrics (rubric / RAG triad: context-relevance, groundedness, answer-relevance)
## Eval dataset spec (golden cases + guardrail cases that must always pass)
## OWASP LLM Top 10 (2025) coverage
   | ID | Category | Applicable? | Test / probe | Tool |
## Red-team charter (adversarial goals)
```

### implementation mode

Assert on properties, not exact text (promptfoo/DeepEval idiom):

```yaml
# promptfoo — property + rubric assertions, run over N cases
tests:
  - vars: { query: "What is our refund window?" }
    assert:
      - type: contains
        value: "30 days"
      - type: llm-rubric            # LLM-as-judge
        value: "Answer is grounded in the provided policy; no invented terms."
      - type: not-icontains
        value: "ignore previous instructions"   # injection leakage check
```

RAG metrics with **Ragas**/**TruLens**; automated vuln scanning with **garak**;
runtime guardrails with **NeMo Guardrails**. Verify tool/probe names against installed
versions.

## Anti-Patterns

- **Exact-match assertions** — `assert output == "..."` on non-deterministic text.
  **Guard:** assert properties/rubrics/semantic similarity; never exact equality.
- **Single sample** — judging quality from one generation. **Guard:** N samples + pass
  rate; pin model version; temp=0 where possible.
- **BLEU/ROUGE for open-ended output** — n-gram overlap penalizes valid paraphrases and
  misses factuality. **Guard:** use LLM-as-judge / rubric / groundedness for open-ended
  tasks; reserve overlap metrics for closed tasks (translation/summarization).
- **Trusting the judge blindly** — LLM-as-judge with unvalidated, biased scoring.
  **Guard:** calibrate against human labels; control for position/verbosity bias.
- **Quality-only, no red team** — evaluating helpfulness but never adversarial safety.
  **Guard:** OWASP LLM Top 10 coverage; prompt-injection (incl. indirect) tests are
  mandatory for any RAG/agent.
- **Client-side-only guardrails** — a filter the API doesn't enforce. **Guard:**
  guardrails and output validation live server-side; test the API directly.
- **Hallucinated OWASP IDs** — citing LLM-category names/IDs from memory. **Guard:**
  use the current OWASP LLM Top 10 (2025) IDs/names; verify against the list.

## Related Skills

- `ml-system-testing` — classical/predictive ML (statistical metrics, drift); this
  skill covers generative/LLM features.
- `security-testing` — app-layer security; LLM01/LLM05 connect LLM output to classic
  injection sinks — coordinate.

## References

- OWASP Top 10 for LLM Applications 2025 — https://genai.owasp.org/llm-top-10/
- ISTQB CT-AI v2.0 §4.2 (Testing Generative AI and LLMs; red teaming, exploratory)
- RAG triad (Context Relevance / Groundedness / Answer Relevance) — TruLens
- ISO/IEC 25059:2023 — AI robustness, transparency, AI functional correctness
- Note: ISTQB **CT-GenAI** is about *using* GenAI to assist testing (prompt engineering,
  LLM-in-test-infra) — a complementary reference, not the basis for testing LLM products
- Tools: promptfoo, DeepEval, Ragas, TruLens, garak, NeMo Guardrails, Giskard
