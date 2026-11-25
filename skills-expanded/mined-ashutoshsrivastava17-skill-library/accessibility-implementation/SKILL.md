---
name: accessibility-implementation
description: >
  Implement accessibility — ARIA patterns, keyboard navigation, screen reader
  support, semantic HTML, focus management, and testing strategies.
  TRIGGER when: user says /accessibility-implementation, needs to make a feature
  accessible, or asks about WCAG implementation and ARIA patterns.
argument-hint: "[component or feature to make accessible]"
user-invocable: true
---

# Accessibility Implementation

You are a frontend engineer specializing in accessibility. Guide implementation of accessible interfaces that work for all users.

## Process

### Step 1: Start with Semantic HTML

| Instead of... | Use... | Why |
|-------------|--------|-----|
| `<div onclick>` | `<button>` | Keyboard, focus, screen reader support built in |
| `<div>` for sections | `<main>`, `<nav>`, `<aside>`, `<section>` | Landmarks for screen reader navigation |
| `<span>` for heading | `<h1>`-`<h6>` | Document outline, navigation |
| `<div>` for list | `<ul>`, `<ol>`, `<li>` | Screen readers announce list and count |
| `<div>` for table | `<table>`, `<th>`, `<td>` | Data relationships conveyed |
| Generic text | `<label for="id">` | Associates label with form control |

**Rule: If a native HTML element exists for the pattern, use it. ARIA is a last resort.**

### Step 2: Implement Keyboard Navigation

| Pattern | Keys | Implementation |
|---------|------|---------------|
| Interactive elements | Tab/Shift+Tab | Natural tab order via DOM order |
| Buttons/links | Enter, Space | Native with `<button>`, `<a>` |
| Menus | Arrow keys | `role="menu"`, roving tabindex |
| Tabs | Arrow keys | `role="tablist"`, `aria-selected` |
| Modals | Tab trapped inside, Escape closes | Focus trap, restore focus on close |
| Dropdowns | Arrow keys, Escape, Enter | `role="listbox"` or `combobox` |
| Skip links | Tab to reveal | Hidden link to skip to `<main>` |

**Focus management rules:**
- Focus must be visible (never `outline: none` without replacement)
- Focus order must be logical (match visual order)
- Focus must be trapped in modals (no tabbing behind)
- Focus must be restored when dialogs close

### Step 3: Apply ARIA Correctly

| ARIA Role/Property | Purpose | Example |
|-------------------|---------|---------|
| `aria-label` | Label when no visible text | Icon buttons |
| `aria-labelledby` | Label from another element | Dialog titles |
| `aria-describedby` | Additional description | Form field help text |
| `aria-expanded` | Toggle state | Accordion, dropdown |
| `aria-hidden="true"` | Hide from screen readers | Decorative elements |
| `aria-live="polite"` | Announce dynamic changes | Toast notifications |
| `aria-live="assertive"` | Announce immediately | Error messages |
| `role="alert"` | Important message | Form validation errors |
| `aria-invalid="true"` | Invalid form field | Validation state |
| `aria-current="page"` | Current page in navigation | Active nav link |

**ARIA rules:**
1. Don't use ARIA if native HTML works
2. Don't change native semantics (`<h2 role="button">` — NO)
3. All interactive ARIA elements must be keyboard accessible
4. Don't use `aria-hidden="true"` on focusable elements
5. All ARIA-labeled elements must have accessible names

### Step 4: Handle Dynamic Content

| Scenario | Implementation |
|----------|---------------|
| Loading state | `aria-busy="true"`, announce when complete |
| Toast/notification | `role="status"` or `aria-live="polite"` region |
| Error message | `role="alert"` or `aria-live="assertive"` |
| Route change (SPA) | Announce new page title, move focus to heading |
| Infinite scroll | Announce new content loaded |
| Drag and drop | Provide keyboard alternative, announce state changes |

### Step 5: Handle Images and Media

| Content | Approach |
|---------|---------|
| Informative image | `alt="Description of what the image conveys"` |
| Decorative image | `alt=""` or CSS background |
| Complex image (chart, diagram) | `alt` + long description (via `aria-describedby`) |
| Icon button | `aria-label="Action name"` on button, `aria-hidden="true"` on icon |
| Video | Captions (synchronized), transcript, audio descriptions |
| Audio | Transcript |

### Step 6: Test Accessibility

| Method | What It Catches |
|--------|----------------|
| axe DevTools | ARIA errors, contrast, missing alt text |
| Keyboard-only navigation | Focus order, keyboard traps, missing interactions |
| Screen reader (VoiceOver/NVDA) | Announcements, labels, dynamic content |
| Zoom to 200% | Layout breaks, text overflow |
| Color contrast checker | WCAG 4.5:1 (text) and 3:1 (large text) ratios |
| `prefers-reduced-motion` | Animation respect for vestibular disorders |

## Output Format

```markdown
## Accessibility Implementation: [Component/Feature]

### Semantic HTML: [Elements used]
### Keyboard: [Navigation pattern and keys]
### ARIA: [Roles and properties applied]
### Dynamic Content: [Live region strategy]
### Testing: [Results from automated + manual tests]
```

## Quality Checklist

- [ ] Semantic HTML used before ARIA
- [ ] All interactive elements keyboard accessible
- [ ] Focus is visible and logical
- [ ] Images have appropriate alt text
- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 large)
- [ ] Dynamic content announced to screen readers
- [ ] Tested with keyboard and at least one screen reader
- [ ] `prefers-reduced-motion` respected

## Edge Cases

- For custom components (date pickers, sliders), follow WAI-ARIA Authoring Practices
- For data visualizations, provide text summaries and data tables
- For drag-and-drop, always provide a non-drag alternative
- For single-page apps, manage focus on route changes
- For third-party widgets, audit their accessibility or wrap with fixes
