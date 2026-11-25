---
name: "llm-eval"
description: "LLM evaluation: build evaluation datasets, choose metrics (RAGAS, G-Eval, LLM-as-judge), run automated evals, monitor production quality, and detect regressions"
---

# LLM Eval Skill

## When to activate
- Building a test suite for an LLM-powered feature before shipping
- Choosing evaluation metrics for RAG, chat, summarisation, or extraction tasks
- Setting up LLM-as-judge to score model outputs automatically
- Detecting prompt or model version regressions in CI
- Monitoring production output quality over time
- Comparing two prompt versions or model versions systematically

## When NOT to use
- Unit testing application code (not LLM outputs) — use Jest/pytest
- A/B testing with real users — use the experiment-designer skill
- Security red-teaming — use the security-reviewer agent
- Choosing between LLMs for a new project — benchmarking is different from eval

## Instructions

### Evaluation dataset design

```
Build an evaluation dataset for [LLM feature].

Feature: [describe — RAG Q&A / summarisation / extraction / classification / chat]
Scale: [20 / 50 / 200 examples]
Data sources: [real user queries / synthetic / domain expert created]

Dataset design principles:

Distribution: match your production input distribution
- Sample from real user queries where possible (anonymised)
- If synthetic: generate with Claude using diverse personas and intents
- Cover: common cases (60%), edge cases (30%), adversarial cases (10%)

For each example, record:
| Field | Description |
|---|---|
| input | The prompt or question |
| expected_output | Ground truth answer (or criteria) |
| category | Type of query (factual / reasoning / format / refusal) |
| difficulty | Easy / Medium / Hard |
| source | Real user / synthetic / expert |
| notes | Why this example is in the set |

Golden set quality rules:
- Every expected_output reviewed by a domain expert
- No examples where the expected answer is ambiguous
- Adversarial examples must be clearly wrong (not borderline)
- Refresh every 3 months — input distribution drifts

For RAG evaluation (additional fields):
| Field | Description |
|---|---|
| ground_truth_context | The document chunk that contains the answer |
| relevant_chunks | All chunks that are relevant |
| is_answerable | Can this question be answered from the corpus? |

Generate a 20-example evaluation set for my feature using synthetic data.
```

### Metric selection

```
Choose evaluation metrics for [LLM task].

Task: [RAG / summarisation / classification / extraction / code generation / chat]
What "good" means: [accuracy / faithfulness / helpfulness / safety / format]
Automation requirement: [fully automated / human-in-loop / hybrid]

Metric menu by task type:

RAG / Q&A:
- Faithfulness: does the answer stick to the retrieved context? (anti-hallucination)
  Tool: RAGAS faithfulness scorer
  Formula: facts in answer that can be attributed to context / total facts in answer
  Target: > 0.85

- Answer Relevancy: does the answer address the question?
  Tool: RAGAS answer_relevancy
  Target: > 0.80

- Context Precision: are the retrieved chunks relevant to the question?
  Tool: RAGAS context_precision
  Target: > 0.75

- Context Recall: were all relevant chunks retrieved?
  Tool: RAGAS context_recall (needs ground truth)

SUMMARISATION:
- ROUGE-L: longest common subsequence overlap with reference summary
  Good for: extractive summaries where exact wording matters
  Weakness: misses semantically equivalent but differently worded summaries
  Target: > 0.30 for most tasks

- BERTScore: semantic similarity using embeddings
  Better than ROUGE for abstractive summaries
  Target: F1 > 0.85

- G-Eval (LLM-as-judge): Claude rates the summary on: coherence, consistency, fluency, relevance (1-5)
  Most correlated with human judgement

CLASSIFICATION / EXTRACTION:
- Accuracy: % correct (for balanced classes)
- F1 score: for imbalanced classes
- Exact match: for structured extraction (JSON fields)
- Partial credit: for list extraction (items correctly identified / total expected)

CODE GENERATION:
- Pass@k: does the code pass the test suite on k attempts?
- Syntax validity: does it compile/parse?
- Test coverage: do the generated tests actually run?

LLM-AS-JUDGE (for anything subjective):
Use Claude to score outputs against criteria.
Prompt: "Rate this response 1-5 for [criterion]: [output]. 
1 = completely fails, 5 = excellent. 
Respond with only: {"score": N, "reason": "one sentence"}"

Select the right metrics for my task and set target thresholds.
```

### RAGAS setup

```
Set up RAGAS evaluation for [RAG system].

Stack: [LangChain / LlamaIndex / custom]
Language: [Python]
LLM for evaluation: [Claude / GPT-4 / same model as production]

RAGAS installation and setup:
pip install ragas langchain-anthropic

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from langchain_anthropic import ChatAnthropic
from datasets import Dataset

# Use Claude as the evaluation LLM
eval_llm = ChatAnthropic(model="claude-opus-4-7")

# Build evaluation dataset
eval_data = {
    "question": [
        "What is our refund policy?",
        "How do I reset my password?",
    ],
    "answer": [
        "Our refund policy allows returns within 30 days...",  # Your RAG output
        "To reset your password, click 'Forgot Password'...",  # Your RAG output
    ],
    "contexts": [
        ["Refund policy document chunk..."],  # Retrieved chunks
        ["Password reset documentation..."],  # Retrieved chunks
    ],
    "ground_truth": [
        "Customers can return items within 30 days for a full refund.",  # Expected answer
        "Users can reset their password via the login page.",  # Expected answer
    ]
}

dataset = Dataset.from_dict(eval_data)

# Run evaluation
results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm=eval_llm,
)

print(results)
# Output: {'faithfulness': 0.87, 'answer_relevancy': 0.82, ...}

# Convert to pandas for analysis
df = results.to_pandas()
df[df['faithfulness'] < 0.7]  # Find low-quality answers

Integrate into CI:
# conftest.py or eval script in CI
assert results['faithfulness'] > 0.80, f"Faithfulness regression: {results['faithfulness']}"
assert results['answer_relevancy'] > 0.75, f"Relevancy regression: {results['answer_relevancy']}"

Generate the RAGAS setup for my RAG pipeline.
```

