---
name: security-app-api
canonical_id: security.app.api
aliases: [api-security, api-top10, rest-graphql-security]
version: 1.0.0
status: stable
created_date: 2026-06-10
updated_date: 2026-06-10
allowed-tools: Read, Grep, Glob, Bash
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - OWASP API Security Top 10: 2023
  - OWASP ASVS: 5.0 (V4 API + V6 Authentication + V7 Session + V8 Authorization + V9 Self-contained Tokens, as relevant)
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key"]
  redact_on_output: ["tokens", "object IDs in production", "real user identifiers", "API keys"]
upstream:
  - appsec-security-orchestrator
downstream:
  - security-remediation
  - appsec-security-orchestrator (back with findings)
description: >-
  Per-endpoint API security review overlay for REST / GraphQL / gRPC, executing OWASP API Security Top 10:2023 (BOLA, broken auth, BOPLA, resource consumption, BFLA, sensitive business flows, SSRF, misconfiguration, inventory, third-party consumption). Composes on the appsec-reviewer agent base auth review. Static and authorized-test-account checks only - no active exploitation.
trigger_phrases:
  - API security / API Top 10 / 接口安全 / API 鉴权
  - BOLA / BFLA / mass assignment / broken object level authorization
  - REST security / GraphQL security / endpoint authorization
  - IDOR / object ownership check / authz matrix
  - excessive data exposure / SSRF in API / API inventory
---

# Security App — API (OWASP API Security Top 10:2023)

## 1. Mission

API 漏洞的核心不是注入，而是 **authorization 在 per-object / per-function / per-property 三个粒度上至少一个没做对**。本 skill 对每个 endpoint 做系统化 API Top 10:2023 审查——object-level（API1）、function-level（API5）、property-level（API3）三层授权 + resource consumption（API4）+ business flow abuse（API6）+ SSRF（API7）+ misconfig（API8）+ inventory（API9）+ unsafe upstream consumption（API10）。

**职责边界**：
- **owns**: per-endpoint API Top 10:2023 review；object/function/property authZ test matrix；rate/quota/pagination/payload limits；API inventory（versioning / shadow / zombie）；outbound API consumption safety
- **不做**: base authentication / session / 通用 authZ 模型设计——那是 `appsec-reviewer` agent 按 ASVS **V6 / V7 / V8** 做的（本 skill COMPOSES on top，引用其 finding，不重复 base auth content）；不做 file upload（→ `security-app-file-upload`）；不做 tenant 隔离（→ `security-app-multitenant`）；不做 WebSocket/SSE（→ `security-app-websocket`）；不做协议层加密（TLS 走 ASVS V12）

**Composition rule（不重复 base）**：
- API2 broken authentication = 在 base auth review **之上** 只审 API-specific 面（per-endpoint auth 强制、JWT alg/aud/exp 在 API 边界的校验、API key vs session 的边界、unauthenticated endpoint inventory）。credential storage / password policy / MFA / session fixation 等 base 内容 **不在此重复**——若发现缺口，引用或路由回 base auth finding（ASVS V6/V7），不在本 skill 重新出 finding。

---

## 2. Activation Triggers

| Trigger | Action |
|---|---|
| 项目暴露 REST endpoint（Express / FastAPI / Spring / Rails / Go net/http 等）| 默认激活 |
| 项目暴露 GraphQL（resolver / schema）| 激活 + §13 GraphQL-specific |
| 项目暴露 gRPC / tRPC | 激活（object/function authZ 同理）|
| Endpoint 接受 path/query 中的 object id（`/orders/{id}`）| 升级 API1 BOLA 深审 |
| Endpoint 接受 client JSON body 写库 | 升级 API3 BOPLA（mass assignment）深审 |
| Endpoint 接受 user-supplied URL（webhook / fetch / import-from-url / avatar-by-url）| 升级 API7 SSRF 深审 |
| 项目 consume 第三方 API（payment / social / data provider）| 升级 API10 深审 |
| 多版本 API（`/v1` `/v2`）或 staging endpoint 与 prod 混部 | 升级 API9 inventory 深审 |

