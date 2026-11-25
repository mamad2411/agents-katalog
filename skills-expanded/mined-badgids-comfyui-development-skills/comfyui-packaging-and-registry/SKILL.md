---
name: comfyui-packaging-and-registry
description: Use when creating or editing custom-node package metadata, pyproject configuration, Registry publication, comfy-cli publishing, Manager compatibility, release automation, node-pack scaffolding, or distribution documentation.
metadata:
  version: "00.01.11"
---
# ComfyUI Packaging and Registry

Packaging requirements evolve. Do not hardcode remembered metadata fields.

## Sources

Use current:

- Registry/publishing docs in `Comfy-Org/docs`;
- `Comfy-Org/cookiecutter-comfy-extension`;
- `Comfy-Org/comfy-cli`;
- `Comfy-Org/registry-backend` when backend behavior matters;
- `Comfy-Org/ComfyUI-Manager` for Manager behavior;
- `Comfy-Org/pyisolate` only when packaging/runtime isolation or conflicting extension dependencies are part of the actual target design.

## Current CLI guidance

When publishing or building through `comfy-cli`, inspect the installed/version-matched CLI help and its current bundled skills rather than freezing command flags or build/deploy behavior here. Use CLI skills for the current operational procedure, then verify Registry/package contracts against official docs and the target package.

## Procedure

1. Inspect the existing project's package metadata and release process.
2. Read current official publishing requirements.
3. Compare with the current official scaffold.
4. Make the smallest metadata/build changes required.
5. Validate package build/install in a clean environment where practical.
6. Confirm node import/registration after installation.
7. Run current registry/CLI validation or dry-run tooling if available.
8. Never publish, tag, or push a release unless the user explicitly requested that action.

## Secrets

Do not write Registry tokens/API keys into committed files or logs. Follow the current official secret-management mechanism for the chosen publishing path.

## Compatibility

Registry acceptance does not prove runtime compatibility. Keep package validation and runtime tests as separate gates.

## Acceptance gate

Before calling a package release-ready:

- verify current Registry/Manager/package requirements from official sources;
- keep version and package metadata consistent;
- run build/import/install smoke checks that fit the package;
- confirm no credentials, developer-only paths, caches, or generated junk are in the release artifact;
- check that published node metadata still matches the runtime interface;
- document any publication step that was not actually executed.

