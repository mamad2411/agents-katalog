---
name: react-types
description: "TypeScript + React typing patterns"
---

# Matt Pocock React TypeScript Patterns

Applying Matt Pocock's TypeScript expertise from "Total TypeScript" and his React TypeScript patterns when typing components, hooks, events, refs, context, and generic components. Auto-triggers on .tsx files, React component typing, hooks with generics, and event handler signatures.

---

## Core Principles

### 1. Component Props: Inline Types vs Interface

Use `interface` for exported/shared component props. Inline types for one-off internals.

```tsx
// Not this: inline type for a shared component
function Button({ label, onClick }: { label: string; onClick: () => void }) {
  return <button onClick={onClick}>{label}</button>;
}

// This: interface for anything reusable or exported
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

function Button({ label, onClick, disabled }: ButtonProps) {
  return <button onClick={onClick} disabled={disabled}>{label}</button>;
}
```

Always type `children` as `ReactNode` -- it covers strings, elements, fragments, portals, null, and arrays.

```tsx
// Not this              // This
interface CardProps {     interface CardProps {
  children: JSX.Element;   children: ReactNode;
}                        }
```

### 2. FC vs Plain Functions

Plain typed functions are preferred over `React.FC<Props>`. FC adds implicit `children` (pre-React 18), obscures the return type, and blocks generics.

```tsx
// Not this
const Greeting: React.FC<GreetingProps> = ({ name }) => {
  return <h1>Hello, {name}</h1>;
};

// This
function Greeting({ name }: GreetingProps) {
  return <h1>Hello, {name}</h1>;
}

// FC blocks generic components -- you can't do this with FC
function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}
```

### 3. ReactNode vs ReactElement vs JSX.Element

```tsx
// ReactNode: anything renderable. Use for children and flexible slots.
interface LayoutProps {
  header: ReactNode;
  children: ReactNode;
}

// ReactElement: a concrete element. Use when you need cloneElement.
function Wrapper({ element }: { element: ReactElement }) {
  return cloneElement(element, { className: 'wrapped' });
}

// JSX.Element: narrowest. Rarely needed directly.
// Prefer ReactElement when you need an element type.
```

**Rule:** Start with `ReactNode`. Narrow to `ReactElement` only for `cloneElement` or element inspection.

### 4. Event Handler Types

Use the specific React event type with the correct HTML element generic.

```tsx
// Not this
const handleClick = (e: any) => { /* ... */ };

// This
import { MouseEvent, ChangeEvent, FormEvent, KeyboardEvent } from 'react';

const handleClick = (e: MouseEvent<HTMLButtonElement>) => {
  e.preventDefault(); // e.currentTarget typed as HTMLButtonElement
};

const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
  const value = e.target.value; // string, fully typed
};

const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  const data = new FormData(e.currentTarget);
};

const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
  if (e.key === 'Enter') { /* ... */ }
};
```

For callback props, use React's handler type aliases:

```tsx
interface InputProps {
  onChange: ChangeEventHandler<HTMLInputElement>;
  onBlur: FocusEventHandler<HTMLInputElement>;
}
```

### 5. useRef Typing

The null in the initial value determines whether the ref is mutable or read-only.

```tsx
// DOM ref: pass null -- React manages .current (readonly RefObject)
function AutoFocusInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => { inputRef.current?.focus(); }, []);
  return <input ref={inputRef} />;
}

// Mutable ref: pass a value -- you manage .current (MutableRefObject)
function Timer() {
  const intervalRef = useRef<number>(0);
  useEffect(() => {
    intervalRef.current = window.setInterval(() => { /* tick */ }, 1000);
    return () => clearInterval(intervalRef.current);
  }, []);
}
```

**The rule:** `useRef<T>(null)` when React writes `.current` (DOM elements). `useRef<T>(value)` when you write `.current` (instance variables).

### 6. useState Typing

Let inference handle simple cases. Explicit generics for complex or initially-empty state.

```tsx
// Inference works -- no annotation needed
const [count, setCount] = useState(0);       // number
const [name, setName] = useState('');         // string

// Explicit generic: initial value doesn't capture the full type
const [user, setUser] = useState<User | null>(null);

// Discriminated union state
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

function useAsync<T>() {
  const [state, setState] = useState<AsyncState<T>>({ status: 'idle' });
  if (state.status === 'success') {
    state.data; // T -- narrowed, accessible only here
  }
  return [state, setState] as const;
}
```

### 7. Context Typing

The common mistake is `createContext(undefined)` then asserting non-null everywhere. Solve it with a custom hook.

```tsx
// Not this: undefined default forces null checks everywhere
const UserContext = createContext<User | undefined>(undefined);
function Profile() {
  const user = useContext(UserContext); // User | undefined every time
  return <p>{user?.name}</p>;
}

// This: custom hook throws if used outside provider
const UserContext = createContext<User | null>(null);

function useUser(): User {
  const user = useContext(UserContext);
  if (user === null) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return user; // User, guaranteed
}

function UserProvider({ user, children }: { user: User; children: ReactNode }) {
  return <UserContext.Provider value={user}>{children}</UserContext.Provider>;
}

function Profile() {
  const user = useUser();
  return <p>{user.name}</p>; // no undefined, no null checks
}
```

### 8. Generic Components

Generic components preserve type relationships between props.

```tsx
interface SelectProps<T> {
  options: T[];
  value: T;
  onChange: (value: T) => void;
  getLabel: (option: T) => string;
}

function Select<T>({ options, value, onChange, getLabel }: SelectProps<T>) {
  return (
    <select
      value={String(value)}
      onChange={(e) => onChange(options[e.target.selectedIndex])}
    >
      {options.map((option, i) => (
        <option key={i} value={String(option)}>{getLabel(option)}</option>
      ))}
    </select>
  );
}

// T inferred from options
<Select
  options={countries}
  value={selected}                // Country
  onChange={(c) => setSelected(c)} // c is Country
  getLabel={(c) => c.name}         // c is Country
/>
```

