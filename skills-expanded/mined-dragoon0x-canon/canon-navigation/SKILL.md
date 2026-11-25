---
name: canon-navigation
description: Use when designing, auditing, or refactoring navigation — top bars, sidebars, breadcrumbs, footer nav, mobile menus, tab bars, or any way-finding element. Covers information architecture, active state, keyboard navigation, skip links, mobile patterns, and the sidebar vs top-bar decision. Trigger when the user mentions nav, navbar, sidebar, menu, breadcrumb, hamburger, or header.
---

# CANON · Navigation

Navigation is a promise: where am I, where can I go, how do I get back. Break any of the three and the user is lost.

## Structural rules

Every page must answer three questions visually and semantically:

1. **Where am I?** — active state in the nav, breadcrumb or page title
2. **Where else can I go?** — primary nav visible or reachable in one tap
3. **How do I go back?** — browser back always works; "back" actions never leave them stranded

## Top bar vs sidebar

| Pattern | Use when | Don't use when |
|---|---|---|
| Top bar | ≤ 7 top-level sections, marketing, simple apps | > 7 sections, deep hierarchies |
| Sidebar | Apps with 8+ sections or nested nav, dashboards | Marketing pages, content-heavy reads |
| Hybrid (top + left) | Product with global sections + workspace nav | Simple apps — overkill |
| Bottom tab bar (mobile) | Apps with 3–5 primary sections | Web-first experiences, > 5 sections |

## Active state — not optional

Every nav item has two states at minimum: **default** and **active**. "Active" means "you are here." It must be **unmistakable at a glance**.

Active state options, in order of clarity:
1. Filled background + contrasting text
2. Left or bottom border in brand color (2–3px)
3. Bolder weight + color shift
4. Underline (text nav only)

**Color shift alone is not enough** — fails for color-blind users. Pair color with weight, underline, or background.

## Sizing

| Element | Dimension |
|---|---|
| Top bar height | 56–72px (64px is the sweet spot) |
| Sidebar width (expanded) | 220–280px |
| Sidebar width (collapsed icon-rail) | 56–72px |
| Nav item height (desktop) | 36–44px |
| Nav item height (mobile, tap target) | ≥ 44px |
| Nav item horizontal padding | 12–16px |
| Gap between items | 2–4px (stack), 16–24px (horizontal) |
| Bottom tab bar height | 56px + safe-area-inset-bottom |

## Mobile menu (hamburger)

Hamburger is acceptable but comes with costs. Known: 30–50% lower discoverability vs visible nav (Luke Wroblewski research).

When hamburger is fine:
- Secondary nav items only (primary nav stays visible via tab bar or top bar)
- Settings and account sections
- Truly space-constrained

When hamburger fails:
- Hiding the only path to primary actions
- Content-heavy apps where users need to jump between sections often

Better alternatives on mobile:
- Bottom tab bar for 3–5 primary destinations
- Visible top bar with overflow menu for extras

## Breadcrumbs

```
Home / Products / Electronics / Laptops / ThinkPad X1
```

Breadcrumbs are for hierarchical depth ≥ 3 levels. At 2 levels, they're noise.

- Use `<nav aria-label="Breadcrumb">` wrapping an `<ol>`.
- Current page is the last item; `aria-current="page"` and not a link.
- Separator is decorative; `aria-hidden="true"`.

## Skip link — required

```html
<a href="#main" class="skip-link">Skip to main content</a>
```

- First focusable element on every page.
- Visually hidden until focused (`:focus` reveals it).
- Jumps keyboard users past the nav to the content.
- WCAG 2.4.1 Bypass Blocks.

## Semantic structure

```html
<header>
  <a href="/" aria-label="Home">...</a>
  <nav aria-label="Primary">
    <ul>
      <li><a href="/products">Products</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main id="main">...</main>

<footer>
  <nav aria-label="Footer">...</nav>
</footer>
```

- Multiple `<nav>` elements allowed. Each needs a unique `aria-label`.
- Lists (`<ul>`) are the correct structure for nav items.
- `<header>` and `<footer>` at the page level; section-level headers don't need nav roles.

## Keyboard behavior

| Key | Behavior |
|---|---|
| Tab | Move through top-level nav items |
| Shift+Tab | Reverse |
| Enter / Space | Activate link/button |
| Arrow keys | Within a menu or menubar — WAI-ARIA disclosure/menu pattern |
| Escape | Close open submenu |

For dropdown menus: use the WAI-ARIA menu or disclosure pattern, pick one, implement it fully.

## Submenus and dropdowns

- **Open on click, not hover.** Hover menus break on touch and trap keyboard users.
- If hover is used for discoverability, still work on click, still work with keyboard.
- Submenus open toward the viewport center, not the edge.
- Close on: Escape, click outside, focus leaves.

## Active state indicator math

Active color needs 3:1 contrast against the nav background — that's the WCAG 1.4.11 non-text contrast floor. A bottom-border at 2px wins against a dim tint at 1.5:1.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| No active state | Users can't tell where they are |
| Active state is color-only | Fails for color-blind users |
| Hamburger hiding primary nav on desktop | Wastes screen real estate, lowers discovery |
| Nav items ≥ 8 deep in a top bar | Visual clutter, sidebar is better |
| Hover-only dropdowns | Broken on touch + keyboard |
| No skip link | WCAG 2.4.1 fail |
| Sticky nav taking > 20% of viewport height | Eats content on mobile |
| Breadcrumbs at depth 1 or 2 | Visual noise |
| Logo without `aria-label` when it's the home link | Screen reader says "link" with no context |
| Nav inside a `<div>` instead of `<nav>` | Semantic fail |

## Decision tree

```
How many primary destinations?
  ├─ 3–5 mobile, 5–7 desktop → Top bar or tab bar
  ├─ 8–15 → Sidebar
  └─ > 15 → Sidebar with grouping / sections

Is there nested hierarchy?
  ├─ Yes → Breadcrumb + sidebar
  └─ No → Top bar is fine

Is the menu opening dropdowns?
  └─ Click-to-open, not hover. Always.

Hamburger menu on desktop?
  └─ Almost never. Only if space is genuinely exhausted.
```

## Audit checklist

- [ ] Active state visible without relying on color alone
- [ ] Skip link is the first focusable element
- [ ] Nav is `<nav>` with `aria-label`
- [ ] Each `<nav>` has a unique label
- [ ] Tab target ≥ 44px on mobile
- [ ] Dropdowns open on click and work with keyboard
- [ ] Escape closes menus
- [ ] Focus-visible on every nav item
- [ ] Breadcrumb uses `aria-current="page"` on last item
- [ ] No nav inside `<div>` when `<nav>` applies

## Sources

- WCAG 2.2 · 2.4.1 Bypass Blocks, 2.4.3 Focus Order, 2.4.7 Focus Visible, 1.4.11 Non-Text Contrast
- WAI-ARIA Authoring Practices · Menubar, Disclosure, Breadcrumb
- Luke Wroblewski · Obvious Always Wins (hamburger research)
- Apple HIG · Navigation Bars, Tab Bars
- Material Design 3 · Navigation bar, Navigation rail, Navigation drawer
