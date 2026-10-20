---
name: ui-ux-engineering
description: Designs the rendered experience before it is coded: reads the existing design system, sets hierarchy, spacing, typography, colour, states, motion, responsive behaviour and accessibility targets, and evaluates generated or third party UI instead of pasting it. Use for any visual or interaction work.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core, project-exploration]
  outputs: [design-decisions, state-inventory, accessibility-targets, motion-spec]
---

# UI/UX Engineering

Decides what the interface should be before anything is built. Works as a
senior product designer who also writes the code, which means every decision
is expressed in terms the implementation can use.

The output is not a mood. It is a specification: hierarchy, spacing values,
states, breakpoints, contrast targets, motion parameters.

## 1. Read the system first

Before any visual decision, extract from the repository:

```
Tokens        spacing scale, type scale, colour palette, radii, shadows,
              breakpoints, z-index layers, motion durations and easings
Components    what already exists, read, not guessed from names
Patterns      how forms, tables, dialogs, empty states and errors are already
              presented
Density       compact or roomy, taken from existing screens
Voice         how existing copy speaks: terse, formal, warm
Themes        light, dark, or both, and how they are switched
```

A new screen that uses different spacing values from the rest of the product
is a defect, whatever it looks like in isolation. Consistency is the design.

When the project has no design system, say so, and derive a minimal one from
the two or three most representative existing screens rather than importing an
external aesthetic.

## 2. Hierarchy

Every screen answers three questions before it is laid out:

```
1 What is this screen for, in one sentence
2 What is the single primary action
3 What can the user safely ignore
```

Then the layout expresses that ranking through size, weight, position,
contrast and space. Three competing primary buttons mean the ranking was never
decided.

Rules that follow:

- one primary action per view, visually unambiguous;
- destructive actions are visually distinct and never adjacent to the primary
  action;
- secondary actions recede without becoming invisible;
- the most important information is readable without interaction.

## 3. Spacing and rhythm

- Use the project's spacing scale. Never an arbitrary pixel value.
- Space communicates grouping: related elements closer, unrelated further.
  Inconsistent spacing is read as disorganisation even when nobody can name
  why.
- Vertical rhythm is consistent down the page.
- Alignment: elements share edges. Optical alignment beats mathematical
  alignment when they disagree.
- Line length for body text stays readable, roughly forty five to seventy five
  characters.

## 4. Typography

- Use the project's type scale. Two or three sizes on a screen, not six.
- Weight and size carry hierarchy; colour carries emphasis; neither carries it
  alone.
- Line height increases as size decreases for body text.
- Numbers in columns use tabular figures.
- Truncation is deliberate, with the full value available on interaction.

## 5. Colour

- Semantic, not decorative: the same colour means the same thing everywhere.
- Never the only carrier of meaning. Status uses colour plus a label or an
  icon.
- Contrast is measured against the project's target, not judged by eye. Body
  text, interactive text and interface boundaries all have targets.
- Dark mode is a separate set of decisions, not an inversion. Elevation,
  shadows and saturation all behave differently.
- Both themes are checked when the project supports both.

## 6. The state inventory

Every component that touches data specifies its states before it is built.

```
default      the normal case
hover        pointer only, never the only affordance
focus        visible, distinct, meeting contrast on both themes
active       the pressed state
disabled     and why it is disabled, communicated somewhere
loading      with the layout space reserved
empty        first use, and filtered to nothing, which are different
partial      some data present
error        what failed, whether retrying helps, and the retry control
success      confirmation that does not vanish before it is read
```

The empty state distinction matters: a new user needs an explanation and a
first action, while a user whose filter matched nothing needs to know the
filter is the cause.

## 7. Interaction

- Feedback within roughly one hundred milliseconds of any action.
- Operations over a second show progress; over ten seconds show progress plus
  the ability to leave and come back.
- Destructive actions are confirmed, and the confirmation names the object and
  the consequence, not just Are you sure.
- Undo is better than confirmation where it is possible.
- Errors are recoverable: the input is preserved and the path forward is
  stated.
- Nothing important is hidden behind hover alone, which excludes touch and
  keyboard users.

## 8. Motion

```
Purpose     explain a change, a spatial relation, or the arrival of content
Duration    150ms to 300ms for interface transitions; longer only for
            deliberate, large spatial moves
Easing      the project's tokens; entrances decelerate, exits accelerate
Property    transform and opacity, which do not force layout
Reduced     prefers-reduced-motion honoured, with the change still legible
Interrupt   the next user action interrupts the animation, never queues
```

Motion that delays interaction is removed. An animation the user waits for
twenty times a day is a tax.

## 9. Responsive

Decisions taken per breakpoint, from the project's own configuration:

```
what reflows, what stacks, what collapses behind a control
what is deliberately hidden, and why that is acceptable
how navigation changes shape
how tables behave: scroll, stack into cards, or hide secondary columns
touch target size and spacing on the narrow widths
```

Hiding content to make a layout fit is a decision that needs a reason. Usually
the reason is that the content was not important, which means it can be
demoted at every width.

## 10. Using generated or third party UI

Tools that generate interfaces, component marketplaces and design system
packages are used when the project already has them configured, or when adding
one passes `dependency-selection`.

Generated output is a draft, never a paste. Before it enters the codebase:

```
Accessibility  semantics, keyboard, focus, labels, contrast, checked by hand
Consistency    tokens replaced by the project's own
Dependencies   what it pulls in, judged by dependency-selection
Maintenance    would the team understand and change this in six months
Performance    bundle cost, render cost
Behaviour      the five data states present, not just the default
Licence        compatible with the project
```

Generated markup is routinely inaccessible in ways that are cheap to fix
before it lands and expensive afterwards. The review is not optional, and no
generated code is committed unread.

## 11. Protocol

1. Extract the design system, section 1.
2. Answer the three hierarchy questions.
3. Specify the state inventory for each new component.
4. Choose spacing, type and colour from the tokens.
5. Set the accessibility targets: contrast values, focus behaviour, keyboard
   path, announcements.
6. Specify motion, or decide there is none.
7. Specify the responsive behaviour per breakpoint.
8. Hand the specification to `frontend-engineering`.
9. Verify the built result against the specification, in a browser, at the
   real breakpoints, with the keyboard.

## 12. Auto-critique

Score from 0 to 5: fidelity to the existing system, clarity of hierarchy,
completeness of the state inventory, contrast and accessibility targets set
and met, purposeful motion, responsive decisions taken rather than inherited,
restraint in introducing new patterns.

Threshold: no axis below 3, average at least 4. A screen whose focus state is
invisible or whose contrast is below the project target fails regardless of
appearance.

## 13. Interfaces

- Upstream: `project-exploration`.
- Downstream: `frontend-engineering` implements the specification,
  `playwright-automation` verifies it in a browser,
  `performance-engineering` checks its rendering cost.
- Lateral: `dependency-selection` for any new UI library.
