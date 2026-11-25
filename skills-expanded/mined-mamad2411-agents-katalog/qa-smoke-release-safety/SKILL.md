---
name: qa-smoke-release-safety
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
description: >-
  QA child skill - release / canary / production smoke safety: read-only or explicitly reversible synthetic actions only, health checks, smoke routes, rollback trigger, observability check, known-issue acknowledgement. Destructive production tests are forbidden without explicit authorization + synthetic account + rollback. Owns parent Smoke layer.
---

# qa-smoke-release-safety

## 1. Position

Release / canary / production smoke 安全执行 skill。是 release lane 最后一道闸门。**production smoke 只允许 read-only 或显式可回滚 synthetic 操作**，禁止真实扣款 / 真实邮件 / 真实客户数据修改 / 真实权限变更。

## 2. Triggers

- Parent §6 Step 5（每次 deploy 都要触发）
- Release candidate / staging sign-off / production deploy
- Canary promotion
- Rollback validation
- Post-deploy verification（5/15/30 min smoke）

## 3. Responsibilities

- **Read-only smoke**：health check / 列表查询 / dashboard render
- **Synthetic account-based 操作**：用 dedicated synthetic account 跑可回滚的写操作（如果业务必要）
- **Health checks**：`/health` / `/ready` / `/live`
- **Critical route smoke**：sign-in / dashboard / checkout submit（synthetic）
- **Rollback plan verified**：rollback 脚本是否已测试 / RTO 是否达标
- **Observability verified**：log / metric / trace / alert 都正常 emit
- **Known-issue acknowledgement**：列出已知 release-time 问题 + owner sign-off

## 4. Non-responsibilities

- 不做长时间压测（→ `qa-performance-reliability`）
- 不做安全 active validation（→ `authorized-pentest-validation`）
- 不替代 SLO 监控（属于 SRE / on-call）
- 不允许在 production 跑破坏性测试

## 5. Workflow

1. 识别 environment（staging / canary / production）
2. 列 critical smoke routes（每条标 read-only / synthetic-write / forbidden）
3. 准备 synthetic accounts（不能用真实用户）
4. 跑 smoke suite（`playwright test --grep @smoke`）
5. 验 health endpoints
6. 验 rollback path（dry run）
7. 验 observability（log/metric/alert 正常）
8. Collect known issues + owner ack
9. Output `release_smoke` YAML

## 6. Output Contract

```yaml
release_smoke:
  environment: staging | canary | production
  destructive_actions: false  # MUST be false in production
  synthetic_accounts:
    - account_id: <id>
      role: <role>
      isolation: dedicated_test_namespace | feature_flag_gated
  smoke_routes:
    - route: /
      type: read_only
      passed: true
    - route: /sign-in
      type: synthetic_write
      passed: true
      cleanup_verified: true
    - route: /checkout
      type: synthetic_write_with_stripe_test_mode
      passed: true
      cleanup_verified: true
  health_checks:
    - endpoint: /health
      passed: true
      latency_ms: <N>
    - endpoint: /ready
      passed: true
  rollback_plan_verified:
    rollback_script_path: <path>
    dry_run_tested: true
    rto_target_seconds: 60
    rto_observed_seconds: <N>
  observability:
    logs_emit_verified: true
    metrics_emit_verified: true
    traces_emit_verified: true
    alerts_test_fired: true
  known_issues_acknowledged:
    - description: ...
      owner: <github handle>
      severity: low | medium
      acceptance_reason: ...
  artifact_path: <smoke-report.json or html>
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 7. Parent Integration

- Triggered by: parent §6 Step 5（release lane 必触发）
- Returns: `release_smoke` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.smoke`

## 8. Forbidden patterns

- production 跑破坏性测试（destructive_actions = true 在 production 必须 BLOCKED）
- 用真实用户账号跑 smoke
- 发真实邮件 / SMS / push
- 真实扣款（必须用 Stripe test mode keys）
- 修改真实客户数据
- 跳过 rollback dry-run
- 接受 observability 不正常（log/metric/alert 异常必须 BLOCKED）
- log / artifact 包含 PII

## 9. References

- [Google SRE — release reliability](https://sre.google/sre-book/release-engineering/)
- [Canary releases — Martin Fowler](https://martinfowler.com/bliki/CanaryRelease.html)
- Parent §11 Release Readiness Evidence
- Parent §6 Step 5/9 — smoke dispatch + readiness decision
