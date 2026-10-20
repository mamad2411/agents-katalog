---
name: enterprise-qa-testing
version: 3.3.0
status: stable
created_date: 2026-05-23
updated_date: 2026-06-16
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Skill, Agent, AskUserQuestion, Task
mode: execution  # execution | plan-only | design-only — 详见 §1.5
parent: null  # 本 skill 自身是 5 大主线 orchestrator 之一
children:
  - qa-static-baseline
  - qa-test-design-tdd-bridge
  - qa-component-behavior
  - qa-integration-service-virtualization
  - qa-contract-api
  - qa-e2e-coverage-gate
  - qa-visual-regression
  - qa-a11y-compliance
  - qa-performance-reliability
  - qa-load-stress-reliability
  - qa-mutation-effectiveness
  - qa-mobile-native-e2e
  - qa-resilience-fault-injection
  - qa-test-data-environment
  - qa-flaky-governance
  - qa-smoke-release-safety
  - qa-evidence-bundle
description: >-
  Commercial-grade QA orchestrator — picks test layers from a risk model, dispatches QA-owned sub-skills, references existing execution agents (tdd-guide / e2e-runner), and aggregates auditable release evidence. Not a test generator and never re-implements the E2E/TDD agents. Use whenever tests or release confidence are the ask: we're about to release or ship, set up or add end-to-end tests for a flow, add a CI quality gate, decide what to test and at which layer, or produce release-readiness evidence. Covers layered automation (static / unit / component / integration / contract / E2E / visual / a11y / perf / smoke / evidence) and AppSec routing. Triggers: "about to release / set up end-to-end tests / add E2E tests for the login flow / CI quality gate / what should we test / 测试策略 / QA / SDET / E2E / 集成测试 / visual regression / release readiness / CI 质量门禁 / 验收测试 / 工业级测试". Entry point for /qa-quick-check, /qa-focused-gate, /qa-release-readiness, /qa-commercial-cert.
execution_modes:
  - prompt-only:  default; §6 9-step inline dispatch + qa-sdk evidence persist
  - workflow-spec: opt-in via .qa/config.json.execution_mode = "workflow-spec" OR
                   explicit slash (/qa-quick-check, /qa-focused-gate,
                   /qa-release-readiness, /qa-commercial-cert);
                   §18.5 14-step launch contract;
                   ~/.claude/workflows/qa-orchestrator.js + qa-preview-gate.js;
                   F verdict (B.1.g) with deferred live coverage (2/9 customs runtime-tested,
                   6/9 wiring-audited cold-start, qa-contract-runner reserved unwired)
---

# enterprise-qa-testing

> **Changelog** → [`references/CHANGELOG.md`](references/CHANGELOG.md)。当前：**v3.3** (默认模式真反算落地：§6 Step 1.7 Architecture Intake + Step 6.5 recompute-context + 9 deterministic parsers + COMMAND_EVIDENCE.v2 全 11 层 + 3 fail-closed gates[required-layer/runtime-mismatch/no-silent-fallback] + 入口 ask L1-L4/tasklist 软 gate) · **v3.2** (workflow-spec dual-mode, §18 + §18.5 launch contract) · **v3.1** (GSD 化：真 dispatch + evidence 验收 + 阻断假通过) · **v3.0** (调度中枢 + 13 QA-owned child skills 网络)。

---

<!-- COMPACTION-SAFE-INDEX: enterprise-qa-testing v2026-05-29 -->
## ⚑ Compaction-safe critical-contract index

> auto-compaction 后每个 skill 只保留**前 5000 tokens**、老 skill 可能被整段丢弃（Claude Code skills docs）。本 index 刻意放在 body 最前，确保以下 binding 契约即便压缩后也留在上下文。**做 workflow-spec / governed-gate 前必读这些锚点**；若 index 之后的章节正文已不在上下文，**重新 invoke 本 skill** 恢复全文再继续。
>
> - **§2 Hard Rules** — 不可违反；commercial-cert 强制 budget approval。
> - **§16 Output Contract（`schema_registry`）** — 每个 schema 的 every-run 输出契约。
> - **§17 Enforcement Registration** — agent/hook NAME 表（binding，preflight 引用）。
> - **§18.5 Launch Contract（14-step）** — workflow-spec first action 必须设 `gate_active`；commercial-cert sentinel 必含 `approved_estimate_high` + approval-text。
> - **Governed-gate 铁律（CLAUDE.md §3.7）** — `/qa-*` release / commercial-cert verdict 只能由 deterministic `qa-orchestrator.js` + `spec_hash` 人审 + evidence bundle 产出；Dynamic Workflow 只能当侦察兵。

---

## 目录（Table of Contents）

> 1400+ 行 governance 契约，按 §-编号导航。§6 9-Step Workflow + §18 Workflow-Spec 是执行核心；§2 Hard Rules、§16 Output Contract（schema_registry）、§18.5 Launch Contract 是 keep-guard 保护面。

- §1 Mission · §1.5 Invocation Mode · §1.6 Enforcement Contract（1.6.1 `.qa/` Dir · 1.6.2 Agent Binding · 1.6.3 Hook Binding · 1.6.4 qa-sdk · 1.6.5 Dispatch Failure Policy）
- §2 Hard Rules · §3 Risk Model（3.1 公式 / 3.4 Modifier + 3.4.1 Rubric / 3.5 Level→层映射 / 3.6 Floor Rules）
- §4 9-Layer QA Matrix · §5 Decision Tree
- **§6 9-Step Orchestration Workflow**（1 Discover → 2 Risk Score → 3 Select Layers → 4 Test Data/Env → 5 Dispatch Child Skills → 6 Dispatch Reference Agents → 7 Validate Evidence → 8 Flaky Triage → 9 Release Decision）
- §7 CI 集成模式 · §8 Test Data & Environment · §9 Flaky Governance · §10 Evidence-Gated Skip Rules · §11 Release Readiness Evidence
- §12 AppSec Routing（必读）· §13 Dispatch & Reference Contract（13.1 语义 / 13.1.1 Bridge 3-stage / 13.2 Preflight / 13.3 Targets / 13.4 Missing / 13.5 GSD 接口）
- §14 Anti-Patterns · §15 Standards Mapping · §16 Output Contract（含 Dispatch/Validation Schema）
- §17 Enforcement Registration（17.1 Agent / 17.2 Hook Scripts / 17.3 Hook 注册 / 17.4 qa-sdk / 17.5 GSD 接口）
- **§18 Workflow-Spec Execution Mode**（18.1 边界 / 18.2 6 Presets / 18.3 Evidence 路径 / 18.4 Dual-Mode / **18.5 Launch Contract**）· §19 参考资源

---

## 1. Mission

- 为商业级 web/server 项目提供工业级 QA/SDET 编排
- 不只是"生成测试"，而是"建立可发布的证据"
- 与 GSD 协同：GSD 决定 acceptance criteria，本 skill 决定如何证明达成
- 输出必须可操作：命令 + 实际 stdout，不接受"逻辑上应该能跑"
- **本 skill 是 orchestrator**，不是测试生成器。能不能发布是结论，不是感觉

---

## 1.5 Invocation Mode（必读 — 决定 Hard Rules 如何适用）

调用本 skill **必须显式声明 mode**。不同 mode 下 §2 Hard Rules §2.1 与 §16 Output Contract 的"完成"判定不同。

| Mode | 用途 | Step 5/6 dispatch evidence 要求（Step 7 验收） | Release Readiness 输出 |
|---|---|---|---|
| `execution` | 真实 CI 或本地完整执行 | dispatch 必产**实际** stdout / artifact evidence（Step 7 验收 schema_conformance=pass） | pass / fail / block |
| `plan-only` | 已有项目但 CI 未跑（PR 准备阶段、本地策略评估） | bridge stage (c) 可标 `BLOCKED — plan-only, see §1.5` + 预计命令 | conditional-pass plan / blocked-pending-evidence |
| `design-only` | 设计阶段、无运行环境、纯方案评估 | 整个 dispatch 标 `BLOCKED — design-only` | strategy / not yet releasable / preconditions list |

**规则**：

- 默认 mode 是 `execution`。frontmatter `mode:` 可改默认；调用方也可在 prompt 里覆盖
- `plan-only` / `design-only` 模式下，Step 6/7 标 `BLOCKED — <mode>` 不算违反 Hard Rule §2.1
- **不许**在 plan-only / design-only 模式下输出 "pass" 结论——只能是 "conditional-pass plan" 或 "preconditions list"
- 任何 mode 都**不许**伪装：design-only 不许声称 evidence 已具备；execution 不许把推理当 stdout
- mode 一旦声明，整个任务期间不允许中途切换；如需切换必须重新走 §6 Step 1

---

## 1.6 Enforcement Contract（v3.1 新增 — GSD 化的硬约束）

本 skill 不再"输出建议给调用方"，而是**自己执行 dispatch + 自己验收 evidence + 自己产 release_decision**。这要求项目侧具备以下 5 项契约（详见 §17）：

### 1.6.1 `.qa/` Directory Contract（项目级）

项目必须有 `.qa/config.json` 才算"启用 QA enforcement"。本 skill 的所有 hook 都先检查这个文件——不存在则 silent exit，**绝不打扰非 QA 项目**。

```
project-root/
├── .qa/
│   ├── config.json                       # qa_enforcement, default_mode, release_tag_pattern
│   ├── evidence/
│   │   └── <release-tag>/
│   │       ├── 00-discovery.yaml         # Step 1 输出
│   │       ├── 01-risk.yaml              # Step 2 输出（qa-risk-classifier agent）
│   │       ├── 02-layer-selection.yaml   # Step 3 输出
│   │       ├── static.yaml | unit.yaml | component.yaml | ...  # 各 child skill 落证据
│   │       ├── flaky.yaml                # qa-flaky-triager agent 输出
│   │       ├── evidence_validation.yaml  # qa-evidence-validator agent 输出
│   │       ├── qa_evidence_bundle.yaml   # qa-evidence-bundle 聚合输出
│   │       └── dispatch-failures.log     # dispatch 异常记录
│   ├── findings/
│   │   └── <id>.yaml                     # hook 落的 finding（internal-mock 等）
│   ├── quarantine.yaml                   # flaky test quarantine 总清单
│   ├── snapshot-update-approval.json     # snapshot baseline 更新审批
│   └── risk-acceptance.yaml              # CONDITIONAL_PASS 时的接受签字
```

**`.qa/config.json` schema**:

```json
{
  "version": "1.0",
  "qa_enforcement": "strict",
  "default_mode": "execution",
  "release_tag_pattern": "v\\d+\\.\\d+\\.\\d+|pr-\\d+|manual-[0-9]{8}",
  "ci_artifact_root": "ci-artifacts/",
  "appsec_handoff_required": true,
  "floor_rule_overrides": [],
  "stop_gate": {
    "block_on_missing_bundle": true,
    "block_on_failed_decision": true,
    "allow_conditional_pass": true
  }
}
```

`qa_enforcement` 取值：
- `strict` — 缺 evidence / 失败 decision 时 Stop hook 必须 block
- `warn` — 仅打印警告不 block
- `off` — 全部 hook silent（用于回退）

### 1.6.2 Agent Binding（3 orchestration agents 必须 present）

本 skill 强依赖以下 3 个 orchestration agents（risk / evidence / flaky 决策层；另有 10 个 dedicated runners + 2 个 Architecture-Intake agents（`qa-runtime-detector` / `qa-path-graph-miner`，§6 Step 1.7）见 §17.1，合计 15 个）：

| Agent | Model | Dispatch 时机 | 失败处理 |
|---|---|---|---|
| `qa-risk-classifier` | opus | §6 Step 2（risk score + Floor Rule） | BLOCKED — 不允许凭感觉打分 |
| `qa-evidence-validator` | sonnet | §6 Step 7（验收 child skill / agent 输出） | BLOCKED — 不允许 parent 自己 grep YAML 跳过 hard rule |
| `qa-flaky-triager` | sonnet | §6 Step 8（仅 retry-pass / CI-only-fail 时） | NOT_APPLICABLE if no flaky |

