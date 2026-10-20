---
description: Python Coding Standards and Best Practices
alwaysApply: false
globs:
  - "**/*.py"
  - "!esp32/**/*.py"
metadata:
  environments: cloud
---

# Python Coding Standards

This file applies only to Python files (excluding MicroPython in esp32/).

## Formatters (MANDATORY)

```
Black (line length: 88)
isort (profile: black)
```

## Code Organization

```
Functions: ≤ 50 lines
Classes: ≤ 300 lines
Single Responsibility Principle
```

## Style Guide

**Type hints:**
- RECOMMENDED for public APIs
- Use standard library types (typing module)
- Example: `def fetch_data(url: str) -> dict:`

**Docstrings:**
- Google style for public functions/classes
- Include Args, Returns, Raises sections
- Example:
  ```python
  def process_sensor_data(reading: dict) -> float:
      """Process raw sensor reading into temperature value.
      
      Args:
          reading: Raw sensor data dictionary
          
      Returns:
          Temperature in Celsius
          
      Raises:
          ValueError: If reading is invalid
      """
  ```

**Error handling:**
- Catch specific exceptions, avoid bare `except`
- Re-raise with context when needed
- Log errors appropriately

**Imports:**
- Group: stdlib, third-party, local
- Sorted alphabetically within groups (isort handles this)
- Avoid `from module import *`

## Before Writing Python Code

Self-check:

```
[ ] Will format with Black before commit
[ ] Function < 50 lines?
[ ] Class < 300 lines?
[ ] Type hints for public API?
[ ] Docstring for public functions?
[ ] Specific exception handling (no bare except)?
```

## Common Patterns

**GCP Client initialization:**
```python
from google.cloud import bigquery

client = bigquery.Client()  # Uses Application Default Credentials
```

**Async/await (when needed):**
```python
import asyncio

async def fetch_data():
    # async operations
    pass

# Run in Cloud Functions
result = asyncio.run(fetch_data())
```

**Environment variables:**
```python
import os

PROJECT_ID = os.environ.get('GCP_PROJECT', 'aquapulse-default')
```

## Prohibited

```
✗ Global mutable state (use function parameters)
✗ Bare except clauses
✗ print() for logging (use logging module)
✗ Hardcoded credentials (use Secret Manager)
```
