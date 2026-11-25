---
name: security-app-sast-deep
canonical_id: security.app.sast_deep
aliases: [taint-analysis, dataflow-sast, deep-sast, interprocedural-sast, source-to-sink]
version: 1.0.0
status: stable
created_date: 2026-06-15
allowed-tools: Read, Grep, Glob, Bash
forbidden-tools: WebFetch, Write, Edit
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - Semgrep (taint mode / Pro cross-file dataflow): living reference, checked 2026-06-15
  - Joern (joern-cli, Apache-2.0, built-in taint/CPG): living reference, checked 2026-06-15
  - CodeQL CLI: living reference, checked 2026-06-15 (FREE for OSI-open-source only — see §3 license boundary)
  - OWASP ASVS: 5.0 (V1 Encoding/Injection / V5 Validation / V13 Configuration)
  - OWASP Top 10: 2025 (A03 Injection family, A01 Broken Access Control dataflow)
  - CWE: source→sink classes (CWE-89/79/78/22/611/918/502 etc.)
  - NIST CSF: 2.0 (ID.RA — vulnerability identification)
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "credentials.json"]
  never_write: ["raw secret material in finding output", "source code to third-party SaaS without authorization"]
  redact_on_output: ["tokens / credentials surfaced in dataflow traces", "internal endpoint URLs in sink reports"]
upstream:
  - appsec-security-orchestrator
  - security-governance-threat-modeling   # threat model points at injection/dataflow surfaces
  - security-app-fuzzing                   # fuzz crash points → taint sink hypotheses
downstream:
  - security-remediation                   # confirmed taint flow → fix + regression
  - appsec-security-orchestrator           # back with findings
description: >-
  Deep taint / dataflow / inter-procedural SAST tracing untrusted SOURCES to dangerous SINKS across functions and files, beyond pattern SAST. CodeQL for OSI-open-source, otherwise Semgrep taint mode or Joern. Read-only - never runs the app, never scans actively.
trigger_phrases:
  - taint analysis / taint mode / 污点分析 / 污点追踪
  - dataflow / data flow analysis / source to sink / source-sink / 数据流分析
  - CodeQL / Joern / semgrep taint / 深度 SAST / interprocedural / 跨函数分析
  - is this user input reachable to / does this flow to / 能不能流到
  - injection dataflow / SSRF dataflow / path traversal dataflow
---

# Security App — Deep SAST (Taint / Dataflow)

## 1. Mission

orchestrator 现有的 SAST 是 **pattern/lint 级**（semgrep 规则匹配单点代码形状）——能抓"用了 `eval`"，但抓不住"**这个 HTTP 参数经过三个函数最终拼进 SQL**"。后者要 **taint / dataflow / inter-procedural** 分析：从**不可信 source**（请求参数、body、header、文件、外部 API）出发，跨函数、跨文件追踪数据，看它是否未经 sanitizer 就到达**危险 sink**（SQL exec、shell、文件路径、模板、反序列化、SSRF 目标）。

本 skill 把 SAST 从"单点模式匹配"升级到"**source→sink 流分析**"，并明确**何时用哪个引擎**（许可证边界是关键决策点）。

**职责边界**：
- **owns**: taint/dataflow 引擎选型（决策树）+ source/sink/sanitizer 建模 + CLI 包装 + 流确认 + triage → §9 finding
- **handoff to**: `security-remediation`（确认的 taint flow → fix + 回归）；与 `security-app-fuzzing` 互喂（fuzz crash 点 → taint sink 假设；taint 不可达 → 降 fuzz crash 优先级）
- **不做**: 不跑应用、不 active scan、不 exploit；不替代 pattern-SAST（是它的**深度补充**，不是替代——见 §8）；**read-only**（`allowed-tools` 无 Write/Edit，findings 只经 `appsec-sdk`）

---

## 2. Activation Triggers

