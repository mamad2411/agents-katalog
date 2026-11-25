---
name: yocto-kernel-bsp
description: Official-doc-first Yocto kernel and BSP workflow support for AI coding agents. Use when working on Linux kernel recipes, linux-yocto, vendor kernel integration, defconfig, kernel config fragments, device tree files, KERNEL_DEVICETREE, MACHINE configuration, BSP layers, bootloader/kernel handoff issues, COMPATIBLE_MACHINE, kernel modules, or board bring-up problems in Yocto Project and OpenEmbedded workspaces.
---

# Yocto Kernel BSP

## Core Workflow

1. Identify the Yocto release, `MACHINE`, BSP layer, kernel provider, and kernel recipe before editing.
2. Inspect existing machine configuration, kernel recipe, `.bbappend`, device tree, defconfig, and config fragments.
3. Prefer the product BSP layer for local changes. Avoid editing upstream `poky`, `meta`, `meta-yocto`, OE-Core, or vendor layers unless preparing an upstreamable patch.
4. Separate concerns:
   - Machine selection belongs in `conf/machine/*.conf`.
   - Kernel source/provider policy belongs in distro or machine config only when locally justified.
   - Kernel config belongs in fragments or defconfig according to the project's existing style.
   - Device tree changes belong near existing DTS/DTSI structure or in a layer-local patch.
5. Validate with BitBake and kernel tasks before claiming success.

## Commands

```sh
bitbake-layers show-recipes virtual/kernel
bitbake-layers show-appends
bitbake -e virtual/kernel
bitbake virtual/kernel
bitbake -c menuconfig virtual/kernel
bitbake -c diffconfig virtual/kernel
bitbake -c deploy virtual/kernel
```

Use [yocto_kernel_doc_router.py](scripts/yocto_kernel_doc_router.py) with a topic name for official documentation links.

## References

- [kernel-bsp-workflows.md](references/kernel-bsp-workflows.md): provider discovery, recipe/appends, fragments, and validation.
- [device-tree-checklist.md](references/device-tree-checklist.md): DTB selection, DTS/DTSI origin, patch workflow, and deploy checks.
- [machine-config-checklist.md](references/machine-config-checklist.md): machine variables, provider policy, overrides, and board variants.

## Guardrails

- Do not assume `linux-yocto` behavior applies to vendor kernels without checking the recipe/classes.
- Do not mix board variants that have different RAM, boot media, storage, or DTBs.
- Do not change `PREFERRED_PROVIDER_virtual/kernel`, `KERNEL_DEVICETREE`, or `COMPATIBLE_MACHINE` globally unless the blast radius is understood.
- Do not hand-edit generated kernel build output as a permanent fix; add patches, fragments, or metadata in the owning layer.