**物理标识**：与 orchestrator 一致——项目根无 `.appsec/config.json` 时 silent exit（单行 log，不落 evidence），由 §16.3 overlay activation 路由进入。

---

## 3. Inputs（review 前先盘点）

```
Step 0  Endpoint inventory（静态优先，不发包）
        → Grep 路由定义：Express `app.(get|post|put|patch|delete)` / FastAPI `@app.*` / Spring `@*Mapping` / Rails routes.rb / OpenAPI/Swagger spec / GraphQL schema
        → 每个 endpoint 记：method + path + auth required? + role(s) + 接受的 object id 参数 + 接受的 body 字段 + 返回的 object 字段
        → 产出 endpoint matrix（§7 authZ 测试矩阵的输入）
        → 如有 OpenAPI/GraphQL schema：以它为权威清单对照实际路由（差集 = API9 shadow/zombie 候选）
```

**Hard rule**：endpoint inventory 必须 **static-first**（读路由定义 / OpenAPI / schema），不靠发包枚举。authorized-test-account 逻辑验证只在 static 盘点后、对自有 staging / 授权环境进行（§6）。

---

## 4. Per-Risk Review（API Top 10:2023）

> 每条给：**look for（静态/被动看什么）** → **test（非破坏性怎么验：static + authorized test accounts）** → **example finding（schema 字段要点）**。
> 所有 finding 走 §8 输出契约（`appsec-sdk finding.add`，redact-first）。`api_top10` 字段填 `[API<n>]`，`asvs_mapping` 用 `v5.0.0-<ch>.<sec>.<req>`。

### API1 — Broken Object Level Authorization (BOLA / IDOR)

每个返回 / 修改单个 object 的 endpoint，是否校验 **当前 caller 拥有 / 有权访问该 object**，而不仅仅是"已登录"。

- **Look for**:
  - endpoint 接受 object id（path / query / body）后，直接 `findById(id)` 返回，**没有** `WHERE owner_id = caller` 或等价 ownership 检查
  - 授权检查只验"登录了"或"有 role"，但不验"这个具体 object 属于这个 caller"
  - 用 sequential / 可预测 id（自增整数）放大可枚举性（id 不可预测 ≠ 授权，只是降低可发现性）
  - GraphQL `node(id:)` / 全局 object id 解析器缺 per-object owner 检查
- **Test（非破坏性）**:
  - static：对每个 object-id endpoint 追代码路径，确认 ownership predicate 存在且在 DB 查询层（不是仅前端隐藏）
  - authorized test accounts：用 **account A** 创建 object，记下 id；用 **account B** 的合法 token 对同一 id 发 **读** 请求（GET），看是否拿到 A 的数据。只读、不改、不删——这是逻辑验证不是 exploit
  - 横向（同角色跨用户）与纵向（低权限访问高权限 object）都测
- **Example finding**: `source: manual_review`, `severity: high`, `api_top10: [API1]`, `cwe: [CWE-639]`, `asvs_mapping: [v5.0.0-8.2.1]`, `description: "GET /api/orders/{id} returns any order by id without owner check; account B retrieved account A's order in staging"`, `reproduction_steps` 用 redacted id + test-account 标注（禁止 raw token / 真实 id）。

### API2 — Broken Authentication（API 边界子集，不重复 base）

> **COMPOSES on base auth (ASVS V6/V7)**——本节只审 API-specific 面；base credential/session 内容路由回 appsec-reviewer。

- **Look for**:
  - 存在 unauthenticated endpoint 但本应鉴权（对照 inventory 中 `auth required?` 列）
  - JWT 校验缺 `alg` 固定 / 缺 `aud` / 缺 `exp` 校验 / 接受 `alg:none`（API 边界处的 token 验证薄弱）
  - API key 当作身份用但无 scope / 无 rotation / hardcode（key 命中 → 路由 `security-platform-secrets`，不在此存 raw 值）
  - token 放 URL query（进 access log / referer）
  - 认证失败与"object 不存在"返回不一致，泄露存在性
- **Test**:
  - static：对 inventory 每个"应鉴权"endpoint 确认 middleware/guard 实际挂载（不是声明了但路由顺序绕过）
  - authorized：无 token / 过期 token / 篡改 `alg` 的 token 发请求，确认被拒（用自有测试 token，不伪造他人凭证）
