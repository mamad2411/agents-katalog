---
name: qa-integration-service-virtualization
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
description: >-
  QA child skill - integration layer with service virtualization: DB, cache, queue, API client and third-party boundaries via MSW / Testcontainers / Docker Compose, covering idempotency, retry, timeout, network error and partial failure. Real dependency preferred over in-memory mock at Medium+ risk. Owns parent section 4 Layer 4.
---

# qa-integration-service-virtualization

## 1. Position

Integration-layer 测试 skill。验证跨模块状态 + 真实/虚拟化服务边界，单元测试不足以证明行为时使用。

## 2. Triggers

- Parent §6 Step 5（默认 dispatch）
- DB / ORM / repository 变更
- API client / fetch wrapper 变更
- Message queue / event publisher / consumer 变更
- Cache layer / Redis 变更
- Third-party API 调用
- 单元测试无法覆盖的 cross-service 行为

## 3. Responsibilities

- **Tool selection**：
  - MSW（msw/node）—— HTTP 边界 mock
  - Testcontainers —— Docker 容器化的真实依赖（推荐 Medium+ risk）
  - Docker Compose —— 完整 service stack
  - Local fake service —— 最后选择
- **High-risk path 偏好真依赖**：Medium+ 优先 Testcontainers / Compose；in-memory mock 仅 Low risk
- **覆盖**：
  - happy path
  - **idempotency**：重复调用结果一致
  - **retry**：重试逻辑 + 退避
  - **timeout**：超时行为
  - **network error**：连接拒绝 / DNS 失败
  - **partial failure**：部分依赖 down
  - **transaction rollback**：跨多步 DB 操作的回滚
- **数据库**：transaction rollback / cleanup hook / namespace-per-worker

## 4. Non-responsibilities

- 不跑浏览器（→ `qa-e2e-coverage-gate`）
- 不写 contract（→ `qa-contract-api`）
- 不替代单元测试（→ `qa-test-design-tdd-bridge`）

## 5. Workflow

1. 识别 dependency type（db / cache / queue / http_api / third_party）
2. 按 risk 选 virtualization tool
3. 设计 test environment（real_dependency: yes/no, tool）
4. 设计 data setup + cleanup
5. 列 failure modes 覆盖矩阵
6. 跑 `vitest run __tests__/integration` 或自定义
7. Output `integration_strategy` YAML

## 6. Output Contract

```yaml
integration_strategy:
  dependency_type: db | cache | queue | http_api | third_party | mixed
  test_environment:
    real_dependency: true | false
    virtualization_tool: msw | testcontainers | docker_compose | local_fake | none
    rationale: <why this tool>
  data_setup:
    method: factory | seeded_db | fixture
    isolation: namespace_per_worker | transaction_rollback | disposable_container
  cleanup_strategy: transaction_rollback | teardown_hook | container_dispose | namespace_delete
  failure_modes_covered:
    happy_path: true
    idempotency: true
    retry: true
    timeout: true
    network_error: true
    partial_failure: true
    transaction_rollback: true
  commands_run:
    - command: npx vitest run __tests__/integration --reporter=verbose
      exit_code: 0
      stdout_excerpt: ...
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 7. Parent Integration

- Triggered by: parent §6 Step 5
- Returns: `integration_strategy` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.integration`

## 8. Forbidden patterns

- Medium+ risk 用 in-memory mock 代替真依赖
- 跳过 negative failure modes
- 共享 mutable DB state 跨 worker
- cleanup 不验证（必须断言 teardown 后 state empty）

## 9. References

- [MSW — Mock Service Worker](https://mswjs.io/)
- [Testcontainers](https://testcontainers.com/getting-started/)
- [Docker Compose](https://docs.docker.com/compose/)
