# Overwatch CLI Skill

Use this skill to help the user manage an Overwatch monitoring server via the CLI. Overwatch is a self-hosted infrastructure monitoring tool shipped as a single Go binary.

## Architecture

- **Server** (`overwatch serve`): runs checks on a schedule, sends alerts on failure, exposes an HTTP API. Config lives in a YAML file (default `overwatch.yaml`).
- **Client** (CLI): talks to the server over HTTP with Ed25519 request signing. Client config lives in `~/.overwatch/` (keypair + `client.yaml`).
- **Auth**: clients join using a join token, which registers their public key. All subsequent API requests are signed.

## Running the server

```bash
# Start with defaults (127.0.0.1:3030, creates overwatch.yaml if missing)
overwatch serve

# Custom bind
overwatch serve --bind-address 0.0.0.0 --bind-port 8080

# With a specific config file
overwatch serve -c /path/to/config.yaml
```

The server prints the join token on startup. Use `overwatch token` from an authenticated client to retrieve it later.

## Setting up a client

```bash
overwatch init
# Select option 2 "Setup a client"
# Paste the join token from the server
```

This generates a keypair, registers with the server, and writes `~/.overwatch/client.yaml`.

## Retrieving the join token

An authenticated client can fetch the join token to share with others:

```bash
overwatch token
```

This prints just the token string, suitable for copy/paste.

## Check types

| Type | Description | Key flags |
|------|-------------|-----------|
| `http` | HTTP/HTTPS endpoint | `--target URL --expected-status 200` |
| `tcp` | TCP connect | `--target host:port` |
| `tls` | TLS certificate expiry | `--target host:443` |
| `dns` | DNS lookup | `--target hostname` |
| `checkin` | Cron/job check-in webhook | `--max-silence 25h` (no target needed; jobs POST to `/api/checkin/{name}`) |

## Managing checks

```bash
# List all checks
overwatch check list

# Add an HTTP check
overwatch check add my-api --type http --target https://api.example.com --interval 30s --timeout 10s --expected-status 200

# Add a TCP check
overwatch check add postgres --type tcp --target localhost:5432 --interval 30s --timeout 5s

# Add a TLS certificate check
overwatch check add cert --type tls --target example.com:443 --interval 1h --timeout 10s

# Add a DNS check
overwatch check add ns --type dns --target example.com --interval 5m --timeout 5s

# Add a check-in (cron monitoring) check
overwatch check add nightly-backup --type checkin --max-silence 25h --interval 1m

# Link a check to alert destinations
overwatch check add my-api --type http --target https://api.example.com --interval 30s --alerts slack,pagerduty

# Update a check (only specified flags change)
overwatch check update my-api --interval 60s
overwatch check update my-api --target https://new-api.example.com --timeout 5s
overwatch check update my-api --alerts slack

# Remove a check
overwatch check remove my-api

# Test a check locally (reads from config file, does not require running server)
overwatch check test my-api
```

## Managing alerts

Alerts are webhook destinations (Slack, Teams, PagerDuty, generic HTTP) or SMTP.

```bash
# List all alert destinations
overwatch alert list

# Add a webhook alert
overwatch alert add slack --url https://hooks.slack.com/services/T.../B.../xxx

# Add with custom method and headers
overwatch alert add custom --url https://my.endpoint/hook --method POST --timeout 15s --headers "Authorization:Bearer tok123"

# Update an alert
overwatch alert update slack --url https://hooks.slack.com/services/NEW/URL
overwatch alert update slack --timeout 30s

# Remove an alert
overwatch alert remove slack

# Send a test alert to all configured destinations
overwatch alert test
```

## Viewing status

```bash
# Full table: all checks with live results + all alert destinations
overwatch status
```

Output includes columns: NAME, TYPE, TARGET, STATUS, LATENCY, INTERVAL, TIMEOUT, LAST CHECK for checks, and NAME, TRANSPORT, DESTINATION, METHOD, TIMEOUT for alerts.

## Config management

```bash
# Generate a starter YAML config
overwatch config init

# Validate config
overwatch config validate

# Use a custom config path
overwatch -c /path/to/config.yaml status
```

## Check-in webhook (cron monitoring)

External jobs POST to the server to check in:

```bash
# Success check-in
curl -X POST http://overwatch-server:3030/api/checkin/nightly-backup

# Report failure
curl -X POST http://overwatch-server:3030/api/checkin/nightly-backup?status=fail
```

The check-in endpoint is unauthenticated. If no check-in arrives within `max_silence`, the check transitions to down and alerts fire.

## Server reload

After editing the YAML config on disk:

```bash
# Via signal
kill -HUP $(pgrep overwatch)

# Via API (authenticated)
curl -X POST http://overwatch-server:3030/api/reload
```

## Common patterns

### Set up monitoring for a new service
```bash
overwatch check add myservice --type http --target https://myservice.example.com --interval 30s --alerts slack
```

### Set up monitoring for a database
```bash
overwatch check add mydb --type tcp --target db.example.com:5432 --interval 30s --timeout 5s --alerts slack
```

### Monitor a cron job
```bash
overwatch check add daily-etl --type checkin --max-silence 25h --interval 1m --alerts slack
# Then in the cron job script: curl -X POST http://overwatch:3030/api/checkin/daily-etl
```

### Share access with a colleague
```bash
# You (authenticated client):
overwatch token
# Copy the output and send it to your colleague
# They run: overwatch init → option 2 → paste token
```
