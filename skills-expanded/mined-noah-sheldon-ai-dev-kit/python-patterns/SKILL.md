---
name: python-patterns
description: Python data and backend patterns including Pandas, NumPy, SQLAlchemy 2.0, Alembic, data validation, performance optimization, and OOP composition.
origin: AI Dev Kit
---

# Python Patterns

Production-grade Python patterns for data engineering (Pandas, NumPy), database access
(SQLAlchemy 2.0, Alembic), data validation (Pydantic, Great Expectations), performance
optimization, and OOP composition in service/repository layers.

## When to Use

- Writing data pipelines with Pandas or NumPy — ETL, transformations, aggregations.
- Building SQLAlchemy 2.0 models with async engines and proper session management.
- Managing database migrations with Alembic (schema + data migrations).
- Validating data at boundaries with Pydantic models or Great Expectations suites.
- Optimizing Python data processing — vectorization, chunking, memory management.
- Designing service and repository layers with OOP composition patterns.
- Building data-heavy backends that serve ML/AI pipelines.

## Core Concepts

### 1. Pandas — DataFrame Operations

**Core Operations:**

```python
import pandas as pd
import numpy as np
from datetime import datetime

# --- Creation ---
df = pd.DataFrame({
    "user_id": [1, 2, 3, 4],
    "email": ["a @x.com", "b @x.com", "c @y.com", "d @y.com"],
    "signup_date": pd.to_datetime(["2024-01-15", "2024-03-20", "2024-06-01", "2024-09-10"]),
    "revenue": [49.99, 0.0, 99.99, 49.99],
    "plan": ["pro", "free", "enterprise", "pro"],
})

# --- Filtering ---
pro_users = df[df["plan"] == "pro"]
recent_revenue = df.loc[
    (df["signup_date"] >= "2024-06-01") & (df["revenue"] > 0),
    ["user_id", "email", "revenue"],
]

# --- Groupby + Aggregation ---
revenue_by_plan = (
    df.groupby("plan")
    .agg(
        total_revenue=("revenue", "sum"),
        avg_revenue=("revenue", "mean"),
        user_count=("user_id", "count"),
    )
    .reset_index()
)

# --- Merge (SQL-style joins) ---
orders = pd.DataFrame({
    "order_id": [101, 102, 103],
    "user_id": [1, 1, 3],
    "amount": [29.99, 19.99, 149.99],
    "order_date": pd.to_datetime(["2024-07-01", "2024-08-15", "2024-09-01"]),
})

merged = df.merge(orders, on="user_id", how="inner")
# left, right, outer, cross also supported

# --- Pivot Table ---
pivot = df.pivot_table(
    index="plan",
    columns=df["signup_date"].dt.quarter,
    values="revenue",
    aggfunc="sum",
    fill_value=0,
)

# --- Time Series ---
df["month"] = df["signup_date"].dt.to_period("M")
monthly = df.groupby("month")["revenue"].sum()

# Resample to weekly frequency (requires DatetimeIndex)
daily = df.set_index("signup_date").resample("D")["revenue"].sum()
```

**Vectorization — Always prefer over `.apply()`:**

```python
# BAD — row-wise Python loop
df["discount"] = df["revenue"].apply(lambda x: x * 0.1 if x > 50 else 0)

# GOOD — vectorized with np.where
df["discount"] = np.where(df["revenue"] > 50, df["revenue"] * 0.1, 0.0)

# GOOD — vectorized with boolean indexing
df.loc[df["revenue"] > 50, "discount"] = df["revenue"] * 0.1

# BAD — string operations with apply
df["domain"] = df["email"].apply(lambda e: e.split("@")[1])

# GOOD — vectorized string accessor
df["domain"] = df["email"].str.split("@").str[1]
```

**Chunking for Large Datasets:**

```python
def process_large_csv(path: str, chunk_size: int = 100_000) -> pd.DataFrame:
    """Process a CSV that doesn't fit in memory by chunking."""
    results = []
    for chunk in pd.read_csv(path, chunksize=chunk_size):
        # Vectorized transformations per chunk
        chunk["signup_date"] = pd.to_datetime(chunk["signup_date"])
        chunk = chunk[chunk["revenue"] > 0]
        chunk["revenue_usd"] = chunk["revenue"] * 1.0  # currency conversion
        results.append(chunk.groupby("plan")["revenue_usd"].sum())
    return pd.concat(results).groupby(level=0).sum()
```

### 2. NumPy — Array Operations

