# Ultra Project Development Rules (Django Styleguide-Aligned)

- Structure per app:
  - `models/` (domain models split per entity, invariants in `clean()`, DB constraints)
  - `selectors/` (read-only query composition, accepts `filters: dict`)
  - `services/` (write workflows, transactional, orchestrate nested ops)
  - `api/serializers.py`, `api/views.py`, `api/urls.py` (I/O layer only)
- Keep business rules close to models; use managers for common lookups; services for multi-model flows.
- Use soft-delete via `BaseModel.soft_delete`; guard deletes with domain checks.
- Prefer `UniqueConstraint` and indexes for duplication/lookup rules.
- Selectors: no side effects; always return QuerySets; use `select_related/prefetch_related`.
- Services: validate first, then write; wrap in transactions; return saved instances.
- Serializers: light validation only; do not implement business rules.
- Views: delegate to selectors/services; avoid direct model logic.
- OpenAPI: annotate computed fields and ambiguous path params with drf-spectacular.
- Tests: models (constraints/clean), services (flows), API (status/payload/errors).
