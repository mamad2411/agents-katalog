---
name: cloud-run
description: "Deploy and manage containerized workloads on Cloud Run. Covers service creation, traffic splitting, IAM, VPC connectivity, secrets integration, auto-scaling, and gcloud CLI patterns. Warns before billable deployments. Use when the user mentions: deploy to cloud run, create cloud run service, serverless container, scale cloud run, cloud run IAM, cloud run VPC, cloud run secrets, gcloud run."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "deploy to cloud run, create cloud run service, cloud run, serverless container, scale cloud run, cloud run IAM, cloud run VPC, cloud run secrets, gcloud run"
  "googlecloud-plugin/required-scopes": "run.services.create, run.services.delete, run.services.get, run.services.list, run.services.update, run.routes.invoke"
  "googlecloud-plugin/mcp-servers": "google-cloud-run"
---

# Cloud Run

Deploy and manage containerized applications on Google Cloud Run — fully managed, serverless, and scales to zero.

## Prerequisites

- `gcloud` CLI authenticated (`gcloud auth login` or ADC)
- Project set: `gcloud config set project PROJECT_ID`
- APIs enabled: `gcloud services enable run.googleapis.com`

## Core Patterns

### Deploy a container

```bash
# Billable action — confirm before running
gcloud run deploy SERVICE_NAME \
  --image IMAGE_URI \
  --region REGION \
  --platform managed \
  --no-allow-unauthenticated
```

### Grant invoker access (least-privilege)

```bash
gcloud run services add-iam-policy-binding SERVICE_NAME \
  --region REGION \
  --member="serviceAccount:SA@PROJECT.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
```

### VPC connector (private connectivity)

```bash
gcloud run services update SERVICE_NAME \
  --vpc-connector CONNECTOR_NAME \
  --region REGION
```

### Mount a secret

```bash
gcloud run services update SERVICE_NAME \
  --set-secrets=/path/to/secret=SECRET_NAME:latest \
  --region REGION
```

## Safety Rules

- Never use `--allow-unauthenticated` without explicit intent and gcp-security sign-off
- Always specify `--no-allow-unauthenticated` as the default
- Cost warning: Cloud Run bills per request and per CPU/memory allocated — estimate before deploying high-traffic services

## References

- [Cloud Run Overview](https://cloud.google.com/run/docs/overview/what-is-cloud-run)
- [Cloud Run IAM](https://cloud.google.com/run/docs/securing/managing-access)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Cloud Run General Development Tips](https://cloud.google.com/run/docs/tips/general)
- [gcloud run reference](https://cloud.google.com/sdk/gcloud/reference/run)
- [Cloud Run Release Notes](https://cloud.google.com/run/docs/release-notes)
