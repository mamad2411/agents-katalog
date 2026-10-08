# logtap

Ephemeral log capture and incident triage for Kubernetes — tap in, grab logs, triage, tap out.

## Install

```bash
brew install ppiankov/tap/logtap
```

## Conventions

- **JSON output**: Use `--json` or `--format json` (both accepted) for machine-readable output
- **Exit codes**: See table below — non-zero exit codes are structured
- Commands that already have `--format` for other purposes (grep, export) use their own format values

## Commands

### logtap init

Initialize logtap configuration. Creates `~/.logtap/config.yaml` with commented defaults if it does not exist.

**Flags:**
- `--json` / `--format json` — JSON output

**JSON output:**
```json
{"config_path": "/home/user/.logtap/config.yaml", "created": true, "local_path": ".logtap.yaml", "local_found": false}
```

### logtap recv

Start log receiver (local or in-cluster).

**Flags:**
- `--dir` — output directory for captured logs
- `--max-disk` — max total disk usage
- `--redact` — enable PII redaction
- `--headless` — disable TUI

### logtap tap

Inject log-forwarding sidecar.

**Flags:**
- `--deployment` — target deployment name
- `--target` — receiver address
- `--dry-run` — show diff without applying
- `-n, --namespace` — Kubernetes namespace

### logtap untap

Remove sidecar.

**Flags:**
- `--deployment` — target deployment name

### logtap triage

Scan captured logs for anomalies and produce report. Safe to run on live captures — skips rotated files and catches up on new files added during the scan.

**Flags:**
- `--json` — output as JSON to stdout
- `--html` — generate HTML report
- `--out` — output directory for triage artifacts
- `--jobs` — parallel scan workers
- `--window` — histogram bucket width (default 1m)
- `--top` — number of top error signatures (default 50)
- `--max-signatures` — cap on unique error signatures in memory (default 10000)

**JSON output (`--json`):**
```json
{
  "dir": "./capture",
  "metadata": {"version": 1, "format": "jsonl", "started": "...", "stopped": "..."},
  "timeline": [{"time": "...", "total_lines": 1200, "error_lines": 45}],
  "errors": [{"signature": "connection refused to ...", "count": 347, "first_seen": "...", "example": "..."}],
  "talkers": {"app": [{"value": "api", "total_lines": 5000, "error_lines": 200}]},
  "windows": {
    "peak_error": {"from": "...", "to": "...", "description": "..."},
    "incident_start": {"from": "...", "to": "...", "description": "..."},
    "steady_state": {"from": "...", "to": "...", "description": "..."}
  },
  "correlations": [{"source": "api", "target": "db", "lag_seconds": 2.5, "pattern": "timeout", "confidence": 0.85}],
  "total_lines": 48230,
  "error_lines": 1247
}
```

### logtap report

Single-command incident report (inspect + triage).

**Flags:**
- `--json` — JSON output
- `--out` — output directory for JSON + HTML artifacts

### logtap inspect

Show capture summary.

**Flags:**
- `--json` — JSON output

**JSON output (`--json`):**
```json
{
  "dir": "./capture",
  "metadata": {"version": 1, "format": "jsonl", "started": "...", "stopped": "..."},
  "files": 24,
  "total_lines": 48230,
  "total_bytes": 15728640,
  "disk_size": 4194304,
  "data_from": "...",
  "data_to": "...",
  "labels": {"app": [{"value": "api", "lines": 5000, "bytes": 1048576}]},
  "timeline": [{"time": "...", "lines": 1200}]
}
```

### logtap grep

Search capture for matching entries. Safe to run on live captures — skips rotated files.

**Flags:**
- `--format` — output format: json (default), text
- `--sort` — sort output chronologically
- `--count` — show match counts per file instead of lines
- `--from` — start time filter (RFC3339, HH:MM, or -30m)
- `--to` — end time filter
- `--label` — label filter (key=value, repeatable)
- `-C, --context` — number of surrounding lines to include

**JSON output (default):** JSONL, one entry per line:
```json
{"ts": "2025-02-27T10:30:45Z", "labels": {"app": "web"}, "msg": "error: connection refused"}
{"ts": "2025-02-27T10:30:46Z", "labels": {"app": "web"}, "msg": "error: timeout"}
```

With `-C` context, entries include a `"context"` field (`"before"` or `"after"`).

### logtap diff

Compare two capture directories.

**Flags:**
- `--json` — output as JSON
- `--baseline` — treat first capture as baseline and produce a verdict

**JSON output (`--json`):**
```json
{
  "a": {"dir": "./capture-a", "lines": 10000, "lines_per_sec": 166.7, "labels": ["app", "zone"]},
  "b": {"dir": "./capture-b", "lines": 15000, "lines_per_sec": 250.0, "labels": ["app", "zone"]},
  "labels_only_a": [],
  "labels_only_b": ["region"],
  "errors_only_a": [{"pattern": "timeout", "count": 5}],
  "errors_only_b": [{"pattern": "oom killed", "count": 3}],
  "rate_compare": [{"minute": "...", "rate_a": 100, "rate_b": 150}]
}
```

### logtap export

Export capture data to parquet, CSV, or JSONL.

**Flags:**
- `--format` — output format: parquet, csv, jsonl (required)
- `--out` — output file path (required)
- `--from` — start time filter
- `--to` — end time filter
- `--label` — label filter (key=value, repeatable)
- `--grep` — regex filter on log message
- `--json` — output summary as JSON

