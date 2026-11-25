---
name: argo-events-and-event-driven-automation
description: >
  Configures Argo Events `EventSource`, `Sensor`, and `EventBus` CRDs to
  trigger Argo Workflows, Kubernetes resource changes, or other actions
  from external events — webhooks, message queues (Kafka/NATS/SQS/
  RabbitMQ), and cron schedules. Use when the user asks to "trigger an
  Argo Workflow from a webhook," "wire up an EventSource for S3/Kafka/
  GitHub events," "fan events out to multiple triggers with a Sensor,"
  "debug a Sensor that isn't firing," or "build event-driven automation on
  Kubernetes without a separate message broker to operate."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: gitops-argo-ecosystem
  maturity: stable
---

# Argo Events and Event-Driven Automation

## Purpose

Argo Events is a Kubernetes-native event framework that decouples *event
sources* (webhooks, message queues, cloud storage notifications, cron
schedules, and dozens of other emitters) from *triggers* (starting an Argo
Workflow, creating/patching a Kubernetes resource, calling another
webhook), connected through a `Sensor`'s dependency/filter logic and an
`EventBus` for durable delivery between them. It exists so that
"kick off automation when X happens" doesn't require bespoke polling
scripts, a hand-rolled webhook receiver Deployment, or gluing together an
external broker's client libraries per language/team — the event
plumbing, retry, and filtering logic is declarative and lives in the same
GitOps-managed cluster as everything else. This matters operationally
because event-driven automation that's implemented as ad hoc scripts
tends to have no consistent retry/dedup/observability story; Argo Events
gives all three uniformly across every event source.

## When to use

- Triggering an Argo Workflows pipeline (see
  [argo-workflows-pipeline-design](../argo-workflows-pipeline-design/SKILL.md))
  from an external event: a GitHub webhook, a file landing in S3/GCS, a
  Kafka/NATS/SQS message, or a cron schedule.
- Fanning one event out to multiple independent triggers (start a
  Workflow *and* post a Slack notification *and* patch a ConfigMap) with
  shared filter logic rather than three separate receivers.
