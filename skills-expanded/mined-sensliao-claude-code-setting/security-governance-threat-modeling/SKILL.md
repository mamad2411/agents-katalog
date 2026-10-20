---
name: security-governance-threat-modeling
canonical_id: security.governance.threat_modeling
aliases: [threat-modeling, stride-workshop, security-threat-model]
version: 1.0.0
status: stable
created_date: 2026-05-25
allowed-tools: Read, Write, Edit, Grep, Glob
forbidden-tools: WebFetch, Bash
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - NIST SP 800-154: 1.0 (initial public draft, threat modeling)
  - NIST CSF: 2.0 (ID.RA)
  - OWASP Threat Modeling: latest
  - STRIDE: 6-category model
  - OWASP ASVS: 5.0 (V1)
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key"]
  never_write: ["real PII in threat scenarios"]
  redact_on_output: ["customer names", "internal IPs", "tokens"]
upstream:
  - appsec-security-orchestrator
  - uiux-product-orchestrator  # production UI architectural change
  - gsd-pipeline-orchestrator  # plan-phase needs threat model
downstream:
  - security-remediation  # if scoping reveals findings
  - appsec-security-orchestrator  # back to orchestrator with output
  - pentest-scope-and-roe  # if model surfaces need for active validation
description: >-
  Structured threat modeling producing a STRIDE register, abuse cases, attack surface inventory and control gap analysis that feed the Risk Register and downstream remediation. Maps to NIST CSF 2.0 ID.RA. Triggers on a new system, new external interface, auth model change, third-party integration, file upload, multi-tenancy, GenAI-agent introduction, or major architecture refactor. Performs no active testing.
trigger_phrases:
  - threat model / 威胁建模 / STRIDE / 攻击面 / abuse case
  - 安全架构评审 / 架构变更安全审 / 新接口安全评估
  - threat modeling workshop / DFD / data flow diagram
---

# Security Governance — Threat Modeling

## 1. Mission

把"系统里哪里可能被攻击、为什么、怎么防"用**结构化方法**回答出来，产物落到可追踪的工件（threat register、DFD、abuse cases、control gap），下游 risk register / remediation / pentest 都从这里取上下文。

**职责边界**：
- 仅做 **threat modeling**：识别威胁、列控制缺口、产出文档
- **不做**：active testing、code-level remediation、风险接受决策
- **不替代** SAST/DAST/pentest——它们是验证手段，本 skill 是发现手段

---

## 2. Activation Triggers（什么时候必须激活）

任一条件成立即触发：

| Trigger | Why |
|---|---|
| 新系统立项 / 重大功能 | 建立首版攻击面台账 |
| 新对外接口 (REST / GraphQL / Webhook / WebSocket) | 接口 = 新攻击向量 |
| 认证 / 授权模型变化 | 触发完整 ASVS V6/V7/V8 复审 |
| 第三方集成引入（OAuth、payment、AI provider） | 信任边界外移 |
| 文件上传引入 | OWASP File Upload Cheat Sheet 强制场景 |
| 多租户引入 | 隔离边界设计核心场景 |
| WebSocket / SSE 长连接 | 传统 HTTP threat 模型不覆盖 |
| GenAI / Agent / LLM 引入 | 需叠加 LLM Top 10 + Agentic threats |
| 敏感数据分类升级 | 数据流图 + 加密策略需重审 |
| 主架构 refactor | DFD 失效，需重建 |
| 12 个月强制 review | 时效控制 |

---

## 3. Inputs（需要先准备好的材料）

无以下材料则**先 block 用户补齐**，不要盲跑：

| Input | Source |
|---|---|
| 系统架构图 / DFD（或可由 code 推导） | docs/architecture / 代码读图 |
| 组件清单 | docs 或 manifest |
| 主要数据类别（PII / 支付 / 健康 / 凭证） | data dictionary |
| 外部依赖列表 | package.json / requirements / Cargo.toml |
| 身份与认证模型说明 | auth design doc / SECURITY.md §4 |
| 部署拓扑（含云、CDN、WAF） | infra docs / IaC |
| 第三方 / 供应商边界 | vendor list / SLA |
| 现有例外项 | risk register |

