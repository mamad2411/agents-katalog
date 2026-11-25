---
name: 27-huawei-olt-board-inventory
description: 采集机框板卡、PON/上联口状态与光学相关只读信息，作为开通与排障前置。
---

# 板卡与光口巡检

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507；来自历史 API 工程的命令标为 [版本不同]/[DISCOVERY]，不可未经校验直接套用。

## 目标

在不开通前建立机框/槽位/端口可用性与光学健康的只读视图。

## 何时使用

新局验收、扩容、光路投诉、autofind 为空、上联异常。

## 前置条件

READ 授权；已知管理地址与 SoT 中的机框角色。

## 已确认命令

- [已确认] `display version`
- [已确认] `display port vlan <F/S/P>`（PON/上联示例见 11/12）

## 发现类命令（API / skill.md）

- [DISCOVERY] `display board 0`（或 `display board <frame>`）
- [DISCOVERY] `interface gpon|epon|scu|giu <F/S>` → `display port state all`
- [DISCOVERY] `display ont optical-info ...` / `display ont wan-info ...`
- [DISCOVERY] `display mac-address port <F/S/P> ont <ONTID>`
- [DISCOVERY] EPON 端口视图与 GPON 并列巡检

## 预期结果

输出槽位类型、端口 Up/Down、可疑光功率/异常口清单；不改配置。

## 依赖

01-baseline；08-ont-status；12-uplink；14-troubleshooting。

## 风险

只读为主；进入 interface 视图时勿误下写命令。

## 安全规则

优先 display；为每条命令分级；对 [破坏性] 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不得把 [版本不同] 升为 [已确认]；不得跳过 service-port 清理直接删 ONT；非授权不得 factory-restore。


## 配置保存（PERSIST）

本 Skill 默认只读/发现，**不**执行全局 save。落盘为**可选**：仅当用户明确要求时，改用 30-huawei-olt-config-save 并取得 PERSIST 授权。禁止在查询后自动 save。


## 来源

- 交叉验证：仓库 HUAWEI-OLT-API-CROSSWALK.md 与历史 API skill.md / 能力脚本。
- 一手证据：MA5800V100R018 / SPH507 会话（已确认子集）。
- 设备 CLI 优先于文档。


