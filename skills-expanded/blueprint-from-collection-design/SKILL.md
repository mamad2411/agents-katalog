---
name: blueprint-from-collection-design
description: "Give the screens the look the user chose: MulmoTerminal's own collection screens, or a design template on the same classes."
---

# The look

The person used this collection in MulmoTerminal and knows how it looks there. Unless they chose a template, the app
should look the same. The design is the `design` answer in `.blueprint/answers.json` (missing means
`MulmoTerminal と同じ`).

1. **Tailwind and the icon font.** Add `tailwindcss`, `@tailwindcss/vite` and `material-symbols` with `yarn add -D`.
   Put `tailwindcss()` in the `plugins` of the web app's `vite.config`, and start the main stylesheet with
   `@import "tailwindcss";`. Import `material-symbols/outlined.css` once, where the app starts.
2. **The template, if one was chosen.** The usecase pack's `design/themes/<theme>.css` (`soft` for やわらかい,
   `crisp` for くっきり, `calm` for 落ち着いた) is copied into the web app unchanged and imported right after
   `@import "tailwindcss";`. It redefines the colours and corners the classes below use, so nothing else changes.
   For `MulmoTerminal と同じ` there is no template: do not redefine any colour.
3. **The screens.** Read the usecase pack's `design/mulmoterminal.md`: the classes MulmoTerminal's collection screens
   use, copied from them. Rewrite every screen the earlier steps made (list, kanban, calendar, detail, forms, sign-in,
   errors) with those classes and that structure — the same header, toolbar, table, pills, cards and record panel.
   Keep each screen's behaviour, text and tests; change markup and classes only. Write class names out in full
   (Tailwind only sees complete names); a choice between classes is a lookup table of whole strings, as the
   reference does. Remove the plain CSS the classes replace.
4. **Each collection's own icon.** `.blueprint/source/source.json` lists every copied collection's slug in
   `collections` (its `start` is the source's name, which for a shared app is the app's title, not a slug). Each
   `collections/<slug>/schema.json` may have `icon` (a Material Symbols name): show it in the icon box beside that
   collection's title, drawn as the reference draws it — MulmoTerminal does not colour that box by the collection's
   `color`, so neither does the app.
5. **`DESIGN.md`** at the app's root, for the person and for every later step: the design chosen (its answer, word
   for word), the template file if any, and the rule that new screens use `design/mulmoterminal.md`'s classes — so
   the screens later steps add look like the rest.
6. Run `yarn build` and the tests, and fix what the markup change broke without weakening a test. Keep Vite's output
   in a folder named `dist` (`dist/`, `dist/client/`, `client/dist/`): the check reads the built stylesheet there.

Done when the check passes: `yarn build` succeeds, and the stylesheet it wrote has MulmoTerminal's main button
(`.bg-indigo-600`), one class of each screen's own (the header's icon box, the table's cells, the record panel's field grid, and the
kanban's columns or the calendar's day cells when the collection has them — see `design/mulmoterminal.md`), the Material Symbols font, and the chosen design's colour and corner values (Tailwind's own for
`MulmoTerminal と同じ`, the template's otherwise); the screens use `material-symbols-outlined` and the collection's
icon; `DESIGN.md` names the design.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
