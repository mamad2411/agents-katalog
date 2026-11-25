---
name: new-api-spec
description: Generate a Playwright API test file covering success, errors, auth failure, and invalid input. Use when the user runs /new-api-spec or asks for tests for an API endpoint.
---

# /new-api-spec — Generate an API Test File

**Type:** API
**Description:** Generates a Playwright API test file for a given endpoint, covering success, error, auth failure, and invalid input with response schema validation.

---

## Input Format

The user provides:
- An endpoint path (e.g. `/api/users`)
- The HTTP methods to cover (GET / POST / PUT / DELETE)
- Optionally, the expected response shape and auth requirement

Ask up to 3 clarifying questions if the schema or auth model is unclear.

## Output Format

An API test file at `tests/api/[feature-name]/[feature].api.spec.ts` following the API conventions in CLAUDE.md:
- Imports `test, expect` from `@playwright/test`
- Uses the `request` fixture
- Validates status code and response schema with `toMatchObject`
- Uses `process.env.API_TOKEN` for auth — never hardcoded
- Covers success, error, auth failure (401), and invalid input (400)

## Step-by-Step Instructions

1. Read the API test conventions in CLAUDE.md.
2. **Probe the endpoint first** (one `curl` per case) to learn its real semantics before
   writing assertions. Two common deviations from the template:
   - Some APIs always answer HTTP 200 and embed the real status in the body
     (e.g. `{"responseCode": 405}`). Assert on the body field, and note the quirk
     in a comment at the top of the spec.
   - Some APIs serve JSON with a `text/html` content type — use
     `JSON.parse(await response.text())` instead of `response.json()` if parsing fails.
3. **Match the API's actual auth model.** Bearer tokens are the template default, but
   not universal — if auth is credential-based (e.g. a `verifyLogin` endpoint), the
   "auth failure" case is wrong/missing credentials, not a missing header.
4. Determine the feature folder (kebab-case) and file name with the `.api.spec.ts` suffix.
5. For each method, generate tests covering:
   - **Success** — valid request → expected status + schema (`toMatchObject`).
   - **Auth failure** — no/invalid token → 401 (or the API's credential-failure equivalent).
   - **Invalid input** — bad payload → 400.
   - **Error/edge** — not found, conflict, unsupported method, etc., as relevant.
6. Read auth tokens and URLs from environment variables only. Use `data/factories/`
   for request payloads that need realistic data.
7. Group tests in a `test.describe('[Endpoint] API')` block.
8. Save to `tests/api/[feature-name]/[feature].api.spec.ts`.
9. Suggest `/api-coverage` to see overall API coverage.

## Rules

- Always validate both status code and schema.
- Always cover success, error, auth failure, and invalid input.
- Never hardcode tokens, URLs, or credentials.
- File name uses kebab-case + `.api.spec.ts`.
