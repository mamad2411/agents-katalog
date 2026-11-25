---
name: security-app-multitenant
canonical_id: security.app.multitenant
aliases: [multitenancy-security, tenant-isolation, multi-tenant]
version: 1.0.0
status: stable
created_date: 2026-05-25
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - OWASP Multi-Tenant Security Cheat Sheet: living reference, checked 2026-05-25
  - OWASP ASVS: 5.0 (V4 API + V8 Authorization)
  - OWASP API Top 10: 2023 (API1 BOLA + API5 BFLA)
  - NIST CSF: 2.0 (PR.AC)
  - SOC2: 2017 TSC CC6 Logical Access (multi-tenant common control)
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "tenant_data/raw/**"]
  redact_on_output: ["tenant IDs in production", "real customer identifiers", "tokens"]
upstream:
  - appsec-security-orchestrator
  - security-governance-threat-modeling
downstream:
  - security-remediation
  - appsec-security-orchestrator (back with findings)  # IAM concerns → orchestrator §5.3 iam capability (no dedicated skill yet)
description: >-
  Multi-tenant isolation overlay - traces tenant ID propagation through every layer: request, auth, query, cache, log, background job, analytics, webhook, backup, export. Overlays tenant isolation on IAM patterns rather than replacing IAM design.
trigger_phrases:
  - multi-tenant / 多租户 / multitenancy / SaaS
  - tenant isolation / 租户隔离
  - cross-tenant / 跨租户
  - BOLA / IDOR with tenant
  - row-level security / RLS / tenant RLS
  - tenant aware cache / per-tenant background job
---

# Security App — Multi-Tenancy

## 1. Mission

多租户的核心安全风险：**tenant ID 在某一层丢失**。本 skill 系统性检查 tenant boundary 在所有层是否被尊重——request 入口、auth、query、cache、log、background job、analytics、webhook、backup、export。任一层 leak = 跨租户数据 breach。

**职责边界**：
- **owns**: tenant boundary 验证 + 跨租户 risk patterns + 隔离策略选型
- **不做**: IAM 整体设计——route IAM concerns to orchestrator §5.3 iam capability (no dedicated skill yet)；不做 application logic 重构

---

## 2. Activation Triggers

| Trigger | Action |
|---|---|
| SaaS（多客户共享 infrastructure）| 默认激活 |
| B2B 平台带 customer accounts | 默认激活 |
| Shared database / schema with tenant_id column | 默认激活 |
| Per-tenant subdomain / per-tenant DNS | 激活 + DNS injection 审 |
| Per-tenant K8s namespace | 激活 + namespace isolation 审 |
| Per-tenant database / schema | 激活 + connection routing 审 |
| Per-tenant encryption key | 激活 + key derivation 审 |

---

## 3. Isolation Strategies（选型决策）

| Strategy | 描述 | 隔离强度 | 成本 |
|---|---|---|---|
| **Shared everything** | 一个 DB / 一个 schema / tenant_id 列 | 弱（依赖应用层）| 低 |
| **Shared DB, separate schemas** | 一个 DB / 每租户一 schema | 中 | 中 |
| **Separate DB per tenant** | 每租户一 DB instance | 强 | 高 |
| **Separate infrastructure per tenant** | 每租户独立 VPC / cluster | 极强 | 极高（适合 enterprise / regulated）|
| **Hybrid** | 大客户独立，小客户共享 | 灵活 | 复杂 |

**默认建议**：shared DB + RLS (Row-Level Security) + tenant-scoped connection pool + 应用层强制 tenant_id 校验（多层防御）。

---

## 4. Critical Layers Checklist（每一层必须验证 tenant boundary）

> **核心 12 层 = 最低要求**。下方 §4.13-§4.18 是 SaaS 常被遗漏的 6 个隔离面，处理 PII / payment / regulated 数据必检。

### L1: Request entry
- [ ] Tenant ID 从哪获取？JWT claim / subdomain / path / header
- [ ] 一个请求只能携带一个 tenant context（禁止 multi-tenant 同 session）
- [ ] tenant ID 校验：存在 + 用户属于该 tenant + tenant active
- [ ] Subdomain hijack 防护（DNS verify + SPF/DKIM/DMARC for tenant emails）

### L2: Authentication
- [ ] User 凭证 scoped to tenant（不能 user A in tenant 1 access tenant 2）
- [ ] Session 含 tenant context
- [ ] Token (JWT) 含 tenant_id claim + signature
- [ ] Re-auth on tenant switch（若 user 跨 tenant）

### L3: Authorization
- [ ] 每个 resource access：先验 user 属于 tenant，再验 user 对 resource 有权限
- [ ] RBAC role scoped per tenant（admin in tenant 1 ≠ admin in tenant 2）
- [ ] No global super-user that traverses tenants without explicit audit
- [ ] Object-level authz: resource.tenant_id == request.tenant_id

### L4: Database query
- [ ] **All queries** include tenant_id WHERE clause（or RLS enforces）
- [ ] RLS policies cover all tables containing tenant data
- [ ] No raw SQL bypassing ORM tenant scope
- [ ] Connection pool 不跨 tenant 重用（如用 separate DB / schema strategy）
- [ ] Migrations test on multi-tenant data

