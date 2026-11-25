---
name: qa-performance-reliability
version: 1.0.0
status: stable
created_date: 2026-05-24
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
description: >-
  QA child skill - performance and reliability: Lighthouse CI budgets, bundle and resource budgets, k6 API load smoke, route-class-aware budgets, cold/warm paths, p50/p95/p99 with variance control, threshold-weakening detection, regression comparison. Owns parent section 4 Layer 9.
---

# qa-performance-reliability

## 1. Position

性能 + 可靠性 skill。**不只是 Lighthouse 分数** —— 包括 bundle/resource budget、k6 load smoke、route-class budget、p50/p95/p99 分位、cold/warm path 区分、variance 控制、threshold weakening 检测。

**Core Web Vitals 阈值锁定（canonical floor）**：`LCP < 2.5s` / `INP < 200ms` / `CLS < 0.1`（Google "good" 边界）。**INP（Interaction to Next Paint）已于 2024-03-12 取代 FID（First Input Delay）成为 Core Web Vital**；本 skill 与所有下游 schema/gate 不再使用 FID。这三项是 commercial-cert workflow 的 hard gate floor，已**双写**进 `PERF_AUDIT_SCHEMA` + `perf_gate_policy`（见 §6.5）。

## 2. Triggers

- Parent §6 Step 5（性能敏感变更）
- Route / page / API 性能敏感
- Bundle size 变更（新依赖 / 升级）
- Dashboard / search / upload / checkout / report generation
- 大数据量渲染
- Release gate
- Latency / throughput / SLO 相关变更

## 3. Responsibilities

- **Lighthouse CI**（lhci）：LCP / INP / CLS / FCP / TBT / SI
- **Bundle/resource budget**：JS gzipped / CSS / image / font
- **k6 API/load smoke**：p50 / p95 / p99 latency + RPS + error rate
- **Route-class-aware budgets**（来自 parent §11 / §6 Step 9）：
  - Marketing：LCP<2.0s / INP<150ms / CLS<0.1
  - Dashboard：LCP<2.5s / INP<200ms / CLS<0.1
  - Internal admin：LCP<3.5s / INP<300ms / CLS<0.1
- **Cold/warm path 区分**：首次加载 vs cache 命中
- **Variance 控制**：多次运行（≥5），固定 CI 环境
- **Threshold weakening 检测**：lighthouserc.json / k6 thresholds 历史 vs 当前
- **Regression comparison**：vs main branch baseline

## 4. Non-responsibilities

- 不做生产级长时间压测（属于专用 SRE / load testing team）
- 不调整生产 SLO（业务决定）
- 不替代 APM（Datadog / New Relic）实时监控

## 5. Workflow

1. 识别 route_class（marketing / dashboard / admin）
2. 选 budget 档（按 §6 / §11 mapping）
3. 跑 `lhci autorun` × 5 + 记录 variance
4. 跑 `k6 run` smoke（API 路径）
5. Bundle analyzer report（webpack-bundle-analyzer / @next/bundle-analyzer）
6. Compare vs baseline，检测 regression
7. 检测 threshold weakening
8. Output `performance_reliability` YAML

## 6. Output Contract

