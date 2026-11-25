---
name: ui-style-creator
description: "Create and save a custom visual style from a product brief, existing UI, or references for reuse in one project or across the user's projects. Use for 自定义风格、保存视觉规范、品牌样式复用; not for merely browsing styles or changing an isolated CSS value."
---

# UI Style Creator

Turn the user's taste and product needs into a reusable local style profile. Keep the conversation in the user's language and explain choices using visible outcomes, not design terminology they must learn.

This skill is self-contained. A parent skill may read this file directly; a host may also install this folder as a separate skill. Nested folders are not assumed to be automatically discovered.

## Establish the design

1. Read the product's existing visual guidance, theme files, component library and a representative page. Keep an established design unless the user asked to change it. A custom profile must fit the actual framework and product tasks.
2. Use the user's brief, selected built-in style, or supplied reference as the starting point. Explain the proposed direction with a representative interface, slide or document page in the requested format. Ask only about decisions that materially change the result; infer routine details and state assumptions. If the user already selected a direction, continue without asking them to choose again.
3. Separate observed reference facts from newly proposed rules. A screenshot cannot prove hover, focus, error, loading or mobile behavior. Specify those missing states and verify them in the actual UI when implementation is in scope.
4. Write a concise visual specification and, when exact values are settled, a token file. Follow the [profile format](references/profile-format.md). Preserve real requirements, existing components and interaction semantics; don't replace the product with a style demo.

## Choose the scope and save

- **Project** is the default: `<project>/.ui-styles/profiles/<slug>/`.
- **User** is for an explicit request to reuse a style across projects: `${XDG_CONFIG_HOME:-~/.config}/ui-styles/profiles/<slug>/`.
- User profiles are optional recipes. They do not become defaults for every project or override an existing brand. Before exporting a project design to user scope, remove private content, customer identifiers, credentials and machine-specific paths; keep portable design rules.
- Prefer one relevant profile over a profile for every minor edit. Use a new slug for a deliberate variant. The helper refuses existing targets; when a user asks to update an existing profile, inspect and edit its specific files in place with normal file tools, preserving unrelated content.
- A company style can be stored in the agreed project/shared repository or user profile location. Name its intended audience and scope; do not imply automatic organization-wide distribution. For slides or document forms, retain template, typography, layout and image rules in the specification; app-specific tokens are optional and should not be forced onto another format.

Use `scripts/profiles.py` to save prepared files. Replace the example paths and slug with the actual task's paths. The script validates inputs before writing, supports `--dry-run`, and never invents a color palette.

```sh
python3 <skill-root>/scripts/profiles.py create calm-editorial \
  --scope project --project /path/to/project \
  --design /path/to/prepared-visual-system.md \
  --tokens /path/to/prepared-tokens.json \
  --description "Editorial reading product with clear navigation" \
  --source "User brief and selected reference"

python3 <skill-root>/scripts/profiles.py list \
  --scope project --project /path/to/project

python3 <skill-root>/scripts/profiles.py create calm-editorial \
  --scope user --design /path/to/portable-visual-system.md
```

`--tokens` is optional when the design is still qualitative. Report missing exact values; do not claim such a profile is ready for automatic theme export. The helper only stores the profile. It does not install libraries, activate themes or change agent settings.

## Refine a saved style

When the user requests an upgrade, compare the selected profile/version, active project and requested changes. Keep stable brand rules, revise only the agreed scope, increment `profile.json`'s `version`, and add a short dated change note to `DESIGN.md`. Distinguish a compatible refinement from a deliberate variant that merits a new name. Record any representative validation and untested states.

An ordinary project edit does not automatically revise a personal/company profile. Once a refinement is useful beyond this project, one optional suggestion to incorporate it is enough; do not repeatedly ask. Prior authorization to update the profile is sufficient. Update current-project adoption only when in scope, recording the adopted version, and leave other consumers unchanged. Do not claim a profile was upgraded merely because its active project was edited.

## Apply and carry the design forward

When application is part of the requested work, continue through the parent `ui-styles` workflow if available. If used independently:

1. Adapt the selected profile into the project's existing visual specification, retaining its path. When none exists, use `design/visual-system.md`; use `design/tokens.json` for settled portable token values. A profile is reusable source material; the project files describe the active design.
2. Resolve conflicts against the user's latest explicit requirements and existing project decisions. Copy only the selected rules and tokens, with a source profile name/version, so later edits to a user profile cannot silently change a project.
3. For UI, reuse the installed library's theme API after checking its version and official documentation; token mappings are adapters, not proof of equivalent components. For slides/documents, use the existing template/master/style system and relevant production skill. Record additional styling and unsupported decisions.
4. Within the authorized project work, add or update a short reference in the relevant host's existing instruction file so future UI tasks read the active visual specification before building a demo or choosing a library. Preserve other instructions; do not modify global agent settings as a side effect. Generic Markdown is portable, but automatic loading depends on each host's entrypoint.
5. For implementation work, inspect representative desktop/mobile views and states for UI, or rendered slides/pages for other artifacts. Distinguish a saved specification from an implemented or visually verified design. For a save-only request, stop after the profile is saved and report its path and scope.

When handing off, explain the chosen direction, profile location/scope, active project specification, how to reuse it, and what was actually verified. Keep undecided choices visible without making the user manage a design process.
