---
name: 18-huawei-olt-cleanup
description: 审计并仅删除 华为 OLT 上的孤立对象，须显式确认、参考、bind-times、影响评估与回滚。
---

# 华为 OLT 清理

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

避免对象堆积，同时不删除在用或默认对象。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

变更窗口、删除授权、完整清单与文本备份。

## 已确认命令

- [已确认] `display dba-profile all`
- [已确认][破坏性] `dba-profile delete profile-id 100`
- [已确认][破坏性] `dba-profile delete profile-id 101`

## 发现类命令

- [DISCOVERY] 发现其他类型的删除语法；不要外推 `dba-profile delete`。
- [DISCOVERY] 孤立 service-port / ONT 注册清理顺序见 `26-huawei-olt-ont-lifecycle`（先流后 ONT）。
- [DISCOVERY] TR069 profile、流量表、组播成员清理须本机 `?`，并分别参见 skill 28/29 与 COMMAND-MATRIX。

## 语法

上述两次已确认删除后，ID 100 与 101 不再出现。

## 示例

删除 DBA 前：查询 profile、bind-times、line profiles/T-CONT 以及 `display dba-profile all`。  
删户/销号：勿仅删 DBA；按 lifecycle 清 service-port 与 ONT。

## 预期结果

仅显式批准的对象不再出现；依赖方保持完整。

## 已知错误

`does not exist` 须确认 ID/上下文；`already existed` 不能证明可查询性。

## 诊断

双向定位引用，并确认零使用。

## 依赖

Line profiles、T-CONTs、ONTs 与 service-ports；ONT 生命周期见 `26-huawei-olt-ont-lifecycle`。

## 风险

删除具有破坏性，可能中断多台 ONT。

## 回滚

重建需要精确参数与可用 ID；删除前登记全部信息。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不得自动删除；不得删除默认对象；不得仅凭名称/ID 判断。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
