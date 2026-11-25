---
name: huawei-olt-decision-tree
description: 对华为 OLT 做端到端排障直至 PPPoE/AAA，并在第一处失败强制停止。
---

# 华为 OLT 决策树

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

在前一层失败时，禁止改动后续层次。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

基线、范围与只读访问。ONT 反复 offline / LOS / Dying Gasp 先读 `diagnosis-onu-flapping`，本树从「是否在线」之后的业务层次展开。

## 已确认命令

- [已确认] 各节点仅使用本包中的 display；无已确认命令的节点必须做 discovery。

## 发现类命令

- [DISCOVERY] 在负责该节点的设备上用 `?`，不要推断语法。

## 语法

固定 20+ 节点序列见 `HUAWEI-OLT-DECISION-TREE.md`。节点 18/19：先确认 ONT WAN route，再查 PADI/PADO/PADR/PADS、LCP、认证与 IPCP。

## 示例

若节点 4 未找到 ONT，停止；不要创建 service-port，也不要改 BNG。

## 预期结果

隔离第一处失败、留下证据，并给出下一条只读动作。

## 已知错误

跳层会导致误诊。

## 诊断

严格按树执行；否/未知即停。

## 依赖

`HUAWEI-OLT-DECISION-TREE.md` 与相关 Skills。

## 风险

在失败节点继续写配置。

## 回滚

本树以只读为主；若已写入，转 safe-change/rollback。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要跳节点；不要在未知处推断命令。


## 配置保存（PERSIST）

本 Skill 默认只读/发现，**不**执行全局 save。落盘为**可选**：仅当用户明确要求时，改用 30-huawei-olt-config-save 并取得 PERSIST 授权。禁止在查询后自动 save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
