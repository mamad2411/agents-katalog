---
name: yocto-deploy-flash
description: Yocto deployment and board flashing skill for AI coding agents. Use when locating deploy artifacts, choosing WIC/SDIMG/EXT4/TAR/BMAP/UBI/UBIFS/NAND/NOR/eMMC/SD/QSPI/DFU/TFTP/NFS artifacts, flashing images with bmaptool, dd, fastboot, UUU, STM32CubeProgrammer, U-Boot, vendor tools, or verifying serial boot logs and first-boot behavior.
---

# Yocto Deploy Flash

## Safety First

Flashing can erase disks or boards. Before any write command, require the target device, board model, storage medium, artifact path, and recovery method to be explicit. For removable media, ask the user to confirm the block device after `lsblk`/Disk Management and after unplug/replug comparison.

## Workflow

1. Identify board, SoC, `MACHINE`, boot medium, RAM/storage variant, and vendor flashing tool.
2. Find deploy artifacts with [find_yocto_artifacts.py](scripts/find_yocto_artifacts.py) and the build directory or repository root.
3. Match artifact type to deployment path:
   - `.wic`, `.wic.bz2`, `.wic.gz`, `.wic.zst`, `.sdimg`: whole-disk removable media images.
   - `.bmap`: use with matching `.wic*` through `bmaptool`.
   - `.ext4`, `.tar.*`: partition/rootfs payloads, not usually whole-disk images.
   - `.ubi`, `.ubifs`, `.mtdimg`: raw flash/NAND/NOR workflows.
   - bootloader, DTB, kernel, FIP, TF-A, flash-layout TSV: board/vendor-specific boot flows.
4. Prefer board vendor docs for boot switches, DFU modes, flash layouts, and recovery.
5. Verify boot on serial console. Capture bootloader, kernel, rootfs, network, and application checkpoints.

## References

- [deploy-flash-playbook.md](references/deploy-flash-playbook.md): deployment methods, artifact interpretation, and boot verification.

## Guardrails

- Never guess `/dev/sdX`, `/dev/mmcblkX`, or Windows physical drive numbers.
- Do not flash compressed images directly unless the tool supports the compression.
- Do not assume STM32, NXP, TI, Xilinx, Microchip, Raspberry Pi, or Intel workflows are interchangeable.
- Treat third-party board skills as examples; verify with official vendor and Yocto docs.
