---
name: llm-evals
description: Builds an eval set and scorer for an LLM feature and tracks regressions with each change. Use it so prompt and model changes are measured, not guessed.
---

# LLM evals

No change ships without a before and after number on the same cases.

## Steps

1. Define what a good answer means for this feature in one or two sentences, and list the failure types that hurt most: wrong fact, wrong format, refusal, unsafe content, too long.
2. Build the case file (JSONL): id, input, and either an expected value, a rule, or a reference answer. Start with 30 to 50 cases drawn from real logs and bug reports, cover each failure type, and label edge cases. Add every new bug as a case.
3. Score with the cheapest reliable method: exact or regex match, JSON schema validation, a unit test over generated code, or a numeric tolerance. Use an LLM judge only for qualities like helpfulness, with a written rubric of 3 to 5 points and a different model than the one being tested.
4. Validate any judge: hand label 20 cases, compare, and report the agreement rate. Do not trust a judge below about 85 percent agreement.
5. Run each case more than once if outputs vary, and report the pass rate, not a single sample.
6. Store results per run with the prompt version, model name and date. Print a diff against the last run: cases that flipped to fail first, then to pass.
7. Wire a command (`make eval`) and, if wanted, a CI check with a threshold.

## Rules

- Never put eval cases into the prompt as examples; keep them held out.
- Do not average away a critical failure; report those separately.

## Report

Overall pass rate, pass rate per failure type, regressions against the last run with case IDs, and the cost of the run.
