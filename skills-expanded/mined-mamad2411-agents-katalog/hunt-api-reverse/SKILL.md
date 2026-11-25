---
name: hunt-api-reverse
description: 线上 API 逆向：从请求/响应、错误结构、参数差分和同源服务恢复 API schema、状态机、鉴权边界、shadow route 与下一处可验证切入点。
---

# Objective

把线上 API 当作状态机和协议来还原，而不是从漏洞名称直接跳到 payload。

# Trigger signals

`rest_api`、`api_endpoint_candidate`、`parameter_map_confirmed`、`required_param_error`、`response_schema_diff`、`route_selector`、`shadow_api`、`framework_error`、`auth_boundary`。

# Required context

first-party endpoint、method、已保存请求/响应、baseline 与 response classification。每个探针只改变一个参数、编码或状态变量。

# First questions

- 参数类型、必填关系、默认值和组合约束是什么？
- `route`、`full`、`detail`、`fields` 是否切换 handler 或响应 schema？
- 错误是 edge、gateway、middleware 还是 application parser？
- 认证失败前后是否有稳定 schema 差异？
- 443 与同源备用端口、v1/v2、web/mobile route 是否行为不同？
- 当前请求是否进入同步 handler、异步 job 或缓存层？

# First probe

建立 `parameter_semantics` 矩阵：先用已知有效/无效基线，选择一个变量比较 status、headers、body schema、字段集合、长度和 timing。429、超时、challenge 只能标记 blocker，不能作为语义差异。

# Adaptive decision tree

- 结构化错误稳定且参数可控：`DEEPEN`，推断 schema 和状态转移。
- route/full/detail 造成可重复 schema 差异：进入对应 handler 的专项验证。
- 同源端口出现 framework/error 差异：进入 framework route reverse，不把 banner 当 CVE。
- 所有路径 catch-all/相同 body hash：`BACKTRACK` 到 client reverse 或 asset provenance。
- 429/冷却：`PIVOT` 到离线 artifact、低频单变量或已有不同入口，不重复矩阵。
- 认证边界明确但无第二对照：输出 auth hypothesis，等待新状态/身份信号。

# Handoff

- object id / owner / response schema → `hunt-idor`；
- writable field / nested JSON → `hunt-api-misconfig`；
- query-like input → `hunt-sqli`/`hunt-nosqli`；
- token verification → `hunt-jwt-crypto`/`hunt-auth-bypass`；
- callback URL/fetch → `hunt-ssrf`；
- template/parser → `hunt-ssti`/`hunt-deserialization`/`hunt-xxe`；
- business state/invariant → `hunt-business-logic`。

# Evidence fields

保存 endpoint、method、参数类型/必填关系、baseline/probe/post-baseline 引用、response class、schema diff、状态节点、confidence、已证伪条件和下一跳。

# Completion

完成标准：至少一个 endpoint 形成 schema 或状态节点，且下一步能指向具体 parameter/state/route；否则返回 `WAIT_FOR_SIGNAL`，明确缺少请求样本、浏览器网络记录、版本差异或身份对照。
