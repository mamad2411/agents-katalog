---
name: analyze-crypto
description: 一键综合分析加密货币。通过并行子代理采集价格、新闻情绪、赛道对比、市场环境、项目基本面五个维度，交叉分析后输出 HTML 报告（含24小时行情和7日趋势）。触发词：分析BTC、analyze ETH、比特币怎么样、SOL值得买吗。
allowed-tools: Agent, WebSearch, WebFetch, Write, Bash
disable-model-invocation: true
context: fork
---

# Analyze Crypto — 一键加密货币综合分析

输入代币名称或符号，自动并行采集五个维度的数据，综合分析后输出标准报告。

## When to Use

当用户请求以下操作时触发：
- "分析BTC" / "分析以太坊" / "分析SOL"
- "analyze BTC" / "analyze Ethereum"
- "比特币怎么样" / "ETH最近为什么涨/跌"
- "帮我看看SOL" / "DOGE值得买吗"

## Phase 0: 解析输入

根据用户输入，识别以下信息：

1. **代币名称映射**（常用代币中英文对照）
   - 比特币/Bitcoin → BTC
   - 以太坊/Ethereum → ETH
   - 索拉纳/Solana → SOL
   - 瑞波/Ripple → XRP
   - 币安币/BNB Chain → BNB
   - 艾达/Cardano → ADA
   - 狗狗币/Dogecoin → DOGE
   - 波卡/Polkadot → DOT
   - 雪崩/Avalanche → AVAX
   - 马蹄/Polygon → POL
   - 链接/Chainlink → LINK
   - 莱特币/Litecoin → LTC
   - Uniswap → UNI
   - Aave → AAVE
   - Toncoin → TON
   - 柴犬币/Shiba Inu → SHIB
   - Sui → SUI
   - Aptos → APT
   - Arbitrum → ARB
   - Optimism → OP
   - Jupiter → JUP
   - Celestia → TIA
   - 如果不在列表中，使用 WebSearch 搜索确认代币符号

2. **识别赛道类别**
   - L1 公链: BTC, ETH, SOL, ADA, AVAX, TON, SUI, APT
   - L2 扩展: ARB, OP, POL
   - DeFi: UNI, AAVE, LINK, JUP
   - Meme: DOGE, SHIB
   - 支付: XRP, LTC
   - 跨链/互操作: DOT
   - 模块化: TIA
   - 其他: 通过 WebSearch 确认

3. **确定关键变量** (后续所有 Agent 都需要用到)
   - `{token}`: 代币符号 (如 BTC, ETH)
   - `{token_name}`: 代币全称 (如 Bitcoin, Ethereum)
   - `{category}`: 赛道类别 (如 L1, DeFi, Meme)
   - `{project_website}`: 项目官网 URL
   - `{competitors}`: 同赛道 2-3 个主要竞品

如果无法确定项目官网或赛道，先用一次 WebSearch 快速查询，**不要跳过这一步**。

---

## Phase 1: 并行数据采集 (5 个 Subagent)

**关键要求**: 以下 5 个 Task 必须放在**同一条消息**中发出，确保并行执行。

每个 Agent 使用 `subagent_type: "general-purpose"`。

---

### Agent 1: 价格与技术指标

**description**: "采集{token}价格数据"

**prompt 模板**:

```
你是加密货币价格分析师。请获取 {token_name}({token}) 近7天的价格数据，并**重点突出最近24小时的变化**。

任务:
1. 使用 WebSearch 搜索 "{token} price last 7 days" 获取最近行情
2. 使用 WebSearch 搜索 "{token} price today 24h" 获取最新24小时详细数据
3. 使用 WebSearch 搜索 "{token} funding rate perpetual" 获取永续合约资金费率
4. 整理以下信息:

   **最近24小时行情:**
   - 当前价格、24h最高、24h最低
   - 24h涨跌幅与涨跌金额
   - 24h成交量与成交额，较前日放量/缩量比例
   - 永续合约资金费率（正=多头支付，负=空头支付）
   - 与BTC同期涨跌幅对比（BTC相关性）
   - 24h内是否有影响价格的即时事件

   **近7天汇总:**
   - 每日收盘价和涨跌幅
   - 7天累计涨跌幅
   - 成交量变化趋势 (放量/缩量)
   - 关键技术信号 (如有: 均线多空排列、RSI超买超卖、明显支撑位/阻力位)
   - 与BTC同期涨跌幅对比

输出要求:
- 以结构化格式返回，**24h行情单独列出**
- 重点突出: 24h涨跌幅、7天涨跌幅、量价配合、资金费率方向、BTC相关性
- 控制在 600 字以内
- 不要给出投资建议
- **标注数据来源**: 关键数据注明来源网站名称（如 CoinGecko、CoinMarketCap、TradingView 等）及原始链接
```

