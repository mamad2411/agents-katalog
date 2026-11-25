---
name: dynamicdocs
description: "DynamicDocs API skill. Use when working with DynamicDocs for templates. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# DynamicDocs
API version: 1.0

## Auth
ApiKey ADVICEment API Key in header | ApiKey RapidAPI.com API Key in header

## Base URL
https://dynamicdocs.p.rapidapi.com

## Setup
1. Set your API key in the appropriate header
3. POST /templates/{template-token}/compile -- create first compile

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### templates
| Method | Path | Description |
|--------|------|-------------|
| POST | /templates/{template-token}/compile | Compile New Document PDF |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a compile?" -> POST /templates/{template-token}/compile
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
