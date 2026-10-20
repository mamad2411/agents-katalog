---
name: wp-playground-blueprints
description: Authors, reviews, validates, and troubleshoots WordPress Playground Blueprint JSON for deterministic demos, tests, snapshots, and local environments.
---

# WordPress Playground Blueprints

Use this skill when creating or reviewing Blueprint JSON, selecting steps/resources, loading plugins/themes/content, or debugging setup failures.

## Required inputs

- Intended context: local, CI, demo, PR preview, or reproduction.
- WordPress/PHP versions.
- Plugin/theme sources and build status.
- Required fixtures, options, users, content, and landing page.
- Whether local adjacent files or public URLs are allowed.
- Reproducibility and security requirements.

## Procedure

1. Start with the smallest Blueprint that proves the scenario.
2. Add the official `$schema`.
3. Pin `preferredVersions` for CI, demos, and reproductions.
4. Prefer declarative shorthands/steps over arbitrary PHP when they cover the requirement.
5. Review every remote resource and executable step.
6. Use synthetic fixtures and test-only credentials.
7. Validate JSON and run the included scanner.
8. Execute in a disposable environment.
9. Verify installed/activated components, versions, content, options, user state, and landing page.
10. Preserve the exact Blueprint with failure evidence.

## Workflow

Use `workflows/author-and-validate-blueprint-workflow.md`.

## Resources and examples

- `resources/blueprint-review-checklist.md`
- `examples/blueprint-examples.md`

## Script

```powershell
python .\.agents\plugins\wp-playground\skills\wp-playground-blueprints\scripts\validate-playground-blueprint.py --help
```

The script is a conservative static scanner. It does not fetch the official JSON Schema, execute code, or validate remote artifacts.
