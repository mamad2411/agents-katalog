# Agent Instructions

**Version:** 1.0.0  
**Purpose:** Comprehensive instructions for autonomous AI agents working on CouponManager  
**Last Updated:** 2025-01-23

---

## Agent Capabilities and Limitations

### What the Agent Can Do

| Capability | Description |
|------------|-------------|
| **Code Generation** | Create new components, services, hooks, and utilities following project standards |
| **Code Modification** | Update existing code while maintaining compatibility and standards |
| **Testing** | Write unit and integration tests using Vitest and React Testing Library |
| **Documentation** | Update and create documentation files in markdown format |
| **Refactoring** | Improve code structure while maintaining functionality |
| **Bug Fixes** | Identify and resolve issues in existing code |
| **Type Definitions** | Create and update TypeScript interfaces and types |

### What the Agent Should NOT Do

| Restriction | Reason |
|-------------|--------|
| **Do not modify `.gitignore`** | Version control configuration is manually managed |
| **Do not modify package versions** | Dependencies are managed by maintainers |
| **Do not create new database migrations** | Migrations require manual review and testing |
| **Do not modify CI/CD workflows** | GitHub Actions workflows require manual approval |
| **Do not access external APIs** | Only interact with Supabase via configured services |
| **Do not modify environment files** | `.env` files contain sensitive data |
| **Do not create new design patterns** | Follow established patterns in the codebase |
| **Do not bypass factory pattern** | Always use factory methods to get service instances |

---

## Workflow Guidelines

### How to Approach New Features

1. **Understand Requirements**
   - Read the issue or feature description carefully
   - Identify affected components and services
   - Determine required permissions and roles

2. **Plan the Implementation**
   - Identify which files need to be created or modified
   - Consider the impact on existing functionality
   - Plan tests before writing code

3. **Follow the Layered Architecture**
   - Start with data layer (types, services)
   - Implement service layer logic
   - Create/update components
   - Add context providers if needed

4. **Use Factory Pattern**
   - Always access services via factory methods
   - Example: `const service = await getAuthService()`
   - Never directly instantiate service implementations

5. **Write Tests**
   - Write tests alongside code (TDD preferred)
   - Aim for ≥ 80% coverage
   - Follow AAA pattern (Arrange, Act, Assert)

6. **Update Documentation**
   - Update relevant documentation files
   - Add code comments for complex logic
   - Update type definitions

### How to Approach Bug Fixes

1. **Reproduce the Issue**
   - Understand the expected vs actual behavior
   - Identify the root cause
   - Check related tests

2. **Isolate the Problem**
   - Identify the affected layer (component, service, data)
   - Check for type errors
   - Verify permission checks

3. **Implement the Fix**
   - Make minimal changes to fix the issue
   - Ensure no side effects on other features
   - Add or update tests to prevent regression

4. **Verify the Fix**
   - Run all tests
   - Check coverage
   - Test in both development and production modes

### How to Approach Refactoring

1. **Understand Existing Code**
   - Read the current implementation
   - Identify code smells or violations of standards
   - Consider the impact on dependent code

2. **Plan Refactoring**
   - Break down into small, safe changes
   - Ensure tests exist before refactoring
   - Consider backward compatibility

3. **Execute Incrementally**
   - Make one change at a time
   - Run tests after each change
   - Commit frequently with descriptive messages

4. **Maintain Functionality**
   - Ensure no behavior changes
   - Update tests if API changes
   - Update documentation

### How to Approach Documentation Updates

1. **Identify Affected Documentation**
   - Core docs: [`ARCHITECTURE.md`](../docs/ARCHITECTURE.md:1), [`CODING_STANDARDS.md`](../docs/CODING_STANDARDS.md:1), [`CONTRIBUTING.md`](../docs/CONTRIBUTING.md:1)
   - Feature docs: [`data-models.md`](../docs/data-models.md:1), [`permission-matrix.md`](../docs/permission-matrix.md:1), etc.

2. **Update Authoritative Documents First**
   - Start with core documentation
   - Ensure consistency across all docs
   - Update cross-references

