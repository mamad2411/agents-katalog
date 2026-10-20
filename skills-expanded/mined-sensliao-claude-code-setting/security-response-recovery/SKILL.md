---
name: security-response-recovery
canonical_id: security.response.recovery
aliases: [security-recovery, bcp-dr, disaster-recovery, business-continuity]
version: 1.0.0
status: stable
created_date: 2026-05-25
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - NIST CSF: 2.0 (RC Recover function)
  - NIST SP 800-61 Rev. 3: incident handling (recovery phase alignment)
  - NIST SP 800-34: contingency planning
  - NIST SP 800-184: cybersecurity event recovery
  - ISO/IEC 22301: business continuity management
  - ISO/IEC 27031: ICT readiness for business continuity
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "production_backup_data/**"]
  never_write: ["raw PII in recovery reports", "real customer data in restore tests"]
  redact_on_output: ["customer identifiers", "internal IPs", "tokens", "credentials"]
upstream:
  - security-response-incident-response (RS → RC handoff after eradication)
  - user (planned BCP/DR exercise)
  - scheduled maintenance (recovery validation routine)
downstream:
  - compliance.reporting (recovery report to regulator if required)
  - appsec-security-orchestrator (Release Evidence §15 Recovery Specifics)
  - security-remediation (any defect found during recovery)
description: >-
  CSF 2.0 RC (Recover) skill - backup validation, restore testing, RTO/RPO verification, BCP/DR plan execution, customer and regulator recovery communications, post-incident recovery review. Runs after incident-response completes containment, and for scheduled recovery exercises or pre-launch DR readiness. Never destructively modifies production backups.
trigger_phrases:
  - recovery / 恢复 / RC / disaster recovery / DR / 灾难恢复
  - business continuity / BCP / 业务连续性
  - backup validation / 备份验证 / restore test / 恢复测试
  - RTO / RPO / recovery time objective / recovery point objective
  - post-incident recovery review / 事件后恢复复盘
  - DR exercise / DR drill / failover test
---

# Security Response — Recovery (NIST CSF 2.0 RC)

## 1. Mission

Recovery 不是"事件结束自动发生"。本 skill 把 CSF 2.0 **RC (Recover)** 功能落成可执行工作流：backup validation / restore testing / RTO-RPO verification / BCP-DR plan execution / customer & regulator comms / post-incident recovery review。

**职责边界**：
- **owns**: 恢复编排、备份验证、恢复测试、RTO/RPO 计算、BCP/DR 演练、recovery comms
- **不做**: incident detection / containment（归 `security-response-incident-response`）
- **不做**: 破坏性生产 backup 操作

**Activation modes**：
- **Mode A — Post-incident**：由 `security-response-incident-response` handoff（RS → RC 切换满足，见 IR §5）
- **Mode B — Scheduled drill**：用户计划 DR 演练 / 季度 backup validation / 上线前 readiness check
- **Mode C — Recovery audit**：合规审计前回顾 recovery 能力 + evidence

---

## 2. Activation Triggers

| Trigger | Mode | Action |
|---|---|---|
| `security-response-incident-response` 触发 RS→RC handoff | A | 立即执行 Mode A workflow |
| 计划 DR 演练 | B | 走 Mode B 演练 workflow |
| 季度 backup validation | B | 走 backup 验证子流程 |
| 上线前 DR readiness check | B | 走 readiness audit |
| 合规审计（ISO 27001 / SOC2 / 等）准备 | C | 走 evidence aggregation |
| 真实 disaster（云 region 故障 / 大规模 outage）| A | 走 Mode A，IR 并行 |

---

## 3. Standards Mapping

| Standard | 适用范围 |
|---|---|
| NIST CSF 2.0 RC | Recover function — recovery planning + improvements + communications |
| NIST SP 800-34 Rev. 1 | Contingency Planning Guide for Federal Information Systems |
| NIST SP 800-184 | Guide for Cybersecurity Event Recovery |
| ISO/IEC 22301 | Business Continuity Management Systems |
| ISO/IEC 27031 | ICT readiness for business continuity |
| NIST SP 800-61 R3 Phase 5 | IR recovery phase alignment |