- **Example finding**: `api_top10: [API2]`, `cwe: [CWE-287]`, `asvs_mapping: [v5.0.0-6.2.1]` 或 self-contained token 缺陷用 `v5.0.0-9.2.1`；若是 base credential 问题 → **不出新 finding**，在 review note 引用 base auth finding id。

### API3 — Broken Object Property Level Authorization (BOPLA)

两个子面：**mass assignment**（client 能写不该写的属性）+ **excessive data exposure**（response 返回不该返回的属性）。

- **Look for**:
  - **Mass assignment**: body 直接 spread 进 model（`User.update(req.body)` / `Model(**request.json)` / `Object.assign(entity, body)`），无 allow-list；存在 `role` / `is_admin` / `verified` / `balance` / `owner_id` 等敏感字段可被 client 设置
  - **Excessive exposure**: 整个 entity 序列化返回（`res.json(user)`）含 `password_hash` / `mfa_secret` / 内部 flag / 其他用户 PII；GraphQL 返回 type 暴露敏感 field 无 field-level authZ；依赖前端"不显示"而非后端不返回
- **Test**:
  - static：追 body→persistence 是否有显式 allow-list（DTO / serializer / schema pick）；追 entity→response 是否有显式输出 DTO
  - authorized：用普通账号 PATCH 一个对象，body 里**额外**塞 `{"role":"admin"}` 之类，看是否被接受（写自己的对象、可逆字段、改完即查即还原——非破坏）；读自有对象看 response 是否含敏感字段
- **Example finding**: mass assignment → `severity: high`, `api_top10: [API3]`, `cwe: [CWE-915]`, `asvs_mapping: [v5.0.0-8.3.1]`；excessive exposure → `cwe: [CWE-213]`, `data_classes: [confidential]`。

### API4 — Unrestricted Resource Consumption

rate / quota / pagination / payload / 计算成本 是否有界。

- **Look for**:
  - 无 global / per-user / per-endpoint rate limit；无 quota
  - list endpoint 无分页或 `limit` 可被 client 设成超大值（`?limit=1000000`）
  - body / file / array 大小无上限；批量 endpoint（`POST /batch`）数组长度无界
  - 昂贵操作（export / report / 第三方调用 / regex / image resize）无单独限流
  - GraphQL 无 query depth / complexity / cost 限制（嵌套 query 放大）
  - 触发外部计费的操作（SMS / email / LLM token）无 per-user 上限（cost runaway）
- **Test**:
  - static：确认 limiter 中间件存在 + pagination 上限 server-side clamp + body size 限制 + GraphQL depth/complexity 插件
  - authorized：对自有账号发合法范围内的 `limit` 边界值（如 `limit=100` vs 文档上限），观察是否被 server clamp。**不做** flood / DoS——只验"上限是否存在且 server-side enforced"
- **Example finding**: `api_top10: [API4]`, `cwe: [CWE-770]`, `asvs_mapping: [v5.0.0-8.1.1]`, `business_impact` 视是否触发计费/容量上限（叠加 §5 reliability lens cost runaway）。

### API5 — Broken Function Level Authorization (BFLA)

role × method × endpoint 矩阵：低权限角色能否调用高权限 **function**（与 API1 的 object 维度正交）。

- **Look for**:
  - admin-only endpoint（`/admin/*`、`DELETE /users/{id}`、`POST /users/{id}/role`）仅靠"前端不显示"或路径不公开，后端无 role guard
  - 同一 resource 不同 method 授权不一致（GET 公开但 DELETE 应限管理员，却共用一个宽松 guard）
  - guard 在 controller 层声明但被 route 顺序 / 通配路由绕过
  - GraphQL mutation 缺 per-mutation role 检查
- **Test**:
  - static：构建 **role × method × endpoint** 矩阵（§7），逐格确认 server-side role 检查
  - authorized：用 **普通用户** token 调 admin function（如 `POST /admin/...`），确认被拒。用自有低权限测试账号，**不**用提权后的真实操作
