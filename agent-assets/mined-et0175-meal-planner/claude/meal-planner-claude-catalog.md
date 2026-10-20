# Catalog Service — Claude context (CARD-003)

## Architecture decisions

- **Auth**: tokens validated by calling `GET /auth/session` on the Identity service (`IDENTITY_SERVICE_URL` env var). The `verify_token` FastAPI dependency is in `auth_middleware.py`. Tests override it via `app.dependency_overrides`.
- **diet_tags storage**: `JSON` column (not PostgreSQL `ARRAY`) so tests run on SQLite in-memory. The column stores a list of strings. Filtering uses SQLAlchemy's `.contains()`.
- **Localization (FR-037, ADR-0012)**: product names are localized via `product_translations (product_id, locale, name)`, `UNIQUE(product_id, locale)`. `products.name` stays the canonical English value and fallback. Reads `LEFT JOIN` translations on the requested `locale` and `COALESCE(translation.name, products.name)`; search and sort run on that resolved name. `list_products` returns `(list[(Product, resolved_name)], total)` and is **paginated** (`limit`/`offset`, real `total`); `get_product` returns `(Product, resolved_name)`. The router applies the resolved name via `model_copy(update={"name": ...})`. Authoring upserts a translation row for the request's `locale` (default `en`). PostgreSQL gets a per-locale `pg_trgm` GIN index (`ix_product_translations_name_trgm`) for NFR-002 at 10k products/language.
- **Localization phases (ADR-0012)**: Phase 1 (done) = product-name translation + pagination + locale-resolved reads. **Deferred**: category/diet-tag vocab tables + their translations (FR-037 AC-124 — `category`/`diet_tags` stay free-text/JSON for now), dropping the legacy `products.name`/`category`/`diet_tags` columns, and the `locale` column on Planning/Shopping denormalized names (cross-service, CARD-005/007).
- **External import (FR-038, ADR-0013)**: global products are bulk-loaded from USDA FoodData Central (Foundation + SR Legacy) via `python -m importer --dir <fdc_csv_dir>`. `products.source`/`external_id` (migration 0003) with a partial `UNIQUE(source, external_id)` make re-import an idempotent upsert. Energy uses a fallback chain (nutrient 1008 → 2048 → 2047), and when no energy nutrient exists it is **derived from macros via Atwater factors** (4·protein + 9·fat + 4·carbs); a product with neither energy nor macros keeps 0.0 but is still imported. Missing macros default to 0.0; units capped at 10 (INV-004) with a canonical `100 g` base. Imported names are English-only; USDA has no diet labels so `diet_tags` are empty. User products keep `source=NULL` and are never touched by the importer.
- **Week flag upsert**: the `week_flags` table stores one row per (product_id, user_id). `set_week_flag` does a select-then-update-or-insert pattern. Monday rollover: Step 1 promotes `next_week → this_week` (capturing the timestamp), Step 2 clears any `this_week` rows whose `updated_at` is still older than the rollover time.
- **Soft-delete**: `products.is_deleted = True`. All queries filter `is_deleted == False`. Hard deletes are never used.
- **INV-006**: global products have `owner_id = NULL`. Any edit/delete attempt by any user returns 403. User can only edit their own (non-null) products.
- **INV-004/007**: enforced in service layer (not DB). Unit limit checked at create time and at PUT time when units are replaced.
- **Scheduler**: APScheduler `AsyncIOScheduler` with `CronTrigger(day_of_week='mon', hour=0, minute=0, timezone='UTC')` started in `lifespan`.
- **mypy**: run with `--explicit-package-bases` to avoid module double-registration. APScheduler has no stubs — `[mypy-apscheduler.*] ignore_missing_imports = true` in `mypy.ini`.

## File map

