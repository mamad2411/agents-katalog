---
name: ui-part-sections
description: "The main content between the hero and the footer: each section's point as its heading, a catalogue of compositions and when each fits (split, label and content, stacked, list, uneven grid, table or comparison, statement, full-bleed band, steps, timeline, before and after, FAQ), evidence in every section, using the width, rhythm and spacing, the lead item given room and the rest compact (the preview repeated-blocks check), features without identical icon cards, hierarchy, items in a list, order by the story, when to stop, and phones. Read before building or reworking a page's sections."
---

# Sections: the main content

A generated page gives itself away in its main content by repeating one
section shape down the page: a label heading ("Selected work", "About",
"Contact"), a line of grey text explaining the section, then a list or a
grid of equal items between hairlines, in one narrow column inside a wide
container. Decide each section on its own. One part of an interface: the
principles (direction, spacing, type, colour, icons, states,
accessibility) are in the `ui` skill, the measures in `ui-layout`, the
page's skeleton in its `ui-page-*` skill.

## 1. For each section, decide

1. **Its point, as a sentence.** The heading says the point ("Tools that run
   on your own machine", "Booking takes two messages"), not the category
   ("Projects", "How it works"). A category heading is right only for a
   section people look for by name: Contact, Pricing, FAQ.
2. **The shape of its content,** which sets the composition:
   - items the reader compares (projects, plans, releases): a list or a
     table with aligned columns;
   - one item that matters most: a feature, larger, with its evidence;
   - an argument or a story: prose at 60 to 70 characters a line, with an
     image or a quote beside it;
   - steps: numbered, only when there really are steps.
3. **Its evidence:** a real screenshot, a real command or code example, a
   real number with its source, a quote with a name. A section with no
   evidence is usually two sentences that belong in another section.

## 2. Compositions, and when each fits

Pick per section by what it holds (`ui-layout` section 7); the same one
twice in a row needs a reason.

| Composition | Fits | How |
|---|---|---|
| Split | one idea and its evidence: text beside a screenshot, a photograph, a quote | text 6 to 7 of 12 columns, media 5 to 6, aligned to the top of the heading |
| Label and content | named items with a paragraph each: services, a CV, a studio's entries | a label column of 3 or 4 (the name, its meta) beside 8 or 9 of content |
| Stacked | an argument that ends in something wide: a large screenshot, a table, a diagram | heading, text at 65ch, then the full-width piece |
| List | many parallel items read by name: projects, releases, talks | rows of a name, one line and a link, hairlines or 16 to 24px between |
| Uneven grid | several items where one matters most | the lead across 7 or 8 columns or two rows, the rest small beside it |
| Table or comparison | items that share attributes: plans, specs, the old way and the new | real columns (`ui-part-tables`, `ui-part-pricing`); old and new row by row |
| Statement | one sentence that changes the pace: a principle, a promise, one quote | 31 to 49px, up to about 60% of the width, 96px or more of space around; once |
| Full-bleed band | a change of pace: a photograph, a dark band for the proof | the background across the window, the content in the container; once or twice |
| Steps | a process with a real order | as many steps as there are, numbered, each with its real screen or result |
| Timeline | dated events: a history, a release record, a project's phases | the dates in a narrow column, each event beside; real dates only |
| Before and after | a change people can see: a room, a cleaned dataset, a redesigned screen | the same crop and scale side by side, labelled; a slider only with a keyboard handle |
| FAQ | the questions people really ask | `details` and `summary`, answers of two to four sentences (`ui-part-faq`) |

Headings and text are left-aligned; centre only a short line that stands
alone (a statement, a closing action).

## 3. Use the width

- One column of text in a 1200px container leaves half of a wide screen
  empty, and reads as unfinished. Either use the grid, or narrow the page.
- Using the grid: a label column (3 or 4 of 12) holding the section's
  heading, or each item's name and its meta, beside a content column (8 or 9
  of 12) holding the description or the prose; or the content beside its
  evidence (6 and 6, 7 and 5).
- Narrowing the page: when it is mostly text, set the whole page on a 720
  to 880px container, so the measure is right and nothing looks missing.

## 4. Rhythm and spacing

- Vary the compositions: a feature, then a list, then prose beside a quote.
  The same heading, subtitle and list three times over is a template.
  Alternate text-led and image-led, contained and full-bleed, dense and
  open.
- Space between sections 96 to 128px on wide screens, 64 to 80px on phones,
  on a page that breathes (a landing page, a portfolio); 64 to 96px and 48
  to 64px on a denser one (docs, a shop). Within a section, less: 8 to 12px
  from a heading to its sentence, 16 to 24px between groups, a heading
  always closer to what follows than to what came before.
- A change of background can mark one section that changes pace, once or
  twice on a page, not every other section.

## 5. The lead item, and the rest compact

- Vary the density: only the lead items (one to three) get the full
  treatment, their description, their evidence (a screenshot when there is
  one) and their details; the rest are compact rows of a name, one sentence
  and a link. Four or more tall blocks built the same way, one after
  another, is a template, and `preview` reports it.