- **Example finding**: `api_top10: [API5]`, `cwe: [CWE-285]`, `asvs_mapping: [v5.0.0-8.1.2]`, `severity: high|critical`（取决于 function 影响面）。

### API6 — Unrestricted Access to Sensitive Business Flows

业务流（注册 / 下单 / 购票 / 评论 / 转账 / 邀请）能否被自动化滥用，即使每个单独请求都"合法授权"。

- **Look for**:
  - 高价值流无 anti-automation（无 CAPTCHA-light / 无 device fingerprint / 无 velocity 限制 / 无 per-account per-time cap）
  - 限量资源（库存 / 优惠券 / 限时票）流无并发/重复保护（可被脚本扫货）
  - 邀请 / referral / 试用流可被批量薅
  - 资源消耗型流（发起退款 / 触发通知 / 调用计费上游）无业务级节流
- **Test**:
  - static：识别敏感 business flow 清单 + 现有 anti-abuse 控制盘点（这是设计审查，不是发包）
  - authorized：在自有账号 + 授权 staging 上，**低频**确认控制存在（如重复提交同一下单是否被幂等键拒绝）。**绝不**真实刷量 / 压测 / 抢占库存
- **Example finding**: `api_top10: [API6]`, `cwe: [CWE-799]`, `asvs_mapping: [v5.0.0-8.1.3]`, `description` 写明 flow + 缺失的 anti-automation 控制；与 §5 reliability lens 的 concurrent invocation / capacity ceiling 叠加。

### API7 — Server-Side Request Forgery (SSRF)

endpoint 接受 user-controlled URL 并由服务端发起请求时，能否被诱导访问内网 / 元数据服务 / 任意目标。

- **Look for**:
  - webhook 注册 / `import from url` / avatar-by-url / link preview / PDF-from-url / 服务端 fetch 的 URL 来自 client 且无 allow-list
  - 仅做 blocklist（`block 127.0.0.1`）而非 allow-list（可被 `169.254.169.254` / DNS rebinding / `[::1]` / 十进制 IP / redirect 绕过）
  - 跟随 redirect 不重新校验目标
  - 错误信息回显上游响应（盲 SSRF 变非盲）
- **Test**:
  - static：追 user-URL → outbound request 路径，确认有 scheme allow-list（仅 http/https）+ host allow-list / DNS resolve 后再校验 IP 段 + 禁 redirect 跨域
  - authorized（受限）：仅在自有授权环境，用指向**自己控制的 collaborator endpoint** 的 URL 验证是否发起出站；**绝不**指向云元数据 / 内网 / 第三方——指向内网属 active exploitation，路由 `authorized-pentest-validation`
- **Example finding**: `api_top10: [API7]`, `cwe: [CWE-918]`, `asvs_mapping: [v5.0.0-4.2.2]`, `severity: high|critical`, `exploit_likelihood` 按是否可达元数据评估；主动验证内网可达性 = 越界（§6）。

### API8 — Security Misconfiguration

API 层的配置面：CORS / headers / methods / error verbosity / 默认开启的能力。

- **Look for**:
  - CORS `Access-Control-Allow-Origin: *` 同时 `Allow-Credentials: true`，或 origin 反射无 allow-list
  - 缺安全 headers（API 也应有 `X-Content-Type-Options: nosniff`、合适的 `Cache-Control`、无 stack trace 回显）
  - 启用不必要的 HTTP method（`TRACE` / `OPTIONS` 泄露 / 未用的 `PUT`/`DELETE`）
  - error response 回显 stack trace / SQL / 内部路径（CWE-209）
  - debug endpoint / GraphQL introspection / actuator / `/metrics` 在 prod 暴露
  - 默认凭证 / 默认 admin 路径未禁用
- **Test**:
  - static：审 CORS 配置、error handler、middleware、framework 默认（不发包亦可大量覆盖）
  - authorized：在 staging 抓 response headers（与 orchestrator §16.4 headers 步骤共享 evidence）；确认 prod-like 配置无 introspection / 无 verbose error
- **Example finding**: `api_top10: [API8]`, `cwe: [CWE-16] | [CWE-209] | [CWE-942]`, `asvs_mapping: [v5.0.0-13.1.1]`（configuration）或 `v5.0.0-4.3.1`（API method/CORS）。

