---
name: Kubernetes Service Specification
description: Reference for Kubernetes Service types, networking, discovery, and troubleshooting.
---

# Kubernetes Service Specification Reference

Use this skill to design, review, explain, or troubleshoot Kubernetes `Service` resources. Keep outputs safe, scoped, and explicit about exposure, selectors, ports, traffic policy, and validation.

## Invocation Triggers

Use when the user asks about:

- Kubernetes Service manifests, Service types, or port mappings.
- ClusterIP, NodePort, LoadBalancer, ExternalName, or headless Services.
- Service discovery, DNS names, endpoints, traffic policy, or session affinity.
- Service mesh routing, network policies, load balancer annotations, or troubleshooting.

## Required Input Contract

Gather or infer:

- Target workload, namespace, labels, and selectors.
- Exposure goal: internal-only, node-level, public/private load balancer, external DNS mapping, or direct pod discovery.
- Port mapping: service port, target port, named ports, protocol, and optional node port.
- Cloud/provider context and load balancer constraints, if relevant.
- Source IP restrictions, network policy needs, and client IP preservation needs.
- Session affinity, StatefulSet/headless, mesh, metrics, or WebSocket/long-connection requirements.

Use placeholders when details are missing.

## Core Workflow

1. Classify the exposure model and choose the Service type.
2. Verify selector-to-pod-label alignment.
3. Map ports, protocols, and named target ports.
4. Add session affinity, headless behavior, traffic policy, or annotations only when justified.
5. Add security controls for public or cross-namespace exposure.
6. Provide a manifest or review findings.
7. Include validation commands for endpoints, DNS, events, and load balancer status when applicable.

## Service Type Routing

| Type | Use For | Main Caution |
|---|---|---|
| `ClusterIP` | Internal service-to-service traffic | Not reachable from outside the cluster |
| `NodePort` | Development or direct node access | Limited port range and node failure exposure |
| `LoadBalancer` | Public or private cloud load balancer | Restrict source ranges and verify provider annotations |
| `ExternalName` | CNAME-style mapping to external DNS | DNS-only; no proxying or endpoint health |
| Headless (`clusterIP: None`) | StatefulSet and direct pod discovery | Clients must handle pod endpoints |

See [service-types.md](references/service-types.md) for full examples and cloud annotations.

## Safety and Security Constraints

- Do not expose a public `LoadBalancer` or broad `0.0.0.0/0` source range without making that exposure explicit.
- Do not invent cloud-specific annotations, certificate ARNs, domains, node IPs, or provider behavior.
- Do not include secrets, credentials, kubeconfigs, tokens, private hostnames, or local paths.
- Prefer named ports and least exposure.
- Recommend network policies for sensitive Services.
- Treat `kubectl apply`, `delete`, production changes, and shared-cluster operations as approval-gated.

## Validation Rules

Before presenting completion:

- Confirm the selector matches intended pod labels.
- Confirm each `port`, `targetPort`, `protocol`, and optional `nodePort` is valid for the use case.
- Confirm Service type matches exposure intent.
- Confirm public exposure includes source-range or network-policy discussion.
- For troubleshooting, inspect service, endpoints, matching pods, DNS, events, and provider status.
- State assumptions and provider-specific uncertainty.

## Output Expectations

- For design: provide a manifest, type choice rationale, safety notes, and validation commands.
- For review: list defects, risks, and corrected YAML.
- For troubleshooting: give ordered diagnostics, likely causes, and next commands.
- For explanation: keep the summary concise and link the relevant reference section.

## Minimal Example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
    - name: http
      port: 80
      targetPort: http
      protocol: TCP
```

## Reference Map

- Service types, use cases, limitations, and cloud load balancer annotations: [service-types.md](references/service-types.md)
- Full Service spec, ports, session affinity, and traffic policies: [spec-and-ports.md](references/spec-and-ports.md)
- Headless Services, discovery, DNS, load balancing, and mesh examples: [discovery-traffic-and-mesh.md](references/discovery-traffic-and-mesh.md)
- Common patterns, network policies, best practices, and production checklist: [patterns-and-security.md](references/patterns-and-security.md)
- Troubleshooting commands and related Kubernetes resources: [troubleshooting.md](references/troubleshooting.md)
