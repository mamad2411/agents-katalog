---
name: sdk-bsp-rpmsg
description: Axera IPC、RPMsg 与 RPZC — M57 Linux/QNX 主域、AX637/AX637R 非 QNX 场景和 SafetyIsland MCU/RTOS/MCAL 的配置、API、联调与故障定位。
metadata:
  author: Axera BSP Team
  tags: [axera, ipc, rpmsg, rpzc, linux, qnx, mcal, shared-memory]
  data-classification: public
---

# Axera IPC / RPMsg / RPZC

## When to use

- 配置或验证 M57 Linux/QNX、或 AX637/AX637R 非 QNX 场景与 SafetyIsland 之间的 RPMsg 通信
- 配置物理通道、endpoint、name service、mailbox/GPIO 通知和 reserved-memory
- 使用 RPZC 完成大块数据的 zero-copy 传输、接收、ACK 和 buffer 生命周期管理
- 联调 M57 Linux/QNX 或 AX637 非 QNX 主域与 MCU MCAL/RTOS 的 `Ipc`、`Ipc_zc` 配置及 reset/reinit
- QNX 日志仅适用于 M57 QNX；AX637 使用实际 Linux/RTOS、设备节点和 MCU/RTOS 状态定位链路问题

不用于 Secure Boot、eFuse、签名镜像或与核间通信无关的构建任务。

## Routing

1. 若参数传入 `platform=<id>`，直接使用；否则按 `routing.yaml` 从上到下匹配，具体 board/SDK 条目排在通用架构条目前面。
2. 命中平台后加载 `platforms/<id>.md`；参考文档路径以 `reference/_index.md` 为准。Linux、MCAL、RTOS 的公共知识先读 `reference/ax_ipc.md`，问题复盘 FAQ 读取本地 `reference/ax_ipc_FAQ.md` 及其相对引用图片，无需访问在线来源；其他参考资料也按索引中的实际路径读取。QNX 流程仅适用于 M57；AX637 不支持 QNX，QNX 相关修改无需同步到 AX637。
3. 用一句话汇报识别到的平台、主域类型和参考来源；未确认主域类型或 MCU 对端时，只识别 SDK 家族，不擅自选择配置文件。
4. 若无匹配，执行 `fallback: ask`，要求用户提供平台或补充路由条目。

## Target confirmation

开始修改配置前一次收集缺失项：芯片/板型、主域（M57 可为 Linux 或 QNX；AX637 不支持 QNX）、MCU 对端与核号、SDK 版本、物理通道、对端类型（MCAL/RTOS/bare-metal）、是否使用 RPZC、shared memory 来源（IRAM/DDR/reserved-memory）和中断通知方式（mailbox 或 GPIO 方案）。

- Linux 重点确认 kernel defconfig、平台 DTS、`rpmsgN`/`rpzc_ctrlN` 和 reserved-memory。
- M57 QNX 重点确认 `kernel/osdrv/open_drv/ax_ipc/` 下的 `driver/cfg`、`driver/rpmsg`、`driver/rpzc`、`lib`，以及 EPT、IPCZC buffer、IRAM/DDR 和中断配置；AX637 不执行 QNX 核对流程。
- MCU/MCAL 重点确认 `SafetyIsland/mcal/mcal_drv/Ipc/`、`Ipc_zc/` 的静态配置、callback、ACK 和锁实现。
- RTOS 重点确认 `SafetyIsland/rt-thread/bsp/m57/drivers/ipc/` 的 `cfg/`、`rpmsg/`、`rpzc/` 配置、实际 endpoint/mailbox/shared-memory 和镜像中是否启用测试入口。

## Instructions

