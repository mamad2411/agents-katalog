---
name: qa-resilience-fault-injection
version: 1.0.0
status: stable
created_date: 2026-06-15
allowed-tools: Read, Bash, Grep, Glob
parent: enterprise-qa-testing
references_agents: [qa-resilience-runner]
description: >-
  QA child skill - chaos / fault injection / resilience: hypothesis-driven steady-state, inject, observe, always rollback, with bounded named faults (Toxiproxy latency/partition/bandwidth, Pumba container kill/pause/netem, dependency failure, resource pressure). RED-LINE skill: PLANNING-FIRST + DOUBLE-GATE, STAGING / LAB ONLY, NEVER production (parent Hard Rule 2.6). Owns parent Resilience/Fault-Injection layer.
---

# qa-resilience-fault-injection

## 1. Position

韧性 / 混沌工程 skill。回答的是"当依赖变慢 / 断连 / 容器死掉 / 资源耗尽时，这个系统**会优雅降级、自愈、还是雪崩**"。它不是压测（`qa-load-stress-reliability` 量"能扛多少 RPS、断点在哪"）——本 skill 量"**遇到坏事时的行为**"：超时是否生效、重试是否有界、熔断是否打开、降级路径是否存在、告警是否触发、恢复是否自动。

混沌工程的产业定义（Principles of Chaos Engineering）是**实验**，不是"随便搞坏看看"：先定义稳态（steady-state）→ 提出假设（注入故障后稳态仍维持）→ 在**有界爆炸半径**内注入真实世界故障 → 观测稳态是否被打破 → **始终回滚**。本 skill 强制这套科学方法，不允许无假设乱注入。

**铁律：这是 RED-LINE skill。planning-first + DOUBLE-GATE，限 staging / lab，绝不打生产。** 注入故障会主动制造 latency / 断连 / 杀进程 / 占资源——在生产上做就是自残（拖垮真实用户、可能触发级联故障）。本 skill 的安全边界**完全复用**父级 Hard Rule §2.6（No destructive production testing），**不发明新的 gate 机制**——它把那条既有规则 + `pentest-scope-and-roe` 式的"先 plan、人确认、再执行"模式套到混沌实验上。

## 2. Triggers

- Parent §6 Step 5（risk 选了 Resilience layer — 通常 High/Critical + 多依赖 / 分布式 / 微服务 / 队列 / 外部 API 重度依赖的后端）
- 架构引入新的失败面：加了外部依赖、消息队列、缓存层、跨服务调用、超时 / 重试 / 熔断逻辑
- 发布前韧性验证（"依赖挂了我们扛得住吗"）
- 事后复盘驱动（生产出过级联故障 / 重试风暴 / 超时雪崩 → 验证修复确实让系统更韧）
- GameDay / DiRT 演练（团队定期做的受控故障演练）
- 独立触发：SRE / 平台团队做 resilience review
- 与 `security-governance-threat-modeling §6.5`（benign failure modes：retry storm / cascade / capacity ceiling）对称——threat-model 在设计期**识别**这些失败模式，本 skill 在 staging **实测**它们

## 3. Responsibilities（planning-first，永远先起草后执行）

### 3.1 故障类型（bounded, named faults — 复用现成 OSS 工具，不手搓）

| 故障类别 | 工具 | 具体注入 | 爆炸半径控制 |
|---|---|---|---|
| **Network latency** | Toxiproxy `latency` toxic | 给上游/依赖连接注入固定/抖动延迟 | 只作用于经 Toxiproxy proxy 的连接；`toxicity`（0-1）控制只影响一部分流量 |
| **Network partition / 断连** | Toxiproxy `timeout` / disable proxy | 模拟依赖不可达 / 连接超时 | 单 proxy 粒度；可随时 enable 恢复 |
| **Bandwidth 限制** | Toxiproxy `bandwidth` toxic | 限制吞吐，模拟慢网络 | 单 proxy 粒度 |
| **慢响应 / 数据截断** | Toxiproxy `slow_close` / `slicer` / `limit_data` | 模拟半开连接 / 分片 / 截断 | 单 proxy 粒度 |
| **Container kill** | Pumba `kill` | 杀容器（SIGKILL/SIGTERM），验证重启 / 副本接管 | `--random` + label/name 过滤，只命中**显式指定**的非关键容器 |
| **Container pause** | Pumba `pause` | 冻结容器一段时间，模拟 GC stall / 卡死 | `--duration` 有界，到点自动 unpause |
| **Container netem** | Pumba `netem delay/loss/duplicate/corrupt` | 容器网络层延迟 / 丢包 / 重复 / 损坏 | `--duration` 有界 + 目标容器显式指定 |
| **Dependency failure** | service-virtualization / Toxiproxy | 模拟下游服务 5xx / 拒绝连接 | 经 proxy 注入，不碰真实依赖 |
| **Resource pressure** | stress-ng（容器内） / `--cpu` / `--vm` | CPU / memory / IO 压力，验证资源耗尽下行为 | 限定容器 + `--timeout` 有界 |

