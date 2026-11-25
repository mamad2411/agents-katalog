---
name: python-testing
description: Python testing workflow covering Pytest, FastAPI testing, Factory Boy, mocking, integration testing, property-based testing with Hypothesis, coverage, xdist parallelization, and AI-focused regression testing.
origin: AI Dev Kit
---

# Python Testing

Comprehensive Python testing patterns: Pytest fixtures and parametrization, FastAPI
TestClient async patterns, Factory Boy test data, mocking strategies, integration testing
with test containers, property-based testing with Hypothesis, coverage configuration, xdist
parallelization, and AI-focused regression testing for prompts and embedding APIs.

## When to Use

- Writing unit, integration, or E2E tests for Python codebases.
- Testing FastAPI endpoints with async TestClient and dependency overrides.
- Creating test data factories with Factory Boy (traits, sequences, sub-factories).
- Mocking external services, time, randomness, or HTTP responses.
- Setting up integration tests with real databases (testcontainers, fixtures).
- Property-based testing with Hypothesis (strategies, state machines).
- Configuring coverage thresholds, reports, and parallel test execution.
- Building regression suites for AI/ML outputs (golden datasets, contract tests).

## Core Concepts

### 1. Pytest — Fixtures, Parametrization, Marks, Plugins

**Fixture Scopes and Organization:**

```python
# tests/conftest.py — root-level shared fixtures
import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture(scope="session")
def event_loop_policy():
    """Use uvloop for faster async tests (optional)."""
    import uvloop
    return uvloop.new_event_loop_policy()


@pytest.fixture
def mock_datetime():
    """Freeze time for deterministic tests."""
    from freezegun import freeze_time
    frozen = datetime(2024, 6, 15, 12, 0, 0)
    with freeze_time(frozen) as frozen_time:
        yield frozen_time


@pytest.fixture
def sample_user_data():
    return {
        "email": "test @example.com",
        "name": "Test User",
        "age": 30,
    }


# tests/users/conftest.py — module-specific fixtures
@pytest.fixture
def user_service(mock_user_repo, mock_event_bus):
    from app.services.user_service import UserService
    return UserService(repo=mock_user_repo, publisher=mock_event_bus)


@pytest.fixture
def mock_user_repo():
    repo = AsyncMock()
    repo.get_by_email.return_value = None
    repo.create.return_value = User(
        id=uuid4(), email="test @example.com", name="Test"
    )
    return repo


@pytest.fixture
def mock_event_bus():
    return AsyncMock()
```

**Parametrization:**

```python
import pytest


@pytest.mark.parametrize(
    "email,expected_valid",
    [
        ("valid @example.com", True),
        ("invalid-email", False),
        ("@missing-local.com", False),
        ("missing-domain @", False),
        ("spaces @ example.com", False),
        ("unicode @tëst.com", True),
    ],
)
def test_email_validation(email: str, expected_valid: bool) -> None:
    from app.schemas.user import UserCreate
    if expected_valid:
        # Should not raise
        UserCreate(email=email, name="Test", password="Str0ngP@ss!")
    else:
        with pytest.raises(ValueError, match="Invalid email"):
            UserCreate(email=email, name="Test", password="Str0ngP@ss!")


@pytest.mark.parametrize(
    "plan,revenue,expected_discount",
    [
        ("free", 0.0, 0.0),
        ("pro", 49.99, 0.0),
        ("pro", 99.99, 9.999),
        ("enterprise", 200.0, 30.0),
    ],
)
def test_discount_calculation(plan, revenue, expected_discount):
    result = calculate_discount(plan, revenue)
    assert result == pytest.approx(expected_discount, rel=1e-3)
```

**Marks and Skip:**

```python
@pytest.mark.slow
def test_large_dataset_processing():
    """Takes >5 seconds — skip in CI fast mode."""
    ...


@pytest.mark.integration
def test_database_migration():
    """Requires real database — skip in unit test runs."""
    ...


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Unix-specific path behavior",
)
def test_unix_paths():
    ...


# conftest.py — configure mark behavior
def pytest_collection_modifyitems(config, items):
    """Auto-skip slow tests unless --run-slow is passed."""
    if config.getoption("--run-slow"):
        return
    skip_slow = pytest.mark.skip(reason="need --run-slow option")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
```