1. **读取事实来源**：先读 `reference/_index.md`。Linux、MCAL、RTOS 的公共事实读取 `reference/ax_ipc.md`，再按场景打开对应 docx 或补充 md；问题复盘读取 `reference/ax_ipc_FAQ.md`，按问题定位并引用本地章节；其中历史配置和建议须核对目标 SDK，不直接套用到其他平台。
2. **核对跨端契约**：确认 physical channel、endpoint local/remote address、name service、buffer name/size/方向、mailbox slot、destination core、shared-memory 地址和通知方式在两端一致。
3. **配置 Linux**：确认 `CONFIG_AXERA_MBOX`、`CONFIG_RPMSG_CHAR`、`CONFIG_RPMSG_CTRL`、`CONFIG_RPMSG_AXERA`；启用 RPZC 时增加 `CONFIG_RPZC_SERVICE_RPMSG` 与 `CONFIG_RPZC_CONTROLLER`。核对 DTS 的 `reg`、`memory-region`、`mboxes` 和可选 `ipc-gpio`。
4. **配置 M57 QNX**：仅 M57 使用此流程。先确认 `kernel/osdrv/open_drv/ax_ipc/` 的 driver、`lib/` 和 resource manager 已编入并启动；核对 `driver/cfg/Ipc_cfg.h/c` 中的 `UniqueId`、`LinkId`、`LocalAddr`、`RemoteAddr`、`NeedInform`、`EptName`、`RxEnable`、ring buffer，以及 `Ipc_zc_cfg.h/c` 中的 `EndpointIdx`、`BufferID`、`BufferName`、`BufferSize`。固定地址模式要求两端 `LocalAddr/RemoteAddr` 交叉匹配；`RL_ADDR_ANY` 必须配合 `NEED_NS` 和服务名。单个物理通道最多 20 个 EPT，endpoint 地址不能相同且须小于 1024。
5. **配置 M57 QNX 资源与通知**：仅 M57 使用此流程。当前工程默认 `IPC_ZC_BUFFER_BY_DDR=0`，IPCZC 使用 IRAM；切换 DDR 时同时修改 `ReservedMemory_cfg.h`/QNX reserved-memory、`AX_RESV_MEM_DDR_ADDR_IPCZC0`、`Ipc_zc_cfg.h` 和 MCU 端。当前 `IPC_GPIO_TRIGGER_IRQ_EN=1` 对应 GPIO + SPI slave CS/回主域 mailbox 方案；改用 mailbox 时，QNX 和 MCU 必须同步切换。可用 `pidin syspage=asinfo` 检查 reserved-memory 是否重叠。
6. **配置 MCU**：使用 `IpcInitial()`/`IpcZcWholeInitial()` 完成初始化，按静态配置注册 endpoint/buffer callback；发送前检查 `IpcEptLinkStatusCheck()` 或 `IpcZcLinkStatusCheck()`。
7. **使用 RPMsg**：Linux 通过 `/dev/rpmsg_ctrlX` 创建 endpoint，再在 `/dev/rpmsgX` 上 `read()`/`write()`；M57 QNX 使用 `lib/public/ax_rpmsg.h` 暴露的接口和 `sample_ipc_rpmsg` 验证驱动创建的 endpoint。地址需与对端交叉匹配，不能私自构造 UAPI ioctl。
8. **使用 RPZC**：创建同名 buffer，等待 `CHECK_AVAIL`，映射 payload 后提交 `TRANSMIT_BUF`；接收 `RECEIVE_BUF` 后先消费数据，再在 `need_ack` 时回复 ACK，完成后 destroy。M57 QNX 可使用 `sample_ipc_rpmsg -z 1 [-t n]` 验证 RPZC 生命周期。
9. **处理 reset 与并发**：远端 reset/remove 后重新检查 transport、name service、link status 和设备节点；不得继续使用失效 fd/mmap。接收端避免上一笔数据未消费就覆盖 buffer，并按 timeout/信号处理中断返回值。
10. **诊断与验证**：按“内核/驱动配置 → DTS/资源 → probe → RPMsg 枚举 → RPZC 生命周期 → MCU/RTOS 状态 → shared memory → reset → 锁实现”的顺序收集证据；M57 QNX 额外记录 resource manager、`pidin syspage=asinfo`、EPT 地址/name service、`sample_ipc_rpmsg` 输出，AX637 仅记录其实际 Linux/RTOS 侧证据；覆盖正向、超时、地址不匹配、buffer 未 ready、重复 name、ACK 和 reset 场景。

## Safety

- shared-memory 地址、mailbox slot、endpoint/buffer/service name 不一致会导致链路失败甚至破坏其他内存；修改前必须同时核对两端。
- 不得把 mailbox/GPIO 通知字段当成业务 payload；payload 分别位于 virtqueue 或 DMA buffer。
- 不得在 RPZC payload 尚未消费前回复 ACK，也不得在同步 ACK 完成前复用发送 buffer。
- 不得在 reset/remove 后假设旧 fd、mmap、endpoint 或 controller 仍有效。
- MCU 端默认锁可能为空实现；BareMetal、RTOS、AUTOSAR 下应由集成方确认 ring buffer 操作的并发保护。

## 平台矩阵

| 平台 id | 说明 | 资料入口 |
|---|---|---|
| `m57` | M57 Linux/QNX 与 SafetyIsland MCU 的 IPC/RPMsg/RPZC 公共规则 | `platforms/m57.md`、`reference/_index.md` |
| `ax637` | AX637/AX637R 非 QNX 场景；仅在有明确 board 差异时叠加，复用适用的 M57 Linux/MCU/RTOS 通信规则 | `platforms/ax637.md`、`reference/_index.md` |

新增平台：更新 `routing.yaml`、`platforms/<id>.md`、`reference/_index.md`（或新增实际来源声明）及对应 evals。
