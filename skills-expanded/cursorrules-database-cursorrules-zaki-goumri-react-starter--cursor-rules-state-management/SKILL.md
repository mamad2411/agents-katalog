# Jotai State Management Rules
# Essential Patterns and Principles

## 🎯 CORE PRINCIPLES
1. **Think Atomic**: Break state into smallest possible units
2. **Bottom-Up Composition**: Combine atoms to create derived state  
3. **TypeScript-First**: Always type atoms properly
4. **Performance-Focused**: Minimize re-renders through atomic subscriptions
5. **Pure Functions**: Atoms are pure, making them predictable and testable

## 🏗️ ARCHITECTURE PATTERNS

### File Structure
```
atoms/
├── auth.ts        # Authentication state
├── ui.ts          # UI/theme state  
├── api.ts         # Server state
├── derived.ts     # Computed values
└── index.ts       # Export all atoms
```

### Atom Naming Convention
```typescript
// ✅ GOOD - Clear, descriptive names
export const userAtom = atom<User | null>(null)
export const isLoadingAtom = atom<boolean>(false)
export const themeAtom = atom<'light' | 'dark'>('light')

// Derived atoms end with computed values
export const userDisplayNameAtom = atom((get) => ...)
export const cartTotalAtom = atom((get) => ...)

// Action atoms are verbs
export const loginAtom = atom(null, async (get, set, credentials) => ...)
export const logoutAtom = atom(null, (get, set) => ...)
```

## ⚛️ ATOM PATTERNS

### 1. Primitive Atoms
```typescript
// Simple state atoms with proper typing
export const userAtom = atom<User | null>(null)
export const countAtom = atom<number>(0)
export const themeAtom = atom<'light' | 'dark'>('light')
```

### 2. Derived Atoms (Read-Only)
```typescript
// Computed values based on other atoms
export const userNameAtom = atom((get) => {
  const user = get(userAtom)
  return user ? `${user.firstName} ${user.lastName}` : 'Guest'
})

export const cartTotalAtom = atom((get) => {
  const items = get(cartItemsAtom)
  return items.reduce((total, item) => total + item.price * item.quantity, 0)
})
```

### 3. Write-Only Atoms (Actions)
```typescript
// Actions that modify state
export const incrementAtom = atom(
  null,
  (get, set) => set(countAtom, c => c + 1)
)

export const loginAtom = atom(
  null, 
  async (get, set, credentials: LoginData) => {
    set(isLoadingAtom, true)
    try {
      const user = await api.login(credentials)
      set(userAtom, user)
    } finally {
      set(isLoadingAtom, false)
    }
  }
)
```

### 4. Read-Write Atoms
```typescript
// Atoms with custom read/write logic
export const doubledAtom = atom(
  (get) => get(countAtom) * 2,
  (get, set, newValue: number) => set(countAtom, newValue / 2)
)
```

### 5. Async Atoms
```typescript
// Server state management
export const todosAtom = atom(async () => {
  const response = await fetch('/api/todos')
  return response.json()
})

// With error handling
export const postsAtom = atom(async () => {
  try {
    const response = await fetch('/api/posts')
    if (!response.ok) throw new Error('Failed to fetch')
    return response.json()
  } catch (error) {
    throw new Error(`Posts error: ${error.message}`)
  }
})
```

### 6. Atom Families (Dynamic Atoms)
```typescript
import { atomFamily } from 'jotai/utils'

// Create atoms dynamically based on parameters
export const postAtomFamily = atomFamily((id: string) =>
  atom(async () => {
    const response = await fetch(`/api/posts/${id}`)
    return response.json()
  })
)

export const formFieldFamily = atomFamily((fieldName: string) =>
  atom<string>('')
)
```

## 🎣 HOOK PATTERNS

### Basic Usage Hooks
```typescript
import { useAtom, useAtomValue, useSetAtom } from 'jotai'

export function useAuth() {
  const user = useAtomValue(userAtom)
  const login = useSetAtom(loginAtom)
  const logout = useSetAtom(logoutAtom)
  
  return {
    user,
    isAuthenticated: !!user,
    login,
    logout
  }
}

export function useCounter() {
  const [count, setCount] = useAtom(countAtom)
  const increment = useSetAtom(incrementAtom)
  
  return { count, setCount, increment }
}
```

