---
name: hunt-payment-workflow
description: 支付与账务状态机专项：验证自有测试订单的金额、库存、优惠、回调、退款和订阅状态是否以服务端权威账务为准；不接触真实款项。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-payment-workflow

## 0. Engagement Gate

- 只在记录了授权、锁定 scope、host/身份态 baseline 后执行；先用主入口确认此路线进入本轮候选。
- 只使用自有账户、对象、域名、回调和可回滚测试数据；WAF、验证码、超时和单次异常均为 `INCONCLUSIVE`。
- 固定节奏为 `baseline → 单变量 probe → post-baseline → oracle → evidence`。第三方资产、共享用户、生产副作用或超出书面窗口时立即停止。

## 1. Trigger Signals

`checkout_flow`、`coupon_code`、`payment_callback`、`ledger_entry`、`refund_action`、`subscription_state`、`inventory_reservation`。

## 2. Preconditions / Discovery

获取书面测试支付窗口、测试商户/买家、零值或沙箱金额、可回滚订单、权威账务和库存读取接口。UI 金额与客户端字段均不是权威 oracle。

## 3. Minimal Safe Validation

按单变量、低频方式比较自有测试订单的正常与边界输入/流程顺序，始终从支付 provider sandbox 和后端 ledger 读回。并发仅在 `hunt-race-condition` 的额外能力满足时进行。

## 4. Oracle / False Positives

有效：服务端 ledger/entitlement/库存对自有订单产生不符合已定义不变量的持久结果，且可在回滚后复现。前端折扣、支付失败页、异步延迟不成立。

## 5. Stop / Evidence / Routing

停止：真实货币、生产库存、第三方账户、批量订单、绕过 provider。保存不变量、订单/ledger 的脱敏 ID、pre/post state、回滚证据。签名回调转 `hunt-webhook-signature`，并发转 `hunt-race-condition`。
