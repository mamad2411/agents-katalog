# Signal System and Extension Implementation Rules

## Signal System Architecture

### Signal System Integration
**ObjectModel with SignalMixin provides signal functionality**
```python
from sqlobjects.model import ObjectModel
from sqlobjects.signals import SignalContext, Operation
from datetime import datetime

class User(ObjectModel):  # Inherits SignalMixin through ModelMixin
    username: Column[str] = StringColumn(length=50)
    email: Column[str] = StringColumn(length=100)
    
    # Signal handlers discovered by method name convention
    async def before_save(self, context: SignalContext):
        self.updated_at = datetime.now()
    
    async def after_create(self, context: SignalContext):
        await self.send_welcome_email()
```

### Instance-Level Signal Types
**Signals for single record operations with automatic detection**
```python
from sqlobjects.model import ObjectModel
from sqlobjects.signals import SignalContext
from datetime import datetime
import uuid

class User(ObjectModel):  # Built-in signal functionality
    # Universal save signals (always triggered)
    async def before_save(self, context: SignalContext):
        """Called before any save operation (CREATE or UPDATE)"""
        self.updated_at = datetime.now()
    
    async def after_save(self, context: SignalContext):
        """Called after any save operation (CREATE or UPDATE)"""
        await self.refresh_from_db()
    
    # Operation-specific signals (triggered based on detected operation)
    async def before_create(self, context: SignalContext):
        """Only triggered for CREATE operations"""
        self.created_at = datetime.now()
        self.uuid = str(uuid.uuid4())
    
    async def before_update(self, context: SignalContext):
        """Only triggered for UPDATE operations"""
        self.version += 1
    
    async def after_create(self, context: SignalContext):
        """After creation only"""
        await self.send_welcome_email()
        await self.create_default_profile()
    
    async def after_update(self, context: SignalContext):
        """After update only"""
        await self.notify_profile_changes()
    
    # Deletion signals
    async def before_delete(self, context: SignalContext):
        """Before deletion"""
        await self.log_deletion()
    
    async def after_delete(self, context: SignalContext):
        """After deletion"""
        await self.cleanup_related_data()
```

### Bulk Operation Signal Types
**Class-level signals for bulk operations affecting multiple records**
```python
class User(ObjectModel):
    @classmethod
    async def before_bulk_create(cls, context: SignalContext):
        """Before bulk creation of multiple records"""
        logger.info(f"Creating {context.affected_count} users")
        # Prepare bulk operation resources
    
    @classmethod
    async def before_bulk_update(cls, context: SignalContext):
        """Before bulk update of multiple records"""
        logger.info(f"Updating {context.affected_count} users")
        # Access update data through context.update_data
        if context.update_data:
            logger.info(f"Update fields: {list(context.update_data.keys())}")
    
    @classmethod
    async def before_bulk_delete(cls, context: SignalContext):
        """Before bulk deletion of multiple records"""
        logger.info(f"Deleting {context.affected_count} users")
        # Prepare cleanup operations
    
    @classmethod
    async def after_bulk_create(cls, context: SignalContext):
        """After bulk creation"""
        # Send batch notifications
        await cls.send_bulk_welcome_emails(context.affected_count)
    
    @classmethod
    async def after_bulk_update(cls, context: SignalContext):
        """After bulk update"""
        # Process bulk operation completion
        # Bulk operation completed successfully
    
    @classmethod
    async def after_bulk_delete(cls, context: SignalContext):
        """After bulk deletion"""
        # Cleanup related data
        await cls.cleanup_bulk_related_data()
```

## Smart SAVE Operation Signal Architecture

### Dual Signal Emission for save() Operations
**Automatic operation detection and dual signal emission**
```python
# For new instances (no primary key values)
user = User(username="new_user", email="new@example.com")
await user.save()
# Triggers: before_save → before_create → after_save → after_create

# For existing instances (has primary key values)
user.email = "updated@example.com"
await user.save()
# Triggers: before_save → before_update → after_save → after_update

# For detached instances (has primary key but not in session)
detached_user = User(id=1, username="detached", email="detached@example.com")
await detached_user.save()
# Triggers: before_save → before_update → after_save → after_update
```

**Implementation Details**:
```python
def _determine_save_operation(self_or_cls) -> Operation:
    """Determine whether SAVE is CREATE or UPDATE."""
    if hasattr(self_or_cls, "_has_primary_key_values"):
        return Operation.UPDATE if self_or_cls._has_primary_key_values() else Operation.CREATE
    return Operation.CREATE

@emit_signals(Operation.SAVE)
async def save(self, validate: bool = True, cascade: bool | None = None, session=None):
    """Save with automatic operation detection.
    
    emit_signals decorator:
    1. Calls _determine_save_operation() to detect CREATE or UPDATE
    2. Sets context.actual_operation to detected operation
    3. Emits before_save signal
    4. Emits before_create or before_update signal
    5. Executes save operation
    6. Emits after_save signal
    7. Emits after_create or after_update signal
    """
    pass
```