---

### Agent 2: 新闻与社区情绪

**description**: "搜索{token_name}近期新闻"

**prompt 模板**:

```
你是加密货币新闻与情绪分析师。请搜索 {token_name}({token}) 最近7天的重要新闻和社区情绪。

任务:
1. 使用 WebSearch 搜索以下关键词 (至少搜3次不同关键词):
   - "{token_name} news this week" 或 "{token_name} 最新新闻"
   - "{token} crypto twitter" 或 "{token} community sentiment"
   - "crypto fear greed index today"
2. 从搜索结果中挑选 3-5 条最重要的新闻
3. 使用 WebFetch 访问其中至少 2 条新闻的原文，验证内容真实性
4. 获取当前 Crypto Fear & Greed Index 数值
5. 分析社区情绪倾向

输出要求:
- 列出 3-5 条关键新闻，每条包含: 日期、标题、来源名称、**原文URL**、简要内容(1-2句)
- Crypto Fear & Greed Index: 当前数值及级别 (Extreme Fear / Fear / Neutral / Greed / Extreme Greed)
- 社区情绪判断: 正面 / 负面 / 中性，并说明理由
- 识别是否有重大事件 (协议升级、安全事件、监管动态、合作公告、交易所上下架等)
- 控制在 600 字以内
```

---

### Agent 3: 赛道对比分析

**description**: "分析{category}赛道情况"

**prompt 模板**:

```
你是加密货币赛道分析师。请分析 {token_name}({token}) 所在的 {category} 赛道近期情况。

任务:
1. 使用 WebSearch 搜索:
   - "{category} crypto sector performance this week" 或 "{category} 赛道 近期表现"
   - "{token_name} vs {competitors} comparison"
2. 整理以下信息:
   - {category} 赛道近期整体趋势 (上升/下行/平稳)
   - 影响赛道的关键因素 (技术升级、TVL变化、用户增长、政策等)
   - 2-3 个主要竞品的近期价格表现和关键动态
   - {token_name} 在赛道中的市值排名和相对地位

输出要求:
- 赛道趋势概述 (2-3句)
- 竞争格局简表: 代币名、近7天涨跌、市值、关键动态
- 该代币的相对优劣势 (1-2条)
- 控制在 500 字以内
- **标注数据来源**: 竞品价格及市值数据注明来源（如 CoinMarketCap、CoinGecko 等）及链接
```

---

### Agent 4: 加密市场环境

**description**: "分析加密市场环境"

**prompt 模板**:

```
你是加密货币宏观市场分析师。请分析当前加密货币市场整体环境，重点关注与 {token_name}({token}) 相关的市场因素。

任务:
1. 使用 WebSearch 搜索最新市场数据:
   - "bitcoin dominance total crypto market cap today"
   - "crypto market overview this week"
   - "DXY dollar index today"
   - "bitcoin ETF fund flow this week"
2. 评估:
   - BTC 主导率 (Bitcoin Dominance) 及趋势
   - 加密货币总市值及7日变化
   - 美元指数 (DXY) 水平及走势
   - BTC 现货 ETF 资金流向 (净流入/流出)
   - 美联储利率政策最新动态
   - 是否有重大监管事件

输出要求:
- 加密市场环境一句话总结
- BTC主导率及含义 (资金在BTC vs 山寨币的分配)
- 总市值水平和趋势
- ETF资金流和机构情绪
- DXY与利率环境对加密市场的影响
- 控制在 400 字以内
- **标注数据来源**: 各市场指标注明来源（如 Alternative.me、Farside Investors、Trading Economics 等）及链接
```

---

### Agent 5: 项目基本面

**description**: "调研{token_name}项目基本面"

**prompt 模板**:

