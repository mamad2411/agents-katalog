---
name: rcc-rpaframework
description: Use when selecting, authoring, reviewing, or debugging RPA Framework libraries and RPA.* keywords in RCC-managed Robot Framework or Python automation projects.
---

# RCC RPA Framework

## First Inspection

Before recommending a library, inspect `robot.yaml`, its dependency configuration (`conda.yaml`, freeze, or equivalent), imports, environment-variable families, and the required OS/browser/desktop platform. Confirm the project artifact directory and whether it is a maintained legacy Robot Framework robot or a new Python automation.

Check live package metadata or release notes before claiming a package version is current. Let the project’s declared `conda.yaml` or freeze resolve dependencies; do not prescribe a host `pip install` or copy an old pin.

In an implementation or review answer, state the dependency source/configuration and either the live check used for a version claim or that no current-version claim is being made.

## Select By Task

Choose the narrowest library that owns the task. Start with the task map in [references/library-selection.md](references/library-selection.md); it distinguishes RPA Framework libraries, platform needs, and better alternatives.

For an implementation pattern, read [references/task-recipes.md](references/task-recipes.md). Keep imports minimal and write generated files only below the RCC artifact path.

## Operating Rules

- Resolve Python and browser dependencies through the RCC project, then run under RCC. Do not install RPA Framework or browser binaries globally.
- Use `RPA.Tables` for tabular CSV work, `RPA.JSON` for document/schema work, and `RPA.Archive` only with explicit member/path validation. Never extract an untrusted archive without rejecting absolute, `..`, or destination-escaping paths.
- Prefer `RPA.Browser.Playwright` for new browser work when its project requirements fit. Declare project-managed `robotframework-browser` and its required Node.js runtime alongside `rpaframework`; run `rfbrowser init` inside that RCC environment only for the Robot Framework Browser project that needs its engines. It is not a generic RCC or Selenium setup step. Treat old Browser Playwright examples as version-sensitive.
- Use `RPA.RobotLogListener` before calls that receive secrets, and avoid logging secret values, headers, credentials, or vault payloads.
- Keep desktop/OCR automation platform-specific: inspect native dependencies, display/session access, OCR engines, and CI capability before selecting it.
- Keep artifacts bounded to `ROBOT_ARTIFACTS` (or the configured `artifactsDir`) and do not upload a directory or archive until its contents are reviewed.

## Boundary With Modern Robocorp Libraries

Do not combine legacy `RPA.Robocorp.WorkItems`/`RPA.Robocorp.Vault` and modern `robocorp.workitems`/`robocorp.vault` in one execution unless an intentional, tested bridge owns separate lifecycles. Their environment families, adapters, reservation/release behavior, and secret-manager contracts differ. Preserve maintained legacy robots; migrate one robot/process boundary at a time, passing plain data rather than live work-item or vault objects.

Read [references/interoperability-and-safety.md](references/interoperability-and-safety.md) for environment-family compatibility, hosted adapters, logging/redaction, archive safety, browser initialization, and migration boundaries.

## References

- [references/library-selection.md](references/library-selection.md): select a library and verify package/platform needs.
- [references/task-recipes.md](references/task-recipes.md): apply concise RCC-safe Robot Framework patterns.
- [references/interoperability-and-safety.md](references/interoperability-and-safety.md): handle legacy/modern interoperability and safety boundaries.
