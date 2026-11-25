---
name: "api-documentation"
description: "API documentation at the docs-set level: the Diátaxis grid, OpenAPI example and error patterns, versioning, a getting-started template, error message and changelog formats, common failure modes, and a tooling reference. Use when planning or reviewing an API's documentation as a whole."
---

# API documentation pattern library

## Diátaxis grid

```
                  Action            Reflection
  Practical   | Tutorial    | How-to guide |
  Theoretical | Reference   | Explanation  |
```

Mix at your peril. The grid is from https://diataxis.fr.

## OpenAPI patterns

### Multiple examples per endpoint

```yaml
requestBody:
  content:
    application/json:
      examples:
        minimal:
          summary: Smallest valid request
          value: { ... }
        full:
          summary: All optional fields populated
          value: { ... }
        edge_case:
          summary: Common edge case
          value: { ... }
```

### Error response template

```yaml
'400':
  description: Bad request
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/Error'
      examples:
        validation_error:
          value:
            code: VALIDATION_ERROR
            message: line_items must contain at least one item
            errors: [{ field: line_items, code: MIN_LENGTH }]
            request_id: req_a8f3
```

### Versioning

URL-based (`/v2/orders`) is the easiest for tooling. Header-based (`Accept: application/vnd.acme.v2+json`) is cleaner but harder for clients.

## Getting-started template

```markdown
# Getting started

## What you'll build
A working integration that creates an order and handles the webhook.

## Prerequisites
- API key (sign up at acme.com/signup)
- curl or HTTP client
- ~30 minutes

## 1. Authenticate
[Working curl command, copy-paste-runnable, with placeholder for their key]
Expected response: { ... }

## 2. Create your first order
[Working curl]
Expected: order created, response shows id

## 3. Handle the webhook
[Sample webhook payload]
[Signature verification example in TypeScript]

## What's next
- Authentication options → ...
- Full API reference → ...
- Language SDKs → ...
```

## Error message format

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Human-readable summary",
  "errors": [{ "field": "...", "code": "...", "details": "..." }],
  "request_id": "req_..."
}
```

`request_id` lets users reference the specific request in support tickets.

## Changelog format

Customer-facing:

```markdown
## v2.5.0 — 2026-05-15

### Breaking changes (call out FIRST)
- ...

### Added
- ...

### Changed
- ...

### Deprecated
- ...

### Fixed
- ...
```

Internal: more detail, including refactors and infrastructure changes that don't surface to users.

## Common mistakes catalog

### "Docs are out of date"
Likely: docs not in version control or not in PR review. Move docs to repo. Reviewers must approve doc changes alongside code.

### "Developers can't find anything"
IA problem. Apply Diátaxis. Audit each page's category.

### "Examples don't work"
Examples aren't tested. Move examples to tested code (doctest, snippet tests). Run in CI.

### "Authentication confused everyone"
Auth is the highest-bounce page. Spend disproportionate effort. Include multiple auth methods if you support them.

### "Error responses are useless"
"Invalid request" tells nothing. Error catalog with structured codes + actions tells everything.

## Tooling reference

- **Renderers**: Redocly, Mintlify (paid), Scalar, Bump.sh, Stoplight, Slate
- **Spec lint**: Spectral
- **Breaking-change**: openapi-diff
- **SDK generation**: openapi-generator (FOSS), Stainless (paid), Speakeasy (paid)
- **Test examples**: doctest (in source), external snippet tests

## Cross-references
- `markdown-discipline-skills` repo — for the prose style of doc pages
- `style-guides` plugin — for voice + vocabulary
- `error-messages` plugin — for the in-product UX writing layer
- Diátaxis: https://diataxis.fr
