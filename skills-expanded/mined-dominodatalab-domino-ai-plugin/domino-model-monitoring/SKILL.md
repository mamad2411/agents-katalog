---
name: domino-model-monitoring
description: Monitor production models in Domino for data drift and model quality. Covers the two workflows (integrated monitoring for Domino endpoints with prediction capture, and Model Monitor for models served elsewhere), the DataCaptureClient prediction-capture library, registering training sets, prediction data and ground truth with the Monitoring Config JSON, drift tests and thresholds, scheduled checks and notifications, where captured predictions live, remediation, and the Model Monitoring REST API including custom metrics. Use when setting up monitoring for an endpoint, registering an external model, ingesting ground truth, reading drift or quality results by API, or automating retraining on drift.
compatibility: Domino 6.3 and Domino Cloud. Model Monitoring API calls use the same bearer authentication as other Domino APIs (DOMINO_API_PROXY or the localhost:8899 access token in a run; PAT or service account outside). Integrated endpoint monitoring is not available for endpoints on remote data planes.
---

# Domino model monitoring

Applies to Domino 6.3 and Domino Cloud.

Serving metrics (CPU, latency, status codes) are in `domino-model-endpoints`; this skill is drift and quality. Reference files: [PREDICTION-CAPTURE.md](./PREDICTION-CAPTURE.md) (endpoint instrumentation, captured data, remediation) and [MONITORING-API.md](./MONITORING-API.md) (routes, config JSON, custom metrics).

## Two workflows

| Model runs as | Workflow | Data handling |
|---------------|----------|---------------|
| Domino endpoint | Integrated endpoint monitoring | Domino captures predictions into a project Dataset; you register a TrainingSet and, optionally, ground truth |
| App, Launcher, Job, or outside Domino | Model Monitor | You connect a data source (S3, generic S3, Azure Blob or Data Lake, GCS, HDFS, NFS, Snowflake) and register training, prediction and ground-truth files with a Monitoring Config JSON |

Prefer deploying as a Domino endpoint: integrated monitoring captures predictions into the project Dataset automatically, with no external data source. The Model Monitor data-source path (S3, Snowflake and the others above) is the exception: models served as an App, Launcher or Job or outside Domino, and ground-truth files. Both show up in **Model Monitor** as one list. Endpoint monitoring is not supported for endpoints deployed to a remote data plane.

## Set up monitoring for a Domino endpoint

1. **Instrument the predict function** with `DataCaptureClient` from `domino_data_capture` (in Domino Standard Environments; otherwise `pip install domino-data-capture` in the environment Dockerfile). Call `capturePrediction(feature_values, predict_values, event_id=..., timestamp=...)` on every request. Full example in [PREDICTION-CAPTURE.md](./PREDICTION-CAPTURE.md).
2. **Publish the endpoint.** Captured rows land hourly as Parquet in the project Dataset `prediction_data`; nothing is analysed yet.
3. **Register training data** for drift. The model must have been trained from a Domino TrainingSet in the same project (https://docs.domino.ai/cloud/reference/api/data_api/trainingsets_usecases/create_trainingset). On the endpoint open **Grafana Monitoring** > **Configure Monitoring** > **Data**, pick the Training Set and version, choose **Classification** (categorical target) or **Regression** (numerical target), save.
4. **Validate**: **Configure Monitoring** > **Target Ranges** shows a populated tests-and-thresholds table once captured predictions have been processed.
5. **Ground truth** (model quality): predictions need a row identifier (the `event_id` you capture); register a ground-truth file carrying the same identifiers with a config JSON (`variableType: ground_truth`, `forPredictionOutput`) under **Model Monitor** > model > **Model Quality** > **Register Ground Truth**, or by API. **Ingest History** shows `Done` when loaded.
6. **Schedule and notify**: **Configure Monitoring** > **Schedule** (name, frequency, "new data since last check" or "data since last N days") and **Alert Recipients** (comma- or semicolon-separated emails) for breach emails.

## Set up Model Monitor for an external model

1. Environment: `domino-data-capture` and `dominodatalab[data]` (Python); R needs `DominoDataCapture`.
2. Connect the data source holding your files: https://docs.domino.ai/cloud/platform-capabilities/features/monitoring/4-set-up-model-monitor/2-connect-a-data-source.
3. **Model Monitor** > **Register Model** > **Upload Model Config File**: JSON with `variables` (`feature` columns, one `prediction`, optional `timestamp` and `row_identifier`), `datasetDetails` (the training file) and `modelMetadata` (`name`, `modelType` classification or regression, `version`).
4. **Data Drift** > **Register Prediction** with a config whose `datasetDetails` point at the prediction file. With a `timestamp` variable Domino re-ingests new rows daily at 00:00 UTC; without it each batch needs a new registration (re-registering the same file ingests rows twice).
5. **Model Quality** > **Register Ground Truth**, then **Schedule** and notifications as above.

## Drift and quality

- Tests: Kullback-Leibler divergence (recommended default), Chi-square (categorical), Population Stability Index (PSI < 0.1 no change, < 0.2 moderate, >= 0.2 significant). Per-feature test, acceptable range and threshold are set on the model's **Data Drift** page (Model Monitor) or **Target Ranges** (endpoint); **Other Actions** > **Save Checks Config** makes them the defaults for scheduled checks; global defaults under **Settings** > **Test Defaults**.
- Scheduled drift checks run daily at noon UTC by default and analyse data through 23:59 of the previous day.
- Quality metrics: classification gives accuracy, precision, recall, F1, AUC-ROC, log loss, normalized Gini and a confusion matrix; regression gives MSE, MAE, MAPE, R2 and normalized Gini. AUC, log loss and Gini need `prediction_probability`; Gini also uses `sample_weight`. Ground truth is matched to predictions by the row identifier among labels ingested in the last 90 days.
- Mute a feature or metric with the bell icon to keep it out of scheduled-check alerts.

## Captured prediction data

Hourly Parquet files in the `prediction_data` Dataset: `/mnt/data/prediction_data/<model_version_id>/...` in Git-based projects, `/domino/datasets/local/prediction_data/<model_version_id>/...` in DFS projects. A daily job deletes files older than 30 days by default. Capture is sized for 8 GB per endpoint per 24 hours. Do not rename the generated files.

## Remediate

1. From the alert, open the model's drift or quality page and the Cohort Analysis report to find the failing cohorts.
2. On the endpoint click **Open in Workspace**: Domino opens a Workspace on a new branch at the published commit, with `prediction_data` available.
3. Fix the code or retrain on recent predictions plus labels; publish a new endpoint version (`domino-model-endpoints`).
4. To automate, a scheduled Job reads check results by API ([MONITORING-API.md](./MONITORING-API.md)) and starts retraining with `POST /api/jobs/v1/jobs` (`domino-jobs`).

## Troubleshooting

| Message or symptom | Cause |
|--------------------|-------|
| Monitoring is not enabled | No capture client in `predict()`, no training set registered, or the first scheduled check has not run yet |
| Waiting for data | Nothing processed yet; **Target Ranges** > **Date Filter** > Today shows arrivals |
| Selected training set version cannot be used | The TrainingSet version has no schema, is empty, or its target type does not match the chosen model type |
| `no package called 'DominoDataCapture'` or an import error | The environment lacks the capture library; use a Domino Standard Environment or install it |

## Documentation

- https://docs.domino.ai/cloud/platform-capabilities/features/monitoring/index (workflows, setup, config JSON, APIs, remediation, troubleshooting)
