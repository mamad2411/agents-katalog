# Query and Operation Implementation Rules

## Field Selection Architecture

### Field Selection Principle
**Provide flexible field loading with metadata caching**
- Load only necessary fields for improved performance
- Defer heavy fields until accessed
- Provide field metadata caching at class level
- Support deferred field loading strategies

```python
# Field selection examples
users = await User.objects.only("id", "username", "email").all()  # Load only needed fields
live_data = await User.objects.defer("bio", "profile_image").all()  # Defer heavy fields
```

### Field Selection Guidelines
- **Select appropriate fields**: Load only what's needed for the operation
- **Defer when appropriate**: Heavy fields, rarely accessed data, large binary content
- **Use field caching**: Leverage automatic field metadata caching
- **Optimize memory usage**: Use deferred loading for memory-intensive operations

## Query Method Classification System

### Query Building Methods (Return QuerySet)
**Chainable methods that modify query without execution**
```python
# Basic query building
User.objects.filter(User.is_active == True)      # Filtering
User.objects.exclude(User.is_deleted == True)    # Exclusion
User.objects.order_by("-created_at")             # Ordering
User.objects.limit(10).offset(20)                # Pagination
User.objects.select_related("profile")           # JOIN preload
User.objects.prefetch_related("posts")           # Separate query preload
User.objects.only("id", "username")              # Field selection
User.objects.defer("heavy_field")                # Field deferring
User.objects.undefer("field")                    # Remove from deferred

# Advanced query building
User.objects.distinct("department")              # Duplicate elimination
User.objects.annotate(post_count=func.count())   # Calculated fields
User.objects.group_by("department")              # Grouping
User.objects.having(func.count() > 5)            # Group filtering
User.objects.join(Post, condition)               # Manual joins (Model class)
User.objects.leftjoin(Comment, condition)        # Left joins (Model class)
User.objects.outerjoin(Tag, condition)           # Outer joins (Model class)
User.objects.select_for_update(nowait=True)      # Row locking
User.objects.select_for_share(skip_locked=True)  # Shared locking
User.objects.extra(columns={"custom": "1"})      # Extra SQL
User.objects.none()                              # Empty queryset
User.objects.reverse()                           # Reverse ordering
User.objects.skip_default_ordering()             # Skip default ordering

# Window functions (used via annotate)
User.objects.annotate(row_num=func.row_number().over(order_by=[User.created_at]))
User.objects.annotate(rank=func.rank().over(partition_by=[User.dept], order_by=[(User.salary, 'desc')]))

# CTE (Common Table Expressions)
User.objects.filter(User.age >= 18).cte("adults")       # Create CTE
User.objects.with_cte(adults_cte)                        # Use CTE in query
User.objects.with_cte(cte).select_from(cte)              # Select from CTE
```

### Expression Methods (Return Composable Expressions)
**Methods that create expressions for execution or use in other queries**
```python
# Aggregation expressions
stats = await User.objects.aggregate(avg_age=func.avg(User.age))
avg_age = User.objects.aggregate(avg_age=func.avg(User.age)).subquery(query_type="scalar")

# Count expressions
total = await User.objects.count()
user_count = User.objects.filter(User.is_active == True).count()

# Existence expressions
has_users = await User.objects.exists()
has_posts = Post.objects.filter(Post.author_id == User.id).exists()

# Collection expressions
users = await User.objects.all()
user = await User.objects.first()
user = await User.objects.last()
user = await User.objects.earliest("created_at")
user = await User.objects.latest("updated_at")

# Data extraction expressions
data = await User.objects.values("id", "username")
values = await User.objects.values_list("username", flat=True)

# Date/time extraction expressions
dates = await User.objects.dates("created_at", "year")
datetimes = await User.objects.datetimes("last_login", "hour")

# Index access expressions
user = await User.objects.get_item(0)
users = await User.objects.get_item(slice(0, 10))

# Subquery expressions
subquery = User.objects.filter(User.is_active == True).subquery("active_users")
```

### Query Execution Methods (Execute and Return Results)
**Terminal methods that execute queries and return final results**
```python
# Single object retrieval
user = await User.objects.get(User.id == 1)
user = await User.objects.filter(User.username == "john").get()

# Iterator for large datasets
async for user in User.objects.iterator(chunk_size=1000):
    await process_user(user)

# Raw SQL execution
users = await User.objects.raw("SELECT * FROM users WHERE age > :age", {"age": 18})
```

