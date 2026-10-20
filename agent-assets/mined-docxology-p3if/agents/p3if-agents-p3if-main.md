# P3IF AI Agent Development Guide

This document provides comprehensive guidance for AI agents (including Large Language Models and autonomous systems) working on the P3IF (Properties, Processes, and Perspectives Inter-Framework) codebase.

## 🎯 P3IF Overview for AI Agents

P3IF is a sophisticated meta-framework for integrating, analyzing, and visualizing complex data relationships across multiple domains. It organizes information around three fundamental dimensions:

- **Properties**: System characteristics (e.g., security, usability, performance)
- **Processes**: Actions and transformations (e.g., authentication, data processing)
- **Perspectives**: Stakeholder viewpoints (e.g., technical, business, legal, user)

## 🏗️ Architecture Understanding

### Modular Design
P3IF follows a clean modular architecture with a modern `src/` layout:

```
p3if/
├── src/p3if/              # Main package
│   ├── core/              # Core framework, models, analysis, composition, orchestration
│   ├── orchestrators/     # Thin orchestrator examples
│   ├── visualization/     # Visualization and animation system
│   ├── utils/             # Shared utility modules
│   └── data/              # Data management, importers, exporters
├── tests/                 # Comprehensive test suite
├── data/                  # Domain data files
├── website/               # Web portal and API
├── docs/                  # Comprehensive documentation
└── scripts/               # All executable tools
```

### Key Concepts
1. **Thin Orchestrators**: Lightweight, reusable workflow patterns
2. **Framework Multiplexing**: Dynamic composition of multiple frameworks
3. **Hot-Swapping**: Runtime reconfiguration of framework components
4. **Multi-Domain Analysis**: Cross-domain pattern recognition and insights

## 🤖 AI Agent Development Guidelines

### 1. Code Generation Standards

#### Follow Established Patterns
```python
# ✅ Good: Follow existing patterns
@dataclass
class NewOrchestrator:
    """Thin orchestrator for specific domain analysis."""

    name: str = "new_domain_orchestrator"
    orchestrator: ThinOrchestrator = field(init=False)

    def __post_init__(self):
        self.orchestrator = ThinOrchestrator(self.name, OrchestratorType.LINEAR)
        self._setup_orchestrator()

    def _setup_orchestrator(self):
        # Define orchestration steps with clear dependencies
        self.orchestrator.add_step("analyze", self._analyze)
```

#### Use Proper Type Hints
```python
# ✅ Good: Complete type hints
def analyze_domain_relationships(
    domain_id: str,
    strength_threshold: Optional[float] = 0.5,
    include_metadata: bool = False
) -> Dict[str, List[Relationship]]:
    """Analyze relationships within a domain."""
    pass
```

#### Include Comprehensive Docstrings
```python
# ✅ Good: Complete docstring
def process_domain_data(
    domain_data: Dict[str, Any],
    validation_rules: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Process and validate domain data.

    Args:
        domain_data: Input domain data dictionary
        validation_rules: Optional list of validation rules to apply

    Returns:
        Dictionary containing processed data and validation results

    Raises:
        PatternValidationError: If validation fails
        P3IFError: If data processing fails

    Example:
        >>> processed = process_domain_data(raw_data, ["check_integrity"])
        >>> print(processed["validation_results"])
    """
    pass
```

### 2. Documentation Requirements

#### Module Documentation
Every new module must include a comprehensive docstring:

```python
"""
New P3IF Module

This module provides [specific functionality] for the P3IF framework.

Key Features:
- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

Usage:
    from p3if.core.models import Property

    instance = NewClass()
    results = instance.process_data(data)
"""
```

#### Function Documentation
All public functions require Google-style docstrings:

```python
def public_function(param1: str, param2: int = 0) -> Dict[str, Any]:
    """
    Process data with specific parameters.

    This function performs [specific operation] on the input data.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter (default: 0)

    Returns:
        Dictionary containing:
        - key1: Description of first result
        - key2: Description of second result

    Raises:
        ValueError: If param1 is invalid
        TypeError: If param2 is not an integer

    Example:
        >>> result = public_function("input", 5)
        >>> print(result["status"])
        "success"
    """
    pass
```

### 3. Testing Requirements

#### Unit Tests
Every new function/class must have corresponding unit tests:

```python
import pytest
from p3if.core.models import Property

class TestNewClass(unittest.TestCase):
    def setUp(self):
        self.instance = NewClass()

    def test_basic_functionality(self):
        """Test basic functionality of NewClass."""
        result = self.instance.process_data("test_input")
        self.assertEqual(result["status"], "success")

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        with self.assertRaises(ValueError):
            self.instance.process_data(None)
```

#### Integration Tests
Include integration tests for component interactions:

