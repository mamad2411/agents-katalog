# SQLObjects Testing Principles

## Testing Philosophy

Focus on testing **behavior and outcomes** rather than implementation details. Tests should verify that the system works correctly from a user perspective, not how it achieves those results internally.

## What to Test

### ✅ Test Behaviors and Results

```python
def test_constructor_accepts_appropriate_fields():
    """Test that constructor works with user-provided fields"""
    user = User(name="John", email="john@example.com")
    assert user.name == "John"
    assert user.email == "john@example.com"

def test_object_creation_produces_clean_state():
    """Test that new objects don't have dirty field markers"""
    user = User.from_dict({"name": "Jane", "email": "jane@example.com"})
    # Test behavior: object should not be marked as having changes after creation
    assert not user._has_changes()

async def test_save_operation_detection():
    """Test that save() correctly detects CREATE vs UPDATE"""
    # New object should trigger CREATE operation
    user = User(name="New User")
    # Test behavior: save() on new object performs INSERT
    await user.save()
    assert user.id is not None  # Should have ID after creation
    
    # Existing object should trigger UPDATE operation
    original_id = user.id
    user.name = "Updated User"
    await user.save()
    # Test behavior: save() on existing object performs UPDATE
    assert user.id == original_id  # ID should remain the same

def test_bulk_operations_performance():
    """Test that bulk operations are significantly faster"""
    # Measure and compare performance, not implementation
    individual_time = await measure_individual_creates(100)
    bulk_time = await measure_bulk_create(100)
    assert bulk_time < individual_time / 5  # At least 5x faster

def test_cache_improves_performance():
    """Test that caching provides performance benefit"""
    # First query (cache miss)
    start = time.time()
    await User.objects.filter(User.is_active == True).all()
    first_time = time.time() - start
    
    # Second query (cache hit)
    start = time.time()
    await User.objects.filter(User.is_active == True).all()
    second_time = time.time() - start
    
    assert second_time < first_time / 2  # Significantly faster
```

### ❌ Avoid Testing Implementation Details

```python
# ❌ Don't test specific parameter values
def test_init_parameter_values():
    field = column(type="integer", primary_key=True)
    assert field.column.info["_codegen"]["init"] is False  # Implementation detail

# ❌ Don't test specific method calls
def test_objects_manager_uses_from_dict():
    with patch.object(User, 'from_dict') as mock_from_dict:
        await User.objects.create(name="test")
        mock_from_dict.assert_called_once()  # Implementation detail

# ❌ Don't test specific cache format
def test_cache_statistics_format():
    stats = User.objects.get_cache_stats()
    assert stats == {"hits": 1, "misses": 0, "hit_rate": 1.0}  # Specific format

# ❌ Don't test specific batch sizes
def test_bulk_create_batch_size():
    await User.objects.bulk_create(data, batch_size=1000)
    # Don't verify internal batching implementation
```

## Testing Layers

### Unit Tests - Component Behavior
Test individual components in isolation, focusing on their public interface and behavior.

```python
class TestFieldSystem:
    def test_field_accepts_valid_parameters(self):
        """Test field creation with valid parameters"""
        field = StringColumn(length=100, nullable=False)
        assert field.column.type.length == 100
        assert not field.column.nullable
    
    def test_field_validation_triggers_on_invalid_data(self):
        """Test that field validators are executed"""
        def validate_email(value):
            if "@" not in value:
                raise ValueError("Invalid email")
            return value
        
        field = column(type="string", validators=[validate_email])
        
        # Should accept valid email
        assert field.validate("test@example.com") == "test@example.com"
        
        # Should reject invalid email
        with pytest.raises(ValueError):
            field.validate("invalid-email")

class TestModelBehavior:
    def test_model_tracks_field_changes(self):
        """Test that field modifications are tracked"""
        user = User(name="Original")
        # Clear initial state after creation
        user._clear_changes()
        
        # Modify field
        user.name = "Modified"
        
        # Behavior: field change is tracked
        assert user._has_changes()
        changed_fields = user._get_changed_fields()
        assert "name" in changed_fields
    
    def test_model_validation_prevents_invalid_data(self):
        """Test that validation prevents saving invalid data"""
        user = User(name="", email="invalid")  # Invalid data
        
        with pytest.raises(ValidationError):
            user.validate()
```

### Integration Tests - System Behavior
Test how components work together, focusing on end-to-end workflows.

