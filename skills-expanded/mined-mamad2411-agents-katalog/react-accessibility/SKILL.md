---
name: react-accessibility
description: "When to activate: ARIA, keyboard navigation, focus management, screen readers, accessible forms, skip links, live regions"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: typescript
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# React Accessibility Patterns

## Semantic HTML First
```tsx
// BAD: div soup
<div onClick={submit} className="button">Submit</div>

// GOOD: semantic element
<button type="submit" onClick={submit}>Submit</button>

// Landmark regions
<header>
  <nav aria-label="Main navigation">...</nav>
</header>
<main id="main-content">
  <h1>Page Title</h1>
</main>
<aside aria-label="Related articles">...</aside>
<footer>...</footer>
```

## ARIA Attributes
```tsx
// Interactive state
<button
  aria-expanded={isOpen}
  aria-controls="dropdown-menu"
  aria-haspopup="listbox"
>
  Options
</button>
<ul id="dropdown-menu" role="listbox" aria-label="Options">
  <li role="option" aria-selected={selected === 'a'}>Option A</li>
</ul>

// Live regions — announce dynamic content
<div role="status" aria-live="polite" aria-atomic>
  {statusMessage}
</div>
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>

// Loading states
<div aria-busy={isLoading} aria-label={isLoading ? 'Loading users' : 'Users list'}>
  {isLoading ? <Spinner /> : <UserList />}
</div>

// Visually hidden but accessible
<span className="sr-only">Loading, please wait</span>
```

## Accessible Forms
```tsx
function AccessibleForm() {
  const emailId = useId()
  const passwordId = useId()
  const emailErrorId = useId()

  return (
    <form noValidate>
      <div>
        <label htmlFor={emailId}>
          Email <span aria-hidden>*</span>
          <span className="sr-only">(required)</span>
        </label>
        <input
          id={emailId}
          type="email"
          required
          aria-required
          aria-invalid={!!emailError}
          aria-describedby={emailError ? emailErrorId : undefined}
          autoComplete="email"
        />
        {emailError && (
          <span id={emailErrorId} role="alert">{emailError}</span>
        )}
      </div>

      <fieldset>
        <legend>Notification preferences</legend>
        <label><input type="checkbox" name="email-notifs" /> Email</label>
        <label><input type="checkbox" name="push-notifs" />  Push</label>
      </fieldset>

      <button type="submit">Submit</button>
    </form>
  )
}
```

## Focus Management
```tsx
// Return focus on dialog close
function Modal({ isOpen, onClose, children }: ModalProps) {
  const triggerRef = useRef<HTMLElement | null>(null)
  const firstFocusableRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    if (isOpen) {
      triggerRef.current = document.activeElement as HTMLElement
      firstFocusableRef.current?.focus()
    } else {
      triggerRef.current?.focus()
    }
  }, [isOpen])

  if (!isOpen) return null

  return createPortal(
    <div role="dialog" aria-modal aria-labelledby="dialog-title">
      <button ref={firstFocusableRef} onClick={onClose} aria-label="Close dialog">
        ×
      </button>
      <h2 id="dialog-title">Dialog Title</h2>
      {children}
    </div>,
    document.body
  )
}

// Focus trap inside modal
function useFocusTrap(containerRef: RefObject<HTMLElement>, active: boolean) {
  useEffect(() => {
    if (!active || !containerRef.current) return
    const el = containerRef.current
    const focusable = el.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    const first = focusable[0]
    const last  = focusable[focusable.length - 1]

    const trap = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault(); last.focus()
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); first.focus()
      }
    }

    el.addEventListener('keydown', trap)
    return () => el.removeEventListener('keydown', trap)
  }, [active, containerRef])
}
```

## Skip Link
```tsx
// Place as very first element in <body>
function SkipLink() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-white focus:px-4 focus:py-2"
    >
      Skip to main content
    </a>
  )
}
```

## Keyboard Navigation
```tsx
// Custom listbox with arrow key navigation
function ListBox({ options, value, onChange }: ListBoxProps) {
  const [activeIdx, setActiveIdx] = useState(0)

  const handleKeyDown = (e: KeyboardEvent<HTMLUListElement>) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setActiveIdx(i => Math.min(i + 1, options.length - 1))
        break
      case 'ArrowUp':
        e.preventDefault()
        setActiveIdx(i => Math.max(i - 1, 0))
        break
      case 'Enter':
      case ' ':
        e.preventDefault()
        onChange(options[activeIdx].value)
        break
      case 'Escape':
        // close listbox
        break
    }
  }

  return (
    <ul
      role="listbox"
      tabIndex={0}
      aria-activedescendant={`option-${activeIdx}`}
      onKeyDown={handleKeyDown}
    >
      {options.map((opt, i) => (
        <li
          key={opt.value}
          id={`option-${i}`}
          role="option"
          aria-selected={value === opt.value}
          onClick={() => onChange(opt.value)}
        >
          {opt.label}
        </li>
      ))}
    </ul>
  )
}
```

## Reduced Motion
```tsx
function useReducedMotion() {
  return useMediaQuery('(prefers-reduced-motion: reduce)')
}

function AnimatedBanner() {
  const reducedMotion = useReducedMotion()

  return (
    <div
      style={{
        animation: reducedMotion
          ? 'none'
          : 'slide-in 0.3s ease-out',
      }}
    >
      Banner content
    </div>
  )
}
```
