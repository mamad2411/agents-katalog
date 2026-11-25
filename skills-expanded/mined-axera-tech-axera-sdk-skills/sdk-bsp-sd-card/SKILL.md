---
name: sdk-bsp-sd-card-skill
description: 面向 AX615 SDK/BSP 的 Linux 启动后 SD 卡问题诊断 skill。根据 Linux SDHCI/MMC、驱动 built-in 或 .ko 加载、card detect、供电、管脚上下拉、block I/O、FAT/VFAT/exFAT、mount、readonly 和热插拔日志定位故障层级；证据明确时直接给出结论，证据不足时明确标为待验证并给出最小化取证建议。用户提到 AX615、SD 卡、sdhci-axera、mmcblk、识别不到、挂载失败、readonly、读写错误、tuning、PHY、电压切换、broken-cd、cd-gpios 或拔卡问题时优先使用；不得仅凭模糊现象猜测硬件根因。
---

# AX615 Linux SD 卡问题分析

当前 AX615 工作区的 Linux 代码基线是 `kernel/linux/linux-4.19.125`。本 skill 重点关注**启动之后 Linux 阶段**的 SD 卡识别、枚举、读写、文件系统和热插拔问题。BL1/SPL、U-Boot 阶段 SD 启动问题暂不作为主要范围；后续需要时再补充启动阶段专项规则。

全程使用中文回答；命令、路径、宏名、日志原文和代码标识符保持原样。目标是把问题定位到“已确认”“高可信待验证”或“信息不足”，而不是为每个“SD 识别不到”或“挂载失败”强行指定根因。

## 适用范围

覆盖以下 Linux 启动后问题：

- `sdhci-axera`、MMC core、MMC block 驱动是否 built-in、是否为 `.ko`、是否需要 `insmod`/`modprobe`；
- Linux `sdhci-axera` probe、`mmc_of_parse()`、card detect、`broken-cd` polling、`cd-gpios` detect、`cd-inverted` 和 debounce；
- SD 卡供电 GPIO、1.8 V/3.3 V voltage switch、PHY/tuning、pinmux 和管脚上下拉；
- `/dev/mmcblk*`、分区、block I/O、CRC/timeout/ADMA/DMA 错误；
- FAT/VFAT/exFAT 挂载失败、readonly、文件系统损坏、未 `umount` 直接拔卡、热插拔后 I/O 错误；
- SD、eMMC、SDIO 或 emmc2sd 变体之间的控制器/设备树配置混淆。

不在没有证据时判断：SD 卡物理损坏、PCB 信号完整性、供电器件损坏、PHY delay 的具体最优值、某个外部案例的根因或某个版本已经包含修复。遇到启动前 BL1/SPL、U-Boot、DDR training、供电波形或示波器眼图等问题，只说明需要的验证，不代替对应专项分析。

## 证据纪律

1. 优先定位**最后成功阶段**和**首个异常**。后续的 `mount failed`、readonly、应用访问失败通常是结果，不自动是根因。
2. 每条结论至少绑定一种有效证据：原始日志及顺序、当前源码函数、目标 DTS/配置、实际 kernel config/模块版本或成功/失败 A/B 对照。
3. 当前工作区源码、示例 DTS 和 defconfig 不等于用户正在运行的 kernel、DTB、rootfs、模块和卡内容。结论中必须标明这一边界。
4. 日志只显示了某个函数返回失败时，只能确认该函数所在层级；不能直接扩展成“卡坏”“硬件坏”或“需要换板”。
5. 每轮结论都必须给出至少一个低风险验证动作、预期结果和反证条件。一次只改变一个变量。
6. 不把外部案例编号、链接或未核验正文当作当前问题的证据；不将相似现象套成固定根因。

## 诊断流程

### 1. 先闭合最小输入

优先收集：

- AX615 具体型号/revision、板型、SD 控制器用途和目标 DTS/DTB；
- SD 是 Linux 运行时插卡、固定存储，还是 SDIO；卡的型号、容量、速度等级；
- kernel、DTB、rootfs、模块包的 SDK/分支/构建时间或版本；
- 实际 kernel config 中 `CONFIG_MMC`、`CONFIG_MMC_BLOCK`、`CONFIG_MMC_SDHCI`、`CONFIG_MMC_SDHCI_PLTFM`、`CONFIG_MMC_SDHCI_AXERA`、`CONFIG_FAT_FS`、`CONFIG_VFAT_FS`、`CONFIG_EXFAT_FS` 是 `=y`、`=m` 还是未启用；
- 是冷启动后识别不上、热插拔识别不上、写入后 readonly，还是未 `umount` 拔卡后损坏；复现率和成功/失败对照；
- 完整原始 `dmesg -T`，至少包含首个 SD 相关异常前后 20～50 行，不要只粘贴最后一行；
- 若是挂载或 readonly，提供 `cat /proc/partitions`、`blkid`、`mount`、`cat /sys/block/mmcblk*/ro` 和对应 `dmesg`；若是读写问题，提供第一次 I/O 错误、读写命令、速率/模式和卡信息。

