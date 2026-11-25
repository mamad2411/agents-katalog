---
name: ui-part-tooltips
description: "Tooltips: what belongs in one and when a toggletip, a popover or visible text is right instead, measures, delays and the WCAG rules for content on hover and focus, ARIA for icon-only buttons, placement with collision handling, disabled controls and truncated text, touch, and a Radix sketch. Read before adding a tooltip or naming an icon-only control."
---

# Tooltips

The generated version: a `title` attribute on everything, or a styled
bubble that appears on the first frame of every hover, holds the only
explanation of a field and a link nobody can reach, never shows for the
keyboard, and does nothing on a phone. A tooltip is a short label or hint
for something focusable, shown after a pause, and never the only place
something important is said. The principles are in the `ui` skill, the
measures in `ui-layout`, the motion in `motion-interface` (section 3).

## 1. When a tooltip, and what instead

- Use them for the name of an icon-only control and for a short hint: the
  full text of a truncated value in a focusable cell, a keyboard shortcut
  ("Bold, Ctrl+B"), an abbreviation or a unit spelled out.
- Never for information the user needs to finish the task: help text sits
  under its field (`ui-part-forms`), an error beside its cause, and the
  reason an action is unavailable on the page itself ("On loan until 3
  Oct").
- Never for interactive or rich content (links, buttons, inputs, headings,
  images): that is a popover opened by a click, which takes focus
  (`ui-part-menus`, `ui-part-dialogs`).
- A button that already shows its word needs no tooltip, except to show its
  shortcut.
- The native `title` attribute is not a tooltip to rely on: it never shows
  for the keyboard or on touch, cannot be styled, and appears late.

| The need | Use |
|---|---|
| Naming an icon-only button | `aria-label` on the button, and a tooltip with the same words |
| A short extra hint on a focusable element | a tooltip, linked with `aria-describedby` |
| Help on touch, or help people read more than once | a toggletip: an "i" button that shows the text on tap until dismissed |
| Links, buttons, anything to act on | a popover |
| Anything needed to finish the task | visible text on the page |

## 2. Anatomy and measures

- Text only: one line if possible, two at most (under about 80
  characters), 12 to 14px and never below 12, sentence case, no full stop
  after a fragment.
- 240 to 320px wide at most, 4 to 8px by 8 to 12px of padding, a 4 to 6px
  radius, on an inverted surface (the text colour as its background) or on
  the overlay surface with a border; an arrow is optional.
- 6 to 8px from its trigger, above it by default, and never over the thing
  the user is working on (the field being typed in).
- A shortcut in `<kbd>`, in a quieter tone, after the words.

## 3. Behaviour (WCAG 1.4.13)

- Shown on hover after 300 to 500ms, and at once on keyboard focus
  (`:focus-visible`, not the focus a mouse click leaves behind).
- Once one is open, its neighbours open without the delay while the pointer
  moves along a toolbar (a skip delay of about 300ms).
- Dismissible: Escape hides it without moving focus or the pointer; it also
  hides on pointer leave and on blur.
- Hoverable: the pointer can move onto the tooltip without it closing.
- Persistent: it stays until the pointer or focus leaves or it is
  dismissed; no timer hides it.
- One at a time.
- Placement with collision handling: it flips to the other side when there
  is no room and shifts to stay 8px inside the window. Floating UI
  (`offset`, `flip`, `shift`), Radix Tooltip (`side`, `sideOffset`,
  `collisionPadding`), React Aria `TooltipTrigger`. The `popover="hint"`
  value and CSS anchor positioning are arriving in browsers but are not
  everywhere yet.

## 4. ARIA

- The bubble has `role="tooltip"`; the element it describes points to it
  with `aria-describedby` while it shows.
- An icon-only button is named by its own `aria-label` (or visually hidden
  text) with the same words as its tooltip, so it has a name while the
  tooltip is closed and on touch, where tooltips do not open.
- The name matches the words the tooltip shows, so voice control users can
  say what they see.
- Libraries wire this: Radix `Tooltip` (shadcn/ui), React Aria `Tooltip`,
  Ark UI and Bits UI tooltips, or Floating UI's `useHover`, `useFocus`,
  `useDismiss` and `useRole` hooks.

## 5. Disabled controls and truncated text

- A `disabled` button is skipped by the keyboard and gets no pointer events
  in some browsers, so its tooltip never appears. Say why it is unavailable
  on the page; or use `aria-disabled="true"` (it stays focusable, the press
  does nothing) with the reason in the tooltip or beside it; or, with
  Radix, wrap the disabled button in a `span` with `tabindex="0"` and make
  that the trigger.
- Truncated text gets a tooltip only when it is actually truncated
  (`scrollWidth > clientWidth`) and only on an element that is already
  focusable (a link, a cell in a grid); otherwise let the text wrap, or
  show it in full in the detail.

## 6. Phones and touch

- There is no hover on touch, so nothing may live only in a tooltip: icon
  buttons people use on phones get a visible label or sit in a labelled
  menu; help that matters becomes a toggletip with a 44px trigger.
- Shortcut hints are hidden where there is no keyboard
  (`@media (hover: none)`).

## 7. Themes and motion

- An inverted tooltip reaches 4.5:1 in both themes; on dark, a light
  surface or a dark one with a border (`ui-themes`).
- A fade of 100ms at most, no slide, no bounce; shown after the delay,
  hidden at once; nothing moves under reduced motion (`motion-interface`,
  section 3).

## 8. A sketch (Radix Tooltip)

```tsx
import * as Tooltip from "@radix-ui/react-tooltip";

// One provider near the root: 400ms before the first opens, neighbours at once.
<Tooltip.Provider delayDuration={400} skipDelayDuration={300}>
  <Tooltip.Root>
    <Tooltip.Trigger asChild>
      <button type="button" className="icon-button" aria-label="Duplicate invoice">
        <CopyIcon aria-hidden />
      </button>
    </Tooltip.Trigger>
    <Tooltip.Portal>
      <Tooltip.Content className="tooltip" side="top" sideOffset={6} collisionPadding={8}>
        Duplicate invoice
      </Tooltip.Content>
    </Tooltip.Portal>
  </Tooltip.Root>
</Tooltip.Provider>
```

```css
.tooltip {
  max-width: 280px;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  background: var(--text);
  color: var(--bg);
  font-size: var(--font-sm);
  line-height: 1.4;
}
```

- A project's own wrapper may set its own delay: check it. A delay of 0
  opens a tooltip on every pass of the pointer.
- Radix Tooltip does not open on touch, by design: the button's
  `aria-label`, and a visible label where the icon is not obvious, carry
  the meaning there.

## Check it

- Mouse: the first tooltip waits 300 to 500ms, its neighbours open at once,
  the pointer can rest on it, and it never covers the field in use.
- Keyboard: Tab to each icon button and its tooltip shows at once; Escape
  hides it and focus stays put.
- `preview`: "controls without a name" lists icon buttons with no name (a
  `title` passes that check but is still not a tooltip; give an
  `aria-label`); at 360px nothing the task needs sits only in a tooltip.
- A screen reader reads each icon button's name once, from its label.

## Avoid

Information the user needs to finish the task, and links or buttons, inside
a tooltip; tooltips on the first frame of a hover, or on hover only;
`title` as the tooltip; tooltips on disabled buttons that nobody can reach;
a tooltip repeating a visible label; tooltips as the only help on touch;
paragraphs in a bubble; a slow fade or a bounce; a tooltip over the field
being typed in; one that vanishes when the pointer moves onto it.
