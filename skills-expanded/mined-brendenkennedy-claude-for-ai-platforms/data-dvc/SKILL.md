---
name: data-dvc
description: >
  Versioning data and model artifacts with DVC — large files stay out of git while a tiny pointer
  tracks them; a git commit + `dvc pull` reproduces the exact bytes a run used. Carries: `dvc add`
  (writes the `.dvc` pointer git commits), `dvc remote add` for S3/GCS/SSH storage, `dvc push`/`dvc
  pull` to move blobs, and reproducible pipelines (`dvc.yaml` stages, `dvc repro`, `dvc.lock`). Load
  before adding a dataset or checkpoint to the repo, wiring remote storage, or building a
  reproducible data→train→eval pipeline. Triggers: dvc, dvc add, dvc push, dvc pull, dvc repro,
  dvc.yaml, .dvc file, data versioning, version a dataset, track a model checkpoint, remote storage,
  pin data to a commit, big files in git, dataset provenance, tie data to code.
---

# data-dvc — data & model versioning with DVC

**Pinned:** dvc — unpinned · authored against 3.x · run `/skill-update data-dvc` once the dep is installed

> On-demand: load this before checking a dataset or checkpoint into the repo, wiring a DVC remote, or
> building a `dvc.yaml` pipeline. DVC keeps big files OUT of git — you commit a small pointer, not the
> bytes. If you're about to `git add data/…` a multi-GB file, stop and use `dvc add` instead.

## When this applies
Adding a dataset or model artifact to version control, pushing/pulling those bytes to shared storage, or
defining a reproducible data→train→eval pipeline whose outputs are pinned to a git commit. Pairs with the
`env-uv` skill (the env that runs the stages) and the `datasets` skill (how splits/provenance are defined
inside the data DVC tracks).

## Track data & models (the `.dvc` pointer)
- **Add a dataset/artifact:** `dvc add data/<PLACEHOLDER: dataset dir>` — DVC moves the bytes into its
  cache and writes a small `data/<...>.dvc` pointer (an md5 + path). It also auto-updates `.gitignore` so
  the raw files can't be committed by accident.
- **Commit the pointer, not the bytes:** `git add data/<...>.dvc data/.gitignore && git commit`. The
  `.dvc` file is tiny and git-friendly; the actual data lives in the DVC cache + remote.
- **Models/checkpoints** version the same way: `dvc add models/<PLACEHOLDER: checkpoint>` → commit the
  `.dvc` pointer alongside the training code that produced it.

## Wire remote storage (where the bytes actually live)
```bash
# pick ONE backend; the URL is the project's shared bucket/host
dvc remote add -d storage <PLACEHOLDER: s3://bucket/path | gs://bucket/path | ssh://host/path>
git add .dvc/config && git commit -m "configure dvc remote"
```
- `-d` makes it the default remote. Credentials go through the backend's normal auth (AWS profile, GCP
  ADC, SSH key) — **never** hardcode secrets in `.dvc/config`; see the `governance` skill (security).
- **Push bytes up:** `dvc push` (after `dvc add`/a pipeline run). **Pull bytes down:** `dvc pull` (after a
  fresh clone or checkout). `dvc status -c` compares local cache vs remote.

## Reproducible pipelines (`dvc.yaml` → `dvc repro`)
Define stages so DVC tracks the DAG of deps → outs and reruns only what changed:
```yaml
# dvc.yaml
stages:
  train:
    cmd: uv run python train.py          # the Hydra entry point; fixed overrides go on this line
    deps: [conf/, data/<PLACEHOLDER: dataset>, src/<PLACEHOLDER: pkg>/]
    outs: [models/best.pt, models/last.pt]
    metrics: [metrics.json]
```
With Hydra there is no `--config <file>` flag and no `params:` entry — DVC's `params:` wants one flat
file, which a composed `conf/` tree isn't. The config participates in the DAG as the `deps: [conf/, …]`
entry instead: any config edit invalidates the stage, which is the behavior you want.
- **Run/reproduce:** `dvc repro` — executes stages whose deps/params/outs changed, skips the rest.
- **`dvc.lock`** records the exact md5 of every dep, param, and out from the last run — the machine-checked
  record of "what produced what". Commit it. Use `uv run` in `cmd` so stages execute inside the locked env
  (see `env-uv`).

## Tie a data+model version to a git commit
This is the whole point and backs the always-on **reproducibility** convention: the git commit carries the
`.dvc` / `dvc.lock` pointers, and those md5s resolve to exact bytes in the remote. So:
```bash
git checkout <sha>     # brings back the pointers as they were
dvc pull               # fetches the exact data + model bytes those pointers name
```
reproduces the precise data and checkpoint that commit's code ran against — no "which version of the
dataset was this?" guessing.

## Gotcha
**Commit the `.dvc` / `dvc.lock` pointers in the same commit as the code that used them, and never `git
add` a raw data/model blob.** If pointer and code drift into separate commits, a checkout resurrects code
against the wrong data. If a blob sneaks into git history it bloats the repo permanently and defeats DVC —
`dvc add` first, and let DVC own `.gitignore`. Licensing/PII constraints on what may even enter the remote
are policy, not DVC's job: check the `datasets` skill and the `data-governance` canon via the `governance`
skill before pushing a new dataset.
