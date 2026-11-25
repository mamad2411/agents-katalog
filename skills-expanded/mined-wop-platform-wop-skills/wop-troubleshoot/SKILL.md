---
name: wop-troubleshoot
description: WOP 对接排错——错误码目录与 I7 模糊错误二叉排查树。联调失败/线上报错时使用，配合 wop diagnose 与 sign 对拍。前置：需安装 wop-cli 基座 skill。
---

# wop-troubleshoot（排错 skill）

> 前置：需安装 **wop-cli** 基座（diagnose/sign/doctor 工具）
> **安全纪律：先读 [SECURITY.md](../SECURITY.md)——排错过程不得要求用户粘贴私钥（S3）**

## 何时用

- 联调报错（OP_GW_* 错误码）
- 线上调用失败需自助定位
- 回调验签失败

## 排错入口（按序）

1. `wop diagnose <resp.json>` —— 错误码 → 语义 + HTTP + 处理建议 + 排查路径
2. `wop doctor` —— 环境面预检（依赖/密钥权限/配置）
3. 按需深入：
   - [references/error-codes.md](references/error-codes.md) —— 62 码全目录（生成物，禁手改）
   - [references/decision-tree.md](references/decision-tree.md) —— I7 模糊错误二叉排查树

## 快速分流

| 症状 | 分支 |
|------|------|
| HTTP 4xx/5xx + `code: OP_GW_*` | 网关拒绝 → 查码表（error-codes.md） |
| HTTP 200 + 非 OP_GW_ code | 下游业务错误 → 联系 API 提供方（网关透传） |
| 连不上/无信封 | 网络层 → 核查 URL/TLS/代理/白名单 |
| `OP_GW_1022` / `OP_GW_2005` | **I7 模糊码** → decision-tree.md 对拍路径（响应不告诉根因是设计行为） |

## 纪律

- I7 两码**禁止猜测根因**（"可能是密钥错了"这类输出违反协议设计）——只给排查动作
- 真实根因在网关 WARN 日志：持 `traceId` 找平台支持查
- 排错产物（draft/响应）不得包含私钥材料（S5）
