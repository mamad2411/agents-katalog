# Backend Database Skill

**Purpose**: Guidance for database operations using SQLModel with Neon PostgreSQL, including models, queries, migrations, and indexes.

## Overview

Database operations MUST use SQLModel ORM, Neon Serverless PostgreSQL, connection pooling, proper session management, and user isolation at database level.

## Key Patterns

### 1. SQLModel Model Definition

**File Location**: `/backend/models.py`

**Pattern**: Define models using SQLModel with proper types and constraints

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    name: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: str = Field(default="medium")  # 'low'|'medium'|'high'
    due_date: Optional[datetime] = Field(default=None, index=True)
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
```

**Pattern Rules**:
- Use `SQLModel, table=True` for database tables
- Use `Field()` for column definitions with constraints
- Use `primary_key=True` for primary keys
- Use `index=True` for indexed columns (user_id, completed, priority, due_date, email)
- Use `foreign_key` for relationships
- Use `default_factory` for auto-generated values
- Use `Optional[]` for nullable fields
- Use `max_length` for string length constraints
- Use `JSON` column type for arrays (tags)

### 2. Database Connection and Session Management

**File Location**: `/backend/db.py`

**Pattern**: Create database engine with connection pooling and session dependency

```python
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Number of connections to maintain
    max_overflow=20,  # Additional connections beyond pool_size
    echo=False  # Set to True for SQL query logging in development
)

def get_db() -> Session:
    """Dependency for FastAPI to get database session"""
    with Session(engine) as session:
        yield session

@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

**Pattern Rules**:
- Use `create_engine()` with connection pooling
- Set `pool_pre_ping=True` for connection health checks
- Configure `pool_size` and `max_overflow` for concurrency
- Use `get_db()` as FastAPI dependency (yields session)
- Use context manager for manual session management
- Always commit on success, rollback on error

### 3. Database Migrations with Alembic

**Pattern**: Use Alembic for database schema versioning

```bash
# Initialize Alembic (one time)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Create users and tasks tables"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

**Alembic Configuration** (`alembic/env.py`):

```python
from sqlmodel import SQLModel
from backend.models import User, Task  # Import all models
from backend.db import engine

# Set target metadata
target_metadata = SQLModel.metadata

def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()
```

**Pattern Rules**:
- Use Alembic for all schema changes
- Import all models in Alembic config
- Use `--autogenerate` for automatic migration generation
- Review generated migrations before applying
- Never edit existing migrations, create new ones

### 4. Database Indexes

**Pattern**: Create indexes for performance optimization

```python
# In Alembic migration file
def upgrade():
    # Create indexes
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_completed', 'tasks', ['completed'])
    op.create_index('ix_tasks_priority', 'tasks', ['priority'])
    op.create_index('ix_tasks_due_date', 'tasks', ['due_date'])
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

def downgrade():
    # Drop indexes
    op.drop_index('ix_tasks_user_id', 'tasks')
    op.drop_index('ix_tasks_completed', 'tasks')
    op.drop_index('ix_tasks_priority', 'tasks')
    op.drop_index('ix_tasks_due_date', 'tasks')
    op.drop_index('ix_users_email', 'users')
```

**Required Indexes**:
- `tasks.user_id` - For filtering by user (user isolation)
- `tasks.completed` - For status filtering
- `tasks.priority` - For priority filtering
- `tasks.due_date` - For due date filtering and sorting
- `users.email` - Unique index for email lookup

**Pattern Rules**:
- Create indexes in Alembic migrations
- Index foreign keys (user_id)
- Index frequently filtered columns (completed, priority, due_date)
- Index unique columns (email)
- Test query performance with indexes

### 5. User Isolation in Queries

**Pattern**: Always filter queries by user_id for user isolation

```python
from sqlmodel import Session, select
from backend.models import Task

def get_user_tasks(db: Session, user_id: str):
    """Get all tasks for a specific user"""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = db.exec(statement).all()
    return tasks

def get_task_by_id(db: Session, user_id: str, task_id: int):
    """Get a specific task with user isolation"""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # CRITICAL: Always filter by user_id
    )
    task = db.exec(statement).first()
    return task

def update_task(db: Session, user_id: str, task_id: int, task_data: dict):
    """Update task with user isolation"""
    # First verify task belongs to user
    task = get_task_by_id(db, user_id, task_id)
    if not task:
        raise ValueError("Task not found")
    
    # Update task
    for key, value in task_data.items():
        setattr(task, key, value)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