- What `preview` counts: four or more blocks in a row under one parent,
  each taller than 120px and wider than 40% of the screen, built the same
  way (the same tag, classes and child elements). It says "the same block
  repeated down the page (article.project ×7): give the lead one more room
  and its evidence, and set the rest as compact rows (ui-part-sections)".
  Table rows are exempt.
- It looks at every width: a grid of six cards that passes at 1440px
  stacks into six tall blocks at 360px. On a phone the rest become rows (a
  name, a line, a link), or split into groups under their own headings.
- Fix the page, not the check: renamed classes leave the same template.

## 6. Features without identical icon cards

- The one or two features that decide a purchase each get room: a split or
  a section of its own, a real piece of the interface or its output, and a
  heading that states the point ("Reminders go out on day 7, by WhatsApp").
- The rest as a list: the name, one line, a link. Six or more of equal
  weight can be a ruled grid of short facts (`ui-reference-launch`).
- Features on one screen: one real screenshot with three to five numbered
  callouts and the notes beside it.
- A product that replaces a chore: the old way and the new, row by row.
- An icon only when it speeds recognition, from the product's one set, with
  no coloured circle behind it (`ui-part-cards` section 2).

## 7. Hierarchy

- A heading outranks what it contains: a group's heading ("Agents that run
  on your machine") is larger or heavier than the names of the items in it.
  When the items' names are bigger than their group's heading, the page reads
  upside down.
- Three levels are usually enough on one page: the section, the group, the
  item. Style each level one way everywhere: sections 31 to 39px, groups 20
  to 25px, item names 16 to 20px at weight 600.
- Each section a `section` with its `h2`, groups `h3`, in order, never
  chosen for their size; an `id` on each section for the navigation's
  anchors (`#work`, `#pricing`), landing below the sticky header
  (`ui-part-header`).

## 8. Items in a list

- Each item says what it is for someone who has never seen it, in one or two
  plain sentences written for this page, with one concrete detail: what it
  replaces, how it works, who uses it. A one-line description copied from a
  repository ("Agentic Coding Tools") says nothing.
- Metadata only when it helps a decision: the language for developers, a
  date when recency matters, a count only when it is large enough to impress
  a stranger (hundreds, not dozens). Not a meta line under every item by
  habit.
- The item's name is the link, and says where it goes: the repository, the
  live site, a write-up. A "Read more" line repeated under every item is
  noise.
- Items set as splits (text beside an image) alternate sides only when every
  item has its image. An item without one becomes a text row (label column
  and content column); a split with an empty half reads as a missing image.
- A command example fits its column: short lines, a comment on its own line
  rather than aligned at the end, nothing clipped at the edge on a phone.

## 9. Order by the story, and when to stop

- The order follows the reader's doubts, not a template: what it is, whether
  it is for them, how it works, whether to believe it, what it costs, what
  to do now (`ui-page-landing` section 1). A portfolio: the work, then who
  made it, then how to reach them.
- The strongest material early: a reader who stops after two sections, or
  reads only the headings, still gets the argument (`writing`).
- Proof sits beside the claim it supports, not in a testimonials section of
  its own at the end (`ui-part-social-proof`).
- Stop when the reader's questions are answered. Cut or merge a section
  with no evidence, one that repeats an earlier point, one whose heading
  fits any product, and one that exists because the template had a slot
  (testimonials, FAQ, a call-to-action band) with nothing real in it.
  Three sections are enough when each carries real content.
- One closing action at the end (`ui-part-cta`), not a band after every
  section.

## 10. On a phone

- One column in reading order: a label column goes above its content; a
  split stacks, text first and its evidence after; splits stop alternating.
- Headings one step smaller; sections 64 to 80px apart (48 to 64px on a
  dense page).
- Tables become one card per record or scroll in their container
  (`ui-part-tables`); a comparison becomes stacked pairs; a timeline keeps
  each date above its event.
- Code blocks and wide images scroll inside their own box; nothing passes
  the edge at 360px.

## 11. Themes and motion

A band's surface and text have a value per theme, so a dark band on the
light page is still a step on the dark one (`ui-themes`). Sections are
simply there, or arrive where the arrival says something, never the same
fade-up on every block (`motion-reveal`).

## Check it

- `preview` at 360, 768 and 1440px: the repeated-block report above, at
  every width; overflow at 360px from code and tables; "links to nowhere"
  for anchors whose section does not exist.
- The 1440px screenshot: no section with its right half empty, the
  compositions differ from section to section, a change of background once
  or twice at most.
- Read only the headings, in order: the argument holds. Put a competitor's
  name in each: every heading that still holds is rewritten.
- Every section shows its evidence; each placeholder is listed in the
  report. `ui_check`: invented figures, generic feature icons, wide
  uppercase labels.

## Avoid

- A subtitle under each heading that explains the section ("Six of my
  repositories, ordered by stars.").
- An uppercase eyebrow or a section number ("01 /") over every heading.
- Every section a centred heading above a grid of equal cards; a bento grid
  of unrelated things; skill bars, percentages and language-count tables; a
  wall of technology logos.
- Counts as content: followers, stars, repositories and years in a row.
- A narrow column of text in a wide container, with the right half empty.
- Sections kept because the template has them; a call-to-action band after
  every section; zig-zag splits with an empty half; a timeline made of
  repository creation dates.
