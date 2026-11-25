---
name: mobile-only-responsive-navigation
description: Mobile-only responsive navigation guidance for RTL Persian sites. Use when improving hamburger menus, drawers, touch targets, and mobile theme controls without changing desktop layout.
---

# Mobile-only responsive navigation

Use this skill when modifying a production HTML/CSS/Vanilla JS site where the desktop design must remain unchanged and only mobile breakpoints may be improved.

## Non-negotiable scope

- All visual/layout changes for navigation, spacing, typography, header, hero, cards, and sections must be limited to existing mobile breakpoints such as `@media (max-width: 768px)` or the project breakpoint (`@media (max-width: 759px)`).
- Desktop navigation, desktop header, desktop spacing, desktop typography, desktop buttons, and desktop theme controls must stay visually identical.
- If a shared JavaScript change is needed, it must preserve desktop behavior and only add accessibility/state handling.

## Mobile navigation requirements

- Hide desktop navigation on mobile and control it with a real hamburger button.
- The hamburger button must expose `aria-expanded`, `aria-controls`, and a clear `aria-label`.
- For Persian/RTL layouts, the mobile drawer should open from the right (`inset-inline-start: 0` in RTL).
- The drawer must be above hero and content with a reliable z-index.
- Include a backdrop/scrim so the drawer does not visually merge with the hero.
- Touch targets must be at least 44px high/wide.
- Menu links must be easy to scan and tap.
- Close the drawer when:
  - the close button is clicked,
  - a menu link is clicked,
  - the user clicks outside/backdrop,
  - the Escape key is pressed.
- Lock body scroll while the drawer is open.
- Restore scroll when it closes.
- Do not create horizontal overflow.

## Mobile theme toggle

- Place the mobile theme toggle inside the drawer.
- Keep it compact, tidy, Persian, and clear: `تیره 🌙` and `روشن ☀️`.
- Active state must be obvious and accessible via `aria-pressed`.
- Preserve the current `localStorage` theme behavior.
- Do not visually change the desktop theme toggle.

## Motion and polish

- Drawer animation should be short, soft, and subtle.
- Avoid bounce, shake, heavy glow, excessive scaling, or constant animation.
- Respect `prefers-reduced-motion`.
- Use solid or frosted surfaces that remain readable in dark and light mode.

## Mobile audit checklist

- Section padding is not excessive.
- Large headings are readable and not cramped.
- Persian line-height is comfortable.
- Cards and CTAs fit the viewport.
- Contact/location cards are ordered and readable.
- Header logo and brand text fit without overflow.
- No horizontal scrolling at common widths (320, 360, 390, 414px).