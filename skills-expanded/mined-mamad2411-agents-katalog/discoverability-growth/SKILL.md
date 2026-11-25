---
name: discoverability-growth
canonical_id: discoverability.growth
aliases: [discoverability-growth, seo-growth, keyword-strategy, content-gap]
version: 1.0.0
status: stable
created_date: 2026-06-15
parent: discoverability-orchestrator
layer: L12
sibling-skills:
  - web-seo
  - web-aeo
  - web-local-seo
  - app-aso
children: []
upstream:
  - discoverability-orchestrator
downstream: []
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
forbidden-tools: []
disable-model-invocation: false
description: >-
  L12 Discoverability GROWTH layer — turns real evidence (post-launch measurement, audits, crawls) into a prioritized growth backlog: keyword strategy, content-gap analysis, internal linking, programmatic SEO. Script-first via advertools and keyword-research tooling; AI only ranks deterministic output and never invents volumes or rankings. Downstream owner of the remediation planner growth tasks and consumer of measurement.json. Not on-page SEO mechanics (web-seo), AI citation (web-aeo), Local SEO (web-local-seo) or metric pulling (disc-measurement-puller).
---

# discoverability-growth — L12 Growth 子层

> L12 Discoverability narrow skill。上游编排：`discoverability-orchestrator`。
> 同级邻居（边界互斥）：`web-seo`（on-page 机制）/ `web-aeo`（AI 引用）/ `web-local-seo`（Local SEO）/ `app-aso`（商店）。
> 这是 `disc-remediation-planner` 路由的 **`growth` owner** 的真实下游实现（此前悬空，无执行者）。

---

## 0. 定位（不要误解）

L12 的其他 4 个 narrow skill 都在回答**当前已上线的页面 discoverability 形态对不对**（robots / metadata / llms.txt / 商店 listing）。`disc-measurement-puller` 回答**上线后实际效果如何**（真实展示/点击/排名）。

**这个 skill 回答的是第三个问题：基于这些证据，接下来该做什么才能被更多人找到？**

它做五件事，全部 evidence-driven：

1. **Keyword strategy** —— 关键词机会发现（autocomplete / related / SERP feature gap）+ 搜索意图 → 页面类型映射（§4）
2. **Content-gap analysis** —— 站内已覆盖 vs 应覆盖的主题差距（站点爬取 + 竞品爬取对比）
3. **Prioritized growth backlog** —— 把机会按 effort/impact 排成可执行清单
4. **Programmatic-SEO patterns** —— 大规模模板化页面的合规模式（避免 doorway / thin-content）
5. **Off-site authority advisory**（§4.5）—— 站外权威 / digital-PR / 未链提及的 **advisory** 清单（永不买链、永不执行、永不 gate）

它**不是** marketing 套件、不发内容、**不买外链 / 不碰任何 Google 链接垃圾红线**（§4.5.3）、不碰社媒投放——off-site 这块只产 **advisory backlog**（该争取什么链接），真正去赢得链接是人做的。只产出"该写 / 该改 / 该争取什么"的 evidence-backed backlog。

### 不在本 skill 范围

| 邻居 | 处理内容 |
|---|---|
| `web-seo` | robots / sitemap / canonical / hreflang / metadata / structured-data / Lighthouse —— on-page **机制** |
| `web-aeo` | llms.txt / citability / AI crawler policy —— AI **引用** |
| `web-local-seo` | Google Business Profile / NAP / Maps —— **Local** |
| `app-aso` | App Store / Google Play listing —— **商店** |
| `disc-measurement-puller` | 从 GSC/GA4/Bing API **拉**真实指标 —— 本 skill **消费** measurement.json，不产出 |
| `appsec-security-orchestrator` | 任何 security / access control |

**铁律边界**：本 skill 发现"某私密 path 被大量搜索/抓取"这类信号时，**只标识 + escalate**，不实施访问控制；programmatic SEO 绝不生成 thin/doorway 页（见 §6）。

---

## 1. 执行宪法 —— Script-first, AI-last（继承 L12）

