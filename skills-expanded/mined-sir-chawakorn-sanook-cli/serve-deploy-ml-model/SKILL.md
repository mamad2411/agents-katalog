---
name: serve-deploy-ml-model
description: Deploys a trained ML model to production — packaging it with the identical training-time preprocessing, registering a versioned model+code+data triple, serving via batch or online REST/gRPC behind a runtime (BentoML/TorchServe/Triton/ONNX), with autoscaling/warmup and canary/shadow rollout — so served predictions reproducibly match offline scoring.
when_to_use: Taking a trained model to production to generate predictions (package, register, serve, scale, roll out). Distinct from train-evaluate-ml-model (building/evaluating the model), monitor-ml-drift (post-deployment drift/quality monitoring), and deploy-release (generic application deploys with no model artifact).
---

## When to Use

Reach for this skill when a working model needs to **serve predictions in production**, not when it's still being built:

- "Deploy this model so the app/service can call it"
- "Stand up a REST/gRPC inference endpoint for `model.pkl`/`model.pt`"
- "Run nightly batch scoring over the warehouse table"
- "Roll the new model out behind the old one (shadow/canary) before cutting over"
- "Our predictions in prod don't match what we got in the notebook" (train/serve skew)
- "Speed up / scale the inference service" (ONNX export, autoscaling, warmup)

NOT this skill:
- Training, hyperparameter search, offline metrics, choosing the model → train-evaluate-ml-model
- Watching the *live* model for input drift, label delay, quality decay, alerting → monitor-ml-drift
- Shipping a normal app/service with no model artifact (web app, API, worker) → deploy-release
- Percentage ramps, kill switches, sticky bucketing for *any* change → feature-flags-rollout (this skill uses it for the model rollout)
- Latency/cost tuning of an *LLM* prompt/provider path → optimize-llm-cost-latency

## Steps

1. **Package the model WITH its exact preprocessing — this is the #1 cause of train/serve skew.** The artifact must contain the *same* feature/transform code that produced training inputs, not a reimplementation. Fit transforms on train data, serialize the fitted objects, and apply the identical pipeline at serve time.

   ```python
   # train.py — ONE fitted pipeline = preprocessing + model, saved as a unit
   from sklearn.pipeline import Pipeline
   from sklearn.compose import ColumnTransformer
   import mlflow, mlflow.sklearn

   pipe = Pipeline([("prep", ColumnTransformer(...)), ("model", clf)]).fit(X_tr, y_tr)

   with mlflow.start_run():
       mlflow.sklearn.log_model(
           pipe, "model",
           registered_model_name="churn",
           input_example=X_tr.iloc[:5],          # captures schema + dtypes
           signature=mlflow.models.infer_signature(X_tr, pipe.predict(X_tr)),
           pip_requirements="requirements.lock",  # pinned, == training env
       )
   ```
   Rules: never re-derive features in the serving codebase; serve the fitted `prep+model` as one object. For deep nets, save the transform graph (e.g. `torchvision`/`torchaudio` transforms or a `tf.function` preprocessing layer) *inside* the exported module so the runtime applies it. Stateful features (counts, embeddings, aggregates) computed from a feature store at train time must be read from the **same** store online — recomputing them in app code drifts.

2. **Register and pin model + code + data together.** A model version is meaningless without the code and data snapshot that produced it. Push to a registry (MLflow Model Registry, SageMaker, Vertex, or a tagged OCI artifact) and record, in the run/version metadata: git SHA, training-data version/hash (DVC/Delta/snapshot id), and the locked dependency file. Use registry **stages** (`Staging` → `Production`) or aliases; deploy by *immutable version*, never "latest".

3. **Pick the serving pattern by latency need — decide, don't hedge.**

   | Pattern | Use when | Interface | Default runtime |
   |---|---|---|---|
   | **Batch / offline** | No realtime need; score a table/file on a schedule | Job writes predictions to warehouse/S3 | Spark / Ray / a plain container in cron/Airflow |
   | **Online (sync)** | A user request blocks on the prediction; p99 budget < ~200 ms | **REST** (simple, debuggable) default; **gRPC** when p99 < 20 ms or high QPS | BentoML / TorchServe / Triton |
   | **Streaming** | React to an event flow (clicks, transactions) continuously | Consume Kafka/Kinesis → predict → emit | Flink / Faust / a Ray Serve consumer |

   Defaults: **batch unless something blocks on the result** — it's cheaper, simpler, and trivially reproducible. For online, start with **REST + JSON** and only move to gRPC/protobuf when a measured latency budget forces it. Do not build an online endpoint for a nightly report.

4. **Choose the runtime; export to ONNX/TensorRT only when you need the speed.** Server defaults: **BentoML** (Python-first, easy custom logic, batching) for most teams; **Triton** for multi-framework, GPU, dynamic batching at scale; **TorchServe** for pure PyTorch shops. Convert to **ONNX Runtime** (CPU) or **TensorRT** (GPU) when profiling shows the framework runtime is the bottleneck — and **re-verify outputs match** the original within tolerance (atol≈1e-4) before trusting it; quantization/op-set changes silently alter predictions.

   ```python
   # bento service.py — load a PINNED model version (never "latest"), server-side batching
   import bentoml
   from bentoml.io import JSON
   runner = bentoml.mlflow.get("churn:prod").to_runner()   # alias -> immutable version; never churn:latest
   svc = bentoml.Service("churn", runners=[runner])

   @svc.api(input=JSON(), output=JSON())   # set batchable=True + max_batch_size on the runner config for throughput
   async def predict(rows: list[dict]) -> list[dict]:
       return await runner.predict.async_run(rows)
   ```