> **Toxiproxy（Shopify, MIT）**：TCP proxy，应用通过它连依赖；toxic 是**命名、有界、可即时移除**的故障注入——blast-radius 最安全。**Pumba（Apache-2.0）**：Docker/containerd/Podman 单 Go 二进制，无控制面，`--duration` 强制有界。两者都是 staging/lab 工具。

### 3.2 实验设计（steady-state hypothesis — 强制）

每个混沌实验**必须**先写出：

1. **Steady-state 定义**：系统"健康"的可量化指标（成功率 ≥ 99.5% / p95 < 500ms / 队列深度 < N / 无 5xx 飙升）——必须是**业务/输出**指标，不是"CPU 没满"这种内部指标
2. **Hypothesis**：注入 X 故障后，稳态**仍维持**（因为有超时/重试/熔断/降级/副本）——这是要**证伪**的命题
3. **Blast radius**：精确限定影响面（哪个 proxy / 哪个容器 / 多大 toxicity / 多长 duration / 单实例还是子集）
4. **Abort conditions**：出现什么立即停（稳态指标跌破阈值的反向、真实用户受影响信号、越出 staging）
5. **Rollback plan**：如何**确定性地**移除故障恢复稳态（remove toxic / enable proxy / unpause / stop pumba / 等重启完成）——**必须先于注入就备好**
6. **Observation plan**：注入期间看什么（错误率 / 延迟 / 熔断状态 / 重试计数 / 日志 / 告警是否触发 / 恢复耗时 MTTR）

### 3.3 验证维度（混沌实验要回答的韧性问题）

- **Timeout**：依赖变慢时，调用方超时是否生效（不会无限挂起）
- **Retry boundedness**：重试是否有上限 + backoff + jitter（**不**触发重试风暴——retry storm 是常见自残）
- **Circuit breaker**：依赖持续失败时熔断是否打开、半开探测是否正确
- **Graceful degradation**：依赖不可用时是否有降级路径（缓存 / 默认值 / 排队 / 友好错误），而非整体 500
- **Bulkhead / 隔离**：一个依赖的故障是否被隔离，不拖垮无关功能（避免 cascade）
- **Self-healing / recovery**：故障移除后系统是否**自动**恢复稳态 + 恢复耗时（MTTR）
- **Alerting**：故障是否触发预期告警（沉默的故障是更大的故障）
- **Data integrity**：注入期间是否产生数据损坏 / 丢失 / 重复处理（幂等性）

## 4. Non-responsibilities

- **绝不打生产**（父级 Hard Rule §2.6）——生产韧性靠真实流量观测 + 渐进发布，不靠注入；本 skill 限 staging/lab
- 不做容量/吞吐压测（→ `qa-load-stress-reliability`；本 skill 量"坏事下的行为"，不量"能扛多少"）
- 不做生产只读 smoke（→ `qa-smoke-release-safety`）
- 不实施修复（发现韧性缺口 → 报给 owner / 走 GSD 修；本 skill 只验证 + 出证据）
- 不替代 APM / 可观测性平台（Datadog / Grafana / OpenTelemetry）——本 skill **消费**它们的指标做 steady-state 判定
- 不做安全 fault-injection / 攻击模拟（→ AppSec `authorized-pentest-validation`；混沌是 observe-and-rollback 的可靠性实验，不是攻击）
- **不发明新 gate 机制**——安全边界复用父级 §2.6 + 本 skill 的 planning-first 双门，不新增 governance machinery

## 5. Workflow（DOUBLE-GATE — 两道人确认坎，绝不自动注入）

