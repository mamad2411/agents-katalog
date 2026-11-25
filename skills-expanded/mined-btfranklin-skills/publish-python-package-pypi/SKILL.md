---
name: publish-python-package-pypi
description: >-
  Configure or troubleshoot PyPI publication for PDM packages with GitHub Actions and Trusted Publishing. Use this skill for the Python package in a mixed-language repository. Do not use it for applications or repositories without a Python distribution. Do not use it for generic CI, containers, or token uploads unless the user requests token uploads.
---

# Publish Python Packages to PyPI

Build a PyPI publication process that follows the package's existing conventions. Include only the required parts. Make each part easy to inspect.

## Workflow

1. Confirm that the repository produces a distributable Python package and uses PDM.
2. Inspect `pyproject.toml` before you propose changes. Identify supported Python versions. Inspect existing workflows, release conventions, and repository instructions.
3. Run `pdm build`. Inspect the wheel and source distribution when the request depends on package contents.
4. Configure publishing around PyPI Trusted Publishing:
   - Trigger publication from the repository's approved release event.
   - Grant `id-token: write` only to the publishing job.
   - Keep ordinary repository permissions read-only.
   - Match the workflow filename, GitHub environment, and PyPI publisher mapping exactly.
5. Keep CI, release-note generation, and package publication separate. Add optional release-note automation only when requested or already established by the repository.
6. For a release to multiple registries, apply the applicable publishing skill to each registry. Derive all package versions from one approved release identity. Complete preflight for every wheel, source distribution, or other package file before any publisher runs.
7. Before publication, validate YAML, package builds, permissions, event semantics, and all manual GitHub and PyPI settings.
8. Apply the authorization rule in Safety Rules before a live release action.
9. If one registry accepts the release and another registry fails, preserve the successful immutable release. Retry only the failed publisher. Use the files that preflight preserved for that registry. Use the exact wheel and source distribution for PyPI. Use the exact tarball for npm. Do not rebuild the files. Do not publish the successful version again.
10. After an authorized release, verify the registry metadata and installation. Identify each external setting or publication result that you could not verify.

## Verify Current Information

Before you change action references, Python matrices, PDM setup, or Trusted Publishing configuration, check current primary documentation and upstream releases. Follow repository pinning or SHA policies when they exist. Otherwise, use supported action references that you verify during the task. Do not state that a fixed reference is current unless you verified it. Record relevant versions or the verification date when they affect the change.

## Safety Rules

- Use PDM for environments, dependency installation, builds, and project commands.
- Do not introduce a long-lived PyPI token unless the user explicitly requires token-based publishing.
- Require explicit authorization to create or push tags, publish releases, configure registry trust, alter repository settings, or perform a live upload. Use authorization already given in the conversation when it covers the action. Ask only for actions outside that scope. Do not treat configuration approval as publication approval.
- Match the project's supported Python versions instead of imposing a global matrix.
- Preserve existing workflow names and conventions unless you must change them to correct the publication process.

## Resources

- Read [references/workflow-templates.md](references/workflow-templates.md) when creating or substantially restructuring GitHub Actions workflows. Adapt the patterns after verifying current action references.

## Output

Include only applicable sections. Keep the report proportional to the scope and results. Report:

1. Existing release coverage and gaps.
2. Workflow changes and the reason for each permission or event.
3. Manual GitHub and PyPI settings. Include required coordination with another package registry.
4. Local validation results. Include anything that you could not verify externally.
5. Authorized next steps, clearly separating configuration from live release actions.
