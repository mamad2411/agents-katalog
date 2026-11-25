---
name: kubernetes-service-connectivity-troubleshooting
description: >
  Guides diagnosing a Kubernetes Service with no Endpoints or traffic
  that isn't reaching backend pods — label selector mismatches between
  a Service and its pods, readiness probe failures silently excluding
  otherwise-healthy pods from Endpoints, and DNS resolution failures
  (CoreDNS health, NetworkPolicy blocking port 53, headless Service/
  StatefulSet DNS). Use when a user asks "why does my Service have no
  endpoints," "connection refused hitting a ClusterIP," "my pod can't
  resolve another service by DNS name," "traffic isn't reaching my
  pods," or "my Service selector isn't matching any pods."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Kubernetes Service Connectivity Troubleshooting

## Purpose

A Kubernetes `Service` is just a stable virtual IP and DNS name backed
by a continuously reconciled list of pod IPs — its `Endpoints`/
`EndpointSlice` — populated automatically from pods matching its
`spec.selector` *and* currently passing readiness. When traffic doesn't
reach a workload, the fault almost always lives in one of three narrow
places: the selector doesn't actually match the pods it's meant to (a
label typo or case mismatch), the pods match but aren't currently
`Ready` (excluding them from Endpoints correctly, not as a bug), or DNS
resolution for the Service name itself is failing for an unrelated
reason (CoreDNS health, or a `NetworkPolicy` blocking DNS traffic). Each
produces a similar-looking "can't connect" symptom but needs a different
fix, and jumping straight to loosening a selector or disabling a
NetworkPolicy tends to create a new, worse problem instead of finding
the real one. This skill covers the diagnostic sequence for all three.

## When to use

- `kubectl get endpoints`/`endpointslices` for a Service returns empty
  despite pods that appear to be running.
- A client gets connection refused or a timeout hitting a Service's
  `ClusterIP` or DNS name.
- `nslookup`/DNS resolution for a Service name fails or times out from
  inside a pod.
- An Ingress or mesh gateway routes correctly but the backend Service it
  points to never receives the request.
- A pod that passes a manual health check locally is still missing from
  its Service's Endpoints.

## Prerequisites & environment

- `kubectl` access to inspect `Service`, `Endpoints`/`EndpointSlice`,
  and `Pod` objects in the relevant namespace(s).
- CoreDNS running in `kube-system` (the standard in-cluster DNS
  provider) — confirm it's healthy before assuming a DNS-specific
  problem is application- or Service-specific.
- A working CNI data path already established at the node/pod-IP level
  — this skill assumes basic pod-to-pod networking works; if same-node
  connectivity works but cross-node doesn't, that's a CNI data-path
  issue instead, covered in
  [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md).
- Basic familiarity with how a Service's `spec.selector` maps to pod
  `metadata.labels` — matching is an exact key/value match (case- and
  whitespace-sensitive), not a fuzzy or partial match.

## Step-by-step guidance

1. **Check the Service's selector and its Endpoints together, side by
   side** — don't eyeball the YAML from memory:
   ```bash
   kubectl get svc <name> -n <namespace> -o jsonpath='{.spec.selector}{"\n"}'
   kubectl get endpoints <name> -n <namespace>
   kubectl get endpointslice -n <namespace> -l kubernetes.io/service-name=<name>
   ```
   Empty `Endpoints`/no `EndpointSlice` addresses is the first branch
   point: either no pod matches the selector at all, or pods match but
   none are currently `Ready` (Kubernetes only populates Endpoints with
   ready pod IPs).

2. **Compare the selector against actual pod labels exactly**:
   ```bash
   kubectl get pods -n <namespace> --show-labels
   ```
   Check every key in the Service's selector is present on the pods
   with an exactly matching value — a Service selector with an extra
   key the pods don't have at all, a typo'd label key/value, or a case
   mismatch (`App: payments` vs. `app: payments`) all produce a silent
   zero-match with no error from the API server on either side.

