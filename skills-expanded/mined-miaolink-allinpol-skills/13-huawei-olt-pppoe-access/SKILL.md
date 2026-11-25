---
name: 13-huawei-olt-pppoe-access
description: 诊断 PPPoE：EG8145X6-10 以路由模式作为客户端，华为 OLT 提供 L2 传输/OMCI 开通，ASR1001-X 作为 BNG/AAA。
---

# PPPoE 接入

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

保持正确的职责划分，并按层定位 PPPoE 故障。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

VLAN 100 连续到 BNG；service-port up；台架 ONT 已应用 WAN route；具备相应系统访问。

## 已确认命令

- [已确认] 在 OLT 上仅使用本包中已确认的 ONT、service-port 与 VLAN 的 display。

## 发现类命令

- [推断] 在 R018 上用 `?` 发现如何查询与开通 ONT 的 WAN PPPoE；随后将已执行的查询登记为 [DISCOVERY]。
- [DISCOVERY] 任何已在 OLT/BNG 执行过的具体 PPPoE 命令，应记录到对应设备文档中。

## 语法

架构：EG8145X6-10（route/NAT/DHCP/Wi-Fi 与 PPPoE 客户端）→ GPON → T-CONT → GEM → GEM mapping VLAN/flow → service-port → VLAN → 上联 → ASR1001-X（PPPoE 服务器/BNG）→ AAA/RADIUS。MA5800 传输流量并可通过 OMCI 开通 WAN；它不以客户端身份终结会话。

## 示例

若 PADI 到达 BNG 但无 PADO，排查 BNG；若认证失败，排查 AAA，而非 DBA。

## 预期结果

在前置各层均正常后，客户端在 BNG 认证并获得 IP。

## 已知错误

未提供 PPPoE 字面错误；不要编造诊断。

## 诊断

校验 ONT 上的 WAN/profile；T-CONT/GEM/mapping/service-port/VLAN/上联；随后 PADI、PADO、PADR/PADS、LCP、PAP/CHAP、IPCP、IP、路由/DNS、NAT/DHCP 与 LAN/Wi-Fi。若 WAN 为 `Disconnected`、service-port `up` 但计数为零且 BNG 无 PADI/PADR，优先检查 GEM 的 mapping VLAN/flow。仅在会话/IP 正常后才评估 NAT/CGNAT。

## 依赖

ONT、GPON、GEM、service-port、VLAN、上联、BNG 与 AAA。

## 风险

凭据与 AAA 日志敏感。

## 回滚

恢复 ONT 的 bridge 基线，并用先前已校验的语法移除 WAN route；BNG 变更有独立方案。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要让 MA5800 充当 PPPoE 客户端。若 OLT/NMS 通过 OMCI 向 ONT 下发凭据，使用测试凭据与安全通道，对返回做脱敏，且切勿将密钥持久化到 Skills、Git、示例或日志中。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
