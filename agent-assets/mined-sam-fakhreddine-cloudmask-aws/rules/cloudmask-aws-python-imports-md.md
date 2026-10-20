# Python Import Rules

## Import Organization

- ALL imports MUST be at the top of the file, immediately after the module docstring
- NEVER use inline imports inside functions or methods
- Group imports in this order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports
- Separate each group with a blank line

## Example

```python
"""Module docstring."""

import os
import tempfile
from pathlib import Path

import yaml

from .exceptions import CustomError
from .utils import helper_function
```

## Exceptions

- Only use inline imports if there's a circular dependency issue
- If inline import is absolutely necessary, add a comment explaining why
- Consider refactoring to avoid circular dependencies instead

## Rationale

- Improves code readability
- Makes dependencies explicit and easy to find
- Follows PEP 8 style guide
- Prevents import-related bugs
- Makes it easier to identify unused imports
