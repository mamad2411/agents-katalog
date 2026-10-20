---
name: qa-evidence-bundle
version: 1.0.1
status: stable
created_date: 2026-05-24
updated_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob, Write
parent: enterprise-qa-testing
description: >
  QA child skill — release evidence aggregator. Collects outputs from all
  other QA child skills + AppSec handoff status + flaky governance state +
  smoke results, produces the auditable `qa_evidence_bundle` YAML consumed
  by `gsd-ship` / `gsd-verify-work` / human reviewer. Owns parent §11.
  Trigger phrases: "release evidence / 发布证据 / QA sign-off / release readiness /
  evidence bundle / ship gate / verify QA".
---

# qa-evidence-bundle

## 1. Position

Release evidence 打包器。本 skill 是商业级 QA 的核心交付物：**最终产物不是"测试建议"，而是可审计 release evidence**。聚合 12 个其他 QA child skill 的输出 + AppSec status + residual risk + flaky state，输出供 release pipeline 直接消费的结构化数据。

## 2. Triggers

- Parent `enterprise-qa-testing` §6 Step 9（默认 dispatch）
- 独立触发：`gsd-ship` / `gsd-verify-work` 直接消费（reverse interface）
- 独立触发：人工 reviewer 要求"出示 QA 证据"
- 独立触发：merge gate / release gate / canary promotion gate

## 3. Responsibilities

- 聚合 child skill evidence（按 §6 schema）
- 标记 skipped layers + skip evidence
- 标记 blocked items + 阻塞原因
- 标记 residual risk + 接受人
- 标记 flaky status + critical-path quarantine 警报
- 标记 AppSec handoff status（已 dispatch / target 缺失 / 不适用）
- 输出 final release decision
- 不**自己**做决策 —— 决策从聚合数据按规则推导（all PASS → PASS；任一 BLOCKED → BLOCKED；FAIL > 0 → FAIL）

## 4. Non-responsibilities

- 不重跑测试（只聚合，跑测试是各 child skill 的事）
- 不调整 risk score（来自 parent §6 Step 2）
- 不审批 residual risk（必须由 owner 签名）
- 不替代 AppSec sign-off（必须由 `appsec-security-orchestrator` 出具）

## 5. Workflow

1. **Collect** child skill outputs：扫描所有相关 child skill 的 YAML 输出
2. **Validate completeness**：必填字段是否齐全（mode-aware）
3. **Cross-check**：layers_required vs layers_executed；skipped layers vs skip evidence
4. **Aggregate flaky state**：从 `qa-flaky-governance` 拉 quarantine 列表
5. **Aggregate AppSec status**：从 `appsec-security-orchestrator` route recommendation 拉 status
6. **Compute decision**（确定性规则，按顺序匹配 — 命中即返回，非 LLM 判断）：
   - 任一 child skill decision = BLOCKED → bundle = BLOCKED
   - 任一 critical release-path flaky 未修 → bundle = BLOCKED
   - AppSec required but not dispatched → bundle = BLOCKED
   - **`test_data.decision = BLOCKED` → bundle = BLOCKED**（与第一条同优先级；显式列出因 `qa-test-data-environment` 使用 READY/BLOCKED 二态而非 PASS/FAIL/BLOCKED 三态）
   - **`test_data.decision = READY` → 视同 PASS 参与聚合**（READY 是该 child skill 的"完成"语义，因为 test data plan 不跑测试，只输出环境/fixture 计划）
   - **`flaky.decision = NOT_APPLICABLE` → 视同 PASS 参与聚合**（无 execution 历史时合法 - 在 plan-only mode 或 green-field 仓库首次跑）
   - 所有 PASS（含上述视同 PASS）+ residual risk 有 owner → bundle = PASS
   - mode != execution → bundle = CONDITIONAL_PASS / STRATEGY_READY（无论 child 状态如何）
7. **Output `qa_evidence_bundle` YAML**

**Decision state 字典（参考表）**：

