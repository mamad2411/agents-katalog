---
name: gpu-accelerator-configuration-validation
description: >
  Guides pre-flight validation of GPU scheduling configuration — device
  plugin health, resource requests/limits, tolerations/nodeSelector, MIG
  profile availability, and driver/CUDA compatibility — before a training or
  serving job silently falls back to CPU or fails deep into a run. Use when
  the user asks to "validate GPU config before submitting a training job",
  "check why a job isn't using the GPU", "make sure a pod actually gets a
  GPU", write a pre-submit GPU validation check/admission policy, or debug a
  job that ran on CPU when it should have used a GPU.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: mlops
  maturity: stable
---

# GPU Accelerator Configuration Validation

## Purpose

[gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
covers building GPU infrastructure correctly; this skill covers verifying
that a *specific job's* configuration actually engages that infrastructure
before it runs. GPU scheduling on Kubernetes has an unusually large number
of small, independently-failing config surfaces — a missing
`resources.limits` block, a typo'd resource key (`nvidia.com/gpu` vs.
`nvidia.com/mig-1g.10gb`), a missing toleration, a CUDA version the job
image wasn't built against — and nearly all of them fail *silently*: the
pod still schedules, the container still starts, and the job still runs to
completion, just on the CPU (much slower) or against the wrong device
(possibly with wrong numerical results). There is rarely a Kubernetes-level
error to alert on. This skill is a pre-submit and in-job validation
checklist specifically aimed at catching that class of silent
misconfiguration before hours or days of compute are wasted.

## When to use

- Before submitting a new or changed training job spec, to confirm it will
  actually be scheduled onto and use a GPU rather than silently running on
  CPU.
- A training or serving job completed (or is running) suspiciously slowly,
  and the user wants to confirm whether it's actually using a GPU.
- Writing an admission-time policy (OPA/Gatekeeper, Kyverno, or a custom
  validating webhook) that rejects pods claiming to be GPU workloads but
  missing the resource fields that would make that true.
- Debugging a job that fails with a CUDA/driver version mismatch, an
  out-of-memory error on a MIG slice that's smaller than expected, or a
  multi-GPU job that only uses one device.
- Auditing an existing set of training/serving manifests for GPU
  configuration correctness after a platform change (driver upgrade, MIG
  profile change, node pool migration).

## Prerequisites & environment

- `kubectl` access to the cluster and namespace running the job, plus
  `nvidia-smi` access on the node or via `kubectl exec` into a running pod
  for direct GPU visibility.
- The GPU infrastructure from
  [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)
  already installed (device plugin, DCGM exporter) — this skill validates
  *against* that infrastructure, it doesn't install it.
  For OOM/crash-loop diagnosis on GPU nodes generally, also see
  [pod-crashloop-and-oom-troubleshooting](../../../kubernetes-platform/skills/pod-crashloop-and-oom-troubleshooting/SKILL.md).
- Framework-level GPU visibility inside the training/serving image
  (`torch.cuda.is_available()` for PyTorch, `tf.config.list_physical_devices('GPU')`
  for TensorFlow) to add in-job fail-fast checks.
- If enforcing validation via admission policy: OPA Gatekeeper or Kyverno
  already installed in the cluster — see
  [opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md).

## Step-by-step guidance

1. **Confirm the device plugin reports the resource the job requests, on
   the node the job would land on**, before looking at the job spec at
   all — a correct pod spec against a broken device plugin still fails
   silently:
   ```bash
   kubectl get nodes -o json \
     | jq '.items[] | {name:.metadata.name, gpu:.status.capacity["nvidia.com/gpu"], mig:.status.capacity | with_entries(select(.key|startswith("nvidia.com/mig")))}'
   ```
   If a node has a physical GPU but no `nvidia.com/gpu` or
   `nvidia.com/mig-*` capacity entry, the device plugin isn't healthy on
   that node — fix that first (see
   [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md))
   since no pod spec fix downstream will make the job actually use a GPU.

