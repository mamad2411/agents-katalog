---
name: ui-part-images
description: "Images that show the real thing: choosing them, aspect ratios and focal points, art direction with picture, srcset and sizes, the LCP image and lazy loading, placeholders that do not shift the layout, formats and image CDNs, alt text, captions and credits, galleries and lightboxes, and both themes. Read before adding or reworking images on a page."
---

# Images

The generated version: a stock photograph of smiling people around a laptop
presented as the team, a 4000px JPEG scaled down in CSS, every image lazy
including the one in the hero, the page jumping as each one arrives, and
`alt="image"`. An image earns its place by showing the product, the place,
the people or the work, and it arrives at the right size without moving
anything. The principles are in the `ui` skill, the measures in
`ui-layout`, the loading budget in `frontend-performance`.

## 1. Choose the image

- Real images of the real thing: the product in use, its interface as a
  screenshot, the shop front, the people who work there (with their
  consent), the finished work. A plain real photograph beats a polished
  stock one.
- Never stock clichés (a handshake, a laptop beside a coffee, a team
  laughing at a whiteboard) and never generated people presented as real
  staff, customers or patients. Stock photographs of people presented as
  the team or the customers are a lie readers often spot.
- No images of text: a headline, a price list or a menu set in an image
  cannot be read aloud, translated, searched or enlarged. Set it in HTML.
- No image yet: leave the slot out, or keep it at its final aspect ratio
  with a visible placeholder (`[Photo: the treatment room]`) listed in your
  report. Never a random photo that looks final.
- Decoration is not a reason: abstract 3D shapes, gradient meshes and
  generic illustrations say nothing about this product (`ui`, section 1).
- Only images the project may use: its own, licensed, or credited the way
  the licence asks.

## 2. Boxes, ratios and crops

- Every image has its box before it loads: `width` and `height` set, or
  `aspect-ratio`, so nothing jumps. With `max-width: 100%; height: auto`
  the attributes give the ratio without fixing the size.
- One ratio per group: every card in a grid shares a ratio, cropped with
  `object-fit: cover` and a focal point, `object-position: 50% 30%` when
  faces sit high in the frame.

| Use | Ratio |
|---|---|
| A wide hero, a video poster | 16:9 (21:9 only on wide screens) |
| Photographs in a story or a case study | 3:2 |
| Product grids, thumbnails | 1:1 or 4:5 |
| Portraits, the phone crop of a hero | 4:5 or 3:4 |
| Screenshots | their own ratio, never cropped through the interface |

- Radius from the tokens; an image inside a padded card takes the card's
  radius minus the padding; a full-bleed image has none.
- Screenshots at 1x and 2x of their display size, never scaled up, the text
  in them readable where they are shown, or cropped to the part that
  matters.

## 3. Sources and formats

- `srcset` with widths and `sizes` for photographs: five to seven widths
  from about 400 to 2400px. `sizes` describes the display width the way the
  layout does (`(min-width: 1024px) 50vw, 100vw`). Without it the browser
  assumes `100vw` and downloads an image twice as wide as a half-width
  column needs.
- Art direction with `<picture>` and `<source media>`: a different crop for
  phones (a 4:5 crop on the subject) rather than a wide image shrunk until
  the subject is a speck. Each `<source>` carries its own `width` and
  `height`, so the ratio changes without a jump.
- Formats: AVIF first, WebP next, JPEG as the fallback, through `<picture>`
  `type` sources or the image CDN's negotiation. PNG or lossless WebP for
  screenshots with text and flat colour; SVG for logos, icons and diagrams
  (inline on a two-theme page, `ui-themes`). Quality about 50 to 60 for
  AVIF, 75 to 80 for WebP and JPEG; a hero under about 200 KB, a thumbnail
  under about 40 KB.
- Let a pipeline make the sizes: the framework's component (`next/image`,
  `astro:assets` with `<Image>` and `<Picture>`, `@nuxt/image`,
  `@sveltejs/enhanced-img`), an image CDN (Cloudinary, imgix, Cloudflare
  Images, Bunny, through Unpic), or `sharp` and `vite-imagetools` at build
  time for a static site. Never one 4000px original scaled down in CSS.

## 4. Loading

- The LCP image (usually the hero, or the first product photo) loads
  first: no `loading="lazy"` on it, `fetchpriority="high"`, and in a
  framework the component's own switch (`priority` in `next/image`, renamed
  `preload` in Next.js 16), on that one image only. A CSS background that
  is the LCP element needs `<link rel="preload" as="image" imagesrcset
  imagesizes>`; better, make it an `<img>`.
- `loading="lazy"` below the fold: roughly everything after the first
  screen on a phone. Lazy on the first screen delays the page.
- Placeholders that do not shift the layout: the box is already sized;
  fill it with the dominant colour (a background on the image or its
  wrapper) or a blurred 16 to 32px preview inlined as a data URI
  (`placeholder="blur"` in `next/image`, BlurHash, ThumbHash). The image
  then appears, or fades over it in 200ms at most.
- A failed image shows its box, a quiet icon and the alt text, never the
  browser's broken-image glyph: an `error` handler swaps in a fallback.

