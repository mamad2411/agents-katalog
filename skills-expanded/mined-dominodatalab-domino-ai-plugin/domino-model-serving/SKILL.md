---
name: domino-model-serving
description: Automate Domino endpoints (Model APIs) and registered models over REST. Covers the /api/modelServing/v1 lifecycle (create an endpoint from a file or a registered model, add versions, poll deployment status, list, update replicas or hardware tier, archive, build and instance logs), registered models v1 vs v2 routes, MLflow tracking vs the registry API, management URL vs prediction URL, and sync Basic vs async Bearer prediction auth. Use when scripting deployments from CI, a Job or a notebook, registering a model version by API, or debugging stop, archive and delete behaviour. For UI publishing, the predict function, scaling and health settings use domino-model-endpoints; for drift and quality monitoring use domino-model-monitoring; for exporting a model out of Domino (image to your registry, NVIDIA Fleet Command, Snowflake UDF, SageMaker) or batch scoring Jobs use domino-model-delivery.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token or service-account token. The modelServing beta visibility and collaborator routes exist only on Domino Cloud.
---

# Domino model serving (REST)

Applies to Domino 6.3 and Domino Cloud.

Programmatic lifecycle for Domino endpoints (**Model APIs** in the API) and registered models. UI publishing, the prediction function, scaling and endpoint health are in `domino-model-endpoints`. Worked requests for every step: [LIFECYCLE.md](./LIFECYCLE.md); route catalog: [API-MODEL-SERVING.md](../domino-python-sdk/API-MODEL-SERVING.md).

## Authentication and base URL

