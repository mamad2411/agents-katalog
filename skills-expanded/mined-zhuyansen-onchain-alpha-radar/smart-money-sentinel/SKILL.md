---
name: smart-money-sentinel
description: |
  Smart money signal tracking + sentiment alert pipeline. Starts from Binance smart money signals,
  then cross-validates with crypto news, KOL discussions, and wallet position changes to determine
  optimal entry timing.

  Chains together: Binance Skills (trading-signal, query-token-info, query-address-info),
  opennews-mcp (crypto news), opentwitter-mcp (KOL tracking), base-mcp (Base chain wallet),
  and excalidraw-diagram (visual diagrams).

  Use when the user wants to: track smart money movements, check entry timing, monitor whale alerts,
  cross-validate trading signals with news and social sentiment, or get a comprehensive signal report.

  Trigger keywords: "聪明钱", "smart money signal", "异动", "舆情预警", "信号追踪", "entry timing",
  "钱包追踪", "whale alert", "信号验证", "入场时机", "聪明钱哨兵", "sentinel", "trading signal",
  "smart money tracking", "KOL舆情", "新闻验证"
---

# Smart Money Sentinel — 聪明钱哨兵

> 信号发现 → 新闻验证 → KOL 舆情 → 钱包确认 → 综合研判 → 可视化图表

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Smart Money Sentinel                         │
│                                                                 │
│  Phase 1          Phase 2         Phase 3        Phase 4        │
│  ┌──────────┐    ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │ Binance  │───▶│ OpenNews │──▶│ Twitter  │──▶│ Wallet   │   │
│  │ Trading  │    │ 新闻验证  │   │ KOL 舆情  │   │ 持仓验证  │   │
│  │ Signal   │    │          │   │          │   │          │   │
│  └──────────┘    └──────────┘   └──────────┘   └──────────┘   │
│       │                                              │         │
│       └──────────────── Phase 5 ─────────────────────┘         │
│                      综合研判 + 行动建议                         │
│                             │                                   │
│                      ┌──────────┐                               │
│                      │ Phase 6  │                               │
│                      │Excalidraw│                               │
│                      │ 可视化图表 │                               │
│                      └──────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

## Tool Dependencies

| Tool | Type | Purpose | Required |
|------|------|---------|----------|
| **trading-signal** | Binance Skill (curl) | 聪明钱信号发现 | ✅ Yes |
| **query-token-info** | Binance Skill (curl) | Token 搜索 + 动态数据 + K线 | ✅ Yes |
| **query-address-info** | Binance Skill (curl) | 钱包持仓查询 | ✅ Yes |
| **opennews-mcp** | MCP Server | 新闻利好/利空验证 | ✅ Yes |
| **opentwitter-mcp** | MCP Server | KOL 讨论追踪 | ⚠️ Optional |
| **base-mcp** | MCP Server | Base 链钱包分析 | ⚠️ Optional |
| **excalidraw-diagram** | Skill | 可视化信号矩阵图表 | ⚠️ Optional |

## Supported Chains

| Chain | Binance chainId | Platform (K-Line) |
|-------|-----------------|-------------------|
| BSC | 56 | bsc |
| Solana | CT_501 | solana |
| Base | 8453 | base |

---

## Phase 1: 信号发现（Signal Discovery）

**Goal**: 从币安聪明钱信号中发现异动 Token

### Step 1.1: 拉取聪明钱信号

用 curl 调用 Binance Trading Signal API：

```bash
curl --location 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money' \
  --header 'Content-Type: application/json' \
  --header 'Accept-Encoding: identity' \
  --header 'User-Agent: binance-web3/1.0 (Skill)' \
  --data '{"smartSignalType":"","page":1,"pageSize":50,"chainId":"{{CHAIN_ID}}"}'
```

- 默认链：用户未指定时扫描 Solana (`CT_501`)，可切换 BSC (`56`)
- 如果用户想看多链，依次请求 `CT_501` 和 `56`

### Step 1.2: 筛选 Top 信号

从返回数据中筛选，优先级：
1. **status = "active"** 优先（仍在有效期）
2. **direction = "buy"** 的买入信号优先（除非用户要看卖出）
3. 按 `smartMoneyCount` 降序（聪明钱钱包数越多越可靠）
4. 过滤 `exitRate > 80%` 的信号（聪明钱已大量退出）

