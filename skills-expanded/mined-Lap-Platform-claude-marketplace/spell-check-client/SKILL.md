---
name: spell-check-client
description: "Spell Check Client API skill. Use when working with Spell Check Client for spellcheck. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Spell Check Client
API version: 1.0

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
https://api.cognitive.microsoft.com/bing/v7.0

## Setup
1. Set your API key in the appropriate header
3. POST /spellcheck -- create first spellcheck

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### spellcheck
| Method | Path | Description |
|--------|------|-------------|
| POST | /spellcheck | The Bing Spell Check API lets you perform contextual grammar and spell checking. Bing has developed a web-based spell-checker that leverages machine learning and statistical machine translation to dynamically train a constantly evolving and highly contextual algorithm. The spell-checker is based on a massive corpus of web searches and documents. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a spellcheck?" -> POST /spellcheck
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
