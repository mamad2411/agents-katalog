---
name: vertex-ai
description: "Build and deploy ML models and generative AI workloads — models, prompts, tuning and endpoints — on Vertex AI. Covers Model Garden, the Gemini API, custom training, endpoint deployment, and IAM. Warns before deploying endpoints (billable). Integrates with Vertex AI MCP server. Use when the user mentions: Gemini on GCP, vertex endpoint, generative AI GCP, vertex training, PaLM, vertex AI pipeline. Use this for models, training and endpoints; use agent-architect instead for anything agentic — Agent Builder, ADK, Agent Runtime, A2A, AP2 and multi-agent topologies all belong there, not here."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "vertex AI, Gemini on GCP, model garden, deploy ML model, vertex endpoint, generative AI GCP, agent builder, vertex training, PaLM, Gemini API, vertex AI pipeline"
  "googlecloud-plugin/required-scopes": "aiplatform.endpoints.create, aiplatform.endpoints.get, aiplatform.endpoints.predict, aiplatform.models.get, aiplatform.models.list, aiplatform.trainingPipelines.create, aiplatform.trainingPipelines.get"
  "googlecloud-plugin/mcp-servers": "google-vertex-ai"
---

# Vertex AI

Unified ML platform for training, deploying, and serving models — including Gemini, generative AI, and custom models.

> **Naming currency:** the platform was renamed to the **Gemini Enterprise Agent Platform (GEAP)** at Next '26 (2026-04-22). The rebrand is branding-only — `vertex-ai` persists in gcloud groups, SDK imports, API hostnames, Terraform resources, and doc URLs, so this skill keeps them. For **agentic** system design (ADK, Agent Runtime, multi-agent, MCP/A2A/AP2, agent evaluation), route to `agent-architect`; this skill covers platform/model mechanics.

## Key Products

| Product | Use |
|---------|-----|
| Gemini API on Vertex | Production-grade Gemini access with data governance |
| Model Garden | Browse and deploy 150+ models (Gemini, Llama, etc.) |
| Custom Training | Train on managed infrastructure (GPUs/TPUs) |
| Vertex AI Endpoints | Serve predictions from deployed models |
| Agent Builder | Build conversational agents on Vertex |
| Vertex AI Pipelines | Orchestrate ML workflows (Kubeflow Pipelines) |

## Core Patterns

### Call Gemini via Vertex (Python)

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="PROJECT_ID", location="us-central1")
model = GenerativeModel("gemini-2.0-flash-001")
response = model.generate_content("Explain Cloud Run in one sentence.")
print(response.text)
```

### Deploy an endpoint (billable — confirm first)

```bash
# Billable: endpoints charge per node-hour when deployed
gcloud ai endpoints create \
  --display-name=ENDPOINT_NAME \
  --region=REGION \
  --project=PROJECT_ID
```

### Grant Vertex AI access (least-privilege)

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA@PROJECT.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

## Safety Rules

- Endpoints incur cost even when idle — undeploy when not needed
- Use `roles/aiplatform.user` for inference; `roles/aiplatform.admin` only for platform admins
- Cost warning: GPUs and TPUs are expensive — confirm instance type and count before training

## References

- [Vertex AI Overview](https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform)
- [Generative AI on Vertex](https://cloud.google.com/vertex-ai/generative-ai/docs/overview)
- [Vertex AI IAM](https://cloud.google.com/vertex-ai/docs/general/access-control)
- [Model Garden](https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models)
