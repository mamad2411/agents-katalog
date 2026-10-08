# Testing & Validation: Unit, Integration, and Property-Based Testing

**Author**: Shuvam Banerji Seal  
**Category**: Foundational Skills  
**Difficulty**: Intermediate  
**Last Updated**: April 2026

## Problem Statement

Comprehensive testing prevents bugs, enables refactoring, and documents system behavior. This skill covers:
- **Unit Testing**: Isolated component testing with pytest
- **Mocking**: Isolation of dependencies with unittest.mock
- **Integration Testing**: Multi-component interaction testing
- **Property-Based Testing**: Hypothesis framework for automated test generation
- **Mutation Testing**: Verify test quality and coverage
- **Test Coverage**: Metrics and strategies
- **CI/CD Integration**: Automated test execution

---

## Theoretical Foundations

### 1. Testing Pyramid

```
        /\
       /E2E\         End-to-End Tests (1-10%)
      /-----\        • Slow, expensive
     /  API  \       • Real infrastructure
    /--------\       • High-level workflows
   /Integration\     Integration Tests (10-30%)
  /-----------\      • Multiple components
 / Unit Tests \     Unit Tests (60-80%)
/_____________\     • Fast, cheap, isolated
```

**Formula for Optimal Test Distribution**:
```
Total Cost = 10*E2E_tests + 5*Integration_tests + 1*Unit_tests
Goal: Minimize cost while maximizing coverage
```

### 2. Coverage Metrics

```
Code Coverage = (Executed Lines / Total Lines) × 100%

Target Guidelines:
- Critical paths: >95% coverage
- Business logic: >80% coverage
- Utilities: >70% coverage
- Infrastructure: >50% coverage (diminishing returns)
```

### 3. Property-Based Testing

```
Traditional Testing: Test(inputs) → Assert(outputs)
Property-Based: Hypothesis(generates inputs) → Verify(property holds)

Properties are invariants that should ALWAYS be true:
P(f(x)) ≡ True for all x in domain
```

---

## Comprehensive Code Examples

### Example 1: Unit Testing with pytest

```python
import pytest
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class User:
    """User model for testing."""
    id: int
    name: str
    email: str
    is_active: bool = True


class UserRepository:
    """Simulated user data store."""
    
    def __init__(self):
        self.users: dict[int, User] = {}
        self.next_id = 1
    
    def create(self, name: str, email: str) -> User:
        """Create new user."""
        if not name or not email:
            raise ValueError("Name and email required")
        
        user = User(id=self.next_id, name=name, email=email)
        self.users[self.next_id] = user
        self.next_id += 1
        return user
    
    def get(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)
    
    def update(self, user_id: int, **kwargs) -> User:
        """Update user attributes."""
        user = self.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False


# Test fixtures
@pytest.fixture
def repository():
    """Provide fresh repository for each test."""
    return UserRepository()


@pytest.fixture
def sample_user(repository):
    """Create sample user."""
    return repository.create("John Doe", "john@example.com")


# Test cases
class TestUserRepository:
    """Test suite for UserRepository."""
    
    def test_create_user_success(self, repository):
        """Test successful user creation."""
        user = repository.create("Alice", "alice@example.com")
        
        assert user.id == 1
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.is_active is True
    
    def test_create_user_missing_name(self, repository):
        """Test validation of missing name."""
        with pytest.raises(ValueError, match="Name and email required"):
            repository.create("", "alice@example.com")
    
    def test_create_user_missing_email(self, repository):
        """Test validation of missing email."""
        with pytest.raises(ValueError):
            repository.create("Alice", "")
    
    def test_get_existing_user(self, repository, sample_user):
        """Test retrieving existing user."""
        user = repository.get(sample_user.id)
        
        assert user is not None
        assert user.id == sample_user.id
        assert user.name == "John Doe"
    
    def test_get_nonexistent_user(self, repository):
        """Test retrieving nonexistent user returns None."""
        user = repository.get(999)
        assert user is None
    
    def test_update_user(self, repository, sample_user):
        """Test updating user attributes."""
        updated = repository.update(
            sample_user.id,
            name="Jane Doe",
            is_active=False
        )
        
        assert updated.name == "Jane Doe"
        assert updated.is_active is False
        assert updated.email == "john@example.com"  # Unchanged
    
    def test_delete_user(self, repository, sample_user):
        """Test user deletion."""
        success = repository.delete(sample_user.id)
        
        assert success is True
        assert repository.get(sample_user.id) is None
    
    def test_delete_nonexistent_user(self, repository):
        """Test deleting nonexistent user returns False."""
        success = repository.delete(999)
        assert success is False
    
    @pytest.mark.parametrize("name,email", [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com"),
        ("Charlie", "charlie@example.com"),
    ])
    def test_create_multiple_users(self, repository, name, email):
        """Test creating multiple users with different data."""
        user = repository.create(name, email)
        
        assert user.name == name
        assert user.email == email


# Coverage report
# Run with: pytest --cov=. --cov-report=html
```

