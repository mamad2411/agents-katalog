# Jetson Debianizer - Cursor/Coder AI Rules

## Project Context
You are building **jetson-debianizer**, a Python-based OS builder that automates the creation of custom Debian images for NVIDIA Jetson devices. Think "Debian installer meets Jetson SDK Manager, but fully automated and scriptable."

## Core Technologies
- **Python 3.9+** with type hints everywhere
- **Typer** for CLI (Beautiful, auto-documented CLI)
- **Rich** for terminal UI (colors, progress bars, tables)
- **Pydantic** for configuration validation
- **aiohttp** for async downloads
- **Poetry** for dependency management
- **pytest** for testing

## Code Style Rules

### Python Style
- **ALWAYS use type hints** for function arguments and return types
- Follow **PEP 8** strictly
- Use **Pathlib** for all file operations, never string paths
- Use **f-strings** for string formatting, not % or .format()
- Use **dataclasses** or **Pydantic models** for data structures
- Maximum line length: **100 characters**
- Use **async/await** for I/O operations (downloads, file operations)

### Example Code Style:
```python
from pathlib import Path
from typing import Optional
import asyncio

async def download_file(
    url: str, 
    output_path: Path,
    checksum: Optional[str] = None
) -> Path:
    """
    Download a file from URL with progress tracking.
    
    Args:
        url: Source URL to download from
        output_path: Destination path for downloaded file
        checksum: Optional SHA-256 checksum to verify
        
    Returns:
        Path to downloaded file
        
    Raises:
        ValueError: If checksum verification fails
        IOError: If download fails
    """
    logger.info(f"Downloading {url}")
    # Implementation here
    return output_path
```

### Imports Organization
1. Standard library imports
2. Third-party imports
3. Local application imports
4. Blank line between groups

```python
import os
import sys
from pathlib import Path
from typing import Optional, Dict, List

import typer
from rich.console import Console
from pydantic import BaseModel

from jetson_debianizer.config import load_config
from jetson_debianizer.utils import verify_checksum
```

## Architecture Guidelines

### Module Structure
Each module should have a **single responsibility**:
- `cli.py` - CLI commands only, delegate to other modules
- `config.py` - Configuration loading and validation
- `downloader.py` - Download logic only
- `rootfs.py` - Rootfs building logic
- `l4t.py` - L4T binary management
- `kernel.py` - Kernel compilation
- `image.py` - Image creation
- `utils.py` - Shared utilities

### Class Design
- Use **composition over inheritance**
- Keep classes **focused and small**
- Use **dependency injection** for testability
- Prefer **functions over classes** when no state needed

Example:
```python
class RootfsBuilder:
    """Builds Debian rootfs using mmdebstrap."""
    
    def __init__(self, config: DebianConfig, cache_dir: Path):
        self.config = config
        self.cache_dir = cache_dir
        self.output_dir = Path("output/rootfs")
    
    def build(self, variant: str = "minimal") -> Path:
        """Build rootfs with specified variant."""
        # Implementation
        pass
```

## Error Handling Rules

### Exception Handling
- **Never use bare `except:`** - always catch specific exceptions
- **Always provide context** in error messages
- **Log before re-raising** exceptions
- Use **custom exceptions** for domain-specific errors

```python
class JetsonDebianizerError(Exception):
    """Base exception for jetson-debianizer."""
    pass

class DownloadError(JetsonDebianizerError):
    """Raised when download fails."""
    pass

class BuildError(JetsonDebianizerError):
    """Raised when build fails."""
    pass

# Usage:
try:
    result = download_file(url, path)
except requests.RequestException as e:
    logger.error(f"Failed to download {url}: {e}")
    raise DownloadError(f"Could not download {url}") from e
```

### Cleanup
- **Always use context managers** for resources (files, connections)
- **Always use try...finally** for cleanup operations
- **Never leave resources open** on error

```python
async def download_with_cleanup(url: str, path: Path) -> Path:
    temp_path = path.with_suffix('.tmp')
    try:
        # Download to temp file
        await download_to(url, temp_path)
        # Verify checksum
        verify_checksum(temp_path)
        # Move to final location
        temp_path.rename(path)
        return path
    except Exception as e:
        logger.error(f"Download failed: {e}")
        if temp_path.exists():
            temp_path.unlink()  # Cleanup on error
        raise
```

