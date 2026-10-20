---
name: type-safe-skill-i-o-contracts
description: Schema-validated input/output contracts for composable Hermes skills — prevent runtime mismatches in skill chains
version: 1.0.0
author: Skillmate
license: MIT
metadata:
  hermes:
    tags: [skills, architecture, types, contracts, composability, validation]
    triggers: [skill schema, I/O contracts, skill chain, composable skills, skill validation, type safety]
    related_skills: [hermes-agent-skill-authoring, domain-modeling, mcp-server-wiring]
---

# Type-Safe Skill I/O Contracts

Extend SKILL.md frontmatter with optional `input_schema` and `output_schema` fields (JSON Schema draft-07). When a skill is loaded and invoked, the agent validates inputs against the schema before calling the skill and outputs against the schema after. This prevents silent type mismatches in skill chains — the most common source of skill-composition bugs — and makes skill interdependencies explicit, testable, and machine-readable.

## Why This Matters

- **Chain safety** — Skill A → Skill B fails at invocation time if A's output shape doesn't match B's input schema, not 5 steps later
- **Self-documenting** — The schema IS the contract: consumers see exactly what inputs/outputs to expect without reading the full skill body
- **Tool-discovery compatible** — Agents can introspect skill I/O schemas to find the right skill for a task
- **Testable** — Auto-generate fixture data from schemas for integration tests

## Trigger

When authoring, reviewing, or modifying any Hermes skill that:
- Is expected to chain with other skills (output feeds another skill's input)
- Has complex input parameters beyond a single string
- Produces structured output that another agent or skill consumes
- Lives in a domain with multiple overlapping skills (design, devops, MCP)

## Step-by-Step

### 1. Add `input_schema` and/or `output_schema` to SKILL.md frontmatter

Add optional entries under `metadata.hermes`:

```yaml
---
metadata:
  hermes:
    schema:
      input:
        type: object
        properties:
          url:
            type: string
            format: uri
            description: "The URL to extract content from"
          max_pages:
            type: integer
            default: 5
            minimum: 1
            maximum: 50
        required: [url]
      output:
        type: object
        properties:
          title:
            type: string
          content:
            type: string
          references:
            type: array
            items:
              type: string
              format: uri
        required: [title, content]
---
```

Use full JSON Schema draft-07. Keep schemas flat (max 2 levels deep) for readability. Use `description` fields on every property — they serve as inline documentation and help the agent understand parameter meaning.

### 2. Validate schemas on skill load

When the agent loads a skill that has a schema block:

```
1) Parse the frontmatter YAML
2) Validate the schema itself is valid JSON Schema (use `jsonschema.Draft7Validator.check_schema()`)
3) On first invocation, validate the actual inputs against `input_schema`
4) After the skill produces output, validate against `output_schema`
```

On validation failure, surface a clear error:
- Input mismatch: `⚠️ Skill "X" input error: missing required field "url", got: {title: "...", content: "..."}`
- Output mismatch: `⚠️ Skill "X" output error: expected array "items", got string`

### 3. Build a `validate-skill-schema` helper

Create a small standalone script or MCP tool that can be called from any skill context:

```python
import json
import yaml
import sys
from jsonschema import Draft7Validator, ValidationError
from pathlib import Path

def validate_skill_io(skill_path: str, inputs: dict = None, outputs: dict = None):
    """Load a SKILL.md and optionally validate inputs/outputs against its schema."""
    with open(skill_path) as f:
        content = f.read()
    # Parse frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {"valid": False, "error": "No frontmatter"}
    fm = yaml.safe_load(parts[1])

    schema_block = fm.get('metadata', {}).get('hermes', {}).get('schema', {})
    if not schema_block:
        return {"valid": True, "note": "No schema defined"}

    results = {}
    if 'input' in schema_block and inputs is not None:
        try:
            Draft7Validator(schema_block['input']).validate(inputs)
            results['input'] = {"valid": True}
        except ValidationError as e:
            results['input'] = {"valid": False, "error": str(e)}

    if 'output' in schema_block and outputs is not None:
        try:
            Draft7Validator(schema_block['output']).validate(outputs)
            results['output'] = {"valid": True}
        except ValidationError as e:
            results['output'] = {"valid": False, "error": str(e)}

    return {"valid": True, "results": results}
```

Requirements: `pip install pyyaml jsonschema`

### 4. Update skill authoring template to include schema block

The default skill authoring template should include a commented-out schema stub:

```yaml
# metadata:
#   hermes:
#     schema:
#       input:
#         type: object
#         properties: {}
#         required: []
#       output:
#         type: object
#         properties: {}
#         required: []
```

This reminds every skill author to consider I/O contracts.

### 5. Add schema enforcement to skill evaluation

When `validate-skill-schema` fails during a skill chain:

```
1) Log the schema mismatch with both schemas involved
2) Attempt coercion: if the output is close to the expected shape (missing a field), try to fill with defaults from the schema
3) If coercion fails, abort the chain and report the exact mismatch
```

Use the jsonschema `Draft7Validator.iter_errors()` to enumerate all mismatches, not just the first one.

## Verification

- A SKILL.md with a valid schema block parses without error
- A skill chain with matching I/O contracts completes without schema errors
- A skill chain with a deliberate type mismatch aborts with a clear error message naming both skills and the mismatched field
- The validate-skill-schema helper returns correct valid/invalid for both inputs and outputs
- Skills with no schema block are unaffected (backward compatible)

## Pitfalls

- **Over-engineering** — Do NOT add schemas to simple skills with trivial I/O (a skill that reads a file and returns its content doesn't need a contract). Add schemas only when skills chain together or have complex parameter shapes.
- **Schema drift** — When a skill's implementation changes, its I/O schema must be updated in the same PR. Missing a schema update is worse than having no schema at all.
- **Deeply nested schemas** — Keep schemas at max 2 levels deep. Deep nesting makes them unreadable in frontmatter and hard to debug. If a skill needs deeply nested I/O, that's a sign it should be split into smaller skills.
- **Performance** — Schema validation adds ~1ms per call with the jsonschema library. For high-frequency skills, cache validated schemas in memory.
- **Circular references** — JSON Schema supports `$ref` but circular refs across skill files create brittle dependencies. Prohibit `$ref` across skill boundaries in the initial implementation.

## Related Skills

- `hermes-agent-skill-authoring` — Authoring SKILL.md files (add schema block to the authoring workflow)
- `domain-modeling` — Designing the data structures that get captured in schemas
- `mcp-server-wiring` — Wiring MCP tool I/O (schema contracts align tool I/O with MCP server I/O)

## Changelog

- 1.0.0 — Initial release: schema frontmatter fields, validation helper, skill-chain enforcement
