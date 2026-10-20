---
name: ui-performance-stability
description: "Diagnose UI Web Vitals, layout shifts, bundles, rendering, and large-list performance."
---

# UI Performance Stability

Frontend performance is part of UX. The interface should stay responsive and visually stable with realistic data and slow networks.

## Process

1. Identify performance-sensitive surfaces: first viewport, LCP element, large lists, tables, charts, forms, third-party scripts, images, fonts, and async sections.
2. Reserve dimensions for images, iframes, skeletons, cards, avatars, charts, alerts and lazy-loaded components.
3. Avoid adding content above the user's current reading position unless caused by direct user action.
4. Limit initial JS and lazy load heavy views, libraries and non-critical media.
5. Avoid rendering thousands of elements without pagination or virtualization.
6. Avoid expensive filtering/sorting/parsing in render paths.
7. Distinguish server state from client state and avoid request waterfalls.
8. Test with realistic record counts, weak devices, slow API, background refetch and retries.

## Layout Shift Causes

- images or iframes without dimensions;
- ads, embeds or charts without reserved space;
- font metric changes after load;
- skeleton size different from final UI;
- late alert/banner above content;
- lazy component with unknown height;
- tables changing column widths after data arrives;
- conditional rendering without stable container;
- validation errors changing input heights.

## CLS Rules

- Set width/height or `aspect-ratio` for images and media.
- Set min-height for async sections.
- Match skeleton size to final UI.
- Reserve space for toasts, banners and sticky elements when they can affect layout.
- Avoid shifting content above what the user is reading.
- Keep table column widths/wrapping predictable.
- Reserve error-message space or render errors without moving the whole form.
- Use stable dimensions for avatars and icons.

## Performance Rules

- Limit JS on first entry.
- Lazy load heavy views and libraries.
- Do not import a whole icon library for a few icons.
- Use pagination or virtualization for large lists.
- Avoid expensive calculations in render.
- Memoize only when cost and dependencies are understood.
- Do not put all state in global state.
- Use API cache but avoid hiding auth/permission changes.
- Avoid request waterfalls.
- Prefetch only when likely to be used.
- Optimize images, fonts and third-party scripts.
- Measure on weaker devices.

## Component Performance

Watch for:

- constantly recreated objects in deep trees;
- costly inline callbacks in huge lists;
- sorting/filtering on every render;
- hidden but still rendered huge DOM;
- drag-and-drop with large lists;
- charts with too many points;
- rich text parsers running repeatedly.
