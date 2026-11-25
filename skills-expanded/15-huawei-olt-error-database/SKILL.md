---
name: 15-huawei-olt-error-database
description: 解读 华为 OLT（参考 R018） 上观测到的字面错误，并选择安全校验，不假设对象状态。
---

# 华为 OLT 错误库

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

将消息映射为：诊断 → 只读动作。

机读薄索引：[registries/errors/v1/errors.yaml](../../registries/errors/v1/errors.yaml)。权威全文仍是本库根目录 `HUAWEI-OLT-ERROR-DATABASE.md`。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

原样复制错误文本、模式与命令。

## 已确认命令

- [已确认] 使用 `HUAWEI-OLT-ERROR-DATABASE.md` 中指向的 display。

## 发现类命令

- [DISCOVERY] 仅用 `?` 发现缺失语法。

## 语法

登记时不要规范化或翻译错误文本。

## 示例

`already existed` 并不能证明 `display ... profile-id` 一定成功。

## 预期结果

错误已分类、假设受约束，且校验为非破坏性。

## 已知错误

八条规范消息见全局文档。

## 诊断

关联上下文、ID、references/bind-times 与第一个失败层。

## 依赖

CLI 命令与决策树。

## 风险

仅凭消息行动可能删除错误对象。

## 回滚

无自动动作；每项纠正都必须有回滚。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要把错误当作创建、缩减或删除的授权。


## 配置保存（PERSIST）

本 Skill 默认只读/发现，**不**执行全局 save。落盘为**可选**：仅当用户明确要求时，改用 30-huawei-olt-config-save 并取得 PERSIST 授权。禁止在查询后自动 save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