### Subquery Expression Creation
**Creating subqueries for use in other queries**
```python
# Scalar subqueries for comparisons
avg_age = User.objects.aggregate(avg_age=func.avg(User.age)).subquery(query_type="scalar")
older_users = await User.objects.filter(User.age > avg_age).all()

# EXISTS subqueries for boolean conditions
has_posts = Post.objects.filter(Post.author_id == User.id).subquery(query_type="exists")
authors = await User.objects.filter(has_posts).all()

# Table subqueries for complex JOINs
active_users = User.objects.filter(User.is_active == True).subquery("active_users")
posts = await Post.objects.join(active_users, Post.author_id == active_users.c.id).all()

# Direct subquery creation
subquery_expr = User.objects.subquery("user_subquery", query_type="auto")
```

## Smart Operation Detection System

### Intelligent save() Method Behavior
**Automatic CREATE vs UPDATE detection based on instance state**
```python
# CREATE operation (no primary key value)
user = User(username="new_user", email="new@example.com")
await user.save()  # Triggers: before_save → before_create → after_save → after_create

# UPDATE operation (has primary key value)
user.email = "updated@example.com"
await user.save()  # Triggers: before_save → before_update → after_save → after_update

# Detached instance UPDATE (has primary key, not in session)
detached_user = User(id=1, username="detached", email="detached@example.com")
await detached_user.save()  # Uses merge() strategy for UPDATE
```

### Detached Instance Operation Support
**Seamless operations on instances not attached to a session**
```python
# Detached instance operations automatically handle session attachment
detached_user = User(id=1)
await detached_user.refresh()                    # Loads current data from database
await detached_user.delete()                     # Deletes the record
detached_user.email = "new@example.com"
await detached_user.save()                       # Updates the record
```

### Operation Context Detection
```python
# Context information available in signals
async def before_save(self, context: SignalContext):
    print(f"Operation: {context.operation}")           # SAVE, CREATE, UPDATE, DELETE
    print(f"Actual operation: {context.actual_operation}")  # Detected operation for SAVE
    print(f"Session: {context.session}")               # Database session
    print(f"Instance: {context.instance}")             # Model instance
```

## Bulk Operation Architecture

### High-Performance Bulk Processing
**10-100x performance improvement for large datasets**
```python
# Bulk create with batch processing
users_data = [{"username": f"user{i}", "email": f"user{i}@example.com"} for i in range(10000)]
await User.objects.bulk_create(users_data, batch_size=1000)

# True bulk update (much faster than individual updates)
mappings = [
    {"id": 1, "status": "active", "last_seen": datetime.now()},
    {"id": 2, "status": "inactive", "last_seen": datetime.now()},
    # ... thousands of records
]
await User.objects.bulk_update(mappings, match_fields=["id"], batch_size=1000)

# Bulk delete with ID list
user_ids = [1, 2, 3, 4, 5]  # Thousands of IDs
await User.objects.bulk_delete(user_ids, id_field="id", batch_size=1000)
```

### Batch Size Control Strategy
```python
# Current implementation uses fixed batch sizes
# Database-specific optimization planned for future releases
await User.objects.bulk_create(users_data, batch_size=1000)  # Fixed batch size
await User.objects.bulk_update(mappings, batch_size=1000)    # Fixed batch size
await User.objects.bulk_delete(user_ids, batch_size=1000)    # Fixed batch size
```

## Expression System Integration

### Field Method Expressions
**Single-field operations using method chaining**
```python
# String operations
users = await User.objects.filter(User.username.like("%admin%")).all()
users = await User.objects.filter(User.email.ilike("%GMAIL%")).all()  # Case insensitive

# Numeric operations
adults = await User.objects.filter(User.age >= 18).all()
recent = await User.objects.filter(User.created_at > datetime.now() - timedelta(days=7)).all()

# Array operations (PostgreSQL)
posts = await Post.objects.filter(Post.tags.contains(["python"])).all()
```

### func Object Expressions
**Multi-field operations using SQLAlchemy functions**
```python
from sqlobjects.expressions import func

# String functions
users = await User.objects.annotate(
    full_name=func.concat(User.first_name, " ", User.last_name)
).all()

# Aggregate functions
stats = await User.objects.aggregate(
    total_users=func.count(),
    avg_age=func.avg(User.age),
    max_age=func.max(User.age)
)

# Date functions
users_by_year = await User.objects.annotate(
    signup_year=func.extract("year", User.created_at)
).all()
```

### Q Object Logic Combinations
**Complex logical expressions with proper precedence**
```python
from sqlobjects.queries import Q

# Q objects must be on the left side of operations
users = await User.objects.filter(
    Q(User.role == "admin") | Q(User.is_staff == True)
).all()

# Complex combinations with proper grouping
users = await User.objects.filter(
    Q(User.age >= 18) & (Q(User.role == "admin") | Q(User.is_staff == True))
).all()

# Negation
users = await User.objects.filter(~Q(User.is_deleted == True)).all()
```

