---
name: wp-divi-5-child-theme-setup
description: Scaffolds and validates Divi 5 child themes. Use when creating or repairing style.css metadata, functions.php, asset loading, file organization, translations, and child-theme-aware paths.
---

# Divi 5 Child-Theme Setup

## Before Starting

- Confirm planning selected a child theme.
- Record exact Divi, WordPress, and PHP versions.
- Work in version control and a development or staging environment.
- Never modify the installed Divi parent.

## Minimal Structure

```text
project-divi-child/
├── style.css
├── functions.php
├── screenshot.png          # optional
├── assets/                 # optional
│   ├── css/
│   ├── js/
│   └── images/
├── inc/                    # optional theme-coupled PHP
├── languages/              # optional translations
└── templates or parent-relative PHP paths only when overrides are justified
```

Use [minimal-divi-child-theme.md](examples/minimal-divi-child-theme.md) as a starting pattern, not as site-specific finished code.

## Setup Rules

- `style.css` is required and must include `Template: Divi` exactly.
- Use a unique theme slug and matching text domain.
- Do not copy the parent `functions.php`; both child and parent functions files load.
- Prefix or namespace PHP symbols and asset handles.
- Inspect the installed Divi enqueue behavior before adding parent styles.
- Load CSS and JavaScript with WordPress enqueue APIs on appropriate hooks.
- Use `get_theme_file_path()` and `get_theme_file_uri()` for child-first lookup with parent fallback.
- Use parent-specific helpers only when deliberate.
- Keep environment configuration and secrets outside the theme.
- Add build output only when it is reproducible and required at runtime.

## Inspector

Run with `--help` first:

```powershell
$Inspector = ".agents/plugins/wp-divi-5-child-theme-development/skills/wp-divi-5-child-theme-setup/scripts/inspect-divi-child-theme.py"
python $Inspector --help
```

The inspector checks metadata and inventories PHP/template relationships. It does not replace PHP linting, WordPress runtime tests, or manual review.

## Workflow

Use [scaffold-divi-child-theme-workflow.md](workflows/scaffold-divi-child-theme-workflow.md) and finish with [child-theme-structure-checklist.md](resources/child-theme-structure-checklist.md).
