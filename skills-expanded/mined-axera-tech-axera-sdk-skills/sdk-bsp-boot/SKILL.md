---
name: sdk-bsp-boot
description: Axera SoC Boot 启动链 — SBL/AB 启动管理、U-Boot 引导内核方式、内存与 FLASH 分区规划、BOOTROM、BootCnt、OTA 升级及启动类问题诊断。通过路由自动适配平台（m57、ax637）。
metadata:
  author: Axera BSP Team
  tags: [axera, boot, sbl, uboot, distro-boot, partition, bootrom, bootcnt, ota, ab]
  data-classification: public
---

# Axera Boot

## When to use

- 查询/配置 Axera SDK 的启动链路（BootROM → SBL → SPL → BL31 → OP-TEE → U-Boot → Kernel）。
- 规划或调整内存（Linux / CMM / Inline ECC）与 FLASH 分区（partitions.json、mtdparts、AB 分区大小约束）。
- 定制 U-Boot 引导内核方式（distro_bootcmd / extlinux / 各组合简化 BOOTCMD）。
- 诊断启动类问题：BOOTROM 字符、SBL AB 管理日志、U-Boot/Kernel 启动日志关键字。
- 对接 OTA A/B 升级、BootCnt 启动计数、调试串口波特率等启动相关特性。
- 不用于：Secure Boot 签名/加密与 eFuse 规划（用 `sdk-bsp-secure-boot`）；纯 Linux 驱动、音视频、NPU 等非启动主题。

## Routing

1. 若 `args` 显式给出 `platform=<id>`，优先使用该平台（可用 id：`m57`、`ax637`）。
2. 否则按 `routing.yaml` 自上而下匹配 `detect` 路径。具体 board/SDK 条目（`ax637`）排在通用架构条目（`m57`）之前。
3. 命中 `ax637` 时，先加载 `platforms/ax637.md`，再按 `extends: m57` 叠加 `platforms/m57.md`；同名条目以 `ax637` 为准。
4. 命中后先用一句话汇报平台身份（`display`）与命中的检测路径，再开始回答；这里的 `platform` 仅表示 SDK/架构路由（`m57` 或 `ax637`），不等于构建用的 `PLAT`。
5. 无命中则按 `fallback` 询问用户显式指定 `platform`，不要猜测。
6. 只加载选中平台的 `platforms/<id>.md`；`reference/<id>/_index.md` 是该平台的文档路由表。禁止跨平台引用路径、分区默认值或日志关键字。

## Platform and target confirmation

- `PLAT` 是用户要确认的目标，不等同于“当前工作区”或“最近一次构建的目标”。不得根据已有 `out/`、生成的 XML、烧录产物、文件修改时间，或任意一个 `config.mk` 自行认定当前 PLAT。
- 用户未显式给出 `PLAT`，却询问“是否开 AB”、默认启动方式或其他依赖构建配置的问题时，先做只读枚举：执行 `make plist` 获取 SDK 支持的全部 PLAT，再读取各候选 `build/platforms/axera/<PLAT>/config.mk` 的 `SUPPORT_AB`，逐项列出 PLAT、FLASHTYPE 和 AB 状态；明确当前没有唯一答案，并请用户选择目标 PLAT。不得只回答最近构建过的一个平台。
- `SUPPORT_AB` 按 SDK 默认值判定：`SUPPORT_AB := FALSE` 才表示关闭 AB；`SUPPORT_AB := TRUE` 表示开启；配置文件未定义 `SUPPORT_AB` 时按默认开启处理，不能把“未定义”当作关闭。枚举结果应区分“显式开启”和“默认开启（未定义）”。
- 用户显式给出 `PLAT` 后，才把该配置作为目标，读取其完整配置与对应分区/镜像文件，并引用具体值；修改前仍需再次确认目标。
- 一次收集关键信息：目标板型/PLAT、FLASHTYPE（only_nand / only_emmc 或 nor_nand / nor_emmc）、是否 AB、是否安全启动、目标介质。
- 目标确认前只允许读取用于平台枚举的配置元数据，不修改任何平台文件；目标确认后才读取/修改平台配置文件与分区文件。

## Instructions