3. **If labels match but Endpoints are still empty, check pod
   readiness** — a `Running` pod that hasn't passed its readiness probe
   is deliberately excluded:
   ```bash
   kubectl get pods -n <namespace> -o wide
   kubectl describe pod <pod> -n <namespace>
   ```
   Look for `Readiness probe failed` in the pod's events, and check the
   probe's configured port/path against what the container actually
   serves.

4. **Test the readiness probe's target manually** from inside the
   container to confirm whether it's a probe-configuration problem or a
   real application issue:
   ```bash
   kubectl exec <pod> -n <namespace> -- curl -sf localhost:<port><path>
   ```
   A probe pointed at the wrong port/path, or one with too short a
   `failureThreshold`/`periodSeconds` for the app's real response time,
   produces the same "no endpoints" symptom as an actually-unhealthy
   app — this step distinguishes them. See
   [pod-crashloop-and-oom-troubleshooting](../pod-crashloop-and-oom-troubleshooting/SKILL.md)
   for the closely related liveness-probe failure mode, which restarts
   the container instead of just excluding it from Endpoints.

5. **Once Endpoints are populated, test the pod IP directly**, bypassing
   the Service layer, before assuming the Service itself works:
   ```bash
   kubectl run net-test -n <namespace> --image=busybox:1.36 --rm -it --restart=Never -- \
     wget -qO- --timeout=2 <pod-ip>:<port>
   ```
   If this fails too, the problem is at the pod/network level (the
   application isn't actually listening, a `NetworkPolicy` is blocking
   the specific port, or a cross-node CNI issue), not the Service
   abstraction.

6. **If the pod IP works but the Service `ClusterIP`/DNS name doesn't,
   check `kube-proxy`** (or your CNI's Service-implementing component,
   for CNIs with an alternative Service data path):
   ```bash
   kubectl get pods -n kube-system -l k8s-app=kube-proxy
   kubectl logs -n kube-system <kube-proxy-pod>
   ```
   A missing or crash-looping `kube-proxy` on the client's node means
   that node has no iptables/IPVS rules programmed for any
   `ClusterIP`, which looks like every Service is broken from that
   node specifically.

7. **For DNS-specific failures**, test resolution directly and check
   CoreDNS itself:
   ```bash
   kubectl exec <pod> -n <namespace> -- nslookup <service>.<namespace>.svc.cluster.local
   kubectl get pods -n kube-system -l k8s-app=kube-dns
   kubectl logs -n kube-system -l k8s-app=kube-dns
   ```
   If CoreDNS pods are healthy but resolution still fails from a
   specific namespace/pod, check for a default-deny `NetworkPolicy`
   without an explicit egress allow rule for DNS (UDP/TCP port 53 to
   `kube-system`) — see
   [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
   for `NetworkPolicy` enforcement details; a policy-enforcing CNI
   applies a DNS-blocking default-deny exactly as configured, silently,
   with no distinct error visible from the client side.

8. **For a headless Service (`clusterIP: None`) or StatefulSet DNS**
   returning no records, check the specific fields that govern
   per-pod DNS rather than the usual Service selector path:
   ```bash
   kubectl get svc <name> -n <namespace> -o yaml | grep clusterIP
   kubectl get statefulset <name> -n <namespace> -o jsonpath='{.spec.serviceName}'
   ```
   The StatefulSet's `spec.serviceName` must reference the exact
   headless Service backing it for per-pod DNS records
   (`<pod>.<service>.<namespace>.svc.cluster.local`) to be created.

9. **For an Ingress that routes but times out reaching the backend**,
   confirm the failure is at the Service layer and not the Ingress
   controller itself by testing the Service directly (steps 1–6) before
   assuming an Ingress-specific misconfiguration — see
   [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md)
   for Ingress-specific 502/504 diagnosis once the backing Service is
   confirmed healthy on its own.

10. **Fix the actual root cause** — correct the mismatched label
    (on the Deployment/pod template, not by loosening the Service
    selector), fix the probe's port/path/timing (or the health endpoint
    it checks), add the missing `NetworkPolicy` egress-allow rule for
    DNS, or fix the headless Service/`serviceName` reference — then
    re-run steps 1 and 5 to confirm Endpoints populate and traffic
    actually reaches the pod, not just that the symptom superficially
    disappeared.

