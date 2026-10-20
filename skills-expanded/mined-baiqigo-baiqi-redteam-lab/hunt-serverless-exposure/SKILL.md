---
name: hunt-serverless-exposure
description: Serverless/API Gateway 专项：验证范围内函数、事件源、公开 route、环境配置和身份边界是否只暴露已授权能力；不调用写操作或读取环境变量。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-serverless-exposure

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 规划验证，不授予目标操作权限。
- 只使用自有账户、对象、域名、测试数据、回调和批准速率；WAF、超时、单次异常、扫描器命中均为 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server/browser/monitor oracle → evidence`；出现第三方数据、共享基础设施或不可回滚副作用立即停止。

## 1. Trigger Signals

`serverless_endpoint`、`api_gateway_marker`、`lambda_function_hint`、`function_route`、`event_source_hint`、`presigned_url`。

## 2. Preconditions / Discovery

确认 cloud/function 所属、公开 route、HTTP method、认证、事件触发、版本/alias、日志和自有 canary。域名或 header 不等于函数归属。

## 3. Minimal Safe Validation

在自有测试账号和 no-op route 中比较匿名/低权身份对健康、schema、错误和 canary 数据的访问；仅按官方文档做版本/配置适用性检查。

## 4. Oracle / False Positives

有效：匿名/低权自有身份访问了本不应暴露的自有函数/route/canary，且云 audit 或服务端日志确认。404、cloud header、scanner hit 不成立。

## 5. Stop / Evidence / Routing

停止：invoke 管理 API、环境变量、IAM、函数更新、异步事件投递。保存 route/identity/audit evidence。云权限转 `hunt-cloud-misconfig`，签名回调转 `hunt-webhook-signature`。
