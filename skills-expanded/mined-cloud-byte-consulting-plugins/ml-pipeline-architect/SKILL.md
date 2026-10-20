---
name: ml-pipeline-architect
description: Design automated ML training and retraining pipelines on Kubernetes with Argo Workflows or Kubeflow Pipelines, covering data validation, features, training, evaluation, registration, deployment, triggers, caching, and spot economics. Use for continuous training, ML DAGs, orchestrator selection, new-data or drift triggers, quality gates, conditional registration, pipeline parameters, checkpointing, or turning one-off scripts into repeatable workflows.
---

# ML Pipeline Architect

## Purpose
Turn one-off training scripts into parameterized, automated, cached, cost-aware pipelines on the org's managed Kubernetes (Lambda GPU cloud — no SageMaker/Azure ML/Vertex; the stack is Argo Workflows/Kubeflow + MLflow + S3-compatible object storage). Design the step graph, choose the trigger model, pick the orchestrator with a defensible rule, and engineer the cost profile (caching + preemptible GPUs). Pipelines exist so researchers stop manually rerunning scripts every time new data arrives and so bad data fails fast instead of producing a plausible-looking bad model.

## Core model to hold in your head

### MLOps maturity — the three stages
- **v1.0 — Manual**: build, train, tune, deploy by hand (notebooks and scripts).
- **v2.0 — Orchestrated**: pipelines exist but a human starts them.
- **v3.0 — Automated**: pipelines start themselves from *deterministic* triggers (code commit, new data, schedule) or *statistical* triggers (drift, bias, explainability divergence).

Rules that follow:
- Diagnose where the team is, then design for exactly one stage up — don't sell v3.0 drift-triggered retraining to a team without a working v2.0 pipeline.
- Know when *not* to build: during rapid feature/model/hyperparameter exploration a pipeline's rigidity hurts — deploy pipelines when training becomes regular.
- Even in the lab, the simplest pipeline (data check → train → evaluate) improves exploration: fewer subtle bugs, lineage for free, and infrastructure that scales past the laptop.
- Pipelines pay for themselves in avoided incidents: small upstream application changes routinely introduce quality issues (values out of range, schema drift) that a model will happily train through and then hurt the business in production.

### The step taxonomy (what each stage validates)
Every effective training pipeline is some subset of these steps, in order. Each step declares typed inputs/outputs (object-storage URIs) so the orchestrator can pass artifacts, cache, and parallelize:

| Step | Does | Validates / gates |
|---|---|---|
| Data ingestion & versioning | Read raw data (DB, object store, stream); convert to pipeline format (Parquet/CSV/JSONL); version raw *and* transformed sets | Both dataset versions recorded — the lineage anchor |
| Data analysis & validation ("step 0") | Schema, ranges, null rates, class balance, bias checks | **Raise a pipeline exception on bad data before any GPU spend.** Data-quality issues are the #1 cause of bad pipelines; a model can "train successfully" on garbage |
| Feature engineering | Transform to model inputs (tokenization, embeddings); balance and split train/validation/test; publish shared features | Split ratios and balancing recorded as parameters; features reusable org-wide |
| Model training & tuning | Train with a hyperparameter set; optionally HPO loop (random/Bayesian, early stopping) | Objective metric extracted per run; repeat until sufficient |
| Model evaluation | Score against the held-out test split; confusion matrix/AUC/task metrics; segment-level checks (per-category bias) | Writes a metrics artifact (evaluation.json) consumed by the gate |
| Conditional registration & deployment | Compare metrics artifact to threshold; register version + metadata only if passed; deploy to staging on approval, production on second approval | The condition step: below-threshold models never enter the registry. Separate *model-build* (researcher-owned, to staging) from *model-deploy* (platform-owned, to production) for access control |
| Feedback & skew detection | Monitor business metrics; compare live input/prediction distributions to the training baseline | Training-serving skew or drift → emits the retrain trigger (closing the v3.0 loop) |

**Parameterize everything** that varies between runs, as first-class pipeline parameters with defaults, not hardcoded values:
- Data: input URI, dataset version, split percentages, balancing flags.
- Model: hyperparameters (learning rate, sequence length, epochs), base-model/image tags.
- Gates: metric thresholds, approval toggles.
This is what lets one pipeline definition serve experimentation (override a param) and production (defaults + trigger) — and what makes A/B/multi-armed-bandit variants cheap: run the same pipeline concurrently with different parameter sets to train and deploy competing versions.

### The four-trigger taxonomy (a design decision, not an afterthought)
Choose deliberately per pipeline; most orgs need two or three:

| Trigger | Mechanism on K8s | When it's right | Watch out |
|---|---|---|---|
| GitOps commit | CI (GitHub Actions) on merge to the pipeline/training-code repo submits the workflow | Code or config changed — model must be rebuilt to stay reproducible | Keep build-and-register separate from deploy; deploy needs its own approval |
| New-data event | Object-store bucket notification (S3-compatible event → webhook/Argo Events → workflow) | Data lands irregularly; freshness drives value | Don't fire per-object — batch/debounce; consider incremental training on the new slice |
| Schedule | Argo CronWorkflow / K8s CronJob (cron syntax) | Steady data flow; predictable cost windows; simplest to reason about | Wasteful if data rarely changes — pair with a "data changed?" first step that short-circuits |
| Statistical drift | Monitoring job compares live distributions vs training baseline (data drift, model-quality drift, bias drift, feature-attribution drift); alert fires the pipeline | Mature teams (v3.0); retrain exactly when needed | Requires a baseline captured at training time and prediction logging; tune thresholds to avoid retrain storms |

### Orchestrator selection

