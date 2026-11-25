---
name: hunt-http-parameter-pollution
description: HTTP 参数污染专项：验证 query、form、JSON、path 与反代/后端之间的重复参数解析是否导致自有业务字段、校验或授权语义不一致。用于重复参数、多值字段、array parser、proxy/backend 差异信号；不通过污染他人请求或支付数据验证。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-http-parameter-pollution

## 0. Engagement Gate

- 仅在用户授权、范围锁定、已建立 host/身份态 baseline 后开展；专项执行前先运行主编排器确认该路线在本轮 Top 3。
- 仅使用自有账户、测试对象、回调域、测试数据和已批准速率。WAF/验证码/超时/单次异常均为 `INCONCLUSIVE`。
- 每个实验遵循 `baseline → 单变量 probe → post-baseline → oracle → evidence`；超出 scope、触及第三方、共享用户或产生不可回滚副作用立即停止。

## 1. Trigger Signals

`duplicate_parameter`、`array_parameter`、`query_parser`、`form_parser`、`proxy_backend_difference`、`multi_value_field`。

## 2. Model First

从正常请求确认每个层对参数的预期：first-wins、last-wins、array、merge、reject。分别记录 URL query、form body、JSON、path/matrix 参数与服务端 schema；不要用前端 UI 猜测后端解析。

## 3. Minimal Safe Validation

在自有只读或可回滚字段上重复同名值，比较服务端权威状态、验证错误和审计记录。每次只增加一个同名参数；控制请求保持原始顺序。对签名/支付/权限字段仅在沙盒交易与明确回滚下测试。

## 4. Oracle / False Positives

有效：前端、网关和后端对同一请求选择不同值，导致自有对象的校验、过滤、授权或状态语义被可重复改变。仅有“响应接受重复值”、数组接口的正常行为、UI 显示差异不成立。

## 5. Stop / Evidence / Routing

停止：真实订单、角色、密码、邮箱、共享缓存或第三方对象。保存 raw request、顺序、每层证据、状态读回与 rollback。签名类交签名 KB；请求边界类交 `hunt-http-smuggling`。