2. **Check that the resource key in the pod spec exactly matches what the
   cluster exposes.** This is the single most common silent-failure cause:
   ```yaml
   # WRONG — this key doesn't exist if the node exposes MIG slices, not
   # whole GPUs; the pod schedules onto a non-GPU-reserved slot and the
   # container runs on CPU with no error.
   resources:
     limits:
       nvidia.com/gpu: 1

   # CORRECT for a MIG-partitioned node pool
   resources:
     limits:
       nvidia.com/mig-1g.10gb: 1
   ```
   ```bash
   # Diff the pod's requested resource key against the node's actual capacity keys
   kubectl get pod <pod> -o jsonpath='{.spec.containers[*].resources.limits}'
   kubectl get node <node> -o jsonpath='{.status.capacity}' | jq 'with_entries(select(.key|startswith("nvidia.com")))'
   ```

3. **Verify the resource appears in `limits`, not only `requests` (or vice
   versa left empty).** Kubernetes device plugins are "limit-only"
   resources — a pod that sets `requests.nvidia.com/gpu: 1` but omits
   `limits` (or sets it to `0` by a templating bug) is **not guaranteed a
   GPU allocation at all** and can schedule onto a CPU-only node, silently
   running the training framework's CPU fallback path with no scheduling
   error:
   ```yaml
   # WRONG — no limits set; many Helm chart templates default resources.limits
   # to {} when a values override is missing, silently dropping the GPU claim
   resources:
     requests:
       cpu: "4"
       memory: 16Gi
   # correct: an explicit GPU limit, matching request
   resources:
     requests:
       cpu: "4"
       memory: 16Gi
     limits:
       nvidia.com/gpu: 1
   ```

4. **Verify tolerations match the node pool's taints exactly**, including
   `effect` — a toleration missing `effect: NoSchedule` or with a typo'd
   `value` silently fails to match, and the pod either stays `Pending`
   forever (visible) or, worse, schedules onto an *untainted* fallback
   node with no GPU at all (invisible):
   ```bash
   kubectl get node <gpu-node> -o jsonpath='{.spec.taints}'
   kubectl get pod <pod> -o jsonpath='{.spec.tolerations}'
   ```

5. **Add an in-job fail-fast assertion** as a second line of defense
   independent of the Kubernetes scheduling layer, so a job that somehow
   schedules onto a GPU node but can't actually initialize CUDA (driver/
   library mismatch) fails loudly in its first seconds instead of running
   to completion on CPU:
   ```python
   import torch, sys

   if not torch.cuda.is_available():
       print("FATAL: CUDA not available — refusing to silently train on CPU. "
             "Check device plugin health, resource limits, and driver/CUDA "
             "version compatibility.", file=sys.stderr)
       sys.exit(1)

   expected_gpus = int(os.environ.get("EXPECTED_GPU_COUNT", "1"))
   actual_gpus = torch.cuda.device_count()
   if actual_gpus != expected_gpus:
       print(f"FATAL: expected {expected_gpus} GPUs, torch sees {actual_gpus}. "
             "Check multi-GPU scheduling and NCCL/device visibility env vars.",
             file=sys.stderr)
       sys.exit(1)
   ```
   This check costs a few seconds and turns a multi-hour silent CPU run
   into an immediate, loud job failure — treat it as a required guard in
   every training entrypoint, not optional boilerplate.

6. **Confirm the container image's CUDA toolkit version is compatible
   with the node's installed driver**, since a version mismatch can
   manifest as either an outright crash or, on some driver/toolkit
   combinations, a silent fallback to a slower or CPU-only code path:
   ```bash
   # Driver version on the node
   kubectl exec -it <pod> -- nvidia-smi --query-gpu=driver_version --format=csv
   # CUDA toolkit baked into the image
   kubectl exec -it <pod> -- nvcc --version
   ```
   Cross-check both against the NVIDIA driver/CUDA compatibility table
   before assuming a mismatch is fine — newer drivers are usually backward
   compatible with older CUDA toolkits, but the reverse is not guaranteed.