只有“完全没有日志”时，先核对驱动是否 built-in 或 module 是否已加载、日志级别、目标 DTB 是否启用该节点；不要把无日志直接等同于 SD 卡未上电或卡损坏。

### 2. 卡识别不上时的优先排查顺序

遇到“没有 `/dev/mmcblk*`”“识别不到卡”“插卡无反应”时，按以下顺序排查，不要直接跳到供电或硬件：

1. **确认驱动配置方式**：查看实际 `.config` 或 `/proc/config.gz`，确认 `CONFIG_MMC*`、`CONFIG_MMC_SDHCI*`、`CONFIG_MMC_SDHCI_AXERA` 是 `=y` built-in、`=m` module，还是未启用。
2. **如果是 built-in（`=y`）**：驱动应随内核启动自动 probe，不应依赖 `insmod`；重点看 `dmesg` 是否有 `axera sdhci probe`、资源/DTS/PHY/GPIO 错误。
3. **如果是 module（`=m`）**：确认 rootfs 是否包含 `sdhci-axera.ko` 及依赖模块，`lsmod` 是否已有 `mmc_core`、`mmc_block`、`sdhci`、`sdhci_pltfm`、`sdhci_axera`；必要时按依赖使用 `modprobe sdhci-axera` 或 `insmod`，并保留失败日志。
4. **确认目标 DTB**：检查节点 `compatible = "axera,sdhc"`、`status = "okay"`、`reg`、`interrupts`、`no-mmc/no-sdio`、`bus-width`、`max-frequency`、PHY delay 和板型是否匹配。
5. **确认 card detect 方式**：`broken-cd` 表示 polling；`cd-gpios` 表示 GPIO detect，需核对 `cd-inverted`、`cd-debounce-delay-ms` 和 GPIO 电平。两类问题的诊断路径不同。
6. **确认供电路径**：核对 `pwr_en_gpioD/Q`、`pwr_sw_gpio`、上电延时和 `dmesg` 中电压稳定性日志；如果没有 `pwr_en_gpioD/Q`，还要核对驱动是否进入保持供电、不能主动断电的路径。
7. **确认 pinmux 和上下拉**：检查硬件设计和 pinmux；当前驱动中 SD 引脚上下拉动态配置代码被注释，注释说明倾向依赖 VDD 硬件上拉。因此不要假设软件一定会切上下拉。
8. **确认枚举与 block 设备**：在 host probe 成功后，再看 MMC core 是否完成 card enumeration、是否出现 `mmcblk`、是否有 CMD/CRC/timeout。

### 3. 按 Linux 层级确定阶段

| 阶段 | 主要确认点 | 不能越界推出的结论 |
|---|---|---|
| driver/module | kernel config、built-in/module、`.ko`、依赖模块、`insmod`/`modprobe`、`lsmod`、`dmesg` | 无 `/dev/mmcblk*` 不等于卡坏 |
| Linux probe | `axera sdhci probe`、资源、IRQ、PHY init/lock、`sdhci_add_host` | probe 失败不能仅凭日志判断 PCB 或电源器件损坏 |
| card detect | `broken-cd` polling、`cd-gpios` detect、`cd-inverted`、debounce、GPIO 电平 | 插卡无反应不能直接归因供电或卡坏 |
| power/pin | `pwr_en_gpioD/Q`、`pwr_sw_gpio`、无电源 GPIO 时的保持供电路径、pinmux、上下拉、3.3 V/1.8 V | GPIO 配置缺失不能直接证明电源器件坏 |
| card enumeration | CMD/响应、MMC core 建卡、`mmcblk` | 枚举失败需区分 detect、供电、卡、时钟和 tuning |
| voltage/timing | 3.3 V/1.8 V、UHS、PHY delay、hardware/software tuning | tuning 回退不等于 SD 卡物理损坏 |
| block I/O | CRC、timeout、ADMA/DMA、数据传输错误、读写复现 | 单次 I/O 错误不能单独区分卡、信号、时钟和供电 |
| partition/filesystem | 分区表、FAT/VFAT/exFAT、superblock、readonly、mount 参数和模块 | mount 失败/readonly 不能反推 SDHCI 控制器必然异常 |
| userspace/hotplug | 设备节点、权限、占用进程、`umount`、热插拔时序 | 业务错误不能覆盖更早的 kernel MMC 错误 |