### Step 1.3: 信号强度评分

对每个信号计算初步评分（满分 25）：

| Factor | Weight | Scoring |
|--------|--------|---------|
| smartMoneyCount | 10 | ≥10: 10, ≥5: 7, ≥3: 5, <3: 3 |
| maxGain | 8 | ≥20%: 8, ≥10%: 6, ≥5%: 4, <5%: 2 |
| exitRate (反向) | 4 | <20%: 4, <50%: 3, <70%: 2, ≥70%: 1 |
| status | 3 | active: 3, timeout: 1, completed: 2 |

### Step 1.4: 输出

选出 Top 3-5 个信号，输出表格：

```
| # | Token | Chain | Direction | SM Count | Max Gain | Exit Rate | Status | Score/25 |
```

**用户交互**：展示信号列表，让用户选择要深入分析的 Token（或默认取 Top 1）

---

## Phase 2: 新闻验证（News Validation）

**Goal**: 检查目标 Token 是否有利好/利空新闻事件

### Step 2.1: 按币种搜索新闻

使用 opennews-mcp 的 `search_news_by_coin` 工具：

```
search_news_by_coin(coin="TOKEN_SYMBOL", limit=20)
```

### Step 2.2: 检查交易信号新闻

使用 `get_news_by_signal` 分别查看看多和看空新闻：

```
get_news_by_signal(signal="long", limit=10)   // 利好
get_news_by_signal(signal="short", limit=10)  // 利空
```

从结果中筛选与目标 Token 相关的条目。

### Step 2.3: 获取高置信度事件

```
get_high_score_news(min_score=70, limit=10)
```

检查是否有与目标 Token 相关的高分新闻。

### Step 2.4: 新闻情绪评分（满分 20）

| Factor | Weight | Scoring |
|--------|--------|---------|
| 利好新闻数量 | 8 | ≥3条: 8, 2条: 6, 1条: 4, 0条: 0 |
| 利空新闻数量（反向） | 6 | 0条: 6, 1条: 4, 2条: 2, ≥3条: 0 |
| 高分新闻命中 | 4 | 有高分利好: 4, 有高分中性: 2, 无: 0 |
| 新闻时效性 | 2 | 24h内: 2, 48h内: 1, 更早: 0 |

### Step 2.5: 输出

```
新闻验证结果：
- 利好事件: [列表]
- 利空事件: [列表]
- 高分事件: [列表]
- 新闻情绪: BULLISH / NEUTRAL / BEARISH
- 新闻评分: XX/20
```

---

## Phase 3: KOL 舆情（Social Sentiment）

**Goal**: 追踪 Twitter KOL 对目标 Token 的讨论

> ⚠️ 如果 opentwitter-mcp 不可用，跳过此阶段，KOL 评分记为 10/20（中性）

### Step 3.1: 搜索 Token 相关讨论

```
search_twitter(keywords="$TOKEN_SYMBOL", limit=20)
```

或使用高级搜索：

```
search_twitter_advanced(keywords="TOKEN_SYMBOL", min_likes=10, limit=20)
```

### Step 3.2: 分析 KOL 参与度

从搜索结果中识别 KOL（粉丝 > 10K 的账号），如需要可进一步查询：

```
get_twitter_kol_followers(username="KOL_USERNAME", limit=10)
```

### Step 3.3: 查看官方账号

如果 Token 有官方 Twitter，获取其最新推文：

```
get_twitter_user_tweets(username="OFFICIAL_ACCOUNT", limit=10)
```

### Step 3.4: KOL 舆情评分（满分 20）

| Factor | Weight | Scoring |
|--------|--------|---------|
| 讨论数量 | 6 | ≥10条: 6, ≥5条: 4, ≥2条: 2, <2条: 0 |
| KOL 参与 | 6 | ≥3 KOL: 6, 2 KOL: 4, 1 KOL: 2, 0: 0 |
| 情绪倾向 | 5 | 多数看多: 5, 中性: 3, 多数看空: 1 |
| 官方活跃度 | 3 | 24h内发推: 3, 7d内: 2, 不活跃: 0 |

