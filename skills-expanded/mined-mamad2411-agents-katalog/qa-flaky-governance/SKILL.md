---
name: qa-flaky-governance
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
description: >-
  QA child skill - flaky test detection, 8-category classification, and accountable quarantine (owner + issue + expiry + repro + last_seen + unblock_condition) with cleanup cadence. Also runs standalone for oncall or periodic flaky review. Owns parent section 9 + section 6 Step 8.
---

# qa-flaky-governance

## 1. Position

Flaky test 检测、分类、隔离、清理治理 skill。"不治理 flaky，测试越多越不可信"是工业级 QA 的红线。本 skill 把 flaky 从"待处理事项"变成"可审计治理流程"。

## 2. Triggers

- Parent `enterprise-qa-testing` §6 Step 8（默认 dispatch — Step 7 出现 retry-pass 或非确定性 fail 时）
- 独立触发：oncall 工程师发现 CI 不稳定
- 独立触发：项目维护 / quarterly flaky review
- 独立触发：release gate 出现可疑的 retry pass
- 独立触发：开发者怀疑某个 test flaky 想确认

## 3. Responsibilities

- **Detection**：
  - first-run fail / retry pass → flaky 候选
  - CI-only fail / non-deterministic fail / order-dependent fail → flaky 候选
  - 记录 retry 次数、首次失败错误、retry 后通过结果、trace / report 路径
- **Diagnosis**：Playwright `repeatEach` 用于诊断（不用于 CI gate）
- **Classification**（8 类）：见 §5 Workflow
- **Quarantine accountability**：owner / issue / expiry / reproduction / last_seen / unblock_condition 全字段
- **Critical release-path 保护**：不允许静默 quarantine
- **Cleanup cadence**：固定周期 review quarantine 列表，过期升级为 release readiness 风险

## 4. Non-responsibilities

- 不修测试代码（属于原作者 / `tdd-guide` / `e2e-runner`）
- 不调测试 framework 配置（属于各 layer child skill）
- 不替代 root-cause debug（属于 `gsd-debug` / 开发者）
- 不允许通过加 retry 解决 flaky（必须分类 + 治理）

## 5. Workflow

1. **Collect signals**：
   - 从 CI 历史拉取 retry pass 列表
   - 从 Playwright report 找 trace（CI failure 必有）
   - 从 Vitest junit / json 找 non-deterministic 测试
2. **Classify**（8 类，必须分类才能 quarantine）：
   - **C1: Selector / locator instability** — DOM query 漂移
   - **C2: Async / timing / race condition** — 等待不充分
   - **C3: Network / third-party dependency** — 外部服务波动
   - **C4: Test data pollution** — fixture 共享 / cleanup 不全
   - **C5: Environment / resource contention** — 端口 / 内存 / 文件锁
   - **C6: Browser / rendering / screenshot variance** — 跨平台 / 字体 / 动画
   - **C7: Order dependence** — 隐式状态依赖
   - **C8: Product nondeterminism**（**最危险，必须修，不许 quarantine**） — 真实产品 bug 表现为偶发
3. **Reproduction attempt**：
   - Playwright `repeatEach: 10` 跑该 test
   - 记录 fail 率（应大于 5% 才是真 flaky）
4. **Decide quarantine**：
   - Critical release-path 测试 → **禁止 quarantine**，升级为 release blocker
   - Non-critical + 有冗余覆盖 → 可 quarantine，但必须挂账
5. **Generate quarantine record**（必填字段，见 §6）
6. **Schedule cleanup**：
   - expiry ≤ 14 天（Critical-adjacent）/ ≤ 30 天（其他）
   - 过期未修必须升级
7. **Output `flaky_governance` YAML**

## 6. Output Contract

```yaml
flaky_governance:
  scan_period: "last 7 days CI"
  candidates_detected: <N>
  classified:
    - test_name: <e2e/checkout.spec.ts:42 — buy now happy path>
      failure_class: C2_async_timing | C1_selector | ...
      first_seen: 2026-05-20T...
      last_seen: 2026-05-23T...
      fail_rate: 0.12  # 12% fail in repeatEach
      trace_path: playwright-report/trace-...zip
      suspected_cause: "checkout iframe load race with assertion"
      is_critical_release_path: true | false
  quarantine_decisions:
    - test_name: ...
      action: quarantine | escalate_to_release_blocker | fix_immediately | no_action
      quarantine_record:  # only when action=quarantine
        owner: <github handle>
        issue_id: ISSUE-1234
        expiry_date: 2026-06-07
        reproduction_command: "npx playwright test --grep 'buy now happy path' --repeat-each 10"
        unblock_condition: "iframe load wait replaced with deterministic event listener"
  cleanup_review:
    overdue_quarantines: []
    upcoming_expiries: []
    release_readiness_risks: []
  decision: PASS | FAIL | BLOCKED
  blockers: []  # Critical release-path tests that can't be quarantined
```

## 7. Parent Integration

- **Triggered by**：`enterprise-qa-testing` §6 Step 8 自动 dispatch；或独立触发
- **Returns**：`flaky_governance` YAML
- **Consumed by**：`qa-evidence-bundle` §6 child_skill_results.flaky
- **Validated by**：parent §6 Step 7 evidence_validation
- **Escalation path**：当存在 critical release-path flaky test 时，parent §6 Step 9 必须输出 BLOCKED，不许放行

## 8. Forbidden patterns

- 通过加 retry 解决 flaky（修根因，不掩盖）
- 静默 quarantine（必须挂账）
- Critical release-path 测试 quarantine（必须修或阻塞 release）
- pass-on-retry 视为 stable pass
- C8 product nondeterminism 当作 flaky 处理（这是真 bug）
- 删除 flaky test 而非 quarantine

## 9. References

- [Playwright — retries](https://playwright.dev/docs/test-retries)
- [Playwright — trace viewer](https://playwright.dev/docs/trace-viewer-intro)
- [Playwright — repeatEach for flaky diagnosis](https://playwright.dev/docs/api/class-testconfig#test-config-repeat-each)
- [Google Testing Blog — Avoiding Flakey Tests](https://testing.googleblog.com/2008/04/tott-avoiding-flakey-tests.html)
