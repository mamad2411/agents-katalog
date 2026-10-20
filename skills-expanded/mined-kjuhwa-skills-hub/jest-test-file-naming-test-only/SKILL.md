---
tags: [frontend, jest, test, file, naming, only]
name: jest-test-file-naming-test-only
description: Use .test.ts naming (not .spec.ts) and explicitly import jest globals; .spec.ts is excluded from the runner
source_project: lucida-builder-r3
version: 1.0.0
category: frontend
---

# Jest naming & globals

## Trigger
- Adding a new Jest test file.
- Debugging a "test file not detected" report.

## Steps
1. Name test files `{subject}.test.ts` (or `.test.tsx`). Do **not** use `.spec.ts` — the Jest config excludes it.
2. Place the test in the same folder as its subject.
3. Explicitly import jest globals:
   ```ts
   import { describe, it, expect } from "@jest/globals";
   ```
4. Write three case classes per function: normal, boundary (empty/min/max), exception (invalid input).
5. Use `jest.mock`, `jest.fn`, `jest.spyOn` for isolation.
6. Check coverage stays within the project's 80% threshold (branches/functions/lines/statements).