```python
class TestCRUDWorkflows:
    async def test_complete_crud_lifecycle(self, test_db):
        """Test complete CRUD operations work correctly"""
        async with ctx_session() as session:
            # Create
            user = await User.objects.using(session).create(
                name="Test User", 
                email="test@example.com"
            )
            assert user.id is not None
            
            # Read
            retrieved = await User.objects.using(session).get(User.id == user.id)
            assert retrieved.name == "Test User"
            
            # Update
            retrieved.name = "Updated User"
            await retrieved.save()
            
            # Verify update
            updated = await User.objects.using(session).get(User.id == user.id)
            assert updated.name == "Updated User"
            
            # Delete
            await updated.delete()
            
            # Verify deletion
            with pytest.raises(DoesNotExist):
                await User.objects.using(session).get(User.id == user.id)

class TestRelationshipBehavior:
    async def test_relationship_loading_prevents_n_plus_one(self, test_db):
        """Test that relationship loading strategies work correctly"""
        async with ctx_session() as session:
            # Create test data
            users = await User.objects.using(session).bulk_create([
                {"name": f"User{i}", "email": f"user{i}@example.com"} 
                for i in range(10)
            ])
            
            # Test select_related prevents N+1 queries
            with query_counter() as counter:
                posts = await Post.objects.using(session).select_related("author").all()
                for post in posts:
                    _ = post.author.name  # Should not trigger additional queries
            
            # Should use only 1 query (JOIN), not N+1 queries
            assert counter.count == 1
```

### Performance Tests - Efficiency Verification
Test that performance requirements are met, focusing on measurable outcomes.

```python
class TestPerformanceRequirements:
    async def test_bulk_operations_meet_performance_targets(self, test_db):
        """Test bulk operations achieve required performance"""
        data = [{"name": f"User{i}", "email": f"user{i}@example.com"} for i in range(1000)]
        
        start = time.time()
        await User.objects.bulk_create(data)
        duration = time.time() - start
        
        # Should complete within reasonable time (adjust based on requirements)
        assert duration < 5.0  # Less than 5 seconds for 1000 records
    
    async def test_iterator_handles_large_datasets(self, test_db):
        """Test iterator can process large datasets without memory issues"""
        # Create large dataset
        await User.objects.bulk_create([
            {"name": f"User{i}", "email": f"user{i}@example.com"} 
            for i in range(10000)
        ])
        
        # Process with iterator
        count = 0
        memory_before = get_memory_usage()
        
        async for user in User.objects.iterator(chunk_size=100):
            count += 1
        
        memory_after = get_memory_usage()
        
        assert count == 10000
        # Memory usage should not grow significantly
        assert memory_after - memory_before < 50  # Less than 50MB growth
```

## Test Organization

### Test Structure
```
tests/
├── unit/                    # Fast, isolated component tests
│   ├── test_fields.py       # Field system behavior
│   ├── test_model.py        # Model behavior
│   ├── test_queries.py      # Query building behavior
│   └── test_validation.py   # Validation behavior
├── integration/             # Component interaction tests
│   ├── test_crud.py         # CRUD workflows
│   ├── test_relationships.py # Relationship behavior
│   └── test_signals.py      # Signal system behavior
└── performance/             # Performance requirement tests
    ├── test_bulk_ops.py     # Bulk operation performance
    └── test_memory.py       # Memory usage tests
```

### Test Naming Conventions
- `test_[component]_[behavior]_[condition]`
- Focus on what the test verifies, not how it's implemented
- Use descriptive names that explain the expected behavior

```python
# ✅ Good test names
def test_user_creation_requires_valid_email():
def test_bulk_update_modifies_only_specified_fields():
def test_cache_bypass_returns_fresh_data():
def test_relationship_loading_prevents_duplicate_queries():

# ❌ Poor test names  
def test_init_parameter_processing():
def test_from_dict_method_call():
def test_cache_statistics_format():
def test_batch_size_configuration():
```

### Fixture Design
Create fixtures that represent realistic usage scenarios, not implementation details.

