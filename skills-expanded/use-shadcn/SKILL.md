---
name: use-shadcn
description: >
  WHEN the foreign `shadcn` skill may be used here, and what our law says louder than it. Load it
  before adding a shadcn component, before building a new BLOCK KIND for the catalogue, before
  building a WIDGET, and the moment the shadcn skill tells you to compose a Dialog, pick a toast, or
  place markup on a page. The shadcn skill owns HOW its components compose; this one owns WHERE the
  result is allowed to live — and in this project there are only two places, a catalogue block and a
  route widget. Four of its rules collide with ours; each collision below is resolved in our favour
  and says why, so you can follow the foreign skill everywhere else with a clear head.
---

# use-shadcn

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The `shadcn` skill (vendored, `.claude/skills/shadcn/`, provenance in its `SOURCE.md`) is genuinely
good and mostly agrees with us: semantic colours over literals, existing components over custom
markup, compose instead of reinvent. Use it. It has one blind spot, and it is not its fault — it
knows shadcn, it does not know that in this project **a page is not a place where you may put
things**.

## 1. The question that comes first, always

Before a single component is added: **what am I building?** → `CLAUDE.md`, *What goes on a page*.

A page here is a LIST OF BLOCKS in a language cell. Whatever appears on it is a **catalogue block**,
a **route widget**, or a **platform primitive**. There is no fourth source, and `check:page-composition`
refuses the build for a page that invents its own layout. The shadcn skill will never stop you from
writing a beautiful hand-laid page — this line is the only thing that does.

## 2. Two legal entries, in this order

**Entry one — a NEW BLOCK KIND. This is the main one.** In this project one does not work without
blocks: whatever the owner wants to create, he creates it as a block, so it is reusable by any page
of his site. The shadcn skill is at its best exactly here — composing the inside of
`sections/blocks/<kind>.server.tsx` out of components that already exist. The kind then lives in the
six places `use-sections` names, and its interactive part lives in an island under `components/`.

**Entry two — a WIDGET.** A widget belongs to ONE route and is allowed an arbitrary look, so foreign
design knowledge has the widest room here — `_widgets/{static|dynamic}/<name>/`. Read the nearest
existing widget before you start (`use-widgets`); isolation forbids sharing code, it does not license
building something that looks foreign to the product.

**Deciding between them is not this skill's job** — the trigger table in `CLAUDE.md` decides, and
`use-sections` explains the boundary. In one line: **reuse decides.** A kind must fit any page of the
project; a widget need fit nobody but its route.

## 3. Four places where the foreign skill is overruled — and why

| It says | Here | Why |
|---|---|---|
| compose `Dialog` + `DialogTitle` yourself | **`AppDialog` only** — `components/dialog/app-dialog.client.tsx` | one owner per genus of thing. A bare `DialogContent` has no height limit and no scrolling body, and a long form grows past the bottom of the screen together with its submit button. `check:dialogs` refuses a direct import; the visible standard is `/{lang}/architect/design?section=dialogs` |
| toast from `toast` for Base UI projects | **`sonner`** | this project carries both base libraries at once, and its toaster is mounted once. A second toast system means two toasters and doubled messages |
| components go wherever you compose them | **nothing under `sections/` is a client component** | the section layer is server-only, whole; interactivity is the island it mounts. `check:static` refuses it |
| semantic colours (`bg-primary`) | same rule, one step further: **the token is the only colour** | the owner repaints his whole project from the design panel. A literal colour does not break — it silently leaves that system. `check:contrast` measures it |

Everywhere else, follow it as written: `cn()`, `gap-*` over `space-*`, `size-*`, `Field`/`FieldGroup`
for forms, `Empty`, `Skeleton`, `Separator`, icons via `data-icon`.

## 4. Adding a component is ordinary work; changing the base is not

`npx shadcn@latest add <component>` into `components/ui/` is a normal act — but check the folder
first: a genus that already has an owner keeps it, and a second implementation of the same thing is a
fork of the product's look (`use-primitives`).

**Changing the base library, migrating Radix to Base UI, swapping the icon set — the owner's
decision, not yours.** The migration skill that ships in the same repository was deliberately not
installed; `SOURCE.md` says how to bring it back if he ever asks for it.

**Never hand-edit anything under `.claude/skills/shadcn/`.** It is foreign, vendored, and the next
`npx skills update` overwrites it silently. What we have to say lives here.
