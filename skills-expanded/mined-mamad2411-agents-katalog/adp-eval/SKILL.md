---
name: adp-eval
description: Evaluates the performance of LLM agents fine-tuned with the Agent Data Protocol (ADP) across software engineering, web browsing, OS/database tool use, and general reasoning tasks. Use when the user wants to benchmark on SWE-Bench Verified, WebArena, AgentBench, GAIA, or asks about evaluating this task. Reports unit test pass rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.24702
  bibtex_key: song2025agentdataprotocol
  confidence: medium
---

# adp-eval

> Agent Data Protocol: Unifying Datasets for Diverse, Effective Fine-tuning of LLM Agents — Song et al. (2025) (arXiv:2510.24702, 2025)

## What this evaluates

Evaluates the performance of LLM agents fine-tuned with the Agent Data Protocol (ADP) across software engineering, web browsing, OS/database tool use, and general reasoning tasks.

## Datasets

- **SWE-Bench Verified** — total ?; splits: verified (-1)
- **WebArena** — total ?; splits: test (-1)
- **AgentBench** — total ?; splits: test (-1)
- **GAIA** — total ?; splits: test (-1)

## Metrics

- `unit test pass rate` **(primary)** — range: percent
  - Not explicitly stated in the text; standard benchmark metrics are implied (e.g., pass@1 for SWE-Bench, task success rate for WebArena/AgentBench/GAIA).

## Input / output format

**Input**: Codebases with bug reports (SWE-Bench), natural language commands in web environments (WebArena), multi-turn OS/database/web tasks (AgentBench), and human-annotated reasoning/tool-use tasks (GAIA).

**Output**: Generated patches, web interaction sequences, tool-use trajectories, or final answers/responses depending on the benchmark.

## Scoring recipe

```python
def score(predictions, gold, benchmark):
    if benchmark == 'SWE-Bench':
        return run_unit_tests(predictions)  # pass@1
    elif benchmark in ['WebArena', 'AgentBench', 'GAIA']:
        return check_task_completion(predictions, gold)  # success rate
    return 0.0
```

## Common pitfalls

- The paper evaluates across 4 distinct benchmarks with different environments and evaluation criteria, but does not specify the exact metrics or thresholds used for each.
- Training data is subsampled from 13 source datasets to balance domains, which may affect reproducibility if mixture weights are not strictly followed.
- Evaluation relies on three different agent frameworks (OpenHands, AgentLab, SWE-Agent), meaning results may vary based on framework-specific tool interfaces and sandbox configurations.

## Evidence (verbatim from paper)

> We evaluated these agents across 4 benchmarks (based on the availability of benchmark evaluation code and specialization of agents) that span different domains. This comprehensive evaluation demonstrates ADP’s expressiveness in preserving critical information across diverse tasks. SWE-Bench (Jimenez et al., [2024]) evaluates agents on real‑world software engineering tasks. Given a Github codebase and a bug report, agents must generate patches that satisfy existing unit tests. We used the SWE-Bench Verified subset for evaluation (Chowdhury et al., [2024]). WebArena (Zhou et al., [2024]) provides a realistic, self‑hosted web environment composed of fully functional websites in domains like e‑commerce, forums, and map navigation, requiring agents to interpret high‑level natural language commands and perform concrete web interactions. AgentBench (Liu et al., [2024b]) evaluates agents across different environments, such as operating systems, databases, and web browsing. It emphasizes multi‐turn reasoning, decision making, and adaptability across domains. GAIA (Mialon et al., [2023]) is a benchmark for general AI assistants featuring human‑annotated tasks that combine reasoning, tool use

## Citation

```bibtex
@misc{song2025agentdataprotocol,
  title={Agent Data Protocol: Unifying Datasets for Diverse, Effective Fine-tuning of LLM Agents},
  author={Song et al. (2025)},
  year={2025},
  note={arXiv:2510.24702}
}
```

- arXiv: 2510.24702
