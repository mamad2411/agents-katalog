---
name: cnab-online
description: "Cnab Online API skill. Use when working with Cnab Online for file. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Cnab Online
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://cnab-online.herokuapp.com/v1

## Setup
1. No auth setup needed
2. GET /file/{fileId}/occurrences -- verify access
3. POST /file -- create first file

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### file
| Method | Path | Description |
|--------|------|-------------|
| POST | /file | Faz o upload de um arquivo |
| GET | /file/{fileId} | Retorna as informações básicas de um arquivo previamente processado |
| GET | /file/{fileId}/occurrences | Retorna as informações de baixa de boletos e outros tipos de ocorrências |
| GET | /file/{fileId}/lines | Retorna todas as linhas e seus respectivos campos (de forma não processada, apenas indicando os campos reconhecidos) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a file?" -> POST /file
- "Get file details?" -> GET /file/{fileId}
- "List all occurrences?" -> GET /file/{fileId}/occurrences
- "List all lines?" -> GET /file/{fileId}/lines

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