```python
@pytest.fixture
async def sample_users(test_db):
    """Create sample users for testing"""
    return await User.objects.bulk_create([
        {"name": "Alice", "email": "alice@example.com", "age": 25},
        {"name": "Bob", "email": "bob@example.com", "age": 30},
        {"name": "Charlie", "email": "charlie@example.com", "age": 35},
    ])

@pytest.fixture
async def user_with_posts(test_db):
    """Create user with associated posts for relationship testing"""
    user = await User.objects.create(name="Author", email="author@example.com")
    posts = await Post.objects.bulk_create([
        {"title": f"Post {i}", "content": f"Content {i}", "author_id": user.id}
        for i in range(5)
    ])
    return user, posts
```

## Assertion Guidelines

### Focus on Observable Outcomes
```python
# ✅ Test observable behavior
assert user.name == "Expected Name"
assert len(posts) == 5
assert user._has_changes()
assert response_time < 1.0

# ❌ Don't test internal state
assert user._state_manager.get("dirty_fields") == {"name"}
assert field.column.info["_codegen"]["init"] is False
```

### Use Meaningful Error Messages
```python
# ✅ Descriptive assertions
assert user.is_valid(), f"User validation failed: {user.get_validation_errors()}"
assert len(results) == expected_count, f"Expected {expected_count} results, got {len(results)}"

# ❌ Generic assertions
assert user.is_valid()
assert len(results) == expected_count
```

## Database Testing Patterns

### Test Database Setup
```python
@pytest.fixture(scope="session")
async def test_db():
    """Setup test database for the entire test session"""
    # Use in-memory SQLite for fast tests
    await init_db("sqlite:///:memory:", create_tables=True)
    yield
    await close_db()

@pytest.fixture
async def clean_db(test_db):
    """Clean database state between tests"""
    async with ctx_session() as session:
        # Clean all tables
        for table in reversed(metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()
```

### Transaction Testing
```python
class TestTransactionBehavior:
    async def test_transaction_rollback_on_error(self, clean_db):
        """Test that transactions rollback properly on errors"""
        async with ctx_session() as session:
            # Create initial data
            user = await User.objects.using(session).create(
                name="Test User", email="test@example.com"
            )
            
            # Attempt operation that should fail
            with pytest.raises(ValidationError):
                async with ctx_session() as inner_session:
                    user.email = "invalid-email"  # Invalid email
                    await user.using(inner_session).save()
            
            # Verify rollback - original data should be unchanged
            fresh_user = await User.objects.using(session).get(User.id == user.id)
            assert fresh_user.email == "test@example.com"
    
    async def test_concurrent_operations_isolation(self, clean_db):
        """Test that concurrent operations are properly isolated"""
        # Create test data
        user = await User.objects.create(name="Concurrent User", balance=100)
        
        async def withdraw_money(amount: int):
            async with ctx_session() as session:
                user_copy = await User.objects.using(session).get(User.id == user.id)
                if user_copy.balance >= amount:
                    user_copy.balance -= amount
                    await user_copy.save()
                    return True
                return False
        
        # Simulate concurrent withdrawals
        results = await asyncio.gather(
            withdraw_money(60),
            withdraw_money(60),
            return_exceptions=True
        )
        
        # Only one withdrawal should succeed due to isolation
        successful_withdrawals = sum(1 for r in results if r is True)
        assert successful_withdrawals == 1
        
        # Final balance should be correct
        final_user = await User.objects.get(User.id == user.id)
        assert final_user.balance == 40
```

## Performance Testing Guidelines

### Memory Usage Testing
```python
import psutil
import os

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

class TestMemoryEfficiency:
    async def test_iterator_memory_efficiency(self, test_db):
        """Test that iterator doesn't load all data into memory"""
        # Create large dataset
        large_data = [
            {"name": f"User{i}", "email": f"user{i}@example.com"}
            for i in range(10000)
        ]
        await User.objects.bulk_create(large_data)
        
        memory_before = get_memory_usage()
        processed_count = 0
        
        # Process with iterator
        async for user in User.objects.iterator(chunk_size=100):
            processed_count += 1
            # Simulate processing
            _ = user.name.upper()
        
        memory_after = get_memory_usage()
        memory_growth = memory_after - memory_before
        
        assert processed_count == 10000
        # Memory growth should be minimal (less than 50MB)
        assert memory_growth < 50, f"Memory grew by {memory_growth:.2f}MB"
```