## ObjectsManager Design Patterns

### Complete Method Coverage
**ObjectsManager provides comprehensive database operation interface**

#### Session Management
```python
User.objects.using(session)              # Bind to specific session
User.objects.using("analytics")          # Bind to named database
```

#### Query Building Shortcuts (Return QuerySet)
```python
User.objects.filter(User.is_active == True)
User.objects.exclude(User.is_deleted == True)
User.objects.order_by("-created_at")
User.objects.limit(10).offset(20)
User.objects.only("id", "username")
User.objects.defer("bio")
User.objects.undefer("bio")
User.objects.select_related("profile")
User.objects.prefetch_related("posts")
User.objects.distinct("department")
User.objects.annotate(count=func.count())
User.objects.group_by("department")
User.objects.having(func.count() > 5)
User.objects.join(Post, condition)               # Supports Model class, Table, or Subquery
User.objects.leftjoin(Comment, condition)        # Supports Model class, Table, or Subquery
User.objects.outerjoin(Tag, condition)           # Supports Model class, Table, or Subquery
User.objects.select_for_update(nowait=True)
User.objects.select_for_share(skip_locked=True)
User.objects.extra(columns={"custom": "1"})
User.objects.skip_default_ordering()
User.objects.none()
User.objects.reverse()

# CTE methods
User.objects.with_cte(cte_expr)                 # Use CTE in query
```

#### Expression Method Shortcuts
```python
User.objects.all()                       # AllExpression
User.objects.count()                     # CountExpression
User.objects.exists()                    # ExistsExpression
User.objects.aggregate(**kwargs)         # AggregateExpression
User.objects.first()                     # FirstExpression
User.objects.last()                      # LastExpression
User.objects.earliest(*fields)           # EarliestExpression
User.objects.latest(*fields)             # LatestExpression
User.objects.values(*fields)             # ValuesExpression
User.objects.values_list(*fields)        # ValuesListExpression
User.objects.dates(field, kind)          # DatesExpression
User.objects.datetimes(field, kind)      # DatetimesExpression
User.objects.get_item(key)               # GetItemExpression
User.objects.subquery(name)              # SubqueryExpression
```

#### Data Operation Methods
```python
# Creation operations
await User.objects.create(**kwargs)
await User.objects.get(**kwargs)
await User.objects.get_or_create(**lookup, defaults={})
await User.objects.update_or_create(**lookup, defaults={})
await User.objects.in_bulk(id_list, field_name="pk")

# Execution methods
await User.objects.raw(sql, params)
async for obj in User.objects.iterator(chunk_size=1000):
    pass

# Bulk operations
await User.objects.bulk_create(objects, batch_size=1000)
await User.objects.bulk_update(mappings, match_fields=["id"])
await User.objects.bulk_delete(ids, id_field="id")
await User.objects.delete_all(fast=False)
await User.objects.update_all(**values)
```

### Method Delegation Strategy
**ObjectsManager delegates to QuerySet for query building**
```python
class ObjectsManager(Generic[T]):
    def filter(self, *args, **kwargs) -> QuerySet[T]:
        """Create QuerySet and apply filter."""
        return QuerySet(self._table, self._model_class, self._db_or_session).filter(*args, **kwargs)
    
    def annotate(self, *args, **kwargs) -> QuerySet[T]:
        """Create QuerySet and apply annotation."""
        return self.filter().annotate(*args, **kwargs)
    
    def all(self):
        """Create AllExpression for execution."""
        return self.filter().all()
    
    def exists(self):
        """Create ExistsExpression for execution."""
        return self.filter().exists()

# Maintains type safety and method chaining
result = await User.objects.filter(User.is_active == True).exists()
queryset = User.objects.annotate(post_count=func.count()).filter(User.post_count > 5)
users = await User.objects.all()
```

