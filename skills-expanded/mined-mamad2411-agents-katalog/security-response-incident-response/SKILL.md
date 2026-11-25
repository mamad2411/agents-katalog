---
name: security-response-incident-response
canonical_id: security.response.incident_response
aliases: [incident-response, security-ir, security-incident, ir-workflow]
version: 1.0.0
status: stable
created_date: 2026-05-25
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - NIST SP 800-61 Rev. 3: incident handling (CSF 2.0 aligned)
  - NIST CSF: 2.0 (RS Respond function)
  - NIST SP 800-53A Rev. 5: control assessment
  - OWASP ASVS: 5.0 (V16 Security Logging)
  - ISO/IEC 27035: incident management
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "real_user_data/**"]
  never_write: ["raw PII in IR reports", "actual credentials in evidence files"]
  redact_on_output: ["all PII", "all tokens", "all credentials", "internal IPs", "real user identifiers"]
upstream:
  - appsec-security-orchestrator (Step 10/11 escalation)
  - security-platform-secrets (leak detection → IR trigger)
  - dast-baseline-scanning (HIGH+ finding → IR consideration)
  - authorized-pentest-validation (confirmed exploit → IR)
  - user (real incident declaration)
  - external monitoring / SIEM alert
downstream:
  - security-response-recovery (when RS → RC transition)
  - appsec-security-orchestrator  # forensics bridge per §6 (no dedicated skill yet) + NIST SP 800-86 inline
  - security-remediation (root-cause fix per vuln finding)
  - compliance.reporting (regulatory notification)
description: >-
  Incident response per NIST SP 800-61 Rev. 3 (CSF 2.0 RS) - preparation, detection, analysis, containment, eradication, recovery transition, lessons learned. Owns severity classification, incident commander assignment, communications cadence, decision log and evidence chain-of-custody initiation. Hands off to `security-response-recovery` at the RS-to-RC transition. No offensive operations against attackers.
trigger_phrases:
  - incident response / 事件响应 / IR / 安全事件
  - breach / data breach / 数据泄露 / 入侵
  - IC declared / incident commander
  - SEV-1 / SEV-2 / pager / 紧急安全告警
  - 凭证泄露响应 / credential leak response
---

# Security Response — Incident Response (NIST SP 800-61 Rev. 3)

## 1. Mission

事件响应不是临场发挥。本 skill 提供 **结构化 IR workflow**：preparation → detection → analysis → containment → eradication → recovery transition → lessons learned，全程产 evidence + decision log + communications artifacts。

**职责边界**：
- **owns**: IR 整体编排、严重性分级、IC 角色分配、通讯节奏、初报/更新报告生成
- **handoff to recovery**: 满足条件即移交 `security-response-recovery`（RS → RC 切换）
- **handoff to remediation**: 每个 underlying defect 走 `security-remediation`（独立 vuln 修复）
- **不做**: offensive ops、attacker hack-back、未授权监听

---

## 2. Activation Triggers

| Trigger | 严重性建议 | 行动 |
|---|---|---|
| Confirmed breach（数据外泄、未授权访问、恶意代码运行）| SEV-1 | Immediate IR + IC + 60-min initial report |
| Confirmed credential leak with active exposure | SEV-1 / SEV-2 | Rotate + IR + check access logs |
| Active exploitation observed in monitoring | SEV-1 / SEV-2 | Containment first, IR coordinated |
| Suspected breach（异常 traffic / log）| SEV-2 / SEV-3 | Investigate + IR ready-state |
| Critical vuln being exploited in wild (CVSS 9.0+ + active exploit) | SEV-1 / SEV-2 | Patch + monitor + IR ready |
| Production outage suspected security cause | SEV-1 / SEV-2 | IR + SRE coordinated |
| Regulatory-reportable event（GDPR / PIPL / SEC / state breach laws）| SEV-1 | IR + 法务 + clock starts (e.g. GDPR 72h) |
| Insider threat reported | SEV-2 | IR + HR + legal coordination |
| Third-party / vendor incident affecting us | SEV-2 / SEV-3 | IR + vendor coordination |

---

## 3. Severity Definitions

| SEV | 定义 | Initial Response Time | IC required? | Comms cadence |
|---|---|---|---|---|
| **SEV-1** | 已确认 breach / 大规模 outage / regulatory-reportable | Immediate（pager）| Yes | 30 min during active, 4h once contained |
| **SEV-2** | 疑似 breach / partial outage / critical vuln being exploited | Within 1 hour | Yes | 1h during active, 8h once contained |
| **SEV-3** | 有限影响 / 无确认 breach / 范围已控 | Within 4 hours | Optional | Daily |
| **SEV-4** | Minor / informational（如低危 disclosure 报告）| Within 24 hours | No | Per-update |

---

## 4. Standard Workflow（Local 7-step IR workflow aligned to NIST SP 800-61 R3 + CSF 2.0 RS function）

