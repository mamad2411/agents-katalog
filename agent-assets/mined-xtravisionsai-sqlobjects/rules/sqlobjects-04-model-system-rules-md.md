# Model System Implementation Rules

## ObjectModel Base Class Design

### Inheritance Chain Architecture
```python
# Core inheritance structure
ObjectModel
├── ModelMixin (complete functionality integration)
│   ├── FieldCacheMixin (field caching and attribute access optimization)
│   ├── DataConversionMixin (data conversion functionality)
│   ├── DeferredLoadingMixin (deferred loading functionality)
│   ├── ValidationMixin (validation logic)
│   ├── PrimaryKeyMixin (primary key operations)
│   ├── SessionMixin (session management)
│   └── BaseMixin (basic functionality and state management)
├── SignalMixin (signal processing)
├── HistoryTrackingMixin (history tracking)
└── ModelProcessor (metadata processor)
```

### Automatic Table Generation
- **Table Naming**: Rails-style pluralization (User → users, Category → categories)
- **Primary Key Detection**: Automatic id field creation if no primary key defined
- **Composite Keys**: Support for multi-column primary keys
- **Index Generation**: Automatic index creation from field parameters

### Model Configuration System

#### Config Class Processing
```python
class User(ObjectModel):
    class Config:
        table_name = "app_users"        # Override default table name
        ordering = ["-created_at"]       # Default query ordering
        indexes = [                      # Additional indexes
            index("idx_username", "username", unique=True),
            index("idx_email_domain", func.split_part("email", "@", 2))
        ]
        constraints = [                  # Table constraints
            constraint("age >= 0", "chk_positive_age"),
            unique("username", "email", name="uq_user_identity")
        ]
```

#### Configuration Inheritance and Merging
- **Parent Config**: Child classes inherit parent configuration
- **Override Rules**: Child config overrides parent config by key
- **List Merging**: Indexes and constraints are merged, not replaced
- **Validation**: Configuration validated at class creation time

## Proxy System Architecture

### Deferred Field Proxy
- **DeferredObject**: Proxy for deferred loading fields
- **Auto-creation**: Created in `__getattribute__` when accessing unloaded deferred fields
- **Caching**: Stored in `_state_manager.object_cache` after creation
- **Lazy loading**: Supports `fetch()` method for explicit data loading
- **State tracking**: Integrates with `_deferred_fields` and `_loaded_deferred_fields`

### Relation Field Proxy
- **RelatedObject**: Proxy for single relationship fields (ForeignKey, OneToOne)
- **RelatedCollection**: Proxy for collection relationships (OneToMany, ManyToMany)
- **Lazy loading**: Load relationship data on demand via `fetch()` method
- **Prefetch integration**: Returns prefetched data when available
- **Cascade support**: Handles cascade save operations for assigned relationships

### Proxy Integration in FieldCacheMixin
```python
class FieldCacheMixin(DataConversionMixin):
    def __getattribute__(self, name: str):
        """Optimized attribute access using unified proxy cache."""
        # Skip special attributes and methods
        if name.startswith("_") or name in method_names:
            return super().__getattribute__(name)
        
        # Check object cache first
        object_cache = self._state_manager.get_object_cache()
        if name in object_cache:
            return object_cache[name]  # May be value, prefetch data, or proxy
        
        # Get field cache from model class
        field_cache = model_class._get_field_cache()
        
        # Handle deferred fields
        if name in field_cache.get("deferred_fields", set()):
            if name in self._deferred_fields and not self.is_field_loaded(name):
                if self._state_manager.is_from_database():
                    proxy = DeferredObject(self, name)
                    self._update_cache(name, proxy)
                    return proxy
        
        # Handle relationship fields
        if name in field_cache.get("relationship_fields", set()):
            # Check cascade_relationships first (manually assigned values)
            cascade_relationships = self._state_manager.get_cascade_relationships()
            if name in cascade_relationships:
                return cascade_relationships[name]
            
            # Return relationship proxy from descriptor
            relationships = getattr(self.__class__, "_relationships", {})
            if name in relationships:
                descriptor = relationships[name]
                proxy = descriptor.__get__(self, self.__class__)
                self._update_cache(name, proxy)
                return proxy
        
        return super().__getattribute__(name)
```

