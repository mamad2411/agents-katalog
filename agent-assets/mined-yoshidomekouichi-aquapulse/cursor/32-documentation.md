---
description: Documentation Standards (Diátaxis Framework)
alwaysApply: false
globs:
  - "docs/**/*.md"
  - "README*.md"
metadata:
  environments: cloud
---

# Documentation Standards

This file applies to all documentation in docs/ and README files.

## Diátaxis Framework

Organize documentation by user intent:

```
docs/
├── tutorials/      # Learning-oriented ("Teach me")
│   └── Example: "Getting Started with ESP32"
├── guides/         # Task-oriented ("Show me how")
│   └── Example: "How to Record Manual Events"
├── reference/      # Information-oriented ("What is")
│   └── Example: "BigQuery Schema Reference"
└── explanation/    # Understanding-oriented ("Why")
    └── Example: "Why Separate Tables for Events"
```

## When to Write What

```
User need → Category

"I want to learn X"          → tutorials/
"How do I accomplish Y?"     → guides/
"What's the spec/API?"       → reference/
"Why this approach?"         → explanation/
```

## Language Policy

**Default: English**

See `.cursor/rules/00-base.mdc` for approved exceptions.

**Current approved Japanese documents:**
- `README.ja.md`
- `docs/guides/aquarium-thermostat-complete-manual.md`

**To add new Japanese document:**
1. User MUST explicitly request
2. Document approval in `00-base.mdc`
3. Use `-ja.md` suffix (e.g., `guide-ja.md`)

## Content Rules

### Style

```
✓ Active voice: "Run the command" (not "The command should be run")
✓ Present tense: "Returns" (not "Will return")
✓ Short sentences: ≤ 25 words
✓ Concrete examples: Show real code, not placeholders
```

### Avoid

```
✗ Marketing language: "amazing", "powerful", "revolutionary"
✗ AI phrases: "Let's dive in", "In conclusion", "It's worth noting"
✗ Vague terms: "simply", "just", "easily" (without evidence)
✗ Future tense: "we will implement" (state current status)
```

### Structure

**Every document should have:**

```markdown
# H1 Title

Brief description (1-2 sentences)

## Section 1

Content...

## Section 2

Content...

## Next Steps / Related

- Link to next document
- Related references
```

## Documentation Types

### Tutorials (Learning)

**Goal:** Teach concepts through a complete example

**Structure:**
- Clear learning objectives
- Step-by-step instructions
- Expected outcomes at each step
- Troubleshooting common issues

**Example:** `tutorials/getting-started-esp32.md`

### Guides (Tasks)

**Goal:** Show how to accomplish a specific task

**Structure:**
- Prerequisites (what you need first)
- Step-by-step instructions
- Verification (how to check success)
- Troubleshooting

**Example:** `guides/record-manual-events-forms.md`

### Reference (Information)

**Goal:** Provide accurate, complete information

**Structure:**
- Technical specifications
- API documentation
- Schema definitions
- Configuration options

**Example:** `reference/schema.md`

### Explanation (Understanding)

**Goal:** Explain why things are the way they are

**Structure:**
- Context and background
- Alternatives considered
- Trade-offs and decisions
- Consequences

**Example:** `explanation/why-separate-tables.md`

## Maintenance

```
✓ Update docs in same PR as code changes
✓ Archive outdated docs (don't delete)
✓ Link to superseding content
```

### Archiving Process

```
1. Move to docs/archive/<category>/
2. Create archive/README.md explaining why
3. Link to replacement document
```

## DRY Principle

```
✗ NG: Duplicate content in multiple files
✓ OK: Write once, link elsewhere

Example:
  reference/sensors.md: DS18B20 specs (write once)
  guides/*.md: Link to reference (don't duplicate)
```

## Before Writing Documentation

Self-check:

```
[ ] Which category? (tutorial/guide/reference/explanation)
[ ] Language policy checked? (English or approved exception)
[ ] Active voice used?
[ ] Sentences < 25 words?
[ ] No AI phrases ("Let's dive in", etc.)?
[ ] Concrete examples included?
[ ] "Next steps" or "Related" section added?
```

## Code Blocks in Documentation

**Always specify language:**

```markdown
✓ Good
\`\`\`python
def hello():
    print("Hello")
\`\`\`

✗ Bad (no language specified)
\`\`\`
def hello():
    print("Hello")
\`\`\`
```

**Use appropriate language tags:**
- `python` - Python code
- `bash` - Shell commands
- `yaml` - YAML configuration
- `json` - JSON data
- `sql` - SQL queries
- `text` - Plain text output

## Links

**Prefer relative links:**

```markdown
✓ Good: [Schema Reference](../reference/schema.md)
✗ Bad: [Schema Reference](https://github.com/.../schema.md)
```

**Check links work:**
- Use `[text](path)` format
- Verify relative paths are correct
- Use anchor links for sections: `[Section](#section-name)`

## Common Mistakes

```
✗ Using "simply" or "just" (implies it's easy, may not be)
✗ Future tense in feature descriptions
✗ No code examples in technical docs
✗ Missing prerequisites in guides
✗ Duplicate content across files (violates DRY)
```
