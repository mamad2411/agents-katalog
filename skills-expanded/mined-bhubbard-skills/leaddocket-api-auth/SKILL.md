---
name: leaddocket-api-auth
description: >
  Reference guide for authenticating with the LeadDocket REST API — API key
  generation and management, required headers, rate limit rules, error codes,
  and developer quickstart. Use at the start of any LeadDocket integration to
  understand authentication requirements before calling any other skill.
---

# LeadDocket — API Authentication & Key Management

Base URL: `https://{instance}.leaddocket.com`  
API Explorer: `https://{instance}/api/explore/index.html`  
OpenAPI Spec: `https://{instance}/api/v1/docs`

---

## Authentication

All API endpoints (except `POST /api/externalcalls/start` and `POST /api/externalcalls/end`) require an API key.

### Required header

```http
X-API-Key: {your-api-key}
```

Alternatively, some endpoints accept the key as a query parameter:
```
?apiKey={your-api-key}
```

---

## Generating an API Key

1. Log in to your LeadDocket instance
2. Navigate to **Settings → API**
3. Click **Generate New Key**
4. Copy and store the key securely — it is shown only once

> API keys are scoped to the account and have full access. Treat them as secrets — never expose in client-side code or version control.

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| `GET /api/leads/{id}` (full) | **25 requests/minute** |
| All other endpoints | No documented per-endpoint limit |
| Global | 429 returned when rate limit exceeded |

**Handle 429 errors**: Always implement exponential backoff. Start with a 2-second delay, double on each retry, cap at 60 seconds.

```js
async function withRetry(fn, maxAttempts = 5) {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      return await fn();
    } catch (err) {
      if (err.status === 429 && i < maxAttempts - 1) {
        await new Promise(r => setTimeout(r, Math.min(2000 * 2 ** i, 60000)));
      } else throw err;
    }
  }
}
```

---

## Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| `200 OK` | Success |
| `201 Created` | Resource created |
| `204 No Content` | Success, no body |
| `400 Bad Request` | Invalid request / missing required field |
| `401 Unauthorized` | Missing or invalid API key |
| `403 Forbidden` | Valid key but insufficient permissions |
| `404 Not Found` | Resource not found |
| `429 Too Many Requests` | Rate limit exceeded — back off and retry |
| `500 Internal Server Error` | Server-side error — retry with backoff |

---

## External Calls Authentication Exception

The VoIP webhook endpoints accept calls **without authentication**:
- `POST /api/externalcalls/start` — public (designed for VoIP provider webhooks)
- `POST /api/externalcalls/end` — public

All `GET` endpoints on external calls (`/api/externalcalls/{id}`, `/recording`, `/transcription`) **do** require the API key.

---

## Best Practices

- **Never hardcode API keys**: Store in environment variables or a secrets manager (AWS Secrets Manager, HashiCorp Vault, `.env` files not checked in).
- **One key per environment**: Use separate API keys for dev, staging, and production.
- **Log request IDs**: Include a `X-Request-ID` header on your requests for easier debugging with LeadDocket support.
- **Base URL pattern**: Always use `https://{instance}.leaddocket.com` — the instance subdomain is firm-specific.
- **Start with `/api/v1/docs`**: Fetch the live OpenAPI spec from `https://{instance}/api/v1/docs` to see the exact schema for your instance version.