> Note: NIST SP 800-61 Rev. 3 is a CSF 2.0 Community Profile for incident response, not a prescriptive "N-phase" lifecycle. The 7 steps below are our **local** workflow that **aligns with** SP 800-61 R3 guidance and the CSF 2.0 RS function. Do not cite this as "the NIST 7-phase model".

```
Phase 1  PREPARATION（事前，平时维护）
         → IR runbook 已写、演练过
         → IC pool 已建（primary + backup）
         → On-call rotation 含 SecOps
         → Communications plan + 模板备好
         → Evidence storage location + retention policy 定义
         → Legal/PR/regulator contact list 最新
         → Backup + restore 测试通过（链接 security-response-recovery）
         → 关键资产 inventory + threat model 更新

Phase 2  DETECTION & ANALYSIS（事件触发）
         → 来源：monitoring / user report / external disclosure / pentest / log review
         → 初判 severity（§3）
         → IC declared，分配角色：
            - Incident Commander (IC)
            - Communications Lead
            - Tech Lead
            - Legal/Compliance Liaison
         → 立即 instantiate `templates/incident-response-initial.md`
         → Evidence hash 起手：sha256 of initial logs/snapshots
         → 决定通知范围（internal vs customer vs regulator）

Phase 3  CONTAINMENT
         → Short-term: 隔离受影响系统、disable compromised creds、deploy WAF rule
         → Long-term: patch + harden + monitor for recurrence
         → 不破坏 evidence：containment 前必须 snapshot
         → 记录每个 containment action 到 decision log

Phase 4  ERADICATION
         → 移除 malware / backdoor / persistence
         → 旋转 all potentially-compromised credentials
         → patch vulnerabilities exploited
         → verify clean state（scan + log review + behavioral monitoring）

Phase 5  RECOVERY TRANSITION
         → 检查 RS → RC 切换条件（见 §5）
         → 若满足 → handoff `security-response-recovery`
         → Recovery skill 负责 backup validation / restore test / BCP/DR / customer comm

Phase 6  POST-INCIDENT
         → 30 天内必须产出：
            - Full timeline / forensic report
            - Root Cause Analysis (RCA) document
            - Customer / regulator final report（若 reporting obligation）
            - Vuln reports per underlying defect → security-remediation
            - Risk register entries for residual risk → templates/risk-register.md
            - Blameless lessons-learned post-mortem
            - Updates: SECURITY.md / threat model / IR runbook / monitoring rules / test cases

Phase 7  LESSONS LEARNED FEEDBACK
         → 演练时间表更新
         → IR runbook 修订
         → Detection 规则补充
         → 流程改进 backlog
         → 6-12 个月内复盘"我们是否从此事件真正变好了"
```

---

## 5. RS → RC Transition Criteria（必须全部满足才能切换）

事件从 **RESPONSE** 切换到 **RECOVERY** 必须**全部**满足以下条件：

- [ ] Root cause 已确认
- [ ] Vulnerability 已 patched / mitigated
- [ ] Attacker access 已确认 terminated（没有 persistence / backdoor）
- [ ] Affected systems clean state 已验证（fresh scan + log review）
- [ ] Backups 可用且已验证未被污染
- [ ] Recovery 计划已定（含 fallback if recovery fails）
- [ ] Monitoring 已部署用于 recurrence detection
- [ ] Stakeholders 已通知 recovery plan
- [ ] Legal / regulatory 通报义务已满足或在轨道上

满足后 → spawn `security-response-recovery` skill 接 RC 阶段。

---

## 6. Forensics Bridge（current — until standalone skill exists）

`security-response-forensics` skill 尚未独立存在。当前 forensics 必须按 NIST SP 800-86 在本 skill 内执行：

### Evidence collection rules
1. **Order of volatility**（先收易失证据）：
   - Memory dump > Network connections > Running processes > Logged-in users > Disk > Backups
2. **Hash immediately**：每个 evidence file 收集后立即 `sha256sum` 存入 `.planning/security/evidence/<incident-id>/hashes.sha256`
3. **Chain of custody log**：每次 evidence 移动 / 复制 / 检视 → 记录到 `chain-of-custody.md`（who / when / where / why）
4. **Storage**：encrypted at-rest，访问审计，retention 按 legal 要求（至少 1 年）
5. **Reproducibility**：commands 用于收集 evidence 必须可复现（写到 runbook）

### Tools (passive only, never modify target)
- Memory: `volatility` / `lime` / `winpmem`
- Network: `tcpdump` / `wireshark`（read-only pcap）
- Disk: `dd` / `dcfldd` with hash verification
- Logs: `grep` / `jq` / `splunk` query export
- Cloud: vendor audit log export (CloudTrail / Stackdriver / Azure Monitor)

