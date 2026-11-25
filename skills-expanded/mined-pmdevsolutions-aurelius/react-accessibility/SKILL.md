---
name: react-accessibility
description: Accessibility patterns for React applications. Covers ARIA patterns for common components, eslint-plugin-jsx-a11y, keyboard navigation, focus management, screen reader testing, color contrast validation, and accessible forms. Keywords: accessibility, a11y, WCAG, ARIA, keyboard navigation, screen reader, focus management, color contrast, accessible forms
---

# React Accessibility

## Overview

This skill provides concrete accessibility patterns for React applications, targeting WCAG 2.2 Level AA compliance. It covers ARIA implementation for common interactive components, keyboard navigation, focus management, screen reader compatibility, and automated accessibility testing.

**Core Principle:** Accessibility is not an afterthought or a checklist. Build accessible components from the start. Use semantic HTML first; add ARIA only when native semantics are insufficient.

**The Rules of ARIA:**
1. If you can use a native HTML element with built-in semantics, do so instead of adding ARIA
2. Do not change native semantics unless absolutely necessary
3. All interactive ARIA controls must be keyboard operable
4. Do not use `role="presentation"` or `aria-hidden="true"` on focusable elements
5. All interactive elements must have an accessible name

## When to Use

Use this skill when:
- Building interactive React components (modals, tabs, dropdowns, accordions)
- Implementing keyboard navigation
- Managing focus in single-page applications
- Adding screen reader support
- Running accessibility audits
- Fixing accessibility violations found by linting or testing

**Trigger phrases:**
- "Make this accessible"
- "Add keyboard navigation"
- "ARIA for this component"
- "Screen reader support"
- "WCAG compliance"
- "Fix accessibility issues"
- "Focus management"

## ESLint Configuration

### Setup

```bash
pnpm add -D eslint-plugin-jsx-a11y
```

### ESLint Config

```typescript
// eslint.config.js (flat config)
import jsxA11y from "eslint-plugin-jsx-a11y";

export default [
  {
    plugins: {
      "jsx-a11y": jsxA11y,
    },
    rules: {
      // Critical rules (errors)
      "jsx-a11y/alt-text": "error",
      "jsx-a11y/anchor-has-content": "error",
      "jsx-a11y/anchor-is-valid": "error",
      "jsx-a11y/aria-activedescendant-has-tabindex": "error",
      "jsx-a11y/aria-props": "error",
      "jsx-a11y/aria-proptypes": "error",
      "jsx-a11y/aria-role": "error",
      "jsx-a11y/aria-unsupported-elements": "error",
      "jsx-a11y/click-events-have-key-events": "error",
      "jsx-a11y/heading-has-content": "error",
      "jsx-a11y/html-has-lang": "error",
      "jsx-a11y/img-redundant-alt": "error",
      "jsx-a11y/interactive-supports-focus": "error",
      "jsx-a11y/label-has-associated-control": "error",
      "jsx-a11y/no-access-key": "error",
      "jsx-a11y/no-autofocus": "warn",
      "jsx-a11y/no-distracting-elements": "error",
      "jsx-a11y/no-interactive-element-to-noninteractive-role": "error",
      "jsx-a11y/no-noninteractive-element-interactions": "warn",
      "jsx-a11y/no-noninteractive-element-to-interactive-role": "error",
      "jsx-a11y/no-noninteractive-tabindex": "warn",
      "jsx-a11y/no-redundant-roles": "error",
      "jsx-a11y/no-static-element-interactions": "error",
      "jsx-a11y/role-has-required-aria-props": "error",
      "jsx-a11y/role-supports-aria-props": "error",
      "jsx-a11y/scope": "error",
      "jsx-a11y/tabindex-no-positive": "error",
    },
  },
];
```

## ARIA Patterns for Common Components

### Modal / Dialog

```typescript
"use client";
import { useEffect, useRef, type ReactNode } from "react";
import { createPortal } from "react-dom";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: ReactNode;
}

function Modal({ isOpen, onClose, title, description, children }: ModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement;
      dialog.showModal();
    } else {
      dialog.close();
      previousFocusRef.current?.focus(); // Restore focus to trigger element
    }
  }, [isOpen]);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    const handleCancel = (e: Event) => {
      e.preventDefault();
      onClose();
    };

    dialog.addEventListener("cancel", handleCancel);
    return () => dialog.removeEventListener("cancel", handleCancel);
  }, [onClose]);

  if (!isOpen) return null;

  return createPortal(
    <dialog
      ref={dialogRef}
      aria-labelledby="modal-title"
      aria-describedby={description ? "modal-description" : undefined}
      className="backdrop:bg-black/50"
      onClick={(e) => {
        // Close on backdrop click
        if (e.target === dialogRef.current) onClose();
      }}
    >
      <div className="p-6" role="document">
        <h2 id="modal-title">{title}</h2>
        {description && <p id="modal-description">{description}</p>}
        {children}
        <button onClick={onClose} aria-label="Close dialog">
          Close
        </button>
      </div>
    </dialog>,
    document.body
  );
}
```