## 5. Alt text

- Alt text that says what the image shows, for this context: a product
  photo names the product and what sets it apart ("Oak bench, 180cm, with a
  live edge"); a photo of a clinic says what the reader learns from it; a
  linked image says where the link goes.
- `alt=""` for decoration, and for an image whose content is already in
  the text beside it (an avatar next to the printed name).
- No "image of" or "photo of" (the screen reader already says image), no
  file names, no keywords stuffed in. One or two sentences. A chart or a
  diagram gets a short alt with its point, and the data in a table or the
  text nearby (`ui-part-charts`).
- A logo's alt is the organisation's name, not "logo". An unavoidable
  image of text (a scanned letter) carries the text in its alt.
- Every `<img>` has the attribute: with none, screen readers read out the
  file name.

## 6. Captions, credits, galleries

- `<figure>` and `<figcaption>` when the image needs context: where, when,
  who. The caption adds what the picture cannot say; the alt says what is
  seen; they do not repeat each other.
- Credits in small muted text (12 to 14px): the photographer, and the
  licence when it requires attribution (Creative Commons BY does).
- Galleries: thumbnails in one ratio, each a link to the full image (it
  works without JavaScript) or a button that opens a lightbox; targets at
  least 44px.
- A lightbox is a modal dialog (`dialog` with `showModal()`, PhotoSwipe, or
  yet-another-react-lightbox): focus moves in and returns to the thumbnail
  on close; Escape and a labelled Close button; Left and Right for previous
  and next; swipe and pinch zoom on touch; a counter ("3 of 12") and the
  caption; the neighbours preloaded; the open image in the URL
  (`?photo=3`) when people share one.
- Carousels: a row with scroll snap (`scroll-snap-type: x mandatory`),
  visible Previous and Next buttons, the next image peeking at the edge.
  No autoplay; if the brief insists, a pause button, and stopped on hover
  and focus (WCAG 2.2.2).

## 7. Phones, themes and motion

- `max-width: 100%` on every image; full-bleed on phones where the image is
  the content; the art-directed crop checked at 360px.
- Themes: photos stay as they are; a very bright one may dim slightly on the
  dark theme (`filter: brightness(.9)`), never inverted; screenshots in the
  matching theme or framed; logos and line art per theme (`ui-themes`).
- Motion: no slow zoom on photos, no parallax by default; a lightbox opens
  like a dialog (`motion-interface`, section 4); nothing zooms under
  reduced motion.

## 8. A sketch

```html
<!-- The hero: the LCP image, first in line, never lazy. -->
<picture>
  <source media="(max-width: 639px)" type="image/avif" width="960" height="1200"
          srcset="/img/room-portrait-480.avif 480w, /img/room-portrait-960.avif 960w"
          sizes="100vw">
  <source type="image/avif"
          srcset="/img/room-800.avif 800w, /img/room-1600.avif 1600w, /img/room-2400.avif 2400w"
          sizes="(min-width: 1024px) 50vw, 100vw">
  <img src="/img/room-1600.jpg" width="1600" height="1067"
       srcset="/img/room-800.jpg 800w, /img/room-1600.jpg 1600w"
       sizes="(min-width: 1024px) 50vw, 100vw" fetchpriority="high"
       alt="Treatment room with two beds and a window onto the garden">
</picture>

<!-- Further down: lazy, sized, in the grid's one ratio. -->
<img class="card-media" src="/img/bench-800.jpg" width="1200" height="800"
     srcset="/img/bench-400.jpg 400w, /img/bench-800.jpg 800w, /img/bench-1200.jpg 1200w"
     sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
     loading="lazy" alt="Oak bench, 180cm, with a live edge">
```

```css
img { max-width: 100%; height: auto; }
.card-media {
  width: 100%;
  aspect-ratio: 3 / 2;
  object-fit: cover;
  object-position: 50% 30%;
  background: var(--surface-2); /* the placeholder colour while it loads */
  border-radius: calc(var(--radius) - var(--space-2));
}
```

## Check it

- `preview` at 360, 768 and 1440px: "images without alt" lists every
  `<img>` with no alt attribute; the overflow list names an image wider
  than the screen; the screenshots show crops that cut off the subject.
- `preview` with `motion: true` reports layout shift over 0.05 while the
  page loads and names what moved: usually images without dimensions.
- `ui_check` flags `<img>` and `<Image>` without `alt=`.
- DevTools at 360 and 1440px, Network filtered to images: each file is
  close to its displayed size times the pixel ratio (`currentSrc` in the
  console), the hero is requested first and is not lazy. Lighthouse names
  the LCP element and any oversized image.
- Read each alt aloud with the image hidden: it tells the reader what they
  need here.

## Avoid

Stock photographs of people presented as the team or the customers;
generated faces; images of text; `alt="image"`, a missing alt or a file
name; a 4000px original scaled down in CSS; `loading="lazy"` on the hero;
no dimensions, so the page jumps; a different ratio on every card, so the
grid is ragged; faces cropped at the forehead; autoplaying carousels; a
lightbox with no close button that loses the place on close; inverted
photos on the dark theme; a placeholder image that looks final.
