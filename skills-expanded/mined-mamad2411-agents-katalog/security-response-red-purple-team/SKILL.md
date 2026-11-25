---
name: security-response-red-purple-team
canonical_id: security.response.red_purple_team
aliases: [red-team-planning, purple-team-coordination, attack-coverage-mapping, mitre-attack-coverage, ttp-coverage]
version: 1.0.0
status: stable
created_date: 2026-06-14
allowed-tools: Read, Grep, Glob, Bash
forbidden-tools: Write, Edit, WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - MITRE ATT&CK: Enterprise (latest) — adversary TTP knowledge base
  - MITRE ATLAS: latest — adversarial threats to AI/ML systems
  - NIST CSF: 2.0 (DE Detect + RS Respond functions)
  - NIST SP 800-115: technical security testing & assessment (planning sections only)
  - OWASP ASVS: 5.0 (V16 Security Logging & Error Handling — detection evidence)
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "credentials.json"]
  never_write: ["raw secrets in coverage files", "real exploit payloads", "live target host inventories with credentials"]
  redact_on_output: ["tokens", "credentials", "PII", "internal IPs", "API keys"]
upstream:
  - appsec-security-orchestrator  # §16 evidence (sca/sast/code-review/headers/threat-model) feeds control+detection status
  - security-governance-threat-modeling  # STRIDE register + attack surface → which techniques are relevant
  - security-response-incident-response  # real-incident TTPs observed → map onto matrix
  - authorized-pentest-validation  # CONFIRMED red findings (only after manual ROE gate) → purple-team correlation
  - user (red/purple-team planning request)
downstream:
  - security-remediation  # detection/control gaps → fix + regression test
  - appsec-security-orchestrator  # attack-coverage evidence layer → release decision DE/RS coverage
  - security-viz  # render attack-coverage.yaml as a matrix diagram (ATT&CK Navigator-style)
  - pentest-scope-and-roe  # if gaps justify ACTIVE validation, hand the prioritized technique list to ROE drafting (manual path)
description: >-
  Red team / purple team PLANNING and COVERAGE MAPPING - strictly defensive, no execution. Maps the attack surface to MITRE ATT&CK Enterprise techniques (plus ATLAS for AI surfaces), scores control_status and detection_status from existing AppSec evidence, and emits attack-coverage.yaml via `appsec-sdk attack.coverage <tag>`. NEVER runs attacks, adversary emulation, stealth or persistence - active validation stays behind the manual `authorized-pentest-validation` gate.
trigger_phrases:
  - red team / 红队 / red-team planning
  - purple team / 紫队 / purple-team coordination
  - MITRE ATT&CK / ATT&CK coverage / ATT&CK Navigator
  - attack coverage matrix / TTP coverage / technique coverage
  - detection coverage / 检测覆盖 / detection gap analysis
  - adversary emulation planning (planning only — never execution)
  - MITRE ATLAS / AI attack coverage
---

# Security Response — Red Team / Purple Team (Planning + Coverage Mapping)

> **Execution mode: SKILL-direct, DEFENSIVE-ONLY.** This is a response-family
> planning skill. It reads existing evidence and writes ONE machine-readable
> fact-source — the ATT&CK coverage matrix — via `appsec-sdk attack.coverage <tag>`.
> It is **not** a pentest, **not** an attack runner, **not** a red-team C2.
> Active adversary validation is a separate, manual, ROE-gated path it never touches.

---

## ⛔ 0. HARD BOUNDARY (read this first — it is the whole point of the skill)

This skill is **PLANNING + COVERAGE MAPPING ONLY**. It maps which adversary
techniques are *relevant* to the project, and for each one records whether a
*control* and a *detection* already exist — sourced from evidence that other
defensive skills already produced. It then plans what blue-team detection /
control work should close the gaps.

