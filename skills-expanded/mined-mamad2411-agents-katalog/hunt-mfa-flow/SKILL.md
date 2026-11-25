---
name: hunt-mfa-flow
description: MFA/2FA 流程专项：验证 MFA challenge 是否被服务端逐端点强制、一次性码/恢复码是否绑定并失效、敏感操作是否要求 step-up。用于 OTP、TOTP、WebAuthn、backup code、pre-MFA session 或 MFA 设置流程；不暴力枚举 OTP、不过验证码。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-mfa-flow

## 0. Engagement Gate

- 仅在用户授权、范围锁定、已建立 host/身份态 baseline 后开展；专项执行前先运行主编排器确认该路线在本轮 Top 3。
- 仅使用自有账户、测试对象、回调域、测试数据和已批准速率。WAF/验证码/超时/单次异常均为 `INCONCLUSIVE`。
- 每个实验遵循 `baseline → 单变量 probe → post-baseline → oracle → evidence`；超出 scope、触及第三方、共享用户或产生不可回滚副作用立即停止。

## 1. Trigger Signals

`mfa_flow`、`otp_validation`、`webauthn`、`backup_code`、`pre_mfa_session`、`mfa_sensitive_action`。

## 2. Preconditions

两名自有账户、两浏览器 profile、可重置 MFA 测试因子。建模密码验证、challenge、post-MFA session、恢复流程、密码/邮箱/资金等敏感 endpoint 的 middleware 要求。

## 3. Minimal Safe Validation

在自有 session 中只验证：是否可直接访问 post-MFA 页面、已消费的自有恢复码是否被拒绝、修改敏感设置时是否触发现有 step-up、pre-MFA token 是否被受保护 endpoint 正确拒绝。OTP 只测试正确码的一次消费/绑定，不猜码。

## 4. Oracle

有效：未完成 MFA 的自有会话访问本应 post-MFA 才可访问的资源，或已使用代码/恢复码被再次接受且造成可观察权限状态。UI 跳转、客户端本地 flag、一次失败不成立。

## 5. Stop / Evidence

停止：无测试恢复渠道、涉及生产管理员、需要批量 OTP、会锁定账户。保存状态转移、cookie/token 类别（值脱敏）、endpoint 角色要求和恢复证据。速率结论交 `hunt-rate-limit`，会话交 `hunt-session`。
