---
name: component-testing-patterns
description: Test React components — unit tests, integration tests, accessibility tests, visual regression
triggers: [component testing, React testing, test components, Vitest, Jest, Testing Library]
---

# SKILL: Component Testing Patterns

## Testing Philosophy

```
1. Test behavior, not implementation
2. Test what users see and do
3. Avoid testing internal state
4. Write tests that give confidence
```

## Setup (Vitest + Testing Library)
```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect } from 'vitest'

// Component under test
function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>
}
```

## Pattern 1: Basic Rendering Test
```tsx
it('renders button with correct text', () => {
  render(<Button>Click me</Button>)
  
  // Query by text (what user sees)
  expect(screen.getByText('Click me')).toBeInTheDocument()
  
  // Query by role (accessibility-first)
  expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument()
})
```

## Pattern 2: User Interaction Test
```tsx
it('calls onClick when clicked', async () => {
  const handleClick = vi.fn()  // Mock function
  const user = userEvent.setup()  // Setup user interactions
  
  render(<Button onClick={handleClick}>Click me</Button>)
  
  // Simulate user click
  await user.click(screen.getByRole('button'))
  
  expect(handleClick).toHaveBeenCalledTimes(1)
})
```

## Pattern 3: Form Testing
```tsx
function LoginForm({ onSubmit }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  
  return (
    <form onSubmit={(e) => { e.preventDefault(); onSubmit({ email, password }) }}>
      <label htmlFor="email">Email</label>
      <input id="email" type="email" value={email} onChange={e => setEmail(e.target.value)} />
      
      <label htmlFor="password">Password</label>
      <input id="password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      
      <button type="submit">Login</button>
    </form>
  )
}

it('submits form with email and password', async () => {
  const handleSubmit = vi.fn()
  const user = userEvent.setup()
  
  render(<LoginForm onSubmit={handleSubmit} />)
  
  // Type into inputs
  await user.type(screen.getByLabelText('Email'), 'user@example.com')
  await user.type(screen.getByLabelText('Password'), 'password123')
  
  // Submit form
  await user.click(screen.getByRole('button', { name: 'Login' }))
  
  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'user@example.com',
    password: 'password123'
  })
})
```

## Pattern 4: Async Data Loading
```tsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => { setUser(data); setLoading(false) })
  }, [userId])
  
  if (loading) return <div>Loading...</div>
  return <div>{user.name}</div>
}

it('loads and displays user', async () => {
  // Mock fetch
  global.fetch = vi.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({ name: 'John Doe' })
    })
  )
  
  render(<UserProfile userId="123" />)
  
  // Initially loading
  expect(screen.getByText('Loading...')).toBeInTheDocument()
  
  // Wait for async operation
  expect(await screen.findByText('John Doe')).toBeInTheDocument()
  
  expect(fetch).toHaveBeenCalledWith('/api/users/123')
})
```

## Pattern 5: Accessibility Testing
```tsx
import { axe, toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)

it('has no accessibility violations', async () => {
  const { container } = render(<Button>Click me</Button>)
  
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

## Pattern 6: Visual Regression (Playwright)
```ts
import { test, expect } from '@playwright/test'

test('button looks correct', async ({ page }) => {
  await page.goto('/components/button')
  
  // Take screenshot
  await expect(page.locator('button')).toHaveScreenshot('button.png')
  
  // Compare with baseline
  // Fails if visual differences detected
})
```

## Quality Checks
- [ ] Components tested with Testing Library (not Enzyme)
- [ ] Tests query by role/label (not test IDs)
- [ ] User interactions use userEvent (not fireEvent)
- [ ] Async tests use findBy* (not waitFor)
- [ ] Accessibility tested with jest-axe
- [ ] Test coverage > 80%
- [ ] Tests are readable (describe what they test)
- [ ] No implementation details tested (internal state)
