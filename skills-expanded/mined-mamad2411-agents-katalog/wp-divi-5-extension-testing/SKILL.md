---
name: wp-divi-5-extension-testing
description: Designs and runs structural, JavaScript, PHP, metadata, rendering, conversion, build, package, install, and compatibility checks for Divi 5 extensions. Use before release, after a Divi update, or when editor and frontend behavior diverge.
---

# wp-divi-5-extension-testing

Use this skill to create a test plan, repair tests, validate a package, or reproduce a compatibility failure.

## Required Inputs

- Exact runtime and toolchain versions.
- Extension root and package manifests.
- Module inventory and module types.
- Supported WordPress/Divi/PHP range.
- Build and package commands.
- Dynamic data, permissions, and external services.
- Divi 4 conversion scope.
- Known defects or review findings.

## Inspector

Run the read-only inspector with `--help` first:

```powershell
python .agents/plugins/wp-divi-5-extension-development/skills/wp-divi-5-extension-testing/scripts/inspect-divi-extension.py --help
```

Then inspect the target extension:

```powershell
python .agents/plugins/wp-divi-5-extension-development/skills/wp-divi-5-extension-testing/scripts/inspect-divi-extension.py --path .
```

Use `--json` for machine-readable output.

## Workflow

Use [`workflows/validate-divi-extension-workflow.md`](workflows/validate-divi-extension-workflow.md).

## Resource

Use [`resources/extension-test-matrix.md`](resources/extension-test-matrix.md).

## Completion Evidence

Record versions, commands, inspector results, test results, build output, package contents, clean-install result, editor/frontend parity, conversion evidence, known gaps, and release blockers.