### SignalContext Information Architecture
**Comprehensive context information for signal handlers**
```python
from sqlobjects.signals import SignalContext, Operation

@dataclass
class SignalContext:
    """Context object for signal handlers."""
    operation: Operation                    # SAVE, CREATE, UPDATE, DELETE
    session: AsyncSession                   # Database session
    model_class: Any                        # Model class
    instance: Any | None = None             # Model instance (single operations)
    affected_count: int | None = None       # Row count (bulk operations)
    update_data: dict[str, Any] | None = None  # Update data (bulk updates)
    actual_operation: Operation | None = None  # Detected operation for SAVE
    
    @property
    def is_bulk(self) -> bool:
        """Check if this is a bulk operation."""
        return self.instance is None
    
    @property
    def is_single(self) -> bool:
        """Check if this is a single-instance operation."""
        return self.instance is not None

# Usage in signal handlers
async def before_save(self, context: SignalContext):
    # Operation information
    print(f"Operation: {context.operation}")           # SAVE, CREATE, UPDATE, DELETE
    print(f"Actual operation: {context.actual_operation}")  # CREATE or UPDATE for SAVE
    
    # Session and model information
    print(f"Session: {context.session}")               # Database session
    print(f"Model class: {context.model_class}")       # Model class
    print(f"Instance: {context.instance}")             # Model instance
    
    # Bulk operation information
    print(f"Is bulk: {context.is_bulk}")               # True for bulk operations
    print(f"Affected count: {context.affected_count}") # Row count for bulk operations
    print(f"Update data: {context.update_data}")       # Data for bulk updates
```

## Signal Naming Convention System

### Instance Signal Naming Rules
```python
# Single record operations - instance methods
async def before_save(self, context):     # Universal save (CREATE or UPDATE)
async def after_save(self, context):      # Universal save (CREATE or UPDATE)
async def before_create(self, context):   # CREATE operations only
async def after_create(self, context):    # CREATE operations only
async def before_update(self, context):   # UPDATE operations only
async def after_update(self, context):    # UPDATE operations only
async def before_delete(self, context):   # DELETE operations
async def after_delete(self, context):    # DELETE operations
```

### Bulk Signal Naming Rules
```python
# Bulk operations - class methods
@classmethod
async def before_bulk_save(cls, context):     # Bulk SAVE
@classmethod
async def after_bulk_save(cls, context):      # Bulk SAVE
@classmethod
async def before_bulk_create(cls, context):   # Bulk CREATE
@classmethod
async def after_bulk_create(cls, context):    # Bulk CREATE
@classmethod
async def before_bulk_update(cls, context):   # Bulk UPDATE
@classmethod
async def after_bulk_update(cls, context):    # Bulk UPDATE
@classmethod
async def before_bulk_delete(cls, context):   # Bulk DELETE
@classmethod
async def after_bulk_delete(cls, context):    # Bulk DELETE
```

### Signal Handler Discovery
**Signals discovered by method name convention**
```python
async def _emit_signal(target, timing: str, context: SignalContext) -> None:
    """Emit signal by discovering handler methods.
    
    Discovery process:
    1. Determine if bulk operation from context.is_bulk
    2. Build signal name: f"{timing}_{bulk_prefix}{operation.value}"
    3. Use getattr() to find handler method
    4. Check if handler is callable
    5. Detect async vs sync using inspect.iscoroutinefunction()
    6. Call handler with context
    """
    is_bulk = context.is_bulk
    bulk_prefix = "bulk_" if is_bulk else ""
    
    # For SAVE operations, emit both SAVE and specific signals
    if context.operation == Operation.SAVE and context.actual_operation:
        # Emit SAVE signal
        save_signal_name = f"{timing}_{bulk_prefix}save"
        save_handler = getattr(target, save_signal_name, None)
        if save_handler and callable(save_handler):
            if inspect.iscoroutinefunction(save_handler):
                await save_handler(context)
            else:
                save_handler(context)
        
        # Emit specific CREATE/UPDATE signal
        specific_signal_name = f"{timing}_{bulk_prefix}{context.actual_operation.value}"
        specific_handler = getattr(target, specific_signal_name, None)
        if specific_handler and callable(specific_handler):
            if inspect.iscoroutinefunction(specific_handler):
                await specific_handler(context)
            else:
                specific_handler(context)
    else:
        # For non-SAVE operations, emit single signal
        signal_name = f"{timing}_{bulk_prefix}{context.operation.value}"
        handler = getattr(target, signal_name, None)
        if handler and callable(handler):
            if inspect.iscoroutinefunction(handler):
                await handler(context)
            else:
                handler(context)
```