**Key requirements:**
- Use the native `<dialog>` element with `showModal()` for built-in focus trapping
- `aria-labelledby` pointing to the title
- `aria-describedby` for optional description
- Restore focus to the trigger element on close
- Close on Escape (native with `<dialog>`) and backdrop click

### Tabs

```typescript
"use client";
import { useState, useRef, type ReactNode, type KeyboardEvent } from "react";

interface Tab {
  id: string;
  label: string;
  content: ReactNode;
}

function Tabs({ tabs }: { tabs: Tab[] }) {
  const [activeTab, setActiveTab] = useState(tabs[0].id);
  const tabRefs = useRef<Map<string, HTMLButtonElement>>(new Map());

  const handleKeyDown = (e: KeyboardEvent, index: number) => {
    let nextIndex: number;

    switch (e.key) {
      case "ArrowRight":
        nextIndex = (index + 1) % tabs.length;
        break;
      case "ArrowLeft":
        nextIndex = (index - 1 + tabs.length) % tabs.length;
        break;
      case "Home":
        nextIndex = 0;
        break;
      case "End":
        nextIndex = tabs.length - 1;
        break;
      default:
        return;
    }

    e.preventDefault();
    const nextTab = tabs[nextIndex];
    setActiveTab(nextTab.id);
    tabRefs.current.get(nextTab.id)?.focus();
  };

  return (
    <div>
      <div role="tablist" aria-label="Content tabs">
        {tabs.map((tab, index) => (
          <button
            key={tab.id}
            ref={(el) => {
              if (el) tabRefs.current.set(tab.id, el);
            }}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeTab === tab.id}
            aria-controls={`panel-${tab.id}`}
            tabIndex={activeTab === tab.id ? 0 : -1}
            onClick={() => setActiveTab(tab.id)}
            onKeyDown={(e) => handleKeyDown(e, index)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {tabs.map((tab) => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`}
          hidden={activeTab !== tab.id}
          tabIndex={0}
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

**Key requirements:**
- `role="tablist"` on the container, `role="tab"` on each tab, `role="tabpanel"` on each panel
- `aria-selected` on the active tab
- Arrow keys move between tabs; only the active tab has `tabIndex={0}`
- `aria-controls` / `aria-labelledby` link tabs to panels
- Home/End keys jump to first/last tab

### Accordion

```typescript
"use client";
import { useState, type ReactNode } from "react";

interface AccordionItem {
  id: string;
  heading: string;
  content: ReactNode;
}

function Accordion({ items, multiple = false }: { items: AccordionItem[]; multiple?: boolean }) {
  const [openItems, setOpenItems] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    setOpenItems((prev) => {
      const next = new Set(multiple ? prev : []);
      if (prev.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <div>
      {items.map((item) => {
        const isOpen = openItems.has(item.id);
        return (
          <div key={item.id}>
            <h3>
              <button
                id={`accordion-trigger-${item.id}`}
                aria-expanded={isOpen}
                aria-controls={`accordion-panel-${item.id}`}
                onClick={() => toggle(item.id)}
                className="flex w-full items-center justify-between text-left"
              >
                {item.heading}
                <span aria-hidden="true">{isOpen ? "\u2212" : "+"}</span>
              </button>
            </h3>
            <div
              id={`accordion-panel-${item.id}`}
              role="region"
              aria-labelledby={`accordion-trigger-${item.id}`}
              hidden={!isOpen}
            >
              {item.content}
            </div>
          </div>
        );
      })}
    </div>
  );
}
```

**Key requirements:**
- The trigger is a `<button>` inside a heading element
- `aria-expanded` indicates open/closed state
- `aria-controls` links to the panel; `aria-labelledby` links panel back to trigger
- `role="region"` on each panel
- Use `hidden` attribute (not `display: none` via CSS) for proper screen reader behavior

### Dropdown Menu

