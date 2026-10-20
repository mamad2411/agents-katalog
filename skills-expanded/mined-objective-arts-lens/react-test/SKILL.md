---
name: react-test
description: "React and testing patterns"
---

# Kent C. Dodds Patterns

Apply Kent C. Dodds' philosophy and patterns for React development and testing.

## Core Philosophy

### The Testing Trophy (not Pyramid)

```
        ╱╲
       ╱  ╲     E2E (few)
      ╱────╲
     ╱      ╲   Integration (most)
    ╱────────╲
   ╱          ╲ Unit (some)
  ╱────────────╲
 ╱              ╲ Static (ESLint, TypeScript)
╱────────────────╲
```

**Key insight:** Integration tests give the best confidence-to-effort ratio.

### The Golden Rule

> "Write tests. Not too many. Mostly integration."

### Test Like Users

> "The more your tests resemble the way your software is used, the more confidence they can give you."

---

## Testing Patterns

### 1. Query Priority (in order of preference)

```javascript
// BEST: Accessible to everyone
getByRole('button', { name: /submit/i })
getByLabelText('Email')
getByPlaceholderText('Enter email')
getByText('Welcome')

// GOOD: Semantic queries
getByAltText('Profile picture')
getByTitle('Close')

// OK: Test IDs (last resort)
getByTestId('submit-button')
```

**Never use:** `container.querySelector`, DOM structure queries

### 2. User Event Over fireEvent

```javascript
// WRONG
fireEvent.click(button)
fireEvent.change(input, { target: { value: 'text' } })

// RIGHT
import userEvent from '@testing-library/user-event'

const user = userEvent.setup()
await user.click(button)
await user.type(input, 'text')
```

### 3. Avoid Implementation Details

```javascript
// WRONG - tests implementation
expect(component.state.isOpen).toBe(true)
expect(wrapper.find('Modal').props().visible).toBe(true)

// RIGHT - tests behavior
expect(screen.getByRole('dialog')).toBeInTheDocument()
expect(screen.getByText('Modal content')).toBeVisible()
```

### 4. One Assertion Per Behavior (not per test)

```javascript
// FINE - multiple assertions for one behavior
test('submitting the form shows success message', async () => {
  const user = userEvent.setup()
  render(<ContactForm />)

  await user.type(screen.getByLabelText(/email/i), 'test@example.com')
  await user.type(screen.getByLabelText(/message/i), 'Hello')
  await user.click(screen.getByRole('button', { name: /submit/i }))

  expect(screen.getByRole('alert')).toHaveTextContent(/success/i)
  expect(screen.queryByLabelText(/email/i)).not.toBeInTheDocument()
})
```

### 5. Avoid Cleanup That Hides Bugs

```javascript
// WRONG - afterEach cleanup can hide issues
afterEach(() => {
  jest.clearAllMocks()
  cleanup()
})

// RIGHT - let Testing Library auto-cleanup
// It does this automatically between tests
```

### 6. Test Error States

```javascript
test('shows error when submission fails', async () => {
  server.use(
    rest.post('/api/contact', (req, res, ctx) => {
      return res(ctx.status(500))
    })
  )

  const user = userEvent.setup()
  render(<ContactForm />)

  await user.click(screen.getByRole('button', { name: /submit/i }))

  expect(screen.getByRole('alert')).toHaveTextContent(/error/i)
})
```

---

## React Component Patterns

### 1. Compound Components

```javascript
// Instead of prop drilling
<Menu items={items} onSelect={onSelect} renderItem={renderItem} />

// Use compound components
<Menu>
  <Menu.Button>Options</Menu.Button>
  <Menu.List>
    <Menu.Item onSelect={() => {}}>Edit</Menu.Item>
    <Menu.Item onSelect={() => {}}>Delete</Menu.Item>
  </Menu.List>
</Menu>
```

### 2. Prop Collections and Getters

