---
name: discoverability-orchestrator
canonical_id: discoverability.orchestrator
aliases: [discoverability, seo-aeo-geo-aso-orchestrator, l12-discoverability]
version: 1.2.0
status: stable
created_date: 2026-05-25
parent: uiux-product-orchestrator
layer: L12
children:
  - web-seo
  - web-aeo
  - web-local-seo
  - app-aso
sibling-skills:
  - web-seo
  - web-aeo
  - web-local-seo
  - app-aso
upstream:
  - uiux-product-orchestrator   # L12 是 UIUX 下游子层
  - gsd-pipeline-orchestrator   # release-readiness gate 串联
downstream:
  - enterprise-qa-testing       # release evidence bundle 引用 discoverability evidence
allowed-tools: Read, Grep, Glob, Write, Bash, Skill, Agent
forbidden-tools: WebFetch
disable-model-invocation: false
description: >-
  L12 Discoverability orchestrator — routes "will this be found after launch" work across the 4 narrow skills (web-seo / web-aeo / web-local-seo / app-aso), decides activation and gate level by project type, and writes an evidence-driven gate-result.yaml as a release gate. Use when the ask spans more than one channel — ranking on Google AND being cited by AI assistants, or web plus app-store reach; a single-domain ask belongs to the narrow skill. Does no design, no security, and never substitutes for access control. Triggers: "rank higher on Google / show up in search results / get cited by ChatGPT / cited by AI search / found by AI assistants / discoverability / 可发现性 / 上线后被找到 / release readiness (discoverability) / L12 audit / 我的网站怎么被 ChatGPT / Google 找到 / AI search + 传统 SEO 一起做"
---

# Discoverability Orchestrator (L12)

> **Execution mode: GSD-lite Harness v1.0 (own track)**（2026-05-29 user lock）— 本 skill **NOT** migrating to Workflow tool workflow-spec mode. L12 已有自己的等同治理产物：`discoverability-sdk.py` 10 命令 + 3 disc-* agents + 5 项目 hooks + 8-step self-dispatch。不需要第二套机制。详 `~/.claude/CLAUDE.md §3.5`。

> **本 skill 是 UIUX 主线下的 L12 子层 router，不是第 6 个 primary orchestrator。**
> 上游：`uiux-product-orchestrator` 触发后下放到 L12。
> 下游：`web-seo` / `web-aeo` / `web-local-seo` / `app-aso` 4 个 narrow skill。

---

## 1. 概述

L12 Discoverability 解决一个工业级 commercial 项目的下游问题——**release 之后，目标用户能不能找到你**。这是 UIUX 主线（设计 + 实现）跑完之后的"可发现性治理层"，不是设计层、不是安全层、不是 QA 层。

四个相互独立、技术栈不同、不可互替的 narrow domain：

| 子 skill | 域名 | 解决问题 | 典型 surface |
|---|---|---|---|
| `web-seo` | 传统 web SEO | Google / Bing / Baidu 等搜索引擎索引 + 排名 | 公开 web 页面、sitemap、metadata |
| `web-aeo` | Answer Engine Optimization（业内别名 GEO=Generative Engine Optimization）| ChatGPT Search / Claude Search / Perplexity / Gemini Overviews 等 AI search 引用 | docs、知识库、blog、llms.txt |
| `web-local-seo` | Local SEO（**只做地理/本地**） | Google Business Profile / Google Maps / Apple Maps 等本地结果 | 实体门店、本地服务页、NAP citations |
| `app-aso` | App Store Optimization | App Store / Google Play 搜索 + 推荐 + 排名 | 移动 app 商店 listing |

**职责边界**：
- 路由 + 治理 + evidence aggregation
- 不亲自跑脚本，由各 narrow skill 实施
- 不做设计 / 不做 access control / 不做 security scan
- 不替代 QA release smoke——但 QA 的 release evidence bundle 可以**引用**本 skill 的产出

---

## 2. 4 个 narrow skill 路由表

> **本 orchestrator 只处理高层协调入口（"discoverability 综合审计" / "L12 audit" / "上线后被找到" 等）。下表列出的 narrow 关键词由 4 个 narrow skill 各自的 `trigger phrases` 直接捕获 —— orchestrator 不与 narrow skill 抢这些关键词。**