```
你是加密货币项目研究员。请调研 {token_name}({token}) 的项目基本面和链上数据。

任务:
1. 使用 WebFetch 访问项目官网: {project_website}
   - 查看最新公告、路线图更新
2. 使用 WebSearch 搜索:
   - "{token_name} tokenomics supply schedule"
   - "{token_name} on-chain metrics active addresses TVL"
   - "{token_name} github development activity"
3. 整理以下信息:

   **代币经济学:**
   - 总供应量 / 流通供应量 / 流通率
   - 近期是否有大额解锁事件
   - 通胀/通缩机制 (如有)

   **链上指标:**
   - 活跃地址数趋势 (如有)
   - TVL (DeFi/L1适用)
   - 哈希率 (PoW适用) 或质押率 (PoS适用)

   **开发活跃度:**
   - GitHub 近期提交频率或重大更新 (如有)
   - 近期协议升级计划

输出要求:
- 项目最新官方动态
- 代币经济学关键数据
- 链上指标概要
- 控制在 400 字以内
- 如果官网无法访问，说明情况并依赖搜索结果
- **标注数据来源**: 链上数据注明来源（如 Glassnode、DeFiLlama、官网等）及访问URL
```

---

## Phase 2: 综合分析 (主线程)

等待 5 个 Agent 全部返回后，在主线程中完成以下分析。

### Step 1: 信息汇总

将 5 个 Agent 的结果整合，识别：
- 各维度之间的 **一致性信号** (如: 价格涨 + 社区看多 + 赛道向上 = 强看多)
- 各维度之间的 **矛盾信号** (如: 价格涨但资金费率极高 = 可能存在过热)
- 同时整理各 Agent 返回的所有**来源 URL**，汇总到来源列表，用于报告末尾「参考来源」区块

### Step 2: 因果归因

分析价格变动的原因，按影响力排序：
1. **项目层面因素**: 协议升级、安全事件、合作公告、代币解锁
2. **赛道传导因素**: 赛道轮动、竞品事件、技术叙事变化
3. **市场环境因素**: BTC走势带动、ETF资金流、宏观政策、监管事件

**特别关注最近24小时变动**: 加密市场24/7运行，对最近24小时的涨跌单独归因分析，区分短期催化因素与中期趋势因素。

### Step 3: 趋势预测

基于以上分析，给出：
- **短期展望** (1-2周): 考虑技术面信号 + 资金费率 + 即将到来的事件
- **中期展望** (1-3月): 考虑项目基本面 + 赛道趋势 + 市场周期
- **主要风险点**: 可能导致走势反转的因素

---

## Phase 3: 输出报告