### Proxy Usage Examples
```python
from sqlobjects.fields.proxies import DeferredObject, RelatedObject, RelatedCollection

class User(ObjectModel):
    bio: Column[str] = column(type="text", deferred=True)
    posts: Related[list["Post"]] = relationship("Post")

# Deferred field proxy
user = await User.objects.defer("bio").get(User.id == 1)
assert isinstance(user.bio, DeferredObject)
bio_content = await user.bio.fetch()  # Explicit loading

# Relationship proxy
assert isinstance(user.posts, RelatedCollection)
posts = await user.posts.fetch()  # Load related posts

# Cascade relationship assignment
user.posts = [post1, post2]  # Stored in cascade_relationships
assert user._state_manager.needs_cascade_save()  # Marked for cascade
```

## State Management Architecture

### StateManager Design
- **Unified state storage**: Avoid state conflicts between mixins
- **Efficient state sharing**: State access across inheritance hierarchies
- **Memory optimization**: Minimize state storage overhead

### State Types
```python
# State type definitions
state_manager = StateManager()
state_manager.set("dirty_fields", set())           # Dirty field tracking
state_manager.set("deferred_fields", set())        # Deferred field set
state_manager.set("loaded_deferred_fields", set()) # Loaded deferred fields
state_manager.set("bound_session", None)           # Bound database session
state_manager.set("proxy_cache", {})               # Proxy object cache
```

## Field System Architecture

### Type System Implementation
```python
# Type creation using create_type_instance function
from sqlobjects.fields.types import create_type_instance

# Create SQLAlchemy type from type name and parameters
enhanced_type = create_type_instance(type_name, type_params)

# Supports auto type inference from Column[T] annotations
if type_name == "auto":
    annotations = getattr(owner, "__annotations__", {})
    if name in annotations:
        annotation = annotations[name]
        inferred_type, inferred_params = _infer_type_from_annotation(annotation)
        type_name = inferred_type
```

### Parameter Processing Pipeline
1. **Extraction**: Extract SQLAlchemy parameters from function arguments
2. **Transformation**: Convert Python types to SQLAlchemy types
3. **Validation**: Validate parameter combinations and constraints
4. **Init Parameter Processing**: Apply intelligent defaults for init parameter based on field characteristics
5. **Instantiation**: Create SQLAlchemy Column instance with processed parameters

### Field Constructor Participation Principle
**Fields should participate in object construction based on their nature**
- Auto-generated fields should not require user input during construction
- User-input fields should be accessible through the constructor
- System-managed fields should be handled transparently
- Clear error messages should guide proper field usage

### Field Definition Strategies

#### Column Descriptor Pattern
```python
# Column class acts as descriptor for field definitions
from sqlobjects.fields import Column, column

# Using column() function with type parameter
name: Column[str] = column(type="string", length=100, nullable=False)
age: Column[int] = column(type="integer", nullable=True, default=0)
data: Column[dict] = column(type="json", default=dict)

# Auto type inference from Column[T] annotation
name: Column[str] = column(type="auto")  # Infers "string" from Column[str]
age: Column[int] = column(type="auto")  # Infers "integer" from Column[int]

# Enhanced functionality parameters
username: Column[str] = column(
    type="string", length=50,
    validators=[validate_length(3, 50)],
    deferred=False,
    init=True, repr=True, compare=False
)
```

#### Shortcut Functions
```python
# Convenience functions for common types
from sqlobjects.fields import StringColumn, IntegerColumn, JsonColumn

name: Column[str] = StringColumn(length=100)
age: Column[int] = IntegerColumn(nullable=True, default=0)
data: Column[dict] = JsonColumn(default=dict)
```

#### Field Definition Guidelines
- **column() function**: Provides explicit control and supports all parameters
- **Shortcut functions**: Convenient for common field types
- **Type inference**: Use `type="auto"` to infer from Column[T] annotation
- **Consistency**: Maintain consistent approach within each project

### Advanced Field Parameters

