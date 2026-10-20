---
name: dast-authenticated
canonical_id: security.app.dast.authenticated
aliases: [authenticated-dast, dast-auth, logged-in-dast, zap-authenticated]
version: 1.0.0
status: stable
created_date: 2026-06-15
allowed-tools: Read
forbidden-tools: Write, Bash, WebFetch
manual_gate_required: true
disable-model-invocation: false
standards_versions:
  - OWASP ZAP Automation Framework: latest (YAML-as-code, authentication contexts)
  - OWASP WSTG: Authentication / Session Management / Authorization testing
  - OWASP ASVS: 5.0 (v5.0.0-3 session, v5.0.0-4 access control, v5.0.0-5 validation, v5.0.0-13 configuration)
  - OWASP API Security Top 10: 2023 (authenticated API surface)
  - NIST SP 800-115: §7 Target Identification & Analysis (active testing under authorization)
  - PTES: Vulnerability Analysis (phase 4) — authenticated active scan layer (scoping reference only)
  - OSSTMM: 3 (Rules of Engagement #6/#14/#17 — authenticated active stays under ROE)
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "production credentials", "real user passwords"]
  redact_on_output: ["session cookies / tokens from scan", "auth headers", "test-account credentials", "PII in responses", "bearer tokens", "CSRF tokens"]
upstream:
  - appsec-security-orchestrator
  - pentest-scope-and-roe (完整 ROE must exist first — 双门第一道)
  - dast-baseline-scanning (passive baseline should run first)
  - security-pentest-recon-scan (recon/scan before authenticated active)
downstream:
  - security-remediation (HIGH+ findings)
  - authorized-pentest-validation (manual hard gate — exploitation upgrade path; 双门第二道)
  - appsec-sdk (evidence persist: dast layer)
description: >-
  Authenticated / logged-in DAST planning — an OWASP ZAP Automation Framework authenticated scan (browser auth context, spider, scan) and Nuclei-with-session against AUTHORIZED staging / preview / lab targets only, reaching post-auth surface that passive baseline cannot. RED-LINE: planning-first + DOUBLE-GATE. HARD-REQUIRES a completed `.planning/PENTEST-ROE.md`, in-scope target, active window and explicit human authorization before any authenticated step. Wrapper-only, raw ZAP/Nuclei CLI FORBIDDEN, never auto-scans, no production, no destructive or DoS action. References `dast-baseline-scanning` and the `authorized-pentest-validation` gate, never bypassing them. Triggers: "authenticated DAST / 登录态扫描 / logged-in scan / authenticated ZAP scan / 认证后扫描 / post-auth DAST / session-based scan".
---

# SKILL: dast-authenticated

> **RED-LINE skill — planning / Read-only by design.** Like `pentest-scope-and-roe`
> and `security-pentest-recon-scan`, this skill reads, plans, and explains; the
> project's validated-wrapper scripts run the scan and `appsec-sdk` persists
> evidence. It sits **between** passive `dast-baseline-scanning` and full
> exploitation, and is governed by the **same double-gate** as active pentest:
> a completed ROE (`pentest-scope-and-roe`) + a manual hard gate
> (`authorized-pentest-validation`). It **never** auto-scans and **never** bridges
> to exploitation on its own.

---

## 1. Mission

为**已授权**的 staging / preview / lab 目标提供**登录态（authenticated）DAST** 的**包装化调用**指导：

- **ZAP Automation Framework**（YAML-as-code `plan.yaml`）：authentication context（browser-based auth 优先）+ spider/ajax-spider 爬取 **post-auth** 页面 + scan
- **Nuclei with session**：带认证 header/cookie 的模板化扫描，覆盖登录后接口

