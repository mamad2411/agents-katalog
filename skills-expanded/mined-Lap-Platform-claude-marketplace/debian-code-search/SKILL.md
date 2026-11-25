---
name: debian-code-search
description: "Debian Code Search API skill. Use when working with Debian Code Search for search, searchperpackage. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Debian Code Search
API version: 1.4.0

## Auth
ApiKey x-dcs-apikey in header

## Base URL
https://codesearch.debian.net/api/v1

## Setup
1. Set your API key in the appropriate header
2. GET /search -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | Searches through source code |

### searchperpackage
| Method | Path | Description |
|--------|------|-------------|
| GET | /searchperpackage | Like /search, but aggregates per package |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /search
- "Search searchperpackage?" -> GET /searchperpackage
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
