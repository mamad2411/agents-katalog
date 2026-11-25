---
name: deepeval-llm-tests
description: >
  Author and run DeepEval (Confident AI) test cases for LLM apps: answer relevancy,
  faithfulness, hallucination, toxicity, bias, RAG context metrics, G-Eval custom criteria,
  pytest integration, CI gates, and dataset/golden-set management. Use when deepeval,
  DeepEval metrics, LLM unit tests, RAG evaluation, faithfulness score, hallucination
  metric, GEval, assert_test, LLMTestCase, ConversationTestCase, or quality gates on
  owned model/app outputs — not for live production prompt injection attacks on third
  parties (use llm-prompt-injection for authorized red-team of LLM features).
---

# DeepEval LLM Tests

## Scope And Authorization

- **In scope:** LLM apps, RAG pipelines, agents, and eval harnesses you own or have written authorization to test.
- **Out of scope:** Scraping or testing third-party public chatbots without permission; exfiltrating user data into eval logs; using live PII as golden data without redaction/consent.
- Prefer offline or staging model endpoints; cap cost and rate on paid judges/models.
- Redact API keys, system prompts with secrets, user content, and customer identifiers from CI logs and tickets.
- Pair implementation with `code-quality-standards` and prompt/tool abuse testing with `llm-prompt-injection` / `ai-ml-security` as neighbors.

## When To Use

- Adding regression tests for chat, completion, RAG, or tool-calling quality.
- Blocking merges when faithfulness, relevancy, or custom G-Eval criteria drop below threshold.
- Building golden datasets and adversarial prompt suites for owned models.
- Comparing model versions or prompt templates with measurable metrics.
- Wiring DeepEval into pytest / GitHub Actions / other CI.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Authorized prompt/tool injection testing | `llm-prompt-injection` |
| Broader ML supply chain / model exposure review | `ai-ml-security` |
| Secrets in prompts/logs inventory | `secrets-management-hygiene` |
| Generic code review baseline | `code-quality-standards` |
| API contract tests without LLM judges | stack unit/integration testing |
| Rate-limit / cost abuse of model APIs | cost/ops controls or authorized rate-limit skills |

## Domain Concepts

| Concept | Role in DeepEval |
| --- | --- |
| `LLMTestCase` | Single turn: `input`, `actual_output`, optional `expected_output`, `context`, `retrieval_context` |
| `ConversationalTestCase` | Multi-turn agent/chat quality |
| Metrics | Faithfulness, AnswerRelevancy, Hallucination, Toxicity, Bias, ContextualPrecision/Recall/Relevancy, G-Eval, custom |
| Judge model | Separate LLM scoring the SUT; control cost, determinism, and PII sent to judge |
| `assert_test` | Fail when metric score is below threshold |
| Dataset / golden set | Versioned inputs and expected behaviors for CI |

## Workflow

### 1. Confirm scope and success criteria

1. Record app owner, model IDs/endpoints (staging preferred), and success bars (e.g. faithfulness ≥ 0.7 on RAG suite).
2. Decide judge model vs local/heuristic metrics; budget token spend for CI.
3. Classify data sensitivity of eval fixtures (synthetic only vs redacted prod samples).

### 2. Inventory current evaluation state

1. Locate existing DeepEval/pytest suites, datasets, and CI workflow files.
2. List prompt templates, retrieval stores, and tool allowlists under test.
3. Note gaps: no faithfulness on RAG, no toxicity gate, flaky judge scores, secrets in fixtures.

### 3. Define test cases and metrics

1. Map product risks to metrics:

| Risk | Metric direction |
| --- | --- |
| Answers ignore user question | Answer relevancy |
| RAG invents facts not in chunks | Faithfulness / hallucination |
| Retrieval returns junk | Contextual precision / recall / relevancy |
| Unsafe or toxic replies | Toxicity / bias + policy checks |
| Custom product rules | G-Eval with explicit evaluation steps |

2. Build `LLMTestCase` objects with stable `input` and captured `actual_output` (call SUT once per case when possible to save cost).
3. For RAG, always pass the `retrieval_context` used at generation time—not a re-query after the fact unless intentional.