| 用户意图 / 触发关键词（narrow skill 负责） | 路由目标 | 互斥规则 |
|---|---|---|
| "SEO" / "搜索引擎排名" / "Google 收录" / "robots.txt" / "sitemap" / "meta tags" / "structured data" / "core web vitals" | `web-seo` | 与 web-aeo / web-local-seo 不互斥，但 4 域分开输出 |
| "AEO" / "AI search" / "ChatGPT Search" / "Claude Search" / "Perplexity" / "Gemini" / "llms.txt" / "AI citation" / "answer engine" / "OAI-SearchBot" / "ClaudeBot" / "PerplexityBot" / "GPTBot" / "GEO"（Generative Engine Optimization 语境）| `web-aeo` | 严格独立 — 不要塞进 web-seo |
| "Local SEO" / "Google Business Profile" / "GBP" / "Google Maps" / "Apple Maps" / "Baidu Map" / "NAP" / "local citations" / "门店地图" / "本地服务" / "near me" | `web-local-seo` | **只做 Local SEO**，不是 generic SEO，不是 GEO（generative engine — 那个归 web-aeo）|
| "App Store" / "Google Play" / "ASO" / "App Store Optimization" / "store listing" / "keywords" / "screenshots" / "icon" / "app ranking" / "TestFlight" | `app-aso` | 独立 — 即使是 web+app 双产品也独立跑 |

**严格 4 域分离**：SEO / AEO / Local SEO / ASO 不互相串味。同一项目可能 4 个都激活，但 evidence 和 gate 分开管理。

**何时触发本 orchestrator（而非 narrow skill）**：
- 用户问"我项目要做哪些 discoverability"（综合诊断 → 跑 §6 决策树后分发）
- 用户问"AI search + 传统 SEO 一起做" / "SEO+AEO+ASO 综合审计"
- 用户问"GEO/AEO/SEO/ASO 哪个适用"（routing 询问语境）
- 用户问"我的网站怎么被 ChatGPT / Google 找到"
- release readiness check 阶段需要聚合 4 域 evidence 时
- "L12 audit" 综合产出

当 narrow 关键词单独出现时，**让 narrow skill 直接接管**，不要先经 orchestrator 中转。

---

## 2.5. GEO Ambiguity Resolver — 双义性消歧

"**GEO**" 在不同 sub-community 含义完全不同：

| 上下文 signal | 路由到 | 说明 |
|---|---|---|
| 提到 ChatGPT / Claude / Perplexity / Gemini / AI search / answer engine / LLM / citation / llms.txt / generative engine | `web-aeo` | Generative Engine Optimization（AI search 引用优化） |
| 提到 Google Business Profile / GBP / Google Maps / Apple Maps / Baidu Map / NAP / 实体店 / 餐厅 / 诊所 / 律师 / 牙医 / 服务区域 / Local SEO / 附近的 / near me / 本地服务 | `web-local-seo` | Local SEO（地理/本地搜索优化）|
| 无上下文 signal（仅 "GEO" 一词，无任何附加词） | **默认 `web-aeo`** | 业界 2025-2026 共识：GEO 缩写默认 = Generative Engine Optimization（见下方权威来源） |

**为什么默认路由 GEO → web-aeo（而非 web-local-seo）**：

