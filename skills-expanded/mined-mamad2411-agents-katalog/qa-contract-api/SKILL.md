---
name: qa-contract-api
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
description: >-
  QA child skill - contract layer: REST (OpenAPI), GraphQL, event-driven (AsyncAPI) and consumer-driven (Pact) contract tests; breaking-change detection, provider/consumer compatibility, error contracts. No happy-path-only, no unreported provider drift. Owns parent section 4 Layer 5.
---

# qa-contract-api

## 1. Position

API contract 测试 skill。**不**做内部 integration（→ `qa-integration-service-virtualization`），不做 E2E（→ `qa-e2e-coverage-gate`）。专注 API 边界 schema + 版本兼容 + breaking change 检测。

## 2. Triggers

- Parent §6 Step 5（API boundary 变更时）
- REST schema / OpenAPI spec 变更
- GraphQL schema 变更
- AsyncAPI / event payload schema 变更
- public API / SDK / microservice provider-consumer 边界
- Frontend-backend 跨团队接口

## 3. Responsibilities

- **REST**：OpenAPI schema validation / backward compat / status / header / body shape
- **Consumer-driven**：Pact contract generation + provider verification
- **Event-driven**：AsyncAPI message shape / channel / payload / versioning
- **GraphQL**：schema diff + deprecation policy
- **Breaking change detection**：响应字段去除 / 类型变更 / 必填变更 / status code 变更
- **Error contract coverage**：4xx / 5xx / validation error / permission error
- **Drift detection**：spec 文档 vs 实际 provider behavior 不一致必须报告

### 3.1 OpenAPI 实务要点（REST contract）

OpenAPI（原 Swagger 规范，现 OpenAPI 3.1 与 JSON Schema 对齐）是 REST contract 的单一真相源。本 skill 验证方向：

- **Schema-as-source-of-truth**：`openapi.yaml` / `openapi.json` 是契约，provider 实际响应必须 conform。验证用 schema validator（如 `openapi-spec-validator` 校 spec 合法性 + response-validation 中间件 / `Dredd` / `schemathesis` 校 provider 响应符合 spec）。
- **Backward-compat diff**：与上一版 spec 做结构 diff（如 `oasdiff` / `openapi-diff`），机器判定 breaking vs non-breaking——**breaking**（删字段 / 收紧类型 / 加必填 req 字段 / 改 status code / 删 endpoint）必须报告并影响 `decision`；**non-breaking**（加可选字段 / 加 endpoint / 放宽约束）记录但不阻断。
- **Examples 即测试数据**：spec 里的 `examples` / `example` 应被用作 payload 验证样本（`payload_examples_verified`），避免"spec 写了 example 但 provider 返回不符"。
- **错误响应建模**：4xx/5xx 也必须在 spec 里有 schema（不只 200），否则 `negative_cases` 无契约可验。

### 3.2 Consumer-driven contract 实务要点（Pact）

Pact 做 consumer-driven contract testing（CDC）——由**消费者**定义期望，生成 pact 文件，由**提供者**回放验证。本 skill 验证方向：

- **两侧分工**：consumer side 跑交互生成 `pacts/*.json`（消费者期望的 request/response 对）；provider side 用 **provider verifier**（`@pact-foundation/pact` provider verification / `pact-verifier`）回放每个 interaction，确认 provider 真能满足。
- **Pact Broker / can-i-deploy 心智**：成熟 CDC 用 Pact Broker 存契约 + `can-i-deploy` 判断"此版本与对端已验证契约是否兼容"。本 skill 若检测到 broker 配置，应在 `verification_report` 标注 broker 验证状态；若无 broker（本地 pact 文件直验），照常回放但标注 confidence 较低（无跨版本矩阵）。
- **provider state**：每个 interaction 常依赖 provider state（"given a user exists"）。验证时这些 state setup 必须真实置备，**不允许 mock 掉 provider 自身行为**来假装通过（与 parent Hard Rule §2.4 一致）。
- **CDC 不替代 E2E**：pact 只证"请求/响应形状契约成立"，不证完整业务流——业务流仍是 E2E（→ `qa-e2e-coverage-gate`）。

### 3.3 Property/generative contract testing 实务要点（Schemathesis — Q5 扩展）

> ADDITIVE 能力扩展（CAPABILITY-UPGRADE Wave A, Q5）。前面 §3.1/§3.2 是"example-based"契约验证（验你手写的 example / pact interaction）。本节加 **property/generative** 维度：**从 OpenAPI/GraphQL schema 自动派生海量测试用例**，零手写，专抓"spec 说会发生但你没想到的输入组合"。两者互补——example 验已知路径，generative 探未知边角。

**Schemathesis**（MIT）从你的 OpenAPI 3.x / GraphQL schema 自动生成请求并对响应做 5 类内置 property 检查：

