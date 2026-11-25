---
name: domino-data-sdk
description: Use the domino-data Python library (PyPI dominodatalab-data, import domino_data) for programmatic data access inside Domino executions. Covers DataSourceClient for SQL queries and object-store reads and writes against Domino Data Sources, DatasetClient for reading Domino Dataset files and snapshots, TrainingSets for versioned training DataFrames, and the Pinecone helpers in domino_data.vectordb. Use when querying a Data Source from Python, downloading Dataset files by API, creating or loading TrainingSet versions, or connecting a Pinecone client through a Domino Data Source.
compatibility: Domino 6.3 and Domino Cloud. Requires dominodatalab-data 6.7.4 or later (Python 3.10+). Designed for Domino executions, where the clients authenticate through DOMINO_API_PROXY and reach the Data Source proxy automatically; outside a run the proxy hosts are not normally reachable.
---

# Domino Data SDK (domino-data)

Applies to Domino 6.3 and Domino Cloud.

`dominodatalab-data` is the Python half of the Domino Data API. It talks to the Data Source
proxy that Domino injects into every execution, so the Data Source credentials stay with the
Data Source, managed by Domino, and never appear in code. Docs: https://docs.domino.ai/cloud/reference/api/data_api (same path under
`/6.3/`). Source: https://github.com/dominodatalab/domino-data. Requires
`dominodatalab-data>=6.7.4`; 6.7.4 needs Python 3.10 or later.

## Install

Pre-installed in Domino Standard Environments. In a custom environment Dockerfile:

```dockerfile
USER root
RUN python -m pip install "dominodatalab[data]" "dominodatalab-data>=6.7.4"
USER ubuntu
```

The `[data]` extra alone only requires `dominodatalab-data>=0.1.0`, so name the floor
explicitly or an older preinstalled copy stays.

Two import styles work: `from domino_data.data_sources import DataSourceClient` (the package)
or `from domino.data_sources import DataSourceClient` (python-domino re-exports it when the
`[data]` extra is installed; `domino.training_sets` exposes the client as `TrainingSetClient`).

## Modules

| Module | Purpose | Reference |
|---|---|---|
| `domino_data.data_sources` | `DataSourceClient`: SQL queries and object-store get/put on Domino Data Sources | [DATA-SOURCES.md](./DATA-SOURCES.md) |
| `domino_data.datasets` | `DatasetClient`: read files from a Domino Dataset or one of its snapshots | [DATASETS.md](./DATASETS.md) |
| `domino_data.training_sets.client` | TrainingSets: versioned DataFrames with key, target and monitoring columns | [TRAINING-SETS.md](./TRAINING-SETS.md) |
| `domino_data.vectordb` | Parameters that route the `pinecone` client through a Domino Data Source | [VECTORDB.md](./VECTORDB.md) |

The package also ships `domino_data.netapp_volumes`; the netapp-volumes skill covers that
storage type. Feature Store is not in this library and is not covered.

## Quick start

```python
from domino_data.data_sources import DataSourceClient

client = DataSourceClient()                        # auto-configured inside a Domino execution
ds = client.get_datasource("analytics-redshift")   # name as shown under Data > Data Sources
res = ds.query("SELECT customer_id, revenue FROM sales LIMIT 1000")
df = res.to_pandas()                               # or res.to_parquet("sales.parquet")

s3 = client.get_datasource("s3-datalake")          # object-store Data Source
keys = [o.key for o in s3.list_objects(prefix="raw/2026/", page_size=500)]
s3.download_file("raw/2026/events.parquet", "/tmp/events.parquet")
s3.put("outputs/summary.json", b'{"rows": 1000}')
```

```python
from domino_data.datasets import DatasetClient, DatasetConfig

dataset = DatasetClient().get_dataset("dataset-training-data-6503324fa1eb367359734bfd")
files = dataset.list_files(prefix="images/", page_size=1000)   # objects with .name
dataset.download("model.pkl", "/tmp/model.pkl", max_workers=8)
dataset.update(DatasetConfig(snapshot_id="<snapshot-id>"))    # read a snapshot, not live data
```