### 4. 文件系统损坏、readonly 与拔卡规范

分析 FAT32/VFAT/exFAT 损坏、readonly 或 mount 失败时，必须单独强调：**SD 卡写入后必须先 `sync`，再 `umount`，确认卸载成功后才能拔卡**。未 `umount` 直接拔卡或异常断电可能导致写缓存和文件系统元数据未落盘，下一次挂载可能失败或自动 readonly。

安全拔卡基本流程：

```text
sync
umount /mnt/<sdcard>
mount | grep mmcblk   # 确认不再挂载；如果仍在，不能拔卡
```

若 `umount: device is busy`，先用 `fuser -vm <mountpoint>` 或 `lsof <mountpoint>` 找占用进程。不要为了继续拔卡而忽略 busy；这会增加 FAT/exFAT 损坏概率。

只读诊断要分层：

- `mount` 显示 `(ro)`：确认挂载是只读，但还不能判断原因；
- `/sys/block/mmcblk*/ro` 为 `1`：块设备层只读；
- `dmesg` 出现 `FAT-fs`、`exFAT-fs`、`Volume was not properly unmounted`、`read-only`：优先考虑文件系统未正常卸载、元数据损坏或 I/O 错误触发只读；
- 只有 `mount failed` 或 readonly，不能直接归因 SDHCI/PHY/tuning。

### 5. 对照当前代码路径

按 `references/code-map.md` 找到实际入口和日志。至少回答：

- 首个错误来自 driver/module、probe、card detect、power/pin、enumeration、block I/O 还是 filesystem？
- 该日志是当前代码的必然失败路径、降级路径还是普通提示？
- 目标 DTB、实际 kernel config、模块和当前源码是否一致？
- 是否有成功卡、成功镜像、低速模式、正常 `umount` 或另一块板的对照？

### 6. 输出闭环

使用 `references/response-template.md` 输出：故障阶段、首个异常、最后成功阶段、证据、机制、验证动作、预期结果、反证条件和下一步。若关键证据缺失，结论等级必须为“信息不足”或“高可信待验证”，并列出最少的补充信息。

## 回归自检 Golden Case

`evals/` 保存 Linux 启动后 SD 卡问题的合成 Golden Case，当前包括 `AXSD-001` 至 `AXSD-005`。每个 Case 分为两个区域：`input/` 是分析阶段可见的现场材料，`answer/` 保存评分用的 `case.yaml`、`oracle.yaml` 和 `reproducer.patch`。先只读取 `input/` 并冻结分析结果，再读取 `answer/` 进行评分；不要在分析阶段提前查看答案。

每个 Case 的覆盖目标、输入文件清单和隔离规则以自己的 `answer/case.yaml` 为准。这些合成输入用于验证诊断纪律，不替代目标设备实际 kernel config、DTB、rootfs、模块和原始日志。

## 当前代码的高信号规则

### Linux `sdhci-axera`

- `sdhci_axera_probe()` 的 `axera sdhci probe` 可用于确认 platform probe 已进入。若后续没有 host 注册或 `mmc` 枚举日志，只能划定在 probe/host 建立之后的失败区间，具体根因仍需核对返回值、DTS、资源和前后文。
- `sdhci_axera_probe()` 调用 `mmc_of_parse()` 解析标准 MMC DTS 属性，包括 `broken-cd`、`cd-gpios`、`cd-inverted`、`cd-debounce-delay-ms`、`non-removable`、`disable-wp` 等。驱动自身不实现私有 card detect 逻辑。
- `sdhci_axera_phy_init()` 通过 Cadence HRS04 访问 PHY、复位 DLL 并写入 DTS delay；`phy lock failed` 只确认 DLL lock 路径失败，不单独证明 delay 错误或硬件损坏。
- `sdhci_axera_set_power()`、`get_sd_pwr_ref_gpio()` 和 `sdhci_axera_start_signal_voltage_switch()` 分别涉及卡电源、电源 GPIO、3.3 V/1.8 V 稳定性和电压切换。`no sd_pwr_sw_gpio, cannot switch to 1.8V`、`3.3V regulator output did not become stable`、`1.8V regulator output did not become stable`、`Failed to get sd pwr_en_gpio from dts` 只能先定位到配置/控制路径。
- `sdhci_axera_execute_tuning()` 的 `no tuning point found`、`hw tuned ok`、`Tuning failed, falling back to fixed sampling clock` 和 `Tuning is not completely, falling back to fixed sampling clock, fixed val:%d` 必须区分。对于 SD，当前代码的软件 tuning 只在 `MMC_TIMING_UHS_SDR104` 下执行；回退或失败后如果低速读写稳定，应把问题范围收敛到高速 timing/电压/信号条件，但仍需 A/B 验证。
- `sdhci_axera_mst_chip_type_handle()` 对部分 AX615D SD master 按设计限制 3.3 V，不支持 UHS。若日志明确出现 `AX615D SD mst only design 3.3V, not support UHS`，这是当前代码的能力限制，不应判为卡故障。
- `axera_sdio_rescan()` 是 SDIO rescan 路径；SDIO/Wi-Fi 问题必须与 SD storage 的 `mmcblk` 枚举和 block I/O 分开分析。
- 驱动中 SD pin 上下拉动态配置代码处于注释状态，注释说明依赖 VDD 硬件上拉更合适；因此识别不上时要核对硬件上下拉/pinmux，而不是假设 Linux 驱动已动态设置上下拉。