```

**Pattern Rules**:
- ALWAYS filter by `user_id` in WHERE clause
- Verify task ownership before update/delete
- Use `select()` with `.where()` for queries
- Use `.first()` for single result, `.all()` for multiple
- Never trust user_id from request, always use from JWT token

### 6. CRUD Operations

**Pattern**: Standard CRUD operations with user isolation

```python
from sqlmodel import Session, select
from backend.models import Task

# CREATE
def create_task(db: Session, user_id: str, task_data: dict) -> Task:
    """Create a new task"""
    task = Task(
        user_id=user_id,  # Always set from authenticated user
        **task_data
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# READ (Single)
def get_task(db: Session, user_id: str, task_id: int) -> Optional[Task]:
    """Get a single task with user isolation"""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    return db.exec(statement).first()

# READ (Multiple)
def get_tasks(db: Session, user_id: str, filters: dict = None) -> List[Task]:
    """Get multiple tasks with user isolation and filters"""
    statement = select(Task).where(Task.user_id == user_id)
    
    # Apply filters
    if filters:
        if filters.get("completed") is not None:
            statement = statement.where(Task.completed == filters["completed"])
        if filters.get("priority"):
            statement = statement.where(Task.priority == filters["priority"])
        # Add more filters as needed
    
    return db.exec(statement).all()

# UPDATE
def update_task(db: Session, user_id: str, task_id: int, task_data: dict) -> Task:
    """Update a task with user isolation"""
    task = get_task(db, user_id, task_id)
    if not task:
        raise ValueError("Task not found")
    
    # Update fields
    for key, value in task_data.items():
        if value is not None:  # Only update provided fields
            setattr(task, key, value)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# DELETE
def delete_task(db: Session, user_id: str, task_id: int) -> bool:
    """Delete a task with user isolation"""
    task = get_task(db, user_id, task_id)
    if not task:
        return False
    
    db.delete(task)
    db.commit()
    return True
```

**Pattern Rules**:
- Always include `user_id` in queries
- Use `db.add()` for new records
- Use `db.commit()` to persist changes
- Use `db.refresh()` to reload from database
- Use `db.delete()` for deletion
- Handle None results appropriately

### 7. Query Filtering and Sorting

**Pattern**: Build dynamic queries with filters and sorting

```python
from sqlmodel import Session, select, or_
from backend.models import Task
from typing import Optional, List

def get_tasks_with_filters(
    db: Session,
    user_id: str,
    status: Optional[str] = None,  # 'all'|'pending'|'completed'
    priority: Optional[str] = None,
    due_date: Optional[datetime] = None,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,  # 'created'|'title'|'updated'|'priority'|'due_date'
    page: int = 1,
    limit: int = 20
) -> tuple[List[Task], int]:  # Returns (tasks, total_count)
    
    # Base query with user isolation
    statement = select(Task).where(Task.user_id == user_id)
    
    # Apply status filter
    if status == "pending":
        statement = statement.where(Task.completed == False)
    elif status == "completed":
        statement = statement.where(Task.completed == True)
    # 'all' means no filter
    
    # Apply priority filter
    if priority:
        statement = statement.where(Task.priority == priority)
    
    # Apply due_date filter
    if due_date:
        statement = statement.where(Task.due_date == due_date)
    
    # Apply tags filter (JSON array contains)
    if tags:
        # PostgreSQL JSONB contains operator
        for tag in tags:
            statement = statement.where(Task.tags.contains([tag]))
    
    # Apply search filter (full-text search on title and description)
    if search:
        search_term = f"%{search}%"
        statement = statement.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )
    
    # Get total count before pagination
    count_statement = select(func.count()).select_from(statement.subquery())
    total_count = db.exec(count_statement).one()
    
    # Apply sorting
    if sort == "created":
        statement = statement.order_by(Task.created_at.desc())
    elif sort == "title":
        statement = statement.order_by(Task.title.asc())
    elif sort == "updated":
        statement = statement.order_by(Task.updated_at.desc())
    elif sort == "priority":
        # Custom priority ordering: high > medium > low
        from sqlalchemy import case
        priority_order = case(
            (Task.priority == "high", 1),
            (Task.priority == "medium", 2),
            (Task.priority == "low", 3)
        )
        statement = statement.order_by(priority_order)
    elif sort == "due_date":
        statement = statement.order_by(Task.due_date.asc().nulls_last())
    else:
        # Default: created_at desc
        statement = statement.order_by(Task.created_at.desc())
    
    # Apply pagination
    offset = (page - 1) * limit
    statement = statement.offset(offset).limit(limit)
    
    # Execute query
    tasks = db.exec(statement).all()
    
    return tasks, total_count
