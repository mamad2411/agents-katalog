---
name: test-strategy
description: Design a comprehensive testing pyramid strategy covering unit, integration, contract, E2E, and performance tests. Outputs test coverage targets, tooling selection, CI configuration, and quality gates.
argument-hint: [application type, team size, tech stack, deployment frequency, current test coverage]
allowed-tools: Read, Write, Bash
---

# Test Strategy

A test strategy answers four questions: what to test, how much to test, which tools to use, and what must pass before code ships. Without a strategy, teams either test too little (production bugs) or too much at the wrong layer (slow, brittle test suites).

## Process

1. **Inventory the system** — services, integrations, user journeys, risk areas.
2. **Define the testing pyramid** — proportions of unit/integration/E2E tests.
3. **Set coverage targets** — by layer, not a single aggregate number.
4. **Choose tooling** — one test framework per layer per language.
5. **Define quality gates** — what must pass at each stage of CI.
6. **Plan test data** — factories, fixtures, test containers.
7. **Establish flakiness policy** — quarantine, fix within SLA, or delete.
8. **Review test metrics** — coverage trends, test duration, failure rates.

## Output Format

### Testing Pyramid

```
                    ┌────────────────────┐
                    │    E2E / UI Tests   │  5-10%
                    │   (Playwright/      │  Slow, brittle, expensive
                    │    Cypress)         │  Test critical user journeys only
                    ├────────────────────┤
                  ┌─┤ Contract Tests     │  5%
                  │ │ (Pact / Dredd)     │  Verify API contracts
                  └─┼────────────────────┤
               ┌────┤ Integration Tests  │  20-30%
               │    │ (pytest, Jest)     │  DB, cache, external services
               │    │ Real dependencies  │  
               └────┼────────────────────┤
          ┌─────────┤  Unit Tests        │  60-70%
          │         │  (pytest, Jest,    │  Fast, deterministic
          │         │   JUnit)           │  No I/O, pure logic
          └─────────┴────────────────────┘
```

### Coverage Targets by Layer

| Layer | Coverage Target | Measurement | Rationale |
|-------|----------------|-------------|-----------|
| Unit | 80% line coverage | Per-file, tracked in CI | High leverage, fast to run |
| Integration | Critical paths | Endpoint + DB combos | Validates real behavior |
| Contract | 100% of APIs consumed | Per consumer-provider pair | Prevents breaking changes |
| E2E | Top 5 user journeys | Explicit scenario list | Too slow/expensive to go broader |
| Performance | Key endpoints | Latency + RPS at SLO | Catch regressions before prod |

### Tooling Selection

```yaml
# test-strategy.yaml — tooling decisions with rationale
tech_stack: python-fastapi-postgres

unit_testing:
  framework: pytest
  runner: pytest-xdist       # Parallel execution
  coverage: coverage.py + pytest-cov
  mocking: unittest.mock + pytest-mock
  factories: factory_boy     # Test data generation
  assertions: built-in + pytest-approx

integration_testing:
  framework: pytest
  database: pytest-postgresql + testcontainers
  http_client: httpx + respx  # Real HTTP calls + mock external APIs
  fixtures: conftest.py with session-scoped DB
  test_data: Alembic migrations + seed scripts

contract_testing:
  framework: pact-python
  broker: PactFlow (managed) or self-hosted Pact Broker
  provider_verification: pytest-pact
  
e2e_testing:
  framework: playwright-python
  environments: [staging]
  parallelism: 4 workers
  visual_regression: playwright-screenshot-compare

performance_testing:
  framework: k6
  ci_schedule: nightly on staging
  baselines: tracked in k6 cloud
  
code_quality:
  linting: ruff (replaces flake8 + isort + pylint)
  type_checking: mypy --strict
  security: bandit + safety
  formatting: black
```

### Project Structure

```
tests/
├── unit/                    # Pure logic, no I/O
│   ├── test_pricing.py
│   ├── test_validators.py
│   └── test_order_logic.py
├── integration/             # Real DB, real cache, mock external
│   ├── conftest.py          # Fixtures: DB, app client
│   ├── test_orders_api.py
│   ├── test_user_repo.py
│   └── test_payment_flow.py
├── contract/                # Pact consumer/provider tests
│   ├── consumer/
│   └── provider/
├── e2e/                     # Full user journeys in staging
│   ├── test_checkout_flow.py
│   └── test_search_flow.py
├── performance/             # k6 scripts
│   └── load_test.js
├── conftest.py              # Root fixtures
└── pytest.ini
```

### pytest Configuration

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts =
    --strict-markers
    --strict-config
    -v
    --tb=short
    --cov=src
    --cov-report=term-missing
    --cov-report=html:coverage-report
    --cov-fail-under=80

markers =
    unit: Pure unit tests (no I/O)
    integration: Tests requiring database or external services
    e2e: End-to-end tests requiring full environment
    slow: Tests taking >1 second
    contract: Pact contract tests