与全 L12 一致：**先跑脚本/CLI 出 evidence，AI 只解读 + 排序，绝不让 AI 凭印象编造搜索量/排名/竞争度**。

### 1.1 L12 5 级 priority ladder（本 skill 适用）

| Level | 类型 | growth 中的体现 | auto/manual |
|---|---|---|---|
| 1 | Deterministic script / API / CLI | `advertools` crawl + SERP/keyword、`seo-keyword-research-tool` autocomplete/related、GSC top-query 导出（来自 measurement.json）、sitemap 解析 | 全自动 |
| 2 | Structured evidence parser | 把 crawl / keyword 输出 normalize 成 backlog item schema | 全自动 |
| 3 | AI synthesis from evidence | AI 读 normalized 数据 → 聚类成 topic cluster → 排 effort/impact 优先级 | 全自动 |
| 4 | Manual AI brainstorm（LAST RESORT） | 仅当无 crawl 权限 / 无 API 时补充选题脑暴，evidence 必标 `source: manual_ai_scan` + `confidence: low` | **降权** |

**反规则（违反即不可信）**：
- ❌ AI 直接"想"一批关键词并标上一个编造的"月搜索量 8100"——搜索量必须来自工具/API，无来源就标 `volume: unknown`
- ❌ 把 AI 的选题建议包装成"数据驱动的关键词机会"而无任何 crawl/SERP evidence
- ❌ 用编造的"竞争度 KD 42"当 backlog 排序依据

---

## 2. 工具（全部 free / OSS；CLI 优先）

> **安装命令留档**（staged tools local，不全局安装、不 wire；用到时在项目内装）：

```bash
# advertools — MIT, Scrapy-based SEO crawler + SERP/keyword utilities
pip install advertools

# seo-keyword-research-tool — MIT, CLI: autocomplete + related keyword expansion
pip install seo-keyword-research-tool
```

| 工具 | License | 用途 | 关键能力 |
|---|---|---|---|
| **advertools** | MIT | 站点/竞品爬取 + 关键词/SERP | `crawl()` (Scrapy SEO spider，导出 title/h1/meta/links/word-count CSV)、`crawl_headers()`、`word_frequency()`、`kw_generate()` (关键词组合)、SERP/log-file 分析 |
| **seo-keyword-research-tool** | MIT | 关键词扩展 | CLI `seo -q "<seed>"` → autocomplete + related keywords，多引擎 |
| **GSC top queries**（已在 measurement.json） | free API | 真实已排名词 | `disc-measurement-puller` 拉的 `rows[].query` —— 现有真实流量词，是最高置信度的 keyword 起点 |

> 若工具未安装：本 skill 提示安装命令并**降级**到 Level 4（manual，标 low confidence），**绝不**伪造工具输出当 Level 1 evidence。

---

## 3. 核心工作流（5 步）

```
Step 1  Seed harvesting（收集种子）
        ├─ 最高置信度：measurement.json 的 GSC rows[].query（已有真实展示/点击的词）
        ├─ 业务种子：用户/config 提供的核心主题词
        └─ 站点已覆盖词：advertools crawl 现站点 → word_frequency / title / h1

Step 2  Keyword expansion（脚本扩展，不靠 AI 编）
        ├─ seo-keyword-research-tool: seo -q "<seed>"  → autocomplete + related
        ├─ advertools kw_generate（组合/match-type 变体）
        └─ 输出 raw → evidence/discoverability/<tag>/raw/keywords.*.json|csv

Step 3  Content-gap analysis（站内 vs 应覆盖）
        ├─ advertools crawl 自站 sitemap → 已覆盖 URL/主题清单
        ├─ （可选）crawl 1-3 个竞品站 → 竞品覆盖主题
        ├─ diff：扩展关键词/竞品主题 中，自站未覆盖的 → gap
        └─ 标注每个 gap：覆盖状态(none/thin/partial) + 证据 URL

Step 4  AI synthesis → prioritized backlog（AI 只排序，不造数）
        ├─ 把扩展词聚类成 topic cluster（pillar + supporting）
        ├─ 每个簇/词分类 search intent（informational / commercial / transactional / navigational；local → handoff web-local-seo）→ 据此定 target_page_type（blog/guide / product / category / comparison / landing）
        ├─ 每个 backlog item 评 effort（S/M/L）× impact（来自真实 GSC 展示量/SERP feature/gap 大小）
        └─ 内链机会：crawl 出的孤立页 / 高权重页未指向 gap 页

Step 5  Emit growth-backlog.* + handoff
        ├─ 写 evidence/discoverability/<tag>/raw/growth-backlog.json
        ├─ （在 harness run 内）经 web-seo channel append 或独立留档
        └─ handoff：on-page 实施 → web-seo / AI 引用优化 → web-aeo / 内容写作 → 团队
```

