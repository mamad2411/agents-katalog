---
name: extract-errors
description: Parse and analyze error logs, stack traces, and build output to identify and fix issues.
---

# Extract Errors Skill

Parse and analyze error logs, stack traces, and build output to identify and fix issues.

## Process

1. **Collect**: Gather the full error output
2. **Parse**: Extract structured information:
   - Error type/code
   - File and line number
   - Stack trace
   - Error message
3. **Categorize**: Group errors by type
4. **Prioritize**: Fix root causes first (errors that cause other errors)
5. **Resolve**: Apply fixes starting from the most fundamental

## Common Error Patterns

### TypeScript
- `TS2304`: Cannot find name → Missing import or type declaration
- `TS2322`: Type not assignable → Type mismatch, check interfaces
- `TS2339`: Property does not exist → Missing property in type
- `TS7006`: Parameter implicitly has 'any' → Add type annotation

### React/Next.js
- Hydration mismatch → Server/client render differ, check dynamic content
- Module not found → Check import paths and package installation
- Hook rules violation → Hooks called conditionally or in loops

### Python
- ImportError → Module not installed or wrong path
- AttributeError → Check object type and available methods
- KeyError → Missing dictionary key, use .get() with default

### Database
- Connection refused → Check host, port, credentials
- Relation does not exist → Run migrations
- Unique constraint violation → Duplicate data, add upsert logic
