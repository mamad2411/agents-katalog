---
description: Comprehensive guide for creating and managing Cursor rules
globs: [".cursor/rules/**/*.mdc"]
alwaysApply: false
---
# Cursor Rules Guide

Quick reference for creating and managing Cursor rules.

## Creation Process

**Use `edit_file` tool** - Cursor auto-adds YAML frontmatter
1. Target: `.cursor/rules/rule-name.mdc`
2. Add content only (no YAML needed)
3. Verify in Cursor editor (not terminal `cat`)

## Rule Types

```yaml
# Always Rules (everywhere)
alwaysApply: true

# Auto-Attached (file patterns)
globs: ["pattern/**/*"]
alwaysApply: false

# Agent-Requested (AI decides)
description: "Detailed description for AI selection"
alwaysApply: false
```

## Common Glob Patterns

```yaml
# Testing
globs: ["**/*.test.*", "tests/**", "**/jest.config.*", "**/playwright.config.*"]

# Authentication  
globs: ["**/auth/**", "lib/auth*", "middleware.ts", "app/api/auth/**"]

# API Routes
globs: ["app/api/**", "**/*route.ts"]

# Components
globs: ["components/**", "**/*.tsx", "app/**/page.tsx"]

# Database
globs: ["prisma/**", "lib/prisma*"]

# Deployment
globs: ["fly.toml", "Dockerfile", "ecosystem.config.js"]

# Config Files
globs: ["eslint.config.*", "prettier.config.*"]
```

## Content Structure

```markdown
# Rule Title

## Quick Commands
Essential CLI commands

## Procedures  
Step-by-step instructions

## Common Patterns
Code conventions

## Error Handling
Common issues and fixes
```

## Best Practices

- **Concise**: Under 200 lines
- **Actionable**: Focus on "what to do"
- **Structured**: Consistent headings
- **Current**: Exact commands and paths
- Use `@filename` for file references

## Troubleshooting

- **Empty files**: Use `edit_file` to add content
- **Not auto-attaching**: Check glob patterns match file paths
- **Content missing**: Open in Cursor editor, not terminal