```python
import numpy as np

# --- Array Creation ---
zeros = np.zeros((3, 4), dtype=np.float32)
ones = np.ones((2, 3), dtype=np.int32)
identity = np.eye(4)
arange = np.arange(0, 10, 0.5)
linspace = np.linspace(0, 1, 100)
random_normal = np.random.normal(loc=0, scale=1, size=(100, 10))
random_int = np.random.randint(0, 100, size=(50,))

# --- Broadcasting ---
a = np.array([[1, 2, 3], [4, 5, 6]])  # shape (2, 3)
b = np.array([10, 20, 30])             # shape (3,)
result = a + b  # broadcasts to (2, 3) → [[11, 22, 33], [14, 25, 36]]

# --- Linear Algebra ---
A = np.array([[1, 2], [3, 4]], dtype=np.float64)
B = np.array([[5, 6], [7, 8]], dtype=np.float64)

dot = A @ B                    # matrix multiplication
eigenvalues, eigenvectors = np.linalg.eig(A)
inverse = np.linalg.inv(A)
determinant = np.linalg.det(A)
svd_u, svd_s, svd_vt = np.linalg.svd(A)
solution = np.linalg.solve(A, np.array([5, 11]))  # Ax = b

# --- Random Generation ---
rng = np.random.default_rng(seed=42)  # reproducible
samples = rng.standard_normal(1000)
choice = rng.choice(["a", "b", "c"], size=100, p=[0.5, 0.3, 0.2])
shuffle = rng.permutation(np.arange(10))

# --- Conditional Operations ---
arr = np.array([1, 2, 3, 4, 5])
clipped = np.clip(arr, 2, 4)  # [2, 2, 3, 4, 4]
masked = np.where(arr > 3, arr * 10, arr)  # [1, 2, 3, 40, 50]
```

### 3. SQLAlchemy 2.0 — ORM and Core

**Core vs ORM — When to Use Each:**

| Use Case | Approach | Why |
|----------|----------|-----|
| Simple CRUD on entities | ORM (`Mapped`, `relationship`) | Declarative models, type safety |
| Bulk inserts / upserts | Core (`insert`, `update`) | Faster, no ORM overhead |
| Complex analytical queries | Core (`select`, `text`) | Fine-grained SQL control |
| Migrations | Alembic (autogenerate) | Schema versioning |

**ORM Pattern (SQLAlchemy 2.0 Style):**

```python
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    select,
    update,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    orders: Mapped[list[Order]] = relationship(back_populates="user", lazy="selectin")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    order_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped[User] = relationship(back_populates="orders")
```

**Async Engine + Session Management:**

```python
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

# Engine creation (do this once at app startup)
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/dbname",
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Session factory
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Usage in repository
class SQLAlchemyUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def list_all(self, skip: int = 0, limit: int = 50) -> list[User]:
        result = await self.session.execute(
            select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
```

**Core Pattern (Bulk Operations):**

```python
from sqlalchemy import insert, update, delete

async def bulk_insert_users(users_data: list[dict]) -> None:
    """Use Core for bulk operations — no ORM overhead."""
    async with async_session() as session:
        stmt = insert(User).values(users_data)
        await session.execute(stmt)
        await session.commit()


async def bulk_deactivate_inactive(user_ids: list[UUID]) -> int:
    """Bulk update returns rowcount."""
    async with async_session() as session:
        stmt = (
            update(User)
            .where(User.id.in_(user_ids), User.is_active == True)
            .values(is_active=False)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount
```

### 4. Alembic — Migration Management

**Migration Generation:**

```bash
# Initialize Alembic (async template)
alembic init -t async alembic

# Configure alembic.ini
# sqlalchemy.url = postgresql+asyncpg://user:pass@localhost/dbname

# Configure env.py — set target_metadata
target_metadata = Base.metadata

# Autogenerate migration from model changes
alembic revision --autogenerate -m "add users and orders tables"

# Review the generated migration, then apply
alembic upgrade head

# Rollback
alembic downgrade -1

# Check for uncommitted migrations
alembic check
```

**Data Migration (Custom Revision):**

```python
"""Seed default admin user.

Revision ID: abc123
Revises: def456
Create Date: 2024-01-15
"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4

revision = "abc123"
down_revision = "def456"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Insert seed data using Core — no ORM in migrations."""
    users_table = sa.table(
        "users",
        sa.column("id", sa.String),
        sa.column("email", sa.String),
        sa.column("name", sa.String),
        sa.column("is_active", sa.Boolean),
    )
    op.bulk_insert(
        users_table,
        [
            {
                "id": str(uuid4()),
                "email": "admin @example.com",
                "name": "Admin",
                "is_active": True,
            },
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE email = 'admin @example.com'")
```

