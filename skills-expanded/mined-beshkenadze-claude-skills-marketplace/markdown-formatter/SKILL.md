---
name: markdown-formatter
description: Format and structure content as clean, well-organized Markdown. Use when asked to create documentation, format text, or generate Markdown output.
version: 1.0.0
---

# Markdown Formatter

## Overview

Transforms unstructured content into clean, well-organized Markdown with proper headings, lists, code blocks, and formatting.

## Instructions

When formatting content to Markdown:

1. **Analyze the content** to identify structure (headings, lists, code, etc.)
2. **Apply hierarchy** using appropriate heading levels (H1 for title, H2 for sections)
3. **Format code** with proper language-specific syntax highlighting
4. **Create lists** for related items (bullet for unordered, numbers for sequential)
5. **Add tables** for structured data comparisons

## Formatting Rules

### Headings
- H1 (`#`) - Document title only
- H2 (`##`) - Major sections
- H3 (`###`) - Subsections
- H4+ - Avoid unless necessary

### Code Blocks
- Inline code: Single backticks for short references
- Fenced blocks: Triple backticks with language identifier

### Lists
- Bullet lists: Related but unordered items
- Numbered lists: Sequential steps or ranked items
- Nested lists: Maximum 2 levels deep

## Examples

### Example: Format API Documentation

**Input:**
"Document the getUser function that takes userId string and returns User object with name email and createdAt fields"

**Output:**
```markdown
## `getUser(userId)`

Retrieves a user by their unique identifier.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| `userId` | `string` | The unique user identifier |

### Returns

`User` object with the following properties:

- `name` - User's display name
- `email` - User's email address
- `createdAt` - Account creation timestamp
```

## Guidelines

### Do
- Keep line length under 100 characters
- Use blank lines to separate sections
- Prefer ATX-style headings (`#`) over Setext
- Use reference-style links for repeated URLs
- Include language identifier in fenced code blocks

### Don't
- Use more than 3 heading levels unless necessary
- Mix heading styles in same document
- Create deeply nested lists (max 2 levels)
- Use HTML tags when Markdown suffices
