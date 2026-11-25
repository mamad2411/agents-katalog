---
name: backend-stack-python
description: "A Python backend: uv, Ruff and a type checker; FastAPI with pydantic v2 models, dependencies for auth and sessions, async versus sync, background tasks versus a real queue, SQLAlchemy 2 async and Alembic, pydantic-settings, problem-details errors, structlog, uvicorn or gunicorn workers, Celery, Dramatiq or arq, pytest with httpx and Testcontainers; and Django with DRF when the project uses it. Read when building or changing a Python backend."
---

# Python

The generated FastAPI app: `async def` routes that call `requests` and a
sync session, freezing every other request; ORM objects returned without a
response model; `Base.metadata.create_all()` at start instead of migrations;
`os.environ` read everywhere; `BackgroundTasks` for work that must survive a
restart; `except Exception: return {"error": str(e)}`. The generated Django
app: `fields = "__all__"`, a query per row, `DEBUG = True`. The backend rules
are in the `backend` skill; these are Python's own.

## 1. Setup

- The project's tool (uv, Poetry, pip-tools) and its lock file; a
  `pyproject.toml`; the Python version pinned. Type hints everywhere, checked
  with mypy or pyright, formatted and linted with Ruff.
- A new service: Python 3.13 or 3.14 (Django 6 needs 3.12, SQLAlchemy 2.1
  3.11), uv (`uv add fastapi`, `uv add --dev pytest`, `uv sync --locked` in CI
  and Docker, `uv run ...`), `requires-python` and `.python-version`.
- Ruff with `select = ["E", "F", "I", "B", "UP", "ASYNC", "S"]`: the `ASYNC`
  rules catch `time.sleep` and blocking HTTP calls inside `async def`.
- mypy `strict = true` with the `pydantic.mypy` plugin (without it,
  `Settings()` reports missing arguments), or pyright in strict mode. Astral's
  `ty` is still pre-1.0: not the gate yet.

## 2. FastAPI

- Layout: `app/main.py` builds the app (a `create_app()` for tests, with a
  `lifespan` that disposes the engine); a package per feature
  (`app/orders/router.py`, `service.py`, `repository.py`, `schemas.py`,
  `models.py`); `app/core/` for config, database, security and errors.
- **Schemas**: pydantic v2 models for every request and response
  (`OrderCreate`, `OrderOut`), with `model_config = ConfigDict(extra="forbid")`
  on inputs; routes declare `response_model` so only those fields go out.
  Never return ORM objects without a response model.
- Limits in the types: `Annotated[int, Field(ge=1, le=100)]`,
  `StringConstraints(strip_whitespace=True, max_length=500)`, `UUID`,
  `AwareDatetime` (refuses a time without a zone), `EmailStr` (with
  `email-validator`), money as `int` minor units or `Decimal`, never `float`.

```python
class OrderLineIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    product_id: UUID
    quantity: Annotated[int, Field(ge=1, le=100)]

class OrderIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    lines: Annotated[list[OrderLineIn], Field(min_length=1, max_length=50)]
    note: Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)] | None = None

class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # reads the ORM object's attributes
    id: UUID
    status: str
    total_minor: int
    created_at: AwareDatetime

@router.post("", status_code=201, response_model=OrderOut)
async def place_order(body: OrderIn, session: SessionDep, user: CurrentUser, response: Response) -> Order:
    order = await service.place_order(session, user, body)
    response.headers["Location"] = f"/orders/{order.id}"
    return order
```

- **Dependencies** for what each request needs: the database session
  (`Depends(get_session)`, one per request, closed after), the current user
  (`Depends(current_user)`), permissions (`Depends(require("orders.refund"))`).
  Name them once as `Annotated` aliases (`SessionDep`, `CurrentUser`); a
  dependency used twice in one request runs once.
- **Errors**: domain exceptions raised from services, turned into the format
  in `backend-errors` by `@app.exception_handler`; `HTTPException` only in
  routes. Override the handler for `RequestValidationError` so validation
  errors use the same format:

```python
@app.exception_handler(DomainError)
async def domain_error(request: Request, exc: DomainError) -> JSONResponse:
    return problem(exc.status, exc.code)  # JSONResponse, media_type="application/problem+json"

@app.exception_handler(RequestValidationError)
async def invalid_request(request: Request, exc: RequestValidationError) -> JSONResponse:
    # ("body", "lines", 0, "quantity") -> "lines[0].quantity"; map pydantic's types to your codes
    errors = [{"field": field_path(e["loc"][1:]), "code": e["type"]} for e in exc.errors()]
    return problem(400, "validation_failed", errors=errors)
```