### Async Data Hooks
```typescript
import { loadable } from 'jotai/utils'

export function useTodos() {
  const todosLoadable = useAtomValue(loadable(todosAtom))
  
  return {
    todos: todosLoadable.state === 'hasData' ? todosLoadable.data : [],
    isLoading: todosLoadable.state === 'loading',
    error: todosLoadable.state === 'hasError' ? todosLoadable.error : null
  }
}
```

## 🔄 COMMON PATTERNS

### Loading States
```typescript
export const isLoadingAtom = atom<boolean>(false)
export const errorAtom = atom<string | null>(null)

export const fetchDataAtom = atom(
  null,
  async (get, set) => {
    set(isLoadingAtom, true)
    set(errorAtom, null)
    
    try {
      const data = await api.fetchData()
      set(dataAtom, data)
    } catch (error) {
      set(errorAtom, error.message)
    } finally {
      set(isLoadingAtom, false)
    }
  }
)
```

### Form State
```typescript
export const formDataAtom = atom<FormData>({})
export const formErrorsAtom = atom<Record<string, string>>({})

export const updateFieldAtom = atom(
  null,
  (get, set, { field, value }: { field: string, value: any }) => {
    set(formDataAtom, prev => ({ ...prev, [field]: value }))
    // Clear error when field is updated
    set(formErrorsAtom, prev => {
      const { [field]: removed, ...rest } = prev
      return rest
    })
  }
)
```

### Persistence
```typescript
import { atomWithStorage } from 'jotai/utils'

// Automatically syncs with localStorage
export const themeAtom = atomWithStorage<'light' | 'dark'>('theme', 'light')
export const userPrefsAtom = atomWithStorage('user-prefs', {
  language: 'en',
  notifications: true
})
```

### Reset Pattern
```typescript
export const RESET = Symbol('reset')

export const resettableAtom = atom(
  initialValue,
  (get, set, newValue) => {
    if (newValue === RESET) {
      set(resettableAtom, initialValue)
    } else {
      set(resettableAtom, newValue)
    }
  }
)

// Usage: set(resettableAtom, RESET)
```

## 🚫 ANTI-PATTERNS

### ❌ Don't Create Monolithic Atoms
```typescript
// BAD - One big atom for everything
const appStateAtom = atom({
  user: null,
  theme: 'light',
  todos: [],
  loading: false,
  // ... huge object
})

// GOOD - Separate concerns
const userAtom = atom(null)
const themeAtom = atom('light')
const todosAtom = atom([])
const loadingAtom = atom(false)
```

### ❌ Don't Mutate Atom Values
```typescript
// BAD - Direct mutation
const mutateAtom = atom(
  null,
  (get, set) => {
    const todos = get(todosAtom)
    todos.push(newTodo) // Mutation!
    set(todosAtom, todos)
  }
)

// GOOD - Immutable updates
const addTodoAtom = atom(
  null,
  (get, set, newTodo) => {
    const todos = get(todosAtom)
    set(todosAtom, [...todos, newTodo])
  }
)
```

### ❌ Don't Use Atoms for Component-Local State
```typescript
// BAD - Using atoms for local UI state
const modalOpenAtom = atom(false) // If only one component needs this

// GOOD - Use useState for component-local state
function MyComponent() {
  const [isOpen, setIsOpen] = useState(false)
  // Only use atoms for shared state
}
```

## 🎯 IMPLEMENTATION RULES

1. **Start Small**: Begin with primitive atoms, compose into derived atoms
2. **Single Responsibility**: Each atom should manage one piece of state
3. **Type Everything**: Always provide TypeScript types for atoms
4. **Use Loadable**: Wrap async atoms with `loadable()` for loading states
5. **Organize by Domain**: Group related atoms in the same file
6. **Custom Hooks**: Create hooks that combine multiple atoms for common use cases
7. **Test Atoms**: Atoms are pure functions - test them in isolation
8. **Debug with DevTools**: Use Jotai DevTools for debugging state changes

## 📋 QUICK REFERENCE

```typescript
// Basic atoms
atom(initialValue)
atom(readFunction)
atom(readFunction, writeFunction)

// Utilities
atomWithStorage(key, initialValue)
atomFamily(atomCreator)
loadable(asyncAtom)

// Hooks
useAtom(atom)        // [value, setValue]
useAtomValue(atom)   // value only
useSetAtom(atom)     // setValue only
```

This covers the essential Jotai patterns you need for effective atomic state management.