```

### Test Fixtures (conftest.py)

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from testcontainers.postgres import PostgresContainer
from factory import Factory, Faker, SubFactory

from src.app import create_app
from src.database import Base, get_db
from src.models import User, Order

# ── Database ───────────────────────────────────────────────

@pytest.fixture(scope="session")
def postgres_container():
    """Single PostgreSQL container for the entire test session."""
    with PostgresContainer("postgres:15") as pg:
        yield pg

@pytest.fixture(scope="session")
def db_engine(postgres_container):
    engine = create_async_engine(postgres_container.get_connection_url())
    yield engine
    engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    """Each test gets a clean transaction that's rolled back after."""
    async with db_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async with conn.begin_nested() as savepoint:
            session = AsyncSession(bind=conn)
            yield session
            await session.close()
        await savepoint.rollback()  # Clean state after each test

# ── App Client ────────────────────────────────────────────

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """HTTP test client with injected test DB session."""
    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# ── Factories ─────────────────────────────────────────────

class UserFactory(Factory):
    class Meta:
        model = User
    
    id = Faker("uuid4")
    email = Faker("email")
    name = Faker("name")
    is_active = True
    created_at = Faker("date_time_this_year")

class OrderFactory(Factory):
    class Meta:
        model = Order
    
    id = Faker("uuid4")
    user = SubFactory(UserFactory)
    status = "pending"
    total_cents = Faker("random_int", min=100, max=100000)

# ── Auth Helpers ──────────────────────────────────────────

@pytest.fixture
def auth_headers(user_factory):
    """Generate valid auth headers for test user."""
    user = UserFactory.create()
    token = generate_test_token(user.id)
    return {"Authorization": f"Bearer {token}"}
```

### Example Test Patterns

```python
# tests/unit/test_order_logic.py — pure unit tests
import pytest
from decimal import Decimal
from src.domain.order import calculate_order_total, apply_discount

class TestCalculateOrderTotal:
    def test_sums_items(self):
        items = [
            {"price_cents": 1000, "quantity": 2},
            {"price_cents": 500, "quantity": 1},
        ]
        assert calculate_order_total(items) == 2500
    
    def test_empty_order_is_zero(self):
        assert calculate_order_total([]) == 0
    
    def test_rejects_negative_quantity(self):
        with pytest.raises(ValueError, match="quantity must be positive"):
            calculate_order_total([{"price_cents": 100, "quantity": -1}])
    
    @pytest.mark.parametrize("discount_pct,expected", [
        (10, 900),
        (50, 500),
        (100, 0),
        (0, 1000),
    ])
    def test_discount_calculation(self, discount_pct, expected):
        assert apply_discount(1000, discount_pct) == expected


# tests/integration/test_orders_api.py — integration tests
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
@pytest.mark.integration
class TestOrdersAPI:
    async def test_create_order_returns_201(self, client, auth_headers, db_session):
        response = await client.post(
            "/api/v1/orders",
            json={
                "items": [{"product_id": "prod-123", "quantity": 2}]
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert "order_id" in data
        assert data["status"] == "pending"
    
    async def test_create_order_persisted_to_db(self, client, auth_headers, db_session):
        response = await client.post(
            "/api/v1/orders",
            json={"items": [{"product_id": "prod-123", "quantity": 1}]},
            headers=auth_headers
        )
        order_id = response.json()["order_id"]
        
        # Verify in database
        order = await db_session.get(Order, order_id)
        assert order is not None
        assert order.status == "pending"
    
    async def test_unauthenticated_returns_401(self, client):
        response = await client.post("/api/v1/orders", json={})
        assert response.status_code == 401
    
    async def test_invalid_items_returns_422(self, client, auth_headers):
        response = await client.post(
            "/api/v1/orders",
            json={"items": []},  # Empty items
            headers=auth_headers
        )
        assert response.status_code == 422
        assert "items" in response.json()["detail"][0]["loc"]
```

### CI Quality Gates

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  unit:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run unit tests
        run: pytest tests/unit/ -m "not integration" --cov-fail-under=80
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  integration:
    name: Integration Tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v4
      - name: Run integration tests
        run: pytest tests/integration/ -m integration
        env:
          DATABASE_URL: postgresql://postgres:test@localhost/test

  quality-gates:
    name: Quality Gates
    runs-on: ubuntu-latest
    needs: [unit, integration]
    steps:
      - name: Check coverage threshold
        run: |
          COVERAGE=$(cat coverage.json | jq '.totals.percent_covered')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi
      
      - name: Check no test files were deleted
        run: |
          git diff origin/main...HEAD --name-only \
            | grep "^tests/" \
            | xargs -I {} git log -1 --diff-filter=D {} \
            | grep -v '^$' && echo "Test files deleted!" && exit 1 || true
```

### Flakiness Policy

```markdown
# Flaky Test Policy

## Definition
A test is **flaky** if it fails intermittently without code changes.

## Detection
- Any test that fails and passes on re-run without code changes is flagged
- CI tracks failure-to-pass ratio: >2% = flagged as flaky

## SLAs
| Category | Action Required |
|----------|----------------|
| P0: Blocking CI | Fix within 24h or quarantine |
| P1: Fails >10% | Fix within 1 week |
| P2: Fails 2-10% | Fix within 2 weeks |
| Investigate: Fails <2% | Log and monitor |

## Quarantine Process
1. Add `@pytest.mark.flaky(reruns=3)` with a GitHub issue link
2. Add to weekly flaky test review meeting
3. Fix or delete within the SLA

## Never Acceptable
- Deleting a failing test without understanding why it fails
- Increasing retry count without addressing root cause
- Using `time.sleep()` to fix timing issues (use explicit waits)
```

## Rules

- **Test pyramid, not test trophy** — most tests should be unit tests; E2E is expensive, keep it minimal.
- **One test framework per layer** — don't mix pytest and unittest; pick one and standardize.
- **Tests must run in any order** — no implicit state between tests; use fixtures with teardown.
- **Fast tests run first** — order CI jobs: unit → integration → E2E. Don't run E2E on every PR.
- **Coverage is a proxy, not a goal** — 80% coverage with weak assertions is worse than 60% with strong ones.
- **Delete tests that don't fail for 6 months** — dead test code is maintenance burden.
- **Test the behavior, not the implementation** — test what, not how. Refactoring shouldn't break tests.
- **Every bug gets a regression test** — before fixing a bug, write a test that reproduces it.
- **No production data in tests** — use factories and synthetic data; never clone prod to test.
- **Quarantine, don't disable** — a disabled test is a lie about test coverage.
