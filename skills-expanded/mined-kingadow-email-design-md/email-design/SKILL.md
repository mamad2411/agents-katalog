---
name: email-design
description: >
  Designs marketing emails in Figma from a brief, using the brand's EMAIL.md and its Figma
  components. The deliverable is a finished, on-brand 600 px email frame (plus a 375 px mobile
  frame when the brand has mobile variants), built so it translates cleanly into an email
  platform such as Klaviyo, with the inbox preview, status box and brief panel around it. Use
  whenever the task is to design, lay out or build an email, a flow email or a campaign in
  Figma. Not for building the email inside the email platform.
---

# Email design

**Role: designer.** The deliverable is a finished Figma frame that looks on-brand and is built
so the email platform can translate it cleanly. Strategy, audience, send timing and the build
inside the email platform are someone else's job.

## Before you start

1. **Read the brand's `EMAIL.md`, all of it.** That's the brand's filled-in copy, not the blank
   template at the root of this repo. Its header names the Figma file and pages it belongs to. It
   is the source of truth for colors, type, components, layout, photography and voice. If the
   brand has no `EMAIL.md`, stop and say so.
2. **Load `figma-use`** before any `use_figma` call. It owns the Figma API rules. This skill owns
   the design intent.
3. **Get the brief.** You need the copy (or what the copy must say), subject and preview text,
   links and button labels. If the copy, prices or links are missing, ask. Never invent a
   price, a claim or a product fact. If the brief needs a fact `EMAIL.md` doesn't have (how to
   brew it, how long it lasts) and you can't ask, write the most careful version you can and put
   it first in the brief panel's checklist, marked "to confirm".
4. **Read `corrections.md`**, which sits next to the brand's `EMAIL.md`, if there is one. Those
   rules come from past misses.

## Build

**Clone and swap, never hand-build.** Assemble the email from the brand's components:
- the top bar, header and footer
- section components: hero, text block, image and text, callout, steps, review
- product blocks

Change copy through component properties. Never detach an instance. If no component fits, build
the section as a one-off with the brand's styles and variables, and promote it to a component
once it has been used three times.

**Swap photos on the image layer.** Section components hold their photo as an image fill on a
layer named for it (usually `Image`). Pick the photo from the photo library in `EMAIL.md`, set it
as that layer's fill with the scale mode on Fill, and check the crop at 1:1. Read what the photo
shows before you use it: the right product, a legible label, and nothing printed on it (a
harvest month, a season, a date) that contradicts the send date.

**Shared backgrounds.** `EMAIL.md` says which sections carry their own background. When two
sections next to each other share one, set the second instance's top padding to 0.

**Place the email like this:**

| Where | What |
|---|---|
| Top | Status box |
| Under it | Inbox preview: sender, send date or time as the inbox shows it, subject A, preview A |
| Under it | A small label: "Desktop · 600" |
| The email | 600 px wide |
| 60 px to the right of the desktop email | Mobile version (375 px), top-aligned, with its own "Mobile · 375" label |
| 60 px to the right of the mobile version | Brief panel |

Keep the status box, inbox preview and label in one column above the email, left-aligned with
it. The subject and preview sit above the email, never inside it.

- **Status box:** clone one from an existing email. Figma's Status widget can only be cloned,
  and its state is set by hand in Figma. A new design starts at the first state.
- **Brief panel:** clone the panel of the most recent email in the file and replace its content.
  If there is none, build a 320 px white card with the fields listed under Finish, in that
  order.

**Never delete existing frames** without the brand owner's say-so. Put new ones to the right of
existing work.

## What makes a frame build-ready

A frame that looks right but is built wrong becomes a broken email.

**Structure**
- Exactly 600 px wide. Auto-layout on every container.
- One column that stacks top to bottom. No overlapping layers, no absolute positioning.
- Every layer named for what it is.

**Text**
- Live, editable text, never outlined.
- Every text box grows with its text. Fixed-size text boxes clip when the fallback font is wider.
- Text styles for every layer, with line height and letter spacing set. Logo wordmarks are
  artwork and are exempt.
- No rotated text.

**Color**
- Every fill bound to a color variable, except logo artwork. No opacity tricks: use a real
  lighter color.
- Buttons are a filled shape behind the label.

**Spacing**
- Padding and gaps set in auto-layout. No empty spacer frames.
- Columns add up to the content width.

**Images**
- Placed at final display size. No text on images: headlines go in live text.
- No effects that can't flatten (shadows, blurs, blend modes).

## Rules that keep coming up

These were learned from blind reviews. They apply to any brand.

- **Each color keeps its role.** Follow `EMAIL.md` exactly, especially which color is for
  buttons, links and prices. An accent used everywhere stops meaning anything.
- **Check every text pairing.** Text on a colored band can fail contrast even when it passes on
  the page background.
- **One section rhythm.** Use the same padding everywhere. When two sections next to each other
  share a background, the second drops its top padding.
- **Buttons breathe.** Leave room between the copy and the button (28 px is a good default).
  Use one width for every standalone button.
- **Columns end level.** Columns in one row end on the same number of lines. Rewrite copy until
  they do.
- **No orphans.** No single word alone on the last line.
- **Line breaks and quotes.** No hard line breaks: split text into separate layers. Use curly
  apostrophes.
- **Mockups show real content.** Merge tags and template code go in layer names and the brief,
  never as visible copy.
- **Seasonal products need an off-season state** in any email that runs all year.
- **Every product photo shows its branding.** A generic jar or blank box reads as someone else's
  product.
- **A label in a photo is a claim.** A harvest month or date printed on the product has to fit
  the send date of every email the photo goes into.
- **Prices and claims match the store,** for every product an email mentions.

## Finish

1. Screenshot the frame at 1:1 and look at every section: clipping, overlaps, orphans, uneven
   columns, placeholder copy.
2. Fill the brief panel:
   - send or trigger, sender (from `EMAIL.md`), audience
   - subject and preview variants (the same number of each)
   - tone, conditional blocks, products, live stock
   - the pre-send checklist and links
3. Run `email-design-review` as a separate, blind agent before anyone builds the email.

## Composes with

- **`figma-use`**: the Figma API rules. Load it before every `use_figma` call.
- **The brand's `EMAIL.md`**: tokens, components, rules.
- **`email-design-review`**: the blind critic that runs next.
