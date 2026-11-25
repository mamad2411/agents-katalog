---
name: 01-baseline
description: 采集并脱敏 Cisco ASR1001-X 的基线：硬件、IOS XE、配置、路由、接口、资源、许可证、boot 与冗余。
---

# ASR1001-X 基线

## 目标

在诊断或变更前生成只读快照。

## 前置条件

识别 ASR1001-X，并以脱敏方式执行 `show version`。在任何变更前确认模式、特权、范围、IOS XE release 与备用访问。

## 已确认命令（ASR1001-X / IOS XE 17.09.03a 上下文）

- [已确认] `show version`
- [已确认] `show running-config`

## 候选命令

- [推断] `show startup-config`
- [推断] `show interfaces`
- [推断] `show ip interface brief`
- [推断] `show ipv6 interface brief`
- [推断] `show ip route`
- [推断] `show ipv6 route`
- [推断] `show arp`
- [推断] `show cdp neighbors`
- [推断] `show lldp neighbors`
- [推断] `show platform`
- [推断] `show processes cpu`
- [推断] `show processes memory`
- [推断] `show memory statistics`
- [推断] `show inventory`
- [推断] `show license summary`
- [推断] `show license`
- [推断] `show bootvar`
- [推断] `show rom-monitor`
- [推断] `show redundancy`
- [推断] `show redundancy states`

## 发现与分类

上表各行在被 CLI 接受前均为 `[推断]`，除非已明确标为 `[已确认]`。使用前在正确模式下执行上下文帮助（`?`、`show ?`、`show <TOKEN> ?`），并将输出记为 `[DISCOVERY]`。字面拒绝记为 `[错误]`。

## 步骤

先执行 `show version`；确认上下文与已验证环境一致；选择该 release 文档；采集其余只读；脱敏 password/secret/key/community/RADIUS/BGP/PPP；记录 uptime 与时间戳。

## 预期结果

证据足以判断状态，或提出保守变更方案，且不编造语法。

## 诊断

关联配置、运行状态与计数器。在第一层失败处停止，并记录命令、模式、时间与脱敏后的字面返回。

## 依赖

提出变更前，先查阅全局矩阵、决策树、错误库及相关 Skills。

## 风险

`show running-config` 与 `show startup-config` 即使加密也可能暴露密钥信息。

## 回滚

只读不适用回滚。立即删除任何未脱敏产物。

## 安全规则

遵循 SHOW → 分析 → 校验 → 提案 → 确认 → 变更 → 校验 → 记录。遮蔽 `password`、`secret`、`key`、`community`、RADIUS、BGP、PPP 与 SSH 密钥。任何可变命令也标 `[破坏性]`。

## 禁止事项

未经显式确认不要变更；不要凭记忆拼语法；不要暴露密钥；不要把 reload/clear/reset 当第一动作；校验完成前不要保存配置。

## 来源

- 已验证上下文：Cisco ASR1001-X，IOS XE 17.09.03a；未登记任何客户身份。
- Cisco ASR1000/IOS XE 官方文档见本包 README。
- 以真实 CLI 为准。其他 release 示例标为 `[版本不同]`；切勿混用 IOS、IOS XE 与 IOS XR。
