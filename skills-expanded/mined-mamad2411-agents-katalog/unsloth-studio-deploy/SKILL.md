---
name: unsloth-studio-deploy
description: Deploy Unsloth Studio on a Civo Helios Kubernetes cluster with B200 GPUs. User provides their kubeconfig file and the skill handles GPU enablement, namespace creation, storage provisioning, and Unsloth Studio deployment automatically. Triggers when user mentions Helios, Unsloth, GPU finetuning on Kubernetes, or drops a kubeconfig file.
---

# Deploy Unsloth Studio on Helios B200 GPUs

This skill automates the full deployment of Unsloth Studio on a Civo Helios Kubernetes cluster with NVIDIA B200 GPUs.

## When to Use This Skill

Use this skill when the user:

- Wants to deploy Unsloth Studio on Kubernetes
- Mentions Helios, Civo, or B200 GPUs
- Provides or mentions a kubeconfig file for a GPU cluster
- Asks about finetuning LLMs on Kubernetes
- Wants to set up a GPU training environment

## Prerequisites

The user needs:
1. A Civo Helios kubeconfig file (downloaded from Civo dashboard)
2. `kubectl` installed locally
3. Network access to the cluster API endpoint

## Step-by-Step Execution

When triggered, follow these steps IN ORDER. Do not skip steps. Report progress after each step.

### Step 0: Locate the Kubeconfig

Ask the user for their kubeconfig file path if not already provided. Verify it exists:

```bash
ls -la <kubeconfig-path>
```

Extract and confirm the API endpoint:

```bash
grep "server:" <kubeconfig-path>
```

Set the KUBECONFIG for all subsequent commands:

```bash
export KUBECONFIG="<kubeconfig-path>"
```

### Step 1: Preflight Checks

Run all checks and report results as a table:

```bash
# Cluster connectivity
kubectl cluster-info

# Node details
kubectl get nodes -o wide

# Check GPU instance type
kubectl get nodes -o jsonpath='{.items[*].metadata.labels.node\.kubernetes\.io/instance-type}'

# Check existing GPU resources
kubectl describe nodes | grep -A5 "nvidia.com/gpu"

# Check storage classes
kubectl get storageclass

# Check existing pods
kubectl get pods -A
```

**Expected results:**
- Cluster responds
- Node shows Alpine Linux with B200 instance type (e.g. `an.g1.b200sxm.kube.x8`)
- Storage class `civo-volume` exists (default)

**If GPUs are NOT listed in node capacity**, proceed to Step 2. Otherwise skip to Step 3.

### Step 2: Install NVIDIA Device Plugin

Helios uses Alpine-based GPU nodes that require a standalone NVIDIA device plugin.

**IMPORTANT:** Get the exact instance type from Step 1 and use it in the DaemonSet manifest.

Create and apply the DaemonSet:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nvidia-device-plugin-daemonset
  namespace: default
spec:
  selector:
    matchLabels:
      name: nvidia-device-plugin-ds
  updateStrategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        name: nvidia-device-plugin-ds
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node.kubernetes.io/instance-type
                operator: In
                values:
                - <INSTANCE_TYPE_FROM_STEP_1>
      runtimeClassName: nvidia
      tolerations:
      - key: nvidia.com/gpu
        operator: Exists
        effect: NoSchedule
      priorityClassName: "system-node-critical"
      containers:
      - image: nvcr.io/nvidia/k8s-device-plugin:v0.17.1
        name: nvidia-device-plugin-ctr
        env:
          - name: DEVICE_DISCOVERY_STRATEGY
            value: "nvml"
          - name: FAIL_ON_INIT_ERROR
            value: "false"
        volumeMounts:
        - name: nvidia-driver
          mountPath: /usr/lib/x86_64-linux-gnu
        - name: device-plugin
          mountPath: /var/lib/kubelet/device-plugins
      volumes:
      - name: nvidia-driver
        hostPath:
          path: /usr/local/glibc
          type: Directory
      - name: device-plugin
        hostPath:
          path: /var/lib/kubelet/device-plugins
