---
name: lighteval
description: "All-in-one LLM evaluation toolkit (HuggingFace LightEval). 1000+ tasks with multi-backend support: Accelerate, vLLM, SGLang, Nanotron, TGI, LiteLLM, inference providers, and custom models. Sample-by-sample result exploration, custom task/metric creation. Used by HuggingFace's Leaderboard and Evals team. For pure GPT-style model eval, also consider lm-evaluation-harness."
license: MIT license
tags: [multilingual-benchmarks, backend-flexible-eval, sample-level-analysis, custom-metrics, lighteval]
metadata:
    skill-author: K-Dense Inc.
------|---------|----------|
| `inspect-ai` | `lighteval eval` | Preferred, modern backend |
| Accelerate | `lighteval accelerate` | Single/multi-GPU local models |
| vLLM | `lighteval vllm` | Fast batched inference |
| SGLang | `lighteval sglang` | Structured generation evals |
| Nanotron | `lighteval nanotron` | Distributed training evaluation |
| TGI | `lighteval endpoint tgi` | Locally served models |
| LiteLLM | `lighteval endpoint litellm` | Any API (OpenAI, Anthropic, etc.) |
| HF Providers | `lighteval endpoint inference-providers` | HuggingFace's hosted API |
| Inference Endpoints | `lighteval endpoint inference-endpoint` | HF Dedicated Endpoints |
| Custom | `lighteval custom` | Anything with a Python API |

### 4. Task Domains

**Knowledge Tasks:**
```bash
lighteval accelerate "model-name" mmlu           # 57-subject knowledge
lighteval accelerate "model-name" mmlu-pro        # Harder MMLU
lighteval accelerate "model-name" gpqa             # Graduate-level science
lighteval accelerate "model-name" triviaqa         # Trivia QA
lighteval accelerate "model-name" humanitys_last_exam  # Very hard questions
```

**Math and Code:**
```bash
lighteval accelerate "model-name" gsm8k            # Grade school math
lighteval accelerate "model-name" math              # Competition math
lighteval accelerate "model-name" aime24            # AIME 2024
lighteval accelerate "model-name" lcb               # LiveCodeBench
```

**Chat Model Evaluation:**
```bash
lighteval accelerate "model-name" ifeval            # Instruction following
lighteval accelerate "model-name" mt_bench           # Multi-turn dialogue
lighteval accelerate "model-name" musr              # Multi-step reasoning
lighteval accelerate "model-name" ruler             # Long context
```

**Multilingual:**
```bash
lighteval accelerate "model-name" mgsm              # Math in 10+ languages
lighteval accelerate "model-name" flores200          # 200-language translation
lighteval accelerate "model-name" mmlu_arabic       # Arabic MMLU
lighteval accelerate "model-name" cmmlu             # Chinese MMLU
lighteval accelerate "model-name" russian_squad     # Russian QA
```

### 5. Custom Tasks

```python
from lighteval.tasks.lighteval_task import LightevalTask
from lighteval.metrics.metrics import SampleLevelMetric

class MyCustomTask(LightevalTask):
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="my_custom_task",
            version=0,
            metrics=["my_metric"],
            *args, **kwargs
        )

    def get_prompt(self, sample):
        return f"Question: {sample['question']}\nAnswer:"

    def process_output(self, output, sample):
        # Extract answer from model output
        return output.strip()

    def get_gold(self, sample):
        return sample["answer"]
```

### 6. Custom Metrics

```python
from lighteval.metrics.metrics import SampleLevelMetric
import numpy as np

class F1Metric(SampleLevelMetric):
    def __init__(self, *args, **kwargs):
        super().__init__(metric_name="f1", *args, **kwargs)

    def compute(self, golds, predictions, **kwargs):
        # golds and predictions are lists
        scores = []
        for gold, pred in zip(golds, predictions):
            # Compute per-sample F1
            gold_tokens = set(gold.lower().split())
            pred_tokens = set(pred.lower().split())
            tp = len(gold_tokens & pred_tokens)
            fp = len(pred_tokens - gold_tokens)
            fn = len(gold_tokens - pred_tokens)
            precision = tp / (tp + fp + 1e-10)
            recall = tp / (tp + fn + 1e-10)
            f1 = 2 * precision * recall / (precision + recall + 1e-10)
            scores.append(f1)
        return np.mean(scores)
```

### 7. Multi-Backend Configuration

```python
# Evaluate same tasks across backends
backends = {
    "vllm": "lighteval vllm",
    "sglang": "lighteval sglang",
    "accelerate": "lighteval accelerate",
}

for backend, cmd in backends.items():
    print(f"Running {backend}...")
    subprocess.run(f"{cmd} meta-llama/Meta-Llama-3-8B-Instruct mmlu gsm8k", shell=True)
```

### 8. Pushing Results to HuggingFace Hub

```bash
lighteval accelerate "model-name" mmlu \
    --push-to-hub \
    --push-results-dir my-org/eval-results \
    --results-org my-org

# Results appear at: https://huggingface.co/my-org/eval-results
```

### 9. Task Discovery

```bash
# List all tasks
lighteval list-tasks

# Filter by domain
lighteval list-tasks --domain math
lighteval list-tasks --domain multilingual

# Search
lighteval list-tasks --query mmlu
```

**Open Benchmark Index (web UI):**
- Browse: https://huggingface.co/spaces/OpenEvals/open_benchmark_index
- Find tasks by domain, language, difficulty

### 10. Detailed Result Analysis

```python
from lighteval.logging.evaluation_tracker import EvaluationTracker

tracker = EvaluationTracker(output_dir="./results")

# After evaluation:
for task_name, task_results in tracker.results.items():
    print(f"\n=== {task_name} ===")
    print(f"  Score: {task_results['score']:.3f}")
    print(f"  Samples: {len(task_results['samples'])}")

    # Inspect failures
    failures = [s for s in task_results['samples'] if not s['correct']]
    for f in failures[:5]:
        print(f"    Q: {f['input']}")
        print(f"    Predicted: {f['prediction']}")
        print(f"    Expected: {f['gold']}\n")
```

## Key Patterns

1. **Use `lighteval eval` as preferred entrypoint** — inspect-ai backend is most modern
2. **vLLM for speed**, Accelerate for simplicity, LiteLLM for API access
3. **Push to Hub** for sharing results and comparing models
4. **Sample-level analysis** for debugging eval failures
5. **Custom metrics** are first-class — no need to fork the library
6. **Open Benchmark Index** for discovering available tasks

## References

- [LightEval Documentation](https://huggingface.co/docs/lighteval/)
- [Open Benchmark Index](https://huggingface.co/spaces/OpenEvals/open_benchmark_index)
- [Adding Custom Tasks Guide](https://huggingface.co/docs/lighteval/adding-a-custom-task)
- [Adding Custom Metrics Guide](https://huggingface.co/docs/lighteval/adding-a-new-metric)
- [Backend Configuration](https://huggingface.co/docs/lighteval/installation)
