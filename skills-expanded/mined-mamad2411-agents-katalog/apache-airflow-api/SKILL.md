---
name: apache-airflow-api
description: 'Execute Apache Airflow Stable REST API queries, manage DAGs, backfills, connections, variables, and assets. You MUST load this skill when interacting with the Airflow API.'
license: MIT
---

# apache-airflow-api

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- Querying, triggering, or managing DAGs and DAG Runs via the Airflow REST API.
- Managing Airflow Variables, Connections, Pools, or Assets autonomously.
- Extracting Task Instance logs, XCom entries, or execution statistics.
- Handling backfill operations (pause, unpause, cancel) programmatically.

## WHEN NOT TO USE

- When interacting with Airflow internal database directly (use standard SQL queries instead).
- When modifying DAG source files locally (use `python` or standard editing skills instead).
- When using Airflow UI-only endpoints (endpoints under `/ui` are subject to breaking changes).

## Core Process

1. **Authentication**: Determine the authentication method configured for the Airflow API (e.g., Basic Auth, OAuth2). For Basic Auth, use `--user <username>:<password>`.
2. **Endpoint Identification**: Identify the appropriate `/api/v2/` endpoint from the API mindmap or documentation.
3. **Payload Construction**: For `POST`, `PUT`, or `PATCH` requests, construct the correct JSON payload (e.g., `{"is_paused": true}`).
4. **Execution**: Use `curl` or a scripting tool (like Python's `requests`) to execute the API call. Include appropriate headers (e.g., `-H "Content-Type: application/json"`).
5. **Response Validation**: Ensure the response is HTTP `200`, `201`, or `204`. If `401` or `403`, verify credentials. If `422`, verify payload format.

## Best Practices

- **Stable Endpoints**: Always use the `/api/v2/` (or `/api/v1/` depending on the Airflow environment version) stable endpoints, avoiding `/ui` endpoints.
- **Filtering and Pagination**: Use `limit`, `offset`, and `order_by` query parameters when querying large collections like Task Instances or DAG Runs.
- **Dry Runs**: Use the `dry_run` endpoints (e.g., `/api/v2/backfills/dry_run`, `/api/v2/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/dry_run`) to validate operations before committing them.

## Mindmap of API Paths

The following mindmap outlines the structure of the Apache Airflow Stable REST API endpoints:

```mermaid
mindmap
  root(("Airflow API"))
    /api
      /v2
        /assets
          /aliases
            /{asset_alias_id}
          /events
          /{asset_id}
            /materialize
            /queuedEvents
        /auth
          /login
          /logout
        /backfills
          /dry_run
          /{backfill_id}
            /cancel
            /pause
            /unpause
        /config
          /section
            /{section}
              /option
                /{option}
        /connections
          /defaults
          /test
          /{connection_id}
        /dagSources
          /{dag_id}
        /dagStats
        /dagTags
        /dagWarnings
        /dags
          /{dag_id}
            /assets
              /queuedEvents
              /{asset_id}
                /queuedEvents
            /clearTaskInstances
            /dagRuns
              /list
              /{dag_run_id}
                /clear
                /hitlDetails
                /taskInstances
                  /list
                  /{task_id}
                    /dependencies
                    /dry_run
                    /externalLogUrl
                      /{try_number}
                    /links
                    /listMapped
                    /logs
                      /{try_number}
                    /tries
                      /{task_try_number}
                    /xcomEntries
                      /{xcom_key}
                    /{map_index}
                      /dependencies
                      /dry_run
                      /hitlDetails
                        /tries
                          /{try_number}
                      /tries
                        /{task_try_number}
                /upstreamAssetEvents
                /wait
            /dagVersions
              /{version_number}
            /details
            /favorite
            /tasks
              /{task_id}
            /unfavorite
        /eventLogs
          /{event_log_id}
        /importErrors
          /{import_error_id}
        /jobs
        /monitor
          /health
        /parseDagFile
          /{file_token}
        /plugins
          /importErrors
        /pools
          /{pool_name}
        /providers
        /variables
          /{variable_key}
        /version
```

## Common Pitfalls

- **Authentication Missing**: Forgetting to pass the bearer token or basic auth credentials, resulting in a `401 Unauthorized` response.
- **Incorrect Content Type**: Omitting `-H "Content-Type: application/json"` when executing `POST` or `PATCH` requests, which Airflow will reject.
- **URL Encoding Paths**: Forgetting to URL-encode variables, connection IDs, or DAG IDs that contain special characters.
- **Timezone Mismatches**: Airflow expects timestamps in strict ISO-8601 format (e.g., `2026-05-20T12:00:00Z`). Passing timezone-naive strings can cause validation errors.

## References

- [Apache Airflow Stable REST API Reference](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html)