```

Apply and verify:

```bash
kubectl apply -f helios-nvidia-device-plugin.yaml

# Wait for plugin to be running
kubectl get pods -l name=nvidia-device-plugin-ds -w

# Verify GPUs are registered (wait ~30 seconds)
kubectl describe node | grep "nvidia.com/gpu"
```

**Success criteria:** `nvidia.com/gpu: N` appears under both Capacity and Allocatable.

### Step 3: Run GPU Verification

Deploy a test pod to confirm nvidia-smi works:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-verification-pod
spec:
  runtimeClassName: nvidia
  restartPolicy: Never
  tolerations:
    - key: "nvidia.com/gpu"
      operator: "Exists"
      effect: "NoSchedule"
  containers:
  - name: cuda-container
    image: nvcr.io/nvidia/cuda:12.4.1-base-ubuntu22.04
    command: ["nvidia-smi"]
    resources:
      limits:
        nvidia.com/gpu: 1
    env:
    - name: NVIDIA_VISIBLE_DEVICES
      value: all
```

```bash
kubectl apply -f gpu-verification-pod.yaml
# Wait for completion
kubectl get pod gpu-verification-pod -w
# Check output
kubectl logs gpu-verification-pod
# Clean up
kubectl delete pod gpu-verification-pod
```

**Report to user:** GPU model, count, VRAM per GPU, total VRAM, driver version, CUDA version.

### Step 4: Deploy Unsloth Studio

Apply three manifests in order:

**namespace.yaml:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: unsloth
  labels:
    app.kubernetes.io/part-of: unsloth-studio
```

**pvc.yaml:**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: unsloth-workspace
  namespace: unsloth
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
```

**studio-pod.yaml:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: unsloth-studio
  namespace: unsloth
  labels:
    app: unsloth-studio
spec:
  runtimeClassName: nvidia
  tolerations:
    - key: "nvidia.com/gpu"
      operator: "Exists"
      effect: "NoSchedule"
  containers:
  - name: studio
    image: unsloth/unsloth
    env:
    - name: NVIDIA_VISIBLE_DEVICES
      value: all
    - name: JUPYTER_PASSWORD
      value: "unsloth-demo"
    ports:
    - containerPort: 8888
      name: jupyter
    - containerPort: 8000
      name: api
    resources:
      limits:
        nvidia.com/gpu: 1
      requests:
        nvidia.com/gpu: 1
        cpu: "4"
        memory: "32Gi"
    volumeMounts:
    - name: workspace
      mountPath: /workspace/work
    - name: shm
      mountPath: /dev/shm
  volumes:
  - name: workspace
    persistentVolumeClaim:
      claimName: unsloth-workspace
  - name: shm
    emptyDir:
      medium: Memory
      sizeLimit: 16Gi
  restartPolicy: Never
```

**CRITICAL NOTES for the pod spec:**
- `runtimeClassName: nvidia` — REQUIRED for Helios Alpine nodes
- `/dev/shm` as 16Gi memory-backed emptyDir — WITHOUT THIS, PyTorch will crash with `Bus error`
- `NVIDIA_VISIBLE_DEVICES=all` — makes all GPUs visible for optional DDP

```bash
kubectl apply -f namespace.yaml
kubectl apply -f pvc.yaml
kubectl apply -f studio-pod.yaml

# Watch pod progress (image is ~19GB, first pull takes 7-8 minutes)
kubectl -n unsloth get pod unsloth-studio -w
```

### Step 5: Verify and Connect

Once pod shows `Running`:

```bash
# Verify GPU inside pod
kubectl -n unsloth exec unsloth-studio -- nvidia-smi --query-gpu=name,memory.total --format=csv

