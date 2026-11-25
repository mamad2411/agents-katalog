---
name: media-optimization
description: Image and video discipline for an Astro 7 site on Cloudflare Workers Static Assets — build-time image optimization with an EXPLICIT compile image service (the adapter default now routes through metered Cloudflare Images, whose free tier fails closed), responsive images via one global layout, priority on the LCP image only, and a video ladder from compressed mp4 in public/ through R2 to Media Transformations. Use when a site ships heavy images or video, when the LCP image is slow, when choosing formats like AVIF or WebP, when configuring astro assets responsive layouts, when a video exceeds the 25 MiB static-asset cap, or when weighing R2, Media Transformations, and Stream. Trigger on optimize my images, responsive images, slow LCP image, video too heavy, self-host video, or autoplay background video. Not for the CI budgets that enforce weight (perf-ci-gates), the WebGL hero and its fallback (webgl-atmosfera), client media libraries (cms-self-edit), or brand exact-file assets (brand-canon-ingest).
---

# media-optimization

> Media on this stack is produced at BUILD TIME: sharp transforms every image during the build, the browser gets srcset/sizes generated from one global layout config, and video ships as aggressively compressed files on the tier the file size dictates. The single most important line is `imageService: 'compile'` — the adapter's DEFAULT quietly turns a free static site into a dependency on a metered service that stops serving images when its free quota runs out.

## Reference materials — load when relevant

This SKILL.md is the verdict and the four locked decisions. Load references only when their content is needed:

- `references/image-pipeline.md` — load when configuring the image service and responsive layout, marking the LCP image, handling remote images or SVGs, or picking formats and quality.
- `references/video-tiers.md` — load when a site ships any video: the compression recipe, the public/ → R2 → Media Transformations ladder with verified caps and billing semantics, poster and reduced-motion wiring, and the Stream flip.

## Verdict

Images are optimized by sharp at build time — full fidelity, zero runtime quota, deterministic CI, works on every preview URL — by pinning the adapter's image service to `compile` explicitly, never trusting the default. Responsive behavior comes from ONE global config (`image.layout: 'constrained'` + `image.responsiveStyles: true`) instead of hand-rolled `sizes`; the LCP image and only the LCP image carries `priority`. Video has no Astro-native path at all: it ships as compressed H.264 mp4 in `public/` under the 25 MiB per-file Static Assets cap, escalates to R2 behind a custom domain when it outgrows that, and mints sized derivatives via Media Transformations instead of storing N encodes. Cloudflare Images is an escape hatch for genuinely dynamic imagery, never the default.

## The four locked decisions

| # | Decision | Rule | Flip when |
|---|---|---|---|
| m1 | Image service | `imageService: 'compile'` EXPLICIT in the adapter config | Genuinely dynamic imagery (on-demand routes, CMS images that must change without rebuild) or build times exploding on thousands of originals — then the binding, on paid |
| m2 | Responsive posture | Global `image.layout: 'constrained'` + `responsiveStyles: true`; per-image overrides (`full-width` banners, `none` opt-out); `priority` on the single LCP image per page | Art direction per breakpoint — explicit Picture with widths/pictureAttributes for those slots only |
| m3 | Video | Tiered — mp4 in `public/` (hard cap 25 MiB/file, budget far lower) → R2 custom domain → Media Transformations derivatives | Long-form, adaptive bitrate, or live — Stream, which has NO free tier |
| m4 | Cloudflare Images | Escape hatch only | User-uploaded or runtime-transformed imagery as a real product need |

## Why m1 is the anchor (verified drift)

- The adapter's default image service flipped from `compile` to `cloudflare-binding` in `@astrojs/cloudflare` v13.0.0 (2026-03), under users' feet — both current majors (13 and 14) carry the new default. The compound form `imageService: { build, runtime }` dates from v13.0.0 too; the `build: 'cloudflare-binding'` option value needs ≥14.2.0.
- The default routes image work through Cloudflare Images, whose FREE tier is 5,000 unique transformations per month and FAILS CLOSED — past the cap, new transformations error (code 9422); there is no overage billing to save you. A modest catalog (500 images × 6 widths = 3,000 uniques) sits uncomfortably close to that cap.
- For a fully prerendered site, request-time transforms buy nothing that build-time sharp does not produce for free. `compile` transforms at build; on-demand pages under it get passthrough — acceptable, because this stack's on-demand surface is endpoints, not image-bearing pages.
- sharp is astro's own optional dependency (`^0.34 || ^0.35`) — do NOT pin sharp separately; let astro resolve it.

## Boundaries

- perf-ci-gates owns every numeric budget and threshold (LCP floor, byte budgets); this skill owns how the artifacts that pass them are produced. No budget number lives here.
- webgl-atmosfera owns the hero canvas and its raster fallback; brand-canon-ingest owns exact-file brand assets (logos, OG images) that must never enter the transform pipeline; cms-self-edit owns editor media uploads (R2 via the CMS).

## Pins (verified 2026-08-17) and review-gates

| Pin | Value | Review-gate |
|---|---|---|
| `imageService` | `'compile'` explicit, `@astrojs/cloudflare` 14.2.1 | Re-read the adapter changelog on every major — this exact knob already flipped defaults once (v13.0.0) |
| sharp | none — astro optional dep `^0.34 \|\| ^0.35` | If astro drops the optional dep, pin sharp explicitly then |
| Static Assets file cap | 25 MiB/file (free and paid) | Platform limit — re-verify on Cloudflare limits page before designing around it in a new project |
| Media Transformations | GA; $0.50/1k unique ops, shares the 5k/month free pool with Image Transformations; video bills 1 op PER SECOND of output | Billing semantics are young (billed since 2025-11) — re-verify pricing page before wiring it into a client site |

## Limitations and out-of-scope

- No numeric performance budgets here — compose perf-ci-gates for enforcement; its resource-summary image budget is the gate this skill's output must pass.
- Font optimization is its own surface (Astro Fonts API) and stays with the token/foundation layer, not here.
- The `custom` image service value bundles arbitrary services without a workerd compatibility check — sharp does not run on workerd, so `custom`+sharp breaks at runtime on any on-demand page; treat `custom` as out of scope.
- Behavior of `build: 'cloudflare-binding'` during local static builds (emulation fidelity, AVIF availability) is undocumented — anyone taking that flip must smoke-test it first.