---

## 4. Standard Workflow — Mode A (Post-Incident Recovery)

```
Step 1  Verify RS→RC transition criteria
        → Read incident-response §5 checklist
        → 任一未满足 → block + 返回 IR

Step 2  Backup integrity verification
        → 列出可用 backup（最近 N 个 restore points）
        → 验证 backup 未被污染（compare against pre-incident hash if available）
        → 检查 backup 是否被 attacker access / modification（log audit）
        → 选择干净 backup point（RPO 内最近的干净点）

Step 3  Isolated restore test
        → 在隔离环境 restore（不直接覆盖生产）
        → 验证 restore 完整性（schema check / data consistency / functional smoke）
        → 验证 vulnerability 在 restored data 上不再 exploit-able
        → 记录 restore 耗时（与 RTO 对比）

Step 4  Recovery decision
        → 决定 path：restore-from-backup / rebuild-from-scratch / partial-restore-plus-replay
        → AskUserQuestion: present options with trade-offs → user 拍板
        → 写到 decision log

Step 5  Production recovery execution
        → 按 decision 执行
        → 实时监控：performance / error rate / functionality
        → 准备 abort path（如 recovery 失败的 fallback）

Step 6  Recovery validation
        → Functional: critical user journeys 通过 smoke test
        → Security: monitoring active，没有 recurrence indicator
        → Data integrity: spot-check critical tables / files
        → Performance: 在可接受范围内

Step 7  Resume normal operations
        → 通知 stakeholders
        → 重启依赖服务
        → 更新 status page
        → 移交 oncall 回常态

Step 8  Customer & regulator recovery communications
        → Status page update：recovery complete + timeline
        → Customer email（affected only）：what happened, what was restored, next steps
        → Regulator update（如有 reporting obligation）：recovery confirmation
        → Press（仅在前期已 public 时）：closing statement

Step 9  Post-incident recovery review（T+30 day max）
        → RTO actual vs target
        → RPO actual vs target
        → 哪些 backup 工作了 / 哪些没有
        → Restore plan 哪里 friction
        → Communications cadence 是否合适
        → BCP/DR plan 修订项目
        → Lessons learned → 更新 runbook + IR plan + threat model

Step 10 Update recovery records
        → AppSec Release Evidence §15 Recovery Specifics 填表
        → templates/incident-response-initial.md §7 Recovery Criteria 复核闭环
        → risk-register.md 新增"recovery capability gap"项（如发现）
```

---

## 5. Standard Workflow — Mode B (Scheduled Drill)

```
Step 1  Plan drill
        → 选 scenario（数据库 corruption / region outage / ransomware simulation / dependency failure）
        → 定 scope（哪些系统、哪些 backup、哪些 stakeholder 参与）
        → 定 success criteria（RTO / RPO 目标 + functional checks）
        → 排时间 + 通知参与方 + 设 abort 条件

Step 2  Pre-drill checks
        → Backups 可读 + recent
        → Restore tooling 可用
        → Test environment 隔离 + 不接生产
        → Communications channels 已 setup（不污染生产 oncall）

Step 3  Execute drill
        → 按 scenario timeline
        → 实时记录：每步耗时、问题、决策
        → 不擅自扩大 scope

Step 4  Validate outcome
        → 与 success criteria 对比
        → 评估 actual RTO/RPO vs target
        → 找到 friction points

Step 5  Drill report
        → 时间线
        → RTO actual vs target
        → RPO actual vs target
        → Friction list + 改进项 owner
        → 下次 drill 排期

Step 6  Update runbook
        → 修订 BCP/DR plan
        → 更新 monitoring 阈值
        → 训练 oncall 新流程
```

---

## 5.5 Standard Workflow — Mode C (Recovery Audit)