Preflight：§6 Step 1 必须 `Glob ~/.claude/agents/qa-*.md` 确认 3 个 agent 都 present；缺失则整体 BLOCKED（不允许降级跑）。

### 1.6.3 Hook Binding（5 个 hooks 项目级注册）

本 skill 强依赖以下 hooks（脚本在 `~/.claude/hooks/qa-*.js`，项目级 `.claude/settings.json` 注册）：

| Hook | 事件 | matcher | 行为 |
|---|---|---|---|
| `qa-block-update-snapshots.js` | PreToolUse | Bash | hard block `--update-snapshots` 无审批 |
| `qa-floor-rule-prompt.js` | PostToolUse | Edit\|Write | 命中高风险路径时 advisory context |
| `qa-detect-internal-mock.js` | PostToolUse | Edit\|Write | 检测 mock 内部模块，落 `.qa/findings/` |
| `qa-quarantine-accountability.js` | PreToolUse | Bash (git commit) | quarantine 缺 8 字段 hard block |
| `qa-evidence-required.js` | Stop | * | strict 模式下缺 bundle / 失败 decision hard block |

所有 hook **必须** gate by `.qa/config.json` 存在性，否则 silent exit 0。注册位置见 §17.3。

### 1.6.4 qa-sdk Helper Contract

`~/.claude/scripts/qa-sdk.sh` 是 evidence 落盘和 gate 检查的统一入口。本 skill §6 各 Step **必须**通过 qa-sdk 落盘，不能自己 `echo > file`。命令契约见 §17.4。

### 1.6.5 Dispatch Failure Policy（绝不伪装 PASS）

任何 dispatch 失败都不允许伪装为通过：

| 失败类型 | release_decision 影响 |
|---|---|
| child skill 不存在 | BLOCKED |
| child skill 返回非 YAML 或缺关键字段 | retry 1 次仍失败则 BLOCKED |
| agent 返回 stdout 但 evidence-validator 检出 hard rule violation | 该 layer FAIL |
| evidence 文件缺失（command_evidence: none in execution mode） | BLOCKED |
| `.qa/evidence/<tag>/dispatch-failures.log` 非空 | Step 9 必须读取，不能 PASS |
| Stop hook 触发 block 后又被 force stop | 视为人工干预，必须有 risk-acceptance.yaml |

---

## 2. Hard Rules（违反即 BLOCKED，不是 DONE）

下列任一规则违反，任务**必须**判定为阻塞，不允许声称完成。

1. **No test pass claim without evidence**
   You must provide exact command, exit code, and stdout/stderr or artifact path.
   声称"测试通过"必须附实际 terminal 输出或 artifact 路径，无 stdout 不算 pass。
   **Mode 例外**：`plan-only` / `design-only` 模式下，对应 step 可标 `BLOCKED — <mode>, see §1.5`，但**最高只能输出 "conditional-pass plan"**，不许输出 "pass"。

2. **No silent snapshot baseline update**
   Never run `--update-snapshots`, approve changed baselines, or overwrite visual references unless explicitly requested or approved.
   Playwright 官方语义：`--update-snapshots` 会覆盖 reference screenshots，必须用户明确授权。
   **首次 baseline 生成**：green-field 仓库首次跑 Visual 层时，必须在 CI Docker 中以 **explicit one-time approval** 生成（建议 ADR 记录：`approved by <owner> on <date>, CI image <hash>, scope <route list>`），之后每次更新都需要 fresh approval。本地 dev 机不允许生成正式 baseline（像素漂移）。

3. **No skip without objective evidence**
   Every skipped layer must cite measurable evidence: project age, route type, package absence, CI duration, changed files, risk score, or existing coverage.
   "我觉得不用测"不是理由，必须有可证伪的证据。

4. **No broad internal mocking to fake confidence**
   Mock network, time, storage, and third-party services when appropriate.
   Do not mock the internal module whose behavior is under test merely to make the test pass.
   测自己的模块就不能 mock 自己。

5. **No quarantine without accountability**
   A flaky test may be quarantined only with: issue ID, owner, suspected cause, expiry date, and scheduled re-run path.
   隔离 flaky test 必须挂账：谁、为什么、什么时候必须重启。

6. **No destructive production testing**
   Never mutate production data, send real customer emails, charge payment methods, alter real permissions, or expose PII.
   生产只允许只读 smoke，禁止任何 mutate / 真实通信 / 真实扣款 / 权限变更。

7. **No threshold weakening without approval**
   Do not lower coverage thresholds, Lighthouse budgets, visual thresholds, timeout values, or accessibility assertions to pass CI unless explicitly approved.
   修根因，不是降标准（与全局规则第 9 条 "检查是对的就不要放宽" 对齐）。

8. **No AppSec bypass**
   If auth, API, secrets, permissions, payments, uploads, data export, or cross-tenant access is touched, trigger AppSec handoff or explicitly mark it as unavailable.
   触及安全敏感面必须 handoff appsec-security-orchestrator，跳过必须显式声明。

9. **No test execution on the main thread — dispatch to subagents (承重柱 2)**
   The main orchestrator thread is DISPATCH-ONLY: it asks → tracks → dispatches subagents → reads evidence → lets the script aggregate. It must NOT run test-runner commands itself (vitest / jest / playwright / k6 / pytest / go test / npm test / …).
   主线程只编排、不亲自跑测试；每个测试层必须派 `qa-*` runner subagent 执行（独立 context + 产出 hashed evidence）。
   **Enforced** by `qa-main-thread-test-guard.js` (PreToolUse[Bash]): a test command with NO `agent_id` (main thread) is BLOCKED (exit 2); a subagent run (`agent_id` present, harness-set) is allowed. Use the Agent tool with named subagents — NOT `fork`/`--agent` (the allow-path needs `agent_id`).

10. **No self-declared verdict — evidence recompute is authoritative (承重柱 1)**
    The release verdict is NEVER whatever the model wrote into `release_decision`. In BOTH workflow-spec mode and DEFAULT (prompt-only) mode, the decision is RE-DERIVED from per-layer evidence by deterministic code (canonical `orchestrator-runtime/shared/qa-aggregate-decision.js`), and the per-command numbers are re-hashed + re-parsed from raw stdout.
    verdict 由证据反算，不是模型自填；数字由 raw stdout 重 hash + 重 parse 核对，改 YAML 数字当场抓。
    **Enforced** by `qa-recompute-gate.js` (invoked by `qa-sdk gate.check`): if the declared `release_decision` is MORE LENIENT than the evidence-computed decision, or any `command_evidence` hash / parse integrity check fails → BLOCKED. Machine evidence is produced by `qa-sdk evidence.run` (the SDK derives every metric; the model never types one).

---

## 3. Risk Model（risk-based 从口号变可计算输入）

每个 QA 任务**必须**在选择测试层前给出 risk score。Risk 不是形容词，是数字。

### 3.1 评分公式

```
Risk Score = Impact × Likelihood + Exposure Modifier
```

### 3.2 Impact（影响）

| 分 | 描述 |
|---|---|
| 1 | cosmetic / non-user-visible |
| 2 | minor UX or low-value internal flow |
| 3 | normal user-facing feature |
| 4 | revenue, permissions, data integrity, critical workflow |
| 5 | auth, payment, privacy, safety, destructive action, regulatory, cross-tenant data |

### 3.3 Likelihood（出错概率）

| 分 | 描述 |
|---|---|
| 1 | isolated, low churn, simple change, well-covered area |
| 2 | small change, familiar code path |
| 3 | moderate change or new dependency |
| 4 | high churn, complex state, async/concurrency, multiple integrations |
| 5 | new architecture, migration, auth/permission rewrite, historical defect area |

### 3.4 Exposure Modifier（暴露面加权，可叠加，但有上限）

| 修饰 | 加分 |
|---|---|
| public unauthenticated surface | +3 |
| production data write path | +3 |
| multi-tenant / role-based access | +3 |
| third-party integration | +3 |
| payment / auth / PII / secrets | +5 |
| release-blocking customer journey | +5 |

**Modifier Cap**：所有 modifier 累加 **≤ +10**，超出按 +10 计。
理由：modifier 不能完全 dominate `Impact × Likelihood` 的乘法部分，否则 Likelihood 退化为装饰；cap 后 Impact/Likelihood 仍是主信号，modifier 是放大器。

### 3.4.1 Modifier Attribution Rubric（边界案例 tie-breaker）

Modifier 归类有歧义时（例如：`canPurchase` 这种"门票谓词"算 multi-tenant +3 还是 payment +5？），按改动**直接做什么**分类：

| 改动性质 | 计入 modifier | 典型例 |
|---|---|---|
| **Predicate-only**：仅做判断 / 授权 gate，不实际 transact 也不 persist | 按"被 gate 的资源"档**减半**取较低档：payment-gated → +3；prod-write-gated → +2；read-gated → +0 | `canPurchase`, `isAdmin`, `hasAccess`, `canDelete` 谓词 |
| **Transaction-only**：实际调第三方 transact API | 完整 +5（payment/auth/PII 对应一项）+ +3 third-party integration | Stripe `paymentIntents.create`，Twilio `messages.create`，邮件发送 |
| **Persistence-only**：写 DB / 写 log / 写 cache，不离开 trust boundary | 完整 +3 production data write path | Prisma `create`/`update`，Redis `set`，写入审计 log |
| **Composite**：同一改动同时 gate + transact + persist | 各自相加，§3.4 Cap +10 兜底 | Stripe 调用 + paymentLog 写库 → +5 + +3 + +3 = +11 → cap → +10 |
| **Read-only**：仅查询不写 | 不加 modifier；例外：public unauthenticated surface 仍 +3 | dashboard 查询、列表渲染 |

**Tie-breaker 原则**：

- 选不准时往**较严**判（取较高 modifier）
- 但 Floor Rule §3.6 优先于 modifier 精打细算 —— attribution 模糊不会让 catastrophic-but-stable 路径降级
- Cap +10 始终适用

**Scenario B 反例验证**：单行 `canPurchase` 修改 = Predicate-only protecting payment → +3（不是 +5）。Pre-floor = 5×1 + 3 + 3 (multi-tenant) = 11 → Medium。Floor §3.6 触发 → 强制 **High**。Attribution 让 modifier 计算干净，但 Floor 仍保证安全网。

### 3.5 Risk Level → 层选择映射

| Score | Level | 必选层 |
|---|---|---|
| 1-5 | Low | Static 必须；Unit 仅在逻辑变更时；Smoke 仅在 deploy path 变化时 |
| 6-11 | Medium | Static + (Unit or Component) + Integration if API/DB/external boundary changed |
| 12-19 | High | Static + Unit/Component + Integration + E2E (≥1 关键 user journey) + a11y/perf/visual (按变更面适配) |
| 20+ | Critical | High 全集 + Negative-path + Role/Permission Matrix + Test Data Isolation + CI Evidence Bundle + AppSec handoff |

### 3.6 Floor Rules（catastrophic-but-stable 路径保护）

某些路径即使 Likelihood 很低、score 也很低，**不允许**降级。Floor Rules 在 Score 计算后**强制**抬升 Level：

| 触发条件 | 强制 Floor |
|---|---|
| Impact ≥ 5（auth / payment / privacy / safety / destructive / regulatory / cross-tenant data） | Level ≥ **High** |
| Impact ≥ 5 **AND** 任一 +5 modifier（payment/auth/PII/secrets 或 release-blocking journey） | Level ≥ **Critical** |
| 任何 production data write path 变更 | Level ≥ **Medium** |
| 任何 public unauthenticated surface 变更 | Level ≥ **Medium** |

**典型反例**：修改 `getTenantPermissions` 一行 return（Impact=5, Likelihood=1, modifier=+3 multi-tenant）→ 原始 score = 5×1+3 = 8 → Medium。Floor Rule 强制抬到 **High**，必须 E2E + AppSec handoff。

**规则**：risk score 没算出来就不许选层；Floor rule 应用情况必须在 §16 Step 2 输出中显式列出（即使未触发也要写 "no floor applied"）；Floor 触发但未应用，视为 Hard Rule §2.3 违反。