**Revision Chain Best Practices:**
- Never edit an already-applied migration — create a new one.
- Use `down_revision` to maintain linear history; use `branch_labels` only for parallel feature development.
- Always write `downgrade()` — it's required for safe rollback.
- Test migrations against a copy of production schema before deploying.

### 5. Data Validation

**Pydantic Models for Data Ingestion:**

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


class UserInput(BaseModel):
    email: str = Field(..., max_length=255)
    name: str = Field(..., min_length=1, max_length=150)
    age: Optional[int] = Field(None, ge=0, le=150)

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        import re
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v.lower()


def validate_csv_row(row: dict) -> UserInput:
    """Validate a single row from CSV/dataframe ingestion."""
    return UserInput(**row)
```

**Great Expectations Integration:**

```python
import great_expectations as gx
from great_expectations.core import ExpectationSuite

# Create context and suite
context = gx.get_context()
suite = context.suites.add(ExpectationSuite(name="user_data_quality"))

# Define expectations
suite.add_expectations(
    gx.expectations.ExpectColumnToExist(column="email"),
    gx.expectations.ExpectColumnValuesToNotBeNull(column="email"),
    gx.expectations.ExpectColumnValuesToMatchRegex(
        column="email", regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    ),
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="age", min_value=0, max_value=150, mostly=0.95
    ),
    gx.expectations.ExpectColumnUniqueValueCountToBeBetween(
        column="email", min_value=1, max_value=None
    ),
)

# Validate a Pandas DataFrame
validator = context.get_validator(
    batch_request=gx.datasource.pandas_datasource(
        name="user_data",
        dataframes={"ingestion": df},
    ),
    suite_name="user_data_quality",
)
results = validator.validate()

if not results["success"]:
    failed = [r["expectation_config"]["kwargs"] for r in results["results"] if not r["success"]]
    raise DataQualityError(f"Validation failed: {failed}")
```

### 6. Performance Optimization

**Vectorization vs Apply:**

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({"a": range(1_000_000), "b": range(1_000_000)})

# Timing comparison (approximate):
# .apply(lambda r: r["a"] + r["b"], axis=1)  → ~200ms
# df["a"] + df["b"]                          → ~2ms   (100x faster)
# np.add(df["a"], df["b"])                   → ~1ms   (200x faster)

# String operations:
# .apply(lambda s: s.upper())     → ~50ms per 100k rows
# .str.upper()                    → ~5ms per 100k rows  (10x faster)

# Conditional:
# .apply(lambda x: "high" if x > 50 else "low")  → slow
# np.where(df["a"] > 50, "high", "low")           → fast
```

**Memory Optimization:**

```python
# Downcast numeric types
def optimize_numeric_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Reduce memory by downcasting numeric columns."""
    for col in df.select_dtypes(include=["int64"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="integer")
    for col in df.select_dtypes(include=["float64"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="float")
    return df


# Use categorical for low-cardinality strings
def optimize_string_columns(
    df: pd.DataFrame, threshold: float = 0.5
) -> pd.DataFrame:
    """Convert string columns with low cardinality to category dtype."""
    for col in df.select_dtypes(include=["object"]).columns:
        cardinality = df[col].nunique() / len(df)
        if cardinality < threshold:
            df[col] = df[col].astype("category")
    return df


# Process in chunks for out-of-core computation
def aggregate_large_file(path: str) -> pd.DataFrame:
    chunks = []
    for chunk in pd.read_csv(path, chunksize=500_000, dtype_backend="pyarrow"):
        summary = chunk.groupby("category")["value"].agg(["sum", "mean", "count"])
        chunks.append(summary)
    return pd.concat(chunks).groupby(level=0).agg({"sum": "sum", "mean": "mean", "count": "sum"})
```

**NumPy Memory Views (Avoid Copies):**

```python
arr = np.arange(1_000_000)

# View (no copy) — modifications affect original
view = arr[100:200]
view[:] = 0  # modifies arr[100:200]

# Copy (explicit) — independent
copy = arr[100:200].copy()
copy[:] = 0  # does NOT modify arr

# In-place operations save memory
arr += 1       # in-place, no extra allocation
arr = arr + 1  # creates new array
```

### 7. OOP Composition in Services/Repositories

**Composition Over Inheritance:**