### LLM-as-judge

```
Set up LLM-as-judge evaluation for [feature].

What to judge: [describe outputs to score]
Criteria: [list — accuracy / helpfulness / tone / safety / format compliance]
Reference: [with ground truth / without ground truth / comparative (A vs B)]

LLM-as-judge prompt template:

Single-answer scoring:
You are evaluating the quality of an AI assistant's response.

Question: {question}
Response to evaluate: {response}
Reference answer (if available): {reference}

Evaluate the response on these criteria. For each, provide a score (1-5) and one-sentence reason.

Criteria:
1. Accuracy (1=completely wrong, 5=fully correct): Does the response contain accurate information?
2. Relevance (1=off-topic, 5=directly answers): Does it address the question?
3. Helpfulness (1=unhelpful, 5=very helpful): Would a user find this useful?
4. Conciseness (1=verbose/rambling, 5=appropriately concise): Is the length appropriate?

Respond in JSON only:
{
  "accuracy": {"score": N, "reason": "..."},
  "relevance": {"score": N, "reason": "..."},
  "helpfulness": {"score": N, "reason": "..."},
  "conciseness": {"score": N, "reason": "..."},
  "overall": N
}

Comparative scoring (A vs B):
Response A: {response_a}
Response B: {response_b}
Which response is better for this question? Respond: {"winner": "A" | "B" | "tie", "reason": "..."}

Calibration tip: run your judge against 20 human-labelled examples.
If judge-human agreement < 70%, refine the prompt or criteria.

Build the judge prompt for my specific criteria.
```

### Production monitoring

```
Monitor LLM output quality in production for [feature].

Feature: [describe]
Traffic: [X requests/day]
Sample rate: [1% / 5% / all]
Quality signals available: [user feedback / thumbs up-down / completion rate / none]

Production monitoring stack:

1. Implicit signals (no user input needed):
   - Completion rate: did the user continue using the app after the LLM response?
   - Follow-up questions: did the user ask the same question again? (indicates bad answer)
   - Copy rate: did the user copy the response? (positive signal)
   - Session abandonment: did the user leave immediately after the response?

2. Explicit signals (user feedback):
   - Thumbs up/down on each response
   - "Was this helpful?" Y/N
   - Free text feedback (requires human review to extract signal)

3. Automated quality checks (run on 5% sample):
   - Format compliance: did the response match expected format?
   - Length check: is it in the expected range?
   - Refusal rate: is the model refusing things it shouldn't?
   - Hallucination check: spot-check facts against source (via LLM-as-judge)

4. Alerting thresholds:
   - User thumbs-down rate > X% → alert
   - Format compliance drops > 5% → prompt regression, investigate
   - Response length increases > 50% → model drift or prompt change

5. Logging structure for each call:
   {
     timestamp, request_id, model, prompt_version,
     input_tokens, output_tokens, latency_ms,
     user_feedback (if received), eval_score (if sampled),
     response_sample (first 200 chars for monitoring)
   }

Set up the monitoring architecture for my specific feature and traffic level.
```

## Example

**User:** Our RAG chatbot answers about our documentation. How do we know if it's getting worse after we update our docs or change the retrieval model?

**Claude's regression testing plan:**

Without a test suite, you'll find out from user complaints — which is too late.

**Step 1 — Build a golden eval set (this week):**
Take 30 real user questions from your logs. For each:
1. Run it through your current RAG system
2. Have a domain expert confirm the answer is correct
3. Record: question + retrieved chunks + correct answer

This becomes your regression test set.

**Step 2 — RAGAS baseline (automated):**
```python
# Run against your golden set
results = evaluate(golden_dataset, metrics=[faithfulness, answer_relevancy])
# Record: faithfulness=0.87, answer_relevancy=0.83 (your baseline)
```

**Step 3 — CI gate:**
```python
# In your deployment pipeline (GitHub Actions, etc.)
results = evaluate(golden_dataset, ...)
assert results['faithfulness'] > 0.82, "Faithfulness regression detected"
assert results['answer_relevancy'] > 0.78, "Relevancy regression detected"
```

Now: any docs update or retrieval change that degrades quality by > 5% **fails the deployment** before it reaches users.

**Step 4 — When to re-evaluate thresholds:**
After docs updates: re-run golden set, update expected answers if docs changed.
Monthly: pull 20 new real queries from production logs, add to golden set.

**Total setup time:** 4-6 hours to build the golden set. 2 hours to add CI gate. Pays off the first time it catches a regression.

---