如系统涉及个人信息 / 跨境数据，**必须**同步拉法务 / 隐私角色，因为数据类别和流向会直接影响后续控制要求。

---

## 4. Standard Workflow

```
Step 1  确认 trigger 并拉齐 §3 inputs
        → inputs 不全 → 反向问用户补，不盲跑

Step 2  绘制 DFD（Data Flow Diagram）
        → 列 component / data flow / trust boundary
        → 每条 boundary 标 control mechanism
        → 用 templates/threat-model-STRIDE.md §2 起手

Step 3  对每个 (component, data flow, trust boundary) 做 STRIDE
        → S Spoofing — 身份伪造
        → T Tampering — 数据篡改
        → R Repudiation — 否认 / 缺乏审计
        → I Information Disclosure — 信息泄露
        → D Denial of Service — 拒绝服务
        → E Elevation of Privilege — 提权
        → 至少每个核心 component 6 类都过一遍

Step 4  写 abuse cases
        → 每个 use case 写一个 abuse case
        → 重点：业务逻辑攻击（Top 10 漏报区）

Step 5  做 attack surface inventory
        → 每个 entry point 列：Auth / Authz / Rate Limit / Input Schema / 当前状态

Step 6  做 cryptography 决策记录
        → TLS / 密码存储 / token 签名 / 数据 at-rest / 随机源

Step 7  汇总 control gap inventory
        → 表格里所有 OPEN + abuse cases 没覆盖 + attack surface 标 🟡
        → 每个 gap 必须对应 Risk Register entry

Step 8  标准映射
        → 对齐 NIST CSF 2.0 ID.RA / PR.AC / PR.DS
        → 对齐 OWASP ASVS 5.0 控制章节
        → 对齐 NIST SP 800-154

Step 9  设定 re-modeling triggers
        → 写下下次强制 review 日期

Step 10 输出
        → 一份完整 threat-model-STRIDE.md（per system / feature，human-readable 必出）
        → 导出 4 个机读 JSON（§8.5：threat-model.json / components.json /
          dfd.json / attack-surface.json），经 `appsec-sdk evidence.append
          <tag> threat-model` 落盘（喂 security-viz / control.coverage / remediation）
        → 把所有 OPEN gap 注入项目 risk-register.md
        → handoff 回 appsec-security-orchestrator
```

---

## 5. STRIDE Quick Reference

| Category | 关注 | 典型 control |
|---|---|---|
| **S** Spoofing | 身份真实性 | 强认证、TLS + cert validation、HMAC、JWT 签名 |
| **T** Tampering | 数据完整性 | 签名 / 哈希、parameterized queries、HSTS、SRI |
| **R** Repudiation | 不可抵赖 | 审计日志（含 user + timestamp + action）、签名收据 |
| **I** Information Disclosure | 保密性 | 加密 at-rest / in-transit、最小权限、output filter、log redaction |
| **D** Denial of Service | 可用性 | 速率限制、配额、超时、circuit breaker、自动 scale |
| **E** Elevation of Privilege | 授权 | server-side authz、resource-level check、最小权限、separation of duties |

---

## 6. 特殊场景叠加规则

| 场景 | 必须叠加的检查 |
|---|---|
| 文件上传 | OWASP File Upload Cheat Sheet 全项（content sniff / 沙箱 / 病毒扫 / Content-Disposition: attachment） |
| 多租户 | OWASP Multi-Tenant Cheat Sheet（每个 query / cache / log 是否带 tenant ID） |
| WebSocket / SSE | OWASP WebSocket Cheat Sheet（握手 / origin check / 消息校验 / 限流 / 断连） |
| Webhook 接收 | HMAC 签名验证 + replay protection（timestamp + nonce） |
| GenAI / Agent | OWASP LLM Top 10 + Agentic AI threats（tool perms / memory poisoning / indirect prompt injection / human override / rollback） |
| Payment | PCI DSS scope（SAQ Level）+ 不存 PAN / CVV |
| 中国 PI / 跨境 | PIPL data minimization + 数据出境评估（必要时 CAC 申报） |

