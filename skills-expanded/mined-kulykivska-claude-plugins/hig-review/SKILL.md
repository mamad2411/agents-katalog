---
name: hig-review
description: >-
  Review a screen, mockup, screenshot or SwiftUI/web code against Apple's
  Human Interface Guidelines: navigation (sidebar or tab bar, at most five
  tabs), large titles, segmented controls, sheets and popovers, the type
  ramp and Dynamic Type, 44pt targets, the 8pt grid, light and dark mode,
  WCAG AA contrast, SF Symbols style icons, empty states and accessibility
  (VoiceOver labels, focus order). Returns ranked findings with fixes.
  Trigger on "HIG review", "does this look like an Apple app", "review
  this screen", "is this native enough", "check against Apple guidelines",
  "accessibility review of this screen", or before a design is approved.
---

# HIG review

**Product name.** `{{app}}` here and in the references stands for the user's product. Take its name from the project (README title, package.json, app.json, Info.plist) or ask once, then write every example with that name and the product's own screens.

Apple-grade means the user never has to learn the interface: it behaves
like the rest of the platform, reads at every text size, and works without
sight. This review checks a screen against that bar. The detailed checklist
with values is in `references/hig-checklist.md`.

## Inputs

Screenshots or a mockup (ideally in light and dark, at the default and at
the largest accessibility text size), the SwiftUI or web source if it
exists, and the platform targets (iPhone, iPad, Mac, web). If only one
appearance or size is provided, review it and list the others under "could
not see".

## The pass

One pass over the screen, in this order; each area names what to check.

1. **Navigation structure**. iPhone: a tab bar for 3 to 5 top-level
   sections, never more than 5 (the rest go into the sections themselves,
   not a "More" tab if avoidable). iPad and Mac: a sidebar when there are
   more sections or deep hierarchies; iPad tab bars that convert to a
   sidebar are fine. Hierarchy uses push navigation with a back button that
   names the previous screen. Tabs never trigger actions.
2. **Titles and bars**. Large title on top-level screens, collapsing to
   inline on scroll; inline titles on detail screens. At most one primary
   action in the navigation bar's trailing position; toolbars for secondary
   actions.
3. **Controls**. Segmented controls for 2 to 5 mutually exclusive views of
   the same content, not for navigation or actions. Toggles for on and off
   settings, not for choices. System pickers and menus before custom ones.
4. **Modality**. Sheets for self-contained tasks, with detents (medium,
   large) and a grabber when resizable; a clear Cancel or Done. Popovers on
   iPad and Mac only (they become sheets on iPhone). Alerts only for
   something that needs a decision now, with at most two or three buttons.
   Full-screen covers only for immersive tasks.
5. **Typography**. The system text styles (Large Title through Caption 2) or
   a custom font mapped to them, scaling with **Dynamic Type** up to the
   accessibility sizes without truncating essential text. At most two
   weights of emphasis per screen.
6. **Layout and spacing**. 8 pt grid (4 pt for tight internals); standard
   margins (16 pt on iPhone, 20 pt on larger widths, or the system readable
   content guides); respects safe areas and the Dynamic Island; content not
   hidden behind the home indicator.
7. **Touch targets**. At least 44x44 pt for everything tappable, including
   icons in rows; at least 8 pt between adjacent targets.
8. **Colour and appearance**. Works in light and dark, using semantic
   colours (label, secondaryLabel, systemBackground, tint) not fixed hex;
   one tint colour for interactive elements; colour never the only carrier
   of meaning.
9. **Contrast**. WCAG AA: 4.5:1 for body text, 3:1 for large text (18 pt,
   or 14 pt bold) and for essential icons and control boundaries. Check both
   appearances.
10. **Iconography**. SF Symbols, or custom icons in the same style: matching
    weight to the adjacent text, consistent rendering mode, optical
    alignment with labels, filled variants for selected tab states.
11. **Empty, loading and error states**. Each exists, explains itself and
    offers one action (see the `ux-copy` skill in `product-design`).
12. **Accessibility**. Every control has a VoiceOver label that names its
    purpose, values and traits are set (selected, button, header), focus
    order follows the visual order, related items are grouped, decorative
    images are hidden, custom gestures have an accessible alternative, and
    Reduce Motion and Reduce Transparency are honoured.
13. **Web targets**. The same rules translate: 44 px targets, the system
    font stack or a mapped ramp that respects the user's font size, dark
    mode through `prefers-color-scheme`, focus rings visible, landmark
    roles and labels in place.

## Severity

- **Blocker**: an accessibility failure that locks someone out (unlabelled
  control, contrast under 3:1 on essential text, text that cannot scale,
  target far below 44 pt on a primary action), or broken navigation (more
  than five tabs, no way back).
- **Major**: clearly non-native behaviour or a guideline break most users
  will feel (a segmented control used as navigation, a custom alert, a
  missing dark mode, fixed-size type).
- **Minor**: polish (off-grid spacing, icon weight mismatch, title style).

## Output

| # | Screen and element | Finding | HIG area | Fix | Severity |
|---|--------------------|---------|----------|-----|----------|

Ranked Blocker, Major, Minor, then by how central the element is. The fix is
concrete: the control to use, the token to apply, the label text. After the
table: **What this review could not see** (appearances, text sizes, devices,
states not provided) and **Open questions**.

For motion and feel, run the checklist in the `delight-spec` skill as well;
the `hig-reviewer` subagent does both in one pass.
