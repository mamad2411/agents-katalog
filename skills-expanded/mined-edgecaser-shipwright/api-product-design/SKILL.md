---
name: api-product-design
description: "For PMs who own APIs, platforms, or developer-facing products. Covers API endpoint design, developer experience (DX), versioning strategy, documentation standards, and developer onboarding. Treats the API as a product with its own personas, jobs-to-be-done, and success metrics."
category: technical
default_depth: standard
---

# API Product Design

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

For PMs who own APIs, platforms, or developer-facing products. Covers API endpoint design, developer experience (DX), versioning strategy, documentation standards, and developer onboarding. Treats the API as a product with its own personas, jobs-to-be-done, and success metrics.

## When to Use

- Designing a new public or partner API
- Improving developer experience for an existing API
- Planning API versioning and deprecation
- Creating developer documentation and getting-started guides
- Evaluating API usability through developer feedback

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Single internal endpoint or quick API extension | API Strategy (persona + JTBD only) + Endpoint Design (one resource) |
| **Standard** | New public API surface or partner integration | All sections |
| **Deep** | Platform API launch or developer ecosystem play | All sections + SDK design per language, sandbox test plan, migration guide from prior version |

**Omit rules:** At Light depth, skip Authentication & Security, Versioning & Deprecation, and Developer Experience. Produce only persona, JTBD, and the endpoint resource table.

## Framework

### Step 1: API Product Strategy

```markdown
## API Product Overview

### API Persona
- **Primary developer:** [Who uses this API, e.g., "Backend engineers at mid-market SaaS companies integrating our data into their dashboards"]
- **Technical proficiency:** [Junior / Mid / Senior]
- **Language ecosystem:** [Python, JavaScript, Go, etc.]
- **Integration context:** [What they're building with our API]

### Job-to-Be-Done
When I [situation, e.g., "need to pull customer analytics into my internal dashboard"],
I want to [goal, e.g., "query our API for real-time usage metrics"],
So I can [outcome, e.g., "show my leadership team live product health data"].

### API Success Metrics
| Metric | Current | Target | Why It Matters |
|---|---|---|---|
| Time to first successful API call | [X min/hours] | < [target] | DX quality indicator |
| API adoption rate (% of customers using API) | [X]% | [target] | Platform value |
| Error rate (4xx + 5xx) | [X]% | < [target] | Reliability |
| P95 latency | [X]ms | < [target] | Performance |
| Developer NPS / satisfaction | [score] | > [target] | DX quality |
| API calls per active integration | [N] | [target] | Engagement depth |
```

### Step 2: Endpoint Design

```markdown
## API Design Principles

### Naming Conventions
- Use nouns for resources, not verbs: `/users` not `/getUsers`
- Plural resource names: `/projects` not `/project`
- Nested resources for relationships: `/projects/{id}/members`
- Consistent casing: [snake_case / camelCase] for fields
- API version in URL path: `/api/v2/...`

### Resource Design
For each resource:

#### Resource: [Name, e.g., "Projects"]

**Endpoints:**
| Method | Path | Description | Auth Required |
|---|---|---|---|
| GET | /api/v2/projects | List all projects | Yes |
| POST | /api/v2/projects | Create a project | Yes |
| GET | /api/v2/projects/{id} | Get a specific project | Yes |
| PATCH | /api/v2/projects/{id} | Update a project | Yes |
| DELETE | /api/v2/projects/{id} | Delete a project | Yes |

**Query Parameters (for list endpoints):**
| Parameter | Type | Default | Description |
|---|---|---|---|
| page | integer | 1 | Page number for pagination |
| per_page | integer | 20 | Items per page (max 100) |
| sort | string | "created_at" | Sort field |
| order | string | "desc" | Sort direction (asc/desc) |
| filter[status] | string | | Filter by status |

**Response Schema:**
```json
{
  "data": [
    {
      "id": "proj_abc123",
      "type": "project",
      "attributes": {
        "name": "string",
        "status": "active | archived",
        "created_at": "ISO 8601",
        "updated_at": "ISO 8601"
      },
      "relationships": {
        "owner": { "id": "user_xyz", "type": "user" }
      }
    }
  ],
  "meta": {
    "total": 42,
    "page": 1,
    "per_page": 20
  }
}
```

### Pagination Strategy
- **Approach:** [Offset-based / Cursor-based / Keyset]
- **Rationale:** [Why this approach fits your data patterns]
- **Max page size:** [100]

### Error Response Format
```json
{
  "error": {
    "code": "validation_error",
    "message": "Human-readable description of what went wrong",
    "details": [
      {
        "field": "name",
        "issue": "required",
        "message": "Name is required"
      }
    ],
    "request_id": "req_abc123"
  }
}
```

### Rate Limiting
| Plan | Rate Limit | Burst | Headers |
|---|---|---|---|
| Free | 60 req/min | 10 req/sec | X-RateLimit-Limit, X-RateLimit-Remaining |
| Pro | 600 req/min | 100 req/sec | Same |
| Enterprise | Custom | Custom | Same |
```

### Step 3: Authentication & Security

