---
name: sdk-bsp-fast-boot-skill
description: 分析定位快起（Fastboot/AOV/打猎相机）场景下的双核共存、外设资源仲裁冲突、Handover（交接）失败/超时、首帧异常、RTOS POSIX 互斥锁断言死锁、跨核 CMM 内存释放 Panic 及裁剪配置缺失等问题。适用于涉及 RTOS(E907) 与 Linux 双核交接、I2C/SPI/GPIO 外设冲突、RPMSG 通信、ISP 快起出流及双核内存移交的故障分析。
---

# Fastboot Analysis (快起与双核交接分析)

## 适用范围

本技能针对芯片（如 AX615 等）在**快起（Fastboot / AOV / 打猎相机）**及**异构双核（RTOS + Linux）共存**场景下的各类疑难问题进行分层分析与排查定位。覆盖以下核心场景：
1. **外设仲裁与互斥冲突**：RTOS 与 Linux 争抢 I2C、SPI、UART、GPIO 等硬件外设，大核报 `busy, rtos using` 或驱动初始化失败（如打猎相机 4G 模组通信死锁等经典问题）。
2. **交接（Handover）失败 / 超时**：Linux 发送交接请求后超时无应答、`handover abort`、`refcnt not zero` 引用计数阻塞、RPMSG 通信死锁。
3. **图像管线与首帧异常**：RTOS 阶段 Sensor/ISP 未出流、交接时 `yuv_done_mask` 不匹配、首帧图像撕裂/花屏、FrameBuffer 丢弃/越界。
4. **中断与时钟移交异常**：交接瞬间触发中断风暴、中断亲和性（Affinity）切换异常、时钟门控（PCLK/CLK）未释放导致大核挂死。
5. **双核内存移交错误**：CMM / PrivPool 物理内存块移交失败、双重释放、内存越界。
6. **交接期系统挂死与复位**：启动中途突发看门狗超时复位、ROM 重新上电打印。

---

## 核心机制与架构参考

分析前建议参考以下文档深入了解机制与日志指征：
- [fastboot-mechanisms.md](references/fastboot-mechanisms.md)：快起时序三阶段、硬件 Dummy 共享状态寄存器分配、Handover 核心接口。
- [fastboot-troubleshooting.md](references/fastboot-troubleshooting.md)：各模块典型错误日志库、排查分类树、Watchdog 现场保护与 Trace32 抓证方法。
- [fastboot-classic-cases.md](references/fastboot-classic-cases.md)：经典深度故障案例库（RTOS 锁未初始化、跨核 CMM vunmap panic、DDR64 Lite 裁剪遗漏驱动）。
- [fastboot-knowledge-base.md](references/fastboot-knowledge-base.md)：高质量缺陷全景知识库（覆盖双核交接、跨核内存、图像管线、智能算法、启动性能与外设环境 6 大维度 113 项核心缺陷机制总结与排查速查）。

---

## 阶段划分与故障定位工作流

快起生命周期严格分为三个阶段，首先通过日志确定故障发生的**精确时间边界**：

```text
阶段 I: Pre-Handover (RTOS 独占期) ──▶ 阶段 II: In-Handover (交接协商期) ──▶ 阶段 III: Post-Handover (Linux 接管期)
- 小核初始化 Sensor/ISP             - Linux 发起 Rpmsg 请求           - Linux App (Sample/QSDemo) 运行
- 独占 Claim 外设 (I2C/SPI)         - RTOS 唤醒 syshandover 线程      - 大核驱动全面接管硬件
- 大核加载，未交接前访问外设        - 释放外设状态、移交中断/内存     - 小核休眠或受限运行
```

### 1. 阶段 I（Pre-Handover）故障诊断
- **现象**：大核应用或驱动在初始化时报外设忙（如 `ax_i2c busy, rtos using`）、返回 `-EBUSY`、外设探测失败。
- **定位步骤**：
  1. 确认大核访问该外设的业务时钟点（是否必须在 Handover 前访问，例如打猎相机 4G 模组提前通信）；
  2. 检查 RTOS 外设 Claim 策略：是否开启了全通道无差别独占（如旧版将 I2C0~2 全部标记使用）；
  3. 检查 RTOS 环境变量配置（如 `rtos_i2c_claim_mask`）及代码中实际使用的通道号，确认是否做到了“按需 Claim”；
  4. 检查硬件共享状态寄存器（如 `AX_DUMMY_SW6_ADDR`）的各个状态位。

