---
name: tool-schema-design
description: Design or tighten a Pydantic v2 tool schema from a plain-English description of what the tool should do. Use this whenever the user is defining a tool or function for an agent, wrapping an API endpoint as an agent tool, writing an MCP tool definition, or asking how to constrain tool parameters — and whenever an existing schema needs review for loose types, unconstrained strings, or thin descriptions.
---

# Tool Schema Design

Take a natural-language description of what a tool should do and produce a
production-ready Pydantic v2 schema following all six tool design principles.

## When to Use

- Designing a new tool for an agent.
- Converting an existing API endpoint into an agent-friendly tool.
- Reviewing and tightening an existing tool schema.

## Inputs

Provide:
- **Tool description**: What the tool does in plain English.
- **Data source** (optional): Database, API, file system, etc.
- **Constraints** (optional): Read-only, rate limits, auth requirements.

## Six Principles Applied

Every generated schema satisfies:

### 1. Verb-Noun Name
- Format: `{verb}_{noun}` in snake_case.
- Good: `run_sql`, `create_chart`, `search_documents`, `validate_address`.
- Bad: `do_stuff`, `process`, `handler`, `tool1`.

### 2. Rich Description
The class docstring includes three sections:

```
"""One-line summary.

Use this tool when:
- {condition 1}
- {condition 2}

Do NOT use this tool for:
- {exclusion 1}

Returns: {description of return value and format}.
Limits: {rate limits, max rows, timeout}.
"""
```

### 3. Constrained Parameters
Apply the tightest constraint that doesn't reject valid inputs:

| Type | Constraint | Example |
|------|-----------|---------|
| String enum | `Literal["a", "b", "c"]` | Chart types, sort orders |
| String pattern | `Field(pattern=r"^SELECT")` | SQL queries |
| String length | `Field(min_length=1, max_length=2000)` | User inputs |
| Integer range | `Field(ge=1, le=100)` | Page size, timeout |
| List length | `Field(min_length=1, max_length=10)` | Batch inputs |

### 4. Small and Focused
- One tool does one thing well.
- If a tool needs more than 5 parameters, consider splitting it.
- If a tool description uses "and" to list capabilities, consider splitting.

### 5. Idempotent
- Read operations: Always idempotent.
- Write operations: Use idempotency keys where possible.
- Flag non-idempotent tools in the docstring.

### 6. Structured Output
Define a return type model:

```python
class {ToolName}Result(BaseModel):
    success: bool
    data: {specific_type}
    error: str | None = None
    metadata: dict = Field(default_factory=dict)
```

## Output Format

For each tool, generate:

```python
from pydantic import BaseModel, Field
from typing import Literal

class {ToolName}Tool(BaseModel):
    """{Rich docstring following template above.}"""
    {param_1}: {type} = Field(
        description="{clear description}",
        {constraints}
    )
    # ... more params

class {ToolName}Result(BaseModel):
    """Return type for {tool_name}."""
    success: bool
    data: {type}
    error: str | None = None
```

## Common Tool Patterns

### Database Query Tool
- Read-only SQL with `pattern=r"^(SELECT|WITH)"`.
- Timeout parameter with `le=30`.
- Max rows hint in description.

### API Wrapper Tool
- Focused interface over a single API capability.
- Map complex API params to simple, constrained fields.
- Include retry-relevant metadata in result.

### File Operation Tool
- Path validation (no traversal: `..`).
- Size limits for reads.
- Explicit read-only or read-write flag.

### Search Tool
- Query string with length limit.
- Filters as optional constrained fields.
- Pagination via `limit` and `offset` with defaults.

## Validation Checklist

Before finalizing a schema, verify:
- [ ] Name is verb_noun format.
- [ ] Docstring has Use/Don't Use/Returns sections.
- [ ] Every parameter has a `description`.
- [ ] Every parameter has at least one constraint.
- [ ] No unconstrained `str` or `dict` parameters.
- [ ] Return type is a Pydantic model, not raw dict or str.
- [ ] Total parameters ≤ 5 (or justified split plan).
