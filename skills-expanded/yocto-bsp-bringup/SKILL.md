---
name: yocto-bsp-bringup
description: Yocto BSP and board bring-up skill for AI coding agents. Use for vendor BSP import, machine configuration, layer dependencies, bootloader recipes, trusted firmware, U-Boot, Linux kernel recipes, device trees, defconfigs, KERNEL_DEVICETREE, COMPATIBLE_MACHINE, virtual/kernel providers, storage variants, serial console, first boot, and hardware enablement.
---

# Yocto BSP Bring-Up

## Workflow

1. Identify board, SoC, BSP vendor, Yocto release, kernel version, boot chain, storage medium, and RAM/storage variant.
2. Inspect layer structure, `conf/layer.conf`, `conf/machine/*.conf`, and `LAYERSERIES_COMPAT`.
3. Confirm collection names with `BBFILE_COLLECTIONS`; use collection names in `LAYERDEPENDS`.
4. Identify providers for `virtual/kernel`, bootloader, trusted firmware, OP-TEE, firmware blobs, and image recipes.
5. Trace device tree and kernel config from machine config through recipe appends.
6. Keep board-specific fixes in the BSP/product layer.

## References

- [bsp-playbook.md](references/bsp-playbook.md): machine, kernel, bootloader, DTB, and vendor BSP workflows.

## Guardrails

- Do not mix machine names across RAM/storage variants.
- Do not copy full vendor recipes when a `.bbappend` or config fragment is enough.
- Do not assume a layer directory name is the layer collection name.
- Do not change bootloader/kernel provider policy without checking all machines in the layer.
