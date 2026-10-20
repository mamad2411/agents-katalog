# CloudMask-AWS Project Structure

## Directory Organization

```
cloudmask/
├── src/cloudmask/          # Main package source code
│   ├── cli/                # Command-line interface
│   ├── config/             # Configuration management
│   ├── io/                 # File I/O and streaming
│   ├── utils/              # Utility functions
│   ├── anonymizer.py       # Core anonymization logic
│   ├── core.py             # Main CloudMask/CloudUnmask classes
│   ├── mapper.py           # Mapping management
│   ├── exceptions.py       # Custom exceptions
│   └── logging.py          # Logging configuration
├── tests/                  # Comprehensive test suite
├── docs/                   # Sphinx documentation
├── examples/               # Usage examples
├── scripts/                # Development and release scripts
├── .github/                # GitHub Actions workflows
└── workspace/              # Development documentation
```

## Core Components

### Main Package (src/cloudmask/)

**Core Modules:**
- `core.py`: CloudMask and CloudUnmask main classes
- `anonymizer.py`: Anonymization engine with pattern matching
- `mapper.py`: Mapping storage and retrieval
- `exceptions.py`: Custom exception hierarchy

**CLI Package (cli/):**
- `cli.py`: Argument parsing and command routing
- `cli_handlers.py`: Command implementation (anonymize, unanonymize, init-config)

**Config Package (config/):**
- `config.py`: Configuration data classes
- `config_loader.py`: YAML/TOML config loading
- `config_templates.py`: Built-in configuration templates

**I/O Package (io/):**
- `file_processor.py`: File reading/writing operations
- `storage.py`: Central storage management (~/.cloudmask/)
- `streaming.py`: Large file streaming support

**Utils Package (utils/):**
- `patterns.py`: AWS resource pattern definitions
- `security.py`: Security utilities (permissions, validation)
- `cache.py`: Pattern compilation caching
- `ratelimit.py`: Rate limiting for operations

## Architectural Patterns

### Class-Based Namespacing

The project uses class-based namespacing for utility functions:

```python
# Storage utilities
from cloudmask import Storage
path = Storage.DefaultMappingPath
dir = Storage.Dir

# Config templates
from cloudmask import ConfigTemplates
templates = ConfigTemplates.List
template = ConfigTemplates.Get('standard')
```

### Singleton Pattern

Stateless utility classes are instantiated as singletons:

```python
class _StorageClass:
    @property
    def DefaultMappingPath(self) -> Path:
        return Path.home() / ".cloudmask" / "mapping.json"

Storage = _StorageClass()  # Singleton instance
```

### Context Manager Pattern

Temporary anonymization with automatic cleanup:

```python
with TemporaryMask(seed="temp") as mask:
    result = mask.anonymize(text)
    # Mapping discarded on exit
```

### Factory Pattern

Batch processing with reusable anonymizers:

```python
anon = create_batch_anonymizer(seed="batch")
result1 = anon("vpc-123")
result2 = anon("i-456")
```

## Component Relationships

### Anonymization Flow

```
User Input
    ↓
CLI/API Entry Point
    ↓
Config Loader → Config Object
    ↓
CloudMask Class
    ↓
Anonymizer Engine
    ↓
Pattern Matcher → Mapper
    ↓
Anonymized Output + Mapping
```

### Unanonymization Flow

```
Anonymized Input + Mapping File
    ↓
CloudUnmask Class
    ↓
Mapper (load mapping)
    ↓
Reverse Substitution
    ↓
Original Output
```

### Configuration Hierarchy

```
1. Default Config (built-in)
2. User Config (~/.cloudmask/config.yml)
3. Project Config (./cloudmask.yaml)
4. CLI Arguments (highest priority)
```

## Key Design Decisions

### Deterministic Hashing
- Same seed + same input = same output
- Enables consistent anonymization across sessions
- Seed verification prevents mapping corruption

### Prefix Preservation
- AWS resource IDs maintain their prefixes (vpc-, i-, sg-)
- Improves readability of anonymized output
- Maintains context for LLM processing

### Central Storage
- Default location: ~/.cloudmask/
- Automatic directory creation with secure permissions (700)
- Mapping files created with 600 permissions
- Auto-merge of mappings with same seed

### Modular Architecture
- Separation of concerns (CLI, core, config, I/O)
- Easy to extend with new patterns
- Testable components
- Clear dependency boundaries

## Extension Points

### Adding New Patterns
- Define pattern in `utils/patterns.py`
- Add to default config in `config/config.py`
- Update tests in `tests/test_patterns.py`

### Adding New Commands
- Add handler in `cli/cli_handlers.py`
- Register in `cli/cli.py`
- Add tests in `tests/test_cli_*.py`

### Custom Storage Backends
- Implement storage interface in `io/storage.py`
- Support for cloud storage, databases, etc.
- Maintain security requirements