| Trigger | Action |
|---|---|
| 后端 / API 项目含不可信输入入口（HTTP / webhook / 消息队列 / 文件）| 默认激活：建 source→sink 模型 |
| pattern-SAST 报了可疑点但需确认"是否真可达 / 是否被 sanitize" | 激活：用 taint 流确认（降假阳）|
| 高危 sink 存在（raw SQL / `exec` / `system` / 反序列化 / 模板渲染 / 动态文件路径 / 出站 URL 拼接）| 激活：反向从 sink 追 source |
| `security-app-fuzzing` 报 crash，需判生产可达性 | 激活：taint 确认 crash 输入路径是否被不可信输入触达 |
| 复杂业务逻辑 / 权限判断分散多函数（IDOR / 越权 dataflow）| 激活 inter-procedural 分析 |
| 接手陌生大型后端，要快速摸清"哪些不可信输入流到哪些危险操作" | 激活：全量 source/sink 清点 |

**判断规则**：pattern-SAST 是地板（每个后端都跑），deep SAST 是"**当单点匹配不够、需要知道数据真实流向**"时上。不对纯前端/纯静态项目跑（无 server-side dataflow 面）。

---

## 3. 决策树：开源 → CodeQL / 闭源 → Semgrep-taint 或 Joern（许可证是关键）

> ⚠️ **CodeQL CLI 仅对 OSI-认可的开源项目免费**。私有/闭源代码在 CI 生成 CodeQL database = 需要付费 **GitHub Advanced Security (GHAS)**。**单人闭源商业项目默认不要用 CodeQL**，走 Semgrep/Joern。这是本 skill 最重要的决策点——别误推 CodeQL 给闭源项目。

```
项目代码是 OSI-认可的开源（公开仓库 + OSI license）?
├─ 是 → CodeQL CLI 免费可用。覆盖最深、query 库最全（尤其 Java/JS/Python/Go/C++/Ruby/Swift）。
│        但仍可叠 Semgrep（更快迭代自定义规则）。
└─ 否（私有 / 闭源 / 商业）→ 默认 CodeQL 不可白嫖（CI 生成 DB 触发 GHAS 付费）。两条免费路径：
    ├─ Semgrep taint mode（推荐起手）：免费层含 Pro Engine 跨文件 taint；规则即 YAML，写得快，CI 友好。
    └─ Joern（Apache-2.0，完全免费）：joern-cli 内置 taint + CPG（Code Property Graph），
             适合需要自定义 query / 深度过程间 / 多语言统一图分析的场景。比 Semgrep 重，但无许可证天花板。
```

**选型速查**：

| 场景 | 首选引擎 | 理由 |
|---|---|---|
| 开源仓库 | **CodeQL** | 免费 + query 库最成熟 |
| 闭源、要快、CI 集成 | **Semgrep taint** | 免费跨文件 taint，规则 YAML 迭代快 |
| 闭源、要深度自定义过程间 query / 无许可证天花板 | **Joern** | Apache-2.0，CPG 内置 taint，无付费门 |
| 多语言混合大仓 | Joern 或 Semgrep（按是否需自定义 query） | 统一图 vs 快规则 |

---

## 4. Source → Sink → Sanitizer 建模（taint 的核心）

Taint 分析三要素，**建模质量决定结果质量**（建错 = 漏报或淹没在假阳）：

| 要素 | 是什么 | 例 |
|---|---|---|
| **Source（污点源）** | 不可信数据进入点 | `req.query` / `req.body` / `req.params` / `req.headers` / `os.environ` 外部输入 / 文件读入 / 外部 API 响应 / 消息队列 payload / **LLM tool-call args**（agent 场景） |
| **Sink（危险汇）** | 数据到这就出事 | SQL `exec/query`（→SQLi）/ `child_process/os.system`（→cmd inj）/ 文件路径 open（→path traversal）/ 模板渲染（→SSTI/XSS）/ `pickle/yaml.load/Marshal`（→反序列化）/ 出站 HTTP URL（→SSRF）/ redirect target（→open redirect）|
| **Sanitizer（净化器）** | 让污点变安全的处理 | 参数化查询 binding / `shlex.quote` / path canonicalize+allowlist / HTML escape / schema 校验 + 强类型转换 / URL allowlist 校验 |

