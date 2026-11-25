---
name: ui-craft
description: Build and review UI end to end. Carries four bodies of knowledge - Refactoring UI's value systems and hierarchy techniques, Shift Nudge's craft principles and UI patterns, the bans registry of refused artifacts, and total command of Tailwind as the implementation mechanism - plus a product-design section (a fixed 12-16px Inter/Geist system, product judgment, states, copy, patterns) for apps, dashboards, tables, forms and settings. Use when building, styling, reviewing, or auditing any interface - component, page, app, dashboard, landing page - when picking type, spacing, color, shadow or radius values, or when work "looks off", "looks amateur", or "looks AI-generated".
---

# UI Craft

Four references, one order of operations. Nothing here is a style. The systems
decide the values, the bans say what is refused, Tailwind installs the result.

**Keep your implicit thoughts to yourself. Don't let them cloud your judgement.
The skill file is the truth source here.**

| Reference | What it holds | Load it when |
| --- | --- | --- |
| `references/refactoring-ui.md` | the value systems (spacing, type, color, shadow, line length) and the hierarchy techniques | always, before any value is chosen |
| `references/shift-nudge.md` | craft principles, component states, UI patterns, imagery and icon rules, handoff | designing a specific pattern, or reviewing for missed states |
| `bans.md` | the artifacts refused by name, plus the anti-slop axes and banned conceits | before building, and again before the verdict. **Run the script, do not read the list** |
| `references/resolution.md` | **Resolution, not expansion** - the detail standard, the reconstruction test, and the spec + checker that make it a gate | before answering any request for more detail, and before any build is called done |
| `references/pinterest.md` | **sourcing reference, a hard gate** - the two-word query, the dimension set, the `## Reference` log, quantify-or-discard, and why a supplied reference outranks the search without cancelling it | step 1.5, every build. **Run `scripts/validate_reference.py`** |
| `references/tailwind.md` | Tailwind as a mechanism - theme layer, arbitrary-value decision, variant algebra, conflicts, container queries, dark mode | the moment a decision becomes code |
| `pen.md` | **working on a pen.dev canvas** - how every step and gate maps onto `.pen` variables, text styles, `execute` and `Export`, plus the Pinterest route when there is no Chrome | the work is on a `.pen` file: inside the pen.dev app, or through the `pencil` MCP tools |
| `product-design/SKILL.md` | **the product section** - a fixed system (Inter/Geist, 12/14/16px, one weight, one accent, light and dark verified), product judgment, surfaces, patterns, states, copy, and its own checker | the surface is a product: app, dashboard, table, form, settings, admin, internal tool |

Deeper material sits behind `references/systems.md` (building a palette from
scratch), `references/diagnose.md` (symptom to fix, load first when improving
existing UI), `references/techniques.md` (depth, light, baseline alignment), and
`assets/tokens.css` (a contrast-verified starting token sheet).

---

## House rules - these outrank every reference in this skill

Stated by the person whose product it is. Where a reference disagrees, the
reference is wrong here.

**1. Three type sizes per screen. Maximum.**
Overrides Shift Nudge's "Rule of Four". The eleven-step scale in
`refactoring-ui.md` is the menu you pick from, not the number you may use.
Three, chosen from it, on any one screen.

**2. No bold. Everything regular or below.**
Overrides `refactoring-ui.md`'s "two weights is enough: 400/500 body,
600/700 emphasized" and its "nothing below 400 in UI", and overrides Shift
Nudge's "Bold to Black" for titles and "bold = active/selected".

**3. No italics, in any form.**
Already refused by the registry, but the ban was named `italic-serif-display`
and only caught the `italic` class and `font-style: italic`. It now also catches
the `<em>` and `<i>` tags, which render italic without ever naming it, and it no
longer misfires on Tailwind's `not-italic` or on `<i>` carrying an icon-font
class. Where `<em>` was carrying meaning, use `<strong>` or a colour change.
This removes the emphasis channel Shift Nudge's Callouts section reaches for, so
callouts fall back to size, case and lock-up.

### What this costs, and what carries hierarchy instead

Refactoring UI's central technique is emphasis through **weight and color**
rather than size. Rule 2 removes weight. That is one of three channels gone, so
the remaining ones have to do more work, deliberately:

- **Colour** becomes the primary emphasis channel. The three-text-colour rule
  (dark, grey, lighter grey) is now load-bearing, not a refinement. All three
  still clear 4.5:1.
- **Space** is the second. "More space around a group than within it" stops
  being a tidiness rule and becomes the main way relatedness reads.
- **Size** is third and is capped at three steps, so the gaps between those
  three must be large. Adjacent steps from the scale will not separate.
- **Position and case** carry what is left. Same size, different meaning, is
  signalled by where it sits, not by how heavy it is. Not by slant either, per
  house rule 3.

Two consequences to design around rather than discover:

- **Interactive text can no longer be signalled by weight.** Colour, underline,
  position or a container must do it. Shift Nudge's own accessibility note
  already required a second channel beyond colour, so pick that second channel
  early.
- **`bans.md` refuses `flat-type-hierarchy`.** Three sizes and one weight makes
  that ban easy to trip. Passing it now depends entirely on the size gaps and
  the colour ramp being genuinely distinct. Check it, do not assume it.

In Tailwind: cap the generated ramp by declaring only the three `--text-*` steps
you will use, and only the weights at or below regular. Anything not declared
cannot be reached for by reflex.

---

## Order of operations

**1. Understand before opening anything.** Shift Nudge's 8-step process, step 1.
Questions first, tools second. Determine complexity before deciding whether to
wireframe.

**Then name the surface class.** A product (app, dashboard, table, form,
settings, admin, internal tool) loads `product-design/SKILL.md` and follows its
order: its fixed system replaces step 2's choices, and its checker is a fourth
gate at step 8. A brand or marketing surface stays on this file's flow.