### 2. 阶段 II（In-Handover）故障诊断
- **现象**：Linux 打印 `rpmsg wait handover done timeout` 或 `ax_rpmsg_request failed`；RTOS 打印 `handover abort` 或 `refcnt not zero`。
- **定位步骤**：
  1. **检查引用计数 (`refcnt`)**：查看 RTOS `syshandover` 是否卡在某个模块，检查 `_ax_sys_handover_check_refcnt_log()` 输出，确认是 `AX_ID_VIN`、`AX_ID_IVPS` 还是 `AX_ID_VENC` 引用未归零；
  2. **检查 Sensor/ISP 状态**：确认 Sensor 在小核阶段是否正常出流，检查 `pipe_mask` 与 `yuv_done_mask` 是否一致；若未出流，确认硬件供电、Reset GPIO、MCLK 及 I2C 通道配置；
  3. **检查中断移交（Affinity）**：排查交接时 `rt_hw_irq_set_affinity` 移交的中断是否在大核已注册 ISR，防止产生未处理的中断风暴。

### 3. 阶段 III（Post-Handover）故障诊断
- **现象**：交接完成后大核业务花屏、卡死、或大核驱动操作外设报超时。
- **定位步骤**：
  1. 检查 RTOS 在交接时是否完整调用了释放接口（如 `i2c_rtos_release_channels`）；
  2. 检查大核外设驱动在 Handover 完成后是否重新正确配置了时钟与中断（如 Linux I2C 的 `devm_request_irq` 状态）；
  3. 检查 PrivPool / CMM 内存块的释放与生命周期交接。

---

## 常见症状排查矩阵

| 故障症状 | 疑似模块 | 核心排查手段 | 典型先例与机理 |
|---|---|---|---|
| Linux 报 `i2c busy, rtos using` | RTOS BSP / Linux I2C | 检查 `rtos_i2c_claim_mask`，确认 RTOS 是否仅占用了实际接 Sensor 的通道；检查 Linux 驱动错误码返回 | I2C 通道全占满导致外设无法通信 |
| 交接超时 `handover done timeout` | RPMSG / Sys Handover / VIN | 检查各模块交接回调执行状态及 refcnt；确认 Sensor 首帧是否按时送达 ISP | 平台 Handover 流程 |
| 突发复位（ROM 重新输出） | 软硬件看门狗 / 供电 | 关掉 Linux 和 RTOS Watchdog，保留现场连 Trace32 分析 PC/LR/SP | 双核死锁超时触发复位 |
| 启动报 `i2c channel x is not claimed by rtos` | RTOS Sensor 驱动 | 检查 sensor 挂载的 I2C 索引与 claim mask 是否匹配 | 打猎相机 / AOV 配置 |
| 首帧图像花屏或丢失 | ISP Kernel / VIN FrameBuffer | 检查 `vin_comm_glb_impl.c` 中 `overflow` 标记及丢帧处理逻辑 | Fastboot 图像流 |
| 压测千轮交接失败，rt_mutex 断言 | RTOS POSIX 适配层 | 检查全局/静态 `pthread_mutex_t` 是否只用静态宏初始化，未显式调用 `pthread_mutex_init` | RTOS POSIX 静态锁未初始化缺陷 |
| reboot 时内核崩溃在 `__vunmap+0x58` | Linux CMM / RPMSG 通信 | 检查多核释放 CMM 远端反查 kvirt 的 RPC 返回校验，杜绝非法脏地址传入 `vunmap` | 跨核 CMM 虚拟地址释放解引用缺陷 |
| 功能使能后报 `NOT_PERM` (0x80200215) | Linux 内核裁剪 defconfig | 检查 Lite 全内置工程中对应驱动（如 ASoC simple-card）是否被误配为 `=m` | Lite 全内置裁剪工程遗漏驱动配置 |
| 关掉串口 log 或降低日志级别后卡死 | 双核并发同步机制 | 海森堡 Bug，排查是否缺少显式物理延时或 RPMSG 共享标志未加锁，依赖了日志打印延时 | 关闭日志暴露时序竞争 |
| 交接后码流全是 P 帧导致拉流花屏 | VENC 编码驱动 | 检查 Linux 接管后编码器是否在首帧主动触发强制请求 IDR 帧 | 交接首帧未强制生成 IDR 关键帧 |
| /proc/ax_proc/mem_cmm_info 为负数 | CMM 跨核内存管理 | 排查 Double Free 或跨核未对齐释放，检查 CMM Bitmap 位图接管对齐 | CMM 跨核释放下溢或位图冲突 |

---

## 交付分析报告规范

当使用本技能输出快起问题分析结论时，应遵循以下结构：

1. **问题阶段界定**：明确故障属于 Pre-Handover、In-Handover 还是 Post-Handover 阶段；
2. **双核时序与资源流转分析**：说明该外设/资源在 RTOS 侧与 Linux 侧的分配与交接期望；
3. **根本原因推断**：结合日志、共享寄存器读数或代码逻辑，指出断裂的关键节点；
4. **验证与行动建议**：
   - 临时验证/现场保护方案（如修改 claim mask、关闭看门狗、保留挂死现场）；
   - 代码修复与规范建议（按需分配、标准错误码、完备的释放与移交回调）。
