---
name: sdk-bsp-nand-fs
description: Axera SoC NAND 与文件系统问题分析入口，覆盖 M57 Linux/QNX 以及 AX637/AX637R Linux 主域的 flash scan、NAND/MTD 适配、坏块/ECC、分区、烧录、挂载和性能排障；按工作区路由到 M57 或 AX637。
metadata:
  author: Axera BSP Team
  tags: [axera, bsp, nand, flash, mtd, ubifs, jffs2, yaffs, qnx, linux, ax637, ax637r]
  data-classification: public
---

# Axera NAND and Filesystem

## When to use

- 识别或适配 NAND/Flash，分析 flash scan、geometry、ECC、坏块和线模式问题。
- 排查 Linux MTD/UBI/UBIFS/JFFS2/YAFFS 的读写、挂载、性能和启动问题；M57 另覆盖 QNX `ax_mtd`/`mtdpart`/`etfs`。
- 分析 AXDL/FDL、镜像打包、分区元数据与设备实际布局不一致导致的烧录或启动失败。
- 需要收集串口日志、内核日志、分区信息、Flash ID、文件系统状态并形成复现与验证路径。

不用于普通 block device、与 NAND 无关的文件系统问题、通用 SDK 编译问题或未经目标平台确认的烧录操作。

## Routing

1. 若 args 传入 `platform=<id>`，直接使用；否则按 `routing.yaml` 从上到下检测工作区。具体 board/SDK 条目必须排在通用架构条目前面。
2. 命中平台后，先加载 `platforms/<id>.md`，再按其中的 reference 路由读取资料。M57 通过环境差异区分 Linux/QNX；AX637/AX637R 仅按当前仓库的 Linux 主域与 Safety/RTOS 启动链分析。
3. 以一句话报告识别到的平台、环境和命中路径，便于用户纠正误判。M57 可按 Linux/QNX 区分；AX637/AX637R 仅按当前仓库的 Linux 主域与 Safety/RTOS 启动链分析。
4. 无匹配时执行 `fallback: ask`；未确认平台、启动介质、Flash 型号和环境前，不修改分区、配置或烧录参数。

## Platform and environment confirmation

开始执行修改、擦写或烧录前，一次收集：芯片/板型、SDK revision、`PLAT`、启动介质与 NAND 型号、容量/页大小/块大小、目标运行环境、AB/non-AB、目标分区、当前问题现象和完整日志。只做只读分析时，仍需标明缺失证据。

## Source locations

- Linux：`kernel/linux/`、`kernel/osdrv/`、`build/platforms/axera/*/partitions*.json`、`build/scripts/`、`tools/mk*fs/`。
- M57 QNX/Safety：`SafetyIsland/sbl/`、`SafetyIsland/mcal/`、`SafetyIsland/rt-thread/` 及对应构建配置。AX637 的 Safety/RTOS 仅作为启动链和 Flash 适配证据，不按 QNX 文件系统分析。
- Boot/打包：`boot/uboot/`、`build/scripts/` 和目标平台的镜像/分区配置。
- 参考文档路由：`reference/m57/_index.md`、`reference/ax637/_index.md`。

## Core knowledge

- 先确认真实 Flash geometry、控制器模式、ECC/坏块策略和分区来源，再解释 scan、读写或挂载失败。
- 区分 raw MTD、MTD block、UBI volume、文件系统挂载点与 QNX ETFS/裸分区语义；不得用一个环境的命令或设备节点替代另一个环境的证据。
- 烧录、分区和文件系统验证必须同时对照镜像包/元数据、Bootloader 定义与系统启动后的实际布局。
- 性能结论必须带环境、访问层级、负载和对照基线；单次吞吐值不能证明 Flash 适配正确。

## Information collection checklist

- 平台：芯片/板型、`PLAT`、SDK revision、启动介质、Linux/QNX、AB/non-AB。
- Flash：厂商/型号、Flash ID、容量、page/block geometry、接口线数、频率、ECC 与坏块信息。
- 软件状态：分区 JSON/mtdparts、生成的 AXDL/FDL/OTA 元数据、U-Boot/SBL 配置、内核或 QNX 启动配置。
- 现象证据：完整串口日志、Linux `dmesg`/`/proc/mtd`/`sysfs` 或 QNX `slog`/设备枚举/挂载信息、复现步骤和期望结果。
- 变更证据：变更前后配置差异、镜像版本、烧录方式、是否擦除持久化区域、测试循环或负载。

## Troubleshooting index

排障统一使用“现象 → 根因假设 → 首要证据 → 操作边界 → 验证结果”格式。已整理的主题入口如下：

- [`reference/m57/nand-filesystem-faq.md`](reference/m57/nand-filesystem-faq.md)：M57/AX637/AX637R 共享副本；Linux NAND/MTD/UBI/UBIFS 原则可复用，QNX 条目仅供 M57 使用。
- [`reference/m57/flash-scan.md`](reference/m57/flash-scan.md)：M57 Flash scan 文档；AX637/AX637R 另有同主题副本，命令可用性须回到目标 defconfig 核对。
- [`reference/m57/flash-adaptation.md`](reference/m57/flash-adaptation.md)：M57 启动链适配，含 MCAL/EB 条件步骤；AX637/AX637R 另有不含这些步骤的副本。
- [`reference/m57/qnx-ax-mtd.md`](reference/m57/qnx-ax-mtd.md)：M57 QNX `ax_mtd`、`mtdpart`、ETFS1/ETFS2、坏块映射和启动顺序。
- AX637/AX637R 使用 [`reference/ax637/_index.md`](reference/ax637/_index.md) 路由；共享 M57 文档只能作为通用方法，不能替代 AX637 的源码、配置和运行时证据。

每个问题至少确认平台、环境、Flash geometry、设备层和最早错误；未确认前不执行全片擦除、重分区或烧录。

## Environment differences

- Linux 侧重点是 MTD/UBI/文件系统设备节点、内核日志、sysfs/proc 状态与 rootfs 构建产物。
- M57 QNX 侧重点是 `ax_mtd`、`mtdpart`、`etfs`、虚拟 Flash、IPC/超时、裸分区坏块管理和自动挂载证据；AX637/AX637R 不适用该环境条目。
- M57 与 AX637/AX637R 的分区、启动介质、Flash 控制器和配置路径不得混用；平台文档只引用对应 reference 路由。

## Constraints and safety

- 分区、擦除、坏块标记和烧录可能导致数据丢失或设备无法启动；写操作前备份原始配置、镜像和持久化数据，并展示精确差异。
- 未确认 Flash geometry、ECC、坏块预留、分区边界和镜像大小前，不建议执行全片擦除或重分区。
- 不把 demo 配置、单次 scan 结果或单个平台命令当作跨平台默认值；不在日志、文档或提交中保存敏感烧录材料。
- 诊断优先采用最早出现的错误和可回读状态；不要只凭最后一条 mount 或 timeout 日志下结论。

## Sources

- 部门 SDK BSP Skills 实施计划（M57 & AX637）
- nand文件系统FAQ
- M57 FAQ计划
- `platforms/m57.md`、`platforms/ax637.md` 与各自 `reference/<id>/_index.md`