- Requiring correlation across multiple events before triggering anything
  (e.g., "only trigger once both the upload-complete and
  validation-passed events have arrived") — Argo Events' Sensor
  dependency/circuit logic exists for this.
- Replacing a bespoke webhook-receiver Deployment/polling script with a
  declarative, GitOps-managed `EventSource`/`Sensor` pair.
- Diagnosing why an event arrived but nothing downstream happened
  (a Sensor that isn't firing, or fired but the trigger silently failed).

## Prerequisites & environment

- Argo Events ≥ 1.9 installed cluster-wide (controller + webhook
  components), with an `EventBus` provisioned in the target namespace —
  the default `NATS`-backed `EventBus` is sufficient for most setups;
  `Kafka`-backed `EventBus` is available for higher-throughput/durability
  needs.
- Network reachability for the event's origin to hit the cluster: for
  webhook-based `EventSource`s (GitHub, Gitlab, generic webhook), an
  Ingress or LoadBalancer exposing the `EventSource`'s Service publicly
  (or within the org's network) with TLS terminated appropriately.
- For queue-based `EventSource`s (Kafka, NATS, SQS, RabbitMQ, Redis
  Streams, etc.), network access and credentials (via a referenced
  `Secret`, never inline) to the broker.
- If triggers target Argo Workflows, the Argo Workflows controller
  installed and the `Sensor`'s `ServiceAccount` granted RBAC to create
  `Workflow`/`WorkflowTemplate` resources in the target namespace — Argo
  Events triggers a Workflow by creating the CRD object directly via the
  Kubernetes API, so ordinary RBAC applies.

## Step-by-step guidance

1. **Provision an `EventBus`** (once per namespace, shared by all
   `EventSource`/`Sensor` pairs in it):
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: EventBus
   metadata:
     name: default
     namespace: automation
   spec:
     nats:
       native:
         replicas: 3
         auth: token
   ```

2. **Define an `EventSource`** for the origin of events. Webhook example
   (generic HTTP webhook — GitHub/GitLab have dedicated event source
   types with signature verification):
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: EventSource
   metadata:
     name: upload-webhook
     namespace: automation
   spec:
     service:
       ports: [{ port: 12000, targetPort: 12000 }]
     webhook:
       upload-complete:
         port: "12000"
         endpoint: /upload-complete
         method: POST
   ```
   Message-queue example (SQS):
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: EventSource
   metadata:
     name: s3-notifications
     namespace: automation
   spec:
     sqs:
       upload-queue:
         region: us-east-1
         queue: <SQS_QUEUE_NAME>
         accessKey:
           name: aws-credentials
           key: access-key
         secretKey:
           name: aws-credentials
           key: secret-key
   ```
   Credentials are referenced from an existing `Secret`
   (`aws-credentials`) — never inlined as plaintext values in the
   `EventSource` spec.
   Cron example:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: EventSource
   metadata:
     name: nightly-trigger
     namespace: automation
   spec:
     calendar:
       nightly:
         schedule: "0 2 * * *"
         timezone: "UTC"
   ```

3. **Define a `Sensor`** that depends on one or more `EventSource`
   event names, filters them, and fires triggers:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Sensor
   metadata:
     name: upload-processor
     namespace: automation
   spec:
     dependencies:
       - name: upload-dep
         eventSourceName: s3-notifications
         eventName: upload-queue
         filters:
           data:
             - path: body.detail.object.key
               type: string
               comparator: "="
               value: ["*.parquet"]
     triggers:
       - template:
           name: start-etl-workflow
           argoWorkflow:
             operation: submit
             source:
               resource:
                 apiVersion: argoproj.io/v1alpha1
                 kind: Workflow
                 metadata:
                   generateName: etl-from-upload-
                 spec:
                   workflowTemplateRef: { name: nightly-etl }
                   arguments:
                     parameters:
                       - name: object-key
                         value: "{{upload-dep.body.detail.object.key}}"
   ```
   The `filters.data` block rejects events that don't match (e.g.,
   non-`.parquet` uploads) before the trigger fires at all — filter as
   early and specifically as possible rather than triggering broadly and
   filtering downstream inside the Workflow.

4. **Fan one event out to multiple independent triggers** by adding
   more entries to `spec.triggers`, each with its own template:
   ```yaml
   spec:
     dependencies:
       - { name: upload-dep, eventSourceName: s3-notifications, eventName: upload-queue }
     triggers:
       - template:
           name: start-etl-workflow
           argoWorkflow: { operation: submit, source: { resource: { ... } } }
       - template:
           name: notify-slack
           http:
             url: https://hooks.example.internal/notify
             method: POST
             payload:
               - src: { dependencyName: upload-dep, dataKey: body.detail.object.key }
                 dest: object-key
       - template:
           name: patch-status-configmap
           k8s:
             operation: patch
             source:
               resource:
                 apiVersion: v1
                 kind: ConfigMap
                 metadata: { name: last-upload-status }
             patchStrategy: merge
   ```

5. **Require correlation across multiple events before triggering**,
   using multiple `dependencies` and a circuit expression:
   ```yaml
   spec:
     dependencies:
       - { name: upload-dep, eventSourceName: s3-notifications, eventName: upload-queue }
       - { name: validate-dep, eventSourceName: validation-webhook, eventName: validation-complete }
     triggers:
       - template:
           name: start-etl-workflow
           conditions: "upload-dep && validate-dep"
           argoWorkflow: { operation: submit, source: { resource: { ... } } }
     eventBusName: default
   ```
   `conditions` is a boolean expression over dependency names — the
   trigger only fires once *both* named dependencies have each delivered
   a matching event (within the Sensor's correlation window), not on
   either alone.

6. **Verify and debug:**
   ```bash
   kubectl get eventsource,sensor,eventbus -n automation
   kubectl logs -n automation deploy/upload-webhook-eventsource -f
   kubectl logs -n automation deploy/upload-processor-sensor -f
   kubectl describe sensor upload-processor -n automation   # trigger conditions/status
   ```
   The Sensor's own logs show whether an event was received, which
   filters it passed/failed, and whether the trigger action itself
   succeeded or errored (e.g., RBAC denial creating the `Workflow`).

## Best practices

- Filter as early as possible in the `Sensor`'s `dependencies.filters`,
  not downstream inside the triggered Workflow — a Sensor that fires
  broadly and relies on the first Workflow step to check "is this event
  actually relevant" wastes Pods and obscures why a Workflow ran at all.
- Scope each `Sensor`'s triggering `ServiceAccount` to only the specific
  namespace/resource kinds its triggers need to create — a Sensor
  authorized to create arbitrary cluster resources is a lateral-movement
  risk if the event source itself is ever spoofable.
- Use dedicated `EventSource` types (GitHub, GitLab, Stripe, etc.) with
  their built-in signature/secret verification rather than the generic
  webhook type whenever the origin supports it — the generic webhook type
  has no built-in authenticity check, so anyone who can reach the
  endpoint can forge events unless you add your own verification.
- Keep `EventBus` sized (`nats.native.replicas`) for the actual event
  throughput and durability needs — a single-replica `EventBus` is a
  single point of failure for every `Sensor` depending on it in that
  namespace.
- Use `conditions` (multi-dependency correlation) rather than chaining
  separate Sensors with ad hoc state (a ConfigMap flag one Sensor sets
  and another polls) when a trigger genuinely depends on multiple prior
  events — the built-in correlation window is simpler and more reliable
  than home-rolled coordination.
- Version and GitOps-manage `EventSource`/`Sensor`/`EventBus` manifests
  the same as any other cluster resource — treat them as part of the
  GitOps-tracked config repo, not a one-off `kubectl apply` nobody
  remembers making.

## Common pitfalls

- **Symptom:** An external webhook provider shows the delivery as
  successful (200 response), but no `Sensor` trigger ever fires.
  **Fix:** Check the `Sensor`'s `dependencies.filters` first — a common
  cause is a filter path/comparator that doesn't match the actual event
  payload shape (e.g., expecting `body.detail.object.key` but the real
  payload nests it under `body.Records[0].s3.object.key`). Inspect the
  raw event via the `EventSource` Pod logs to confirm the actual payload
  structure before assuming the Sensor itself is broken.

- **Symptom:** A `Sensor` trigger fires but the target `Workflow` never
  gets created, with no obvious error in the `EventSource` logs.
  **Fix:** Check the `Sensor` Pod's own logs and `kubectl describe
  sensor` — this is almost always an RBAC denial (the Sensor's
  `ServiceAccount` lacks permission to create `Workflow` resources in the
  target namespace) or a malformed `argoWorkflow.source.resource`
  template, both of which surface in the Sensor's logs, not the
  EventSource's.

- **Symptom:** A single upstream event (e.g., one S3 upload) triggers the
  downstream Workflow multiple times.
  **Fix:** Check whether the underlying message queue's delivery
  semantics are at-least-once (SQS, most Kafka configurations) — Argo
  Events does not deduplicate by default. Either make the triggered
  Workflow idempotent (safe to run twice on the same input) or add a
  dedup filter keyed on a stable event ID if true single-delivery
  semantics are required.

- **Symptom:** A `Sensor` with a multi-dependency `conditions` expression
  never fires even though both source events clearly occurred (visible in
  each `EventSource`'s logs).
  **Fix:** Multi-dependency correlation has a bounded time window; if the
  two events arrive further apart than the Sensor's correlation logic
  tolerates (or across a Sensor Pod restart, since in-memory correlation
  state may not survive it depending on version/config), the condition
  never becomes true. Confirm event arrival timing and consider whether
  the two events are actually expected to arrive close enough together
  for correlation to be the right pattern versus a stateful `Workflow`
  step that waits on both explicitly.

- **Symptom:** A generic webhook `EventSource` is receiving forged/
  spoofed events from outside the expected origin, triggering unwanted
  Workflow runs.
  **Fix:** The generic `webhook` EventSource type has no built-in
  signature verification. Migrate to the origin's dedicated EventSource
  type (e.g., `github` with a configured webhook secret) which validates
  a signature header before the event is even considered, or add an
  authenticating proxy/Ingress rule in front of the generic webhook
  endpoint.

## Worked example

**Scenario:** A file landing in an S3 bucket should trigger the
`nightly-etl` `WorkflowTemplate` (from
[argo-workflows-pipeline-design](../argo-workflows-pipeline-design/SKILL.md)),
but only for `.parquet` files, and only after a separate validation
webhook confirms the file passed a checksum check.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata:
  name: s3-notifications
  namespace: automation
spec:
  sqs:
    upload-queue:
      region: us-east-1
      queue: <SQS_QUEUE_NAME>
      accessKey: { name: aws-credentials, key: access-key }
      secretKey: { name: aws-credentials, key: secret-key }
---
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata:
  name: validation-webhook
  namespace: automation
spec:
  service:
    ports: [{ port: 12001, targetPort: 12001 }]
  webhook:
    validation-complete:
      port: "12001"
      endpoint: /validation-complete
      method: POST
---
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: upload-processor
  namespace: automation
spec:
  eventBusName: default
  dependencies:
    - name: upload-dep
      eventSourceName: s3-notifications
      eventName: upload-queue
      filters:
        data:
          - path: body.detail.object.key
            type: string
            comparator: "="
            value: ["*.parquet"]
    - name: validate-dep
      eventSourceName: validation-webhook
      eventName: validation-complete
      filters:
        data:
          - path: body.status
            type: string
            comparator: "="
            value: ["passed"]
  triggers:
    - template:
        name: start-etl-workflow
        conditions: "upload-dep && validate-dep"
        argoWorkflow:
          operation: submit
          source:
            resource:
              apiVersion: argoproj.io/v1alpha1
              kind: Workflow
              metadata: { generateName: etl-from-upload- }
              spec:
                workflowTemplateRef: { name: nightly-etl }
                arguments:
                  parameters:
                    - name: object-key
                      value: "{{upload-dep.body.detail.object.key}}"
```

Only when both `upload-dep` (a `.parquet` object key) and `validate-dep`
(`status: passed`) have each delivered a matching event does `conditions:
"upload-dep && validate-dep"` become true and the `nightly-etl` Workflow
gets submitted — a non-parquet upload or a failed validation never
triggers the pipeline, and `kubectl describe sensor upload-processor -n
automation` shows exactly which dependency is still pending if the
Workflow doesn't start when expected.

## Cross-references

- [argo-workflows-pipeline-design](../argo-workflows-pipeline-design/SKILL.md)
- [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
- [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)