**Useful Plugins:**

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = """
    --strict-markers
    --strict-config
    --tb=short
    --durations=20
    --maxfail=1
    -v
"""
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests requiring external services",
    "unit: fast isolated unit tests",
]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["app"]
branch = true
omit = ["tests/*", "app/__main__.py"]

[tool.coverage.report]
fail_under = 80
show_missing = true
skip_empty = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]
```

### 2. FastAPI Testing — TestClient, Async, Dependency Overriding

```python
# tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import create_app
from app.config import Settings
from app.database import Base, get_db_session

TEST_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):
    """Per-test isolated session with rollback."""
    factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session):
    """FastAPI TestClient with overridden DB dependency."""
    settings = Settings(database_url=TEST_URL, secret_key="test-secret")
    app = create_app(settings)

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# tests/test_users_api.py
import pytest
from httpx import AsyncClient


class TestUserEndpoints:
    async def test_create_user_returns_envelope(self, client: AsyncClient) -> None:
        payload = {
            "email": "new @example.com",
            "name": "New User",
            "password": "Str0ngP@ss123!",
        }
        resp = await client.post("/api/v1/users", json=payload)

        assert resp.status_code == 201
        body = resp.json()
        assert body["success"] is True
        assert body["data"]["email"] == "new @example.com"
        assert body["data"]["id"] is not None
        assert "error" not in (body.get("error") or {})

    async def test_create_duplicate_user_409(self, client: AsyncClient) -> None:
        payload = {
            "email": "dup @example.com",
            "name": "Dup",
            "password": "Str0ngP@ss123!",
        }
        await client.post("/api/v1/users", json=payload)

        resp = await client.post("/api/v1/users", json=payload)
        assert resp.status_code == 409
        assert resp.json()["error"]["code"] == 409

    async def test_get_nonexistent_user_404(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/users/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404

    async def test_list_users_paginated(self, client: AsyncClient) -> None:
        # Seed data
        for i in range(25):
            await client.post("/api/v1/users", json={
                "email": f"user{i} @example.com",
                "name": f"User {i}",
                "password": "Str0ngP@ss123!",
            })

        resp = await client.get("/api/v1/users?page=1&page_size=10")
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["data"]["items"]) == 10
        assert body["data"]["meta"]["total"] >= 25
        assert body["data"]["meta"]["page"] == 1

    async def test_invalid_payload_422(self, client: AsyncClient) -> None:
        resp = await client.post("/api/v1/users", json={
            "email": "not-an-email",
            "name": "",
            "password": "short",
        })
        assert resp.status_code == 422
        errors = resp.json()["detail"]
        assert any("email" in str(e).lower() for e in errors)

    async def test_health_endpoint_public(self, client: AsyncClient) -> None:
        """Health endpoint should work without auth."""
        resp = await client.get("/api/v1/health")
        assert resp.status_code == 200
```

**Testing WebSocket Endpoints:**

```python
import pytest
from fastapi.testclient import TestClient
from starlette.testclient import TestClient as StarletteTestClient


def test_websocket_echo():
    from app.main import create_app
    app = create_app(Settings())

    with TestClient(app) as tc:
        with tc.websocket_connect("/ws/test-room/client-1") as ws:
            ws.send_json({"type": "ping", "data": "hello"})
            data = ws.receive_json()
            assert data["type"] == "message"
            assert data["data"] == {"type": "ping", "data": "hello"}
```

### 3. Factory Boy — Test Data Factories

```python
# tests/factories.py
import factory
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.entities import User, Order


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid4)
    email = factory.Sequence(lambda n: f"user{n} @example.com")
    name = factory.Faker("name")
    is_active = True
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))

    class Params:
        # Traits for conditional attributes
        inactive = factory.Trait(is_active=False)
        admin = factory.Trait(
            email=factory.Sequence(lambda n: f"admin{n} @example.com"),
            name=factory.Faker("name", prefix="Admin"),
        )


class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    id = factory.Sequence(lambda n: 1000 + n)
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute("user.id")
    amount = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    order_date = factory.LazyFunction(lambda: datetime.now(timezone.utc))


