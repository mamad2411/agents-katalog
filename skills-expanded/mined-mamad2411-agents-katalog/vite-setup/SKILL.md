---
name: vite-setup
description: "Configure Vite for the framework and project requirements. Use to add or repair Vite project wiring, including moving an existing webpack or Create React App project to Vite; vite-upgrade changes an existing version and migrate plans multi-step platform transitions beyond the bundler."
---

# vite-setup

Configure Vite for the framework and project requirements.

## Choose this workflow

Use to add or repair Vite project wiring, including moving an existing webpack or Create React App project to Vite; vite-upgrade changes an existing version and migrate plans multi-step platform transitions beyond the bundler.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vite methods](../../references/packs/vite.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; framework, language, project location, deployment shape, and dependency constraints.

**Pack prerequisites:** Project manifests, lockfile, Vite/framework/plugin versions, and existing build scripts. Verify current version-specific documentation when changing configuration. Requested isolated verification may generate disposable build/cache artifacts; inspect their scripts first and preserve product files.

- **Infer from evidence:** Read manifests, lockfile, installed Vite/plugins, entry points, aliases, modes and current build scripts.
- **Reasonable default:** Preserve existing tooling and base-path conventions; in apply mode, make a local focused change when the brief identifies the behavior, and otherwise propose it.
- **Ask only when needed:** Ask if the intended serving subpath or deployment target cannot be inferred and would change generated URLs; do not ask for versions present in the lockfile.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Vite configuration and required scripts/integration; no app redesign or unrelated toolchain replacement.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Inspect the existing setup, package manager, workspace root, framework plugin and Node support.
2. Choose compatible plugins and establish dev, build and preview scripts using project conventions, preserving existing source and entry files.
3. Validate the development, production and subpath paths.

## Technical method

- **Inspect:** Inspect framework, installed Node/Vite/plugin versions, workspace scripts, module format and deployment base path.
- **Method:** Adapt the existing build convention; align dev entry, production output and asset resolution using supported version-specific settings.
- **Avoid misdiagnosis:** Copying a config for another major or adding a second package manager can create a setup that only works on one machine.
- **Check the result:** Verify dev startup, production build and a direct nested route against generated output with the chosen package manager.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vite worked example](../../references/examples/vite.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).

## Decision branches

- **When an existing app already has a bundler or non-root deployment path:** Plan an explicit transition and base-path handling rather than copying a new template over it.

## Deliver and verify

- Working setup with dependency, configuration and script changes, usage, and dev/production/subpath check results.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- The existing app builds; deploying under the requested base path resolves assets correctly.

## Stop and recover

- Do not overwrite an existing project with a template. Respect no-new-dependency constraints and unsupported framework combinations.

## Example requests

- **Normal (apply):** Set up Vite for this existing React app without replacing source files.
- **Edge (apply):** Configure Vite in an existing React workspace served under /dashboard/.
- **Blocked (inspect):** Inspect setup requirements without installing dependencies or overwriting source.