### 3.7 ISO/IEC 25010:2023 Product Quality Matrix（characteristic → layer 映射）

> ADDITIVE（v3.2 文档增强，不改任何 gate / schema / decision 逻辑）。Risk Model（§3.1-§3.6）回答"这次改动有多危险、必选哪些层"；本矩阵回答"**这次改动该证明哪些 quality characteristic**"——两者正交：Risk 给数字驱动选层，25010 给"质量维度别漏"的 checklist。
>
> ISO/IEC 25010:2023（2023 修订，取代 2011 版）把 product quality 拆成 **9 大 characteristic**。相对 2011 版，2023 版新增 **Safety** 为顶层独立特性，并把 Interaction Capability（原 Usability）、Flexibility（原 Portability 的 adaptability 部分上提）重命名/重组。下表把 9 特性映射到 §4 的测试层 / child skill / handoff，方便审计时"按质量维度反查覆盖"。

| # | 25010:2023 Characteristic | 子特性（节选） | 主要落在哪层 / 哪个 child skill | 备注 |
|---|---|---|---|---|
| 1 | **Functional Suitability** | completeness / correctness / appropriateness | Unit/TDD（`qa-test-design-tdd-bridge`）+ Integration + E2E + Contract | acceptance criteria 对照的主战场 |
| 2 | **Performance Efficiency** | time-behaviour / resource-utilization / capacity | Performance（`qa-performance-reliability`）+ §11 route-class budgets | capacity ceiling 也属 reliability/cost lens（threat-model 侧 `security-governance-threat-modeling` §6.5 的 benign failure modes 之一） |
| 3 | **Compatibility** | co-existence / interoperability | Contract（`qa-contract-api`）+ Integration | 跨服务 / 跨团队 / event payload 兼容 |
| 4 | **Interaction Capability**（原 Usability，2023 改名） | appropriateness-recognizability / learnability / operability / **accessibility** / user-error-protection | a11y（`qa-a11y-compliance`，WCAG 2.2）+ E2E（关键流可操作性） | accessibility 是其子特性 → a11y 层是 25010 的硬覆盖点，不是可选 |
| 5 | **Reliability** | maturity / availability / fault-tolerance / recoverability | Integration + E2E + benign failure-mode lens（retry storm / cascade / capacity，归 `security-governance-threat-modeling` §6.5） | recoverability 涉发布回滚 → 与 AppSec Recover（CSF 2.0）相邻，运行时可靠性边界见 standards-mapping.md §15.2 SLO-SLI 段 |
| 6 | **Security** | confidentiality / integrity / authenticity / non-repudiation / accountability | **handoff → `appsec-security-orchestrator`**（§12 强制） | QA 不自实施 security 验证；触及即 handoff |
| 7 | **Maintainability** | modularity / reusability / analysability / modifiability / testability | Static（`qa-static-baseline`）+ test quality review（`code-reviewer`） | testability 差会反噬所有层，是 §2 Hard Rule 4 的上游 |
| 8 | **Flexibility**（2023 重组：含原 Portability adaptability/installability + scalability） | adaptability / scalability / installability / replaceability | Integration（env/容器）+ `env-parity-baseline`（cross-env handoff）+ Performance（scalability） | 部署一致性走 `env-parity-baseline`，本 skill 只标识 |
| 9 | **Safety**（2023 **新增**顶层特性） | operational-constraint / risk-identification / fail-safe / hazard-warning / safe-integration | Floor Rule §3.6（destructive/safety Impact≥5）+ E2E negative-path + AppSec handoff | 与 §3 Impact=5 的 "safety / destructive action" 同源；安全攸关路径不允许降级 |

**使用方式**（不改流程，只加 checklist 视角）：

- §6 Step 3 选层后，**可选**对照本矩阵自查"9 特性里哪些与本次改动相关、是否都有对应层覆盖或显式 skip"。这是 advisory 自查，**不新增 gate**——最终选层仍由 §3 Risk Model 验算 + §10 Evidence-Gated Skip 决定。
- Characteristic 与层是**多对多**：一个改动可能触及多个特性（如支付改动 = Functional + Security + Safety + Reliability），一层也可能覆盖多个特性（E2E 同时给 Functional + Interaction + Reliability 信号）。
- **Security / Safety 两特性永远不在 QA 内闭环**：Security → §12 handoff `appsec-security-orchestrator`；Safety 的 destructive 路径走 Floor Rule §3.6 + AppSec。本矩阵只负责"别漏维度"，不负责"自己实施 security/safety 验证"。
- 标识符引用：用 `ISO/IEC 25010:2023`（注明年份，避免与 2011 版子特性命名混淆——2011 的 Usability / Portability 标签在 2023 已被 Interaction Capability / Flexibility 取代）。

---

## 4. 9-Layer QA Matrix（核心层定义 + Owned Skill / Reference Agent）

**v3.0 关键变化**：每层不再仅是定义，而是绑定到一个 **Owned QA Skill**（QA 主线内部实施）或 **Reference Agent**（已有通用 agent，不重新实现，只通过 bridge skill 引用）。

| # | 层 | 工具推荐 | Owned Skill / Reference Agent | 启用条件 | 跳过条件 |
|---|----|---------|------------------------------|---------|---------|
| 1 | Static | tsc + ESLint + Prettier + npm audit + git-secrets | `qa-static-baseline` | 任何项目 | 无 |
| 2 | Unit / TDD | Vitest | `qa-test-design-tdd-bridge` → `tdd-guide` (agent ref) | 工具函数 / Server Actions / Zod schema / 逻辑变更 | 纯 UI 渲染层 |
| 3 | Component | Vitest + Testing Library + jsdom | `qa-component-behavior` | 同步 Client Components / 交互组件 | async Server Components |
| 4 | Integration | Vitest + MSW / Testcontainers / Docker Compose | `qa-integration-service-virtualization` | 跨模块状态 / DB / cache / queue / API handler | 纯 CRUD 路由（E2E 覆盖更高效）|
| 5 | Contract | OpenAPI / Pact / AsyncAPI / GraphQL schema | `qa-contract-api` | API boundary / SDK / 跨团队 provider / event payload | 内部模块且 integration 已覆盖 |
| 6 | E2E | Playwright | `qa-e2e-coverage-gate` → `e2e-runner` (agent ref) | Auth flow / async RSC / 关键 user journey | 纯静态 marketing 站 |
| 7 | Visual | Playwright `toHaveScreenshot()` / Storybook+Chromatic | `qa-visual-regression` | 设计系统稳定后 / 核心页像素精度 | 早期迭代 / 内容频繁变动 |
| 8 | Accessibility | @axe-core/playwright + vitest-axe + WCAG 2.2 | `qa-a11y-compliance` | 任何含 HTML 输出的 surface | — |
| 9 | Performance | Lighthouse CI + k6 + bundle budget | `qa-performance-reliability` | 关键 landing/dashboard / 性能敏感 | 内部工具且无变更（须配合 §10）|
| 10 | Load/Reliability | k6 open-model (`ramping-arrival-rate`) + breakpoint/soak | `qa-load-stress-reliability` → `qa-load-stress-runner` (agent) | backend capacity / release-blocking journey / high-throughput change | no backend perf-sensitive change |
| 11 | Mutation/Test-Effectiveness | StrykerJS / cargo-mutants / mutmut / PIT (diff-scoped) | `qa-mutation-effectiveness` → `qa-mutation-runner` (agent) | High/Critical logic-dense module | Low/Medium or no logic change |
| 12 | Mobile E2E (conditional) | Maestro YAML flows (emulator/simulator) | `qa-mobile-native-e2e` → `qa-mobile-e2e-runner` (agent) | mobile-app marker present | no marker → NOT_APPLICABLE |
| 13 | Resilience/Fault-Injection (RED-LINE, double-gate) | Toxiproxy (latency/partition/bandwidth) + Pumba (kill/pause/netem) + stress-ng | qa-resilience-fault-injection → qa-resilience-runner (agent) | High/Critical + multi-dependency/distributed/queue/external-API-heavy backend; staging only | no backend resilience surface OR no staging env |
| + | Smoke | Playwright tag `@smoke` 子集 | `qa-smoke-release-safety` | 每次 deploy / release | 本地开发 |
| ★ | Test Data | factory / fixture / role matrix / tenant matrix | `qa-test-data-environment` | Medium+ risk（详见 §3.5） | Low risk 且无 DB/auth 变更 |
| ★ | Flaky Triage | Playwright retries + repeatEach + 8 类分类 | `qa-flaky-governance` | retry-pass / CI-only fail / 非确定性 fail | 项目无 flaky 历史 |
| ★ | Evidence | release evidence aggregator | `qa-evidence-bundle` | 任何 release gate / merge gate / sign-off | — |

★ 行不属于"测试层"而是横切关注 (cross-cutting)；它们在 §6 Step 4 / 8 / 9 被 dispatch。

### 4.1 选层平衡注记 — Test Pyramid vs Testing Trophy（ADDITIVE）

> 文档增强，不改选层算法（最终选层仍由 §3 Risk Model + §5 Decision Tree + §10 Evidence-Gated Skip 决定）。这里只给"层与层之间该如何配比"的两个业界心智模型，避免两种典型失衡：① 全堆 E2E（慢、flaky、反馈晚）② 只写 unit 不碰 integration（个体绿、组合炸）。

- **Test Pyramid（Mike Cohn / Martin Fowler）**：底宽顶窄——unit 最多、integration 居中、E2E 最少。核心主张：**越往上越慢越脆越贵**，应把尽量多的验证下沉到快而稳的低层（§4 Layer 2-4），E2E（Layer 6）只留**关键 user journey**（与 §4 Layer 6 启用条件一致）。
- **Testing Trophy（Kent C. Dodds）**：对前端 / 组件密集型项目，**Integration 层（§4 Layer 4）权重最大**——因为"用户感知到的价值多在模块组合处，单测个体函数信号弱"。底座是 Static（§4 Layer 1，tsc + ESLint「免费的测试」），其上 unit → **integration（最厚）** → E2E。
- **本 skill 的取舍**：不强制单一模型。**用 §3 Risk Model 数字驱动配比**——
  - 逻辑密集 / 算法 / 纯函数变更 → 偏 Pyramid（厚 unit，§4 Layer 2）；
  - 前端组件 / RSC + Client 组合 / 多模块状态 → 偏 Trophy（厚 integration + component，§4 Layer 3-4）；
  - High/Critical + 关键 user journey → 两模型都要求"E2E 必有但不滥"（§3.5 High 档 ≥1 E2E，不是堆满）。
- **反平衡红线**（已被 §2 Hard Rules / §14 覆盖，此处只点名）：用 E2E 补 unit 的洞（慢且 flaky）、用 unit 假装 integration（mock 掉真实组合）、为追覆盖率平铺写测试无风险分配（§14 第 7 类反模式）。

---

## 5. Decision Tree（"这个功能用哪层测试"）

```
Is it an async Server Component?
  └─ YES → E2E (Vitest 无法渲染 async RSC)

Is it a Client Component nested inside an async Server Component?
  └─ YES → Component test for the client + E2E for the parent RSC boundary
     (覆盖 client 内部状态 + RSC + client 组合的完整渲染路径，不能只测一边)

Is it a pure function / utility / Zod schema?
  └─ YES → Unit

Is it a Client Component with user interaction (standalone, not nested in RSC)?
  └─ YES → Component (Testing Library)

Is it error handling across API boundary?
  └─ YES → Integration + MSW mock

Is it a complete user journey (login → action → result)?
  └─ YES → E2E

Did visual layout / theme / images change?
  └─ YES → add Visual Regression（受 §10 Evidence-Gated Skip 约束）

Is it a deploy?
  └─ YES → add Smoke (@smoke tag subset)

Does it touch backend / auth / user data / payment?
  └─ YES → MANDATORY handoff to appsec-security-orchestrator
```

Decision Tree 是层选择启发式，**最终选层必须经过 §3 Risk Model 验算**。

---