| Child Skill | Possible Decision States | 聚合时映射 |
|---|---|---|
| qa-static-baseline / component / integration / contract / e2e / visual / a11y / performance / smoke / test-design-tdd-bridge | PASS / FAIL / BLOCKED | 直接参与 |
| qa-test-data-environment | READY / BLOCKED | READY→PASS / BLOCKED→BLOCKED |
| qa-flaky-governance | PASS / FAIL / BLOCKED / NOT_APPLICABLE | NOT_APPLICABLE→PASS |
| qa-evidence-bundle (self) | PASS / FAIL / BLOCKED / CONDITIONAL_PASS / STRATEGY_READY | 输出，不聚合 |

## 6. Output Contract

```yaml
qa_evidence_bundle:
  feature: <name>
  risk_score: <N>
  risk_level: low | medium | high | critical
  mode: execution | plan-only | design-only
  layers_required:
    - static
    - unit_tdd
    - component
    - integration
    - contract
    - e2e
    - visual
    - a11y
    - performance
    - smoke
    # cross-cutting:
    - test_data
    - flaky
    - evidence
  layers_executed: [...]
  layers_skipped:
    - layer: visual
      reason: <从 §10 evidence>
      evidence: <仓库内证据>
      owner: <github handle>
  child_skill_results:
    static: { decision: PASS, source: qa-static-baseline, artifact: ... }
    test_design: { decision: PASS, source: qa-test-design-tdd-bridge, artifact: ... }
    component: { decision: PASS, source: qa-component-behavior, artifact: ... }
    integration: { decision: PASS, source: qa-integration-service-virtualization, artifact: ... }
    contract: { decision: SKIPPED, source: qa-contract-api, reason: ... }
    e2e: { decision: PASS, source: qa-e2e-coverage-gate, artifact: playwright-report/ }
    visual: { decision: SKIPPED, source: qa-visual-regression, reason: ... }
    a11y: { decision: PASS, source: qa-a11y-compliance, artifact: a11y-junit.xml }
    performance: { decision: PASS, source: qa-performance-reliability, artifact: lhci-report.html }
    test_data: { decision: READY, source: qa-test-data-environment }
    flaky: { decision: PASS, source: qa-flaky-governance, quarantine_count: 0 }
    smoke: { decision: PASS, source: qa-smoke-release-safety, artifact: smoke-log.txt }
  appsec:
    required: true | false
    handoff_target: appsec-security-orchestrator
    status: dispatched | not_dispatched | not_applicable | target_missing
    baseline_artifact: <path or null>
  residual_risks:
    - description: <known un-tested edge case>
      owner: <github handle>
      acceptance_reason: <why acceptable>
      tracking_issue: <ID>
  release_decision: PASS | FAIL | BLOCKED | CONDITIONAL_PASS | STRATEGY_READY
  blockers: []  # if BLOCKED, list each blocker with source skill
  preconditions: []  # if CONDITIONAL_PASS, list each precondition
  evidence_confidence:
    command_evidence: complete
    artifact_evidence: complete
    environment_confidence: high
    flaky_confidence: stable
  artifacts:
    paths: [...]
    total_size_kb: <N>
  generated_at: <ISO8601>
  signed_off_by: <human reviewer handle or null>
```

## 7. Parent Integration

- **Triggered by**：`enterprise-qa-testing` §6 Step 9 自动 dispatch
- **Returns**：`qa_evidence_bundle` YAML
- **Consumed by**：`gsd-ship` / `gsd-verify-work` / 人工 reviewer / release dashboard
- 本 skill 是 parent Output Contract Step 9 的实际生产者

## 8. Forbidden patterns

- 篡改 child skill 输出（必须忠实聚合）
- 在 BLOCKED 情况下输出 PASS
- 在 mode != execution 时输出 "可发布"
- 漏掉 critical release-path flaky 警报
- AppSec 未 dispatch 时 release_decision = PASS
- residual risk 无 owner / 无 tracking issue

## 9. References

