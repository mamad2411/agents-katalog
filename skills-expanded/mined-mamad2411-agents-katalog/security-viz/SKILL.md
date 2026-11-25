---
name: security-viz
description: >-
  Render security DIAGRAMS from existing AppSec and governance fact-sources — AI-agent risk graph (agents x skills x tools x permissions with safety gates), vulnerability lifecycle Kanban, security evidence and release-decision dashboard, or pentest scope-boundary map. Reads what the harness registry and `.appsec/` artifacts already declare: adds no data collection and never runs scans. For CODE architecture use `arch-viz`. Triggers: "security diagram / 安全可视化 / 安全架构图 / AI agent risk graph / agent 权限图 / 漏洞看板 / security evidence dashboard / pentest scope map / DFD / trust boundary / attack surface map".
allowed-tools: Read, Bash, Grep, Glob, Write
forbidden-tools: WebFetch
model_note: "Sonnet 默认足够（确定性脚本渲染 + 读已有 fact-source）。涉及把图解读成 release 结论 / 客户对外汇报时升 opus 复核一次。绝不让本 skill 替代 appsec gate verdict。"
---

# security-viz

> Supporting utility skill (Layer 11 Meta · "Security Visualization", a sibling of `arch-viz` but on the **security** axis, not the code axis).
> Wraps a local Node generator — `scripts/security-viz.js` — that renders Mermaid + markdown security diagrams from **existing fact-sources** the harness already produces.
> Pure Node (`fs`/`path` only, no npm deps). No network, no scans, no code parsing.

## 1. Purpose（一句话业务价值）

把已经存在的安全信息**画成图**，让人一眼看懂——agent 都有哪些权限和安全闸门、漏洞修到哪一步了、这次发布的安全证据全不全、渗透测试到底准能动哪儿不能动哪儿。它**不采集任何新数据**：所有节点都来自 harness registry 和项目里 `.appsec/` 的产物。fact-source 是空的，它就如实说"空"，绝不编节点。

It renders FROM fact-sources; it never collects, scans, or parses code. The fact-source is the source of truth — security-viz only draws it.

## 2. Boundary vs `arch-viz`（不重叠声明 — 必读）

这两个 skill 都"出图"，但轴完全不同，永远不抢对方的活：

| | `arch-viz` | `security-viz` (本 skill) |
|---|---|---|
| 画的是 | **代码结构**（modules / files / call graph / clusters） | **安全产物**（agent 权限 / 漏洞生命周期 / release 证据 / pentest 范围） |
| fact-source | repo 源码（tree-sitter parse via CodeGraph） | harness registry + `.appsec/` artifacts（**绝不 parse 代码**） |
| 落盘 | `<repo>/docs/architecture/`（committable，给客户/团队） | `<project>/.appsec/evidence/<tag>/viz/`（安全证据，随 evidence bundle 走） |
| 性质 | 可提交的交付物 | release gate 的可读化视图 |

**铁律**：security-viz 永远不调 CodeGraph、永远不读源码做结构分析。要画代码架构 → 用 `arch-viz`。要画安全态势 → 用本 skill。

## 3. What it owns — 4 LIVE diagrams（今天就能跑）

A5 audit 结论：企业级安全可视化有 12 张图，其中 **4 张的 fact-source 今天已经存在**，所以本 skill 真实实现这 4 张：

| # | 图 | fact-source（已存在） | 子命令 |
|---|---|---|---|
| 1 | **AI Agent Risk Graph**（最高价值） | `~/.claude/manifests/skills.manifest.json` + `agents/*.md` frontmatter + AppSec-family `skills/*/SKILL.md` frontmatter | `agent-risk-graph` |
| 2 | **Vulnerability Lifecycle Board** | `<project>/.appsec/findings/<tag>/*.yaml`（finding schema v1.0） | `vuln-board <tag>` |
| 3 | **Security Evidence Dashboard** | `<project>/.appsec/decisions/<tag>/appsec_release_decision.yaml` | `evidence-dashboard <tag>` |
| 4 | **Pentest Scope Map** | `<project>/.planning/PENTEST-ROE.md`（YAML frontmatter，11-section ROE 的 parser surface） | `pentest-scope-map [<roe-file>]` |

### 3.1 AI Agent Risk Graph — 为什么是最高价值

整个 harness 的"控制面"第一次被画成一张图：哪些 agent / skill 是 `disable-model-invocation: true`（手动硬闸，绝不自动触发）、哪些 skill 有 `forbidden-tools`、哪个是 manual-gate。**零新数据采集——registry 本身就是 fact-source。** 它读：
- `skills.manifest.json`（AppSec-family + `name_freeze` + primary appsec orchestrator）
- 每个 `agents/*.md` 的 frontmatter：`name` / `model` / `tools`（兼容 `["A","B"]` 和 `A, B` 两种写法）/ `disable-model-invocation`
- 每个 AppSec-family `SKILL.md` 的 frontmatter：`allowed-tools` / `forbidden-tools` / `disable-model-invocation` / `manual_gate_required` / `upstream` / `downstream`