### Example 2: Mocking with unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock, call
from typing import Optional
import requests

class ExternalAPIClient:
    """Client for external API."""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
    
    def get_user(self, user_id: int) -> dict:
        """Fetch user from external API."""
        url = f"{self.base_url}/users/{user_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def create_user(self, name: str, email: str) -> dict:
        """Create user via API."""
        url = f"{self.base_url}/users"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"name": name, "email": email}
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()


class TestAPIClient:
    """Test suite using mocks."""
    
    @patch("requests.get")
    def test_get_user_success(self, mock_get):
        """Test successful user fetch."""
        # Setup mock
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 1,
            "name": "John",
            "email": "john@example.com"
        }
        mock_get.return_value = mock_response
        
        # Execute
        client = ExternalAPIClient("https://api.example.com", "token123")
        user = client.get_user(1)
        
        # Assert
        assert user["name"] == "John"
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "users/1" in args[0]
        assert "Authorization" in kwargs["headers"]
    
    @patch("requests.get")
    def test_get_user_api_error(self, mock_get):
        """Test API error handling."""
        # Setup mock to raise exception
        mock_get.side_effect = requests.HTTPError("404 Not Found")
        
        # Execute and assert
        client = ExternalAPIClient("https://api.example.com", "token123")
        with pytest.raises(requests.HTTPError):
            client.get_user(999)
    
    @patch("requests.post")
    def test_create_user_success(self, mock_post):
        """Test user creation."""
        # Setup
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 2,
            "name": "Alice",
            "email": "alice@example.com"
        }
        mock_post.return_value = mock_response
        
        # Execute
        client = ExternalAPIClient("https://api.example.com", "token123")
        user = client.create_user("Alice", "alice@example.com")
        
        # Assert
        assert user["id"] == 2
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        assert kwargs["json"]["name"] == "Alice"


# Using MagicMock for complex interactions
class TestComplexMocking:
    """Test complex mocking scenarios."""
    
    def test_chained_method_calls(self):
        """Test mocking chained method calls."""
        mock_client = MagicMock()
        mock_client.users.get.return_value = {"id": 1, "name": "John"}
        
        result = mock_client.users.get()
        
        assert result["name"] == "John"
        mock_client.users.get.assert_called_once()
    
    def test_multiple_calls_different_returns(self):
        """Test mock with different return values per call."""
        mock_api = Mock()
        mock_api.fetch.side_effect = [
            {"data": "first"},
            {"data": "second"},
            Exception("Service down")
        ]
        
        # First call
        result1 = mock_api.fetch()
        assert result1["data"] == "first"
        
        # Second call
        result2 = mock_api.fetch()
        assert result2["data"] == "second"
        
        # Third call raises
        with pytest.raises(Exception):
            mock_api.fetch()
```

### Example 3: Property-Based Testing with Hypothesis

```python
from hypothesis import given, strategies as st, assume
from hypothesis import settings, Verbosity
import math

class MathOperations:
    """Mathematical operations for property-based testing."""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Addition operation."""
        return a + b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiplication operation."""
        return a * b
    
    @staticmethod
    def sqrt_safe(n: float) -> float:
        """Safe square root (only for non-negative)."""
        if n < 0:
            raise ValueError("Cannot sqrt negative number")
        return math.sqrt(n)


