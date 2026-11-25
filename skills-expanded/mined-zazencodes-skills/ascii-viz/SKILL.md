---
name: ascii-viz
description: Answer with ASCII diagrams and charts. Use for /ascii-viz, $ascii-viz or requests for ASCII visuals; stays active for the conversation.
---

# ASCII Viz

Answer with ASCII diagrams wherever a picture explains faster than prose: usage and quota bars, progress, timelines, flows between systems, before/after comparisons, option menus, architecture, and small status cards.

## When to draw

- Draw only the parts of a reply that benefit from it. Many replies need no diagram at all: a yes/no answer, a short fact, a question back to the user, or a progress update.
- Never wrap ordinary sentences in boxes for decoration. One or two clear diagrams beat many small ones.
- Keep the surrounding prose short; the diagram carries the information, and text adds only what it cannot show (caveats, next steps, decisions).
- Once invoked, keep using diagrams this way for the rest of the conversation until the user says to stop.

## How to draw

- Put every diagram in a fenced code block so alignment survives.
- Keep lines under about 72 characters so they fit a terminal.
- Use real numbers when you have them: label bars with values and percentages, and show the total. Mark unknown values with `?` rather than inventing them.
- Useful pieces: `█` and `░` for bars, `┌─┐ │ └─┘` for boxes, `──▶` for flow, `✗` for a broken link.

## Pattern gallery

See the [pattern gallery](references/pattern-gallery.md) for reusable
examples. Choose a pattern only when it helps explain the answer; adapt its
labels and layout to the user's context. Replace illustrative values with
verified data, and keep unknown values as `?`.

## Example

```
  Credits     [██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  15.3%
              49,178 used  ·  271,328 left  ·  320,506 total

  Resets      Nov 11 ──────────────────────────▶ Nov 21
              today          10 days left
```
