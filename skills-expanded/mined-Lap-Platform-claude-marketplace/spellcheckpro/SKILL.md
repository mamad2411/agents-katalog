---
name: spellcheckpro
description: "SpellCheckPro API skill. Use when working with SpellCheckPro for check_spelling. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# SpellCheckPro

## Auth
No authentication required.

## Base URL
https://spellcheckpro.p.rapidapi.com

## Setup
1. No auth setup needed
3. POST /check_spelling -- create first check_spelling

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### check_spelling
| Method | Path | Description |
|--------|------|-------------|
| POST | /check_spelling | Check Spelling (English) |
| POST | /check_spelling | Check Spelling (Russian) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a check_spelling?" -> POST /check_spelling

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
