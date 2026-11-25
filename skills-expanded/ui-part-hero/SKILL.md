---
name: ui-part-hero
description: "The first screen (the hero): its job (what it is, for whom, the one action, the proof in view), the claim in about twelve words or fewer with the competitor test, the supporting line, the primary and secondary actions, the visual (the real product, a real photo, a demo, or nothing), proof beside the claim, compositions (claim beside proof, statement over the work, index first, product in use, centred statement, full-bleed image with a legible overlay), type and height, the hero image as the LCP, the phone layout, and the variants for launch pages, products, local businesses and portfolios. Read before building or reworking one."
---

# Hero

The first screen is where a generated page gives itself away: a name or a
slogan, a line of grey text, one button that scrolls down, and empty space
where the proof should be. The reader decides in that screen whether to go
on, so it carries the most specific thing you have, not the most general.
One part of an interface: the principles (direction, spacing, type,
colour, icons, states, accessibility) are in the `ui` skill, the measures
in `ui-layout`, the page around it in its `ui-page-*` skill.

## 1. The job of the first screen

In view without scrolling, on a 1440 by 900 laptop and on a 360px phone:
what it is (the claim, as the page's one `h1`), for whom (in the claim or
the line under it), the one action when the reader takes one here, and the
proof: the work, the product, or a fact the reader can check. The rest of
the story goes below; the hero does not summarise the page. An application
screen has no hero: a signed-in home starts with its page header
(`ui-part-page-header`).

## 2. Decide before building

1. **The claim.** One sentence only this product or person can say. Test it:
   put a competitor's name in it. If it still holds, it is not specific yet.
   "Handmade furniture from reclaimed wood" fits a thousand workshops;
   "Tables and benches from the teak of Jepara's demolished houses, made to
   order in six weeks" fits one. Write it from the facts you found about this
   subject (its readme, its work, its own words), never from invented ones,
   and never from an example in these skills. Keep it to twelve words or
   fewer: a list of everything the person makes is the supporting line's
   job, not the headline's.
2. **The proof.** What makes the claim believable, in the same screen: the
   work itself (a real screenshot, a real photograph, the first two or three
   projects), a real command and its real output, a real quote with a name.
   A claim whose proof is one scroll away reads as a claim.
3. **The next step,** only if there is one the reader takes here: book,
   install, download, email. "See my work" or "Learn more" is not a next step
   when the work is right below; leave the button out.

## 3. The words

- The headline states the benefit or the fact, not a slogan: nothing that
  fits any product, no question ("Tired of spreadsheets?"), no pun that
  needs the picture (`writing`).
- A turn is allowed: the claim, then its consequence in the muted colour or
  an italic, both within the twelve words, as one `h1` with a `span`
  inside, not two headings.
- The supporting line: one or two sentences naming the audience and backing
  the claim with a detail (how it works, what it replaces, a number with
  its source). Not a second slogan, not a list of every feature.
