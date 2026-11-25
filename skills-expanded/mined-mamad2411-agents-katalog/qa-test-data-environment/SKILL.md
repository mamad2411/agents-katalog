---
name: qa-test-data-environment
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
description: >-
  QA child skill - test data, environments, fixtures, factories, role matrix, tenant matrix, time control, PII policy, environment parity. Required at Medium+ risk with extra rules at High/Critical; also runs standalone when a developer just needs a fixture or role matrix. Owns parent section 6 Step 4.
---

# qa-test-data-environment

## 1. Position

Test data + environment strategy 中心 skill。所有 test layer 共享的 fixture / role / tenant / time / env 配置由本 skill 输出。其他 QA child skill（component / integration / contract / e2e / a11y / perf）消费本 skill 输出。

## 2. Triggers

- Parent `enterprise-qa-testing` §6 Step 4（默认 dispatch）
- 独立触发：开发者单写一个 endpoint test 需要 fixture 模板，不走完整 QA review
- 独立触发：项目升级 multi-tenant，需要 role/tenant matrix
- 独立触发：`qa-flaky-governance` 排查发现 flaky 由数据污染引起，handback 给本 skill 重做 isolation
- 独立触发：Medium+ risk feature 启动前的 test data plan

## 3. Responsibilities

- **Fixture strategy**：factory / static fixture / seeded DB / mocked API / generated account
- **Cleanup strategy**：transaction rollback / teardown hook / unique namespace / disposable tenant / idempotent delete
- **Time control**：fake timers / frozen clock / injected date provider / 真实时间 + 容差
- **Auth strategy**：test users + role matrix + permission matrix
- **Tenant matrix**（multi-tenant 系统必填）：own allow / other deny / role downgrade deny / stale session
- **Environment target**：local / preview / staging / production-readonly
- **PII / secrets / production data 禁止规则**
- **Synthetic data**：Faker.js / fishery 配合 + 防止误打真实 email/phone/payment
- **Clock / timezone / currency / locale 固定**：避免 CI vs local 差异引起 flaky

## 4. Non-responsibilities

- 不写测试代码（属于各 layer child skill）
- 不执行 cleanup runtime（属于实际测试 framework / CI hooks）
- 不管 production smoke 安全（属于 `qa-smoke-release-safety`）
- 不做 schema migration（属于应用代码 / DB migration tool）

## 5. Workflow

1. **Risk-driven matrix scale**：根据 parent Step 2 risk level 决定 role/tenant matrix 规模（Low: 1-2 角色；Medium: 全角色；High/Critical: 全角色 × 全租户 + 边界）
2. **Fixture source 选型**：factory（默认）/ static（CRUD-only）/ seeded DB（complex relations）/ mocked API（third-party 边界）
3. **Cleanup contract**：每个 fixture 必须有对应 cleanup；优先 transaction rollback；E2E 用 namespace-per-worker
4. **Auth / Tenant matrix 矩阵**：列出 N 角色 × M 租户组合，标记必测 / 可选 / 禁测
5. **Time / locale 固定**：给出 `vi.useFakeTimers()` / `Intl.DateTimeFormat` lock；Playwright 用 `page.clock` API
6. **PII policy 校验**：扫描 fixture 数据，确保无真实 email/phone/payment patterns（regex 检查）
7. **Environment 标定**：标 base_url + 依赖服务 + secrets 可用性 + 缺失项
8. **Output `test_data_environment` YAML**（见 §6）

## 6. Output Contract

```yaml
test_data_environment:
  data_strategy: fixture | factory | seed | snapshot | synthetic
  factory_tool: faker | fishery | factory-bot | custom | none
  roles:
    - name: owner
      seed_method: direct_session_injection | oauth_test_provider | jwt_inject
      count_required: 1
    - name: admin
      seed_method: ...
      count_required: 1
    - name: member
      seed_method: ...
      count_required: 1
    - name: viewer
      seed_method: ...
      count_required: 1
  tenants:
    - name: tenant-A
      isolation: namespace_per_worker | dedicated_db | shared_with_prefix
    - name: tenant-B
      isolation: ...
  permission_matrix:  # required when multi-tenant
    own_tenant_allow: [list of test cases]
    other_tenant_deny: [list]
    role_downgrade_deny: [list]
    stale_session_behavior: [list]
  cleanup:
    strategy: transaction_rollback | teardown_hook | namespace_delete | idempotent_delete
    cleanup_verified: true | false
    leak_detection_enabled: true | false
  time_control:
    method: fake_timers | frozen_clock | injected_provider | real_with_tolerance
    locked_time: "2026-05-24T00:00:00Z"
    locale: en-US
    timezone: UTC
    currency: USD
  isolation:
    worker_scoped_namespace: true | false
    order_independent: true | false
    parallel_safe: true | false
  pii_policy:
    production_data_used: false
    real_email_blocked: true
    real_phone_blocked: true
    real_payment_blocked: true
    pii_regex_scan_passed: true
  environment:
    target: local | preview | staging | production-readonly
    base_url: ...
    services_required: [postgres, redis, ...]
    services_available: [...]
    secrets_required: [DATABASE_URL, ...]
    secrets_available: [...]
    secrets_missing: [...]
  decision: READY | BLOCKED
  blockers: []
```

## 7. Parent Integration

- **Triggered by**：`enterprise-qa-testing` §6 Step 4
- **Returns**：`test_data_environment` YAML
- **Consumed by**：每个 test layer child skill（`qa-component-behavior` / `qa-integration-service-virtualization` / `qa-contract-api` / `qa-e2e-coverage-gate` / `qa-visual-regression` / `qa-a11y-compliance` / `qa-performance-reliability` / `qa-smoke-release-safety`）
- **Validated by**：parent §6 Step 7 evidence_validation
- 若 decision = BLOCKED，parent §6 Step 7 evidence_validation 不可能 PASS，必须修复后重试

## 8. Forbidden patterns

- 共享 mutable test account 跨 worker（必须 namespace 隔离，否则 race）
- 真实 PII / production data 进入测试
- order-dependent tests（每个测试必须能独立跑）
- 依赖手工预置状态而不在 fixture 中文档化
- production 环境写入测试数据（read-only 例外见 `qa-smoke-release-safety`）
- 硬编码时间 / locale / timezone（必须用 fake timers 或 lock）

## 9. References

- [Faker.js — fake data generation](https://fakerjs.dev/guide/)
- [Vitest — fake timers / mocking](https://vitest.dev/guide/mocking.html#timers)
- [Playwright — storageState for auth fixture](https://playwright.dev/docs/auth)
- [Playwright — page.clock API](https://playwright.dev/docs/clock)
- [Testcontainers — disposable dependencies](https://testcontainers.com/getting-started/)
