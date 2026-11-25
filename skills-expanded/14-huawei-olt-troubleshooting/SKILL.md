---
name: 14-huawei-olt-troubleshooting
description: 分层诊断 华为 OLT 故障，在任何变更之前先使用 display 与字面错误信息。
---

# 华为 OLT 排障

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

停在第一个故障点，并形成可验证的假设。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

加载 `huawei-olt-decision-tree` 与 `15-huawei-olt-error-database`。频繁掉线的**解释层**见跨厂商 `diagnosis-onu-flapping`（本 Skill 仍负责华为取证命令）。

## 已确认命令

- [已确认] `display ont autofind all`；`display ont info summary 0/1/0`；`display service-port 1000`；`display port vlan 0/1/0`；`display port vlan 0/8/0`。

## 发现类命令

- [DISCOVERY] 仅在故障点使用 `?` 以扩大证据。

## 语法

按物理→GPON→profiles→T-CONT→GEM→GEM mapping VLAN/flow→同一 GEM 上的 service-port→VLAN PON/上联→BNG→AAA 顺序做只读。在 `mapping-mode VLAN` 下，不要仅因 GEM 存在就推断会转发：须登记与业务 VLAN 兼容的显式 mapping。

## 示例

service-port down：不要改 AAA；ONT 不存在：不要重建 service-port。

## 预期结果

一个首发故障、证据、影响、假设与下一步安全只读。

## 已知错误

查阅 `HUAWEI-OLT-ERROR-DATABASE.md` 中的八条字面错误。

## 诊断

应用 21 步决策树并停下。签名「ONT online + service-port `up` 无计数 + WAN PPPoE `Disconnected` + BNG 无 PADI/PADR」要求优先检查 GEM 的 mapping VLAN/flow。将 `Match state: mismatch` 作为并行线索，直到有证据表明影响转发。

## 依赖

基线，以及所分析各层设备的访问。

## 风险

同时做多项变更会掩盖原因并扩大事故。

## 回滚

没有变更前状态与回退准则时，不要开始变更。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要散弹式排障；不要改动后续层。


## 配置保存（PERSIST）

本 Skill 默认只读/发现，**不**执行全局 save。落盘为**可选**：仅当用户明确要求时，改用 30-huawei-olt-config-save 并取得 PERSIST 授权。禁止在查询后自动 save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