### Instance Creation Pattern
**ObjectsManager uses from_dict() for consistent instance creation**
```python
class ObjectsManager(Generic[T]):
    @emit_signals(Operation.SAVE)
    async def create(self, validate: bool = True, **kwargs) -> T:
        """Create new object with proper initialization."""
        # Use from_dict for consistent state initialization
        obj = self._model_class.from_dict(kwargs, validate=False)
        
        # Execute validation if requested
        if validate:
            obj.validate_all_fields()
        
        # Execute INSERT directly (signals handled by decorator)
        stmt = insert(self._table).values(**obj._get_all_data())
        session = self._get_session(readonly=False)
        result = await session.execute(stmt)
        
        # Set primary key from result
        if result.inserted_primary_key:
            obj._set_primary_key_values(result.inserted_primary_key)
        
        return obj
    
    async def get_or_create(self, defaults=None, validate=True, **lookup):
        """Get or create with consistent initialization."""
        try:
            obj = await self.filter(*conditions).get()
            return obj, False
        except DoesNotExist:
            create_data = lookup.copy()
            if defaults:
                create_data.update(defaults)
            
            # Use from_dict for consistent initialization
            obj = self._model_class.from_dict(create_data, validate=False)
            await obj.using(self._get_session(readonly=False)).save(validate=validate)
            return obj, True

# Benefits of from_dict():
# - Handles init=False fields correctly
# - Clears dirty field tracking
# - Applies validation consistently
# - Ensures clean state initialization
```

## Component Architecture Rules

### QueryBuilder - SQL Construction and Optimization
**Immutable query building through composition**
```python
# All methods return new QueryBuilder instances
new_builder = builder.add_filter(User.age >= 18)
new_builder = builder.add_ordering("-created_at")
new_builder = builder.add_annotations(post_count=func.count())

# Handles all SQL clauses
- Conditions (WHERE)
- Ordering (ORDER BY)
- Grouping (GROUP BY, HAVING)
- Joins (INNER, LEFT, OUTER)
- Locking (FOR UPDATE, FOR SHARE)
- Pagination (LIMIT, OFFSET)
```

### FieldCache - Metadata Caching Mechanism
**Automatic field metadata caching at class level**
```python
# Field cache access
field_cache = User._get_field_cache()

# Field categorization
deferred_fields = field_cache.get("deferred_fields", set())
relationship_fields = field_cache.get("relationship_fields", set())
regular_fields = field_cache.get("regular_fields", set())

# Performance optimization through field metadata caching
```

### QueryExecutor - Unified Query Execution
**Single execution interface for all query types**
```python
# Unified execute method
result = await executor.execute(
    query, 
    query_type="all",  # all, count, exists, update, delete, etc.
    deferred_fields=deferred_fields,
    field_cache=field_cache
)

# Iterator support for memory efficiency
async for item in executor.iterator(query, chunk_size=1000):
    yield item  # Automatic memory cleanup every 10 chunks
```

## Advanced Query Method Rules

### Distinct Operations
```python
# Remove duplicate rows
.distinct()           # All columns
.distinct("field1", "field2")  # Specific fields
```

### Annotation Operations
```python
# Add calculated fields using func expressions
.annotate(
    full_name=func.concat(User.first_name, " ", User.last_name),
    post_count=func.count(User.posts),
    latest_post=func.max(User.posts.created_at)
)
```

### Grouping and Aggregation
```python
# GROUP BY and HAVING clauses
.group_by("department", "role")
.having(func.count() > 5, func.avg(User.salary) > 50000)
```

### Manual Joins
```python
# Manual joins (supports Model class, Table object, or Subquery)
.join(Post, User.id == Post.author_id, join_type="inner")      # Using Model class (recommended)
.leftjoin(Comment, Post.id == Comment.post_id)                 # Using Model class
.outerjoin(Tag, Post.id == Tag.post_id)                        # Using Model class

# Backward compatible: using Table object
.join(Post.__table__, User.id == Post.author_id)
```

### Row Locking
```python
# Pessimistic locking
.select_for_update(nowait=False, skip_locked=False)  # FOR UPDATE
.select_for_share(nowait=True, skip_locked=True)     # FOR SHARE
```

### Date and Time Extraction
```python
# Multi-database compatible date extraction
.dates(field, precision, order="ASC")    # Returns list[date]
.datetimes(field, precision, order="ASC") # Returns list[datetime]

# Supported precision levels:
# dates(): "year", "month", "day"  
# datetimes(): "year", "month", "day", "hour", "minute", "second"
```

### Index Access Operations
```python
# QuerySet index and slice access
.get_item(index)        # Single item by integer index
.get_item(slice_obj)    # Multiple items by slice object
```

## Query Operation Implementation Changes

### New Query Method Addition Process
1. **Interface Design**: Define method signature and return type
2. **QueryBuilder Integration**: Add method to QueryBuilder with proper chaining
3. **SQL Generation**: Implement SQLAlchemy query generation in build() method
4. **QuerySet Integration**: Add corresponding method to QuerySet
5. **ObjectsManager Integration**: Add delegation method to ObjectsManager for API completeness
6. **Field Selection Compatibility**: Ensure method works with field selection system
7. **Type Safety**: Add proper type annotations and validation
8. **Testing**: Comprehensive tests for all parameter combinations
9. **Documentation**: Update query documentation with examples

