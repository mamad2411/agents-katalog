---
name: inference-rollout-strategist
description: Choose and design a safe production rollout for model inference on GPU Kubernetes, including shadow, canary, blue-green, A/B, and bandit strategies. Use for traffic splitting, progressive delivery, versioned endpoints, batch-versus-real-time decisions, model selectors and caching, rollback triggers, KServe-style serving, or asymmetric KEDA/HPA autoscaling.
---

# Inference Rollout Strategist

## Purpose
Once a model clears the release gate, decide *how* it meets real traffic and design the mechanics: the serving pattern, the traffic-shifting ladder, the versioned-endpoint plumbing, the autoscaling policy, and — most importantly — the rollback triggers wired to the eval and monitoring signals so a bad model retreats automatically. A great model rolled out carelessly is still an incident. This skill turns a green gate into a safe, reversible production exposure.

## Core model to hold in your head

### First fork: batch vs real-time
| | Real-time endpoint | Batch / offline |
|---|---|---|
| Optimize for | **Latency** — interactive, per-request | **Throughput** — bulk, tolerant of staleness |
| Interface | REST/gRPC, streaming | Job reads from object store, writes results |
| Lifecycle | Runs 24/7, autoscaled | Cluster spins up, runs, tears down |
| Cost | Higher, continuous | Lower, predictable |
| Use when | Live research UIs, interactive eval, A/B or bandit comparison | Nightly re-scoring, large eval sweeps, dataset labeling |
| GPU note | Latency-bound; asymmetric autoscaling | Batches exploit GPUs best; teardown saves cost |
Decide this first — it determines everything downstream. Research inference testing usually needs a real-time endpoint for interactive evaluation *and* batch jobs for large offline eval sweeps; they can coexist behind the same registry version. A useful default: serve the interactive path real-time with asymmetric GPU autoscaling, and run periodic large-scale evaluation as batch jobs that spin up, saturate the GPUs, and tear down — cheaper and kinder to scarce GPU capacity than holding a giant endpoint idle between sweeps.

### Shadow mode specifics
Shadow is the safest first exposure and worth designing carefully because it carries zero user risk: mirror live production requests to the new model version, **serve the incumbent's response to the user, and discard the shadow response** after logging it. It validates the candidate on the true production distribution — the inputs an eval dataset can never fully anticipate — surfacing latency, error, and behavior problems before a single user sees an answer. Pair it with the `llm-eval-harness` guardrail metrics scored on the shadow responses so you get a quality read, not just a liveness read, before promoting to canary.

### The rollout ladder (shadow → canary → blue/green → A/B → bandit)
Each rung trades safety for signal. Pick the lowest rung that answers your question.

| Strategy | What it does | Traffic | Intent | Use when |
|---|---|---|---|---|
| **Shadow** | New model receives mirrored traffic, responses discarded | 0% served, 100% mirrored | Validate on real inputs with zero user risk | Highest-risk first exposure; verifying perf/behavior on prod distribution |
| **Canary** | Small slice served by the new model | ~5% → grow | **Risk mitigation** — catch prod-only issues on few users | Every routine promotion; the default |
| **Blue/green** | Full parallel cluster, flip traffic at once | 0→100% instant | Fast cutover + instant rollback | Avoiding the mixed-version debugging state; keep blue idle ~24h for rollback |
| **A/B** | Two variants split for statistical comparison | e.g. 50/50, run for weeks | **Measure** which model wins on a business/quality metric | Comparing candidates on outcomes, not just risk; needs significance |
| **Bandit (MAB)** | RL router shifts traffic toward the winner dynamically | Adaptive | Minimize regret; exploit winner early while still exploring | Many variants, want to stop paying for losers mid-experiment |

Canary and A/B both split traffic but differ in intent: canary is about *risk* on a small group for a short window; A/B is about *statistical evidence* on a larger group over a longer window (weeks, for significance). Bandits beat fixed A/B when a bad variant is costly — a static A/B keeps sending traffic to a losing variant for the whole run, accruing regret, and can't shift mid-experiment or add/remove variants. A bandit **explores** (keeps testing non-winners in case the early leader isn't the true best) and **exploits** (routes more traffic to the current best) dynamically, minimizing regret. Named exploration strategies: epsilon-greedy (fixed explore threshold), Thompson sampling (dynamic Bayesian threshold), online cover, bagging.

