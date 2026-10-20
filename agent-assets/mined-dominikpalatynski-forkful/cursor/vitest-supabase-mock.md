---
alwaysApply: false
---

# Vitest Supabase Chaining Mock Rule

## When to Use
Use manual `vi.fn()` mocks for services that receive Supabase client via constructor injection (dependency injection pattern).

## Core Mock Functions (Shared Across Tests)
```typescript
const createBaseMocks = () => {
  const mockSingle = vi.fn();
  const mockInsert = vi.fn();
  const mockUpdate = vi.fn();

  // KEY: Self-referential chaining - each method returns remaining methods
  const mockEq = vi.fn(() => ({ eq: mockEq, single: mockSingle }));
  const mockSelect = vi.fn(() => ({ eq: mockEq, single: mockSingle }));
  const mockFrom = vi.fn(); // Empty initially, configured per test

  return { from: mockFrom, select: mockSelect, insert: mockInsert, update: mockUpdate, eq: mockEq, single: mockSingle };
};
```

## Test Setup Pattern
```typescript
describe('Service Tests', () => {
  let service: MyService;
  let baseMocks: ReturnType<typeof createBaseMocks>;

  beforeEach(() => {
    vi.resetAllMocks();
    baseMocks = createBaseMocks();

    // Default fallback for all tables
    baseMocks.from.mockImplementation((tableName: string) => ({
      select: baseMocks.select,
      insert: baseMocks.insert,
      update: baseMocks.update,
      delete: vi.fn()
    }));

    // Create service with mock client
    const mockClient = { from: baseMocks.from } as SupabaseClientType;
    service = new MyService(mockClient);
  });

  it('should handle specific scenario', () => {
    // Override behavior for specific tables
    baseMocks.from.mockImplementation((tableName: string) => {
      if (tableName === 'my_table') {
        return { /* custom behavior */ };
      }
      return { /* fallback */ };
    });

    // Configure responses
    baseMocks.single.mockResolvedValueOnce({ data: result, error: null });

    // Test...
  });
});
```

## Key Insights
- **Self-referential chaining**: `mockEq` returns `{eq: mockEq, single: mockSingle}` to allow multiple `.eq()` calls
- **Table-specific behavior**: Use `mockImplementation` to return different objects per table
- **Shared infrastructure**: `createBaseMocks()` provides consistent chaining across all tests
- **Test isolation**: `beforeEach` resets mocks and sets up defaults, tests override as needed

## Verification Patterns
```typescript
// Verify specific call with arguments
expect(baseMocks.select).toHaveBeenNthCalledWith(1, 'id, user_id');
expect(baseMocks.eq).toHaveBeenNthCalledWith(2, 'id', recordId);

// Verify total call counts
expect(baseMocks.from).toHaveBeenCalledTimes(2); // 2 queries made
expect(baseMocks.eq).toHaveBeenCalledTimes(3);   // 3 eq() calls total
expect(baseMocks.single).toHaveBeenCalledTimes(2); // 2 single() calls
```

## Advanced: Complex Table-Specific Overrides
```typescript
baseMocks.from.mockImplementation((tableName: string) => {
  if (tableName === 'recipes') {
    return {
      insert: vi.fn().mockReturnValue({
        select: vi.fn().mockReturnValue({
          single: vi.fn().mockResolvedValue(insertResult)
        })
      }),
      select: baseMocks.select,
      delete: vi.fn().mockReturnValue({ eq: vi.fn().mockResolvedValue({}) })
    };
  }
  // Fallback for other tables...
});
```
