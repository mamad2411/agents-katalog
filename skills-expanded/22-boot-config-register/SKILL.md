---
name: 22-boot-config-register
description: 在 Cisco ASR1001-X 上识别 boot 变量与 config-register 问题，勿把 reload 当测试手段。
---

# Boot 与 config-register

## 目标

识别 boot 问题，且不以 reload 作为测试。

## 前置条件

识别 ASR1001-X，并以脱敏方式执行 `show version`。在任何变更前确认模式、特权、范围、IOS XE release 与备用访问。

## 候选命令

- [推断] `show boot`
- [推断] `show bootvar`
- [推断] `show version | include register`
- [推断] `boot ?`
- [推断] `config-register ?`

## 发现与分类

上表各行在被 CLI 接受前均为 `[推断]`，除非已明确标为 `[已确认]`。使用前在正确模式下执行上下文帮助（`?`、`show ?`、`show <TOKEN> ?`），并将输出记为 `[DISCOVERY]`。字面拒绝记为 `[错误]`。

## 步骤

确认 release 与语法；比较 BOOT/CONFIG_FILE/BOOTLDR/register；将 0x2102 理解为典型正常流、0x2142 为忽略 startup-config，并始终在该 release 上校验。

## 预期结果

证据足以判断状态，或提出保守变更方案，且不编造语法。

## 诊断

关联配置、运行状态与计数器。在第一层失败处停止，并记录命令、模式、时间与脱敏后的字面返回。

## 依赖

提出变更前，先查阅全局矩阵、决策树、错误库及相关 Skills。

## 风险

错误 boot 变量/register 可能导致无法启动或忽略配置；reload 是关键操作。

## 回滚

登记先前值；在不 reload 的情况下恢复；仅在专项授权后安排 reboot。

## 安全规则

遵循 SHOW → 分析 → 校验 → 提案 → 确认 → 变更 → 校验 → 记录。遮蔽 `password`、`secret`、`key`、`community`、RADIUS、BGP、PPP 与 SSH 密钥。任何可变命令也标 `[破坏性]`。

## 禁止事项

未经显式确认不要变更；不要凭记忆拼语法；不要暴露密钥；不要把 reload/clear/reset 当第一动作；校验完成前不要保存配置。

## 来源

- 目标设备：Cisco ASR1001-X；真实版本尚未提供。
- Cisco ASR1000/IOS XE 官方文档见本包 README。
- 以真实 CLI 为准。其他 release 示例标为 `[版本不同]`；切勿混用 IOS、IOS XE 与 IOS XR。
