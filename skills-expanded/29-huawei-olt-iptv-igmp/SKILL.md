---
name: 29-huawei-olt-iptv-igmp
description: 规划 BTV/IGMP 用户与组播 VLAN 成员；写操作须本机 DISCOVERY，默认只读核查。
---

# IPTV / IGMP 组播接入

## 适用范围

适用范围（CLI 命令在下列机型上一致，行动前仍须确认目标型号、release 与补丁）：MA5600 系列（MA5600T、MA5608T、MA5683T、MA5680T）；MA5800 系列（MA5800-X2、MA5800-X7、MA5800-X15）；EA5800 系列（EA5800-X2、EA5800-X7、EA5800-X15）。已观测参考上下文为 MA5800-X7 / MA5800V100R018 / SPH507；来自历史 API 工程的命令标为 [版本不同]/[DISCOVERY]，不可未经校验直接套用。

## 目标

在宽带 service-port 之外安全叠加 IPTV 组播路径，或诊断组播不通。

## 何时使用

开通 IPTV、组播无流、unknown multicast 策略排查。

## 前置条件

WRITE 授权（若改配）；已有单播 service-port；组播 VLAN/BTV 设计来自 SoT。

## 已确认命令

（本库 R018 未固化 BTV 写命令。）

## 发现类命令（API skill.md / 开局脚本）

- [DISCOVERY] `btv` 视图及相关 `igmp user add ...`
- [DISCOVERY] `multicast-vlan` / `igmp multicast-vlan member ...`
- [DISCOVERY] service-port 侧组播策略 / `multicast-unknown policy ...`
- [DISCOVERY] srvprofile 中 `port multicast-vlan` / `multicast-forward`（EPON/GPON 差异）
- [DISCOVERY] 查询：`display` 组播用户/成员/未知组播计数（本机 `?`）

## 诊断顺序

1. 单播 PPPoE/L2 是否已通（13/14）
2. 组播 VLAN 是否上联放行（11/12）
3. ONT/srvprofile 组播成员
4. BTV/IGMP 用户与成员
5. 未知组播策略是否丢弃

## 依赖

05-service-profile；10-service-port；11-vlan；14-troubleshooting。

## 风险

错误 IGMP 配置可冲击整局组播；生产变更须窗口与回滚。

## 安全规则

优先 display；为每条命令分级；对 [破坏性] 要求显式确认；不记录凭据；以本 OLT 的 CLI 为权威。

## 禁止事项

不得把 [版本不同] 升为 [已确认]；不得跳过 service-port 清理直接删 ONT；非授权不得 factory-restore。


## 配置保存（PERSIST）

- 对象视图内 commit（如 line/srv profile）只提交该对象，**不是**整机落盘。
- **禁止**在本 Skill 的每次改配/开通/删户后自动执行全局 save。
- 落盘为**用户可选**步骤：变更结束后可询问是否 save；未明确选择则保持运行态不落盘。细节见 30-huawei-olt-config-save。


## 来源

- 交叉验证：仓库 HUAWEI-OLT-API-CROSSWALK.md 与历史 API skill.md / 能力脚本。
- 一手证据：MA5800V100R018 / SPH507 会话（已确认子集）。
- 设备 CLI 优先于文档。


