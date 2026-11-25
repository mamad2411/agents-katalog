---
name: signal-deck-design
description: "Create or restyle HTML slideshows in the saved Signal Deck visual language: cool plotting paper, disciplined sans/mono typography, flat technical geometry, measurement motifs, and restrained semantic color. Use when the user requests the Signal Deck look or wants a slideshow to feel like a precise measuring instrument. Do not use for generic presentations without this visual direction."
---

# Signal Deck Design

Build a self-contained HTML deck that feels like a precise measuring instrument. This skill governs visual direction, composition, typography, graphic language, interaction, and finish.

## Content boundary

Treat the supplied content, ordering, and argument as the source of truth. Make only light edits needed for fit, legibility, or obvious repetition unless the user also asks for writing or narrative work. Do not impose a decision framework, a one-claim-per-slide rule, or a required facts/inferences/actions taxonomy.

Preserve factual qualifiers, sources, and sensitive-data boundaries while styling. When content is sparse, establish visual hierarchy without inventing a stronger argument than the source supports.

## Apply the saved visual language

Read [references/visual-system.md](references/visual-system.md) before designing or editing the deck. Its token meanings and typography rules are part of this style.

The core invariants are:

- cool grey plotting-sheet ground, graphite text, and a restrained technical grid;
- local-safe modern sans for editorial headlines and body copy;
- monospace only for dates, labels, sources, and tabular data;
- one primary signal color for measured evidence;
- amber reserved for an action, warning, or future decision;
- diagonal hatch reserved for incomplete, unresolved, or noisy data;
- a recurring measurement device derived from the subject: a rail, axis, route, slope, range, or ledger;
- flat geometry without gradients, shadows, ornamental icons, rounded dashboard tiles, or decorative chrome.

Choose the signature measurement device to suit the material. It may be structural rather than analytical, but its labels and geometry must remain coherent with the content.

Use sentence case for main headlines. Small utility labels may be uppercase. Avoid condensed display faces, oversized all-caps paragraphs, high-contrast serif headlines, and tiny body copy.

## Build from the template

For a new deck, start from [assets/signal-deck-template.html](assets/signal-deck-template.html) and adapt its tokens, slide shell, navigation, and accessibility behavior. Replace the example content and extend the layout vocabulary to suit the supplied material.

For an existing deck, preserve correct content and interaction behavior while replacing the visual system coherently. Do not layer this style on top of conflicting components.

Keep the deliverable self-contained unless the user requests a build system. Prefer semantic HTML, inline CSS, and small dependency-free JavaScript.

## Interaction requirements

Support:

- previous/next controls;
- Left/Right, Page Up/Page Down, Space, Home, and End keys;
- direct `#slide-number` links;
- touch swipes on mobile;
- visible keyboard focus;
- `prefers-reduced-motion`;
- readable mobile reflow;
- print output with one slide per page when the deck may be printed or exported.

Controls, slide position, and sources must remain legible without obscuring content.

## Quality check

Render the actual result, not only the source. Check at minimum:

- `1280×800` desktop presentation;
- `390×844` mobile;
- first, densest, and final slides;
- every slide for clipped or hidden content;
- correct keyboard, button, swipe, and hash navigation;
- consistent number formatting and labels;
- sufficient contrast and meaningful color without color-only interpretation.

If a slide overflows, edit its composition or copy. Do not solve it by shrinking body text below comfortable reading size.

When archiving, generate a preview image and update the repository's existing gallery/index workflow. Create a public tunnel only when the user asks for one, and make clear when that URL is ephemeral.
