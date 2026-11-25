---
name: email-remix
description: >
  Takes an email someone admires (a screenshot, a forwarded email, a URL or HTML), keeps only
  its layout, and rebuilds it in the user's own brand in Figma using their EMAIL.md and
  components. Their copy, images, logos and illustrations are never carried over. Use when
  someone says "make an email like this one", "I love this layout", "remix this email for our
  brand", or shares another brand's email as inspiration.
---

# Email remix

Good emails are worth learning from. Copying them is a problem: someone else's words, photos and
brand. This skill takes the part that's fair to borrow, the structure, and rebuilds it as a new
email that only uses your brand.

## What you keep and what you leave

| Keep: the layout | Leave behind: their brand |
|---|---|
| Section order, from first screen to footer | All copy, including headlines, subject lines and button labels |
| How each section is built: one column, two columns, grid, image left or right | Photos, illustrations, icons and any artwork |
| Proportions: how tall the hero is, how much room the copy gets | Logos, brand names, product names |
| The hierarchy: what's biggest, what the eye hits first | Their colors and fonts |
| The idea behind a section, such as "three steps" or "one review, big" | Distinctive graphic devices that identify their brand |

If a layout only works because of their artwork (a custom illustration that *is* the section),
say so and propose the nearest layout your components can do.

## Steps

1. **Read your `EMAIL.md`** and load `figma-use`.
2. **Map the source email.** List its sections in order. For each, name the closest section
   component the brand already has (hero, text block, image and text, callout, steps, review,
   product grid) and note anything with no match. Note the hierarchy and proportions, not the
   content.
3. **Show the map before building.** One line per section: theirs, then yours. The user may
   want to drop or reorder sections.
4. **Write new copy** in the brand's voice from `EMAIL.md`, for the brand's own product and the
   job of this email. If there is no brief, ask what the email is for. Never translate or
   paraphrase their copy.
5. **Build with `email-design`.** Use the brand's components, colors, type, photos and rules.
   The result should look like your brand first, with the source's structure underneath.
6. **Add a short note to the brief panel**: "Layout adapted from <source>. Copy, images and
   branding are original." Keep the source screenshot out of the deliverable file.
7. **Run `email-design-review`** blind, like any other email.

## Don'ts

- Don't trace or place their screenshot inside the frame, not even as a guide layer.
- Don't keep their headline "with a few words changed".
- Don't match their colors because they "look nice". Use your tokens.
- Don't remix an email you can't name the source of. You need to know whose structure you're
  learning from.

## Composes with

- **`email-design`**: does the build.
- **`email-design-review`**: checks the result.
- **The brand's `EMAIL.md`**: the only source of colors, type, voice and photos.
