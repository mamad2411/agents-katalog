---
name: publish-npm-package
description: >-
  Configure or troubleshoot npm package publication with GitHub Actions and npm Trusted Publishing. Use this skill for JavaScript or TypeScript packages. Also use it for the npm package in a mixed-language repository. Do not use it for applications or repositories without an npm package. Do not use it for generic CI, containers, or token publishing unless the user requests token publishing.
---

# Publish npm Packages

Build an npm publication process that follows the package's existing conventions. Include only the required parts. Make each part easy to inspect.

## Workflow

1. Confirm that the repository produces a publishable npm package and identify the exact workspace or package directory.
2. Inspect `package.json` and the repository's lockfile before you propose changes. Identify the package manager and supported Node.js versions. Inspect exports, included files, repository metadata, release conventions, workflows, and repository instructions.
3. Run the repository's normal validation and build commands. Create the exact tarball with `npm pack`. Inspect its manifest and contents. Test an isolated installation when the request depends on package contents or type declarations.
4. Configure npm Trusted Publishing around the repository's approved release event:
   - Use a supported hosted runner and a compatible Node.js and npm pair.
   - Grant `id-token: write` only to the publishing job.
   - Keep ordinary repository permissions read-only.
   - Match the npm package, GitHub owner and repository, workflow filename, environment, and allowed publish action exactly.
   - Publish the exact validated tarball. Do not rebuild it in the publishing job.
   - Use Trusted Publishing's automatic provenance for eligible public packages. Disable it only when the repository documents a specific reason.
5. For a first publication, use this bootstrap sequence:
   - Determine whether the package name already exists.
   - Determine whether npm permits Trusted Publishing configuration before the first publication.
   - If the first publication needs authentication, validate the exact tarball.
   - Apply the authorization rule in Safety Rules before the first publication.
6. For a release to multiple registries, apply the applicable publishing skill to each registry. Derive all package versions from one approved release identity. Complete preflight for every package file before any publisher runs.
7. Before publication, validate YAML, package metadata, archive contents, permissions, event semantics, and all manual GitHub and npm settings.
8. If one registry accepts the release and another registry fails, preserve the successful immutable release. Retry only the failed publisher. Use the files that preflight preserved for that registry. Use the exact tarball for npm. Use the exact wheel and source distribution for PyPI. Do not rebuild the files. Do not publish the successful version again.
9. After an authorized release, verify registry metadata, expected provenance, and a clean installation. Identify each external setting or publication result that you could not verify.

## Verify Current Information

Check current primary documentation before you change action references, Node.js matrices, or npm requirements. Also check it before you change Trusted Publishing, provenance, or staged-publishing settings. Check applicable upstream releases. Follow repository pinning or SHA policies when they exist. Otherwise, use supported action references that you verify during the task. Do not state that a fixed reference is current unless you verified it. Record relevant versions or the verification date when they affect the change.

## Safety Rules

- Respect the repository's package manager for dependency installation and validation. Use the npm CLI for npm registry operations that require it.
- Do not introduce a long-lived npm publish token unless the user explicitly requires token-based publishing. Keep any token needed to install private dependencies read-only and separate from publication.
- Require explicit authorization to create or push tags, publish a release, configure registry trust, alter repository settings, bootstrap a package, or perform a live upload. Use authorization already given in the conversation when it covers the action. Ask only for actions outside that scope. Do not treat configuration approval as publication approval.
- Treat package names and versions as immutable registry coordinates. Recheck name availability immediately before a first publication. Do not try to overwrite an existing version.
- Inspect lifecycle scripts and the tarball before publication. `npm pack` and `npm publish` can execute package scripts.
- Scope workspace commands to the intended package. Do not assume trust-management commands understand npm workspaces.
- Preserve existing workflow names and release conventions unless changing them is necessary to make the publishing identity correct.

## Resources

- Read [references/workflow-templates.md](references/workflow-templates.md) when you create or substantially change a GitHub Actions workflow. Also read it when you configure a trusted publisher or handle an initial package bootstrap. Read it when you coordinate npm with another registry. Adapt the patterns after you verify current primary documentation and action references.

## Output

Include only applicable sections. Keep the report proportional to the scope and results. Report:

1. Existing npm release coverage and gaps.
2. Workflow changes and the reason for each permission or event.
3. Manual GitHub and npm settings, including whether an initial bootstrap remains.
4. Package and tarball validation results. Include anything that you could not verify externally.
5. Coordination with each other registry in the release.
6. Authorized next steps, clearly separating configuration from live release actions.