# Usage in tests
def test_create_user_with_factory(db_session):
    user = UserFactory(email="specific @example.com", name="Specific")
    # user is a plain domain entity — not persisted


async def test_order_belongs_to_user(db_session):
    user = UserFactory()
    order = OrderFactory(user=user)

    repo = SQLAlchemyUserRepository(db_session)
    await repo.create(user)

    fetched = await repo.get_by_id(user.id)
    assert fetched is not None
    assert len(fetched.orders) == 0  # order not persisted to DB


# Building multiple
users = UserFactory.create_batch(10)  # creates 10 persisted users (if model supports it)
users = UserFactory.build_batch(10)   # builds 10 without persisting
```

### 4. Mocking — External Services, Time, Randomness

```python
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
from freezegun import freeze_time
import pytest


# Mocking HTTP responses
@patch("httpx.AsyncClient.get")
async def test_external_api_call(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"id": 1, "name": "Item"}]}
    mock_get.return_value = mock_response

    result = await fetch_external_data("https://api.example.com/items")
    assert len(result) == 1
    mock_get.assert_called_once_with("https://api.example.com/items")


# Mocking async services
async def test_service_uses_repo():
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = UserFactory.build()

    service = UserService(repo=mock_repo, publisher=AsyncMock())
    result = await service.get_user("some-uuid")

    assert result is not None
    mock_repo.get_by_id.assert_called_once_with("some-uuid")


# Freezing time
@freeze_time("2024-06-15 12:00:00")
def test_timestamp_is_deterministic():
    user = UserFactory()
    assert user.created_at == datetime(2024, 6, 15, 12, 0, 0)


# Mocking randomness
@patch("random.uniform", return_value=0.5)
def test_sampling_is_reproducible(mock_uniform):
    result = stochastic_process()
    assert result == expected_value_with_05


# Context manager for partial mocking
def test_partial_service_mock():
    with patch.object(UserService, "validate_email", return_value=True):
        service = UserService(mock_repo, mock_publisher)
        # validate_email always returns True in this block
        result = service.create_user("anything", "name")
```

### 5. Integration Testing — Database, Test Containers, Migrations

```python
# Using testcontainers for real PostgreSQL
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine
from alembic.config import Config
from alembic import command


