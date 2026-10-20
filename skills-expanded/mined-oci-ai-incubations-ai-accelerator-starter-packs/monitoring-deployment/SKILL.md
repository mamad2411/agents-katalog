---
name: monitoring-deployment
description: >-
  Continuously polls ORM job status and logs, scans cluster health across all
  namespaces (nodes, pods, PVCs, Helm releases), and reports structured status
  tables. Checks everything every cycle, not just errors. Use when monitoring a
  running deployment or when the user says "check what is running" or "monitor
  the deploy."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Edit
  - AskUserQuestion
  - Glob
argument-hint: "[cluster-ocid] [job-or-stack-ocid]"
---

# Monitoring Deployment

Continuous cluster health scanner that polls ORM job status and scans all namespaces every cycle.

---

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| cluster-ocid | No | OKE cluster OCID. Asked if not provided. |
| job-or-stack-ocid | No | ORM job or stack OCID. Asked if not provided. If a stack OCID is given, the latest active job is resolved automatically. |

If arguments are missing, ask the user for:
1. **Cluster OCID** (`ocid1.cluster...`)
2. **ORM job or stack OCID** (`ocid1.ormjob...` or `ocid1.ormstack...`)
3. **Region** (default: `us-sanjose-1`)
4. **OCI CLI profile** (default: `SANJOSE`)

---

## Phase 1: Connect to Cluster

Generate kubeconfig and patch it with the OCI CLI profile. Follow the exact procedure in `references/kubeconfig-patching.md`.

```bash
export OCI_CLI_PROFILE=<PROFILE>

oci ce cluster create-kubeconfig \
  --cluster-id <CLUSTER_OCID> \
  --file ~/.kube/config \
  --region <REGION> \
  --token-version 2.0.0 \
  --kube-endpoint PUBLIC_ENDPOINT \
  --profile <PROFILE>

# Patch kubeconfig with profile
sed -i '' "s/      env: \[\]/      - --profile\n      - <PROFILE>\n      env: []/" ~/.kube/config
```

Verify with `kubectl get nodes`. If this fails, stop and troubleshoot before entering the poll loop.

---

## Phase 2: Resolve ORM Job

If the user provided a **stack OCID**, resolve the latest active job:

```bash
oci resource-manager job list \
  --stack-id <STACK_OCID> \
  --sort-by TIME_CREATED \
  --sort-order DESC \
  --limit 1 \
  --profile <PROFILE> \
  --region <REGION> \
  --query 'data[0].id' \
  --raw-output
```

Store the job OCID for polling. Also capture the job operation type (APPLY, PLAN, DESTROY).

---

## Phase 3: Poll Cycle

Run the following checks **every 30 seconds**. Report ALL results every cycle, not just errors.

### 3.1 ORM Job Status + Logs

```bash
# Job status
oci resource-manager job get \
  --job-id <JOB_OCID> \
  --profile <PROFILE> \
  --region <REGION> \
  --query 'data.{"status": "lifecycle-state", "operation": operation, "percent": "percent-complete"}' 2>/dev/null

# Log tail (last 50 lines)
oci resource-manager job get-job-logs \
  --job-id <JOB_OCID> \
  --profile <PROFILE> \
  --region <REGION> \
  --limit 50 \
  --sort-order DESC \
  --query 'data[].message' 2>/dev/null
```

**Log filtering rules:**
- Suppress repeated "Still creating..." / "Still destroying..." lines. Show the first occurrence and then only when the resource name changes.
- Always surface: `Creation complete`, `Destruction complete`, `Error:`, `Apply complete!`, `Destroy complete!`.
- Show resource creation/destruction completions as they appear.

### 3.2 Instance Pool Work Requests (during infra apply)

If the ORM logs show `instance_pool` or `cluster_network` is "Still creating...", check the instance pool work requests for GPU capacity failures. These errors don't surface in Terraform logs until the timeout — work requests reveal them immediately.

```bash
# List instance pools in the compartment
export OCI_CLI_PROFILE=<PROFILE>
oci compute-management instance-pool list \
  --compartment-id <COMPARTMENT_OCID> \
  --region <REGION> \
  --lifecycle-state PROVISIONING \
  --query 'data[].{id:id,state:"lifecycle-state",size:size}' \
  --output table 2>/dev/null

# Get work requests for each provisioning instance pool
oci work-requests work-request list \
  --compartment-id <COMPARTMENT_OCID> \
  --resource-id <INSTANCE_POOL_OCID> \
  --query 'data[].{id:id,status:status,"percent-complete":"percent-complete",started:"time-started"}' \
  --output table 2>/dev/null

# If any work request has FAILED status, get the error details
oci work-requests work-request-error list \
  --work-request-id <WORK_REQUEST_OCID> \
  --query 'data[].{code:code,message:message}' \
  --output table 2>/dev/null
```

Common failure: `Out of host capacity` (InternalError 500) — means no GPU bare-metal hosts available in the region/AD. Report immediately — don't wait for Terraform timeout.

### 3.3 Node Health

```bash
kubectl get nodes -o wide --no-headers 2>/dev/null
```

Report: total nodes, Ready count, NotReady count. Flag any node in NotReady/SchedulingDisabled state.

### 3.4 Pod Status — All Namespaces

```bash
kubectl get pods -A --no-headers 2>/dev/null
```