Constrain with `extends` when you need specific properties:

```tsx
interface TableProps<T extends { id: string | number }> {
  rows: T[];
  columns: (keyof T)[];
  onRowClick: (row: T) => void;
}

function Table<T extends { id: string | number }>({
  rows, columns, onRowClick
}: TableProps<T>) {
  return (
    <table><tbody>
      {rows.map((row) => (
        <tr key={row.id} onClick={() => onRowClick(row)}>
          {columns.map((col) => <td key={String(col)}>{String(row[col])}</td>)}
        </tr>
      ))}
    </tbody></table>
  );
}
```

### 9. ComponentProps and ComponentPropsWithRef

Extract props from existing components instead of redeclaring them.

```tsx
import { ComponentProps } from 'react';

// Extend native element props
interface IconButtonProps extends ComponentProps<'button'> {
  icon: ReactNode;
  label: string;
}

function IconButton({ icon, label, ...buttonProps }: IconButtonProps) {
  return <button aria-label={label} {...buttonProps}>{icon}</button>;
}

// Extract from custom components
type DialogProps = ComponentProps<typeof Dialog>;
```

The polymorphic `as` prop pattern:

```tsx
interface BoxProps<T extends React.ElementType> {
  as?: T;
  children: ReactNode;
}

type PolymorphicProps<T extends React.ElementType> =
  BoxProps<T> & Omit<ComponentProps<T>, keyof BoxProps<T>>;

function Box<T extends React.ElementType = 'div'>({
  as, children, ...rest
}: PolymorphicProps<T>) {
  const Component = as || 'div';
  return <Component {...rest}>{children}</Component>;
}

<Box as="a" href="/home">Link</Box>        // href valid
<Box as="button" onClick={fn}>Click</Box>  // onClick valid
<Box>Just a div</Box>                       // defaults to div
```

### 10. forwardRef Typing

forwardRef requires a specific generic signature. React 19 simplifies this.

```tsx
// React 18: forwardRef<Element, Props>
interface InputProps {
  label: string;
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({ label, error, ...props }, ref) {
    return (
      <div>
        <label>{label}</label>
        <input ref={ref} {...props} />
        {error && <span className="error">{error}</span>}
      </div>
    );
  }
);

const inputRef = useRef<HTMLInputElement>(null);
<Input ref={inputRef} label="Email" />

// React 19: ref is just a prop -- no wrapper needed
interface InputPropsR19 {
  label: string;
  error?: string;
  ref?: React.Ref<HTMLInputElement>;
}

function Input({ label, error, ref, ...props }: InputPropsR19) {
  return (
    <div>
      <label>{label}</label>
      <input ref={ref} {...props} />
      {error && <span className="error">{error}</span>}
    </div>
  );
}
```

---

## Anti-Patterns

- **`any` in event handlers** -- Defeats TypeScript. You lose autocomplete on `e.target`, `e.currentTarget`, and element-specific properties.
- **`children: JSX.Element`** -- Breaks on strings, numbers, null, fragments. Always use `ReactNode`.
- **`React.FC` everywhere** -- Adds implicit children (pre-18), blocks generics, obscures return types.
- **Casting context with `as`** -- `useContext(Ctx) as T` silences the compiler but crashes at runtime if the provider is missing. Use a custom hook with a runtime guard.
- **Over-typing useState** -- `useState<string>('')` is redundant. Only use explicit generics when the initial value is narrower than the intended type.
- **`useRef<T>(null!)`** -- The non-null assertion hack creates a mutable ref and bypasses safety. Stick with `null` for DOM refs.

---

## Decision Framework

| Situation | Approach |
|-----------|----------|
| Shared/exported component props | `interface` with descriptive name |
| Internal one-off component | Inline type in destructuring |
| Children slot | `ReactNode` |
| Cloning/inspecting elements | `ReactElement` |
| Event handler prop | `ChangeEventHandler<HTMLInputElement>` |
| Event handler inline | `(e: ChangeEvent<HTMLInputElement>) => void` |
| DOM ref | `useRef<HTMLElement>(null)` |
| Instance variable ref | `useRef<T>(initialValue)` |
| Simple initial state | Let inference work |
| Nullable or union state | Explicit `useState<T \| null>(null)` |
| Context consumed by many | Custom hook with runtime guard |
| Type-safe list/table | Generic component with `extends` constraint |
| Wrapping native elements | `ComponentProps<'element'>` |
| Polymorphic `as` prop | `ComponentProps<T>` with `Omit` |
| Exposing ref (React 18) | `forwardRef<Element, Props>` |
| Exposing ref (React 19) | `ref?: React.Ref<Element>` as a prop |

---

## Code Review Checklist

When reviewing TypeScript React code, verify:

- [ ] Props use `interface` for exported components, not inline types
- [ ] `children` typed as `ReactNode`, not `JSX.Element` or `string`
- [ ] No `React.FC` -- plain functions with typed props
- [ ] Event handlers use specific React event types with element generics
- [ ] DOM refs use `useRef<Element>(null)`, mutable refs use `useRef<T>(value)`
- [ ] `useState` only has explicit generics when inference is insufficient
- [ ] Context has a custom hook that throws outside its provider
- [ ] Generic components use `extends` to constrain type parameters
- [ ] Native element wrappers use `ComponentProps<'element'>` not manual re-typing
- [ ] `forwardRef` uses the correct `<Element, Props>` generic order
- [ ] No `any` in event handlers, context values, or hook returns
- [ ] No `as` type assertions to work around missing providers
