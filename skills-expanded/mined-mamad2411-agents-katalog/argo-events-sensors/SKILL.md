---
name: argo-events-sensors
description: >
  Argo Events EventSources and Sensors for owned clusters: webhook/Kafka/SQS/calendar
  sources, dependency filters, triggers to Workflows/K8s resources, and secure webhook
  auth. Use when wiring event-driven automation on authorized Argo Events installs —
  not for probing third-party webhooks or abusing event buses you do not operate.
---

# Argo Events Sensors

## Scope And Authorization

- **In scope:** Argo Events (EventSource, Sensor, EventBus) on clusters you own or administer under authorization.
- **Out of scope:** Sending forged events to third-party endpoints; scanning random webhook receivers.
- Treat webhook secrets, cloud credentials, and bus passwords as high-value secrets.
- Prefer non-prod EventBus namespaces when experimenting; rate-limit production triggers.
- Pair manifests with `code-quality-standards`; use `argo-workflows-rbac` for Workflow SA privileges.

## When To Use

- Creating EventSources (webhook, resource, kafka, amqp, calendar, github, aws sns/sqs, etc.).
- Authoring Sensors that filter events and trigger Workflows, HTTP, or K8s objects.
- Debugging “event received but no trigger,” dependency failures, or NATS/JetStream bus issues.
- Hardening public webhook EventSources (auth headers, ingress TLS, network policies).
- Migrating cron-like jobs to calendar EventSources + Sensors.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Argo Workflows RBAC / SA | `argo-workflows-rbac` |
| Argo CD GitOps apps | `argocd-app-of-apps` / `argo-cd-rbac-basics` |
| Generic Kubernetes RBAC | cluster RBAC skill |
| Kafka platform ops broadly | messaging platform skill |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Component | Role |
| --- | --- |
| EventBus | NATS/JetStream (or compatible) transport between sources and sensors |
| EventSource | Ingest external/internal events into the bus |
| Sensor | Subscribe, filter dependencies, fire triggers |
| Trigger | Workflow, Standard K8s, HTTP, AWS Lambda, OpenWhisk, custom |
| ServiceAccount | Identity used by triggers to create resources |

## Event → Action Flow

```text
External system → EventSource → EventBus → Sensor (filters/deps) → Trigger → Workflow/K8s/HTTP
```

## Workflow

### 1. Confirm scope and success criteria

1. Record cluster, namespace, Argo Events version, EventBus type, producer systems, consumers.
2. Success: test event creates expected Workflow once; invalid/auth-fail events ignored; no open unauthenticated webhook in prod.
3. Define failure mode: retry? DLQ? alert on sensor errors?

### 2. Inventory current state

```bash
kubectl get eventbus,eventsource,sensor -A
kubectl -n argo-events get pods
kubectl -n argo-events logs deploy/eventbus-controller --tail=100
# List webhook services/ingresses
kubectl -n argo-events get svc,ingress
```

1. Map each Sensor → triggers → target Workflow templates.
2. Note which EventSources are Internet-facing.
3. Collect recent sensor error logs.

### 3. Baseline

1. Export existing CRs to Git before edits.
2. Capture a sample CloudEvent/payload schema from the producer.
3. Confirm EventBus is healthy (all replicas ready).

### 4. Apply EventSource + Sensor patterns

**Minimal webhook EventSource (sketch):**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata:
  name: webhook
  namespace: argo-events
spec:
  service:
    ports:
      - port: 12000
        targetPort: 12000
  webhook:
    example:
      port: "12000"
      endpoint: /push
      method: POST
      # Prefer auth (e.g. k8s secret for basic/token) per current CRD fields
```

**Sensor with filter + Workflow trigger (sketch):**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: webhook-workflow
  namespace: argo-events
spec:
  template:
    serviceAccountName: operate-workflow-sa
  dependencies:
    - name: webhook-dep
      eventSourceName: webhook
      eventName: example
      filters:
        data:
          - path: body.action
            type: string
            value:
              - "deploy"
  triggers:
    - template:
        name: wf-trigger
        k8s:
          operation: create
          source:
            resource:
              apiVersion: argoproj.io/v1alpha1
              kind: Workflow
              metadata:
                generateName: from-event-
              spec:
                entrypoint: main
                templates:
                  - name: main
                    container:
                      image: public.ecr.aws/docker/library/busybox:1.36
                      command: [echo]
                      args: ["event received"]
```

**Hardening checklist for webhooks**

1. TLS at ingress; deny plain HTTP externally.
2. Shared secret / signature validation (GitHub HMAC, Stripe-style, or mutual TLS).
3. NetworkPolicy: only ingress controller → EventSource pods.
4. Payload size limits; schema validation in filters.
5. Least-privilege SA on Sensor (cannot create arbitrary cluster-admin objects).

**Filters**

| Filter type | Use |
| --- | --- |
| data | JSON path equals/not equals |
| context | CloudEvents context fields |
| time | windows |
| exprs | expr-lang boolean logic |

### 5. Verify with evidence

```bash
# Port-forward webhook (lab)
kubectl -n argo-events port-forward svc/webhook-eventsource-svc 12000:12000
curl -sS -X POST localhost:12000/push \
  -H 'Content-Type: application/json' \
  -d '{"action":"deploy","app":"demo"}'
kubectl -n argo-events get workflows --sort-by=.metadata.creationTimestamp | tail
kubectl -n argo-events logs -l sensor-name=webhook-workflow --tail=50
```

1. Negative tests: wrong secret → 401/ignored; wrong filter → no Workflow.
2. Idempotency: confirm duplicate events do not create unsafe storms (rate limits / resource filters).
3. Bus down scenario documented (alerts fire).

### 6. Observe and harden

1. Metrics: event rate, trigger success/fail, sensor errors.
2. Alerts on sustained trigger failures and EventBus pod restarts.
3. Review SAs quarterly for over-privileged `create` on `*` resources.

### 7. Hand off

1. Diagram producers → sources → sensors → workflows.
2. GitOps the CRs; document how to add a new event type safely.
3. Link Workflow RBAC skill for SA and Role design.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Webhook | Auth + TLS + NetworkPolicy | Open `/` POST from Internet |
| Filters | Explicit action allowlist | Trigger on any body |
| SA | Minimal create verbs/resources | `cluster-admin` on sensor SA |
| Triggers | Parameterized WorkflowTemplate | Inline privileged pods |
| Ops | Metrics + failed-trigger alerts | Silent drop of events |
| Scope | Owned clusters | Hitting external sensors without auth |

## Output Checklist

- [ ] Cluster, namespaces, versions, authorization recorded
- [ ] EventBus healthy; sources/sensors inventoried
- [ ] Payload schema and filters documented
- [ ] Webhook auth/TLS/network controls applied (if exposed)
- [ ] Sensor SA least privilege verified
- [ ] Positive + negative event tests evidenced
- [ ] Alerts for bus/sensor failures configured
- [ ] GitOps ownership clear
- [ ] `code-quality-standards` applied to manifests

## Rules

- Authorized clusters and event producers only.
- Never leave production webhooks unauthenticated “for debugging.”
- Prefer WorkflowTemplates over ad-hoc privileged specs.
- Sensors must not become a privilege-escalation path into the cluster.
- Focus on EventSource/Sensor/EventBus wiring; route pure Workflow RBAC and CD apps elsewhere.