### Hard rules
- ❌ 不在 evidence file 上做 destructive operation
- ❌ 不向 LLM 暴露 raw PII / credentials / tokens（必须 redact）
- ❌ 不与 attacker 沟通 / 通报 attacker（让 attacker 知道被发现 = blow op）
- ❌ 不在没有 chain-of-custody 时复制 evidence

---

## 7. Communications Playbook

| 受众 | When | Channel | Owner | Template |
|---|---|---|---|---|
| Incident team | Continuous | War room / Slack channel | IC | rolling update |
| Engineering leadership | T+15 min, then every 30 min during active | Email + chat | IC | initial report → status updates |
| Executive leadership | T+1h (SEV-1) / T+4h (SEV-2) | Email + call | Comms lead + CISO | exec summary |
| Customers (affected) | Per breach laws / SLA, often within 72h | Status page + email | Comms lead + Legal | customer notification template |
| Regulators | Per regulation（GDPR 72h / PIPL / SEC 4 business days for material breaches）| Official channel | Legal | regulatory notification template |
| Press / Public | Only if escalated; coordinated | Press release | PR + CEO + Legal | press template |
| Partners / Vendors | If affected | Direct contact | Comms lead | partner notification template |

**Iron rule**: NO unauthorized speculation in public communications. NO admission of liability before facts confirmed. ALL external comms reviewed by Legal before send.

---

## 8. Decision Log Discipline

每个 IR 决策必须记录：

| Field | Required |
|---|---|
| Timestamp (ISO 8601 with timezone) | Yes |
| Decision | Yes (one-line) |
| Decision-maker (role + name) | Yes |
| Rationale | Yes |
| Alternatives considered | Recommended |
| Reversible? | Yes (yes/no/partial) |
| Confidence level | High/Medium/Low |
| Linked evidence | If applicable |

存储位置：`.planning/security/incidents/<incident-id>/decision-log.md`

---

## 9. Standard Outputs

每个 incident 必须产出：

1. **Initial report**（T+30min / T+60min）— `templates/incident-response-initial.md`
2. **Status updates** — same template, version-bumped
3. **Decision log** — `decision-log.md`
4. **Evidence inventory + chain of custody** — `.planning/security/evidence/<incident-id>/`
5. **Containment actions log**
6. **Communications log**（who notified, when, content sent）
7. **Final report**（post-incident, within 30 days）含：
   - Full timeline
   - Root cause analysis
   - Damage assessment
   - Customer/regulator notifications status
   - Vuln reports per defect → security-remediation
   - Recovery report → security-response-recovery
   - Lessons learned

---

## 10. Hard Rules

- ❌ **不**在 chat / report / log 中放未 redact 的 PII / token / credential
- ❌ **不**做 hack-back / offensive ops / attacker pursuit
- ❌ **不**在 containment 前破坏 evidence
- ❌ **不**让 IC 同时担任 Tech Lead（分离职责）
- ❌ **不**跳过 communications cadence（沉默会引发猜测和恐慌）
- ❌ **不**在没有 legal 参与时通知 regulator
- ❌ **不**自动声明 "no data accessed" 除非 forensics 完成
- ❌ **不**在事件未完全 contained 时切换到 recovery
- ❌ **不**关闭事件而不做 post-incident review
- ❌ **不**用 user / customer 数据做 IR 演练

---

## 11. Anti-patterns

- ❌ "Incident command by Slack thread" — 无 IC 无角色无决策日志
- ❌ "Just patch and move on" — 跳过 RCA / lessons learned
- ❌ "Tell legal later" — 通报时钟可能已在跑（GDPR 72h、PIPL 等）
- ❌ "Customer doesn't need to know" — breach 通报法律义务，不是商业决策
- ❌ "We'll write the post-mortem next sprint" — 30 天死线
- ❌ 把 vuln remediation 和 IR 混在同一个 workflow（应 handoff to security-remediation per vuln）
- ❌ Recovery 提前启动（在 containment + eradication 未完成时尝试恢复 = 重新感染）

---

## 12. References

- [NIST SP 800-61 Rev. 3 Incident Handling Guide](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [NIST SP 800-86 Forensics Integration](https://csrc.nist.gov/pubs/sp/800/86/final)
- [NIST CSF 2.0 RS / RC Functions](https://www.nist.gov/cyberframework)
- [ISO/IEC 27035 Incident Management](https://www.iso.org/standard/44379.html)
- [GDPR Art. 33-34 Breach Notification](https://gdpr-info.eu/art-33-gdpr/)
- [China PIPL Art. 57 Breach Notification](http://www.cac.gov.cn/2021-08/20/c_1631050147315362.htm)
- [templates/incident-response-initial.md](../appsec-security-orchestrator/templates/incident-response-initial.md) — required template
- [security-response-recovery](../security-response-recovery/SKILL.md) — RS → RC handoff
- [security-remediation](../security-remediation/SKILL.md) — per-vuln fix
- [appsec-security-orchestrator §7 Step 10/11](../appsec-security-orchestrator/SKILL.md)
