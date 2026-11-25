---
name: 02-huawei-olt-cli-discovery
description: 在 Huawei OLT 上用 `?` 发现 CLI 语法，再建议未确认命令，或处理其他 release/上下文。
---

# 华为 OLT CLI 发现

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

教授增量语法发现，禁止凭空编造命令。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

处于正确模式；当命令树到达具体动作时，使用测试用 ONT/profile。

## 已确认命令

- [已确认] `display ont-lineprofile gpon all detail`
- [已确认] `display ont-lineprofile gpon all`
- [已确认] `display ont-srvprofile gpon all`
- [已确认] `display dba-profile all`
- [已确认] `display dba-profile all detail`
- [已确认] `display service-port all`

## 发现类命令

- [待验证] `display current-configuration ?` 仅枚举当前观测 CLI 提供的选项；本步不执行任何过滤
- [DISCOVERY] `ont-lineprofile gpon profile-id ?`
- [DISCOVERY] `dba-profile add profile-id ?`
- [DISCOVERY] `dba-profile add profile-id 200 profile-name "TESTE" type5 fix ?`
- [DISCOVERY] `dba-profile add profile-id 101 profile-name "DBA-OMCI-2G" type5 fix 128 ?`
- [DISCOVERY] `dba-profile add profile-id 101 profile-name "DBA-OMCI-2G" type5 fix 128 assure ?`
- [DISCOVERY] `dba-profile add profile-id 101 profile-name "DBA-OMCI-2G" type5 fix 128 assure 128 ?`
- [DISCOVERY] `tcont 0 ?`
- [DISCOVERY] `ont add ?`
- [DISCOVERY] `ont add 0 ?`
- [DISCOVERY] `ont add 0 0 sn-auth ?`
- [DISCOVERY] `ont add ${PON_PORT} ${ONT_ID} sn-auth ${ONT_SERIAL} ?`
- [DISCOVERY] `ont add ${PON_PORT} ${ONT_ID} sn-auth ${ONT_SERIAL} omci ?`
- [DISCOVERY] `ont-port ?`
- [DISCOVERY] `ont-port eth ?`
- [DISCOVERY] `port ?`
- [DISCOVERY] `port vlan ?`
- [DISCOVERY] `port vlan eth ?`
- [DISCOVERY] `port vlan eth 1-4 ?`
- [DISCOVERY] `display ont info summary ?`

## 语法

每次只追加一个 token；记录选项与 `<cr>`；未经成功执行，切勿把显示的选项提升为已确认命令。

## 全局备份发现

1. 确认目标华为 OLT 型号与 release/补丁（参考 MA5800-X7 / MA5800V100R018C00/SPH507）、user view，以及对 discovery 的明确授权。
2. 仅执行字面候选 `display current-configuration ?`；不要补全任何选项，也不要去掉 `?`。
3. 以脱敏方式记录选项、过滤器、`<cr>`、分页、错误信息以及回到提示符的情况。
4. 若帮助出现分页，仅使用当前上下文已验证的手动翻页；遇模糊行为立即中止。
5. 凡仅被显示的选项一律保持为 `[DISCOVERY]`。在没有新的真实证据前，不要执行过滤，也不要将语法提升为 `[已确认]`。
6. 仅当 CLI 自身枚举了所需全部域，且每段输出均有可核验的起止与提示符、无错误、超时、残留分页、断连或截断时，才可考虑未来的完整采集。
7. 若覆盖无法证明为穷尽，登记 `[待验证]`，勿将不完整内容作为备份发布。

## 示例

若 `ont add 0 ?` 列出 `sn-auth`，则继续执行 `ont add 0 0 sn-auth ?`。

## 预期结果

得到本 release 自身的 token 树；以 `?` 结尾的查询不改变设备。

## 已知错误

出现 `^` 或拒绝：按字面登记为 `[错误]`，禁止靠猜测修正。

## 诊断

确认模式、上一 token、给出的取值范围与 release。

## 依赖

全局矩阵 `HUAWEI-OLT-CLI-COMMANDS.md`。

## 风险

部分 CLI 可能执行完整前缀；动作类命令未带 `?` 时不要按 Enter。

## 回滚

纯 `?` 查询无需回滚；退出上下文且不保存任何变更。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不要去掉 `?`，不要凭记忆补全，不要混用不同 release，也不要在自动流程中使用 `save`、写操作、拷贝、导出、reload、reboot 或 restore。


## 配置保存（PERSIST）

本 Skill 默认只读/发现，**不**执行全局 save。落盘为**可选**：仅当用户明确要求时，改用 30-huawei-olt-config-save 并取得 PERSIST 授权。禁止在查询后自动 save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
