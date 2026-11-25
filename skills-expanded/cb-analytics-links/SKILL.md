---
name: cb-analytics-links
description: |
  Use this skill when the user is managing Analytics data-source links —
  S3, Azure Blob, GCS, or remote Couchbase links — including creating,
  updating, listing, or deleting them. Trigger when they mention "S3 link",
  "Azure Blob", "GCS link", "remote Couchbase link", "external dataset",
  "data source", "create_link", or credentials for any of those.
license: MIT
---

# Managing Analytics links

A *link* in Analytics connects external storage so it can be queried as a
dataset. The 5 tools cover the lifecycle: list, get, create, update, delete.

## Link types and their config

### S3
```json
{
  "type": "s3",
  "region": "us-east-1",
  "accessKeyId": "AKIA...",
  "secretAccessKey": "...",
  "serviceEndpoint": "https://s3.example.com",   // optional (MinIO, etc.)
  "sessionToken": "..."                          // optional (STS)
}
```

### Azure Blob
```json
{
  "type": "azureblob",
  "accountName": "myacct",
  "accountKey": "...",                  // OR sharedAccessSignature
  "sharedAccessSignature": "?sv=...",
  "endpoint": "https://blob.example.com"   // optional
}
```

### GCS
```json
{
  "type": "gcs",
  "jsonCredentials": "{...full service account JSON...}",
  // OR
  "applicationDefaultCredentials": true,
  "endpoint": "https://storage.googleapis.com"  // optional
}
```

### Remote Couchbase
```json
{
  "type": "couchbase",
  "hostname": "remote.example.com",
  "username": "analytics",
  "password": "...",
  "encryption": "full",            // none | half | full
  "certificate": "-----BEGIN ...",
  "clientCertificate": "...",      // optional mTLS
  "clientKey": "..."
}
```

## Credentials in audit logs

All of the above keys (accessKeyId, secretAccessKey, accountKey, jsonCredentials,
password, clientKey, etc.) are auto-redacted in the audit log. You can be
confident that passing credentials through `create_link` won't leave them in
the audit trail.

## Workflow

1. `list_links(dataverse="X")` — see what already exists; don't recreate.
2. `create_link(name, dataverse, config)` — create new.
3. `get_link(name)` — verify the type and active datasets.
4. `update_link(name, config)` — rotate credentials without recreating the
   datasets that point to it.
5. `delete_link(name)` — safe only when no datasets reference it; otherwise
   it returns a `RequestError`.

## Naming convention

The community convention is `<source>-<purpose>`, e.g. `s3-events`,
`azure-archive`, `cb-replica`. Stick to it for consistency.

## What to avoid

- Don't put credentials in source control. Always upsert them via the tool
  at deploy time, or read from a secrets manager.
- Don't switch a link's `type` via update; delete and recreate instead.
- Don't rotate credentials by deleting + recreating — use `update_link` so
  existing datasets stay attached.

## Rate limits & safety

Link tools split across categories:

- **`read`** (60/sec): `list_links`, `get_link`.
- **`write`** (1/sec, intentional): `create_link`, `update_link`,
  `delete_link`.

Link mutations are destructive — deleting a link with attached datasets
breaks downstream queries; updating credentials wrong takes ingestion
offline. The 1/sec write limit is deliberately constraining. If you're
batch-creating links from a config file, sequence the calls and accept
the throttling.

If `RateLimitExceeded` comes back from a `create_link` / `update_link` /
`delete_link`, honour `retry_after_sec`. Don't retry-storm — sleep for
the indicated duration, then continue.

`list_links` and `get_link` share the global `read` bucket with every
other read-only tool on the server. In a "show me everything about the
link landscape" workflow, prefer one `list_links` plus targeted
`get_link` calls over polling.

## Related skills

- `cb-analytics-schema` — once a link is connected and datasets exist, use this to discover their field shapes
- `cb-analytics-query` — querying data that arrives via links
- `cb-analytics-mcp-setup` — configuring the MCP server credentials (S3/Azure/GCS keys go in env vars, not inline)
