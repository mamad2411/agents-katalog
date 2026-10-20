# CloudMask-AWS Development Guidelines

## Code Quality Standards

### Import Organization (CRITICAL)
**ALL imports MUST be at the top of the file, immediately after the module docstring.**

```python
"""Module docstring."""

# Standard library imports
import json
import sys
from pathlib import Path
from typing import Any

# Third-party imports
import pytest
import yaml

# Local application imports
from ..config.config import Config
from ..exceptions import CloudMaskError
```

**Import Grouping:**
1. Standard library imports
2. Third-party imports  
3. Local application imports
4. Separate each group with a blank line

**Frequency: 5/5 files follow this pattern**

### Module Docstrings
Every module starts with a docstring describing its purpose:

```python
"""Command-line interface for CloudMask."""
```

**Frequency: 5/5 files have module docstrings**

### Type Hints (Modern Python 3.10+)
Use modern type hint syntax throughout:

```python
# Modern union syntax (NOT Optional[str])
def get_password(prompt: str, args_password: str | None) -> str:
    pass

# Built-in generics (NOT Dict[str, str])
def load_mapping() -> dict[str, str] | None:
    pass

# Built-in list types (NOT List[Path])
def process_files(files: list[Path]) -> int:
    pass
```

**Frequency: 5/5 files use modern type hints**

### Function Signatures
All functions have complete type hints:

```python
def save_mapping_with_encryption(
    mask: CloudMask,
    mapping_path: Path,
    encrypt: bool,
    password: str | None,
    quiet: bool
) -> None:
    """Save mapping with optional encryption."""
    pass
```

**Frequency: 5/5 files have complete type hints**

## Structural Conventions

### Class Organization
Classes follow consistent structure:

```python
class CloudMask:
    """Main anonymizer class."""

    def __init__(self, config: Config | None = None, seed: str | None = None):
        """Initialize CloudMask with configuration and seed."""
        self.config = config or Config()
        self.seed = seed or self.config.seed
        self._anonymizer = Anonymizer(self.config, self.seed)
        self._mapper = MappingManager(self.seed)

    @property
    def mapping(self) -> dict[str, str]:
        """Get current mapping."""
        return self._anonymizer.mapping

    def anonymize(self, text: str) -> str:
        """Anonymize text."""
        return self._anonymizer.anonymize(text)
```

**Pattern: Docstring → __init__ → Properties → Public methods → Private methods**

**Frequency: 3/3 classes follow this pattern**

### Test Class Organization
Test classes group related tests:

```python
class TestCLICommands:
    """Test all CLI commands comprehensively."""

    def test_no_command_shows_help(self, capsys):
        """Test that running without command shows help."""
        pass

    def test_init_config_list_templates(self, capsys):
        """Test listing available templates."""
        pass
```

**Frequency: All test files use this pattern**

## Naming Conventions

### Functions and Variables
- **snake_case** for functions and variables
- **Descriptive names** that indicate purpose
- **Verb-based** function names (handle_, get_, set_, load_, save_)

```python
def handle_anonymize(args: Any) -> int:
    """Handle anonymize command."""
    pass

def get_clipboard_text() -> str:
    """Get text from clipboard."""
    pass

def save_mapping_with_encryption(...) -> None:
    """Save mapping with optional encryption."""
    pass
```

**Frequency: 5/5 files follow snake_case consistently**

### Private Methods
Use single underscore prefix for internal methods:

```python
class Anonymizer:
    def _hash(self, value: str, prefix: str = "") -> str:
        """Generate deterministic hash."""
        pass

    def _anonymize_by_type(self, original: str, resource_type: str) -> str:
        """Anonymize based on resource type."""
        pass

    def _extract_prefix(self, resource_id: str) -> str:
        """Extract AWS resource prefix."""
        pass
```

**Frequency: 2/2 classes with private methods follow this pattern**

### Constants
Use UPPER_CASE for module-level constants:

```python
CLIPBOARD_AVAILABLE = True
AWS_ACCOUNT_PATTERN = re.compile(r'\b\d{12}\b')
```

**Frequency: Used consistently across codebase**

## Documentation Standards

### Docstring Style (Google Convention)
All functions have Google-style docstrings:

```python
def anonymize_file(self, input_path: Path, output_path: Path) -> int:
    """Anonymize a file.

    Args:
        input_path: Path to input file
        output_path: Path to output file

    Returns:
        Number of unique identifiers anonymized

    Raises:
        FileOperationError: If file cannot be read/written
    """
    pass
```

**Frequency: 5/5 files use Google-style docstrings**

### Inline Comments
Comments explain "why", not "what":

```python
# Anonymize account IDs within ARN
result = AWS_ACCOUNT_PATTERN.sub(
    lambda m: self._anonymize_by_type(m.group(0), "account"), original
)

# Sort by length to avoid partial replacements
for company in sorted(self.config.company_names, key=len, reverse=True):
    pass
```

**Frequency: Strategic comments in complex logic**

## Semantic Patterns

### Pattern Matching (Python 3.10+)
Use structural pattern matching for type-based logic:

```python
match (mapping, mapping_file):
    case (dict() as m, None):
        logger.debug("Initializing with provided mapping")
        self.reverse_mapping = {v: k for k, v in m.items()}
    case (None, Path() as f):
        logger.debug(f"Loading mapping from {f}")
        # Load from file
    case (None, None):
        logger.debug("Initializing with empty mapping")
        self.reverse_mapping = {}
    case _:
        raise ValidationError("Provide either mapping or mapping_file, not both")
```

**Frequency: 2/5 files use pattern matching**

### Pattern Matching for Resource Types
```python
match resource_type:
    case "account":
        anonymized = self._hash_to_account(original)
    case "ip":
        anonymized = self._hash_to_ip(original)
    case "domain":
        anonymized = self._hash_to_domain(original)
    case "company":
        anonymized = f"Company-{self._hash(original, 'company')[:8]}"
    case _:
        anonymized = self._hash(original, resource_type)[:12]
```

**Frequency: Used for type-based dispatch**

### Walrus Operator
Use assignment expressions for efficiency:

```python
if cached := self.mapping.get(original) or self._cache.get(original):
    return cached

if cached := self.mapping.get(original):
    return cached
```

**Frequency: 2/5 files use walrus operator**

### Dictionary Comprehensions
```python
# Reverse mapping creation
self.reverse_mapping = {v: k for k, v in m.items()}

# Result dictionary building
result: dict[str, Any] = {}
for key, value in data.items():
    match value:
        case str():
            result[key] = mask.anonymize(value)
        case dict():
            result[key] = anonymize_dict(value, mask)
```

**Frequency: Common pattern for transformations**

### Lambda Functions
Used for inline transformations:

```python
# Pattern substitution
result = AWS_ACCOUNT_PATTERN.sub(
    lambda m: self._anonymize_by_type(m.group(0), "account"), result
)

# Sorting with key function
for company in sorted(self.config.company_names, key=len, reverse=True):
    pass

# Sorted with custom key
for anonymized, original in sorted(
    self.reverse_mapping.items(), key=lambda x: len(x[0]), reverse=True
):
    pass
```

**Frequency: 4/5 files use lambda functions**

## Error Handling Patterns

### Custom Exception Hierarchy
Use custom exceptions with helpful messages:

```python
from ..exceptions import CloudMaskError, ClipboardError, FileOperationError

try:
    text: str = pyperclip.paste()
except Exception as e:
    raise ClipboardError(
        f"Cannot access clipboard: {e}",
        "Ensure clipboard access is available on your system",
    ) from e
```

**Frequency: 3/5 files use custom exceptions**

