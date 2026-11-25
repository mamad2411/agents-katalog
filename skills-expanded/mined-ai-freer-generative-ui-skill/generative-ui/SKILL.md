---
name: generative-ui
description: "Create inline visualizations and interactive widgets in hosts that support show-widget: diagrams, charts, parameter tools and spatial explainers. Use for requested visual or interactive explanations, not standalone website development or routine text-only questions."
metadata: { "openclaw": { "emoji": "📊" } }
---

# Generative UI

Help the user understand a relationship, explore a variable or finish a task. A widget is a means, not the default answer to every question.

## Shared generation

Read [the generation contract](prompts/system.md) and [core guidance](prompts/guidelines/core.md). Choose the smallest useful form: text, static comparison, local interactive tool, or 3D when space, shape or motion is central. Respect an explicitly requested format.

Load only the relevant guidelines, using the module table in the contract. Do not read every long template or example up front. Playground exposes explicit task profiles; old sessions and requests without a profile keep the all-module baseline. Profiles select guidance, not a required answer format.

- Charts: [chart](prompts/guidelines/chart.md), UI and color guidance from the module table.
- Diagrams: [diagram](prompts/guidelines/diagram.md), SVG and color guidance.
- Controls and prototypes: [UI components](prompts/guidelines/ui-components.md) and color guidance.
- Spatial scenes: [3D scenes](prompts/guidelines/3d-scene.md); identify important shapes and relations before adding detail. More geometry does not imply measurement accuracy or Gaussian Splatting.
- Illustrations: [art](prompts/guidelines/art.md) and SVG guidance.

Use examples only for a relevant implementation detail, not as compulsory page templates. The maintained [probability experiment](examples/dice-probability.html) and [architecture example](examples/palace-detail.html) are illustrations, not scientific or survey-grade reconstructions.

## Constraints and delivery

- Keep the fragment/fence format, sandbox and allowed resources, valid calculations, accessible controls and synchronized state. Never invent data or claim an unavailable tool was used.
- Native, flat styling is the default, not a ban on an explicit brand or visual direction. Preserve contrast, readable labels, responsive layout and usable streaming previews.
- Prefer local operations. Use `window.__widgetSendMessage()` only for an explicitly labelled request for new content. Preserve unrelated state in revisions; do not promise cross-reload persistence without host support.
- **Interactive hosts / Playground:** return the supported widget format. Do not replace an interactive deliverable with an IM screenshot workflow.
- **OpenClaw IM only:** read [channel delivery](references/openclaw-im.md) for its screenshot, environment and button requirements. Sending still requires authorization for that channel and recipient.

## Acceptance

Use [task-based validation](references/validation.md) when rendering or browser tools are available, or when preparing an evaluation. Check the initial view and a meaningful action, including the visible result and computed values. Repair evidenced problems locally within the authorized scope; do not silently add paid calls, retries or uploads.

Report generated, rendered, behavior-checked and visually-checked separately. With no runtime tools, say those checks were not performed. An HTML file, a screenshot or a successful model response alone is not task acceptance.
