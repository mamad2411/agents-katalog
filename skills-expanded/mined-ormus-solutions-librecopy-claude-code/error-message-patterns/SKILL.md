---
name: "error-message-patterns"
description: "Error message patterns: the three-part message, RFC 7807 type, title, and detail, error code hierarchies, HTTP status semantics, user vs developer errors, localization-ready strings, and anti-patterns such as blaming the user. Use when writing or reviewing error messages."
---

# Error Message Patterns

## The Three-Part Error Message

Every error message should answer three questions:
1. What happened? (context - what operation failed on what resource)
2. Why? (cause - the specific condition that prevented success)
3. Now what? (remedy - the concrete action to take)

```
# Bad: answers none of the three questions
"An error occurred"
"Error 422"
"Invalid input"

# Bad: answers what but not why or how
"Validation failed"

# Good: answers all three
"Unable to create the subscription (what): the selected plan 'enterprise_annual'
requires a verified business email address (why). Add a verified business email
at /account/email or choose a different plan (how to fix)."
```

## RFC 7807 Problem Details

The standard JSON structure for API error responses. Use `application/problem+json` as the Content-Type.

```json
{
  "type": "https://api.example.com/errors/rate-limit-exceeded",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "You have made 1000 requests in the last 60 seconds. The limit is 1000/minute.",
  "instance": "/api/v2/users",
  "error_id": "err_01HXA83KPQRST",
  "retry_after": 47
}
```

### type vs title vs detail
- `type`: Stable URI, same for all instances of this error type. Points to documentation.
- `title`: Human-readable label, same for all instances. Use for programmatic display (e.g., toast notifications).
- `detail`: Specific to this occurrence. Includes the actual values, field names, context.

```json
// type and title are the same for all rate limit errors:
"type": "https://api.example.com/errors/rate-limit-exceeded"
"title": "Rate Limit Exceeded"

// detail changes per occurrence:
"detail": "You have made 1000 requests in the last 60 seconds. The limit is 1000/minute."
// vs
"detail": "You have made 50 requests in the last second. The burst limit is 50/second."
```

## Error Code Hierarchy Design

Use namespaced string codes, not raw integers. String codes are self-documenting in logs.

```
# Namespace pattern: DOMAIN_CATEGORY_SPECIFIC

AUTH_TOKEN_MISSING          # No token in request
AUTH_TOKEN_EXPIRED          # Token is past expiry
AUTH_TOKEN_INVALID          # Token signature invalid
AUTH_SCOPE_INSUFFICIENT     # Valid token, wrong scope

PAYMENT_CARD_DECLINED       # Processor declined the charge
PAYMENT_CARD_EXPIRED        # Card expiration date past
PAYMENT_INSUFFICIENT_FUNDS  # Not enough balance
PAYMENT_CURRENCY_UNSUPPORTED # Currency not available

ORDER_ITEM_OUT_OF_STOCK     # Cannot fulfill line item
ORDER_MINIMUM_NOT_MET       # Below minimum order value
ORDER_DUPLICATE             # Idempotency key reused with different params
```

### Numeric range assignment (when using codes)
```
1000-1999: Authentication and authorization
2000-2999: Validation and input errors
3000-3999: Payment and billing
4000-4999: Resource state conflicts
5000-5999: External service failures
9000-9999: Internal server errors (do not expose details)
```

## HTTP Status Code Semantics

Correct status codes prevent unnecessary support tickets:

```
400 Bad Request:
  Request structure is invalid. JSON parse error, wrong content type.
  The client must change the request format.

401 Unauthorized:
  No valid authentication. Client must authenticate.
  Include WWW-Authenticate header indicating the scheme.

403 Forbidden:
  Authenticated but not authorized. Client is known, action is denied.
  Do NOT use 404 to hide existence of a resource (that's security theater
  for most cases; use it deliberately when appropriate).

404 Not Found:
  Resource does not exist, or does not exist for this user.
  Use consistently.

409 Conflict:
  State conflict. Duplicate creation, edit conflict, stale version.
  Include the conflicting state in the response.

422 Unprocessable:
  Request is valid JSON and correct content type, but fails validation.
  Prefer 422 over 400 for business rule violations.
  Always include per-field errors.

429 Too Many Requests:
  Rate limit exceeded. Include Retry-After header.
```

## User-Facing vs Developer-Facing Errors

User-facing (displayed in UI):
```json
{
  "title": "Payment Failed",
  "detail": "Your card was declined. Try a different payment method or contact your bank."
}
```

Developer-facing (included in the same response for API consumers):
```json
{
  "title": "Payment Failed",
  "detail": "Card declined by processor.",
  "error_id": "err_01HXA83K",
  "processor_code": "insufficient_funds",
  "help_url": "https://docs.example.com/errors/payment-card-declined"
}
```

What is **never** in the response:
- Stack traces
- SQL queries
- Internal file paths
- System usernames or service account names
- Database error messages
- Environment variable names

## Localization-Ready Error Strings

Write error strings for localization from day one:

```json
// Bad: hardcoded sentence that cannot be translated naturally
"The field email is required and must be a valid email address"

// Good: template with interpolation placeholder
"The field '{{field}}' must be a valid {{format}} (e.g., {{example}})"
```

Avoid:
- Idioms: "The token has been burned" (doesn't translate well)
- Directional language: "See above" (position changes with layout)
- Concatenated strings: `"Invalid " + field` (word order differs by language)

## Anti-Patterns

### Leaking internal details
```json
// Bad: exposes internal architecture
{
  "error": "SQLSTATE[23000]: Integrity constraint violation: Duplicate entry 'user@example.com' for key 'users.email'"
}

// Good: user-meaningful error
{
  "type": "https://api.example.com/errors/duplicate-email",
  "title": "Email Already Registered",
  "status": 409,
  "detail": "An account with this email address already exists. Sign in instead or use password recovery."
}
```

### Single validation error message
```json
// Bad: forces user to resubmit to find other errors
{ "error": "email is invalid" }

// Good: all errors at once
{
  "errors": [
    { "field": "email", "message": "Must be a valid email address" },
    { "field": "password", "message": "Must be at least 12 characters" }
  ]
}
```

### Blaming the user
```
# Bad: accusatory
"You provided an invalid token"
"Your request is malformed"

# Good: describes the condition
"The authentication token is invalid or has expired"
"The request body is not valid JSON"
```

### No actionable remedy
```
# Bad: tells the user what happened but not what to do
"Your subscription has expired"

# Good: tells the user what happened and what to do next
"Your subscription expired on March 15, 2025. Renew at /billing/subscription to restore access."
```

## References
- [RFC 7807 Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc7807)
- [RFC 9457 (updates to RFC 7807)](https://datatracker.ietf.org/doc/html/rfc9457)
- [HTTP Status Codes](https://httpstatuses.io/)
- [Error Messages: Being Humble, Human, and Helpful](https://www.nngroup.com/articles/error-message-guidelines/)