- Anything unexpected is caught once, in the request middleware that binds
  the request id: logged with its stack, answered with a generic `500`
  problem carrying `requestId`.

## 3. Async or sync

- `async def` routes only with async libraries all the way down (asyncpg,
  httpx, async SQLAlchemy); a blocking call in an `async def` stalls every
  request. With a sync driver, write plain `def` routes.
- A `def` route runs in a thread pool (40 threads by default through
  AnyIO), so it blocks one thread, not the loop. One unavoidable blocking
  call inside async code goes through `await anyio.to_thread.run_sync(fn)`
  (or `asyncio.to_thread`).
- The swaps: `requests` for one `httpx.AsyncClient` per app (made in the
  lifespan, `timeout=httpx.Timeout(10.0, connect=3.0)`), `time.sleep` for
  `await asyncio.sleep`, psycopg2 for asyncpg or psycopg 3.
- CPU-bound work (PDFs, images, big pandas jobs) goes to a process pool or a
  queue, never the event loop. `PYTHONASYNCIODEBUG=1` logs every callback
  that holds the loop over 100 ms.

## 4. Background work

- `BackgroundTasks` run in the same process after the response: lost on a
  restart or crash, never retried. Fine for best effort (a cache warm), not
  for an email, a charge or a webhook.
- Work that must happen goes to a queue: Celery (Redis or RabbitMQ; the
  default beside Django), Dramatiq (simpler, sound defaults), arq or taskiq
  (asyncio-native). The payload is ids, enqueued after the commit
  (`backend-jobs`).
- Celery defaults to change: `task_acks_late=True` with
  `task_reject_on_worker_lost=True` (a task on a dead worker runs again, so
  tasks are idempotent), `worker_prefetch_multiplier=1` for long tasks,
  `task_soft_time_limit` below `task_time_limit`, and per task
  `autoretry_for=(TransientError,)`, `retry_backoff=True`, `max_retries=5`.

## 5. Data

- SQLAlchemy 2.0 style (`select()`, `Mapped[...]`, `session.execute`),
  sessions from one `sessionmaker`, transactions with `async with
  session.begin()`; Alembic for migrations, autogenerated then read and
  corrected before committing.
- Eager loading on purpose (`selectinload`, `joinedload`) to avoid N+1; the
  rest in `backend-data`.

```python
engine = create_async_engine(str(settings.database_url), pool_size=5, max_overflow=5,
                             pool_timeout=5, pool_pre_ping=True)
# expire_on_commit=False: reading an attribute after commit must not need a query.
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid7)  # Python 3.14
    status: Mapped[str] = mapped_column(default="open")
    total_minor: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # lazy="raise": an unplanned load is an error in tests, not a hidden query per row.
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", lazy="raise")

async with session.begin():  # race-free: two payments cannot both see "open"
    order = await session.scalar(update(Order)
        .where(Order.id == order_id, Order.status == "open")
        .values(status="paid").returning(Order))
    if order is None:
        raise Conflict("already_paid")
```

- In async code a lazy load raises `MissingGreenlet`; `lazy="raise"` makes it
  fail the same way in every test, with a clear message.
- `with_for_update()` only when you must read, decide, then write.
- Alembic: `alembic init -t async migrations`, a naming convention on
  `MetaData` so constraints get stable names, autogenerate read line by line
  (a rename comes out as drop and add), `alembic upgrade head` as a release
  step, and `alembic check` in CI to fail when models and migrations differ.

## 6. Config and logs

- `pydantic-settings` (`class Settings(BaseSettings)`) read once and passed or
  imported; required fields have no default; secrets as `SecretStr`.

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    environment: Literal["development", "test", "production"] = "development"
    database_url: PostgresDsn          # required: no default
    payments_api_key: SecretStr        # prints as '**********'

@lru_cache
def get_settings() -> Settings:
    return Settings()  # a missing or malformed variable raises here, naming it
