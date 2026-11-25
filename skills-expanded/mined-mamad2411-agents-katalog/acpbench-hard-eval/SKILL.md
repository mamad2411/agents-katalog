---
name: acpbench-hard-eval
description: Evaluates language and reasoning models on open-ended, generative planning tasks derived from PDDL domains. It probes capabilities like action applicability, reachability, progression, justification, and next-action prediction without predefined answer choices. Use when the user wants to benchmark on ACPBench Hard, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.24378
  bibtex_key: kokel2025acpbenchhard
  confidence: high
---

# acpbench-hard-eval

> ACPBench Hard: Unrestrained Reasoning about Action, Change, and Planning — Kokel et al. (2025) (arXiv:2503.24378, 2025)

## What this evaluates

Evaluates language and reasoning models on open-ended, generative planning tasks derived from PDDL domains. It probes capabilities like action applicability, reachability, progression, justification, and next-action prediction without predefined answer choices.

## Datasets

- **ACPBench Hard** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Fraction of correctly predicted responses after parsing the model output with a lenient grammar. Computed per task and per domain.

## Input / output format

**Input**: PDDL planning domain/task description with 2-shot prompting using static examples from outside the evaluation set, plus instructions to follow a specific response format.

**Output**: Open-ended text response parsed by a domain-specific grammar. Formats vary by task: progression_list (two lists for positive/negative effects), action_list (list of actions), or index (integer index of first inapplicable action).

## Scoring recipe

```python
def compute_accuracy(predictions, golds):
    correct = 0
    for pred, gold in zip(predictions, golds):
        parsed = parse_with_grammar(pred)
        if parsed == gold:
            correct += 1
    return correct / len(predictions)
```

## Common pitfalls

- Models frequently fail to strictly adhere to the instructed output format, necessitating a lenient grammar-based parser that discards non-conforming tokens.
- Performance is highly domain-dependent; some computationally hard domains show better accuracy than simpler ones, and generative formats yield significantly higher error rates than boolean/multiple-choice variants.

## Evidence (verbatim from paper)

> For each task, we evaluated a 2-shot prompting with static examples from outside the evaluation set. The two examples come from the grid and logistics domains, one each per task. This allows to exemplify the expected response format. Additionally, we instructed the language models to produce their response in a particular format. Still, the tested language models do not necessarily adhere to the instructions or the example format. Therefore, to be able to extract the answer from the response, we developed a lenient grammar based parser, which would discard tokens if they did not fit expected token values. Table 2: Large size language and reasoning models accuracy.

## Citation

```bibtex
@misc{kokel2025acpbenchhard,
  title={ACPBench Hard: Unrestrained Reasoning about Action, Change, and Planning},
  author={Kokel et al. (2025)},
  year={2025},
  note={arXiv:2503.24378}
}
```

- arXiv: 2503.24378