[domino-api-intro](../domino-api-intro/SKILL.md#authentication). Legacy API keys are deprecated; do not use them.

Connectivity check: `GET /api/modelServing/v1/modelApis?limit=1` returns 200.

## Three surfaces (do not mix them)

| Surface | Base path | Purpose |
|---------|-----------|---------|
| Model Serving | `/api/modelServing/v1/modelApis` | Endpoints: create, versions, list, update, archive, logs |
| Registered models | `/api/registeredmodels/v2` (list, register); `/api/registeredmodels/v1/{modelName}` (get, patch, versions) | Registry records; `modelName` is the name, not an id |
| MLflow tracking | `MLFLOW_TRACKING_URI` in a run; `/api/2.0/mlflow/...` on the deployment URL with a bearer token | Experiments, runs, artifacts, the MLflow registry client |

MLflow logging or registration deploys nothing; deployment is a Model Serving call.

## Management URL vs prediction URL

Management calls go to the base above under `/api/...`. Predictions go to the deployment URL: `/models/{modelApiId}/latest/model` (sync, Basic auth) or `/api/modelApis/async/v1/{modelApiId}` (async, Bearer). The `ModelApi` object has no `url` field; build the prediction URL from its `id` and the deployment URL shown on the endpoint's Overview tab.

## Lifecycle

1. Train and, optionally, register (`POST /api/registeredmodels/v2`, or the MLflow client).
2. `POST /api/modelServing/v1/modelApis` with `name`, `description`, `environmentId`, `isAsync`, `strictNodeAntiAffinity`, `environmentVariables`, `version{projectId, source, logHttpRequestResponse, monitoringEnabled}`; `source.type` is `File` (`file`, `function`) or `Registry` (`registeredModelName`, `registeredModelVersion`). Optional `hardwareTierId`, `replicas`.
3. Poll the version: `GET .../modelApis/{modelApiId}/versions/{modelApiVersionId}` until `deployment.status` is `Running` and `isPending` is false (absent `deployment` means pending), then confirm `activeVersion.id` on the Model API. `Running` is not health: fetch `.../instanceLogs?maxResults=3000` (no `tail`), keep `model-` container lines, expect `WSGI app 0 (mountpoint='') ready` (`no app loaded. GAME OVER` is a crash loop), then one test prediction. Sync or commit before step 2 and pin `version.commitId`; the head lags uploads by seconds.
4. New code: `POST .../modelApis/{modelApiId}/versions` (same `version` fields plus `shouldDeploy: true`). Poll that version, not the Model API; the old one stays active until the new one runs.
5. Change replicas, hardware tier, name or environment: `PUT .../modelApis/{modelApiId}` (`name`, `description`, `replicas`, `environmentId` required; send current values back, including `resourceQuotaId`). Scale changes need a restart: UI, or internal `stopModelDeployment` then `startModelDeployment` (LIFECYCLE.md).
6. Retire: stop the running version first (UI **Versions** > **Actions**, or `POST /v4/models/{modelApiId}/{versionId}/stopModelDeployment` with `{}`; non-public route; may change in a future Domino version), then `DELETE .../modelApis/{modelApiId}`: 500 while a version runs; after success `GET` is 404 and the endpoint leaves all lists.
7. Verify each mutation with a `GET`; 2xx means accepted, not applied.

Logs: `GET .../versions/{modelApiVersionId}/buildLogs`, `exportLogs`, `instanceLogs`.

`/api/modelServing/v1/modelDeployments` (with `start`, `stop`, `credentials`, `logs`, `versions`) is a separate entity: a registered model deployed onto an admin-defined external deployment target, SageMaker only. It is not a Model API; see [domino-model-delivery](../domino-model-delivery/EXPORT-TARGETS.md#amazon-sagemaker).

## Registered models

- List: `GET /api/registeredmodels/v2?projectId=&searchPattern=&maxResults=` (token-paginated with `pageToken`). Register: `POST /api/registeredmodels/v2` (`modelName`, `modelSource{sourceType, mlflowSource|huggingFaceSource}`, `create`). `POST /api/registeredmodels/v1/{modelName}/versions` is deprecated.
- Get and patch: `GET|PATCH /api/registeredmodels/v1/{modelName}` (`PATCH` takes `description` and `discoverable`; `GET` returns neither `discoverable` nor aliases); versions at `/api/registeredmodels/v1/{modelName}/versions/{version}`; endpoints serving a version at `.../versions/{version}/modelapis`.
- Aliases and tags are MLflow features: the MLflow client on `MLFLOW_TRACKING_URI`, or `/api/2.0/mlflow/registered-models/...` on the deployment URL; see `domino-experiment-tracking`.

## Prediction auth

Restricted **sync** endpoints require HTTP Basic with the endpoint access token as username and password. **Async** endpoints require `Authorization: Bearer <token>`. Unrestricted endpoints need neither. Tokens: the user's, or create one (`domino-model-endpoints` DEPLOY-ENDPOINT.md); never print it. Source: https://docs.domino.ai/cloud/platform-capabilities/features/model-deployment/domino-endpoint-authorization.

## Which path applies

```bash
curl -s "$DOMINO_API_HOST/version"   # "version": "6.3.x" self-managed; "6.4.x" or later on Domino Cloud
```

Domino Cloud adds `/api/modelServing/beta/modelApis/{modelApiId}/visibility` (`Public`, `Discoverable`, `Private`), `.../access` and `.../collaborators` (roles `Owner`, `Editor`, `Operator`, `Viewer`); not on 6.3, where you set them in the UI (**Settings** > **Access and Sharing**).

## Related

- [LIFECYCLE.md](./LIFECYCLE.md): request and response examples for each step
- [API-MODEL-SERVING.md](../domino-python-sdk/API-MODEL-SERVING.md), [API-MODELS.md](../domino-python-sdk/API-MODELS.md)
- [domino-model-endpoints](../domino-model-endpoints/SKILL.md): UI, predict code, scaling, health, logs
- [domino-model-delivery](../domino-model-delivery/SKILL.md): model export, SageMaker, batch scoring
- Route discovery: [API-SPECS.md](../domino-api-intro/API-SPECS.md)
- Model registry: https://docs.domino.ai/cloud/platform-capabilities/features/models/register-and-govern/model-registry
