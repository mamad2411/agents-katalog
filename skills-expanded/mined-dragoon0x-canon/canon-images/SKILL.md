---
name: canon-images
description: Use when optimizing images for the web — format selection (AVIF, WebP, PNG, SVG), responsive images with srcset, lazy loading, aspect ratio preservation, LCP image optimization, and image CDN usage. Trigger when the user mentions image optimization, srcset, lazy loading images, AVIF, WebP, image format, or responsive images.
---

# CANON · Images

Images are the largest payload on most pages. Format, size, and loading strategy make or break performance.

## Format decision tree

```
Is it a photo or complex gradient?
  ├─ Yes → AVIF (best compression), WebP fallback, JPEG last resort
  └─ No →
     Is it an icon, logo, or simple shape?
       ├─ Yes → SVG (infinitely scalable, tiny file)
       └─ No →
          Does it need transparency?
            ├─ Yes → WebP or PNG (WebP preferred, smaller)
            └─ No → AVIF/WebP/JPEG
```

## Responsive images — srcset

Serve the right size for the viewport. Don't send a 2400px image to a 375px phone.

```html
<img
  src="hero-800.webp"
  srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w, hero-1600.webp 1600w"
  sizes="(max-width: 768px) 100vw, 50vw"
  alt="Product showcase"
  width="1200"
  height="800"
  loading="lazy"
  decoding="async"
>
```

## LCP image — the critical one

The Largest Contentful Paint image needs special treatment:

- **No `loading="lazy"`** — it must load eagerly.
- **`fetchpriority="high"`** — tells the browser to prioritize.
- **Preload** — `<link rel="preload" as="image" href="hero.webp">`.
- **Serve at rendered size** — don't serve 3000px for a 600px container.

```html
<link rel="preload" as="image" href="hero.webp" fetchpriority="high">
<img src="hero.webp" alt="..." width="1200" height="800" fetchpriority="high">
```

## Always declare width and height

```html
<img src="photo.webp" alt="..." width="800" height="600">
```

This reserves layout space before the image loads, preventing Cumulative Layout Shift (CLS). The browser calculates aspect ratio from these attributes. CSS can still make the image responsive:

```css
img { max-width: 100%; height: auto; }
```

## Lazy loading

All images below the fold should use `loading="lazy"`. Native browser lazy loading works without JavaScript.

Exception: the LCP image (above the fold) must NOT be lazy loaded.

## Image CDNs

Services like Cloudinary, imgix, Cloudflare Images serve optimized formats and sizes automatically:

```
https://cdn.example.com/photo.jpg?w=800&format=auto&quality=75
```

Quality 70–80 is visually lossless for photos. Below 60, artifacts appear.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Serving PNG for photos | 5–10× larger than WebP/AVIF |
| No srcset (one giant image for all screens) | Wasted bandwidth on mobile |
| Lazy loading the LCP image | Delays the most important metric |
| No width/height attributes | Layout shift (CLS) |
| Using JPEG 2000 or JPEG XR | Poor browser support |
| Base64-inlining large images | Inflates HTML, blocks parser |
| Screenshots as PNG when WebP would work | Unnecessary size |

## Audit checklist

- [ ] Photos use AVIF/WebP, not PNG/JPEG
- [ ] Icons and logos use SVG
- [ ] LCP image has `fetchpriority="high"`, no lazy, preloaded
- [ ] All images have `width` and `height` attributes
- [ ] Below-fold images use `loading="lazy"`
- [ ] `srcset` + `sizes` on responsive images
- [ ] Image quality 70–80 for photos
- [ ] No base64-inlined images > 2KB

## Sources

- web.dev · "Serve images in modern formats", "Optimize LCP"
- `canon-performance` for Core Web Vitals targets
- Cloudinary · image optimization best practices
