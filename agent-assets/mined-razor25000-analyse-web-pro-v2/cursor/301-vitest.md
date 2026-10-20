---
description: 
globs: 
alwaysApply: false
---
## Context

- Create a new component with a tests inside the folder `/__tests__`.
- Use ONLY the folder that is in the root of the projects `/__tests__`
- Fix the test or the component until the command `pnpm test:ci <name-of-the-file>` work

## React Tests

```tsx
import { setup } from "../test/setup";
import { screen, waitFor } from "@testing-library/react";

describe("ComponentName", () => {
  it("should do...", async () => {
    const { user } = setup(<DialogManagerWrapper />);

    // Use `screen` for element retreiving
    // Use `user` to interact with the page
  })
})
```