**为什么需要它**（与 passive baseline 的差别）：passive `dast-baseline-scanning` 只在**未登录**视角做 spider + passive 检测，碰不到登录后的攻击面（用户面板 / 越权 / 认证后表单 / 会话管理）。authenticated DAST **登录后**驱动 scanner，能覆盖 post-auth surface —— 这天然比 baseline **更主动**，因此提级到**红线 + 双门**纪律，而**不**改 `dast-baseline-scanning`（其名字 safety-frozen，passive-only 边界不动）。

**永不**做以下任何一项：
- ❌ 自动扫描（任何步骤都须先过 §3 双门前置；NEVER auto-scans）
- ❌ 对 **production** 目标扫描（authenticated active 在生产 = 高风险，默认硬拒）
- ❌ 对未授权 / 第三方 / SaaS 控制面目标扫描
- ❌ destructive / DoS / 资源耗尽 / 压力测试
- ❌ exploitation / 实际利用 / PoC 注出数据（→ `authorized-pentest-validation`，manual 硬门）
- ❌ raw free-form ZAP / Nuclei CLI 调用（必须走 wrapper）
- ❌ persistence / 横向移动 / 数据带出 / stealth
- ❌ 自动升级为 active exploitation（升级 100% 手动）

---

## 2. 三层 DAST 谱系（本 skill 的精确定位）

| 层 | Skill | 视角 | 行为 | 门 |
|---|---|---|---|---|
| **Passive baseline** | `dast-baseline-scanning` | **未登录** | spider + passive scan，零攻击 payload | 简化 ROE（target + 授权 + 时间窗）|
| **Authenticated（本 skill）** | `dast-authenticated` | **登录态** | auth context + spider post-auth + scan（覆盖认证后面）| **完整 ROE + 双门**（更主动 → 提级）|
| **Active exploitation** | `authorized-pentest-validation` | 登录态 + 主动利用 | 实际 PoC / 漏洞验证 | **manual 硬门**（disable-model-invocation: true）|

> 本 skill 是中间层：比 baseline 主动（登录后驱动 scanner），但**不越** active exploitation 红线（不实际利用/注出）。ZAP Automation Framework 的 **active scan** 能力本身能发攻击 payload —— 本 skill 的 wrapper 把它约束在"authenticated spider + 受控 scan policy"，**任何实际利用验证仍须**手动 `/authorized-pentest-validation`。

---

## 3. 双门前置（DOUBLE-GATE — 任何 authenticated 步骤之前全部确认）

本 skill 是红线 skill，沿用 active pentest 的**双门**，**不放宽** `pentest-scope-and-roe` / `authorized-pentest-validation` 的任何要求：

### 3.1 第一道门 — 完整 ROE（`pentest-scope-and-roe` 产出）

authenticated DAST 触登录后攻击面，**须完整 11 项 ROE**（不是 baseline 的简化版）：

- [ ] `.planning/PENTEST-ROE.md` 已存在且**完整**（11 项 checklist 全填，§4.3 sign-off 由**有签字权**代表完成 — 见 ROE §3.6.3，非 IT 联系人）
- [ ] Target 在 ROE **in-scope[]** 精确列表内（URL / IP CIDR / domain）
- [ ] Target **不**在 production（authenticated active 默认硬拒生产；除非 ROE 明确授权 production + 隔离环境 + 二次书面确认 + 独立 grantor sign-off）
- [ ] Target **不**是第三方 / SaaS 控制面（Auth0 / Okta / Cognito / Supabase managed / Firebase Auth 等 —— 即使"看起来是 user 的登录"，托管认证面不在 user 授权范围）
- [ ] 当前时间在 ROE **time_window** 内（含 permitted hours / blackout periods）
- [ ] ROE §4 Allowed methods 已勾选 **"Authenticated testing with dedicated test accounts"**（authenticated 是 ROE §4 明列项；未勾 → 停）
- [ ] ROE §4 已为本次**技术层 L2 主动扫描**勾选授权（authenticated spider + scan 属 L2；exploitation L3/L4 **不**在本 skill）
- [ ] 速率上限已定（§5）+ 触发 WAF/IDS/告警的停止条件已定（ROE §7 / §10）
- [ ] 报告 / evidence 输出路径已定（不输出到项目 src 内）