### 4. Implement pytest + DeepEval harness

```python
# tests/test_rag_faithfulness.py — illustrative
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric

@pytest.mark.llm
def test_rag_answer_faithful(rag_case):
    tc = LLMTestCase(
        input=rag_case["q"],
        actual_output=rag_case["answer"],
        retrieval_context=rag_case["chunks"],
    )
    assert_test(
        tc,
        [
            FaithfulnessMetric(threshold=0.7),
            AnswerRelevancyMetric(threshold=0.6),
        ],
    )
```

```bash
# Local / CI (owned project)
pip install deepeval pytest
# Configure judge provider keys via CI secrets, never commit
export OPENAI_API_KEY="***"   # redacted
pytest tests/ -m llm --tb=short
```

1. Mark LLM tests so unit tests stay free/fast: `@pytest.mark.llm`.
2. Cache SUT outputs for metric-only re-runs when prompts are unchanged.
3. Pin DeepEval and judge model versions in lockfiles for reproducibility.

### 5. Golden sets and adversarial suites

1. Store cases as JSON/JSONL under `evals/goldens/` with schema: `id`, `input`, `expected_behavior`, optional `retrieval_context`, `tags`.
2. Include happy path, edge formats, empty retrieval, conflicting context, and authorized policy/adversarial fixtures for owned apps.
3. Version goldens with the app; require review when thresholds or goldens change.

### 6. CI gates and flakiness control

1. Run the LLM suite on PR when prompts, retrieval, or model config change; nightly for full golden set if cost-limited.
2. Set explicit thresholds; avoid “any score” pass.
3. Mitigate flaky judges: temperature 0 where supported, multi-trial majority, slightly lower threshold plus human review for borderline cases.
4. Fail closed on safety metrics when the product requires it; document fail-open only with owner and expiry.

### 7. Observe, cost, and hand off

1. Track pass rate, mean metric scores, judge token cost per run, and flaky test rate.
2. Alert on sudden score drops after model/prompt deploys.
3. Document how to add a golden and who owns threshold changes.
4. Apply `code-quality-standards` to harness code; never log full production user transcripts.

## DeepEval metric selection

| Metric | Needs | Typical use |
| --- | --- | --- |
| Answer relevancy | input + actual_output | General Q&A |
| Faithfulness | actual_output + retrieval_context | RAG groundedness |
| Hallucination | actual_output + context | Contradiction with provided context |
| Contextual precision/recall | input + retrieval_context | Retriever quality |
| G-Eval | criteria text + case fields | Product-specific rubrics |
| Toxicity / bias | actual_output | Safety gates (complement policy filters) |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Fixtures | Synthetic or redacted goldens | Raw prod PII in git |
| RAG eval | Context = chunks model saw | Re-embedding after answer |
| Thresholds | Documented and versioned | Arbitrary 0.5 everywhere |
| CI | Secrets in vault; marked jobs | Keys in workflow YAML |
| Scope | Owned apps / authorized | Testing random public bots |
| Changes | Small metric/prompt diffs | Unreviewed threshold drops to pass CI |

## Output Checklist

- [ ] Owner, SUT endpoint/model, and judge model documented
- [ ] Success thresholds defined per metric and suite
- [ ] Test cases cover golden and adversarial tags
- [ ] RAG cases include correct retrieval_context
- [ ] pytest/DeepEval commands green on staging with redacted logs
- [ ] CI gate path and cost controls documented
- [ ] Flakiness strategy (temp, retries, cache) recorded
- [ ] No secrets or live PII in goldens or CI artifacts
- [ ] Neighbor skills used for injection / SSDLC as needed
- [ ] `code-quality-standards` applied to harness code

## Rules

- Authorized/owned systems only; evidence (scores, logs) over vibes.
- Never commit API keys or unredacted user content.
- Do not lower safety thresholds to green CI without ticket, owner, and expiry.
- Keep focus on DeepEval-style LLM quality gates; route injection red-team and broad ML security elsewhere.
- Prefer deterministic fixtures and versioned goldens for reproducible failures.
