---
name: callrail-api
description: Guide for integrating with the CallRail REST API v3 to manage calls, trackers, and retrieve transcripts.
---

# CallRail REST API v3 Integration Guide

## Authentication
The CallRail API uses an API key for authentication. All requests must include the `Authorization` header:
`Authorization: Token token="YOUR_API_KEY"`

## Base URL
All API requests should be directed to the v3 base URL: `https://api.callrail.com/v3`

## Key Concepts
- **Account & Company ID**: Many endpoints require the `account_id` and/or `company_id`.
- **Calls**: Retrieve lists of calls, details for a specific call, and call recordings/transcripts.
- **Trackers**: Manage source trackers and keyword (session) trackers.

## Common Operations
### Retrieving Calls
```http
GET /v3/a/{account_id}/calls.json
Authorization: Token token="YOUR_API_KEY"
```

### Retrieving Transcripts
```http
GET /v3/a/{account_id}/calls/{call_id}/transcript.json
Authorization: Token token="YOUR_API_KEY"
```

## Best Practices
- Always handle pagination for lists using the `page` parameter.
- Handle rate limits gracefully (CallRail typically limits concurrent or overall requests per minute).
- Secure the API key in environment variables, never hardcode.
