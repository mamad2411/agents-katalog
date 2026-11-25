---
name: recording-studio-flatpack
description: Build Recording Studio screens with Flatpack ViewComponents instead of custom HTML or Tailwind. Use when adding or changing UI, forms, alerts, cards, or navigation. For the words on the screen, use recording-studio-text.
---

# Flatpack UI

Flatpack is the Recording Studio UI library. Search for an existing component before writing markup.

For **page shape** — UI slices, mount points, replaceable gem views, one-action screens, and the core default layout — follow `recording-studio-ui` first. This skill is which Flatpack component to render. For taste critique and named-theme direction, use `recording-studio-taste`.

## When to use

- Adding or changing a screen, form, alert, card, table, modal, or navigation
- Deciding whether custom HTML is justified
- Checking that CSS actually loaded in the running app

## Instructions

1. Look up the component in this repo's Flatpack usage and at https://flatpack.bowerbird.io/.
2. Compose Flatpack components. Do not recreate buttons, forms, alerts, cards, or nav with custom markup.
3. Semantic layout markup is fine when Flatpack has no structure for it.
4. If Flatpack cannot support the requirement, explain the gap before adding custom UI.
5. Do not rewrite unrelated legacy UI just because it is in a touched file. Migrate a legacy element only when the change is local and behavior stays the same.
6. Words on the screen: `recording-studio-text`. Use Flatpack `Tooltip` and `Popover` when a visible label is not obvious.

## Validation

- Start the app and confirm Tailwind/Flatpack CSS loaded.
- Screenshot the screens you changed.
- Exercise the flow, not just the default render.