输出 Mermaid `graph` + 一张"safety-gate summary"表，红色标 manual-only、紫色标 forbidden-tool、琥珀标 manual-gate。

## 4. Roadmap — 8 PLANNED diagrams（被 fact-source 卡住，诚实标注）

剩下 8 张图**不是没做，是它们的 fact-source 还没有别的 skill 产出**。本 skill 不会为了"看起来全"而编造这些图。完整目录（含每张图的前置 fact-source + 产出它的 skill/SDK 命令）见 [`references/diagram-catalog.md`](references/diagram-catalog.md)。摘要：

| # | 图 | 状态 | 前置 fact-source（谁先产出） |
|---|---|---|---|
| 5 | DFD / Trust-boundary diagram | PLANNED | 结构化 DFD（`security-governance-threat-modeling` 需先产出 machine-readable data-flow，不是 prose STRIDE） |
| 6 | Attack surface map | PLANNED | `appsec-risk-classifier` 的 attack-surface inventory 需落成结构化 fact-source |
| 7 | Auth / authorization matrix | PLANNED | role × resource × permission 矩阵 fact-source（无人产出） |
| 8 | API security map | PLANNED | 结构化 endpoint inventory（`security-app-api` 需落 fact-source，非 prose） |
| 9 | Data classification map | PLANNED | data-store × 分类（public/internal/confidential/restricted）fact-source |
| 10 | MITRE ATT&CK coverage matrix | PLANNED（producer 已出现） | `attack-coverage.yaml`，由 `security-response-red-purple-team` 经 `appsec-sdk attack.coverage <tag>` 产出 → 一旦稳定即可升 LIVE |
| 11 | Control coverage matrix | PLANNED | CSF/ASVS control × status 结构化 fact-source（`appsec_release_decision.yaml.csf2_coverage` 是雏形，需扩成完整 control 列表） |
| 12 | Security architecture diagram | PLANNED | 安全组件拓扑 fact-source（WAF / IAM / secret-store / network boundary）需有人产出 |

**升级规则**：某张 PLANNED 图的 fact-source 一旦由某 skill/SDK 稳定产出，就在 `security-viz.js` 加对应子命令 + reader，并把 catalog 里该行从 PLANNED 改 LIVE。**绝不在 fact-source 缺位时假装能画。**

## 5. Command surface（脚本命令面）

```bash
S=~/.claude/skills/security-viz/scripts/security-viz.js

# 1. AI Agent Risk Graph — 读 GLOBAL harness（默认 ~/.claude）
node "$S" agent-risk-graph                              # → <cwd>/security-agent-risk-graph.md
node "$S" agent-risk-graph --out report/agents.md
node "$S" agent-risk-graph --harness /path/to/.claude   # 指定别的 harness 根

# 2. Vulnerability Lifecycle Board — 读 <project>/.appsec/findings/<tag>/
node "$S" vuln-board v1.2.0                              # → .appsec/evidence/v1.2.0/viz/vuln-board.md
node "$S" vuln-board v1.2.0 --project /path/to/proj --out board.md

# 3. Security Evidence Dashboard — 读 .appsec/decisions/<tag>/appsec_release_decision.yaml
node "$S" evidence-dashboard v1.2.0                      # → .appsec/evidence/v1.2.0/viz/evidence-dashboard.md

# 4. Pentest Scope Map — 读 .planning/PENTEST-ROE.md frontmatter
node "$S" pentest-scope-map                              # → .appsec/evidence/pentest/viz/pentest-scope-map.md
node "$S" pentest-scope-map path/to/PENTEST-ROE.md

# 5. all — 一次出 4 张（pentest map best-effort：无 ROE 自动跳过）
node "$S" all v1.2.0 --project /path/to/proj
```