### 3.2 第二道门 — explicit human authorization（本 session）

除 ROE 落盘外，authenticated active 须用户**在本 session 显式授权**（不依赖跨 session memory）：

- [ ] 用户在**本次对话**给出 explicit 授权文本，含明确意图，例如：
  > "I authorize an authenticated DAST scan on `<in-scope-staging-URL>` per the ROE in `.planning/PENTEST-ROE.md`, within the active window."
- [ ] 该授权针对**具体 in-scope target**，不是泛化"你看着办 / 都谈过了 / 快点扫"
- [ ] 用户理解这是 authenticated（登录态）扫描，会触达 post-auth 攻击面

> **双门关系**：第一道（ROE 落盘）是 paperwork；第二道（session explicit authorization）是 act。两道都过才能进 §6 工作流。**任一缺失或含糊 → 停止**，回 `pentest-scope-and-roe`，**不**讨论 scan 细节。

### 3.3 与 enforcement 的关系（instruction + hook 叠加，不替代）

本 skill 的 §3 是 **instruction-layer** 前置。production hosts 即使有 ROE 也由 `appsec-security-orchestrator §18.6` 的 PreToolUse hook **hard-deny**（命令含 zap/nuclei + target 在 `production_hosts[]` → 物理拦截）。两者叠加。本 skill **不**重新发明任何 gate —— 它**引用**既有的 ROE skill + 既有的 hard gate skill + 既有的 hook，全部 frozen-name。

---

## 4. Recon / baseline before authenticated active（顺序铁律）

**绝不**第一步就 authenticated active scan。严格按谱系逐层升级，前一层产出/确认喂后一层：

```
Stage 0 (passive baseline)  dast-baseline-scanning   → 未登录视角 passive 发现 + 攻击面初判
Stage 1 (recon/scan)        security-pentest-recon-scan → 授权 recon + non-intrusive 模板扫（如适用）
   │  ── 双门前置全过（§3.1 ROE + §3.2 session authorization）──
Stage 2 (auth context)      经 wrapper 配 ZAP auth context（browser-based auth：loginUrl + 专用 test 账号）
Stage 3 (auth spider)       经 wrapper 登录态 spider/ajax-spider 爬 post-auth 页面（仅 in-scope）
Stage 4 (controlled scan)   经 wrapper 受控 scan policy（authenticated）；nuclei-with-session 覆盖登录后接口
   │
   └─►  findings → appsec-sdk evidence (dast 层) → 路由 security-remediation
        需要实际利用验证（注出数据 / PoC）？ → 停。手动 /authorized-pentest-validation（不在本 skill）
```

**逐层铁律**：
- Stage 0/1（passive/recon）授权 **≠** Stage 2-4（authenticated active）授权。ROE §4 必须分别勾选。
- 每个 Stage 开始前**重新确认** §3（尤其 in-scope + time window + session authorization 仍有效）。
- authenticated active 暴露疑似漏洞 → **不**就地"试一下能不能利用"。那是 exploitation（L3）→ 手动 `/authorized-pentest-validation`。

---

## 5. Wrapper 设计（核心安全边界 — 与 dast-baseline-scanning 完全一致的家族纪律）

**不直接调用 raw ZAP / Nuclei CLI。** 项目必须自带 wrapper（脚本 / npm script），由 wrapper 固定安全行为。本 skill 只**指导** wrapper 长什么样，不自己运行（Read-only），与 `dast-baseline-scanning` §4 + `security-pentest-recon-scan` §5 同源。

### 5.1 每个 wrapper 必须强制