7. **Enforce this as an admission-time policy for GPU-labeled workloads**,
   so misconfiguration is rejected before it ever reaches the scheduler,
   rather than relying on every job author remembering the checklist above:
   ```yaml
   # Kyverno ClusterPolicy: any pod labeled workload-type=gpu-training must
   # declare a GPU-family resource limit
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: require-gpu-resource-limit
   spec:
     validationFailureAction: Enforce
     rules:
       - name: require-gpu-limit-for-gpu-workloads
         match:
           any:
             - resources:
                 kinds: [Pod]
                 selector:
                   matchLabels:
                     workload-type: gpu-training
         validate:
           message: "Pods labeled workload-type=gpu-training must set a nvidia.com/gpu or nvidia.com/mig-* resource limit."
           deny:
             conditions:
               all:
                 - key: "{{ request.object.spec.containers[].resources.limits.keys(@)[?contains(@, 'nvidia.com')] || [] | length(@) }}"
                   operator: Equals
                   value: 0
   ```
   This turns "the pipeline author forgot the GPU resource block" from a
   silent, expensive CPU run into an immediate admission rejection with a
   clear message.

## Best practices

- Never treat "the job finished without a Kubernetes-level error" as
  evidence it used a GPU — the failure modes here are specifically the
  ones that don't produce scheduler or container errors.