### Database Compatibility Implementation
1. **Dialect Detection**: Use `session.bind.dialect.name` to detect database type
2. **Function Mapping**: Map to database-specific functions (PostgreSQL: `date_trunc()`, SQLite: `strftime()`, MySQL: `date_format()`)
3. **Type Conversion**: Ensure consistent Python object types across databases
4. **Fallback Strategy**: Provide `extract()` function fallback for unsupported databases

## Advanced Query Patterns

### Subquery Integration Patterns
```python
# Scalar subqueries for comparisons
avg_age = User.objects.aggregate(avg_age=func.avg(User.age)).subquery(query_type="scalar")
older_users = await User.objects.filter(User.age > avg_age).all()

# EXISTS subqueries for boolean conditions
has_posts = Post.objects.filter(Post.author_id == User.id).subquery(query_type="exists")
authors = await User.objects.filter(has_posts).all()

# Table subqueries for complex JOINs
active_users = User.objects.filter(User.is_active == True).subquery("active_users")
posts = await Post.objects.join(active_users, Post.author_id == active_users.c.id).all()
```

### Advanced Query Patterns
```python
# Basic aggregations
stats = await User.objects.aggregate(
    total_users=func.count(),
    avg_age=func.avg(User.age),
    max_age=func.max(User.age)
)

# Subquery patterns
avg_age = User.objects.aggregate(avg_age=func.avg(User.age)).subquery(query_type="scalar")
older_users = await User.objects.filter(User.age > avg_age).all()
```

### Window Function Patterns
```python
from sqlobjects.expressions import func

# Window functions must be used via annotate(), not executed directly
users = await User.objects.annotate(
    row_num=func.row_number().over(order_by=[User.created_at]),
    dept_rank=func.rank().over(
        partition_by=[User.department],
        order_by=[(User.salary, 'desc')]
    ),
    prev_salary=func.lag(User.salary, 1).over(order_by=[User.created_at])
).all()

# Available window functions:
# Ranking: row_number(), rank(), dense_rank(), percent_rank(), ntile(n)
# Offset: lag(col, offset, default), lead(col, offset, default)
# Value: first_value(col), last_value(col), nth_value(col, n)
```

### CTE Patterns
```python
# Basic CTE - reusable named subquery
adults = User.objects.filter(User.age >= 18).cte("adults")
result = await User.objects.with_cte(adults).filter(adults.c.age < 30).all()

# Multiple CTEs
active = User.objects.filter(User.is_active == True).cte("active")
recent = User.objects.filter(User.created_at >= cutoff).cte("recent")
result = await User.objects.with_cte(active, recent).all()

# Recursive CTE - hierarchical data
base = Employee.objects.filter(Employee.manager_id.is_(None)).cte("tree", recursive=True)
recursive = Employee.objects.join(base, Employee.manager_id == base.c.id)
tree = base.union_all(recursive)
all_emps = await Employee.objects.with_cte(tree).select_from(tree).all()
```

## Performance Optimization Rules

### Query Optimization Guidelines
```python
# Use select_related for foreign key relationships (JOIN)
posts = await Post.objects.select_related("author", "category").all()

# Use prefetch_related for reverse relationships (separate queries)
users = await User.objects.prefetch_related("posts", "comments").all()

# Skip default ordering when not needed (significant performance boost)
count = await User.objects.skip_default_ordering().count()

# Use only() and defer() for field selection
users = await User.objects.only("id", "username", "email").all()
users = await User.objects.defer("bio", "profile_image").all()
```

### Memory Management Patterns
```python
# Use iterator for large result sets
async for user in User.objects.filter(User.is_active == True).iterator():
    await process_user(user)

# Configure chunk size for optimal performance
async for user in User.objects.iterator(chunk_size=1000):
    await process_user(user)
    # Automatic memory cleanup every 10 chunks (fixed interval)

# Efficient pagination for large datasets
last_id = 0
while True:
    users = await User.objects.filter(User.id > last_id).order_by("id").limit(100).all()
    if not users:
        break
    for user in users:
        await process_user(user)
    last_id = users[-1].id

# Field selection for memory optimization
large_dataset = await User.objects.defer("heavy_field").filter(
    User.created_at >= datetime.now() - timedelta(days=1)
).iterator(chunk_size=500)
```

### Bulk Operation Performance Rules
- **Batch Size Selection**: Use database-appropriate batch sizes
- **Memory Management**: Process large datasets in chunks
- **Transaction Control**: Use appropriate transaction boundaries
- **Error Handling**: Implement proper error recovery for bulk operations
- **Progress Monitoring**: Provide progress feedback for long-running operations