Instrument a bandit with three quantities:
- **Reward** — e.g. 1 if the response was correct/accepted, 0 otherwise.
- **Action probability** — probability a given model is the best choice given accumulated reward + context.
- **Sample probability** — probability the router actually picks that model given its exploration policy.

You can seed the bandit by pre-training on historical data so it starts near the right split and pays less exploration regret early.

### Testing a nondeterministic system before and during rollout
Models are nondeterministic, so equality assertions don't work at this layer. Gate rollout progression on **statistical "good enough" testing** — evaluate a change across a large selection of prompts and ask whether it improves quality *on average*; a change that helps one input but hurts many others must fail. Use **LLM-as-judge** to score response quality at the scale human review can't reach. This is the same measurement the `llm-eval-harness` produces; the rollout consumes its aggregate verdict per exposure step, not per request.

### Progressive rollout mechanics on Kubernetes
- **Versioned model endpoints.** Serve each model version behind its own endpoint/revision; the router shifts weight between versions (KServe-class canary weight, or Service-weighted routing). Models change less often than code but each change has large, unpredictable quality impact — so expose progressively: small user subset or single geography → grow to 100% as confidence builds.
- **Model-selector API.** Front the versions with a wrapper API that takes a parameter for *which* model to use; this hides the model choice from callers and lets you point dev/test at a cheap **SLM** and prod at the full **LLM** (a Kubernetes Service swap). Use small/cheap models for continuous evaluation and automated tests unless you are specifically evaluating quality — it keeps CI cost down without changing the interface under test.
- **Model caching.** Large model weights must not be re-downloaded per pod start (adds minutes). Cache weights in a shared filesystem or an in-memory store so every serving replica loads from the same cache and survives restarts/redeploys without re-download — this also makes the cold-start numbers from `inference-benchmark-runner` tractable and shrinks the scale-out lag that the autoscaling policy has to absorb.
- **Model format for portability.** Distribute in an open format (e.g. ONNX) rather than a framework-native one when models move between environments, so the selector API can serve heterogeneous checkpoints behind one interface.
- **Gate the progression on feedback signals**, not just errors/latency — measure whether users/evaluators stay satisfied with responses before widening exposure.

### Production variants — one endpoint, many models
Implement the ladder with **production variants**: multiple model versions behind a single endpoint, each a (instance type + count + model) unit, with traffic apportioned by weight rather than strict percentage. Shifting a rollout is then a weight update, not a redeploy:
- **Canary** = give the new variant a small weight (one instance out of twenty ≈ 5%); grow the weight as confidence builds.
- **Blue/green** = stand up a full parallel variant, shift 100% of weight at once, keep the old variant idle (~24h) for instant rollback, then retire it.
- **A/B** = fixed weights (e.g. 50/50) held long enough for significance, then shift to 0/100 for the winner.
- **Bandit** = a router variant that owns 100% of ingress and dynamically dispatches to the underlying model variants by sample probability.
For fine-grained routing (by header, region, or user cohort) put a load balancer in front and route to variants explicitly rather than by weight.

### Rollback triggers wired to eval metrics
A rollout is only safe if it halts automatically and rolls back on confirmed candidate harm. Compare the candidate with the incumbent over a documented confirmation window and require the regression to correlate with candidate exposure:
- **Quality/safety:** a sustained faithfulness, answer-relevance, or safety regression below the gate floor relative to the incumbent may trigger automatic rollback.
- **Performance:** a sustained candidate-correlated p95 TTFT, end-to-end latency, or error-rate breach may trigger automatic rollback.
- **Data or attribution drift:** halt rollout expansion and page by default. These signals can reflect legitimate traffic change that rollback cannot fix; roll back only when a confirmed quality/safety regression is also exposure-correlated.
- **Model-quality or bias drift:** halt and investigate; automate rollback only when the confirmation window and incumbent comparison attribute harm to the candidate.
- **Business/feedback:** halt on regression; roll back automatically only when experiment design establishes candidate causality and the minimum-sample rule is met.
Rollback mechanics differ by strategy:
- **Blue/green** — fastest rollback: flip 100% of weight back to the idle blue variant.
- **Canary** — zero the canary weight; the incumbent already carries the majority of traffic.
- **A/B** — abort the experiment, route 100% to the incumbent variant.
- **Bandit** — the router already starves a losing variant, but wire an absolute floor that yanks a variant on a hard SLO or safety breach rather than waiting for reward to converge.

