---
name: social-media-blog-cover
description: Make the cover for a blog post or article (1200 x 630 OG card and 1920 x 1080) with design's banner-design engine, in Thai or English, and bench it for crop, contrast and phone width. Title-led: kicker, 2 or 3 title lines, a handwritten note, the author, and a motif that shows the post's subject. Thai uses Kanit, Anuphan and Mali. Use WHENEVER the user wants a blog cover, article cover, OG image, post thumbnail, hero image for a post, "ทำปกบทความ", "ปกบล็อก", "รูปปกโพสต์", or blog-post hands over a title.
---

# Blog cover and post images

A post gets three kinds of image from one spec: the cover, one image per explained step, and a
closing image of the finished work. A cover carries the post's title and little else, and it is read at feed size first (about 360 to 400px wide),
so the title is the only core element; everything else is support or decoration.

The renderer is [`../../design/banner-design/scripts/banner.py`](../../design/banner-design/scripts/banner.py)
with the `cover` layout. This sub-skill holds the cover rules and the spec; it adds no second renderer.

## The spec

A post's images live in one spec with `pages`. Each page names its layout, size and content;
`render` lists the styles (a page may override it). Files come out as `{id}-{style}-{W}x{H}.svg`.

```json
{
  "fonts": {"title": "kanit-700", "strong": "anuphan-700", "text": "anuphan-500", "accent": "mali-600"},
  "styles": {"riso": {"...": "tokens"}},
  "render": ["riso"],
  "pages": [
    {"id": "cover", "layout": "cover", "sizes": [[1200, 630], [1920, 1080]], "cover": {"...": "below"}},
    {"id": "step-1", "layout": "step", "size": [1200, 675],
     "step": {"kicker": "ขั้นที่ 1 จาก 4", "num": "01", "title": ["two short", "lines"], "caption": ["one or two lines"],
              "visual": {"kind": "checks", "rows": [{"mark": "pass", "text": "..."}, {"mark": "fail", "text": "..."}]},
              "author": "name · link"}},
    {"id": "end", "layout": "stack", "size": [1200, 675], "brand": {}, "steps": [], "cta": {}}
  ]
}
```

A step's `visual` is `checks` (rows marked pass or fail), `code` (mono lines) or `size` (a file frame
with the shown frame inside, both labelled). The closing page reuses any banner layout with the
finished banner's own content, restyled in the post's theme.

The cover block on its own:

```json
{
  "sizes": [[1200, 630], [1920, 1080]],
  "fonts": {"title": "kanit-700", "strong": "anuphan-700", "text": "anuphan-500", "accent": "mali-600"},
  "cover": {
    "kicker": "what the post is about, in a few words",
    "title": ["2 or 3", "short lines"],
    "note": "one handwritten line (optional)",
    "author": "name · link",
    "motif": ["columns", "rail", "stairs", "bento", "stack"]
  },
  "styles": {"mine": {"...": "tokens as in banner-design, plus accent"}},
  "variants": ["cover-mine"]
}
```

- `fonts` maps roles to `family-weight`. Thai text needs a Thai family: Kanit 700 for titles, Anuphan
  500/700 for labels and the kicker, Mali 600 for the handwritten note. Archivo and JetBrains Mono
  have no Thai glyphs, and the renderer refuses a string a font can't draw.
- `motif` draws thumbnails of banner layouts; for a post on another subject, leave it out or add a
  motif to `banner.py` that shows that subject.
- The title is drawn twice: the ink copy is the core zone, and an accent copy offset by a few pixels
  sits in the decorative zone (`data-zone="decor"`), which the bench skips.

## Workflow

1. Take the title and kicker from blog-post. Cut the title to 2 or 3 lines that read alone.
2. Pick a style that is not the brand's last campaign: the cover belongs to the post. Define it in the
   spec's `styles` so it travels with the spec.
3. Render: `uv run ../../design/banner-design/scripts/banner.py cover.banner.json` (every size, every variant).
4. Bench each SVG with `bench.py`; fix every FAIL in the spec or the layout, never by hand-editing SVG.
5. Look at the `-400.png` export: the title must read in two seconds.

## Done when

- One image per step, plus the cover and the closing image; each placed under its heading.

- Every variant passes `bench.py` at every size.
- Thai text renders whole (check vowels above and below, and ำ) at full size and at 400px.
- The cover's title matches the post's title in meaning, and the kicker names the subject.