### API9 — Improper Inventory Management

版本化 / shadow / zombie / deprecated endpoint 的治理——"不知道自己有多少 API"是最常被遗忘的风险。

- **Look for**:
  - 多版本并存（`/v1` 仍在线但已弃用、无 sunset）
  - shadow endpoint（路由实现存在但不在 OpenAPI/文档/网关清单中）
  - zombie endpoint（旧版本仍可达、仍连旧后端 / 旧权限模型）
  - staging / debug / internal endpoint 在 prod 可达
  - 无 host/endpoint 清单 = 无法评估攻击面；缺 deprecation policy
- **Test（纯 static / inventory，不发包枚举）**:
  - 对照三方清单：实际路由（代码）× OpenAPI/schema × 网关/文档；**差集**即 shadow（代码有文档无）/ stale doc（文档有代码无）
  - 检查版本生命周期标注（`Deprecation` / `Sunset` header、版本下线计划）
  - **不做** 主动 path 枚举 / 字典爆破——那是 active recon，路由 `authorized-pentest-validation`
- **Example finding**: `api_top10: [API9]`, `cwe: [CWE-1059]`（或 inventory-related），`severity: medium|high`, `description` 列出 shadow/zombie endpoint（path 脱敏到结构级，不含敏感参数值）。

### API10 — Unsafe Consumption of Third-Party / Upstream APIs

服务端 **作为 client** 调用第三方 / 内部上游 API 时，是否盲信其响应。

- **Look for**:
  - 第三方响应未 validate 就直接落库 / 渲染（信任边界错置——上游也是不可信输入）
  - 跟随上游返回的 redirect / URL 无校验（SSRF 间接面）
  - 上游 TLS 校验关闭（`verify=False` / `rejectUnauthorized:false`）
  - 上游超时 / 重试 / 熔断缺失（上游慢/挂导致 retry storm、failure cascade）
  - 上游凭证 hardcode（命中 → `security-platform-secrets`）
  - 上游错误数据当可信数据进入业务决策（如计费 / 授权）
- **Test**:
  - static：审 outbound HTTP client 配置（TLS verify、timeout、retry、circuit breaker）+ 上游响应是否过 schema validation 再使用
  - authorized：用 mock / 自有 sandbox 上游返回畸形 / 超大 / 慢响应，确认本服务优雅降级（service virtualization；不打真实第三方）
- **Example finding**: `api_top10: [API10]`, `cwe: [CWE-20] | [CWE-295]`, `asvs_mapping: [v5.0.0-2.2.1]`（input validation 用于上游响应）；retry/cascade 风险叠加 §5 reliability lens failure cascade。

---

## 5. Reliability & Cost Lens（API benign failure modes — 叠加在 attacker-centric 之上）

> 与 `security-governance-threat-modeling §6.5` 同源：API4 / API6 / API10 不只被攻击者滥用，正常负载也会触发资源/成本失效。审 API 时叠加这 6 类：

| Failure mode | API 关联 | 看什么 |
|---|---|---|
| Retry storm | API10 | 上游 5xx 触发客户端无退避重试 → 雪崩 |
| Concurrent invocation | API6 | 限量资源流无并发保护 → 超卖 / 重复 |
| Unbounded resource | API4 | 无 pagination / payload cap → 内存/CPU 打满 |
| Failure cascade | API10 | 上游慢 → 本服务线程池耗尽 → 全站挂 |
| Cost runaway | API4/API6 | 计费操作（LLM/SMS/出站流量）无 per-user 上限 |
| Capacity ceiling | API4 | 无 backpressure → 容量上限处行为未定义 |

---

## 6. Non-Destructive Test Boundary（铁律）

