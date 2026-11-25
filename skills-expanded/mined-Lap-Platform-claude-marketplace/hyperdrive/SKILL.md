---
name: hyperdrive
description: "HyperDrive API skill. Use when working with HyperDrive for hyperdrive. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# HyperDrive
API version: 2019-09-30

## Auth
OAuth2

## Base URL
Not specified.

## Setup
1. Configure auth: OAuth2
3. POST /hyperdrive/v1.0/{armScope}/runs -- create first runs

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### hyperdrive
| Method | Path | Description |
|--------|------|-------------|
| POST | /hyperdrive/v1.0/{armScope}/runs | Create an Experiment. |
| POST | /hyperdrive/v1.0/{armScope}/runs/{runId}/cancel | Cancel an Experiment. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a run?" -> POST /hyperdrive/v1.0/{armScope}/runs
- "Create a cancel?" -> POST /hyperdrive/v1.0/{armScope}/runs/{runId}/cancel
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
