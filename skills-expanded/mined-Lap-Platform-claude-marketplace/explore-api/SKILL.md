---
name: explore-api
description: "Explore API skill. Use when working with Explore for catalog. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Explore API
API version: v2.0

## Auth
ApiKey apikey in query

## Base URL
https://public.opendatasoft.com/api/explore/v2.0

## Setup
1. Set your API key in the appropriate header
2. GET /catalog/datasets -- verify access

## Endpoints

16 endpoints across 1 groups. See references/api-spec.lap for full details.

### catalog
| Method | Path | Description |
|--------|------|-------------|
| GET | /catalog/datasets | Query catalog datasets |
| GET | /catalog/exports | List export formats |
| GET | /catalog/exports/{format} | Export a catalog |
| GET | /catalog/exports/csv | Export a catalog in CSV |
| GET | /catalog/exports/dcat{dcat_ap_format} | Export a catalog in RDF/XML (DCAT) |
| GET | /catalog/facets | List facet values |
| GET | /catalog/datasets/{dataset_id}/records | Query dataset records |
| GET | /catalog/datasets/{dataset_id}/exports | List export formats |
| GET | /catalog/datasets/{dataset_id}/exports/{format} | Export a dataset |
| GET | /catalog/datasets/{dataset_id}/exports/csv | Export a dataset in CSV |
| GET | /catalog/datasets/{dataset_id}/exports/parquet | Export a dataset in Parquet |
| GET | /catalog/datasets/{dataset_id}/exports/gpx | Export a dataset in GPX |
| GET | /catalog/datasets/{dataset_id} | Show dataset information |
| GET | /catalog/datasets/{dataset_id}/facets | List dataset facets |
| GET | /catalog/datasets/{dataset_id}/attachments | List dataset attachments |
| GET | /catalog/datasets/{dataset_id}/records/{record_id} | Read a dataset record |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all datasets?" -> GET /catalog/datasets
- "List all exports?" -> GET /catalog/exports
- "Get export details?" -> GET /catalog/exports/{format}
- "List all csv?" -> GET /catalog/exports/csv
- "Get dcat{dcat_ap_format} details?" -> GET /catalog/exports/dcat{dcat_ap_format}
- "List all facets?" -> GET /catalog/facets
- "List all records?" -> GET /catalog/datasets/{dataset_id}/records
- "List all exports?" -> GET /catalog/datasets/{dataset_id}/exports
- "Get export details?" -> GET /catalog/datasets/{dataset_id}/exports/{format}
- "List all csv?" -> GET /catalog/datasets/{dataset_id}/exports/csv
- "List all parquet?" -> GET /catalog/datasets/{dataset_id}/exports/parquet
- "List all gpx?" -> GET /catalog/datasets/{dataset_id}/exports/gpx
- "Get dataset details?" -> GET /catalog/datasets/{dataset_id}
- "List all facets?" -> GET /catalog/datasets/{dataset_id}/facets
- "List all attachments?" -> GET /catalog/datasets/{dataset_id}/attachments
- "Get record details?" -> GET /catalog/datasets/{dataset_id}/records/{record_id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
