---
name: skill-icon-workflow
description: >-
  Create, update, or validate Codex skill icons. Use this skill for the small SVG, the 100x100 PNG, and the icon fields in `agents/openai.yaml`. Do not use it for app icons, favicons, badges, unrelated artwork, or skill work that does not include an icon.
---

# Skill Icon Workflow

Use this skill for the icon part of skill creation or maintenance. Also use `skill-creator` when the task changes skill instructions or other metadata.

## Workflow

1. Read [references/icon-workflow.md](references/icon-workflow.md) for the asset and validation contract.
2. Inspect the existing skill assets and `agents/openai.yaml`. Preserve the established visual identity when you repair or convert icons.
3. Keep the editable design source and `icon_small` as SVG. Export `icon_large` from that source as a 100x100 PNG.
4. Store both files in the target skill's `assets/` directory. Use paths that are relative to the skill directory.
5. Validate SVG structure, PNG format and dimensions, YAML syntax, file existence, and rendered appearance at small size.
6. Limit metadata changes to icon fields unless the broader task explicitly includes metadata maintenance.

Use `imagegen` when the request requires new artwork or visual concepts. Do not use it only to convert files or update icon paths.

## Verify Current Information

Before you change Codex metadata conventions, verify the current official skill-authoring guidance that is available in the environment. Record the convention or source when it changes the implementation. Do not treat an old local example as permanently authoritative.

## Design Rules

- Use a full-bleed background unless transparency is intentional.
- Use simple silhouettes and strong contrast. Avoid details that disappear at small sizes.
- Preserve gradients and alpha through export.
- Never accept file extension alone as proof of format or dimensions.

## Output

Report the files that you created or changed. Report the metadata paths, structural checks, image dimensions, and visual inspection result.
