---
name: qa-load-stress-reliability
version: 1.0.0
status: stable
created_date: 2026-06-15
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
references_agents: [qa-load-stress-runner]
description: >-
  QA child skill - load / stress / soak / spike plus capacity and reliability SLO: k6 open-model `ramping-arrival-rate` (drives REQUEST RATE, not VU count) for breakpoint and capacity-ceiling discovery, asserting p95/p99, error rate and throughput. STAGING / LAB / PREVIEW ONLY - never production (parent Hard Rule 2.6). Owns parent Load/Reliability layer.
---

# qa-load-stress-reliability

## 1. Position

后端容量 + 可靠性压测 skill。**不是** `qa-performance-reliability` 的 Lighthouse / CWV 前端预算（那是单次页面性能），也**不是**它内置的 `k6 API smoke`（轻量冒烟 — 一两个并发摸一下接口）。本 skill 专做**持续负载 / 应力 / 浸泡 / 峰值**，回答的是"这服务能扛多少 RPS、断点在哪、长时间跑会不会漏内存 / 退化"。

`qa-performance-reliability` §4 明确自声明："不做生产级长时间压测（属于专用 SRE / load testing team）"——本 skill 正是补上这块能力（仍非生产：限 staging / lab / preview）。

**铁律：限 staging / lab / preview，绝不打生产。** 对生产只读 smoke 是 `qa-smoke-release-safety` 的事；压测会制造高负载、可能触发 autoscaling 计费、可能拖垮真实用户——生产环境一律拒。

## 2. Triggers

- Parent §6 Step 5（risk 选了 Load/Reliability layer — 通常 backend capacity / release-blocking journey / high-throughput API 变更）
- 后端 API / service 上线前的容量验证（"这次发布能扛住吗"）
- 新增 / 改动高吞吐路径（搜索、列表分页、批量导出、webhook 接收端、消息消费者）
- 架构变更影响容量（加缓存、换 DB、改连接池、引入队列）
- 容量规划 / 找断点 RPS（breakpoint）/ SLO 回归（p95/p99 是否较 baseline 退化）
- 独立触发：SRE / oncall 做 capacity review

## 3. Responsibilities

- **4 + 1 种 profile**（k6 官方 test-type 心智）：
  - **smoke**（≠ 前端 smoke）：1-5 VU 极低负载，验证脚本本身能跑通、SLO 阈值合理（不是测系统）
  - **load**（average load）：稳定到目标 RPS，验证常规负载下 SLO 达标
  - **stress**：逐步加压超过常规峰值，看系统在高压下是否仍正确 / 优雅降级
  - **soak**（endurance / 浸泡）：中等负载**长时间**跑（≥30min–数小时），抓内存泄漏 / 连接耗尽 / 性能随时间退化
  - **spike**：瞬间拉到极高负载再骤降，验证突发流量（促销、热点）下的弹性与恢复
- **Open model 优先（k6 `ramping-arrival-rate`）**：驱动 **到达 RATE（iterations/s ≈ RPS）** 而非 VU 数。这是 k6 官方做 **breakpoint / 容量上限**的推荐方式——闭模型（`ramping-vus`）会因系统变慢而自动降速、掩盖真实断点；开模型保持施压速率，能真正逼出系统拐点。
- **Breakpoint 发现**：用 `ramping-arrival-rate` 逐级抬升 target RPS，直到 SLO 破裂（error rate 飙升 / p99 越界），记录**断点 RPS** + **容量裕度**（断点 vs 预期峰值的倍数）。
- **Reliability SLO 断言**（k6 `thresholds`，break-on-fail）：
  - `http_req_duration`：p95 / p99 上限
  - `http_req_failed`：error rate 上限（如 `rate<0.01`）
  - `http_reqs` / `iterations`：达成的吞吐（RPS）
  - `checks`：功能正确性断言通过率（高负载下不能只快不对）
- **容量裕度断言**：断点 RPS ≥ 预期峰值 × 安全系数（默认 ≥ 2×，可配）。
- **环境隔离校验**：执行前**必须**确认 target 是 staging/lab/preview（见 §5 Step 1 + §8 Forbidden）。

### 3.1 k6 实务要点（开模型 / executor / thresholds）

- **Executor 选型**：
  - `ramping-arrival-rate`（**开模型，本 skill 默认**）：按时间段 ramp 目标 `rate`（每 `timeUnit` 启动的 iteration 数）；需设 `preAllocatedVUs` + `maxVUs`（VU 是用来满足 rate 的资源池，不是负载目标）。做 load / stress / spike / breakpoint 都用它。
  - `constant-arrival-rate`：恒定 RPS，做 soak（长时间稳定到达率）。
  - `ramping-vus` / `constant-vus`（闭模型）：仅当你刻意要模拟"固定并发用户数"语义时用；**不要**用它找断点（会自降速掩盖拐点）。
- **`scenarios` 多场景**：一个 k6 脚本可并行多个 scenario（如 read-heavy + write-heavy 混合），各自 executor。
- **`thresholds` = pass/fail gate**：`thresholds` 不满足 → k6 进程 `exit code 99`（结合 `--fail-on-threshold`/默认行为），runner 据此判 FAIL。这是 SLO 断言的硬挂钩。
- **`summaryTrendStats`**：显式要 `["avg","p(95)","p(99)","max"]`，确保 p99 被输出。
- **结果产物**：`k6 run --summary-export=k6-summary.json`（机器可读）+ stdout（人读）。runner 把这俩当 evidence artifact。
- **分布式 / 大规模**：单机 k6 受限于本机资源；超大规模用 `k6 run` 多 load generator 或 k6 Cloud（**留档命令即可，本 skill 不要求云**）。

