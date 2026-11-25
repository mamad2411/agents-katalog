---
name: 27-service-policy-troubleshooting
description: 在 ASR1001-X 上诊断 service-policy 缺失、方向、分类、policing、shaping 与丢包。
---

# Troubleshooting de service-policy

## 目标

用 MQC 计数器解释速率/丢包。

## 前置条件

识别 ASR1001-X，并以脱敏方式执行 `show version`。在任何变更前确认模式、特权、范围、IOS XE release 与备用访问。

## 候选命令

- [推断] `show policy-map interface`
- [推断] `show policy-map`
- [推断] `show running-config interface <INTERFACE>`

## 发现与分类

上表各行在被 CLI 接受前均为 `[推断]`，除非已明确标为 `[已确认]`。使用前在正确模式下执行上下文帮助（`?`、`show ?`、`show <TOKEN> ?`），并将输出记为 `[DISCOVERY]`。字面拒绝记为 `[错误]`。

## 步骤

确认挂接/方向；检查对应 class、offered rate、drops、police/shape 与层级；在 PPPoE 上比较 Template 与 Virtual-Access。

## 预期结果

证据足以判断状态，或提出保守变更方案，且不编造语法。

## 诊断

关联配置、运行状态与计数器。在第一层失败处停止，并记录命令、模式、时间与脱敏后的字面返回。

## 依赖

提出变更前，先查阅全局矩阵、决策树、错误库及相关 Skills。

## 风险

计数器可能累计；共享 policy 会放大影响面。

## 回滚

仅只读；变更走 `17-policy-map`。

## 安全规则

遵循 SHOW → 分析 → 校验 → 提案 → 确认 → 变更 → 校验 → 记录。遮蔽 `password`、`secret`、`key`、`community`、RADIUS、BGP、PPP 与 SSH 密钥。任何可变命令也标 `[破坏性]`。

## 禁止事项

未经显式确认不要变更；不要凭记忆拼语法；不要暴露密钥；不要把 reload/clear/reset 当第一动作；校验完成前不要保存配置。

## 来源

- 目标设备：Cisco ASR1001-X；真实版本尚未提供。
- Cisco ASR1000/IOS XE 官方文档见本包 README。
- 以真实 CLI 为准。其他 release 示例标为 `[版本不同]`；切勿混用 IOS、IOS XE 与 IOS XR。