### Signal Integration with Operations
**Automatic signal triggering for all database operations**
```python
# get_or_create triggers appropriate signals
user, created = await User.objects.get_or_create(
    username="signal_user",
    defaults={"email": "signal@example.com"}
)
# If created: before_save → before_create → after_save → after_create
# If found: no signals triggered

# update_or_create triggers appropriate signals
user, created = await User.objects.update_or_create(
    username="signal_user",
    defaults={"last_login": datetime.now()}
)
# If updated: before_save → before_update → after_save → after_update
# If created: before_save → before_create → after_save → after_create

# Bulk operations trigger bulk signals
await User.objects.bulk_create(user_data)
# Triggers: before_bulk_create → after_bulk_create

await User.objects.bulk_update(mappings, match_fields=["id"])
# Triggers: before_bulk_update → after_bulk_update
```

## Proxy Class Extension Rules

### DeferredFieldProxy Usage
- **Auto-creation**: Automatically create proxies through __getattribute__
- **Proxy management**: Proxy objects cached in StateManager
- **Error-friendly**: Provide clear error messages

```python
from sqlobjects.model import ObjectModel, DeferredFieldProxy

class User(ObjectModel):
    bio: Column[str] = StringColumn(deferred=True)

# 使用示例
user = await User.objects.defer("bio").get(User.id == 1)
assert isinstance(user.bio, DeferredFieldProxy)
bio_content = await user.bio.fetch()  # Lazy loading
```

### RelationFieldProxy Usage
- **Relationship loading**: Integrate with existing prefetch logic
- **Session management**: Automatically get correct database session
- **Caching strategy**: Work cooperatively with existing field caching mechanisms

```python
from sqlobjects.model import ObjectModel, RelationFieldProxy

class User(ObjectModel):
    posts = relationship("Post", back_populates="author")

# 使用示例
user = await User.objects.get(User.id == 1)
assert isinstance(user.posts, RelationFieldProxy)
posts = await user.posts.fetch()  # Lazy loading relationships
```

### Proxy Integration Architecture
```python
# Proxy objects integrated in FieldCacheMixin
class FieldCacheMixin:
    def __getattribute__(self, name: str):
        # Smart dispatch to different types of proxies
        if name in deferred_fields:
            return DeferredFieldProxy(self, name)
        elif name in relationship_fields:
            return RelationFieldProxy(self, name)
        return super().__getattribute__(name)
```

## Extension System Architecture

### Exception Handling System
**Comprehensive exception hierarchy with English messages**
```python
# Base exception classes
class SQLObjectsError(Exception):
    """Base exception for all SQLObjects errors"""
    pass

class ValidationError(SQLObjectsError):
    """Raised when data validation fails"""
    def __init__(self, message: str, field: str = None, code: str = None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.code = code

class DatabaseError(SQLObjectsError):
    """Raised when database operations fail"""
    pass

class ConfigurationError(SQLObjectsError):
    """Raised when configuration is invalid"""
    pass

# Usage with English messages
raise ValidationError("Email address is required", field="email", code="required")
raise ValidationError("Username must be at least 3 characters long", field="username", code="min_length")
```

### Utility Function System
**Core utility functions for common operations**
```python
# Naming conversion utilities
def to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case"""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def pluralize(word: str) -> str:
    """Convert singular word to plural (Rails-style)"""
    # Implement Rails-style pluralization rules
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'sh', 'ch', 'x', 'z')):
        return word + 'es'
    else:
        return word + 's'

# Type conversion utilities
def convert_python_type_to_sqlalchemy(python_type: type) -> str:
    """Convert Python type to SQLAlchemy type string"""
    type_mapping = {
        str: "string",
        int: "integer",
        float: "float",
        bool: "boolean",
        datetime: "datetime",
        date: "date",
        time: "time",
        dict: "json",
        list: "json",
    }
    return type_mapping.get(python_type, "string")
```

### Configuration System Architecture
**Separation of model configuration and system configuration**
```python
# ModelConfig for individual model configuration
class ModelConfig:
    def __init__(self, config_dict: dict):
        self.table_name = config_dict.get("table_name")
        self.ordering = config_dict.get("ordering", [])
        self.indexes = config_dict.get("indexes", [])
        self.constraints = config_dict.get("constraints", [])
        self.verbose_name = config_dict.get("verbose_name")
        self.verbose_name_plural = config_dict.get("verbose_name_plural")

# ConfigManager for system-wide configuration
class ConfigManager:
    def __init__(self):
        self.default_string_length = 255
        self.auto_create_tables = True
        self.validate_on_save = True
        self.signal_enabled = True
    
    def update_from_dict(self, config_dict: dict):
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

# Global configuration instance
config = ConfigManager()
```