| This skill DOES | This skill NEVER does |
|---|---|
| Inventory relevant MITRE ATT&CK / ATLAS techniques for the surface | Run any attack, exploit, payload, or adversary emulation |
| Assess `control_status` + `detection_status` per technique from existing evidence | Establish stealth, persistence, C2, or hands-on-keyboard access |
| Plan purple-team coordination (red findings ↔ blue detection) | Scan, fuzz, brute-force, or probe any live target |
| Produce `attack-coverage.yaml` via `appsec-sdk attack.coverage` | Write payloads / exploit code / live credentialed host inventories |
| Route detection/control gaps to `security-remediation` | Invoke / route-to / pre-stage `authorized-pentest-validation` |
| Hand a prioritized technique list to `pentest-scope-and-roe` (if active validation is justified) | Authorize, schedule, or kick off active validation itself |

**Charter alignment (CLAUDE.md §3 + rules/security-appsec.md):** the harness
**forbids** active adversary emulation / stealth / persistence outside the
manual pentest gate. Active validation is gated by **`authorized-pentest-validation`**
(`disable-model-invocation: true`, manual ROE + session sign-off, hook
`appsec-pentest-authorization.js`). **This skill never invokes that gate and is
not a step toward bypassing it.** If coverage analysis concludes that an actual
adversary simulation is warranted, the *only* legitimate next move is the
governed path: draft a ROE via `pentest-scope-and-roe`, get explicit human
sign-off, then a human manually runs `/authorized-pentest-validation`.

**Tool boundary:** `allowed-tools: Read, Grep, Glob, Bash`. There is **no Write**
to evidence — coverage is persisted exclusively through `appsec-sdk attack.coverage`
(same canonical-path discipline as every other AppSec finding/evidence writer;
direct Writes to `.appsec/**` are physically blocked by
`appsec-finding-schema-prewrite.js`). `Bash` is used to call `appsec-sdk` and to
grep evidence — **never** to run security tooling (active-scan binaries are
blocked by `appsec-active-scan-guard.js`; secret reads by
`appsec-secret-access-guard.js`).

---

## 1. Mission

Defensive coverage analysis is not "imagine how a hacker thinks" theater. This
skill produces a **structured, evidence-anchored ATT&CK coverage matrix**: for
the techniques an attacker would plausibly use against *this* surface, does the
project already have a *control* (prevent/reduce) and a *detection*
(see-it-happen)? Where it doesn't, that becomes prioritized blue-team work.

**职责边界**：
- **owns**: 相关 ATT&CK/ATLAS 技术清单、每条技术的 control/detection 覆盖判定、purple-team 协调计划（红队发现 ↔ 蓝队检测改进）、`attack-coverage.yaml` 事实源
- **hands off to remediation**: 每个 detection/control gap → `security-remediation`（按 finding schema 修复 + 回归测试）
- **hands off to ROE (manual)**: 若 gap 严重到需要*真实*对抗验证 → 把优先技术清单交 `pentest-scope-and-roe` 起草，人工签字后人工跑 `/authorized-pentest-validation`
- **renders via**: `security-viz` 把 coverage 画成矩阵图（ATT&CK Navigator 风格）
- **不做**: 任何 active emulation / exploit / stealth / persistence / 调用 active 工具或 pentest gate

**Why DE + RS (not just one CSF function):**
- **DE (Detect)** is the primary lens — `detection_status` per technique *is* the
  CSF DE evidence (anomalies/events, continuous monitoring, ASVS V16 logging).
- **RS (Respond)** is the second lens — coverage gaps drive response-readiness:
  which techniques would we currently *miss* mid-incident, and does an IR runbook
  step exist for the ones we'd catch.

---

## 2. Activation Triggers

| Trigger | Mode | Action |
|---|---|---|
| User asks for "red team planning" / "紫队" / "ATT&CK coverage" / "detection coverage" | Standalone | Run §4 workflow against active release tag |
| `appsec-security-orchestrator` release run wants DE/RS coverage evidence | Downstream of §16 | Build coverage from the run's evidence; persist via SDK |
| `security-governance-threat-modeling` finished a STRIDE register | After threat model | Map STRIDE entries + attack surface → relevant techniques |
| A real incident closed and IR produced observed TTPs | After incident-response | Map observed techniques onto matrix; flip detection_status where the incident proved a gap |
| **Authorized** pentest (manual gate already passed) produced CONFIRMED findings | Purple-team correlation | Correlate red findings ↔ blue detection on the shared matrix (§5) |
| Pre-release "are we blind to anything an attacker would try?" check | Standalone | Coverage map → gap list → remediation routing |

