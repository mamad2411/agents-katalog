---
name: ai-evaluation-dataset
description: "Build versioned JSONL evaluation datasets for AI workflows with golden/regression/holdout layers, leakage checks, rubrics, and provenance hashes. Use when creating or revising eval sets before comparing models, prompts, or RAG configs."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-09-11"
tags: ["ai-workflows", "evaluation", "dataset", "golden-set", "jsonl", "leakage", "versioning", "rubric"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# AI Evaluation Dataset AI Skill Guide (Claude)

## Overview & Engine Architecture

An evaluation dataset is a **governed test artifact**, not a bag of questions. Scores are only comparable when every run pins an **immutable dataset revision**, a **system fingerprint** (prompt/model/tools/retriever), and a **judge/scorer fingerprint**. Most “the new prompt is better” claims are dataset drift, label edits, or train/eval leakage in disguise.

Claude operates as a Principal AI Evaluation Engineer, specializing in **three-layer dataset design** (golden / regression / production-holdout), **group-aware splits**, **rubric-first labeling**, **contamination checks**, and **bridge reports** when labels change.

```
┌─────────────────────────────────────────────────────────────┐
│                 Evaluation Dataset Stack                    │
│                                                             │
│  Layers (version independently)                             │
│  ├── golden/     30–100 hand-verified canonical cases       │
│  ├── regression/ 200–500 known failures + edge coverage     │
│  └── holdout/    rolling production sample (drift)          │
│                                                             │
│  Case record                                                │
│  ├── id, input, expected_behavior, forbidden_behavior       │
│  ├── rubric / assertions, gold evidence (source+offsets)    │
│  └── tags, split, provenance, ACL, created_at               │
│                                                             │
│  Run binding                                                │
│  ├── dataset_version + content_hash                         │
│  ├── system_hash (prompt/model/retriever/tools)             │
│  └── judge_hash (rubric/LLM-judge/deterministic scorers)    │
└─────────────────────────────────────────────────────────────┘
```

---

## When to use / when not to

**Use when**

- You need to compare prompts, models, retrievers, or agent tools honestly.
- Production failures should become regression cases.
- An LLM judge needs a human-calibration subset.
- RAG needs gold evidence labels (passages/offsets), not only answers.

**Do not use when**

- The ask is a one-off demo with no reuse — a checklist may suffice.
- Someone wants to “fix” a score by editing gold labels mid-comparison without a new version + bridge.
- Private user data would be included without permission and redaction (`@ai-pii-redaction-review`).

---

## Operational Capabilities & Agent Directives

1. **Ask first**: target task, deployment population, unacceptable error types, existing evaluator format, and data-handling constraints.
2. **Reuse project schemas** when present; otherwise ship JSONL + `manifest.json` as below.
3. **Label before peeking** at candidate model outputs (reduces confirmation bias).
4. **Split by group** (document, user, ticket, conversation) — not random rows — when rows share information.
5. **Keep near-duplicates / paraphrases in the same split** (classic leakage).
6. **Version immutably**: typo fix in gold = new `vN`; never mutate a shipped file in place.
7. **Bridge on change**: evaluate the same system snapshot on old and new manifests; report unchanged / added / removed / revised deltas.
8. **Never report accuracy without running the evaluator** on the frozen hash.

---

## Three-layer strategy

| Layer | Size (start) | Purpose | Change cadence |
| :--- | :--- | :--- | :--- |
| **Golden** | 30–100 | Hand-trusted gate for releases | Rare, reviewed |
| **Regression** | 200–500 | Past bugs, edges, adversarial | Add on every incident |
| **Holdout / drift** | rolling sample | Catch product/user shift | Refresh on schedule |

Recommended intent mix for product evals (adjust to traffic):

- ~50–60% common production intents
- ~20–25% paraphrase / distractor-hard
- ~10–15% multi-hop / synthesis (if applicable)
- ~10–15% no-answer / ambiguous / policy-abstain / adversarial

For RAG specifically, include: direct lookup, paraphrase, multi-hop, constraint (“latest”, plan-tier), distractor-heavy, stale-vs-current conflict, and **explicit unanswerable** cases (catch hallucination instead of “I don’t know”).

---

## Case schema (JSONL)

One object per line. Prefer **source + character/page offsets** for evidence so chunk-size changes do not force full relabeling.

```json
{
  "id": "eval-0042",
  "split": "golden",
  "task": "support_rag",
  "input": {
    "query": "What is the refund window for enterprise?",
    "locale": "en-US",
    "user_acl": ["tenant:acme", "plan:enterprise"]
  },
  "expected_behavior": {
    "answerable": true,
    "must_include_facts": ["30 days from invoice", "enterprise plan only"],
    "preferred_answer_outline": "State 30-day window and cite policy section.",
    "gold_evidence": [
      {"source_id": "policy/refunds.md", "content_hash": "sha256:…", "start": 1204, "end": 1388}
    ],
    "gold_chunk_ids_optional": ["c-881"]
  },
  "forbidden_behavior": {
    "must_not": ["invent a different window", "cite consumer-plan policy", "bypass ACL"]
  },
  "assertions": [
    {"type": "json_schema", "ref": "schemas/support_answer.schema.json"},
    {"type": "citation_resolves_to_retrieved"},
    {"type": "regex_forbid", "pattern": "(?i)90\\s*days"}
  ],
  "rubric": {
    "dimensions": [
      {"name": "correctness", "weight": 0.4, "scale": "0-2"},
      {"name": "groundedness", "weight": 0.4, "scale": "0-2"},
      {"name": "abstention", "weight": 0.2, "scale": "0-2"}
    ],
    "pass_rule": "correctness>=1 AND groundedness>=1 AND no forbidden_behavior"
  },
  "tags": ["refunds", "enterprise", "constraint", "difficulty:medium"],
  "provenance": {
    "source": "prod_ticket:T-9182",
    "created_at": "2026-10-01",
    "annotator": "human:ali",
    "label_status": "adjudicated"
  }
}
```

### Manifest (`evals/data/v3/manifest.json`)

```json
{
  "dataset_version": "v3",
  "created_at": "2026-10-05",
  "description": "Added unanswerable refund edge cases; fixed gold span on eval-0017",
  "files": ["golden.jsonl", "regression.jsonl"],
  "case_count": 128,
  "content_hash": "sha256:REPLACE_AFTER_FREEZE",
  "changelog": ["v2→v3: 4 added, 1 revised, 0 removed"],
  "corpus_hash_optional": "sha256:…",
  "split_policy": "group_by:source_id|ticket_id; paraphrases_co_located"
}
```

Pin production/CI with `DATASET_VERSION=v3` and store `content_hash` on every result row.

---

## Procedure

### 1. Discover & scope

Collect: task definition, user population, known failure modes, severity classes (e.g. P0 = wrong medical/legal/money advice), and whether retrieval, tools, or pure generation are in path.

### 2. Seed cases

1. Cluster real query/ticket logs; sample from each cluster first.
2. Add hand-written edges underrepresented in logs.
3. Use synthetic generation **only to fill gaps**, with a different model than the judge, and human-verify before golden promotion.
4. Always add **unanswerable / abstention** cases for grounded systems.

### 3. Annotate

- Write `expected_behavior` and `forbidden_behavior` with **observable** criteria (facts, schema, citations), not a single preferred sentence.
- For subjective style, use rubric dimensions with examples of 0/1/2.
- For retrieval: label acceptable source sets + optional preferred authoritative source; report coverage vs authority separately (`@rag-retrieval-audit`).
- Pooling: for large corpora, retrieve candidates from multiple systems and label the pool (0/1/2) — do not label the entire corpus.

### 4. Split & leakage controls

- Assign `split` by originating document/user/conversation.
- Keep paraphrases of one ticket in one split (example: five rewrites of the same refund question → all `golden` or all `dev`, never mixed into holdout).
- Hold out a **hidden** set not used for prompt iteration.
- If fine-tuning or few-shot banks exist, run n-gram / near-duplicate overlap checks against those corpora (conceptually aligned with LM Evaluation Harness decontamination).
- Remove secrets; redact PII before commit.

### 5. Freeze & bind

1. Write immutable `evals/data/vN/*.jsonl` + manifest.
2. Compute content hash over canonicalized JSONL (stable key order).
3. Calibrate any LLM judge on 50–100 human-labeled items (agreement / Cohen’s κ) before trusting scaled scores.
4. Run evaluator; refuse to quote metrics without this step.

### 6. Evolve safely

- Incidents → new regression cases in a **new** version.
- Label fixes → new version + **bridge report** (same system_hash on vN and vN+1).
- Refresh holdout from production on a schedule; never silently replace golden.

---

## Production example: freeze hash + leakage grouping check

```python
"""Dataset freeze utilities: content hash + paraphrase co-location check."""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


def canonical_line(obj: dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def content_hash(jsonl_paths: Iterable[Path]) -> str:
    h = hashlib.sha256()
    for path in sorted(jsonl_paths, key=lambda p: p.as_posix()):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            h.update(canonical_line(obj).encode("utf-8"))
            h.update(b"\n")
    return "sha256:" + h.hexdigest()


def assert_paraphrase_groups_colocated(rows: list[dict[str, Any]], group_key: str = "ticket_id") -> None:
    """Fail if the same originating group appears in multiple splits."""
    by_group: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        prov = row.get("provenance") or {}
        gid = prov.get(group_key) or row.get("group_id")
        if not gid:
            continue
        by_group[str(gid)].add(row["split"])
    leaked = {g: sorted(splits) for g, splits in by_group.items() if len(splits) > 1}
    if leaked:
        raise SystemExit(f"Split leakage by {group_key}: {leaked}")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# Example:
# rows = load_jsonl(Path("evals/data/v3/golden.jsonl"))
# assert_paraphrase_groups_colocated(rows, group_key="source")
# print(content_hash([Path("evals/data/v3/golden.jsonl"), Path("evals/data/v3/regression.jsonl")]))
```

### Result row minimum (bind every run)

```json
{
  "dataset_version": "v3",
  "dataset_hash": "sha256:…",
  "system_hash": "sha256:…",
  "judge_hash": "sha256:…",
  "corpus_hash": "sha256:…",
  "metrics": {"pass_rate": 0.91, "n": 128},
  "per_case_path": "results/2026-10-05/per_case.jsonl"
}
```

For RAG, `corpus_hash` (index revision / embedding model / chunker) prevents false “model improved” reads when the corpus moved ([corpus-provenance gap](https://hongsupshin.github.io/posts/2026-02-22-rag_data_provenance/index.html)).

---

## Technical troubleshooting matrix

| Failure signature | Root cause | Fix |
| :--- | :--- | :--- |
| Scores jump after “small label tweak” | In-place mutation of gold | New `vN` + bridge on same system_hash |
| High eval, poor prod | Golden overfit / no holdout drift set | Add rolling production holdout |
| Synthetic-only set looks easy | Questions paraphrase source wording | Prefer log-derived queries; hand-write messy phrasings |
| Judge disagrees with humans | Uncalibrated LLM judge | 50–100 human labels; κ before scale-out |
| Retrieval labels break after rechunk | Labeled chunk IDs only | Relabel with source+offsets; keep chunk IDs optional |
| Train/few-shot boosts eval oddly | Contamination / leakage | Group splits; n-gram overlap check; hidden holdout |
| “Accuracy 92%” with no run artifact | Metric theater | Refuse; require hash-bound result row |

---

## Best practices

1. Start small (30–50 golden) and grow from production misses — labeling is one-time per case.
2. Separate **retrieval gold** (IDs/offsets) from **answer rubrics**; do not force an LLM judge onto arithmetic retrieval metrics (`@rag-retrieval-audit`).
3. Version judge prompts and assertion code separately; bind `judge_hash` in results.
4. Promote synthetic cases to golden only after human adjudication.
5. Use observable pass rules (schema, citations resolve, required facts) plus a thin semantic rubric.
6. Document unacceptable errors (P0) as hard gates independent of average pass rate.

---

## Limitations

- Public benchmarks may be contaminated in pretraining; prefer private product sets for ship decisions.
- This skill does not replace domain-expert review for regulated content.
- Stop and ask if permissions, population definition, or P0 severity rules are missing.

---

## Related skills

- `@rag-retrieval-audit` — score retrieval against gold evidence
- `@prompt-regression-gate` — run frozen dataset on prompt changes
- `@llm-json-contract-check` — structural assertions on outputs
- `@ai-citation-verification` — citation support checks
- `@ai-pii-redaction-review` — sanitize cases and traces
- `@llm-cost-latency-benchmark` — cost of running the set
- `@ai-human-handoff-contract` — escalate P0 / low-confidence cases

---

## Agent Operational Directive

> **MANDATORY**: Treat eval data as immutable versioned artifacts with content hashes. Split by group; co-locate paraphrases. Label expected/forbidden behavior before viewing model outputs. Bridge when labels change. Never claim accuracy without a hash-bound evaluator run. Never include secrets or unauthorized private content.

---

## Source anchors (research)

- Evaluation dataset design (golden / regression / holdout layers): [thellms.dev](https://thellms.dev/evals/evaluation-dataset-design-creating-high-quality-test-sets/)
- Immutable versioning + result provenance: [AI Evals — versioning](https://www.aievals.co/learn/datasets/versioning-lineage), [QASkills versioning](https://qaskills.sh/blog/llm-eval-golden-dataset-versioning)
- Compact golden sets & eval-driven iteration: [arXiv:2601.22025](https://arxiv.org/html/2601.22025v1)
- RAG corpus provenance gap: [Hongsup Shin](https://hongsupshin.github.io/posts/2026-02-22-rag_data_provenance/index.html)
- Decontamination concepts: [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/decontamination.md)
- r/Rag: log-first gold sets, unanswerable cases, source+offset labels, judge calibration
