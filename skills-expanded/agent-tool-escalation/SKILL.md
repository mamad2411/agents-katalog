---
name: agent-tool-escalation
description: Agent 工具调用失败的复盘与升级阶梯。当用户提到 "工具失败"、"403 / 404 抓不到"、"clone 不动"、"为什么不直接用 gh"、"toolcalling issue"、"工具调用问题"、"如何避免（同样的失败）"、"工具升级"、"escalation"、复盘 agent 工具使用反模式时使用。提供完整工具阶梯参考、历史失败案例、AskQuestion 之前的自检三问。
---

# Agent Tool Escalation

> **核心原则**：低权限工具失败时升级**工具**，不要升级**用户**。
> 想要硬保障的话，把本文「自检三问」沉淀成 agent 的 always-apply 规则（各家 agent 的规则机制见 `../openorder/docs/compatibility.md`）；本 skill 是「按需展开」的完整参考。

## AskQuestion 之前的自检三问（每次失败都跑）

1. 还有什么工具我没试？
2. 有没有一条 ≤3 秒的环境探针能澄清这个不确定性？
3. 如果用户告诉我答案，他会反问"你为什么不自己查"吗？

三问全过 → 才允许 AskQuestion。

## 「修正已有信息」之前的自检三问（NEW，Case 3 教训）

任何"我发现 v1 写错了，要修正"的瞬间，先停下，跑这三问：

1. **我打算推翻的是什么** —— 是新发现 vs 已有 baseline 的冲突，还是仅凭"我以为"的内省怀疑？
2. **支持我修正的证据是什么** —— 是官方公告 / 一手数据 / 用户原话（ground truth），还是逻辑推断 / 类比 / "印象"？
3. **如果我错了，污染半径多大** —— 这个修正会衍生几个论断？会被几个文件引用？会污染哪个 framework？

**任何一问不通过 → 必须先 WebFetch 官方源 / 跑环境探针 / 直接 AskQuestion，不允许直接修正。**

> **核心原则**：补充新信息的证据门槛 < 修正已有信息的证据门槛 < 全面推翻已有结论的证据门槛。门槛比例 1 : 10 : 100。

## Case 6：vector 路径搜索反模式（NEW，2026-05-10 晚）

### 反模式描述

判断"A 跟 B **没有**关系 / **没有**合作 / **是 narrative 不是事实**"时，**只用 1-2 条直接关键词搜索**（如 "A B partnership"、"A B Inphi"），**没有穷尽 vector 路径**：

- A → 第三方 → B（A 卖材料给 C，C 被 B 收购）
- A → 共同技术 → B（A、B 都用同一种技术 / 平台 / foundry）
- A → 共同投资人 → B（A、B 都被同一基金投）
- A → 共同客户 → B（A、B 都卖给同一家 hyperscaler）
- A → 论文/学术 → B（A 在 B 的论文 acknowledgment 里被点名）

**结果**：在没找到直接合作公告时，错误地下"没有合作"结论 + 强烈用词（"散户 narrative"、"不是事实"），并把这个错误结论沉淀进知识库。

### 真实案例（2026-05-10 LWLG-Polariton-MRVL）