1. **识别平台**：按 §Routing 加载 `platforms/<id>.md`（及 `extends` 的父平台文件），并读取 `reference/<id>/_index.md` 定位文档。
2. **定位主题章节**：启动链路见 `platforms/m57.md` §启动链路；构建与 PLAT 见 §目标平台配置与公共构建规则；内存见 §内存规划；分区见 §FLASH 存储空间分配与分区与对应平台文件；U-Boot 引导见 §U-Boot 引导内核方式。
3. **回答内存问题**：明确区分 Linux 内存、CMM、Inline ECC 三部分，并给出调整入口——M57 与 AX637 一致，均改对应平台 `config.mk` 的 `SYSTEM_MEMORY_SZ` / `LINUX_MEMORY_SZ`（两者之差为 CMM），Inline ECC 见 `platforms/m57.md` §内存规划。
4. **回答分区问题**：引用该平台 `partitions.json`（AB）/ `partitions_without_ab.json`（非 AB）的默认值与约束；强调 size 单位 KB、需为 block size 整数倍、AB 场景 SBL 分区必须用默认值。
5. **回答 U-Boot 引导问题**：先给默认 `distro_bootcmd` 链路与 `extlinux.conf`（`platforms/m57.md` §U-Boot 引导内核方式），再按“是否 AB × 是否安全启动”给出对应简化 BOOTCMD（`platforms/ax637.md` §U-Boot 简化引导命令）；only_emmc 场景把 `load mtd` 换成 `load mmc`。
6. **诊断启动失败**：按阶段对齐现象——BootROM 阶段看 §故障定位 §BOOTROM 字符含义；SBL 阶段看 §SBL AB 管理 FAQ log 与 §复位 main 域，其中 AB FAQ log 需按“自己/对面槽状态 × 自己是 A/B × 异常断电/软复位”映射到 S1/S2/S3.x 场景，判断是可在 AB 间切换恢复还是已变砖（完整枚举见 `reference/m57/M57 SBL启动特性介绍.md` §1.2）；U-Boot/Kernel 阶段看启动日志关键字。不得把串口关键字跨平台混用。
7. **OTA / 串口波特率 / BootCnt**：OTA 见 `platforms/m57.md` §OTA 升级；串口波特率见对应平台文件（AX637 默认 115200，trunk 车载 921600）。BootCnt 仅 M57 支持，AX637 / AX637R 不支持，问 AX637 时不要套用 M57 的 BootCnt 方案。
8. **引用文档**：只引用命中的 `reference/<id>/` 下的文档与实际路径，不臆造链接、日志或分区数值。
9. **超出范围**：若问题涉及 Secure Boot、eFuse、签名加密，转向 `sdk-bsp-secure-boot`。

## Safety

- 分区表与 SBL/metadata 大小直接影响能否启动：AB 场景 SBL 分区必须用默认值；不确定时先备份 `partitions.json` 并提示风险，不擅自改小启动分区。
- 修改内存/分区后必须重新编译并用 AXDL 烧写验证；只读文件系统下不能依赖板端就地修改。
- 不擅自更改用户 PLAT 工程、不臆造分区名；新增 Acore 侧分区必须同步 U-Boot `main_part_id[]` 白名单。
- 涉及擦写 FLASH、AXDL 烧录等破坏性操作前，说明影响范围并先征得确认。

## 平台矩阵

| 平台 id | 说明 | 自动检测触发条件 | 主文档 |
| --- | --- | --- | --- |
| ax637 | AX637 / AX637R SDK（基于 M57） | `SafetyIsland/rt-thread/bsp/m57/configs_ax637`、`configs_ax637r` 任一存在 | `platforms/ax637.md`（+ `platforms/m57.md`） |
| m57 | Axera M57 SDK（M57 架构） | `SafetyIsland/mcal` 存在 | `platforms/m57.md` |

新增平台：在 `routing.yaml` 增加条目（`id`/`display`/`detect`/`load`/`reference_root`/可选 `extends`）→ 新增 `platforms/<id>.md`（仅写与父平台差异）→ 新增 `reference/<id>/` 与 `_index.md` → 在 `evals/<id>/tasks.yaml` 增加验收任务 → 更新本表、`README.md` §平台矩阵、`skill-card.md`。
