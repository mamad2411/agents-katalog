---
name: hunt-client-reverse
description: 线上前端逆向：从一方 HTML/JS/chunk/source map 恢复路由、参数构造、编码、签名提示、token storage 与 source-to-sink 调用链，为 API、鉴权、业务逻辑和专项漏洞路由提供切入点。
---

# Objective

把前端运行时还原成可检验的 client surface，不把文档示例、第三方脚本或静态字符串直接当成凭据或漏洞。

# Trigger signals

`javascript_bundle`、`source_map`、`xhr_fetch`、`spa_framework`、`token_storage`、`route_selector`、`encoding_hint`、`signature_hint`、`feature_flag`。

# Required context

目标 scope、first-party asset provenance、页面/脚本证据、请求或静态 artifact。优先使用保存的线上证据做离线逆向；新请求只补一个能区分假设的信号。

# First probe / questions

1. 哪些脚本是一方资产，哪些是第三方？
2. 哪些函数构造 URL、query、body、header 或 token？
3. 参数经过何种编码、序列化、哈希或签名？
4. token 从哪里读取、何时刷新、交给哪些 endpoint？
5. feature flag、route、error branch 是否暴露备用 API？

# Standard output

对每条调用链输出：`client_entry`、`runtime_config`、`route`、`method`、`parameter`、`encoding`、`signature_hint`、`auth_storage`、`error_branch`、`feature_gate`、`related_asset`、`confidence`、evidence path。

# Adaptive decisions

- 找到明确 endpoint 和参数：交给 `hunt-api-reverse`，再按参数语义路由到 IDOR/API misconfig/SQLi/business logic。
- 找到 token lifecycle：交给 session/JWT/auth-bypass；不从静态字符串猜 token。
- 找到 source-to-sink DOM 链：交给 `hunt-dom`/`hunt-xss`。
- 只有第三方文档或示例：降为 reference，不继续主动验证。
- WAF/429 阻断：停止重复脚本触发请求，优先离线解析新资产或切换已有一方入口。

# False-positive kill rules

静态 `key`/`secret` 字符串、文档示例、注释、第三方域名、未被运行时引用的 route 不构成凭据、API 或漏洞结论。

# Evidence fields

保存脚本 URL/hash、asset provenance、函数/行号或匹配片段、endpoint/parameter graph、编码/签名说明、token storage 名称（不保存 token 值）和 confidence。

# Handoff / completion

完成标准：一方 client surface 已进入 graph，至少一条 route 有参数/调用来源/证据；若没有新信号，返回 `WAIT_FOR_SIGNAL` 并列出需要的新资产或浏览器网络记录。
