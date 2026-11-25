---
name: domino-model-delivery
description: Deliver a Domino model outside a Domino endpoint. Covers batch scoring Jobs (a scoring script run once or on a schedule, results, notifications, the async endpoint alternative), the Model Export API (buildModelImage, exportImageToRegistry, build and export status and logs, .modelignore, running the exported image on your own Kubernetes), and the export targets NVIDIA Fleet Command (exportImageForNvidia) and Snowflake (Snowpark UDF), and SageMaker. Use when the user wants to batch-score a dataset or table with a trained model, run scoring on a schedule, export a model image out of Domino to a container registry from GitHub Actions, Jenkins or another CI/CD pipeline, push a model to NVIDIA Fleet Command or Snowflake, deploy a registered model to a SageMaker external endpoint, or asks about the Exports page. Not for deploying or updating a Domino-hosted endpoint, from CI/CD or otherwise; that belongs to domino-model-serving (REST) and domino-model-endpoints (UI).
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token. The Model Export routes (/v4/models) are non-public, documented per deployment, and may change in a future Domino version.
---

# Domino model delivery: batch scoring, model export, CI/CD

Applies to Domino 6.3 and Domino Cloud.

Ways to get predictions out of a trained model without serving it as a Domino endpoint.
Deploying or updating a Domino-hosted endpoint, including from CI/CD, is
[domino-model-serving](../domino-model-serving/SKILL.md) (REST) and
[domino-model-endpoints](../domino-model-endpoints/SKILL.md) (UI, monitoring), not this skill.

| Need | Path | Detail |
|---|---|---|
| Score a file, table or Dataset on demand or on a schedule, no latency SLA | **Batch scoring Job**: a Job that runs your scoring script | [BATCH-SCORING.md](./BATCH-SCORING.md) |
| Run the model in your own Kubernetes, staging and CI/CD pipeline | **Model Export API**: Domino builds the endpoint image, pushes it to your registry, you deploy it | [EXPORT-API.md](./EXPORT-API.md) |
| Run the model on NVIDIA edge devices or inside Snowflake | **Export targets**: Fleet Command image plus Helm chart; Snowpark UDF | [EXPORT-TARGETS.md](./EXPORT-TARGETS.md) |
| Serve on Amazon SageMaker | Deployment targets (Public API) or the legacy SageMaker image export | [EXPORT-TARGETS.md](./EXPORT-TARGETS.md#amazon-sagemaker) |

## Authentication

Base URL and credential per context: [domino-api-intro](../domino-api-intro/SKILL.md#authentication).
Legacy API keys (`X-Domino-Api-Key`) are deprecated; send a Bearer token.

## Batch scoring in one screen

1. Write a scoring script (for example `score.py`) that loads the model, reads the input (a
   mounted Dataset, a Data Source, or a project file) and writes predictions to a file.
2. Run it as a Job: **Jobs > Run** in the UI, or
   `POST $BASE/api/jobs/v1/jobs` with `{"projectId", "runCommand": "python score.py", "environmentId", "hardwareTier"}`
   ([domino-jobs](../domino-jobs/SKILL.md)).
3. Schedule it: **Jobs > Schedules > Schedule a Job** (**Notify emails**, **Update Domino endpoint**)
   or `POST /v4/projects/{projectId}/scheduledjobs` (non-public route; may change in a future Domino version;
   `publishModelId` = that endpoint): [SCHEDULED-JOBS.md](../domino-jobs/SCHEDULED-JOBS.md).
4. Collect results: files the Job added or changed are its results. Poll
   `GET $BASE/api/jobs/beta/jobs/{jobId}` until `status.isCompleted`, then read
   `commitDetails.outputCommitId` and fetch a file with
   `GET $BASE/api/projects/v1/projects/{projectId}/files/{commitId}/{path}/content`.

Too slow? Attach a Spark, Ray or Dask cluster
([domino-distributed-computing](../domino-distributed-computing/SKILL.md)). Long single
predictions that need request/response semantics: an **asynchronous endpoint**
(`POST /api/modelApis/async/v1/{asyncModelId}`, Public API), see BATCH-SCORING.md.

## Model Export API in one screen (CI/CD)

Every `/v4/models/...` call in this skill, the five below and the NVIDIA and Snowflake exports,
is a **non-public route; may change in a future Domino version**. Docs:
https://docs.domino.ai/cloud/platform-capabilities/features/models/integrate-ci-cd-workflows
and each cluster's `https://<domino-domain>/docs`.

```text
POST /v4/models/buildModelImage                                   -> {modelId, modelVersionId}
GET  /v4/models/{modelId}/{modelVersionId}/getBuildStatus         -> status: Preparing | Building | Complete | Failed
POST /v4/models/{modelId}/{modelVersionId}/exportImageToRegistry  -> {exportId, status}
GET  /v4/models/{exportId}/getExportImageStatus                   -> status (terminal: complete | failed)
GET  /v4/models/{exportId}/getExportLogs                          -> logs
```

Public API complement (both specs): `GET /api/modelServing/v1/modelApis/{modelApiId}/versions/{modelApiVersionId}/exportLogs`.

python-domino ([domino-python-sdk](../domino-python-sdk/SKILL.md)) wraps export, status and logs
but not the build call. Request bodies, a pipeline script with a GitHub Actions job, the
Kubernetes manifests, the test call, `.modelignore` and the python-domino method map:
[EXPORT-API.md](./EXPORT-API.md).

## Export targets in one screen

- **NVIDIA Fleet Command** (beta): `POST /v4/models/{modelId}/{modelVersionId}/exportImageForNvidia`
  (non-public route; may change in a future Domino version) with NGC container and Helm repositories,
  a semver Helm version and an NGC API key; the edge port is hardcoded to 30008.
- **Snowflake**: published from the UI as a Snowpark UDF (Python 3.8, root `requirements.txt`
  limited to the Snowflake Anaconda channel, type-hinted predict function); **Push new version**
  re-exports the project HEAD.
- **SageMaker**: an admin creates a deployment target (`/api/admin/v1/deploymentTargets`, Public
  API), then **Endpoints > External > Create external endpoint** or
  `POST /api/modelServing/v1/modelDeployments`; AWS EKS control plane only. The
  `exportImageForSagemaker` image export is the alternative.
- **Exports page** lists every export with target `Sagemaker`, `NvidiaFleetcommand`, `Snowflake`
  or `Domino`; `GET /v4/modelManager/getModelExports/{projectId}` (non-public route; may change in a future Domino version).

## Pitfalls

- Build first, export second: the model version's build must reach `Complete`.
- The NVIDIA export fails when the image tag or Helm chart version already exists in NGC; derive
  tags from the version so re-runs never collide.
- Export bodies carry registry, NGC or Snowflake credentials in plain JSON; JSON-encode them from
  the environment, never splice or commit them.
- The build body requires `logHttpRequestResponse`; send `false` unless payload logging is wanted.
- Every project file goes into the image unless listed in `.modelignore`; exported images and
  UDFs cannot reach Domino-only assets (Datasets, Data Sources, the API proxy) at inference time.

## Related skills

- [domino-jobs](../domino-jobs/SKILL.md): Job bodies, logs, scheduled Jobs, script patterns
- [domino-model-serving](../domino-model-serving/SKILL.md), [domino-model-endpoints](../domino-model-endpoints/SKILL.md): endpoints
- [domino-model-monitoring](../domino-model-monitoring/SKILL.md): drift and quality for exported models
- [domino-api-intro](../domino-api-intro/SKILL.md): hosts, pagination, errors