## 6. 9-Step Orchestration Workflow（v3.0 dispatch-aware）

每次 QA 任务**按此 9 步顺序执行**，每步必须输出结构化结果。前一步未输出，不进入下一步。
v3.0 关键变化：Step 5/6 不再是"自己写测试 / 自己跑 fast lane"，而是**dispatch QA-owned skills + dispatch reference agents**；Step 7 是**验收 dispatch 返回的 evidence**。

### Step 0 — Collect QA Intake（v3.4 — 入口结构化采集，四项必填）

**第一个动作**是**一次 `AskUserQuestion` 问四件事**(不是只问级别)，照 GSD"先把信息灌进 required artifact 才能往下走"的模式(GSD plan-phase 没有 `PROJECT.md`/`REQUIREMENTS.md` 就进行不下去)。**诚实边界**(CLAUDE.md §0.1)：hook 看不见 `AskUserQuestion`、看不见激活的 skill，所以平台**无法硬锁"ask 必须第一"**——改用 required-artifact + 窄 gate 兜底（见下）。

**四个必问(一次 `AskUserQuestion`，≤4 问)**：

1. **级别 (level)** — L1-L4：
   | 级别 | 用途 | 大致对应 preset |
   |---|---|---|
   | **L1** Quick self-check | dev 提交前自检：Static + risk-selected 关键层，fail-fast | quick-check |
   | **L2** PR-review gate | PR 门禁：按 risk 在 changed surfaces 上铺层 | focused-qa-gate |
   | **L3** Release readiness | 发布就绪：完整 evidence bundle | release-readiness |
   | **L4** Commercial cert | 客户可见/合规：+Visual/A11y/Perf，**强制 budget approval** | commercial-cert |
2. **范围 / change-set (scope)** — `git-diff`(默认,当前改动) / `named-target`(点名一个模块·流程) / `release`(整发布) / `whole-product`。**+ 一句话 detail**(diff base / 目标名)。补"不知道测啥"的洞。
3. **模式 (mode)** — `execution`(真跑) / `plan-only`(还没 CI) / `design-only`(纯方案)。
4. **功能判据来源 (acceptance_criteria)** — `gsd-plan`(给 PLAN.md 引用) / `user-inline`(用户内联给标准) / `none-acknowledged`(明确承认没有功能 oracle)。补"对照什么标准"的洞(§1 / §3.7 / Q3)。**非 `none-acknowledged` 时必须给 detail**(spec 引用或内联标准)。

答完立即把四项落盘：

```
bash "$HOME/.claude/scripts/qa-sdk.sh" intake.write \
  --level L<n> --scope-kind <git-diff|named-target|release|whole-product> --scope-detail "<...>" \
  --mode <execution|plan-only|design-only> --acceptance <gsd-plan|user-inline|none-acknowledged> [--acceptance-detail "<...>"] \
  --decided-by user
```

写出 `.qa/state/intake.json`。**`--decided-by user` 只有在你真的回答了上面的 AskUserQuestion 时才填**；非交互场景(subagent / CI / 无真人)只能填 `--decided-by model-default`。**Gate**：`qa-entry-ask-required.js` 拦住 `qa-sdk evidence.run/evidence.append/gate.check`，直到 intake.json **五项齐全且 `decided_by=user`** 为止——strict 下 **model-default(self-fill)会被拒**(legacy `level.select` 更不足以解锁)。窄 gate 只拦那三个命令、fail-open。**诚实天花板**：hook 能强制"完整的、标记 user 的 intake 存在"，**仍不能证明真是人填的**(模型可谎称 `user`；平台看不见 AskUserQuestion)。真正的真人输入只在**交互主循环**(AskUserQuestion 真弹给用户)成立；非交互必然 model-default → 被 strict gate 挡下,逼你拿真人 intake 再继续。

**级别是意图，risk 是真相**：L<n> 只设下限，Step 2 `qa-risk-classifier` + Floor Rules(§3.6)只能把级别**往高抬**不能往低压——auth/payment 即使选 L1 也会被 floor 抬到 High/Critical。

### Step 0.5 — Build durable to-do（v3.3 新增 — 账本兜底 /clear）

`TaskCreate` 拆 QA 步骤（实时 UI 视图）**并**写持久账本 `.qa/state/tasklist.json`（`TaskCreate` 绕过 hook、扛不住 `/clear`，账本才是被拦物 + 跨 session 续点）：

```
（先 TaskCreate 建实时清单）
echo '{"release_tag":"<tag>","level":"L<n>","tasks":[{"id":1,"title":"Step 1 Discover","status":"pending"}, ...]}' \
  | bash "$HOME/.claude/scripts/qa-sdk.sh" tasklist.write
```

`qa-tasklist-required.js` 无账本时**软提醒**（advisory，永不阻断）。

### Step 1 — Discover

Output:
- package manager（npm / pnpm / yarn / bun）
- test scripts（package.json scripts 节点）
- framework（Vitest / Jest / Playwright / Cypress / 其他）
- existing test files（文件路径列表）
- CI config（`.github/workflows/*` / `.gitlab-ci.yml` / 其他）
- affected files（本次变更涉及的源码文件）
- changed user journeys（变更影响的用户流程）
- **preflight**：Glob `~/.claude/agents/*.md` + 检查 available-skills 列表，确认 13 个 QA child skill 与 reference agent（tdd-guide / e2e-runner / code-reviewer / appsec-security-orchestrator）present
  - **+ intake（v3.3）**：Glob 确认 `qa-runtime-detector` / `qa-path-graph-miner` present；缺失则 Step 1.7 BLOCKED（不允许跳过 intake 跑 web-only 默认）

### Step 1.7 — Architecture Intake（v3.3 新增 — prompt-only 优先，先挖架构再测）

**目的**：先弄清"这项目到底是什么、改动碰到哪些关键路径"，让下游"按目标类型测、按关键路径测"，不再 web-only 猜。本阶段在 Step 1（Discover）之后、Step 2（Risk）之前跑——runtime + critical_paths 同时喂给 risk 打分。

**三件套（缺一不可；未全部落盘前，Step 5/6 测试层 agent 一律不开工）**：

1. **00-runtime.json** ← 派 `qa-runtime-detector`（opus, read-only）。marker-bound 判定每个可运行目标（web/api/mobile/desktop/cli/library/multi-service）+ start/health-probe。`decision: BLOCKED`（no_marker / confidence_conflict / type_known_no_entrypoint / only_low_confidence / host_incapable）→ 停下问用户，**绝不默认成 web app**。
   ```
   runtime = Agent(subagent_type=qa-runtime-detector, model=opus,
                   prompt={release_tag, repo_root, changed_files, host_os})
   bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> 00-runtime.json <runtime_structuredoutput>
   ```

2. **path-graph.json** ← 派 `qa-path-graph-miner`（opus, read-only）。依赖图+路由图（每边带 source_tool+confidence）→ changed→反向可达→entrypoint→正向到 sink 的 critical_paths + 每路径 required_layers。`graph_status: BLOCKED/REDUCED` → 下游 coverage 降 `UNVERIFIED`，**不号称全覆盖**。
   ```
   graph = Agent(subagent_type=qa-path-graph-miner, model=opus,
                 prompt={release_tag, repo_root, changed_files, runtime:<00-runtime summary>, risk_level})
   bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> path-graph.json <graph_structuredoutput>
   ```

3. **00-test-plan.json** ← 主线程综合（读 00-runtime.json + path-graph.json，按 `TEST_PLAN_SCHEMA.v1` 产 `required_layers[]`（每层 required + expected_artifact + run_command + target_kind）+ `critical_release_paths[]` + `runtime_targets[]`）。
   ```
   bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> 00-test-plan.json <test_plan_json>
   ```

**Intake Gate（instruction-layer）**：三件套未全落盘 → 不进 Step 5/6。**Mode 适配**：plan-only/design-only 时 intake 仍跑（纯静态分析，无需运行环境）；host_capable=false 的 target 标 `NOT_APPLICABLE` + `RUNTIME_HOST_INCAPABLE`（不双重 BLOCK，也绝不算 PASS）。

**Schema**：`RUNTIME_DETECTION_SCHEMA.v1` / `PATH_GRAPH_SCHEMA.v1` / `TEST_PLAN_SCHEMA.v1`（`~/.claude/orchestrator-runtime/qa/schemas/`）。**本版 intake 只做 prompt-only**，不接 workflow-spec 指纹/resume cache（§18.5 14-step 不变）。三件套是下游 P3 fail-closed gate（`qa-runtime-mismatch-gate` / `qa-required-layer-gate`）的事实源——intake 未跑时那些 gate additive NO-OP（与 legacy 兼容）。

### Step 2 — Risk Score

Output:
- 风险表（按 §3）
- Impact 分数 + 理由（仓库内证据）
- Likelihood 分数 + 理由（仓库内证据）
- Exposure Modifier 列表 + 加分（按 §3.4 Cap +10 后的最终值）
- Modifier Attribution（按 §3.4.1 rubric 分类，predicate-only / transaction-only / persistence-only / composite / read-only）
- Pre-Floor Score + Pre-Floor Level
- **Floor Rule 状态**（必填，即使未触发也要写 "no floor applied"）
- Final Level
- **Evidence Confidence**（v3.0 新增，独立于 risk）：
  - command_evidence: none / partial / complete
  - artifact_evidence: none / partial / complete
  - environment_confidence: low / medium / high
  - flaky_confidence: stable / suspected / confirmed_flaky

### Step 3 — Select Required Layers

Output:
- 选定层列表（每层标注 Owned Skill / Reference Agent，按 §4 表）
- 选定层 Scope（必填，按 §16 Step 3 表格）
- 跳过层列表 + §10 Evidence-Gated Skip 证据
- 每层风险依据（来自 Step 2）

### Step 4 — Build Test Data / Environment Plan（v3.1 真 dispatch）

**v3.1 关键变化**：本 skill **自己** `Skill(skill=qa-test-data-environment, args=...)` 收 evidence 落盘。不再"输出给调用方让他调"。

```
result = Skill(skill=qa-test-data-environment, args={
  risk_level: <from Step 2 final_level>,
  changed_surfaces: <from Step 1>,
  mode: <execution|plan-only|design-only>,
})
bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> test_data <result>
```

返回结果（`test_data_environment` YAML，见 `qa-test-data-environment` §6）作为本 skill Step 7 验收输入。

### Step 5 — Dispatch QA-owned Child Skills（v3.1 真 dispatch）

**v3.1 关键变化**：本步骤不再"输出 dispatch_qa_owned YAML 让调用方执行"，而是**本 skill 自己执行** `Skill(skill=<qa-child-skill>, args=...)`，收 evidence 落到 `.qa/evidence/<release-tag>/<layer>.yaml`。

执行流：

```
for layer in Step 3 selected_layers:
  child = §4 表里 layer 对应的 owned skill
  input = build_input_from_step1_step2(layer)

  try:
    result = Skill(skill=child, args=input)
    if result is not valid YAML matching expected schema:
      retry once with sharpened input
      if still failed:
        append to .qa/evidence/<tag>/dispatch-failures.log
        mark layer status=failed (continue, 不要 abort 整体流程)
    else:
      bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> <layer> <result>
      mark layer status=dispatched
  except dispatch error:
    append to dispatch-failures.log
    mark layer status=failed
```

按 §4 表 dispatch（每个 layer 选 owned skill / 经 bridge 的 reference agent）。bridge layer 走 Step 6。

落盘后输出**实际** dispatch 结果（不是建议）：

```yaml
child_skill_dispatch_results:
  - skill: qa-static-baseline
    status: dispatched  # dispatched | failed | skipped
    evidence_file: .qa/evidence/<tag>/static.yaml
    dispatched_at: <timestamp>
    retry_count: 0
  - skill: qa-component-behavior
    status: dispatched
    evidence_file: .qa/evidence/<tag>/component.yaml
    dispatched_at: <timestamp>
    retry_count: 1   # 第一次返回非 YAML，retry 后通过
  - skill: qa-visual-regression
    status: skipped
    reason: §10 evidence-gated skip — UI files 0 changed + no baseline approved
```