class TestMathOperations:
    """Property-based tests for math operations."""
    
    @given(st.floats(allow_nan=False, allow_infinity=False))
    def test_addition_commutative(self, x):
        """Property: a + b = b + a (commutative)."""
        y = st.floats().example()
        
        result1 = MathOperations.add(x, y)
        result2 = MathOperations.add(y, x)
        
        assert result1 == result2
    
    @given(st.floats(allow_nan=False, allow_infinity=False))
    def test_addition_associative(self, x):
        """Property: (a + b) + c = a + (b + c) (associative)."""
        y = st.floats().example()
        z = st.floats().example()
        
        result1 = MathOperations.add(MathOperations.add(x, y), z)
        result2 = MathOperations.add(x, MathOperations.add(y, z))
        
        # Use approximate equality for floating point
        assert abs(result1 - result2) < 1e-10
    
    @given(st.floats(allow_nan=False, allow_infinity=False))
    def test_multiplication_identity(self, x):
        """Property: a * 1 = a (identity element)."""
        result = MathOperations.multiply(x, 1.0)
        
        assert abs(result - x) < 1e-10
    
    @given(
        st.floats(min_value=0, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, allow_nan=False, allow_infinity=False)
    )
    def test_sqrt_properties(self, x, y):
        """Property: sqrt(x) >= 0 and sqrt(x)^2 ≈ x."""
        result = MathOperations.sqrt_safe(x)
        
        # Non-negative
        assert result >= 0
        
        # Inverse property
        assert abs(result * result - x) < 1e-10
    
    @given(st.lists(st.integers()))
    def test_list_length_preserved(self, lst):
        """Property: reverse of reverse equals original."""
        reversed_list = list(reversed(lst))
        double_reversed = list(reversed(reversed_list))
        
        assert len(double_reversed) == len(lst)
        assert double_reversed == lst
    
    @given(
        st.lists(st.integers(), min_size=1),
        st.sampled_from([min, max, sum])
    )
    def test_aggregation_functions(self, lst, func):
        """Property: aggregation functions handle non-empty lists."""
        result = func(lst)
        
        # Result should be valid for non-empty list
        if func == min:
            assert result <= max(lst)
        elif func == max:
            assert result >= min(lst)
        elif func == sum:
            assert result >= min(lst) if lst else 0


# Settings for hypothesis
class TestWithCustomSettings:
    """Tests with custom hypothesis settings."""
    
    @settings(
        max_examples=1000,
        verbosity=Verbosity.verbose
    )
    @given(st.integers(min_value=0, max_value=100))
    def test_with_more_examples(self, n):
        """Test with 1000 examples for thorough testing."""
        result = n * 2
        assert result % 2 == 0


# Stateful testing
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize_state

class TestListStateful(RuleBasedStateMachine):
    """Stateful property-based testing for list operations."""
    
    def setup_example(self):
        """Setup before each example."""
        self.lst = []
    
    @initialize_state
    def initialize(self):
        """Initialize state machine."""
        self.lst = []
    
    @rule(value=st.integers())
    def add_item(self, value):
        """Add item to list."""
        self.lst.append(value)
    
    @rule()
    def remove_item(self):
        """Remove last item if list not empty."""
        if self.lst:
            self.lst.pop()
    
    @rule()
    def verify_invariants(self):
        """Verify list invariants."""
        # Property: list length should match
        assert len(self.lst) >= 0


# Run stateful tests
TestListStateful().runTest()
```

### Example 4: Integration Testing

```python
import pytest
from contextlib import contextmanager
from typing import Iterator
import tempfile
import sqlite3
from pathlib import Path

# Simulated database
class Database:
    """Simple database wrapper for testing."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_schema()
    
    def _init_schema(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            """)
            conn.commit()
    
    def create_user(self, name: str, email: str) -> int:
        """Create user in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_user(self, user_id: int) -> dict:
        """Retrieve user from database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, name, email FROM users WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "email": row[2]}
            return {}