---

## 6.5. Reliability & Cost Failure Modes (R&C Lens — beyond STRIDE)

> **Added 2026-05-26 — 缘起：Agent Atlas Phase 1 STRIDE 跑完仍漏掉 cron 并发烧钱 + Vercel IP allowlist 假阳两个 PLAN 级问题。**

STRIDE 默认是 **attacker-centric** 视角，但有一类失稳是 **benign** 的——没有恶意攻击者，平台 / 服务 / 调度系统自身特性导致系统失稳或烧钱。这类失败模式必须独立建模，否则 STRIDE 表过了仍会被它们打穿。

对每个核心 component / data flow，按以下 6 类问：

| Category | 关注 | 典型场景 | 典型 control |
|---|---|---|---|
| **R&C-1 Retry storms** | 调度系统 / webhook / cron 自身的 retry 行为 | Vercel Cron 重复触发同一 endpoint；Stripe webhook 3xx/5xx 时 retry；客户端无 backoff 重试 | server-side idempotency key + observable retry budget + advisory lock |
| **R&C-2 Concurrent invocation** | 同一资源被并发触发，在 dedup 检查前就已花费成本 | 两个 cron 实例同时跑同一 agent 的 tick，**都打** Google Places + LLM，最后只有一个 INSERT 成功（UNIQUE 防的是 DB 重复，不防资金重复） | per-key advisory lock 在花钱操作 **之前** + singleflight 模式 + 队列化 + lock-then-spend 顺序 |
| **R&C-3 Unbounded resource** | tokens / API quota / DB connections / file handles 无上限 | LLM 输出无 maxTokens cap → 单次 $100；Postgres 无 statement_timeout → 慢查询挂池；图片处理无 memory cap → OOM | per-call cap + per-user-per-day cap + 资源池上限 + 预算告警 |
| **R&C-4 Failure cascade** | 一个 dep 故障，所有 caller 同步重试 → 雪崩 | Stripe API 5xx，下游所有 webhook handler 拒绝写库 → 数据丢失；LLM provider 故障，所有 tick 同步重试 → 自身被限流 | circuit breaker + bulkhead isolation + graceful degradation + dead letter queue |
| **R&C-5 Cost runaway** | per-call 成本 × 实际 scale > 预算 | LLM 输入暴涨 10× → 月账单暴涨 100×；Google Places per-photo $0.007 × 用户增长曲线；无 cap 的 webhook bombing 触发 Stripe billing | per-account / per-user 月预算硬 cap + cost monitoring alert + circuit break on budget exceeded |
| **R&C-6 Capacity ceiling** | 平台 / 服务套餐的硬上限 | Vercel Hobby 10s function timeout；Vercel free 无 stable egress IP（IP allowlist 不可用，需 Pro+ Static IPs / Enterprise Secure Compute）；Supabase free pgvector 限额；Stripe sandbox transaction 上限 | 文档化平台限制 + plan upgrade decision + 设计兼容 fallback + 不假设 IP/IO/容量"默认可用" |

### 强制覆盖规则

- **每个 cron / scheduler / async job endpoint** 必须过 R&C-1 + R&C-2
- **每个 LLM / 付费第三方 API 调用** 必须过 R&C-3 + R&C-5
- **每个跨服务依赖** 必须过 R&C-4
- **任何使用 PaaS（Vercel / Netlify / Supabase / Stripe / etc.）的设计** 必须过 R&C-6
- 在 `threat-model-STRIDE.md` 加 §3.5 "R&C Register" 表（结构与 §3 STRIDE Register 相同：ID / Component / Category / Scenario / Existing Control / Gap / Owner / Disposition），把 R&C OPEN 项也注入 `risk-register.md`，与 STRIDE OPEN 同等优先级处理

### 为什么独立成节（不并入 STRIDE D Denial of Service）

R&C 故障不是 attacker → 用 STRIDE 6 类硬套（"Denial of Service" 太狭窄、"Tampering" 不贴切）会逼模型选错 category，结论失真。**独立 R&C 让 facilitator / model 心智简单**：先 STRIDE 抓恶意，再 R&C 抓 benign。