**关键差别**：失败不允许伪装通过。dispatch-failures.log 非空时，Step 9 必须读取并影响 release_decision。

### Step 6 — Dispatch Reference Agents via Bridge Skills（v3.1 真 dispatch）

reference agents（`tdd-guide` / `e2e-runner`）必须走 §13.1.1 的 **3-stage bridge chain**，本 skill 自己执行 stage (b) → (c) → (d)：

```
for layer in Step 3 selected_layers with reference_agent:
  bridge = §4 表 bridge skill (e.g. qa-e2e-coverage-gate)
  agent = §4 表 reference agent (e.g. e2e-runner)

  # Stage (b) — bridge skill prepare input
  prep = Skill(skill=bridge, args={mode: "prepare_input", layer_input: ...})

  # Stage (c) — agent execute
  agent_output = Agent(subagent_type=agent, prompt=prep.dispatch_input)

  # Stage (d) — bridge skill validate evidence
  validation = Skill(skill=bridge, args={mode: "validate_evidence", agent_output: ...})

  bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> <layer> <validation>

  if validation.status == FAIL or has hard_rule_violations:
    layer status = FAIL  # 不允许跳过 stage (d) 直接信 agent stdout
```

输出实际结果：

```yaml
reference_agent_dispatch_results:
  - bridge_skill: qa-e2e-coverage-gate
    reference_agent: e2e-runner
    stage_b_completed: true
    stage_c_completed: true
    stage_d_completed: true    # 必须 true，否则视为 hard rule §2.1 违反
    evidence_file: .qa/evidence/<tag>/e2e.yaml
    layer_status: PASS | FAIL | BLOCKED
```

**调用方常见错误已被本 skill 自动规避**：本 skill 现在自己跑 stage (b)(c)(d)，不会出现"跳过 stage (d) 拿 agent stdout 当 evidence"。

### Step 6.5 — Assemble recompute-context.json（v3.3 新增 — 让默认模式真反算 verdict）

承重柱 1（§2 Hard Rule #10）的**默认模式**落地：把反算门所需上下文落盘，使 Step 9 `qa-sdk gate.check` 调用的 `qa-recompute-gate.js` 能从机器证据反算 verdict、与模型自填值比对，偏松即 BLOCK。

```
recompute_context = {
  selected_layers:           <Step 3 选定层名>,
  policy:                    <floors: static_floor / a11y_floor / perf_floor / visual_floor（preset 自带 + 项目收紧项 merge，绝不放宽）>,
  risk_snapshot:             <Step 2 qa-risk-classifier 输出>,
  critical_release_paths:    <00-test-plan.json.critical_release_paths>,
  declared_release_decision: null,   # Step 9 gate.check 用 --declared 传模型自填值
}
bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> recompute-context.json <recompute_context_json>
```

**机器证据来源（关键）**：执行层（Component/Integration/Contract/E2E/Visual/A11y/Perf/Load/Mutation/Resilience）的测试**必须**由对应 `qa-*` runner subagent 经 `qa-sdk evidence.run` 跑——它落 raw stdout + SHA256 + 命名 parser → `<layer>.json`（主线程绝不亲跑测试命令，§2 Hard Rule #9 由 `qa-main-thread-test-guard.js` 硬拦）。反算门重读 `<layer>.json` 重 hash + 重 parse + 重判；无机器证据时 NO-OP（additive 回退，legacy 兼容）。

### Step 7 — Validate Evidence via qa-evidence-validator Agent（v3.1 真验收）

**v3.1 关键变化**：不再让 parent 自己 grep YAML。`.qa/evidence/<tag>/` 整目录交给 `qa-evidence-validator` agent 做 gate decision。

```
validation = Agent(
  subagent_type=qa-evidence-validator,
  prompt={
    evidence_dir: .qa/evidence/<release-tag>/,
    schema_registry: §16.schema_registry,
    hard_rules: §2,
    mode: <execution|plan-only|design-only>
  }
)

bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> evidence_validation <validation>
```

agent 输出 `evidence_validation.yaml`（structure 见 §16）：

```yaml
evidence_validation:
  by_layer:
    static: { status: PASS | FAIL | BLOCKED, missing_artifacts: [], hard_rule_violations: [] }
    unit: ...
    component: ...
    e2e: ...
  missing_artifacts: []
  skipped_layers_unjustified: []
  blocked_items: []
  overall_evidence_confidence: low | medium | high
  release_decision_input: PASS | FAIL | BLOCKED | CONDITIONAL_PASS | STRATEGY_READY
```

**Step 7 失败 = 该层未通过**，无论 child skill / agent 自报什么。

### Step 8 — Flaky / Failure Triage via qa-flaky-triager Agent + qa-flaky-governance Skill

若 Step 7 检出任何 retry-pass / CI-only fail / 非确定性 fail：

```
triage = Agent(
  subagent_type=qa-flaky-triager,
  prompt={
    candidates: [from evidence_validation.flaky_signals],
    quarantine_existing: .qa/quarantine.yaml,
    critical_release_paths: [auth, payment, checkout, ...]
  }
)

# 双重校验：再走 qa-flaky-governance child skill 做规则化最终判断
governance_result = Skill(skill=qa-flaky-governance, args={triage_input: triage.output})

bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> flaky <governance_result>
```

无 flaky candidate 时整步跳过，写入 `flaky: { status: NOT_APPLICABLE, reason: "no flaky signals from Step 7" }`。

Critical release-path test 不允许静默 quarantine — `qa-flaky-triager` 必须拒绝并标 BLOCKED。

### Step 9 — Release Readiness Decision via qa-evidence-bundle Skill

```
# 检查 dispatch-failures.log（v3.1 硬约束）
failures = Read(.qa/evidence/<tag>/dispatch-failures.log)
if failures non-empty:
  forced_decision = BLOCKED  # 不允许 PASS

# 聚合 + 出 decision
bundle = Skill(
  skill=qa-evidence-bundle,
  args={
    evidence_dir: .qa/evidence/<release-tag>/,
    mode: <execution|plan-only|design-only>,
    risk_acceptance: .qa/risk-acceptance.yaml (if present),
    forced_decision: <if any>
  }
)

bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> qa_evidence_bundle <bundle>

# 最后 gate check
bash "$HOME/.claude/scripts/qa-sdk.sh" gate.check <tag>
```

`qa-evidence-bundle` 输出 `qa_evidence_bundle` YAML，含 `release_decision: PASS | FAIL | BLOCKED | CONDITIONAL_PASS | STRATEGY_READY`。

mode 决定空间：
- `execution` mode：PASS = 可发布 / FAIL = 待修复后发布 / BLOCKED = 阻塞发布 / CONDITIONAL_PASS = 需 risk-acceptance.yaml 显式签字
- `plan-only` mode：CONDITIONAL_PASS plan + preconditions list（不允许 PASS）
- `design-only` mode：STRATEGY_READY / not yet releasable + preconditions list（不允许 PASS）

并显式列出：
- AppSec status（已推荐路由 / 不适用 / target 缺失）
- Downstream Route Recommendation（按 §13）
- Residual risk + 接受理由 + 责任人
- Stop hook 状态（缺 bundle 时 strict 模式必须 block）

Output（按 mode 决定空间）：
- `execution` mode：可发布 / 待修复后发布 / 阻塞发布
- `plan-only` mode：conditional-pass plan + preconditions list
- `design-only` mode：strategy ready / not yet releasable + preconditions list

并显式列出：
- AppSec status（已推荐路由 / 不适用 / target 缺失）
- Downstream Route Recommendation（按 §13）
- Residual risk + 接受理由 + 责任人

---

## 7. CI 集成模式  →  references/ci-integration.md
> Relocated (SAFE-A appendix — verbatim, not weakened; not needed to execute a run). Read on demand.

---
## 8. Test Data and Environment Strategy（→ `qa-test-data-environment`）

**v3.0 变化**：本节已下沉为 child skill `qa-test-data-environment`。本节仅保留摘要 + dispatch contract。详细规范、output schema、实施模板见该 child skill。

**摘要要点**：

- Medium+ risk **必须**给出：fixture / cleanup / time / auth role / tenant matrix / env target
- High/Critical risk **额外必须**：无共享 mutable account、test order independence、multi-tenant 4 项（own allow / other deny / role downgrade deny / stale session）
- Production **特殊**：仅 read-only smoke、禁邮件/SMS/扣款/客户数据修改、artifact 无 PII

**Dispatch trigger**：
- §6 Step 4 自动触发
- 任何独立 fixture / role matrix 需求（不走完整 QA review）也可单独触发

**Output contract**：见 `qa-test-data-environment` §6。本 skill Step 7 按其 schema 验收。

---

## 9. Flaky Test Governance（→ `qa-flaky-governance`）

**v3.0 变化**：本节已下沉为 child skill `qa-flaky-governance`。本节仅保留摘要 + dispatch contract。

**摘要要点**：

- **Detection**：任何 retry-pass / CI-only fail / 非确定性 fail 视为 flaky 候选
- **Playwright 语义**：`retries` 用于降噪但 pass-on-retry **不算干净通过**；`repeatEach` 用于诊断不用于 gate
- **8 类分类**：Selector instability / Async-timing race / Network 3rd-party / Test data pollution / Env contention / Browser variance / Order dependency / Product nondeterminism
- **Quarantine accountability 字段**（必填）：test_name / failure_class / owner / issue_id / expiry_date / reproduction_command / last_seen / unblock_condition
- **Critical release-path 测试不允许静默 quarantine**

**Dispatch trigger**：
- §6 Step 8 自动触发（Step 7 出现 retry-pass 或 nondeterministic fail）
- 独立 ops 触发：oncall / project maintenance / quarterly flaky review

**Output contract**：见 `qa-flaky-governance` §6。

---

## 10. Evidence-Gated Skip Rules（跳过必须给可证伪证据）

**任何层只能在所有必需证据齐备时跳过**。"我觉得不用"不是证据。

**v3.0 变化**：每层的具体 skip evidence 规范由各 child skill 自己定义并强制执行（每个 child skill 的 §"Skip Evidence" 段）。本节仅保留全局总则；详见各 child skill。

### 全局总则（所有 child skill 必须遵守）

1. **任何 skip 必须以仓库内可验证的事实作证据**（变更文件列表、route 列表、git diff、metadata、CI duration、risk score、已存在的低层覆盖）；不接受主观判断（如"这个项目还在早期"）
2. **Floor Rule §3.6 优先于 skip 规则**：High/Critical risk 即使路径白名单满足，relevant 层也不允许跳过
3. **Prototype-only 例外**仅当仓库显式标注 prototype/experiment **且**无 production release path **且**不涉及 auth/payment/PII/destructive 时成立
4. Skip evidence 必须在 §16 Step 3 Skip Evidence 列填写，并在 §16 evidence_validation.skipped_layers_unjustified 中被验收

---

## 11. Release Readiness Evidence（→ `qa-evidence-bundle`）

**v3.0 变化**：本节已下沉为 child skill `qa-evidence-bundle`。本节仅保留摘要 + dispatch contract。

**摘要要点**（必须能在 release 前出示）：

1. 实施摘要：功能范围 vs acceptance criteria 对照
2. 测试层覆盖表：13 层（9 测试层 + 4 横切）中哪些 dispatched、哪些 skipped + §10 evidence
3. 失败处理证据：关键错误路径有测试覆盖
4. **性能达标**（route-class-aware）：
   - Marketing / landing：LCP < 2.0s / INP < 150ms / CLS < 0.1
   - User-facing dashboard：LCP < 2.5s / INP < 200ms / CLS < 0.1
   - Internal admin / data-heavy：LCP < 3.5s / INP < 300ms / CLS < 0.1
   - 无法标定时按"较严"档（避免 budget-shopping）
5. a11y 达标：axe-core 无 CRITICAL violation + 关键路径 manual check
6. AppSec baseline 报告（来自 `appsec-security-orchestrator`）
7. 部署 Smoke 报告：`@smoke` 全绿（来自 `qa-smoke-release-safety`）
8. Flaky 状态：quarantine 列表 + accountability（来自 `qa-flaky-governance`）
9. 剩余风险登记：已知未覆盖项 + 接受理由 + 责任人