- **Target allowlist**：只允许 ROE in-scope[] / config 声明的 staging/preview/lab URL；wrapper 启动先比对 allowlist，不在表内 → 拒绝退出
- **Non-production 硬标志**：wrapper 检测 target 命中 `production_hosts[]` → 直接拒（与 §18.6 hook 双保险）
- **Authenticated scan = 受控 scan policy**：把危险/破坏性 active 规则写死为安全/禁用值，不暴露给调用方自由拼接（避免误开 full active 攻击）
- **专用 test 账号**：auth context 只用 ROE §8 声明的 dedicated test account，**绝不**用真实用户/admin 凭据；凭据经环境变量/secrets-manager 注入，**不**进 LLM context、**不**进 repo
- **参数校验**：target / loginUrl 必须匹配严格 pattern（拒注入 / 拒 shell 元字符）
- **速率上限**：rate-limit / concurrency / delay / spider 深度 写死或 clamp（防压垮目标 = OSSTMM #14/#30）
- **超时 cap**：wall-clock 上限（authenticated scan 比 baseline 久，建议 ≤30-45 分钟并 clamp）
- **输出目录隔离**：report 写到 `./security/dast-auth/`，不进 src
- **Session 隔离**：scan 用的 session token / cookie 仅存于 report 输出区，输出前经 redact

### 5.2 推荐 wrapper 形态（示意 — 由项目实现，本 skill 不落盘）

```bash
# Authenticated ZAP（Automation Framework plan.yaml 驱动，browser-based auth）
scripts/security/zap-authenticated.sh \
  --plan=./security/dast-auth/plan.yaml \
  --target=<in-scope-staging-URL> \
  --report=./security/dast-auth/auth-report.html
# Nuclei with session（带认证 header/cookie，受 allowlist + 速率约束）
scripts/security/nuclei-authenticated.sh \
  --target=<in-scope-staging-URL> \
  --session=./security/dast-auth/session.txt \
  --severity=low,medium,high,critical
```

wrapper 内部固定安全行为（ZAP：scan policy 禁危险 active 规则、`-config` 速率/超时、auth context 只读 dedicated 账号；nuclei：`-rate-limit` / `-timeout` / `-no-interactsh`（除非 ROE 授权 OOB）），调用方**改不动**。

### 5.3 ZAP Automation Framework `plan.yaml`（authenticated context 示意）

ZAP Automation Framework 用声明式 YAML 描述 context + auth + jobs。authenticated 关键 = `authentication` 段（browser-based auth 只需 loginUrl + 凭据，firefox-headless 默认）：

```yaml
# security/dast-auth/plan.yaml  —— 示意；凭据用环境变量占位，绝不硬编码
env:
  contexts:
    - name: app-staging
      urls: ["https://staging.example.test"]   # ← 仅 ROE in-scope staging
      includePaths: ["https://staging.example.test/.*"]
      excludePaths: ["https://staging.example.test/logout.*"]   # 避免扫到自己登出
      authentication:
        method: browser                          # browser-based auth：最省配置
        parameters:
          loginPageUrl: "https://staging.example.test/login"
          loginPageWait: 5
      sessionManagement:
        method: headers                          # 或 cookie，按应用而定
      users:
        - name: test-user
          credentials:
            username: "${DAST_TEST_USER}"        # ← 环境变量，dedicated test 账号
            password: "${DAST_TEST_PASS}"        # ← 绝不写明文，绝不用真实账号
jobs:
  - type: spider                                 # 登录态 spider 爬 post-auth 页面
    parameters: { context: app-staging, user: test-user, maxDuration: 10 }
  - type: spiderAjax                             # SPA 需要时
    parameters: { context: app-staging, user: test-user, maxDuration: 10 }
  - type: passiveScan-wait
  - type: activeScan                             # ← 受控 scan policy（wrapper 已禁危险规则）
    parameters: { context: app-staging, user: test-user, policy: "controlled-auth" }
  - type: report
    parameters:
      template: traditional-html
      reportDir: ./security/dast-auth/
```