### Try-Except with Context
```python
try:
    return handler(args)
except CloudMaskError as e:
    print(f"Error: {e.message}", file=sys.stderr)
    if e.suggestion:
        print(f"💡 {e.suggestion}", file=sys.stderr)
    log_error(e, "CLI operation failed")
    return 1
except KeyboardInterrupt:
    print("\n⚠️  Operation cancelled by user", file=sys.stderr)
    return 130
except Exception as e:
    print(f"Unexpected error: {e}", file=sys.stderr)
    log_error(e, "Unexpected error")
    if args.debug:
        raise
    return 1
```

**Frequency: All CLI handlers use this pattern**

### Validation with Early Returns
```python
def handle_anonymize(args: Any) -> int:
    """Handle anonymize command."""
    if args.clipboard:
        if not check_clipboard_available():
            return 1
        if args.input or args.output:
            print("Error: --clipboard cannot be used with -i/--input or -o/--output",
                  file=sys.stderr)
            return 1
    elif not args.input or not args.output:
        print("Error: -i/--input and -o/--output are required when not using --clipboard",
              file=sys.stderr)
        return 1

    # Main logic here
    return 0
```

**Frequency: All command handlers validate early**

## Internal API Usage

### Config Loading Pattern
```python
from ..config.config_loader import load_config
from ..io.storage import Storage

config_path = args.config or Storage.DefaultConfigPath
config = (
    load_config(config_path, format=args.format, use_env=not args.no_env)
    if config_path
    else load_config(use_env=not args.no_env)
)
```

**Frequency: 3/5 files load config this way**

### CloudMask Initialization
```python
from ..core import CloudMask

mask = CloudMask(config)
# or
mask = CloudMask(config=config, seed=seed)
```

**Frequency: Standard initialization pattern**

### Mapping Management
```python
# Save mapping
mask.save_mapping(mapping_path)

# Load mapping
unmask = CloudUnmask(mapping_file=mapping_path)
# or
unmask = CloudUnmask(mapping=mapping_dict)
```

**Frequency: 4/5 files use this pattern**

### File Processing
```python
from ..io.file_processor import FileProcessor

# Process with callback
FileProcessor.process_file(input_path, output_path, self.anonymize)

# Or use class methods
count = mask.anonymize_file(input_path, output_path)
count = unmask.unanonymize_file(input_path, output_path)
```

**Frequency: Standard file processing pattern**

### Streaming for Large Files
```python
from ..io.streaming import stream_anonymize_file, stream_unanonymize_file

if args.stream:
    count = stream_anonymize_file(
        mask, args.input, args.output, show_progress=args.progress
    )
else:
    count = mask.anonymize_file(args.input, args.output)
```

**Frequency: Used in CLI handlers**

## Testing Patterns

### Pytest Fixtures
```python
@pytest.fixture
def tmp_path(tmp_path_factory):
    """Create a temporary directory."""
    return tmp_path_factory.mktemp("cli_test")
```

**Frequency: All test files use fixtures**

### Mock Patching
```python
from unittest.mock import patch

with patch("sys.argv", ["cloudmask", "anonymize", "-i", str(input_file)]):
    result = main()

with patch("cloudmask.core.CloudMask.anonymize_file", side_effect=KeyboardInterrupt):
    result = main()
```

**Frequency: All CLI tests use patching**

### Test Naming
```python
def test_no_command_shows_help(self, capsys):
    """Test that running without command shows help."""
    pass

def test_anonymize_with_streaming(self, tmp_path):
    """Test anonymize with streaming mode."""
    pass

def test_batch_with_failed_file(self, tmp_path):
    """Test batch processing with one failed file."""
    pass
```

**Pattern: test_<feature>_<scenario>**

**Frequency: 100% of tests follow this naming**

### Assertion Patterns
```python
# Return code assertions
assert result == 0
assert result == 1

# File existence
assert output_file.exists()
assert mapping_file.exists()

# Content assertions
assert "vpc-123" not in output_text
assert "usage:" in captured.out.lower()

# Count assertions
assert len(mask.mapping) > 0
```

**Frequency: Standard assertion patterns**

## Code Idioms