#### Enhanced Field Parameters
```python
# Performance optimization parameters
bio: Column[str] = column(
    type="text",
    deferred=True,  # Defer loading until accessed
    deferred_group="details",  # Group deferred fields
    deferred_raiseload=True  # Raise error if accessed when deferred
)
important_field: Column[str] = column(
    type="string",
    active_history=True  # Track field value changes
)

# Code generation control parameters
internal_id: Column[str] = column(type="string", init=False, repr=False)  # Hidden from __init__ and __repr__
api_key: Column[str] = column(type="string", repr=False, compare=False)   # Hidden from __repr__ only
sort_key: Column[int] = column(type="integer", compare=True, hash=True)   # Used in comparison operations
optional_param: Column[str] = column(type="string", kw_only=True)         # Keyword-only in __init__

# Enhanced functionality parameters
created_at: Column[datetime] = column(
    type="datetime",
    default_factory=datetime.now,  # Dynamic default
    validators=[validate_datetime()]  # Field-level validation
)
status: Column[str] = column(
    type="string",
    insert_default="pending"  # Default only for INSERT operations
)

# Init parameter controls constructor participation
id: Column[int] = column(type="integer", primary_key=True, init=False)  # Excluded from __init__
created_at: Column[datetime] = column(type="datetime", server_default=func.now(), init=False)  # Server-generated
user_input: Column[str] = column(type="string", init=True)  # Included in __init__
```

#### Special Field Types
```python
# Array columns (PostgreSQL)
tags: Column[list[str]] = ArrayColumn("string")
matrix: Column[list[list[int]]] = ArrayColumn("integer", dimensions=2)

# Enum columns
status: Column[UserStatus] = EnumColumn(UserStatus, default=UserStatus.ACTIVE)

# Identity and computed columns
id: Column[int] = identity(start=1, increment=1)
full_name: Column[str] = computed(
    "first_name || ' ' || last_name",
    column_type="string"
)

# UUID columns with automatic generation
uuid: Column[str] = UuidColumn(default_factory=uuid.uuid4)
```

## Model Implementation Change Management

### New Field Type Addition Process
1. **Design Phase**: Define type mapping and parameter requirements
2. **Registration**: Add to TypeRegistry with appropriate SQLAlchemy type
3. **Shortcut Function**: Create convenience function if commonly used
4. **Testing**: Comprehensive tests for all parameter combinations
5. **Documentation**: Update field documentation with examples

### Model Feature Extension Process
1. **Compatibility Analysis**: Assess impact on existing models
2. **Interface Design**: Design backward-compatible API extensions
3. **Implementation**: Implement with feature flags if needed
4. **Migration Tools**: Provide migration utilities if schema changes required
5. **Documentation**: Update model documentation and examples

### Configuration System Modifications
1. **Parser Updates**: Modify configuration parsing logic
2. **Validation Rules**: Update configuration validation
3. **Application Logic**: Update configuration application to model
4. **Backward Compatibility**: Ensure existing configurations still work
5. **Migration Guide**: Provide migration guide for configuration changes

## Primary Key and Identity Management

### Primary Key Detection Logic
```python
# Automatic primary key detection priority:
# 1. Explicit primary_key=True parameter
# 2. Field named 'id' with integer type
# 3. Composite primary key from multiple primary_key=True fields
# 4. Auto-generated 'id' field if no primary key found

# Examples
class User(ObjectModel):
    # Explicit primary key
    user_id: Column[int] = IntegerColumn(primary_key=True)

class Post(ObjectModel):
    # Implicit primary key (auto-generated 'id' field)
    title: Column[str] = StringColumn(length=200)

class UserRole(ObjectModel):
    # Composite primary key
    user_id: Column[int] = foreign_key("users.id", primary_key=True)
    role_id: Column[int] = foreign_key("roles.id", primary_key=True)
```

### Identity and Computed Field Shortcuts
```python
# Identity columns with database-native auto-increment
id: Column[int] = identity()  # Auto-increment primary key
order_id: Column[int] = identity(start=1000, increment=1, cache=10)

# Computed columns with SQL expressions
full_name: Column[str] = computed(
    "first_name || ' ' || last_name",
    column_type="string"
)
total: Column[Decimal] = computed(
    "subtotal * (1 + tax_rate)",
    persisted=True,  # Store computed value in database
    column_type="numeric"
)

# Timestamp fields using column() function
created_at: Column[datetime] = column(type="datetime", default_factory=datetime.now)
updated_at: Column[datetime] = column(type="datetime", onupdate=datetime.now)
```

## Model Validation Integration