## Logging Rules

### Log Levels
- **DEBUG**: Detailed diagnostic info (command execution, API calls)
- **INFO**: General informational messages (progress updates)
- **WARNING**: Something concerning but not fatal
- **ERROR**: An error occurred but program can continue
- **CRITICAL**: Fatal error, program must exit

### Logging Style
```python
from jetson_debianizer.logging import logger

# Good logging
logger.debug(f"Executing command: {' '.join(cmd)}")
logger.info("Starting rootfs build...")
logger.warning("Cache directory not found, creating...")
logger.error(f"Failed to extract archive: {e}")

# Use Rich for success messages
from rich.console import Console
console = Console()
console.print("✓ Build completed successfully!", style="bold green")

# Bad logging - don't do this
print("Starting build")  # Never use print
logger.info("Error occurred")  # Wrong level
logger.error("Starting build")  # Wrong level
```

## CLI Command Rules

### Typer Commands
- **Every command needs a docstring** (becomes help text)
- **Use descriptive argument/option names**
- **Provide sensible defaults**
- **Add examples in docstrings**
- **Use --help to guide users**

```python
@app.command()
def build_rootfs(
    variant: str = typer.Option(
        "minimal",
        help="Rootfs variant: minimal, standard, or desktop"
    ),
    packages: Optional[List[str]] = typer.Option(
        None,
        "--package", "-p",
        help="Additional packages to install"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be done without executing"
    )
):
    """
    Build a Debian rootfs for Jetson devices.
    
    Creates an ARM64 Debian rootfs using mmdebstrap with the specified
    variant and optional additional packages.
    
    Examples:
        # Build minimal rootfs
        jetson-debianizer build-rootfs
        
        # Build with additional packages
        jetson-debianizer build-rootfs -p vim -p htop
        
        # Dry run to see what would happen
        jetson-debianizer build-rootfs --dry-run
    """
    if dry_run:
        console.print("[yellow]DRY RUN MODE - No changes will be made[/]")
    
    logger.info(f"Building {variant} rootfs...")
    # Implementation
```

## Testing Rules

### Test Structure
- **One test file per module**: `test_downloader.py` tests `downloader.py`
- **Use descriptive test names**: `test_download_file_with_valid_checksum`
- **Follow AAA pattern**: Arrange, Act, Assert
- **Use pytest fixtures** for common setup

```python
import pytest
from pathlib import Path
from jetson_debianizer.downloader import Downloader

@pytest.fixture
def temp_cache(tmp_path):
    """Provide temporary cache directory."""
    cache = tmp_path / "cache"
    cache.mkdir()
    return cache

@pytest.fixture
def downloader(temp_cache):
    """Provide configured Downloader instance."""
    return Downloader(cache_dir=temp_cache)

def test_download_file_creates_file(downloader, temp_cache):
    """Test that download_file creates the output file."""
    # Arrange
    url = "https://example.com/file.txt"
    output = temp_cache / "file.txt"
    
    # Act
    result = downloader.download_file(url, output)
    
    # Assert
    assert result.exists()
    assert result == output

def test_download_file_with_invalid_checksum_raises_error(downloader, temp_cache):
    """Test that invalid checksum raises ValueError."""
    url = "https://example.com/file.txt"
    output = temp_cache / "file.txt"
    
    with pytest.raises(ValueError, match="Checksum verification failed"):
        downloader.download_file(url, output, checksum="invalid")
```

### Mocking
- **Mock external dependencies** (network, filesystem operations)
- **Don't mock what you don't own** (test real pathlib operations)
- **Use pytest-mock** for clean mocking

```python
def test_download_with_network_error(downloader, mocker):
    """Test handling of network errors."""
    # Mock the requests.get to raise exception
    mock_get = mocker.patch('requests.get', side_effect=requests.RequestException("Network error"))
    
    with pytest.raises(DownloadError):
        downloader.download_file("https://example.com/file", Path("/tmp/file"))
    
    mock_get.assert_called_once()
```

## Configuration Rules

### Pydantic Models
- **Use Pydantic for all configs**
- **Add validators for complex validation**
- **Provide Field descriptions**
- **Use proper types** (Path, not str for paths)