```python
def test_integration_with_core():
    """Test integration with P3IF core components."""
    from p3if.core import P3IFCore

    core = P3IFCore()
    framework = core.create_framework("property", "Example", domain="example")

    assert framework.domain == "example"
```

### 4. Error Handling

#### Robust Error Handling
Implement comprehensive error handling:

```python
from p3if.core.validation import ValidationEngine

def robust_function(data: Dict[str, Any]) -> Dict[str, Any]:
    """Function with robust error handling."""
    try:
        # Validate input
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary")

        # Process data
        result = process_data_internal(data)

        # Validate the framework
        validator = ValidationEngine()
        validation_result = validator.validate_framework(framework)

        if not validation_result["overall_valid"]:
            raise FrameworkValidationError("Output validation failed")

        return result

    except Exception as e:
        logger.error(f"Error in robust_function: {e}")
        raise P3IFError(f"Processing failed: {str(e)}") from e
```

### 5. Performance Considerations

#### Caching for Expensive Operations
```python
from p3if.core.caching import CacheManager, CacheStrategy

@cached(CacheStrategy.LRU, ttl=3600)
def expensive_operation(data: Dict[str, Any]) -> Dict[str, Any]:
    """Expensive operation with caching."""
    # Implementation that benefits from caching
    pass
```

#### Async Support for I/O Operations
```python
from p3if.utils.storage import JSONStorage

async def async_data_processing(storage: JSONStorage, pattern: BasePattern) -> None:
    """Async pattern persistence via the storage layer."""
    await storage.save_pattern_async(pattern)
```

### 6. Documentation Updates

#### Update Relevant Documentation
When adding new functionality:

1. **Update module docstrings** to reflect new capabilities
2. **Add usage examples** in the module documentation
3. **Update README files** for new components
4. **Add tutorial content** if introducing new concepts
5. **Update API documentation** for new public interfaces

#### Example Documentation Update
```python
"""
P3IF New Module

This module provides enhanced [functionality] for the P3IF framework.

New Features:
- Feature A: Description and benefits
- Feature B: Description and benefits

Usage Examples:
    from p3if.visualization.interactive import InteractiveVisualizer

    # Basic usage
    feature = NewFeature()
    result = feature.process_data(data)

    # Advanced usage
    feature.configure(options)
    result = feature.process_advanced(data)
"""
```

## 🧪 Testing Guidelines for AI Agents

### 1. Test Coverage Requirements
- **Unit Tests**: >90% coverage for new code
- **Integration Tests**: Test component interactions
- **Error Tests**: Test error conditions and edge cases
- **Performance Tests**: Ensure performance requirements are met

### 2. Test Data Generation
Use P3IF's test utilities:

```python
from tests.fixtures import create_test_framework, create_multi_domain_test_framework

# Create test data
framework = create_test_framework(num_properties=10, num_processes=8)
multi_domain = create_multi_domain_test_framework(domains=["healthcare", "finance"])
```

### 3. Test Organization
Follow the established test structure:

```python
class TestNewFeature(unittest.TestCase):
    """Test cases for NewFeature functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.feature = NewFeature()

    def test_basic_functionality(self):
        """Test basic functionality."""
        pass

    def test_error_conditions(self):
        """Test error handling."""
        pass

    def test_performance(self):
        """Test performance characteristics."""
        pass
```

## 📚 Documentation Standards for AI Agents

### 1. Module Documentation
Include comprehensive module docstrings:

```python
"""
P3IF New Module

This module provides [specific functionality] for the P3IF framework,
extending the core capabilities with [key features].

Key Features:
- Feature 1: Description
- Feature 2: Description

Integration:
    This module integrates with:
    - p3if.core: Core framework functionality
    - p3if.visualization: Visualization capabilities
    - tests: Testing framework

Usage:
    from p3if.core.models import Property

    instance = NewClass()
    result = instance.process_data(data)
"""
```

### 2. Function Documentation
Use Google-style docstrings:

```python
def process_complex_data(
    data: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None,
    validate: bool = True
) -> Dict[str, Any]:
    """
    Process complex data with optional validation.

    This function processes complex data structures, applying
    transformations and validations as specified.

    Args:
        data: Input data dictionary to process
        options: Optional processing options
        validate: Whether to perform validation (default: True)

    Returns:
        Dictionary containing:
        - processed_data: The processed data
        - validation_results: Validation outcomes
        - metadata: Processing metadata

    Raises:
        P3IFError: If processing fails
        ValidationError: If validation fails and validate=True

    Example:
        >>> result = process_complex_data(
        ...     {"key": "value"},
        ...     {"transform": True},
        ...     validate=True
        ... )
        >>> print(result["processed_data"])
    """
    pass
```

## 🔧 Development Workflow for AI Agents