### 与上游 orchestrator 的关系

`gsd-pipeline-orchestrator` execution rule 13 明确要求：任何 threat-modeling skill 调用必须输出 R&C Register。Skip 该 lens = 漏 benign cost-runaway / capacity-ceiling 漏洞，属于 orchestrator 阶段 hygiene 违规。

---

## 7. Hard Rules

- ❌ **不**做 active testing / probe / scan
- ❌ **不**绕过 inputs 检查（§3 任一缺失就 block）
- ❌ **不**把 threat model 写成 generic checklist——必须结合本系统具体上下文
- ❌ **不**把 STRIDE 当成"全部"——业务逻辑攻击（API6 / API10）是 STRIDE 弱项，必须额外 abuse cases 补
- ❌ **不**漏 Recover 维度——Threat Model 末尾必须问"如果这个攻击成功，怎么恢复"
- ❌ **不**只做一次——每次架构变更必须 re-model
- ❌ **不**单线作战——必须 architect / dev lead / AppSec 三方在场

---

## 8. Output Contract

> **v3.0 evidence sink**: machine-readable findings MUST be written via `appsec-sdk finding.add` (schema-validated against orchestrator §9, redacted first). Direct Write to `.appsec/findings/**` is blocked by the PreToolUse hook. The markdown report (risk-register.md) is the human-rendered view only.

每次 threat modeling 必须产出：

1. `threat-model-STRIDE.md`（per system / feature）— 完整 STRIDE 模板填写（**human-readable，必出**）
2. `threat-model-STRIDE.md §3.5 R&C Register` — 6 类 benign 失效模式覆盖（§6.5 强制要求）
3. **Machine-readable JSON outputs（§8.5，additive — 不替代 markdown）** — 4 个文件经 `appsec-sdk evidence.append <tag> threat-model` 落盘，喂下游自动化（security-viz / control.coverage / remediation routing）。**注（analysis-only 边界）**：本 skill frontmatter 是 `forbidden-tools: Bash`，**不自己跑** `appsec-sdk`——它只负责*生成* JSON 内容（分析产物），落盘（`evidence.append`）由**上游 orchestrator（已激活 Bash）或后续 Bash-capable dispatch 步骤**执行。这不是契约冲突：skill 保持纯分析/Read-only，持久化是 appsec-sdk 层的职责（详 §8.5 落盘说明）。
4. `risk-register.md` 更新（每个 STRIDE OPEN gap **和** R&C OPEN gap → 一条 Risk Register entry，同等优先级处理）
5. Threat Model 摘要回写到 `SECURITY.md` §1-3
6. Trigger conditions for re-model 写明
7. 下次 review 日期

---

## 8.5. Machine-Readable JSON Output Contract (additive — feeds downstream automation)

> **Added 2026-06-14 (A1 D3 / A5).** 起因：threat model 此前**只有** markdown（`threat-model-STRIDE.md`），下游无法机器消费——`security-viz` 画不出 Security Architecture Diagram / DFD（A5 记录当前 DFD 是 ASCII-only，blocks viz），`control.coverage` 无法 cross-check ASVS 映射，remediation routing 拿不到结构化 threat 列表。
>
> **原则**：markdown 仍是 human-readable 真相源、**仍必出**；JSON 是**叠加**输出，不替代。两者内容必须一致（同一份 STRIDE register，两种渲染）。

每次 threat modeling 在写完 markdown 后，**额外**生成以下 4 个 JSON 工件，并**逐个**经 SDK 落盘：

```bash
# 落盘命令（每个 JSON 一次；evidence.append 从 stdin 读 piped content）
printf '%s' "$THREAT_MODEL_JSON" | bash ~/.claude/scripts/appsec-sdk.sh evidence.append <release-tag> threat-model
printf '%s' "$COMPONENTS_JSON"   | bash ~/.claude/scripts/appsec-sdk.sh evidence.append <release-tag> threat-model
printf '%s' "$DFD_JSON"          | bash ~/.claude/scripts/appsec-sdk.sh evidence.append <release-tag> threat-model
printf '%s' "$ATTACK_SURFACE_JSON" | bash ~/.claude/scripts/appsec-sdk.sh evidence.append <release-tag> threat-model
```

