---
name: hunt-password-recovery
description: 密码找回与账户恢复专项：验证自有账户的枚举、reset token 生成/绑定/失效、恢复步骤与 step-up 约束。用于 forgot-password、recovery code、reset token、email change、account recovery 信号；不猜测 token、不向他人发送重置邮件。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-password-recovery

## 0. Engagement Gate

- 仅在用户授权、范围锁定、已建立 host/身份态 baseline 后开展；专项执行前先运行主编排器确认该路线在本轮 Top 3。
- 仅使用自有账户、测试对象、回调域、测试数据和已批准速率。WAF/验证码/超时/单次异常均为 `INCONCLUSIVE`。
- 每个实验遵循 `baseline → 单变量 probe → post-baseline → oracle → evidence`；超出 scope、触及第三方、共享用户或产生不可回滚副作用立即停止。

## 1. Trigger Signals

`password_reset_flow`、`recovery_flow`、`reset_token`、`recovery_code`、`email_change`、`account_recovery`。

## 2. Workflow Map

用两个自有账户记录 request → issuance → delivery → confirmation → password set → session revoke 的完整状态机。分别标记 token 的主体绑定、浏览器/设备绑定、单次使用、过期、撤销、速率/枚举防护及 email-change step-up。

## 3. Minimal Safe Validation

只重放自己获得的已消费/已撤销 token，或在两名自有账户间验证 token 主体绑定。对枚举只做极少量有效/无效地址差分，比较状态、长度、时间和邮件副作用；不进行字典或验证码绕过。

## 4. Oracle / Stop

有效：自有 token 在消费/撤销后仍可用、跨自有账户/会话错误绑定，或 reset API 直接暴露 token 且可完成受控恢复。文案不同、邮件延迟、正常单设备重置不成立。停止：第三方邮箱、真实管理员账户、猜测 token、批量请求。

## 5. Evidence / Routing

保存脱敏状态图、token hash/生命周期、会话撤销差分和自有账户归属。Host 生成交 `hunt-host-header`，OAuth 链接交 `hunt-oauth`，完整接管结论须经 `hunt-auth-bypass` / `triage-validation`。
