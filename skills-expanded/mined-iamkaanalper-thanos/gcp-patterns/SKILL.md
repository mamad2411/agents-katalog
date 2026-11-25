---
name: gcp-patterns
description: Cloud Run deployment, BigQuery optimization, Pub/Sub patterns, IAM best practices. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When building or reviewing GCP/serverless or data-heavy backend features, especially in swarms with infra or backend tracks. Pair with gcp-expert, backend-dev, devops.
---

# GCP Patterns (Grok Port)

Production-grade patterns for Google Cloud Platform workloads. Focus on reliable, observable, cost-aware serverless and data systems. Adapted for Grok with full the original Claude Code AI software team system parity (Production Contract, hooks, compound, palace, claim-verification).

## Cloud Run Deployment

### Dockerfile for Cloud Run (multi-stage, non-root)
```dockerfile
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

FROM node:20-slim
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER app
EXPOSE 8080
ENV PORT=8080 NODE_ENV=production
CMD ["node", "dist/server.js"]
```

### Cloud Run Service + Deploy (with secrets, probes, scaling)
```yaml
# service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: order-service
  annotations:
    run.googleapis.com/launch-stage: GA
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "100"
        run.googleapis.com/cpu-throttling: "false"
        run.googleapis.com/startup-cpu-boost: "true"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      serviceAccountName: order-service@project-id.iam.gserviceaccount.com
      containers:
        - image: gcr.io/project-id/order-service:latest
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "2"
              memory: 1Gi
          env:
            - name: DB_CONNECTION
              valueFrom:
                secretKeyRef:
                  key: latest
                  name: db-connection-string
          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 3
```

```bash
gcloud run deploy order-service \
  --image gcr.io/$PROJECT_ID/order-service:$GIT_SHA \
  --region us-central1 \
  --service-account order-service@$PROJECT_ID.iam.gserviceaccount.com \
  --set-secrets "DB_URL=db-connection:latest" \
  --min-instances 1 --max-instances 100 \
  --cpu 2 --memory 1Gi \
  --concurrency 80 \
  --no-allow-unauthenticated
```

## BigQuery Optimization
```sql
-- Partition + cluster for cost/performance
CREATE TABLE `project.dataset.events`
PARTITION BY DATE(event_timestamp)
CLUSTER BY user_id, event_type
AS SELECT * FROM `project.dataset.raw_events`;

-- Always filter on partition key
SELECT event_type, COUNT(*) as cnt
FROM `project.dataset.events`
WHERE DATE(event_timestamp) BETWEEN '2025-01-01' AND '2025-01-31'
  AND event_type = 'purchase'
GROUP BY event_type;

-- Approximate for exploration; SELECT only needed cols
SELECT APPROX_COUNT_DISTINCT(user_id) as unique_users
FROM `project.dataset.events`
WHERE DATE(event_timestamp) = CURRENT_DATE();
```

## Pub/Sub Patterns (idempotency, ordering, exactly-once)
```python
from google.cloud import pubsub_v1
import json

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("project-id", "order-events")

def publish_event(event: dict, ordering_key: str = "") -> str:
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data, ordering_key=ordering_key, event_type=event["type"])
    return future.result(timeout=30)

# Subscriber with dedup + ack/nack
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("project-id", "order-events-sub")

def callback(message):
    try:
        event = json.loads(message.data.decode("utf-8"))
        if already_processed(message.message_id):
            message.ack(); return
        process_event(event)
        mark_processed(message.message_id)
        message.ack()
    except Exception as e:
        logger.error(f"Failed: {e}")
        message.nack()

subscriber.subscribe(subscription_path, callback=callback)
```

## IAM Best Practices
- Least-privilege service accounts per service.
- Use Workload Identity Federation for CI/CD (no long-lived keys).
- Prefer IAM Conditions + resource tags over broad roles.
- Audit logs always on for data-access + admin.

## Grok Integration (Production Contract)
- Primary pair: gcp-expert + backend-dev + devops agents.
- Fire on_infra_change, on_db_change, on_api_feature hooks when GCP resources or data flows change.
- Pre-Flight (mandatory for infra tasks): "Have we modeled cost at scale, secret injection, startup probes, IAM least-privilege, and rollback plan?"
- Ledger: record every infra change / secret rotation / schema evolution with task_id.
- Handoff: include service YAML diff, cost estimate, secret ref (no values), rollback command, SLO impact.
- Friction + compound: every "Cloud Run cold start killed latency SLO" or "BigQuery scan cost $X because no partition filter" → compound to evolve defaults, linter rules, or preflight checklists.
- Palace: store "chose Cloud Run + minScale=1 for this service because startup <3s required; rejected GKE because ops burden".
- Claim-verification: ALWAYS read actual deployed config / terraform plan / query profile before claiming "deploy safe", "cost optimized", or "no PII leak". Two-pass: hypothesize from grep → read_file actual resource definition → "X exists at service.yaml:42 ✓VERIFIED".
- Use with: aws-patterns (for multi-cloud), kubernetes-patterns (if GKE), sast-patterns (secret scanning), gdpr-compliance (data residency), test-enforcement (infra tests).

## When to Activate
- Any new GCP service, migration, or cost/perf review.
- In swarm Phase 2 (infra/backend tracks) and Phase 3 (review).
- Before deploys touching Cloud Run / BigQuery / Pub/Sub / IAM.
- When reviewing PRs with gcloud / terraform GCP changes.
- Pre-release (shipper + verifier).

## Quick Commands (Grok)
- Deploy: gcloud run deploy ... (use --set-secrets, never --set-env for secrets).
- Cost: gcloud billing budgets ... + BigQuery INFORMATION_SCHEMA.
- Debug: gcloud logging read + Cloud Trace.
- Integrate tldr for large IaC scans; layered-recall for prior GCP decisions.

See .grok/skills/aws-patterns/SKILL.md, kubernetes-patterns, backend-patterns, preflight, compound-learnings, memory-palace + layered-recall. Always verify with gcp-expert agent + real plan output. Production Contract requires ledger + handoff + preflight + friction capture on every non-trivial infra change.

Prioritize executable guards (probes, IAM conditions, partition filters, idempotency keys) over docs. Cost and security surprises are the #1 infra failure modes — catch them in preflight.