**关键**：taint engine 报"source 流到 sink **且中间无 sanitizer**" = 高价值 finding。若中间有合法 sanitizer，engine 应止流（建模时把 sanitizer 告诉它，否则假阳）。

---

## 5. CLI 包装（CLI-first；只读本仓库；不假设已装）

> 全部 **只读分析本仓库源码**，不跑应用、不连网打目标。安装命令附上，**不假设环境已装**。本 skill `allowed-tools` 无 Write——报告/finding 落盘经 `appsec-sdk`（Bash）。

### 5.1 Semgrep taint mode（闭源首选）

```bash
pip install semgrep        # 或 brew install semgrep / docker run returntocorp/semgrep

# 跑官方 + 自带 taint 规则集（含跨文件 Pro dataflow）
semgrep --config p/default --config p/owasp-top-ten \
  --json --output .appsec/evidence/<tag>/sast-deep/semgrep-taint.json .

# 跑自定义 taint 规则
semgrep --config ./.semgrep/taint-rules.yml \
  --json --output .appsec/evidence/<tag>/sast-deep/semgrep-custom.json .
```

自定义 taint 规则写法（`mode: taint` + 显式 source/sink/sanitizer）：
```yaml
rules:
  - id: req-to-sql-exec
    mode: taint                         # ← 关键：开 taint 引擎，不是单点 pattern
    pattern-sources:
      - pattern: $REQ.query.$P          # 不可信 source
      - pattern: $REQ.body.$P
    pattern-sanitizers:
      - pattern: parameterize(...)      # 合法净化 → 止流
    pattern-sinks:
      - pattern: db.query($SINK)        # 危险 sink
    message: Untrusted request data reaches db.query without parameterization (SQLi).
    languages: [javascript, typescript]
    severity: ERROR
```

> **自写 sink pattern 的假阳纪律**：自定义 sink 易过宽，连带 flag 本就安全的参数化/预编译调用（如 `db.query(sql, params)`、`prepare(...).run(...)`、ORM builder）。除了上面的 `pattern-sanitizers`（止 taint 流），对**已知安全的同名调用形态**再加一道 `pattern-not` 显式排除（如 sink 下加 `pattern-not: db.query($Q, $PARAMS)`），否则参数化安全路由会被误报。E2E 实测：初版只给宽 sink 时会连带命中参数化安全路由，补 `pattern-not` 参数化排除后才精确命中唯一漏洞行。

### 5.2 Joern（闭源、无许可证天花板）

```bash
# 下载 joern-cli release（https://github.com/joernio/joern；JVM 11+）
# 解压后用 joern / joern-parse / joern-export

joern-parse . --output cpg.bin            # 建 Code Property Graph
joern                                     # 进交互 shell，或 --script 跑脚本
```

Joern source→sink query（CPGQL，过程间 reachability）：
```scala
// taint-query.sc  ——  用 joern --script taint-query.sc
importCpg("cpg.bin")
// 定义 source / sink，问 source 能否流到 sink（过程间）
val src = cpg.method.name("getParameter").parameter        // 不可信 source
val snk = cpg.call.name("executeQuery").argument           // 危险 sink
snk.reachableBy(src).l                                      // 可达路径 = 候选 taint flow
// 导出 JSON 供 §9 triage
```

### 5.3 CodeQL（**仅开源项目**）

```bash
# 仅 OSI-开源项目免费。闭源用此 = 触发 GHAS 付费，本 skill 默认不走。
# 下载 codeql-cli-binaries release
codeql database create db --language=javascript --source-root=.
codeql database analyze db codeql/javascript-queries \
  --format=sarifv2.1.0 --output=.appsec/evidence/<tag>/sast-deep/codeql.sarif
```
> CodeQL 的内建 query 套件（`codeql/<lang>-queries`）已含成熟 taint flow query（SQLi/XSS/path-injection/SSRF…），开源项目首选。