@pytest.fixture(scope="session")
def postgres_container():
    """Starts a real PostgreSQL container for integration tests."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture
async def integration_engine(postgres_container):
    """Engine connected to container with migrations applied."""
    url = postgres_container.get_connection_url(drivername="asyncpg")
    engine = create_async_engine(url, echo=False)

    # Run Alembic migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", url.replace("+asyncpg", ""))
    command.upgrade(alembic_cfg, "head")

    yield engine

    await engine.dispose()


@pytest.mark.integration
async def test_user_repository_against_real_db(integration_engine):
    from sqlalchemy.ext.asyncio import async_sessionmaker

    session_factory = async_sessionmaker(integration_engine, expire_on_commit=False)
    async with session_factory() as session:
        repo = SQLAlchemyUserRepository(session)

        user = User(email="integration @test.com", name="Integration Test")
        created = await repo.create(user)

        fetched = await repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.email == "integration @test.com"


@pytest.mark.integration
def test_migration_upgrade_downgrade(postgres_container):
    """Verify migrations can upgrade and downgrade cleanly."""
    url = postgres_container.get_connection_url(drivername="postgres")
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", url)

    # Upgrade to head
    command.upgrade(alembic_cfg, "head")

    # Downgrade to base
    command.downgrade(alembic_cfg, "base")

    # Upgrade again — should succeed without errors
    command.upgrade(alembic_cfg, "head")
```

### 6. Property-Based Testing — Hypothesis

```python
from hypothesis import given, settings, strategies as st
import pytest


# Strategies
@st.composite
def valid_user_payloads(draw):
    """Generate valid UserCreate payloads."""
    email = draw(st.emails())
    name = draw(st.text(min_size=1, max_size=150).filter(str.strip))
    password = draw(
        st.from_regex(r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d! @#$%^&*]{8,128}$")
    )
    return {"email": email, "name": name, "password": password}


@given(valid_user_payloads())
@settings(max_examples=200)
def test_valid_user_payload_always_creates_user(payload):
    """For any valid payload, UserCreate should instantiate."""
    from app.schemas.user import UserCreate
    model = UserCreate(**payload)
    assert model.email == payload["email"].lower()
    assert model.name == payload["name"].strip()


@given(st.emails(), st.text(min_size=1, max_size=150))
def test_create_then_get_user_is_idempotent(email, name):
    """Creating and fetching a user should round-trip correctly."""
    # This would need a real repo fixture
    ...


# State machine testing for a cache
from hypothesis.stateful import (
    RuleBasedStateMachine,
    rule,
    invariant,
    precondition,
)


class CacheStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.cache = {}

    @rule(key=st.text(), value=st.integers())
    def put(self, key, value):
        self.cache[key] = value

    @rule(key=st.text())
    @precondition(lambda self: True)
    def get(self, key):
        result = self.cache.get(key)
        assert result is None or isinstance(result, int)

    @rule(key=st.text())
    def delete(self, key):
        self.cache.pop(key, None)

    @invariant()
    def cache_size_bounded(self):
        assert len(self.cache) < 10_000


TestCache = CacheStateMachine.TestCase


# Testing ID generation
@given(st.uuids())
def test_uuid_parse_is_reversible(uid):
    """UUID string conversion should round-trip."""
    s = str(uid)
    parsed = __import__("uuid").UUID(s)
    assert parsed == uid
```

### 7. Coverage — Configuration, Thresholds, Reporting

```toml
# pyproject.toml
[tool.coverage.run]
source = ["app"]
branch = true
parallel = true  # Required for xdist
omit = [
    "tests/*",
    "app/__main__.py",
    "app/**/__init__.py",
]

[tool.coverage.report]
fail_under = 80
show_missing = true
skip_empty = true
precision = 1
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
    "raise NotImplementedError",
    "\\.\\.\\.",
]

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

```bash
# Run with coverage
pytest --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml

# Fail if coverage drops below threshold
pytest --cov=app --cov-fail-under=80

# Combine parallel coverage (from xdist)
coverage combine
coverage report --show-missing
```

### 8. Test Performance — xdist Parallelization

```bash
# Install
pip install pytest-xdist

# Run tests in parallel across all CPU cores
pytest -n auto

# Run with specific worker count
pytest -n 4

# Parallel + coverage (combine after)
pytest -n auto --cov=app --cov-report=term-missing
coverage combine
coverage report

# Run only changed tests (pytest-testmon)
pip install pytest-testmon
pytest --testmon

# Profile slow tests
pytest --durations=20 --durations-min=1.0
```

```toml
# pyproject.toml — xdist-compatible coverage
[tool.pytest.ini_options]
addopts = "-n auto --cov=app --cov-report=term-missing"
```

### 9. AI-Focused Regression Testing

**Golden Dataset Testing for Prompts:**

```python
# tests/ai/test_prompt_regression.py
import json
import pytest
from pathlib import Path


GOLDEN_DIR = Path("eval/golden")


def load_golden_dataset(name: str) -> list[dict]:
    """Load golden input/expected-output pairs."""
    path = GOLDEN_DIR / f"{name}.json"
    with open(path) as f:
        return json.load(f)


class TestPromptGolden:
    """Verify prompt outputs haven't regressed against golden datasets."""

    @pytest.mark.parametrize(
        "case",
        load_golden_dataset("rag_retrieval"),
        ids=lambda c: c["id"],
    )
    def test_rag_retrieval_matches_golden(self, case):
        """Retrieval for a given query should match expected document IDs."""
        query = case["input"]["query"]
        expected_ids = set(case["expected"]["doc_ids"])

        results = retrieve_documents(query, top_k=5)
        result_ids = {doc["id"] for doc in results}

        # At least 80% overlap with golden
        overlap = len(result_ids & expected_ids) / len(expected_ids)
        assert overlap >= 0.8, (
            f"Retrieval overlap {overlap:.2f} < 0.80 for query: {query[:50]}"
        )

    @pytest.mark.parametrize(
        "case",
        load_golden_dataset("classification"),
        ids=lambda c: c["id"],
    )
    def test_classification_accuracy(self, case):
        result = classify_intent(case["input"]["message"])
        assert result == case["expected"]["intent"]