### Context Managers
```python
# File operations
with Path(args.mapping).open() as f:
    mapping = json.load(f)

# Multiple context managers
with (
    patch("cloudmask.core.CloudMask.anonymize_file", side_effect=KeyboardInterrupt),
    patch("sys.argv", ["cloudmask", "anonymize", ...]),
):
    result = main()
```

**Frequency: 3/5 files use context managers**

### Ternary Expressions
```python
# Config selection
config = config or Config()
seed = seed or self.config.seed

# Conditional assignment
log_level = "ERROR" if args.quiet else ("DEBUG" if args.debug else "WARNING")

# Default values
mapping_path = args.mapping or Storage.DefaultMappingPath
```

**Frequency: 5/5 files use ternary expressions**

### F-strings for Formatting
```python
print(f"✓ Anonymized {count} unique identifiers")
print(f"Error: {e.message}", file=sys.stderr)
print(f"  Total files: {total_files}")
print(f"  {category:20s}: {count:5d} ({percentage:5.1f}%)")
```

**Frequency: 5/5 files use f-strings exclusively**

### Pathlib Over os.path
```python
from pathlib import Path

# Path operations
config_file = tmp_path / "config.yaml"
output_file = args.output_dir / input_file.name

# File I/O
config_file.write_text("seed: test-seed\n")
text = input_file.read_text()

# Existence checks
if not f.exists():
    raise FileOperationError(f"Mapping file not found: {f}")
```

**Frequency: 5/5 files use pathlib**

## Annotations and Decorators

### Property Decorator
```python
@property
def mapping(self) -> dict[str, str]:
    """Get current mapping."""
    return self._anonymizer.mapping
```

**Frequency: Used for read-only attributes**

### Type Annotations in Lambdas
```python
# Capture variable in lambda with type hint
result = re.sub(
    custom.pattern,
    lambda m, name=pattern_name: self._anonymize_by_type(m.group(0), name),  # type: ignore[misc]
    result,
    flags=re.IGNORECASE,
)
```

**Frequency: Used when mypy needs help**

## Performance Patterns

### Caching
```python
from ..utils.cache import LRUCache

class Anonymizer:
    def __init__(self, config: Config, seed: str):
        self._cache = LRUCache(maxsize=1000)

    def _anonymize_by_type(self, original: str, resource_type: str) -> str:
        if cached := self.mapping.get(original) or self._cache.get(original):
            return cached
        # ... compute and cache
```

**Frequency: Used in hot paths**

### Sorting for Correctness
```python
# Sort by length to avoid partial replacements
for company in sorted(self.config.company_names, key=len, reverse=True):
    pass

# Sort for longest-first replacement
for anonymized, original in sorted(
    self.reverse_mapping.items(), key=lambda x: len(x[0]), reverse=True
):
    result = result.replace(anonymized, original)
```

**Frequency: Critical for text replacement**

## CLI Patterns

### Argument Parser Structure
```python
def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="cloudmask",
        description="Anonymize AWS infrastructure identifiers for LLM processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples: ...""",
    )

    # Global arguments
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")

    # Subcommands
    subparsers = parser.add_subparsers(dest="command")

    return parser
```

**Frequency: Standard CLI structure**

### Command Handler Dispatch
```python
handlers = {
    "init-config": handle_init_config,
    "anonymize": handle_anonymize,
    "unanonymize": handle_unanonymize,
    "validate": handle_validate,
    "batch": handle_batch,
    "stats": handle_stats,
}

handler = handlers.get(args.command)
if handler:
    return handler(args)
```

**Frequency: Used in main() function**

### User Feedback
```python
# Success messages with checkmark
print(f"✓ Config file created from '{args.template}' template: {args.config}")
print(f"✓ Anonymized {count} unique identifiers")

# Error messages to stderr
print("Error: -i/--input and -o/--output are required", file=sys.stderr)

# Suggestions with emoji
if e.suggestion:
    print(f"💡 {e.suggestion}", file=sys.stderr)

# Progress indicators
print(f"Processing {total_files} files...")
```

**Frequency: Consistent user feedback style**
