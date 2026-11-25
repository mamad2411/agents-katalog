---
name: 08-huawei-olt-ont-status
description: 在 华为 OLT（参考 R018） 上查看 GPON ONT 的状态、身份、距离与光功率，不改动配置。
---

# ONT 运行状态

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

确认 ONT 存在且在正确的 F/S/P 上 online。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

已知 F/S/P；具备只读访问。

## 已确认命令

- [已确认] `display ont info summary 0/1/0`

## 发现类命令

- [DISCOVERY] `display ont info summary ?`。
- [DISCOVERY] `display ont wan-info ...`、`display ont version ...`、`display mac-address port ... ont ...`、`display ont optical-info ...`（API 工程常用；本机须先 `?`）。
- [DISCOVERY] `display ont info by-sn <SN>` — 迁机/重开定位。

## 语法

使用完整 F/S/P。本上下文中 `display ont info 0/1` 无效。

## 示例

参数化示例：ONT `${ONT_ID}` online，SN `${ONT_SERIAL}`，型号 `${ONT_MODEL}`，距离 `${ONT_DISTANCE}`，Rx/Tx `${ONT_RX_DBM}`/`${ONT_TX_DBM}`。

## 预期结果

total 1、online 1，且身份一致。

## 已知错误

[错误] `display ont info 0/1` 被拒绝；[错误] `Failure: The ONT does not exist`。

## 诊断

确认 F/S/P 与 ONT-ID、autofind、开通、供电与光路。光功率查询走 Capability `onu_optical_power`；判断光衰走 `diagnosis-onu-optical-power`；频繁掉线走 `diagnosis-onu-flapping`。

## 依赖

ONT 已添加在 PON 0/1/0。

## 风险

在无文档化光模块门限时解读功率，可能导致错误诊断。

## 回滚

不适用。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要仅因 online 就判定 ONT 健康；须关联业务与光功率。


## 配置保存（PERSIST）

本 Skill 默认只读/发现，**不**执行全局 save。落盘为**可选**：仅当用户明确要求时，改用 30-huawei-olt-config-save 并取得 PERSIST 授权。禁止在查询后自动 save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