| 允许（本 skill 自己做）| 越界（路由 `authorized-pentest-validation` 手动门）|
|---|---|
| 读路由 / OpenAPI / GraphQL schema（static） | 任何 active fuzz / 字典爆破 / path 枚举 |
| 用**自有授权测试账号**做 read-only 跨账号 BOLA 逻辑验证 | 真实读取 / 修改 / 删除他人数据 |
| PATCH **自己的**对象塞额外字段验 mass assignment（可逆 + 立即还原）| 提权后执行真实管理操作 |
| 在自有 staging 抓 response headers / 验配置 | 对 production host 任何 active 操作（即使有 ROE 也 hard-deny）|
| SSRF：仅指向**自己控制的** collaborator endpoint | SSRF 指向云元数据 / 内网 / 第三方 |
| 用 mock 上游返回畸形响应验降级 | DoS / flood / 压测 / 真实刷量 |

- 任何"主动证明可利用"的步骤 = active validation，**不在本 skill 范围**，路由 `pentest-scope-and-roe` → `authorized-pentest-validation`（manual hard gate）。
- 测试账号必须是项目方授权的、本就属于 caller 的账号；**绝不**伪造 / 窃取 / 复用他人凭证。
- 与 orchestrator §12 一致：不读 `.env*` / `secrets/**` / `*.pem` / `*.key`；任何 finding 落盘前走 `appsec-sdk redact`。

---

## 7. AuthZ Test Matrix（object × function × property — 核心交付物）

三个授权维度正交，必须分别覆盖。对 §3 inventory 每个 endpoint 填一行：

| Endpoint (method path) | Object-level (API1) | Function-level (API5) | Property-level (API3) |
|---|---|---|---|
| `GET /api/orders/{id}` | caller owns order? (DB-layer predicate) | 该 role 可读 order? | response 仅返回允许字段? |
| `PATCH /api/users/{id}` | caller == {id} 或 admin? | 该 role 可改 user? | body 仅允许 self-editable 字段（拒 `role`/`is_admin`）? |
| `DELETE /api/admin/users/{id}` | N/A（admin 全局） | **仅 admin**? (server-side guard) | N/A |
| `POST /graphql` (mutation) | per-node owner? | per-mutation role? | per-field authZ on input/output? |

- **每格三态**：`enforced (server-side, 有证据)` / `missing` / `client-side-only`（= missing）。
- 矩阵任一格 `missing` 且涉敏感 object/function/field → 出 finding（API1 / API5 / API3 对应）。
- 矩阵是 review 的可审计骨架，进 §8 输出契约。

**正交性提醒**：API1（这个 object 是不是你的）≠ API5（你这个角色能不能调这个 function）≠ API3（这个 object 的这个字段你能不能读/写）。三者其一通过不代表另两个通过——分别测。

---

## 8. Output Contract

每次 review 产出：

1. **Endpoint inventory matrix**（§3 Step 0：method / path / auth / role / object-id 参数 / body 字段 / 返回字段）
2. **AuthZ test matrix**（§7：object × function × property，每格 enforced/missing/client-only + evidence）
3. **API Top 10:2023 coverage**：API1–API10 逐条 PASS / FINDING / N/A（每条附 §4 的 look-for 结论）
4. **Reliability & cost lens**（§5 六类 benign failure mode 结论）
5. **Findings** —— 全部经 `appsec-sdk finding.add <file>`（redact-first）落 `.appsec/findings/<tag>/`，符合 orchestrator §9 schema v1.0：
   - `source: manual_review`（或 sast 命中）；`api_top10: [API<n>]`；`severity` **小写**（critical/high/medium/low）
   - `asvs_mapping` 用版本化三段格式 `v5.0.0-<ch>.<sec>.<req>`（正则 `^v5\.0\.0-\d+\.\d+\.\d+$`；ASVS V4 API / V6 Auth / V7 Session / V8 Authorization / V9 Tokens）
   - `cwe`、`owasp_top10`（如适用，`A<n>:2025`）、`reproduction_steps`（**禁含 raw secret / raw token / 真实 object id**——脱敏）
   - **绝不** Write 直写 `.appsec/findings/**`（orchestrator hook §18.5 物理拦）；只走 sdk
