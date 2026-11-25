---
name: 10-vlan-subinterfaces
description: 在 Cisco ASR1001-X 上配置并诊断 802.1Q 子接口、L3、bridge-domain 与 BDI，勿当交换机对待。
---

# VLAN 与子接口

## 目标

正确使用 L3 子接口、bridge-domain 与 BDI，不把 ASR 当交换机。

## 前置条件

识别 ASR1001-X，并以脱敏方式执行 `show version`。在任何变更前确认模式、特权、范围、IOS XE release 与备用访问。

## 候选命令

- [推断] `interface ?`
- [推断] `show interfaces`
- [推断] `show vlan brief`
- [推断] `show bridge-domain`
- [推断] `show derived-config interface <INTERFACE>`

## 发现与分类

上表各行在被 CLI 接受前均为 `[推断]`，除非已明确标为 `[已确认]`。使用前在正确模式下执行上下文帮助（`?`、`show ?`、`show <TOKEN> ?`），并将输出记为 `[DISCOVERY]`。字面拒绝记为 `[错误]`。

## 步骤

用 `interface ?` 确认真实名称；区分 L2、L3、子接口、bridge-domain 与 BDI；校验 tag、父接口、MTU、IP 与重叠。

## 预期结果

证据足以判断状态，或提出保守变更方案，且不编造语法。

## 诊断

关联配置、运行状态与计数器。在第一层失败处停止，并记录命令、模式、时间与脱敏后的字面返回。

## 依赖

提出变更前，先查阅全局矩阵、决策树、错误库及相关 Skills。

## 风险

错误 tag/父接口/BDI 绑定可中断整段接入 VLAN。

## 回滚

登记先前接口段；仅移除或恢复本次对象。

## 安全规则

遵循 SHOW → 分析 → 校验 → 提案 → 确认 → 变更 → 校验 → 记录。遮蔽 `password`、`secret`、`key`、`community`、RADIUS、BGP、PPP 与 SSH 密钥。任何可变命令也标 `[破坏性]`。

## 禁止事项

未经显式确认不要变更；不要凭记忆拼语法；不要暴露密钥；不要把 reload/clear/reset 当第一动作；校验完成前不要保存配置。

## 来源

- 目标设备：Cisco ASR1001-X；真实版本尚未提供。
- Cisco ASR1000/IOS XE 官方文档见本包 README。
- 以真实 CLI 为准。其他 release 示例标为 `[版本不同]`；切勿混用 IOS、IOS XE 与 IOS XR。
