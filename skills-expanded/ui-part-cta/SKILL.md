---
name: ui-part-cta
description: "A closing call-to-action band: when a page needs one, repeating the hero's verb and destination, the heading, one line of context and only true reassurance, the band's surface and measures, an email form inside it, phones and themes. Read before ending a page with a call to action."
---

# Call to action band

The generated version: "Ready to get started?" over a purple gradient with
a glow, two equal buttons, "Join 10,000+ happy customers", a countdown
that resets on every reload, and a new slogan that appears nowhere else on
the page. A closing call to action repeats the page's one primary action
for the reader who has scrolled to the end and is ready. One part of an
interface: the principles (direction, spacing, type, colour, icons,
states, accessibility) are in the `ui` skill, the measures in `ui-layout`,
the page it closes in `ui-page-landing`.

## 1. When to use it

- For repeating the primary action at the end of a long page: a landing
  or product page, a service page, a long case study that ends in a way to
  hire.
- One per page at most, after the last section and before the footer. Not
  between every section; not on application screens, docs (they end with
  the next page to read), short pages, or a page with no primary action.
- On a personal site a closing line in the owner's voice, with the email as
  a link, often does this better (`ui-part-footer`); on a local business's
  page, the phone, the address and the booking link
  (`ui-page-local-business`).

## 2. What it says

- The same action as the hero's and the header's primary button: the same
  verb and the same destination (`ui-part-hero`, `ui-part-header`). "Book a
  first appointment"; "Start a 14-day trial" only if the trial exists and
  lasts 14 days; "Download for macOS". A different verb here reads as a
  different offer.
- A heading that says what acting gets the reader, in the page's voice.
  Not a new slogan and not a question: a fact from the page ("A first
  appointment takes 45 minutes", when it does), not "Ready to get
  started?".
- One line on why, or on what happens after the click: the next step, the
  cost, the time it takes.
- Reassurance only when true and specific: "No card needed", "Cancel any
  time", "Replies within one working day". A fact you were not given stays
  a visible placeholder ("[Reply time]") and goes in your report.
- No fake urgency: no countdowns, "only 3 spots left" or "offer ends
  tonight" unless it is true and live. No invented counts of customers or
  ratings (`ui_check` reports figures like "10,000+ users").

## 3. Anatomy and measures

- A band that stands apart from the sections above: a full-bleed surface
  one step from the page (`--surface-2`), or the page's accent area with
  `--on-accent` text. The content stays in the page's container.
- Vertical padding 64 to 96px on wide screens, 48 to 64px on phones; the
  content at most 640 to 720px wide.
- The heading at the page's section size (25 to 39px); the line at body
  size, under 60 characters a line; 12 to 16px between them, 24 to 32px
  down to the button.
- One button, the primary, large (44 to 48px). At most a secondary text
  link beside or under it ("Or email [address]", "See pricing"), never a
  second filled button.
- On an accent band the button inverts (the surface colour with accent
  text), so it stays the strongest thing in the band and keeps 3:1
  against it.
- Centred text is allowed here: it is a short standalone line (`ui-layout`
  7). Or a split: the words at the left, the button at the right, on the
  content's edges.
- No gradient, glow, blobs, grid pattern, stock photograph of a handshake,
  or illustration that only fills space.

## 4. An email form in the band

- Only when the action is leaving an email (a waitlist, a newsletter that
  exists): one field and one button on one line, a label (visible, or
  visually hidden when the heading names the field's purpose),
  `type="email"`, `autocomplete="email"`.
- It sends somewhere real, says what will arrive and how often, links the
  privacy notice, and replaces itself with the result ("Check your inbox
  to confirm") without a reload. A form that sends nothing is removed.
- Errors under the field, in words (`ui-part-forms`, `frontend-forms`).

## 5. Phones, themes, motion

- One column: heading, line, button. The button may go full width below
  about 480px; its target 48px.
- Clear of the back-to-top control and of any bar fixed to the bottom
  (`ui-part-back-to-top`).
- Themes: the band's surface and text have a value per theme; on an accent
  band, `--on-accent` at 4.5:1 and the inverted button at 3:1 in both
  (`ui-themes`).
- Motion: none, or the page's own section entrance (`motion-reveal`). No
  pulsing button, no shine sweeping across it (`motion-interface`).

## 6. A sketch

```html
<section class="cta" aria-labelledby="cta-title">
  <div class="cta__inner">
    <h2 id="cta-title">[What acting gets the reader, in the page's voice]</h2>
    <p>[What happens after the click, and what it costs]</p>
    <a class="btn btn--primary btn--large" href="/book">Book a first appointment</a>
    <p class="cta__note">[Real reassurance, or remove this line]</p>
  </div>
</section>
```

```css
.cta { background: var(--surface-2); padding-block: clamp(48px, 8vw, 96px); }
.cta__inner {
  display: grid; justify-items: center; gap: 16px; text-align: center;
  max-inline-size: 42rem; margin-inline: auto; padding-inline: 16px;
}
.cta__inner .btn { margin-block-start: 8px; }
.cta__note { font-size: 14px; color: var(--text-muted); }
@media (max-width: 480px) { .cta__inner .btn { justify-self: stretch; } }
```

The button is a link: it goes to the booking page (`ui-part-buttons`).

## Check it

- Compare the verb and the destination with the hero's and the header's
  primary action: the same.
- `ui_check`: generic actions ("Get started", "Learn more"), buzzwords,
  invented figures, default gradients and glow in the band.
- `preview`: the band's text at 4.5:1 and the button at 3:1 in both themes,
  the button 44px or more at 360px, its link not in "links to nowhere",
  nothing under the back-to-top control.
- Every claim in the band traced to a fact you were given; the rest are
  visible placeholders listed in the report.

## Avoid

More than one per page; a new slogan in it; "Ready to get started?";
"Join thousands of…" with no count behind it; countdowns and scarcity that
are not true; two equal buttons; a gradient band with a glow; a verb that
differs from the hero's; a newsletter form with no newsletter; a band on an
application screen.