## Best practices

- Diagnose Service/selector/Endpoints/labels with exact `kubectl`
  output compared side by side, not by reading YAML from memory — label
  mismatches are frequently a single case or whitespace difference that
  is easy to miss visually.
- Give every workload a distinct, meaningful readiness probe (not just a
  copy of the liveness probe) — readiness failing should mean "don't
  send traffic yet/right now," a normal and expected state during
  startup or brief overload, not an error condition to alarm on
  immediately.
- Test connectivity at the pod-IP level before the Service level, and
  the Service level before the Ingress/mesh-gateway level — each layer
  adds its own potential failure mode, and testing from the inside out
  isolates which one actually broke.
- When diagnosing DNS, separate "CoreDNS itself is unhealthy" from "a
  NetworkPolicy is blocking DNS traffic" from "the pod's `resolv.conf`
  is wrong" — these three have different fixes and are easy to conflate
  under a single "DNS is broken" label.
- Re-validate Service DNS/connectivity as part of any new cluster's
  post-provision smoke tests — see
  [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md)
  — rather than only discovering a cluster-wide DNS/NetworkPolicy
  interaction issue when the first real application hits it.
- Never "fix" an empty-Endpoints Service by loosening its selector until
  something matches — verify and correct the actual label mismatch on
  the workload instead.

## Common pitfalls

- **Symptom:** A Service has zero Endpoints despite pods that are
  clearly `Running` and appear to be the intended backend.
  **Fix:** Compare `kubectl get svc -o jsonpath='{.spec.selector}'`
  against `kubectl get pods --show-labels` directly — a label typo,
  case mismatch, or an extra selector key not present on the pods at
  all is the most common cause, and neither side surfaces an error for
  it since selector matching is silent by design.

- **Symptom:** A pod intermittently appears and disappears from a
  Service's Endpoints even though it looks healthy and its logs show no
  errors.
  **Fix:** Its readiness probe is intermittently failing — check the
  probe's configured port/path and `failureThreshold`/`periodSeconds`
  against the app's actual response behavior. A pod excluded from
  Endpoints purely due to failing readiness is Kubernetes working
  correctly, not a bug; fix the probe or the underlying slow-response
  cause, don't treat the exclusion itself as the problem.

- **Symptom:** DNS resolution for `<service>.<namespace>.svc.cluster.local`
  times out or fails from within specific pods, while CoreDNS pods
  themselves show `Running` and healthy.
  **Fix:** Check for a default-deny `NetworkPolicy` in that namespace
  with no explicit egress-allow for DNS (UDP/TCP port 53 to
  `kube-system`) — a policy-enforcing CNI blocks DNS exactly as silently
  as any other denied traffic, and "CoreDNS is up" does not rule this
  out. Add an explicit DNS egress-allow rule alongside the intended
  application-traffic rules.

- **Symptom:** An empty-Endpoints Service is "fixed" by progressively
  removing keys from its selector until it starts matching something.
  **Fix:** This routes traffic to whatever pods happen to match the
  now-overbroad selector, which is very likely the wrong backend rather
  than the intended one — find and correct the actual label mismatch on
  the target Deployment/pods instead of loosening the Service's
  matching criteria to paper over it.

