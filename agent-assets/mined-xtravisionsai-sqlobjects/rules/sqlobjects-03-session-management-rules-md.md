# Session Management and Transaction Architecture

## Session Management Design Patterns

### Core Session Interfaces

#### `using()` Method Pattern
**Universal session binding interface across all operations**
```python
# Model operations
user = await User.objects.using(session).create(username="john")
await user.using(session).save()

# Query operations  
users = await User.objects.using(session).filter(User.is_active == True).all()

# Bulk operations
await User.objects.using(session).bulk_create(user_data)
```

#### ModelProxy Pattern
**Transparent session management for detached instances**
- Automatically attaches detached instances to appropriate sessions
- Handles session binding for save(), delete(), refresh() operations
- Maintains session context across method calls
- Provides seamless experience for detached instance operations

### Session Context Managers

#### Single Database Sessions
```python
# ctx_session() for single database operations
from sqlobjects.session import ctx_session

async with ctx_session() as session:
    user = await User.objects.using(session).create(username="alice")
    posts = await user.posts.using(session).all()
    # Automatic commit on success, rollback on exception
```

#### Multiple Database Sessions
```python
# ctx_sessions() for multi-database operations
from sqlobjects.session import ctx_sessions

async with ctx_sessions("main", "analytics") as sessions:
    user = await User.objects.using(sessions["main"]).create(username="bob")
    await Log.objects.using(sessions["analytics"]).create(message="User created")
    # Coordinated transaction across databases
```

### Session Acquisition with Read/Write Separation
**Session management supports readonly parameter for read/write separation**
```python
from sqlobjects.session import get_session

class ObjectsManager:
    def _get_session(self, readonly: bool = True) -> AsyncSession:
        """Get database session with explicit readonly parameter.
        
        Args:
            readonly: Whether the session is for read-only operations
        
        Returns:
            AsyncSession instance
        """
        if self._db_or_session is None:
            return get_session(readonly=readonly)
        elif isinstance(self._db_or_session, str):
            return get_session(self._db_or_session, readonly=readonly)
        else:
            return self._db_or_session

# Usage examples
session = self._get_session(readonly=False)  # Write operations
session = self._get_session(readonly=True)   # Read operations (default)

# In ObjectsManager methods
async def create(self, **kwargs):
    session = self._get_session(readonly=False)  # Write operation
    # ...

async def get(self, **kwargs):
    session = self._get_session(readonly=True)   # Read operation
    # ...
```

## Transaction Management Patterns

### Three Transaction Modes

#### 1. ContextVar Inheritance (Unified Transactions)
**Use Case**: All operations should be in the same transaction
```python
async with ctx_session() as session:
    # All async tasks inherit the same session context
    tasks = [asyncio.create_task(process_user(user_id)) for user_id in user_ids]
    await asyncio.gather(*tasks)
    # All operations committed together
```

#### 2. Independent Context (Fault Isolation)
**Use Case**: Operations should be isolated from each other
```python
# Each task gets independent transaction context
tasks = [
    asyncio.create_task(process_user(user_id), context=contextvars.copy_context())
    for user_id in user_ids
]
await asyncio.gather(*tasks, return_exceptions=True)
# Failures in one task don't affect others
```

#### 3. Explicit Session Passing (Full Control)
**Use Case**: Complex transaction logic with explicit control
```python
async with ctx_session() as session:
    tasks = [asyncio.create_task(process_user(user_id, session)) for user_id in user_ids]
    await asyncio.gather(*tasks)
    # Explicit session management with full control
```

## Database Connection Architecture

### DatabaseManager Design
**Singleton pattern for multi-database management**
- Centralized database registration and configuration
- Connection pool management and health monitoring
- Automatic failover and load balancing support
- Named database routing and default database handling

### SessionContextManager Implementation
**ContextVar-based session context management**
- ContextVar (`_explicit_sessions`) for context-level session storage
- Token-based nesting support for correct nested `ctx_session()` behavior
- Context manager lifecycle management
- Transaction boundary control and cleanup
- Error handling and rollback strategies

### Auto-Default Mechanism
**Automatic database failover system**
```python
# Graceful shutdown with automatic failover
await close_db("primary", auto_default=True)
# Automatically switches default to next available database

# Health-based failover
if not await check_db_health("primary"):
    await switch_default_db("backup")
```

## Design Decision Rationale

### Why using() Method Pattern?
**Alternative Considered**: Parameter passing (session=session)
**Decision**: using() method for consistency
**Rationale**:
- Consistent interface across all operation types
- Chainable with other query methods
- Clear indication of session binding
- Supports both bound and unbound operations

### Why ModelProxy vs Direct Session Binding?
**Alternative Considered**: Always require explicit session
**Decision**: ModelProxy for transparent session management
**Rationale**:
- Seamless experience for detached instances
- Reduces boilerplate for simple operations
- Maintains session context across operations
- Backward compatibility with session-less operations