3. **Use Clear Formatting**
   - Use markdown headings and lists
   - Include code examples
   - Add diagrams where helpful

4. **Regenerate Diagrams**
   - Run `pnpm generate-diagrams` after updating diagrams
   - Verify diagram accuracy

---

## Code Quality Standards

### TypeScript Strict Mode Compliance

All code must comply with TypeScript strict mode:

```typescript
// ✅ Correct - Explicit types
const formatDate = (date: string, locale: string = 'en-US'): string => {
  return new Date(date).toLocaleDateString(locale);
};

// ❌ Incorrect - Implicit any
function processData(data) {
  return data.map(item => item.value);
}

// ✅ Correct - Explicit null check
const coupon = coupons.find(c => c.id === id);
if (coupon) {
  console.log(coupon.retailer);
}

// ❌ Incorrect - Potential null reference
const coupon = coupons.find(c => c.id === id);
console.log(coupon.retailer);
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `CouponList`, `AddCouponForm` |
| Services | PascalCase | `CouponService`, `AuthService` |
| Factories | PascalCase + Factory suffix | `CouponServiceFactory` |
| Contexts | PascalCase + Context suffix | `AuthContext` |
| Hooks | use + PascalCase | `useCoupons`, `useAuth` |
| Types/Interfaces | PascalCase | `Coupon`, `CouponFormData` |
| Variables | camelCase | `userId`, `isActive` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| Files | PascalCase (components), camelCase (utilities) | `CouponList.tsx`, `dateUtils.ts` |

### Testing Requirements

1. **Test File Naming**
   - Component tests: `ComponentName.test.tsx`
   - Service tests: `ServiceName.test.ts`
   - Real tests (with actual backend): `*.real.test.tsx` or `*.real.test.ts`
   - Mobile-specific tests: `*.mobile.test.tsx`

2. **Test Structure (AAA Pattern)**
```typescript
describe('CouponService', () => {
  it('should add a new coupon', async () => {
    // Arrange
    const service = getCouponService();
    const couponData: CouponFormData = {
      retailer: 'Amazon',
      initialValue: '50'
    };

    // Act
    const result = await service.addCoupon(couponData, 'user-123');

    // Assert
    expect(result).toBeDefined();
    expect(result.retailer).toBe('Amazon');
    expect(result.userId).toBe('user-123');
  });
});
```

3. **Coverage Requirements**
   - Minimum 80% code coverage
   - All critical paths must be tested
   - Edge cases should be covered

### Documentation Requirements

1. **File Header Comments**
```typescript
/**
 * Brief description of the file purpose
 *
 * @module ComponentName/ServiceName
 * @description Detailed description of what this file does
 */
```

2. **Function Documentation**
```typescript
/**
 * Adds a new coupon to the system
 *
 * @param couponData - The coupon data to add
 * @param userId - The ID of the user adding the coupon (optional)
 * @returns Promise<Coupon> The created coupon with generated ID
 * @throws {Error} If coupon data is invalid
 */