class UserService:
    """Service layer using database."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def register_user(self, name: str, email: str) -> dict:
        """Register new user."""
        user_id = self.db.create_user(name, email)
        return self.db.get_user(user_id)
    
    def get_user_profile(self, user_id: int) -> dict:
        """Get user profile."""
        return self.db.get_user(user_id)


# Integration test fixtures
@pytest.fixture
def temp_db() -> Iterator[str]:
    """Provide temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    
    yield db_path
    
    # Cleanup
    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def database(temp_db):
    """Provide database instance."""
    return Database(temp_db)


@pytest.fixture
def service(database):
    """Provide service instance."""
    return UserService(database)


class TestUserServiceIntegration:
    """Integration tests for user service with real database."""
    
    def test_user_registration_flow(self, service):
        """Test complete user registration flow."""
        # Register user
        user = service.register_user("Alice", "alice@example.com")
        
        # Verify registration
        assert user["id"] is not None
        assert user["name"] == "Alice"
        assert user["email"] == "alice@example.com"
    
    def test_user_retrieval_after_registration(self, service):
        """Test retrieving user after registration."""
        # Register
        registered = service.register_user("Bob", "bob@example.com")
        
        # Retrieve
        retrieved = service.get_user_profile(registered["id"])
        
        assert retrieved["name"] == "Bob"
        assert retrieved["email"] == "bob@example.com"
    
    def test_multiple_users(self, service):
        """Test handling multiple users."""
        users = []
        for i in range(5):
            user = service.register_user(f"User{i}", f"user{i}@example.com")
            users.append(user)
        
        # Verify all users
        for user in users:
            retrieved = service.get_user_profile(user["id"])
            assert retrieved["name"] == user["name"]
    
    def test_duplicate_email_constraint(self, service):
        """Test database constraint on duplicate emails."""
        # Register first user
        service.register_user("Alice", "alice@example.com")
        
        # Attempt to register with same email
        with pytest.raises(sqlite3.IntegrityError):
            service.register_user("Bob", "alice@example.com")
```

### Example 5: Test Coverage and Metrics

```python
import pytest
from coverage import Coverage
from typing import List

class Calculator:
    """Simple calculator for coverage demonstration."""
    
    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b
    
    @staticmethod
    def divide(a: int, b: int) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    
    @staticmethod
    def process_list(items: List[int]) -> dict:
        """Process list with multiple branches."""
        if not items:
            return {"status": "empty", "sum": 0}
        
        total = sum(items)
        average = total / len(items)
        
        if average > 10:
            return {"status": "high", "sum": total, "avg": average}
        elif average > 5:
            return {"status": "medium", "sum": total, "avg": average}
        else:
            return {"status": "low", "sum": total, "avg": average}


class TestCalculatorCoverage:
    """Test suite for calculator with full coverage."""
    
    def test_add_positive(self):
        """Test addition of positive numbers."""
        assert Calculator.add(2, 3) == 5
    
    def test_add_negative(self):
        """Test addition with negative numbers."""
        assert Calculator.add(-2, 3) == 1
    
    def test_divide_success(self):
        """Test successful division."""
        assert Calculator.divide(10, 2) == 5.0
    
    def test_divide_by_zero(self):
        """Test division by zero error."""
        with pytest.raises(ValueError, match="Division by zero"):
            Calculator.divide(10, 0)
    
    def test_process_empty_list(self):
        """Test processing empty list."""
        result = Calculator.process_list([])
        assert result["status"] == "empty"
    
    def test_process_high_average(self):
        """Test processing list with high average."""
        result = Calculator.process_list([15, 20, 10])
        assert result["status"] == "high"
    
    def test_process_medium_average(self):
        """Test processing list with medium average."""
        result = Calculator.process_list([4, 6, 8])
        assert result["status"] == "medium"
    
    def test_process_low_average(self):
        """Test processing list with low average."""
        result = Calculator.process_list([1, 2, 3])
        assert result["status"] == "low"


# Run coverage analysis
# pytest --cov=calculator --cov-report=html --cov-report=term
```

---

## Step-by-Step Implementation Guide

### 1. Setting Up pytest

**Step 1.1: Install pytest**
```bash
pip install pytest pytest-cov pytest-mock
```

**Step 1.2: Create test structure**
```
project/
├── src/
│   └── mymodule.py
└── tests/
    ├── __init__.py
    ├── conftest.py  (shared fixtures)
    └── test_mymodule.py
