---
name: website-launch-collage
description: Create polished screenshot-led marketing graphics for websites, apps, docs portals, dashboards, and internal tools. Use when someone needs an internal announcement image, product launch visual, feature reveal, team update, or Slack-shareable PNG that combines real interface screenshots with a concise message panel. Supports supplied images, local app captures, live-site references, brand adaptation, exact copy, and secret-safe delivery.
---

# Website Launch Collage

Create a single shareable marketing image that makes a real digital product
feel tangible: recognizable interface screenshots arranged as physical or
editorial objects, plus one concise message card (Slack-style when requested).
The screenshots are the product evidence. The surrounding art direction should
amplify their identity without replacing them with generic UI.

## Workflow

### 1. Frame the communication

Identify:

- audience: internal team, leadership, customers, or community;
- channel: Slack, email, docs, social, or presentation;
- message: launch, milestone, capability, workflow, or invitation;
- required canvas: default to landscape 1536×1024 or 16:9;
- exact copy: headline, support line, proof/feature line, and CTA.

If the user has not supplied copy, draft a compact option and label it as
proposed. Do not invent claims about adoption, performance, canon, security,
or production readiness.

### 2. Gather and inspect references

Prefer three visual surfaces:

1. Overview/home screen — establishes the product identity.
2. Detail/workflow screen — explains the capability or user value.
3. Feature/demo screen — provides a concrete proof object.

Accept supplied screenshots, local screenshots, or live-site captures. Inspect
each local image with `view_image` before generation. If a live site requires
authentication, use the authorized browser/session or an explicit local test
mode; never bypass access controls, inspect cookies/password stores, or copy
secrets from a page.

Record each reference role in the prompt (`Image 1 = overview`, etc.). Preserve
the product's real logo, type character, navigation density, color relationships,
and distinctive feature states. Use a screenshot only as a reference when its
content is stale; tell the user if the visual may no longer represent current
product behavior.

### 3. Choose the visual direction

Use the built-in `image_gen` tool by default. Choose one primary direction from
the reference file [layout-variants.md](references/layout-variants.md), then
adapt its palette and materials to the supplied product.

Good defaults:

- editorial desk: overlapping paper/window sheets with quiet negative space;
- dark product wall: matte dark ground, luminous screenshot cards, restrained
  accent color;
- structured board: asymmetric grid, one dominant screen, compact evidence
  tiles, and a message card;
- device/tabletop: screenshots framed as cards or tablet-like surfaces without
  pretending to be a literal hardware product shot.

Do not force every composition into left-text/right-image. Vary the dominant
screen scale, overlap, crop, and message-card position while keeping one clear
reading path.

### 4. Write the generation prompt

Use this scaffold:

```text
Use case: ads-marketing
Asset type: internal product-launch announcement image
Input images: Image 1 = overview; Image 2 = detail/workflow;
Image 3 = feature/demo. Preserve their actual visual identity.
Primary request: combine recognizable product screenshots with one concise
message panel for <audience> in <channel>.
Scene/backdrop: <material, surface, or environment>
Subject: <screenshot cards/windows> plus <Slack-style message panel if requested>
Style/medium: <editorial, premium product campaign, technical, playful, etc.>
Composition/framing: <dominant screen, overlap, message-card placement,
negative space, thumbnail hierarchy>
Lighting/mood: <soft studio, matte dark, daylight, restrained shadow>
Color palette: derive from the product references; name 3–5 key colors
Text (verbatim): "<headline>" "<support>" "<proof>" "<CTA>"
Constraints: screenshots recognizable; exact copy legible; no credentials
Avoid: generic SaaS dashboard, unrelated stock imagery, fake product claims,
gibberish, watermark, accidental extra text
```

For a Slack-style card, include only the visual conventions needed: channel
label, avatar/sender, timestamp treatment, message headline, support line,
proof line, and CTA. It should read as an announcement object, not as a claim
that the image is an authenticated Slack screenshot.

### 5. Preserve text and product fidelity

Image models can distort dense interface text. Reduce copy before reducing the
screenshots. Use short exact strings and generous type size. When exact text is
business-critical, create the art-directed collage first and add the final text
as a deterministic overlay in a compositor or HTML/SVG render; keep the
screenshot pixels unchanged.

Never put passwords, API keys, bearer tokens, private URLs, private Slack IDs,
customer data, or secret operational instructions in the image. Redact secrets
from screenshots before using them as references.

### 6. Inspect and iterate

Check the generated output at full size and thumbnail size:

- overview, detail, and feature screenshots remain recognizable;
- the visual hierarchy is clear in under two seconds;
- copy is complete, readable, and not clipped or mirrored;
- the message panel is visually distinct and brand-consistent;
- no screenshot was replaced by unrelated or invented UI;
- claims match the user's supplied facts;
- no credential, private identifier, or sensitive screenshot content appears.

If one defect remains, make one targeted iteration, such as “increase the
message-card copy size; keep all screenshot positions and colors unchanged.”

### 7. Save and report

For project-bound work, copy the final PNG into the project's existing marketing
asset directory, using a versioned sibling filename rather than overwriting an
existing asset. For preview-only work, the generated image may remain in the
default image-generation directory.

Return:

```text
Asset: <absolute path or preview>
Canvas: <width × height>
References: <overview, detail, feature>
Direction: <chosen layout variant>
Copy: <headline / support / proof / CTA>
Validation: <fidelity, legibility, secret-safety>
```

## Design rules

- Let the real interface screenshots carry product specificity.
- Use one dominant focal point, two supporting surfaces, and one message panel.
- Keep the message short enough to read at Slack thumbnail size.
- Derive accents from the product; do not add a fashionable palette arbitrarily.
- Prefer tactile surfaces, measured shadows, and restrained grain over gradients,
  neon, or glassmorphism.
- Use calm asymmetry and generous breathing room; avoid cards nested inside
  cards nested inside cards.
- Keep logos and product names accurate; do not invent partner marks.
- Never imply that an image is a live, authenticated Slack or product session.

## Safety boundaries

- Do not use this skill to expose or distribute secrets.
- Do not screenshot private pages without authorization.
- Do not bypass a password gate or browser login to obtain references.
- Do not include credentials in prompt text, image text, filenames, or metadata.
- Treat screenshots as visual evidence, not proof of security, approval, canon,
  availability, or production readiness unless explicitly established.
- If a requested screenshot or message contains sensitive data, ask for a
  redacted reference or redact it before generation.
