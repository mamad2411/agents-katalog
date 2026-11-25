---
name: sdk-bsp-memory-partition
description: DDR memory and FLASH partition planning and customization for AX637/AX637R (ONLY_NAND/ONLY_eMMC) and M57 (NOR+NAND). Covers Linux/CMM memory sizing, partition tables, AB constraints, alignment, image packaging, and AXDL/OTA verification. Use for partition-layout, memory-reservation, or rootfs-size questions on these platforms.
metadata:
  version: 1.0.1
  author: SDK Team
  tags: [ax637, m57, memory, cmm, partition, nand, emmc, axdl]
  data-classification: public
---

# Memory and Partition Guide

## Purpose

Guide SDK users through DDR memory allocation and FLASH partition changes for:
- **AX637/AX637R**: ONLY_NAND / ONLY_eMMC configurations, AB constraints, custom ACore partitions
- **M57**: NOR+NAND dual-flash, Inline ECC, NAND adaptation and mtd scan tuning

Preserves boot-chain, A/B, NAND bad-block, and image-packaging constraints.

## When to use

Use when:
- changing Linux or CMM memory size/address;
- resizing, adding, removing, or auditing `partitions.json` or mtdparts partitions;
- extending `rootfs`, comparing ONLY_NAND/ONLY_eMMC/NOR+NAND layouts, or checking AB behavior;
- diagnosing a partition mismatch after AXDL or OTA packaging;
- tuning M57 NAND mtd scan parameters or Flash controller settings.

Do not use for unrelated SoCs, generic Linux partitioning, or application heap allocation. Route whole SDK compilation issues to the SDK build skill and peripheral-specific memory usage to the relevant module skill.

## Routing

1. If args includes `platform=<id>`, use it directly; otherwise match this skill's `routing.yaml` against the current workspace.
2. Report the detected platform (`display` name and source) in one sentence so the user can correct a mistaken match.
3. If no platform matches, execute `fallback: ask`: report that the platform is unknown, ask for the chip/board and SDK, and end the turn. If the user requests output files, write the clarification and the unknown platform result there before ending. Load platform documents after the platform is identified.
4. Load `platforms/<id>.md` for platform-specific paths, baseline values, partition constraints, verification details, and the reference documentation table.
5. Reference documents are listed in the "参考文档" section of `platforms/<id>.md`; read them directly from their listed paths.

## Instructions

For read-only consultation, answer the requested question with the relevant facts and commands. Read references only as needed; after writing the requested answer files, end the turn.

1. **Collect the target first.** Confirm chip/board (e.g., `ax637_demo`, `ax637r_demo`, `demo_nor_nand`), FLASH type (`only_nand`, `only_emmc`, or `NOR+NAND`), AB/non-AB mode, SDK checkout, target partition(s), desired size, and whether the output will be flashed with AXDL or delivered through OTA. Treat the selected platform file's values as documented demo baselines; inspect the selected platform files before changing them.

2. **Validate DDR ownership.** Use the selected platform file for the documented Linux/CMM baseline and paths. Keep Linux and CMM ranges non-overlapping, account for ATF/OPTEE and image-loading reservations, and verify boot logs plus `/proc/meminfo`/CMM module state on the target.

3. **Change Linux memory.** 
   - **AX637/AX637R**: Edit `config.mk` LINUX_MEMORY_SZ (compiled into U-Boot; the DTS has no static `memory` node — it is generated at boot by U-Boot `ft_system_fixup_memory`), rebuild U-Boot and the image, then verify the deployed DTB and Linux-reported memory. Alternatively set the U-Boot env variable `linux_mem` at runtime.
   - **M57**: Edit `config.mk` SYSTEM_MEMORY_SZ and LINUX_MEMORY_SZ, or adjust via uboot command line. For Inline ECC configurations, also update `ddrmc_init.h` INLINE_ECC_BLOCK_1_START.

4. **Change CMM memory.**
   - **AX637/AX637R**: Edit `load_modules.sh` under the platform build tree's initialization directory, rebuild and package `rootfs.img`, and flash it through AXDL. On a writable target inspect the installed script; changes to a read-only filesystem require rebuilding the image.
   - **M57**: Edit `config.mk` or use uboot command line.
   Keep CMM start/size consistent with the DDR map and Linux reservation.

5. **Read the partition source of truth.** Parse the selected platform's `partitions*.json` or mtdparts; use its order and units to calculate cumulative sizes. Do not infer offsets from screenshots. Distinguish ONLY_NAND metadata handling from ONLY_eMMC GPT handling and NOR+NAND fixed-order layouts; preserve the documented AB boot-chain layout.

6. **Resize safely.** Edit the non-AB or matching AB variant as appropriate. Keep `size` aligned to the actual NAND block size (M57: NOR 4K / NAND 256K; AX637: NAND 256K / eMMC constraints), preserve bad-block allowance and hsm attachment, and maintain image/filesystem fit. Do not casually change BootROM-dependent AB SBL sizes or MCU boot partitions.

7. **Respect partition ownership.** Boot-chain partitions must remain in their supported order. For M57 partition creation/deletion is not currently supported. For AX637 custom ACore partitions, update U-Boot's `main_part_id[]`; if a custom partition carries an image, update the image-packaging helper paths (`axp_make.sh`) for every affected `PLAT`.

8. **Propagate and verify.** Regenerate partition metadata/image packages and ensure generated mtdparts/XML/GPT agrees with U-Boot definitions before flashing. For AXDL use repartition only when intentionally rewriting the partition table and avoid full erase when persistent environment data must survive. For OTA keep XML data synchronized and review `ota_repartition` behavior. Verify names/sizes, mountability, available space, and the expected A/B slot after boot.

9. **Diagnose failures by evidence.** Capture the selected platform, source JSON, generated XML/mtdparts, AXDL/OTA package version, complete serial log, and `/proc/mtd`/block-device layout. Compare order/size/alignment, SBL sizing, stale metadata/GPT, and XML/U-Boot definitions before recommending reflashing.

## Safety

- Partition edits can make the board unbootable and can destroy data. Back up the original JSON, generated package, and persistent data before mutation; show the exact diff and obtain confirmation before flashing a changed layout.
- Never shrink a partition below its image plus filesystem overhead, NAND bad-block reserve, or required alignment. A larger `rootfs` also requires a matching filesystem/image size.
- Do not change AB SBL sizes or MCU boot partitions casually; BootROM offsets and the safety boot chain depend on them.
- Treat demo values as examples. Confirm actual DDR size, NAND block geometry, eMMC GPT layout, and SDK version in the target checkout.
