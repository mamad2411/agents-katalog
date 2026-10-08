---
name: test-generator
description: Generates comprehensive unit and integration tests using Vitest and Testing Library with proper mocking, coverage, and AAA pattern. Use when writing tests, adding test coverage, or when the user mentions testing, unit tests, integration tests, or mocks.
metadata:
  version: "1.0.0"
  author: picasso
---

# Test Generator

Create thorough tests for React components, hooks, and API endpoints.

## Instructions

### 1. Unit Test Template (Component)

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  const defaultProps = {
    prop1: 'test value',
    onClick: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('rendering', () => {
    it('renders correctly with required props', () => {
      render(<ComponentName {...defaultProps} />);
      expect(screen.getByText('test value')).toBeInTheDocument();
    });

    it('applies custom className', () => {
      const { container } = render(
        <ComponentName {...defaultProps} className="custom-class" />
      );
      expect(container.firstChild).toHaveClass('custom-class');
    });
  });

  describe('interactions', () => {
    it('calls onClick when clicked', async () => {
      const user = userEvent.setup();
      render(<ComponentName {...defaultProps} />);

      await user.click(screen.getByRole('button'));

      expect(defaultProps.onClick).toHaveBeenCalledTimes(1);
    });
  });

  describe('accessibility', () => {
    it('has correct aria attributes', () => {
      render(<ComponentName {...defaultProps} />);
      expect(screen.getByRole('button')).toHaveAttribute('aria-label');
    });
  });
});
```

### 2. Hook Test Template

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useCustomHook } from './useCustomHook';

describe('useCustomHook', () => {
  describe('initial state', () => {
    it('returns initial values', () => {
      const { result } = renderHook(() => useCustomHook());

      expect(result.current.data).toBeNull();
      expect(result.current.loading).toBe(true);
      expect(result.current.error).toBeNull();
    });
  });

  describe('data fetching', () => {
    it('fetches and returns data', async () => {
      const { result } = renderHook(() => useCustomHook());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.data).toBeDefined();
    });
  });
});
```

### 3. API Route Test Template

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { NextRequest } from 'next/server';
import { GET, POST } from './route';

// Mock dependencies
vi.mock('@/lib/prisma', () => ({
  prisma: {
    resource: {
      findMany: vi.fn(),
      create: vi.fn(),
    },
  },
}));

vi.mock('next-auth', () => ({
  getServerSession: vi.fn(),
}));

describe('/api/resource', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('GET', () => {
    it('returns 401 when not authenticated', async () => {
      const request = new NextRequest('http://localhost/api/resource');
      const response = await GET(request);

      expect(response.status).toBe(401);
    });

    it('returns paginated resources', async () => {
      const request = new NextRequest('http://localhost/api/resource?page=1&limit=10');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data).toHaveProperty('data');
      expect(data).toHaveProperty('pagination');
    });
  });
});
```

### 4. Test Coverage Requirements

#### Components

- [ ] Renders without crashing
- [ ] Displays all required content
- [ ] Handles optional props gracefully
- [ ] Responds to user interactions
- [ ] Applies custom className
- [ ] Meets accessibility standards

#### Hooks

- [ ] Returns correct initial state
- [ ] Updates state correctly
- [ ] Handles side effects
- [ ] Cleans up on unmount

#### API Routes

- [ ] Returns correct status codes
- [ ] Validates input correctly
- [ ] Returns proper error responses
- [ ] Handles authentication

### 5. Mocking Patterns

```typescript
// External APIs
vi.mock('@/lib/api', () => ({
  fetchData: vi.fn().mockResolvedValue({ data: 'mocked' }),
}));

// Browser APIs
const mockLocalStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
};
Object.defineProperty(window, 'localStorage', { value: mockLocalStorage });
```

## Output Files

1. `component.test.tsx` - Component tests
2. `hook.test.ts` - Hook tests
3. `route.test.ts` - API route tests
