---
name: pcq
description: >
  Use when creating, modifying, validating, running, or reviewing CQ ML
  experiments that use cq.yaml, pcq contract scripts, RunRecord artifacts,
  or CQ worker execution.
---

# pcq Skill (v4.0)

## Goal

Operate CQ ML experiments through the CQ runtime contract:

```text
cq.yaml -> resolved config -> contract script -> standard artifacts -> RunRecord
```

Use this skill when a user asks to:

- create a CQ ML experiment
- modify an existing pcq experiment
- connect any ML framework (sklearn, XGBoost, HF Trainer, PyTorch, ...)
- validate or summarize experiment artifacts
- debug missing metrics, artifacts, RunRecord, or output directory issues
- prepare a project for CQ worker execution

## Core Rules

- `cq.yaml` is the execution contract.
- `run_record.json` is the completion record.
- Use `pcq.output_dir()` for artifact paths.
- Use `pcq.save_all(...)` or equivalent standard artifact helpers.
- pcq is a contract runtime + agent CLI — there is **no model catalog** inside
  pcq. All ML code (model, dataset, loss, optimizer, scheduler, metric, train
  loop) lives in your project's `train.py`.
- Any ML framework is valid if it honors the CQ contract.

## Start Here

From the project root, gather structured state:

```bash
pcq resolve --json
pcq inspect . --json
pcq validate . --strictness 2 --json
```

Read the output before editing. Identify:

- selected `cq.yaml`
- command
- output directory
- declared metrics
- existing output artifacts

## Contract Script Pattern

Every project has one `train.py` shaped roughly like this:

```python
import pcq

cfg = pcq.config()
out = pcq.output_dir()
pcq.seed_everything(cfg.get("seed", 42))

# === Your ML code here — any framework ===
# import sklearn / torch / xgboost / transformers / ...
# build model, train, evaluate
score = float(model.score(X_test, y_test))

pcq.log(epoch=0, eval_score=score)
pcq.save_all(
    history=[{"epoch": 0, "eval_score": score}],
    status="completed",
    artifacts={"model": "model.pkl"},
)
```

`pcq.save_all()` writes 6 standard artifacts in one call:

- `config.json`
- `metrics.json`
- `manifest.json`
- `run_summary.json`
- `run_record.json` (canonical completion SSOT)
- `validation_report.json` (post-run gates)

## Validation Workflow

Before execution:

```bash
pcq resolve --json
pcq inspect . --json
pcq validate . --strictness 2 --json
```

After execution:

```bash
pcq validate-run <output_dir> --strictness 3 --json
pcq describe-run <output_dir> --json
```

For live agent observation during execution:

```bash
pcq run --path . --jsonl
pcq run --path . --events output/events.jsonl --json
```

For comparisons:

```bash
pcq compare-runs <base_output_dir> <candidate_output_dir> --json
pcq lineage <candidate_output_dir> --json
```

## Agent-Authored Plans

`ExperimentPlan` lets an LLM agent propose `set_config` mutations on cq.yaml:

```bash
pcq apply-plan plan.json --path . --json
pcq apply-planset planset.json --path . --output-pattern 'runs/exp{i}' --json
```

Plans only mutate `cq.yaml.configs.<key>`; `train.py` is your code and is not
touched.

## Common Fixes

### Artifacts Are Split Across Directories

Cause:

- code used `Path("output")` directly
- helper ignored `cq.yaml.configs.output_dir`

Fix:

- use `pcq.output_dir()`
- keep all standard artifacts under the resolved output directory
- rerun `pcq resolve --json` and `pcq inspect --json`

### Missing RunRecord

Fix:

```bash
pcq finalize <output_dir>
pcq validate-run <output_dir> --strictness 3 --json
```

### Undeclared Metric

Fix:

- add the metric to `cq.yaml.metrics`
- keep emitted `pcq.log(...)` keys aligned with declarations

## Done Criteria

A completed agent change should leave:

- valid `cq.yaml`
- contract script `train.py`
- passing pre-run validation
- standard post-run artifacts when a run was executed
- `run_record.json`
- `validation_report.json`
- clear summary of what changed and what result evidence supports it

## Attribution Usage Pattern

Every run can carry authorship metadata in `run_record.json`.
Attribution is driven entirely by `CQ_ATTRIBUTION_*` env vars —
no code changes required.

### Setting up attribution

Set env vars before calling `pcq run` or inside a launcher script:

```bash
export CQ_ATTRIBUTION_OPERATOR=user-a3f8c1e2        # 식별자 (pseudonym/UUID)
export CQ_ATTRIBUTION_COMMITTER_KIND=agent
export CQ_ATTRIBUTION_COMMITTER_ID=claude-sonnet-4-6
export CQ_ATTRIBUTION_SESSION_ID=sess-9b2d4f1a

pcq run --path . --json
```

For the full env var table and PII guidance, see
`templates/AGENTS.pcq.md` → `## Attribution`.

### Accessing attribution in describe-run output

`pcq describe-run <output_dir> --json` exposes attribution in two forms:

**Nested (full object)**:

```bash
pcq describe-run output/ --json | jq '.attribution'
# {
#   "operator": "user-a3f8c1e2",
#   "committer": {"id": "claude-sonnet-4-6", "kind": "agent"},
#   "session_id": "sess-9b2d4f1a"
# }
```