按以下 HTML 格式输出最终报告。使用内联 CSS 确保在浏览器和飞书中均可良好显示：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{token_name} ({token}) 综合分析报告</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; color: #1a1a1a; background: #f8f9fa; }
  .report { background: #fff; border-radius: 12px; padding: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
  h1 { font-size: 24px; border-bottom: 3px solid #1a73e8; padding-bottom: 12px; }
  h2 { font-size: 18px; color: #1a73e8; margin-top: 28px; border-left: 4px solid #1a73e8; padding-left: 10px; }
  h3 { font-size: 15px; color: #333; margin-top: 16px; }
  .meta { color: #666; font-size: 13px; margin-bottom: 16px; }
  .summary { background: #e8f0fe; border-radius: 8px; padding: 16px; font-size: 16px; font-weight: 500; margin: 16px 0; }
  .daily-highlight { background: #fff8e1; border: 1px solid #ffcc02; border-radius: 8px; padding: 16px; margin: 16px 0; }
  .daily-highlight h2 { color: #f57f17; border-left-color: #f57f17; }
  table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 14px; }
  th { background: #f1f3f4; text-align: left; padding: 10px 12px; font-weight: 600; border-bottom: 2px solid #ddd; }
  td { padding: 8px 12px; border-bottom: 1px solid #eee; }
  tr:hover td { background: #f8f9fa; }
  .up { color: #2e7d32; font-weight: 600; }
  .down { color: #d32f2f; font-weight: 600; }
  .tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; }
  .tag-positive { background: #e8f5e9; color: #2e7d32; }
  .tag-negative { background: #ffebee; color: #c62828; }
  .tag-neutral { background: #f5f5f5; color: #616161; }
  .risk { background: #fff3e0; border-radius: 8px; padding: 12px 16px; margin: 8px 0; }
  .onchain { background: #f3e5f5; border-radius: 8px; padding: 16px; margin: 16px 0; }
  .onchain h2 { color: #7b1fa2; border-left-color: #7b1fa2; }
  .disclaimer { margin-top: 24px; padding-top: 16px; border-top: 1px solid #eee; color: #999; font-size: 12px; }
  .references { margin-top: 16px; padding: 16px 20px; background: #f8f9fa; border-radius: 8px; border-top: 1px solid #eee; }
  .references h3 { font-size: 13px; color: #888; font-weight: 600; margin: 0 0 8px 0; }
  .references ol { margin: 0; padding-left: 18px; }
  .references li { font-size: 12px; color: #999; margin: 3px 0; line-height: 1.5; }
  a.src { color: #1a73e8; text-decoration: none; font-size: 12px; }
  a.src:hover { text-decoration: underline; }
  ul, ol { padding-left: 20px; }
  li { margin: 6px 0; line-height: 1.6; }
</style>
</head>
<body>
<div class="report">

<h1>{token_name} ({token}) 综合分析报告</h1>
<div class="meta">分析日期: {date} | 分析周期: 近7天 | 赛道: {category}</div>

<div class="summary">{一句话总结}</div>

<!-- 最近24小时行情 — 黄色高亮区块，放在最前面 -->
<div class="daily-highlight">
<h2>最近24小时行情</h2>
<table>
  <tr><th>指标</th><th>数值</th></tr>
  <tr><td>当前价格</td><td>$...</td></tr>
  <tr><td>24h最高 / 最低</td><td>$... / $...</td></tr>
  <tr><td>24h涨跌</td><td><span class="up/down">+/-X.XX%</span> (±$金额)</td></tr>
  <tr><td>24h成交量</td><td>$XXX亿 (较前日 +/-XX%)</td></tr>
  <tr><td>资金费率</td><td>+/-X.XX% (多头/空头支付)</td></tr>
  <tr><td>BTC同期表现</td><td>+/-X.XX% (相关性: 强/中/弱)</td></tr>
</table>
<p><strong>24h变动归因:</strong> 简要说明最近24小时涨跌的直接原因</p>
</div>

<h2>一、7日价格概览</h2>
<table>
  <tr><th>指标</th><th>数值</th></tr>
  <tr><td>当前价格</td><td>$XXX</td></tr>
  <tr><td>7日涨跌幅</td><td><span class="up/down">+/-X.XX%</span></td></tr>
  <tr><td>同期BTC表现</td><td>+/-X.XX%</td></tr>
  <tr><td>市值 / 排名</td><td>$XXX亿 / #XX</td></tr>
  <tr><td>成交量趋势</td><td>放量/缩量/持平</td></tr>
  <tr><td>技术面信号</td><td>...</td></tr>
</table>

<h2>二、价格变动原因分析</h2>
<h3>项目层面因素</h3>
<ol><li>...</li></ol>
<h3>赛道传导因素</h3>
<ol><li>...</li></ol>
<h3>市场环境因素</h3>
<ol><li>...</li></ol>

<h2>三、新闻与社区情绪</h2>
<table>
  <tr><th>日期</th><th>事件</th><th>来源</th><th>影响</th></tr>
  <tr><td>...</td><td>...</td><td><a href="原文URL" class="src">来源名称</a></td><td><span class="tag tag-positive/negative/neutral">利好/利空/中性</span></td></tr>
</table>
<p>Fear & Greed Index: <strong>XX — 级别</strong></p>
<p>社区情绪: <strong>正面/负面/中性</strong></p>

<h2>四、赛道对比</h2>
<table>
  <tr><th>代币</th><th>7日涨跌</th><th>市值</th><th>关键动态</th></tr>
  <tr><td>{token_name}</td><td>...</td><td>...</td><td>...</td></tr>
  <tr><td>竞品A</td><td>...</td><td>...</td><td>...</td></tr>
  <tr><td>竞品B</td><td>...</td><td>...</td><td>...</td></tr>
</table>

<div class="onchain">
<h2>五、链上指标与代币经济学</h2>
<h3>链上指标</h3>
<ul>
  <li>活跃地址: ...</li>
  <li>TVL: $XXX (适用于DeFi/L1)</li>
  <li>哈希率/质押率: ...</li>
</ul>
<h3>代币经济学</h3>
<ul>
  <li>流通量/总供应量: XXX / XXX (流通率 XX%)</li>
  <li>近期解锁: ...</li>
  <li>通胀/通缩机制: ...</li>
</ul>
</div>

<h2>六、市场环境</h2>
<ul>
  <li>BTC主导率: XX% (资金偏向BTC/山寨币)</li>
  <li>加密总市值: $X.XX万亿 (7日变化: +/-XX%)</li>
  <li>DXY (美元指数): XXX (强势/弱势)</li>
  <li>BTC ETF 资金流: 本周净流入/流出 $XXX亿</li>
  <li>关键宏观因素: ...</li>
</ul>

<h2>七、趋势展望</h2>
<h3>短期 (1-2周)</h3>
<ul><li>...</li></ul>
<h3>中期 (1-3月)</h3>
<ul><li>...</li></ul>
<h3>主要风险</h3>
<div class="risk">
<ol><li>...</li></ol>
</div>

<div class="references">
<h3>参考来源</h3>
<ol>
  <li>价格数据: <a href="URL" class="src">来源名称（如 CoinGecko / CoinMarketCap）</a></li>
  <li>新闻: <a href="URL" class="src">来源1</a> / <a href="URL" class="src">来源2</a></li>
  <li>链上数据: <a href="URL" class="src">来源名称（如 Glassnode / DeFiLlama）</a></li>
  <li>Fear & Greed Index: <a href="URL" class="src">来源名称（如 Alternative.me）</a></li>
  <li>市场数据 (BTC主导率 / ETF资金流等): <a href="URL" class="src">来源名称（如 Farside Investors）</a></li>
</ol>
</div>

<div class="disclaimer">声明: 本报告由 AI 自动生成，仅供参考，不构成任何投资建议。加密货币波动剧烈，投资有风险，决策需谨慎。</div>
</div>
</body>
</html>
```

**HTML 填写规则:**
- 加密货币涨跌幅为正时使用 `class="up"`（绿色），为负时使用 `class="down"`（红色）— 注意与A股相反，遵循国际惯例
- 新闻影响标签: 利好用 `tag-positive`，利空用 `tag-negative`，中性用 `tag-neutral`
- 链上指标区块使用 `class="onchain"`（紫色背景）
- 将模板中的占位符替换为实际数据，删除注释
- 确保 HTML 完整可直接在浏览器中打开
- 「参考来源」区块须填入各 Agent 返回的实际 URL；新闻表格的「来源」列须包含可点击原文链接

将报告保存为文件: `{token_name}-analysis-{date}.html`，保存在当前工作目录。

---

## Phase 4: 生成 PDF 报告

基于 Phase 3 生成的 HTML 文件，通过 Chrome headless 打印 PDF：

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf="$(pwd)/{token_name}-analysis-{date}.pdf" \
  --no-pdf-header-footer \
  "file://$(pwd)/{token_name}-analysis-{date}.html"
```

> **注意**: 如果系统没有 Chrome，可使用 `npx -y md-to-pdf "$(pwd)/{token_name}-analysis-{date}.html"` 作为备选方案。

最终输出两份文件：
- `./{token_name}-analysis-{date}.html` — HTML 版本（可在浏览器中打开）
- `./{token_name}-analysis-{date}.pdf` — PDF 版本（可直接分享）

---

## Error Handling

- **Agent 超时或失败**: 如果某个 Agent 未返回结果，在报告中标注该维度为"数据缺失"，其余维度照常分析
- **代币名称无法识别**: 提示用户确认代币名称或符号
- **官网无法访问**: 跳过官网抓取，依赖搜索引擎结果
- **数据源不一致**: 以多数数据源为准，在报告中注明数据差异

## Notes

- 每个 Agent 的输出严格限制字数，防止主线程上下文溢出
- 综合分析阶段重在 **交叉关联**，而非简单罗列
- 因果分析应区分 "相关" 与 "因果"
- 趋势预测需明确标注不确定性
- 加密市场 24/7 运行，时间参考以 UTC 为准
- 涨跌颜色遵循国际惯例 (绿涨红跌)，与 A 股分析不同