```
Step 1  Audit scope decision
        → 哪些 system / business process 在范围
        → 哪个 framework 做 reference（ISO 22301 / NIST CSF RC / SOC2 CC9.1 / 行业）
        → audit period（过去 12 / 6 / 3 个月）
        → 上次 audit 时间 + 改进项是否闭环

Step 2  Recovery capability inventory
        → 列每个 critical system 的：
          - 当前 RTO / RPO target
          - 上次 measured MTTR / MTBF
          - Backup 策略（频率 / 加密 / immutability / 跨 region）
          - Standby tier（hot / warm / cold）
          - DR site / region 配置
          - BCP plan 链接 + 最近 review date
          - IR / RC runbook 链接

Step 3  Evidence aggregation（按 audit framework）
        → 收集过去 audit period 的：
          - Backup validation 报告（每月 / 每季）
          - Restore test 报告（每季 / 每年）
          - DR drill 报告（每年至少 1 次）
          - Real incident recovery reports + post-mortem
          - Configuration baseline + drift 记录
          - Vendor recovery commitments + SLAs

Step 4  RTO / RPO evidence verification
        → Actual vs target deltas
        → Trend analysis（improving / stable / degrading）
        → Tier 分类是否仍合适（business criticality 有变？）

Step 5  BCP / DR plan review
        → 与 actual business operations 是否对齐
        → 关键人员 contact 是否最新
        → Vendor + 3rd party 依赖是否仍准确
        → 上次 review date（如 >12 个月 → red flag）

Step 6  Compliance mapping
        → 按 framework 逐 control:
          - ISO 22301: 6.1, 8.4, 8.5, 9.1, 9.3
          - NIST CSF 2.0 RC: RC.RP, RC.IM, RC.CO
          - SOC2 CC9.1, CC9.2
          - 行业（HIPAA / PCI / FFIEC / 等）
        → 每条 control：evidence 存在 yes/no + audit-grade quality

Step 7  Gap scoring + remediation roadmap
        → 每个 gap：severity + effort + business impact + owner + due date
        → 优先级矩阵（high-impact / low-effort 先做）
        → 写入 risk-register.md

Step 8  Audit package output
        → 给 internal / external auditor 的完整 evidence 包：
          - Executive summary
          - Per-system capability inventory
          - Per-framework control coverage
          - Gap analysis + remediation roadmap
          - Improvement metrics（vs last audit）
        → 输出到 `.planning/security/recovery-audit-<date>/`
```

---

## 6. Backup Validation Checklist

每个 backup 必须满足：

- [ ] Backup 是 immutable（attacker 攻击生产时 backup 不可被 delete / encrypt）
- [ ] Backup 存放在独立帐号 / region / cloud（blast radius 隔离）
- [ ] Backup encryption at-rest（key 独立管理，不与生产共享 KMS）
- [ ] Backup integrity hash 存档（防 silent corruption）
- [ ] Backup retention 满足 RPO + 合规要求
- [ ] Backup restore 在过去 N 天内被验证过（无未测试的 backup）
- [ ] Backup contains all critical data（database / config / secrets / user uploads / audit logs）
- [ ] Backup metadata 可读（不依赖未保存的 schema）
- [ ] Restore script 可在 fresh 环境跑通（不依赖手动步骤）
- [ ] Restore 耗时已 measure（用于 RTO 计算）

---

## 7. RTO / RPO Specification

| Metric | 定义 | 影响 |
|---|---|---|
| **RTO** (Recovery Time Objective) | 从 disaster 发生到系统恢复可用的最长可接受时间 | 决定 hot/warm/cold standby、failover automation |
| **RPO** (Recovery Point Objective) | 可接受的最大数据丢失（时间窗）| 决定 backup 频率、replication lag tolerance |
| **MTTR** (Mean Time To Recover) | 历史平均恢复时间 | 与 RTO 对比，判断目标是否现实 |
| **MTBF** (Mean Time Between Failures) | 历史平均故障间隔 | 用于 SLA 设计 |

**Tier 建议（参考，按业务调整）**：

