---
name: canvas-ship
description: "Finishing a standalone HTML page: the accessibility and robustness pass, respecting reduced motion, testing a file that opens from disk with no server, keeping it one portable file, and the final check before it is done. Read before calling a canvas page finished."
---

# Finishing a standalone page

The page works on your machine; this is the pass that makes it hold up when
someone else double-clicks it. The `canvas` skill built it, `canvas-interactive`
gave it behaviour, `canvas-data` gave it data; this is the last mile.

## 1. The accessibility pass

- **Real semantics**: one `<h1>`, headings in order, `<button>` for actions,
  `<a href>` for links, `<label>` tied to every field (wrap it, or `for`/`id`).
  Landmarks (`<header>`, `<main>`, `<nav>`) for a page with structure.
- **Keyboard**: Tab reaches every control in a sensible order, Enter and
  Space operate them, Escape leaves a panel or dialog. A visible
  `:focus-visible` ring on each. Nothing works on hover alone.
- **Contrast**: body text and controls meet a comfortable ratio on their own
  background, in both themes. A faint grey on a near-white card that looks
  fine on your screen can fail on another; keep text clearly darker or
  lighter than its surface.
- **Names**: an icon-only button has an `aria-label`; an image has `alt` (or
  `alt=""` when decorative); a form field has a visible label, not only a
  placeholder.
- **State out loud**: a live result or a status message sits in an
  `aria-live="polite"` region so a change is announced, not only shown.

## 2. Respect reduced motion

Any animation beyond a simple hover is wrapped so it does not run for someone
who asked the OS for less:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

A `requestAnimationFrame` loop that is decorative checks
`matchMedia("(prefers-reduced-motion: reduce)").matches` and stays still or
runs minimally; a loop that is the whole point (a game, a live visualiser)
may continue, but nothing autoplays a big motion in the first frame.

## 3. Robustness

- **Guard every optional API**: `localStorage`, `navigator.clipboard`,
  `matchMedia`, the File API. A `file://` page or a private window may lack
  them; wrapped, the page degrades instead of dying (`canvas-data`).
- **Clipboard**: write inside the click handler, catch the rejection, and
  fall back to selecting the text so the person can copy manually.
- **No uncaught throw on first interaction**: a parse or a computation that
  can fail is wrapped and shows a message on the page.
- **No blocking dialogs**: no `alert`/`confirm`/`prompt`; a confirmation is a
  visible row in the page.
- **Empty and error states exist**: an empty list, a failed import, a field
  left blank each have a designed state, not a blank or a console error.
- **The page is correct at rest**: it renders its initial state once at load,
  before any interaction (the `canvas` skill's "complete at rest").

## 4. One portable file

The point of a canvas page is that it travels as a single file.

- CSS and JS inline; small images and icons as inline SVG or `data:` URIs.
- A real library from a pinned CDN `<script>` is allowed and keeps the file
  portable (it loads over the network when opened); inlining a whole
  framework's source is not the goal, a CDN script is.
- No build step, no `node_modules`, no separate `.css`/`.js` the page needs
  beside it. If the project genuinely wants split files, that is a different
  deliverable; a canvas page is the one-file kind.
- Keep it under a few megabytes; a large inlined image as a `data:` URI
  bloats the file and slows the open. Resize or compress it first, or load it
  from a CDN if it is public.

## 5. Test it the way it will be opened

- **Open the actual file from disk** (`file://`), not through a dev server.
  Behaviour differs: some APIs are stricter, module scripts may not load, and
  this is how the person will open it.
- If a `preview` or screenshot tool is available in the session, take one
  look: it renders light and dark at desktop and phone widths and lists
  overflow, colours that ignore the theme, blocked loads and console errors.
  Make one pass of fixes for what it shows, then stop; do not loop.
- Check the real widths: 360px (no sideways scroll, nothing clipped, the
  primary control in reach), and a wide screen (content not stranded in a
  thin centred column with empty bands).
- Click through the real path once: enter, compute, save, reload, load back.
- For a page whose point is logic (money, dates, scoring, parsing), run its
  core function on one sample input in your head or in a scratch file and
  confirm the number.

## 6. The final check

- Opens from a double-click, no server, nothing missing, no console error.
- Reads in light and dark; every colour from a token; `body` sets its
  background.
- Keyboard-complete with a visible focus ring; contrast comfortable in both
  themes; icon buttons and fields named.
- Reduced motion respected; no autoplaying big motion in the first frame.
- Optional APIs guarded; no blocking dialogs; empty and error states
  designed.
- One portable file (own code inline, any library a pinned CDN script);
  under a few megabytes.
- Complete and correct at rest; the real path works end to end.
- Specific to its subject, not one of the generated defaults.
