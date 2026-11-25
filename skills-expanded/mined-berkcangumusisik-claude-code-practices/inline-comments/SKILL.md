---
name: inline-comments
description: Adds inline comments to complex or non-obvious code sections
argument-hint: <file-path>
user-invocable: true
allowed-tools: Read Edit
effort: low
---

## Add Inline Comments

File: **$1**

1. Read the file. Identify sections that are non-obvious:
   - Complex algorithms or math
   - Regex patterns
   - Bitwise operations
   - Non-intuitive business logic
   - Workarounds or known limitations
   - Performance-sensitive sections

2. Write comments that explain the **why**, not the **what**:
   ```ts
   // ❌ Bad: increment counter
   count++

   // ✅ Good: offset by 1 because API uses 1-based page numbering
   page = requestedPage + 1
   ```

3. For workarounds, use this format:
   ```ts
   // HACK: Safari doesn't support X, so we Y instead
   // TODO: remove when Safari 18 becomes baseline
   ```

4. Don't comment obvious code. If code needs a comment to be understood, also consider if it should be refactored instead.

5. Apply comments. Show before/after diff.
