---
name: api-documentation
description: "Creates API documentation templates with endpoint descriptions, request/response examples, and authentication guides. Use when documenting REST APIs for developers."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# API Documentation

## When to Use This Skill

Use this skill when you need to:
- Create API documentation for a REST API with endpoint references
- Write authentication guides, request/response examples, and error handling docs
- Build a getting started guide for API consumers
- Structure a complete API reference for developer onboarding

**DO NOT** use this skill for internal code documentation, SDK documentation, or webhook setup guides. This is for external-facing REST API documentation.

---

## Core Principle

API DOCUMENTATION IS WRITTEN FOR DEVELOPERS WHO WANT TO INTEGRATE, NOT READ — EVERY PAGE MUST ANSWER "HOW DO I DO THIS?" WITH A COPY-PASTE EXAMPLE.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **API purpose** | "What does this API do in one sentence?" | No default — must be provided |
| **Base URL** | "What is the base URL for API requests?" | No default — must be provided |
| **Authentication method** | "How do users authenticate? API key, OAuth, Bearer token?" | API key in header |
| **Endpoints to document** | "List all endpoints with their HTTP methods." | No default — must be provided |
| **Response format** | "JSON, XML, or both?" | JSON |
| **Rate limits** | "Are there rate limits? If so, what are they?" | 100 requests per minute |

**GATE: Confirm the brief before structuring the documentation.**

---

## Phase 2: Structure

### Documentation Architecture

1. **Overview** — What the API does, who it is for, base URL
2. **Authentication** — How to get and use API keys
3. **Quick Start** — First API call in under 5 minutes
4. **Endpoints Reference** — Full endpoint documentation
5. **Error Handling** — Error codes, messages, and resolution
6. **Rate Limits** — Limits, headers, and handling 429 responses
7. **Changelog** — Version history and breaking changes

### Endpoint Documentation Template

For each endpoint, document:
- HTTP method and path
- Description (one sentence)
- Authentication required (yes/no)
- Request parameters (path, query, body)
- Request example (cURL)
- Response example (JSON)
- Error responses
- Rate limit notes

**GATE: Confirm structure and endpoint list before writing.**

---

## Phase 3: Write

### Authentication Section

```
## Authentication

All API requests require an API key passed in the header:

\`\`\`
Authorization: Bearer YOUR_API_KEY
\`\`\`

**Getting your API key:**
1. Log in to your dashboard
2. Navigate to Settings → API
3. Click "Generate API Key"
4. Copy and store securely — it will not be shown again

**Security:** Never expose your API key in client-side code, public repositories, or URLs.
```

### Quick Start Section

Write a complete first-request walkthrough:
1. Get your API key (link to auth section)
2. Make your first request (cURL example)
3. Understand the response
4. Next steps (link to full reference)

### Endpoint Reference Format

```
## [METHOD] /endpoint/path

[One-sentence description of what this endpoint does.]

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | The resource ID |
| limit | integer | No | Max results (default: 20, max: 100) |

### Request Example

\`\`\`bash
curl -X GET "https://api.example.com/v1/resource" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
\`\`\`

### Response Example

\`\`\`json
{
  "data": [...],
  "meta": {
    "total": 42,
    "page": 1,
    "per_page": 20
  }
}
\`\`\`

### Error Responses

| Code | Message | Resolution |
|------|---------|------------|
| 401 | Unauthorized | Check your API key |
| 404 | Not found | Verify the resource ID exists |
| 429 | Rate limited | Wait and retry after the Retry-After header value |
```

### Writing Rules

- Every endpoint has a cURL example that can be copied and run immediately
- Response examples use realistic (but fake) data
- Error responses include resolution steps, not just codes
- Parameters table specifies type, required/optional, and default values
- Use consistent formatting across all endpoints

---

## Phase 4: Polish

### 1. Error Reference Table

```
## Error Codes

| HTTP Code | Error Type | Description | Resolution |
|-----------|-----------|-------------|------------|
| 400 | Bad Request | Invalid parameters | Check request body against schema |
| 401 | Unauthorized | Missing or invalid API key | Verify your API key |
| 403 | Forbidden | Insufficient permissions | Check your plan's API access level |
| 404 | Not Found | Resource does not exist | Verify the resource ID |
| 429 | Too Many Requests | Rate limit exceeded | Retry after Retry-After header value |
| 500 | Internal Server Error | Server-side issue | Retry; contact support if persistent |
```

### 2. SDK and Library Suggestions

List official or community SDKs if available. If none exist, provide example code in 2-3 popular languages (Python, JavaScript, cURL).

### 3. Quality Checklist

```
## API Documentation Checklist

- [ ] Base URL is clearly stated at the top
- [ ] Authentication section includes step-by-step key setup
- [ ] Quick start gets a developer to their first response in under 5 minutes
- [ ] Every endpoint has method, path, description, parameters, and examples
- [ ] cURL examples are copy-paste ready
- [ ] Response examples use realistic fake data
- [ ] Error codes include resolution steps
- [ ] Rate limit policy is documented with handling guidance
- [ ] Changelog tracks breaking changes with dates
- [ ] No placeholder text or TODO items remain
```

---

## Example

**API:** Invoice management API for a billing SaaS

**Quick start excerpt:**
```
## Quick Start

Make your first API call in 3 steps:

### 1. Get your API key
Go to Settings → API in your dashboard and generate a key.

### 2. List your invoices
curl -X GET "https://api.invoicebot.com/v1/invoices" \
  -H "Authorization: Bearer sk_test_abc123"

### 3. Check the response
{
  "data": [
    {
      "id": "inv_001",
      "client": "Acme Corp",
      "amount": 2500.00,
      "status": "paid"
    }
  ]
}

You are ready. Explore the full endpoint reference below.
```

---

## Anti-Patterns

- **No examples** — documentation without copy-paste examples is unusable. Every endpoint needs a request and response sample.
- **Outdated examples** — examples that return errors destroy developer trust. Test every example before publishing.
- **Missing error documentation** — developers spend more time handling errors than happy paths. Document every error code.
- **Jargon-heavy descriptions** — "Retrieves a paginated collection of resource entities" should be "Lists all invoices."
- **No quick start** — forcing developers to read the entire reference before making their first call is a conversion killer.

---

## Recovery

- **API is still changing:** Mark the docs as "beta" and version the API. Document known limitations upfront.
- **Too many endpoints to document at once:** Start with the 5 most-used endpoints. Add the rest incrementally.
- **No SDK available:** Provide examples in cURL, Python (requests), and JavaScript (fetch) for the top 3 endpoints.
- **Authentication is complex (OAuth):** Create a dedicated authentication guide with a flow diagram and step-by-step walkthrough.
