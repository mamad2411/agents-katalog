---
name: hunt-request-signature
description: API 请求签名、HMAC、canonical request、timestamp 与 nonce 边界专项：验证自有客户端与服务端之间的签名覆盖、重放防护、时效和规范化是否由服务端可靠执行。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-request-signature

## 0. Engagement Gate

- 仅在授权、scope、host/身份 baseline 和主编排器路由齐备时执行；本 Skill 只描述验证流程，不授予对目标的操作权限。
- 仅使用自有 client、账号、测试 API key、无害 request body、审批速率和可审计服务端；超时、WAF、单次异常或客户端报错均是 `INCONCLUSIVE`。
- 固定执行 `baseline → 单变量 probe → post-baseline → server oracle → evidence`；涉及真实签名密钥、生产凭据、共享 webhook、第三方服务或不可回滚动作立即停止。

## 1. Trigger Signals

`api_signature_header`、`hmac_signature`、`canonical_request_hint`、`signed_query`、`timestamp_header`、`nonce_header`、`signature_verification_error`。

## 2. Preconditions / Discovery

从真实自有请求确认：签名覆盖的方法、path、query、body、host、timestamp/nonce、key ID 和 canonicalization 规则；记录正常请求及服务端审计中对应的验证结果。只看到 `X-Signature` 或浏览器生成哈希不等于存在缺陷。

## 3. Minimal Safe Validation

使用专用测试 client 对同一无害、可回滚请求做一次单变量对照，例如在不改变业务语义的前提下改变**一个**已声明应被覆盖的字段，或重放已过期的自有 no-op 请求。每轮重新建立 baseline，禁止并发重放、构造密钥猜测或试图计算未知签名。

## 4. Oracle / False Positives

有效：服务端审计与权威状态共同证明它接受了本应因 method/path/query/body/timestamp/nonce/canonicalization 不匹配而拒绝的自有请求。仅 HTTP 200、签名错误信息、SDK 前端限制、缓存命中或客户端 UI 差异不成立。

## 5. Stop / Evidence / Routing

停止：密钥提取、生产/第三方 key 使用、真实交易/资源写入、批量重放、绕过请求配额。保存脱敏 request shape、字段覆盖矩阵、单变量差分、server audit、post-baseline 和重新开启条件。JWT 转 `hunt-jwt-crypto`；webhook sender/receiver 转 `hunt-webhook-signature`；客户端 Web Crypto 数据流转 `hunt-web-crypto`。
