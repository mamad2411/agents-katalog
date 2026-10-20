---
name: hunt-api-abuse
description: API 资源与滥用防护专项：在批准窗口检查分页、批处理、复杂度、导出、搜索、上传和异步任务的服务端配额、成本控制与滥用边界；不实施 DoS。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-api-abuse

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 规划验证，不授予目标操作权限。
- 只使用自有账户、对象、域名、测试数据、回调和批准速率；WAF、超时、单次异常、扫描器命中均为 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server/browser/monitor oracle → evidence`；出现第三方数据、共享基础设施或不可回滚副作用立即停止。

## 1. Trigger Signals

`expensive_api_action`、`batch_endpoint`、`export_job`、`search_endpoint`、`pagination_limit`、`graphql_complexity_hint`、`async_job`。

## 2. Preconditions / Discovery

需要书面速率/性能窗口、服务端监控、测试对象、停止阈值与恢复责任人。建立单请求成本、配额、队列和权威审计基线。

## 3. Minimal Safe Validation

以最小数量的自有 no-op 请求比较 page size、batch size、filter complexity 或任务重复的服务器拒绝/配额行为；不做并发、长任务、wide query 或实际下载。

## 4. Oracle / False Positives

有效：在阈值内，服务器错误接受超出明示限制的自有低成本请求并产生可观测不应有成本/状态，或缺失关键配额控制。客户端限流、网络延迟、单个 429 不成立。

## 5. Stop / Evidence / Routing

停止：资源阈值、共享生产、任何排队/CPU/错误率异常。保存批准、监控、请求成本、拒绝/接受与恢复记录。特定 ReDoS 转 `hunt-redos`，GraphQL 转 `hunt-graphql`，rate limit 转 `hunt-rate-limit`。