**Non-AppSec project guard:** if `<project-root>/.appsec/config.json` is absent,
this skill **silent-exits** (single log line, 0 side effects) — identical
discipline to the orchestrator §16.0 (the SDK has no evidence dir to write to).

---

## 3. Standards Mapping

| Standard | 适用范围 |
|---|---|
| **MITRE ATT&CK Enterprise** | The TTP taxonomy — every technique id/tactic in the matrix comes from here (attack.mitre.org). Source of `references/mitre-attack-web-techniques.md`. |
| **MITRE ATLAS** | Adversarial threats to AI/ML systems. Use for the AI/agent overlay (composes with `security-app-llm`): e.g. AML.T0051 prompt injection, AML.T0057 LLM data leakage, model evasion/extraction. |
| **NIST CSF 2.0 DE** | Detect function — `detection_status` per technique is the evidence for DE.AE (anomalies/events) + DE.CM (continuous monitoring). |
| **NIST CSF 2.0 RS** | Respond function — covered techniques must map to an IR runbook step; gaps are response blind spots. |
| **NIST SP 800-115** | Technical testing & assessment — **planning sections only** (test planning, rules of engagement, coordination). Execution sections are out of scope (that's the manual pentest gate). |
| **OWASP ASVS 5.0 V16** | Security logging & error handling — the control surface most `detection_status` assessments depend on. |

> **Naming note**: this skill uses **MITRE ATT&CK "TTP" = Tactics, Techniques,
> Procedures**. It is unrelated to the harness's "GEO" disambiguation. Keep
> ATT&CK (adversary behavior) separate from ASVS (control requirements) — a
> technique is mapped to *both* a control and a detection, never conflated.

---

## 4. Standard Workflow (5 steps — defensive coverage mapping)

> Pre-req: an active release tag exists (`appsec-sdk init <tag>` already ran in
> the orchestrator). This skill writes into that tag's evidence dir via the SDK.

```
Step 1  INVENTORY relevant techniques (scope the matrix to THIS surface)
        → Read the surface signals (do NOT guess):
            • .appsec/state.json → overlays[] (api / multitenant / file_upload /
              llm / payment / websocket / mobile / cn_data / privacy), asvs_level
            • .appsec/evidence/<tag>/threat-model/ → STRIDE register + attack surface
            • package manifests / framework markers (web / api / cloud / identity / AI)
        → Select the relevant ATT&CK tactics+techniques from
          references/mitre-attack-web-techniques.md, keyed by surface:
            • Always (web/api SaaS): Initial Access, Credential Access, Execution,
              Persistence, Priv-Esc, Defense Evasion, Discovery, Collection/Exfil, Impact
              # ATT&CK Enterprise v19 (2026-04-28, verified) = 15 tactics: "Defense Evasion"
              #   (TA0005) split into "Stealth" (TA0005) + "Defense Impairment" (TA0112).
              #   Prefer v19 tactic names or version-pin. (ATLAS still uses "Defense Evasion".)
            • +cloud   → T1530 (Data from Cloud Storage), T1567 (Exfil over Web), cloud IAM techniques
            • +identity/auth → T1078 (Valid Accounts), T1110 (Brute Force), T1098 (Account Manipulation)
            • +file_upload → T1505.003 (Web Shell), T1190 (Exploit Public-Facing App)
            • +llm/agent → ALSO pull MITRE ATLAS techniques (prompt injection / data leakage /
              model evasion) — note them under a separate atlas: block; compose with security-app-llm
        → Mark each `relevant: true|false`. Irrelevant techniques stay in the file
          as `relevant: false` (honesty: "we considered it and it doesn't apply"),
          they are NOT silently dropped.

Step 2  ASSESS control_status + detection_status per technique (from EXISTING evidence)
        → For EACH relevant technique, read what the defensive skills already proved.
          Use references/mitre-attack-web-techniques.md "typical control" + "typical
          detection signal" columns as the rubric for WHAT would count as coverage.
        → control_status   ∈ {none | partial | covered}
            covered  = a real, evidenced control exists (e.g. WAF rule + input
                       validation finding closed for T1190; MFA + lockout for T1110)
            partial  = control exists but incomplete / not on all surfaces
            none     = no control evidence found
        → detection_status ∈ {none | partial | covered}
            covered  = a real detection signal exists (e.g. auth-failure-rate alert
                       for T1110; egress-volume alert for T1567; FIM/web-root-write
                       alert for T1505.003), backed by logging (ASVS V16) evidence
            partial / none likewise
        → evidence_ref: point at the concrete artifact that justifies the status
          (e.g. ".appsec/findings/<tag>/2026-..-sast-003.yaml",
           ".appsec/evidence/<tag>/code-review/...", "monitoring/alerts/auth.yml").
          NO evidence_ref → status MUST be `none` (no honest claim without proof).
        → NEVER fabricate coverage. "We probably log that" is `none`, not `partial`.

Step 3  PERSIST coverage via `appsec-sdk attack.coverage <tag>`
        → Build the YAML in the schema below (matches templates/attack-coverage-template.yaml
          and the SDK skeleton at appsec-sdk.sh cmd_attack_coverage):
            attack_coverage:
              framework: "MITRE ATT&CK Enterprise"      # add an atlas: block for AI surfaces
              techniques:
                - id: T1190
                  tactic: Initial Access
                  relevant: true
                  control_status: partial
                  detection_status: none
                  evidence_ref: ".appsec/evidence/<tag>/code-review/..."
                - ...
        → Pipe it through the SDK (canonical write path; redacts at write-time):
            cat coverage.yaml | bash ~/.claude/scripts/appsec-sdk.sh attack.coverage <tag> -
          (or pass a file arg). Writes →
            .appsec/evidence/<tag>/attack-coverage/attack-coverage.yaml
        → DO NOT Write to .appsec/** directly — the prewrite hook blocks it; the SDK
          is the only sanctioned writer. (allowed-tools has no Write for this reason.)

Step 4  PURPLE-TEAM IMPROVEMENT PLAN (gaps → blue-team work, routed)
        → Derive the gap list: every relevant technique where
          detection_status != covered OR control_status != covered.
        → Prioritize by: tactic criticality × exploit likelihood (from threat model)
          × business impact of the affected asset. Initial Access + Credential Access
          + Impact on payment/auth/data assets rank highest.
        → For each gap, produce a remediation task and ROUTE to `security-remediation`:
            • Detection gap  → "add/Tune detection: <signal>" (e.g. alert on auth
              failure rate spike → T1110), with the ASVS V16 logging requirement it needs.
            • Control gap    → "add/strengthen control: <control>" (e.g. enforce MFA,
              add CSP, lock down web-root writes → T1505.003).
          Each task carries the technique id + evidence_ref so remediation is traceable.
        → Detection improvements are framed as BLUE-team work (logging, alerting,
          monitoring, hardening) — never "go attack it to prove the gap."

Step 5  ATT&CK NAVIGATOR LAYER EXPORT (optional, defensive visualization)
        → The attack-coverage.yaml is the fact-source for two renderings:
            (a) `security-viz` renders it as a coverage matrix diagram (heat by
                detection_status: none=red, partial=amber, covered=green).
            (b) A standard MITRE ATT&CK Navigator layer JSON can be generated FROM
                attack-coverage.yaml (techniqueID + score + color per technique) so
                teams can view it in the public Navigator. This is a presentation
                artifact only — it carries NO live target data, NO payloads.
        → Note in the coverage file's header which renderings were produced and where.
```

---

## 5. Purple-Team Coordination (red findings ↔ blue detection on one matrix)

Purple teaming is the discipline of putting **what an attacker did/could do (red)**
and **what defenders can see/stop (blue)** on the *same* ATT&CK matrix so the
output is concrete detection improvement — not a score, not a trophy.

In this harness, the matrix is `attack-coverage.yaml`, and the two inputs are:

| Side | Source (in this harness) | Maps to matrix field |
|---|---|---|
| **RED** (techniques an adversary used / would use) | Threat model (planned), `security-app-*` overlay abuse cases, and — **only after the manual gate** — CONFIRMED findings from `authorized-pentest-validation` | which techniques get `relevant: true`; a confirmed red finding *downgrades* the implied `control_status` if it bypassed the control |
| **BLUE** (what we detect / prevent) | `appsec-security-orchestrator` evidence (code-review, headers, SAST), logging/monitoring config (ASVS V16), IR runbook detection rules | `control_status` + `detection_status` |

**Coordination loop (defensive framing):**

```
1. RED input arrives (planned abuse case OR authorized-pentest CONFIRMED finding).
2. Locate the matching technique id in attack-coverage.yaml (or add it, relevant: true).
3. BLUE answers honestly: did we PREVENT it (control), did we SEE it (detection)?
      - Authorized pentest confirmed exploitation succeeded → control_status downgraded
        to partial/none for that technique + a finding routed to security-remediation.
      - Pentest tried it and our alert fired → detection_status: covered, with the
        alert as evidence_ref (this is the GOOD purple-team outcome: validated detection).
4. Every "RED succeeded AND BLUE was blind" cell = top-priority gap → §4 Step 4.
5. Re-render (§4 Step 5) so the improvement is visible on the matrix.
```

**Iron rule for purple-team correlation:** red findings may only enter this loop
from **(a)** planning artifacts (threat model / abuse cases — no execution), or
**(b)** an **already-authorized** pentest whose ROE + sign-off + hook checks
passed. This skill **does not** generate red findings by attacking anything, and
**does not** request authorization. It only *correlates* findings that the
governed path legitimately produced.

---

## 6. Relationship to neighboring skills (no overlap)

| Skill | Boundary |
|---|---|
| **`security-viz`** | Renders `attack-coverage.yaml` as a matrix/heatmap diagram. This skill produces the *facts*; `security-viz` produces the *picture*. This skill does not draw; `security-viz` does not assess coverage. |
| **`pentest-scope-and-roe`** | The ACTIVE-validation on-ramp. If §4 Step 4 concludes a gap warrants real adversary simulation, this skill hands the prioritized technique list to `pentest-scope-and-roe` to draft an ROE. That skill (and the manual `authorized-pentest-validation` after it) owns execution; this skill never does. |
| **`authorized-pentest-validation`** | The manual hard gate (`disable-model-invocation: true`). This skill **never** invokes, routes-to, or pre-stages it. It only *consumes* confirmed findings the gate already produced (§5). |
| **`security-governance-threat-modeling`** | Produces the STRIDE register + attack surface that scopes which techniques are `relevant` (§4 Step 1). Threat modeling = "what could go wrong by design"; this skill = "which adversary TTPs map to it + do we detect them." |
| **`security-app-llm`** | Owns AI-surface security review. This skill *composes* with it for the MITRE ATLAS overlay (AI techniques in a separate `atlas:` block), but does not duplicate its LLM control review. |
| **`security-remediation`** | Receives the detection/control gap tasks (§4 Step 4) and implements fixes + regression tests against the finding schema. This skill plans; remediation fixes. |
| **`appsec-security-orchestrator`** | The parent. `attack-coverage.yaml` is an evidence layer the orchestrator's §16.9 validator can fold into DE/RS coverage of the release decision. |

---

## 7. Output Contract

Every run produces exactly one persisted artifact plus routed tasks:

1. **`attack-coverage.yaml`** → `.appsec/evidence/<tag>/attack-coverage/` (via
   `appsec-sdk attack.coverage <tag>` — the ONLY write path). Conforms to the §4
   Step 3 schema; populated from `templates/attack-coverage-template.yaml`.
2. **Purple-team gap list** → remediation tasks routed to `security-remediation`,
   each tagged with technique id + evidence_ref.
3. **(Optional) Navigator layer / `security-viz` diagram** reference noted in the
   coverage file header (presentation only — no live data, no payloads).
4. **(Conditional) ROE hand-off** to `pentest-scope-and-roe` *iff* a gap justifies
   active validation — a prioritized technique list, NOT an authorization.

The coverage file is read back by:
- `appsec-security-orchestrator` §16.9 validator → DE/RS coverage in the release decision.
- `security-viz` → matrix diagram.

---

## 8. Hard Rules

- ❌ **不**执行任何 attack / exploit / payload / adversary emulation（这是 planning skill）
- ❌ **不**做 stealth / persistence / C2 / hands-on-keyboard
- ❌ **不**扫描 / fuzz / brute-force / probe 任何 live target（active-scan binaries 被 hook 物理拦）
- ❌ **不** invoke / route-to / pre-stage `authorized-pentest-validation`（manual 硬门完全不动）
- ❌ **不**自己申请授权 —— active 验证的授权 100% 走人工 ROE + session sign-off
- ❌ **不**直接 Write 到 `.appsec/**`（必须走 `appsec-sdk attack.coverage`；prewrite hook 物理拦）
- ❌ **不**编造 coverage：无 `evidence_ref` 的技术 `control_status`/`detection_status` 必须是 `none`
- ❌ **不**把 `relevant: false` 的技术悄悄删掉（保留 = 诚实地"考虑过且不适用"）
- ❌ **不**把 detection gap 描述成"去打它来证明" —— 一律 framed 为 blue-team logging/alerting/hardening 工作
- ❌ **不**在 coverage 文件里放 raw secret / 真实 exploit payload / 带凭证的 live host 清单
- ❌ **不**用 MITRE ATT&CK 当"how-to attack" 手册 —— 它是 defensive coverage taxonomy

---

## 9. Anti-patterns

- ❌ "Let's red-team it" → 真去打靶 —— 本 skill 是 coverage mapping，不是 attack runner；真打靶走 manual pentest gate
- ❌ 把"我们应该能记到这个 log"标成 `partial` —— 没 evidence_ref 就是 `none`
- ❌ 只标 `control_status` 不标 `detection_status` —— 两者必须都判（DE lens 是核心）
- ❌ 给 coverage 打一个总分（"我们覆盖 73%"）当成结论 —— 价值在 per-technique gap，不在虚荣指标
- ❌ 把 ATLAS（AI）技术混进 ATT&CK Enterprise 主表 —— AI 技术放独立 `atlas:` block，compose with security-app-llm
- ❌ 把所有技术无脑标 `relevant: true` —— 必须按 surface 裁剪（scope to THIS project）
- ❌ 把 Navigator layer / 矩阵图当成交付终点 —— 图是给人看的，gap → remediation 才是动作
- ❌ 让本 skill 成为绕过 pentest gate 的"软入口" —— 它消费已授权的发现，绝不生产新攻击

---

## 10. References

- [MITRE ATT&CK Enterprise](https://attack.mitre.org/matrices/enterprise/) — TTP taxonomy (source of every technique id/tactic)
- [MITRE ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) — defensive coverage visualization (layer export target)
- [MITRE ATLAS](https://atlas.mitre.org/) — adversarial threats to AI/ML systems (AI overlay)
- [NIST CSF 2.0 DE + RS Functions](https://www.nist.gov/cyberframework) — Detect + Respond
- [NIST SP 800-115 Technical Testing & Assessment](https://csrc.nist.gov/pubs/sp/800/115/final) — planning sections only
- [OWASP ASVS 5.0 V16 Security Logging](https://owasp.org/www-project-application-security-verification-standard/) — detection control basis
- [references/mitre-attack-web-techniques.md](references/mitre-attack-web-techniques.md) — curated technique → control + detection rubric (fill the matrix without external lookup)
- [templates/attack-coverage-template.yaml](../appsec-security-orchestrator/templates/attack-coverage-template.yaml) — pre-populated coverage template
- [appsec-security-orchestrator §17.1 `attack.coverage`](../appsec-security-orchestrator/SKILL.md) — canonical persist command (enterprise module #14)
- [pentest-scope-and-roe](../pentest-scope-and-roe/SKILL.md) — ACTIVE-validation on-ramp (manual)
- [authorized-pentest-validation](../authorized-pentest-validation/SKILL.md) — manual hard gate (never invoked by this skill)
- [security-governance-threat-modeling](../security-governance-threat-modeling/SKILL.md) — scopes relevant techniques
- [security-remediation](../security-remediation/SKILL.md) — receives gap → fix tasks
