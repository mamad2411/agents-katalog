# Development Standards and Technical Requirements

## Development Environment

### Required Tools and Versions
- **Python**: 3.12+ required
- **Package Manager**: uv for dependency management
- **Type Checker**: pyright for static type analysis
- **Formatter**: ruff for code formatting and linting
- **Testing**: pytest + pytest-asyncio for async testing

### Command Execution Standards
**All Python commands must use uv run prefix:**
- **Script Execution**: `uv run python script.py`
- **Module Execution**: `uv run python -m module_name`
- **Testing**: `uv run pytest`
- **Type Checking**: `uv run pyright`
- **Code Formatting**: `uv run ruff format`
- **Linting**: `uv run ruff check`

### Code Style Standards
- **Line Length**: 120 characters maximum
- **Import Organization**: Standard library → Third-party → Local imports
- **Language**: English for all comments, docstrings, and documentation
- **Naming**: snake_case for functions/variables, PascalCase for classes

## Code Organization Principles

### Module Structure
```python
# Required __all__ definition for public API control
__all__ = ["PublicClass", "public_function"]

# Import order (enforced by ruff)
import asyncio
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from .base import ObjectModel
from .exceptions import ValidationError
```

### Class Method Organization
```python
class ExampleModel(ObjectModel):
    # 1. Field definitions
    name: Column[str] = StringColumn(length=100)
    
    # 2. Configuration
    class Config:
        table_name = "examples"
    
    # 3. Validation methods
    def validate(self):
        pass
    
    # 4. Signal handlers
    async def before_save(self, context):
        pass
    
    # 5. Instance methods
    def get_display_name(self):
        pass
    
    # 6. Class methods
    @classmethod
    def create_default(cls):
        pass
```

### Error Handling Standards
- **Error Messages**: Always in English
- **Exception Types**: Use appropriate built-in or custom exceptions
- **Error Context**: Include relevant information for debugging
- **Logging**: Use structured logging with appropriate levels

## Testing Standards

### Test Structure
```python
import pytest
import pytest_asyncio

class TestUserModel:
    """Test class docstring describing test scope"""
    
    async def test_create_user_success(self):
        """Test method docstring describing specific scenario"""
        # Arrange
        user_data = {"username": "test", "email": "test@example.com"}
        
        # Act
        user = await User.objects.create(**user_data)
        
        # Assert
        assert user.username == "test"
        assert user.email == "test@example.com"
```

### Test Categories
- **Unit Tests**: Individual function/method testing
- **Integration Tests**: Component interaction testing
- **End-to-End Tests**: Full workflow testing
- **Performance Tests**: Benchmarking and load testing

## Documentation Standards

### Five-Section Structure
1. **Overview**: What the feature/module does
2. **Core Features**: 4 main capabilities with examples
3. **Module Architecture**: Technical design and structure
4. **API Reference**: Complete interface documentation
5. **Usage Guide**: Basic and advanced usage patterns

### Code Examples
- **Progressive Complexity**: Start simple, build to advanced
- **Complete Examples**: Runnable code snippets
- **English Comments**: Clear explanations in code
- **Real-World Scenarios**: Practical use cases
- **Multi-database support**: Show same functionality across PostgreSQL, SQLite, MySQL
- **Type consistency**: Ensure return types are consistent across databases  
- **Performance considerations**: Include database-specific optimization notes
- **Fallback handling**: Document graceful degradation for unsupported features

### Documentation Types
- **API Documentation**: Function/class interface specs
- **Feature Documentation**: User-focused how-to guides
- **Design Documentation**: Technical architecture details
- **Tutorial Documentation**: Step-by-step learning guides

## Quality Assurance

### Code Review Requirements
- [ ] Follows coding standards and style guide
- [ ] Includes appropriate tests with good coverage
- [ ] Documentation updated for public API changes
- [ ] Type annotations complete and accurate
- [ ] Error handling appropriate and consistent

### Performance Considerations
- **Async/Await**: Proper async patterns and context management
- **Memory Usage**: Efficient data structures and cleanup
- **Database Operations**: Optimized queries and bulk operations
- **Field Optimization**: Appropriate use of field selection and deferred loading

### Security Guidelines
- **Input Validation**: Sanitize and validate all inputs
- **SQL Injection**: Use parameterized queries exclusively
- **Error Information**: Don't expose sensitive data in errors
- **Dependencies**: Keep dependencies updated and secure

## Development Workflow Integration

### Pre-commit Checks
- Type checking with `uv run pyright`
- Code formatting with `uv run ruff format`
- Linting with `uv run ruff check`
- Basic test suite execution with `uv run pytest`

### Continuous Integration
- Full test suite with `uv run pytest` on multiple Python versions
- Code coverage reporting and thresholds
- Type checking with `uv run pyright`
- Code quality checks with `uv run ruff check`
- Documentation build verification
- Security vulnerability scanning

### Release Process
- Version bumping and changelog updates
- Documentation deployment
- Package building and distribution
- Release notes and migration guides