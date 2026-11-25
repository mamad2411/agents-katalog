---
name: "restful-convention"
description: "Enforces RESTful API design conventions for HTTP interface layer. Invoke when designing REST APIs, writing Controller classes, defining endpoints, or reviewing API design."
---

# RESTful API Design Conventions

This skill encodes RESTful API design principles for HTTP interface layer. Apply when designing, implementing, or reviewing REST API endpoints.

| Section | Reference File | When to Read |
|---------|---------------|-------------|
| URI Design | `references/uri-design.md` | When designing API paths, naming endpoints, structuring URLs |
| HTTP Methods | `references/http-methods.md` | When choosing HTTP verbs, handling CRUD operations, ensuring idempotency |
| Response & Status Codes | `references/response-status.md` | When returning API responses, selecting HTTP status codes, formatting error messages |
| Versioning & Filtering | `references/versioning-filtering.md` | When versioning APIs, adding pagination, sorting, or filtering parameters |

## How to Apply

### When Designing New APIs
Read `references/uri-design.md` → define resource paths → choose HTTP methods from `references/http-methods.md` → plan responses from `references/response-status.md` → add versioning from `references/versioning-filtering.md`.

### When Writing Controller Code
1. Verify URI follows naming rules (lowercase, plural nouns, no verbs)
2. Map CRUD to correct HTTP verbs (GET/POST/PUT/PATCH/DELETE)
3. Return proper HTTP status codes (not always 200)
4. Include version prefix in URI path

### When Reviewing API Code
1. Read the corresponding reference file based on the code area
2. Verify each rule against the code
3. Categorize violations as **Mandatory** (must fix), **Recommended** (should fix), or **Reference** (nice to have)