```
  ┌─ GATE 1: 环境隔离 + 实验设计审批（planning-first）──────────────┐
  │ Step 1  环境隔离校验（最先做，硬门）                              │
  │ Step 2  起草混沌实验（steady-state / hypothesis / blast-radius / │
  │         abort / rollback / observation —— §3.2 六件齐全）        │
  │ Step 3  ⛔ 渲染实验卡 → 等用户显式 "go / 批准 / 执行"            │
  └──────────────────────────────────────────────────────────────┘
                              ↓ 用户批准后
  ┌─ GATE 2: 执行（仍可随时 abort + 强制 rollback）─────────────────┐
  │ Step 4  dispatch qa-resilience-runner（mode=execution）         │
  │         先验稳态 baseline → 注入 → 观测 → **始终 rollback**     │
  │ Step 5  验收 runner 返回的 RESILIENCE_SCHEMA                    │
  │ Step 6  Output resilience_fault_injection YAML                 │
  └──────────────────────────────────────────────────────────────┘
```

1. **环境隔离校验（GATE 1 第一步，硬门）**：确认 target 是 staging / lab / preview / localhost / 隔离 Docker 网络。命中生产信号（prod / www 顶级生产域 / 已知生产 host / 真实流量端点）或无法证明非生产 → **BLOCKED**，不起草、不执行。要求调用方显式提供 staging target + 书面确认非生产。
2. **起草混沌实验（planning-only）**：按 §3.2 六件套写完整——steady-state 量化指标 / hypothesis / blast-radius 精确边界 / abort conditions / rollback plan / observation plan。任一缺失 → 不进 Step 3。
3. **GATE 1 — 渲染实验卡 + 等人确认**：把实验卡（环境 + 故障类型 + 爆炸半径 + 假设 + abort + rollback）展示给用户，**等显式 "go / 批准 / 执行 / proceed"**。沉默 / 含糊 ≠ 批准。这一道坎复用 `pentest-scope-and-roe` 的 deliberate-action 哲学：先 plan，人点头，再动。
4. **GATE 2 — dispatch runner 执行**：用户批准后 dispatch `qa-resilience-runner`（mode=execution）。runner：① 先量 steady-state baseline（不健康就不注入）② 在 blast-radius 内注入 named fault ③ 注入期间采集观测指标 ④ **无论成败始终执行 rollback** ⑤ rollback 后再量一次稳态确认恢复。全程 command_evidence 留证。
5. **验收 RESILIENCE_SCHEMA**：检查 command_evidence 真实、steady-state 前后都量了、rollback 确实执行且恢复确认、hypothesis 结论有观测数据支撑、未越爆炸半径。
6. **Output** `resilience_fault_injection` YAML。

> **plan-only / design-only mode**：Step 1-3 照走（起草实验卡），但 **Step 4 不实际注入**——runner 标 `BLOCKED — <mode>, not executed` + 列出计划注入的命令。这是允许的，**不算**假通过。生产环境即使在 plan-only 也只输出实验设计，绝不执行。

## 6. Output Contract

```yaml
resilience_fault_injection:
  environment:
    target: https://staging.example.com        # 必须 staging/lab/preview
    is_production: false                         # 必须 false；true 则整体 BLOCKED
    environment_confirmed_by: <handle/source>    # 谁/什么证明非生产
    isolation: docker-network | k8s-namespace | lab | localhost
  gates:
    gate1_experiment_approved: true              # planning 审批（人确认）
    gate1_approved_by: <handle>
    gate2_execution_mode: execution | plan-only | design-only
  experiment:
    name: <e.g. "checkout survives 2s payment-gateway latency">
    steady_state:
      metric: <e.g. checkout success rate>
      healthy_threshold: ">= 99.5%"
      measured_baseline: <observed before injection>
    hypothesis: <注入后稳态仍维持，因为有 X 机制>
    fault:
      category: network-latency | network-partition | bandwidth | container-kill | container-pause | netem | dependency-failure | resource-pressure
      tool: toxiproxy | pumba | stress-ng | service-virtualization
      injection: <e.g. "toxiproxy latency 2000ms toxicity=0.5 on payment-proxy">
      blast_radius: <精确边界：哪个 proxy/容器 + toxicity + duration>
      duration: <有界，e.g. 5m>
    abort_conditions: [<触发即停的反向信号>]
    rollback_plan: <确定性恢复步骤>
  results:
    steady_state_held: true | false              # 稳态是否维持（hypothesis 验证）
    observed_behavior:
      timeout_triggered: true | false | n/a
      retry_bounded: true | false | n/a          # 无重试风暴
      circuit_breaker_opened: true | false | n/a
      graceful_degradation: true | false | n/a
      cascade_contained: true | false | n/a      # 故障未拖垮无关功能
      alert_fired: true | false | n/a
      data_integrity_preserved: true | false | n/a
    recovery:
      rollback_executed: true                    # 必须 true（始终回滚）
      self_healed: true | false                  # 移除故障后是否自动恢复
      steady_state_restored: true | false        # rollback 后稳态确认恢复
      mttr_seconds: <恢复耗时>
    weaknesses_found: []                          # 韧性缺口（无超时/重试无界/无降级/cascade/无告警）
  artifacts:
    runner_log: <path>
    observation_metrics: <path to collected metrics>
  decision: PASS | FAIL | BLOCKED
  blockers: []
```

