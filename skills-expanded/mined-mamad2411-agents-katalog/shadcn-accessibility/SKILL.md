---
name: shadcn-accessibility
description: Use when building accessible shadcn/ui components from the start — covering per-component Radix ARIA contracts, WCAG 2.2 success criteria mapping, keyboard interaction implementation, focus management, and screen reader announcement patterns.
---

# shadcn/ui Accessibility

## Specialization

Provide expert-level guidance for building WCAG 2.2 AA-compliant shadcn/ui components — covering per-component Radix ARIA role/state contracts, keyboard interaction implementation, focus management strategies, `aria-live` announcement patterns for async components, reduced-motion compliance, and screen reader testing sequences.

This skill is for building accessibility in from the start. Pre-merge gate checks are handled by `shadcn-quality-gate`. Component design patterns and CVA variants are handled by `shadcn-component-design`. Testing keyboard and ARIA behavior is handled by `shadcn-testing`.

## Trigger Conditions

- Implementing a shadcn/ui component that must pass WCAG 2.2 AA for a production feature.
- A Dialog, Sheet, Tooltip, Popover, Select, Combobox, or DataTable component needs correct ARIA role and state implementation.
- Focus management is needed: trapping focus in dialogs, restoring focus on close, managing focus in multi-step flows.
- An async component (Command palette, Combobox, async DataTable) needs `aria-live` region announcements for screen readers.
- A component uses `tailwindcss-animate` or Framer Motion and needs `prefers-reduced-motion` compliance.
- Icon-only buttons, decorative images, or visually hidden labels need correct ARIA patterns.
- An accessibility audit has returned failures that need remediation guidance.
- Designing skip links, landmark regions, and page-level accessibility scaffolding.

## When Not to Use

- Automated pre-merge accessibility gate (use `shadcn-quality-gate`).
- Writing test cases for ARIA behavior (use `shadcn-testing`).
- Deep accessibility audit across an entire app surface (use `web-ux-accessibility`).
- Mobile-specific accessibility for MAUI/Capacitor (use `capacitor-accessibility` or `mobile-accessibility-quality-gate`).

## Inputs

- Component name and Radix primitive base.
- Feature context: what user action does this component enable?
- WCAG target level: AA (default) or AAA.
- Whether `prefers-reduced-motion` support is required.
- Whether `aria-live` announcements are needed (async filter, loading state, toast/alert).
- Framework and RSC context.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| ARIA contract | Complete role, state, property, and relationship requirements for the component per WAI-ARIA APG |
| WCAG mapping | SC identifiers and pass criteria for each accessibility requirement |
| Keyboard interaction table | Full key sequence for all interactive states |
| Focus management spec | Focus-on-open, focus-trap, and focus-on-close behavior defined |
| `aria-live` contract (if async) | Region role, `aria-atomic`, `aria-relevant`, and trigger timing defined |
| Reduced-motion implementation | CSS `@media (prefers-reduced-motion: reduce)` rules or Framer Motion `useReducedMotion` usage |
| Visually hidden pattern | `sr-only` utility application for labels that should be off-screen but accessible |
| Screen reader test sequence | Manual verification steps for VoiceOver (macOS/iOS) and NVDA/JAWS (Windows) |
| Open findings | Known gaps, browser/AT quirks, and deferred items with rationale |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | One component ARIA contract and keyboard map | Role, state, and keyboard behavior documented; no obvious WCAG failures |
| L2 Practical Delivery | Full accessible implementation for one component | All SC mapped; focus management correct; reduced-motion applied |
| L3 Advanced Patterns | Async announcements, complex focus flows, multi-component orchestration | `aria-live` tuned; focus restoration after async operations correct; dialog-in-dialog handled |
| L4 Expert Standardization | Cross-project accessible component library contract | Reusable ARIA pattern library, shared `sr-only` utilities, and screen reader test scripts documented |

## Per-Component ARIA Reference

### Dialog / AlertDialog / Sheet

| Attribute | Value | Notes |
|---|---|---|
| `role` | `dialog` | Set by Radix automatically on content element |
| `aria-modal` | `true` | Set by Radix; signals to AT that background is inert |
| `aria-labelledby` | ID of `DialogTitle` | **Required** — Radix warns if missing |
| `aria-describedby` | ID of `DialogDescription` | Recommended for context |
| Focus on open | First focusable element inside content | Radix handles; verify no custom override breaks it |
| Focus on close | Trigger element that opened the dialog | Radix restores automatically |
| Focus trap | All interactive elements inside dialog only | Radix `FocusScope` handles; verify no portaled children escape |