**Dispatch trigger**：
- §6 Step 9 自动触发
- 也是 `gsd-ship` / `gsd-verify-work` 的 consumer 接口

**Output contract**：见 `qa-evidence-bundle` §6（`qa_evidence_bundle` YAML）。

---

## 12. AppSec Routing（必读）

当任务涉及以下任一情况，**停止当前流程，先 handoff 给 `appsec-security-orchestrator`**：

- 后端 / 服务端代码（Next.js Route Handler、API Route、Server Action）
- 认证 / 授权逻辑（session、JWT、OAuth、RBAC）
- 用户数据存储 / PII 处理
- 文件上传处理
- 支付或金融数据
- 管理员 surface
- 生产部署

**Active penetration testing 永远不能自动跑**——走 `authorized-pentest-validation` 手动入口，需用户显式授权（双 gate：ROE + manual confirmation）。

---

## 13. Dispatch & Reference Contract（v3.1 自 dispatch 版）

### 13.1 重要语义澄清（v3.1 重大变化）

**v3.1 关键变化**：本 skill 的 `allowed-tools` 现在**包含** `Skill, Agent, AskUserQuestion` —— **它自己执行 dispatch 并自己验收 evidence**。这是 GSD 化升级的核心：从"输出建议（软）"到"真 dispatch + 真验收 + 阻断假通过（硬）"。

**本 skill 在 §6 Step 5/6/7/8/9 必须亲自做以下事情**：

- Step 2: `Agent(subagent_type=qa-risk-classifier, ...)` 做 risk score + Floor Rule
- Step 5: `Skill(skill=<qa-child-skill>, ...)` dispatch 13 个 owned QA skill
- Step 6: `Skill(skill=<bridge-skill>, ...) → Agent(subagent_type=<reference-agent>) → Skill(skill=<bridge-skill>, mode=validate_evidence)` 跑 3-stage bridge chain
- Step 7: `Agent(subagent_type=qa-evidence-validator, ...)` 验收 `.qa/evidence/<tag>/` 整目录
- Step 8: `Agent(subagent_type=qa-flaky-triager, ...)` + `Skill(skill=qa-flaky-governance, ...)` 双校验
- Step 9: `Skill(skill=qa-evidence-bundle, ...)` 聚合 + 出 release_decision

**绝不允许的反模式**：

- ❌ 输出 dispatch_qa_owned YAML 然后说"等调用方执行" — v3.0 行为，v3.1 已禁
- ❌ 跳过 §6 Step 7 的 evidence validator agent，自己 grep YAML 决定 PASS — 视为 Hard Rule §2.1 违反
- ❌ dispatch 失败时伪装 PASS — `.qa/evidence/<tag>/dispatch-failures.log` 非空时必须读取并影响 release_decision
- ❌ Stop hook 被 force-skip 后宣称完成 — 必须有 `.qa/risk-acceptance.yaml` 显式签字

**与 GSD 接口**：`gsd-ship` / `gsd-verify-work` 现在直接消费 `.qa/evidence/<tag>/qa_evidence_bundle.yaml` 文件（不需要再调本 skill 自己 dispatch）。它们读取 release_decision 即可：

```bash
bash "$HOME/.claude/scripts/qa-sdk.sh" gate.check <release-tag>   # exit 0 = PASS/CONDITIONAL_PASS(valid)/STRATEGY_READY(design-only), exit 1 = FAIL, exit 2 = BLOCKED
```

### 13.1.1 Bridge skill 3-stage dispatch chain（本 skill 自己跑全 chain）

reference agents（`tdd-guide` / `e2e-runner`）走 3-stage chain，本 skill 自己执行 (b)(c)(d)：**(b)** `Skill(bridge, mode="prepare_input")` → dispatch_input → **(c)** `Agent(reference-agent, prompt=<b 输出>)` 真跑（Playwright/trace/report）→ **(d)** `Skill(bridge, mode="validate_evidence", agent_output=<c>)` 按 §6 acceptance 验收 → `qa-sdk evidence.append <tag> <layer>`。完整 ASCII 图解见 [`references/dispatch-contract.md`](references/dispatch-contract.md)。

**禁止反模式**：跳 stage (d) 把 agent stdout 直接当 evidence；合并 (b)(d)；让 bridge skill 自调 Agent（必须 parent 调）。**适用 bridge**：`qa-test-design-tdd-bridge`(→`tdd-guide`) / `qa-e2e-coverage-gate`(→`e2e-runner`)；其余 11 child 是 1-stage dispatch。

### 13.2 Preflight（强制前置检查）

在输出 Route Recommendation 前，verify the target agent or skill exists locally：

- Glob `~/.claude/agents/*.md`
- 检查 available-skills 列表（system reminder 提供）
- 仅推荐 **present** 的 agent / skill
- 缺失时**不**推荐，改为 "target `<name>` not found in preflight; suggest fallback to <tool-level instruction>"

### 13.3 Dispatch Targets — 三类

#### A. QA-owned Child Skills（17 个，本 skill 直接 dispatch）

| Child Skill | 触发 | 触发 Step |
|---|---|---|
| `qa-static-baseline` | Static layer | §6 Step 5 |
| `qa-test-design-tdd-bridge` | Unit/TDD layer | §6 Step 5/6 (bridges to tdd-guide) |
| `qa-component-behavior` | Component layer | §6 Step 5 |
| `qa-integration-service-virtualization` | Integration layer | §6 Step 5 |
| `qa-contract-api` | Contract layer | §6 Step 5 |
| `qa-e2e-coverage-gate` | E2E layer | §6 Step 5/6 (bridges to e2e-runner) |
| `qa-visual-regression` | Visual layer | §6 Step 5 |
| `qa-a11y-compliance` | a11y layer | §6 Step 5 |
| `qa-performance-reliability` | Perf layer | §6 Step 5 |
| `qa-load-stress-reliability` | Load/Reliability layer | §6 Step 5 (bridges to qa-load-stress-runner) |
| `qa-mutation-effectiveness` | Mutation/Test-Effectiveness layer | §6 Step 5 (bridges to qa-mutation-runner) |
| `qa-mobile-native-e2e` | Mobile E2E layer (conditional) | §6 Step 5 (bridges to qa-mobile-e2e-runner) |
| qa-resilience-fault-injection | Resilience/Fault-Injection layer (RED-LINE, double-gate) | §6 Step 5 (bridges to qa-resilience-runner) |
| `qa-test-data-environment` | Test data plan | §6 Step 4 |
| `qa-flaky-governance` | Flaky triage | §6 Step 8 |
| `qa-smoke-release-safety` | Smoke / release safety | §6 Step 5 |
| `qa-evidence-bundle` | Release evidence aggregator | §6 Step 9 |

#### B. Reference Agents（通过 bridge skill 引用，不重写）

| Agent | 通过哪个 bridge skill 调用 | 用途 |
|---|---|---|
| `tdd-guide` | `qa-test-design-tdd-bridge` | unit / component / regression test 实现 |
| `e2e-runner` | `qa-e2e-coverage-gate` | Playwright execution, sharding, reports, traces |
| `code-reviewer` | direct（QA review 测试质量时） | review test quality / mocks / assertions / coverage gaps |
| `typescript-reviewer` / `python-reviewer` / `go-reviewer` / `rust-reviewer` | direct | 语言专项 review |

#### C. External Handoff Skills（跨主线，不属于 QA 内部）

| Skill | 类型 | 触发 |
|---|---|---|
| `appsec-security-orchestrator` | 跨主线 orchestrator | auth / secrets / API / permissions / injection / data exposure（按 §12 强制）|
| `dast-baseline-scanning` | AppSec sub-skill | 被动 DAST baseline scan |
| `pentest-scope-and-roe` | AppSec governance gate | 起草 ROE（不自动） |
| `authorized-pentest-validation` | AppSec manual-only | 主动 pentest，需 user explicit |
| `gsd-add-tests` / `gsd-code-review` / `gsd-verify-work` / `gsd-ship` / `gsd-debug` | GSD 主线 | GSD 流程运行时的接口 |
| `qa-evidence-bundle` 是 `gsd-ship` / `gsd-verify-work` 的 **consumer 接口** | 反向接口 | release/verify 直接消费 evidence bundle |

### 13.4 Missing Target 规则

- 若预期下游 agent / skill 缺失：
  - **不**伪装 dispatch 已发生
  - 输出：`"<name>" not found in preflight; recommendation: fallback to tool-level <Read/Grep/Bash> with prompt <X>`
  - 上层调用方决定是否补齐 / 接管

### 13.5 GSD 接口角色对照（见 §13.3 Section C；仅当 GSD 工作流运行时生效）

- `gsd-add-tests`：本 skill 提供分层决策 + 测试模板（→ 各 child skill 的 §"Implementation plan" 段）
- `gsd-code-review`：本 skill 提供 QA checklist + anti-pattern check（→ §2 + §14）
- `gsd-verify-work`：本 skill 提供 release readiness checklist（→ §11 + `qa-evidence-bundle`）
- `gsd-ship`：触发 release quality gate 全流程（→ §7 release lane + `qa-evidence-bundle` + `qa-smoke-release-safety`）
- `gsd-debug`：诊断 flaky test / env 差异根因（→ `qa-flaky-governance`）

**v3.1 注意**：以上 GSD slash commands 不需要"调本 skill 输出 dispatch 建议给 caller"。它们直接消费 `.qa/evidence/<tag>/qa_evidence_bundle.yaml`（见 §17.5 GSD 接口）。本 skill 内部所有 dispatch 由 §6 Step 4-9 自己完成。

---

## 14. Anti-Patterns（细则见 §2 Hard Rules，各 child skill 复述领域反模式）

8 类总反模式：硬睡（`waitForTimeout`）/ CSS 路径 locator / mock 内部模块 / 无 stdout 声称通过 / 自动 `--update-snapshots` / 主观跳过层 / 平铺写测试无风险分配 / quarantine 无 owner+expiry。详细禁令在 §2 Hard Rules；各 child skill 在自己的 §"Forbidden patterns" 段复述该层最相关的子集。

---

## 15. Standards Mapping  →  references/standards-mapping.md
> Relocated (SAFE-A appendix — verbatim, not weakened; not needed to execute a run). Read on demand.

---
## 16. Output Contract（任务输出强制结构）

每次 QA 任务完成后必须输出以下结构。**任一节缺失视为任务未完成**。