```yaml
performance_reliability:
  route_class: marketing | dashboard | admin
  budgets:
    lcp_ms: 2500
    inp_ms: 200
    cls: 0.1
    bundle_js_gz_kb: 200
    bundle_css_gz_kb: 30
    api_p95_ms: 500
    api_p99_ms: 1000
    api_error_rate: 0.001
  lighthouse:
    artifact: lighthouse-report.html
    runs: 5
    median:
      lcp_ms: <N>
      inp_ms: <N>
      cls: <N>
    variance: <stddev>
  bundle_analysis:
    js_gz_kb: <N>
    css_gz_kb: <N>
    biggest_chunks: [...]
    regression_vs_baseline_kb: <delta>
  k6_smoke:
    artifact: k6-summary.json
    p50_ms: <N>
    p95_ms: <N>
    p99_ms: <N>
    error_rate: <N>
    rps: <N>
  cold_warm_path:
    cold_lcp_ms: <N>
    warm_lcp_ms: <N>
  samples: 5
  variance_acceptable: true | false
  regressions:
    - metric: <e.g. LCP>
      baseline: <N>
      current: <N>
      delta_pct: <N>
  threshold_changed: false  # detected by git log on lighthouserc.json / k6 config
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 6.5 Hard threshold (DOUBLE-WRITE — workflow mode 才会拦)

> 在 prompt-only 模式下本 skill 给 advisory decision；在 **workflow-spec 模式（commercial-cert）** 下，拦截由 deterministic `perf_gate_policy` op 完成。要让它真的拦，CWV 阈值必须**双写**：同步进 `PERF_AUDIT_SCHEMA` 与 `perf_gate_policy` 的 floor。**特别注意**：`perf_gate_policy` 对任何未设置的 floor 字段默认 `Infinity`（永不拦）——所以 floor 不填 = 静默不拦。baked default 已补，闭掉此洞。

**Canonical CWV floor（已双写，2026-06-05）**：

| metric | floor | 超出后果 | gate 读取字段 |
|---|---|---|---|
| LCP | **< 2500 ms** | **BLOCK**（CWV core）| `ctx.policy.perf_floor.max_lcp_ms` |
| INP | **< 200 ms**（取代 FID）| **BLOCK**（CWV core）| `ctx.policy.perf_floor.max_inp_ms` |
| CLS | **< 0.1** | **WARN** | `ctx.policy.perf_floor.max_cls` |
| TBT | **< 200 ms** | **WARN** | `ctx.policy.perf_floor.max_tbt_ms` |
| bundle size | per-project（不全局 baked）| WARN（设了才拦）| `ctx.policy.perf_floor.max_bundle_size_bytes` |

**双写位置（三处一致，字段名与 `qa-orchestrator.js` `perf_gate_policy` 读取处逐字对齐）**：
1. Schema：`~/.claude/orchestrator-runtime/qa/schemas/PERF_AUDIT_SCHEMA.v1.json` → `_canonical_threshold_policy`
2. Gate policy（baked default）：`~/.claude/orchestrator-runtime/qa/presets/commercial-cert.json` → `context.policy.perf_floor`
3. Runtime：parent `enterprise-qa-testing` §18.5 step 13 把 `policy` 透传进 `Workflow` 的 `input.context.policy`（engine 在 `qa-orchestrator.js` 第 47 行读 runtime `input.context.policy`，非 preset 静态块）。

**与 §3 route-class budgets 的关系**：route-class budget（Marketing `LCP<2.0s` 等）是把 floor **向下收紧**用于 advisory 评估，**绝不放宽到** floor 之上。global hard floor（本节）是 workflow gate 的拦截线；route-class budget 是更严的 advisory 目标。两者不冲突——project 可在 `ctx.policy.perf_floor` 里基于 route_class 进一步调严（如 Marketing 设 `max_lcp_ms: 2000`），但不得高于 canonical floor。

> decision 语义：`lcp_ms` 或 `inp_ms` 超阈 => **BLOCK**；`cls`/`tbt_ms`/`bundle_size_bytes` 超阈 => **WARN**；全过 => **PASS**。

## 7. Parent Integration

- Triggered by: parent §6 Step 5
- Returns: `performance_reliability` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.performance`

## 8. Forbidden patterns

- 单次 lhci run 就判定（必须 ≥5 次取 median）
- 为 pass 调高 budget（threshold weakening）
- 跳过 cold path（生产用户多数是 cold）
- 跳过 bundle analyzer（依赖膨胀是无声 regression）
- variance 过大不调查（CI 环境不稳）
- 把 CWV 阈值只写进 schema 不写进 `perf_gate_policy`（或反之）→ floor 缺失默认 Infinity，workflow 模式静默不拦（见 §6.5 双写）
- 残留 FID（已被 INP 取代，2024-03-12）：任何 FID 字段/阈值都应迁移为 INP

## 9. References

- [Lighthouse CI](https://googlechrome.github.io/lighthouse-ci/)
- [k6 — load testing](https://grafana.com/docs/k6/latest/)
- [MDN — performance budgets](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Performance_budgets)
- [web.dev — Core Web Vitals](https://web.dev/articles/vitals)
- Parent §11 route-class budget table
