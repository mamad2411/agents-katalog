---
name: hunt-csp
description: Content Security Policy 专项：验证 CSP、Trusted Types、frame-ancestors、base-uri 与脚本来源策略是否在真实浏览器中有效执行，并把配置缺陷与可利用客户端注入明确区分。用于 CSP header/meta、nonce/hash、report endpoint、XSS 或 clickjacking 信号；不依赖外联窃取或绕过库。
metadata:
  maintained_by: OpenTgtyLab
  design: evidence-gated-specialist-route
---

# hunt-csp

## 0. Engagement Gate

- 仅在用户授权、范围锁定、已建立 host/身份态 baseline 后开展；专项执行前先运行主编排器确认该路线在本轮 Top 3。
- 仅使用自有账户、测试对象、回调域、测试数据和已批准速率。WAF/验证码/超时/单次异常均为 `INCONCLUSIVE`。
- 每个实验遵循 `baseline → 单变量 probe → post-baseline → oracle → evidence`；超出 scope、触及第三方、共享用户或产生不可回滚副作用立即停止。

## 1. Trigger Signals

`csp_header`、`csp_meta`、`trusted_types`、`script_nonce`、`frame_ancestors`、`xss_signal`、`clickjacking_signal`。

## 2. Audit Model

记录每个响应的 CSP source、多个 header 合并规则、report-only 与 enforce、script-src、object-src、base-uri、frame-ancestors、connect-src、nonce/hash、strict-dynamic 和 Trusted Types。以 Chrome console 的 policy violation 为主证据，不只解析字符串。

## 3. Minimal Validation

使用页面内无害 marker 结合已有 XSS/DOM 证据验证 CSP 是否阻断目标上下文；对 frame-ancestors 用自有 iframe 演示页确认。不要上传外部脚本、发起数据外带或使用第三方 JSONP/开放重定向作为绕过链。

## 4. Oracle / Stop

有效：已确认的可执行注入或 frame 场景在 CSP 应阻断时仍可执行，或敏感页面可被任意外部 origin frame。报告端点不可达、某个 header 缺失但另一 header 覆盖、Report-Only 告警都不是独立漏洞。

## 5. Evidence / Routing

保存 raw headers、Chrome console、页面上下文、enforce/RO 区分、无害 marker 结果。XSS 影响交 `hunt-xss`/`hunt-dom`，UI 影响交 `hunt-clickjacking`。
