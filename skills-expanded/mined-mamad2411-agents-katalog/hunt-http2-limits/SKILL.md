---
name: hunt-http2-limits
description: HTTP/2 与协议资源限制专项：在隔离窗口审计协议协商、流/头/continuation/priority 的配额和厂商版本适用性；不发送耗尽序列或 request smuggling payload。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-http2-limits

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 规划验证，不授予目标操作权限。
- 只使用自有账户、对象、域名、测试数据、回调和批准速率；WAF、超时、单次异常、扫描器命中均为 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server/browser/monitor oracle → evidence`；出现第三方数据、共享基础设施或不可回滚副作用立即停止。

## 1. Trigger Signals

`http2_enabled`、`http2_settings`、`h2_error`、`continuation_hint`、`stream_limit_hint`、`http2_cve_candidate`。

## 2. Preconditions / Discovery

需要多跳架构证据、书面性能窗口、isolated path、监控、请求基线和停止阈值。确认 HTTP/2 是否端到端启用，而非只在 CDN 边缘。

## 3. Minimal Safe Validation

优先读取 ALPN、SETTINGS、server limits、版本公告和单一正常流行为；如批准，只在预置 fixture/隔离 gateway 上验证服务器是否拒绝超限的低成本 canary。

## 4. Oracle / False Positives

有效：隔离监控/日志确认实现未执行应有协议限制，或产品/版本/配置满足厂商公告。浏览器支持 H2、连接错误、工具警告不成立。

## 5. Stop / Evidence / Routing

停止：并发流洪泛、continuation flood、connection exhaustion、共享网关。保存 TLS/ALPN/SETTINGS、monitor、version evidence。request boundary 转 `hunt-http-smuggling`，CVE 转 `bb-methodology`。