### 5.4 与 pattern-SAST 对照跑

```bash
# orchestrator 现有的 pattern-SAST（地板）照常跑，deep SAST 叠加在上面
semgrep --config auto --json --output .appsec/evidence/<tag>/sast/semgrep-pattern.json .
```

---

## 6. Standard Workflow

```
Step 1  许可证 + 生态判定（决定引擎）
        → 开源 OSI? → CodeQL 可用
        → 闭源? → Semgrep taint（起手）或 Joern（深度自定义）
        → 识别语言 / 框架（决定 source/sink 内建库覆盖度）

Step 2  Source / Sink / Sanitizer 建模（§4）
        → 列项目的不可信入口（HTTP/webhook/MQ/文件/外部 API/agent tool args）
        → 列危险 sink（SQL/shell/path/template/deserialize/出站URL）
        → 列已有 sanitizer（参数化/escape/allowlist/schema 校验）
        → 引擎内建覆盖不够的，补自定义规则/query

Step 3  跑 taint 分析（§5）
        → Semgrep taint / Joern reachableBy / CodeQL analyze
        → 落 .appsec/evidence/<tag>/sast-deep/

Step 4  流确认 + 降假阳
        → 每条候选 flow：source 真不可信？sink 真危险？中间真无 sanitizer？
        → 与 pattern-SAST 结果交叉：pattern 命中 + taint 可达 = 高置信
        → fuzz 联动：security-app-fuzzing crash 点是否在某条 taint flow 上

Step 5  三角验证（与 fuzzing / 威胁模型）
        → taint 可达 + fuzz 能触发 → critical/high（实证可利用）
        → taint 可达但 fuzz 没触发 → 仍记（静态可达 ≥ 动态未触）
        → taint 不可达 → 降级 / 标 unmapped，但留痕（不静默丢）

Step 6  输出 + 路由
        → 确认 flow → §9 schema finding（source: sast）→ appsec-sdk finding.add
        → 高危 → security-remediation（fix → 回归：重跑 taint 确认 flow 断）
        → evidence 经 appsec-sdk evidence.append <tag> sast 落盘 → AppSec Release Evidence §5 SAST
        → 不可达/被抑制项写明 justification（不静默忽略）
```

---

## 7. Deep SAST vs Pattern SAST（分工 —— 不替代）

| 维度 | Pattern/Lint SAST（orchestrator 现有地板）| Deep SAST（本 skill）|
|---|---|---|
| 分析单位 | 单点代码形状（"用了危险 API"）| 数据流路径（"不可信输入流到危险 API"）|
| 跨函数/跨文件 | 否 | **是**（inter-procedural / cross-file）|
| 假阳特征 | 高（命中 API 但输入其实可信）| 低（要求真实流可达 + 无 sanitizer）|
| 假阴特征 | 漏跨函数污染 | 漏建模外的 source/sink（建模质量依赖）|
| 速度 | 快（每次 commit 跑）| 慢（PR / 定时 / 高危模块跑）|
| 角色 | **每个后端必跑的地板** | **当需要知道数据真实流向时的深度补充** |

**铁律**：deep SAST **不替代** pattern SAST。pattern 做广度+速度（CI 每次跑），deep 做深度+确认（降假阳 + 抓跨函数）。两者结果交叉提升置信度。

---

## 8. 与 Fuzzing 的互喂闭环

- **fuzz → taint**：`security-app-fuzzing` 报 crash → 用 taint 确认 crash 的输入是否在生产里被不可信 source 触达（可达性判定，§9 triage Step 4）。
- **taint → fuzz**：taint 报"source 可达 sink 但需特定输入"→ 给 fuzzing 提供高价值 harness target（针对该 sink 写 structure-aware harness 验证可利用）。
- **双确认 = 最高置信**：静态可达（taint）+ 动态可触发（fuzz）= critical/high 实证 finding；只静态可达 = 仍记但标证据强度。