```python
from domino_data.training_sets import client as ts, model

version = ts.create_training_set_version(
    training_set_name="customer-churn",            # letters, digits, - and _ only
    df=df,
    key_columns=["customer_id"],
    target_columns=["churned"],
    monitoring_meta=model.MonitoringMeta(categorical_columns=["churned", "plan"]),
    description="Q3 features",
)
train_df = ts.get_training_set_version("customer-churn", version.number).load_training_pandas()
```

The UI generates copy-ready snippets for any Data Source or Dataset: **Data > Data Sources** (or
**Datasets**) > the item > **Code snippet**.

## Authentication

Inside a Workspace, Job, scheduled Job, Launcher or App (as the publisher) the clients authenticate on their own
from `token=` (if you pass one), `DOMINO_API_PROXY` (a short-lived JWT fetched from
`$DOMINO_API_PROXY/access-token`), `DOMINO_TOKEN_FILE` (if that file exists) and
`DOMINO_USER_API_KEY` (legacy API key, deprecated, never rely on it). The precedence differs
per call path; [DATA-SOURCES.md](./DATA-SOURCES.md) lists it. Hosts come from
`DOMINO_API_PROXY`, else `DOMINO_API_HOST`, plus `DOMINO_DATASOURCE_PROXY_HOST` and
`DOMINO_DATASOURCE_PROXY_FLIGHT_HOST` for the Data Source proxy; Domino injects all of them.

- **Domino endpoints (model APIs)** get no automatic token. Store a service-account token as
  an environment variable on the endpoint and pass it: `DataSourceClient(token=os.environ["DATA_API_TOKEN"])`
  (`token=`, not the deprecated `api_key=`).
- **Apps acting for the calling user**: pass the incoming request's bearer token,
  `DatasetClient(token=token)`, built per request. Without
  extended identity propagation that token covers only Dataset file reads and Data Source
  lookup by name. With no bearer or an empty one, answer 401; never pass `token=None`, which
  uses the publisher's credentials.
- **Outside Domino**: the Data Source proxy hosts are internal to the deployment, so run Data
  API code inside a Domino execution. If your admin exposes them, set `DOMINO_API_HOST` to the
  deployment URL, the two proxy host variables as the admin gives them, and pass `token=` a
  Personal Access Token (https://docs.domino.ai/cloud/reference/api/domino-api-authentication).

Docs: https://docs.domino.ai/cloud/reference/api/data_api/authentication.

## Errors

Exceptions raised by 6.7.4 (examples in the reference files):

- Client construction with no credential source, and `get_datasource` on a non-200: a bare
  `Exception` with the message.
- `query()`: `domino_data.data_sources.DominoError` for any Flight or Arrow failure, SQL and
  authentication errors included (401s are retried for up to 60 seconds first).
- `list_objects`, `get_key_url`, Dataset `list_files`/`get_file_url`:
  `domino_data.data_sources.UnauthenticatedError` after 60 seconds of 401s; bare `Exception`
  otherwise.
- Object and file transfers (`get`, `download*`, `put`, `upload*`): `httpx.HTTPStatusError`.
- TrainingSets: `ServerException`, `SchemaMismatchException`, `ValueError` for a bad name.

`domino_data.datasets` defines its own `DominoError` and `UnauthenticatedError` but nothing
raises them; catch the `data_sources` ones and `httpx.HTTPStatusError`.

## Practices

1. Reuse one client per process; every `get_datasource` call is an API round trip.
2. Use `page_size` on listings and `max_workers` on `download` for large objects (default 10).
3. `to_parquet` and `to_pandas` both materialise the whole result in memory (`to_parquet`
   keeps Arrow types); push filters and `LIMIT` into SQL for large results.
4. Override connection settings per session with the `*Config` classes and `reset_config()`
   instead of creating duplicate Data Sources.
5. Data Sources do not query nested objects; `UNNEST` in SQL first.
6. `DatasetClient` is read-only. Write to a Dataset through its mount path (domino-datasets
   skill), the UI, the CLI (domino-cli skill) or `POST /api/datasetrw` routes.
