---
name: ui-design-principles
description: The seven UI design principles - hierarchy, progressive disclosure, consistency, contrast, accessibility, proximity, alignment - turned into concrete, checkable rules for React + Tailwind + shadcn product UI. Use when designing or reviewing dashboards, forms, tables, app shells, empty states, and multi-step builders. Pairs with impeccable and minimalist-ui; this one is the checklist you verify against, not the aesthetic.
---

# UI design principles

Source: Figma's *Seven essential UI design principles* (Thomas Lowry). This skill is the
operational form: each principle below has rules you can check in a diff or a screenshot, not
advice you can nod along to.

> "Our job as digital designers is to help users navigate to the content and features they need,
> to accomplish what they want to do."

**Use this alongside a taste skill, not instead of one.** `impeccable` or `minimalist-ui` decide
how it *looks*; this decides whether it *works*. A screen can pass every rule here and still be
ugly, and it can be beautiful while failing half of them.

---

## The seven principles, as rules

### 1. Hierarchy — the eye must land somewhere first

Every screen has exactly one primary action, and it must be the most visually prominent thing.

- Pick the primary action per screen. It gets the solid/filled button. Everything else is
  `outline`, `ghost`, or a link. Two filled buttons side by side means you have not decided.
- Size and weight carry rank: page title > section heading > label > body > helper text. If two
  levels render at the same size and weight, they are the same level — merge them or differentiate.
- Never signal rank with colour alone (see Accessibility).
- **Check:** squint at the screen, or blur it. The thing you still see should be the thing the
  user came to do. If a decorative card outranks the submit button, hierarchy is wrong.

### 2. Progressive disclosure — show the next decision, not all decisions

- A long form becomes steps. A step shows what is needed *now* and nothing else.
- Always show position: "Step 2 of 4", a tab that is visibly selected, a breadcrumb. Users must
  know where they are and how much is left, or they abandon.
- Advanced, destructive, or rare options live behind a disclosure — an accordion, a "More"
  menu, a secondary panel. They are not deleted, they are deferred.
- Empty states are a disclosure surface: say what this is, and offer the one action that fills it.
- **Check:** count the decisions visible at once. If a first-time user must understand more than
  about five things before acting, split it.

### 3. Consistency — the same thing looks and behaves the same everywhere

This is the principle most often broken by accident, especially mid-migration.

- One component per job. If two buttons in the app differ, the difference must be meaningful.
- Spacing comes from the scale, never from a one-off. `p-4` yes; `padding: 13px` no.
- Colours, radii, shadows and type come from tokens (`tailwind.config.ts`, CSS variables). A
  literal hex in a component is a bug unless it is deliberately outside the system.
- The same verb means the same thing: "Save" always persists, "Submit" always advances state.
  Do not use "Save" on one screen and "Apply" on the next for identical behaviour.
- **Check:** grep the diff for hardcoded hex, px values, and duplicate component variants.
  Deviations need a stated reason, because an unexplained deviation reads as a bug to the user.

### 4. Contrast — loudness is a budget, spend it deliberately

- Reserve the strongest contrast for the primary action and for genuine danger. If everything
  shouts, nothing does.
- Destructive actions look destructive (`destructive` variant), and their safe alternative looks
  calm. Never make Delete and Cancel visually equal.
- Use contrast to separate zones: page ground, surface/card, and elevated overlay should be
  distinguishable without borders doing all the work.
- **Check:** if you removed all colour, could you still tell the primary action from the
  secondary? If not, you are relying on hue alone.

### 5. Accessibility — not a pass at the end, a constraint while building

More than one in four people worldwide have a vision impairment. WCAG minimums:

- **Contrast ratio ≥ 4.5:1** for body text, ≥ 3:1 for large text and for UI component boundaries.
- **Never colour alone.** A red border must be joined by an icon or a message. A status must have
  a label, not just a dot.
- **Keyboard:** every interactive element reachable by Tab, in a sensible order, with a *visible*
  focus ring. Never `outline: none` without a replacement.