> **decision 语义**：`steady_state_held == true` AND `rollback_executed == true` AND `steady_state_restored == true` → **PASS**（系统在该故障下韧性达标）。`steady_state_held == false`（hypothesis 被证伪，稳态被打破）→ **FAIL**（发现真实韧性缺口，列入 `weaknesses_found`，不是 BLOCKED——这是有价值的发现）。环境无法证明非生产 / GATE 1 未批准 / rollback 未执行 / 越出爆炸半径 → **BLOCKED**。

## 7. Parent Integration

- Triggered by: parent §6 Step 5（reference agent 模式 — 本 skill prepare + 双门审批 → `qa-resilience-runner` execute → 本 skill validate）
- Returns: `resilience_fault_injection` YAML
- Consumed by: `qa-evidence-bundle` → `child_skill_results.resilience`（evidence layer key: `resilience`）
- Runner emits `RESILIENCE_SCHEMA.v1`（workflow-spec mode）；本 skill §6 YAML 是 prompt-only mode 输出
- 落盘：`bash "$HOME/.claude/scripts/qa-sdk.sh" evidence.append <tag> resilience <result>` → `.qa/evidence/<tag>/resilience.yaml`
- **安全边界来源**：父级 §2.6（No destructive production testing）——本 skill **不新增** gate，复用它 + planning-first 双门

## 8. Forbidden patterns

- **对生产环境注入任何故障**（绝对红线，违反父级 Hard Rule §2.6）—— target 无法证明非生产即 BLOCKED，连 plan-only 也不执行
- **跳过 GATE 1**（无实验卡审批就注入）—— planning-first 双门是本 skill 的安全核心，绝不自动注入
- **无 steady-state hypothesis 就注入**（"随便搞坏看看" ≠ 混沌工程；必须先定义健康、提出可证伪假设）
- **无界注入**（toxic 不设 toxicity 边界 / pumba 不设 `--duration` / 故障不限定单 proxy/容器）—— blast radius 必须精确有界
- **不 rollback 或 rollback 不确定**（注入后不恢复 = 把 staging 搞坏；rollback plan 必须先于注入就备好，且执行后确认稳态恢复）
- **注入第三方依赖真身**（应经 Toxiproxy proxy 模拟其故障，不真的去打 Stripe/外部 API —— 那是 DoS 别人）
- **声称韧性通过但无 command_evidence / 无前后稳态测量**（违反父级 Hard Rule §2.1）
- **把 hypothesis 被证伪当失败掩盖**（稳态被打破 = 发现真实缺口，要如实 FAIL + 记 `weaknesses_found`，不是藏起来）
- 用混沌注入做安全攻击模拟（→ AppSec；混沌是 observe-and-rollback 可靠性实验，永不带攻击意图）

## 9. References

- [Principles of Chaos Engineering](https://principlesofchaos.org/) — steady-state hypothesis / bounded blast radius / always rollback
- [Toxiproxy (Shopify, MIT)](https://github.com/Shopify/toxiproxy) — TCP proxy, named bounded toxics (latency / timeout / bandwidth / slicer / limit_data)
- [Pumba (Apache-2.0)](https://github.com/alexei-led/pumba) — Docker/containerd/Podman chaos: kill / pause / netem (delay/loss/corrupt), `--duration` bounded
- [Netflix Chaos Engineering / Chaos Monkey](https://netflix.github.io/chaosmonkey/) — origin of discipline (production only at extreme maturity; NOT this skill's scope)
- Parent §4 Layer matrix · §2.6 No destructive production testing (the reused Hard Rule — NOT a new gate) · §3.6 Floor Rules
- Sibling boundary: `qa-load-stress-reliability` §1 (capacity ceiling vs behavior-under-fault) · `security-governance-threat-modeling` §6.5 (benign failure-mode lens, design-time)
- Governance pattern mirrored: `pentest-scope-and-roe` (planning-first, deliberate-action, double-gate)
