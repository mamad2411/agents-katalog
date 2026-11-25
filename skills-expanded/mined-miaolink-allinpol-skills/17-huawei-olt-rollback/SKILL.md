---
name: 17-huawei-olt-rollback
description: 准备并执行受控的 华为 OLT 变更回滚，按逆序恢复对象并校验依赖。
---

# 华为 OLT 回滚

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

回到上一已知状态，且不扩大影响范围。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

先前文本快照、经 `?` 校验的反向命令、中止准则与授权。

## 已确认命令

- [已确认] 使用本包中的 display 校验状态；不得推断任何通用 undo/delete 命令。

## 发现类命令

- [DISCOVERY] 在确切上下文中发现 `undo`/`delete` 语法，再进入变更窗口。

## 语法

典型逆序：业务 → binding → 新建 profiles；保留共享/默认对象。

对 GEM mapping，回滚只能针对新建的 GEM 与 mapping-index。先在确切上下文发现 `undo gem mapping <GEM_ID> <MAPPING_INDEX>` 形式，并确认该索引对应刚加入的 VLAN/flow；未经显式授权不得使用全局 `save`。

## 示例

若新建 service-port 失败，仅在确认索引与语法后再删除；随后再评估 ONT/profile。

## 预期结果

状态与基线一致，管理可达，原业务已恢复。

## 已知错误

若回退被拒绝，停止并重新核对对象/引用。

## 诊断

对比变更前后 display；不要盲目重复执行。

## 依赖

已演练的回退方案、备用访问路径与 binding 清单。

## 风险

若 ID 被共享，破坏性回滚可能比原变更更糟。

## 回滚

本流程本身即是回滚；保留升级/上报计划。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不得使用未确认命令，也不得删除默认 profile。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