```markdown
## QA 任务报告

### Step 1. Discovery
- package manager / framework / 现有测试文件 / CI config
- 变更文件清单
- 受影响 user journey
- preflight agent/skill 可用性

### Step 2. Risk Score
- Impact: X — [理由 + 仓库证据]
- Likelihood: Y — [理由 + 仓库证据]
- Exposure Modifiers: [+a, +b, ...]，累加 = M（应用 §3.4 Cap +10 后 = M'）
- Pre-Floor Score = X*Y + M' = N → Pre-Floor Level: Low/Medium/High/Critical
- **Floor Rule 状态**（必填，即使未触发也要写 "no floor applied"）：
  - Impact≥5 floor: triggered → forced ≥ High / not triggered
  - Impact≥5 + +5 modifier floor: triggered → forced Critical / not triggered
  - production data write path floor: triggered / not triggered
  - public unauthenticated surface floor: triggered / not triggered
- **Final Level**（pre-floor 与 floor 取较高者）：Low / Medium / High / Critical

### Step 3. 测试层决策
| 层 | 状态 | Risk 依据 | Scope（启用时必填）| Skip Evidence（跳过时必填）|
|----|------|----------|------------------|--------------------------|
| Static | 启用 | 任何项目必须 | tsc + ESLint + npm audit + git-secrets 全仓 | — |
| Unit | 启用 | 新增 permissions 逻辑 | `src/lib/permissions.ts` 角色矩阵全覆盖 | — |
| Visual | 跳过 | Low | — | UI 文件 0 变更 + baseline 未批准 |

### Step 4. Test Data & Environment
- Fixture / Cleanup / Time / Auth / Tenant / Environment

### Step 5. Dispatch QA-owned Child Skills（v3.1 真 dispatch，镜像 §6 Step 5）
本 skill 自己 `Skill(skill=<qa-child-skill>, args=...)` 收 evidence 落 `.qa/evidence/<tag>/<layer>.yaml`（不再"自己写测试"）。inline **实际** dispatch 结果（含每层文件改动）：

\`\`\`yaml
child_skill_dispatch_results:
  - skill: qa-static-baseline
    status: dispatched          # dispatched | failed | skipped
    evidence_file: .qa/evidence/<tag>/static.yaml
    files_changed: [__tests__/xxx.test.ts(新增)]   # 该层产出/改动的文件
    dispatched_at: <timestamp>
    retry_count: 0
  - skill: qa-component-behavior
    status: skipped
    reason: §10 evidence-gated skip — UI files 0 changed + no baseline approved
\`\`\`

dispatch-failures.log 非空时，Step 9 必须读取并影响 release_decision（失败不允许伪装通过）。

### Step 6. Dispatch Reference Agents via Bridge Skills（v3.1 真 dispatch，镜像 §6 Step 6）
reference agents（`tdd-guide` / `e2e-runner`）走 §13.1.1 3-stage bridge chain，本 skill 自己执行 stage (b)→(c)→(d)。inline **实际** bridge 结果：

\`\`\`yaml
reference_agent_dispatch_results:
  - bridge_skill: qa-e2e-coverage-gate
    reference_agent: e2e-runner
    stage_b_completed: true
    stage_c_completed: true
    stage_d_completed: true     # 必须 true，否则视为 §2.1 hard rule 违反
    evidence_file: .qa/evidence/<tag>/e2e.yaml
    layer_status: PASS | FAIL | BLOCKED
\`\`\`

**Mode 适配**：`plan-only` / `design-only` 时 stage (c) 不实跑，bridge 输出 `BLOCKED — <mode>, see §1.5` + 预计执行命令 + 预计 unblock 条件；`execution` 时必附实际 stdout / artifact 路径。

### Step 7. Validate Evidence via qa-evidence-validator Agent（v3.1 真验收，镜像 §6 Step 7）
`.qa/evidence/<tag>/` 整目录交给 `qa-evidence-validator` agent 做 gate decision（不再自己 grep YAML）。inline 返回的 `evidence_validation` YAML：

\`\`\`yaml
evidence_validation:
  schema_conformance: pass | fail
  hard_rule_violations: []        # §2 违反列表（非空 → 阻断）
  per_layer_status: { static: PASS, component: PASS, e2e: FAIL }
  dispatch_failures_seen: 0
  release_decision_input: PASS | WARN | CONDITIONAL_PASS | FAIL | BLOCKED
\`\`\`

### Step 8. Flaky Triage
- 失败 → retry → 结果
- quarantine 决定 + accountability（issue / owner / expiry）

### Step 9. Release Readiness（dispatch 到 `qa-evidence-bundle`）
- 调用 `qa-evidence-bundle`，由它聚合 Step 1-8 输出
- 本节直接 inline `qa-evidence-bundle` 返回的 `qa_evidence_bundle` YAML（见该 child skill §6）

简要决策（按 mode）：
  - `execution` mode：可发布 / 待修复后发布 / 阻塞发布
  - `plan-only` mode：conditional-pass plan + preconditions list
  - `design-only` mode：strategy ready / not yet releasable / preconditions list（不允许输出 "可发布"）

### v3.0 新增 Dispatch / Validation Schema（贯穿 Step 4-9 输出）

```yaml
child_skill_dispatch:
  - skill: <name>
    reason: <为什么调>
    input: { <input fields> }
    expected_output: <YAML schema name>
    status: pending | dispatched | validated | failed
    validated_at: <step number, e.g. "Step 7">

external_references:
  - bridge_skill: <name>          # 例如 qa-test-design-tdd-bridge
    reference_agent: <name>        # 例如 tdd-guide
    reason: <为什么引用>
    input: { <fields prepared by bridge> }
    required_evidence: [commands, stdout, artifacts, ...]
    status: pending | dispatched | validated | failed

evidence_validation:
  by_layer:
    <layer>:
      status: PASS | FAIL | BLOCKED
      missing_artifacts: []
      hard_rule_violations: []
  missing_artifacts: []
  skipped_layers_unjustified: []
  blocked_items: []
  flaky_signals: []                          # 由 validator 填充，Step 8 triage 输入
  overall_evidence_confidence: low | medium | high
  release_decision_input: PASS | FAIL | BLOCKED | CONDITIONAL_PASS | STRATEGY_READY
  # 注：这是 validator 的 "input recommendation"。最终 release_decision 由
  # qa-evidence-bundle 在 Step 9 写入 qa_evidence_bundle.yaml；二者可能不同
  # （e.g. validator 给 CONDITIONAL_PASS，bundle 因 dispatch-failures.log 非空 forced BLOCKED）。

# v3.0 新增：调用方 1-shot 拿到 13 个 child skill 的 schema 入口，
# 避免 onboarding 时挨个 Read 每个 child SKILL.md 找 §6
schema_registry:
  qa-static-baseline:           { schema_section: "§6", path: "~/.claude/skills/qa-static-baseline/SKILL.md",                 output_key: "static_baseline" }
  qa-test-design-tdd-bridge:    { schema_section: "§6", path: "~/.claude/skills/qa-test-design-tdd-bridge/SKILL.md",          output_key: "test_design", bridges_agent: "tdd-guide" }
  qa-component-behavior:        { schema_section: "§6", path: "~/.claude/skills/qa-component-behavior/SKILL.md",              output_key: "component" }
  qa-integration-service-virtualization: { schema_section: "§6", path: "~/.claude/skills/qa-integration-service-virtualization/SKILL.md", output_key: "integration" }
  qa-contract-api:              { schema_section: "§6", path: "~/.claude/skills/qa-contract-api/SKILL.md",                    output_key: "contract", runner_agent: "qa-contract-runner", output_schema: "~/.claude/orchestrator-runtime/qa/schemas/CONTRACT_TEST_SCHEMA.v1.json" }
  qa-e2e-coverage-gate:         { schema_section: "§6", path: "~/.claude/skills/qa-e2e-coverage-gate/SKILL.md",               output_key: "e2e", bridges_agent: "e2e-runner" }
  qa-visual-regression:         { schema_section: "§6", path: "~/.claude/skills/qa-visual-regression/SKILL.md",               output_key: "visual" }
  qa-a11y-compliance:           { schema_section: "§6", path: "~/.claude/skills/qa-a11y-compliance/SKILL.md",                 output_key: "a11y" }
  qa-performance-reliability:   { schema_section: "§6", path: "~/.claude/skills/qa-performance-reliability/SKILL.md",         output_key: "performance" }
  qa-load-stress-reliability:   { schema_section: "§6", path: "~/.claude/skills/qa-load-stress-reliability/SKILL.md",         output_key: "load",       runner_agent: "qa-load-stress-runner",  output_schema: "~/.claude/orchestrator-runtime/qa/schemas/LOAD_TEST_SCHEMA.v1.json" }
  qa-mutation-effectiveness:    { schema_section: "§6", path: "~/.claude/skills/qa-mutation-effectiveness/SKILL.md",          output_key: "mutation",   runner_agent: "qa-mutation-runner",     output_schema: "~/.claude/orchestrator-runtime/qa/schemas/MUTATION_SCHEMA.v1.json" }
  qa-mobile-native-e2e:         { schema_section: "§6", path: "~/.claude/skills/qa-mobile-native-e2e/SKILL.md",               output_key: "mobile_e2e", runner_agent: "qa-mobile-e2e-runner",   output_schema: "~/.claude/orchestrator-runtime/qa/schemas/MOBILE_E2E_SCHEMA.v1.json", decision_states: "PASS|FAIL|BLOCKED|NOT_APPLICABLE" }
  qa-resilience-fault-injection: { schema_section: "§6", path: "~/.claude/skills/qa-resilience-fault-injection/SKILL.md",      output_key: "resilience", runner_agent: "qa-resilience-runner",   output_schema: "~/.claude/orchestrator-runtime/qa/schemas/RESILIENCE_SCHEMA.v1.json", decision_states: "PASS|FAIL|BLOCKED" }
  qa-test-data-environment:     { schema_section: "§6", path: "~/.claude/skills/qa-test-data-environment/SKILL.md",           output_key: "test_data", decision_states: "READY|BLOCKED" }
  qa-flaky-governance:          { schema_section: "§6", path: "~/.claude/skills/qa-flaky-governance/SKILL.md",                output_key: "flaky", decision_states: "PASS|FAIL|BLOCKED|NOT_APPLICABLE" }
  qa-smoke-release-safety:      { schema_section: "§6", path: "~/.claude/skills/qa-smoke-release-safety/SKILL.md",            output_key: "smoke" }
  qa-evidence-bundle:           { schema_section: "§6", path: "~/.claude/skills/qa-evidence-bundle/SKILL.md",                 output_key: "<aggregator — does not appear in own child_skill_results>" }
```

### CI 集成建议
- [具体 GitHub Actions 片段或说明]
```

---

## 17. Enforcement Registration（v3.1 — agent / hook / qa-sdk 注册）

> **SEMI-CRIB 骨架**：绑定的 NAMES 留在此处（`preflight-check.sh` / `qa-sdk init` 据此校验与注册）；完整 `settings.json` snippet + qa-sdk 逐命令契约 + exit-code 表 + Windows 路径注意 + GSD bash 例 见 [`references/enforcement-registration.md`](references/enforcement-registration.md)（init 时按需读取）。

### 17.1 Agents（`~/.claude/agents/`，frontmatter `name:` 必须匹配 — preflight Check 1 据此）
**3 orchestration agents + 10 dedicated runners + 2 Architecture-Intake agents = 15**（intake = `qa-runtime-detector` · `qa-path-graph-miner`，opus read-only，§6 Step 1.7，输出 `RUNTIME_DETECTION_SCHEMA.v1` / `PATH_GRAPH_SCHEMA.v1`，并由主线程综合 `TEST_PLAN_SCHEMA.v1`）：orchestration = `qa-risk-classifier`(opus) · `qa-evidence-validator`(sonnet) · `qa-flaky-triager`(sonnet)（即 §1.6.2 binding 三件套）；runners（B.1.f R2 dedicated）= `qa-static-baseline-runner` · `qa-component-runner` · `qa-contract-runner`(已接线 — schema_registry.qa-contract-api.runner_agent) · `qa-visual-runner` · `qa-a11y-runner` · `qa-perf-runner`；runners（CAPABILITY-UPGRADE Wave A）= `qa-load-stress-runner` · `qa-mutation-runner` · `qa-mobile-e2e-runner`(DORMANT/备选 — 仅 mobile-app marker present 时激活)；runner（CAPABILITY-UPGRADE Wave B）= `qa-resilience-runner`（RED-LINE — gated behind parent planning-first double-gate，**不 auto-dispatch**：仅在 staging 目标 + High/Critical resilience surface + 人审通过后由 `qa-resilience-fault-injection` 桥接）。每个必须输出 §16 schema YAML（或 workflow-spec 对应 `*_SCHEMA.v1`），否则视为 dispatch 失败。