Define the trigger, confirmation window, incumbent comparison, automated action, and who is paged before shifting the first percent—a rollback path designed during an incident is not a rollback path.

### Autoscaling policy pairing (asymmetric for GPU)
GPU serving needs **asymmetric autoscaling — fast scale-out, slow scale-in**. Pair the rollout with:
- **Scale-out fast:** near-zero stabilization window, aggressive step (e.g. double replicas within seconds) so latency spikes are absorbed immediately.
- **Scale-in slow:** long stabilization window (e.g. 120s+) before removing pods — expensive GPU capacity you may need again should not be released on a brief dip.
- **Scale on serving signals, not node CPU:** drive KEDA/HPA off Prometheus metrics — request rate and p95 latency (whichever hits its threshold first drives the action) — because GPU serving health isn't visible at the node. Use the saturation-knee concurrency from `inference-benchmark-runner` to set the target. Karpenter-class node autoscaling adds/consolidates GPU nodes underneath.
- **Preload weights to shrink scale-out lag:** the model-caching design above means a new replica loads from cache instead of downloading, so fast scale-out actually delivers capacity in seconds rather than minutes — without it, aggressive scale-out policies just queue cold pods.

## Workflow
1. **Decide batch vs real-time** (often both) from the latency-vs-throughput need.
2. **Confirm the gate is green.** Pull `model-release-gate` go + rollback thresholds; do not design a rollout for an ungated model.
3. **Pick the ladder rung.** Start at shadow for first exposure of a high-risk model; canary for routine promotions; add A/B or bandit only when you need a comparative verdict.
4. **Design the endpoint plumbing.** Versioned endpoints, model-selector API (SLM-dev/LLM-prod), model caching for fast, restart-safe loads.
5. **Wire rollback triggers.** Bind quality guardrails, performance SLOs, and drift signals to automated halt/rollback actions; name the pager target.
6. **Pair the autoscaling policy.** Asymmetric fast-out/slow-in on Prometheus serving metrics, target set from the benchmark saturation knee.
7. **Sequence the exposure.** Define the percentage/geography steps and the feedback-signal criterion for advancing each step; define the full-rollout and full-rollback end states.
8. **Dry-run the rollback.** Trigger one rollback condition in staging and confirm the automated action fires and pages correctly — an untested rollback path is a liability, not a safety net.

## Output spec
Deliver a **Rollout Plan**: (1) batch-vs-real-time decision with rationale; (2) chosen ladder strategy with the when-each justification and, if A/B or bandit, the comparison metric and stopping rule; (3) endpoint architecture — versioned endpoints, model-selector API, model-caching design; (4) the exposure schedule (steps, per-step advance criterion, end states); (5) rollback-trigger table — signal, threshold, automated action, pager target — sourced from the gate and the drift monitors; (6) autoscaling policy — asymmetric scale-out/scale-in config, the Prometheus signals and targets, the saturation-knee input; (7) handoff to `drift-monitor-designer` to stand up the live signals the rollback triggers depend on. Note the Lambda managed-Kubernetes / OSS context: KServe-class serving with weighted revisions, KEDA/HPA + Karpenter for scaling, Prometheus for the driving metrics.

## Siblings
`model-release-gate` (supplies the go + rollback thresholds) · `inference-benchmark-runner` (supplies the saturation knee and SLOs) · `llm-eval-harness` (supplies the guardrail thresholds that become rollback triggers) · `drift-monitor-designer` (supplies live drift signals to trigger rollback).