Classify every pod into one of these buckets:
- **Running** — STATUS is Running, all containers ready (READY column N/N)
- **Running (not ready)** — STATUS is Running but READY column shows containers not yet ready
- **Pending** — STATUS is Pending
- **CrashLoopBackOff** — STATUS contains CrashLoopBackOff
- **Init** — STATUS contains Init or PodInitializing
- **Completed** — STATUS is Completed (jobs/hooks, normal)
- **Failed/Error** — STATUS is Error, Failed, OOMKilled, or ImagePullBackOff
- **Terminating** — STATUS is Terminating

Count pods per bucket. List individual pods only for non-healthy states (Pending, CrashLoopBackOff, Failed/Error).

### 3.4 Pending Pod Investigation

For each Pending pod (max 5):

```bash
kubectl describe pod <POD> -n <NAMESPACE> 2>/dev/null | grep -A 20 "^Events:"
```

Extract the reason from Events (e.g., Unschedulable, FailedScheduling, insufficient GPU). Report the most recent event message.

### 3.5 CrashLoopBackOff Investigation

For each CrashLoopBackOff pod (max 5):

```bash
kubectl logs <POD> -n <NAMESPACE> --tail=20 2>/dev/null
```

Report the last 20 lines. If the pod has multiple containers, check the one that is crash-looping:

```bash
kubectl get pod <POD> -n <NAMESPACE> -o jsonpath='{.status.containerStatuses[?(@.state.waiting)].name}' 2>/dev/null
```

### 3.6 PVC/PV Status

```bash
kubectl get pvc -A --no-headers 2>/dev/null
```

Flag any PVC not in Bound state. Report total count and any Pending PVCs with their namespace and claim name.

### 3.7 Helm Release Status

```bash
helm list -A --no-headers 2>/dev/null
```

Flag any release not in `deployed` status. Report releases in `failed`, `pending-install`, `pending-upgrade`, or `uninstalling` states with their namespace.

---

## Output Format

After each poll cycle, output a structured status block:

```
================================================================================
DEPLOYMENT MONITOR — Cycle #N — HH:MM:SS
================================================================================

ORM JOB: <status> (<operation>) [<percent>%]
  Last log: <most recent meaningful log line>

NODES: <ready>/<total> Ready
  [Issues: <node-name> NotReady, ...]

PODS:
  Running:          NN
  Running (partial): NN
  Pending:          NN   <-- pod-name (reason)
  CrashLoop:        NN   <-- pod-name (last log line)
  Init:             NN
  Completed:        NN
  Failed/Error:     NN   <-- pod-name (status)
  Terminating:      NN

PVC: <bound>/<total> Bound
  [Pending: <namespace>/<pvc-name>, ...]

HELM: <deployed>/<total> Deployed
  [Issues: <release> in <namespace> — <status>]

HEALTHY NAMESPACES: <comma-separated list of namespaces where all pods are Running/Completed>

ISSUES SUMMARY:
  - <issue 1>
  - <issue 2>
  [or] No issues detected.

STABILITY: <N>/2 consecutive clean cycles
================================================================================
```

### Between Cycles

Print a single line: `Next poll in 30s... (Ctrl+C to stop)`

Then wait 30 seconds before the next cycle. Use `sleep 30`.

---

## Termination Conditions

The monitor exits automatically when ALL of:
1. ORM job is in a terminal state: `SUCCEEDED`, `FAILED`, `CANCELED`
2. All pods are Running (ready), Completed, or expected system pods for **2 consecutive cycles**
3. No Pending PVCs
4. No failed/pending-install Helm releases

### On Success (ORM SUCCEEDED + cluster stable)

```
================================================================================
DEPLOYMENT COMPLETE — All checks passing
================================================================================
ORM job SUCCEEDED. Cluster stable for 2 cycles.
Total time monitored: X minutes.

Ready for testing. Suggested next steps:
  /deploy-and-test   — run pack-specific API + UI tests
  /kubectl            — interactive cluster inspection
================================================================================
```

### On Failure (ORM FAILED or CANCELED)

```
================================================================================
DEPLOYMENT FAILED
================================================================================
ORM job <status>.
Last error from logs: <error line>

Suggested next steps:
  /diagnosing-stack   — investigate the failure
  /destroy-stack      — clean up resources
================================================================================
```

### On User Interrupt

If the user says "stop", "quit", or otherwise interrupts, print the current status one final time and exit cleanly.

---

## Error Handling

- **kubectl not connected:** If `kubectl get nodes` fails at any point during the poll loop, log the error and retry next cycle. Do not abort — the cluster may still be provisioning.
- **ORM CLI errors:** If `oci resource-manager` commands fail, log the error and continue polling cluster state. The job may have already completed.
- **Helm not installed or no releases:** If `helm list` fails or returns empty, note "No Helm releases found" and continue. Helm releases appear after ORM apply progresses past the Helm resources.
- **Transient errors:** Any single check failure should not stop the loop. Log the error inline and continue to the next check.

---

## Notes

- This skill checks EVERYTHING every cycle. Do not skip checks because previous cycles were clean.
- Pod classification must cover ALL pods in ALL namespaces, including kube-system and OKE system pods.
- The 2-cycle stability requirement prevents premature "complete" signals when pods are still churning.
- If the cluster OCID is not yet known (infrastructure stack still creating OKE), ask the user to provide it once available, or poll the ORM job logs for the cluster OCID.