### 17.2 / 17.3 Hooks（脚本 `~/.claude/hooks/qa-*.js`；**项目级** `.claude/settings.json` 注册，经 `qa-sdk init`，不污染全局）
5 个：`qa-block-update-snapshots`(PreToolUse Bash) · `qa-floor-rule-prompt`(PostToolUse Edit|Write) · `qa-detect-internal-mock`(PostToolUse Edit|Write) · `qa-quarantine-accountability`(PreToolUse Bash) · `qa-evidence-required`(Stop)。**+ workflow-spec mode 必装** `qa-preview-gate`(PreToolUse Workflow)。**+ v3.3 additive gates（随 init 装，非 QA 项目 silent）**：`qa-main-thread-test-guard`(PreToolUse Bash, 承重柱2 真锁) · `qa-required-layer-gate`(Stop, fail-closed) · `qa-runtime-mismatch-gate`(Stop, fail-closed) · `qa-no-silent-fallback`(PreToolUse Write|Edit|MultiEdit + Stop, fail-closed) · `qa-entry-ask-required`(PreToolUse Bash, 软 gate, fail-open) · `qa-tasklist-required`(PreToolUse Bash, advisory)。完整 NAMES + trigger 单一真相源 = `manifests/hook-registry.json` qa subsystem。每 hook 第一步 `_qa-common.preflight`：无 `.qa/config.json` → silent exit 0；解析失败 → fail-closed；`off`/`warn`/`strict` 分级。**注册铁律**：Stop 不带 `async:true`（异步无法 block）；PreToolUse exit 2 = hard block / exit 0 = allow；PostToolUse 只 advisory；`Edit|Write|MultiEdit` 全 match。完整 snippet + 绝对路径展开见 reference。

### 17.4 qa-sdk 命令（`~/.claude/scripts/qa-sdk.sh`；§6 各 Step **必经**，不许 `echo > file`）
`init` / `set-active` / `evidence.append` / `evidence.list` / `evidence.validate-presence` / `gate.check` / `finding.add` / `quarantine.add`(8字段) / `approve.snapshot`(`--human-attested` 强制) / `spec.hash` / `sentinel.write` / `sentinel.show`。**gate.check 严格表**：`PASS`→0 · `STRATEGY_READY`→0 仅 `--mode design-only` · `CONDITIONAL_PASS`→需 `.qa/risk-acceptance.yaml` 完整且未过期否则 2 · `FAIL`→1 · `BLOCKED`→2 · 未识别→2。逐命令 exit code 见 reference。
**`workflow-state` layer 边界（D4+R10 lock）**：是 Skill-level provenance / planning snapshot（单文件累加器），**不是** Workflow native cross-session resume cache（`resumeFromRunId` 仅 same-session）；下次 run 由 Skill 主线显式读 + 注入 `args.previous_results`。

### 17.5 GSD 接口（反向，artifact-based 解耦）
`gsd-ship` / `gsd-verify-work` 直接消费 `.qa/evidence/<tag>/qa_evidence_bundle.yaml`（读 `qa-sdk gate.check <tag>` exit code：0 PASS / 1 FAIL / 2 BLOCKED）。bash 例见 reference。

## 18. Workflow-Spec Execution Mode (Phase B v3.2 — 2026-05-29)

`execution_mode: "workflow-spec"` 是 v3.2 引入的"高保真、可 audit、可 resume、cost-deterministic"运行模式，与现有 v3.1 Skill-direct dispatch 并存。本节给所有读者一个**够看的入口图**，细节查 [QA-PHASE-B-BLUEPRINT.md](file://~/QA-PHASE-B-BLUEPRINT.md) 与 [ORCHESTRATION-MIGRATION-PLAN.md](file://~/ORCHESTRATION-MIGRATION-PLAN.md)。

### 18.1–18.4 workflow-spec 边界 / Presets / Evidence 路径 / Dual-Mode（骨架）

> 详细 boundary 表 · preset 选择树（wall-clock/token est） · evidence 路径树 · dual-mode 对比表 relocated to [`references/workflow-spec-dispatch.md`](references/workflow-spec-dispatch.md)（CONTRACT-SENTINEL `qa.workflow-spec-dispatch.v2026-05-29`）。

**6 presets**：`smoke` / `graph-smoke`（内部 harness，**绝不暴露用户**）· `quick-check`（/qa-quick-check）· `focused-qa-gate`（/qa-focused-gate）· `release-readiness`（/qa-release-readiness）· `commercial-cert`（/qa-commercial-cert，15 phases，+Visual/A11y/Perf Audit→Gate，**强制 budget approval**）。

**边界铁律**（binding）：
1. **风险分类永远先在 Skill 主线跑**（R4 Option A）——`qa-risk-classifier` 出 `risk_snapshot` → 写入 `spec.context` → 再 launch；Workflow 入口 LayerSelect 消费 snapshot，不重跑
2. **commercial-cert 强制 Preview + budget approval**——Skill 渲染 `=== REQUIRES EXPLICIT BUDGET APPROVAL ===` + 等 explicit approve + 写 sentinel（必含 `approved_estimate_high` + approval_text 含 approved/approve/批准/确认/同意 任一）→ `qa-preview-gate` 校 sentinel 才允许 `Workflow({name:"qa-orchestrator"})`
3. **Workflow body 是 pure**：no `Date.now / Math.random / require / fs / fetch / process.cwd`；所有外部命令（tsc/eslint/playwright/lighthouse/axe/pa11y）在 agent node 跑，deterministic op 只解析已收集证据
4. workflow-spec **永远**在风险分类 / preview / approval / sentinel 写盘**之后**才 launch；Skill-direct **永远**不调 `Workflow`（除非用户显式 enable）；同一 release_tag 不能同时跑两 mode（launch 前 `qa-sdk evidence.list <tag>` 查冲突）

### 18.5 Workflow-Spec Launch Contract（Skill → Workflow handshake，B.1.g 2026-05-29 — REQUIRED）

> 镜像 `appsec-security-orchestrator` §16.11。Skill 主线在 workflow-spec mode 下 launch Workflow 之前**必走的 14 步**；任一 skip / silent fallback = bug。Helper：`qa-sdk spec.hash` / `qa-sdk sentinel.write` / `qa-sdk sentinel.show`（§17.4）+ `shared/spec-hash.js`。
>
> **READ [`references/workflow-spec-dispatch.md`](references/workflow-spec-dispatch.md) IN FULL before launching** — 它carries 每步逐字 body（exact bash、preset 路径、context 字段、draft-07 约束）。CONTRACT-SENTINEL: `qa.workflow-spec-dispatch.v2026-05-29`。
>
> **Governed Gate Mode (CLAUDE.md §3.7) — gate_active window**：作为本 contract 的**第一个动作**（在 Step 1 / preview render 之前），Skill 必须写 `.qa/state.json` `gate_active: true`，并在 terminal verdict / abort 时清除。这关掉 pre-sentinel 窗口，使 `governed-gate-workflow-guard.js` 在**整个 gate 期间**拦截 inline model-authored Dynamic Workflows。

**14 步骨架**（标题 + 约束；逐步 body 见 reference）：

1. 解析触发：显式 slash（/qa-quick-check / /qa-focused-gate / /qa-release-readiness / /qa-commercial-cert）OR `config.execution_mode=="workflow-spec"` → 都不匹配则走 §6 Skill-direct，不进 §18.5
2. 跑 §1.6.1 Discover + §3 Risk Model（dispatch `qa-risk-classifier`）→ `risk_snapshot`（不出 snapshot 不能进 §18.5，**R4 Option A 锁**）
3. Pick preset（`~/.claude/orchestrator-runtime/qa/presets/`：quick-check / focused-qa-gate / release-readiness / commercial-cert；内部 smoke / graph-smoke 绝不暴露用户）
4. Load preset → `spec`；walk phases + pipeline.stages inline 每个 prompt_ref/schema_ref。**缺文件 = hard fail**
5. 注入 `spec.context`：risk_snapshot / release_tag / run_id / critical_release_paths / **policy**（commercial-cert 额外 budget_approval 占位）。**policy 的 canonical floor = preset 自带 `spec.context.policy`（a11y_floor + perf_floor）**，只准在其上 merge 项目收紧项、绝不丢/绝不放宽——引擎读 `args.context.policy`（≠ `spec.context`），`perf_gate_policy` 缺 floor 默认 Infinity = perf 门静默失效（详注见 reference step 5）
6. 决定 fanout / pipeline width（ComponentOrContract = changed_surfaces；VisualAudit = surfaces×viewports×themes；E2E pipeline = critical_scenarios，按 preset clamp）
7. **Skill-side alias resolution（§1.11 #2 必走）**：node.model alias → `resolved_model`；`args.model_policy_version`。**Model-tier 铁律（Policy A, 2026-05-30，取代旧 sonnet-cap）**：haiku 仅 smoke preset；real gate ≥ sonnet；judgment/verdict 节点 bake `resolved_model: opus`；fanout 封顶 sonnet。强制器 = `shared/lint-model-policy.js`（接进 qa\|appsec validate-all-presets.sh）。注：旧"`workflow-lint.sh` 拒 preset 写死 opus / 自动上提"**从未实装**（workflow-lint 只 lint runner JS），已废
8. Compute `spec_hash`（`qa-sdk spec.hash`；`sha256:<64hex>`；与 `qa-preview-gate.js` byte-identical）
9a. `validate-spec.js <spec>` → exit 0 OK / 2 INVALID（中止，0 token）
9b. `preflight-check.sh <spec>`（agentType frontmatter / required hook in settings.json / qa-sdk / model alias / **13 embedded_skill_contracts anchors in SKILL.md**）— **不可 skip，缺一不 launch**
10. Render Execution Preview（`shared/preview-template.md`）；commercial-cert 额外 banner `=== REQUIRES EXPLICIT BUDGET APPROVAL ===` + echo `token_estimate_high` 数字
11. 等 reply，match approval whitelist（精确，大小写无关，trim）。**non-budget modes**（quick-check / focused-qa-gate / release-readiness）：EN `OK/okay/approve/approved/go/yes/proceed/ship it/LGTM`；CN `跑/批准/同意/继续/好/执行`。**commercial-cert 收紧为铁律 2 的 5 词集**：`approve / approved / 批准 / 确认 / 同意` 任一（与 `qa-sdk sentinel.write` + `qa-preview-gate.js` 实现一致；广义词如 OK/go/yes **不**算 commercial-cert 批准），AND reply 含批准的 `estimate_high` 数字 OR 复述 banner。不 match → 不写 sentinel → 不 launch
12. 写 sentinel（fail-closed）：`qa-sdk sentinel.write --run-id --mode --spec-file --approval-text --ttl-seconds [--approved-estimate-high]`（重算 spec_hash 防漂移 / TTL clamp [30,3600] / 原子写 `.qa/state/preview/<safe_run_id>.json`）。Bash 失败 = abort
13. Launch `Workflow({name:"qa-orchestrator", args:{spec, run_id, release_tag, spec_hash, context:{risk_snapshot, critical_release_paths, policy, branch_sha, viewport, …}, model_policy, previous_results}})`（`context.policy` 必须是 Step 5 的 merged policy，**带全 a11y_floor + perf_floor**；引擎读 `input.context.policy`，perf 缺 floor = 不拦）。`qa-preview-gate` 校 sentinel → 允许/拒。错误绝不 silent re-launch
14. Persist：result.phase_outputs 各层 → `qa-sdk evidence.append <tag> <layer>`；workflow-state snapshot（**含 `execution_fingerprint`**：`node ~/.claude/orchestrator-runtime/shared/run-fingerprint.js <assembled-spec> <project-root> --fanout <actual> --domain qa` → 折 spec_hash + agent_hashes + resolved_models + prompt/schema hash + policy_version + lint_version + fanout；provenance 锚，非 launch gate）；`qa-sdk gate.check <tag>` 出 release_decision exit code

**非协商铁律**：
- **Step 8 在 Step 9 之前**（hash 先于 validate；hash 必须在 Step 7 alias-resolve 之后，否则 resolved_model 不入 hash）
- **Step 9b preflight 不可 skip**（"为省 token" 跳 → 一次跑废）
- **Step 11 approval 是 human-in-the-loop**：不 auto-approve / 不把沉默当批准 / 不把 unrelated reply 当批准
- **Step 12 sentinel = fail-closed**：Bash 写失败 → abort，绝不 Workflow() 裸 launch
- **Step 14 persist 必经 qa-sdk**（不允许 `echo > file`）；`workflow-state.yaml` 是 Skill provenance log（D4），不是 Workflow native resume cache

## 19. 参考资源  →  references/external-links.md
> Relocated (SAFE-A appendix — verbatim, not weakened; not needed to execute a run). Read on demand.

---