---

## 9. Triage → §9 Finding

1. **确认 source 不可信**：是真外部输入，不是被误标的内部常量/已验证数据。
2. **确认 sink 危险**：真的是 SQL exec/shell/path/deserialize，不是同名的安全函数。
3. **确认无有效 sanitizer**：中间没有合法净化（参数化/escape/allowlist/schema+类型转换）。漏建 sanitizer → 假阳，先补建模重跑。
4. **定 CWE + ASVS**：按 source→sink 类别（SQLi=CWE-89/A03；cmd inj=CWE-78；path traversal=CWE-22；SSTI=CWE-1336；反序列化=CWE-502；SSRF=CWE-918/A10）。
5. **可达性 + 可利用性**：过程间路径在生产配置下真能走通？联动 fuzz 看能否实际触发。
6. **脱敏**：dataflow trace 若途经 secret/PII/内部 URL，**先 `appsec-sdk redact`**，不把 raw 值贴进 finding。

---

## 10. Hard Rules

- ❌ **不**给闭源/私有项目误推 CodeQL（CI 生成 DB = 触发 GHAS 付费）——闭源默认 Semgrep/Joern
- ❌ **不**跑应用 / 不 active scan / 不 exploit——只**静态读源码**做 dataflow（read-only，无 Write 工具）
- ❌ **不**把 deep SAST 当 pattern SAST 的替代——它是深度补充，pattern 仍是必跑地板（§7）
- ❌ **不**在没建 sanitizer 模型时就报 finding——漏建 sanitizer = 假阳淹没真问题，先补建模
- ❌ **不**把 taint 候选 flow 直接当确认漏洞——必须过 §9 triage（source 真不可信 + sink 真危险 + 无 sanitizer + 可达）
- ❌ **不**向第三方 SaaS 传源码做分析（除非明确授权且用户知情）——本地 CLI 优先
- ❌ **不**读 `.env` / `secrets/**` / `*.pem` / `*.key`——只读应用源码
- ❌ **不**把 dataflow trace 里的 raw secret / PII / 内部 URL 贴进 chat / log / finding——先 `appsec-sdk redact`
- ❌ **不**把 taint 不可达项静默丢弃——降级但留痕（标 justification / unmapped_reason）
- ❌ **不**直接 Write 到 `.appsec/findings/**`——只走 `appsec-sdk`（hook §18.5 物理拦截；本 skill 也无 Write 工具）

---

## 11. Anti-patterns

- ❌ "闭源也用 CodeQL，反正能下载" —— CI 生成 private DB 触发 GHAS 付费，违 no-paywall 原则
- ❌ "pattern SAST 报了就是漏洞" —— 单点匹配不看数据流，高假阳；用 taint 确认可达性
- ❌ "taint engine 报了一条路径就是真洞" —— 没确认 source 可信度 / sanitizer / 可达性前都是候选
- ❌ "source/sink 用默认就行" —— 框架特有入口（自定义中间件 / ORM / 模板引擎）默认库常漏，要补建模
- ❌ "把 sanitizer 忘了告诉 engine" —— 合法净化被无视 → 满屏假阳 → 真问题被淹
- ❌ "deep SAST 慢，那就只跑 deep 不跑 pattern" —— 反了：pattern 每 commit 跑（快广），deep PR/定时跑（深确认）
- ❌ "taint 不可达就删掉" —— 静态不可达可能是建模盲区，应留痕降级而非静默丢
- ❌ "agent 的 tool-call args 不算 source" —— LLM 产出的 args 是不可信输入，是 taint source（agent 后端尤其要建）
- ❌ "用 SaaS 上传整个私有仓库扫一下最省事" —— 源码外泄风险，本地 CLI 优先，SaaS 需授权+知情

---

## 12. Output Contract