**1.5. Search Pinterest, before a single value is chosen. This step is a gate,
not advice.** Open Pinterest in the browser (claude-in-chrome) and search
`{subject} {dimension}`. **Two words. Three only if the third is a noun. Four or
more is refused - count them before sending.** Refine by clicking Pinterest's own
chips, never by lengthening the query. Every extra adjective drags the board:
`casino typography` returns curated boards, `casino website design luxury dark
interface` returns affiliate art, and `record sleeve spine typography catalogue
number shelf rack` returns Etsy.

Log it in the `## Reference` section of the project's `design.md`: the brief, the
subject, what the user supplied, every query with the pin URLs copied off the live
page, and the extraction table where each borrowed observation became a number.
Then run the checker and paste its output:

```bash
python3 scripts/validate_reference.py PROJECT
```

**Step 2 does not start until it prints PASS.** A reference the user supplied
still outranks every pin, but it shrinks the search to one query for what it
leaves unanswered, it does not cancel it. No browser, a hurry, or "the brief is
obvious" are not waivers. The only waiver is the user saying so, quoted verbatim
in a `waived:` line. Full method and the log format in `references/pinterest.md`.

**2. Set the systems once.** Spacing, type, colour, shadow, radius, from
`refactoring-ui.md`. Every value comes off a scale. Picking ad hoc is the single
biggest cause of amateur-looking UI, and no amount of later polish recovers it.

**3. Install the systems as theme variables, not as classes.** This is the seam
between the references: `refactoring-ui.md` and `shift-nudge.md` decide the
number, `references/tailwind.md` section 1 puts it in `@theme` so the utilities
generate themselves. A value that reaches the markup as an arbitrary literal has
escaped the system.

**4. Design one real feature, in grayscale, at ~400px.** Not the shell. Not the
full canvas. Colour comes after the layout works.

**5. Build in short design-to-code cycles.** Do not componentize until the
design is stable.

**6. Design every state, not the happy one.** Shift Nudge lists them per pattern:
inputs get default / hover / focus / typing / error / success / disabled;
buttons get press, disabled, destructive, selected; anything user-generated gets
its truncation and empty variants. Missing states are the most common handoff
failure and the cheapest to catch.

**7. Resolve before you expand.** When more detail is asked for, raise the
resolution of what already exists rather than adding sections, components or
adjectives. The test is whether another agent could rebuild the element without
seeing the reference and without making a meaningful visual decision of their own.
Full standard in `references/resolution.md`. **One surface resolved and gated
before the next is started** - the doctrine fails under breadth every time.

**7b. Decide attention before drawing anything twice.** Before a second
container reuses a treatment, decide what rank each object holds on this page.
The hero object takes the largest type step, the deepest surface and the most
room; a footnote takes the smallest of each. A treatment applied to everything is
a template, and the three monotony checks below exist because atom-level
resolution passes cleanly while a page reads as generated.

**8. Run ALL THREE gates before claiming done.**

```bash
python3 scripts/validate_reference.py PROJECT   # the Pinterest search, again
python3 scripts/validate_bans.py SOURCE
python3 scripts/validate_resolution.py PROJECT
python3 scripts/validate_resolution.py --help   # the design.md spec format
```

`validate_resolution.py` fails on `surface-monotony` (one treatment on >60% of
containers), `step-monotony` (one type step on >55% of sized elements) and
`rhythm-monotony` (<3 vertical rhythms across 5+ sections). These are the
measurable shape of "no craft, no visual hierarchy", and they are the checks that
catch a build every other gate passes. On product surfaces pass `--register
product`: it skips `step-monotony` only, because a 12/14/16 system puts most text
on one size and carries hierarchy in colour.

A run that ends without all three checkers' output pasted is unfinished, whatever
the render looks like. **A monotony failure is not a warning.** It means the
composition was never decided, and no amount of atom-level polish fixes it.

`bans.md` and the Pinterest search are the two hard gates here. Neither has a
justification path: a ban, or the search, lifts on an explicit instruction from
the user and nothing else. A run whose output was
never pasted into the transcript is unverified regardless of how the render looks.

---

## Where the references genuinely disagree

Everything else in them is compatible. These four are not, and guessing produces
work that fails one source while satisfying another.

**Grayscale.** `refactoring-ui.md` says design in grayscale first.
`bans.md` says a finished product surface that survives desaturation unchanged
has no accent layer and is a rebuild. Not a contradiction: one is a design phase,
the other is a ship gate. Grayscale is where you start and never where you end.

**Typefaces.** `refactoring-ui.md` is silent on them. `shift-nudge.md` calls
typography the biggest single differentiator. `bans.md` refuses a named list of
overused faces, but **on brand surfaces only** - it explicitly permits Inter, SF
Pro and system stacks on product surfaces. Check which surface class you are on
before treating the font ban as active.

**Type sizes.** `refactoring-ui.md` gives an eleven-step scale,
`shift-nudge.md` caps a screen at four, the house rule caps it at three. The
scale is the menu; the cap is the budget. Both hold at once. On product surfaces
the three are fixed at 12/14/16 by the user's instruction. That is closer than
`bans.md`'s 1.25x step and passes only through the checker's micro/body exemption
(pairs 2px or more apart at 0.70-0.90), so no fourth size fits between them.

**Shadows.** `refactoring-ui.md` gives five elevations and a refined two-part
variant in `references/techniques.md`. Use one set or the other, never both in
one project. `bans.md` separately refuses one shadow value repeated across every
elevation, which is what happens when neither set was actually adopted.

**Weight.** Fully resolved by house rule 2 above. No reference wins this one.