```python
from pydantic import BaseModel, Field, validator
from pathlib import Path
from typing import List

class DebianConfig(BaseModel):
    """Configuration for Debian rootfs."""
    
    release: str = Field(
        default="bookworm",
        description="Debian release codename"
    )
    variant: str = Field(
        default="minimal",
        description="Rootfs variant: minimal, standard, or desktop"
    )
    packages: List[str] = Field(
        default_factory=list,
        description="Additional packages to install"
    )
    mirror: str = Field(
        default="http://deb.debian.org/debian",
        description="Debian mirror URL"
    )
    
    @validator('release')
    def validate_release(cls, v):
        valid = ['bookworm', 'bullseye', 'sid']
        if v not in valid:
            raise ValueError(f"Release must be one of {valid}")
        return v
    
    @validator('variant')
    def validate_variant(cls, v):
        valid = ['minimal', 'standard', 'desktop']
        if v not in valid:
            raise ValueError(f"Variant must be one of {valid}")
        return v
```

## Shell Command Execution

### Running Commands
- **Always log commands before execution**
- **Capture stderr for debugging**
- **Handle timeouts**
- **Check return codes**

```python
import subprocess
from typing import List, Optional

def run_command(
    cmd: List[str],
    check: bool = True,
    capture: bool = False,
    cwd: Optional[Path] = None,
    timeout: Optional[int] = None
) -> subprocess.CompletedProcess:
    """
    Run shell command with proper logging and error handling.
    
    Args:
        cmd: Command and arguments as list
        check: Raise exception on non-zero exit
        capture: Capture stdout/stderr
        cwd: Working directory
        timeout: Timeout in seconds
        
    Returns:
        CompletedProcess with results
        
    Raises:
        subprocess.CalledProcessError: If command fails and check=True
        subprocess.TimeoutExpired: If command times out
    """
    logger.debug(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=capture,
            text=True,
            cwd=cwd,
            timeout=timeout
        )
        
        if capture:
            logger.debug(f"stdout: {result.stdout}")
            if result.stderr:
                logger.debug(f"stderr: {result.stderr}")
        
        return result
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(f"stderr: {e.stderr}")
        raise
    except subprocess.TimeoutExpired as e:
        logger.error(f"Command timed out after {timeout}s")
        raise
```

## Progress Indication

### Use Rich Progress Bars
```python
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

def download_with_progress(url: str, output: Path, size: int):
    """Download with progress bar."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task(f"Downloading {output.name}", total=size)
        
        # Download in chunks
        downloaded = 0
        while downloaded < size:
            chunk = min(8192, size - downloaded)
            # Download chunk
            downloaded += chunk
            progress.update(task, advance=chunk)
```

## File Operations

### Path Operations
- **Always use Pathlib**, never os.path
- **Check existence before operations**
- **Use atomic operations** when possible
- **Handle permissions properly**

```python
from pathlib import Path
import shutil

def safe_copy(src: Path, dst: Path) -> Path:
    """Copy file with proper error handling."""
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")
    
    # Create parent directory
    dst.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy with metadata
    shutil.copy2(src, dst)
    
    logger.debug(f"Copied {src} -> {dst}")
    return dst

def atomic_write(path: Path, content: str):
    """Write file atomically."""
    temp_path = path.with_suffix('.tmp')
    try:
        temp_path.write_text(content)
        temp_path.rename(path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise
```

## Documentation Rules

### Docstrings
- **Use Google style docstrings**
- **Document all public APIs**
- **Include examples in docstrings**
- **Document exceptions**

```python
def build_rootfs(config: DebianConfig, output_dir: Path) -> Path:
    """
    Build a Debian rootfs using mmdebstrap.
    
    This function creates an ARM64 Debian rootfs with the specified
    configuration. It handles cross-architecture building using QEMU.
    
    Args:
        config: Debian configuration including release, packages, etc.
        output_dir: Directory where rootfs will be created
        
    Returns:
        Path to the created rootfs directory
        
    Raises:
        BuildError: If rootfs build fails
        PermissionError: If running without sufficient privileges
        
    Examples:
        >>> config = DebianConfig(release="bookworm", variant="minimal")
        >>> rootfs = build_rootfs(config, Path("output/rootfs"))
        >>> print(f"Rootfs created at {rootfs}")
        Rootfs created at output/rootfs
    """
    # Implementation
```