### L5: Cache (Redis / Memcached / 应用内存)
- [ ] Cache key 含 tenant_id（如 `tenant:123:user:456:profile`）
- [ ] Cache TTL 一致防 stale data 跨 tenant 残留
- [ ] Cache invalidation 不跨 tenant
- [ ] Local in-memory cache 不被 cross-request 复用 without tenant check

### L6: Logging
- [ ] 每条 log 含 tenant_id field
- [ ] Log query / dashboard scoped per tenant（debug 一个客户问题不应见其他客户）
- [ ] Sensitive data redaction tenant-aware

### L7: Background jobs / queues
- [ ] Job payload 含 tenant_id
- [ ] Queue worker 按 tenant 处理（不混 tenant）
- [ ] Job result 写回正确 tenant 的 storage
- [ ] Job retry 不跨 tenant（如 dead-letter queue 仍 tenant-scoped）

### L8: Analytics / metrics
- [ ] Per-tenant metrics（不只 global）
- [ ] Cross-tenant query 需 explicit admin role + audit
- [ ] Aggregated metrics 不 leak tenant size / activity to other tenants

### L9: Webhooks / outbound
- [ ] Outbound webhook destination scoped per tenant
- [ ] Webhook payload 不含其他 tenant 数据
- [ ] Webhook secret 独立 per tenant
- [ ] Webhook delivery 不阻塞 other tenants（独立 queue / retry）

### L10: Backup
- [ ] Backup includes tenant_id（restore 时不混 tenant）
- [ ] Per-tenant backup retrieval / export support
- [ ] Backup 不在 tenant 注销后保留（GDPR / PIPL right to delete）
- [ ] Backup encryption key 跨 tenant 分离（如适用）

### L11: Export / data portability
- [ ] User 只能 export 自己 tenant 的数据
- [ ] Bulk export rate-limited per tenant
- [ ] Export 不含其他 tenant references（如 reference IDs leaked through joins）

### L12: Admin / support tooling
- [ ] Support agent access scoped + audited（"break-glass" with full audit trail + customer notification）
- [ ] Tenant impersonation feature（如有）必有 audit + customer transparency
- [ ] Admin dashboard 不默认见所有 tenant data

---

## 5. Common Attack Patterns

| Attack | 描述 | Defense |
|---|---|---|
| **BOLA across tenants** | 修改 URL ID 访问其他 tenant 资源 | Object-level authz: resource.tenant_id == request.tenant_id |
| **Subdomain hijack** | DNS / hosting 配置错让 attacker 注册 `evil.app.com` | Strict subdomain validation + DNS health check |
| **JWT tenant claim tampering** | 修改 JWT 中 tenant_id（若签名弱）| Strong JWT signature + tenant_id 必须 server-side verify |
| **Cache poisoning across tenants** | Cache key 缺 tenant_id | Cache key 强制 tenant prefix |
| **Background job cross-tenant** | Worker 处理时丢 tenant context | Job payload mandatory tenant_id + worker assert |
| **Analytics leak** | Aggregated stats reveal tenant size / patterns | k-anonymity / differential privacy |
| **Backup restore mix** | Restore 时混 tenant data | tenant-scoped restore + verification |
| **Support tool over-access** | 支持工程师能看所有 tenant data | 最小权限 + audit + customer notification |
| **Webhook delivery leak** | Webhook 发到错误 tenant URL | Outbound destination 配置 per tenant + signature |

---

## 6. RLS (Row-Level Security) Pattern (PostgreSQL example)

```sql
-- 启用 RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- 强制：连接 session 必须 SET app.current_tenant_id
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- Force RLS even for table owners
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- 应用层连接每次都设：
-- SET app.current_tenant_id = '<tenant-uuid>';
-- 永不用没设这个 GUC 的连接做 query
```

**Hard rule**: RLS 是 defense-in-depth，**不替代**应用层 tenant_id WHERE 校验。两层都要。

---

## 7. Hard Rules

- ❌ **不**用 global super-user 跨 tenant 而不 audit
- ❌ **不**让 cache key 缺 tenant prefix
- ❌ **不**让 background job 缺 tenant payload
- ❌ **不**让 log 缺 tenant_id field
- ❌ **不**让 raw SQL 绕过 ORM tenant scope
- ❌ **不**用 separate DB strategy 时 connection pool 跨 tenant 复用
- ❌ **不**让 backup restore 混 tenant 数据
- ❌ **不**让 support tool 默认见所有 tenant data
- ❌ **不**让 admin 跨 tenant 看数据无 audit + customer notification
- ❌ **不**忽略 webhook outbound 的 tenant scoping
- ❌ **不**用 application-layer tenant check **代替** RLS（要双层 defense）

---

## 8. Anti-patterns