### Why Three Transaction Modes?
**Alternative Considered**: Single transaction model
**Decision**: Multiple patterns for different use cases
**Rationale**:
- ContextVar inheritance for unified transactions
- Independent contexts for fault tolerance
- Explicit passing for complex scenarios
- Flexibility without complexity for simple cases

## Session Lifecycle Management

### Session Creation and Configuration
```python
# Sessions are created automatically via ctx_session() context manager
from sqlobjects.session import ctx_session

async with ctx_session() as session:
    # session is an AsyncSession instance (built on SQLAlchemy Core AsyncConnection)
    # auto_commit=False, readonly=False — manual transaction control
    user = await User.objects.using(session).create(username="alice")
    # Auto-commit on success, rollback on exception
```

### Transaction Boundaries
- **Automatic Commit**: Success path commits automatically
- **Automatic Rollback**: Exception path rolls back automatically
- **Manual Control**: Available when needed for complex scenarios
- **Nested Transactions**: Support for savepoints and nested contexts

### Token-Based Nested Session Support
**Internal mechanism for correct nested `ctx_session()` behavior**

`_SessionContextManager.set_session()` returns a `contextvars.Token` which captures the previous
ContextVar state. `reset_session(token)` restores that state when the inner context exits,
ensuring the outer session is correctly reinstated.

```python
# Internal flow (users should use ctx_session() directly):
# 1. ctx_session() creates a new AsyncSession
# 2. set_session(session) stores it in _explicit_sessions ContextVar, returns Token
# 3. On exit, reset_session(token) restores the previous ContextVar state

# This enables safe nesting:
async with ctx_session() as outer:
    # _explicit_sessions = {"default": outer}
    async with ctx_session() as inner:
        # _explicit_sessions = {"default": inner}
        pass
    # Token reset restores: _explicit_sessions = {"default": outer}
```

### Connection Pool Integration
```python
# Pool configuration for optimal performance
engine = create_async_engine(
    database_url,
    pool_size=20,           # Base connection pool
    max_overflow=30,        # Burst capacity
    pool_timeout=30,        # Connection wait timeout
    pool_recycle=3600,      # Connection refresh interval
    pool_pre_ping=True      # Connection health checks
)
```

## Error Handling and Recovery

### Session Error Recovery
- **Connection Errors**: Automatic retry with exponential backoff
- **Transaction Conflicts**: Deadlock detection and retry logic
- **Pool Exhaustion**: Graceful degradation and queuing
- **Database Unavailability**: Failover to backup databases

### Transaction Rollback Strategies
- **Automatic Rollback**: All exceptions trigger rollback
- **Partial Rollback**: Savepoint-based partial rollback
- **Manual Recovery**: Explicit rollback and retry logic
- **Error Propagation**: Clean error propagation to application layer

## Performance Optimization

### Session Reuse Patterns
- **Context Inheritance**: Reuse sessions across async tasks
- **Connection Pooling**: Efficient connection reuse
- **Prepared Statements**: Statement caching and reuse
- **Batch Operations**: Session-aware bulk processing

### Memory Management
- **Session Cleanup**: Automatic session cleanup and resource release
- **Object Expiration**: Configurable object expiration policies
- **Memory Monitoring**: Session memory usage tracking
- **Garbage Collection**: Proactive cleanup of unused sessions

## Integration Guidelines

### Framework Integration

#### ASGI Middleware (`sqlobjects.contrib.asgi`)
**Automatic request-scoped session for any ASGI framework**
```python
from fastapi import FastAPI
from sqlobjects.contrib.asgi import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware)
# Optional parameters: db_name="analytics", readonly=True

# How it works:
# 1. Creates AsyncSession for each HTTP/WebSocket request
# 2. Calls _SessionContextManager.set_session() with Token
# 3. Commits on success, rolls back on error
# 4. Calls reset_session(token) in finally block
```

#### FastAPI Dependency (`sqlobjects.contrib.fastapi`)
**Dependency injection for explicit session access**
```python
from fastapi import Depends
from sqlobjects.contrib.fastapi import get_db_session
from sqlobjects.session import AsyncSession

@app.post("/users")
async def create_user(session: AsyncSession = Depends(get_db_session)):
    user = await User.objects.using(session).create(username="alice")
    return {"id": user.id}
```

- **Standalone**: Direct usage without framework dependencies

### Testing Integration
```python
# Test session management
@pytest.fixture
async def test_session():
    async with ctx_session() as session:
        yield session
        # Automatic cleanup after test

# Isolated test transactions
async def test_user_creation(test_session):
    user = await User.objects.using(test_session).create(username="test")
    assert user.username == "test"
    # Transaction rolled back after test
```