### logtap slice

Extract a time range and/or label filter into a new smaller capture directory.

**Flags:**
- `--from` — start time (RFC3339, HH:MM, or -30m)
- `--to` — end time
- `--label` — label filter (key=value, repeatable)
- `--grep` — regex filter on message content
- `-o, --out` — output directory (required)
- `--json` — output summary as JSON

### logtap merge

Combine multiple captures into one.

**Flags:**
- `-o, --out` — output directory (required)
- `--json` — output summary as JSON

**JSON output (`--json`):**
```json
{
  "sources": ["./capture-1", "./capture-2"],
  "output": "./merged",
  "entries": 150000,
  "files": 24,
  "bytes": 2097152
}
```

### logtap snapshot

Package or extract a capture archive (.tar.zst).

**Flags:**
- `-o, --output` — output path (required)
- `--extract` — extract archive to directory
- `--json` — output summary as JSON

**JSON output (`--json`):**
```json
{"operation": "pack", "source": "./capture", "output": "./capture.tar.zst", "bytes": 1048576}
{"operation": "extract", "source": "./capture.tar.zst", "output": "./capture"}
```

### logtap upload

Upload capture to cloud storage (S3 or GCS).

**Flags:**
- `--to` — destination URL (s3://bucket/prefix or gs://bucket/prefix)
- `--concurrency` — parallel uploads (default 4)
- `--share` — generate presigned URLs after upload
- `--expiry` — presigned URL expiry (default 24h, max 168h)
- `--force` — allow sharing unredacted captures
- `--json` — output summary as JSON

### logtap download

Download capture from cloud storage.

**Flags:**
- `-o, --out` — output directory (required)
- `--concurrency` — parallel downloads (default 4)
- `--json` — output summary as JSON

### logtap gc

Delete old capture directories.

**Flags:**
- `--max-age` — delete captures older than this (e.g. 7d, 24h)
- `--max-total` — delete oldest until total size under limit (e.g. 100GB)
- `--dry-run` — show what would be deleted without removing
- `--json` — output deletion list as JSON

### logtap check

Validate cluster readiness and detect leftover sidecars. Also available as `logtap doctor`.

**Flags:**
- `-n, --namespace` — namespace (defaults to current context)
- `--json` / `--format json` — output as JSON

### logtap status

Show tapped workloads and receiver stats.

**Flags:**
- `-n, --namespace` — namespace (defaults to current context)
- `--json` — output as JSON

### logtap watch

Tail a live or completed capture directory.

**Flags:**
- `-n, --lines` — number of initial lines to show (default 10)
- `--grep` — regex filter on message content
- `--label` — label filter (key=value)
- `--json` — output as JSON

### logtap catalog

Discover and list capture directories.

**Flags:**
- `--json` — output as JSON

### logtap deploy

Deploy in-cluster receiver.

**Flags:**
- `-n, --namespace` — namespace
- `--json` — output as JSON

### logtap completion

Generate shell completion scripts.

**Flags:**
- `bash`, `zsh`, `fish`, `powershell` — target shell

### logtap version

Print version, commit, and build date.

## Exit Codes

| Code | Name | Meaning | Recoverable |
|------|------|---------|-------------|
| 0 | OK | Success | - |
| 1 | Internal | Unexpected failure | No |
| 2 | Usage | Invalid arguments or flags | No |
| 3 | NotFound | Capture directory, file, or resource missing | No |
| 4 | Permission | Access denied (RBAC, filesystem) | No |
| 5 | Network | Network error (timeout, DNS, connection refused) | Yes |
| 6 | Findings | Triage/check found anomalies or issues | No |

**JSON error output (`--json` on failure):**
```json
{"exit_code": 3, "error": "not_found", "message": "capture directory not found: ./missing", "recoverable": false}
```

## What This Does NOT Do

- Does not persist after use — ephemeral by design
- Does not stream to external services — captures locally
- Does not use ML — deterministic anomaly pattern matching
- Does not require persistent cluster access — tap in, capture, tap out

## Parsing Examples

```bash
# Incident capture workflow
logtap recv --dir ./capture --max-disk 1GB --redact --headless &
logtap tap --deployment api-gateway --target localhost:3100
logtap report ./capture --json

# Triage with jq
logtap triage ./capture --json | jq '.errors[] | select(.count > 100)'
logtap triage ./capture --json | jq '.windows.peak_error'

# Search logs
logtap grep "error|panic" ./capture --sort | jq '.msg'
logtap grep "timeout" ./capture -C 3 --format json | jq 'select(.context == null) | .msg'

# Time-filtered grep
logtap grep "5xx" ./capture --from -30m --to -5m --format json

# Capture summary
logtap inspect ./capture --json | jq '{files, total_lines, labels}'

# Compare captures
logtap diff ./baseline ./current --json | jq '.errors_only_b'
logtap diff ./baseline ./current --baseline --json | jq '{verdict, confidence}'

# Export for external analysis
logtap export ./capture --format parquet --out ./data.parquet
logtap export ./capture --format csv --grep "error" --out ./errors.csv

# Slice and share
logtap slice ./capture --from 10:32 --to 10:45 --label app=api -o ./incident
logtap snapshot ./incident -o ./incident.tar.zst
logtap upload ./incident --to s3://bucket/incidents/2025-02-27 --share --json

# Garbage collection
logtap gc ./captures --max-age 7d --dry-run --json
```
