---
name: sdk-bsp-boot-diag-skill
description: 面向 AX615 SDK/BSP 的系统启动诊断 skill。根据 BL1/SPL、DDR、镜像加载、U-Boot、Linux/OP-TEE 启动日志和可核实的代码证据判断启动故障；证据不足时明确标为待验证并给出下一步取证建议。适用于启动卡死、无日志、镜像加载失败、启动介质异常、Linux 启动回退、bootargs/DTB 问题和启动后立即复位，不用于无启动链路依据的泛化硬件猜测。
---

# AX615 系统启动诊断

当前 AX615 工作区的 Linux 代码基线是 `kernel/linux/linux-4.19.125`。涉及内核、SPI NAND、驱动或启动后行为时，只引用该版本的实际文件和符号；启动链路的 BL1/SPL/U-Boot 仍以工作区对应分支为准。

全程用中文回答；命令、路径、宏名、日志原文和代码标识符保持原样。目标是把问题定位到“已由证据确认的结论”“高可信但待验证的方向”或“无法判断”，而不是为每个启动失败强行指定根因。

## 适用边界

- 只针对本仓库可见的 AX615 启动链路和用户提供的实际镜像/日志。
- 不把历史案例标签、最后一行日志或“偶发”描述当作根因。
- 不直接修改 `boot/`、`kernel/` 下的源码或镜像；诊断阶段只读分析并给出低风险验证步骤。
- 如果问题明确属于 DDR training、DDRMC/DDRPHY 或内存稳定性，提示用户改用 `sdk-bsp-ddr-diag-skill`，不要在本 skill 中重复展开 DDR 寄存器诊断。

## 证据规则

每条结论至少绑定一种证据：日志原文及时间顺序、当前源码文件/行号、镜像构建信息、可复现 A/B 结果或用户提供的已确认修复记录。没有证据时使用“待验证”，不得补写修复版本、寄存器含义、硬件规格或历史结论。

优先找**首个异常**，再解释后续 `boot failed`、回退或 watchdog。启动阶段必须区分：ROM/BL1、SPL DDR、存储初始化、镜像加载、OP-TEE/U-Boot、Linux/RTOS 和 userspace。

## 诊断流程

1. **闭合输入**：确认板型、AX615 具体型号/revision、启动介质（SD/eMMC/NOR/NAND）、SDK/分支/镜像时间、串口参数、是否冷启动或复位、可稳定对照组；收集首个异常前后至少 20~50 行原始日志。
2. **确定最后成功阶段**：用日志锚点判断是否到达 `serial_initf`、`The system boot from ...`、DDR 初始化、`flash:<name> init failed`、`<image> image load failed`、`enter optee`/U-Boot 或 Linux early console。
3. **匹配已知代码行为**：按 [code-map.md](references/code-map.md) 的入口和证据要求核对实际源码，不凭相似文件名推断。
4. **检索案例**：按日志特征、芯片/介质和版本匹配 [known-cases.md](references/known-cases.md)。案例仅在适用条件和关键证据同时命中时使用；缺少闭环证据的案例不得表述为最终根因。
5. **输出结论**：按 [response-template.md](references/response-template.md) 输出“结论等级、依据、机制、验证、边界、下一步”。若关键输入缺失，一次只追问最影响判断的一项。

每轮诊断都要完成一个闭环：明确最后成功阶段，指出首个异常，给出一条可复现的验证动作，并说明什么结果会推翻当前判断。仅罗列可能性而没有验证动作，不算完成诊断。

## 当前代码的高信号规则

- `boot/bl1/common/include/printf.h` 中 `DEBUG` 为 `0` 时，`info`/`debug`/`printf` 可能不输出；“没有 BL1 日志”不能直接等同于 BL1 未执行。
- `boot/bl1/spl/spl_main.c` 的 `main()` 按 `init_sequence_f` 执行初始化，随后调用 `spl_dram_init()`；失败会打印 `ddr init fail` 并停机。若日志停在该阶段，先收集 DDR skill 所需信息。
- `setup_boot_mode()` 根据 `TOP_CHIPMODE_GLB_SW` 选择 SD/eMMC/NOR/NAND，并输出 `The system boot from ...`；介质判断应以实际日志和芯片模式寄存器为准。
- `spl_load_images()` 先初始化 loader，再逐个加载镜像；`flash:<name> init failed`、`<image> image load failed` 和 `<image> post-load failed` 是不同故障层级，不能合并为“存储坏”。
- `spl_postload_image()` 可能复制 DTB、更新 bootargs；`copy_dtb_img failed` 或 `post-load failed` 应优先核对镜像布局、DTB 地址和构建宏。
- `boot_next_stage()` 在跳转 Linux/OP-TEE/U-Boot 前设置 `BOOT_KERNEL_FAIL`；`is_boot_uboot()` 连续计数达到 3 会打印 `kernel boot failed!` 并切换路径。该日志表示启动回退状态，不等于 Linux 根因。
- `boot/bl1/board/board.c` 定义了 watchdog 操作和芯片/DDR 类型 efuse 读取；出现复位时要区分 watchdog、软件复位、panic 和电源复位，缺少 reset reason 时只能列为待验证。
- Linux 启动后若进入 SPI NAND 读取/ECC 错误路径，使用工作区 `kernel/linux/linux-4.19.125/drivers/mtd/nand/spi/core.c` 和对应器件驱动核对 `eccinfo.get_status`；`status=0x30` 的含义依赖具体 NAND 型号，不能脱离器件驱动解释。

## 禁止瞎猜与升级条件

不要仅凭以下现象给出确定结论：无日志、`ddr init fail`、`flash init failed`、`image load failed`、`kernel boot failed!`、黑屏、自动重启。至少补齐阶段、首个异常、启动介质、镜像版本和一份稳定/失败对照。

若三轮低风险取证仍无法确定，输出证据清单和交接建议，不继续扩展猜测。需要硬件团队介入时，明确还缺少串口波特率、芯片型号、板卡版本、电源/复位波形、存储原始读校验或完整镜像哈希中的哪些项目；不要用“概率性”“偶现”替代复现率、触发条件和对照组。

## Eval 与发布门禁

- `evals/evals.json` 覆盖静默启动、镜像加载、跨阶段 ABI 和 SPI NAND ECC 四类诊断边界。