> `evidence.append <tag> threat-model` 写到 `.appsec/evidence/<tag>/threat-model/<timestamp>-<rand>.yaml`（SDK 落地为同一 layer 下的时间戳文件；`.yaml` 容器内承载 JSON 内容亦可被 evidence-validator 读取）。**直接 Write `.appsec/**` 被 PreToolUse hook 拒**——必须走 SDK。Allowed-tools 注：本 skill frontmatter `forbidden-tools: Bash`；落盘由 orchestrator（已激活 Bash 的上游）或后续 dispatch 步骤执行，本 skill 只负责**生成 JSON 内容**并交给 orchestrator 落盘。

### 8.5.1 `threat-model.json` — 机读 STRIDE register

正式 schema：[`templates/threat-model.schema.json`](../appsec-security-orchestrator/templates/threat-model.schema.json)（JSON Schema draft-07）。

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-06-14T00:00:00Z",
  "system": "<system / feature name>",
  "threats": [
    {
      "id": "T-001",
      "title": "Horizontal IDOR on /api/orders/:id",
      "stride_category": "E",
      "component": "ASSET-001 orders-api",
      "attacker": "authenticated user",
      "mitigation": "Add server-side ownership check per resource (WHERE user_id = current_user)",
      "disposition": "mitigate",
      "asvs_refs": ["v5.0.0-8.1.1"],
      "status": "open",
      "risk": { "likelihood": "high", "impact": "high" }
    }
  ]
}
```

字段约束（schema 强制）：`stride_category ∈ {S,T,R,I,D,E}`；`disposition ∈ {mitigate,accept,transfer,avoid}`；`status ∈ {open,mitigated,accepted}`；`asvs_refs[]` **仅** `^v5\.0\.0-\d+\.\d+\.\d+$`（ASVS 5.0 版本化，禁 4.x `V8.1.1` 旧标）；空 `[]` 允许（无诚实映射时，不编造）；`risk.likelihood ∈ {high,medium,low,theoretical}`，`risk.impact ∈ {high,medium,low}`。`id` 与 markdown §3 register 行 id 对齐（`T-NNN`）。`component` 尽量引用 `components.json` 的 id 或 asset-inventory `ASSET-id`。

### 8.5.2 `components.json` — 喂 Security Architecture Diagram

```json
{
  "components": [
    { "id": "C-001", "name": "orders-api", "type": "service", "trust_zone": "semi-trusted" },
    { "id": "C-002", "name": "primary-postgres", "type": "datastore", "trust_zone": "trusted" },
    { "id": "C-003", "name": "browser-spa", "type": "frontend", "trust_zone": "untrusted" }
  ]
}
```

`type` 沿用 asset-inventory enum（`service|api|datastore|frontend|agent-tool|third-party|cloud-resource`）；`trust_zone` 与 markdown §1 Components 表的 Trust Level 一致（`untrusted|semi-trusted|trusted`）。能对得上时 `id`/`name` 直接复用 asset-inventory，避免双份真相。

### 8.5.3 `dfd.json` — 喂 DFD / Trust-Boundary 图（取代 ASCII-only DFD 的机读版）

```json
{
  "nodes": [
    { "id": "C-003", "name": "browser-spa", "kind": "external-entity" },
    { "id": "C-001", "name": "orders-api", "kind": "process" },
    { "id": "C-002", "name": "primary-postgres", "kind": "datastore" }
  ],
  "flows": [
    { "from": "C-003", "to": "C-001", "data": "order request (JSON over HTTPS)", "crosses_trust_boundary": true },
    { "from": "C-001", "to": "C-002", "data": "parameterized SQL", "crosses_trust_boundary": true }
  ],
  "trust_boundaries": [
    { "id": "B1", "name": "Internet → app edge", "between": ["C-003", "C-001"], "controls": ["TLS", "WAF", "rate-limit"] },
    { "id": "B2", "name": "app → data", "between": ["C-001", "C-002"], "controls": ["least-priv DB user", "connection encryption"] }
  ]
}
```

`nodes[].id` 复用 `components.json` id；`flows[].crosses_trust_boundary` 为 true 的边正是 STRIDE 分析的重点（应在 `threat-model.json` 有对应 threat）。这份是 markdown §2 ASCII DFD 的机读等价物——markdown 仍保留供人读。

### 8.5.4 `attack-surface.json` — 机读 attack surface inventory（markdown §5 等价）

```json
{
  "entry_points": [
    {
      "id": "EP-001",
      "path": "GET /api/orders/:id",
      "auth": "required",
      "authz": "object-level ownership (BOLA-critical)",
      "rate_limit": "60/min",
      "input_schema": "path param :id (uuid)",
      "exposure": "public"
    },
    {
      "id": "EP-002",
      "path": "POST /api/uploads",
      "auth": "required",
      "authz": "RBAC: customer",
      "rate_limit": "5/min",
      "input_schema": "multipart; size + MIME whitelist",
      "exposure": "public"
    }
  ]
}
```

`exposure ∈ {public|internal|private}`（与 asset-inventory `exposure` 一致）；`authz` 字段描述 object-level / function-level 检查现状，与 `authz-matrix` artifact 互为印证（BOLA/BFLA）。每个 `entry_point` 应能在 `threat-model.json` 找到至少一条相关 threat。

### 8.5.5 一致性铁律

- markdown 与 4 个 JSON 是**同一份分析的两种渲染**——内容不一致 = bug。先写 markdown 把分析做扎实，再机械导出 JSON，避免两边漂移。
- `id` 跨工件复用（`C-*` ↔ components/dfd nodes；`ASSET-*` ↔ asset-inventory；`T-*` ↔ markdown register）。**绝不**为同一实体在不同工件造两个 id。
- JSON 不准引入 markdown 里没有的"新威胁"——JSON 是导出层，不是分析层。

---

## 9. 与下游 skill 的接口

- → `security-remediation`：每个 OPEN gap 如果已有 PoC → 转 finding 格式（appsec-security-orchestrator §9 schema）
- → `pentest-scope-and-roe`：如果 threat model 揭示需要 active validation → 路由
- → `compliance.audit`：每次 threat model 产物作为合规证据归档

---

## 10. Anti-patterns

- ❌ 拿 OWASP Top 10 当 threat model——Top 10 是常见 vulnerability list，不是 threat model methodology
- ❌ 把"过了 SAST / DAST"当成 threat model 已完成——它们是验证，不是建模
- ❌ 只画 DFD 不做 STRIDE——DFD 是输入，STRIDE 是分析
- ❌ STRIDE 表里"E"全填"已通过 RBAC"——RBAC 不防 IDOR，资源级 ownership check 才防
- ❌ Cryptography 决策记录里只写"用 TLS"——必须写 TLS 1.x+ 版本、HSTS preload 状态、cert 验证级别
- ❌ Gap inventory 列出但不映射到 risk register——脱钩等于不存在
- ❌ **只跑 STRIDE 不跑 R&C lens**——cron retry storm / 并发烧钱 / 平台容量上限是工业级 outage 的常见根因，attacker 视角看不到（§6.5 强制覆盖）
- ❌ 把 R&C 失效"挤"进 STRIDE D 类——逼模型选错 category 导致 control 错配（如 cron 并发不是"防 DoS"是"加 advisory lock"）

---

## 11. References

- [templates/threat-model-STRIDE.md](../appsec-security-orchestrator/templates/threat-model-STRIDE.md) — markdown 模板（human-readable）
- [templates/threat-model.schema.json](../appsec-security-orchestrator/templates/threat-model.schema.json) — `threat-model.json` 正式 JSON Schema（draft-07，§8.5.1）
- [templates/risk-register.md](../appsec-security-orchestrator/templates/risk-register.md) — 下游 register
- [NIST SP 800-154 Threat Modeling](https://csrc.nist.gov/pubs/sp/800/154/ipd)
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [OWASP Multi-Tenant Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)
- [OWASP WebSocket Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP Agentic AI Threats](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md) — 路由总入口
