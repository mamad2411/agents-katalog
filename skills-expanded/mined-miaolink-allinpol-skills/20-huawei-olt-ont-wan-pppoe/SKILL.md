---
name: 20-huawei-olt-ont-wan-pppoe
description: 规划、发现并校验台架华为 ONT EG8145X6-10 上由 华为 OLT（参考 R018） 经 profile/OMCI 下发的路由型 WAN PPPoE；不臆造语法，不持久化凭据。
---

# ONT 上的路由型 WAN PPPoE

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

将台架 ONT 从 bridge 基线迁到路由目标：EG8145X6-10 作为 PPPoE 客户端，从 BNG 获取地址，并按计划通过 NAT/DHCP/Wi-Fi 向 LAN 交付。

## 何时使用

规划或诊断 ONT 上的 Internet 路由型 WAN、WAN profiles、OMCI 下发、PPPoE、NAT、DHCP 或 LAN/Wi-Fi bindings 时使用。

## 前置条件

确认 MA5800V100R018/SPH507、EG8145X6-10 确切固件、台架 ONT、直至 ASR1001-X 的 VLAN 100、临时测试凭据、授权，以及回退到 bridge 的方案。

## 已确认命令

- [已确认] 本包中已有的 ONT、profiles、service-port 与 VLAN 相关 display。
- 尚无已确认命令用于在 ONT 上创建 WAN profile、路由型 WAN、PPPoE、NAT 或 DHCP。

## 发现类命令

- [推断] 在 CONFIG、GPON INTERFACE 及相关 profile 上下文中从 `?` 开始；执行后将每条查询原文登记为 [DISCOVERY]。
- [推断] 先发现 WAN/profile 查询命令，再发现创建语法。
- 在 R018 CLI 自身给出之前，不要建议 `ont wan-*`、`wan-profile` 或等价名称。

## 语法

尚无已确认的 WAN PPPoE 语法。需发现：可复用 profile 机制、route 模式、VLAN 100、PPPoE、支持的认证、NAT、DHCP LAN、ETH/Wi-Fi bindings、DNS/MTU，以及安全告知密钥的方式。

## 示例

操作员告知状态：台架 ONT 已按 bridge 授权。尚未在 CLI 确认的目标：路由型 ONT、VLAN 100 上的 WAN PPPoE、ASR1001-X 作为服务器/BNG、AAA/RADIUS 作为认证方。

## 预期结果

ONT 发起 PPPoE 会话，在 BNG 获 IP，建立 WAN 连通，并向 LAN/Wi-Fi 客户端交付地址/连通，且不暴露凭据。

## 已知错误

未提供 ONT 侧 WAN PPPoE 的字面错误。将 PADI/PADO/PADR/PADS、LCP、认证与 IPCP 记为不同阶段。

## 诊断

按序校验：已应用 WAN/profile → VLAN/GEM/service-port → BNG 上 PADI → PADO → PADR/PADS → LCP → PAP/CHAP → IPCP/IP → 路由/DNS → NAT/DHCP/LAN/Wi-Fi。在第一处失败停止。

## 依赖

ONT 固件、OMCI/厂商扩展支持、兼容 profile、VLAN 100、GEM 1、service-port 1000、上联、BNG 与 AAA。

## 风险

以 route 替换 bridge 可能中断台架、重复 NAT/DHCP、改变 LAN/Wi-Fi bindings，并将密钥持久化到 OLT/ONT 运行配置。

## 回滚

完整捕获 bridge 基线、profiles 与 bindings。预先校验移除路由型 WAN 并恢复 bridge 的语法；不要依赖恢复出厂。

## 安全规则

仅使用测试凭据；执行时经安全通道接收密钥；屏蔽输出；不要把真实值写入示例命令、Skill、Git、PR、注释或日志；若平台支持，优先引用/密钥注入。

## 禁止事项

发现过程中不得使用真实签约用户凭据；不得假定 Ethernet service profile 即配置 WAN；不得执行其他 release 的语法；不得在台架外改动在线 ONT。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 操作员告知的台架 ONT 状态与目标。
- 一手 CLI 证据：MA5800V100R018，patch SPH507。
- 华为 ONT Web Page Reference 及门户上的 EG8145X6 文档。
- 华为 PPPoE 文档：客户端/服务器、发现、会话与认证。
- 以 R018 CLI 与 ONT 固件为准；其他版本须标为 [版本不同]。