### 3.1 与 measurement 的闭环（核心增值）

本 skill 的最高价值在于**消费 `disc-measurement-puller` 的真实数据**：

- `measurement.json` 里 GSC `rows[].query` = 你**已经在排名但可能在第 2 页**的词 → 这些是 ROI 最高的 growth 目标（小改动可上首页）
- `measurement-compare.json` 的 `regressed` 指标 → 优先级提升（曾经有效、现在掉了的主题）
- 高展示低点击（impressions 高 / ctr 低）的词 → title/meta 改写机会（routes to web-seo）

> 无 measurement.json 时本 skill 仍可跑（纯 keyword + crawl），但要在 backlog 里标注"未接入真实流量数据，impact 估算置信度降低"。

---

## 4. growth-backlog item schema

每个 backlog item 落 `evidence/discoverability/<tag>/raw/growth-backlog.json`：

```json
{
  "_schema_version": "1.0.0",
  "tag": "<tag>",
  "channel": "seo",
  "source": "script",
  "generated_by": "discoverability-growth",
  "topic_clusters": [
    {
      "pillar": "kubernetes cost optimization",
      "pillar_status": "thin",
      "evidence_ref": "raw/site-crawl.csv#/url/42",
      "supporting": [
        {
          "keyword": "reduce eks node cost",
          "intent": "commercial",
          "target_page_type": "comparison",
          "volume": "unknown",
          "volume_source": "no_volume_api",
          "current_position": 14.2,
          "position_source": "measurement.json#/providers/gsc/rows/7",
          "gap": "none_on_site",
          "effort": "M",
          "impact": "high",
          "impact_basis": "GSC shows 3.2k impressions, position 14 → page-2; small content add likely moves to page-1",
          "owner_handoff": "web-seo (on-page) + content team (write)"
        }
      ]
    }
  ],
  "internal_linking_opportunities": [
    {"from": "https://x/blog/high-authority", "to": "https://x/blog/orphan-gap-page",
     "evidence_ref": "raw/site-crawl.csv#/links", "reason": "orphan page, 0 inbound internal links"}
  ],
  "programmatic_seo_candidates": [
    {"pattern": "/compare/<toolA>-vs-<toolB>", "estimated_pages": 120,
     "uniqueness_plan": "each page ≥400 unique words + real data table per pair",
     "doorway_risk": "mitigated", "owner_handoff": "web-seo + content team"}
  ],
  "notes": "<≤2 lines>"
}
```

**硬规则**：
- 任何 `volume` 无工具来源 → `"volume": "unknown"` + `"volume_source": "no_volume_api"`，**不**编数字
- 任何 `current_position` 必须来自 measurement.json（真实 GSC）或标 `unknown`
- `impact` 评级必须有 `impact_basis`（指向真实 evidence），不能是"感觉重要"
- 每个 supporting keyword 必须带 `intent`（informational/commercial/transactional/navigational）+ `target_page_type`（决定该词该落 blog/product/category/comparison/landing 哪种页）—— 这是"对的查询配对对的页"的核心纪律（Google SOP Phase 4/5）；`local` intent 的词 handoff `web-local-seo`

---

## 4.5 Off-site authority & digital-PR advisory backlog（站外权威 — advisory-only）

