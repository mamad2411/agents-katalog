---
name: 02-cli-discovery
description: 在 Cisco ASR1001-X 上用上下文帮助发现语法与模式，再使用任何未确认命令。
---

# Discovery da CLI IOS XE

## 目标

将文档假设转化为该设备的具体语法。

## 前置条件

识别 ASR1001-X，并以脱敏方式执行 `show version`。在任何变更前确认模式、特权、范围、IOS XE release 与备用访问。

## 候选命令

- [推断] `?`
- [推断] `show ?`
- [推断] `show interfaces ?`
- [推断] `show ip ?`
- [推断] `show ipv6 ?`
- [推断] `show bgp ?`
- [推断] `show pppoe ?`
- [推断] `show aaa ?`
- [推断] `show policy-map ?`
- [推断] `show service-policy ?`
- [推断] `show platform ?`
- [推断] `show controllers ?`
- [推断] `show license ?`
- [推断] `show bootvar ?`
- [推断] `configure terminal`
- [推断] `interface ?`
- [推断] `router ?`
- [推断] `ip ?`
- [推断] `ipv6 ?`
- [推断] `aaa ?`
- [推断] `policy-map ?`
- [推断] `class-map ?`
- [推断] `route-map ?`
- [推断] `ip access-list ?`
- [推断] `username ?`
- [推断] `line ?`
- [推断] `snmp-server ?`
- [推断] `logging ?`
- [推断] `service ?`
- [推断] `boot ?`

## 发现与分类

上表各行在被 CLI 接受前均为 `[推断]`，除非已明确标为 `[已确认]`。使用前在正确模式下执行上下文帮助（`?`、`show ?`、`show <TOKEN> ?`），并将输出记为 `[DISCOVERY]`。字面拒绝记为 `[错误]`。

## 步骤

识别提示符/模式；每次只插入一个 token；保留字面输出；已执行的帮助查询标为 `[DISCOVERY]`；仅成功动作标为 `[已确认]`。

## 预期结果

证据足以判断状态，或提出保守变更方案，且不编造语法。

## 诊断

关联配置、运行状态与计数器。在第一层失败处停止，并记录命令、模式、时间与脱敏后的字面返回。

## 依赖

提出变更前，先查阅全局矩阵、决策树、错误库及相关 Skills。

## 风险

配置模式下的上下文帮助可能暴露危险选项；未经授权勿补全可变命令行。

## 回滚

退出模式且不改动。若某前缀被执行，停止并审计 running-config。

## 安全规则

遵循 SHOW → 分析 → 校验 → 提案 → 确认 → 变更 → 校验 → 记录。遮蔽 `password`、`secret`、`key`、`community`、RADIUS、BGP、PPP 与 SSH 密钥。任何可变命令也标 `[破坏性]`。

## 禁止事项

未经显式确认不要变更；不要凭记忆拼语法；不要暴露密钥；不要把 reload/clear/reset 当第一动作；校验完成前不要保存配置。

## 来源

- 已验证上下文：Cisco ASR1001-X，IOS XE 17.09.03a；未登记任何客户身份。
- Cisco ASR1000/IOS XE 官方文档见本包 README。
- 以真实 CLI 为准。其他 release 示例标为 `[版本不同]`；切勿混用 IOS、IOS XE 与 IOS XR。
