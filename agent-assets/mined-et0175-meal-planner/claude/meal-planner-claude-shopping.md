# Shopping List Service — Claude context

## Key architecture decisions (CARD-007)

- **Single active list per user (ADR-0008)**: `shopping_lists` has a unique constraint on `user_id`. Each generate replaces the previous list via upsert (delete items + update row).
- **Staleness (ADR-0003)**: `is_stale` flag on `shopping_lists`. Set via `POST /shopping/events/plan-changed` (stub for future event bus). Cleared on generate/refresh.
- **Default date range (ADR-0007)**: `GET /shopping` uses current ISO week Mon–Sun. Returns existing list if one exists; only generates on first access.
- **Planning client**: Calls `GET /plan?week=YYYY-WW` once per ISO week in the range using `asyncio.gather` for concurrency. Forwards the user's Bearer token.
- **Catalog client**: Calls `GET /products/{id}` for each unique `product_id` after aggregation, to enrich items with category. Best-effort — falls back to `None` per product if catalog is unavailable.
- **Aggregation key**: `(product_id, unit)` — same product in different units gets separate rows.
- **INV-011**: `from_date <= to_date` enforced by Pydantic `model_validator` → 422.
- **INV-012**: Only mark list stale when the changed assignment date falls within the list's stored date range.
- **Index conflict**: `list_id` column in `shopping_list_items` uses `index=False` in `mapped_column` because the index is defined explicitly in `__table_args__`. Both active causes SQLite to error "index already exists".
- **Auth status codes**: FastAPI 0.138+ returns 401 (not 403) for missing Bearer credentials. Tests accept `in (401, 403)`.

## File map

| File | Role |
|------|------|
| `main.py` | FastAPI app factory, lifespan (HTTP clients + DB engine cleanup) |
| `auth_middleware.py` | Token validation via Identity service (HTTP call) |
| `db/models.py` | SQLAlchemy 2 ORM: `ShoppingList`, `ShoppingListItem` |
| `db/engine.py` | Async engine / session factory; `reset_engine()` for tests |
| `db/migrations/env.py` | Alembic env wired to `Base.metadata` |
| `db/migrations/versions/0001_initial_schema.py` | Create `shopping_lists` + `shopping_list_items` |
| `generator/schemas.py` | Pydantic v2: `GenerateRequest`, `ShoppingListResponse`, `ShoppingItemResponse`, `PlanEventRequest` |
| `generator/service.py` | Core business logic: generate, upsert, mark stale, refresh |
| `generator/planning_client.py` | HTTP calls to Planning service (week-by-week, concurrent) |
| `generator/catalog_client.py` | HTTP calls to Catalog for category enrichment (concurrent, best-effort) |
| `generator/router.py` | `GET /shopping`, `POST /shopping/generate` |
| `staleness/router.py` | `POST /shopping/refresh`, `POST /shopping/events/plan-changed` |
| `pdf/service.py` | reportlab PDF generator grouped by category |
| `pdf/router.py` | `POST /shopping/export/pdf` |
| `tests/conftest.py` | Test fixtures: in-memory SQLite engine, mocked auth, `make_client()` |
| `tests/test_generator.py` | AC-070–074, AC-119 — generation + aggregation |
| `tests/test_staleness.py` | AC-075, AC-076, AC-103–105 — staleness + refresh |
| `tests/test_pdf.py` | AC-077, AC-120, NFR-004 — PDF export |
| `tests/test_performance.py` | NFR-003 — 31 days × 4 slots × 5 items < 500ms |

## How to run tests

```bash
cd backend/shopping
pip install -r requirements.txt
python3 -m pytest -v
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./shopping.db` | PostgreSQL connection string in production |
| `IDENTITY_SERVICE_URL` | `http://identity:8000` | Token validation service |
| `PLANNING_SERVICE_URL` | `http://planning:8000` | Meal plan assignments source |
| `CATALOG_SERVICE_URL` | `http://catalog:8000` | Product category enrichment |

## Non-obvious constraints

- `GET /shopping` returns the stored list (may be stale); it does NOT regenerate on every call.
- `POST /shopping/refresh` regenerates using the stored `from_date`/`to_date`, not the current ISO week.
- The `events/plan-changed` endpoint is a **stub** — in the future an event bus would call it. Currently the frontend calls it after plan mutations.
- Planning service returns no `category` field in `AssignmentResponse`; category is fetched separately from Catalog.
- Token forwarding: the shopping service re-uses the user's Bearer token when calling Planning — do NOT create a service-to-service token here.
