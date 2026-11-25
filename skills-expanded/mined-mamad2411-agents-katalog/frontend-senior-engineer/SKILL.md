---
name: frontend-senior-engineer
description: "Senior React/Next.js: responsive, a11y, states, forms, performance. Use when building or reviewing frontend UI components."
---

# Frontend Senior Engineer

## Overview

Implement UI at a senior engineer quality level. Every component accounts for loading, error, empty, and edge case states. Accessibility is not optional — it's a requirement. Performance is a feature, not an afterthought.

**Core principle:** A COMPONENT IS NOT DONE UNTIL IT HANDLES EVERY STATE. If it only shows the happy path, it's not finished.

## The Iron Law

```
EVERY DATA-FETCHING COMPONENT MUST HANDLE FOUR STATES: LOADING, EMPTY, ERROR, SUCCESS
```

No exceptions. Not for "simple" components. Not when "it's just internal." Not ever.

## When to Use

**Use this when:**
- Implementing UI from a spec + architecture plan
- Reviewing existing frontend code
- Adding new pages, components, or features
- Debugging frontend rendering issues

**Use this ESPECIALLY when:**
- The component seems "too simple for error handling"
- Someone says "we'll add loading states later"
- You're tempted to use `useEffect` for data fetching
- The design only shows the happy path

