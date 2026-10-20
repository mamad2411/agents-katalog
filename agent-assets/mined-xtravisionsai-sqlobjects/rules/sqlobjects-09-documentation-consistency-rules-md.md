# Documentation Consistency and Maintenance Rules

## Core Principles

### Documentation-Code Alignment
- **100% Consistency**: All documentation must match actual code implementation
- **No Fictional Features**: Remove or clearly mark unimplemented functionality
- **Runnable Examples**: All API examples must be executable code
- **Accurate Specifications**: Parameter descriptions, return values, and behavior must be precise

### Feature Status Classification
- **✅ Implemented**: Features fully working in current codebase
- **🚧 Partial**: Features with limited implementation (specify scope)
- **❌ Unimplemented**: Features moved to TODO.md or removed from docs
- **📋 Planned**: Features in TODO.md with clear version targets

## Documentation Update Requirements

### Immediate Updates Required
When code changes, documentation must be updated in the same commit/PR:

```python
# Code change example
async def bulk_create(self, objects, batch_size=1000, on_conflict="ignore"):
    # Implementation...
    pass

# Documentation must reflect actual parameters
# ✅ Correct documentation
await User.objects.bulk_create(data, batch_size=1000, on_conflict="ignore")

# ❌ Incorrect documentation (shows unimplemented features)
await User.objects.bulk_create(data, on_conflict="update")  # "update" not implemented
```

### API Example Validation
All code examples in documentation must:

1. **Be Syntactically Correct**: No syntax errors or typos
2. **Use Actual APIs**: Only show implemented methods and parameters
3. **Include Imports**: Show necessary import statements
4. **Handle Errors**: Show appropriate error handling where relevant
5. **Be Complete**: Provide full working examples, not fragments

```python
# ✅ Good example - complete and runnable
from sqlobjects.model import ObjectModel
from sqlobjects.fields import Column, StringColumn
from sqlobjects.exceptions import ValidationError

class User(ObjectModel):
    username: Column[str] = StringColumn(length=50)
    email: Column[str] = StringColumn(length=100)

try:
    user = await User.objects.create(username="john", email="john@example.com")
    print(f"Created user: {user.username}")
except ValidationError as e:
    print(f"Validation failed: {e}")

# ❌ Bad example - incomplete and uses unimplemented features
user = await User.objects.create_with_validation(...)  # Method doesn't exist
```

## Feature Documentation Standards

### Implemented Features Documentation
For features that exist in the codebase:

```markdown
## Query Caching (✅ Implemented)

SQLObjects provides basic query caching with cache bypass functionality:

```python
# Cache is used by default
users = await User.objects.filter(User.is_active == True).all()

# Skip cache for real-time data
live_users = await User.objects.no_cache().filter(User.status == "online").all()
```

**Available Methods:**
- `no_cache()`: Skip cache for this query
- Basic cache statistics (implementation varies by component)
```

### Unimplemented Features Handling
For features mentioned in design docs but not implemented:

```markdown
## Advanced Cache Management (❌ Not Implemented)

Advanced cache management features are planned for future releases.
See [TODO.md](../TODO.md) for implementation timeline.

**Planned Features:**
- Detailed cache statistics
- Cache size management
- Performance monitoring
- Cache invalidation strategies

**Current Alternative:**
Use `no_cache()` method to bypass caching when needed.
```

## Validation Checklist

### Pre-Release Documentation Review
Before any release, verify:

- [ ] All API examples can be executed successfully
- [ ] Parameter descriptions match actual method signatures
- [ ] Return value descriptions are accurate
- [ ] Exception handling examples use correct exception types
- [ ] Performance claims are backed by actual measurements
- [ ] Feature availability matches implementation status

### Code Change Documentation Impact
When making code changes, check if updates needed in:

- [ ] API reference documentation
- [ ] Feature documentation examples
- [ ] Tutorial code samples
- [ ] README examples
- [ ] Architecture documentation
- [ ] Performance optimization guides

### Documentation Testing
Implement automated checks where possible:

