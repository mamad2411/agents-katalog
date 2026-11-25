---
name: hunt-rate-limit
description: 速率限制与枚举防护专项：在低频、自有输入集上判断登录、OTP、恢复、搜索、邀请码、API 或业务动作是否具有服务端速率、锁定、幂等与验证码边界。用于 429、retry-after、attempt counter、验证码、OTP 或敏感批处理信号；不做撞库、喷洒、暴力或大 keyspace 枚举。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-rate-limit

## 0. Engagement Gate

- 仅在用户授权、范围锁定、已建立 host/身份态 baseline 后开展；专项执行前先运行主编排器确认该路线在本轮 Top 3。
- 仅使用自有账户、测试对象、回调域、测试数据和已批准速率。WAF/验证码/超时/单次异常均为 `INCONCLUSIVE`。
- 每个实验遵循 `baseline → 单变量 probe → post-baseline → oracle → evidence`；超出 scope、触及第三方、共享用户或产生不可回滚副作用立即停止。

## 1. Trigger Signals

`rate_limited_endpoint`、`login_flow`、`otp_validation`、`password_reset_flow`、`invite_code`、`captcha`、`retry_after`、`attempt_counter`。

## 2. Safe Measurement Plan

定义服务方允许的极低请求上限与两三个自有输入；分别记录每个请求的状态、长度、延迟、响应头、账户状态和后续正确请求是否仍可用。区分显式 429、延迟/影子节流、账号锁定、IP/设备维度、成功与失败计数。

## 3. Minimal Validation

只做必要的少量失败后跟一个已知正确的自有尝试，验证控制是否触发且不会误伤。不要用大量错误 token/password、伪造 IP header、CAPTCHA solver、分布式源或并发绕过来“证明”缺限流。

## 4. Oracle / FP Gate

有效：在声明阈值内，敏感 endpoint 对超过合理失败次数的自有请求仍没有任何可观察服务端限速/锁定/验证码/风险控制，且已排除异步或账号级策略。单个 200、网络快、无 429 都不成立。

## 5. Stop / Evidence / Routing

停止：达到测试上限、触发锁定、验证码、WAF、账号风险或影响共享服务。保存精确次数、时间窗、身份/源维度、正确请求复原结果。恢复流转 `hunt-password-recovery`，MFA 转 `hunt-mfa-flow`，业务自动化转 `hunt-business-logic`。
