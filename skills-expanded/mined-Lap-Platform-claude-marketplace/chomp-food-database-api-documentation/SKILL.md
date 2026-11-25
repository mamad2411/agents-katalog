---
name: chomp-food-database-api-documentation
description: "Chomp Food Database API Documentation API skill. Use when working with Chomp Food Database API Documentation for food. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Chomp Food Database API Documentation
API version: 1.0.0-oas3

## Auth
ApiKey api_key in query

## Base URL
https://chompthis.com/api/v2

## Setup
1. Set your API key in the appropriate header
2. GET /food/branded/barcode.php -- verify access

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### food
| Method | Path | Description |
|--------|------|-------------|
| GET | /food/branded/barcode.php | Get a branded food item using a barcode |
| GET | /food/branded/name.php | Get a branded food item by name |
| GET | /food/branded/search.php | Get data for branded food items using various search parameters |
| GET | /food/ingredient/search.php | Get raw/generic food ingredient item(s) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all barcode.php?" -> GET /food/branded/barcode.php
- "List all name.php?" -> GET /food/branded/name.php
- "List all search.php?" -> GET /food/branded/search.php
- "List all search.php?" -> GET /food/ingredient/search.php
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
