---
name: yocto-recipe-maintenance
description: Yocto recipe maintenance skill for AI coding agents. Use for creating, updating, auditing, or reviewing .bb and .bbappend files; package version bumps; dependency, license, PACKAGECONFIG, configure flag, patch, CVE, runtime dependency, package split, and cross-distro packaging comparisons against OpenEmbedded, Alpine, Buildroot, Debian, or upstream sources.
---

# Yocto Recipe Maintenance

## Workflow

1. Identify the target Yocto release, layer, recipe name, version, provider, and image impact.
2. Search local layers and the OpenEmbedded Layer Index before creating new metadata.
3. Compare how OE-Core/meta-openembedded, Alpine, Buildroot, Debian, and upstream package the same software when useful.
4. Inspect upstream source for build system, license files, tags/releases, dependencies, optional features, and patches.
5. Make the smallest metadata change: new recipe, `.bbappend`, version bump, dependency fix, `PACKAGECONFIG`, patch refresh, or package split.
6. Validate with BitBake introspection and a targeted build.

## Maintenance Modes

- **Create recipe**: choose build class, source, `SRCREV`/checksums, license, dependencies, package config, and install behavior.
- **Update recipe**: bump version/source revision, refresh checksums, inspect release notes, review patches, and test reverse dependencies.
- **Audit recipe**: review missing deps, runtime deps, license, QA risks, package splits, bundled libraries, patch freshness, and security issues.
- **Review append**: ensure the append applies only where intended and does not mask upstream behavior broadly.

## References

- [recipe-maintenance-playbook.md](references/recipe-maintenance-playbook.md): create/update/audit workflow and cross-distro checks.

## Guardrails

- Do not create a new recipe if a maintained layer already provides the package and a `.bbappend` is enough.
- Do not guess license metadata; inspect upstream files and use exact `LIC_FILES_CHKSUM`.
- Do not disable features just to make a build pass without explaining product impact.
- Do not install missing host tools globally; model them as native dependencies or disable nonessential generated docs/tests.