# Check running services
kubectl -n unsloth exec unsloth-studio -- ps aux | grep -E "(jupyter|run.py)"

# Port forward
kubectl -n unsloth port-forward pod/unsloth-studio 8888:8888 8000:8000
```

**Tell the user:**

> Unsloth Studio is ready!
>
> - **Studio UI**: http://localhost:8000
> - **JupyterLab**: http://localhost:8888 (password: unsloth-demo)
>
> **Quick-start finetuning:**
> 1. Open http://localhost:8000
> 2. Create a password
> 3. Select a model (try `unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit` or `unsloth/Qwen3.5-9B`)
> 4. Select a dataset (try `yahma/alpaca-cleaned`)
> 5. Set 60 steps, QLoRA, and hit Start Training
> 6. Watch the loss drop in real-time

### Step 6 (Optional): Multi-GPU DDP Job

If the user wants to use all GPUs for a larger training run:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: unsloth-ddp-training
  namespace: unsloth
spec:
  backoffLimit: 0
  template:
    spec:
      runtimeClassName: nvidia
      tolerations:
        - key: "nvidia.com/gpu"
          operator: "Exists"
          effect: "NoSchedule"
      containers:
      - name: trainer
        image: unsloth/unsloth
        env:
        - name: NVIDIA_VISIBLE_DEVICES
          value: all
        command: ["torchrun"]
        args:
        - "--nproc_per_node=<NUM_GPUS>"
        - "unsloth-cli.py"
        - "--model_name=<MODEL>"
        - "--dataset=<DATASET>"
        - "--max_seq_length=4096"
        - "--load_in_4bit"
        - "--per_device_train_batch_size=1"
        - "--gradient_accumulation_steps=4"
        - "--max_steps=100"
        - "--learning_rate=2e-5"
        - "--save_model"
        resources:
          limits:
            nvidia.com/gpu: <NUM_GPUS>
          requests:
            nvidia.com/gpu: <NUM_GPUS>
            cpu: "32"
            memory: "128Gi"
        volumeMounts:
        - name: workspace
          mountPath: /workspace/work
        - name: shm
          mountPath: /dev/shm
      volumes:
      - name: workspace
        persistentVolumeClaim:
          claimName: unsloth-workspace
      - name: shm
        emptyDir:
          medium: Memory
          sizeLimit: 64Gi
      restartPolicy: Never
```

## Cleanup

When the user is done:

```bash
kubectl -n unsloth delete pod unsloth-studio
kubectl -n unsloth delete job --all
kubectl -n unsloth delete pvc unsloth-workspace   # WARNING: deletes saved models
kubectl delete namespace unsloth
kubectl delete daemonset nvidia-device-plugin-daemonset
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Pod stuck in `Pending` | No GPU available | `kubectl -n unsloth describe pod unsloth-studio` — check Events |
| Pod `CrashLoopBackOff` | CUDA driver mismatch or missing runtimeClassName | Verify `runtimeClassName: nvidia` is set |
| `Bus error` during training | `/dev/shm` too small | Ensure the shm emptyDir volume is mounted with `medium: Memory` |
| PVC stuck in `Pending` | No StorageClass | Check `kubectl get storageclass`; Civo default is `civo-volume` |
| Image pull slow/failing | 19GB image, network issues | Wait longer or pre-pull with a separate pod |
| `i/o timeout` on kubectl | Wrong kubeconfig or VPN needed | Verify API endpoint matches cluster dashboard |
| Port-forward drops | Network interruption | Re-run the port-forward command |

## Model Recommendations by GPU Memory

| VRAM Available | Model | Method |
|----------------|-------|--------|
| 183 GB (1x B200) | Any model up to 70B | QLoRA 4-bit |
| 183 GB (1x B200) | Up to 40B | Full finetune |
| 1.43 TB (8x B200) | Up to 405B | QLoRA 4-bit (sharded) |
| 1.43 TB (8x B200) | Up to 70B | Full finetune |