| Option | What it is | Choose when | Decision rule |
|---|---|---|---|
| **Argo Workflows** | K8s-native workflow engine; CRD-based; each DAG step = a pod; retries, artifacts, parallelism; underlies Kubeflow Pipelines, Katib, Seldon | K8s-first shop, general-purpose (ML + batch + CI/CD), minimal platform overhead | **Default here** — the org is already on managed K8s and Argo doubles for non-ML batch |
| **Kubeflow Pipelines** | ML-specific layer on K8s (with Notebooks, Katib HPO, KServe serving); DAGs, artifact repo, metadata/lineage, step caching | You want the integrated ML platform (notebooks + HPO + serving + pipelines) and accept operating it | Pick if the team will use ≥2 other Kubeflow components; it's a platform to run, not just a library — budget real ops time |
| **Apache Airflow** | Mature ETL/data-engineering orchestrator; huge operator library | Airflow already runs the org's data pipelines; ML DAGs ride existing rails | Never introduce Airflow *for* ML; adopt only if it's incumbent. Has built-in Dask support |
| **MLflow (Projects/recipes)** | Experiment tracking + packaging with *limited* workflow support | Lightweight chaining of steps during research | Not an orchestrator — pair it with Argo/Kubeflow as the tracking layer, never as the DAG engine |
| **TFX** | Python component libraries covering every pipeline step; runs *on top of* an orchestrator; distributed processing via Apache Beam | Deep TensorFlow shop wanting opinionated structure | Rare here (PyTorch-leaning research org); adds a Beam learning curve; limited non-TF support |

### Step caching (cost + iteration speed)
Most engines can skip a step whose inputs haven't changed: cache key = input artifacts + parameters (+ image); on hit, prior outputs are reused and the pipeline continues. Kubeflow Pipelines has native step caching; Argo has memoization (cache key + ConfigMap-backed cache with TTL).
- Design steps deterministic so a cache hit is actually safe to reuse.
- Key on dataset *version*, not file path — a path-keyed cache silently serves stale features after the data changes.
- Set an expiry (`expire_after`/TTL); never cache the evaluation/condition gate.
- Payoff is largest for expensive feature engineering (tokenization/embedding of a large corpus) sitting upstream of many training iterations — and for restart-after-failure, where completed steps replay from cache instead of re-running.

### Spot/preemptible training economics
Preemptible GPU capacity is the single biggest training cost lever, and it only works with engineering:
- **Checkpointing is mandatory** — write checkpoints to object storage on an interval; on preemption the replacement pod resumes from the last checkpoint instead of restarting. Modern frameworks (PyTorch, TF) tolerate node loss but need explicit checkpoint/restore code and config.
- Bound the blast radius: set a max wait/run time; cap retries; make steps idempotent so a re-run is safe.
- Mix pools: run the head/orchestration and short critical steps on-demand; long training steps on preemptible nodes.
- Multi-node jobs on spot amplify the gang-scheduling problem — see distributed-training-advisor for the Kueue/Volcano caveat.
- Remaining levers: step caching (above), early-stopping HPO, right-sized instance types per step (CPU pods for prep/eval, GPU only for train).
- Track pipeline cost per run as a first-class metric alongside model quality — a retraining trigger that fires too often is a budget bug, and you can't tune what you don't measure.

## Workflow
1. **Inventory the current loop.** For [the team's model], map how training happens today onto the maturity stages: who runs what, where data/artifacts live, what's manual. Identify the pain (stale models? bad-data incidents? GPU bill?).
2. **Draw the step graph.** Instantiate the taxonomy — name each step, its container, its typed inputs/outputs (object-storage URIs), its parameters, and its validation/gate. Insist on step 0 (data validation) and the conditional registration gate with an explicit metric threshold.
3. **Choose the orchestrator** with the table above; record the decision rule invoked (incumbency, platform appetite, K8s-native default).
4. **Choose triggers.** Pick from the four-trigger taxonomy per pipeline; specify the mechanism (CI job, bucket event, CronWorkflow, monitor alert) and debounce/short-circuit behavior.
5. **Engineer cost.** Mark cacheable steps and their cache keys; mark preemptible-safe steps and their checkpoint URIs + resume logic; assign CPU vs GPU node pools per step.
6. **Wire tracking and registry.** Every training/eval step logs to MLflow; registration follows the promotion criteria from `experiment-registry-standard`. Lineage must let you walk from any deployed model back to raw-dataset version.
7. **Define the human gates.** Staging deploy on registration approval; production deploy on a second approval; name the approver roles (researcher vs platform).
8. **Output.** A pipeline design doc: step table (image, inputs, outputs, params, gate), trigger spec, orchestrator decision + rule, caching/spot plan with checkpoint locations, tracking/registry integration points, and a skeleton workflow manifest (Argo `WorkflowTemplate` or Kubeflow pipeline definition) the team can fill in.

## Guardrails
- No pipeline without a data-validation step that can fail the run before training spends GPU hours.
- No unconditional registration — a metric-threshold condition step guards the registry, and evaluation runs on a held-out test split, never training data.
- Don't recommend Kubeflow to a team that only needs pipelines; don't recommend Airflow unless it's already the org's incumbent.
- Never enable spot/preemptible training without checkpoint-and-resume demonstrated in a test run.
- Keep model-build and model-deploy as separately-permissioned phases; researchers promote to staging, not production.
- Statistical-drift triggers require a stored training baseline and prediction logging — don't promise v3.0 without them.
- Cache keys must include dataset version and parameters; a cache keyed on file path silently serves stale features.
- This org runs OSS on Lambda managed K8s — translate any managed-service pattern (SageMaker Pipelines etc.) to Argo/Kubeflow + MLflow + object storage rather than recommending the service.

## Suggested effort
Medium-high — one session for the design doc (steps 1–7); a second to pair on the skeleton manifest and a smoke-run with caching and a forced preemption test.
