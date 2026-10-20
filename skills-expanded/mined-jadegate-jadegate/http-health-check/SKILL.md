---
name: http-health-check
description: Check if a website is up by sending HTTP GET and measuring response time
---

# HTTP Health Check

Check if a website is up by sending HTTP GET and measuring response time

## When to Use

- User wants to health check
- User wants to ping check
- User wants to site check
- Keywords: ping, health, uptime, monitor

## Required Parameters

- **url** (string): URL to check

## Output

- **status** (string): up or down
- **status_code** (number): HTTP status code
- **response_ms** (number): Response time in ms

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: *
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `fetch` -> 4 steps -> Exit: `ret_up`, `ret_down`
