---
name: extract-function
description: Extracts a code block into a named function with proper types and tests
argument-hint: <file-path> <line-start>-<line-end>
user-invocable: true
allowed-tools: Read Edit
effort: low
---

## Extract Function

File: **$1**
Lines: **$2**

1. Read the file, locate the specified lines.

2. Analyze the block:
   - What are the inputs? (variables read from outer scope)
   - What are the outputs? (values written to or returned)
   - What is the single responsibility of this block?

3. Propose a function name that describes what it does (verb phrase).

4. Show the extracted function with:
   - Proper TypeScript/language types
   - JSDoc if the file uses JSDoc
   - The call site replacement

5. Ask for confirmation, then:
   - Add the new function (above the calling function, or in a utils file if appropriate)
   - Replace the original block with the function call

6. Note if this function would be useful elsewhere in the codebase.
