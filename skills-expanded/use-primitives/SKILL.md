---
name: use-primitives
description: >
  The UI primitives — one owner per kind of thing, and gates that refuse hand-rolled copies. Load it
  before writing a heading, a modal, a side panel, a button, an empty state, or anything that "just
  needs a div"; also when a gate refuses your markup and the message names a primitive you have not
  met. The point of the layer: shadcn/ui with ONE owner per kind of thing, and every colour taken as a
  TOKEN — so the owner repaints his whole project from the panel in a single move. An element with a
  literal colour does not break, it silently leaves that system. There is exactly one modal here, a
  hand-built one is refused by a gate, headings never carry raw classes, and a size never shrinks as
  the screen grows. Each rule replaced a real mess, not a preference.
---

# use-primitives

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

## 1. One owner per kind of thing

`components/ui/` — shadcn/ui plus `lucide-react` icons plus Sonner for toasts. No other UI library.
Twenty-four primitives live there today; read the folder rather than guessing what exists.

The rule underneath all of it: **if a kind of thing has an owner, you use the owner.** A second
implementation of the same thing is not extra work, it is a fork of the product's look that nobody
declared.

## 2. 🔒 Text is a primitive — `components/ui/typography.tsx`

Never a hand-classed heading. `check:typography` refuses `raw-heading` — an `<h1…h6>` with its own
`className`.

Bought with: nine different descriptions of `<h1>` in one project (`text-xl` on panels, `text-4xl` in
the blog) and forty-five paragraph variants. Types were fine and the build was green the whole time —
which is exactly why a gate exists instead of a style guide.

Two more refusals from the same gate, and both are worth knowing as facts about people, not code:

- **`shrinking-text` / `shrinking-space`** — `text-4xl md:text-3xl`, bigger on a phone than on a
  monitor. It shipped in eight places including every `h2` of every content page. **One exception**:
  `input` and `textarea` stay at 16px, because Safari zooms the whole page when a field is smaller.
- **`font-family-in-heading`** — the family is chosen by the primitive, not by the file. `font-serif`
  lived in two files out of ten, and those pages read as if they came from a different project.

Page chrome has an owner too: `PageHeader`. A bare `<header>` outside it is refused (`raw-page-header`).

## 3. 🔒 One modal in the whole product — `AppDialog`

`components/dialog/app-dialog.client.tsx`. It owns the portal, the scrim, the focus trap, Escape and
the scroll lock. A side panel is `components/ui/sheet.tsx`.

`check:dialogs` refuses `hand-rolled-modal` (a full-screen backdrop assembled by hand) and
`hand-rolled-portal` (`createPortal` into `body`).

Bought with: eight windows of three species, three of them built from bare `div`s — no
`role="dialog"`, no focus trap, no Escape, so a keyboard user could not close them at all. Overlays
had drifted to `z-50`, `z-[70]` and `z-[200]`, and two stacked windows swallowed each other's clicks.

🔒 **A dialog's dictionary is never imported by value into a client file** (`dialog-dict-in-client`).
Chrome words are 82 languages; the server calls `appDialogUi(lang)` and passes the result as the `ui`
prop. From a client file only `import type` is legal. Otherwise 82 languages ship to the browser on
every page that can open a window.

## 4. 🔒 Colour by token — this is what makes the whole thing worth doing

Everything above buys one property, and it is the reason the layer exists:

> **The owner changes his palette in the panel, and the entire project changes with it — in one move,
> without a rebuild.**

The chain: panel → `DESIGN-CONFIG` → CSS variables → every primitive at once. Nothing in between
knows the colour; each element only knows its ROLE — `primary`, `muted`, `destructive`, `border`.

So a literal colour is not a small sin. An element painted `#7c5cff` keeps that colour when everything
around it becomes green — it does not break, it silently leaves the system, and it is found by the
owner on the day he rebrands, not by you today. An inline style is the worst case: it outranks classes
and does not hear the theme at all.

The same for the rest of the scale — spacing, radii, the type scale, fonts: all of it is
`DESIGN-CONFIG`. Empty there means "the owner has not spoken", and the theme answers
(`config/design/design-minimal-001.css`). Never copy theme values into a second place: two palettes
diverge on the first edit, and silently — the page looks fine, it just no longer matches the CSS.

Fills come in pairs: `bg-primary` with `text-primary-foreground`. Half a pair is unreadable text in
exactly one theme — the half nobody opens while building. `check:contrast` and `check:sections` refuse
both mistakes in their own layers; the reflex is the same everywhere.

## 5. When there is genuinely no primitive for it

Then it is not a primitive — it is a **widget** of its route (`use-widgets`), and its unusual look is
the whole point. What must not happen is a third road: a new shared component quietly added beside
`components/ui/` because it felt reusable. Reusable is a decision with an owner and a maintenance
cost, and it is the owner's to make, named in a step.

The exception that proves it: something a SECOND project would want, carrying real logic and needing
the build, is a **tool** — `_tools/`, `use-tools`.

## 6. Before you call it done

- `npm run check:typography`, `check:dialogs`, `check:contrast`, `check:layout` — each guards a
  different primitive's territory.
- Open the thing in **both themes** and in a narrow window; then reach it with the keyboard alone —
  Tab in, Escape out. A window you cannot leave without a mouse is broken however it looks.
- If you wrote something that felt like it should already exist, say so in your report: that is how
  the missing primitive gets noticed instead of being re-invented a fourth time.

- **Foreign knowledge about these components** lives in the vendored `shadcn` skill; `use-shadcn`
  says when it may be used here and where our law overrules it — the dialog above all.
