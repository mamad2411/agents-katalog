# API Design Rules

## Class-Based Namespacing

- Use class-based namespacing for related utility functions instead of `get_*` function patterns
- Properties should use PascalCase to match class naming conventions
- Create singleton instances for stateless utility classes

### Example Pattern

**Bad:**
```python
from mylib import get_default_path, get_storage_dir, get_config_path

path = get_default_path()
dir = get_storage_dir()
```

**Good:**
```python
from mylib import Storage

path = Storage.DefaultPath
dir = Storage.Dir
config = Storage.ConfigPath
```

### Implementation

```python
class Storage:
    """Utility class for storage paths."""

    @property
    def DefaultPath(self) -> Path:
        """Get default path."""
        return _get_default_path()

    @property
    def Dir(self) -> Path:
        """Get storage directory."""
        return _get_storage_dir()

# Create singleton instance
Storage = Storage()
```

## Benefits

- Cleaner imports: `from cloudmask import CloudMask, Storage, ConfigTemplates`
- Consistent naming: All imports look like classes
- Better IDE autocomplete: `Storage.` and `ConfigTemplates.` show all available options
- Logical grouping: Related functionality under one namespace
- Backward compatibility: Keep old functions as aliases

## Examples

### Storage
```python
from cloudmask import Storage

path = Storage.DefaultMappingPath
dir = Storage.Dir
config = Storage.DefaultConfigPath
```

### ConfigTemplates
```python
from cloudmask import ConfigTemplates

templates = ConfigTemplates.List
template = ConfigTemplates.Get('standard')
ConfigTemplates.Save('minimal', Path('config.yml'))
```

## Backward Compatibility

Always maintain backward compatibility when refactoring:

```python
# New API
Storage = Storage()

# Old API (deprecated but functional)
get_default_path = _get_default_path
get_storage_dir = _get_storage_dir
```