```python
from typing import Protocol, Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")


# --- Protocol-based interfaces (structural subtyping) ---
class ReadableRepository(Protocol[T]):
    async def get_by_id(self, id: str) -> T | None: ...
    async def list_all(self, skip: int = 0, limit: int = 50) -> list[T]: ...


class WritableRepository(Protocol[T]):
    async def create(self, entity: T) -> T: ...
    async def update(self, entity: T) -> T: ...
    async def delete(self, id: str) -> bool: ...


# --- Mixin for caching behavior ---
class CachingMixin:
    """Adds simple in-memory caching to any repository."""

    _cache: dict = {}

    async def get_by_id_cached(self, id: str, fetch_fn):
        if id not in self._cache:
            self._cache[id] = await fetch_fn(id)
        return self._cache[id]

    def invalidate_cache(self, id: str) -> None:
        self._cache.pop(id, None)


# --- Concrete repository composing multiple behaviors ---
class CachedUserRepository(CachingMixin):
    def __init__(self, base_repo: ReadableRepository[User] & WritableRepository[User]):
        self.base_repo = base_repo

    async def get_by_id(self, user_id: str) -> User | None:
        return await self.get_by_id_cached(
            user_id, lambda uid: self.base_repo.get_by_id(uid)
        )

    async def create(self, user: User) -> User:
        result = await self.base_repo.create(user)
        self.invalidate_cache(str(result.id))
        return result


# --- Service composition with dependency injection ---
class UserService:
    def __init__(
        self,
        user_repo: ReadableRepository[User] & WritableRepository[User],
        cache: CachingMixin | None = None,
        event_bus: EventBus | None = None,
    ) -> None:
        self.user_repo = user_repo
        self.cache = cache or CachedUserRepository(user_repo)
        self.event_bus = event_bus

    async def create_user(self, email: str, name: str) -> User:
        user = User(email=email, name=name)
        user = await self.user_repo.create(user)
        self.cache.invalidate_cache(str(user.id))
        if self.event_bus:
            await self.event_bus.publish(UserCreated(user_id=user.id))
        return user
```

## Anti-Patterns

- **Using `.apply()` on DataFrames** — always vectorize with numpy or pandas built-ins first.
- **Loading entire CSV into memory** — use `chunksize` or Dask/Polars for large files.
- **Mixing SQLAlchemy ORM and Core in the same query** — pick one approach per operation.
- **Calling `session.commit()` inside repository methods** — commit at the service or dependency level.
- **Not setting `expire_on_commit=False`** — causes DetachedInstanceError on attribute access after commit.
- **Using sync SQLAlchemy engine in async FastAPI** — blocks the event loop; use `+asyncpg` or `+aiosqlite`.
- **Editing committed Alembic migrations** — always create a new migration; never modify history.
- **Skipping `downgrade()` in migrations** — makes rollback impossible.
- **Validating data only at API boundary** — also validate at ingestion/ETL boundaries.
- **Using `int64`/`float64` for everything** — downcast to save 50-70% memory.
- **Inheritance-heavy repository hierarchies** — prefer composition and protocols.

## Best Practices

1. **Vectorize everything** — `np.where`, `.str`, `.dt` accessors beat `.apply()` by 10-200x.
2. **Use `dtype_backend="pyarrow"`** — faster parsing, lower memory for large datasets.
3. **Downcast numerics early** — `pd.to_numeric(..., downcast="integer")` saves memory.
4. **Category dtype for low-cardinality strings** — threshold <50% unique values.
5. **SQLAlchemy 2.0 `select()` style** — never use legacy `session.query()`.
6. **`expire_on_commit=False`** — prevents DetachedInstanceError in async contexts.
7. **`selectin` lazy loading** — avoids N+1 for relationships; use `joinedload` for single joins.
8. **Alembic autogenerate + manual review** — always review auto-generated migrations before applying.
9. **Data migrations use Core, not ORM** — migrations shouldn't depend on application models.
10. **Pydantic at every boundary** — API input, CSV ingestion, event payloads.
11. **Great Expectations for pipeline QA** — run before loading data into production tables.
12. **Composition over inheritance** — protocols + mixins > deep class hierarchies.
13. **Repository returns domain entities** — never leak ORM models to service layer.
14. **Test with in-memory SQLite or testcontainers** — isolate DB state per test.
15. **Profile before optimizing** — use `pandas-profiling`, `memory_profiler`, `line_profiler`.

## Related Skills

- `backend-patterns` — FastAPI architecture, dependency injection, error handling
- `python-testing` — Pytest, Hypothesis, Factory Boy, coverage
- `database-migrations` — Alembic deep-dive, migration strategies
- `postgres-patterns` — PostgreSQL-specific patterns, indexing, query optimization
- `data-pipelines-ai` — Airflow, Prefect, Kafka, data versioning for AI pipelines
- `security-review` — Input validation, SQL injection prevention, secret management
