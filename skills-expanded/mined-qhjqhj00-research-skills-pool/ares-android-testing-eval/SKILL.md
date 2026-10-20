---
name: ares-android-testing-eval
description: Evaluates the ability of automated black-box testing tools and reinforcement learning agents to explore Android applications effectively. It probes how well algorithms navigate complex UI states, maximize code/activity coverage, and trigger unique application crashes within a fixed time budget. Use when the user wants to benchmark on F-Droid top starred apps, AndroTest, Synthetic FATE models, or asks about evaluating this task. Reports AUC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2101.02636
  bibtex_key: romdhana2021ares
  confidence: high
---

# ares-android-testing-eval

> Deep Reinforcement Learning for Black-Box Testing of Android Apps — Romdhana et al. (2021) (arXiv:2101.02636, 2021)

## What this evaluates

Evaluates the ability of automated black-box testing tools and reinforcement learning agents to explore Android applications effectively. It probes how well algorithms navigate complex UI states, maximize code/activity coverage, and trigger unique application crashes within a fixed time budget.

## Datasets

- **F-Droid top starred apps** — total 41; splits: test (41)
- **AndroTest** — total 68; splits: test (68)
- **Synthetic FATE models** — total 4; splits: test (4)

## Metrics

- `AUC` **(primary)** — range: [0, 1]
  - Area Under the Curve of the coverage percentage plot over time. Computed as the integral of the coverage curve from time 0 to the experiment timeout.
- `code coverage` — range: percent
  - Percentage of executable instructions covered during the test run, measured via JaCoCo or Emma instrumentation.
- `number of unique crashes` — range: other
  - Count of distinct app crashes/faults triggered, identified by parsing Logcat, filtering by package name, and hashing sanitized stack traces.

## Input / output format

**Input**: Current Android UI state/screen content and available actions observed in a black-box manner.

**Output**: Discrete UI action to execute next (e.g., tap, swipe, text input, back press).

## Scoring recipe

```python
def compute_metrics(run_data):
    coverage_curve = [coverage_at_t for t in range(timeout_steps)]
    auc = np.trapz(coverage_curve) / timeout_steps
    final_coverage = coverage_curve[-1]
    crashes = len(set(hash(sanitize_trace(t)) for t in logcat_output))
    return auc, final_coverage, crashes
```

## Common pitfalls

- Non-deterministic exploration requires averaging over multiple runs (60 for synthetic, 10 for real apps) and applying Wilcoxon tests with Holm-Bonferroni correction to avoid Type I errors.
- Coverage metrics depend on the instrumentation tool used (JaCoCo vs. Emma), making direct cross-tool comparisons sensitive to tool-specific coverage granularity.
- Crash detection relies on Logcat parsing and stack trace hashing; improper sanitization or package-name filtering can lead to false positives or missed unique crashes.

## Evidence (verbatim from paper)

> For the assessment, we adopt the widely used metric AUC (Area Under the Curve), measuring the area below the activity coverage plot over time. To account for the non determinism of the algorithms, we repeated each experiment 30 times and applied the Wilcoxon non-parametric statistical test. In addition to code coverage, we also report the number of failures (unique app crashes) triggered by each approach (RQ6). To measure the number of unique crashes observed, we parsed the output of Logcat and (1) removed all crashes that do not contain the package name of the app; (2) extracted the stack trace; (3) computed the hash code of the sanitized stack trace, to uniquely identify it.

## Citation

```bibtex
@misc{romdhana2021ares,
  title={Deep Reinforcement Learning for Black-Box Testing of Android Apps},
  author={Romdhana et al. (2021)},
  year={2021},
  note={arXiv:2101.02636}
}
```

- arXiv: 2101.02636
