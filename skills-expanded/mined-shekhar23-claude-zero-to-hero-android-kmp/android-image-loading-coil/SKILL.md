---
name: android-image-loading-coil
description: |
  Coil image loading patterns for Android/Compose - async images, placeholders, sizing, caching, transformations, and list performance. Use this skill whenever loading remote or local images, optimizing image-heavy screens, handling loading/error states, or deciding how images should be displayed in Compose. Trigger on phrases like "Coil", "AsyncImage", "image loading", "placeholder", "image cache", "transformations", or "loading avatars/photos".
---

# Android Image Loading with Coil

## Core Principles

- Load images with explicit sizing whenever possible.
- Treat image loading as UI infrastructure, not business logic.
- Prefer simple loading pipelines before adding transformations.
- Keep loading/error UI states intentional.
- Optimize for scrolling performance on image-heavy screens.

---

## Default Compose Usage

For most screens, use Coil's Compose integration:

```kotlin
AsyncImage(
    model = imageUrl,
    contentDescription = stringResource(R.string.cd_profile_photo),
    modifier = Modifier.size(64.dp),
    contentScale = ContentScale.Crop
)
```

This is appropriate for:
- avatars
- thumbnails
- banners
- article/product images

---

## Prefer Explicit Image Requests When Needed

Use `ImageRequest` when behavior should be controlled more precisely:

```kotlin
AsyncImage(
    model = ImageRequest.Builder(LocalContext.current)
        .data(imageUrl)
        .crossfade(true)
        .build(),
    contentDescription = stringResource(R.string.cd_cover_image)
)
```

Good reasons to use `ImageRequest`:
- enable crossfade
- specify placeholders or error drawables
- set size or transformations
- add headers or special cache behavior

---

## Loading and Error States

Screens should define what happens when an image:
- is loading
- fails to load
- is absent entirely

Typical options:
- placeholder while loading
- fallback avatar/icon when missing
- stable error UI when request fails

Avoid blank flashing regions when image state matters to layout clarity.

---

## Size Matters

One of the biggest image mistakes is loading much larger images than the UI needs.

Guidelines:
- constrain layout size intentionally
- avoid full-resolution loads for small thumbnails
- use crop/fit rules that match the design
- prefer server-provided thumbnail sizes when available

Large, unnecessary decodes hurt memory and scrolling performance.

---

## List Performance

For list/grid screens:
- keep image composables simple
- avoid expensive per-item transformations when possible
- provide stable item keys in lazy lists when appropriate
- avoid rebuilding complex requests unnecessarily
- prefer thumbnails in feeds and full images only on detail screens

See the **android-compose-ui** and **android-performance-profiling** skills for adjacent list and UI performance guidance.

---

## Content Scale

Choose `ContentScale` intentionally:

- `Crop` for avatars and edge-to-edge cards
- `Fit` when the full image must remain visible
- `FillBounds` only when distortion is acceptable

Wrong scale choices create visual bugs even when loading succeeds.

---

## Transformations

Use transformations sparingly.

Good uses:
- circle crop for avatars
- rounded corners when layout requires bitmap transformation instead of clipping
- blur only when clearly valuable

Avoid stacking heavy transformations on scrolling lists unless measured.

Often, Compose clipping with shapes is enough and simpler.

---

## Caching

Coil handles memory and disk caching for common cases.

Guidelines:
- rely on defaults first
- customize caching only for a clear reason
- avoid disabling cache casually
- understand that changing request keys/URLs affects cache reuse

If the same image appears across multiple screens, stable URLs/keys improve cache effectiveness.

---

## Accessibility

Every meaningful image needs a proper `contentDescription`.

Rules:
- informative image -> meaningful localized description
- decorative image -> `contentDescription = null`
- do not duplicate nearby visible text unnecessarily

See the **android-compose-ui** and future accessibility/localization guidance for broader semantics rules.

---

## Previews and Testing

For previews:
- use stable sample URLs only if preview support is reliable in the project
- otherwise show placeholder/mock image states

For tests:
- focus on surrounding UI behavior, not real network image loading
- verify placeholders, fallback states, and layout behavior

---

## Checklist: Adding Image Loading

- [ ] Use `AsyncImage` or explicit `ImageRequest` intentionally
- [ ] Define placeholder, fallback, and error behavior
- [ ] Load images at the size the UI actually needs
- [ ] Keep list/grid image requests lightweight
- [ ] Choose `ContentScale` intentionally
- [ ] Add meaningful `contentDescription` or mark decorative images as null