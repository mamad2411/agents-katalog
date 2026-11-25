---
name: sdk-bsp-can-safety
description: 诊断 M57 Linux/QNX 项目 Safety 侧 AUTOSAR MCAL CAN/CAN FD 问题。仅适用于 M57 Safety MCAL；AX637/AX637R Safety 侧 RTT CAN、主 CPU 原生 CAN 和 baremetal CAN 不适用。
metadata:
  version: 1.0.0
  tags: [m57, can, canfd, autosar, mcal]
---

# M57 Safety MCAL CAN 诊断

本 skill 只提供诊断入口和证据路由。实现事实从当前 SDK 源码、生成配置和用户手册读取；[M57 CAN 常见问题解决思路](references/M57%20CAN%20常见问题解决思路.md)仅作为问题经验 reference，不作为实现事实。

## S0：确认输入

收集芯片、主项目 OS、CAN 所属侧、SDK 版本、controller、现象、首个异常日志和目标生成配置。无法确认 CAN 所属侧时，先澄清该问题属于 Safety MCAL 还是主 CPU CAN。

处理日志、配置和截图时只保留诊断所需字段。保留必要的 CAN ID、错误状态和时序信息；在落盘、归档或加入 eval 前，移除账号或凭据、个人主目录、客户/项目标识及无关的设备、主机或网络标识。

## S1：确认范围

读取[平台范围](references/平台范围.md)。仅在芯片为 M57 且问题位于 Safety 侧 AUTOSAR MCAL CAN 时继续。M57 主项目可以是 Linux 或 QNX。

## S2：定位实现

读取[代码与文档索引](references/代码地图-mcal.md)，在当前 SDK 中核对相关 API、IRQ、CanIf callback、插件配置和生成配置。不得仅凭文件名或 FAQ 推断目标版本行为。

## S3：读取对应资料

- API 或模块能力：读取源码、生成配置以及 `SafetyIsland/mcal/plugins/Can/Doc/AXERA-M57 MCAL CAN UM.docx`。
- EB 配置、MB/RAM 分区、RX MB/Enhanced FIFO、FD CBT、RX 过滤或 RX DMA：读取[M57 MCAL CAN EB 配置说明](references/M57%20MCAL%20CAN%20EB%20配置说明.md)，再按[代码与文档索引](references/代码地图-mcal.md)中的“EB 配置核对矩阵”检查 `Can.xdm`、生成器和目标生成配置。
- Bus-Off、ISR、TX 失败或 Enhanced FIFO 问题：读取[M57 CAN 常见问题解决思路](references/M57%20CAN%20常见问题解决思路.md)的对应编号，并按[代码与文档索引](references/代码地图-mcal.md)中的“FAQ 核对矩阵”回查目标源码和生成配置。回答中明确区分 FAQ 建议与目标项目事实。

## S4：形成结论

回答中区分：源码已确认、生成配置已确认、用户手册记载、FAQ 建议和待补证据。证据不足时给出需要核对的具体文件、配置项或运行现象，不把假设写成根因。

## S5：验证

使用用户提供的目标构建产物或现场结果验证结论。修改配置或源码前，先说明修改对象和预期验证结果。

## 输出格式

需要落盘结论时（如 CI 评测或客户要求归档），将结果写入 `result.md`，使用以下固定小节：

```text
结论：<支持|不支持|证据不足>
判断依据：<芯片、主项目 OS、CAN ownership、Safety 侧 CAN 框架>
引用：<引用的 reference 及小节，或待补证据说明>
```

结论只能取支持、不支持、证据不足之一；S1 平台门场景依据必须同时给出芯片和 Safety 侧 CAN 框架。平台范围判断请求使用“支持/不支持”作为结论；故障诊断请求在平台门通过但缺少根因证据时，首行使用“结论：证据不足”，将平台适用性写入判断依据，并列出最小补采清单。平台支持不代表根因已确认。对话式问答不强制此格式。

## S6：沉淀

只有经过实际项目验证且能注明来源的结论才能加入 reference 或 eval。Golden Case 只收录合成数据，或经授权、脱敏且最小化的复现证据；不得收录原始客户日志、凭据或可识别客户、人员和环境的信息。

## 源码位置

见[代码与文档索引](references/代码地图-mcal.md)。

## 核心知识

- CAN Driver 对外 API 和实现位于 `SafetyIsland/mcal/mcal_drv/Can/`。
- CanIf callback 位于 `SafetyIsland/mcal/mcal_drv/CanIf/`。
- EB 插件位于 `SafetyIsland/mcal/plugins/Can/`，生成配置位于 `SafetyIsland/mcal/mcal_config/generated/`。
- M57 MCAL CAN 用户手册位于 `SafetyIsland/mcal/plugins/Can/Doc/`。
- M57 MCAL CAN 的 EB 配置补充说明位于 [`references/M57 MCAL CAN EB 配置说明.md`](references/M57%20MCAL%20CAN%20EB%20配置说明.md)。

## 信息收集清单

- M57 项目的主 OS，以及 CAN 是否属于 Safety 侧 MCAL。
- SDK/MCAL 版本或提交号、controller 和复现步骤。
- 首个异常日志及对应时间点。
- `Can_Cfg.h`、`Can_Cfg.c`、`Can_PBcfg.c` 中与问题 controller 相关的配置。
- EB 中相关 controller、RAM block、hardware object、bit timing、filter 和 DMA 配置截图或导出值。
- 若涉及总线通信，提供对端配置或总线分析结果。

## 常见问题排查表

当前只有以下四类问题具有所提供 FAQ 的直接依据。具体建议保留在 reference 中，核对路径见[代码与文档索引](references/代码地图-mcal.md)，不在入口文件重复。

| 现象 | 读取依据 | 操作边界 |
|---|---|---|
| Bus-Off | 第 1 节 | controller、处理模式、自动恢复配置、通知路径、错误计数 |
| ISR 处理时间过长 | 第 2 节 | controller、IRQ 路径、回调内容、时序或负载证据 |
| TX 失败 | 第 3 节 | `Can_Write()` 返回值、HTH、确认回调、错误状态、位时序和对端证据 |
| RX Enhanced FIFO 丢帧 | 第 4 节 | FIFO/处理模式/overflow callback 配置、接收计数与 overflow 证据 |

## 限制与约束

- 支持 M57 Linux/QNX 项目的 Safety 侧 AUTOSAR MCAL CAN。
- 不支持 AX637/AX637R；其 Safety 侧使用 RTT RTOS CAN 框架。
- 不支持主 CPU Linux SocketCAN、QNX 原生 CAN、SafetyIsland baremetal CAN 或其他非 AUTOSAR MCAL 软件栈。
- 不把 FAQ、样例配置或其他 SDK 版本的行为直接当作目标项目事实。
- EB 配置说明中的工程建议保留其文档来源；应用到目标工程前核对目标 SDK、硬件版本和生成结果。

## Sources

- 用户提供的平台范围说明。
- [`references/M57 CAN 常见问题解决思路.md`](references/M57%20CAN%20常见问题解决思路.md)。
- [`references/M57 MCAL CAN EB 配置说明.md`](references/M57%20MCAL%20CAN%20EB%20配置说明.md)。
- [`references/代码地图-mcal.md`](references/代码地图-mcal.md) 中列出的当前 SDK 文件。
- `SafetyIsland/mcal/plugins/Can/Doc/AXERA-M57 MCAL CAN UM.docx`。