```

- The standard `logging` with a JSON formatter or structlog, with the request
  id in a context variable set by middleware
  (`structlog.contextvars.bind_contextvars(request_id=...)`) and one line per
  request with the route template (`request.scope["route"].path`).
- structlog: `merge_contextvars`, `TimeStamper(fmt="iso", utc=True)`,
  `JSONRenderer()` in production, and exceptions through
  `ExceptionRenderer(ExceptionDictTransformer(show_locals=False))`: the
  default `dict_tracebacks` writes every frame's local variables, secrets
  included. Uvicorn's access log off (`--no-access-log`) when you write your
  own line.

## 7. Serving

- Run with `uvicorn app.main:app --reload` in development; in production
  `uvicorn` with workers (or gunicorn with uvicorn workers) behind a proxy.
- Workers: about one per core, or one per container when the platform scales
  containers. Under gunicorn use `uvicorn_worker.UvicornWorker` from the
  `uvicorn-worker` package; `uvicorn.workers` is deprecated.
- Behind a proxy, `--forwarded-allow-ips` names it (the default trusts only
  127.0.0.1), or client IPs and `https` are wrong; never `*` when clients can
  reach the app directly.
- On `SIGTERM` uvicorn stops accepting, waits for requests in flight up to
  `--timeout-graceful-shutdown 20`, then runs the lifespan's shutdown.

## 8. Tests

pytest with pytest-asyncio or anyio; `httpx.AsyncClient` with
`ASGITransport(app=app)` for FastAPI, DRF's `APIClient` for Django;
dependency overrides for the session and the user; a real database per
`backend-testing`; respx for outbound HTTP.

- pytest-asyncio 1.x: `asyncio_mode = "auto"`, and with a session-scoped
  engine fixture both `asyncio_default_fixture_loop_scope` and
  `asyncio_default_test_loop_scope` set to `"session"`, or asyncpg
  connections end up on the wrong event loop.
- One transaction per test with `join_transaction_mode="create_savepoint"`
  (the fixture is in `backend-testing`), PostgreSQL from
  `testcontainers.community.postgres` (the old `testcontainers.postgres`
  path still imports, with a warning).
- `ASGITransport` does not run the lifespan: wrap the app in
  `asgi_lifespan.LifespanManager` when startup matters to the test.
- time-machine for the clock; factory_boy or polyfactory for data.

## 9. Django and DRF

When the project is Django:

- Apps per feature, models with constraints (`UniqueConstraint`,
  `CheckConstraint`), migrations from `makemigrations`, read before
  committing.
- DRF serializers with explicit `fields` (never `"__all__"`), permission
  classes on every view, querysets filtered by the user in `get_queryset`,
  `select_related` and `prefetch_related` for relations.
- `transaction.atomic()` around writes that belong together;
  `F("stock") - n` with a filter for race-free updates.
- Settings from the environment (django-environ or os.environ in one
  place), `DEBUG = False` and `ALLOWED_HOSTS` set in production.
- Closed by default: `DEFAULT_PERMISSION_CLASSES` set to `IsAuthenticated`,
  `DEFAULT_PAGINATION_CLASS` with `PAGE_SIZE` 25, throttle rates for
  anonymous and user requests.
- `select_for_update()` inside `atomic()` to read then write;
  `transaction.on_commit(lambda: send_receipt.delay(order.id))` so a task
  never runs before its data exists; `Prefetch("items", queryset=...)` for
  filtered relations; `assertNumQueries` (or pytest-django's
  `django_assert_num_queries`) pins a list view's query count.
- Behind a proxy: `SECURE_PROXY_SSL_HEADER`, `CSRF_TRUSTED_ORIGINS`, secure
  cookies; `python manage.py check --deploy` passes.
- PostgreSQL with psycopg 3: Django's pool (`"OPTIONS": {"pool": True}`, 5.1
  and later) or `CONN_MAX_AGE = 60` with `CONN_HEALTH_CHECKS = True`, never
  both (Django refuses the pair).
- Django 6: `BigAutoField` is the default key, CSP is built in
  (`SECURE_CSP` with its middleware), and `django.tasks` defines tasks but
  ships only development backends: production work still needs Celery or a
  third-party backend.
- Views stay sync unless there is async I/O to wait for; the ORM's async
  methods run the sync code in a thread. django-ninja when the team wants
  FastAPI-style typed endpoints inside Django.

## Check it

`ruff check`, `ruff format --check`, the type checker, `pytest`; `alembic
upgrade head` on an empty database, then `alembic check`; for Django,
`python manage.py makemigrations --check --dry-run` and `check --deploy`.
Then start it and call the endpoints with `curl` or the `/docs` page: a bad
body gives a `400` listing every field, an unknown field included.

## Avoid

Returning ORM objects without a response model; `extra` fields accepted on
inputs; blocking calls inside `async def`; a session shared across requests;
`"__all__"` serializers; `DEBUG = True` in production; settings read with
`os.environ` all over the code; migrations committed without reading them;
`create_all()` in place of migrations; `BackgroundTasks` for work that must
happen; `float` for money; naive datetimes; exception locals in logs; a task
queued before its transaction commits.