## 4. Non-responsibilities

- **不打生产**（Hard Rule §2.6）——生产只读 smoke 走 `qa-smoke-release-safety`
- 不做前端单页性能 / Lighthouse / CWV / bundle budget（→ `qa-performance-reliability`）
- 不做 chaos / fault-injection（断网、注延迟、kill 容器 → Wave B `qa-resilience-fault-injection`，planning-first 双门）
- 不调整生产 SLO 数值（业务 / SRE 决定；本 skill 只验证是否达标）
- 不替代 APM 实时监控（Datadog / New Relic / Grafana）

## 5. Workflow

1. **环境隔离校验（GATE，最先做）**：确认 target URL / host 是 staging / lab / preview / localhost。命中生产域名特征（prod / www 顶级生产域 / 已知生产 host）或无法证明非生产 → **BLOCKED**，不跑。要求调用方显式提供 staging target + 书面确认非生产。
2. 识别压测目标（API endpoint 列表 / 关键 user journey 的后端调用 / 消息消费路径）
3. 选 profile（按 trigger：上线前→load+stress；长期稳定性→soak；突发流量→spike；找上限→breakpoint via ramping-arrival-rate）
4. 设定 SLO 阈值（p95/p99/error-rate/吞吐）+ 容量裕度目标（默认断点 ≥ 2× 预期峰值）——阈值来源：现有 SLO 文档 / baseline / route-class 默认，**不允许**为 pass 临时放宽（Hard Rule §2.7）
5. dispatch `qa-load-stress-runner`（它在 staging 跑 k6、`--summary-export`、抓 stdout+exit_code）
6. 验收 runner 返回的 `LOAD_TEST_SCHEMA`：command_evidence 是否真实、阈值是否真触发判定、断点是否找到、容量裕度是否达标
7. Output `load_stress_reliability` YAML

## 6. Output Contract

```yaml
load_stress_reliability:
  environment:
    target: https://staging.example.com/api   # 必须 staging/lab/preview
    is_production: false                        # 必须 false；true 则整体 BLOCKED
    environment_confirmed_by: <handle/source>   # 谁/什么证明非生产
  profiles_run:
    - profile: load | stress | soak | spike | smoke | breakpoint
      executor: ramping-arrival-rate | constant-arrival-rate | ramping-vus
      duration: <e.g. 10m / 2h soak>
      target_rate_rps: <N>          # 开模型驱动的到达率
      pre_allocated_vus: <N>
      max_vus: <N>
  slo_thresholds:
    http_req_duration_p95_ms: 500
    http_req_duration_p99_ms: 1000
    http_req_failed_rate_max: 0.01
    min_throughput_rps: <N>
    checks_pass_rate_min: 0.99
  results:
    achieved_rps: <N>
    p50_ms: <N>
    p95_ms: <N>
    p99_ms: <N>
    error_rate: <N>
    checks_pass_rate: <N>
    thresholds_breached: []          # 列出破裂的 threshold
  breakpoint:
    found: true | false
    breakpoint_rps: <N>              # SLO 首次破裂时的到达率
    expected_peak_rps: <N>
    capacity_margin_x: <breakpoint_rps / expected_peak_rps>
    margin_target_x: 2.0
    margin_met: true | false
  soak_findings:                     # 仅 soak profile
    memory_leak_suspected: false
    latency_drift_pct: <N>           # p95 末段 vs 首段
    resource_exhaustion: false
  artifacts:
    k6_summary_json: <path k6-summary.json>
    k6_stdout_log: <path>
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

## 7. Parent Integration

- Triggered by: parent §6 Step 5（reference agent 模式 — 经本 skill prepare input → `qa-load-stress-runner` execute → 本 skill validate）
- Returns: `load_stress_reliability` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.load` (evidence layer key: `load`)
- Runner emits `LOAD_TEST_SCHEMA.v1`（workflow-spec mode）；本 skill §6 YAML 是 prompt-only mode 输出
- 落盘：`bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> load <result>` → `.qa/evidence/<tag>/load.yaml`

## 8. Forbidden patterns

- **对生产环境跑任何 profile**（绝对红线，违反 Hard Rule §2.6）—— target 无法证明非生产即 BLOCKED
- 用闭模型（`ramping-vus`）找断点（系统变慢自降速 → 掩盖真实容量拐点；用 `ramping-arrival-rate`）
- 单次短跑就下"能扛"结论（容量是统计量；soak 必须够长才能抓泄漏）
- 为 pass 放宽 SLO 阈值（p95/p99/error-rate 调高 → 违反 Hard Rule §2.7 threshold weakening）
- 声称压测通过但无 `k6-summary.json` + stdout（违反 Hard Rule §2.1）
- 不设 `thresholds` 就跑（没有 pass/fail gate 的压测只是观光，不产 decision）
- 不输出 p99（只看 avg / p95 会掩盖长尾；`summaryTrendStats` 必含 p99）

## 9. References

- [k6 — load testing](https://grafana.com/docs/k6/latest/)
- [k6 test types: smoke / average-load / stress / soak / spike / breakpoint](https://grafana.com/docs/k6/latest/testing-guides/test-types/)
- [k6 breakpoint testing guide](https://grafana.com/docs/k6/latest/testing-guides/test-types/breakpoint-testing/) (open model `ramping-arrival-rate` to find capacity ceiling)
- [k6 executors — arrival-rate (open) vs vus (closed)](https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/)
- [k6 thresholds (pass/fail gate, exit code 99)](https://grafana.com/docs/k6/latest/using-k6/thresholds/)
- Parent §4 Layer matrix · §2.6 No destructive production testing · `qa-performance-reliability` §4 (self-declared scope boundary)