### DTS、地址与内核配置

- `AX615.dtsi` 的 aliases 仅说明默认 `mmc0`/`mmc1` 关联；板级 DTS 可能覆盖控制器用途和地址。
- `AX615_nor_emmc2sd.dts` 等 emmc2sd 变体可能将 SD 放在 eMMC 控制器地址。控制器地址、IRQ、`compatible`、`no-sdio`/`no-mmc`、`bus-width`、`cap-sd-highspeed`、UHS 属性、`broken-cd` 或 `cd-gpios`/`cd-inverted`/debounce、`pwr_en_gpioD/Q`、`pwr_sw_gpio`、无 `pwr_en_gpioD/Q` 时的保持供电行为、`max-frequency` 和 PHY delay 必须以目标 DTB 为准。
- `CONFIG_MMC_SDHCI_AXERA` 在 Kconfig 中是 `tristate`，既可 built-in，也可 module。不同 defconfig/项目配置可能为 `=y` 或 `=m`；必须查看目标设备实际 `.config` 或 `/proc/config.gz`。
- 若为 `=m`，需要确认 `sdhci-axera.ko`、`sdhci-pltfm.ko`、`sdhci.ko`、`mmc_core.ko`、`mmc_block.ko` 等模块是否生成、打包并加载。若为 `=y`，则不会有独立 `.ko`，不应把 `modprobe` 找不到模块误判为驱动缺失。

## 现场取证原则

优先保存原始输出，不要只截取结论行。Linux 现场可根据权限执行以下只读检查，并注明命令失败或路径不存在：

```text
dmesg -T | grep -iE 'mmc|sdhci|sdio|tuning|phy|voltage|power|timeout|crc|adma|dma|error|fail|read-only|FAT-fs|exFAT'
cat /proc/partitions
ls -l /sys/class/mmc_host
ls -l /sys/block/mmc*
mount
blkid
lsmod | grep -iE 'mmc|sdhci'
zcat /proc/config.gz | grep -E 'CONFIG_MMC|CONFIG_FAT|CONFIG_EXFAT'
```

对具体卡和 host，再按实际路径读取：

```text
cat /sys/class/mmc_host/mmc*/mmc*/type
cat /sys/class/mmc_host/mmc*/mmc*/name
cat /sys/class/mmc_host/mmc*/mmc*/cid
cat /sys/class/mmc_host/mmc*/mmc*/csd
cat /sys/class/mmc_host/mmc*/mmc*/scr
cat /sys/block/mmcblk*/ro
```

以上 glob 在路径不存在时可能返回错误；应保留错误文本，不要把“路径不存在”改写为“卡损坏”。涉及 `dd`、`mkfs`、`fsck -y`、分区修改或格式化前，必须确认设备节点、备份数据和操作授权；诊断第一步不做破坏性写操作。

## 禁止瞎猜与升级条件

不要仅凭以下现象给出确定根因：无日志、无 `/dev/mmcblk*`、`mount failed`、readonly、`phy lock failed`、`no tuning point found`、`card removed`、自动重启或“偶发”。至少补齐故障阶段、首个异常、芯片/板型、目标 DTB、实际 kernel config/模块、SD 卡信息和一份成功/失败对照。

若三轮低风险取证仍不能区分驱动加载、DTB、card detect、供电、上下拉、信号、卡兼容性和文件系统问题，输出证据清单和升级交接项，不继续扩展猜测。交接时明确还缺少哪些内容：完整 dmesg、目标 DTB、kernel config 与模块清单、SD 卡料号和容量、复现率、原始读校验、正常 `umount` 记录、供电/时钟波形或成功对照。