```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button>Edit Profile</Button>
  </DialogTrigger>
  <DialogContent aria-describedby="profile-desc">
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>                 {/* aria-labelledby target */}
      <DialogDescription id="profile-desc">             {/* aria-describedby target */}
        Make changes to your profile here.
      </DialogDescription>
    </DialogHeader>
    {/* content */}
  </DialogContent>
</Dialog>
```

**WCAG SCs:** 1.3.1 (Info and Relationships), 2.1.2 (No Keyboard Trap — trapped is correct here), 2.4.3 (Focus Order), 4.1.2 (Name, Role, Value).

---

### Select

| Attribute | Value | Notes |
|---|---|---|
| `role` | `combobox` on trigger | Set by Radix |
| `aria-expanded` | `true`/`false` | Reflects open/closed state |
| `aria-haspopup` | `listbox` | Set by Radix |
| `aria-labelledby` | Associated `<label>` or `SelectLabel` ID | Must be explicitly wired when using inside `FormField` |
| `role` on content | `listbox` | Set by Radix |
| `role` on items | `option` | Set by Radix |
| `aria-selected` | `true` on selected option | Set by Radix |

```tsx
<FormField
  control={form.control}
  name="role"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Role</FormLabel>
      <Select onValueChange={field.onChange} defaultValue={field.value}>
        <FormControl>
          <SelectTrigger>
            <SelectValue placeholder="Select a role" />
          </SelectTrigger>
        </FormControl>
        <SelectContent>
          <SelectItem value="admin">Admin</SelectItem>
          <SelectItem value="editor">Editor</SelectItem>
        </SelectContent>
      </Select>
      <FormMessage />
    </FormItem>
  )}
/>
```

**WCAG SCs:** 1.3.1, 2.1.1 (Keyboard), 4.1.2.

---

### Combobox (Command + Popover)

| Requirement | Implementation |
|---|---|
| Input has accessible label | `<label>` associated via `htmlFor` or `aria-label` on input |
| Results list role | `role="listbox"` on Command list |
| Result items role | `role="option"` on Command items |
| Active descendant | `aria-activedescendant` pointing to focused option |
| Status announcements | `aria-live="polite"` region announcing result count: "5 results found" |
| Empty state | `aria-live` region announces "No results" |

```tsx
// Announce result count to screen readers
<p role="status" aria-live="polite" className="sr-only">
  {filteredItems.length === 0
    ? "No results found."
    : `${filteredItems.length} result${filteredItems.length !== 1 ? "s" : ""} available.`}
</p>
```

---

### DataTable (TanStack Table)

| Requirement | Implementation |
|---|---|
| Table semantics | `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>` — not `div`-based |
| Column header sort state | `aria-sort="ascending"` / `"descending"` / `"none"` on `<th>` |
| Row selection | `aria-selected="true"` on selected `<tr>` |
| Loading state | `aria-busy="true"` on `<table>` during data fetch |
| Caption | `<caption className="sr-only">Table description</caption>` |
| Pagination | `aria-label` on each navigation button; current page announced via `aria-current="page"` |

```tsx
<th
  aria-sort={
    column.getIsSorted() === "asc"
      ? "ascending"
      : column.getIsSorted() === "desc"
      ? "descending"
      : "none"
  }
>
```

---

### Tooltip

| Requirement | Implementation |
|---|---|
| Trigger must be focusable | Use `asChild` with a `<button>` or ensure trigger is keyboard reachable |
| Content linked to trigger | Radix sets `aria-describedby` on trigger pointing to tooltip content |
| No pointer-only trigger | Tooltip must open on keyboard focus, not only on hover |
| Delay on open | Default 700ms — acceptable; do not set to 0 (causes AT conflicts) |

```tsx
<Tooltip>
  <TooltipTrigger asChild>
    <Button variant="ghost" size="icon" aria-label="Settings">
      <Settings className="h-4 w-4" aria-hidden="true" />
    </Button>
  </TooltipTrigger>
  <TooltipContent>
    <p>Open settings</p>
  </TooltipContent>
</Tooltip>
```

---

### Icon-Only Buttons