- **`not_a_server_error`**：任何请求都不该让服务返 5xx（最常抓的 bug —— 畸形输入打穿到未处理异常）。
- **`status_code_conformance`**：响应 status 必须在 spec 声明的集合内（spec 写了 200/400，实际返了 500/418 = 违约）。
- **`content_type_conformance`**：响应 `Content-Type` 必须匹配 spec。
- **`response_schema_conformance`**：响应 body 必须 conform spec 里声明的 schema（字段缺失 / 类型错 / 多余字段视配置）。
- **`response_headers_conformance`**：声明的必需 header 必须出现。

实务要点：

- **Schema-driven 生成 + shrink**：Schemathesis 基于 Hypothesis 引擎，对每个 endpoint 用 schema 约束生成输入（边界值、空、超长、Unicode、类型边缘、enum 全集），失败时 **自动 shrink 到最小复现请求** —— report 直接给"打挂服务的最小输入"。
- **`--checks all`**：跑全部内置 check（默认只跑部分）。CI 里建议 `schemathesis run --checks all <spec-or-url>`。
- **Stateful testing（可选）**：基于 OpenAPI links 做有状态序列（create → 用返回 id → get/delete），抓"单接口都对但组合起来违约"。
- **与 AppSec 边界**：Schemathesis 跑在 **你拥有的 staging/local API** 上做契约鲁棒性，**不是** active security scan / fuzzing-for-exploit。当它打出的是**安全语义**问题（auth bypass、injection、敏感数据泄漏在响应里）→ 标识并 **handoff `appsec-security-orchestrator`**（与 AppSec fuzzing 能力共用底座，但本 skill 只做契约符合性，不做漏洞利用）。**绝不对生产或第三方 API 跑**（高频请求 = 事实上的压力/骚扰）。
- **target 来源**：spec 文件（静态 schema 校验）或 staging base URL（live 响应符合性）。live 模式打 staging，不打 prod。
- **gate 挂钩**：Schemathesis 非零 exit（有 check 失败）→ runner 据此判该 contract layer FAIL；失败用例进 `negative_cases` / `breaking_changes` 旁的 `generative_findings`。

落 §6 输出时：generative 结果记进新增的 `property_testing` 段（见 §6），区分于 example-based 的 `verified_interactions`。

## 4. Non-responsibilities

- 不替代 E2E（happy path 完整业务流是 E2E 的事）
- 不替代 integration（内部模块边界不在本层）
- 不做 perf load testing（→ `qa-performance-reliability`）

## 5. Workflow

1. 识别 contract type（REST / GraphQL / event / pact）
2. 抽取 provider spec + consumer expectations
3. Compat check（与上一版 spec diff）
4. Generate verification cases（含 4xx/5xx）
5. Run verification（OpenAPI validator / Pact provider verifier / GraphQL inspector）
6. **Property/generative pass（§3.3，有 OpenAPI/GraphQL schema 时）**：跑 Schemathesis（`--checks all`，打 staging 或静态 spec）自动派生用例，抓 5xx / status / schema 不符；失败 shrink 到最小请求
7. Output `contract_testing` YAML

## 6. Output Contract

```yaml
contract_testing:
  contract_type: openapi | pact | asyncapi | graphql | mixed
  provider: <name>
  consumers: [<list>]
  compatibility:
    breaking_change_detected: false
    breaking_changes: []  # if any, list each (removed field / type change / required)
    deprecated_fields: []
  verified_interactions:
    - endpoint: GET /api/checkout
      status_codes_tested: [200, 400, 401, 403, 404, 500]
      schema_match: true
      payload_examples_verified: true
  negative_cases:
    validation_error_covered: true
    permission_error_covered: true
    rate_limit_covered: true
  property_testing:                       # §3.3 generative/property pass (Q5)
    tool: schemathesis | none
    schema_source: openapi.yaml | https://staging.example.com/openapi.json | graphql-schema
    target_is_production: false           # 必须 false（live 模式只打 staging）
    checks_run: [not_a_server_error, status_code_conformance, content_type_conformance, response_schema_conformance, response_headers_conformance]
    examples_generated: <N>
    stateful_testing: true | false        # 基于 OpenAPI links
    generative_findings:                  # 失败用例（已 shrink 到最小复现）
      - check: not_a_server_error
        endpoint: POST /api/checkout
        minimal_repro: { body: { qty: -2147483648 } }
        observed: "500 unhandled IntegerOverflow"
        security_relevant: false          # true → handoff appsec-security-orchestrator
    artifact: <path schemathesis report / cassette>
  artifacts:
    contract_file: openapi.yaml | pacts/*.json | asyncapi.yaml
    verification_report: <path>
  drift_detected: false
  drift_details: []
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 7. Parent Integration

- Triggered by: parent §6 Step 5
- Returns: `contract_testing` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.contract`