- **Names:** every icon-only control needs `aria-label`. Every input needs a real `<label>` or
  `aria-label` — placeholder text is not a label, it disappears when typing starts.
- **Semantics:** a thing that navigates is an `<a>`; a thing that acts is a `<button>`. A `<div>`
  with an onClick is unreachable by keyboard and invisible to screen readers.
- **Targets:** at least 44×44px of hit area for anything touch-reachable.
- **Check:** Tab through the whole screen without a mouse. If you cannot complete the main task,
  it is broken regardless of how it looks.

### 6. Proximity — related things sit together, unrelated things do not

- Group by spacing before reaching for borders or cards. Whitespace is the cheapest grouping tool
  and the quietest.
- A label belongs to its input: the gap between them must be visibly smaller than the gap to the
  next field. If the spacing is uniform, the eye cannot tell what pairs with what.
- Destructive actions are physically separated from routine ones, so a misclick is unlikely.
- **Check:** for any element, is the nearest thing to it actually the most related thing? If a
  field sits closer to the previous field's helper text than to its own label, fix the rhythm.

### 7. Alignment — invisible lines the eye can still feel

- Pick a grid and hold it. Content shares left edges down the page; nothing is "almost" aligned.
- Labels, inputs and helper text share an axis. Numbers in a table are right-aligned; text is
  left-aligned; headers match their column.
- Optical alignment beats mathematical alignment: icons and round shapes often need a nudge to
  *look* centred.
- **Check:** drag a straight edge — or a browser ruler — down the layout. Every stray edge is a
  small, cumulative signal of carelessness.

---

## Four practices

- **Perspective.** Place elements in the order of the user's task, not the order of your data
  model. The API's field order is not an information architecture.
- **Effortless.** Good interfaces are invisible. Consistent navigation, immediate feedback on
  every interaction, and a shortcut where it genuinely helps.
- **Shortcuts.** Speed up the repeated action: Enter submits, Esc closes, `/` focuses search.
- **Test.** Watch someone use it. Regular testing catches what reading the diff cannot.

---

## Applying this to product UI (dashboards, forms, tables)

The article's examples are general; these are the recurring failures in product interfaces.

| Surface | Most common failure | Rule that catches it |
|---|---|---|
| Sidebar | icons with no labels; active state too subtle | Hierarchy, Accessibility |
| Empty state | bare centred text like "no results" | Progressive disclosure |
| Toolbar | controls of unequal height, edges not aligned | Alignment |
| Table | every column the same weight; no zebra or hover | Hierarchy, Proximity |
| Form | placeholder used as label; uniform spacing | Accessibility, Proximity |
| Multi-step builder | no position indicator | Progressive disclosure |
| Destructive action | same weight as the safe one | Contrast |
| Loading | layout jumps when data arrives | Consistency |

**Icon-only navigation is the one to fight hardest.** It is the most common "clean" choice and the
most costly: it forces every user to learn a private vocabulary, and it fails screen readers
outright. If space is tight, use a collapsible rail that shows labels when expanded and
tooltips plus `aria-label` when collapsed — never bare icons with nothing else.

---

## Review checklist

Run this before claiming a screen is done. It is a verification pass, not a feeling.

1. One primary action, and it is the most prominent element.
2. Type scale has visible steps; no two adjacent levels look alike.
3. Every spacing value comes from the scale.
4. No hardcoded colour; everything resolves to a token.
5. Body text ≥ 4.5:1 contrast. Checked, not assumed.
6. No state communicated by colour alone.
7. Tab reaches every control, in order, with a visible focus ring.
8. Every icon-only control has an accessible name.
9. Labels are real labels, not placeholders.
10. Related items are closer to each other than to anything else.
11. Shared left edge held down the page; table columns aligned by type.
12. Empty, loading and error states all designed — not just the happy path.
13. Destructive actions are visually and physically distinct from safe ones.
14. Layout does not shift when data loads.
15. Works at narrow width and in both light and dark themes.

A screen that looks right but no longer performs its task is a failure, not a redesign. Verify
behaviour after any visual change.
