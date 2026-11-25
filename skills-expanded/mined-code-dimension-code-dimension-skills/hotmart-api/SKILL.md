---
name: hotmart-api
description: Master knowledge base for interacting with the Hotmart API (v1). Use this skill when generating, maintaining or debugging integrations with Hotmart.
metadata:
  author: code-dimension
  version: 1.0
---

# Hotmart API Skill

This skill provides context and instructions for working with the Hotmart API (v1).
The API is vast, so the documentation is organized by domain using a **progressive disclosure strategy**.

**Do not hallucinate API endpoints or parameters.** Always refer to the specific domain reference file before implementing a new API call.

---

## 1. Core API Concepts

These foundational concepts apply globally across all domains:

### 1.1. Authentication

- **Protocol:** OAuth 2.0 Client Credentials flow.
- **Process:** Generate credentials (`client_id`, `client_secret`) on the platform and get the token by making a `POST` to `/security/oauth/token` with an `Authorization: Basic [credentials_base64]` header.
- **Expiration:** Tokens are short-lived. Integration logic must automatically intercept `401 Unauthorized` responses and request a new token.
- **Reference:** See [auth.md](./references/auth.md) for curl payloads and specific implementation rules.

### 1.2. HTTP Response Codes

- `200 OK`: Success (returns requested payload or empty `{}` for mutations).
- `400 Bad Request`: Invalid payload format, query parameters, or semantic error (e.g. refund request for already refunded sale).
- `401 Unauthorized`: Token expired or invalid signature. Must refresh OAuth token.
- `403 Forbidden`: Insufficient permissions or incorrect developer keys.
- `404 Not Found`: Non-existent resource (e.g. invalid product ID or ticket code).
- `429 Too Many Requests`: Rate limit exceeded. Must implement exponential backoff.
- `500 Internal Server Error`: Platform-level failure.

### 1.3. Rate Limiting

- **Quota:** Strict maximum of **500 calls per minute** (combining read and write operations).
- **Control Headers:** Every API response includes limit headers that should be monitored to prevent hitting a `429`:
  - `RateLimit-Limit` / `X-RateLimit-Limit-Minute`: Total quota per minute.
  - `RateLimit-Remaining` / `X-RateLimit-Remaining-Minute`: Remaining requests in current window.
  - `RateLimit-Reset`: Time remaining in seconds before reset.

### 1.4. Pagination (Cursor-Based)

- **Parameters:** Collection endpoints accept `max_results` (int, default 50) and `page_token` (string, the cursor cursor).
- **Format:** All collection responses return a standard structure:
  ```json
  {
    "items": [...],
    "page_info": {
      "total_results": 120,
      "next_page_token": "eyJwYWdlIjoyLCJzaXplIjo1MH0=",
      "prev_page_token": "eyJwYWdlIjoxLCJzaXplIjo1MH0=",
      "results_per_page": 50
    }
  }
  ```

### 1.5. Custom Response (X-Hotmart-Custom-Response)

- **Optimization:** Use this header to specify only the JSON fields your application needs, preventing over-fetching and decreasing payload size.
- **Usage:** Set the `X-Hotmart-Custom-Response` header to a comma-separated list of fields (e.g., `items(transaction,status),page_info(next_page_token)`).

### 1.6. Sandbox Environment

- **Domain:** For development and integration testing, replace the production host (`api-sec-vlc.hotmart.com` or `developers.hotmart.com`) with:
  `https://sandbox.hotmart.com/`
- **Behaviors:** Integrations behave identically to production but return mock/fictitious data, ensuring zero impact on live customers or finances.

---

## 2. Domain References

To preserve the context window and prevent token bloat, the documentation is modularized. **Identify the domain of your current task and load ONLY the corresponding reference file.**

1. **Authentication (`auth`)**
   - **File Path:** [auth.md](./references/auth.md)
   - **Topics:** OAuth 2.0 flow, token generation, and client credential setup.

2. **Products (`products`)**
   - **File Path:** [products.md](./references/products.md)
   - **Topics:** Product catalogs, active formats, available offers, and pricing plans.

3. **Coupons (`coupons`)**
   - **File Path:** [coupons.md](./references/coupons.md)
   - **Topics:** CRUD coupons, campaign tracking, and validation checkout integration.

4. **Subscriptions (`subscriptions`)**
   - **File Path:** [subscriptions.md](./references/subscriptions.md)
   - **Topics:** Subscriptions list, status changes, cancellations, reactivations, billing due dates, and batch processes.

5. **Sales (`sales`)**
   - **File Path:** [sales.md](./references/sales.md)
   - **Topics:** Sales history, commission summaries, pricing details (tax/fee breakdowns), buyers/participants, and refund processing.

6. **Members Area (`club`)**
   - **File Path:** [club.md](./references/club.md)
   - **Topics:** Students verification, module lists, lessons (pages), and subdomain tracking.

7. **Event Tickets (`tickets`)**
   - **File Path:** [tickets.md](./references/tickets.md)
   - **Topics:** Event detail retrieval, participant lists, QR Code ticketing, and check-in audits.

8. **Installments Negotiation (`negotiation`)**
   - **File Path:** [negotiation.md](./references/negotiation.md)
   - **Topics:** Creating payment and installment renegotiation proposals for overdue billings.

---

## 3. Guidelines for Implementing Hotmart API Calls

1. **Strict Progressive Disclosure:** When writing code, DO NOT read all reference files. Read the task, map it to a specific domain above, and view only the required `.md` reference file.
2. **Resilience & Token Handling:** Always implement robust token refresh handling. If a request fails with a `401 Unauthorized`, trigger a token refresh flow and automatically retry the failed request.
3. **Over-fetching Mitigation:** ALWAYS specify the `X-Hotmart-Custom-Response` header if your application only consumes a subset of the returned properties.
4. **Strong Typing:** Define exact TypeScript interfaces mapping the nested elements in each domain reference. Timestamps are routinely returned in **milliseconds** (Unix Epoch) and must be parsed accordingly.
