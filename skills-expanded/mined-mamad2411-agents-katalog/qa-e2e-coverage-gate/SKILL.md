---
name: qa-e2e-coverage-gate
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
references_agents: [e2e-runner]
description: >-
  QA bridge skill - E2E coverage gate: prepares browser E2E scope (flows, risk, browsers, roles, tenants, data, cleanup, artifacts, retry and trace policy) and validates returned evidence. Execution belongs to the `e2e-runner` agent - never re-implements the Playwright runner.
---

# qa-e2e-coverage-gate

## 1. Position

E2E layer reference adapter / coverage gate. 本 skill **不**重新实现 Playwright runner，**不**替代 `e2e-runner` agent。本 skill 的工作：
- 把 parent 风险分析 + journey 信息**翻译成**对 `e2e-runner` 的 input
- **验收** `e2e-runner` 返回的 evidence（commands / stdout / report / trace / screenshot / video）
- 失败时分类（retry-pass → flaky / 真 fail → product bug / 配置 → infra）

## 2. Triggers

- Parent `enterprise-qa-testing` §6 Step 5/6（默认 dispatch）
- 任何 Critical user journey、auth flow、async RSC、role-permission 验证
- Floor Rule §3.6 抬升到 High 后 mandatory
- Release gate（merge full lane / release gate）

## 3. Responsibilities

- **Scope preparation**：flow_name / risk_level / browsers / roles / tenants / data / cleanup / artifacts
- **Selectors policy**：`getByRole` / `getByLabel` / `getByText` > `data-testid` > CSS path（最差）
- **Retry policy**：CI retries=2；retry pass 触发 `qa-flaky-governance` triage
- **Artifacts contract**：playwright-report + trace + screenshot-on-failure + video-on-failure + stdout
- **Acceptance criteria**：每条 spec 必须有真实命令、真实 stdout、覆盖 scope 内的所有 file/journey
- **Failure classification**：handoff 给 `qa-flaky-governance` 或上报 product bug

## 4. Non-responsibilities

- 不写 Playwright spec（由 `e2e-runner` 实施）
- 不配置 Playwright config（由项目 owner，本 skill 输出约束）
- 不重试 / 不 fix flaky（由 `qa-flaky-governance`）
- 不评测视觉回归（由 `qa-visual-regression`）

## 5. Workflow

1. **Pull from parent**：Step 3 选了哪个 journey、Step 4 test_data_environment、Step 2 risk_level
2. **Build input package** for `e2e-runner`（见 §6 schema）
3. **Dispatch recommendation**（由调用方执行 Task）
4. **Receive evidence** from `e2e-runner`
5. **Validate**：commands actually ran? stdout present? report path valid? trace on failure? retry-pass classified?
6. **Output `e2e_coverage_gate` YAML**

## 6. Output Contract

```yaml
e2e_coverage_gate:
  reference_agent: e2e-runner
  e2e_runner_reference_input:
    flow_name: <e.g. checkout-happy-path>
    risk_level: high | critical
    route_class: marketing | dashboard | admin
    browsers: [chromium]  # default; firefox/webkit only if cross-browser risk
    roles: [owner, admin, member, viewer]
    tenants: [tenant-A, tenant-B]
    test_data_ref: qa-test-data-environment output
    setup_steps: [...]
    cleanup_steps: [...]
    selectors_policy:
      prefer: user_visible_locators  # getByRole / getByLabel / getByText
      avoid: brittle_css_selectors
      data_testid_allowed: as_fallback_only
    artifacts_required:
      - html_report
      - trace_on_failure
      - screenshot_on_failure
      - video_on_failure
      - stdout
    retry_policy:
      retries_in_ci: 2
      retries_local: 0
      retry_pass_classified_as_flaky: true
  validation_of_returned_evidence:
    commands_actually_ran: true | false
    stdout_present: true | false
    report_path: <playwright-report/>
    trace_on_failure_present: true | false
    scope_coverage: full | partial | missing
    retry_pass_count: <N>
    retry_pass_flaky_handoff: pending | dispatched
    hard_rule_violations: []  # e.g. waitForTimeout used / internal mock
  failure_classification:
    real_product_bugs: []
    flaky_candidates: []  # handed off to qa-flaky-governance
    infra_issues: []
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 7. Parent Integration

- **Triggered by**：parent §6 Step 5/6
- **Returns**：`e2e_coverage_gate` YAML
- **Consumed by**：`qa-evidence-bundle` → `child_skill_results.e2e`
- 与 `qa-test-data-environment`（输入）+ `qa-flaky-governance`（输出）协作

## 8. Forbidden patterns

- 让 `e2e-runner` 自由发挥而不传 scope 约束
- 接受无 stdout 的"已完成"声明
- 把 retry-pass 算 stable pass
- 用 `data-testid` 而不优先 user-visible locator
- 用 `waitForTimeout(...)` 硬睡
- 跳过 trace 采集

## 9. References

- [Playwright — best practices (locators)](https://playwright.dev/docs/best-practices)
- [Playwright — retries](https://playwright.dev/docs/test-retries)
- [Playwright — trace viewer](https://playwright.dev/docs/trace-viewer-intro)
- [Playwright — projects (browser matrix)](https://playwright.dev/docs/test-projects)