- `main.py` — FastAPI app factory, router registration, APScheduler lifespan
- `auth_middleware.py` — `verify_token` dependency (HTTP call to Identity service)
- `db/models.py` — `Product`, `ProductTranslation`, `ProductUnit`, `NutritionPer100g`, `WeekFlag` ORM models
- `db/migrations/versions/0002_product_translations.py` — adds `product_translations`, backfills `name`→`en`, builds the per-locale trigram index
- `db/migrations/versions/0003_product_provenance.py` — adds `products.source`/`external_id` + partial unique index for idempotent imports
- `importer/usda.py` — parse USDA FDC CSVs → `ImportRecord` (energy fallback, unit cap)
- `importer/loader.py` — idempotent batched upsert keyed on `(source, external_id)`
- `importer/__main__.py` — `python -m importer --dir <fdc_csv_dir>` CLI
- `scripts/bench_search.py` — NFR-002 scale benchmark: seeds 10k/locale (source='scale_bench'), measures search p95 via the API, cleans up
- `db/engine.py` — `AsyncEngine` / `AsyncSession` factory; `reset_engine()` for tests
- `db/migrations/env.py` — Alembic async migration runner
- `db/migrations/versions/0001_initial_schema.py` — initial schema migration
- `query/schemas.py` — read schemas: `ProductSummary`, `ProductDetail`, `ProductListResponse`
- `query/service.py` — `list_products`, `get_product`, `count_user_products`
- `query/router.py` — `GET /products`, `GET /products/:id`
- `authoring/schemas.py` — `CreateProductRequest`, `UpdateProductRequest`, `ProductResponse`
- `authoring/service.py` — `create_product`, `update_product`, `delete_product`; `UnitDict` TypedDict
- `authoring/router.py` — `POST /products`, `PUT /products/:id`, `DELETE /products/:id`
- `weekflag/schemas.py` — `SetWeekFlagRequest`, `WeekFlagResponse`
- `weekflag/service.py` — `set_week_flag`, `rollover_week_flags`
- `weekflag/router.py` — `PUT /products/:id/week-flag`
- `scheduler/jobs.py` — `run_weekly_rollover` async job
- `tests/conftest.py` — SQLite in-memory fixtures: `test_engine`, `db`, `client`, `client_user2`, `anon_client`
- `tests/test_query.py` — FR-010/011/012, NFR-002 tests
- `tests/test_authoring.py` — FR-013/014/032 tests
- `tests/test_weekflag.py` — FR-015 tests including rollover
- `tests/test_localization.py` — FR-037 tests: locale resolution, English fallback, creator-locale authoring, pagination
- `tests/test_import.py` — FR-038 tests: FDC parse (energy fallback, unit cap), idempotent load
- `seed.py` — idempotent seed with 5 realistic products
- `pytest.ini` — `asyncio_mode = auto`, testpaths = tests

## How to run tests

```bash
cd backend/catalog
python3 -m pytest tests/ -q
```

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite+aiosqlite:///./catalog.db` | PostgreSQL async URL for prod (`postgresql+asyncpg://...`) |
| `IDENTITY_SERVICE_URL` | `http://identity:8000` | Base URL of the Identity service for token validation |

## Constraints / invariants

- `INV-004`: max 10 units per product — enforced in `authoring/service.py:create_product` and `update_product`
- `INV-005`: all nutrition values >= 0 — enforced by Pydantic `ge=0` field validators in `NutritionIn`
- `INV-006`: only owner can edit/delete; global products (`owner_id=null`) → 403 always
- `INV-007`: max 500 user products per user — checked before insert in `create_product`
- `NFR-002`: list reads are paginated (`limit`/`offset`). **Validated at 10k products/language** (`scripts/bench_search.py`): search p95 ≈ 30 ms (≤ 200 ms). The localized search predicate is `t.name ILIKE :q OR (t.name IS NULL AND p.name ILIKE :q)` (not `COALESCE(...) ILIKE`, which can never use a per-column index) so it is trigram-index-eligible. At 10k/language the planner correctly seq-scans anyway (cheaper than the GIN index at this size); the trgm indexes become effective only at much larger scale. See `docs/database-localization-scale-analysis.md` §8.
- `FR-037`/`CON-007`/`ADR-0012`: per-locale product names via `product_translations`; reads resolve to `?locale=` with English fallback; user products stored in creator's locale
- `ADR-0002`: `GET /products?week_flag=this_week&user_id=X` is the Planning service's read endpoint
- `ADR-0009`: Monday 00:00 UTC rollover via APScheduler CronTrigger