### Multi-Level Validation Architecture
```python
class User(ObjectModel):
    # Field-level validation using validators parameter
    email: Column[str] = column(type="string", validators=[validate_email()])
    age: Column[int] = column(type="integer", validators=[validate_range(0, 150)])
    
    # Model-level validation
    def validate(self):
        if self.age and self.age < 13:
            raise ValidationError("Users must be at least 13 years old")
        
        # Cross-field validation
        if self.is_admin and self.age < 18:
            raise ValidationError("Admin users must be adults")
```

### Validation Execution Flow
1. **Field Validation**: Execute field-level validators during assignment
2. **Model Validation**: Execute model validate() method before save
3. **Database Validation**: Database constraints as final validation layer
4. **Error Collection**: Collect and report all validation errors together

## Dirty Field Tracking System

### Automatic Tracking
- **__setattr__ interception**: Automatically track field modifications
- **Smart filtering**: Skip private attributes and initialization phase
- **Performance optimization**: Minimize tracking overhead
- **Creation vs Modification**: New instances clear dirty fields after from_dict() creation

### UPDATE Optimization
```python
# Incremental update example
user = await User.objects.get(User.id == 1)
user.email = "new@example.com"  # Automatically mark as dirty field
await user.save()  # Only update email field

# New instance creation (no dirty fields)
user = User.from_dict({"username": "john", "email": "john@example.com"})
# Dirty fields cleared after creation to prevent unnecessary UPDATE operations

# Batch cleanup: Automatically clean dirty field marks after save
# Transaction safety: Work cooperatively with transaction system
```

## Field Cache Optimization Rules

### Field Classification Cache
- **Auto-classification**: Fields automatically classified as deferred, relationship, regular
- **LRU caching**: Field information uses LRU cache
- **Cache invalidation**: Provide manual cache invalidation mechanism

### Attribute Access Optimization
```python
# Attribute access optimization example
class User(ObjectModel):
    def __getattribute__(self, name: str):
        # Smart skip: Skip optimization for special attributes and methods
        # Proxy creation: Create field proxy objects on demand
        # Cache reuse: Reuse proxy object cache
        pass
```

## Performance Optimization Rules

### Model Creation Optimization
- **Metaclass Caching**: Cache model metadata creation
- **Lazy Loading**: Defer expensive operations until needed
- **Memory Efficiency**: Minimize memory footprint of model instances
- **Type Checking**: Optimize type checking for runtime performance

### Field Processing Optimization
- **LRU Caching**: Cache field instance creation
- **Parameter Reuse**: Reuse common parameter combinations
- **Lazy Evaluation**: Defer field processing until table creation
- **Memory Pooling**: Reuse field instances where possible

### Configuration Processing Optimization
- **Parse Once**: Parse configuration once at class creation
- **Inheritance Caching**: Cache inherited configuration
- **Validation Caching**: Cache validation results
- **Merge Optimization**: Optimize configuration merging algorithms

## Core Method Implementation Rules

### save() Method Implementation

**Strategy**: UPSERT with fallback to query-then-save

```python
@emit_signals(Operation.SAVE)
async def save(self, validate: bool = True, cascade: bool | None = None, session=None):
    """Save operation with UPSERT support and cascade handling.
    
    Implementation:
    1. Determine cascade behavior from model relationships
    2. Use CascadeExecutor for cascade operations
    3. Call _save_internal for direct save operations
    """
    if cascade is None:
        cascade = self._has_cascade_relations()
    
    if cascade:
        executor = CascadeExecutor()
        return await executor.execute_save_operation(self, validate, session)
    
    return await self._save_internal(validate, session)

async def _save_internal(self, validate: bool = True, session=None):
    """Internal save using UPSERT with fallback.
    
    Implementation:
    1. Try UPSERT using UpsertHandler (PostgreSQL ON CONFLICT, SQLite INSERT OR REPLACE)
    2. Fallback to query-then-save for unsupported databases
    3. Query database to determine INSERT or UPDATE
    4. Execute appropriate operation
    """
    # Try UPSERT first
    try:
        from .objects.upsert import ConflictResolution, UpsertHandler
        handler = UpsertHandler(session)
        stmt = handler.get_upsert_statement(
            table=table,
            values=[data],
            conflict_resolution=ConflictResolution.UPDATE,
            match_fields=pk_columns,
        )
        result = await session.execute(stmt)
        # Handle result...
    except (ValueError, Exception):
        # Fallback: query database to determine operation
        existing = await session.execute(select(table).where(and_(*pk_conditions)))
        if existing.first():
            # UPDATE operation
            update_data = self._get_dirty_data()
            stmt = update(table).where(and_(*pk_conditions)).values(**update_data)
        else:
            # INSERT operation
            stmt = insert(table).values(**data)
        await session.execute(stmt)
```