### 1. Understand the Request
- Analyze the user's requirements thoroughly
- Identify which P3IF components are involved
- Determine the appropriate module for implementation

### 2. Plan the Implementation
- Design the solution following P3IF patterns
- Consider integration with existing components
- Plan comprehensive testing
- Consider documentation needs

### 3. Implement the Solution
- Follow established code patterns
- Include proper error handling
- Add comprehensive docstrings
- Implement unit tests
- Update documentation

### 4. Validate the Implementation
- Run tests to ensure functionality
- Check integration with other components
- Validate documentation accuracy
- Ensure performance requirements are met

### 5. Document Changes
- Update relevant README files
- Add usage examples
- Update API documentation
- Add tutorial content if needed

## 🚨 Common Pitfalls to Avoid

### 1. Code Quality Issues
- **Missing type hints**: Always include complete type annotations
- **Incomplete docstrings**: Ensure all functions have comprehensive documentation
- **Poor error handling**: Implement robust error handling patterns
- **Hardcoded values**: Use configuration and avoid magic numbers

### 2. Integration Issues
- **Breaking existing APIs**: Maintain backward compatibility
- **Ignoring dependencies**: Consider how changes affect other components
- **Missing tests**: Always include comprehensive test coverage
- **Incomplete documentation**: Document all new functionality

### 3. Performance Issues
- **Inefficient algorithms**: Optimize for large datasets
- **Missing caching**: Use caching for expensive operations
- **Memory leaks**: Ensure proper resource cleanup
- **Blocking operations**: Use async where appropriate

## 🛠️ Available Tools and Resources

### Development Tools
- **Interactive Terminal**: `./interactive_terminal.sh` - Full development environment
- **Test Runner**: `pytest tests/ -v` - Comprehensive testing
- **Performance Benchmark**: `python scripts/benchmark_performance.py` - Performance analysis

### Documentation Resources
- **Core Concepts**: [docs/concepts/P3IF.md](docs/concepts/P3IF.md)
- **API Reference**: [docs/api/README.md](docs/api/README.md)
- **Tutorials**: [docs/tutorials/](docs/tutorials/)
- **Examples**: [docs/examples/](docs/examples/)

### Code Resources
- **Core Framework**: [src/p3if/core/](src/p3if/core/)
- **Orchestrators**: [src/p3if/orchestrators/](src/p3if/orchestrators/)
- **Visualization**: [src/p3if/visualization/](src/p3if/visualization/)
- **Tests**: [tests/](tests/)
- **Utilities**: [src/p3if/utils/](src/p3if/utils/)

## 🤝 Contributing as an AI Agent

### 1. Follow the Process
1. Understand the request thoroughly
2. Plan your implementation
3. Implement following P3IF patterns
4. Add comprehensive tests
5. Update documentation
6. Validate everything works

### 2. Quality Standards
- Maintain the established code quality
- Follow the documentation standards
- Include comprehensive testing
- Ensure performance optimization
- Maintain backward compatibility

### 3. Communication
- Explain your implementation choices
- Document any assumptions made
- Highlight any limitations or trade-offs
- Suggest future improvements

## 🎯 Success Metrics for AI Agents

### Code Quality
- [ ] All code follows PEP 8 standards
- [ ] Complete type hints for all functions
- [ ] Comprehensive docstrings for all public APIs
- [ ] Robust error handling
- [ ] Performance considerations addressed

### Testing
- [ ] Unit tests for all new functionality
- [ ] Integration tests for component interactions
- [ ] Error condition testing
- [ ] Performance benchmarking
- [ ] >90% test coverage

### Documentation
- [ ] Module docstrings updated
- [ ] Function docstrings complete
- [ ] Usage examples included
- [ ] README files updated
- [ ] API documentation current

### Integration
- [ ] Works with existing P3IF components
- [ ] Maintains backward compatibility
- [ ] Follows established patterns
- [ ] No breaking changes introduced

## 📞 Getting Help

If you need assistance:

1. **Check Documentation**: Review existing docs for patterns and examples
2. **Examine Code**: Look at similar implementations in the codebase
3. **Run Tests**: Ensure your changes don't break existing functionality
4. **Ask Questions**: Use the development resources and community

## 🔮 Future Considerations

When developing for P3IF, consider:

1. **Extensibility**: How can others build on your work?
2. **Performance**: How will this scale with large datasets?
3. **Integration**: How does this fit with the broader ecosystem?
4. **Maintenance**: How easy will this be to maintain and update?

By following these guidelines, AI agents can contribute high-quality, well-documented, and well-tested code to the P3IF project while maintaining consistency with the established patterns and standards.

---

*This guide is designed to help AI agents contribute effectively to the P3IF project by understanding the codebase structure, following established patterns, and maintaining high-quality standards.*

