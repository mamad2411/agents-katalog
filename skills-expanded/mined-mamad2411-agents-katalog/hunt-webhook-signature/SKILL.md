---
name: hunt-webhook-signature
description: Webhook 签名与重放专项：验证自有 sender/receiver 的签名算法、canonicalization、timestamp/nonce 与事件授权；用于 webhook/header/signature/callback 信号。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-webhook-signature

## 0. Engagement Gate

- 只在记录了授权、锁定 scope、host/身份态 baseline 后执行；先用主入口确认此路线进入本轮候选。
- 只使用自有账户、对象、域名、回调和可回滚测试数据；WAF、验证码、超时和单次异常均为 `INCONCLUSIVE`。
- 固定节奏为 `baseline → 单变量 probe → post-baseline → oracle → evidence`。第三方资产、共享用户、生产副作用或超出书面窗口时立即停止。

## 1. Trigger Signals

`webhook_endpoint`、`signature_header`、`event_timestamp`、`nonce_header`、`callback_secret`、`signed_payload`。

## 2. Preconditions / Discovery

记录 sender/receiver ownership、签名覆盖字段、时钟偏差、nonce 存储、重试策略和 no-op event。先查官方集成文档与真实日志，避免猜测算法。

## 3. Minimal Safe Validation

用自有 sender/receiver 和预置 no-op event 对比正常事件、过期 timestamp、重复 event id、字段顺序/编码差异的拒绝行为；不篡改真实订单、部署或外部回调。

## 4. Oracle / False Positives

有效：receiver 接受本应拒绝的自有重复/失效/未覆盖事件，且 server audit 显示实际处理。仅签名错误、HTTP 2xx ack、客户端重放工具输出不成立。

## 5. Stop / Evidence / Routing

停止：真实密钥导出、第三方 sender、业务状态事件或高频重放。保存规范摘要、事件 ID、时间戳、server audit、pre/post state。回调 URL 转 `hunt-ssrf`/`hunt-open-redirect`，支付事件转 `hunt-payment-workflow`。