---

## Phase 4: 钱包验证（Wallet Validation）

**Goal**: 通过链上数据确认持仓变化和 Token 基本面

### Step 4.1: 获取 Token 动态数据

用 curl 调用 Binance Token Dynamic Data API：

```bash
curl --location 'https://web3.binance.com/bapi/defi/v4/public/wallet-direct/buw/wallet/market/token/dynamic/info?chainId={{CHAIN_ID}}&contractAddress={{CONTRACT_ADDRESS}}' \
  --header 'Accept-Encoding: identity' \
  --header 'User-Agent: binance-web3/1.0 (Skill)'
```

关注字段：
- `price`, `percentChange24h`, `percentChange4h`
- `volume24h`, `volume24hBuy`, `volume24hSell` → 买卖比
- `holders`, `kolHolders`, `smartMoneyHolders`
- `top10HoldersPercentage` → 集中度
- `liquidity`, `marketCap`

### Step 4.2: 获取 Token 元数据

```bash
curl --location 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/dex/market/token/meta/info?chainId={{CHAIN_ID}}&contractAddress={{CONTRACT_ADDRESS}}' \
  --header 'Accept-Encoding: identity' \
  --header 'User-Agent: binance-web3/1.0 (Skill)'
```

关注：`links`（社交链接）, `creatorAddress`, `auditInfo`, `description`

### Step 4.3: 查询聪明钱钱包持仓（如有地址）

如果信号中包含具体钱包地址，查询其当前持仓：

```bash
curl --location 'https://web3.binance.com/bapi/defi/v3/public/wallet-direct/buw/wallet/address/pnl/active-position-list?address={{WALLET_ADDRESS}}&chainId={{CHAIN_ID}}&offset=0' \
  --header 'clienttype: web' \
  --header 'clientversion: 1.2.0' \
  --header 'Accept-Encoding: identity' \
  --header 'User-Agent: binance-web3/1.0 (Skill)'
```

### Step 4.4: Base 链补充分析

> ⚠️ 仅在 Chain = Base 时使用 base-mcp，其他链跳过

如果目标 Token 在 Base 链上：
- `list-balances` → 查看钱包余额
- `check-address-reputation` → 地址信誉评估

### Step 4.5: 持仓验证评分（满分 20）

| Factor | Weight | Scoring |
|--------|--------|---------|
| 买卖比 (Buy/Sell) | 6 | Buy>Sell*1.5: 6, Buy>Sell: 4, 均衡: 2, Sell>Buy: 0 |
| SM/KOL 持仓人数 | 5 | SM≥5+KOL≥3: 5, SM≥3: 3, SM≥1: 2, 0: 0 |
| 持仓集中度(反向) | 5 | Top10<30%: 5, <50%: 3, <70%: 2, ≥70%: 1 |
| 流动性健康度 | 4 | Liq/MCap>20%: 4, >10%: 3, >5%: 2, ≤5%: 1 |

### Step 4.6: 基本面评分（满分 15）

| Factor | Weight | Scoring |
|--------|--------|---------|
| 市值规模 | 4 | $1M-$50M: 4, $50M-$200M: 3, <$1M: 2, >$200M: 2 |
| 24h 交易量 | 4 | Vol/MCap>50%: 4, >20%: 3, >10%: 2, <10%: 1 |
| 持有人数 | 4 | ≥10K: 4, ≥5K: 3, ≥1K: 2, <1K: 1 |
| 社交链接完整性 | 3 | 有website+X+TG: 3, 有2项: 2, 有1项: 1, 无: 0 |

---

## Phase 5: 综合研判（Verdict）

**Goal**: 汇总所有数据，给出行动建议

### Step 5.1: 汇总评分

| Dimension | Max Score | Source |
|-----------|-----------|--------|
| 信号强度 | 25 | Phase 1 |
| 新闻情绪 | 20 | Phase 2 |
| KOL 舆情 | 20 | Phase 3 |
| 持仓验证 | 20 | Phase 4 |
| 基本面 | 15 | Phase 4 |
| **Total** | **100** | |

### Step 5.2: 行动建议

