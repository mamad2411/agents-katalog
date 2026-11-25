---
name: brand-studio
description: Configure and apply a persistent brand identity across PowerPoint, Word, SVG logos, HTML, PDF, PNG, and social media assets. Use when the user asks to set up brand guidelines, apply brand colors or typography, create branded content, generate logo variants, or check brand consistency. Do not use for unbranded artifacts or presentation storytelling that does not require a brand system.
---

# Brand Studio

Use one active brand configuration as the source of truth, load only the
reference needed for the requested artifact, and verify the final output against
that configuration.

## Resolve the active configuration

Check these locations in order:

1. `${CLAUDE_PROJECT_DIR}/.brand-studio/brand-config.md` for a project-specific brand.
2. `${CLAUDE_PLUGIN_DATA}/brand-config.md` for the personal default.

Use the project config when both exist. Do not write user configuration into
`${CLAUDE_PLUGIN_ROOT}`; installed plugin files are versioned and may be
replaced during an update.

If neither config exists, run the setup flow before producing a branded asset.

## Configure a brand

1. Ask whether the configuration is project-specific or the personal default.
2. Collect the brand name, optional tagline, industry, and personality.
3. Collect primary, secondary, accent, background, and text colors. Request hex
   codes or propose accessible values for confirmation.
4. Collect heading and body fonts, fallbacks, logo assets or direction, tone,
   preferred phrases, and prohibited language.
5. Summarize the proposed system and resolve missing or conflicting choices.
6. Read [the configuration template](references/brand-config-template.md).
7. Write the confirmed config to the selected persistent location.
8. Continue with the user's original asset request.

When updating a config, preserve unspecified values and show the proposed
changes before writing.

## Route the request

Read only the relevant reference:

| Request | Reference |
|---|---|
| PowerPoint or slide branding | [PowerPoint branding](references/ppt-branding.md) |
| Word document or report branding | [Document branding](references/doc-branding.md) |
| Logo concepts or SVG variants | [Logo creation](references/logo-creator.md) |
| Website, HTML, email, or design tokens | [Web branding](references/web-branding.md) |
| Social banners, cards, or channel kits | [Social templates](references/social-media-templates.md) |

If the output type is unclear, ask one focused question before loading a
reference.

## Apply the brand

- Use exact configured values; do not invent replacement colors, fonts, logos,
  or voice rules.
- Treat an explicit instruction in the current request as an override. Flag the
  difference and ask whether to persist it when it appears intentional.
- Preserve the source artifact's content unless the user also requests content
  editing.
- Use available artifact-specific tools and preserve editability when the target
  format supports it.
- Do not claim a font, logo, contrast ratio, or layout was applied unless the
  resulting artifact was inspected.

## Verify the output

Before delivery:

1. Compare colors, typography, logo placement, and tone with the active config.
2. Check legibility, contrast, clipping, overflow, and missing assets.
3. Render or preview the artifact when possible.
4. Report any substitution or unsupported brand feature explicitly.
5. Name the configuration scope used without exposing unrelated local paths.

The Brand Guard hook reinforces this workflow for common branded file types. It
adds guidance only; it never auto-approves or blocks a tool call.
