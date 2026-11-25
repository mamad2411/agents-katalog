---
name: enterobase-api
description: "Enterobase-API API skill. Use when working with Enterobase-API for api. Covers 30 endpoints."
version: 1.0.0
generator: lapsh
---

# Enterobase-API
API version: v2.0

## Auth
basic

## Base URL
Not specified.

## Setup
1. Configure auth: basic
2. GET /api/v2.0 -- verify access
3. POST /api/v2.0/lookup/{barcode} -- create first lookup

## Endpoints

30 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v2.0 | Top level information about EnteroBase databases |
| GET | /api/v2.0/login | Login endpoint, refresh your API token |
| GET | /api/v2.0/lookup | Generic endpoint for lookup list of barcodes |
| GET | /api/v2.0/lookup/{barcode} | Generic endpoint for lookup of barcodes |
| POST | /api/v2.0/lookup/{barcode} | Generic endpoint for lookup of barcodes |
| GET | /api/v2.0/{database}/AMRdata | AMR data |
| GET | /api/v2.0/{database}/AMRdata/{barcode} | AMR data |
| POST | /api/v2.0/{database}/AMRdata/{barcode} | AMR data |
| PUT | /api/v2.0/{database}/AMRdata/{barcode} | AMR data |
| GET | /api/v2.0/{database}/assemblies | Genome assemblies |
| GET | /api/v2.0/{database}/assemblies/{barcode} | Genome assemblies |
| POST | /api/v2.0/{database}/assemblies/{barcode} | Genome assemblies |
| PUT | /api/v2.0/{database}/assemblies/{barcode} | Genome assemblies |
| GET | /api/v2.0/{database}/schemes | Genotyping schemes |
| GET | /api/v2.0/{database}/schemes/{barcode} | Genotyping schemes |
| POST | /api/v2.0/{database}/schemes/{barcode} | Genotyping schemes |
| PUT | /api/v2.0/{database}/schemes/{barcode} | Genotyping schemes |
| GET | /api/v2.0/{database}/straindata | Strain data |
| GET | /api/v2.0/{database}/strains | Strain metadata |
| GET | /api/v2.0/{database}/strains/{barcode} | Strain metadata |
| POST | /api/v2.0/{database}/strains/{barcode} | Strain metadata |
| PUT | /api/v2.0/{database}/strains/{barcode} | Strain metadata |
| GET | /api/v2.0/{database}/strainsversion | Strain previous metadata |
| GET | /api/v2.0/{database}/traces | Traces (sequence-reads) metadata |
| GET | /api/v2.0/{database}/traces/{barcode} | Traces (sequence-reads) metadata |
| POST | /api/v2.0/{database}/traces/{barcode} | Traces (sequence-reads) metadata |
| PUT | /api/v2.0/{database}/traces/{barcode} | Traces (sequence-reads) metadata |
| GET | /api/v2.0/{database}/{scheme}/alleles | Alleles  data |
| GET | /api/v2.0/{database}/{scheme}/loci | Loci |
| GET | /api/v2.0/{database}/{scheme}/sts | ST profile data |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all v2.0?" -> GET /api/v2.0
- "List all login?" -> GET /api/v2.0/login
- "List all lookup?" -> GET /api/v2.0/lookup
- "Get lookup details?" -> GET /api/v2.0/lookup/{barcode}
- "List all AMRdata?" -> GET /api/v2.0/{database}/AMRdata
- "Get AMRdata details?" -> GET /api/v2.0/{database}/AMRdata/{barcode}
- "Update a AMRdata?" -> PUT /api/v2.0/{database}/AMRdata/{barcode}
- "List all assemblies?" -> GET /api/v2.0/{database}/assemblies
- "Get assembly details?" -> GET /api/v2.0/{database}/assemblies/{barcode}
- "Update a assembly?" -> PUT /api/v2.0/{database}/assemblies/{barcode}
- "List all schemes?" -> GET /api/v2.0/{database}/schemes
- "Get scheme details?" -> GET /api/v2.0/{database}/schemes/{barcode}
- "Update a scheme?" -> PUT /api/v2.0/{database}/schemes/{barcode}
- "List all straindata?" -> GET /api/v2.0/{database}/straindata
- "List all strains?" -> GET /api/v2.0/{database}/strains
- "Get strain details?" -> GET /api/v2.0/{database}/strains/{barcode}
- "Update a strain?" -> PUT /api/v2.0/{database}/strains/{barcode}
- "List all strainsversion?" -> GET /api/v2.0/{database}/strainsversion
- "List all traces?" -> GET /api/v2.0/{database}/traces
- "Get trace details?" -> GET /api/v2.0/{database}/traces/{barcode}
- "Update a trace?" -> PUT /api/v2.0/{database}/traces/{barcode}
- "List all alleles?" -> GET /api/v2.0/{database}/{scheme}/alleles
- "List all loci?" -> GET /api/v2.0/{database}/{scheme}/loci
- "List all sts?" -> GET /api/v2.0/{database}/{scheme}/sts
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