> **read-only**：本 skill `allowed-tools` 无 Write/Edit。所有 finding / evidence 落盘经 `appsec-sdk` 命令（Bash），从工具层杜绝绕过 schema 直写。

每次 deep-SAST engagement 产出：

1. **引擎选型说明**：开源/闭源判定 + 选 CodeQL/Semgrep/Joern 的理由（许可证边界写明）
2. **Source/Sink/Sanitizer 模型**：本项目建模清单（per-语言/框架）
3. **Taint flow 报告**：候选 flow 列表（source→中间→sink 路径）→ `.appsec/evidence/<tag>/sast-deep/`
4. **流确认表**：每条 flow 的 triage 结论（source 可信度 / sink 危险性 / sanitizer 有无 / 可达性 / 与 fuzz 交叉）
5. **Pattern-SAST 交叉对照**：哪些 pattern 命中被 taint 证实可达（升置信）/ 哪些被证为不可达（降假阳）
6. **Findings** —— 确认的 taint flow 全部经 `appsec-sdk finding.add <file>`（canonical path，redact-first）落 `.appsec/findings/<tag>/`，符合 orchestrator §9 finding schema v1.0：
   - `source`：`sast`（用现有 enum，不发明 `taint`/`dataflow` 新值；PreToolUse prewrite hook 拒 schema 漂移）
   - `detector`：引擎名 + 版本（`semgrep@1.x` / `joern@4.x` / `codeql@2.x`）
   - `severity` **小写**；taint 可达 + fuzz 可触发 = critical/high；只静态可达按 sink 危险度定
   - `cwe`：按 source→sink 类别（CWE-89/78/22/79/502/918/611/1336…）
   - `asvs_mapping`：versioned `v5.0.0-<ch>.<sec>.<req>`（injection/encoding 用 V1；validation 用 V5；正则 `^v5\.0\.0-\d+\.\d+\.\d+$`）。无诚实映射留空 `[]` + `unmapped_reason`，**禁止编造**
   - `owasp_top10`：注入族 `A03:2025`；SSRF `A10:2025`；越权 dataflow `A01:2025`
   - `reproduction_steps` / `evidence`：dataflow trace **禁含 raw secret/PII/内部 URL**——先 `appsec-sdk redact`
   - **绝不** Write 直写 `.appsec/findings/**`（hook §18.5 物理拦截 + 本 skill 无 Write 工具）；只走 sdk
   - 高危 → `security-remediation`（fix → 回归：重跑 taint 确认 flow 已断）
7. AppSec Release Evidence **§5 SAST** 写入（deep SAST 是 §5 的深度层；evidence 经 `appsec-sdk evidence.append <tag> sast`）

---

## 13. References

- [Semgrep — taint mode](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode/) / [Semgrep Pro cross-file dataflow](https://semgrep.dev/docs/semgrep-code/semgrep-pro-engine-intro/)
- [Joern (joern-cli, Apache-2.0)](https://github.com/joernio/joern) / [Joern docs — taint tracking / CPGQL](https://docs.joern.io/)
- [CodeQL CLI](https://codeql.github.com/docs/codeql-cli/) — **free for OSI-open-source only**
- [CodeQL CLI license boundary](https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md) — 闭源走 GHAS（付费），故本 skill 闭源默认不走 CodeQL
- [OWASP ASVS 5.0 — V1 Encoding & Injection / V5 Validation](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE — Top 25 source→sink classes](https://cwe.mitre.org/top25/)
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md) — §9 finding schema / §5 SAST in Release Evidence / §18.5 finding-path hook
- [security-app-fuzzing](../security-app-fuzzing/SKILL.md) — fuzz crash ↔ taint reachability 互喂（sibling）
- [security-governance-threat-modeling](../security-governance-threat-modeling/SKILL.md) — injection/dataflow surfaces (upstream)
- [security-remediation](../security-remediation/SKILL.md) — confirmed flow → fix → regression