6. **路由**：high+ finding → `security-remediation`（fix → 回归测试）；base auth 缺口 → 引用/路由回 `appsec-reviewer`（ASVS V6/V7/V8），不在此重复；secret 命中 → `security-platform-secrets`；需主动验证可利用性 → `pentest-scope-and-roe` → `authorized-pentest-validation`
7. **回灌 orchestrator**：本 overlay 落 `.appsec/evidence/<tag>/overlay-api/checklist.yaml`（API1–API10 + authZ matrix 状态），供 §16.9 evidence-validator 判 release decision（缺 checklist → validator BLOCK）；映射 orchestrator §13 Release Evidence **§7 API Security**

---

## 9. Hard Rules

- ❌ **不**做 active exploitation（fuzz / 爆破 / 真实 CRUD 他人数据 / DoS / SSRF 打内网）—— 越界即 `authorized-pentest-validation`
- ❌ **不**把"id 不可预测"当作 object-level authZ（obscurity ≠ authorization）
- ❌ **不**信任 client 自报的 user_id / role / tenant_id —— 永远 server/session-derived
- ❌ **不**把"已登录 / 有 role"等同于"对这个具体 object 有权"（API1 与 API2/API5 是不同维度）
- ❌ **不**用前端隐藏字段代替后端 property-level authZ（API3 两面都要后端 enforce）
- ❌ **不**只用 blocklist 防 SSRF（必须 allow-list scheme + host/IP）
- ❌ **不**对 production host 做任何 active 操作（即使持有 ROE 也 hard-deny，与 orchestrator §18.2 一致）
- ❌ **不**重复 base authentication/session finding（COMPOSES on ASVS V6/V7/V8；引用，不 fork）
- ❌ **不**直写 `.appsec/findings/**` —— 必须 `appsec-sdk finding.add`（hook §18.5）
- ❌ **不**在 chat / report / finding 中输出 raw token / raw secret / 真实 object id —— 落盘前走 `appsec-sdk redact`
- ❌ **不**读 `.env*` / `secrets/**` / `*.pem` / `*.key`
- ❌ **不**靠主动 path 枚举做 API inventory（用 code × OpenAPI × gateway 三方对照的 static 差集）

---

## 10. Anti-patterns

- ❌ "有 auth middleware 就安全" —— middleware 验"谁"，不验"这个 object/function 是不是你的"（BOLA/BFLA 专绕）
- ❌ "ORM 自动加 owner_id" —— 一旦 raw query / `findById` bypass 就漏（同 multitenant 教训）
- ❌ "response 字段前端不显示就行" —— API3 excessive exposure 看的是 wire 上返回了什么
- ❌ "body 直接 spread 进 model 省事" —— mass assignment 头号入口；必须 allow-list DTO
- ❌ "GraphQL 一个 endpoint，授权一次就够" —— 每个 resolver/mutation/field 都是独立授权面
- ❌ "限流在网关做了" —— per-user / per-flow / GraphQL cost 仍可能缺（API4/API6）
- ❌ "第三方 API 是可信的" —— 上游响应也是不可信输入（API10），需 validate + TLS verify + timeout
- ❌ "旧版本没人用了" —— zombie endpoint 常带旧权限模型，是真实攻击面（API9）
- ❌ "blocklist 127.0.0.1 防住 SSRF 了" —— `169.254.169.254` / DNS rebinding / redirect / 十进制 IP 全绕（API7）
- ❌ "BOLA 测了就不用测 BFLA" —— object / function / property 三维正交，分别测（§7）

---

## 11. References

- [OWASP API Security Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [OWASP ASVS 5.0 — V4 API / V6 Authentication / V7 Session / V8 Authorization / V9 Tokens](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP API Security Project](https://owasp.org/www-project-api-security/)
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md) — §5.2 app layer / §6.3 API Top 10 mapping / §9 finding schema / §16.3 overlay activation / §18 hooks
- [appsec reviewer base auth (ASVS V6/V7/V8)](../appsec-security-orchestrator/SKILL.md) — §16.5 Defensive Code Review (this skill COMPOSES on top, does NOT duplicate)
- [security-app-multitenant](../security-app-multitenant/SKILL.md) — tenant dimension of BOLA (API1) / BFLA (API5)
- [security-governance-threat-modeling](../security-governance-threat-modeling/SKILL.md) — §6.5 reliability & cost lens
- [security-remediation](../security-remediation/SKILL.md) — downstream fix + regression