**输出约定**：
- 所有图都是 ```` ```mermaid ```` fenced markdown，可直接贴进 PR / docs / evidence bundle。
- project-scoped 图（2/3/4）默认落 `<project>/.appsec/evidence/<tag>/viz/`（pentest map 落 `.../evidence/pentest/viz/`）。
- agent-risk-graph 读 GLOBAL harness，默认落 `<cwd>/security-agent-risk-graph.md`，可 `--out` 改。

## 6. Use this skill when

- 用户想**看图/画图**理解安全态势：agent 权限 / 漏洞进度 / 发布证据 / 渗透范围。
- 用户要把安全状态做成**给非技术读者看**的 dashboard（traffic-light 红黄绿）。
- 用户想知道"harness 里哪些 agent/skill 是手动硬闸、哪些被禁用某工具"——一张 agent risk graph 全标出来。
- AppSec orchestrator 跑完后，想把 `appsec_release_decision.yaml` / findings **可读化**进 evidence bundle。
- ROE 起草后想**一眼确认** in-scope vs out-of-scope 边界没画错。

## 7. Do NOT use this skill when

- 用户要画**代码架构 / 调用链 / 模块图** → 用 `arch-viz`（code 轴）。
- 用户要的是**实际的安全审查 / 找漏洞 / 出 finding / 出 release 结论** → 这些是 fact-source 的**生产者**，走 `appsec-security-orchestrator`；本 skill 只画已产出的东西。
- fact-source 还不存在（没跑过 AppSec orchestrator、没起草 ROE）→ 先去产出 fact-source，本 skill 不能凭空画。
- 用户想画一张 PLANNED 图（§4 的 8 张）但其 fact-source 尚无人产出 → 如实说"该图的 fact-source 还没有 skill 产出"，不编。
- 用户把"画了张安全图/发了 dashboard"当成**实际防护或访问控制** → 图不是控制面；访问控制走 `appsec-security-orchestrator`。

## 8. Safety & boundaries（不可违反）

1. **Render-only.** 本 skill 只渲染已有 fact-source，**绝不**采集新数据、**绝不**扫描、**绝不** parse 代码。
2. **No fabrication（诚实硬规则）.** fact-source 缺失 → 清晰报错 + 非零退出（project-scoped 命令）；fact-source 为空 → 输出里如实写"空"，**绝不编节点**。占位符未填的 ROE → 标 "ROE NOT READY"，**绝不**当成 authorization。
3. **Diagram ≠ verdict.** 这些图**永远不是** release 结论。release verdict 只能由 deterministic `appsec-orchestrator.js` + `spec_hash` 人审 + evidence bundle 产出（CLAUDE.md §3.7 governed-gate 铁律）。security-viz 的图可以**喂进** evidence bundle 当可读化视图，但不替代 `appsec-sdk gate.check`。
4. **Path-fenced writes.** project 图写在 `<project>/.appsec/evidence/<tag>/viz/`；tag 必须过 `^[A-Za-z0-9._-]+$` 安全名校验（挡 `../` 路径穿越）。
5. **Never reads secrets.** 本 skill 不读 `.env` / `*.pem` / `*.key` / `credentials.json`；它读的 finding/decision YAML 已经过 `appsec-sdk redact`，本 skill 也**不反向解 redaction**——图里出现的就是 fact-source 里 redacted 后的值。
6. **Viewer is not access control.** 一张 scope map / dashboard 不 gate 任何访问。访问控制是 AppSec orchestrator 的事。
7. **No deps, no network.** 纯 Node `fs`/`path`，零 npm 依赖，零网络调用——与 harness 的 no-deps 约定一致。

## 9. Handoff matrix

| Downstream | When to hand off |
|---|---|
| `appsec-security-orchestrator` | 用户想要的是**实际**的安全审查 / finding / release 结论（fact-source 的生产者），不是画图。 |
| `arch-viz` | 用户其实要的是**代码结构**图（modules / call graph / committable 架构 bundle）。 |
| `pentest-scope-and-roe` | scope map 显示 ROE 未填全 / 缺字段 → 回去补 ROE。 |
| `security-response-red-purple-team` | 用户想要 ATT&CK coverage matrix（图 #10）→ 它先产出 `attack-coverage.yaml`，之后本 skill 可渲染。 |
| `enterprise-qa-testing` | 这些图可被引用进 QA release evidence bundle（不重叠测试策略）。 |

## 10. Anti-patterns

- ❌ 用 security-viz 画代码架构 / 调用链 —— 那是 `arch-viz`，security-viz **绝不** parse 代码。
- ❌ fact-source 缺位时编节点凑一张"完整"的图 —— 缺就如实报缺。
- ❌ 把一张 dashboard / scope map 当成 release verdict 或访问控制。
- ❌ 把 PLANNED 的 8 张图说成"能画" —— 它们卡在 fact-source 上，照实标 PLANNED。
- ❌ 反向解 finding/decision 里的 redaction 试图还原 raw secret。
- ❌ 跳过 `appsec-security-orchestrator` 直接让本 skill"出安全结论" —— 它只出图，不出结论。

## 11. Maintenance

- 子命令 / flag 变化 → 同步更新 §5 命令面 + `node security-viz.js --help` 输出。
- 某张 PLANNED 图的 fact-source 落地 → 加 reader + 子命令 + 把 `references/diagram-catalog.md` 该行改 LIVE。
- fact-source schema 漂移（finding schema / release decision / ROE frontmatter）→ 同步更新对应 reader（reader 是保守的：解析不了就报，不猜）。
- 这是 **global** user skill，不绑任何单个 repo。
