---
name: util-function
description: Creates a well-typed, tested utility function from a description
argument-hint: <description-of-what-it-should-do>
user-invocable: true
allowed-tools: Read Glob Edit
effort: low
---

## Generate Utility Function

Description: **$ARGUMENTS**

1. Check if a similar utility already exists:
```bash
grep -rn "export.*function\|export const" src/utils/ src/lib/ src/helpers/ 2>/dev/null | head -20
```

2. If a similar one exists, consider extending it instead of creating a new one.

3. Implement the function:
   - Pure function (no side effects) where possible
   - Full TypeScript generics/types
   - Handle edge cases: null, undefined, empty arrays/strings, negative numbers
   - Performance-conscious for likely large inputs

4. Write unit tests covering:
   - Normal usage
   - Edge cases
   - Type narrowing behavior

5. Place in the appropriate utils file or create `src/utils/<name>.ts`.

6. Add a usage example in JSDoc.

Example output:
```ts
/**
 * Chunks an array into smaller arrays of the specified size.
 * @example chunk([1,2,3,4,5], 2) // [[1,2],[3,4],[5]]
 */
export function chunk<T>(arr: T[], size: number): T[][] {
  if (size <= 0) return []
  return Array.from({ length: Math.ceil(arr.length / size) }, (_, i) =>
    arr.slice(i * size, i * size + size)
  )
}
```