```typescript
"use client";
import { useState, useRef, useEffect, type KeyboardEvent, type ReactNode } from "react";

interface MenuItem {
  id: string;
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

function DropdownMenu({ label, items }: { label: string; items: MenuItem[] }) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const menuRef = useRef<HTMLUListElement>(null);
  const itemRefs = useRef<Map<number, HTMLLIElement>>(new Map());

  useEffect(() => {
    if (isOpen && activeIndex >= 0) {
      itemRefs.current.get(activeIndex)?.focus();
    }
  }, [isOpen, activeIndex]);

  // Close on outside click
  useEffect(() => {
    if (!isOpen) return;
    const handleClick = (e: MouseEvent) => {
      if (!menuRef.current?.contains(e.target as Node) && !buttonRef.current?.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [isOpen]);

  const handleTriggerKeyDown = (e: KeyboardEvent) => {
    switch (e.key) {
      case "ArrowDown":
      case "Enter":
      case " ":
        e.preventDefault();
        setIsOpen(true);
        setActiveIndex(0);
        break;
      case "ArrowUp":
        e.preventDefault();
        setIsOpen(true);
        setActiveIndex(items.length - 1);
        break;
    }
  };

  const handleMenuKeyDown = (e: KeyboardEvent) => {
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setActiveIndex((prev) => (prev + 1) % items.length);
        break;
      case "ArrowUp":
        e.preventDefault();
        setActiveIndex((prev) => (prev - 1 + items.length) % items.length);
        break;
      case "Home":
        e.preventDefault();
        setActiveIndex(0);
        break;
      case "End":
        e.preventDefault();
        setActiveIndex(items.length - 1);
        break;
      case "Escape":
        setIsOpen(false);
        buttonRef.current?.focus();
        break;
      case "Enter":
      case " ":
        e.preventDefault();
        if (activeIndex >= 0 && !items[activeIndex].disabled) {
          items[activeIndex].onClick();
          setIsOpen(false);
          buttonRef.current?.focus();
        }
        break;
    }
  };

  return (
    <div className="relative">
      <button
        ref={buttonRef}
        aria-haspopup="true"
        aria-expanded={isOpen}
        aria-controls="dropdown-menu"
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleTriggerKeyDown}
      >
        {label}
      </button>
      {isOpen && (
        <ul
          ref={menuRef}
          id="dropdown-menu"
          role="menu"
          aria-label={label}
          onKeyDown={handleMenuKeyDown}
          className="absolute mt-1 rounded-md border bg-popover shadow-md"
        >
          {items.map((item, index) => (
            <li
              key={item.id}
              ref={(el) => {
                if (el) itemRefs.current.set(index, el);
              }}
              role="menuitem"
              tabIndex={activeIndex === index ? 0 : -1}
              aria-disabled={item.disabled || undefined}
              onClick={() => {
                if (!item.disabled) {
                  item.onClick();
                  setIsOpen(false);
                  buttonRef.current?.focus();
                }
              }}
              className="cursor-pointer px-4 py-2 hover:bg-accent"
            >
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

**Key requirements:**
- `aria-haspopup="true"` and `aria-expanded` on the trigger
- `role="menu"` on the list, `role="menuitem"` on each item
- Arrow keys navigate items; Escape closes and restores focus
- Only the active item has `tabIndex={0}`; others have `tabIndex={-1}`
- Close on outside click

## Keyboard Navigation

### Skip Link

The first focusable element on the page should be a skip-to-content link:

```typescript
// components/layout/skip-link.tsx
function SkipLink() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground"
    >
      Skip to main content
    </a>
  );
}

