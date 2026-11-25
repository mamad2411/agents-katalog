---
name: data-acquisition
description: |
  This skill should be used when the user mentions "dump database", "acquire data", "download dump", "extract records", "mongodump", "elasticdump", "mongoexport", "database dump", "data extraction", "redis dump", "couch dump", or discusses safely pulling data from an open database, converting database export formats, setting extraction limits, or monitoring dump progress. It routes data acquisition through dumper.js and pipeline.js.
---

# Data Acquisition

## Overview

Safely acquire data from confirmed open/unauthenticated databases. All acquisition follows a read-only, rate-limited approach with safety caps. Raw dumps are stored in the `dumps/` directory and registered in the acquisition tracker before any downstream processing.

## Pre-Acquisition Checklist

Before dumping any database:

1. Confirm source is classified as `open` in the source tracker
2. Verify the active hunt profile authorizes the acquisition scope
3. Ensure sufficient disk space for the estimated dump size
4. Note the target IP/port and database name

## Acquisition via dumper.js

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/dumper.js probe <url> [--service auto|mongo|elastic|redis|couch|mysql|postgres]
node ${CLAUDE_PLUGIN_ROOT}/scripts/dumper.js dump <url> --service <type> --source-id <source-tracker-id> [--timeout N]
```

This is a full-dump tool — it acquires all accessible data from the target. Probe first to estimate size before committing to a full dump.

## Post-Acquisition Registration

After a successful dump, register it in the acquisition tracker:

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/acquisition-tracker.js add \
  --source-id <source-tracker-id> \
  --file dumps/<filename> \
  --record-count <N> \
  --format <jsonl|csv|bson|json>
```

## Format Conversion

Convert raw dumps to normalized JSONL for downstream pipeline processing:

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/pipeline.js convert \
  --input dumps/<raw-file> \
  --output dumps/<target>-normalized.jsonl \
  --format <source-format>
```

Supported input formats: BSON, JSON array, CSV (auto-detect headers), NDJSON.

## Per-Database Acquisition Patterns

**MongoDB**: Use `mongoexport` for collection-level exports or `mongosh` for selective queries. Prefer JSONL output (`--type json --jsonArray false`).

**Elasticsearch**: Use scroll API for paginated extraction. `elasticdump` with `--type data --limit 1000` handles pagination automatically.

**Redis**: Use `KEYS *` followed by `GET` for small keyspaces. For large instances, use `SCAN` with cursor to avoid blocking. Export as JSON key-value pairs.

**CouchDB**: `GET /_all_docs?include_docs=true` for full database. Use `limit` and `skip` parameters for pagination.

**MySQL/PostgreSQL**: `mysqldump` / `pg_dump` for schema+data. Use `--no-create-info` for data-only exports.

## Additional Resources

- **`references/dumping-guide.md`** — Step-by-step database dumping for each supported type, safety limits, progress monitoring
- **`references/format-conversion.md`** — Format conversion reference: JSONL, CSV, JSON, SQL, BSON; encoding issues; data normalization
