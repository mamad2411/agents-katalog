---
name: s1-api-conventions
description: Python API coding conventions for this BookStore project. Use when writing or reviewing Python code.
---

# S1 — BookStore API Conventions

Follow these conventions when writing or reviewing Python code in this project.

## Data Models

- Use `@dataclass(slots=True)` for all models
- Store monetary values as `int` in cents (e.g., `price_cents: int`)
- Use `field(default_factory=list)` for mutable defaults
- Type-annotate every field using modern syntax (`str | None`, not `Optional[str]`)

## API Functions

- All public API functions return `dict` (not dataclass instances)
- Include a `"status"` key in mutation responses (`"created"`, `"updated"`, `"deleted"`)
- Use `snake_case` with a verb prefix: `create_book`, `get_author`, `list_books`
- Private helpers start with underscore: `_to_dict`, `_validate_input`

## Docstrings

Every public function must have a docstring with:
```
"""One-line summary.

Args:
    param_name: Description.

Returns:
    Description of return value.

Raises:
    ValueError: When and why.
"""
```

## Error Handling

- Raise `ValueError` for invalid inputs (bad data from the caller)
- Raise `KeyError` for missing resources (not found)
- Never silently swallow exceptions

## Imports

- Standard library first, then third-party, then local
- Use absolute imports: `from models.book import Book`
- No wildcard imports