### Query Performance Testing
```python
import time
from contextlib import asynccontextmanager

@asynccontextmanager
async def query_timer():
    """Context manager to measure query execution time"""
    start_time = time.perf_counter()
    yield
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return execution_time

class TestQueryPerformance:
    async def test_select_related_performance(self, test_db):
        """Test that select_related improves query performance"""
        # Create test data
        users = await User.objects.bulk_create([
            {"name": f"User{i}", "email": f"user{i}@example.com"}
            for i in range(100)
        ])
        
        posts = await Post.objects.bulk_create([
            {"title": f"Post{i}", "content": f"Content{i}", "author_id": users[i % len(users)].id}
            for i in range(1000)
        ])
        
        # Test without select_related (N+1 queries)
        start_time = time.perf_counter()
        posts_without_select = await Post.objects.all()
        for post in posts_without_select[:10]:  # Only test first 10 to avoid too many queries
            _ = await post.author  # This triggers additional queries
        time_without_select = time.perf_counter() - start_time
        
        # Test with select_related (single JOIN query)
        start_time = time.perf_counter()
        posts_with_select = await Post.objects.select_related("author").all()
        for post in posts_with_select[:10]:
            _ = post.author  # This should not trigger additional queries
        time_with_select = time.perf_counter() - start_time
        
        # select_related should be significantly faster
        assert time_with_select < time_without_select / 2, \
            f"select_related ({time_with_select:.3f}s) should be much faster than N+1 queries ({time_without_select:.3f}s)"
```

## Error Testing Patterns

### Validation Error Testing
```python
class TestValidationErrors:
    def test_validation_error_messages_are_helpful(self):
        """Test that validation errors provide clear, actionable messages"""
        user = User(name="", email="invalid-email")
        
        with pytest.raises(ValidationError) as exc_info:
            user.validate()
        
        error = exc_info.value
        # Error message should be in English and descriptive
        assert "name" in str(error).lower()
        assert "required" in str(error).lower() or "empty" in str(error).lower()
    
    async def test_database_constraint_errors_are_handled(self, test_db):
        """Test that database constraint violations are properly handled"""
        # Create user with unique email
        await User.objects.create(name="First User", email="unique@example.com")
        
        # Attempt to create another user with same email
        with pytest.raises(DatabaseError) as exc_info:
            await User.objects.create(name="Second User", email="unique@example.com")
        
        # Error should be informative
        error_message = str(exc_info.value)
        assert "unique" in error_message.lower() or "duplicate" in error_message.lower()
```

This testing approach ensures that tests remain valuable as the implementation evolves, focusing on the contract and behavior that users depend on rather than internal implementation details.on
# ✅ Good test names
def test_user_creation_requires_valid_email():
def test_bulk_update_modifies_only_specified_fields():
def test_cache_bypass_returns_fresh_data():
def test_relationship_loading_prevents_duplicate_queries():

# ❌ Poor test names  
def test_init_parameter_processing():
def test_from_dict_method_call():
def test_cache_statistics_format():
def test_batch_size_configuration():
```

### Fixture Design
Create fixtures that represent realistic usage scenarios, not implementation details.

```python
@pytest.fixture
async def sample_users(test_db):
    """Create sample users for testing"""
    return await User.objects.bulk_create([
        {"name": "Alice", "email": "alice@example.com", "age": 25},
        {"name": "Bob", "email": "bob@example.com", "age": 30},
        {"name": "Charlie", "email": "charlie@example.com", "age": 35},
    ])

@pytest.fixture
async def user_with_posts(test_db):
    """Create user with associated posts for relationship testing"""
    user = await User.objects.create(name="Author", email="author@example.com")
    posts = await Post.objects.bulk_create([
        {"title": f"Post {i}", "content": f"Content {i}", "author_id": user.id}
        for i in range(5)
    ])
    return user, posts
```

## Assertion Guidelines

### Focus on Observable Outcomes
```python
# ✅ Test observable behavior
assert user.name == "Expected Name"
assert len(posts) == 5
assert user._has_changes()
assert response_time < 1.0

# ❌ Don't test internal state
assert user._state_manager.get("dirty_fields") == {"name"}
assert field.column.info["_codegen"]["init"] is False
```

### Use Meaningful Error Messages
```python
# ✅ Descriptive assertions
assert user.is_valid(), f"User validation failed: {user.get_validation_errors()}"
assert len(results) == expected_count, f"Expected {expected_count} results, got {len(results)}"

# ❌ Generic assertions
assert user.is_valid()
assert len(results) == expected_count
```

This testing approach ensures that tests remain valuable as the implementation evolves, focusing on the contract and behavior that users depend on rather than internal implementation details.