```

**Step 1.3: Run tests**
```bash
pytest                    # Run all tests
pytest tests/test_*.py   # Specific pattern
pytest -v                # Verbose output
pytest --cov             # Coverage report
```

### 2. Creating Test Fixtures

**Step 2.1: Function fixtures**
```python
@pytest.fixture
def resource():
    return create_resource()
```

**Step 2.2: Fixture scope**
```python
@pytest.fixture(scope="module")  # Reuse across tests
def expensive_resource():
    pass
```

**Step 2.3: Using fixtures**
```python
def test_something(resource):
    assert resource.operation() == expected
```

### 3. Property-Based Testing Setup

**Step 3.1: Install hypothesis**
```bash
pip install hypothesis
```

**Step 3.2: Write properties**
```python
@given(st.integers())
def test_property(x):
    assert property_holds(x)
```

---

## Common Pitfalls and Solutions

### Pitfall 1: Brittle Tests
**Problem**: Tests break on minor implementation changes
```python
def test_api_response_structure(self):
    response = client.get("/api/users")
    # Tests exact structure
    assert response["data"][0]["id"] == 1  # Brittle!
```

**Solution**: Test behavior, not structure
```python
def test_api_returns_users(self):
    response = client.get("/api/users")
    assert len(response["data"]) > 0
    assert all("id" in user for user in response["data"])
```

### Pitfall 2: Shared State Between Tests
**Problem**: Tests fail depending on execution order
```python
shared_list = []

def test_first():
    shared_list.append(1)

def test_second():
    assert len(shared_list) == 1  # Fails if run first
```

**Solution**: Use fixtures for isolation
```python
@pytest.fixture
def fresh_list():
    return []

def test_first(fresh_list):
    fresh_list.append(1)
```

### Pitfall 3: Over-Mocking
**Problem**: Tests pass but code doesn't work in production
```python
@patch("requests.get")
def test_api_call(mock_get):
    mock_get.return_value = Mock(json=lambda: {})
    # Test passes but real API might fail differently
```

**Solution**: Use integration tests and real dependencies
```python
def test_api_call():
    # Use real API or VCR for recorded responses
    response = api.get_user(1)
```

---

## Performance Benchmarks

```
Test Type              Speed      Cost       Coverage
Unit test             <1ms       Low        ~70%
Integration test      10-100ms   Medium     ~80%
E2E test             1-10s      High       ~90%
Property test        100-500ms  Medium     Finds edge cases
```

---

## Integration with LLM Systems

### 1. Testing LLM Outputs
```python
@given(st.text(min_size=1, max_size=1000))
def test_llm_output_valid(prompt):
    response = llm.generate(prompt)
    assert isinstance(response, str)
    assert len(response) > 0
```

### 2. Mocking External APIs
```python
@patch("openai.ChatCompletion.create")
def test_llm_integration(mock_create):
    mock_create.return_value = {"choices": [{"text": "response"}]}
    result = query_llm("test")
```

---

## Authoritative Sources

1. **pytest documentation**: https://docs.pytest.org/
2. **hypothesis documentation**: https://hypothesis.readthedocs.io/
3. **unittest.mock documentation**: https://docs.python.org/3/library/unittest.mock.html
4. **Test-Driven Development by Kent Beck**: https://www.oreilly.com/library/view/test-driven-development/0201616416/
5. **Working Effectively with Legacy Code by Michael Feathers**
6. **Property-Based Testing Research**: https://www.semanticscholar.org/
7. **RealPython - Testing**: https://realpython.com/python-testing/
8. **Coverage.py documentation**: https://coverage.readthedocs.io/
9. **Mutation Testing Guide**: https://mutmut.readthedocs.io/
10. **12 Factor App - Tests**: https://12factor.net/

---

## Summary

Comprehensive testing through:
- Unit tests for isolated component behavior
- Integration tests for multi-component interaction
- Property-based testing for edge case discovery
- Proper mocking and fixtures for isolation
- Coverage metrics for quality assurance

These patterns enable confident refactoring and prevent regressions in production systems.
