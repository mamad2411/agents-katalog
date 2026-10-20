---
name: hunt-paywall-entitlement
description: 付费墙、订阅与 entitlement 边界专项：验证自有测试账号的服务端权限、内容交付、缓存和订阅状态是否一致；不绕过真实付费或抓取内容。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-paywall-entitlement

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 规划验证，不授予目标操作权限。
- 只使用自有账户、对象、域名、测试数据、回调和批准速率；WAF、超时、单次异常、扫描器命中均为 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server/browser/monitor oracle → evidence`；出现第三方数据、共享基础设施或不可回滚副作用立即停止。

## 1. Trigger Signals

`paywall_gate`、`subscription_state`、`premium_content`、`entitlement_api`、`content_access_header`、`trial_flow`。

## 2. Preconditions / Discovery

准备免费与付费测试账号、可删除/可公开的 canary 内容、测试订阅或 sandbox entitlement、权威权限/ledger 读取。页面遮罩/DOM 隐藏不等于服务端控制。

## 3. Minimal Safe Validation

比较两自有身份在同一 canary 内容/API 上的正常访问、缓存和流程状态，并确认服务端是否在内容字节/API 层强制 entitlement；不使用 header 篡改去读取实际付费内容。

## 4. Oracle / False Positives

有效：免费自有身份稳定取得仅限付费的自有 canary 内容/服务端权限，且权威 entitlement 未授予。CSS 隐藏、浏览器缓存、公开预览不成立。

## 5. Stop / Evidence / Routing

停止：真实付费内容、第三方订阅、批量提取、支付绕过。保存账号状态、content canary、server response/ledger evidence。支付状态转 `hunt-payment-workflow`，缓存转 `hunt-cache-deception`。
