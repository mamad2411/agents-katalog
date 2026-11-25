---
name: sqlalchemy-patterns
description: "When to activate: SQLAlchemy 2.0, ORM, async sessions, relationships, query optimization, migrations"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# SQLAlchemy 2.0 Patterns

## Model Definition
```python
from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    
    # Relationships
    posts: Mapped[list["Post"]] = relationship(back_populates="author", lazy="selectin")

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    author: Mapped["User"] = relationship(back_populates="posts")
```

## Async Session Usage
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@host/db",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Queries: use select() style (2.0 API)
async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_users_with_posts(session: AsyncSession) -> list[User]:
    from sqlalchemy.orm import selectinload
    result = await session.execute(
        select(User).options(selectinload(User.posts))
    )
    return list(result.scalars().all())
```

## Avoiding N+1 Queries
```python
from sqlalchemy.orm import selectinload, joinedload

# For 1:N relationships: selectinload (2 queries, better for collections)
stmt = select(User).options(selectinload(User.posts))

# For N:1 relationships: joinedload (1 query with JOIN, better for single objects)
stmt = select(Post).options(joinedload(Post.author))

# For deep nesting
stmt = select(User).options(
    selectinload(User.posts).selectinload(Post.comments)
)
```

## Repository Pattern
```python
class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def get_by_id(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)
    
    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self._session.add(user)
        await self._session.flush()  # get id without committing
        return user
    
    async def list_paginated(self, offset: int = 0, limit: int = 20) -> list[User]:
        result = await self._session.execute(
            select(User).offset(offset).limit(limit).order_by(User.created_at.desc())
        )
        return list(result.scalars().all())
```

## Anti-Patterns
- Using `Session.query()` (legacy 1.x API) — use `select()` instead
- `expire_on_commit=True` (default) with async sessions — objects expire after commit but can't be lazily loaded
- Loading relationships in a loop (N+1) — use `selectinload` or `joinedload`
- Missing `.limit()` on list endpoints
- Catching `Exception` to rollback — let the session context manager handle it
