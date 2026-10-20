---
name: vite-assets
description: "Fix asset paths, public files, base paths, and deployment paths. Use for missing assets or wrong emitted URLs; vercel-routing handles platform rewrites."
---

# vite-assets

Fix asset paths, public files, base paths, and deployment paths.

## Choose this workflow

Use for missing assets or wrong emitted URLs; vercel-routing handles platform rewrites.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vite methods](../../references/packs/vite.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; broken asset URLs, deployment base path, source assets, and target routes.

**Pack prerequisites:** Project manifests, lockfile, Vite/framework/plugin versions, and existing build scripts. Verify current version-specific documentation when changing configuration. Requested isolated verification may generate disposable build/cache artifacts; inspect their scripts first and preserve product files.

- **Infer from evidence:** Read manifests, lockfile, installed Vite/plugins, entry points, aliases, modes and current build scripts.
- **Reasonable default:** Preserve existing tooling and base-path conventions; in apply mode, make a local focused change when the brief identifies the behavior, and otherwise propose it.
- **Ask only when needed:** Ask if the intended serving subpath or deployment target cannot be inferred and would change generated URLs; do not ask for versions present in the lockfile.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Imported/public assets, URL construction, and base-path handling; no asset redesign.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Resolve the actual mode, root, base path and deployment routing. Trace each failing URL from an imported asset, public file, CSS reference or runtime string to emitted output; compare dev and production behavior.
2. Repair the owning URL construction using supported installed-version semantics. Keep case-sensitive paths, hashed output and assets consumed by lazy routes distinct; do not fix every route with an unconditional root-relative path.
3. Verify root navigation, direct nested navigation, configured subpath base and refresh in a production preview. Check response status and content type: a fallback HTML page with status 200 is still a broken image or module.

## Technical method

- **Inspect:** Trace imported assets, public files, CSS URLs and runtime-generated paths through base and nested routes.
- **Method:** Use the correct asset mechanism for build-time imports versus runtime names; inspect emitted URLs under the deployed base.
- **Avoid misdiagnosis:** A leading slash can escape a subpath deployment; a concatenated filename may never enter the build graph.
- **Check the result:** Check direct nested loads, fonts, CSS images and dynamic assets in production output, not only the dev server.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vite worked example](../../references/examples/vite.md).
- Creating, editing or reviewing frontend UI, copy, states or visual assets: [Frontend iconography](../../references/frontend-icons.md).

## Decision branches

- **When runtime concatenation prevents static asset discovery:** Use an explicit asset map or supported URL/import pattern appropriate to the installed version.

## Deliver and verify

- Asset-path patch and production-build/browser verification.
- Source-to-output mapping and root/subpath/nested-route results.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Emitted asset URLs resolve under the requested base and nested routes, with correct content types and no reliance on navigation from the root.

## Stop and recover

- Do not hard-code a development origin or copy secret files into public output. Missing deployment evidence is stated separately.

## Example requests

- **Normal (apply):** Fix images that work locally but fail when hosted under a subpath.
- **Edge (apply):** Fix a font referenced from CSS that returns 404 once the app is served under /app/.
- **Blocked (inspect):** Inspect source paths without deployment access; separate build evidence from live serving.