```

**Contract Tests for Embedding APIs:**

```python
class TestEmbeddingAPIContract:
    """Ensure embedding API behavior is stable across model/version changes."""

    def test_embedding_dimensions_are_consistent(self):
        """Same model should always produce same-dimensional vectors."""
        embedding = generate_embedding("test sentence")
        assert len(embedding) == 1536  # text-embedding-3-small

    def test_similarity_is_symmetric(self):
        """cos(a, b) should equal cos(b, a)."""
        a = generate_embedding("hello world")
        b = generate_embedding("world hello")
        sim_ab = cosine_similarity(a, b)
        sim_ba = cosine_similarity(b, a)
        assert sim_ab == pytest.approx(sim_ba, rel=1e-6)

    def test_identical_inputs_produce_identical_embeddings(self):
        """Same input should produce same output (deterministic API)."""
        text = "deterministic test input"
        e1 = generate_embedding(text)
        e2 = generate_embedding(text)
        assert e1 == pytest.approx(e2, rel=1e-6)

    def test_semantic_similarity_ordered_correctly(self):
        """Related concepts should be closer than unrelated ones."""
        dog = generate_embedding("dog")
        cat = generate_embedding("cat")
        car = generate_embedding("car")
        pizza = generate_embedding("pizza")

        assert cosine_similarity(dog, cat) > cosine_similarity(dog, car)
        assert cosine_similarity(dog, cat) > cosine_similarity(dog, pizza)

    def test_empty_input_handling(self):
        """Empty string should not crash the API."""
        embedding = generate_embedding("")
        assert len(embedding) == 1536
        assert all(isinstance(x, float) for x in embedding)
```

## Anti-Patterns

- **Testing through the database** — assert domain behavior, not ORM internals.
- **Shared mutable fixtures** — each test gets a fresh, isolated fixture.
- **Over-mocking** — mock only external boundaries (HTTP, DB, filesystem); test real logic.
- **Testing implementation details** — test observable behavior, not private method calls.
- **No teardown in integration tests** — always rollback or drop test data.
- **Golden tests without maintenance plan** — version golden files, update intentionally.
- **Running slow tests in CI fast path** — use marks to gate long-running tests.
- **Skipping coverage on error paths** — the `fail_under` threshold should include failure branches.
- **Testing prompts by visual inspection** — use golden datasets + automated overlap metrics.
- **Assuming embedding API is stable** — contract tests catch model version changes.

## Best Practices

1. **80%+ coverage minimum** — enforce with `--cov-fail-under=80` in CI.
2. **One assertion per test** — or related assertions about the same behavior.
3. **Arrange-Act-Assert** — structure every test with clear setup, execution, verification.
4. **Factory Boy over manual dicts** — reusable, traitable, sequence-safe test data.
5. **`dependency_overrides` in FastAPI tests** — swap real services for mocks per test.
6. **Rollback after every test** — `await session.rollback()` in fixture teardown.
7. **`freeze_time` for temporal logic** — never rely on wall clock in tests.
8. **Hypothesis for boundary logic** — validate input ranges, edge cases, invariants.
9. **`-n auto` for parallel** — xdist cuts test time by 3-5x on multi-core machines.
10. **Testcontainers for integration** — real PostgreSQL, not SQLite-in-memory for PG-specific features.
11. **Golden datasets versioned in git** — track prompt regression over time.
12. **Embedding contract tests** — symmetry, determinism, semantic ordering, dimension stability.
13. **`pytest --durations=20`** — identify and optimize the slowest tests.
14. **Branch coverage** — `branch = true` catches uncovered `if/else` paths.
15. **`exclude_lines` for boilerplate** — don't punish coverage for `TYPE_CHECKING` blocks.

## Related Skills

- `python-patterns` — Pandas, NumPy, SQLAlchemy 2.0, data validation, performance
- `backend-patterns` — FastAPI architecture, TestClient patterns, error contracts
- `e2e-testing` — Playwright end-to-end test patterns
- `eval-harness` — AI evaluation frameworks, pass@k metrics, graded outputs
- `tdd-workflow` — RED-GREEN-REFACTOR cycle, test-first development
- `verification-loop` — Continuous verification and quality gates
