---
name: diagnosing-stack
description: Investigates failed ORM stack deployments by analyzing job logs, cluster state, pod events, and Helm releases. Maps errors to known patterns with specific recommended fixes. Reports only, never acts autonomously. Use when a stack apply failed or when the user says 'why did this fail' or 'diagnose this stack.'
user-invocable: true
allowed-tools: Bash, Read, Edit, AskUserQuestion, Glob
argument-hint: <stack-ocid-or-name> [region]
---

# Diagnose Stack

Investigate a failed ORM stack deployment. Analyze logs, cluster state, and error patterns. **Report findings only — never take corrective action.**

---

## Arguments

- `$0` (required) — ORM stack OCID or display name
- `$1` (optional) — OCI region (default: `us-sanjose-1`)

Also ask the user for:
- **Compartment** — name or OCID. If name given, resolve with: `oci iam compartment list --compartment-id-in-subtree true --all --query "data[?name=='<name>'].id | [0]" --raw-output`
- **OCI CLI profile** — check available profiles: `grep '^\[' ~/.oci/config`

Set these early and reuse throughout:

```bash
export OCI_CLI_PROFILE=<profile>
REGION=<region>
COMPARTMENT_OCID=<compartment-ocid>
STACK_ID=<stack-ocid>
```

---

## Key Principle

**This skill is read-only.** It investigates and reports. It never runs `helm uninstall`, `kubectl delete`, `oci resource-manager job create-*`, or any other mutating command. All recommendations go in the output report for the user to decide.

---

## Phase 1: Stack State Assessment

### Step 1a: Resolve stack OCID

If the user provided a display name instead of an OCID:

```bash
oci resource-manager stack list \
  -c $COMPARTMENT_OCID \
  --region $REGION \
  --all \
  --query "data[?contains(\"display-name\", '<name>')].{id:id, name:\"display-name\", state:\"lifecycle-state\"}" \
  --output table
```

### Step 1b: Get stack details

```bash
oci resource-manager stack get --stack-id $STACK_ID --region $REGION
```

Record: display name, lifecycle state, Terraform version, last updated time, variables (look for `starter_pack_category`, `deploy_infrastructure`, `deploy_application`).

### Step 1c: List jobs

```bash
oci resource-manager job list \
  --stack-id $STACK_ID \
  --region $REGION \
  --all \
  --sort-by timeCreated \
  --sort-order DESC \
  --query "data[*].{id:id, operation:operation, state:\"lifecycle-state\", created:\"time-created\"}" \
  --output table
```

Find the most recent job with `lifecycle-state` = `FAILED`. If no failed jobs exist, report the stack as healthy and exit.

Record the failed job OCID for Phase 2.

---

## Phase 2: ORM Job Log Analysis

### Step 2a: Get job logs

```bash
FAILED_JOB_ID=<job-ocid>

oci resource-manager job get-job-logs \
  --job-id $FAILED_JOB_ID \
  --region $REGION \
  --all
```

### Step 2b: Extract error information

Scan the logs for:

1. **Error lines** — lines containing `Error:`, `error:`, `FAILED`, `failed`
2. **Failed resource** — the Terraform resource address (e.g., `oci_database_autonomous_database.oracle_26ai[0]`)
3. **Error message** — the OCI/Terraform error text
4. **File and line** — the `.tf` file and line number if reported
5. **Error code** — OCI error codes like `400-InvalidParameter`, `404-NotAuthorizedOrNotFound`, `500-InternalError`

Also look for:
- `Plan: X to add, Y to change, Z to destroy` — what was the plan scope?
- `Apply complete! Resources: X added` — how far did apply get before failing?
- Warnings about deprecated attributes or provider issues

### Step 2c: Check for Terraform state issues

Look in logs for:
- `Error acquiring the state lock` — another job may be running
- `Error loading state` — state corruption
- `Resource already exists` — resource was created outside Terraform

---

## Phase 3: Cluster Investigation

**Only proceed if:** the stack deployed an OKE cluster (check `deploy_infrastructure` variable or look for cluster resources in the logs).

### Step 3a: Find the cluster OCID

From the job logs or stack outputs:

```bash
oci resource-manager job get-job-logs \
  --job-id $FAILED_JOB_ID \
  --region $REGION \
  --all \
  --query "data[?contains(message, 'cluster')].message"
```

Or list OKE clusters in the compartment:

```bash
oci ce cluster list \
  -c $COMPARTMENT_OCID \
  --region $REGION \
  --all \
  --query "data[?\"lifecycle-state\"=='ACTIVE'].{id:id, name:name}" \
  --output table
```

### Step 3b: Get kubeconfig