| Tier | RTO | RPO | Approach |
|---|---|---|---|
| **0 Mission-critical** | < 5 min | < 1 min | Multi-region active-active + sync replication |
| **1 Business-critical** | < 1h | < 15 min | Hot standby + frequent replication |
| **2 Important** | < 8h | < 4h | Warm standby + scheduled replication |
| **3 Non-critical** | < 24h | < 24h | Daily backup + cold restore |

---

## 8. Hard Rules

- ❌ **不**在 production backup 上做破坏性操作（restore 必须在隔离环境先做）
- ❌ **不**用过期 / 未验证的 backup 直接恢复生产
- ❌ **不**在 IR 未完成 containment + eradication 时尝试 recovery（重新感染风险）
- ❌ **不**忽略 backup 污染检查（attacker 可能预先污染 backup）
- ❌ **不**用生产数据做 drill（脱敏 / synthetic data only）
- ❌ **不**跳过 post-incident recovery review（30 天死线）
- ❌ **不**自动声明"recovered"除非 functional + security 双验证
- ❌ **不**在 communications 中承诺未来 SLA 改进而无 follow-through plan
- ❌ **不**让 recovery 跳过 customer/regulator 通报义务
- ❌ **不**把 Recovery 当 IR 的尾巴（它是独立 CSF 功能，配独立计划 + 演练 + 度量）

---

## 9. Output Contract

每次 recovery 活动产出：

### Mode A (Post-incident)
1. RS→RC transition verification checklist（完整签字）
2. Backup validation report（哪个 backup 选了，为什么）
3. Isolated restore test report
4. Recovery decision log
5. Production recovery execution log
6. Recovery validation report
7. Customer / regulator recovery communications log
8. Post-incident recovery review（T+30d）
9. AppSec Release Evidence §15 Recovery Specifics 填表
10. risk-register entries（recovery capability gaps）

### Mode B (Scheduled drill)
1. Drill plan
2. Pre-drill check report
3. Execution timeline
4. Drill outcome vs success criteria
5. Friction list + 改进项 + owner
6. Updated BCP/DR plan
7. Next drill schedule

### Mode C (Recovery audit)
1. Recovery capability inventory
2. Evidence aggregation（drills + post-incident reviews）
3. Compliance mapping（ISO 22301 / NIST CSF RC / SOC2 CC9.1）
4. Gap analysis + remediation roadmap

---

## 10. Anti-patterns

- ❌ "We have backups, we're fine" — backup 存在 ≠ recovery capability
- ❌ "We tested restore last year" — backup 验证必须季度 cadence
- ❌ "RTO is whatever it ends up being" — 没有目标就没有改进
- ❌ "DR drill is too disruptive" — 不演练 = 真实事件第一次跑流程
- ❌ Recovery comms 用 IR template — 它是独立阶段，独立 messaging
- ❌ "Just restore from latest backup" — 没有验证清洁度 = 重新感染
- ❌ "Skip post-mortem if recovery succeeded" — 成功也要复盘（哪里偶然，哪里可靠）
- ❌ 把 RC 等同于 "restore data" — RC 含 communications / process / improvements，不只 data
- ❌ BCP/DR plan 写完不维护 — 业务变化 plan 要跟

---

## 11. References

- [NIST SP 800-184 Cybersecurity Event Recovery](https://csrc.nist.gov/pubs/sp/800/184/final)
- [NIST SP 800-34 Rev. 1 Contingency Planning](https://csrc.nist.gov/pubs/sp/800/34/r1/final)
- [NIST CSF 2.0 RC Function](https://www.nist.gov/cyberframework)
- [ISO/IEC 22301 BCMS](https://www.iso.org/standard/75106.html)
- [ISO/IEC 27031 ICT Readiness](https://www.iso.org/standard/44374.html)
- [security-response-incident-response](../security-response-incident-response/SKILL.md) — upstream handoff
- [templates/incident-response-initial.md §7](../appsec-security-orchestrator/templates/incident-response-initial.md) — RC criteria
- [appsec-security-orchestrator §15](../appsec-security-orchestrator/SKILL.md) — Recovery Specifics evidence
