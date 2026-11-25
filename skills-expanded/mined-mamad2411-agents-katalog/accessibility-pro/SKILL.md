---
name: accessibility-pro
description: Advanced accessibility — WAI-ARIA, screen readers, keyboard navigation, focus management
triggers: [accessibility, ARIA, screen reader, keyboard navigation, focus, a11y, WCAG]
---

# SKILL: Accessibility Pro

## WAI-ARIA Roles & Properties

### Common Roles
```tsx
// Navigation
<nav role="navigation" aria-label="Main">
  <ul>...</ul>
</nav>

// Search
<form role="search">
  <input type="search" aria-label="Search" />
</form>

// Alert/Status
<div role="alert">Error: Invalid input</div>
<div role="status" aria-live="polite">Loading...</div>

// Dialog/Modal
<div role="dialog" aria-labelledby="dialog-title" aria-modal="true">
  <h2 id="dialog-title">Confirm</h2>
</div>

// Tabs
<div role="tablist">
  <button role="tab" aria-selected="true">Tab 1</button>
  <button role="tab">Tab 2</button>
</div>
<div role="tabpanel">Content</div>
```

### ARIA States & Properties
```tsx
// Expanded/Collapsed
<button
  aria-expanded={isOpen}
  aria-controls="menu-id"
>
  Menu
</button>
<div id="menu-id" hidden={!isOpen}>
  Menu items
</div>

// Current page (navigation)
<nav>
  <a href="/" aria-current="page">Home</a>
  <a href="/about">About</a>
</nav>

// Disabled vs aria-disabled
<button disabled>Can't click</button>  // Not focusable
<button aria-disabled="true">Can focus, can't activate</button>  // Focusable

// Required fields
<input type="email" required aria-required="true" />

// Invalid fields
<input 
  type="email" 
  aria-invalid={hasError}
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">
  {hasError && "Invalid email"}
</span>
```

## Keyboard Navigation Patterns

### Tab Order
```tsx
// Positive tabindex (avoid - breaks natural order)
<button tabIndex={1}>Bad</button>

// Negative tabindex (remove from tab order)
<div tabIndex={-1}>Not tabbable</div>

// Zero tabindex (add to tab order)
<div tabIndex={0}>Tabbable</div>

// Best practice: Use semantic HTML (naturally focusable)
<button>Naturally tabbable</button>
```

### Focus Management (Modal)
```tsx
function Modal({ isOpen, onClose }) {
  const modalRef = useRef<HTMLDivElement>(null)
  const previousFocus = useRef<HTMLElement | null>(null)
  
  useEffect(() => {
    if (!isOpen) return
    
    // Save current focus
    previousFocus.current = document.activeElement as HTMLElement
    
    // Move focus to modal
    modalRef.current?.focus()
    
    // Trap focus inside modal
    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return
      
      const focusable = modalRef.current?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      if (!focusable?.length) return
      
      const first = focusable[0] as HTMLElement
      const last = focusable[focusable.length - 1] as HTMLElement
      
      if (e.shiftKey && document.activeElement === first) {
        last.focus()
        e.preventDefault()
      } else if (!e.shiftKey && document.activeElement === last) {
        first.focus()
        e.preventDefault()
      }
    }
    
    document.addEventListener('keydown', handleTab)
    
    return () => {
      document.removeEventListener('keydown', handleTab)
      // Restore focus
      previousFocus.current?.focus()
    }
  }, [isOpen])
  
  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
    >
      Modal content
      <button onClick={onClose}>Close</button>
    </div>
  )
}
```

### Keyboard Shortcuts
```tsx
function Dashboard() {
  useEffect(() => {
    const handleKeyboard = (e: KeyboardEvent) => {
      // Cmd/Ctrl + K: Open search
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        openSearch()
      }
      
      // Escape: Close modal
      if (e.key === 'Escape') {
        closeModal()
      }
      
      // Arrow keys: Navigate list
      if (e.key === 'ArrowDown') {
        focusNextItem()
      }
    }
    
    document.addEventListener('keydown', handleKeyboard)
    return () => document.removeEventListener('keydown', handleKeyboard)
  }, [])
}
```

## Screen Reader Testing

```bash
# Mac: VoiceOver
Cmd + F5  # Toggle VoiceOver
Ctrl + Option + Right Arrow  # Next element
Ctrl + Option + Cmd + H  # Next heading

# Windows: NVDA (free)
Ctrl + Alt + N  # Start NVDA
H  # Next heading
K  # Next link
B  # Next button
```

## Quality Checks
- [ ] All interactive elements keyboard accessible
- [ ] Focus visible on all elements (not outline: none)
- [ ] ARIA roles on custom components
- [ ] Form inputs have labels (visible or aria-label)
- [ ] Error messages associated (aria-describedby)
- [ ] Modal focus trapped
- [ ] Screen reader tested (VoiceOver/NVDA)
- [ ] Heading hierarchy correct (h1 → h2 → h3)
- [ ] Alt text on images (meaningful descriptions)
- [ ] Color contrast ≥ 4.5:1 (text on background)