// In layout
function Layout({ children }: { children: ReactNode }) {
  return (
    <>
      <SkipLink />
      <Header />
      <main id="main-content" tabIndex={-1}>
        {children}
      </main>
      <Footer />
    </>
  );
}
```

### Roving Tabindex

For groups of related controls (toolbars, radio groups, tab lists), only one item should be in the tab order at a time:

```typescript
function Toolbar({ items }: { items: ToolbarItem[] }) {
  const [activeIndex, setActiveIndex] = useState(0);

  const handleKeyDown = (e: KeyboardEvent, index: number) => {
    let next: number;
    switch (e.key) {
      case "ArrowRight":
        next = (index + 1) % items.length;
        break;
      case "ArrowLeft":
        next = (index - 1 + items.length) % items.length;
        break;
      default:
        return;
    }
    e.preventDefault();
    setActiveIndex(next);
  };

  return (
    <div role="toolbar" aria-label="Formatting options">
      {items.map((item, index) => (
        <button
          key={item.id}
          tabIndex={index === activeIndex ? 0 : -1}
          onKeyDown={(e) => handleKeyDown(e, index)}
          onFocus={() => setActiveIndex(index)}
          aria-pressed={item.active}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}
```

### Focus Visible Styles

Ensure all interactive elements have visible focus indicators:

```css
/* Global focus styles in Tailwind */
@layer base {
  *:focus-visible {
    @apply outline-2 outline-offset-2 outline-primary;
  }
}
```

```typescript
// Component-level focus styles
<button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2">
  Click me
</button>
```

**Never remove focus outlines without providing an alternative:**
```css
/* Bad */
*:focus { outline: none; }

/* Good - only remove default, provide custom */
*:focus { outline: none; }
*:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }
```

## Focus Management

### Focus Trap (for Modals)

Using the native `<dialog>` element with `showModal()` provides automatic focus trapping. For custom implementations:

```typescript
"use client";
import { useEffect, useRef, type ReactNode } from "react";

function FocusTrap({ children, active }: { children: ReactNode; active: boolean }) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!active || !containerRef.current) return;

    const container = containerRef.current;
    const focusableSelector =
      'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

    const handleKeyDown = (e: globalThis.KeyboardEvent) => {
      if (e.key !== "Tab") return;

      const focusable = Array.from(container.querySelectorAll<HTMLElement>(focusableSelector));
      if (focusable.length === 0) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    container.addEventListener("keydown", handleKeyDown);
    return () => container.removeEventListener("keydown", handleKeyDown);
  }, [active]);

  return <div ref={containerRef}>{children}</div>;
}
```

### Restore Focus on Navigation

In single-page applications, manage focus when routes change:

```typescript
// Next.js App Router - focus main content on navigation
"use client";
import { usePathname } from "next/navigation";
import { useEffect, useRef } from "react";

function FocusManager({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const mainRef = useRef<HTMLElement>(null);
  const isFirstRender = useRef(true);

  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }
    // Focus main content area after route change
    mainRef.current?.focus();
  }, [pathname]);

  return (
    <main ref={mainRef} id="main-content" tabIndex={-1} className="outline-none">
      {children}
    </main>
  );
}
```

### Live Regions for Dynamic Content

Announce changes to screen readers:

```typescript
// Announce status updates
function StatusMessage({ message, type }: { message: string; type: "polite" | "assertive" }) {
  return (
    <div aria-live={type} aria-atomic="true" className="sr-only">
      {message}
    </div>
  );
}

