---
name: 11-huawei-olt-vlan
description: 在 华为 OLT（参考 R018） 的 PON 与上联上查询并校验客户 VLAN 与管理 VLAN，同时保持管理连通性。
---

# 华为 OLT VLAN

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

保证 VLAN 100 的 L2 连续性，且不触碰 VLAN 10。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

方案：VLAN 10 管理，VLAN 100 客户；上联 0/8/0。

## 已确认命令

- [已确认] `display port vlan 0/1/0`
- [已确认] `display port vlan 0/8/0`
- [已确认][破坏性] `vlan 10 smart`；`vlan 100 smart`
- [已确认][破坏性] `vlan desc 10 description "gerencia"`
- [已确认][破坏性] `port vlan 10 0/8 0`；`port vlan 100 0/8 0`

## 发现类命令

- [DISCOVERY] 在任何关联/移除变体之前，先用 `?`。

## 语法

观测到 PON 0/1/0 带有 VLAN 100。上联 0/8/0 带有 1、10、100，native VLAN 为 1。

## 示例

在排查 BNG 之前，先在两侧校验 VLAN 100。

## 预期结果

VLAN 100 存在于 PON 与上联；管理面完好。

## 已知错误

任一侧缺失都会中断路径；未提供特定字面错误。

## 诊断

按 PON → VLAN → 上联 排查；在第一个缺失点停下。跨厂商解释层见 `diagnosis-service-vlan`（意图 `vlan不通`）。

## 依赖

service-port 1000 与上联 0/8/0。

## 风险

变更 VLAN 10/native VLAN/路由可能导致管理中断。

## 回滚

记录 membership 与 native VLAN；仅执行已发现语法的回退。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

未经授权不要变更 VLAN 10、Vlanif10 或 native VLAN 1。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
