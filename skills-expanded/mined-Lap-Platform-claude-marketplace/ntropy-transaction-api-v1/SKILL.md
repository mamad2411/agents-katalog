---
name: ntropy-transaction-api-v1
description: "Ntropy Transaction API v1 API skill. Use when working with Ntropy Transaction API v1 for classifier, types, health. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Ntropy Transaction API v1

## Auth
ApiKey key in header

## Base URL
https://api.ntropy.network

## Setup
1. Set your API key in the appropriate header
2. GET /types -- verify access
3. POST /classifier/consumer/batch -- create first batch

## Endpoints

10 endpoints across 4 groups. See references/api-spec.lap for full details.

### classifier
| Method | Path | Description |
|--------|------|-------------|
| POST | /classifier/consumer/batch | Classify a batch of transactions. |
| GET | /classifier/consumer/batch/{id} | Get a batch of consumer transaction classification results. |
| POST | /classifier/consumer | Classify a consumer transaction. |
| POST | /classifier/business/batch | Classify a batch of business transactions. |
| GET | /classifier/business/batch/{id} | Get a batch of business transaction classification results. |
| POST | /classifier/business | Classify a business transaction. |
| POST | /classifier/report | Report a wrongly classified transaction. |

### types
| Method | Path | Description |
|--------|------|-------------|
| GET | /types | Get dictionary of type values. |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Check API health. |

### performance
| Method | Path | Description |
|--------|------|-------------|
| GET | /performance | Check the Transaction API performance report. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a batch?" -> POST /classifier/consumer/batch
- "Get batch details?" -> GET /classifier/consumer/batch/{id}
- "Create a consumer?" -> POST /classifier/consumer
- "Create a batch?" -> POST /classifier/business/batch
- "Get batch details?" -> GET /classifier/business/batch/{id}
- "Create a business?" -> POST /classifier/business
- "Create a report?" -> POST /classifier/report
- "List all types?" -> GET /types
- "List all health?" -> GET /health
- "List all performance?" -> GET /performance
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
