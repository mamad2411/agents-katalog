---
name: prompt-regression-gate
description: "Gate prompt, model, tool-schema, or packer changes with paired runs on a frozen eval set, slice-level regression checks, relative baselines, and explicit go/no-go thresholds. Use before merging prompt PRs or swapping models."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-09-11"
tags: ["ai-workflows", "evaluation", "prompt-regression", "ci", "baseline", "promptfoo", "a-b"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Prompt Regression Gate AI Skill Guide (Claude)

## Overview & Engine Architecture

A prompt is production code. Unit tests do not catch “fluent but worse.” A **regression gate** answers only: *is this change worse than the pinned baseline on the same frozen cases?* Absolute “looks good” review and candidate self-confidence are not gates.

Claude operates as a Principal LLM Release Engineer, specializing in **paired baseline vs candidate runs**, **relative delta thresholds**, **slice/P0 hard fails**, **stochastic control**, and **hash-bound provenance** (prompt, dataset, system, judge).

```
┌─────────────────────────────────────────────────────────────┐
│                 Prompt Regression Gate                      │
│                                                             │
│  Inputs (frozen before compare)                             │
│  ├── dataset_version + dataset_hash (@ai-evaluation-dataset)│
│  ├── baseline: prompt_hash + model + tools + retriever      │
│  ├── candidate: same knobs except the intentional delta     │
│  └── thresholds agreed BEFORE seeing scores                 │
│                                                             │
│  Runner                                                     │
│  ├── Paired per-case execution (identical context)          │
│  ├── Deterministic scorers + optional pinned LLM judge      │
│  └── Provider errors tracked separately from quality fails  │
│                                                             │
│  Gate                                                       │
│  ├── Aggregate delta vs baseline within tolerance           │
│  ├── Slice / P0: no critical regressions                    │
│  └── Verdict: go | no-go | untested + rollback plan         │
└─────────────────────────────────────────────────────────────┘
```

---

## When to use / when not to

**Use when**

- A PR touches prompts, templates, tool/JSON schemas, packers, model IDs, or retrieval config that changes model context.
- Promoting a model upgrade or temperature/tool change.
- You need a merge-blocking CI check, not a dashboard vibe.

**Do not use when**

- There is no frozen eval set yet — build `@ai-evaluation-dataset` first.
- Someone wants to “tune until the gate passes” on the **held-out** set (that destroys the audit).
- Claiming a winner without executed paired runs (deliver config only; mark **untested**).

---

## Operational Capabilities & Agent Directives

1. **Agree thresholds before scores** — write them in the PR/template; do not move bars after seeing results.
2. **One intentional delta** — change prompt *or* model *or* tools *or* retriever; log everything else as identical.
3. **Reuse held-out / golden cases** — never add failing test cases into the gate set mid-experiment to force a pass; promote failures via a **new dataset version** after adjudication.
4. **Pair cases** — same `case_id`, same retrieved context / tool stubs unless retrieval is the variable under test.
5. **Pin judges** — exact judge model + judge prompt hash; temp 0 (or documented sampling with repeats).
6. **Never** use the candidate’s self-reported confidence as the sole quality metric.
7. **Blind humans** to baseline/candidate identity when rubric review is required.
8. **Separate** provider/timeouts/rate-limits from “wrong answer” in metrics.

---

## What must be captured (run manifest)

```json
{
  "gate_id": "support-agent-prompt",
  "dataset_version": "v3",
  "dataset_hash": "sha256:…",
  "baseline": {
    "prompt_hash": "sha256:…",
    "model": "gpt-4.1-2025-04-14",
    "tools_hash": "sha256:…",
    "retriever_revision": "idx-…",
    "gen": {"temperature": 0, "max_tokens": 1024}
  },
  "candidate": {
    "prompt_hash": "sha256:…",
    "model": "gpt-4.1-2025-04-14",
    "tools_hash": "sha256:…",
    "retriever_revision": "idx-…",
    "gen": {"temperature": 0, "max_tokens": 1024}
  },
  "judge": {"model": "…", "prompt_hash": "sha256:…", "temperature": 0},
  "thresholds": {
    "max_aggregate_drop": 0.02,
    "max_slice_drop": 0.03,
    "p0_allowed_regressions": 0,
    "min_decisive_cases_for_claim": 50
  },
  "budget": {"max_usd": 25, "repeats": 1}
}
```

Hash prompt files as canonical bytes (normalized newlines). Include system + developer + tool descriptors in `prompt_hash` / `tools_hash`.

---

## Scoring strategy

| Output type | Prefer | Notes |
| :--- | :--- | :--- |
| JSON / tools / enums | Deterministic (`@llm-json-contract-check`, exact/regex) | Cheap, stable CI |
| Citations / grounding | Deterministic resolve-to-context | Don’t LLM-judge retrieval arithmetic |
| Open-ended quality | Rubric or pinned LLM judge | Average ≥2 judge passes if noisy |
| Safety / refusal | Dedicated slice + hard gate | Average gains must not hide P0 |

**Relative gate (recommended):** fail if `score_candidate < score_baseline - tolerance` (often 0.02–0.05 absolute pass-rate or mean rubric). Absolute floors (“must be ≥90%”) are optional secondary bars and go stale.

**Per-case first-class outcomes**

- `improved` / `regressed` / `tied` / `error_baseline` / `error_candidate`
- Slice tags from the dataset: `p0`, `refusal`, `ambiguous`, `adversarial`, `rag`, `latency_sensitive`

A small average gain that hides a P0 regression is a **no-go**.

---

## Statistical honesty (don’t overclaim)

On paired decisive cases (exclude ties), a coin-flip null is ~50/50 wins. Rough two-sided sign-test intuition (llmbestpractices):

- ~100 decisive cases → need ~61 wins for p&lt;0.05
- ~50 decisive cases → need ~33 wins

Report sample size and uncertainty. “+2pp on 40 cases” is usually noise—not a promotion story.

If outputs are stochastic and budget allows: repeat each case N times (e.g. 3) and majority-vote or average before compare.

---

## Procedure

### 1. Preflight (block if missing)

- Frozen dataset + hash; thresholds; baseline artifact from **main** (not another open PR)
- Secrets for providers; cost budget
- Path filter intent: only run when prompts/evals/LLM call paths change

### 2. Execute paired runs

1. Load cases; for each `case_id`, run baseline then candidate (or parallel with isolated caches).
2. Score with the same scorers/judge revision.
3. Record missing runs and HTTP/provider errors separately.
4. Persist per-case JSONL + summary.

### 3. Apply gate rules (order matters)

1. **Infra**: if candidate error rate exceeds agreed bound → no-go (or retry once).
2. **P0 / critical slice**: any regression beyond tolerance → no-go.
3. **Aggregate**: relative drop beyond `max_aggregate_drop` → no-go.
4. **Optional**: latency/cost ceilings (`@llm-cost-latency-benchmark`).
5. Else **go**, with failing/improving example links.

### 4. Deliverable

Always produce:

1. Go / no-go / **untested** (if runs did not execute)
2. Aggregate + slice table (baseline, candidate, delta)
3. Top regressed `case_id`s with short diffs
4. Provenance hashes (dataset, prompts, judge, system)
5. Rollback: revert prompt file / model pin / feature flag instructions

After merge on main: refresh **baseline artifact** from the new main run (explicit promotion).

---

## Production example: relative gate comparator

```python
"""Compare baseline vs candidate per-case scores; exit 1 on regression."""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import fmean
from typing import Any


@dataclass(frozen=True)
class Thresholds:
    max_aggregate_drop: float = 0.02
    max_slice_drop: float = 0.03
    p0_allowed_regressions: int = 0
    error_rate_max: float = 0.05


def load_scores(path: Path) -> dict[str, dict[str, Any]]:
    """JSONL rows: case_id, score (0..1), slice (list[str]), error (bool)."""
    out: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        out[row["case_id"]] = row
    return out


def mean_score(rows: dict[str, dict[str, Any]], ids: list[str] | None = None) -> float:
    keys = ids or list(rows)
    vals = [rows[i]["score"] for i in keys if not rows[i].get("error")]
    return fmean(vals) if vals else float("nan")


def gate(baseline_path: Path, candidate_path: Path, th: Thresholds) -> int:
    b, c = load_scores(baseline_path), load_scores(candidate_path)
    ids = sorted(set(b) & set(c))
    if not ids:
        print("NO-GO: no paired case ids")
        return 2

    b_err = sum(1 for i in ids if b[i].get("error")) / len(ids)
    c_err = sum(1 for i in ids if c[i].get("error")) / len(ids)
    if c_err > th.error_rate_max:
        print(f"NO-GO: candidate error rate {c_err:.2%} > {th.error_rate_max:.2%}")
        return 1

    # P0 regressions: baseline pass-ish, candidate worse beyond tiny eps
    p0_regs = []
    for i in ids:
        slices = set(b[i].get("slice") or []) | set(c[i].get("slice") or [])
        if "p0" not in slices:
            continue
        if b[i].get("error") or c[i].get("error"):
            continue
        if c[i]["score"] + 1e-9 < b[i]["score"]:
            p0_regs.append(i)
    if len(p0_regs) > th.p0_allowed_regressions:
        print(f"NO-GO: P0 regressions: {p0_regs}")
        return 1

    b_mean, c_mean = mean_score(b, ids), mean_score(c, ids)
    drop = b_mean - c_mean
    print(f"aggregate baseline={b_mean:.4f} candidate={c_mean:.4f} drop={drop:.4f}")
    if drop > th.max_aggregate_drop:
        print("NO-GO: aggregate regression")
        return 1

    # slice checks
    slice_names = sorted({s for i in ids for s in (b[i].get("slice") or [])})
    for name in slice_names:
        sids = [i for i in ids if name in (b[i].get("slice") or [])]
        sd = mean_score(b, sids) - mean_score(c, sids)
        print(f"slice {name}: drop={sd:.4f} n={len(sids)}")
        if sd > th.max_slice_drop:
            print(f"NO-GO: slice regression ({name})")
            return 1

    # paired win counts (exclude ties & errors)
    wins = loses = 0
    for i in ids:
        if b[i].get("error") or c[i].get("error"):
            continue
        if c[i]["score"] > b[i]["score"] + 1e-9:
            wins += 1
        elif c[i]["score"] + 1e-9 < b[i]["score"]:
            loses += 1
    print(f"paired decisive wins={wins} loses={loses} (ties excluded)")
    print("GO")
    return 0


if __name__ == "__main__":
    sys.exit(gate(Path(sys.argv[1]), Path(sys.argv[2]), Thresholds()))
```

### CI sketch (path-filtered)

```yaml
# Run only when prompts / evals / LLM callers change
on:
  pull_request:
    paths: ["prompts/**", "evals/**", "src/**/llm/**", ".github/workflows/prompt-gate.yml"]

# 1) Run candidate suite → candidate.jsonl
# 2) Fetch baseline.jsonl from main branch artifact or committed baseline
# 3) python scripts/prompt_gate.py baseline.jsonl candidate.jsonl
# 4) On main merge: refresh baseline artifact
```

Compatible runners: Promptfoo (`eval --fail-on-error` + custom delta), Evalgate-style baseline compare, DeepEval for RAG slices—**same relative question**.

---

## Technical troubleshooting matrix

| Signature | Root cause | Fix |
| :--- | :--- | :--- |
| Flaky red/green | temp&gt;0, unpinned judge, tiny N | temp 0; pin judge; more cases/repeats; tolerance margin |
| “Improved” after editing gold | Dataset moved mid-gate | Immutable dataset; bridge via `@ai-evaluation-dataset` |
| Baseline from another PR | Wrong artifact selection | Only `ci`/`main` baselines |
| Avg up, safety down | No slice gates | Hard-fail `p0` / `refusal` slices |
| README PR burns $ | No path filter | Limit workflow paths |
| Untested marked GO | Skipped runner | Forbid; status must be untested/no-go |
| Model upgrade blamed on prompt | Multiple deltas | Single-variable compare; re-baseline deliberately |

---

## Best practices

1. Treat prompts as versioned files with hashes, not ChatGPT scratchpads.
2. Grow the set from production failures; keep adversarial/refusal as visible slices.
3. Prefer deterministic scorers in CI; LLM judges for open-ended with pins + averaging.
4. Update eval cases in the **same commit** when output contracts/schemas change.
5. Re-baseline consciously when upgrading the judge or dataset version—never silently.
6. Post a PR comment table (baseline / head / delta / slice)—humans review regressions, CI blocks merges.

---

## Limitations

- Gates measure the frozen set, not the whole world—pair with production holdout monitoring.
- This skill does not replace red-team security testing (`@agent-injection-boundary-test`).
- Stop and ask if thresholds, baseline source, or dataset hash are missing.

---

## Related skills

- `@ai-evaluation-dataset` — frozen cases + hashes
- `@rag-retrieval-audit` — isolate retrieval before prompt gates
- `@llm-json-contract-check` — deterministic structured scorers
- `@llm-cost-latency-benchmark` — cost/latency ceilings in the same gate
- `@ai-citation-verification` — grounding assertions
- `@prompt-regression-gate` — this skill
- `@ai-human-handoff-contract` — P0 human paths

---

## Agent Operational Directive

> **MANDATORY**: Gate with paired baseline vs candidate on a frozen hashed dataset. Agree thresholds before scores. Fail on P0/slice regressions even if the average rises. Pin judge and generation settings. Record provider errors separately. Without executed runs, mark **untested**—never invent a go. Deliver rollback instructions with every no-go.

---

## Source anchors (research)

- [Prompt evals and regression testing](https://llmbestpractices.com/prompt-engineering/prompt-evals) (paired runs, sign-test caution, don’t tune on gold)
- [LLM evals in CI/CD — relative gates](https://ai-tldr.dev/learn/evaluation-safety/evaluation-basics/llm-eval-ci-cd-pipeline/)
- [Promptfoo CI/CD](https://github.com/promptfoo/promptfoo/blob/main/site/docs/integrations/ci-cd.md)
- Evalgate / prompt-regress patterns: baseline delta, PR comments, main-only baselines
- Agent eval templates: Promptfoo + DeepEval + regression delta threshold
