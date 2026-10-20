---
name: "react-native-ux-a11y"
description: "Figma-safe UX and accessibility rules for mobile (touch targets, contrast, form errors, loading). Partial merge from ui-ux-pro-max UX domain — never overrides Omantel design tokens."
version: 1
created: "2026-07-06"
updated: "2026-07-06"
sources_merged: "ui-ux-pro-max UX/a11y guidelines (adapted); Omantel CONSTR-007/008"
---

# React Native UX & Accessibility (Figma-safe)

**Authority order:** Figma design + `theme/` tokens + requirement.txt **>** this skill.  
Do **not** apply generic color palettes, font pairings, or visual styles from external UX libraries.

## Touch & interaction
- Minimum touch target **44×44 dp** (CONSTR-008).
- Primary CTAs: clear `accessibilityRole` (`button`, `link`, `header`).
- `accessibilityLabel` on every interactive element (match or paraphrase visible canvas label).
- Destructive actions: ConfirmationModal before API (CONSTR-004).

## Forms
- Inline validation before submit (e.g. MSISDN regex).
- Error text associated with field; do not rely on color alone.
- Disable submit while mutation in flight; show loading on button or skeleton.

## Loading & empty
- Skeleton placeholders during fetch — not blank screens.
- Empty state with optional CTA (e.g. "Add Number").
- Error toast with retry/dismiss on API failure.

## Visual (within Figma tokens only)
- Text contrast ≥ WCAG AA (4.5:1) using theme colors.
- Consistent spacing from `theme.spacing` — no arbitrary padding.
- Modal overlays: dimmed backdrop; focus trap on modal actions.

## Motion
- Prefer subtle transitions; respect reduced motion when detectable.
- Swipe-to-confirm: haptic on completion where platform supports.

## Anti-patterns (from UX review)
- Generic "AI slop" gradients or glassmorphism not in Figma.
- Replacing Omantel brand fonts with unrelated Google Font pairings.
- Hidden navigation — every screen reachable from registry/graph.
- Spinner-only loading on data-heavy screens without skeleton structure.
