# CloudMask-AWS Technology Stack

## Programming Languages

### Python 3.10+
- **Minimum Version**: Python 3.10
- **Supported Versions**: 3.10, 3.11, 3.12, 3.13
- **Modern Features Used**:
  - Structural pattern matching (match/case)
  - Union type operators (X | Y instead of Union[X, Y])
  - Built-in generic types (list[str] instead of List[str])
  - Parenthesized context managers

## Core Dependencies

### Runtime Dependencies
- **PyYAML** (>=6.0.3): YAML configuration file parsing
- **pyperclip** (>=1.11.0): Clipboard integration for CLI
- **cryptography** (>=41.0.0): Secure hashing and encryption

### Development Dependencies
- **pytest** (>=8.4.2): Testing framework
- **pytest-cov** (>=7.0.0): Code coverage reporting
- **black** (>=25.9.0): Code formatting
- **ruff** (>=0.14.0): Fast Python linter
- **mypy** (>=1.18.2): Static type checking
- **pre-commit** (>=4.3.0): Git hooks for code quality
- **sphinx** (>=7.0.0): Documentation generation

### Optional Dependencies
- **tqdm** (>=4.66.0): Progress bars for large file processing

## Build System

### Package Management
- **Build Backend**: setuptools (>=80.9.0)
- **Package Manager**: uv (preferred) or pip
- **Lock File**: uv.lock for reproducible builds

### Project Configuration
- **pyproject.toml**: Modern Python project configuration
- **PEP 517/518**: Standard build system interface
- **Entry Points**: CLI command registered as `cloudmask`

## Development Tools

### Code Quality
- **black**: Line length 100, Python 3.10+ target
- **ruff**: Comprehensive linting (pycodestyle, pyflakes, isort, bugbear, etc.)
- **mypy**: Strict type checking with disallow_untyped_defs
- **pydocstyle**: Google-style docstring validation

### Testing
- **pytest**: Test discovery and execution
- **Coverage**: HTML and terminal coverage reports
- **Test Structure**: tests/ directory with test_*.py files

### CI/CD
- **GitHub Actions**: Automated workflows
  - test.yml: Run tests on multiple Python versions
  - publish.yml: PyPI publishing
  - auto-release.yml: Semantic versioning and releases
  - codeql.yml: Security scanning
  - dependency-review.yml: Dependency vulnerability checks

## Development Commands

### Package Management (uv)
```bash
# Install dependencies
uv pip install -e ".[dev]"

# Install specific package
uv pip install <package>

# Run script in venv
uv run python script.py

# Run tests
uv run pytest

# Check versions
uv pip list
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=cloudmask --cov-report=html

# Run specific test file
uv run pytest tests/test_cloudmask.py

# Run specific test
uv run pytest tests/test_cloudmask.py::test_anonymize
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Building
```bash
# Build package
python -m build

# Install locally
uv pip install -e .

# Install with dev dependencies
uv pip install -e ".[dev]"
```

### Documentation
```bash
# Build Sphinx docs
cd docs/
make html

# View docs
open _build/html/index.html
```

## Configuration Files

### pyproject.toml
- Project metadata and dependencies
- Tool configurations (black, ruff, mypy, pytest)
- Build system configuration
- Entry points for CLI

### .pre-commit-config.yaml
- Git hooks for automated checks
- Runs black, ruff, mypy before commits

### mypy.ini
- Type checking configuration
- Strict mode enabled
- Module-specific overrides

### .pydocstyle
- Docstring style configuration
- Google convention

### .gitignore
- Python cache files
- Build artifacts
- Virtual environments
- IDE files

## Virtual Environment

### Setup
```bash
# Create venv
uv venv

# Activate (Unix/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install project
uv pip install -e ".[dev]"
```

### Location
- Default: `.venv/` in project root
- Excluded from version control

## Type System

### Type Hints
- Full type coverage in src/cloudmask/
- py.typed marker for PEP 561 compliance
- Strict mypy configuration

### Common Types
```python
from pathlib import Path
from typing import Any

# Modern union syntax
str | None  # instead of Optional[str]
list[str]   # instead of List[str]
dict[str, Any]  # instead of Dict[str, Any]
```

## Versioning

### Semantic Versioning
- Format: MAJOR.MINOR.PATCH
- Current: 0.4.0
- Automated via python-semantic-release

### Version Bumping
- Conventional commits determine version
- feat: → MINOR bump
- fix: → PATCH bump
- feat!: or BREAKING CHANGE: → MAJOR bump

## Distribution

### PyPI Package
- Package name: cloudmask-aws
- Distribution: Source distribution + wheel
- Automated publishing via GitHub Actions

### Installation
```bash
# From PyPI
pip install cloudmask-aws

# From source
git clone <repo>
cd cloudmask
uv pip install -e ".[dev]"
```
