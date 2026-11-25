---
name: mock-gen
description: Generates mock data factories and API mocks for testing
argument-hint: <type-or-interface-name>
user-invocable: true
allowed-tools: Read Grep Glob Edit
effort: low
---

## Generate Mocks

Target type/interface: **$ARGUMENTS**

1. Find the type definition:
```bash
grep -rn "interface $ARGUMENTS\|type $ARGUMENTS\s*=" src/ --include="*.ts" | head -5
```

2. Read the full type definition.

3. Generate a factory function:
```ts
// Generated mock factory
export function create$ARGUMENTS(overrides?: Partial<$ARGUMENTS>): $ARGUMENTS {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    createdAt: faker.date.recent(),
    // ...all fields
    ...overrides,
  }
}
```

4. If `faker` or `@faker-js/faker` is not in the project, use inline test data patterns instead.

5. Also generate:
   - MSW handler if the project uses MSW (`src/mocks/`)
   - Array factory: `createMany$ARGUMENTS(n: number)`

6. Place in `src/__mocks__/` or `src/testing/factories/` - match project convention.
