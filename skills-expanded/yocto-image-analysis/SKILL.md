---
name: yocto-image-analysis
description: Yocto image analysis skill for AI coding agents. Use to explain why a package is in an image, estimate image size impact, compare manifests, inspect package data, analyze dependencies, answer what-if package changes, reduce image footprint, inspect buildhistory, or use oe-pkgdata-util, bitbake -g, image manifests, license manifests, and installed package lists.
---

# Yocto Image Analysis

## Workflow

1. Identify image recipe, `MACHINE`, `DISTRO`, package format, and actual deploy directory.
2. Collect image manifests, package data, dependency graphs, and buildhistory when available.
3. Trace inclusion from image recipe, packagegroups, features, runtime dependencies, recommends, and distro/machine policy.
4. Estimate "what-if" changes by checking dependency chains before editing metadata.
5. Route recipe changes to `$yocto-recipe-maintenance` and build failures to `$yocto-build-debug`.

## Commands

```sh
oe-pkgdata-util list-pkgs
oe-pkgdata-util find-path <path>
oe-pkgdata-util lookup-recipe <pkg>
oe-pkgdata-util list-pkg-files <pkg>
bitbake -g <image>
bitbake -e <image>
```

Use [find_image_package_refs.py](scripts/find_image_package_refs.py) with a build/repo path and package name for a quick text scan across manifests, package data, and dependency graph files.

## References

- [image-analysis-playbook.md](references/image-analysis-playbook.md): why/what-if/image-size workflows.

## Guardrails

- Do not assume a package is directly listed in `IMAGE_INSTALL`; it may arrive through packagegroups, recommends, shlib deps, or image features.
- Do not remove packages from an image without checking runtime dependencies and service impact.
- Do not optimize size blindly; preserve required update, debug, recovery, and compliance artifacts.
