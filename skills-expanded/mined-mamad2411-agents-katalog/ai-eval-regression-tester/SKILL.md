---
name: ai-eval-regression-tester
description: Use to run a regression eval suite over an LLM application — fixed test cases with deterministic graders (exact match, JSON schema, regex, embedding similarity, LLM-as-judge). Compares the candidate model/prompt against a baseline and gates a release on pass rate + per-tag thresholds.
---

# AI Eval Regression Tester

## When to invoke
- "Run the eval suite for the new prompt version."
- "Compare gpt-X vs the current baseline on our customer-support eval."
- "Block release if eval pass rate drops below 95%."

## Inputs needed
1. **Eval YAML / JSONL** — list of cases with `input`, expected outputs, graders, tags.
2. **Candidate runner** — Python callable / HTTP endpoint that takes input and returns output.
3. **Baseline run** — JSONL of prior outputs (optional, for diffing).
4. **Pass thresholds** — overall and per-tag.

## Workflow
1. **Load** cases.
2. **Run** candidate over each case (parallelized).
3. **Grade** with configured graders.
4. **Aggregate** — pass rate overall + per tag + diff vs baseline.
5. **Gate** — exit 1 if any threshold fails (CI-friendly).
6. **Report** — Markdown + JSONL of every case for diffing.

## Eval case schema
```yaml
- id: refund_basic
  tags: [refund, policy]
  input: "How do I request a refund after 60 days?"
  graders:
    - type: contains
      values: ["return policy", "support team"]
    - type: not_contains
      values: ["sure thing", "lol"]
    - type: regex
      pattern: "policy"
    - type: json_schema
      schema:
        type: object
        required: [answer, citation]
```

## Guardrails
- Always require deterministic graders before LLM-as-judge.
- LLM-judge results must include the judge's reasoning verbatim.
- Per-case results must be logged to JSONL for forensics.
- No silent retries on grader failures.

## Reference code
`run_eval.py` runs cases in parallel, grades, diffs vs baseline, and exits with the right code.
