---
name: ui-responsive-media
description: "Implement responsive UI/media across breakpoints, touch, zoom, images, video, and iframes."
---

# UI Responsive Media

Responsive design adapts layout, priorities and interaction model to the device. It is not just a smaller desktop.

## Process

1. Decide what information and actions are needed first on small screens.
2. Design content flow before choosing breakpoints; use flex/grid/min/max/container constraints.
3. Prefer one responsive implementation unless mobile and desktop interaction models are genuinely different.
4. Convert dense desktop patterns intentionally: tables to cards, filters to drawers/bottom sheets, sidebars to contextual nav, detail panels to separate screens or expanded cards.
5. Use max-widths and additional context on desktop instead of stretching mobile layouts.
6. Set stable dimensions or aspect ratios for images, videos, iframes, avatars, thumbnails, charts and media placeholders.
7. Test real viewport sizes, landscape mobile, zoom, long text, touch, keyboard, soft keyboard and safe areas.

## General Rules

- Breakpoints come from content, not device names.
- Do not design for one specific phone or laptop.
- Store repeated breakpoints in the design system.
- Consider container queries when component width matters more than viewport width.
- Mobile-first layers are usually easier than desktop-down overrides.
- Do not use breakpoints to hide content problems.

## Desktop To Mobile

- Prioritize immediate information.
- Move secondary data into details, accordion or separate screens.
- Convert multi-column layout to ordered sections.
- Convert unreadable tables to card lists.
- Move filters into drawer, bottom sheet or collapsible section.
- Make the main action reachable by touch.
- Do not hide actions behind hover.
- Increase touch targets.
- Avoid precise drag when a simpler control works.
- Keep modals within viewport height and avoid stacked overlays.

## Mobile To Desktop

- Do not stretch narrow forms to full width.
- Use max-widths and layout rhythm.
- Use extra space for preview, context or details panel.
- Do not add actions only because there is space.
- Group related data into sections.
- Use master-detail or side panels when they shorten the workflow.

## Images And Media

- Set `width`/`height` or `aspect-ratio`.
- Use responsive image sources where useful.
- Lazy load images outside the first screen.
- Do not lazy load the LCP image.
- Reserve space for avatars, thumbnails, charts and iframes.
- Avoid rendering images larger than needed.
- Provide fallback for broken images.
- Give video and iframe stable aspect ratio and placeholder.

## Responsive QA

Check:

- mobile portrait and landscape;
- tablet, desktop and wide desktop;
- zoom 125 percent and 200 percent;
- no unwanted horizontal scroll;
- sticky header/footer does not cover content;
- modal fits on small screens;
- mobile keyboard does not hide active fields;
- tables/lists have readable mobile variants;
- filters and sorting work without hover;
- safe area on iOS does not cover actions.
