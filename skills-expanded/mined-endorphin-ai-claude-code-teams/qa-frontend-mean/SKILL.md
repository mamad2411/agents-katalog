---
name: qa-frontend-mean
description: "Frontend testing for MEAN stack React apps. Use when writing and running tests for React components, pages, hooks, user interactions, routing, and API integration using Jest, React Testing Library, and MSW."
---

# Qa Frontend Mean

## Purpose

Write and run frontend tests for MEAN stack React applications. Cover component rendering tests, user interaction tests, hook tests, routing tests, form validation tests, and API integration tests using mocked service workers.

## Key Patterns

### Test Structure
```
client/src/
├── __tests__/
│   ├── setup.js                    # Global test setup (MSW, custom matchers)
│   └── mocks/
│       ├── handlers.js             # MSW request handlers
│       └── server.js               # MSW server setup
├── components/
│   ├── common/
│   │   ├── Button.jsx
│   │   └── Button.test.jsx         # Co-located test
│   └── features/
│       ├── LoginForm.jsx
│       └── LoginForm.test.jsx
├── pages/
│   ├── LoginPage.jsx
│   └── LoginPage.test.jsx
├── hooks/
│   ├── useAuth.js
│   └── useAuth.test.js
└── context/
    ├── AuthContext.jsx
    └── AuthContext.test.jsx
```

### Component Test Pattern (React Testing Library)
```javascript
// components/common/Button.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders children text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows spinner when loading', () => {
    render(<Button loading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.queryByText('Submit')).not.toBeInTheDocument();
  });

  it('applies variant class', () => {
    render(<Button variant="danger">Delete</Button>);
    expect(screen.getByRole('button')).toHaveClass('danger');
  });
});
```

### Page Test Pattern (with Auth Context)
```javascript
// pages/DashboardPage.test.jsx
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider } from '../context/AuthContext';
import DashboardPage from './DashboardPage';
import { server } from '../__tests__/mocks/server';
import { rest } from 'msw';

const renderWithProviders = (component, { route = '/' } = {}) => {
  return render(
    <MemoryRouter initialEntries={[route]}>
      <AuthProvider>{component}</AuthProvider>
    </MemoryRouter>
  );
};

describe('DashboardPage', () => {
  it('shows loading spinner initially', () => {
    renderWithProviders(<DashboardPage />);
    expect(screen.getByRole('status')).toBeInTheDocument(); // spinner
  });

  it('displays dashboard data after loading', async () => {
    renderWithProviders(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText(/welcome/i)).toBeInTheDocument();
    });
  });

  it('shows error message on API failure', async () => {
    server.use(
      rest.get('/api/dashboard/stats', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ success: false, error: { message: 'Server error' } }));
      })
    );
    renderWithProviders(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
    });
  });
});
```

### Form Test Pattern
```javascript
// components/features/LoginForm.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginForm from './LoginForm';

describe('LoginForm', () => {
  it('submits with valid credentials', async () => {
    const onSubmit = jest.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'Password123');
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({ email: 'test@example.com', password: 'Password123' });
    });
  });

  it('shows validation error for empty email', async () => {
    render(<LoginForm onSubmit={jest.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    });
  });

  it('disables submit button while submitting', async () => {
    const onSubmit = jest.fn(() => new Promise(resolve => setTimeout(resolve, 1000)));
    render(<LoginForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'Password123');
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    expect(screen.getByRole('button', { name: /login/i })).toBeDisabled();
  });
});
```

### MSW Mock Server Pattern
```javascript
// __tests__/mocks/handlers.js
import { rest } from 'msw';

export const handlers = [
  rest.post('/api/auth/login', (req, res, ctx) => {
    return res(ctx.json({
      success: true,
      data: { user: { id: '1', name: 'Test User', email: 'test@example.com' }, token: 'fake-jwt-token' }
    }));
  }),
  rest.get('/api/auth/me', (req, res, ctx) => {
    return res(ctx.json({
      success: true,
      data: { id: '1', name: 'Test User', email: 'test@example.com', role: 'user' }
    }));
  }),
  rest.get('/api/dashboard/stats', (req, res, ctx) => {
    return res(ctx.json({ success: true, data: { totalUsers: 100, totalPosts: 50 } }));
  }),
];

// __tests__/mocks/server.js
import { setupServer } from 'msw/node';
import { handlers } from './handlers';
export const server = setupServer(...handlers);
```

### Hook Test Pattern
```javascript
// hooks/useAuth.test.js
import { renderHook, act } from '@testing-library/react';
import { AuthProvider } from '../context/AuthContext';
import { useAuth } from './useAuth';

const wrapper = ({ children }) => <AuthProvider>{children}</AuthProvider>;

describe('useAuth', () => {
  it('returns null user initially', () => {
    const { result } = renderHook(() => useAuth(), { wrapper });
    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('sets user after login', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper });
    await act(async () => {
      await result.current.login('test@example.com', 'Password123');
    });
    expect(result.current.user).toBeDefined();
    expect(result.current.isAuthenticated).toBe(true);
  });

  it('clears user after logout', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper });
    await act(async () => { await result.current.login('test@example.com', 'Password123'); });
    act(() => { result.current.logout(); });
    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });
});
```

## Conventions

- Use Jest + React Testing Library (NOT Enzyme -- deprecated)
- Use MSW (Mock Service Worker) for API mocking -- no manual axios mocks
- Test files co-located with components: `Component.test.jsx` next to `Component.jsx`
- Query priority: getByRole > getByLabelText > getByText > getByTestId (accessibility first)
- Use `userEvent` over `fireEvent` for user interactions (more realistic)
- Wrap components needing context/router in test utilities: `renderWithProviders()`
- Test behavior, not implementation -- never test state variables or internal methods
- Every component test: renders correctly, handles user interaction, shows loading/error states
- Every form test: valid submission, validation errors, disabled during submit
- Every page test: loading state, success state, error state with retry
- Clean up: MSW handlers reset after each test

## Knowledge Strategy

- **Patterns to capture:** Test patterns for common React components (forms, lists, modals, auth flows)
- **Examples to collect:** Complete test files for standard components, MSW handler patterns
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
