---
name: serving
description: >
  Shipping a model — batch scoring jobs and online endpoints. Carries: the batch-first bias (a
  scheduled scoring job beats an endpoint whenever latency isn't a stated requirement), the
  endpoint shape (load the model ONCE at startup from the registry alias `models:/<name>@champion`
  — never per-request), training-serving skew prevention (import the SAME preprocessing module
  training used; never reimplement it), input validation at the boundary (schema mirrors
  training-time assumptions; reject, don't coerce), export paths (ONNX/TorchScript with an
  output-parity check), model version stamped into every prediction, prediction logging wired
  BEFORE launch (the `monitoring` precondition), and latency/throughput basics (batching,
  workers, timeouts). Load when deploying, building an inference endpoint or batch scorer, or
  exporting a model. Triggers: deploy, serve, serving, endpoint, inference API, FastAPI, batch
  scoring, ONNX, TorchScript, export the model, latency, throughput, real-time prediction,
  production, ship the model.
---

# serving — the model meets traffic

> On-demand: load this at deploy time (P6→P7). Which model ships is the registry's alias
> (`tracking-mlflow`), promotion is governed (`model-governance` + decision log), and the moment
> it serves, `monitoring` takes over — this skill is the mechanics between those: the scoring
> path itself.
>
> **Where the neighbours start:** endpoint authentication and per-request authorization are
> `authn-authz` (`I4`, `I5` — a valid token is not an authorization decision); what may be logged
> is `security.md` `S6` + `data-governance`; running the endpoint on a cluster, autoscaling it,
> and GPU scheduling are `kubernetes`; timeouts, retries, circuit breakers, fallbacks, and the
> latency SLO are `reliability-sre` (`R1`, `R4`, `R5`); traces and token/cost telemetry are
> `observability`; and for an LLM endpoint, output filtering and structured-output validation are
> `guardrails` while the agent-layer design is `agent-security`.

## LLM inference endpoints — what differs from classic model serving

Most of this skill applies unchanged, but four things break the usual assumptions:

- **Load the weights once, and expect it to be slow.** Multi-gigabyte weights mean cold start is
  measured in minutes, not milliseconds — which drives the `startupProbe`, the warm-replica floor,
  and honest cold-start accounting against the latency SLO (`kubernetes`, `reliability-sre` `R1`).
- **Streaming changes the latency contract.** Time-to-first-token is what users feel; total
  completion time hides it. Emit both (`observability`), and remember that **output filters wired
  only on the complete response do nothing on the streaming path** (`guardrails`).
- **Throughput comes from continuous batching, not from more workers.** Reach for a dedicated
  inference server before optimising your own loop — see below.
- **Cost and tokens are first-class operational signals.** Per-request token and cost caps that
  fail closed are canon (`ai-security.md` `AI9`), not a nice-to-have — unbounded consumption is
  simultaneously a DoS vector and a budget incident.

Third-party model APIs are dependencies with versions: pin to a dated snapshot and record it
(`model-governance.md` `M14`), or your evaluations stop being reproducible when the provider ships.

### Self-hosting: what the inference server is doing for you

If you serve open weights yourself, use **vLLM**, **TGI**, or **Triton** rather than a FastAPI
wrapper around `model.generate()`. The gap is not incremental — it is often an order of magnitude in
throughput — and it comes from four things a hand-rolled loop doesn't do:

- **Continuous (in-flight) batching.** Naive batching waits for a batch to fill, then runs it to
  completion, so one long generation stalls every short one behind it. Continuous batching adds and
  evicts sequences *per decoding step*, so the GPU stays saturated and short requests aren't held
  hostage. This is the single biggest win.
- **KV-cache management.** The attention cache grows with sequence length × batch size and is what
  actually limits concurrency — not FLOPs. vLLM's paged allocation stops the fragmentation that
  otherwise forces you to over-provision. **Model weights are the floor of your GPU memory, not the
  ceiling**: budget the cache too, or concurrency collapses at exactly the load you sized for.
- **Prefix caching.** A shared system prompt or a long RAG context reused across requests is
  recomputed every time without it. For agent workloads with a large fixed preamble, this is a
  substantial and easily-missed saving.
- **Tensor parallelism** across GPUs for models that don't fit on one — with the caveat that it
  needs fast interconnect; across a slow link it can be slower than a quantized model on a single
  device.

**Quantization** trades quality for memory and speed, and the trade is real: FP16 → INT8/FP8 is
usually near-lossless and worth taking; INT4 buys a lot of memory and costs measurable quality.
**Measure it on your own eval set** (`agent-evaluation`), not on a published perplexity number —
the degradation is task-dependent, and it tends to show up first on exactly the hard cases you care
about.

Two operational notes: the container image is tens of gigabytes and the weights are more, so **image
pull plus model load dominates cold start** — pre-pull, keep warm replicas, and set the
`startupProbe` accordingly (`kubernetes`). And **one server per GPU**; these do not share a device
gracefully.

## First decision: batch beats online until proven otherwise
If predictions are consumed on a cadence (daily scores, nightly QC reports), ship a **scheduled
batch job**: score → write to a table/file → done. No service to keep alive, trivial retries,
easy backfills, and monitoring is just reading the output table. Build an online endpoint only
when a stated latency requirement exists — it's an operational liability you now own 24/7.

## The endpoint shape (when online is justified)
```python
@asynccontextmanager
async def lifespan(app: FastAPI):                  # load ONCE at startup — never per-request
    app.state.model = mlflow.pyfunc.load_model(f"models:/{NAME}@champion")
    app.state.version = resolve_version(NAME)      # pin what actually loaded
    yield

app = FastAPI(lifespan=lifespan)

class Item(BaseModel):                             # the boundary contract
    ...                                            # fields + ranges the TRAINING data assumed

@app.post("/predict")
def predict(item: Item):
    x = preprocess(item)                           # THE training preprocess module, imported
    y = app.state.model.predict(x)
    return {"prediction": y, "model_version": app.state.version}

@app.get("/health")
def health(): return {"ok": True, "model_version": app.state.version}
```
- **Validate at the boundary; reject, don't coerce.** Out-of-range values, unknown categories,
  wrong image sizes → 422 with a reason. Silent coercion turns bad inputs into confident wrong
  predictions.
- **`model_version` rides in every response** — without it, `monitoring`'s logs can't attribute
  drift to a rollout, and incident debugging is archaeology.

## Training–serving skew: the #1 silent killer
The serving path **imports** the training preprocessing (the same `src/<pkg>` functions —
resize/normalize/encode), it never reimplements it. Two implementations *will* diverge (one
resize interpolation flag is enough) and the model quietly degrades with no error anywhere.
Test it: one fixture through the training path and the serving path must produce identical
tensors (add it to the `testing` suite).

## Export (when the runtime can't carry torch)
ONNX / TorchScript export is fine — with a **parity check as a gate**: run N fixtures through
the original and the exported model; max output delta must be ~float tolerance. An export
without a parity check is a different model with the same name. Pin the exported artifact to
its source run (`data-dvc` + run id).

## Launch checklist
The endpoint/batch job registered in the resource matrix
(`.claude/memory/process/resources.md`: address, env keys, auth reference) · prediction
logging wired (inputs sampled, outputs, version — `monitoring` is unbootable without it) · load basics set deliberately (worker count, request timeout, batch size; measure
p95 under realistic load, don't guess) · rollback = moving the registry alias back (rehearse it
once) · shadow/canary before full traffic (per `monitoring`).