## Performance Guidelines

### Async Operations
- **Use async for I/O-bound operations** (downloads, file operations)
- **Use ProcessPoolExecutor for CPU-bound** operations
- **Don't block the event loop**

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

async def download_many(urls: List[str]) -> List[Path]:
    """Download multiple files concurrently."""
    tasks = [download_file(url, get_output_path(url)) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if isinstance(r, Path)]

def compile_kernel_parallel(sources: List[Path]) -> List[Path]:
    """Compile kernel sources in parallel."""
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(compile_file, src) for src in sources]
        results = [f.result() for f in futures]
    return results
```

## Security Guidelines

### Checksum Verification
- **Always verify checksums** for downloaded files
- **Use SHA-256 or better**, never MD5
- **Fail if checksum missing** for security-critical files

```python
import hashlib

def verify_checksum(filepath: Path, expected: str, algorithm: str = 'sha256') -> bool:
    """
    Verify file checksum.
    
    Args:
        filepath: Path to file to verify
        expected: Expected checksum (hex)
        algorithm: Hash algorithm (default: sha256)
        
    Returns:
        True if checksum matches
        
    Raises:
        ValueError: If checksum doesn't match
    """
    hasher = hashlib.new(algorithm)
    
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            hasher.update(chunk)
    
    actual = hasher.hexdigest()
    
    if actual != expected:
        raise ValueError(
            f"Checksum mismatch for {filepath.name}\n"
            f"Expected: {expected}\n"
            f"Got:      {actual}"
        )
    
    logger.debug(f"✓ Checksum verified: {filepath.name}")
    return True
```

## Git Commit Guidelines

### Commit Messages
- **Use conventional commits**: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- **Write in imperative mood**: "Add feature" not "Added feature"
- **Be specific and clear**

Examples:
```
feat: add download manager with checksum verification
fix: handle network timeout in downloader
docs: add architecture documentation
test: add unit tests for config validation
refactor: simplify rootfs builder interface
```

## Common Patterns

### Singleton Logger
```python
# logging.py
from rich.logging import RichHandler
import logging

_logger = None

def get_logger() -> logging.Logger:
    """Get configured logger instance."""
    global _logger
    if _logger is None:
        _logger = logging.getLogger("jetson-debianizer")
        _logger.addHandler(RichHandler(rich_tracebacks=True))
        _logger.setLevel(logging.INFO)
    return _logger

# Usage everywhere:
from jetson_debianizer.logging import get_logger
logger = get_logger()
```

### Config Loading
```python
from pydantic import ValidationError

def load_config(config_path: Path) -> JetsonConfig:
    """Load and validate configuration file."""
    try:
        data = yaml.safe_load(config_path.read_text())
        config = JetsonConfig(**data)
        logger.info(f"Loaded config from {config_path}")
        return config
    except ValidationError as e:
        logger.error(f"Invalid configuration: {e}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML: {e}")
        raise
```

## What NOT to Do

### Anti-Patterns to Avoid
❌ **Don't use global state** (except for logger)
❌ **Don't use `os.path`** (use Pathlib)
❌ **Don't use bare `except:`**
❌ **Don't use `print()`** (use logger)
❌ **Don't ignore errors silently**
❌ **Don't write functions longer than 50 lines**
❌ **Don't mix concerns** in single function
❌ **Don't commit commented-out code**
❌ **Don't use mutable default arguments**

```python
# Bad
def bad_function(items=[]):  # Mutable default!
    items.append(1)
    return items

# Good
def good_function(items: Optional[List] = None) -> List:
    if items is None:
        items = []
    items.append(1)
    return items
```

## AI Assistance Guidelines

When implementing:
1. **Read the IMPLEMENTATION_PLAN.md** first
2. **Implement one phase at a time**
3. **Write tests alongside code**
4. **Ask for clarification** if requirements unclear
5. **Suggest improvements** if you see better approaches
6. **Show examples** in your responses
7. **Explain complex decisions**

## Final Notes

- **Quality over speed** - Take time to do it right
- **Test as you go** - Don't accumulate technical debt
- **Document decisions** - Future you will thank you
- **Keep it simple** - Complexity is the enemy
- **Make it maintainable** - Others will read this code

---

**Remember:** This is a complex project serving real users. Code quality matters. Take pride in your work! 🚀