> **加入 2026-06-27（SEO-doc audit P1）。** 此前整个 L12 没有任何 skill 拥有"站外权威 / 外链 / digital PR"——`web-seo` 只管站内、`web-aeo` 的 brand-entity 只是 AI 引用信号、本 skill §0 又声明"不买外链"。结果：Google 官方 SOP 里 off-page 最高杠杆的一整块（authority / backlinks）**无主**。本节补上，且**严格限定为 advisory**。

### 4.5.0 边界（本节能做什么、绝不做什么）

| ✅ 本节做（advisory backlog）| ❌ 本节绝不做 |
|---|---|
| 产出"可争取的 link-worthy 资产 / digital-PR / 目录 / 未链提及"清单 | 自动外联、发邮件、代发 PR |
| 用 **GSC Links report**（免费、deterministic）做现状基线 | 买链接 / 换链 / PBN / 评论灌水（红线，见 §4.5.3）|
| 把 off-site 机会按 effort/impact 排进 backlog（severity 永远 warn/info）| 把"外链数"当 release blocker（authority 是长期积累，不可 gate）|
| 标注哪些是**手动 / 线下**动作（大部分 off-page 本质如此）| 新增第 5 个 evidence channel 或新 gate（本 skill 不是 channel、不是 gate）|

> **为什么是 advisory**：外链绝大多数是 off-platform + 人际动作（PR pitch、合作、赞助），脚本无法"执行"。本节能 deterministic 的只有**现状基线**（GSC Links）+ **机会枚举**；真正去赢得链接是人做的。所以本节产出是 backlog/建议，`severity` 一律 `warn`/`info`，**永不 blocker**（与 §6 反模式"把 growth backlog 当 release blocker"一致）。

### 4.5.1 Script-first 锚点：GSC Links report（免费、deterministic）

唯一能脚本化的 off-site 现状真相源是 **Google Search Console Links report**（免费）：top linking sites / top linked pages / 锚文本分布。它由 `disc-measurement-puller` 经 GSC API 拉（与 search-analytics 同源凭证），落独立 raw export；本 skill **消费**它，不自己拉。

- 有 GSC Links 数据 → backlog 基于真实 referring domains（"竞品有、你没有的 referring domain" = 可争取目标）
- 无数据 → 标 `referring_domains: unknown`，机会清单仍可产（基于 link-worthy 资产类型），但置信度降低，**绝不编造外链数**

### 4.5.2 Advisory backlog item（off-site 类）

并入 `growth-backlog.json` 的新数组 `offsite_authority_opportunities[]`（与 §4 同文件，severity warn/info）：

```json
{
  "offsite_authority_opportunities": [
    {
      "type": "linkable_asset | digital_pr | directory | unlinked_mention | partnership",
      "title": "原创基准数据报告：2026 K8s 成本基准",
      "rationale": "原创数据是最稳的自然外链磁铁（Google: link-worthy original research）",
      "evidence_ref": "raw/gsc-links.json#/top_linking_sites  (or 'unknown' if no GSC Links)",
      "action_mode": "manual",
      "effort": "M", "impact": "high",
      "impact_basis": "竞品该主题有 N 个 referring domains，你 0（GSC Links 对比）",
      "owner_handoff": "team (PR/content) — 本 skill 只产清单，不外联"
    }
  ]
}
```

机会类型（对照 Google 官方安全做法）：
- **linkable_asset** —— 原创研究 / 计算器 / 模板 / 行业统计 / 指南（自然外链磁铁）
- **digital_pr** —— 记者 / 播客 / newsletter / 行业 blog 的 pitch 角度（清单，不代发）
- **directory** —— 与业务相关的**正经**目录（非链接农场）
- **unlinked_mention** —— 品牌被提及但未加链接 → 半自动检测（品牌名 search），人工去要链接
- **partnership** —— 供应商 / 协会 / 高校 / 本地组织（Local 的本地外链 → 与 `web-local-seo §13.5.4` prominence 呼应）

### 4.5.3 Google 链接垃圾红线（AVOID — 永不建议、永不执行）

下列一律**不**进 backlog、**不**建议、**不**执行（违反 Google link-spam policy，会致排名下降 / 移除）：

