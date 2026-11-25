---
name: repo-scanning-and-detection
description: Enumerate files, detect language/framework, and identify config/test/source directories.
---

# Repo Scanning And Detection

Enumerate files, detect language/framework, and identify config/test/source directories.

## When to Use

Use this skill when:

- Working with code in `src/scanner/index.ts/`
- User mentions "scan"
- User mentions "glob"
- User mentions "language"
- User mentions "framework"
- User mentions "config"
- User mentions "tests"

## Patterns

- glob-based enumeration with ignore filters
- language detection via extension counts and tsconfig override
- framework detection via package.json dependencies
- config and test file heuristics
- source directory inference from common roots

## Examples

```
const scanner = new Scanner(rootPath, verbose); const result = await scanner.scan();
```

## Category

**architecture** - Structural patterns and system design