```markdown
## Authentication

### Auth Method: [OAuth 2.0 / API Keys / Both]

**API Key Authentication:**
- Keys issued per organization (not per user)
- Prefix: `sk_live_` (production) / `sk_test_` (sandbox)
- Passed via header: `Authorization: Bearer sk_live_abc123`
- Key rotation: Supported, old key valid for 24 hours after rotation

**OAuth 2.0 (for user-context integrations):**
- Grant type: Authorization Code with PKCE
- Token expiry: Access token [1 hour], Refresh token [30 days]
- Scopes: [list of available scopes and what they grant]

### Security Requirements
- [ ] All endpoints require HTTPS (TLS 1.2+)
- [ ] API keys never logged or exposed in URLs
- [ ] Webhook signatures for verification (HMAC-SHA256)
- [ ] IP allowlisting available for enterprise plans
```

### Step 4: Versioning & Deprecation

```markdown
## Versioning Strategy

**Approach:** [URL versioning: /api/v2/... ]

### Compatibility Rules
**Non-breaking changes (no version bump):**
- Adding new endpoints
- Adding new optional fields to responses
- Adding new optional query parameters
- Adding new webhook event types

**Breaking changes (require version bump):**
- Removing or renaming fields
- Changing field types
- Changing endpoint URLs
- Changing error response format
- Changing authentication mechanism

### Deprecation Policy
1. **Announcement:** [6 months] before end-of-life
2. **Sunset header:** `Sunset: [date]` added to all deprecated endpoint responses
3. **Migration guide:** Published with each version bump
4. **Communication:** Email to all API key holders + docs banner + changelog
5. **Grace period:** Deprecated version responds with warnings for [3 months]
6. **End of life:** Returns 410 Gone with migration instructions
```

### Step 5: Developer Experience (DX)

```markdown
## Developer Experience Design

### Getting Started Flow (Time to First Call)
Target: Developer makes their first successful API call in < [N] minutes.

1. **Sign up** → Get API key instantly (no approval queue)
2. **Quickstart guide** → Copy-paste example that works
3. **First call** → a copy-paste terminal command they can run immediately
4. **SDK install** → `pip install your-sdk` / `npm install your-sdk`
5. **Build something** → Tutorial that builds a real mini-project

### Documentation Structure
```
docs/
├── Getting Started
│   ├── Authentication
│   ├── Quick Start (< 5 min)
│   └── First Integration Tutorial (30 min)
├── API Reference
│   ├── [Resource 1]
│   ├── [Resource 2]
│   └── Errors
├── Guides
│   ├── Pagination
│   ├── Webhooks
│   ├── Rate Limiting
│   └── Migration (v1 → v2)
├── SDKs & Libraries
│   ├── Python
│   ├── JavaScript/TypeScript
│   └── Go
└── Changelog
```

### SDK Design Principles
- **Idiomatic:** Follow language conventions (snake_case for Python, camelCase for JS)
- **Type-safe:** Full type definitions / interfaces
- **Async-first:** Native async/await support
- **Error handling:** Typed exceptions, not generic errors
- **Pagination:** Iterator/generator patterns, not manual page management

### Sandbox / Testing Environment
- Separate test environment with test API keys
- Seed data available for common scenarios
- No rate limits in sandbox
- Webhook testing via [tool, e.g., local tunnel or webhook.site integration]
```

## Minimum Evidence Bar

**Required inputs:** Product brief or PRD identifying the integration need, target developer persona, and at least one concrete use case the API must support.

**Acceptable evidence:** Developer interviews or support tickets showing integration demand, existing internal API usage data, competitive API benchmarks, or documented partner requirements.

**Insufficient evidence:** If no developer persona has been validated with real users or prospects, produce a partial artifact with unanswered sections marked `[TBD, requires: validated developer persona from discovery interviews]` and flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Developer persona, JTBD, endpoint resource structure (must be grounded in validated use cases)
- **Hypotheses:** Adoption rate targets, rate limit tiers, pagination strategy choice (must be labeled as assumptions pending production data)

## Output Format

Produce an API Product Spec with:
1. **API Strategy**, persona, JTBD, success metrics
2. **Endpoint Design**, resource schemas, pagination, errors
3. **Authentication**, auth methods and security
4. **Versioning**, compatibility rules and deprecation policy
5. **Developer Experience**, getting started flow, docs structure, SDK design

**Shipwright Signature (required closing):**
6. **Decision Frame**, recommended API strategy (build vs. extend vs. partner), trade-off, confidence with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, unvalidated persona assumptions, untested rate limits, unknown integration patterns
8. **Pass/Fail Readiness**, PASS if developer persona validated and at least one endpoint schema reviewed by engineering; FAIL if no developer has attempted the proposed getting-started flow (Light depth: FAIL gate scopes to persona validation and endpoint schema review only, since DX/getting-started flow is omitted at Light)
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Designing for internal convenience, not developer experience**, Your database schema is not your API schema
- **No sandbox environment**, Developers won't risk production data to test your API
- **Inconsistent naming**, Mixed casing, plural/singular inconsistency, or verb-based endpoints destroy trust
- **Breaking changes without notice**, This is the fastest way to lose developer trust permanently
- **Documentation as afterthought**, For APIs, docs ARE the product; budget for them accordingly

## Weak vs. Strong Output

**Weak:**
> "The API should support pagination for list endpoints."

No pagination strategy chosen, no max page size, no rationale for offset vs. cursor approach.

**Strong:**
> "List endpoints use cursor-based pagination (cursor + limit, max 100) because the projects table exceeds 500K rows and offset-based pagination degrades past page 5000. Cursor is the opaque `created_at` + `id` composite, returned as `next_cursor` in the response `meta` object."

Specifies the approach, justifies it with data volume, and defines the implementation contract.
