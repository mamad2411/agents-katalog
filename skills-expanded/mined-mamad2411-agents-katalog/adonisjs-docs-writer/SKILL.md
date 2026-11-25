---
name: adonisjs-docs-writer
description: AdonisJS documentation writing style guide. Use when creating, editing, or reviewing AdonisJS documentation, tutorials, guides, or API references. Provides priority-ranked patterns for document structure, code examples, tone, warnings, and explanatory writing. Includes an interview workflow for gathering requirements when creating new documentation from scratch.
---

# AdonisJS Documentation Writer

Write clear, actionable AdonisJS documentation following priority-ranked patterns.

## Core Workflow

1. **New docs**: Use the interview process in [references/interview-process.md](references/interview-process.md)
2. **Writing/editing**: Follow critical rules below, consult [references/full-guidelines.md](references/full-guidelines.md) for details

## Critical Rules (Non-Negotiable)

### Document Structure

**Feature summary before overview**: After the title, list what the guide covers as bullet points. Then write the Overview section explaining concepts.

```markdown
# Exception Handling

This guide covers exception handling in AdonisJS. You will learn how to:

- Use the global exception handler
- Customize error handling for specific types
- Report errors to logging services

## Overview

Exception handling provides a centralized system for managing errors...
```

**Start major topics with Overview**: Provide context and purpose before technical details.

### Code Examples

**No sandwich pattern**: Never explain code both before AND after. Choose one:
- Preferred: Explanation before code, with inline comments for details
- Alternative: Only inline comments within code

```markdown
<!-- CORRECT: Explanation before + inline comments -->
Named middleware receive options. This middleware checks roles and terminates early if unauthorized.

```ts title="app/middleware/authorize_middleware.ts"
export default class AuthorizeMiddleware {
  async handle(ctx: HttpContext, next: NextFn, options: AuthOptions) {
    const user = auth.getUserOrFail()
    // Check if user has required role
    if (user.role !== options.role) {
      return response.unauthorized()
    }
    await next()
  }
}
```

<!-- WRONG: Sandwich pattern -->
Let's build a middleware that checks roles.

```ts
if (user.role !== options.role) { return response.unauthorized() }
```

This code checks whether the user's role matches the required role.
```

**Complete, runnable examples**: Include all imports and realistic usage. Never use pseudo-code.

**File paths on every code block**: Use `title="path/to/file.ts"` format.

**Highlight changes**: Use `// [!code ++]` for additions, `// [!code --]` for removals.

### Warnings and Errors

**Always include solutions**: Never show a problem without a fix.

```markdown
:::warning
In order for HMR to work, you must lazy-load controllers. Static imports won't reflect changes until restart.

```ts
// Wrong - static import
import PostsController from '#controllers/posts_controller'

// Correct - lazy load
import { controllers } from '#generated/controllers'
router.get('/posts', [controllers.Posts, 'index'])
```
:::
```

### Tone and Explanation

**Explain "why" not just "what"**: Every feature needs purpose and rationale.

**Natural prose flow**: Never use labeled sections like "What it does:", "Where it lives:". Write flowing sentences.

**Confident language**: Use "will", "must", "should". Avoid hedging with "might", "possibly".

**Direct address**: Use "you" and "your" to speak to the reader.

**No em dashes**: Use periods, commas, and parentheses instead.

### Formatting

**Inline code for technical terms**: Always use backticks for code, filenames, commands.

**Tables for comparisons only**: Use options component for parameters/properties, not tables.

**Complexity labels**: Mark sections as Basic, Intermediate, or Advanced when spanning skill levels.

## Quick Reference: When to Use What

| Element | Use For |
|---------|---------|
| `:::warning` | Critical issues that cause problems |
| `:::tip` | Common gotchas, best practices |
| `:::note` | General context |
| `::::options` | Parameters, config, properties |
| Tables | Feature comparisons only |
| `// [!code ++]` | Code additions |
| `// [!code --]` | Code removals |

## Detailed Guidelines

For comprehensive rules with examples, see [references/full-guidelines.md](references/full-guidelines.md).

For the interview process when creating new documentation, see [references/interview-process.md](references/interview-process.md).