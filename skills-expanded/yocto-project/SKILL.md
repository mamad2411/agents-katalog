---
name: yocto-project
description: Official-doc-first Yocto Project workflow support for AI coding agents. Use when working with Yocto Project, OpenEmbedded, or Poky repositories; creating or modifying layers, recipes, images, SDKs, BSPs, machine or distro configuration, packagegroups, kernel integration, devtool workflows, builds, troubleshooting, release migration, layer compatibility, or files such as bblayers.conf, local.conf, layer.conf, image recipes, packagegroup recipes, machine .conf files, distro .conf files, kas configs, and oe-init-build-env based workspaces.
---

# Yocto Project

## Core Workflow

1. Identify the target release before giving commands or editing metadata. Inspect branch names, `conf/layer.conf`, `LAYERSERIES_COMPAT`, `bblayers.conf`, `README`, `kas*.yml`, `poky/meta/conf/distro/include/yocto-uninative.inc`, or release tags.
2. Prefer the workspace's own metadata over generic examples. Search existing layers for the same pattern before inventing a new recipe, image feature, class, override, or machine setting.
3. Check official docs for version-sensitive behavior. Use [yocto_doc_router.py](scripts/yocto_doc_router.py) with a topic name for a quick URL map, then open the relevant docs.
4. Make the smallest layer-local change that fits Yocto conventions. Avoid editing `poky/` or upstream layers unless the user explicitly asks for an upstream patch.
5. Validate with BitBake-native tools whenever available: `bitbake-layers`, `bitbake -e`, `bitbake -c listtasks`, `bitbake -c cleansstate`, `devtool`, `oe-pkgdata-util`, or the existing project build wrapper.

## Source Priority

Use official sources first:

- Local workspace metadata and build configuration.
- Yocto Project docs: `https://docs.yoctoproject.org/`
- BitBake manual: `https://docs.yoctoproject.org/bitbake/`
- Yocto source: `https://git.yoctoproject.org/`
- OpenEmbedded source: `https://git.openembedded.org/`
- OpenEmbedded Layer Index: `https://layers.openembedded.org/`

If the user asks for "latest", "current", "supported", "LTS", package versions, release notes, migration rules, or security status, verify online before answering.

## Task Routing

- For recipe syntax, tasks, overrides, fetchers, signatures, or `.bbappend` mechanics, use `$bitbake-metadata` as the primary skill and return here for Yocto workflow context.
- For layers, images, SDKs, BSPs, distro/machine policy, build setup, package selection, or migration planning, stay in this skill.
- For kernel recipe and device-tree work, inspect existing machine and kernel metadata first, then read the kernel development sections from the official docs.

## References

Read only the reference file needed for the task:

- [official-sources.md](references/official-sources.md): source list, docs version notes, release/branch selection rules.
- [workflows.md](references/workflows.md): practical workflows for layers, images, SDKs, BSPs, packages, and troubleshooting.

## Guardrails

- Do not assume a variable, class, package manager, init system, or override syntax is valid for every Yocto release.
- Do not use random blog snippets as authority when official docs or source metadata answer the question.
- Do not add broad config changes to `local.conf` when a layer, recipe, image, distro, or machine file is the durable location.
- Do not paper over build failures with `INSANE_SKIP`, `BBMASK`, `COMPATIBLE_MACHINE`, or task disabling unless the reason is documented and locally appropriate.
- Prefer `.bbappend` in the product layer over copying whole upstream recipes.
