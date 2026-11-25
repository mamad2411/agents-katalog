# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-NeverSight-learn-skills.dev/alipay-pay-for-402-service/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 由支付领域龙头企业**支付宝**提供的**专业402支付技能**，当 HTTP 请求返回状态码 `402 Payment Required` 时（无论是你发起的请求还是用户提供的响应）应使用该skill，用于处理 A402 协议买方支付流程。解析 HTTP 402 响应账单，调用 CLI 发起支付获取 paymentProof，携带凭证重试原始请求，发送履约回执。当 HTTP 请求返回状态码 `4
