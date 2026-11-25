---
name: alicloud-acs-agent-sandbox
description: Bootstrap, create, connect to, operate, secure, scale, upgrade, troubleshoot, inspect, and tear down Alibaba Cloud Container Compute Service (ACS) Agent Sandbox environments. Use for zero-to-Sandbox deployments from VPC and ACS cluster creation, Sandbox, SandboxSet, SandboxClaim, Checkpoint, SandboxUpdateOps, E2B SDK integration, tenant API keys and quotas, OSS or NAS CSI mounts, TrafficPolicy and SecurityProfile controls, SandboxGateway routing, Prometheus monitoring, ACK-based deployments, or ACK One multi-cluster fleet operations.
---

# Manage ACS Agent Sandbox

Operate ACS Agent Sandbox through Kubernetes custom resources and the E2B-compatible API. Treat the sandbox workload as untrusted and preserve a reproducible evidence trail under `output/alicloud-acs-agent-sandbox/`.

## Start here

1. Confirm whether the target is an ACS cluster, an ACK cluster using ACS compute, or an ACK One fleet.
2. Confirm kubeconfig context, namespace, region, desired image, resource size, network boundary, and requested lifecycle action.
3. Run the read-only inspection before changing an existing environment:

```bash
python3 skills/compute/acs/alicloud-acs-agent-sandbox/scripts/inspect_agent_sandbox.py \
  --output output/alicloud-acs-agent-sandbox/inspection.json
```

4. Read the reference that matches the task:

- Start from an empty account/network or release the complete stack: [references/bootstrap-and-teardown.md](references/bootstrap-and-teardown.md)
- Create, connect, pause, resume, checkpoint, clone, upgrade, restart, or delete: [references/creation-lifecycle.md](references/creation-lifecycle.md)
- Manage teams, API keys, quotas, or MySQL key storage: [references/tenancy-storage.md](references/tenancy-storage.md)
- Mount and validate OSS or NAS storage: [references/storage-mounts.md](references/storage-mounts.md)
- Configure gateway routing, TrafficPolicy, L7 egress policy, credential injection, or network expansion: [references/networking-security.md](references/networking-security.md)
- Monitor, inspect, alert, or diagnose: [references/observability-inspection.md](references/observability-inspection.md)
- Look up CRDs, phases, conditions, labels, and annotations: [references/crd-reference.md](references/crd-reference.md)
- Deploy OpenClaw or operate through ACK One: [references/platform-patterns.md](references/platform-patterns.md)
- Verify currency or follow an upstream procedure: [references/sources.md](references/sources.md)

5. State the planned mutation and its blast radius. Obtain confirmation before delete, destructive replacement, fleet-wide policy, credential-store migration, gateway cutover, or upgrade operations.
6. Apply the smallest scoped change, wait for the documented terminal condition, rerun inspection, and save sanitized outputs.

## Non-negotiable safety rules

- Never print, log, commit, or place API keys, runtime tokens, JWTs, AccessKeys, DSNs, `hashPepper`, kubeconfigs, or generated migration SQL in evidence.
- Do not use `kubectl describe pod` or dump Deployment/Pod arguments for Sandbox Manager: some addon versions place the admin API key in container arguments. Use the redacting inspector and bounded JSONPath queries; rotate the key immediately if it is exposed.
- Keep `automountServiceAccountToken: false` unless the workload explicitly needs Kubernetes API access.
- Use a dedicated sandbox vSwitch and enterprise security group. Deny metadata service `100.100.100.200/32` and private networks except for explicitly required endpoints.
- Do not rely on TrafficPolicy alone when a container has root, privileged mode, `NET_ADMIN`, `SYS_ADMIN`, `CAP_SETUID`, or `CAP_SETGID`; these privileges can bypass in-namespace ACLs.
- Treat the public `code-interpreter:v1.6` and OpenClaw examples as validation images, not production-hardened images.
- Require HTTPS for E2B production access. Prefer the native protocol with a wildcard domain and certificate; use the private protocol for simplified test integration.
- Treat China mainland ICP filing as a public-ALB preflight gate. A domain can work briefly before delayed enforcement returns HTTP 403 or resets TLS.
- Do not assume paused sandboxes can always resume. Capacity shortage and account arrears can prevent wake-up; WebSocket, SSE, and gRPC connections must reconnect.
- Do not upgrade a claimed sandbox without a data plan. `SandboxUpdateOps` rebuilds the Pod and does not retain rootfs, memory, or IP.
- Do not change a live PV authentication mode in place. Relevant `volumeAttributes` are immutable; recreating a PV can interrupt OSS access.
- Enable the `csi` runtime only on storage-enabled SandboxSets. It injects a privileged container and a `/var/run/csi` hostPath, which changes the isolation boundary.
- Keep NAS mount targets in the Sandbox VPC, use NFSv3, and never delete a NAS mount target while a Sandbox still has it mounted.
- Quota enforcement fails open when Redis is unavailable. Alert on this condition and do not describe quota as a hard security boundary during Redis failure.

## Core creation path

For an empty-account deployment, use `$aliyun-vpc-manage` and `$alicloud-acs-cluster` as described in `bootstrap-and-teardown.md`. Then use this sequence for the Agent Sandbox layer:

1. Enable Agent Sandbox for the cluster and verify component prerequisites from `creation-lifecycle.md`. Confirm `managed-coredns` is active before creating any component or Sandbox that needs cluster service discovery.
2. Enable RRSA before Agent Identity, then install a supported Ingress Controller, `ack-agent-identity` when required, `ack-agent-sandbox-controller`, and `ack-sandbox-manager`. Grant `AliyunCSManagedAgentSandboxRole` only through the documented authorization flow.
3. Configure the manager domain, admin API key, TLS, and the Ingress listener. Keep the admin key in a secret manager or protected component configuration.
4. Create a `SandboxSet` warm pool with explicit requests and limits, ACS labels, `automountServiceAccountToken: false`, and only required runtimes.
5. Wait until `status.availableReplicas == spec.replicas`.
6. Allocate with E2B `Sandbox.create()` or a `SandboxClaim`. Prefer claims for declarative Kubernetes workflows.
7. Verify Sandbox `status.phase=Running`, `Ready=True`, the claimed label, runtime API operations, and network policy behavior.
8. Set an explicit timeout, pause policy, or shutdown time. Never leave temporary sandboxes without a lifecycle owner.

Minimal warm-pool shape:

```yaml
apiVersion: agents.kruise.io/v1alpha1
kind: SandboxSet
metadata:
  name: code-interpreter
  namespace: default
spec:
  replicas: 4
  runtimes:
    - name: agent-runtime
  template:
    metadata:
      labels:
        alibabacloud.com/acs: "true"
        alibabacloud.com/compute-class: agent-sandbox
        alibabacloud.com/compute-qos: default
    spec:
      automountServiceAccountToken: false
      containers:
        - name: sandbox
          image: <REGION-LOCAL-HARDENED-IMAGE>
          resources:
            requests: {cpu: "1", memory: 1Gi, ephemeral-storage: 30Gi}
            limits: {cpu: "1", memory: 1Gi}
      terminationGracePeriodSeconds: 30
```

## E2B client path

The official ACS documentation currently requires E2B Python SDK versions below `2.25.0`; its validated example pins `e2b-code-interpreter==2.7.0` and `e2b==2.24.0`. Recheck the official page before changing these versions.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install "e2b-code-interpreter==2.7.0" "e2b==2.24.0"
```

Set `E2B_DOMAIN` and `E2B_API_KEY` outside source code. Exercise `run_code`, `files.write/read`, and `commands.run`, then explicitly pause or kill the test sandbox.

For private acceptance, port-forward `service/sandbox-manager` on port 7788, install the OpenKruise customized E2B patch package, set `E2B_DOMAIN=localhost:7788`, and pass `--private-protocol`. This uses HTTP only on the local tunnel and is not a production ingress design.

Run the bundled smoke test for a repeatable acceptance and guaranteed cleanup attempt:

```bash
python3 skills/compute/acs/alicloud-acs-agent-sandbox/scripts/e2b_smoke_test.py \
  --template code-interpreter \
  --output output/alicloud-acs-agent-sandbox/e2b-smoke.json
```

For an existing OSS or NAS PV, enable the `csi` runtime on the target SandboxSet and pass the mount as E2B metadata:

```bash
python3 skills/compute/acs/alicloud-acs-agent-sandbox/scripts/e2b_smoke_test.py \
  --template code-interpreter \
  --storage-type nas \
  --storage-pv pv-nas-sandbox \
  --storage-mount-path /mnt/shared \
  --output output/alicloud-acs-agent-sandbox/e2b-nas-smoke.json
```

For OSS Agent Identity, also pass `--credential-provider` and `--agent-name`. See `storage-mounts.md`; the script never accepts or records AccessKeys.

## Inspection workflow

Run inspection before and after a change. For manual follow-up, use bounded queries:

```bash
kubectl get sandbox,sandboxset,sandboxclaim,checkpoint,sandboxupdateops -A
kubectl get pods -n sandbox-system -o wide
kubectl get events -A --field-selector type=Warning --sort-by=.lastTimestamp
kubectl get trafficpolicy -A
kubectl get globaltrafficpolicy
kubectl get securityprofile -A
kubectl get globalsecurityprofile
```

Classify findings as:

- Critical: credential exposure, metadata/private-network access without justification, missing isolation, destructive operation in progress without backup, or an admin path exposed without authentication.
- High: component not ready, failed lifecycle operation, unavailable warm pool, quota Redis fail-open, gateway errors, or repeated reconciliation failures.
- Medium: version prerequisite not met, missing monitoring, insufficient vSwitch/security-group capacity, or policy gaps.
- Info: capacity, phase distribution, claim utilization, configured policies, and current topology.

## Output And Evidence

Save the inspection JSON, redacted manifests, command transcript, and final verification beneath `output/alicloud-acs-agent-sandbox/<operation>/`. A task is complete only when:

- the requested resource reaches its documented terminal state;
- readiness, lifecycle, network, storage, and authentication checks relevant to the task pass;
- secrets are absent from evidence;
- rollback or cleanup ownership is explicit;
- the final report lists resource names, namespaces, observed versions, changes, risks, and evidence paths.

## Validation

```bash
python3 -m py_compile skills/compute/acs/alicloud-acs-agent-sandbox/scripts/inspect_agent_sandbox.py
python3 -m py_compile skills/compute/acs/alicloud-acs-agent-sandbox/scripts/e2b_smoke_test.py
python3 skills/compute/acs/alicloud-acs-agent-sandbox/scripts/inspect_agent_sandbox.py --help
python3 skills/compute/acs/alicloud-acs-agent-sandbox/scripts/e2b_smoke_test.py --help
python3 scripts/quick_validate.py skills/compute/acs/alicloud-acs-agent-sandbox
```
