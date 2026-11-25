---
name: domino-model-endpoints
description: Publish and call Domino endpoints (model APIs) for synchronous or asynchronous predictions. Covers the prediction function and request JSON, how the endpoint image is built (environment, required packages, no requirements.txt), sync Basic-auth vs async Bearer invocation, versions and routing, instance counts and endpoint hardware tiers, health checks, metrics and logs. Use when deploying a model as an API from the UI, writing predict code, calling an endpoint, or debugging a slow or failing endpoint. For scripted lifecycle automation over REST (create, version, archive, logs) use domino-model-serving; for drift and model-quality monitoring use domino-model-monitoring; for batch scoring Jobs and for exporting a model out of Domino (an image to your registry, NVIDIA Fleet Command, a Snowflake UDF, SageMaker) use domino-model-delivery.
compatibility: Domino 6.3 and Domino Cloud. Management calls need DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token. Prediction calls use the endpoint's own access token.
---

# Domino endpoints (model APIs)

Applies to Domino 6.3 and Domino Cloud.

A Domino endpoint (**Model API** in the API) wraps a function from your project in an HTTP API: Domino builds an image from the selected compute environment plus the project files, adds a Flask (Python) or Plumber (R) harness, sources your script once at publish time, and routes each request to your function.

## Which skill

| Need | Skill |
|------|-------|
| UI publish, predict function, calling, instances, health, logs | this skill |
| REST lifecycle: create, version, list, delete, logs, registered models | `domino-model-serving` |
| Drift, model quality, prediction capture | `domino-model-monitoring` |
| Batch scoring with a Job; export the model out of Domino (image to your registry or Kubernetes, NVIDIA Fleet Command, Snowflake UDF, SageMaker) | [domino-model-delivery](../domino-model-delivery/SKILL.md) |

## Reference files

| File | Use when |
|------|----------|
| [DEPLOY-ENDPOINT.md](./DEPLOY-ENDPOINT.md) | Predict function, sync before publish, API and registry publish, health check, calling, versions, access |
| [SCALING.md](./SCALING.md) | Instance count, endpoint tiers, routing modes, parallelism |
| [MONITORING.md](./MONITORING.md) | CPU, memory, status codes, health checks, timeouts, logs |

## Packaging rules (what breaks publishes)

- The environment is chosen per endpoint (`environmentId` is required by the API). Python endpoints need `uwsgi`, `flask`, `six` and `prometheus-client`; async ones also `seldon-core`. Domino Standard Environments ship them (the minimal image lacks `seldon-core` and `mlflow`).
- Endpoint hosts do **not** read `requirements.txt` or run environment setup scripts; put packages in the environment's Dockerfile instructions. Exception: a registry model's MLflow-inferred `requirements.txt` is installed at build.
- Project environment variables are not inherited; set endpoint variables under **Settings** and restart running versions.
- The image is built from the Project's **committed** files, never the Workspace disk: DFS, **File Changes** > **Sync to Domino** first; Git-based, commit and push the code and sync artifacts. Include every file the function loads and pin that commit (`version.commitId`): the head lags an upload by seconds, and a missing file crash-loops the container with `FileNotFoundError` ("Sync or commit first", DEPLOY-ENDPOINT.md). Files mount at `/mnt/<username>/<project_name>` (`DOMINO_WORKING_DIR`); `.modelignore` excludes files; images over 500 MB fail. New files need a new version.
- The endpoint runs as uid/gid 12574; the image build runs as the Dockerfile's last `USER`.

## Quick start

Sources: a project-file prediction function (pickle path below) or a **Model Registry** version.

```python
# model.py (project root)
import pickle
_model = pickle.load(open("model.pkl", "rb"))   # runs once, when the version starts

def predict(sepal_length, sepal_width, petal_length, petal_width):
    pred = _model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
    return {"variety": str(pred[0])}            # JSON-serializable: no NumPy types
```

Registry path: `mlflow.sklearn.log_model(model, "model", signature=sig, input_example=X[:5], registered_model_name="iris-rf")` in a run (or **Register model from run** in Experiments), then pick that model and version in **Create Domino Endpoint**; by API `version.source = {"type": "Registry", "registeredModelName": "iris-rf", "registeredModelVersion": 1}`. Domino installs the MLflow-inferred `requirements.txt` (DEPLOY-ENDPOINT.md; `domino-experiment-tracking` MODEL-REGISTRY.md).

1. Sync or commit `model.py` and `model.pkl` (packaging rules), then go to **Deployments** > **Endpoints** > **Create Domino Endpoint**.
2. Name, description, the file (`model.py`) and function (`predict`), or the registered model and version.
3. Pick the compute environment, instance count and endpoint hardware tier (SCALING.md).
4. **Request Type**: **Sync** (real-time) or **Async** (long-running; payloads by reference).
5. Publish, wait for **Running**, then confirm health: a **Tester** request succeeds, or the model container logs `WSGI app 0 (mountpoint='') ready` (a crash loop also reports `Running`). The **Overview** tab shows the URL, model ID and code samples.

## Calling an endpoint

Restricted endpoints need an access token (**Settings** > **Invocation**); sync and async authenticate differently:

```bash
# Sync: HTTP Basic, the token as username and password
curl -s -u "$MODEL_API_TOKEN:$MODEL_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"data": {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}}' \
  "$DEPLOYMENT_URL/models/$MODEL_ID/latest/model"

```

Async endpoints use `Authorization: Bearer $MODEL_API_TOKEN` at `.../api/modelApis/async/v1/$MODEL_ID` and return an `asyncPredictionId` to poll.

`DEPLOYMENT_URL` is the deployment's external URL (the one you sign in at; no API field or in-run variable holds it, and in-run hosts do not route `/models/...`) and `MODEL_ID` the endpoint id; both are on the Overview tab. The token: use the one the user supplies, otherwise create one and store it as a Domino environment variable without ever printing it (DEPLOY-ENDPOINT.md "Access tokens"); your own Domino token gets 401 even on a Public endpoint. Never put the token in browser code.

## Versions and routing

Each publish creates a version. **Basic** routing (default) points `/models/<modelId>/latest/model` at the newest successful version and stops the old one; **Advanced** adds a promoted version at `/models/<modelId>/labels/prod/model` so clients stay on production while you test `latest` (**Settings** > **Deployment**). A scheduled Job can redeploy on fresh data via **Update Domino Endpoint**.

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Build fails on an import | Put the package in the environment Dockerfile, not `requirements.txt` |
| `IOException ... 500` in the build log | Image over 500 MB; add large files to `.modelignore` |
| 401 on predictions | Sync: Basic auth with the endpoint token; async: Bearer; user tokens and PATs never work |
| `Running` but 503, or `Running` / `Starting` alternating | Crash loop; model-container logs (no `tail`, `maxResults=3000`) show `FileNotFoundError` ... `no app loaded`. Sync, pin the commit, republish |
| 504 | Request timeout (default 60 s) under **Settings** > **Advanced**; restart after changing |
| Not Running | Build, export, instance logs (**Logs** column); health-check settings |

## Documentation

- https://docs.domino.ai/cloud/platform-capabilities/features/model-deployment/index
- Route discovery: [API-SPECS.md](../domino-api-intro/API-SPECS.md)
