---
name: nextjs-ui-implementation
metadata:
  stack: [nextjs, react, tailwind]
description: Apply when implementing or modifying UI in the frontend app - pages, routes, layouts, styling, Tailwind classes. Covers browser testing, state verification, Figma comparison, and pixel-perfect workflow.
---

# UI Implementation Workflow

Follow this workflow for pixel-perfect UI implementation.

## 1. Learn from Existing Patterns First

Before implementing:
- Read similar existing components in the codebase
- Study layout patterns: flex-col vs absolute positioning, gap values
- Match existing conventions: class order, state transitions, naming

Example: Building `ComboboxWithLabel`? Read `SelectWithLabel` and `InputWithLabel` first.

## 2. Browser Testing During Development

- Test changes in real browser environment AS YOU BUILD
- Don't wait until "done" to test
- Test on the CORRECT route specified by user
- Take screenshots at each state to verify

## 3. Test All UI States

Verify each state:
- [ ] **Empty/default**: No value, not focused
- [ ] **Open/active**: Dropdown open, input focused
- [ ] **Selected/filled**: Has value, not focused
- [ ] **Error**: Validation errors displayed
- [ ] **Disabled**: Non-interactive appearance
- [ ] **Loading**: Async operations in progress

## 4. Verify Against Design Specs

- Compare with Figma designs pixel-by-pixel
- Check spacing, typography, colors, transitions
- Verify behavior matches design intent
- Don't assume - validate every detail

## 5. Console and Error Checking

Before presenting:
- [ ] Zero console errors
- [ ] No React warnings (unknown props, invalid HTML)
- [ ] No layout shift or flicker during transitions
- [ ] Keyboard navigation works
- [ ] Focus states are visible

## 6. Iterate Until Perfect

- If something looks wrong, keep iterating
- Don't present UI changes with known issues
- Match reference designs exactly, not approximately

## Design Token Syntax

**PascalCase for design tokens**:
```
bg-SurfaceInputOnBodyDefault
text-ContentNeutralDefault
border-BorderNeutralSubtle
```

**Lowercase for standard Tailwind**:
```
mt-4 px-2.5 flex gap-1 rounded-md
```

## Common Pitfalls to Avoid

- Using absolute positioning when flex-col is correct
- Testing on wrong route or with wrong data
- Passing invalid props to components
- Assuming layout looks correct without browser verification
- Presenting "done" when console shows errors
- Guessing at spacing values instead of matching patterns

## Goal

Pixel-perfect implementation on first presentation.
Browser testing + learning patterns + state verification = success.