- Validate at three independent layers: admission-time policy (catches bad
  manifests before scheduling), the in-job fail-fast assertion (catches
  runtime CUDA/driver issues the scheduler can't see), and post-hoc
  monitoring on `DCGM_FI_DEV_GPU_UTIL` for the pod (catches a job that got
  a GPU allocation but isn't actually using it, e.g. a data-loading
  bottleneck or a code path that never calls `.cuda()`).
- Keep a single source of truth for the resource key naming convention
  (`nvidia.com/gpu` for whole GPUs, `nvidia.com/mig-<profile>` for MIG
  slices) documented alongside the node pool labels from
  [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md),
  so job authors aren't guessing the exact string.
- Bake the in-job fail-fast GPU assertion into a shared base training image
  or entrypoint script rather than leaving it to each job author to
  remember — configuration discipline that depends on everyone
  remembering a step will eventually be skipped.
- Alert on GPU allocation without GPU utilization (a pod holding
  `nvidia.com/gpu: 1` with `DCGM_FI_DEV_GPU_UTIL` near zero for more than a
  few minutes past job startup) as its own signal, separate from job
  failure alerts — this catches jobs that "work" but aren't actually using
  the expensive resource they're holding.
- Version-pin the base training/serving image's CUDA toolkit and document
  the driver version range it's validated against, and re-validate that
  pairing explicitly whenever the platform team upgrades node drivers.

## Common pitfalls

- **Symptom:** A training job runs for the expected wall-clock duration of
  a CPU run (much longer than a GPU run would take) and completes with a
  plausible-looking loss curve; nobody notices until someone compares
  timing against a previous run.
  **Warning:** This is the core dangerous case this skill exists for — a
  job silently falling back to CPU produces no error and no alert, just
  wasted compute budget and a delayed result. Treat any GPU-labeled job
  without an in-job fail-fast CUDA assertion as unvalidated and at risk of
  this failure mode, and add GPU-utilization alerting rather than relying
  on someone noticing run duration by eye.
  **Fix:** Add the in-job `torch.cuda.is_available()` (or framework
  equivalent) assertion from step 5, plus admission-time enforcement from
  step 7, plus a utilization-based alert — layer all three since each
  catches a different failure path.

- **Symptom:** A pod requests `nvidia.com/gpu: 1` but the node pool was
  reconfigured for MIG partitioning last week; the pod stays `Pending`
  indefinitely with no obvious reason in `kubectl describe pod`.
  **Fix:** Check `kubectl describe node <node>` for the actual resource
  keys currently advertised — a MIG-enabled node no longer advertises
  `nvidia.com/gpu` at all, only `nvidia.com/mig-<profile>` keys. Update the
  job spec to request the matching MIG resource key, and communicate MIG
  layout changes to job authors before rolling them out.

- **Symptom:** A multi-GPU distributed training job only uses one GPU
  despite requesting `nvidia.com/gpu: 4`, with no error.
  **Fix:** Check the training framework's distributed launch configuration
  (`torchrun --nproc_per_node`, `CUDA_VISIBLE_DEVICES`, or the framework's
  device-count detection) separately from the Kubernetes resource request —
  Kubernetes correctly allocating 4 GPU devices to a pod does not
  automatically make a training script use more than one of them; that's
  a framework-level distributed launch concern, not a scheduling one.

- **Symptom:** A job that worked fine last month now crashes immediately
  with a CUDA driver/library version mismatch error after a platform-wide
  driver upgrade.
  **Fix:** Roll driver upgrades to a canary GPU node pool first (per
  [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md)'s
  best practices) and validate the existing fleet of training/serving
  images' CUDA toolkit versions against the new driver before a
  cluster-wide rollout, rather than discovering incompatibility from a
  production job crash.

- **Symptom:** An admission policy correctly requires a
  `nvidia.com/gpu`-family limit on GPU-labeled pods, but a job author works
  around it by simply removing the `workload-type: gpu-training` label
  from their pod spec, and the (still GPU-intended) job now silently runs
  on CPU with no policy check applied at all.
  **Fix:** Don't rely solely on a workload-shaped label the job author
  controls as the enforcement trigger; also add a monitoring-side check
  independent of pod labels — e.g. alert when a container image known to
  be a GPU-training image is running on a node with no GPU resource
  allocation, using image name/tag as the trigger instead of a
  self-reported label.

## Worked example

**Scenario:** A data scientist copies an existing training Job manifest to
start a new fine-tuning run, but the copy-paste drops the `resources.limits`
block while keeping `resources.requests` (a common templating mistake when
overriding only some Helm values). Validate it before submission.

Submitted manifest (broken):
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: finetune-run-2026-07-28
  labels:
    workload-type: gpu-training
spec:
  template:
    spec:
      nodeSelector:
        gpu-pool: training
      tolerations:
        - {key: workload, operator: Equal, value: training, effect: NoSchedule}
      containers:
        - name: trainer
          image: registry.internal/finetune:2.4.0
          resources:
            requests:
              cpu: "8"
              memory: 32Gi
              nvidia.com/gpu: 1
            # limits block missing — templating bug dropped it
      restartPolicy: Never
```

Pre-submit validation catches it two ways:

1. **Admission policy** (step 7) rejects the manifest outright:
   `Pods labeled workload-type=gpu-training must set a nvidia.com/gpu or
   nvidia.com/mig-* resource limit.` — submission fails immediately with a
   clear message, no compute spent.

2. If the policy weren't in place, the pod **would schedule** — Kubernetes
   only strictly enforces device-plugin resources via `limits`, so a
   `requests`-only GPU key is not a guaranteed allocation — and the
   in-job assertion (step 5) baked into the training entrypoint fires
   within seconds:
   ```
   FATAL: CUDA not available — refusing to silently train on CPU. Check
   device plugin health, resource limits, and driver/CUDA version
   compatibility.
   ```
   instead of the job running for the next several hours on CPU
   undetected.

Corrected manifest adds the missing `limits`:
```yaml
          resources:
            requests:
              cpu: "8"
              memory: 32Gi
              nvidia.com/gpu: 1
            limits:
              nvidia.com/gpu: 1
```

## Cross-references

- [gpu-accelerator-infrastructure-for-ml-training](../gpu-accelerator-infrastructure-for-ml-training/SKILL.md) — the infrastructure layer (device plugin, MIG, node pools) this skill validates a specific job's config against.
- [training-pipeline-orchestration](../training-pipeline-orchestration/SKILL.md) — where GPU resource requests should be templated consistently across pipeline steps rather than hand-copied per job.
- [kubeflow-ml-pipeline-orchestration](../kubeflow-ml-pipeline-orchestration/SKILL.md) and [ray-distributed-ml-orchestration](../ray-distributed-ml-orchestration/SKILL.md) — orchestrators whose component/task GPU resource declarations should be validated with this checklist before a pipeline run.
- [pod-crashloop-and-oom-troubleshooting](../../../kubernetes-platform/skills/pod-crashloop-and-oom-troubleshooting/SKILL.md) — general Kubernetes pod failure diagnosis, complementary when a GPU pod fails outright rather than silently falling back.
- [opa-gatekeeper-policy-authoring](../../../policy-and-governance-tooling/skills/opa-gatekeeper-policy-authoring/SKILL.md) — authoring the admission-time policies referenced in step 7 as OPA/Rego instead of Kyverno.