- One filled button that says what happens: "Download for macOS", "Book a
  20-minute call", "Join the waitlist". The second action is a text link to
  the proof or the price, never a second filled button; not "Get started",
  "Learn more", "Explore" or "Discover" (`ui_check` flags them). A line
  under it only when true and useful ("Free for personal use. No account
  needed."). A command-line tool's action can be its real install command,
  with a Copy button.

## 4. The visual

Choose by what exists, in this order:

- **The real product**: a screenshot cropped to the part the claim is
  about, readable at the size shown, in the page's theme (`ui-part-images`).
- **The product moving**: a scripted demo of the real interface, one per
  page (`motion-demo`), or a recorded screen loop of 6 to 15s, muted, with
  a poster and a pause control.
- **The real output**: a command and its real output for a command-line
  tool; the report, document or photograph the product makes.
- **A real photograph** the user gave: the place, the people, the work.
- **Nothing**: the claim and its line alone, large and set left. A true
  blank beats a false picture.

Never a stock image, a generated face, people smiling at laptops, a fake
terminal for a product that is not a command-line tool, a dashboard of
invented numbers, a phone mockup with invented messages, or 3D blobs.

## 5. Proof beside the claim

- In the first screen, beside or directly under the claim it supports: the
  work itself; one real number with its source and date ("as of May 2026")
  that backs this claim; a quote with a full name and role; logos of
  customers who agreed, under "Clients include" (`ui-part-social-proof`).
- Not a row of counts, not logos nobody agreed to, not a rating without its
  source. With none of these, the product is the proof: show it.

## 6. Compositions

Choose by what the proof is. Do not reach for the first one by habit.

- **Claim and proof side by side** (wide screens): the claim, one line of
  support and the action in 6 or 7 of 12 columns; the proof (a screenshot, a
  photograph, the first projects as a short list) in 5 or 6, aligned to the
  top of the headline, not floating in the middle. On a phone: the claim,
  then the proof.
- **Statement over the work**: the claim large across 9 or 10 columns, set
  left, and the work beginning immediately under it, inside the first
  screen. The hero is the top of the content, not a banner above it.
- **Index first** (a portfolio of many small tools, documentation, a
  changelog): the name and one line as a compact block, then the list of
  work starts at once and is itself the focal point.
- **Product in use** (software): the interface or its real output large, the
  claim beside or above it in one or two lines.
- **Centred statement**: a short claim (two lines at most) with one line and
  one action under it and nothing beside it: a launch with nothing to show
  yet, an event. Never a centred paragraph (`ui-layout` section 7).
- **Full-bleed image with a legible overlay**, when a real photograph is
  the proof (a place, a room, a landscape): the words over its calm part,
  on a scrim (about 60% black fading to transparent) or a solid panel, at
  4.5:1 against the lightest pixels behind them (3:1 from 24px). A 4:5 crop
  for phones keeps the subject out from under the words (`ui-part-images`);
  the header over it follows `ui-part-header` section 4.

## 7. Type, space and height

- The claim is the largest type on the page: 39 to 61px on wide screens
  with `clamp()`, 31 to 39px on phones, line height 1.05 to 1.15, at most
  about 20 words a line. Set it in the display face the direction chose,
  with `text-wrap: balance` so its lines come out even at every width.
- The supporting line is body size or one step up, in the text colour or
  slightly muted, never faded to a grey that fails contrast; at most about
  60 characters a line, 16 to 24px under the headline, the action 24 to
  32px under it.
- On a laptop (1440 by 900) the first screen shows the start of the content
  below the hero. The hero is as tall as its content, usually 320 to 560px;
  never `100vh` (`ui_check` flags `height: 100vh` and `h-screen`).
- A full-bleed photograph may take more of the screen, never all of it: up
  to `min-height: 85svh`, so the next section's edge shows. `svh` holds
  still while a phone's toolbar slides away; `dvh` resizes with it.

## 8. The first screen's speed

- The claim is text in the served HTML, never an image or drawn by script.
- The hero image is usually the LCP element: an `<img>` in the HTML (not a
  CSS background), AVIF or WebP through `srcset` and `sizes`, width and
  height set, `fetchpriority="high"`, never `loading="lazy"`, under about
  200 KB (`priority` in `next/image`, `preload` from Next.js 16). What sits
  below the first screen is lazy.
- With a text-only hero the headline is the LCP element: preload its one
  `woff2`, with `font-display: swap` and fallback metrics (`size-adjust`),
  so it shows at once and does not jump when the font arrives.
- LCP under 2.5s and CLS under 0.1 on a mid-range phone
  (`frontend-performance`). A demo, video or canvas starts after the first
  paint; a video is muted, `playsinline`, has a poster, and does not
  autoplay under reduced motion.

## 9. On a phone

- The headline first, at 31 to 39px, then the supporting line and the
  action, all in the first screen at 360px wide; the visual after the text,
  or smaller: a crop of the part that matters, not a whole screenshot
  shrunk to a blur.
- A split stacks (claim, then proof); a full-bleed image takes its 4:5
  crop; a demo keeps its story and drops its side panels (`motion-demo`).
- A sign-up field and its button stack, the button full width below about
  480px; other buttons keep their width.

## 10. Variants

| Page | The first screen holds | Read |
|---|---|---|
| Launch or waitlist | the claim, the sign-up as one control (email joined to "Join the waitlist"), what the address is for, real output beside | `ui-reference-launch`, `ui-page-landing` section 9 |
| Product or SaaS | the claim, the product in use or its demo, one action and a link to the proof | `ui-reference-saas`, `motion-demo` |
| Local business | what and where as the `h1`, open now, Book, Call, WhatsApp, Directions, the address, today's hours, a photo of the place | `ui-page-local-business` section 2 |
| Portfolio | what the person makes, and the work starting in the same screen | `ui-page-portfolio` |
| Studio | a two-line claim, a paragraph, the first project entry beginning | `ui-reference-studio` |

## 11. Names and people

- A person's name belongs in the header, or as a byline under the claim. It
  is rarely the best headline: it says nothing about the work.
- A portrait only when a real photo is given, and then with some size (160
  to 320px) as part of the composition. A 64px avatar in a rounded square
  beside a name is decoration.
- No full stop, underscore, bracket or blinking cursor after a name used as a
  logo or a headline ("Enow Dev.", "enowdev_"): it is the default flourish,
  not an identity.

## 12. Accessibility, themes and motion

- One `h1`, the claim; the supporting line a `p`; the action a link when it
  goes somewhere, a button when it acts (`ui-part-buttons` section 5). Alt
  text says what the image shows; a demo carries `role="img"` and a label
  telling its loop in one sentence.
- Themes: the muted half of the claim and the supporting line at 4.5:1 in
  both; screenshots in the matching theme, or framed (`ui-themes`). Motion:
  the first screen never waits for a scroll or a script, one short entrance
  on load or simply there (`motion-reveal`); no typewriter, no parallax on
  the headline; under reduced motion, the final state.

## Check it

- `preview` at 360, 768 and 1440px: "the headline has N words: a headline
  says one thing, in about twelve or fewer (ui-part-hero)" when the page's
  first `h1` runs past 14 words; "N h1 elements; a page has one". The
  1440px screenshot shows the next section's edge, the 360px one the claim
  and the action. Text over a photograph is measured against the nearest
  background colour, not the picture: check it against the image yourself.
- Put a competitor's name in the claim: if it still holds, rewrite it.
- `ui_check`: `100vh` and `h-screen`, gradient text, default gradients,
  generic actions, buzzwords, invented figures, emoji.
- Lighthouse on mobile: the LCP element is the hero image or the headline,
  under 2.5s, CLS under 0.1. With JavaScript off, the claim, the action and
  the image are all there.

## Avoid

- "Hi, I'm X" with a waving hand, "Welcome to…", "Unlock the power of…", a job
  title as the headline ("Full-stack developer").
- A single button whose only job is to scroll to the next section.
- Half of the first screen empty on a wide window.
- A row of numbers under the claim (followers, stars, years): the work
  proves more than its counts.
- Gradient text, blobs and 3D shapes, a floating "New" pill, a "trusted by"
  logo row, a fake terminal window, a typewriter effect, a pulsing
  "available for work" dot.
- A `100vh` hero with a scroll-down arrow, a carousel, a stock photo, two
  filled buttons, a video with sound, a pop-up on arrival.
