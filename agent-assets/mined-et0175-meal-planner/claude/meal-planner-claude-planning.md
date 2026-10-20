# Planning Service — Claude Context (CARD-005)

## Key architecture decisions

- **logging/ stub removed**: The stub `logging/__init__.py` shadowed Python stdlib `logging` and broke all test imports. Renamed log-from-plan functionality to `logplan/` package. Do not recreate `logging/` as a package in this service.
- **Inline nutrition denormalization**: `meal_plan_assignments` stores `kcal_per_unit`, `protein_g_per_unit`, `fat_g_per_unit`, `carbs_g_per_unit` so that PDF export and plan summary work without a runtime call to the Catalog service. The client populates these at assignment-creation time.
- **product_name denormalization**: Also stored inline in `meal_plan_assignments` so PDF renders product names without a Catalog call (NFR-004 < 3 s).
- **Week-flagged products (ADR-0002)**: Only fetched from Catalog for the current ISO week. Falls back to `[]` gracefully if Catalog is unavailable. Uses `mealplan.router.get_this_week_products` (imported at router module level) — patch there in tests, not at `weekflag_reader.service`.
- **NutritionTarget UPSERT**: `PUT /plan/target` is idempotent — exactly one target per user (INV-014). Implemented as get-then-update-or-create.
- **Assignment limit (INV-010)**: Enforced in service layer (`count >= 10_000 → AssignmentLimitError → 409`). Uses `func.count` in DB, not Python-side counting.
- **Dual-client test pattern**: When two client fixtures (`client`, `client_user2`) are in the same test, `app.dependency_overrides` is shared and the last-set fixture wins. Seed user data via `db` fixture directly rather than using both client fixtures for writes.
- **PDF**: Uses `reportlab` pure-Python library. Generates in-memory (`io.BytesIO`), well under the 3 s NFR-004 limit.
- **Log-from-plan (ADR-0001)**: Writes to `tracking_entries` table in the Planning DB. Returns 0 entries (not an error) for empty days / invalid assignment IDs.

## File map

| File | Role |
|------|------|
| `main.py` | FastAPI app factory, router registration, lifespan |
| `auth_middleware.py` | Bearer token validation via Identity service |
| `db/models.py` | ORM models: MealPlanAssignment, NutritionTarget, TrackingEntry |
| `db/engine.py` | AsyncEngine + AsyncSession factory |
| `db/migrations/` | Alembic scripts |
| `mealplan/router.py` | GET /plan, POST/PUT/DELETE/MOVE /plan/assignments, GET /plan/search |
| `mealplan/service.py` | Assignment CRUD, search sort logic |
| `mealplan/schemas.py` | Pydantic request/response models for assignments |
| `target/router.py` | GET /plan/target, PUT /plan/target |
| `target/service.py` | Nutrition target get/upsert |
| `target/schemas.py` | Nutrition target schemas |
| `summary/router.py` | GET /plan/summary |
| `summary/service.py` | Aggregate weekly nutrition totals |
| `summary/schemas.py` | PlanSummaryResponse |
| `logplan/router.py` | POST /plan/log/day, /plan/log/week, /plan/log/item |
| `logplan/service.py` | Create TrackingEntry rows |
| `logplan/schemas.py` | Log request/response schemas |
| `pdf/router.py` | POST /plan/export/pdf |
| `pdf/service.py` | reportlab PDF generation |
| `weekflag_reader/service.py` | HTTP client for Catalog service (week flags + search) |
| `tracking_stub/` | Empty stub package (read UI deferred to v1.1) |
| `tests/conftest.py` | aiosqlite fixtures, auth override helpers |
| `tests/test_mealplan.py` | Assignment CRUD + search tests |
| `tests/test_target.py` | Nutrition target tests |
| `tests/test_log.py` | Log-from-plan tests |
| `tests/test_pdf.py` | PDF export tests |
| `tests/test_summary.py` | Plan summary tests |
| `seed.py` | Idempotent seed script |

## How to run tests

```bash
cd backend/planning
python3 -m pytest tests/ -q
```

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./planning.db` | PostgreSQL connection string |
| `IDENTITY_SERVICE_URL` | `http://identity:8000` | Identity service for token validation |
| `CATALOG_SERVICE_URL` | `http://catalog:8000` | Catalog service for week flags + product search |

## Non-obvious constraints

- `MealSlot` enum values must be lowercase: `breakfast`, `lunch`, `dinner`, `snacks`.
- Week format is ISO `YYYY-WNN` (e.g. `2026-W27`). Legacy `YYYY-WW` (e.g. `2026-27`) is still accepted by the parsers (`int(parts[1].lstrip("W"))`) for backward compatibility, but `_current_iso_week()` now emits the `W`-prefixed form. An omitted `week` param defaults to today's ISO week via `date.today().isocalendar()`.
- The `logging/` directory must NOT exist as a Python package — it shadows `stdlib logging` and breaks pytest + FastAPI logging.
- Inline nutrition fields (`kcal_per_unit` etc.) are nullable. Summary totals use `COALESCE(..., 0.0)` in SQL so NULL values contribute 0 rather than NULL-propagating the sum.
