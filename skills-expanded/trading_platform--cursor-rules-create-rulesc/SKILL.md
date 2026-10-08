---
description: USE WHEN creating new Cursor rule files or modifying existing rules
globs: .cursor/rules/*.mdc
alwaysApply: false
---

# Creating Cursor Rules

## File Location
Always place rule files in `.cursor/rules/`:
```
.cursor/rules/
├── project-overview.mdc    # alwaysApply: true
├── python-style.mdc        # globs: app/**/*.py
├── database.mdc            # globs: app/db.py,app/models.py
├── api-clients.mdc         # globs: app/clients/*.py
└── your-new-rule.mdc
```

## Naming Convention
- Use kebab-case: `my-rule-name.mdc`
- Make names descriptive of the rule's purpose
- Always use `.mdc` extension

## Rule Structure
```mdc
---
description: Short description for agent to decide relevance
globs: path/pattern/**/*.py
alwaysApply: false
---

# Rule Title

Main content with markdown formatting.

## Section Heading

- Use bullet points for lists
- Include code examples in fenced blocks

```python
# Code example
def example():
    pass
```

@referenced-file.py
```

## Rule Types (via frontmatter)

### 1. Always Apply
```yaml
---
description: Project-wide conventions
globs: 
alwaysApply: true
---
```
Use for: Core project rules, coding standards

### 2. Auto-Attached (by file pattern)
```yaml
---
description: Python coding standards
globs: app/**/*.py,tests/**/*.py
alwaysApply: false
---
```
Use for: Language/framework-specific rules

### 3. Agent-Requested (by description)
```yaml
---
description: USE WHEN implementing authentication or security features
globs: 
alwaysApply: false
---
```
Use for: Task-specific guidance, optional patterns

## Best Practices

### Do
- Keep rules focused and concise (<500 lines)
- Include concrete code examples
- Use @filename.py to reference relevant files
- Start description with "USE WHEN" for agent-requested rules
- Test that rules are being applied (ask agent in chat)

### Don't
- Don't combine globs AND description (pick one trigger method)
- Don't duplicate information across rules
- Don't make rules too generic
- Don't forget the frontmatter YAML block