| Score Range | Action | Description |
|-------------|--------|-------------|
| 80-100 | 🟢 **立即关注** | 多维共振，信号强+新闻利好+KOL看多+持仓健康 |
| 60-79 | 🟡 **等待确认** | 部分维度正面，需等更多信号确认 |
| 40-59 | 🟠 **谨慎观望** | 信号混合，存在矛盾信息 |
| 0-39 | 🔴 **回避** | 多维度负面，风险过高 |

### Step 5.3: 生成预警研报

使用 `templates/alert-report.md` 模板生成研报，保存到 `reports/` 目录。

文件命名：`{token_symbol}-sentinel-{date}.md`

---

## Phase 6: 可视化图表（Excalidraw Visualization）

**Goal**: 生成 Excalidraw 可视化图表，直观展示信号验证结果

> ⚠️ 如果 excalidraw-diagram skill 不可用，跳过此阶段

### Step 6.1: 信号矩阵图

生成一个 Sentinel Signal Matrix 图表，包含：

1. **标题区**: "Smart Money Sentinel — {TOKEN_SYMBOL}" + 日期 + 链名
2. **信号概览行**: Token 名称、方向、SM 数量、MaxGain、ExitRate、状态、得分（高亮第 1 名）
3. **五维评分面板**: 5 个色块分别展示各维度得分
   - 信号强度 → 蓝色块
   - 新闻情绪 → 绿色/红色块（根据利好利空）
   - KOL 舆情 → 紫色块
   - 持仓验证 → 青色块
   - 基本面 → 橙色块
4. **箭头汇聚**: 5 个色块箭头指向底部
5. **Verdict 面板**: 深色底 + 总分 + 行动建议 + 关键风险

### Step 6.2: 信号对比图（批量扫描模式）

在批量扫描模式下，生成所有信号的横向对比图：

1. 每个信号一行，包含 Token 名、SM 数量、MaxGain、状态
2. 按得分降序排列
3. 用颜色区分：绿色(高分) → 黄色(中等) → 灰色(低分)

### Step 6.3: 输出

- 保存为 `reports/{token_symbol}-sentinel-matrix.excalidraw`
- 如果 render_excalidraw.py 可用，渲染为 PNG：`reports/{token_symbol}-sentinel-matrix.png`

---

## Execution Modes

### Mode 1: 全量扫描（默认）

触发词：「扫描聪明钱信号」「查看最新异动」「smart money scan」

执行 Phase 1 → 展示 Top 5 信号 → 用户选择 → Phase 2-5 深入分析

### Mode 2: 单币验证

触发词：「验证 $TOKEN 信号」「$TOKEN 能不能买」「check $TOKEN」

跳过 Phase 1，直接用 query-token-info 搜索 Token → Phase 2-5 验证

### Mode 3: 批量快扫

触发词：「批量扫描」「batch scan」「快速过一遍信号」

执行 Phase 1 → 对 Top 10 信号每个只做 Phase 2（新闻） → 输出批量概览表

使用 `templates/batch-scan.md` 模板

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Binance API 返回空数据 | 提示用户「当前无活跃聪明钱信号」，建议稍后重试 |
| Binance API 网络错误 | 检查代理设置（中国需 `all_proxy`），提示用户 |
| opennews-mcp 不可用 | 跳过 Phase 2，新闻评分记为 10/20（中性），提示用户 |
| opentwitter-mcp 不可用 | 跳过 Phase 3，KOL 评分记为 10/20（中性），提示用户 |
| base-mcp 不可用 | 跳过 Base 链补充分析，不影响其他链 |
| Token 在 Binance 无数据 | 用 query-token-info 搜索确认，若无则提示 Token 可能过小 |
| 代理问题 | web3.binance.com 在中国需代理，用 `export all_proxy=http://127.0.0.1:7890` |

---

## Notes

- Binance Trading Signal API 无需认证，但需要 `User-Agent: binance-web3/1.0 (Skill)` header
- opennews-mcp 需要 OPENNEWS_TOKEN（从 https://6551.io/mcp 获取）
- opentwitter-mcp 需要 TWITTER_TOKEN（同样从 https://6551.io/mcp 获取）
- 中国用户访问 web3.binance.com 需要代理
- 6551.io API 无需代理可直接访问
- 所有价格数据为 USD，时间戳为毫秒级