5. **Add warmup, resource limits, and autoscaling — in that order.** Cold models cause p99 spikes: run a synthetic prediction at startup (load weights, JIT/CUDA-warm, fill caches) and gate the readiness probe on it so traffic only arrives warm. Set CPU/memory/GPU **requests and limits** from a load test (see load-stress-test), not by guessing. Autoscale on the right signal — **request concurrency / queue depth / GPU util**, not CPU% for GPU models — with `minReplicas ≥ 2` (no cold-start on scale-from-zero for latency-critical paths) and a scale-down stabilization window so it doesn't flap. Pin threads (`OMP_NUM_THREADS`) to avoid oversubscription under the container limit.

6. **Roll out shadow → canary against the current model; keep an instant rollback.** Never hard-cut. **Shadow** first: mirror live traffic to the new version, log its predictions, serve the old model's response to users — compares behavior on real traffic at zero user risk. Then **canary**: route 1% → 10% → 50% → 100% by sticky hashed bucketing, watching guardrail metrics (latency, error rate, and prediction distribution vs the incumbent); auto-halt and revert on breach. Drive the ramp/kill switch with feature-flags-rollout. Rollback = repoint the alias/route to the previous **registered version** (still deployed) — must be one command, seconds, no rebuild.

7. **Lock inference reproducibility end to end.** Serve from the **locked** requirements captured at registration (same library versions, same op-set), pin the base image by digest, set seeds where any stochasticity exists, and freeze the feature-store read path. The contract: the same input row produces a bit-identical (or within-tolerance) prediction in the notebook, the batch job, and the online endpoint.

## Common Errors

- **Reimplementing preprocessing in the serving code.** The serving normalizer/encoder/tokenizer drifts from the training one → skew. Serialize and serve the *fitted* pipeline as one artifact; never rewrite the transforms.
- **Fitting a transform at serve time** (e.g. `StandardScaler().fit(request_batch)`, or imputing with the request's own mean). Must use stats fitted on **training** data, frozen in the artifact.
- **Deploying "latest"/an unpinned stage.** A retrain silently swaps the model under prod. Deploy an immutable version id; promote via alias (`churn:prod`), not `churn:latest`.
- **Env mismatch between train and serve.** Different numpy/sklearn/torch/CUDA or ONNX op-set changes outputs. Serve from the exact locked requirements; pin the image by digest.
- **ONNX/TensorRT export assumed equivalent.** Quantization, fused ops, or op-set bumps shift predictions. Always diff converted vs original outputs on a fixed sample before shipping.
- **No warmup → readiness flaps.** First requests hit an unloaded/un-JIT'd model and time out; the cold pod is added to the pool before it can serve. Warm at startup and gate readiness on it.
- **Online endpoint for a batch problem.** Standing up a low-latency REST service to score a table on a schedule wastes cost and adds failure modes. Use a batch job.
- **Hard cutover with no shadow/canary.** A skew or perf regression hits 100% of traffic instantly. Shadow, then ramp, with auto-rollback.
- **Single replica / scale-to-zero on a latency path.** Any restart or scale event becomes a user-visible cold start. Keep `minReplicas ≥ 2`.
- **Autoscaling GPU models on CPU%.** CPU sits low while the GPU saturates → it never scales and latency explodes. Scale on concurrency/queue depth/GPU util.
- **Stateful features recomputed in app code.** Online aggregates/counts computed differently from the training feature store drift per request. Read from the same store.
- **No rollback artifact.** The previous version was torn down, so "revert" means a rebuild. Keep the prior registered version deployed and one alias-flip away.

## Verify

1. **Parity (the skew gate):** Take a **fixed** holdout sample, score it three ways — training notebook, the batch job, and the online endpoint — and assert predictions match within tolerance (exact for classification labels; `atol≤1e-4` for probabilities/regression). Any mismatch blocks the deploy. This is the single most important check.
2. **ONNX/quantized parity:** If exported, diff converted-runtime outputs vs the original framework on the same sample within tolerance.
3. **Schema/contract:** Send a malformed/missing-field request → a clean 4xx, not a 500 or a silently wrong prediction. The logged input signature matches the registered one.
4. **Latency/throughput:** Under the target arrival rate (load-stress-test), p95/p99 and sustained QPS meet the documented SLO **with warmup applied** — measure warm, not cold.
5. **Warmup/readiness:** A freshly started replica reports ready only after a successful synthetic prediction; first real request is not a cold spike.
6. **Autoscaling:** Drive load past the per-replica knee → replicas scale up on the chosen signal and back down after the stabilization window; `minReplicas` is honored at idle.
7. **Shadow:** New version receives mirrored traffic and logs predictions while users still get the incumbent's response; their distributions are comparable before any canary.
8. **Rollback:** Flip the alias to the previous version and confirm traffic serves the old model within seconds, no rebuild.
9. **Reproducibility pin:** The deployed image digest, model version, training-data hash, and git SHA are all recorded together and resolvable from the running service.

Done = served predictions match offline scoring on the fixed sample within tolerance, latency/throughput meet the SLO warm, shadow/canary ran with guardrails, and a one-command rollback to the prior registered version is proven.
