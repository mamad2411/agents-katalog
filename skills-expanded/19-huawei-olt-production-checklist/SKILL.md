---
name: 19-huawei-olt-production-checklist
description: 在放行生产前对华为 OLT 开通做端到端校验，不执行本地测试或未授权变更。
---

# 华为 OLT 生产检查清单

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507，不可未经校验直接套用到其他 release。

## 目标

为 ONT 与 PPPoE 给出可复现的运维验收。

## 何时使用

当任务与本 Skill 描述匹配时使用。先校验 release、patch、CLI 模式与范围。

## 前置条件

变更已授权且已完成；签约用户数据在 Skills 外处理。

## 已确认命令

- [已确认] `display ont info summary 0/1/0`；`display service-port 1000`；`display port vlan 0/1/0`；`display port vlan 0/8/0`。

## 发现类命令

- [DISCOVERY] 对任何其他状态使用 `?` 并登记 release。

## 语法

完整清单见 README：board/PON、profiles/DBA、ONT、WAN route、GEM、service-port、VLAN、上联、BNG 上的 PPPoE、AAA、IP、NAT/DHCP 与 LAN/Wi-Fi。

验收通过后，**不要**自动 `save`。若用户选择防重启丢失，再走可选 **PERSIST**（`30-huawei-olt-config-save`）；「已验收」≠「必须已 save」。

## 示例

目标验收：台架 ONT 在线、已应用 WAN route、service-port up、VLAN100 端到端贯通、BNG 上有该 ONT 的 PPPoE 会话、已获 IP，且 LAN/Wi-Fi 可上网。

## 预期结果

全部项目经证据与责任人批准。

## 已知错误

任一项目失败即中断验收；查阅错误库。

## 诊断

回到决策树中第一处失败层。

## 依赖

OLT、传输/BNG 与 AAA 团队。

## 风险

部分验收可能掩盖冗余或管理面丢失。

## 回滚

若触发中止准则，遵循 `17-huawei-olt-rollback`。

## 安全规则

优先 `display`；为每条命令分级；查阅参考与 Binding times；对 `[破坏性]` 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不得仅凭 ONT 在线状态宣告成功。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 一手证据：操作员提供的 CLI 会话，MA5800V100R018，patch SPH507。
- 华为官方参考：MA5800 支持门户及 README 所列官方指南。
- 设备 CLI 优先于文档。其他 release 材料标为 `[版本不同]`。
