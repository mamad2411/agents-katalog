---
name: webscrapingai
description: "WebScraping.AI API skill. Use when working with WebScraping.AI for ai, html, text. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# WebScraping.AI
API version: 3.2.0

## Auth
ApiKey api_key in query

## Base URL
https://api.webscraping.ai

## Setup
1. Set your API key in the appropriate header
2. GET /ai/question -- verify access

## Endpoints

7 endpoints across 6 groups. See references/api-spec.lap for full details.

### ai
| Method | Path | Description |
|--------|------|-------------|
| GET | /ai/question | Get an answer to a question about a given web page |
| GET | /ai/fields | Extract structured data fields from a web page |

### html
| Method | Path | Description |
|--------|------|-------------|
| GET | /html | Page HTML by URL |

### text
| Method | Path | Description |
|--------|------|-------------|
| GET | /text | Page text by URL |

### selected
| Method | Path | Description |
|--------|------|-------------|
| GET | /selected | HTML of a selected page area by URL and CSS selector |

### selected-multiple
| Method | Path | Description |
|--------|------|-------------|
| GET | /selected-multiple | HTML of multiple page areas by URL and CSS selectors |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account | Information about your account calls quota |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all question?" -> GET /ai/question
- "List all fields?" -> GET /ai/fields
- "List all html?" -> GET /html
- "List all text?" -> GET /text
- "List all selected?" -> GET /selected
- "List all selected-multiple?" -> GET /selected-multiple
- "List all account?" -> GET /account
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
