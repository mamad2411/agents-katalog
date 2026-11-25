---
name: 28-huawei-olt-access
description: 指导经 Cisco ASR1001-X 跳转到私网华为 OLT 的 SSH 访问，不暴露凭据，也不经公网直连。
---

# 经 ASR 访问下游华为 OLT

## 目标

将 ASR 用作到达 `${DOWNSTREAM_HOST}` 的授权跳板。

## 前置条件

识别 ASR1001-X，并以脱敏方式执行 `show version`。在任何变更前确认模式、特权、范围、IOS XE release 与备用访问。

## 候选命令

- [已确认] 在源会话：`ssh -l ${DOWNSTREAM_USERNAME} ${DOWNSTREAM_HOST}`。在目标上校验。

## 发现与分类

上列命令由操作员声明为已使用。对任何变体，新命令行在被 CLI 接受前均为 `[推断]`。在正确模式执行上下文帮助，将输出记为 `[DISCOVERY]`，字面拒绝记为 `[错误]`。

## 步骤

[已确认] 命令由操作员声明为已使用。先按授权方式进入 ASR；再从其上 SSH 到私网 OLT；加载华为 OLT Skills；保持提示符与语法分离。

## 预期结果

证据足以判断状态，或提出保守变更方案，且不编造语法。

## 诊断

关联配置、运行状态与计数器。在第一层失败处停止，并记录命令、模式、时间与脱敏后的字面返回。

## 依赖

提出变更前，先查阅全局矩阵、决策树、错误库及相关 Skills。

## 风险

用户名是运营数据；密码/密钥切勿登记。跳转可能混淆设备/提示符。

## 回滚

仅访问。不得为绕过失败而改管理路由/ACL。

## 安全规则

遵循 SHOW → 分析 → 校验 → 提案 → 确认 → 变更 → 校验 → 记录。遮蔽 `password`、`secret`、`key`、`community`、RADIUS、BGP、PPP 与 SSH 密钥。任何可变命令也标 `[破坏性]`。

## 禁止事项

未经显式确认不要变更；不要凭记忆拼语法；不要暴露密钥；不要把 reload/clear/reset 当第一动作；校验完成前不要保存配置。

## 来源

- 目标设备：Cisco ASR1001-X；真实版本尚未提供。
- Cisco ASR1000/IOS XE 官方文档见本包 README。
- 以真实 CLI 为准。其他 release 示例标为 `[版本不同]`；切勿混用 IOS、IOS XE 与 IOS XR。