1. **Princeton et al. 2023 论文** 将 GEO = Generative Engine Optimization 正式立项（[arxiv 2311.09735](https://arxiv.org/abs/2311.09735)，KDD 2024）
2. **Wikipedia 条目** "Generative engine optimization" 直接成立、无 disambiguation 页面 → 行业默认含义
3. **Search Engine Land / SEJ / Ahrefs / Semrush** 等行业媒体在 2024-2026 年间将 GEO 默认解释为 Generative Engine Optimization（[Search Engine Land 介绍](https://searchengineland.com/what-is-generative-engine-optimization-geo-444418)）
4. Local SEO 这个域在英文社区**几乎从不**缩写为 "GEO" — 通常写全 "Local SEO" / "Google Business Profile SEO" / "Maps SEO"

**消歧执行规则**：
- 用户消息含 "GEO" 但同时含 maps/local/near me/门店/服务区域 关键词 → 直接路由 `web-local-seo`，不询问
- 用户消息含 "GEO" 但同时含 AI search/ChatGPT/Claude/Perplexity/Gemini/llms.txt/citation → 直接路由 `web-aeo`，不询问
- 用户消息**只**含 "GEO"（无任何附加 signal）→ 默认路由 `web-aeo`，并在第一句回答开头**显式声明** "按业界 2025-2026 共识，将 GEO 默认解读为 Generative Engine Optimization → 路由到 `web-aeo`。如果你指的是 Local SEO（Google Business Profile / 地图），请告知，会切到 `web-local-seo`"
- 任何情况下，**不要**让 "GEO" 单词触发本 orchestrator —— orchestrator 不抢 narrow 域

权威来源：
- [arxiv 2311.09735 "GEO: Generative Engine Optimization"](https://arxiv.org/abs/2311.09735) (Princeton, KDD 2024)
- [Wikipedia: Generative engine optimization](https://en.wikipedia.org/wiki/Generative_engine_optimization)
- [Search Engine Land: What is Generative Engine Optimization (GEO)](https://searchengineland.com/what-is-generative-engine-optimization-geo-444418)
- Google AI Search / AI Overviews 官方 docs（不使用 "GEO" 一词，但讨论的是同一现象）

---

## 3. 执行宪法 — Script-first, Skill-second, AI-last

这是 L12 子层全部 narrow skill 的**核心硬规则**。所有 runner、所有 audit、所有 gate 都按此优先级：

```
Execution Priority

1. Deterministic script / API / CLI
   PSI (PageSpeed Insights API) / Search Console API / GBP API /
   App Store Connect API / Google Play API / lighthouse CLI /
   sitemap.xml fetch / robots.txt parser / Schema.org validator

2. Framework adapter
   Next.js metadata API / Nuxt SEO module / Astro SEO integration /
   Docusaurus plugin-sitemap / WordPress Yoast/Rank Math export /
   SvelteKit @sveltejs/adapter sitemap

3. Structured evidence parser
   读 framework / CMS / 配置文件生成 evidence YAML/JSON，
   不调 AI，只做结构化解析

4. AI synthesis from evidence
   读取上面 3 步产出的 evidence，做 narrative / 优先级 / 修复建议
   AI 不亲自审计，AI 解读脚本产出

5. Manual AI scan (LAST RESORT)
   仅当：项目无 framework / 无 API 接入权 / 无可解析配置 时才允许
   必须在报告里标 "manual-ai-scan: true" 注明
```

**反规则**（违反即 BLOCKED）：
- ❌ 跳过 step 1-3 直接让 AI"凭感觉审计 SEO"
- ❌ 把 AI 的 narrative 当作 deterministic evidence
- ❌ 把 AI synthesis 输出包装成"官方 ranking factor"

**判断依据**：Google Search Essentials、Schema.org spec、sitemaps.org、RFC 9309 (robots.txt)、Apple App Store Review Guidelines、Google Play Policies 都是公开 deterministic 的规则——能用脚本验证的部分**必须**用脚本验证。

---

## 3.5 GSD-lite Harness (v1.2)

L12 v1.2 引入 GSD-lite execution harness（详 `~/.claude/templates/discoverability/harness-contract.md`）。**orchestrator 不再只是 policy router，而是 execution router**：自己 dispatch、自己写 evidence、自己跑 gate.check、自己 handoff。

### 3.5.1 Harness 组件

| 层 | 组件 | 位置 |
|---|---|---|
| Orchestrator | 本 skill (self-dispatch) | `~/.claude/skills/discoverability-orchestrator/SKILL.md` |
| SDK | `discoverability-sdk.py` (10 commands) | `~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py`（**全局单一位置**；canonical 安装链不复制进项目，统一以 `--project-root .` 指向项目）|
| Agents | disc-scope-classifier / disc-evidence-validator / disc-remediation-planner | `~/.claude/agents/` 或项目 `.claude/agents/` |
| Hooks | 5 个 disc-* hooks + _disc-common.js | 项目 `.claude/hooks/` (template 在 `~/.claude/templates/discoverability/hooks/`) |
| State | `.discoverability/state.json` + `runs/<tag>/` | project root |
| Evidence | `evidence/discoverability/<tag>/` (tag-scoped) | project root |
| Config | `discoverability.config.yaml` (含 `harness:` 段) | project root |

### 3.5.2 Tag dimension（v1.2 break change vs v1.1）

evidence 路径加 `<tag>` 维度：

- 旧 (v1.1)：`evidence/discoverability/{seo,aeo,geo,aso}/`
- 新 (v1.2)：`evidence/discoverability/<tag>/{seo,ai-search,local,aso}.json`

`<tag>` 来源：git describe / commit short SHA / 显式传入（见 config `harness.active_release_tag_source`）。

### 3.5.3 Channel key canonicalization

evidence 端 channel key 与 narrow skill 名对应：

| Config 端 key | Evidence channel key | Narrow skill |
|---|---|---|
| `channels.seo` | `seo` | `web-seo` |
| `channels.aeo` | `ai-search` | `web-aeo` |
| `channels.geo` | `local` | `web-local-seo` |
| `channels.aso` | `aso` | `app-aso` |

Config 端 key 名（`aeo` / `geo`）保留是 contract 兼容性；orchestrator + SDK 内部 ALWAYS use canonical channel keys (`ai-search` / `local`)。

---

## 4. Activation 规则速查（按 project type）

详细规则见 `activation-rules.yaml`。简表如下：

| project_type | web-seo | web-aeo | web-local-seo | app-aso |
|---|---|---|---|---|
| `content_site`（blog / 媒体 / 公开文章） | required | required | disabled | disabled |
| `ecommerce`（商品 + 购物车） | required | optional | conditional_local | disabled |
| `local_service`（实体服务 / 门店 / 诊所 / 餐厅） | required | optional | **required** | disabled |
| `b2b_saas_marketing`（marketing site + product docs） | required | warn_only | disabled | disabled |
| `api_with_public_docs`（API 平台 + docs） | required | required | disabled | disabled |
| `pure_backend_api_no_public_surface` | **disabled** | disabled | disabled | disabled |
| `mobile_app`（纯 app） | optional (landing page only) | disabled | conditional_local | required |
| `web_app_plus_mobile_app`（web 产品 + app） | required | optional | conditional_local | required |

**`conditional_local`**：仅当产品涉及 brick-and-mortar / service-area-business 时激活 `web-local-seo`，否则跳过。

具体触发逻辑：`project.physical_locations > 0` OR `len(project.service_areas) > 0`（字段定义在 `discoverability.config.yaml` 的 `project:` 节）。两者皆为 0 / 空时，即便 activation-rules.yaml 标 `conditional_local`，runner 也必须 disable 该 skill 并在 `00-activation.json` 写明原因。详见 §6 决策树底部说明。

**判断流程**：
1. 读 `discoverability.config.yaml` 的 `project_type`
2. 若无该文件 → 询问用户 project_type，**绝不猜测**
3. 按上表激活对应 narrow skill
4. `disabled` 的 skill 不生成 evidence，但 `00-activation.json` 必须记录"为什么 disabled"

---

## 5. discoverability.config.yaml 约定

**Schema source of truth**：`~/.claude/templates/discoverability/discoverability.config.yaml`（顶部带 `_schema_version: "1.0.0"`）。本节是 **SEMI-CRIB 骨架**（顶层结构 + binding 规则）；完整带注释字段示例见 [`references/config-schema.md`](references/config-schema.md)（按需读取，非每次运行必读）。

每个 commercial 项目根目录建议有此配置文件，所有 runner 先读它。顶层键骨架：

```yaml
_schema_version: "1.0.0"
project:          # name / canonical_url / type(8种) / framework / auth_model / locales / regions / physical_locations / service_areas
public_surfaces:  # 实际上线的 surface 列表
channels:         # seo / aeo / geo(=Local SEO) / aso —— 每个是 dict {enabled, state, gate_level}，不是 string 直值
crawler_policy:   # 每 bot 一个 enum: allow|disallow|policy_decision|verify_before_gate|user_initiated_not_robots_controlled
seo: / aeo: / geo: / aso:   # per-domain scope（sitemap/robots/llms.txt/nap/gbp/platforms…）
quality_gates:    # per-domain pass/fail（见 reference 完整列表）
evidence:         # output_dir / report_formats / retention_days
monitoring:       # search_console / chatgpt_referral_tracking / lighthouse_ci
vendor_tools:     # 固定 commit 的外部 runner
```

**Schema 演化规则**（binding）：
- 顶部 `_schema_version` 是 sem-ver；任何 break-change 必须 bump major
- `channels.<domain>` 是 dict（`enabled / state / gate_level`），**不是** string 直值（向后兼容已删除）
- `geo` 这个 config key 名保留是历史原因；语义 = Local SEO，runner 必须路由到 `web-local-seo` skill
- 任何新字段加入 template 后，本骨架 + `references/config-schema.md` 同步

**runner 行为**：缺失字段一律走 `activation-rules.yaml` default。**绝不**在缺失配置时静默激活全部 4 域——会浪费资源 + 输出无意义 evidence。

---

## 6. Evidence 输出 contract

所有 narrow skill 的产出必须落到统一的 **tag-scoped** 目录（`evidence.output_dir` 默认 `evidence/discoverability/`，下挂 `<tag>` 维度 — 见 §3.5.2）。canonical channel key 是 `seo / ai-search / local / aso`（与 §3.5.3 / §10 / frontmatter 一致）：

```
evidence/discoverability/
└── <tag>/                      # tag 维度（git describe / commit SHA / 显式传入，见 §3.5.2）
    ├── 00-activation.json      # 哪些 channel 激活 / 为什么 / project.type
    ├── 00-scope.yaml           # disc-scope-classifier 输出（§10 Step 1）
    ├── seo.json                # channel: seo        owner: web-seo
    │                           #   crawl / metadata / structured-data / core-web-vitals / i18n
    ├── ai-search.json          # channel: ai-search  owner: web-aeo   (config 端别名 aeo)
    │                           #   llms.txt / crawler-policy / citability / content-snapshots
    ├── local.json              # channel: local      owner: web-local-seo (config 端别名 geo)
    │                           #   gbp-profile / nap-consistency / service-area-map / reviews
    ├── aso.json                # channel: aso        owner: app-aso
    │                           #   store-listings / visual-assets / localization / reviews-ratings
    ├── evidence-validation.yaml # disc-evidence-validator 输出（§10 Step 5）
    ├── remediation-plan.yaml    # disc-remediation-planner 输出（§10 Step 6）
    ├── gate-result.yaml        # blocker / warn-only / pass + 失败项（release gate 产物）
    ├── report.md               # human-readable narrative
    └── report.pdf              # release-attached PDF（可选）
#
# Canonical evidence path (v1.2, single source of truth): TAG-SCOPED.
# The 4 narrow SKILL.md and project runners MUST read/write
# `evidence/discoverability/<tag>/<channel>.json` with canonical channel keys
# `seo` / `ai-search` / `local` / `aso`. `aeo` and `geo` are CONFIG-SIDE
# ALIASES ONLY (see §3.5.3): config `channels.aeo` → channel `ai-search`,
# config `channels.geo` → channel `local`. Runners + SDK ALWAYS persist under
# the canonical channel key, NEVER under `aeo` / `geo`, and MUST NOT add
# `01-/02-/03-/04-` or any other prefix. CI artifact ordering is handled by CI
# tooling (sort flags, separate upload names), not by mutating the evidence path.
```

**evidence 格式硬规则**：
- 所有 channel evidence JSON（`<channel>.json`）必须有 `source` 字段（`script` / `api` / `framework_adapter` / `manual_ai_scan`）
- 所有 finding 必须有 `severity`（blocker / warn / info）
- 所有 finding 必须有 `evidence_path`（具体文件 / API endpoint / 截图）
- 同一 finding 在 `report.md` 出现时，必须能反向追溯到 `evidence/` 下的原始数据

---

## 7. Gate 规则分级

| Gate Level | 行为 | 默认适用 |
|---|---|---|
| `blocker` | 失败 → release 阻断，必须修复或显式 waive | web-seo（公开站点）/ web-local-seo（本地业务）/ app-aso |
| `warn-only` | 失败 → 进 report，不阻断 release | web-aeo（新生态，标准未稳定）|

**Blocker 失败项示例**：
- web-seo：sitemap 返回 5xx / robots.txt disallow 全站 / 首页缺 title or description / Core Web Vitals LCP > 4s
- web-local-seo：GBP 配置缺失 / NAP 跨平台不一致 / 服务区域未设置
- app-aso：listing 缺 icon / 缺 screenshots / 缺 keywords / description 空

**Warn-only 示例**：
- web-aeo：缺 llms.txt（非 docs-heavy 项目）/ FAQ schema 缺失 / AI crawler 未明确 allow
- web-seo：image alt 文本覆盖率 < 80% / sitemap 包含 noindex 页面

**严禁**把 warn-only 项偷偷升级成 blocker——会导致 release 误阻断。升级必须显式改 `discoverability.config.yaml` 的 `gate_level`。

---

## 8. 与其他 orchestrator 边界

### 8.1 与 UIUX 主线的关系

L12 是 **UIUX 主线下游的子层**。`uiux-product-orchestrator` 完成 L1-L11（设计 + 实现）后，进入 release 阶段才下放到 L12。

```
UIUX 主线
└─ L1 Discovery → L2 Exploration → L3 Style → L4 Production → ... → L11 Meta
                                                                       └─ L12 Discoverability ← 本 skill
```

调用顺序：`uiux-product-orchestrator` 路由 → 设计 + 实现完成 → `gsd-pipeline-orchestrator` release-readiness → 本 skill → narrow skill 跑 evidence → QA bundle 引用。

### 8.2 与 enterprise-qa-testing 的关系

L12 的 `evidence/discoverability/` 目录可被 `qa-evidence-bundle` 子 skill **引用**，作为 release evidence 的一部分。但：

- L12 evidence **不算** QA test coverage
- L12 不替代 QA 的 smoke / E2E / a11y / perf 测试
- QA 跑 a11y 是无障碍合规，L12 跑的是 discoverability——不重叠（虽然有些规则相关，如 alt text）

### 8.3 与 AppSec 边界（不重叠声明）

L12 处理 discoverability。访问控制 / 认证 / 授权 / 凭据管理 / 漏洞修复 / 威胁建模 全部不属于 L12。

- `robots.txt` / `noindex` / `llms.txt` 是 crawler policy，**不是** access control
- 私密内容如果通过 discoverability 被错误暴露给搜索引擎，L12 **标识 + escalate** 给 `appsec-security-orchestrator`，但不实施访问控制修复
- 详细 AppSec 规则 → `~/.claude/rules/security-appsec.md` 和 `appsec-security-orchestrator` skill

### 8.4 与 dast-baseline-scanning 的边界

discoverability 是**发布后可见性**，DAST 是**安全扫描**，互不替代、互不重叠。任何 security 类问题（漏洞、auth、敏感数据暴露）→ escalate 给 `appsec-security-orchestrator` / `dast-baseline-scanning`，L12 不处理。

### 8.5 与 ux-principles 的边界

`ux-principles` 是 UX 战术 + audit lens，关注 usability。L12 关注 discoverability（被找到）。两者互补但不重叠：

- ux-principles 看 "用户进来后能不能用"
- L12 看 "用户能不能进来"

---

## 9. CLI 约定  →  references/cli-reference.md
> Relocated (SAFE-A appendix — verbatim, not weakened; not needed to execute a run). Read on demand.

---
## 10. 标准 Workflow — Self-dispatch Contract (8 步, v1.2)

> **铁律**：orchestrator 必须按下列 8 步执行；任何 step 失败 → 写 `.discoverability/runs/<tag>/failures.log` + decision=BLOCKED；永不"伪造 PASS"，永不"输出建议但不写 evidence"。

```
Step 0  Load discoverability.config.yaml
        │
        ├─ 缺失 → enter setup mode: 主动询问 project_type
        │   + 从 ~/.claude/templates/discoverability/discoverability.config.yaml 复制模板
        │   + 不静默猜测、不直接 dispatch
        └─ 存在 → continue

Step 1  Skill calls Agent(disc-scope-classifier)
        → 写 evidence/discoverability/<tag>/00-scope.yaml
        失败 → halt + BLOCKED

Step 2  Bash: python ~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py --project-root . init <tag>
        （canonical 安装链不复制 SDK 进项目；统一用全局路径 + --project-root .，
         与 manifests/hook-registry.json install_command 一致）
        → 创建 .discoverability/runs/<tag>/ + evidence/discoverability/<tag>/
        → 写 state.json {active_run_tag, active_run: true, gate_status: PENDING}

Step 3  Per active_channel in scope, dispatch narrow skill:
        - seo:        Skill(web-seo)
        - ai-search:  Skill(web-aeo)
        - local:      Skill(web-local-seo)
        - aso:        Skill(app-aso)
        Narrow skill 必须 Script-first（§3 宪法）+ 写 channel evidence JSON

Step 4  Per channel: Bash discoverability-sdk evidence.append <tag> <channel> <file>
        → 归一化进 canonical schema

Step 5  Agent(disc-evidence-validator)
        → 写 evidence-validation.yaml
        → 强制规则: 任何 required channel 全 manual_ai_scan → BLOCKED
                  llms.txt grading per project_type (api_with_public_docs only blocker)
                  AEO/GEO score 类 finding 不能 blocker

Step 6  Agent(disc-remediation-planner)
        → 写 remediation-plan.yaml
        → 按 owner 分派: frontend / uiux / growth / mobile / appsec / qa

Step 7  Bash: discoverability-sdk gate.check <tag>
        → 写 gate-result.yaml + 更新 state.json
        → exit code: 0 PASS/WARN | 1 FAIL | 2 BLOCKED | 3 STALE
        → governed release gate (CLAUDE.md §3.7): 当 gate-result.yaml 充当
          release verdict 时，verdict 只能来自 deterministic SDK gate.check +
          evidence；Dynamic Workflows / ultracode 只能 scout 候选发现，
          NEVER 产出 release verdict，无 self-approval。

Step 8  Handoff:
        ├─ validation.appsec_handoff.required → escalate to appsec-security-orchestrator
        ├─ enterprise-qa-testing 同步运行 → 提供 gate-result.yaml 引用
        └─ gsd-pipeline-orchestrator release-readiness phase → 反馈 exit_code
```

### 10.1 Failure handling

| Step 失败 | 行为 |
|---|---|
| 0 (config absent) | 进入 setup mode，不 dispatch |
| 1 (classifier) | failures.log + BLOCKED + halt |
| 2 (sdk init) | failures.log + BLOCKED + halt |
| 3 (narrow skill) | per-channel failure 记录，继续其他 channel；最后 validator 会处理 |
| 5 (validator) | 写 partial validation + 标记 unknown_status；gate 默认 BLOCKED |
| 6 (planner) | warn 但允许 gate 继续；handoff 信息不完整 |
| 7 (gate.check) | exit code 直接报告；不重试 |

### 10.2 反模式（v1.2 新增）

- ❌ 只输出 narrative 建议而不写 evidence 文件 — 违反 GSD-lite harness 契约
- ❌ 跳过 Step 1（scope-classifier）直接 dispatch narrow skills — 没 scope 就没 activation 依据
- ❌ Step 7 失败但仍宣称"discoverability done"
- ❌ 把 manual_ai_scan 当 deterministic evidence
- ❌ 把 AEO/GEO score 类 finding 作为 blocker（AI search 官方 ranking 未公开）
- ❌ 一次性激活 4 个 narrow skill 而不按 scope 表
- ❌ 把 narrow skill 跑出的 raw output 直接当 channel evidence —— 必须经过 evidence.append 归一化

---

## 11. 反模式（不要这么做）

1. ❌ **让 AI 自己"凭感觉审计 SEO"** — 必须先跑脚本 / API / framework adapter（Script-first 硬规则）
2. ❌ **把内部 citability score 包装成 Google / OpenAI / Anthropic 官方 ranking factor** — 官方都没公开 ranking factor，内部分数只能叫"内部启发式分数"
3. ❌ **把 llms.txt 当所有项目的 release blocker** — llms.txt 还在生态早期（Mintlify 提案 + 部分采用），是 docs-heavy / API-heavy 项目的 enhancement，不是 universal requirement
4. ❌ **把 robots.txt 当 access control** — robots.txt 是 crawler policy，礼貌爬虫遵守，恶意爬虫不会遵守。真正的访问控制走 server-side authorization
5. ❌ **把 web-aeo 和 web-local-seo 混用** — AEO 是 Answer Engine Optimization（AI search / Generative Engine Optimization，业界 2025-2026 GEO 缩写默认指此）；`web-local-seo` 是 Local SEO（Google Business Profile / Maps / NAP）。**遇到 "GEO" 必须按 §2.5 GEO Ambiguity Resolver 消歧**，不要凭印象路由
6. ❌ **SEO / AEO / Local SEO / ASO 互相串味** — 4 域分开 evidence 路径、分开 gate、分开 report 章节
7. ❌ **在没有 framework adapter 的情况下直接让 AI 改 metadata** — 应该先确认有没有 Next.js Metadata API / Nuxt useSeoMeta / Astro `<head>` slot，能用 framework 就用 framework
8. ❌ **把 Lighthouse / PSI 跑出来的"performance score"等同于"SEO score"** — 这是两个 audit 类别，Lighthouse 同时跑 SEO + Performance + a11y + Best Practices，不要混
9. ❌ **修改 sitemap.xml 时不验证 sitemaps.org schema** — schema 错的 sitemap 会被搜索引擎拒收，必须用 validator
10. ❌ **AEO 一上来就改 prompt 让自家品牌排第一** — AEO 是优化"可被引用性"，不是"指令注入 AI"。后者既无效，又有违反 OpenAI / Anthropic 政策的风险
11. ❌ **只输出 prompt-style narrative 建议而不写 evidence** —— harness 模式下 orchestrator 必须落 evidence 文件 + gate-result.yaml，否则视为未完成
12. ❌ **跳过 self-dispatch 8 步**（直接调 narrow skill 而不经 §10 contract）—— 会导致 evidence 路径错乱 + gate.check 拒绝识别
13. ❌ **AEO/GEO score 类 finding 作为 blocker** —— AI search 官方 ranking factor 未公开，本体系所有 score 都是 internal_heuristic
14. ❌ **deploy 前不跑 gate.check** —— harness 配套 disc-deploy-gate hook 会 PreToolUse 阻断；orchestrator 自身也不应宣称完成

---

## 12. 何时**不**用本 orchestrator

- **pure backend API，无 public surface** — 没人会"搜到"一个内部 API；跳过
- **internal admin / staging-only** — 不需要被发现；跳过（且 staging 应该 `robots.txt: disallow` + auth-gate）
- **1-3 行 bugfix** — 不涉及 discoverability metadata 时直接改
- **设计阶段 / prototype 阶段** — 没上线就没必要做 discoverability
- **legacy migration 中途状态** — 等 migration 完成后再做完整 audit
- **用户明确说"不用 SEO"** — 尊重，但要确认是 internal tool / not public

---

## 13. 引用源  →  references/sources.md
> Relocated (SAFE-A appendix — verbatim, not weakened; not needed to execute a run). Read on demand.

---
## 15. Harness contract reference

完整 ground-truth contract（SDK / agents / hooks / schemas）:
`~/.claude/templates/discoverability/harness-contract.md`

依赖文件清单：
- `~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py` (SDK 10 commands)
- `~/.claude/agents/disc-scope-classifier.md`
- `~/.claude/agents/disc-evidence-validator.md`
- `~/.claude/agents/disc-remediation-planner.md`
- `~/.claude/templates/discoverability/discoverability.config.yaml` (含 `harness:` 段)
- `~/.claude/templates/discoverability/gate-result.schema.yaml`
- `~/.claude/templates/discoverability/state.schema.json`
- `~/.claude/templates/discoverability/hooks/_disc-common.js`
- `~/.claude/templates/discoverability/hooks/disc-{session-context,mark-stale,robots-sitemap-guard,deploy-gate,evidence-required}.js`
- `~/.claude/templates/discoverability/settings-snippet.json`

### 15.1 Safety-critical name freeze

下列名称冻结（hook / agent / SDK command 通过名字识别调用，改名 = 打掉 safety gate）：

- skill: `discoverability-orchestrator`, `web-seo`, `web-aeo`, `web-local-seo`, `app-aso`
- agent: `disc-scope-classifier`, `disc-evidence-validator`, `disc-remediation-planner`
- hook: `disc-session-context`, `disc-mark-stale`, `disc-robots-sitemap-guard`, `disc-deploy-gate`, `disc-evidence-required`
- SDK command: `init`, `classify`, `audit`, `evidence.append`, `evidence.validate`, `gate.check`, `report`, `mark-stale`, `explain`, `status`
