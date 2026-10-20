---
name: fastapi-patterns
description: |
  FastAPI production patterns with SQLAlchemy 2.0 async. Apply for any FastAPI project,
  endpoint, dependency, or middleware. Covers async patterns, Pydantic v2 schemas,
  dependency injection, background tasks, lifespan events, and OpenAPI customization.
---

# FastAPI Production Patterns

## App Structure
```
app/
├── main.py              # FastAPI app, lifespan, middleware
├── config.py            # Pydantic settings
├── database.py          # AsyncEngine, session factory
├── dependencies.py      # Shared dependencies (auth, db session)
├── routers/
│   ├── users.py
│   └── orders.py
├── models/              # SQLAlchemy ORM models
├── schemas/             # Pydantic request/response schemas
├── services/            # Business logic
├── repositories/        # DB query layer
└── core/
    ├── security.py      # JWT, password hashing
    ├── exceptions.py    # Custom exception classes
    └── middleware.py    # Request ID, logging
```

## App Lifespan & Middleware
```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    await redis.ping()
    yield
    # Shutdown
    await database.disconnect()
    await redis.close()

app = FastAPI(
    title="MyWeb API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url=None,
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

## Async Database Session
```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    echo=settings.DEBUG,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# dependencies.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

## Pydantic v2 Schemas
```python
# schemas/order.py
from pydantic import BaseModel, Field, model_validator
from decimal import Decimal

class OrderItemCreate(BaseModel):
    product_id: str = Field(min_length=1)
    quantity: int = Field(ge=1, le=100)

class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1, max_length=50)
    delivery_address: str = Field(min_length=10, max_length=500)
    note: str | None = Field(None, max_length=1000)

    @model_validator(mode='after')
    def check_unique_products(self) -> 'OrderCreate':
        product_ids = [item.product_id for item in self.items]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Duplicate products are not allowed")
        return self

class OrderResponse(BaseModel):
    id: str
    status: str
    total: Decimal
    items: list[OrderItemResponse]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

## Dependency Injection
```python
# dependencies.py
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_repo.get_by_id(db, user_id)
    if not user or user.deleted_at:
        raise credentials_exception
    return user

# Usage in router
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```