```python
# Example: Automated API example validation
def test_documentation_examples():
    """Test that documentation examples actually work"""
    # Extract code examples from documentation
    # Execute them in isolated environment
    # Verify they run without errors
    pass

def test_api_signature_consistency():
    """Test that documented APIs match actual implementations"""
    # Compare documented method signatures with actual code
    # Verify parameter names, types, and defaults match
    pass
```

## Error Message Standards

### Consistency Requirements
All error messages must:

1. **Use English**: All error messages in English only
2. **Be Descriptive**: Clearly explain what went wrong
3. **Provide Context**: Include relevant information for debugging
4. **Suggest Solutions**: When possible, suggest how to fix the issue
5. **Use Consistent Terminology**: Use same terms across all error messages

```python
# ✅ Good error messages
raise ValidationError("Email address is required", field="email", code="required")
raise ValidationError("Username must be at least 3 characters long", field="username", code="min_length")
raise DatabaseError("Connection to database 'main' failed: timeout after 30 seconds")

# ❌ Poor error messages
raise ValidationError("Invalid")  # Too vague
raise ValidationError("电子邮件是必需的")  # Not in English
raise ValidationError("Bad stuff happened")  # Not descriptive
```

## Documentation Maintenance Process

### Regular Audits
Perform quarterly documentation audits:

1. **API Consistency Check**: Verify all documented APIs exist and work as described
2. **Example Validation**: Run all code examples to ensure they work
3. **Feature Status Review**: Update feature status markers (✅❌🚧📋)
4. **Performance Claims Verification**: Validate performance statements with benchmarks
5. **Link Validation**: Check all internal and external links work correctly

### Version-Specific Updates
For each version release:

1. **New Features**: Document all new functionality with examples
2. **Changed APIs**: Update documentation for any API changes
3. **Deprecated Features**: Mark deprecated features and provide migration paths
4. **Removed Features**: Remove documentation for deleted functionality
5. **Performance Improvements**: Update performance claims with new benchmarks

### Documentation Debt Management
Track and address documentation debt:

```markdown
## Documentation Debt Tracking

### High Priority
- [ ] Update bulk operations examples to show actual return values
- [ ] Add missing error handling examples for relationship operations
- [ ] Verify all performance claims with current benchmarks

### Medium Priority
- [ ] Improve code examples in advanced querying section
- [ ] Add more real-world usage scenarios
- [ ] Update architecture diagrams to reflect current implementation

### Low Priority
- [ ] Improve formatting consistency across all docs
- [ ] Add more cross-references between related sections
- [ ] Expand troubleshooting guides
```

## Quality Metrics

### Documentation Quality Indicators
Track these metrics to ensure documentation quality:

1. **API Coverage**: Percentage of public APIs documented with examples
2. **Example Success Rate**: Percentage of documentation examples that run successfully
3. **Consistency Score**: Percentage of documented features that match implementation
4. **Freshness**: Time since last update for each documentation section
5. **User Feedback**: Issues and questions indicating documentation problems

### Automated Validation
Implement automated checks:

```python
# Example validation scripts
def validate_api_examples():
    """Extract and test all API examples from documentation"""
    pass

def check_feature_status_accuracy():
    """Verify feature status markers match actual implementation"""
    pass

def validate_cross_references():
    """Check all internal documentation links are valid"""
    pass

def check_import_statements():
    """Verify all import statements in examples are correct"""
    pass
```

## Integration with Development Workflow

### Pre-Commit Hooks
Add documentation validation to pre-commit hooks:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-doc-examples
        name: Validate Documentation Examples
        entry: python scripts/validate_doc_examples.py
        language: python
        files: 'docs/.*\.md$'
```

### CI/CD Integration
Include documentation validation in CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Validate Documentation
  run: |
    python scripts/validate_doc_examples.py
    python scripts/check_api_consistency.py
    python scripts/verify_feature_status.py
```

### Code Review Requirements
For code reviews involving documentation:

- [ ] All new APIs have documentation with examples
- [ ] Changed APIs have updated documentation
- [ ] Examples are tested and work correctly
- [ ] Feature status markers are accurate
- [ ] Error messages follow consistency standards

This ensures documentation remains a reliable and accurate resource for SQLObjects users.