---
name: openai-evals
description: LLM evaluation framework and registry (OpenAI Evals). Framework for evaluating LLMs and LLM-based systems with a registry of community-contributed eval templates. Supports model-graded evals, classification, simple completion matching, and custom completion functions. Use for systematic LLM quality testing, regression detection, and prompt engineering validation.
license: MIT license
tags: [model-graded-evals, regression-testing, prompt-validation, eval-registry, openai-evals]
metadata:
    skill-author: K-Dense Inc.
---|------|--------|
| `mmlu` | Match | Knowledge (57 subjects) |
| `hellaswag` | Match | Commonsense reasoning |
| `truthfulqa` | Model-graded | Truthfulness |
| `gsm8k` | Match | Math reasoning |
| `humaneval` | Custom | Code generation |
| `ifeval` | Model-graded | Instruction following |
| `bbq` | Model-graded | Bias detection |
| `factuality` | Model-graded | Factual accuracy |
| `translation` | Model-graded | Translation quality |

Browse full registry: `evals/registry/evals/`

### 10. Production Eval Pipeline Pattern

```python
# CI/CD eval pipeline
def run_eval_suite(model_name, eval_names):
    results = {}
    for eval_name in eval_names:
        cmd = f"oaieval {model_name} {eval_name} --max_samples 200"
        result = subprocess.run(cmd, shell=True, capture_output=True)
        results[eval_name] = parse_accuracy(result.stdout)
    return results

# Regression test
previous = {"mmlu": 0.86, "gsm8k": 0.92, "hellaswag": 0.85}
current = run_eval_suite("my-finetuned-model", ["mmlu", "gsm8k", "hellaswag"])

for name, score in current.items():
    if score < previous[name] - 0.02:  # 2% regression threshold
        alert(f"Regression in {name}: {previous[name]:.2f} → {score:.2f}")
```

## Key Patterns

1. **Start with templates** — most evals don't need custom Python code
2. **Use model-graded evals** for subjective quality (fluency, helpfulness, safety)
3. **Use match evals** for objective metrics (classification, multiple choice)
4. **`git lfs fetch --all`** is required before running community evals
5. **Custom completion functions** enable testing non-OpenAI models
6. **Record paths** enable debugging individual failures
7. **Private evals** can test proprietary data without exposing it

## References

- [OpenAI Evals Repo](https://github.com/openai/evals)
- [Build an Eval Guide](https://github.com/openai/evals/blob/main/docs/build-eval.md)
- [Run Evals Guide](https://github.com/openai/evals/blob/main/docs/run-evals.md)
- [Eval Templates Reference](https://github.com/openai/evals/blob/main/docs/eval-templates.md)
- [Custom Eval Example](https://github.com/openai/evals/blob/main/docs/custom-eval.md)
- [Completion Functions Guide](https://github.com/openai/evals/blob/main/docs/completion-fns.md)