> **凭据纪律**：`plan.yaml` 里凭据**只能**是 `${ENV_VAR}` 占位；wrapper 从环境/secrets-manager 注入 dedicated test 账号。明文凭据进 `plan.yaml` / repo / chat = 红线违规。

### 5.4 CLI 安装命令（命令留档，实装以各 repo 当下 README 为准 — 版本号别写死）

> 安装是 user / 项目环境的事，本 skill 不自动装。跨平台（Windows / macOS / Linux）均可用 Docker 或预编译。

| CLI | 用途 | 安装（命令留档） | 许可 |
|---|---|---|---|
| **OWASP ZAP** | Automation Framework authenticated scan | Docker `ghcr.io/zaproxy/zaproxy:stable`（含 Automation Framework + firefox-headless）；或桌面版 + `zap.sh -cmd -autorun plan.yaml` | Apache-2.0 (OWASP) |
| **Nuclei** | 带 session 的模板化扫描 | `go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest`（需 Go ≥ 1.24.x；或 release 二进制）| MIT (ProjectDiscovery) |

> ZAP `zaproxy/action-af` GitHub Action 可在 CI 跑 Automation Framework；CI 中**只**对受控 staging/preview 跑，且默认不对外部 URL（同 `dast-baseline-scanning` §8 铁律）。
> **Windows 提示**：用 Docker Desktop 或 Git-Bash / PowerShell；wrapper 脚本建议 POSIX sh + 在 PowerShell 下 `bash scripts/...`。

### 5.5 settings.json 权限建议（项目级，name-based deny 防路径前缀绕过）

```jsonc
{
  "permissions": {
    "allow": [
      "Bash(bash scripts/security/zap-authenticated.sh *)",
      "Bash(bash scripts/security/nuclei-authenticated.sh *)"
    ],
    "deny": [
      "Bash(*zap-full-scan.py*)",
      "Bash(*zap-api-scan.py*)",
      "Bash(docker run *zap*full*)",
      "Bash(*nuclei*-itags*)"
    ]
  }
}
```

> deny-list 是 best-effort defense-in-depth；真正的控制是 **wrapper allowlist + §3 双门前置 + §18.6 hook**。raw `zap.sh` / `zap-full-scan.py` / `nuclei` 直接调用不进 allow（默认走 `ask`，且 wrapper 才是 canonical 路径）。这与 `dast-baseline-scanning` §4 的 deny-list 同源 —— 本 skill 不放宽其中任何一条。

---

## 6. 工作流（8 步）

```
Step 1 — 逐条确认 §3.1 第一道门（完整 ROE）。缺任一 → 回 pentest-scope-and-roe，不继续
Step 2 — 确认 §3.2 第二道门（本 session explicit human authorization + 具体 in-scope target）
Step 3 — 确认 Stage 0/1 已做（passive baseline / recon）或 user 显式知情跳过的理由；authenticated ≠ 第一步
Step 4 — 指导项目配 ZAP auth context（plan.yaml，browser-based auth，dedicated test 账号 via env）
Step 5 — 经 zap-authenticated wrapper 跑登录态 spider/ajax-spider（仅 in-scope，受深度/速率约束）
Step 6 — 经 wrapper 跑受控 authenticated activeScan + nuclei-with-session（受控 policy，禁危险规则）
Step 7 — 解释结果（按 severity 分类）；findings 经 appsec-sdk 持久化（dast 层，过 redact）
Step 8 — 路由：HIGH+ → security-remediation；需实际利用验证（注出/PoC）→ 提示用户手动 /authorized-pentest-validation
         （本 skill 绝不自动跳转，绝不就地利用）
```

> 每个 Stage 失败 / 触发 WAF/IDS 告警 → 按 ROE §10 立即停止 + 通知紧急联系人。
> Step 1-3 是 Read/planning（本 skill 做）；Step 4-6 的实际执行由 **wrapper** 跑、Step 7 evidence 由 **appsec-sdk** 写 —— 本 skill 不自己 Bash、不自己 Write。