**Flat surface fields** (top-level, for easy filtering):

```bash
pcq describe-run output/ --json | jq '{
  op: .attribution_operator,
  committer_id: .attribution_committer_id,
  session: .attribution_session_id
}'
```

Filter agent-committed runs across a set of outputs:

```bash
for d in runs/*/; do
  pcq describe-run "$d" --json
done | jq -s '[.[] | select(.attribution_committer_kind=="agent")]'
```

### Conformance fixtures

Five conformance fixtures under `tests/conformance/attribution/`
cover the full attribution schema contract: `baseline`,
`agent-committer`, `operator-only`, `empty-env`, `full`.

## Worker Spec Usage Pattern

Every run can record hardware and runtime environment metadata in
`run_record.json`. Worker spec is built automatically (psutil + torch) and
optionally overridden by 13 `CQ_WORKER_*` env vars — no code changes required.

### Accessing worker_spec in describe-run output

`pcq describe-run <output_dir> --json` exposes worker spec in two forms:

**Nested (full object)**:

```bash
pcq describe-run output/ --json | jq '.worker_spec'
# {
#   "schema_version": 1,
#   "cpu": {"model": "Intel Core i9-14900K", "cores_physical": 24, "cores_logical": 32, "max_freq_mhz": 5800},
#   "memory": {"total_gb": 64.0},
#   "accelerator": {"kind": "cuda", "gpus": [{"model": "NVIDIA RTX 5080", "vram_gb": 16.0}]},
#   "os": {"system": "Linux", "machine": "x86_64"},
#   "container": {"kind": "docker"},
#   "source": "detected"
# }
```

**Flat surface fields** (top-level, for easy filtering):

```bash
pcq describe-run output/ --json | jq '{
  cpu: .worker_spec_cpu_model,
  memory: .worker_spec_memory_gb,
  accel: .worker_spec_accelerator_kind,
  gpu0: .worker_spec_gpu_model_0
}'
```

### Filtering runs by hardware

```bash
# cuda GPU가 있는 실행만 선택
for d in runs/*/; do
  pcq describe-run "$d" --json
done | jq -s '[.[] | select(.worker_spec_accelerator_kind=="cuda")]'

# 특정 GPU 모델로 필터
for d in runs/*/; do
  pcq describe-run "$d" --json
done | jq -s '[.[] | select(.worker_spec_gpu_model_0 | test("RTX 5080"))]'
```

For the full env var table, cgroups host-view warning, and PII guidance, see
`templates/AGENTS.pcq.md` → `## Worker Spec`.

## Fingerprint Usage Pattern

Every run can record the **dataset problem type** (modality, task kind, domain,
size class, PII flag) in `run_record.json`. The fingerprint is the third axis
of the matchmaker: 행위자 (Attribution) + 컴퓨터 (Worker Spec) + 문제 (Fingerprint).

### One-line agent call

```python
import pcq

fp = pcq.fingerprint(X_train, y_train, modality="tabular", task_kind="classification")
pcq.save_all(..., fingerprint=fp)
```

### Accessing fingerprint in describe-run output

`pcq describe-run <output_dir> --json` exposes fingerprint in two forms:

**Nested (full object)**:

```bash
pcq describe-run output/ --json | jq '.fingerprint'
# {
#   "schema_version": 1,
#   "modality": "tabular",
#   "task_kind": "classification",
#   "domain": "general",
#   "n_samples": 10000,
#   "size_class": "medium",
#   "pii_flag": false,
#   "pii_layers": [],
#   "content_hash": "a3f8c1e2...",
#   "source": "detected"
# }
```

**Flat surface fields** (top-level, for easy filtering):

```bash
pcq describe-run output/ --json | jq '{
  mod: .fingerprint_modality,
  task: .fingerprint_task_kind,
  n: .fingerprint_n_samples,
  sc: .fingerprint_size_class
}'
```

### Filtering by modality across run sets

```bash
# tabular 실험만 선택
for d in runs/*/; do
  pcq describe-run "$d" --json
done | jq -s '[.[] | select(.fingerprint_modality=="tabular")]'

# multi-modality 필터: tabular 또는 time_series
for d in runs/*/; do
  pcq describe-run "$d" --json
done | jq -s '[.[] | select(.fingerprint_modality | IN("tabular","time_series"))]'

# PII 없는 classification 실험만 (content hash 비교 가능)
for d in runs/*/; do
  pcq describe-run "$d" --json
done | jq -s '[.[] | select(.fingerprint_task_kind=="classification" and .fingerprint_modality!="") | select(.fingerprint | .pii_flag==false)]'
```

For the full schema, modality detection rules, domain gate warning, PII
4-layer policy, and 6 warning codes, see
`templates/AGENTS.pcq.md` → `## Fingerprint`.

## References

- `docs/CQ_YAML_RUNTIME_CONTRACT.md`
- `docs/AGENT_OPERATING_GUIDE.md`
- `docs/JSON_CONTRACTS.md`
- `docs/STRICTNESS.md`
- `templates/AGENTS.pcq.md` — env var table + PII guidance + Worker Spec + Fingerprint
