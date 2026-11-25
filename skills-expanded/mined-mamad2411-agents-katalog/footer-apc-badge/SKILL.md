---
name: footer-apc-badge
description: Add the Academy of Professional Celebrants certification badge to celebrant website footers. Use this skill whenever the user asks to add an APC badge, Academy of Professional Celebrants seal, celebrant certification badge, accreditation badge, trained and certified footer text, or to apply the footer APC badge handoff to a site. This is especially relevant for Vite, React, Tailwind, static celebrant websites, and client footer amends.
metadata:
  version: 1.0.0
---

# Footer APC Badge

Add the Academy of Professional Celebrants badge to an existing celebrant website footer without redesigning the footer.

This skill preserves the target site's footer system. The badge is a compact accreditation block, not a new feature section.

## Source Asset

This skill bundles the badge at:

```text
assets/APC-seal.png
```

Copy it into the target site's public/static images folder. For Vite or React sites, prefer:

```text
public/images/APC-seal.png
```

If the target site already has an official APC seal or Academy badge asset, use that official site asset instead. Keep the same copy, link, placement rules, and accessible alt text.

## Required Content

Use this link for the whole badge block:

```text
https://www.funeralcelebrantacademy.co.uk
```

Use this visible text exactly, unless the client has already approved different wording:

```text
Trained and certified by the Academy of Professional Celebrants
```

Use this image alt text:

```text
Academy of Professional Celebrants certified badge
```

Avoid ampersands in the visible text unless the client specifically asks for the shorter version.

## Placement Rules

1. Inspect the existing footer component or template before editing.
2. If the footer has a Service Area, Areas Covered, Locations, or similar column, place the badge underneath that content.
3. If there is no service-area column, place it where it naturally supports footer trust information, usually below the brand/about statement, near contact details, or around sitemap/get-in-touch footer content.
4. Keep the block above the very bottom copyright/legal strip where possible.
5. Do not create a new oversized footer section unless the footer layout genuinely needs it.
6. Preserve the target site's footer styling, spacing, colour palette, and responsive behaviour.

## Implementation Pattern

Adapt class names to the project. For Tailwind sites, keep the badge near `h-14 w-14`. For plain CSS, set the image to roughly `56px` square and align the text vertically with the badge.

```tsx
<a
  href="https://www.funeralcelebrantacademy.co.uk"
  target="_blank"
  rel="noopener noreferrer"
  className="inline-flex items-center gap-3 group"
>
  <img
    src="/images/APC-seal.png"
    alt="Academy of Professional Celebrants certified badge"
    className="h-14 w-14 object-contain"
  />
  <span className="text-xs leading-tight">
    Trained and certified by the Academy of Professional Celebrants
  </span>
</a>
```

On desktop, prefer badge and text side by side. On narrow mobile footers, side-by-side is still fine if it fits; otherwise stack neatly. The text must not overflow the footer column, so add `min-w-0`, `break-words`, or equivalent if the local layout needs it.

## Workflow

1. Find the footer file. Common locations are `src/components/layout/Footer.tsx`, `src/components/Footer.tsx`, `src/layout/Footer.*`, or template partials.
2. Copy `assets/APC-seal.png` from this skill into the target site's public image folder if no project asset already exists.
3. Add a compact linked badge block in the best footer column using the placement rules above.
4. Match existing footer typography and hover treatment. The block should read as secondary trust evidence, not a primary CTA.
5. Run the normal verification command, at minimum `npm run build` for Vite/React sites.
6. Check desktop and mobile footer layouts.
7. If the user asked you to commit, use a clear message such as `Add APC certification badge to footer`.

## Quality Checklist

- The whole badge block links to `https://www.funeralcelebrantacademy.co.uk`.
- The link opens in a new tab with `rel="noopener noreferrer"`.
- The image uses `alt="Academy of Professional Celebrants certified badge"`.
- The visible text says `Trained and certified by the Academy of Professional Celebrants`.
- The badge is compact, roughly 56px square unless the local footer scale clearly calls for a small adjustment.
- The footer's existing style and responsive layout remain intact.
- `npm run build` passes, or the final response clearly reports why verification could not run.