Generate and patch the kubeconfig. Reference `references/kubeconfig-patching.md` for the full procedure.

```bash
CLUSTER_OCID=<cluster-ocid>
KUBECONFIG_FILE="$HOME/.kube/config-diag-$(date +%s)"

oci ce cluster create-kubeconfig \
  --cluster-id $CLUSTER_OCID \
  --file $KUBECONFIG_FILE \
  --region $REGION \
  --token-version 2.0.0 \
  --kube-endpoint PUBLIC_ENDPOINT \
  --profile $OCI_CLI_PROFILE
```

Patch the kubeconfig to add `--profile` args (see `references/kubeconfig-patching.md`), then:

```bash
export KUBECONFIG=$KUBECONFIG_FILE
```

Verify connectivity:

```bash
kubectl get nodes
```

If connectivity fails, record the error and skip to Phase 4 (log-only diagnosis).

### Step 3c: Node status

```bash
kubectl get nodes -o wide
kubectl top nodes 2>/dev/null || echo "Metrics server not available"
```

Check for:
- Nodes in `NotReady` state
- GPU nodes present (look for `nvidia.com/gpu` in labels)
- Node resource pressure (MemoryPressure, DiskPressure, PIDPressure)

### Step 3d: Pod status (all namespaces)

```bash
kubectl get pods -A -o wide
```

Identify pods NOT in `Running` or `Completed` state. For each failing pod:

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --tail=100
kubectl logs <pod-name> -n <namespace> --previous --tail=100 2>/dev/null
```

### Step 3e: PVC status

```bash
kubectl get pvc -A
```

Check for PVCs in `Pending` state. For pending PVCs:

```bash
kubectl describe pvc <pvc-name> -n <namespace>
```

### Step 3f: Helm releases

```bash
helm list -A --all
```

Check for releases in `failed`, `pending-install`, or `pending-upgrade` state.

For failed releases:

```bash
helm status <release-name> -n <namespace>
helm history <release-name> -n <namespace>
```

### Step 3g: Recent events

```bash
kubectl get events -A --sort-by='.lastTimestamp' | tail -50
```

Look for `Warning` events, especially:
- `FailedScheduling`
- `FailedMount`
- `BackOff` (image pull or crash loop)
- `ProvisioningFailed`

### Step 3h: Node resource allocation

For each node (especially GPU nodes):

```bash
kubectl describe nodes | grep -A 20 "Allocated resources"
```

---

## Phase 4: Error Matching

Read the error catalog:

```
references/error-catalog.md
```

Match the errors found in Phase 2 and Phase 3 against known patterns. For each match, record:
- The pattern matched
- The catalog's root cause
- The catalog's recommended fix
- Any additional context from this specific failure

If no catalog match is found, note the error as **UNKNOWN PATTERN** and include the full error text for the user to investigate.

Also check `BUGS.md` at the repo root for previously documented bugs that match the error.

---

## Output Format

Present the diagnosis as a structured report:

```
## Diagnosis Report: <stack-display-name>

**Stack OCID:** <stack-ocid>
**Region:** <region>
**Failed Job:** <job-ocid>
**Job Type:** APPLY | PLAN | DESTROY
**Failure Time:** <timestamp>
**Category:** <starter_pack_category>

### ROOT CAUSE

<1-3 sentence summary of why the deployment failed.
Be specific — name the resource, the error code, and the underlying issue.>

### CLUSTER STATE

<Summary of cluster health. Include:
- Node count and status
- Pod failures (count and names)
- Helm release status
- PVC issues
- If cluster was not reachable, state why.>

### RECOMMENDED FIX

<Numbered list of specific actions the user should take.
Reference the exact commands, resource names, and namespaces.
If the fix involves code changes, reference the file path and what to change.>

### ADDITIONAL OBSERVATIONS

<Any warnings, unusual patterns, or secondary issues found during investigation
that are not the root cause but may need attention.>
```

---

## Edge Cases

- **No cluster deployed yet** — If the failure is in networking or OKE creation, skip Phase 3 entirely. Diagnosis is log-only.
- **Cluster unreachable** — If kubeconfig generation or kubectl fails, record the connectivity error and proceed with log-only diagnosis.
- **Multiple failures** — If the job logs show multiple errors, report all of them ranked by likely root cause (first error is usually the root).
- **Destroy job failed** — For failed destroy jobs, check if the failure is on the Kubernetes provider (common). Recommend updating the stack to Terraform 1.5.x and retrying.
- **Plan job failed** — For failed plan jobs, the issue is in the Terraform code itself (validation errors, missing variables, provider config). No cluster investigation needed.