| ❌ 红线 | 说明 |
|---|---|
| 买 / 卖链接（含用 goods/services 换 do-follow 链）| Google link-spam policy 明确禁止 |
| PBN（private blog network）| 人为操纵的链接网络 |
| 大规模链接交换（"你链我我链你"）| 互惠链接滥用 |
| 隐藏链接 / 隐藏文本 | cloaking 类 |
| 评论区 / 论坛 / UGC 灌链 | user-generated spam |
| 寄生 SEO / site-reputation abuse | 借高权威站发垃圾内容 |
| 关键词堆砌锚文本的批量外链 | 过度优化锚文本 |

> 这是 §0 "不买外链" 红线的完整版——把一句话扩成**完整 AVOID 清单**，既是给用户的护栏，也是给 AI 的硬约束：**任何 off-site 建议若落入上表，立即丢弃**。安全做法只有一条主线：**做出值得被链接的东西，然后让真实的人发现它**（Google: earn links, never manipulate）。

---

## 5. CLI 命令示例

> **路径约定（v1.2 harness）**：raw 产物写 tag-scoped `evidence/discoverability/<tag>/raw/`。本 skill 产出的 backlog 主要是**信息性 growth 输出**（不是 release blocker——growth 是前瞻规划，不阻断发布）。若在 harness run 内运行，可经 `discoverability-sdk evidence.append <tag> seo <file>` 把 SEO 域可执行 finding 归并到 `seo.json`（severity 一律 `warn`/`info`，growth 永不 blocker）。下例用 shell 变量 `TAG`。

```bash
mkdir -p "evidence/discoverability/$TAG/raw"

# 1. 爬自站（导出 title/h1/meta/word-count/links）
python -c "import advertools as adv; adv.crawl('https://example.com', \
  'evidence/discoverability/'$TAG'/raw/site-crawl.jl', \
  custom_settings={'CLOSESPIDER_PAGECOUNT': 500})"

# 2. 关键词扩展（autocomplete + related）
seo -q "kubernetes cost optimization" \
  > "evidence/discoverability/$TAG/raw/keywords.expanded.json"

# 3. advertools 关键词组合（match-type 变体）
python -c "import advertools as adv, json; \
  print(adv.kw_generate(['eks','gke'], ['cost','pricing']).to_json(orient='records'))" \
  > "evidence/discoverability/$TAG/raw/keywords.generated.json"

# 4.（可选）爬竞品做 content-gap
python -c "import advertools as adv; adv.crawl('https://competitor.com', \
  'evidence/discoverability/'$TAG'/raw/competitor-crawl.jl', \
  custom_settings={'CLOSESPIDER_PAGECOUNT': 300})"

# 5. （若有真实流量）读 measurement.json 的 GSC top queries 作高置信度种子
python -c "import json; d=json.load(open('evidence/discoverability/'$TAG'/measurement.json')); \
  print(json.dumps(d.get('providers',{}).get('gsc',{}).get('rows') or [], ensure_ascii=False))" \
  > "evidence/discoverability/$TAG/raw/gsc-top-queries.json" 2>/dev/null || \
  echo '[]  # no measurement.json yet — backlog impact estimates lower confidence'
```

> AI 在拿到 step 1-5 的 raw 输出后，做 Step 4 synthesis（聚类 + 排序），写 `growth-backlog.json`。**AI 不重跑 crawl，只解读已有 evidence。**

---

## 6. 反模式（不要这么做）

| ❌ 反模式 | ✅ 正确做法 |
|---|---|
| AI 凭印象列关键词并编造搜索量 | 关键词来自 autocomplete/related/GSC；无 volume API 就标 `unknown` |
| 把 growth backlog 当 release blocker | growth 是前瞻规划，severity 永远 warn/info，绝不阻断发布 |
| programmatic SEO 生成上千 thin/doorway 页 | 每个模板页 ≥ 400 unique words + 真实数据；无独特价值的组合不生成（Google doorway policy） |
| 不接 measurement.json 就估 impact | 有真实 GSC 数据时必须用；无数据时显式标"低置信度估算" |
| 把 on-page 改动直接做了 | 发现 canonical/meta/sitemap 问题 → handoff 给 `web-seo`，本 skill 只产 backlog |
| 把 AI 引用优化塞进来 | llms.txt / citability → `web-aeo`，不在本 skill |
| 爬竞品时无视 robots / rate limit | advertools 尊重 robots + 设 CLOSESPIDER 上限；只爬公开内容 |
| 发现高流量私密 path 自己改权限 | 标识 + escalate `appsec-security-orchestrator`，不碰 access control |