## 8. Forbidden patterns

- happy-path-only contract verification
- 跳过 4xx / 5xx error contract
- 接受 schema 文档与 provider 实际行为不一致而不报告
- 跳过 breaking-change 检测
- 对生产 / 第三方 API 跑 Schemathesis 生成式用例（高频请求 = 事实压力；只打你拥有的 staging/local — 与 parent §2.6 同源）
- 把 Schemathesis 打出的**安全语义**问题（auth bypass / injection / 响应泄敏）在 QA 内闭环（必须 handoff `appsec-security-orchestrator`，本 skill 只判契约符合性）
- 有 OpenAPI/GraphQL schema 却只做 example-based 验证、跳过 generative pass（漏掉"spec 允许但你没想到的输入"边角）

## 9. References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Pact — consumer-driven contract testing](https://docs.pact.io/)
- [Pact Broker / can-i-deploy](https://docs.pact.io/pact_broker/can_i_deploy) (cross-version contract compat matrix)
- [oasdiff](https://github.com/Tufin/oasdiff) / [openapi-diff](https://github.com/OpenAPITools/openapi-diff) (OpenAPI breaking-change detection)
- [schemathesis](https://schemathesis.readthedocs.io/) / [Dredd](https://dredd.org/) (provider response conformance to OpenAPI spec)
- [Schemathesis — property-based API testing (auto-derives cases from OpenAPI/GraphQL; 5 built-in checks; shrinks to minimal repro)](https://schemathesis.readthedocs.io/en/stable/) · [quick start](https://schemathesis.readthedocs.io/en/stable/quick-start/) · [stateful testing via OpenAPI links](https://schemathesis.readthedocs.io/en/stable/stateful/)
- [AsyncAPI](https://www.asyncapi.com/)
- [GraphQL Inspector](https://the-guild.dev/graphql/inspector) (schema diff)

## 10. Workflow-spec status & KNOWN GAP（contract 层在 workflow-spec 模式下尚未接线）

> 诚实标注边界（不夸大已实现能力）。本 skill 在 parent 的两种 execution mode 下成熟度**不同**，必须分开看：

- **prompt-only mode（parent §6 Skill-direct，默认）— 可用**：parent §6 Step 5 直接 `Skill(skill=qa-contract-api, ...)` 调用本 skill，本 skill 按 §5 workflow 跑、输出 §6 `contract_testing` YAML、由 parent 经 `qa-sdk evidence.append <tag> contract` 落盘。此路径是 contract 层的**当前实际产证据路径**。

- **workflow-spec mode（parent §18 / qa-orchestrator.js）— contract evidence 由 qa-component-runner 双兼容产出；dedicated runner 预备未接线**：
  - workflow-spec 模式下，contract **由 `qa-component-runner` 经 `component-or-contract.v1` prompt 按 `item.kind`（api-contract / schema）路由，emit `CONTRACT_TEST_SCHEMA.v1`，`.qa/evidence/<tag>/contract.yaml` **会被产出**（preset 的 expected evidence 已含 contract.yaml）。所以 contract 层在 workflow-spec 模式**有 evidence**——经 component-runner 双兼容，而非经 dedicated runner。
  - 仍未接线的是 **专职 `qa-contract-runner` 的独立拆分**：parent §17.1 把它标「预备」，与其余 5 个 R2 runner（static/component/visual/a11y/perf）不同——后者已 wiring-audited，专职 `qa-contract-runner` **尚未接入** `qa-orchestrator.js` 的 deterministic spec phases（无独立 Contract phase fan-out）。
  - 不要伪装两件事：① contract evidence 确实产出（别记为 NOT_WIRED / 静默抹掉），② 但专职 runner 拆分尚未落地（别声称 dedicated `qa-contract-runner` 已 active）。若该 release 实际触及 API boundary（§2 触发条件成立）且需更细的 provider/consumer 拆分，可在 prompt-only 路径补跑本 skill，或登记为 residual risk + owner（parent §11 / `qa-evidence-bundle`）。

- **后续 wire 需要做的（交主控 / 后续 slice，不在本 slice 范围）**：① 接线已存在的 `~/.claude/agents/qa-contract-runner.md`（文件已在，缺的是 runner 接线 —— 把它 wire 进 `qa-orchestrator.js` + 一个专职 Contract phase；agentType frontmatter + 输出 `CONTRACT_TEST_SCHEMA.v1`）；② 在 `qa-orchestrator.js` 相关 preset 的 phases 里加 contract phase（fan-out by changed API surfaces）；③ parent §17.1 把「预备」改为「runtime-PROVEN」前需 cold-start wiring audit。本 slice **仅文档标注 gap，不动 runner / orchestrator / preset / schema**。
