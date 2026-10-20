---
description: Create components using Test-Driven Development (TDD) principles
---

# TDD Unit Component Development

Create React components following Test-Driven Development principles.

## Context

- Create components following TDD principles
- Only for components without integration tests (no database)
- Write tests FIRST, then implement the component

## Workflow

1. **Plan** - Define component location, name, and functionality
2. **Create test file** in `__tests__` folder
3. **Create component** in appropriate folder (e.g., `src/features/`)
4. **Run tests** with `pnpm test:ci`
5. **Iterate** - Fix component until tests pass

## Test Structure

```tsx
import { setup } from "../test/setup";
import { screen, waitFor } from "@testing-library/react";

describe("ComponentName", () => {
  it("should do...", async () => {
    const { user } = setup(<ComponentName />);
    // Test implementation
  });
});
```

Create a component using TDD for: $ARGUMENTS