---

## 7. 与 harness / orchestrator 集成

### 7.1 作为 `growth` owner 的下游

`disc-remediation-planner`（contract §6.3）把这些 finding 路由到 `growth` owner：
- `seo-keyword-coverage-gap`
- keyword strategy / content gap 类 finding

此前 `growth` owner **无下游执行者**（悬空）。本 skill 是它的真实落地：planner 产出 `tasks.growth[]` → 本 skill 接手 → 跑 keyword/crawl → 出 `growth-backlog.json`。

> 注：`disc-remediation-planner` 的 owner 表也把部分 **Local business/GBP/NAP** finding 暂挂在 `growth` owner 名下——那些**仍归 `web-local-seo`** 实施（Local SEO 机制不在本 growth skill 范围，见 §0 边界表）。本 skill 只接 keyword strategy / content-gap 类 growth 任务。

### 7.2 触发方式

- 用户直接说 growth / keyword strategy / content gap / 程序化 SEO / 该写什么内容 → 本 skill 直接接管（narrow skill 自己 trigger，不经 orchestrator 中转）
- orchestrator 综合 audit 后，remediation-plan 有 `growth` 任务 → 本 skill 执行
- 与 measurement 配合：先 `disc-measurement-puller` 拉数 → 本 skill 消费 measurement.json 做高置信度 backlog

### 7.3 handoff 出口

| backlog 项类型 | handoff 到 |
|---|---|
| on-page 实施（canonical/meta/sitemap/structured-data） | `web-seo` |
| AI 引用友好度（答案块/llms.txt） | `web-aeo` |
| Local 主题（门店/服务区） | `web-local-seo` |
| 内容写作（实际写文章） | 团队/内容 owner（本 skill 不写最终内容，只产选题 + 大纲建议） |
| 站外权威 / digital-PR / 外链争取（§4.5）| 团队（PR / 内容 / BD）—— 本 skill 只产 advisory 清单，不外联、不代发 |
| 高流量私密 path 暴露 | `appsec-security-orchestrator`（escalate，不修） |

---

## 8. 完成判据

本 skill 视为"已完成一轮 growth 分析"，必须满足：

- [ ] 至少跑过 1 个 deterministic source（advertools crawl / seo-keyword-research-tool / GSC top-queries），raw 产物在 `<tag>/raw/`
- [ ] `growth-backlog.json` 已生成，每个 item 有 `evidence_ref` + `effort` + `impact` + `impact_basis`
- [ ] 任何无工具来源的 volume/position 字段已显式标 `unknown` / `no_volume_api`（零编造）
- [ ] backlog 已按 effort × impact 排序，最高优先级项可追溯到真实 evidence（GSC 展示量 / gap 大小 / SERP feature）
- [ ] programmatic SEO 候选（如有）每个都有 `uniqueness_plan` 且 `doorway_risk: mitigated`
- [ ] on-page / AEO / Local / appsec 类发现已正确 handoff（不在本 skill 实施）

不要在 evidence 缺失的情况下声称"做了关键词策略"。

---

## 9. 参考

- L12 constitution（script-first，never AI-guess metrics）：`~/.claude/rules/discoverability-l12.md`
- Contract（tag-scoped evidence dir）：`~/.claude/templates/discoverability/harness-contract.md` §1 §6.3
- Owner 路由（growth owner 定义）：`~/.claude/agents/disc-remediation-planner.md` §2
- Measurement 上游：`~/.claude/agents/disc-measurement-puller.md`（先拉数，本 skill 消费）
- advertools docs：https://advertools.readthedocs.io
- Google doorway pages policy（programmatic SEO 红线）：https://developers.google.com/search/docs/essentials/spam-policies#doorways