- **Symptom:** A headless Service backing a StatefulSet returns no DNS
  records for individual pods (`<pod-name>.<service>.<namespace>.svc
  .cluster.local`).
  **Fix:** Confirm the Service has `clusterIP: None` and that the
  StatefulSet's `spec.serviceName` field references that exact Service
  by name — per-pod DNS records are only created when this link is
  correct, and a StatefulSet pointed at the wrong (or a non-headless)
  Service name produces no per-pod records with no explicit error.

- **Symptom:** Traffic reaches a pod's IP directly but not through the
  Service's `ClusterIP`, and this is isolated to client pods on one
  specific node.
  **Fix:** Check `kube-proxy` (or the CNI's Service-dataplane
  equivalent) on that specific node — a crashed or misconfigured
  `kube-proxy` there means no iptables/IPVS rules exist for any
  `ClusterIP` from that node's perspective, which looks like a
  single-Service failure but is actually node-wide.

## Worked example

**Scenario:** `payments-api` clients get connection refused hitting the
Service; separately, a different pod fails to resolve
`billing.finance.svc.cluster.local`.

```bash
kubectl get svc payments-api -n payments -o jsonpath='{.spec.selector}{"\n"}'
# {"app":"payments"}

kubectl get endpoints payments-api -n payments
# NAME           ENDPOINTS   AGE
# payments-api   <none>      3h

kubectl get pods -n payments --show-labels
# NAME                            READY   STATUS    LABELS
# payments-api-7d9f6-abc12        1/1     Running   app=payments-api
```

The Service selector (`app: payments`) doesn't match the pod's actual
label (`app: payments-api`) — a naming-convention drift, not a probe or
network issue.

```bash
kubectl patch deployment payments-api -n payments --type merge \
  -p '{"spec":{"template":{"metadata":{"labels":{"app":"payments"}}}}}'
kubectl get endpoints payments-api -n payments
# NAME           ENDPOINTS
# payments-api   10.244.2.14:8080,10.244.3.9:8080
```

Endpoints populate immediately once the label matches, confirming the
fix.

Second issue, in a different namespace:

```bash
kubectl exec -n reporting deploy/reporting-job -- \
  nslookup billing.finance.svc.cluster.local
# ;; connection timed out; no servers could be reached

kubectl get pods -n kube-system -l k8s-app=kube-dns
# coredns-...   1/1   Running   (both replicas healthy)

kubectl get networkpolicy -n reporting -o yaml
# a default-deny-all-egress policy with no DNS (port 53) exception
```

CoreDNS itself is healthy — the `reporting` namespace's default-deny
egress `NetworkPolicy` has no explicit allow rule for DNS traffic to
`kube-system`. Adding one resolves it:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: { name: allow-dns-egress, namespace: reporting }
spec:
  podSelector: {}
  policyTypes: ["Egress"]
  egress:
    - to: [{ namespaceSelector: { matchLabels: { kubernetes.io/metadata.name: kube-system } } }]
      ports:
        - { protocol: UDP, port: 53 }
        - { protocol: TCP, port: 53 }
```

```bash
kubectl apply -f allow-dns-egress.yaml
kubectl exec -n reporting deploy/reporting-job -- \
  nslookup billing.finance.svc.cluster.local
# Address: 10.96.44.201
```

## Cross-references

- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — NetworkPolicy enforcement mechanics and cross-node data-path issues underlying several of the failure modes above.
- [pod-crashloop-and-oom-troubleshooting](../pod-crashloop-and-oom-troubleshooting/SKILL.md) — the related liveness-probe failure mode (restarts the container) versus the readiness-probe failure mode (excludes from Endpoints) covered here.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — diagnosing an Ingress-level 502/504 once the backing Service itself is confirmed healthy.
- [service-mesh-istio](../service-mesh-istio/SKILL.md) — diagnosing a 503 from an Istio sidecar, a related but distinct failure mode layered on top of the Service/Endpoints mechanics here.
- [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md) — the post-provision smoke test that should catch cluster-wide DNS/Service issues before applications hit them.
