---
name: jsdoc
description: Adds JSDoc/TSDoc comments to all public functions and types in a file
argument-hint: <file-path>
user-invocable: true
allowed-tools: Read Edit
effort: low
---

## Add JSDoc Comments

File: **$1**

1. Read the file. Identify all public functions, methods, types, and interfaces without JSDoc.

2. For each, write a JSDoc comment that includes:
   - `@description` - what it does (one sentence)
   - `@param` - each parameter with type and description
   - `@returns` - return value description
   - `@throws` - if it can throw, what and when
   - `@example` - a short usage example for non-obvious functions

Follow TSDoc format (`/** */`) for TypeScript files.

3. Rules:
   - Don't state the obvious: `// Gets the user` → write *why/when* to use it
   - Private/internal functions: add a brief comment only if logic is non-obvious
   - Don't add params that are self-explanatory single-letter generics

4. Apply all comments to the file.