---

## 7. Finding / Evidence（接 appsec-sdk，schema v1.0 兼容）

authenticated DAST 产出经 `appsec-sdk` 写入 evidence sink（**过 redact**，绝不在 chat / log / report 出 raw session token / 凭据 / PII）。findings 必须符合 orchestrator **§9 Standardized Finding Schema v1.0**：

```bash
# 扫描阶段证据（ZAP / nuclei authenticated 输出）
appsec-sdk evidence.append <tag> dast ./security/dast-auth/auth-report.json
# 单条 finding（schema v1.0）
appsec-sdk redact < raw-finding.yaml | appsec-sdk finding.add -
```

本 skill findings 的 schema v1.0 关键字段约定（与 §9 一致，不 fork）：

| 字段 | 本 skill 取值 |
|---|---|
| `source` | `dast`（authenticated DAST 属 dast 源，与 baseline 同源类型）|
| `detector` | `zap@<ver>` / `nuclei@<ver>`（带版本）|
| `csf_function` | 多为 `DE`（detection）或 `PR`（暴露的可加固项）|
| `asvs_mapping` | `^v5\.0\.0-\d+\.\d+\.\d+$`（认证后常见：v5.0.0-3.x session / v5.0.0-4.x access control / v5.0.0-5.x validation）；无诚实映射则空 `[]` + 填 `unmapped_reason`（禁编造）|
| `owasp_top10` | `[A<n>:2025]`（如越权 A01 / 注入 A03）|
| `api_top10` | 认证后 API 面命中时填（如 `[API1]` BOLA / `[API5]` BFLA）|
| `reproduction_steps` | 仅 in-scope；**不得含 raw secret / session token**（经 redact）|
| `evidence.log_excerpt` | 必须走 `appsec-sdk redact` |

> 直接 Write 到 `.appsec/findings/**` 会被 PreToolUse hook（orchestrator §18.5）拒绝 —— canonical 路径是 `appsec-sdk finding.add`。evidence 工件规范（六类 + SHA256 + 写保护 + 访问日志）详 `appsec-security-orchestrator §17`（dast 层）。

---

## 8. Hard Rules

- ❌ **NEVER auto-scans** —— 任何 authenticated 步骤前必须过 §3 双门（完整 ROE + 本 session explicit authorization）
- ❌ 不在 §3 双门全部确认前讨论 scan 细节 / 配 plan.yaml
- ❌ 不对 **production** 目标做 authenticated active 扫描（默认硬拒；例外须 ROE 明授 + 隔离 + 二次书面确认 + 独立 grantor）
- ❌ 不对未授权 / 第三方 / SaaS 托管认证面（Auth0 / Okta / Cognito / Supabase managed / Firebase）扫描
- ❌ 不直接调用 raw ZAP / Nuclei CLI（必须走 wrapper）
- ❌ 不开启破坏性 / DoS / 资源耗尽 / full active 攻击模式（wrapper 用受控 scan policy）
- ❌ 不用真实用户 / admin 凭据做 auth context（只用 ROE §8 dedicated test 账号，经 env 注入）
- ❌ 不把凭据 / session token 写进 plan.yaml / repo / chat / log / report（明文凭据 = 红线违规；必经 redact）
- ❌ 不做 exploitation / PoC 利用 / 注出数据（→ `authorized-pentest-validation`，manual 硬门）
- ❌ 不自动把 scan 发现升级为利用尝试（升级 100% 手动）
- ❌ 不做 persistence / 横向移动 / 数据带出 / stealth / anti-forensics
- ❌ 不跳过 passive/recon 直接 authenticated active（谱系铁律：baseline/recon 先行）
- ❌ 不改名 / 不绕过 / 不弱化 `dast-baseline-scanning` 与 `authorized-pentest-validation`（frozen names = control surface）
- ❌ 本 skill 不自己 Write 盘 / 不自己跑 Bash / 不 WebFetch（Read/planning-only；wrapper + appsec-sdk 才执行）