**Operation Detection for Signals**:
- `_determine_save_operation()` checks `_has_primary_key_values()`
- Returns `Operation.CREATE` if no primary key values
- Returns `Operation.UPDATE` if primary key values exist
- Used by `emit_signals` decorator to emit specific signals

### Object Creation Consistency Principle

**All object creation paths produce consistent clean state**

```python
@classmethod
def from_dict(cls, data: dict[str, Any], validate: bool = True):
    """Create model instance from dictionary with clean state.
    
    Implementation:
    1. Filter data to include only valid table fields
    2. Separate init=True and init=False fields
    3. Call __init__ with init=True fields
    4. Set init=False fields directly (id, server_default fields)
    5. Clear dirty_fields immediately after creation
    6. Execute validation if requested
    """
    # Separate fields by init parameter
    init_data = {}
    non_init_data = {}
    
    for field_name, value in filtered_data.items():
        field_attr = getattr(cls, field_name, None)
        if field_attr and hasattr(field_attr, "get_codegen_params"):
            codegen_params = field_attr.get_codegen_params()
            if codegen_params.get("init", True):
                init_data[field_name] = value
            else:
                non_init_data[field_name] = value
    
    # Create instance with init fields
    instance = cls(**init_data)
    
    # Set non-init fields directly
    for field_name, value in non_init_data.items():
        setattr(instance, field_name, value)
    
    # CRITICAL: Clear dirty fields to ensure clean state
    instance._state_manager.clear_dirty_fields()
    
    if validate:
        instance.validate_all_fields()
    
    return instance
```

**Why Clear Dirty Fields**:
- New instances should not have dirty field markers
- Prevents unnecessary UPDATE operations on first save()
- Maintains consistency across all creation methods
- Ensures predictable object state

**Consistent Creation Methods**:
```python
# All methods produce clean state
user = User.from_dict({"username": "john", "email": "john@example.com"})
user = await User.objects.create(username="jane")
user, created = await User.objects.get_or_create(username="bob")

# All instances have clean state after creation
assert len(user._state_manager.get_dirty_fields()) == 0
```

## Validation System Integration

### Multi-Level Validation
- **Field level**: Specify validators in field definition
- **Model level**: Override validate() method
- **Signal level**: Execute validation in before_save

### Validation Timing
- **Auto validation**: save() method executes validation by default
- **Manual validation**: Provide validate_field() and validate_all_fields()
- **Skip validation**: Support validate=False parameter

```python
# Validation integration example
class User(ObjectModel):
    email: Column[str] = column(type="string", validators=[validate_email()])  # Field level
    
    def validate(self):  # Model level
        if self.age < 18 and self.is_admin:
            raise ValidationError("Admin users must be adults")
    
    async def before_save(self, context):  # Signal level
        if not self.email:
            raise ValidationError("Email is required")
```

## Testing and Quality Assurance

### Model Testing Patterns
```python
# Model definition testing
def test_user_model_creation():
    assert User.__table__.name == "users"
    assert "username" in User.__table__.columns
    assert User.__table__.columns["username"].type.length == 50

# Field validation testing
async def test_user_validation():
    with pytest.raises(ValidationError):
        user = User(age=-5)
        user.validate()

# Configuration testing
def test_user_config():
    assert User.Config.table_name == "users"
    assert len(User.Config.indexes) == 2
```

### Performance Testing Requirements
- **Model Creation Benchmarks**: Measure model class creation time
- **Field Processing Benchmarks**: Measure field instantiation performance
- **Memory Usage Tests**: Monitor memory usage of model instances
- **Configuration Processing Tests**: Measure configuration parsing performance

## Integration Testing Rules