- ❌ "RLS 就够了" — RLS 是最后防线，应用层校验是第一线
- ❌ "ORM 自动加 tenant_id" — 一旦 raw SQL bypass 就完
- ❌ "我们 dashboard 让运营看所有 tenant" — 必须 audit + customer transparency
- ❌ "Cache TTL 短点就不会 leak" — TTL 不解决 cache key 问题
- ❌ "Background job 用 tenant_id 即可" — 还要 worker 自己 assert
- ❌ "Tenant 注销后数据保留 90 天" — 必须 GDPR / PIPL right to delete 流程
- ❌ "Subdomain wildcard cert 就够" — 还要 DNS verify + 防 subdomain takeover
- ❌ "Support tool 内部用，不审" — 内部权限滥用是 SaaS breach top cause
- ❌ "我们用 separate DB strategy，自动隔离" — connection pool 重用、migration 跨实例都是坑

---

## 9. Output Contract

每次 review 产出：

1. Isolation strategy 决定 + rationale
2. 12-layer checklist coverage matrix（每层 evidence）
3. RLS policies inventory + force RLS 状态
4. Common attack pattern verification（每种 attack 已验证 mitigation）
5. Tenant lifecycle policy（onboarding / data export / deletion / archive）
6. Support / admin tooling audit policy
7. SECURITY.md multi-tenant section + AppSec Release Evidence §12 叠加层
8. **Findings** —— 全部经 `appsec-sdk finding.add <file>`（canonical path，redact-first）落 `.appsec/findings/<tag>/`，符合 orchestrator §9 finding schema v1.0：
   - `source`（`manual_review` 或扫描命中）；`severity` **小写**；`cwe`（跨租户多为 `CWE-639` / `CWE-285`）；`api_top10`（如 `[API1]` BOLA / `[API5]` BFLA）；`reproduction_steps`（**禁含 raw tenant id / 真实 customer 标识 / token**——脱敏）
   - `asvs_mapping` 用版本化三段 `v5.0.0-<ch>.<sec>.<req>`（正则 `^v5\.0\.0-\d+\.\d+\.\d+$`；Authorization 用 ASVS V8），不用 4.x 旧标签
   - **绝不** Write 直写 `.appsec/findings/**`（orchestrator hook §18.5a 拦 Write/Edit/MultiEdit）；只走 sdk
   - high+ finding → `security-remediation`（fix → 回归测试）；IAM 模型缺口 → 回灌 orchestrator §5.3 iam capability

### 9.1 Overlay Evidence Contract（满足 release gate — 不可省）

> 起因：appsec-evidence-validator（orchestrator §16.9 check #3）对**每个激活的 overlay** HARD-REQUIRE `.appsec/evidence/<tag>/overlay-<name>/checklist.yaml`，缺一即 release **BLOCKED**。本 overlay 的 `<name>` = `multitenant`。

每次 review 结束，**两步落盘**（按序）：

1. **标记 overlay active**：
   ```bash
   appsec-sdk overlay.activate "<release-tag>" multitenant
   # → 建 .appsec/evidence/<tag>/overlay-multitenant/ + 写 .activated 标记
   ```
2. **写 overlay checklist evidence**（validator 真正校验的文件）：
   - 写 `.appsec/evidence/<release-tag>/overlay-multitenant/checklist.yaml`
   - 直接 Write 即可（evidence 路径不被 hook 拦；只有 `.appsec/findings/**` + `.appsec/decisions/**` 被 §18.5a 拦）
   - 内容：把 §4 的 12-layer checklist（L1-L12，含 §4.13-§4.18 补充层如适用）逐项转成 `items[]`（每项 `id` / `requirement` / `asvs_ref`（`v5.0.0-8.x.x`）/ `status: pass|fail|na|not_tested` / `evidence_ref` / `notes`）+ `summary{total, pass, fail, na}`
   - 任何 `status: fail` 在 `evidence_ref`/`notes` 引用对应 `finding.add` 出的 finding id（finding 本体走 sdk，不塞 checklist）
   - 模板：[`appsec-security-orchestrator/templates/overlay-checklist.template.yaml`](../appsec-security-orchestrator/templates/overlay-checklist.template.yaml)（含 multitenant 示例 items：tenant isolation / cross-tenant IDOR / row-level security / cache+job tenant-scoping / admin cross-tenant audit）

无此 checklist.yaml → §16.9 validator BLOCK 整个 release。

---

## 10. References

- [OWASP Multi-Tenant Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)
- [OWASP API Top 10 2023 API1 BOLA + API5 BFLA](https://owasp.org/www-project-api-security/)
- [PostgreSQL Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [AWS Multi-Tenant SaaS Patterns](https://aws.amazon.com/blogs/apn/category/saas-and-apn/)
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md) — §9 finding schema / §16.3 overlay activation / §16.9 evidence validation / §18.5a finding-path hook
- [overlay-checklist.template.yaml](../appsec-security-orchestrator/templates/overlay-checklist.template.yaml) — overlay-multitenant/checklist.yaml 模板
- [security-app-api](../security-app-api/SKILL.md) — API1 BOLA / API5 BFLA tenant 维度
- [security-governance-threat-modeling](../security-governance-threat-modeling/SKILL.md) — must include multi-tenant boundary in STRIDE
