---
name: 01-huawei-olt-baseline
description: 在诊断、开通或变更前登记并核对 Huawei OLT 的真实基线，参考 release MA5800V100R018 SPH507（其他机型须先核对）。
---

# 华为 OLT 基线

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

在不改动 OLT 的前提下，建立身份、硬件、寻址与已知对象。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

只读访问；确认 release 与 patch；仅当后续步骤会改配置时才需要变更窗口。

## 已确认命令

- [已确认] `display version` 于华为 OLT（参考 MA5800-X7 / MA5800V100R018C00/SPH507）；确认 `<cr>` 并处理手动分页。
- [已确认] `display port vlan 0/1/0`
- [已确认] `display port vlan 0/8/0`
- [已确认] `display current-configuration | include ont-lineprofile`
- [已确认] `display current-configuration | include ont-srvprofile`
- [已确认] `display service-port all`

## 发现类命令

- [DISCOVERY] 对矩阵未列出语法的板卡、端口或版本查询，在当前模式下使用 `?`。
- [DISCOVERY] `display board 0`（或本机 frame 等价）— 机框/槽位巡检细节见 `27-huawei-olt-board-inventory`。

## 语法

勿泛化 F/S/P：PON `0/1/0`、ONT `0`、上联 `0/8/0` 为已观测基线。

## 示例

硬件：0/1 H907CGHF；0/8 H901MPLA Active_normal；0/9 H901MPLA Standby_normal；0/10-11 H901PILA。VLAN 10 管理，VLAN 100 客户。

## 预期结果

release 与 patch 已确认；`${UPLINK_VLANS}` 在上联；`${PON_VLANS}` 在 PON；`${MGMT_VLANIF}` 带 `${MGMT_PREFIX}`；路由经 `${MGMT_GATEWAY}`。

## 已知错误

release、板卡状态、VLAN 或路由任一不一致，均使基线不可自动套用。

## 诊断

将读到的状态与基线对比，在第一处不一致处停止。

## 依赖

经 VLAN 10 与上联 0/8/0 进行管理访问。

## 风险

基于错误槽位/release 的结论可能导致业务中断。

## 回滚

只读不适用回滚。后续若有变更，须原样记录变更前状态。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

勿改动 VLAN 10、Vlanif10、默认路由或默认 profiles。


## 配置保存（PERSIST）

本 Skill 默认只读/发现，**不**执行全局 save。落盘为**可选**：仅当用户明确要求时，改用 30-huawei-olt-config-save 并取得 PERSIST 授权。禁止在查询后自动 save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
