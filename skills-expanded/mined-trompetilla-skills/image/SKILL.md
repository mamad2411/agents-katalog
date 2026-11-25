---
name: Image  
description: Apply specific quality thresholds and compression rules to prevent performance penalties.
---

## Performance Budget Ceilings
- Hero images: 150KB maximum (LCP target), 85% JPEG quality ceiling
- Above-fold thumbnails: 25KB limit, WebP 80% quality with JPEG fallback
- Below-fold content: 400KB budget per viewport, lazy load 200px threshold
- Mobile optimization: 10-15% quality reduction below desktop, 200KB absolute maximum

## Format Selection Thresholds
- Photos >800px: AVIF 60% quality primary, WebP 75% fallback, JPEG 85% baseline
- Transparency required: WebP with alpha 80% quality, PNG fallback mandatory
- Animation limits: WebP animated under 3MB, GIF 16-color palette maximum
- Vector graphics: SVG for scalable elements, PNG-8 for <256 color illustrations

## Quality Target Patterns
- JPEG portraits: 88-92% quality range (skin tone preservation requirement)
- JPEG landscapes: 80-85% quality acceptable (texture compression tolerance)
- WebP compression: Start 10-15% lower than equivalent JPEG quality setting
- E-commerce products: 95% minimum quality (cart abandonment prevention)

## Responsive Implementation Rules
- Density descriptors: 1x, 1.5x, 2x maximum (3x wastes bandwidth unnecessarily)
- Breakpoint set: 480w, 768w, 1200w, 1920w minimum coverage required
- Art direction trigger: Use picture element when aspect ratio changes >20%
- Critical image preloading: Largest variant only, others use loading="lazy"

## Accessibility Standards
- Text overlay contrast: 4.5:1 minimum ratio, drop shadows blur-radius: 3px, offset: 1px
- Alt text limit: 125 characters maximum for screen reader compatibility
- Decorative images: aria-hidden="true" mandatory, remove from tab order

## Compression Optimization
- Progressive JPEG: Mandatory for images >40KB file size
- EXIF stripping: Automated removal saves 10-50KB, preserve orientation data only
- ICC profile removal: 8-20% file size reduction for sRGB color space
- Sharp resizing: Lanczos3 for >50% downscaling, bicubic for minor adjustments