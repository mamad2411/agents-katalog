---
name: 06-huawei-olt-ont-autofind
description: 在华为 OLT 上发现 GPON ONT，受控启用 autofind，并在开通前校验 SN、型号与端口。
---

# ONT Autofind

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

定位并识别 ONT，避免与其他 PON 上的设备混淆。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

ODN 已连接；PON 正确；已获启用 autofind 的授权。

## 已确认命令

- [已确认] `display ont autofind all`
- [已确认][破坏性] `interface gpon 0/1`
- [已确认][破坏性] `port 0 ont-auto-find enable`

## 发现类命令

- [DISCOVERY] 若 release 不同，在 GPON 上下文使用 `port ?`。

## 语法

enable 在 `config-if-gpon-0/1` 上下文、端口 0 执行。

## 示例

参数化示例：`${PON_FSP}`，SN `${ONT_SERIAL}`，vendor `${ONT_VENDOR}`，型号 `${ONT_MODEL}`，MAC `${ONT_MAC}`，NNI `${ONT_NNI_RATE}`。

## 预期结果

`display ont autofind all` 返回正确 ONT；最初可能返回无结果。

## 已知错误

[错误] `Failure: The automatically found ONTs do not exist` 表示无结果，不是语法失败。

## 诊断

检查 enable、PON/ODN、供电、激光、距离与 SN；参考华为官方自动发现失败指南。

## 依赖

槽位 0/1 的板卡 H907CGHF 与 PON 0。

## 风险

Autofind 可能暴露未授权 ONT；启用并不等于开通。

## 回滚

若策略要求，先用 `?` 发现并校验 disable 命令，再执行。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要仅因出现就添加 ONT；须校验 SN 与位置。


## 配置保存（PERSIST）

本 Skill 默认只读/发现，**不**执行全局 save。落盘为**可选**：仅当用户明确要求时，改用 30-huawei-olt-config-save 并取得 PERSIST 授权。禁止在查询后自动 save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
