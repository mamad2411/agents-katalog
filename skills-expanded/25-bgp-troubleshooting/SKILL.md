---
name: 25-bgp-troubleshooting
description: 在 ASR1001-X 上从物理连通性到 RIB/FIB 诊断 BGP，勿把重启会话当第一动作。
---

# Troubleshooting BGP

## 目标

隔离传输、FSM、address-family、策略或 best path 故障。

## 前置条件

识别 ASR1001-X，并以脱敏方式执行 `show version`。在任何变更前确认模式、特权、范围、IOS XE release 与备用访问。

## 候选命令

- [推断] `show bgp summary`
- [推断] `show ip bgp summary`
- [推断] `show bgp neighbors`
- [推断] `show ip route <PREFIX>`
- [推断] `show ip cef <PREFIX>`

## 发现与分类

上表各行在被 CLI 接受前均为 `[推断]`，除非已明确标为 `[已确认]`。使用前在正确模式下执行上下文帮助（`?`、`show ?`、`show <TOKEN> ?`），并将输出记为 `[DISCOVERY]`。字面拒绝记为 `[错误]`。

## 步骤

按 interface → IP → 可达性 → TCP/179 → neighbor → state → AFI/SAFI → 策略 → received/advertised → best-path → RIB → FIB 推进。

## 预期结果

证据足以判断状态，或提出保守变更方案，且不编造语法。

## 诊断

关联配置、运行状态与计数器。在第一层失败处停止，并记录命令、模式、时间与脱敏后的字面返回。

## 依赖

提出变更前，先查阅全局矩阵、决策树、错误库及相关 Skills。

## 风险

Reset BGP 可能撤回 Internet 并掩盖根因。

## 回滚

仅只读；任何 policy 变更走 BGP Skills 与回滚。

## 安全规则

遵循 SHOW → 分析 → 校验 → 提案 → 确认 → 变更 → 校验 → 记录。遮蔽 `password`、`secret`、`key`、`community`、RADIUS、BGP、PPP 与 SSH 密钥。任何可变命令也标 `[破坏性]`。

## 禁止事项

未经显式确认不要变更；不要凭记忆拼语法；不要暴露密钥；不要把 reload/clear/reset 当第一动作；校验完成前不要保存配置。

## 来源

- 目标设备：Cisco ASR1001-X；真实版本尚未提供。
- Cisco ASR1000/IOS XE 官方文档见本包 README。
- 以真实 CLI 为准。其他 release 示例标为 `[版本不同]`；切勿混用 IOS、IOS XE 与 IOS XR。

