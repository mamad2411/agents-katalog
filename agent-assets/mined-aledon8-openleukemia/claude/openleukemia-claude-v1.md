# API v1 Memory

Apply this inside `ai-service/app/api/v1/`.

- Preserve stable v1 response shapes unless intentionally changing the API contract.
- Add tests for route behavior when endpoints, schemas, or status behavior change.
- Keep tags and prefixes clear for OpenAPI consumers.
- Version-breaking behavior belongs in a new version, not a silent v1 change.