### Proxy System Testing
```python
# Deferred loading test
async def test_deferred_field_proxy():
    user = await User.objects.defer("bio").get(User.id == 1)
    assert isinstance(user.bio, DeferredFieldProxy)
    bio_content = await user.bio.fetch()
    assert isinstance(bio_content, str)

# Relationship proxy test
async def test_relation_field_proxy():
    user = await User.objects.get(User.id == 1)
    assert isinstance(user.posts, RelationFieldProxy)
    posts = await user.posts.fetch()
    assert isinstance(posts, list)

# Error handling test
def test_proxy_error_handling():
    proxy = DeferredFieldProxy(user, "bio")
    with pytest.raises(DeferredFieldError):
        len(proxy)  # Should throw friendly error message
```

### State Management Testing
```python
# Dirty field test
def test_dirty_field_tracking():
    user = User(username="test")
    assert "username" in user._state_manager.get("dirty_fields")
    
    user._state_manager.get("dirty_fields").clear()
    user.email = "test@example.com"
    assert "email" in user._state_manager.get("dirty_fields")
    assert "username" not in user._state_manager.get("dirty_fields")

# State isolation test
def test_state_isolation():
    user1 = User(username="user1")
    user2 = User(username="user2")
    
    user1._state_manager.set("test_key", "value1")
    user2._state_manager.set("test_key", "value2")
    
    assert user1._state_manager.get("test_key") == "value1"
    assert user2._state_manager.get("test_key") == "value2"

# Cache test
def test_field_cache():
    cache = User._get_field_cache()
    assert "deferred_fields" in cache
    assert "relationship_fields" in cache
    assert "regular_fields" in cache
```

### Signal Integration Testing
```python
# Auto-registration test
def test_signal_auto_registration():
    class TestUser(ObjectModel):
        async def before_save(self, context):
            self.test_flag = True
    
    # Signal handlers should be auto-registered
    user = TestUser(username="test")
    await user.save()
    assert hasattr(user, "test_flag")

# Signal triggering test
async def test_signal_triggering():
    signals_called = []
    
    class TestUser(ObjectModel):
        async def before_save(self, context):
            signals_called.append("before_save")
        
        async def before_create(self, context):
            signals_called.append("before_create")
    
    user = TestUser(username="test")
    await user.save()
    
    assert "before_save" in signals_called
    assert "before_create" in signals_called

# Context test
async def test_signal_context():
    class TestUser(ObjectModel):
        async def before_save(self, context):
            assert context.operation == Operation.SAVE
            assert context.instance == self
            assert context.model_class == TestUser
    
    user = TestUser(username="test")
    await user.save()
```

### ObjectsManager Integration Testing
```python
# Test ObjectsManager method coverage
async def test_objects_manager_method_coverage():
    # Test that all QuerySet methods are available on ObjectsManager
    assert hasattr(User.objects, 'exists')
    assert hasattr(User.objects, 'annotate')
    assert hasattr(User.objects, 'subquery')
    assert hasattr(User.objects, 'raw')
    
    # Test method delegation works correctly
    exists_result = await User.objects.exists()
    assert isinstance(exists_result, bool)
    
    annotated_qs = User.objects.annotate(count=func.count())
    assert hasattr(annotated_qs, 'filter')  # Should return QuerySet

# Test from_dict integration in ObjectsManager
async def test_objects_manager_from_dict_integration():
    # Test create() uses from_dict
    user = await User.objects.create(username="test", email="test@example.com")
    assert not user._state_manager.get("dirty_fields")  # Should be clean after creation
    
    # Test get_or_create() uses from_dict for creation
    user, created = await User.objects.get_or_create(
        username="new_user",
        defaults={"email": "new@example.com"}
    )
    if created:
        assert not user._state_manager.get("dirty_fields")  # Should be clean

# Test constructor behavior
def test_constructor_behavior():
    class TestModel(ObjectModel):
        id: Column[int] = IntegerColumn(primary_key=True)
        name: Column[str] = StringColumn()
        created_at: Column[datetime] = column(type="datetime", server_default=func.now())
    
    # Test constructor accepts appropriate fields
    model = TestModel(name="test")
    assert model.name == "test"
    
    # Test from_dict handles all fields and produces clean state
    model = TestModel.from_dict({"id": 1, "name": "test", "created_at": datetime.now()})
    assert model.id == 1
    assert model.name == "test"
    
    # Verify clean state after creation
    dirty_fields = model._state_manager.get("dirty_fields", set())
    assert len(dirty_fields) == 0
```