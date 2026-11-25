---
name: 09-huawei-olt-gem-tcont
description: 分析 华为 OLT（参考 R018） 上 GPON line profile 中 DBA、T-CONT 与 GEM 的关系，并避免使用未确认的 GEM 命令。
---

# GEM 与 T-CONT

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

在创建或诊断业务之前，先校验 GPON 传输路径：T-CONT → GEM → GEM mapping → service-port。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

已列出 line profile 详情与 DBA。

## 已确认命令

- [已确认][破坏性] `tcont 0 dba-profile-id 200`；[已确认][破坏性] `tcont 0 dba-profile-id 201`

## 发现类命令

- [DISCOVERY] `tcont 0 ?`；用 `?` 发现全部 GEM 语法，因为没有任何 GEM 创建命令被提供为已确认。

## 语法

profile 100 的 T-CONT 0 使用 DBA 201；GEM Index 1 为 ETH，encrypt on，cascade off，queue 0。若 profile 处于 `mapping-mode VLAN`，GEM 需要服务 VLAN/flow 的显式 mapping；仅 GEM 与 service-port 为 `up`，并不能单独证明转发。

## 示例

路径：ONT → T-CONT 0/DBA 201 → GEM 1 → GEM mapping VLAN/flow → service-port 1000 → VLAN PON/uplink → BNG。

## 预期结果

line profile 显示与 service-port 的 VLAN/flow 兼容的 T-CONT、GEM 与 mapping；当 ONT 尝试该业务时，service-port 有流量计数。

## 已知错误

本场景下 Type 4 与 OMCI 不兼容；DBA Max 不兼容可能阻止 ONT 添加。

## 诊断

核对 DBA、T-CONT 关联、GEM index/service type、mapping VLAN/flow、`binding times`、service-port 与 ONT 能力。勿将 `Match state: mismatch` 自动当作转发阻塞原因：将该能力/service profile 差异作为独立排查线索。

## 依赖

DBA 201、line profile 100、service-port 1000。

## 风险

更换 DBA/T-CONT 会影响上行；错误的 GEM 会中断业务流。

## 回滚

恢复已记录的先前关联；变更前后均做校验。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

勿编造 `gem add` 命令；勿混淆 T-CONT 与 GEM。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