## Extension Development Rules

### New Signal Type Addition Process
1. **Signal Definition**: Define signal name and triggering conditions
2. **Context Design**: Determine what information should be in SignalContext
3. **Integration Points**: Identify where signals should be triggered
4. **Handler Registration**: Implement automatic handler discovery
5. **Testing**: Comprehensive tests for signal triggering and handling
6. **Documentation**: Update signal documentation with examples

### Custom Validator Development
```python
# Validator interface implementation
def custom_validator(value, **kwargs):
    """Custom validator following standard interface"""
    if not meets_criteria(value):
        raise ValidationError("Custom validation failed", code="custom_error")
    return value

# Pattern validator example
class CustomPatternValidator:
    def __init__(self, pattern: str, message: str = None):
        self.pattern = pattern
        self.message = message or f"Value must match pattern: {pattern}"
    
    def __call__(self, value: str) -> str:
        import re
        if not re.match(self.pattern, value):
            raise ValidationError(self.message, code="pattern_mismatch")
        return value

# Range validator example
class CustomRangeValidator:
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value
    
    def __call__(self, value: int) -> int:
        if value < self.min_value or value > self.max_value:
            raise ValidationError(
                f"Value must be between {self.min_value} and {self.max_value}",
                code="out_of_range"
            )
        return value
```

### Error Handling Integration
**Consistent error handling across all extension points**
```python
# Error message internationalization support
class ErrorMessage:
    def __init__(self, message: str, code: str, params: dict = None):
        self.message = message
        self.code = code
        self.params = params or {}
    
    def __str__(self) -> str:
        return self.message.format(**self.params)

# Usage in validators
def validate_length(min_length: int, max_length: int):
    def validator(value: str) -> str:
        if len(value) < min_length:
            raise ValidationError(
                ErrorMessage(
                    "Value must be at least {min_length} characters long",
                    "min_length",
                    {"min_length": min_length, "actual_length": len(value)}
                )
            )
        return value
    return validator
```

## Performance and Quality Guidelines

### Signal Performance Optimization
```python
# Efficient signal handling
from sqlobjects.model import ObjectModel
from sqlobjects.signals import SignalContext
import asyncio

class User(ObjectModel):
    async def after_create(self, context: SignalContext):
        # Group related operations
        await asyncio.gather(
            self.send_welcome_email(),
            self.create_default_preferences(),
            self.log_user_creation()
        )
    
    async def before_save(self, context: SignalContext):
        # Critical operations only - keep fast
        self.updated_at = datetime.now()
        
        # Non-critical operations in background
        if not context.is_bulk_operation:
            asyncio.create_task(self.update_search_index())
```

### Extension Error Handling Best Practices
```python
# Graceful error handling in extensions
from sqlobjects.model import ObjectModel
from sqlobjects.signals import SignalContext
from sqlobjects.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class User(ObjectModel):
    async def after_create(self, context: SignalContext):
        try:
            # Non-critical operations
            await self.send_welcome_email()
            await self.create_default_preferences()
        except Exception as e:
            # Log but don't fail the transaction
            logger.error(f"Post-creation tasks failed for user {self.id}: {e}")
    
    async def before_save(self, context: SignalContext):
        # Critical validation - let exceptions bubble up
        if not self.email:
            raise ValidationError("Email is required")
        
        # Business rule validation
        if self.is_admin and self.age < 21:
            raise ValidationError("Admin users must be at least 21 years old")
```

### Extension Testing Requirements
```python
# Signal testing patterns
from sqlobjects.model import ObjectModel
from sqlobjects.signals import Operation
from unittest.mock import patch
import pytest

class User(ObjectModel):
    username: Column[str] = StringColumn(length=50)
    email: Column[str] = StringColumn(length=100)

class TestUserSignals:
    async def test_before_save_signal(self):
        user = User(username="test", email="test@example.com")
        
        # Mock signal handler
        with patch.object(user, 'before_save') as mock_signal:
            await user.save()
            mock_signal.assert_called_once()
    
    async def test_signal_context_information(self):
        user = User(username="test", email="test@example.com")
        
        async def check_context(context):
            assert context.operation == Operation.SAVE
            assert context.actual_operation == Operation.CREATE
            assert context.instance == user
        
        user.before_save = check_context
        await user.save()

    async def test_proxy_integration(self):
        # Test proxy system integration
        user = await User.objects.defer("bio").get(User.id == 1)
        assert hasattr(user, '_state_manager')
        proxy_cache = user._state_manager.get("proxy_cache", {})
        assert isinstance(proxy_cache, dict)
```