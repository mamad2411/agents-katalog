---
name: suggest-java-fix
description: Suggests a concrete Java fix pattern for a NullPointerException given the file location and the null variable.
version: 1.0.0
category: java/debugging
level: atomic
tags: [java, fix, null-pointer, patch, refactoring]

input:
  type: object
  required: [file, line, variable]
  properties:
    file:
      type: string
      description: Java source file with the error
    line:
      type: integer
      description: Line number where NPE occurs
    variable:
      type: string
      description: Variable that is null
    code_context:
      type: string
      description: The actual Java source code around the error line

output:
  type: object
  properties:
    fix_suggestion:
      type: string
      description: Human-readable description of the root cause and recommended fix
    code_snippet:
      type: string
      description: Short Java code snippet demonstrating the fix pattern

constraints:
  host:
    os: [linux, darwin, windows]
  resources:
    memory: "512MB"
    timeout: "30s"
  safety:
    fs_access: read-only
    requires_approval: false
---

## Instructions

1. Given the file name, line number, and null variable, determine the most appropriate Java fix pattern.
2. Consider these common patterns in order of preference:
   - `if (x != null)` guard clause
   - `Objects.requireNonNull(x, "message")`
   - `Optional<T>` wrapping
   - Constructor or dependency injection initialization
   - `@NonNull` annotation + static analysis
3. Write a clear `fix_suggestion` explaining what went wrong and how to fix it.
4. Provide a concise Java `code_snippet` (5–15 lines) showing the fix in context.
5. Return ONLY the JSON with fix_suggestion and code_snippet.
