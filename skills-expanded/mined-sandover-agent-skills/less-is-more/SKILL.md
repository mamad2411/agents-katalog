---
name: less-is-more
description: Keep front-end work spare, clear, and purposeful. Use whenever designing, building, revising, or reviewing interfaces, including websites, app screens, dashboards, charts and data pages, wireframes, interactions, and UI copy.
---

# Less is more

Adapted from Jakub Krehel's
[Less is more, more or less](https://jakub.kr/writing/less-is-more).

Agents make adding things cheap, so most pages fail by carrying too much.
Simplicity comes from understanding: once you know who uses the page, what
they came to do, and how often they do it, most removals become obvious. A
menu opened two hundred times a day should open instantly; an animation there
costs its user hours a year. Before you add an element, a line of copy, an
animation, or a dependency, ask whether it makes the outcome better for that
person. Keep the features, style, and scope the user asked for.

## Cut

- Open with the content. Remove layers that stand between the reader and it,
  such as eyebrows, intro paragraphs, and summary blocks.
- Drop structure that organizes nothing: a header over a single item, a border
  that separates nothing.
- Delete copy that says what the page already shows.
- Leave off details this reader won't use, including how the page or system
  was built.
- Put each detail next to what it describes, and let fuller detail wait behind
  a hover or a click.

## Write copy for the person

Read each label and sentence as the person in that situation, who knows only
what the screen has shown them so far. Write friendly, plain words, and stop
when the person has what they need to act.

There are two kinds of state to reason about, and you must reason about both:
the state of the website or UI system, and the state of mind of the user, and
what they know and expect at each step. Use that reasoning, but keep the
reasoning, and any test or preview controls, off the client-facing page.

## Keep it legible

Spare pages still need clear structure. Make different kinds of things look
different, so an overlay, a control, and the content around them never blend.
Match the page's existing type, color, and spacing, so new elements belong.
Reuse familiar patterns and keep the main path obvious. Use motion only to
show a change or give feedback.

When a design falls flat, rethink the form before decorating it. For charts,
follow Tufte: label data directly, and drop marks that carry no information.

## Build small

Choose the smallest readable implementation that does the job. Prefer what the
platform and the existing code already provide to new fonts, frameworks, and
dependencies.

## Check the result

Look at the rendered page and click through the paths people will take. Check
that the copy matches what the page does. Then read the page once more, asking
of each element what the person would lose without it, and remove what fails.
Say what you didn't check before calling the work ready to share.