async addCoupon(couponData: CouponFormData, userId?: string | null): Promise<Coupon>
```

3. **Inline Comments**
   - Use comments to explain "why", not "what"
   - Comment complex logic
   - Comment workarounds or temporary solutions

---

## File Modification Rules

### Files That Can Be Modified

| Directory/File | Modification Allowed | Notes |
|----------------|---------------------|-------|
| `src/components/*.tsx` | ✅ Yes | React components |
| `src/services/*.ts` | ✅ Yes | Service implementations |
| `src/services/*.tsx` | ✅ Yes | Context providers |
| `src/types/index.ts` | ✅ Yes | Type definitions |
| `src/locales/**/*.json` | ✅ Yes | Translation files |
| `src/test/**/*.test.tsx` | ✅ Yes | Test files |
| `src/test/**/*.test.ts` | ✅ Yes | Test files |
| `docs/*.md` | ✅ Yes | Documentation |
| `.cursor/*.md` | ✅ Yes | AI configuration |

### Files That Should NOT Be Modified

| Directory/File | Reason |
|----------------|--------|
| `.gitignore` | Version control configuration |
| `package.json` | Dependency management (maintainers only) |
| `pnpm-lock.yaml` | Lock file (auto-generated) |
| `.env` | Contains sensitive data |
| `.env.example` | Environment template |
| `tsconfig.json` | TypeScript configuration (maintainers only) |
| `vite.config.ts` | Build configuration (maintainers only) |
| `vitest.config.ts` | Test configuration (maintainers only) |
| `.github/workflows/*` | CI/CD workflows (maintainers only) |
| `migrations/sql/*.sql` | Database migrations (maintainers only) |

### When to Create New Files

1. **Create New Component** when:
   - Adding a new UI feature
   - Extracting complex UI logic
   - Reusable UI component needed

2. **Create New Service** when:
   - Adding new business logic
   - Abstracting data access
   - Implementing new API integration

3. **Create New Hook** when:
   - Reusable stateful logic needed
   - Complex component state management
   - Shared side effects

4. **Create New Type** when:
   - New data structure needed
   - API response types
   - Component prop types

### When to Delete Files

1. **Delete Component** when:
   - Feature is being removed
   - Component is no longer used
   - Replaced by a better implementation

2. **Delete Service** when:
   - Functionality is being removed
   - Service is consolidated into another

3. **Delete Test** when:
   - Corresponding code is deleted
   - Test is superseded by a better test

**Warning:** Always verify file is not imported elsewhere before deletion.

---

## Error Handling Guidelines

### How to Handle Errors in Services

1. **Use Try-Catch for Async Operations**
```typescript
async addCoupon(couponData: CouponFormData, userId?: string | null): Promise<Coupon> {
  try {
    // Validate input
    if (!couponData.retailer || !couponData.initialValue) {
      throw new Error('Retailer and initial value are required');
    }

    // Execute operation
    const result = await this.db.insert(couponData);
    return result;
  } catch (error) {
    console.error('Error adding coupon:', error);
    throw new Error(`Failed to add coupon: ${error.message}`);
  }
}
```

2. **Return Consistent Error Objects**
```typescript
interface ServiceError {
  message: string;
  code?: string;
  details?: any;
}

// Return error object
return {
  data: null,
  error: {
    message: 'Coupon not found',
    code: 'NOT_FOUND'
  }
};
```

3. **Log Errors Appropriately**
```typescript
// Log with context
console.error('CouponService.addCoupon failed:', {
  userId,
  couponData,
  error: error.message,
  stack: error.stack
});
```

### How to Handle Errors in Components

1. **Use Error Boundaries for Component Errors**
```typescript
// Wrap components that might throw errors
<ErrorBoundary fallback={<ErrorMessage />}>
  <CouponList />
</ErrorBoundary>
```

2. **Handle Service Errors Gracefully**
```typescript
const handleSubmit = async () => {
  try {
    await service.addCoupon(couponData, user.id);
    // Show success message
  } catch (error) {
    // Show error message to user
    setError(error.message);
  }
};
```

3. **Provide User-Friendly Error Messages**
```typescript
// Translate error messages
const errorMessage = t('errors.coupon.addFailed', {
  defaultMessage: 'Failed to add coupon. Please try again.'
});
```

### How to Handle Async Errors

1. **Always Await Async Operations**
```typescript
// ✅ Correct
const coupon = await service.getCoupon(id);

// ❌ Incorrect - Promise not awaited
const coupon = service.getCoupon(id);
```

2. **Handle Promise Rejections**
```typescript
// Using try-catch
try {
  const result = await service.operation();
} catch (error) {
  // Handle error
}

// Using .catch()
service.operation()
  .then(result => {
    // Handle success
  })
  .catch(error => {
    // Handle error
  });
```

3. **Use Async/Await Over Promises**
```typescript
// ✅ Preferred - Async/await
async function loadCoupons() {
  const coupons = await service.getAllCoupons();
  return coupons;
}

// ⚠️ Acceptable - Promise chain
function loadCoupons() {
  return service.getAllCoupons()
    .then(coupons => coupons);
}
```

### How to Handle Validation Errors

1. **Validate Input Before Processing**
```typescript
function validateCouponData(data: CouponFormData): void {
  if (!data.retailer || data.retailer.trim() === '') {
    throw new ValidationError('Retailer is required');
  }
  if (!data.initialValue || isNaN(parseFloat(data.initialValue))) {
    throw new ValidationError('Initial value must be a valid number');
  }
}
```

2. **Return Validation Errors to User**
```typescript
const handleSubmit = () => {
  try {
    validateCouponData(couponData);
    service.addCoupon(couponData);
  } catch (error) {
    if (error instanceof ValidationError) {
      setFieldError(error.field, error.message);
    }
  }
};
```

3. **Use Form Validation Libraries**
```typescript
// Example with Material-UI validation
<TextField
  label="Retailer"
  value={retailer}
  onChange={(e) => setRetailer(e.target.value)}
  error={!!errors.retailer}
  helperText={errors.retailer}
  required
/>
```

---

## Testing Guidelines

### Test File Naming Conventions

| Pattern | Purpose | Example |
|---------|---------|---------|
| `ComponentName.test.tsx` | Component unit tests | `CouponList.test.tsx` |
| `ServiceName.test.ts` | Service unit tests | `CouponService.test.ts` |
| `*.real.test.tsx` | Tests with real backend | `LanguageContext.real.test.tsx` |
| `*.mobile.test.tsx` | Mobile-specific tests | `CouponList.mobile.test.tsx` |

### Test Structure (AAA Pattern)

```typescript
describe('CouponService', () => {
  describe('addCoupon', () => {
    it('should add a new coupon successfully', async () => {
      // Arrange - Set up test data and mocks
      const service = getCouponService();
      const couponData: CouponFormData = {
        retailer: 'Amazon',
        initialValue: '50',
        currentValue: '50'
      };
      const userId = 'user-123';

      // Act - Execute the function being tested
      const result = await service.addCoupon(couponData, userId);

      // Assert - Verify the expected outcome
      expect(result).toBeDefined();
      expect(result.id).toBeDefined();
      expect(result.retailer).toBe('Amazon');
      expect(result.userId).toBe(userId);
    });
  });
});
```

### Mock Usage Patterns

1. **Mock Service Dependencies**
```typescript
import { vi } from 'vitest';

// Mock a service
vi.mock('../services/AuthService', () => ({
  default: {
    getUser: vi.fn().mockResolvedValue({ id: 'user-123', role: 'user' })
  }
}));
```

2. **Mock API Calls**
```typescript
// Using MSW for API mocking
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/coupons', (req, res, ctx) => {
    return res(ctx.json(mockCoupons));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

3. **Mock React Context**
```typescript
import { render } from '@testing-library/react';
import { AuthContext } from '../services/AuthContext';

const mockAuthContext = {
  user: { id: 'user-123', email: 'test@example.com', role: 'user' },
  login: vi.fn(),
  logout: vi.fn()
};

render(
  <AuthContext.Provider value={mockAuthContext}>
    <YourComponent />
  </AuthContext.Provider>
);
```

### Coverage Requirements

1. **Minimum 80% Coverage**
   - Enforced via CI/CD pipeline
   - Check coverage with: `pnpm test:coverage`

2. **Critical Path Coverage**
   - All user-facing features must be tested
   - Error handling must be tested
   - Permission checks must be tested

3. **Edge Case Testing**
   - Test with empty data
   - Test with invalid data
   - Test boundary conditions
   - Test error scenarios

---

## Cross-References

- **Project Context:** [`.cursor/PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md:1)
- **Dependency Mapping:** [`.cursor/DEPENDENCY_MAPPING.md`](DEPENDENCY_MAPPING.md:1)
- **Workflow Constraints:** [`.cursor/WORKFLOW_CONSTRAINTS.md`](WORKFLOW_CONSTRAINTS.md:1)
- **Quick Reference:** [`.cursor/QUICK_REFERENCE.md`](QUICK_REFERENCE.md:1)
- **Coding Standards:** [`../docs/CODING_STANDARDS.md`](../docs/CODING_STANDARDS.md:1)
- **Contribution Guidelines:** [`../docs/CONTRIBUTING.md`](../docs/CONTRIBUTING.md:1)

---

**End of Agent Instructions**
