---
name: nextjs-image-optimization
description: Always use next/image; never raw img tags
---

# Next.js Image Optimization

`next/image` is a drop-in replacement for `<img>` that automatically handles lazy loading, format conversion (WebP/AVIF), responsive sizes, and Core Web Vitals (CLS prevention via reserved space). Raw `<img>` tags opt out of all of this.

## Rules

- **Always import `Image` from `next/image`** and use it instead of `<img>`.
- **Provide `width` and `height` for remote/string sources** (or `fill` + a positioned parent) to prevent layout shift. Static imports infer dimensions automatically; never omit both for non-static sources.
- **Use `fill` with `sizes`** for responsive images that take a percentage of their container.
- **Set `priority` on above-the-fold images** (hero, LCP candidate) to preload them.
- **Never use raw `<img>`** in application code. The only acceptable exception is inside SVG markup or third-party embed iframes.

## Examples

```tsx
// BAD
<img src="/hero.jpg" alt="Hero" />

// GOOD — fixed dimensions
import Image from 'next/image'
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />

// GOOD — fills its container (parent must be position: relative with a height)
<div className="relative h-64 w-full">
  <Image
    src="/banner.jpg"
    alt="Banner"
    fill
    sizes="100vw"
    className="object-cover"
  />
</div>

// GOOD — remote image (must be whitelisted in next.config.js remotePatterns)
<Image
  src="https://cdn.example.com/avatar.webp"
  alt="User avatar"
  width={48}
  height={48}
/>
```

## next.config.js

Remote images must be explicitly whitelisted:

```js
/** @type {import('next').NextConfig} */
module.exports = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.example.com' },
    ],
  },
}
```