- [ISTQB CTFL — exit criteria](https://glossary.istqb.org/en_US/term/exit-criteria/2)
- [ISO/IEC/IEEE 29119 — software testing standard](https://www.iso.org/standard/81291.html) (Part 1 concepts · Part 2 processes · **Part 3 test documentation** · Part 4 techniques · Part 5 keyword-driven)
- [ISO/IEC/IEEE 29119-3 — test documentation](https://standards.ieee.org/ieee/29119-3/7686/)
- Parent §11 Release Readiness Evidence (summary)

## 10. ISO/IEC/IEEE 29119-3 文档骨架对照（evidence bundle ⇄ 标准文档类型）

> ADDITIVE 文档增强，不改 §6 schema、不改 §5 decision 规则。把本 skill 输出的 `qa_evidence_bundle` 映射到 ISO/IEC/IEEE 29119-3 的标准测试文档类型，便于"按国际标准审计"时把我们的 evidence 对号入座。本骨架是**对照视角**，不是要求另写一套独立文档——我们的真相源始终是 `.qa/evidence/<tag>/` 下的机器可读 YAML。

| 29119-3 文档类型 | 标准定义（节选） | 在本体系里对应 | 备注 |
|---|---|---|---|
| **Test Policy** | 组织级测试方针 | parent `enterprise-qa-testing` §2 Hard Rules + §1 Mission | 组织层"测试是 DoD 一部分"的硬规则 |
| **Test Strategy / Organizational Test Plan** | 跨项目测试策略 | parent §3 Risk Model + §4 Layer Matrix + §5 Decision Tree | 风险驱动选层即 strategy |
| **Test Plan**（project / phase 级） | 本次测什么、用哪些层、范围、进度 | `qa_evidence_bundle.layers_required` + `layers_executed` + `layers_skipped` + parent §6 Step 1-3 | 选层 + scope + skip 证据 = test plan 实质 |
| **Test Design Specification** | 测试条件 → 测试用例设计 | `qa-test-design-tdd-bridge` §6 `scenario_matrix` + `techniques_applied`（§3.1 黑盒技术） | scenario 设计的可审计记录 |
| **Test Case Specification** | 具体用例（输入/预期/前置） | 各 layer child skill §6 输出里的 verified interactions / scenarios / test files | 散落在各层 evidence YAML |
| **Test Data / Environment Requirements** | 测试数据与环境需求 | `qa-test-data-environment` §6 `test_data_environment`（fixture/role/tenant/env） | parent §6 Step 4 产出 |
| **Test Execution Log / Test Results** | 执行记录与结果 | 各 layer child skill 的 `artifacts`（实际 stdout / playwright-report / junit / lhci） + parent §2 Hard Rule 1（无 stdout 不算 pass） | execution mode 下的真实 terminal evidence |
| **Test Incident / Defect Report** | 缺陷与异常报告 | `qa-flaky-governance` quarantine（8 字段 accountability）+ `blockers` + `dispatch-failures.log` | flaky / blocked / dispatch 失败 |
| **Test Completion / Summary Report** | 测试完成总结 + exit criteria 判定 | **本 skill 的 `qa_evidence_bundle` 本体** + `release_decision` + `residual_risks` + `signed_off_by` | 这是 29119-3 的 Test Completion Report 在本体系的落地物 |

**使用方式**：

- 这是**映射表，不是新增产物要求**——审计方问"你们的 Test Completion Report 在哪"，答"即 `.qa/evidence/<tag>/qa_evidence_bundle.yaml` 的 `release_decision` + `residual_risks` + `signed_off_by` 三段"。
- 29119-3 强调 **tailoring（裁剪）**：不是每个项目都要全 9 类文档齐备。Low risk 项目可能只有 Test Plan + Test Results + Completion Report；High/Critical 才需要完整链。裁剪依据仍是 parent §3 Risk Level，**不弱化任何 gate**。
- mode 影响：`plan-only` / `design-only` 模式下，Test Execution Log 类文档合法地标 `BLOCKED — <mode>`（parent §1.5），对应 bundle 输出 `CONDITIONAL_PASS` / `STRATEGY_READY` 而非伪装的"已执行"。