```

**Pattern Rules**:
- Always start with user_id filter
- Build query dynamically based on filters
- Use `or_()` for OR conditions
- Use `ilike()` for case-insensitive search
- Use `contains()` for JSON array filtering
- Apply sorting before pagination
- Get total count before applying limit
- Use `offset()` and `limit()` for pagination

### 8. Full-Text Search

**Pattern**: Implement full-text search using PostgreSQL features

```python
from sqlmodel import Session, select, func
from sqlalchemy import text

def search_tasks(db: Session, user_id: str, search_term: str) -> List[Task]:
    """Full-text search on title and description"""
    # PostgreSQL full-text search
    statement = select(Task).where(
        Task.user_id == user_id,
        or_(
            func.to_tsvector('english', Task.title).match(search_term),
            func.to_tsvector('english', Task.description).match(search_term)
        )
    ).order_by(
        func.ts_rank_cd(
            func.to_tsvector('english', Task.title),
            func.plainto_tsquery('english', search_term)
        ).desc()
    )
    
    return db.exec(statement).all()
```

**Pattern Rules**:
- Use PostgreSQL `to_tsvector()` and `match()` for full-text search
- Use `ts_rank_cd()` for relevance ranking
- Filter by user_id first
- Order by relevance score

### 9. Transaction Management

**Pattern**: Use transactions for atomic operations

```python
from sqlmodel import Session

def bulk_update_tasks(db: Session, user_id: str, task_ids: List[int], updates: dict):
    """Bulk update with transaction"""
    try:
        # Get all tasks for user
        tasks = db.exec(
            select(Task).where(
                Task.id.in_(task_ids),
                Task.user_id == user_id
            )
        ).all()
        
        if len(tasks) != len(task_ids):
            raise ValueError("Some tasks not found or don't belong to user")
        
        # Update all tasks
        for task in tasks:
            for key, value in updates.items():
                setattr(task, key, value)
            db.add(task)
        
        # Commit all changes atomically
        db.commit()
        return len(tasks)
    
    except Exception as e:
        db.rollback()
        raise
```

**Pattern Rules**:
- Use `db.commit()` to persist all changes
- Use `db.rollback()` on errors
- Wrap related operations in try/except
- Verify user ownership before bulk operations

### 10. Database Connection Error Handling

**Pattern**: Handle database connection errors gracefully

```python
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status

def safe_db_operation(db: Session, operation):
    """Wrapper for database operations with error handling"""
    try:
        result = operation(db)
        db.commit()
        return result
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database constraint violation: {str(e)}"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred"
        )
```

**Pattern Rules**:
- Catch `IntegrityError` for constraint violations (400)
- Catch `SQLAlchemyError` for database errors (500)
- Always rollback on errors
- Log errors for debugging
- Return user-friendly error messages

## Steps for Adding New Database Model

1. **Define Model** (in `/backend/models.py`)
   - Inherit from `SQLModel, table=True`
   - Define all fields with proper types
   - Add indexes for frequently queried fields
   - Add foreign keys for relationships

2. **Create Migration** (using Alembic)
   - Run `alembic revision --autogenerate -m "Add new model"`
   - Review generated migration
   - Add indexes if needed
   - Apply migration: `alembic upgrade head`

3. **Add Service Methods** (in `/backend/services/`)
   - Add CRUD methods with user isolation
   - Add query methods with filters
   - Add validation logic

4. **Add Tests** (in `/backend/tests/`)
   - Test model creation
   - Test queries with user isolation
   - Test constraints and validations

## Common Patterns Summary

- ✅ Use SQLModel for all database models
- ✅ Always filter by user_id for user isolation
- ✅ Use connection pooling for performance
- ✅ Use Alembic for schema migrations
- ✅ Create indexes for frequently queried columns
- ✅ Use transactions for atomic operations
- ✅ Handle database errors gracefully
- ✅ Use type hints throughout
- ✅ Commit changes explicitly
- ✅ Rollback on errors

