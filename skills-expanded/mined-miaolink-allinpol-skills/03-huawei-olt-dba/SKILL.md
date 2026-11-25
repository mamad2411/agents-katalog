---
name: 03-huawei-olt-dba
description: 在 华为 OLT（参考 R018） 上查询、创建、校验与诊断 DBA profiles，含 OMCI 限制、bind-times 与 ID 不一致问题。
---

# 华为 OLT DBA Profiles

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

依据设备证据与 OMCI 兼容性处理 DBA。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

执行 `display dba-profile all`；先查询再选 ID；了解 ONT 能力与参考资料。

## 已确认命令

- [已确认] `display dba-profile all`
- [已确认] `display dba-profile profile-id 100`（也可用于 101、102、200 与 201）
- [已确认][破坏性] `dba-profile add profile-id 101 profile-name "DBA-OMCI-2G" type5 fix 128 assure 128 max 2000000`
- [已确认][破坏性] `dba-profile add profile-id 102 profile-name "DBA-OMCI-2G" type5 fix 1000 assure 1000 max 2000000`
- [已确认][破坏性] `dba-profile add profile-id 103 profile-name "DBA-OMCI-2G" type5 fix 2048 assure 2048 max 2048000`
- [已确认][破坏性] `dba-profile add profile-id 200 profile-name "TESTE" type5 fix 2048 assure 2048 max 2048000`

## 发现类命令

- [DISCOVERY] `dba-profile add profile-id ?` 以及 discovery Skill 中已登记的递进查询。

## 语法

观测到的 Type 5：`fix <kbps> assure <kbps> max <kbps>`。在目标 release 上用 `?` 校验取值范围。

## 示例

最终观测到的 profile 200：DBA-VLAN100-2G-OMCI，Type 5，2048/2048/2048000，best-effort。Profile 201：DBA-OMCI-GPON-1G，2048/2048/1024000，bind-times 1。

## 预期结果

profile 可查询且数值与计划一致；曾观测到 profile 101 为 128/128/2000000，尽管在其他上下文中低于最小值会被拒绝。

## 已知错误

[错误] `Failure: OMCI must not use type4 DBA-profile`；[错误] `Failure: The bandwidth of OMCI can't be less than 1Mbps`；102 不一致：先报 `already existed`，随后又报 `does not exist`。

## 诊断

不要因报错就假定对象存在。重新查询列表、ID、bind-times、T-CONT 与 ONT 限制。拥塞/争用解释层见 `diagnosis-pon-congestion`（意图 `pon拥塞`）。

## 依赖

Line profile、T-CONT OMCI、ONT 能力。

## 风险

Max 不兼容会阻止 `ont add`；修改已绑定的 DBA 会影响订户。

## 回滚

先创建兼容的新 profile 并回退关联，再考虑删除；切勿自动删除。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要在 T-CONT OMCI 上使用 Type 4；不要未经诊断就降低 DBA；不要凭假设复用 ID。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
