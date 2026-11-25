---
name: "api-doc-patterns"
description: "Writing inside an OpenAPI spec: summary vs description, parameter and requestBody documentation with examples, complete response coverage, string format annotations, x-codeSamples, and anti-patterns such as fake examples. Use when documenting individual operations in a spec."
---

# API Documentation Patterns

## Operation Documentation

### summary vs description
`summary` is the one-line entry in navigation and index tables. `description` is the full explanation. Both matter.

```yaml
# Bad: summary that restates the method and path
summary: GET user by ID

# Good: summary that describes intent
summary: Retrieve a user

# description adds what summary cannot:
description: |
  Returns a single active user. Suspended users still return 200 with
  `status: suspended`. Deleted users return 404.

  If the authenticated user does not have `read:users` scope, returns 403.
```

### Parameter documentation
Every parameter needs `description`, `example`, and schema constraints.

```yaml
parameters:
  - name: user_id
    in: path
    required: true
    description: Unique identifier of the user. Format is UUID v4.
    schema:
      type: string
      format: uuid
    example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

  - name: include
    in: query
    description: |
      Comma-separated list of related resources to embed in the response.
      Supported values: `profile`, `settings`, `subscriptions`.
    schema:
      type: string
      pattern: '^[a-z_]+(,[a-z_]+)*$'
    example: "profile,settings"

  - name: X-Idempotency-Key
    in: header
    description: |
      Client-generated UUID to make the request idempotent. If a request
      with this key was already processed, the original response is returned
      without re-processing. Required for POST /payments.
    schema:
      type: string
      format: uuid
    required: false
```

### requestBody with examples

```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/CreateOrderRequest'
      examples:
        digital_product:
          summary: Order for a digital product
          value:
            items:
              - product_id: "prod_abc123"
                quantity: 1
            payment_method_id: "pm_xyz789"
        physical_with_shipping:
          summary: Order requiring shipping address
          value:
            items:
              - product_id: "prod_def456"
                quantity: 2
            shipping_address:
              line1: "123 Main St"
              city: "Austin"
              state: "TX"
              postal_code: "78701"
              country: "US"
```

## Response Documentation

### Complete response coverage

Every operation should document at minimum:
- Primary success (200 or 201)
- 400 Bad Request for invalid input
- 401 Unauthorized when auth required
- 403 Forbidden when access denied
- 404 Not Found for resource operations
- 422 Unprocessable Entity for validation failures
- 429 Too Many Requests
- 500 Internal Server Error

```yaml
responses:
  '201':
    description: Order created successfully
    headers:
      Location:
        description: URL of the created order resource
        schema:
          type: string
          format: uri
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Order'
  '422':
    description: Validation failed
    content:
      application/problem+json:
        schema:
          $ref: '#/components/schemas/ValidationProblem'
        example:
          type: "https://api.acme.com/errors/validation-failed"
          title: "Validation Failed"
          status: 422
          errors:
            - field: "items[0].quantity"
              code: "out_of_range"
              message: "Quantity must be between 1 and 99"
  '429':
    description: Rate limit exceeded
    headers:
      Retry-After:
        description: Seconds until the rate limit resets
        schema:
          type: integer
      X-RateLimit-Remaining:
        schema:
          type: integer
```

## String Format Annotations

Use standard formats for tooling support (validation, mock generation, SDK typing):

```yaml
properties:
  id:
    type: string
    format: uuid
  created_at:
    type: string
    format: date-time        # ISO 8601 with timezone
  birth_date:
    type: string
    format: date             # YYYY-MM-DD
  webhook_url:
    type: string
    format: uri
  email:
    type: string
    format: email
  amount:
    type: integer
    description: Amount in cents (USD). $10.00 = 1000
  currency:
    type: string
    pattern: '^[A-Z]{3}$'
    description: ISO 4217 currency code
    example: "USD"
```

## x-codeSamples Extension (Redoc)

```yaml
/users/{user_id}:
  get:
    x-codeSamples:
      - lang: Shell
        label: curl
        source: |
          curl -X GET https://api.acme.com/v2/users/usr_abc123 \
            -H "Authorization: Bearer $API_TOKEN"
      - lang: JavaScript
        label: Node.js
        source: |
          const response = await fetch('https://api.acme.com/v2/users/usr_abc123', {
            headers: { 'Authorization': `Bearer ${process.env.API_TOKEN}` },
          });
          const user = await response.json();
      - lang: Python
        label: Python
        source: |
          import httpx
          client = httpx.Client(headers={"Authorization": f"Bearer {api_token}"})
          user = client.get("https://api.acme.com/v2/users/usr_abc123").json()
```

## Anti-Patterns

### Vague descriptions
```yaml
# Bad
description: The user object

# Good
description: |
  Authenticated user making the request. Includes profile data but
  excludes payment methods. Use GET /users/{id}/payments for payment access.
```

### Missing discriminator mapping
```yaml
# Bad: oneOf without discriminator - clients cannot determine which schema applies
schema:
  oneOf:
    - $ref: '#/components/schemas/CreditCardPayment'
    - $ref: '#/components/schemas/BankTransferPayment'

# Good
schema:
  oneOf:
    - $ref: '#/components/schemas/CreditCardPayment'
    - $ref: '#/components/schemas/BankTransferPayment'
  discriminator:
    propertyName: method
    mapping:
      card: '#/components/schemas/CreditCardPayment'
      bank_transfer: '#/components/schemas/BankTransferPayment'
```

### Fake examples
```yaml
# Bad
example:
  id: "string"
  email: "email@example.com"
  created_at: "2024-01-01"

# Good: realistic example usable for testing
example:
  id: "usr_01HX4K9Z2MVNPGR8TQ3W7Y5B6C"
  email: "ada.lovelace@example.com"
  created_at: "2024-03-15T14:32:07.891Z"
  status: "active"
  plan: "pro"
```

### Inline complex schemas
```yaml
# Bad: inline - cannot be reused, hard to maintain
responses:
  '200':
    content:
      application/json:
        schema:
          type: object
          properties:
            id:
              type: string

# Good: named schema
responses:
  '200':
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
```

## References
- [OpenAPI 3.1 Specification](https://spec.openapis.org/oas/v3.1.0)
- [Redocly CLI docs](https://redocly.com/docs/cli/)
- [Spectral ruleset reference](https://docs.stoplight.io/docs/spectral/83527ef2dd8c0-custom-rulesets)
- [RFC 7807 Problem Details](https://datatracker.ietf.org/doc/html/rfc7807)
