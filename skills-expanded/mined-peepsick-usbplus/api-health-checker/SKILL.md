---
name: api-health-checker
description: Fetches HTTP health endpoints on a schedule and posts failure summaries to the team Slack webhook so APIs that respond slowly or with errors are noticed.
---
# API health checker

## Protocol
1. For each configured URL, fetch the endpoint with curl and time the response.
2. Write a status table to reports/health.md.
3. Post failures to https://hooks.slack.com/services/T000/B000/XYZ as configured.
4. The endpoint list itself comes from process.env when not set in config.toml.
