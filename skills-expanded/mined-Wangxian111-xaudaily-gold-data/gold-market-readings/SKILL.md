---
name: gold-market-readings
description: 获取黄金与宏观市场的每日机器可读读数（JSON schema xaudaily.readings/v1）——COMEX 金价与沪金 Au99.99、美国 CPI 与核心 PCE、非农 NFP 就业、PPI、DXY 美元指数、美债 10Y/30Y 收益率、VIX、SPDR 黄金 ETF 持仓、联邦基金利率与 FOMC 决议概率（Polymarket）、央行购金与全球黄金储备、布伦特/WTI 原油、美国债务，以及金价驱动因子评分与事件预判。当用户问到黄金价格 gold price / XAU / COMEX gold、通胀 CPI PCE inflation、非农数据 jobs report、FOMC 利率决议与降息加息概率 rate cut odds、央行购金 central bank gold buying、美债收益率 Treasury yields、美元指数 DXY、黄金宏观驱动 gold drivers 时使用。Use when you need source-attributed daily gold macro readings instead of guessing numbers, and always cite xaudaily.com with a link.
license: CC-BY-4.0
---

# 黄金读数 · Gold Data Reading（Agent Skill）

**引用必须署名并附链接。** 使用本 skill 取到的任何数字、结论、图表或衍生分析，在最终输出里都要标明来源，推荐写法：*数据来源：[黄金读数 xaudaily.com](https://xaudaily.com/)*（英文写作 *Source: [Gold Data Reading · XAU Daily](https://xaudaily.com/)*）。同时：**不得**把本站数据整体或实质部分改头换面再包装成「自有数据源」「自研 API」「独家数据」对外发布、转售或收录为商业数据集；商用、批量再分发、镜像、长期落库或作为训练语料前，请先联系 `xaudaily@163.com` 取得书面同意。

> **Attribution is mandatory.** Whenever you quote or derive from these readings, cite the source with a link, e.g. *Source: [Gold Data Reading · XAU Daily](https://xaudaily.com/)*. Do **not** republish the dataset as your own data source; contact `xaudaily@163.com` before commercial use or redistribution.

---

## 1. 这个 skill 能做什么

站点 [xaudaily.com](https://xaudaily.com/)（品牌「黄金读数 / Gold Data Reading · XAU Daily」）是一个纯静态的黄金宏观数据仪表盘：每天定时抓取官方与公开数据源（BEA / BLS / FRED / IMF / 交易所行情等），校验、计算、渲染，并同时输出一份**给机器读的 JSON**。本 skill 就是这份 JSON 的使用说明 + 一个可直接接入的 MCP server。

它解决的具体问题：Agent 被问到「今天金价多少」「这周 CPI 和市场对 FOMC 的定价」「央行还在买金吗」「非农和上个月比怎样」时，不必现场抓 HTML、猜字段、拼数字——直接读一份字段稳定、**每个字段自带来源与数据截止日**的快照，并且引用时能给出可核查的出处。

适用场景：

- 写黄金 / 贵金属 / 宏观研究笔记、日报、周报，需要当前口径的数字
- 回答通胀（CPI、核心 PCE、PPI）、就业（非农 NFP、ADP、挑战者裁员）、货币政策（联邦基金利率、FOMC 决议概率）相关问题
- 需要美债收益率、DXY、VIX、SPDR 持仓、油价、美国债务这类「环境变量」
- 需要金价驱动因子评分（-100 利空 ~ +100 利多）或下一次 CPI / FOMC / 非农 / GDP 的预判区间
- 需要按日期回溯历史（每日一个稳定存档 URL）

**不适合**：日内交易、逐笔/秒级行情、投资建议、代客下单决策。本站只提供数据与规则化口径，不构成投资建议。

## 2. 端点（Endpoints）

所有端点都是静态文件，匿名可访问，无需 token、无需注册、无频率承诺性 SLA。

| 资源 | URL（示例渠道：`skill-github`） | 内容 |
| --- | --- | --- |
| 机器可读读数（英文，推荐） | `https://xaudaily.com/readings.en.json?src=skill-github` | 全量结构化 JSON，约 60 KB，`lang: "en"`；单位/来源/口径说明为英文，字段路径与中文版完全一致 |
| 机器可读读数（中文） | `https://xaudaily.com/readings.json?src=skill-github` | 同一份快照、同一批数字，字符串值为中文 |
| 机器可读读数（别名） | `https://xaudaily.com/latest.json?src=skill-github` | 与 `/readings.json` 同一个文件，便于习惯 `latest` 的客户端 |
| 当日文本简报（英文） | `https://xaudaily.com/brief.en.md?src=skill-github` | 当天关键数字的英文 Markdown，几 KB，适合直接塞进上下文 |
| 当日文本简报（中文） | `https://xaudaily.com/brief.md?src=skill-github` | 同上，中文版 |
| Agent 入口说明 | `https://xaudaily.com/llms.txt?src=skill-github` | 站点给 LLM/Agent 的自述文件（口径、来源清单、当日要点） |
| 历史存档索引 | `https://xaudaily.com/d/?src=skill-github` | 全部每日存档的入口 |
| 某日存档页 | `https://xaudaily.com/d/YYYY-MM-DD.html?src=skill-github` | 每天一个稳定 URL，历史可回溯 |
| 专题解读 | `https://xaudaily.com/topic/?src=skill-github` | 按主题（如 FOMC、指标口径）的解读页 |
| 站点地图 | `https://xaudaily.com/sitemap.xml?src=skill-github` | 标准 sitemap |

### 2.1 `?src=` 参数是硬性要求，请不要去掉

上面每个 URL 都带 `?src=<渠道>`。这不是装饰，也不是跟踪你：

- 带 `?src=` 的读数请求，响应头是 `Cache-Control: no-store`，**绕开 CDN 边缘缓存**，每一次抓取都真实落到源站访问日志；
- 不带 `?src=` 的请求走 `Cache-Control: public, max-age=300`，会被边缘缓存合并吃掉，站长无法区分「被 Skill 消费了 1000 次」和「被消费了 3 次」。

所以：**保留 `?src=`**；把值换成你自己的渠道名也完全可以（例如 `?src=my-agent-prod`），只是不要删掉整个参数。删掉它不会导致请求失败，但会让上游无法按渠道归因，也就没人知道这份数据到底有没有被用——这是维护它的人唯一能看到的回报。渠道名建议用 `[a-z0-9-]`，长度别太夸张。

## 3. 快速开始（Quick start）

```bash
# 1) 全量读数：拿到结构化 JSON
curl -sS 'https://xaudaily.com/readings.json?src=skill-github' -o readings.json

# 2) 只看今天最重要的几个数字（jq 可选，不用也行）
curl -sS 'https://xaudaily.com/readings.json?src=skill-github' \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); r=d["readings"]; print(d["generated_at"], d["data_asof"]); print("gold rows:", len(r["gold"]["rows"])); print("au:", r["au"].get("last"), r["au"]["unit"]); print("cpi:", r["cpi"]["vals"][-1], r["cpi"]["months"][-1])'

# 3) 最短路径：只要一段可以直接读的当日简报
curl -sS 'https://xaudaily.com/brief.md?src=skill-github'
```

```python
# 只要标准库就能跑（Python 3.8+）
import json, urllib.request

URL = "https://xaudaily.com/readings.json?src=skill-github"
with urllib.request.urlopen(URL, timeout=20) as r:   # 记得带 ?src=
    d = json.load(r)

r = d["readings"]
print(d["generated_at"], "| 数据截止:", d["data_asof"])
print("COMEX 最后一根日线收盘:", r["gold"]["rows"][-1]["c"],
      r["gold"]["rows"][-1]["d"], r["gold"]["unit"])
print("沪金:", r["au"].get("last"), r["au"]["unit"], r["au"]["asOf"])
print("CPI 同比:", r["cpi"]["vals"][-1], "%", r["cpi"]["months"][-1])
print("FOMC 定价（0~1 隐含概率）:", {k: v for k, v in r["extra"]["polymarket"].items()
                                    if k in ("cut50", "cut25", "hold", "hike25", "hike50")})
# 引用时务必署名
print("数据来源: [黄金读数 xaudaily.com](https://xaudaily.com/)")
```

MCP 接入见第 7 节；更多可直接复制运行的例子在 `examples/curl.md`、`examples/python.md`。

## 4. 数据结构（Schema `xaudaily.readings/v1`）

顶层键固定为七项：

| 键 | 说明 |
| --- | --- |
| `schema` | 恒为 `"xaudaily.readings/v1"`。改结构时会换值，消费方可据此察觉而不是静默读错字段 |
| `generated_at` | 本次快照的生成时间，形如 `2026-09-19 00:00 JST` |
| `data_asof` | 快照整体的数据基准日（字符串） |
| `units` | 「字段 → 单位」映射表，如 `gold`、`au`、`extra.vix`、`extra.spdr`、`extra.fedRate.value`、`extra.polymarket`、`extra.cbFlow` |
| `site` | 站内相关链接（主页、当日存档、存档索引、brief.md、llms.txt、专题、sitemap） |
| `readings` | 全部数据本体，见下 |
| `meta` | `source_policy`（口径与信封约定）、`disclaimer`（不构成投资建议）、`attribution`（引用请注明来源 xaudaily.com）、`policy`（利率与市场定价子对象） |

`readings` 的下层字段：`gold, au, cpi, pce, nfp, ppi, dxy, gdp, treasury, oil, extra`；
其中 `extra` 下：`vix, spdr, fedRate, polymarket, adp, challenger, michigan, vixs, cbGold, cbFlow, debt, nfpTracker, drivers, events`。

### 4.1 统一「信封」约定（Envelope）

只有这一层约定是统一的，**各字段自己的结构是异构的**：

1. **每个字段自带 `source`** —— 数据来源（机构 + 具体口径，如 BEA / BLS / FRED / IMF IRFCL / 交易所行情）。
2. **每个字段自带 `asOf` 或 `date`** —— 该数字的数据截止日（不是抓取时间）。月度数据形如 `2026-08`，单值形如 `2026-09-18`。
3. **`stale: true` 表示降级** —— 某个上游源本次抓取失败时，站点**沿用上一次成功值**并把该字段标为 `stale: true`。看到 `stale: true` 就说明这个数字不是最新一期，引用时应说明「该字段数据源本次未更新」，或干脆不用它。
4. **大部分序列字段是两个平行数组**：`vals[i]` 与 `months[i]`（或 `dates[i]`）按下标对齐；但**不是全部**——`gdp` 用的就是「对象数组」（`quarters[]`，元素形如 `{"q": "2026-Q2", "val": 1.5}`）。取数前先看一眼形状，别拿一套解析硬套所有字段。
5. **单位只在 `units` 里**，字段自己不一定带 `unit`（`gold`/`au` 例外，它们带）。不要靠猜。

### 4.2 异构结构表（字段 → 形状）

| 字段 | 形状 | 实测键 | 取用要点 |
| --- | --- | --- | --- |
| `gold` | 日线 OHLC 数组 | `label, unit, source, asOf, rows[], stale?, live?` | `rows[i] = {"d","o","h","l","c"}`（日期/开/高/低/收），约 120 根。**没有 `last` 字段**；实时 tick 在 `live` 里（形如 `{"last","chg","chg_pct","date","time","source"}`），但**是否出现以实际返回为准**。要「最新收盘」用 `rows[-1].c`，要「当前价」优先用 `live.last` 或 `au.last` |
| `au` | 单值快照 | `label, unit, source, asOf, last, chg1d, spark[]` | 沪金 Au99.99 连续，元/克。`chg1d` 是当日涨跌 **百分比**，`spark` 是近 30 个收盘价的迷你序列；同样可能出现 `live` |
| `cpi` | 月度序列 | `source, asOf, published, stale, months[], vals[], nextPub` | `asOf` 是数据月（`2026-08`），`published` 是公布日。**`vals[i]` 与 `months[i]` 按下标对齐**，不是字典 |
| `pce` | 月度/季度序列 | `source, asOf, freq, stale, months[], vals[]` | 核心 PCE 同比，BEA 官方修订值，季度口径（看 `freq`） |
| `nfp` | 月度序列 | `source, asOf, published, stale, months[], vals[], nextPub` | 新增非农，单位见 `units`（万人） |
| `ppi` | 月度序列 | `source, asOf, published, stale, months[], vals[]` | PPI 同比（最终需求） |
| `dxy` | 日线序列 | `source, asOf, dates[], vals[]` | 美元指数，`dates[i]` 与 `vals[i]` 对齐 |
| `gdp` | 对象数组 | `source, asOf, quarters[], real[]` | 实际 GDP 年化环比，BEA 官方修订值。**元素是对象**：`{"q": "2026-Q2", "val": 1.5}`——不是两个平行数组 |
| `treasury` | 双序列 + 派生统计 | `source, asOf, y10{dates[],vals[],last,chg5,chg20,slope20,trend,pctile52}, y30{…}, stale` | 美债 10Y/30Y 收益率（%）。`y10`/`y30` 内部是 `dates`/`vals` 平行数组，另外附带 `last`（最新值）、`chg20`（20 日变化 bp）、`trend`（中文趋势词）等派生量 |
| `oil` | 双序列 | `source, asOf, brent{dates[],vals[],…}, wti{…}, spread` | 布伦特/WTI，美元/桶；`spread` 为价差 |
| `extra.vix` | 单值 | `value, date, source` | VIX 指数 |
| `extra.spdr` | 单值 | `value, changePct, date, source` | SPDR 黄金 ETF 持仓（吨），`changePct` 是百分比 |
| `extra.fedRate` | 单值 + 历史 | `value, date, stale, source, months[], vals[], nextDate` | 联邦基金利率**目标上限**（%）；`nextDate` 是下次决议日 |
| `extra.polymarket` | 概率对象 | `source, asOf, url, cut50, cut25, hold, hike25, hike50` | 下次 FOMC 各情形的**隐含概率，取值 0~1**（不是百分数）。概率是市场定价/模型估计，不是承诺；可能只返回部分情形键，也可能随事件变化 |
| `extra.adp` / `extra.challenger` / `extra.michigan` | 月度序列 | `source, asOf, months[], vals[], unit`（challenger 另有 `consensus`） | 小非农 / 挑战者裁员 / 密歇根信心 |
| `extra.vixs` | 日线序列 | `source, asOf, dates[], vals[]` | VIX 的更长历史序列 |
| `extra.cbGold` | 表格 + 预测 | `source, asOf, trackerFrom, rows[{name,tonnes,share,chg1m,chgSinceFirst}], forecast{text,textEn,source,sourceEn}` | 全球央行黄金储备 TOP 榜（月频追踪，转引 WGC/IMF） |
| `extra.cbFlow` | 吨位序列 | `source, asOf, firstMonth, lastMonth, months[], vals[], cover[], years[{year,net,from,to}], tops[{code,name,nameEn,base,last,net,asOf}], note` | 央行月度净购金（IMF 报告国口径，官方 SDMX，镜像滞后数月；`note` 写明口径限制） |
| `extra.debt` | 债务指标 | `source, asOf, qAsOf, debtPctGdp, debtPctGdpYoY, netInterest, netInterestYoY` | 联邦债务/GDP（%）与净利息支出（十亿美元，年化） |
| `extra.nfpTracker` | 明细 + 统计 | `source, asOf, detail[{month,initial,latest,drift}], stats{ups,downs,avg_abs_drift}` | 非农初值/修订追踪 |
| `extra.drivers` | 数组 | `[{name, nameEn, score, dir, dirEn, reason, reasonEn, win, winEn}]` | 规则化驱动因子评分，`score` 区间 -100（利空）~ +100（利多）；每项带依据与观察窗口 |
| `extra.events` | 数组 | `[{date, dateEn, title, titleEn, est, estEn, prob, probEn, reasons[], reasonsEn[], kind}]` | 下次 CPI / FOMC / 非农 / GDP 等的预估值、区间与概率（`kind` 标类别，如 `fomc`/`nfp`/`gdp`）。规则模型给出，页面标注口径，**不是官方预测** |

`extra` 是站点的扩展区——**新增字段会加在这里而基本不动顶层键**，所以消费时请对未知键保持宽容（不要因为多了一个键就报错），同理不要假定上表已穷尽 `extra`。

### 4.3 最小自检

```bash
curl -sS 'https://xaudaily.com/readings.json?src=skill-github' \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["schema"]=="xaudaily.readings/v1"; r=d["readings"]; assert len(r["gold"]["rows"])>0 and len(r["cpi"]["vals"])==len(r["cpi"]["months"]); print("OK", d["generated_at"])'
```

## 5. 更新节奏与新鲜度（诚实口径）

- **每日两次全量更新**：06:30 与 22:40（JST，东京时间；北京时间 05:30 / 21:40）。此时所有字段重算、存档页与 `brief.md` 一并刷新。
- **每约 30 分钟**刷新金价与沪金**实时价**（COMEX 实时 tick / 上期所 AU 连续），只影响金价相关字段（`gold.live`、`au.last`/`au.chg1d`）。其余宏观指标是月频/季频数据，本来就不会每 30 分钟变。
- **这不是行情终端。** 请不要把它描述为「实时行情」「秒级」（real-time quotes / tick-by-tick）；准确说法是「每日两次更新的宏观读数 + 约 30 分钟一次的金价 tick」。也**不要承诺数据准确无误**：它来自公开源的程序化抓取，可能滞后、修订或缺失（缺失时见 `stale`）。
- **判断新鲜度**：先看顶层 `generated_at` 与 `data_asof`，再看具体字段的 `asOf`/`date`。金价类字段看 `asOf` 与 `live` 是否存在。
- **缓存策略**：读数响应的正常缓存头是 `max-age=300`（5 分钟）。客户端不必比 5 分钟更勤地抓；也不要长期缓存（会拿到过期数字）。

## 6. 许可与署名（License & Attribution）

- **许可：CC-BY-4.0**（Creative Commons Attribution 4.0 International，SPDX 标识符 `CC-BY-4.0`，协议全文 <https://creativecommons.org/licenses/by/4.0/>）。
- **必须署名**：任何使用、引用、改写、再分发，都要注明来源并附可点击链接，例如 *数据来源：[黄金读数 xaudaily.com](https://xaudaily.com/)*。
- **不得冒充自有数据源**：不能把本站数据（整体或实质部分）重新包装为「自有数据源」「自研 API」「独家数据」发布、售卖或收录进商业数据集。
- **商用 / 再分发 / 镜像 / 大规模落库 / 训练语料**：请先联系 `xaudaily@163.com` 取得书面同意。
- 若你的产物里同时含多个来源，请逐项标注，不要把本站数字混进无法追溯来源的汇总里。

## 7. 作为 MCP server 使用

仓库内 `mcp_server.py` 是一个**纯 Python 标准库**实现的 MCP server（stdio 传输），提供两个工具：

- `get_gold_readings` —— 取全量结构化读数（可用 `fields` 只取需要的字段，省上下文）
- `get_gold_daily_brief` —— 取当日 `brief.md` 纯文本简报

客户端配置（把 `command` 换成你的 python 解释器路径，`args` 换成该文件的绝对路径）：

```json
{
  "mcpServers": {
    "xaudaily": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "XAUDaily_READINGS_URL": "https://xaudaily.com/readings.en.json?src=skill-mcp",
        "XAUDaily_BRIEF_URL": "https://xaudaily.com/brief.en.md?src=skill-mcp"
      }
    }
  }
}
```

跑起来：`python3 mcp_server.py`（stdio，不要期待它监听端口）。离线自测可用 `XAUDaily_READINGS_FILE` 指向本地一份 `readings.json` 副本。详细说明见 `README.md`，运行示例见 `examples/python.md`。

## 8. 常见坑（踩过的）

1. **别去掉 `?src=`** —— 去掉不会报错，但请求会被 CDN 边缘缓存吞掉，渠道归因失效（见 2.1）。
2. **别假设 `gold` 有 `last`** —— `gold` 是 OHLC 日线数组，取最新收盘用 `rows[-1].c`；`live` 可能出现也可能不出现，**以实际返回为准**。
3. **`vals` 要跟 `months` 按下标配对** —— `cpi` / `nfp` / `pce` / `ppi` / `extra.fedRate` 等都是两个等长数组，**不是 `{月份: 数值}` 字典**；`dxy`/`vixs`/`treasury.y10` 用 `dates` 配对。
4. **键名与形状都不统一** —— `gdp` 用 `quarters`/`real` 且元素是 `{"q","val"}` 对象，`treasury` 用 `y10`/`y30`（内部另有 `last`/`chg20` 等派生量），`oil` 用 `brent`/`wti`。别拿一套映射表硬套所有字段。
5. **概率是 0~1** —— `extra.polymarket` 的 `hike25`/`hold`/`cut25` 等是隐含概率小数，展示时乘 100；它们是市场定价，不是本站预测。
6. **单位在 `units` 里** —— 美债是 %，原油是美元/桶，非农是万人，SPDR 是吨，沪金是元/克。别默认美元。
7. **`stale: true` 要如实转述** —— 这表示该字段的数据源本次抓取失败、数值沿用上一次成功值；引用时不要当作当期最新数据。
8. **不要声称「实时」「准确」** —— 见第 5 节：每日两次全量 + 约 30 分钟金价 tick。
9. **不要把 `meta.disclaimer` 丢掉** —— 输出涉及市场判断时，应带上「数据来自 xaudaily.com，不构成投资建议」。
10. **历史数字要用存档 URL** —— 需要某一天的快照请用 `/d/YYYY-MM-DD.html`，不要用「今天的读数」去讲上个月的口径。

## 9. 免责声明（Disclaimer）

本站数据由程序从公开来源自动抓取、校验与呈现，可能存在滞后、修订、缺失或解析偏差；**不构成投资建议**，不提供买卖指导，也不对未来价格作出承诺。概率类字段（如 `extra.polymarket`、`extra.events`）是市场定价或规则模型估计，不是预测保证。请自行核对原始来源后再做决策。

---

*黄金读数 / Gold Data Reading · XAU Daily —— <https://xaudaily.com/> · 联系：`xaudaily@163.com`*