| 阶段 | 行为 | 错误本质 |
|---|---|---|
| 17:25 v1.0 | 用户问 "LWLG 是不是有个技术和 MRVL 密切相关？" | 触发 |
| 17:25 v1.0 | 我搜 "Lightwave Logic Marvell partnership" / "LWLG Marvell Inphi" → 找不到 | **只用直接关键词** |
| 17:25 v1.0 | 写入 LWLG.md v1.0：「LWLG 跟 MRVL **没有**任何官方公告的直接合作」+「投资者论坛叙事是**散户 narrative，不是事实**」 | **强烈否定 + 沉淀进档案** |
| 17:35 | 用户提供 [PhotonCap "What Marvell Bought Was the Slot"](https://photoncap.net/p/what-marvell-bought-was-the-slot) + 2 张截图 | ground truth 触发 |
| 17:50 v1.1 | 5 个独立官方源验证：MRVL 4/22 收购 Polariton + Polariton 5+ 年用 LWLG Perkinamine + Optica 2025 record device 论文 acknowledgment 明确名 LWLG | **完全推翻 v1.0** |

→ **正确搜索路径**：`LWLG Polariton` + `MRVL Polariton` + `Polariton ETH spinoff` + `Polariton plasmonic chromophore` —— 任何一条都能立即命中 5+ 年合作历史 + 4/22 收购公告。

### 「下"没有 X"结论」之前的自检三问

1. **直接关键词搜了几条？** ≤ 2 条 → 立即 stop，必须搜 ≥5 条 vector 路径
2. **A 跟 B 中间可能有什么 vector？** 列出至少 3 个候选第三方（共同 foundry / 共同收购方 / 共同 hyperscaler / 共同论文 / 共同 supplier / 共同投资人）
3. **如果我下"没有"结论，污染半径多大？** 涉及几个公司档 / 几个 framework / 几个 portfolio 论据？污染半径越大，标准越高

**任何一问不通过 → 不允许写"X 跟 Y 没有合作 / 不是事实 / 散户 narrative" 类强否定句到知识库**

### vector 路径搜索 checklist（投资 / 公司关系判断时强制跑）

下结论 "A 跟 B 没合作" 之前，至少跑下面 6 类搜索：

```
1. "A B"                       直接合作（最弱信号）
2. "A B partnership/M&A/JV"    直接公告
3. "A acquired by B" / "A acquired"  → 找到收购公告再搜该公司跟 B 关系
4. "B acquired" + 列出 B 近 3 年收购清单 → 检查这些被收购公司跟 A 是否有关
5. "A foundry" / "A platform"   找 A 的 foundry/平台合作伙伴 → 检查这些伙伴是否跟 B 有关
6. "A scientific paper" / "A acknowledgment"  → 学术论文里 A 是否给 B 系产品提供材料/IP
```

**任何一条命中 → 必须把"vector 关系"也写进档案**，不能只看 "直接合作 = 0"。

### 三种关系强度梯度（写档案时用）

| 强度 | 判定 | 写法示例 |
|---|---|---|
| **直接合作** | A、B 双方 IR 公告 / 8-K / 联合 PR | "A 跟 B 于 YYYY-MM-DD 签 LSA / 战略入股 / JV" |
| **vector 关系（强）** | A 是 B 系（被 B 收购的）公司的核心 supplier / IP holder / 论文 acknowledgment | "A 通过 X (B 系) 间接进入 B 的产品路线，X 5+ 年用 A 材料" |
| **理论 indirect tie（弱）** | A、B 共用 foundry / 共同平台 / 投资者论坛叙事 | "A 跟 B 共用 GFS 流片 = 理论 indirect，**不构成合作**" |

**v1.0 错误**：把"vector 关系（强）"误归到"理论 indirect tie（弱）"+ 用"散户 narrative"否定 → 双重错误

### 跨知识库扩展

这个反模式不止于投资知识库。任何"A 跟 B 没关系"的结论都需要 vector 路径穷尽：
- 软件依赖：「A 库不依赖 B」→ 检查 transitive deps（A → C → B）
- 学术论文：「论文 A 不引用 B 的工作」→ 检查 chained citations
- 公司治理：「A 公司高管跟 B 没关系」→ 检查共同董事 / 共同基金 / 校友
- 法律案件：「A 跟 B 没法律关系」→ 检查 subsidiary / parent / 股东链

### 沉淀的 4 句话

1. "搜不到 ≠ 不存在"，搜不到只意味着搜索路径不对
2. 推翻已有信息标准必须高于补充新信息（Case 3 Rule + 这次再次验证）
3. 在下"没有 X"结论之前，必须**穷尽 vector 路径**（A→中间方→B、A→技术→B、A→投资→B、A→学术→B、A→共同 foundry/客户→B）
4. 用户带着第三方文章/截图来时（不是简单提问） = ground truth 信号，必须先做官方源 5+ 验证再决定是否回滚

---

## Case 5：估值数据溯源反模式（NEW，2026-05-08 下午）

### 反模式描述

在投资 / 财务分析场景中：
1. **写公司档案时**，PE / PS / 市值 / 营收等估值数据**直接抄 web search 文章里的数字**
2. 文章里的数字往往是：
   - 几周 / 几个月前的（涨跌后已经偏差很大）
   - **forward / TTM 混着写**（差异 5-10×）
   - **GAAP / Non-GAAP 混着写**（差异 30-50%）
   - 某些媒体故意挑对叙事有利的口径
3. **没有标 source / timestamp** → 事后无法审计、无法判断是否过期

### 真实案例（2026-05-08 用户审计触发）

用户反馈："你这里面很多估值数据都不对，是哪里取的？"

API 实测对比知识库：
| 公司 | 知识库写的 | API 真实 (Finnhub TTM) | 偏差 |
|---|---|---|---|
| COHR | "Forward P/E ~50x" | **PE TTM 216.6** | **4× 偏差** |
| LITE | "Forward P/E ~30x" | **PE TTM 253.3** | **8× 偏差** |
| VECO | "Forward P/E ~30x" | **PE TTM 101.3** | **3× 偏差** |
| AXTI | "Forward P/E ~20x" | **N/A 亏损** + PS 67 | **完全错** |
| AAOI | "Forward P/E ~18x" | **N/A 亏损** + PS 28 | **完全错** |
| O-Net 0877.HK | "上市港股" | **2020-10 已私有化退市** | **事实错误**！ |

→ **本质：用低可信度数据（C/D 级文章）驱动高影响决策（portfolio 加权预期 +50-55%）**

### 后果

直接影响投资决策。如果 portfolio 加权预期收益是基于错误估值算的：
- 实际预期 +30% 被写成 +55% → 用户 over-allocate
- COHR/LITE 实际 PE 200+ 被写成 50/30 → 用户低估 down-side risk
- 整个知识库的"科学性"信誉破产

### 修复（5 条强制规则）

#### Rule 5.1: 估值数据必须 API 实时拉

**禁止**：用 web search 文章里的 PE / PS / 市值数字

**强制**：
- 价格 / 市值 / PE / PS / PB → 必须从 **FMP / Finnhub / Yahoo / Tencent qt** 实时拉，且标 `source: fmp@2026-05-08T13:35Z`
- 工作区有 `~/openorder/automation/fetch_valuations.py` v1.1 已经路由好（FMP 主源 美股 / Finnhub 备用台股.TWO / Yahoo 台股.TW欧日 / Tencent qt A股港股）
- 跑一次只要 150 秒，没理由不跑

**🆕 数据源升级阶梯（v2 沉淀）**：
1. **FMP 主源**（美股，需要 FMP_API_KEY）→ 拿 EV/EBITDA / FCF Yield / PEG / ROIC / Beta / Sector 等深度字段
2. **Finnhub 备用**（FMP 失败 / quota 超额时自动 fallback）→ 仍能拿 PE/PS/PB/ROE/营收增长
3. **Yahoo Finance**（台股 .TW / 欧 / 日 / 加，免费）→ 仅价格 + 部分 metric
4. **Tencent qt**（A 股 / 港股，免费 GBK 编码）→ 价格 + PE TTM / 动态 PE / PB / 市值

**FMP 限制反思（NEW v2）**:
- 免费 tier **250 calls/day**（每 ticker 5 calls = quote/profile/ratios/key-metrics/growth）
- → 实际只能跑 **~50 ticker/天**
- → **关键 ticker 优先**（NVDA / TSM / 自己 portfolio 持仓 5 个 = 用 25 calls 拿全 EV/EBITDA）
- → 其他 ticker 自动 fallback 到 Finnhub 也够用
- 如果常态化日跑 → **升级 FMP Plus $14/mo = 500 calls/day + 5 年历史数据** 性价比合理

#### Rule 5.2: 必须区分 TTM / Forward / GAAP / Non-GAAP

**禁止**：含糊地写 "Forward P/E 30x"

**强制**：
- 写 "PE TTM 253 (GAAP) / PE Forward FY27 ~75 (consensus, non-GAAP)"
- 不知道口径就标 `unknown valuation methodology - to verify`

#### Rule 5.3: 亏损公司不能用 PE 定价

**禁止**：给亏损公司编造 "Forward P/E ~18x"

**强制**：
- 亏损公司 PE 必须写 "N/A (TTM 净利亏损)"
- 用 PS / EV/Sales / Forward Revenue 定价
- 明确标记 "not yet profitable" 风险

#### Rule 5.4: 上市状态必须验证

**禁止**：直接把"上市公司"写到档案里，不验证 ticker 是否有效

**强制**：每个新公司归档前**必须**做 1 个 quick check：
```bash
# 港股
curl -s "https://qt.gtimg.cn/q=hk00877"
# 期望：v_hk00877="..." 含报价
# 警告：v_pv_none_match="1" → 该 ticker 无效（已退市 / 暂停交易）

# 美股 / 台股 .TWO
curl -s "https://finnhub.io/api/v1/quote?symbol=NVDA&token=$FINNHUB_API_KEY"
# 期望：{"c": price, ...}
# 警告：{} 或 {"error":"..."} → ticker 无效

# 欧 / 日 / 加 / 台股 .TW
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/2330.TW?interval=1d&range=1d"
```

如果返回 empty → **该公司已退市或暂停交易** → 标记为 `PRIVATE-` 前缀，移出"可投资"清单

#### Rule 5.5: 估值数字必须带 source / timestamp

模板：
```markdown
> 股价: $211.50 (5/7 收盘) `source: finnhub@2026-05-08T07:58Z`
> PE TTM: 43.2 (GAAP) | PE Forward FY27: ~25 (consensus)
```

### 自检三问（写公司档案 / 调权重前问自己）

1. 我现在写的 PE / 市值 / 营收 数字，**source 是 API 还是 web 文章？**
2. 这个数字是 **TTM 还是 Forward？GAAP 还是 Non-GAAP？什么时间口径？**
3. 这家公司**真的还在上市交易吗？**还是已经退市 / 私有化 / 被收购了？

→ 任何一题答不上来 → **不能写到档案里 / 不能驱动权重调整**

### 后续工程化（已落地）

- `automation/fetch_valuations.py` — 多源路由抓取（已写）
- `automation/tickers.tsv` — 48 个 ticker 清单（已写）
- `data/valuations-{date}.md` — 每个交易日跑一次（待加 cron）
- `raw/snapshots/{date}/{ticker}.json` — 原始 API 响应（已落，可审计）
- `data/valuations-audit-2026-05-08.md` — 审计报告（已写，记录了 3 个事实错误 + 5 个估值偏差）

---

## Case 4：投资分析中"看价格翻转 thesis"反模式（NEW，2026-05-08）

### 反模式描述

在投资 / 财务分析场景中：
1. **第一轮**：看到业绩数据好就立刻把"卡脖子梯度评分"等结构性指标 +1 ~ +3 + 立刻给"加仓"建议
2. **第二轮**：看到业绩日 ±2 天股价跌就立刻翻转 + 把同一个评分调回去 + 立刻给"减仓"建议

→ **本质：把 1 个季度业绩 + 短期价格当成结构性 thesis 信号**

### 真实案例（2026-05-08 Photonics 业绩 super-week）

| 时间 | 标的 | 操作 | 错误本质 |
|---|---|---|---|
| 5/8 11:00 | LITE | 卡脖子 21 → 24 + 权重 15% → 17% + 12 月目标 +25-40% → +50-65% | 看 1 季度业绩调结构性评分 |
| 5/8 11:00 | AAOI | 卡脖子 14 → 17 + 权重 5% → 6% + 12 月目标 +20-40% → +30-50% | 同上 |
| 5/8 11:27 | LITE | "卡脖子 24 → 21 / 12 月调回 +30-45% / 减仓" | 看 -13% 价格翻转 thesis |
| 5/8 11:27 | AAOI | "卡脖子 17 → 15 / 减仓" | 同上 |

→ 用户原话："**你这个观点变化得太快了 ... 这是很不对应的，你应该按某个逻辑去分析**"

### 「调整 thesis」之前的自检三问

1. **我的调整是基于已发生的 SEC filing / 官方公告 / 已签合同，还是基于价格/管理层 statement/我的推测？**
2. **如果我对同一个标的在 90 天内已经调过分，再调是不是过度反应？**
3. **同行业其他市场（A 股 / H 股 / 日股 / 欧股）的同期数据是不是也支持我的调整方向？还是只看美股就调？**

**任何一问不通过 → 不允许调整结构性评分 / 权重，只允许补充多空论据。**

### 三层信息分离规则（**必须严格遵守**）

| 层 | 内容 | 时间属性 | 能否驱动 thesis 变化？ |
|---|---|---|---|
| **A 基本面** | 已发生的财报数字 + 已签的合同 + 已建的产能 + 管理层判断 | 季度/年度 | ✅ **能**，但要 S/A 级证据（10-K / 10-Q / 8-K / IR / earnings call）|
| **B 长期价格 thesis** | 12-36 个月 fair value | 1-3 年 | ✅ 能，由 A 推导 |
| **C 短期价格 + 情绪** | ±30 天股价 / 板块轮动 / 头条 | 1-30 天 | ❌ **绝对不能** |

### Silo 偏见反模式（同时发生 in Case 4）

讨论一组同行业标的时**只看一个市场**（如只看美股），完全忽略 A 股 / H 股 / 日股的同行业数据。

**反例**：5/8 photonics super-week 整轮讨论都聚焦美股 LITE/COHR/AAOI/VECO/AXTI/MRVL，**完全没提 A 股 1Q26 同行业集体爆发**（中际 +262% / 源杰 +1153% / 华工 +56% / 天孚 +46% + 创业板涨 1.45% 创近 11 年新高）。

**事实**：5/7 美股 photonics -10% / A 股 photonics +6% = **完全反向**。如果同时看两个市场，会立刻意识到美股的 -10% 是资金轮动 + 估值消化（不是 thesis 问题），而不是基本面恶化。

### 跨市场交叉验证规则

每次讨论一组同行业标的时，必须问：
1. 这个行业 / 主题在 A 股有没有同行业公司？（如有 → 必须 WebSearch 同行业 1Q / 2Q / 半年报）
2. H 股 / 日股 / 欧股有没有同行业公司？
3. 多市场是同向上行、同向下行、还是反向背离？

**全球同向 = 行业 thesis 信号；多市场反向背离 = 单一市场资金面/情绪面问题，不动 thesis**

### 落档要求

每次"调整 thesis"必须：
1. 在公司档案 Changelog 里写明：这次调整基于什么 S/A 级证据
2. 在 portfolio Changelog 里写明：这次调整 vs 上次的对比
3. 如果是撤回上一次调整 → 必须明确写"v1.x 已撤回"+ 解释方法论错误
4. 不允许在 Changelog 里只写"升级 X → Y"而不解释证据来源

## 完整工具阶梯

### 抓网页内容

```
Step 1  WebFetch                       便宜，纯 HTTP，无 JS 渲染
  失败信号：403 / 451 / SPA 空 body / chat.* / x.com / linkedin
  → 直接跳 Step 2，不重试
Step 2  cursor-ide-browser MCP         真实 Chromium，能过 SPA / 反爬
  组合：browser_navigate → browser_wait_for → browser_snapshot
  失败信号：登录墙 / 需要 OAuth → Step 3
Step 3  让用户操作真实浏览器导出文本    最后手段
```

### 抓 GitHub 仓库

```
Step 0  gh auth status                 环境探针，0 成本
Step 1a 已登录 → gh repo clone / gh api
Step 1b SSH 报错 → 立刻 HTTPS over token：
        git clone "https://oauth2:$(gh auth token)@github.com/o/r.git"
        clone 后 git remote set-url 抹 token
Step 2  未登录 → WebFetch 仅适用于公开仓库
Step 3  404 不要立即下结论：
        gh search repos --owner OWNER KEYWORD
        gh repo list OWNER --limit 200
```

### 任意外部 API 失败

```
Step 0  环境探针：哪些凭据已配置？
        gh auth status / doctl auth list / aws sts get-caller-identity
        env | grep -i KEY_NAME
        ls ~/.config/<service>/
Step 1  若已配置 → 用对应 CLI 重试一次
Step 2  401/403 → 检查 token scope / 过期，不当结论
Step 3  仍失败 → 列出还没试的工具，再 AskQuestion
```

## 历史失败案例（供模式识别）

### Case 1：DeepSeek 分享页 403
- 现象：`WebFetch(chat.deepseek.com/share/*)` → CloudFront 403
- 错误处理：直接 AskQuestion 问用户怎么办
- 正确处理：CloudFront 403 = 反爬 → 立即换 `cursor-ide-browser`
- 教训：`chat.*/share/*` 几乎都是 SPA + 反爬，**应直接跳过 WebFetch**

### Case 2：GitHub 私有仓库 404
- 现象：`WebFetch(github.com/owner/private-repo)` → 404；`WebFetch(api.github.com/...)` → 404
- 错误处理：把 404 当作"仓库不存在"的硬证据，AskQuestion 问用户
- 正确处理：GitHub 对私有 + 未授权返回 404（不是 401）。1 条 `gh auth status` 即可澄清。
- 教训：**404 在 GitHub 上歧义**，必须先跑环境探针。

### Case 3：内省式纠偏 — 错误推翻已有正确信息（投资知识库 NVDA $6B → $4B）

> **2026-05-07/08 投资知识库 photonics P0/P1 建档过程中真实发生**

- **现象**：知识库 v1 写入"NVDA 2026/3 投资 COHR/LITE/Marvell 各 $2B = $6B 三路线全押"。Agent 在后续建档过程中"凭印象"认为 Marvell 没被 NVDA 直接投资，**没有去查官方源**就把"$6B → $4B"作为"重要修正"写进 4 个文件（NVDA.md / Marvell.md / INDEX.md / Celestial-AI.md），并在每个文件加粗强调"**实际 $4B 不是 $6B / Marvell 没有 NVDA 直接入股 / MRVL 比 COHR/LITE 更独立**"。
- **错误传播**：错误结论生成 5+ 个衍生论断（"MRVL 不依赖 NVDA 资金背书"、"NVDA = 路线 A+B 双押 + 自做路线 C"、"MRVL 是独立 alpha"等），污染 Marvell 配置建议、Celestial AI 收购的 implication、NVDA Bull case 论据。
- **用户介入**：用户提供 [NVIDIA Newsroom 官方公告](https://nvidianews.nvidia.com/news/nvidia-ai-ecosystem-expands-as-marvell-joins-forces-through-nvlink-fusion)（2026/3/31）+ Marvell 投资者关系页 + Marvell 8-K 文件三个官方源，原文 "*In addition, NVIDIA has invested $2 billion in Marvell.*" —— **agent 之前的修正完全错误**。
- **正确处理**：在做"修正"之前**必须先 WebFetch 官方源** —— 这种已经写入知识库的"已知事实"具有强先验，推翻它的证据门槛应该比"补充新信息"高一个数量级。
- **教训（核心）**：

  1. **「推翻已有信息」标准必须高于「补充新信息」** —— 已有信息已经过历史 review 形成知识库基线，否定它需要 ground truth 级别证据（官方公告 / 法律文件 / 第一手数据），不是"我以为"。
  2. **「内省式纠偏」是反模式** —— Agent 不允许仅凭"逻辑推断"或"印象"就推翻 v1 写入的事实。任何"修正"必须前置 1 步：**WebFetch 官方源 / 一手数据 / 用户原话**。
  3. **错误的"修正"比缺失的信息危害更大** —— 缺失信息会触发用户提问；错误的"修正"会沉淀进知识库 + 衍生 5+ 论断 + 多文件级联污染。
  4. **用户提供官方链接 = ground truth** —— 必须立即接受、全面回滚、公开承认错误。不允许"找补"、"部分接受"、"重新解读"。
  5. **Changelog 必须保留错误版本的痕迹** —— 不要直接覆盖错误，要在 Changelog 里明确标注"【⚠️ 错误版本】" + 回滚日期 + 触发回滚的官方源链接。这样未来再做类似纠偏时有 reference。

- **延伸场景**：这个反模式不只发生在投资知识库。任何 agent 在长 session（多轮 / 多任务）中"自我感觉发现错误"并主动"修正"已有信息时，都必须先做官方源验证。**如果你没有 WebFetch 一个权威源就要"修正"，停下来。**

## HTTP 错误码读法（提醒）

| 错误 | 在不同上下文 | 真实含义 |
| --- | --- | --- |
| 403 | + CF/Cloudflare 头 | 反爬，**不是**真的禁止访问 |
| 403 | + 已携带 token | scope 不够 / 资源真的拒绝 |
| 404 | github.com 私有仓库 | 多半是没授权 |
| 404 | 一般站点 | 真不存在的概率较高 |
| 451 | 任何 | 地理封锁 |

## 同一工具的「沉默期」

同一工具对同一目标连续失败 1 次 → **禁止用同样方式重试**。换工具或换参数。

反例：
```
WebFetch(github.com/x/y)            → 404
WebFetch(api.github.com/repos/x/y)  → 404   ← 仍是 WebFetch，等价重复
WebFetch(raw.githubusercontent.com) → 404   ← 还是 WebFetch
```

正例：
```
WebFetch(github.com/x/y)  → 404
gh auth status            → 已登录有 repo scope
gh repo clone x/y         → 成功
```

## skill ≠ 硬约束

实践经验：prompt 里写「每次回顾 error-patterns」，模型不一定每次都听。这条 skill 是「按需展开的教材」——**真要硬保障，还是要把上面的自检三问沉淀成 agent 的 always-apply 规则**（各家 agent 的规则机制见 `../openorder/docs/compatibility.md`）。
