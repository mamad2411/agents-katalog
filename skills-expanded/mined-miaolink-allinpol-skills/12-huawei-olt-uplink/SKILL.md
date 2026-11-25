---
name: 12-huawei-olt-uplink
description: 校验上联 0/8/0、其上 VLAN 以及到 BNG 的连通性，不改动管理面，也不假设未观测到的命令。
---

# 华为 OLT 上联

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

确认 VLAN 100 离开 OLT，且 VLAN 10 仍保持管理连通。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

任何变更前具备备用/带外访问；与 BNG 侧协调。

## 已确认命令

- [已确认] `display port vlan 0/8/0`；[已确认][破坏性] `port vlan 10 0/8 0`；[已确认][破坏性] `port vlan 100 0/8 0`

## 发现类命令

- [DISCOVERY] 用 `?` 发现 H901MPLA 物理状态相关命令；未提供任何已确认命令。

## 语法

观测到的上联：槽位 0/8 H901MPLA Active_normal，端口 0，VLAN 1/10/100，native 1。

## 示例

将 0/8/0 上的 VLAN 100 与 ASR1001-X 上对应的子接口/bridge 关联对照。对端若是华为 VRP 交换机，交叉 `36-huawei-switch-vlan` / `37-huawei-switch-eth-trunk`（DISCOVERY）。

## 预期结果

板卡正常且 VLAN 存在；连通性也在 BNG 侧得到校验。

## 已知错误

未提供上联字面错误；在行动前记录任何新的返回信息。

## 诊断

板卡 → 端口 → VLAN → 远端链路 → BNG。

## 依赖

H901MPLA、VLAN、线缆与 ASR1001-X。

## 风险

远程变更可能导致管理面与客户业务同时丢失。

## 回滚

要求带外方案与变更前状态；不要临时拼凑。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要通过 `${MGMT_GATEWAY}` 或 `${MGMT_VLANIF}` 变更默认路由。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