```tsx
// Pattern 1: aria-label on button
<Button variant="ghost" size="icon" aria-label="Delete item">
  <Trash2 className="h-4 w-4" aria-hidden="true" />
</Button>

// Pattern 2: visually hidden span (preferred when icon + visible label co-exist)
<Button variant="ghost" size="icon">
  <Trash2 className="h-4 w-4" aria-hidden="true" />
  <span className="sr-only">Delete item</span>
</Button>
```

**Rule:** All icon-only interactive elements MUST have an accessible name via `aria-label` or `sr-only` text. `aria-hidden="true"` on the icon SVG prevents double-reading.

---

## Focus Management Patterns

### Programmatic Focus After Async Operation

```tsx
import { useRef, useEffect } from "react"

function AsyncResultPanel({ results, isLoading }: Props) {
  const headingRef = useRef<HTMLHeadingElement>(null)

  useEffect(() => {
    if (!isLoading && results.length > 0) {
      headingRef.current?.focus()
    }
  }, [isLoading, results])

  return (
    <section>
      <h2 ref={headingRef} tabIndex={-1}>
        Search Results ({results.length})
      </h2>
      {/* result list */}
    </section>
  )
}
```

**Rule:** `tabIndex={-1}` allows programmatic focus on non-interactive elements without adding them to the tab order.

### Skip Link

```tsx
// Place as the first element in <body>
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-background focus:text-foreground focus:rounded-md focus:border"
>
  Skip to main content
</a>
<main id="main-content">
  {/* page content */}
</main>
```

---

## `aria-live` Patterns

### Status / Progress Announcements

```tsx
// Polite: for non-urgent updates (search results, save confirmations)
<div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
  {statusMessage}
</div>

// Assertive: for errors and critical alerts only
<div role="alert" aria-live="assertive" aria-atomic="true" className="sr-only">
  {errorMessage}
</div>
```

**Rules:**
- `aria-live="assertive"` interrupts the screen reader immediately — use only for errors.
- `aria-live="polite"` waits for the reader to finish — use for informational updates.
- `aria-atomic="true"` announces the entire region content on any change, not just the diff.
- Update the text content; do not add/remove the element — AT may miss newly mounted live regions.

---

## Reduced-Motion Implementation

```css
/* globals.css — apply to all transitions */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

For Framer Motion:
```tsx
import { useReducedMotion } from "framer-motion"

function AnimatedPanel({ children }: { children: React.ReactNode }) {
  const shouldReduce = useReducedMotion()

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduce ? 0 : 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: shouldReduce ? 0 : 8 }}
      transition={{ duration: shouldReduce ? 0 : 0.2 }}
    >
      {children}
    </motion.div>
  )
}
```

**WCAG SC:** 2.3.3 Animation from Interactions (AAA) — providing reduced-motion is best practice at AA.

---

## Screen Reader Test Sequences

### Dialog (VoiceOver / macOS)

1. `Tab` to trigger button.
2. Press `Space` or `Enter` — dialog should open.
3. VoiceOver should announce: "dialog, [DialogTitle], [DialogDescription if present]".
4. `Tab` through interactive elements — should stay inside dialog.
5. `Escape` — dialog closes; VoiceOver should return focus to trigger and announce the button.

### Select (NVDA / Windows)

1. `Tab` to select trigger.
2. NVDA announces: "Role, combobox, collapsed".
3. `Space` — listbox opens; NVDA announces: "Role, expanded".
4. `Arrow Down/Up` — NVDA announces each option.
5. `Enter` — selection confirmed; NVDA announces selected value.

### Combobox (VoiceOver / macOS)

1. `Tab` to combobox trigger; VoiceOver announces label and "collapsed".
2. `Enter` — popover opens; focus moves to Command input.
3. Type characters; VoiceOver announces live region result count.
4. `Arrow Down` — first option focused; VoiceOver announces option text.
5. `Enter` — item selected; popover closes; trigger announces new value.

---

## Pragmatic Stop Rule

Stop and deliver when:
1. All ARIA roles, states, and properties are documented against WAI-ARIA APG patterns.
2. WCAG SC identifiers are mapped to each requirement.
3. Keyboard interaction table is complete for all interactive states.
4. Focus management (open, trap, close, async) is specified.
5. Any `aria-live` regions are typed (role, atomic, relevant) with trigger timing.
6. Reduced-motion implementation exists at the CSS or Framer Motion level.
7. Screen reader test sequences are written for each AT+OS combination required.
