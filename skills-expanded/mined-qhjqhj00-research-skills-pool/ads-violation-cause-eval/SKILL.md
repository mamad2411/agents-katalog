---
name: ads-violation-cause-eval
description: Evaluates an automated root-cause analysis tool for autonomous driving systems by measuring its ability to correctly identify the faulty component and the specific output message that caused a driving violation in simulation. It also measures the debugging scope reduction and computational efficiency of the tool. Use when the user wants to benchmark on ADS Violation Cause Benchmark, or asks about evaluating this task. Reports component-level success.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2401.10443
  bibtex_key: wan2024towards
  confidence: high
---

# ads-violation-cause-eval

> Towards Automated Driving Violation Cause Analysis in Scenario-Based Testing for Autonomous Driving Systems — Wan et al. (2024) (arXiv:2401.10443, 2024)

## What this evaluates

Evaluates an automated root-cause analysis tool for autonomous driving systems by measuring its ability to correctly identify the faulty component and the specific output message that caused a driving violation in simulation. It also measures the debugging scope reduction and computational efficiency of the tool.

## Datasets

- **ADS Violation Cause Benchmark** — total ?; splits: test (-1)

## Metrics

- `component-level success` **(primary)** — range: [0, 1]
  - Boolean accuracy indicating whether the tool's reported component matches the ground-truth faulty component.
- `message-level success` — range: [0, 1]
  - Boolean accuracy indicating whether the tool's reported output message matches the ground-truth faulty message.
- `reduction_rate` — range: percent
  - Defined as 1 - 1/|M|, where |M| is the total number of messages in the violation-included driving trace. Drops to 0% if message-level success fails.
- `attribution_time` — range: other
  - Wall-clock time in minutes required for the tool to complete the cause attribution task.

## Input / output format

**Input**: Simulation traces and inter-component messages from Baidu Apollo 7.0 running in the LGSVL simulator under predefined collision scenarios.

**Output**: A tuple containing (1) the identified faulty component name, and (2) a specific input/output message pair from that component.

## Scoring recipe

```python
def compute_metrics(predictions, gold):
    comp_success = 1.0 if predictions.component == gold.component else 0.0
    msg_success = 1.0 if predictions.msg_pair == gold.msg else 0.0
    total_msgs = len(gold.trace_messages)
    reduction = (1.0 - 1.0 / total_msgs) if msg_success else 0.0
    return comp_success, msg_success, reduction
```

## Common pitfalls

- Simulation replay randomness can cause vehicle state drift, making exact message matching difficult and leading to near-miss timestamp matches instead of exact failures.
- The reduction rate metric drops to 0% for any instance where message-level success fails, heavily penalizing partial matches.
- Real bug scenarios require manual reconstruction from GitHub PRs/commits, introducing potential variability in ground-truth alignment.

## Evidence (verbatim from paper)

> We use two boolean metrics to report the effectiveness of the cause localization task: (1) component-level success: which is defined as whether the reported component is the component that contains a real bug/fault, and (2) message-level success: whether the reported output message is the result of the real bug/injected fault.

## Citation

```bibtex
@misc{wan2024towards,
  title={Towards Automated Driving Violation Cause Analysis in Scenario-Based Testing for Autonomous Driving Systems},
  author={Wan et al. (2024)},
  year={2024},
  note={arXiv:2401.10443}
}
```

- arXiv: 2401.10443