```javascript
function useToggle() {
  const [on, setOn] = useState(false)
  const toggle = () => setOn(o => !o)

  // Prop getter - flexible
  const getTogglerProps = (props = {}) => ({
    'aria-pressed': on,
    onClick: () => {
      props.onClick?.()
      toggle()
    },
    ...props,
  })

  return { on, toggle, getTogglerProps }
}

// Usage
const { on, getTogglerProps } = useToggle()
<button {...getTogglerProps({ onClick: customHandler })}>
  {on ? 'ON' : 'OFF'}
</button>
```

### 3. State Reducer Pattern

```javascript
function useToggle({ reducer = (state, action) => action.changes } = {}) {
  const [{ on }, dispatch] = useReducer(
    (state, action) => reducer(state, { ...action, changes: toggleReducer(state, action) }),
    { on: false }
  )

  const toggle = () => dispatch({ type: 'toggle' })
  return { on, toggle }
}

// Consumer can intercept state changes
const { on, toggle } = useToggle({
  reducer: (state, action) => {
    if (action.type === 'toggle' && clickedTooMany) {
      return state // Prevent change
    }
    return action.changes
  }
})
```

### 4. Control Props

```javascript
function useToggle({ on: controlledOn, onChange } = {}) {
  const [internalOn, setInternalOn] = useState(false)

  // Is it controlled?
  const isControlled = controlledOn !== undefined
  const on = isControlled ? controlledOn : internalOn

  const toggle = () => {
    if (!isControlled) {
      setInternalOn(o => !o)
    }
    onChange?.(!on)
  }

  return { on, toggle }
}
```

---

## Accessibility Patterns

### 1. Semantic HTML First

```javascript
// WRONG
<div onClick={handleClick}>Click me</div>

// RIGHT
<button onClick={handleClick}>Click me</button>
```

### 2. ARIA When Needed

```javascript
// Custom component needs ARIA
<div
  role="button"
  tabIndex={0}
  aria-pressed={isActive}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick()
    }
  }}
>
  Toggle
</div>
```

### 3. Labels for Inputs

```javascript
// WRONG
<input placeholder="Email" />

// RIGHT
<label>
  Email
  <input type="email" />
</label>

// OR
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// OR (visually hidden label)
<label htmlFor="search" className="sr-only">Search</label>
<input id="search" placeholder="Search..." />
```

### 4. Focus Management

```javascript
function Modal({ isOpen, onClose, children }) {
  const closeButtonRef = useRef()

  useEffect(() => {
    if (isOpen) {
      closeButtonRef.current?.focus()
    }
  }, [isOpen])

  // Trap focus inside modal
  // Return focus when closed
}
```

---

## Code Review Checklist

When reviewing React code, check:

### Testing
- [ ] Tests use accessible queries (getByRole, getByLabelText)
- [ ] Tests use userEvent, not fireEvent
- [ ] Tests check behavior, not implementation
- [ ] Error states are tested
- [ ] No mocking of implementation details

### Components
- [ ] Semantic HTML used where possible
- [ ] Form inputs have associated labels
- [ ] Interactive elements are keyboard accessible
- [ ] Custom hooks follow conventions (use* prefix)
- [ ] Props have sensible defaults

### Patterns
- [ ] No unnecessary state (derived values computed)
- [ ] Effects have correct dependencies
- [ ] Cleanup functions in effects where needed
- [ ] Error boundaries for async operations

---

## Quick Reference

| Instead of | Use |
|------------|-----|
| `fireEvent.click()` | `userEvent.click()` |
| `getByTestId()` | `getByRole()` or `getByLabelText()` |
| `wrapper.find()` | `screen.getByRole()` |
| `expect(state)` | `expect(screen.getBy...)` |
| `<div onClick>` | `<button onClick>` |
| Mock everything | Mock at network boundary |

---

## Resources

- [Testing Library Docs](https://testing-library.com)
- [Kent's Blog](https://kentcdodds.com/blog)
- [Epic React](https://epicreact.dev)
- [Common Testing Mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