---

## 9. 与上下游接口

| 方向 | Skill / Agent | 说明 |
|---|---|---|
| 上游 | `pentest-scope-and-roe` | **完整** ROE 必须先完成（本 skill §3.1 验证其产物 —— 双门第一道）|
| 上游 | `appsec-security-orchestrator` | 决定是否进入 authenticated DAST（backend/API/auth 项目 + 授权）|
| 上游/前置 | `dast-baseline-scanning` | passive baseline 应先跑（Stage 0）；本 skill 是其**更主动**的中间层，**不**改它、**不**抢它的 passive 工 |
| 平级 | `security-pentest-recon-scan` | 同属 wrapper-safety + ROE-gated 家族；recon/scan（nuclei/amass/ffuf）先行（Stage 1），互不抢工 |
| 下游 | `security-remediation` | 处理每条 HIGH+ finding 的代码修复 |
| 升级（手动） | `authorized-pentest-validation` | 需要实际利用验证（注出/PoC）时，用户**手动**调用（disable-model-invocation: true —— 双门第二道）|
| 证据 | `appsec-sdk` | dast 层 evidence 持久化（过 redact，schema v1.0）|

本 skill **永不**自动跳转到 `authorized-pentest-validation` 或任何利用阶段。所有升级都需用户显式调用。

---

## 10. Failure Modes（已知坑）

| 反模式 | 正确做法 |
|---|---|
| "ROE 大概齐了，先登录扫起来" | 停。§3.1 逐条确认完整 ROE；不完整 → 回 `pentest-scope-and-roe` |
| "都谈过了，直接跑 authenticated scan" | 停。§3.2 须**本 session** explicit authorization + 具体 in-scope target；不依赖跨 session memory |
| 用 baseline 的简化 ROE 跑 authenticated | 拒。authenticated 触登录后面 → **完整** 11 项 ROE，不是简化版 |
| 直接 `zap-full-scan.py -t https://target`（raw + full active） | 拒。必须走 `zap-authenticated.sh` wrapper（受控 scan policy + auth context）|
| auth context 填真实 admin 账号图省事 | 拒。只用 ROE §8 dedicated test 账号；真实账号 = 红线 |
| 凭据直接写进 plan.yaml | 拒。只能 `${ENV_VAR}` 占位；明文凭据进 repo/chat = 红线违规 |
| authenticated scan 报疑似 SQLi，"试试能不能注出来" | 停。那是 exploitation（L3）→ 手动 `/authorized-pentest-validation`，不在本 skill |
| 对生产 staging 镜像（实为 prod 数据）跑 authenticated | 停。确认 target 不在 production_hosts[] 且无真实用户数据（ROE §2）|
| 跳过 passive baseline 直接 authenticated active | 先 Stage 0（baseline）/ Stage 1（recon）；authenticated 是逐层升级的中间层 |
| 扫到 session token 贴进 chat / finding | 拒。必经 `appsec-sdk redact`；finding.add 会拒 raw secret |

---

## 11. Mental Model

> Passive baseline 是"站在门外看这栋楼有几扇窗"。
> Authenticated DAST 是"拿着**授权发的访客证**进了大厅，看看楼里（登录后）哪些门没锁好"——
> 但**绝不**撬任何一把锁（那是 exploitation，永远是手动硬门）。
> 访客证（dedicated test 账号）是别人发的、写在 ROE 里的，不是你自己配的 master key（真实/admin 凭据）。
> 双门的意义：进楼（authenticated active）比看窗（passive）风险高一档，所以要两道签字——
> 一道写在纸上（ROE 落盘），一道当场口头确认（session explicit authorization）。
> wrapper 的意义：让 scanner 只能按"看门不撬锁"的受控方式开火，堵死"手一抖开了 full active 攻击"那条翻车路。