// Usage in a form
function SearchForm() {
  const [results, setResults] = useState<Item[]>([]);
  const [announcement, setAnnouncement] = useState("");

  const handleSearch = async (query: string) => {
    const data = await searchAPI(query);
    setResults(data);
    setAnnouncement(`${data.length} results found for "${query}"`);
  };

  return (
    <>
      <input type="search" onChange={(e) => handleSearch(e.target.value)} aria-label="Search" />
      <StatusMessage message={announcement} type="polite" />
      <ul>{results.map(/* ... */)}</ul>
    </>
  );
}
```

## Screen Reader Testing

### VoiceOver (macOS)

1. Enable: Cmd + F5 (or System Settings > Accessibility > VoiceOver)
2. Navigate: VO + Right/Left arrow (VO = Ctrl + Option)
3. Interact: VO + Space to activate buttons/links
4. Rotor: VO + U to browse headings, links, landmarks
5. Read all: VO + A

**What to verify:**
- All content is read in a logical order
- Interactive elements announce their role and state
- Headings form a logical hierarchy in the rotor
- Landmarks (header, nav, main, footer) are detected
- Form fields announce their labels
- Dynamic changes are announced via live regions

### NVDA (Windows)

1. Download from nvaccess.org (free)
2. Navigate: Tab/Shift+Tab for focusable elements; Up/Down for virtual buffer
3. Headings: H key to jump between headings
4. Landmarks: D key to jump between landmarks
5. Forms: F key to jump between form fields

**What to verify:**
- Same checklist as VoiceOver
- Verify that ARIA roles and states are announced correctly
- Check that focus indicators match visual state

### Automated Screen Reader Testing

Use `@testing-library/react` queries that mirror screen reader behavior:

```typescript
// These queries use accessibility semantics, matching what screen readers expose
screen.getByRole("button", { name: "Submit" });        // Role + accessible name
screen.getByRole("heading", { name: "Welcome", level: 1 }); // Heading level
screen.getByRole("link", { name: "Read more" });       // Link with name
screen.getByRole("textbox", { name: "Email" });        // Input with label
screen.getByRole("alert");                              // Live region alert
```

## Color Contrast

### WCAG Requirements

| Text Type | Minimum Ratio (AA) | Enhanced Ratio (AAA) |
|-----------|--------------------|--------------------|
| Normal text (< 18px) | 4.5:1 | 7:1 |
| Large text (>= 18px bold or >= 24px) | 3:1 | 4.5:1 |
| UI components and graphics | 3:1 | Not specified |

### Checking Contrast in Code

```typescript
// Utility to check contrast ratio
function getLuminance(hex: string): number {
  const rgb = hex
    .replace("#", "")
    .match(/.{2}/g)!
    .map((c) => {
      const v = parseInt(c, 16) / 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
  return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
}

function getContrastRatio(hex1: string, hex2: string): number {
  const l1 = getLuminance(hex1);
  const l2 = getLuminance(hex2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Check: getContrastRatio("#1a1a1a", "#ffffff") => 17.4 (excellent)
```

### Tools for Contrast Checking

- Chrome DevTools: Inspect element > Color picker shows contrast ratio
- Lighthouse accessibility audit flags contrast issues
- axe DevTools browser extension
- WebAIM Contrast Checker (webaim.org/resources/contrastchecker)

## Accessible Forms

### Labels and Descriptions

```typescript
// Every input MUST have an associated label
<label htmlFor="email">Email address</label>
<input id="email" type="email" aria-describedby="email-hint" />
<p id="email-hint" className="text-sm text-muted-foreground">
  We will never share your email.
</p>

// For visually hidden labels (e.g., search inputs with placeholder)
<label htmlFor="search" className="sr-only">Search</label>
<input id="search" type="search" placeholder="Search..." />

// Group related fields
<fieldset>
  <legend>Shipping Address</legend>
  <label htmlFor="street">Street</label>
  <input id="street" />
  <label htmlFor="city">City</label>
  <input id="city" />
</fieldset>
```

### Error Messages

```typescript
function FormField({ label, error, id, ...inputProps }: FormFieldProps) {
  const errorId = `${id}-error`;

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        aria-invalid={!!error}
        aria-describedby={error ? errorId : undefined}
        {...inputProps}
      />
      {error && (
        <p id={errorId} role="alert" className="text-sm text-destructive">
          {error}
        </p>
      )}
    </div>
  );
}
```

**Key requirements:**
- `aria-invalid="true"` on inputs with errors
- `aria-describedby` linking to the error message
- `role="alert"` on error messages so screen readers announce them immediately
- Error messages must be visible (not just color-coded -- include text/icon)

### Required Fields

```typescript
<label htmlFor="name">
  Name <span aria-hidden="true" className="text-destructive">*</span>
</label>
<input id="name" required aria-required="true" />
```

## Accessibility Testing Checklist

```
Keyboard
[ ] All interactive elements reachable with Tab
[ ] Tab order matches visual order
[ ] No keyboard traps (can always Tab/Escape out)
[ ] Skip link present and functional
[ ] Focus indicators visible on all focusable elements
[ ] Custom components support expected keyboard patterns

Screen Reader
[ ] All images have meaningful alt text (or alt="" for decorative)
[ ] Headings form a logical hierarchy (h1 > h2 > h3, no skips)
[ ] Landmarks present: header, nav, main, footer
[ ] Form inputs have associated labels
[ ] Dynamic content changes announced via live regions
[ ] Links and buttons have descriptive accessible names

Visual
[ ] Color contrast meets WCAG AA (4.5:1 normal text, 3:1 large text)
[ ] Information not conveyed by color alone
[ ] Text resizable to 200% without loss of content
[ ] No content lost at 320px viewport width (reflow)
[ ] Animations respect prefers-reduced-motion

Automated
[ ] eslint-plugin-jsx-a11y passes with zero errors
[ ] Lighthouse accessibility score >= 95
[ ] axe-core reports zero violations
[ ] All React Testing Library queries use accessible roles
```

## Integration

This skill works with:
- **figma-react-converter agent** -- Ensures generated components include ARIA attributes
- **visual-qa-agent** -- Validates keyboard navigation and focus indicators during QA
- **accessibility-auditor agent** -- Runs comprehensive accessibility audits
- **react-testing-workflows skill** -- Testing Library queries verify accessibility semantics
- **Chrome DevTools MCP** -- Lighthouse accessibility audits, contrast checking
- **Playwright MCP** -- Automated keyboard navigation testing across browsers

---

**Skill Version:** 1.0.0
**Last Updated:** 2026-03-11