**Don't skip when:**
- "It's just a demo/prototype" (prototypes become production)
- "The API is internal and always works" (it won't)
- "It's a small component" (small components can fail too)

## The Four States (Mandatory)

```tsx
function ProjectList() {
  const { data, isLoading, error } = useQuery(...)

  // 1. LOADING — Show immediately (no artificial delays)
  if (isLoading) return <ProjectListSkeleton />

  // 2. ERROR — Human-readable + actionable
  if (error) return (
    <ErrorState
      title="Failed to load projects"
      message={error.message}
      action={<Button onClick={refetch}>Try Again</Button>}
    />
  )

  // 3. EMPTY — Informative + next action
  if (!data?.length) return (
    <EmptyState
      title="No projects yet"
      description="Create your first project to get started."
      action={<CreateProjectButton />}
    />
  )

  // 4. SUCCESS — The actual data
  return <ProjectCards projects={data} />
}
```

## Mandatory Checks (Every Component)

### 1. Accessibility (WCAG 2.1 AA)

| Check | Implementation | Why You'll Skip | Reality |
|-------|---------------|-----------------|---------|
| Semantic HTML | `<nav>`, `<main>`, `<button>` not `<div onClick>` | "A div works fine" | Screen readers need semantics |
| Keyboard nav | All interactive elements reachable via Tab | "Everyone uses a mouse" | 1 in 4 users has a motor disability |
| Focus management | Trap focus in modals, return on close | "It's a small modal" | Keyboard users get stuck |
| Color contrast | 4.5:1 text, 3:1 large text | "The brand colors look fine" | 8% of users are colorblind |
| Screen reader | ARIA labels, live regions | "I'll add it later" | You won't. Do it now. |

### 2. Responsive Design

```
Mobile-first CSS (base = mobile, md = tablet, lg = desktop)
Test at: 320px (small phone), 768px (tablet), 1024px (desktop), 1440px (wide)
Touch targets: ≥ 44×44px (WCAG 2.5.5 — thumb zone)
No horizontal scroll at ANY breakpoint
```

### 3. Form Validation Patterns

```tsx
// DO THIS:
// - Validate on blur (not every keystroke)
// - Validate on submit (always)
// - Inline errors next to field
// - Server errors map to correct field
// - Double-submit prevention

const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
  resolver: zodResolver(schema),
})

// DON'T DO THIS:
// - Validation only on submit
// - Alert/Toast for field errors
// - Clear fields on validation error
// - No loading state on submit button
```

### 4. Performance Budget

| Metric | Target | Hard Limit |
|--------|--------|-----------|
| Bundle per page | < 200KB gzipped | 300KB |
| LCP | < 2.5s | 4.0s |
| INP | < 200ms | 500ms |
| CLS | < 0.1 | 0.25 |
| Lighthouse score | > 90 | > 80 |

## Decision Tree

Use this before writing a single line of component code.

```
Is this component read-only (no interactivity, no client hooks)?
├── YES → React Server Component (RSC). Fetch in the component body.
│          Only add "use client" when you need onClick / useState / useEffect.
└── NO  → Client component. Then:
           Does it fetch data?
           ├── YES → Use React Query (useQuery) or SWR.
           │          Never useEffect + fetch. Never.
           └── NO  → Local state (useState/useReducer) is fine.

Where should state live?
├── Needed by ONE component only         → useState inside that component
├── Needed by a small subtree (≤3 deep)  → prop drilling (explicit, traceable)
├── Needed across a feature / many pages → React Query cache (server state)
│                                           OR Zustand/Jotai (client state)
└── Needed app-wide (auth, theme, locale)→ React Context
     ⚠ Wrap only the subtree that needs it.
     ⚠ Memoize the context value: const val = useMemo(() => ({user, logout}), [user])
        Missing this memo re-renders EVERY consumer on every parent render.

Should I memoize?
├── useMemo / useCallback
│   ├── YES if: expensive computation (>1ms), referential stability required
│   │           (object/array passed to React.memo child or dep of another hook)
│   └── NO  if: primitive value, component re-renders cheap, "feels slow" (profile first)
└── React.memo
    ├── YES if: pure presentational component with stable props, list item rendered 50+× 
    └── NO  if: parent rarely re-renders, component has cheap render, props include callbacks
                (memoize the callback with useCallback first, then consider React.memo)
```

## Worked Example

**Feature: Users List page** — all four states + form with validation + double-submit guard.

Full annotated code (RSC shell → client list → create-user form) lives in
[REFERENCE.md](./REFERENCE.md). Key decisions narrated there:

- Why the page shell is an RSC and only the interactive parts are `"use client"`
- How React Query drives loading / error / empty / success without a single `useEffect`
- How `react-hook-form` + Zod give blur validation, submit validation, and field-level
  server errors without re-inventing the wheel
- How `isSubmitting` from `useForm` prevents double-submit without any extra state

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I'll add loading states later"
- "This component is too simple for error handling"
- "The design doesn't show error states, so I'll skip them"
- "useEffect is fine for this one fetch" — it's not; use React Query or RSC
- "I'll just use the array index as the key" — index keys break diffing on reorder/delete
- "I'll pass this prop through five components" — that's prop drilling; use Query cache or context
- "I don't need to test on mobile"
- "The colors have enough contrast" (without checking)
- "Keyboard navigation works fine" (without testing)
- "This custom dropdown doesn't need ARIA" — yes it does; use `<select>` or radix-ui

**ALL of these mean: STOP. Handle the missing concern first.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "What happens when this fails?" — You didn't handle error state
- "What does it look like on mobile?" — You didn't test responsive
- "I can't tab to this button" — You missed keyboard navigation
- "The colors blend together" — You didn't check contrast
- "This dropdown is broken in Safari" — You built a custom control without ARIA/keyboard support

**When you see these:** STOP. Fix the missed state before adding new features.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll add error handling later" | You'll forget. Production will remember for you. |
| "The skeleton is ugly, I'll skip it" | A spinner is worse. Blank screen is worst. |
| "It works on my screen" | Your screen is not the only screen. |
| "This component is internal only" | Internal tools have users too. |
| "useEffect is standard for data fetching" | Not anymore. Use RSC or React Query. |
| "key={index} is fine, the list never reorders" | Lists always eventually reorder or delete. Use stable IDs. |
| "I'll just use Context for everything" | Unmemoized context value causes every consumer to re-render on every parent update. Profile before adding context. |
| "I'll memoize everything to be safe" | Premature memoization hides bugs and costs more than it saves. Profile first; memoize what the profiler flags. |
| "This custom select only needs onClick" | Custom interactive controls need full keyboard support (Enter/Space/Escape/Arrow) and correct ARIA roles or they are broken for keyboard and screen-reader users. |

## Related Skills

- **spec-first-development** — spec defines all four states
- **test-engineer** — tests verify loading, empty, error states
- **performance-engineer** — measures Core Web Vitals
- **edge-case-hunter** — finds missing mobile/responsive scenarios

## Self-Review (Before PR)

- [ ] Every data-fetching component handles all four states
- [ ] Keyboard navigation tested (Tab through entire flow)
- [ ] Screen reader tested (VoiceOver/NVDA)
- [ ] Tested at 320px, 768px, 1024px, 1440px
- [ ] No `console.log`, no `any`, no unused imports
- [ ] Lighthouse score > 90
- [ ] Form validation: blur + submit + inline errors + double-submit prevention
- [ ] Error boundaries wrap each feature module
