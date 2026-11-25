---
name: flight-monitor-skill
description: 监测国内 + 国际航班价格，盯特定航班号、当价格跌破心理价位时自动推送告警。触发场景：用户说"机票价格监测"、"监测航班价格"、"flight price tracker"、"订机票提醒"、"CZ6895 价格"、"降到多少提醒我"、"盯航班"、"便宜了告诉我"、"机票午间总结"、"国际机票"、"东京机票"、"PEK-NRT"、"机票历史趋势"、"飞猪机票"，或要求监控某条航线在低价时收到通知。
version: 1.5.5
author: qinthqod
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [flight, monitor, price-tracker, china, ctrip, csair, feishu, wechat, daily-summary, international, cabin, roundtrip, multi-route, price-trend, holiday, fliggy, flyai]
    related_skills: [cron-web-briefings, gateway-platform-operations, alibaba-flyai/flyai-skill]
---

# Flight Price Monitor — 机票价格监测 skill

Track domestic **and international** China flight routes and get notified when your target flight (or any flight on the route) drops below a price you set.

**v1.1.0 双 job 模式**（2h 监测 + 12:00 午间总结）

**v1.2.0 五大新功能**（2026-08-13）：
- **🌏 国际机票**（携程国际 + 去哪儿国际，主备双源；自动币种识别 USD/EUR/JPY/KRW 等）
- **📈 价格趋势**（7d / 30d 最低均价 + 相对跌幅% + 30天新低标记，从 SQLite 历史快照算）
- **✈️ 往返航线**（`return_date` 字段，渲染时显示"→ 返程日"）
- **📋 多航线同装**（`config.json` 改 `routes: []` 数组，`--all-routes` 一次跑全部）
- **🛏️ 多舱位**（Y=经济/C=商务/F=头等/W=超级经济，舱位独立去重 + 趋势）
- **🎉 节假日错峰提示**（节前 14 天 ~ 节后 3 天，给"订票高峰/错峰窗口"建议）

> **🔀 跟 FlyAI（飞猪）skill 的协作**：本 skill 是 **monitor**（持续盯 + 跌破告警）。  
> 如果用户**想先查一次实时价**（不是持续盯），推荐装 [alibaba-flyai/flyai-skill](https://github.com/alibaba-flyai/flyai-skill) 走飞猪数据（`npm i -g @fly-ai/flyai-cli`）。  
> **v1.3.0 起**：本 skill 的国际航线**主源**直接调 `flyai search-flight`（与 alibaba-flyai/flyai-skill 共用 CLI）。  
> 两个 skill 是**深度集成**关系——flyai 提供数据，monitor 提供持续告警。AI 抽取时按用户意图分发：  
> - 用户说"查一下 / 找一下 / 多少钱" → 调 flyai search-flight  
> - 用户说"盯着 / 监测 / 降到 X 告诉我" → 用本 skill 装 monitor（自动调 flyai）

## 🚀 30 秒上手（复制粘贴给 AI）

> 把下面这段直接发给 Codex / Workbuddy / 任何智能体，它就懂怎么用这个 skill：

```
请阅读 https://github.com/qinthqod/flight-monitor-skill/blob/master/SKILL.md 学习这个 skill。

我要监测一个航班：乌鲁木齐到广州，10 月 5 号出发，盯 CZ6895 这班，
降到 ¥2000 以下提醒我（推飞书）。
```

**接下来用户只需要像聊天一样说就行**，AI 会问剩下的问题：

```
帮我监测一下机票                              ← 最简输入
国庆回广州便宜点告诉我                          ← 自然语言
监测北京大兴到上海虹桥，11 月 20 号，低于 1500 推微信
10 月 5 号乌鲁木齐到广州 CZ6895 降到 2000 告诉我
```

AI 会自动：
1. 抽取城市、日期、航班、阈值
2. 缺什么就问什么（一次只问一个，不烦你）
3. 确认后自动装好 cron + 跑一次验证
4. 价格跌破阈值时才推你，否则静默

## When to Use

- User wants to monitor flight prices: "监测 X 到 Y 的机票", "flight price tracker"
- User wants a price drop alert: "降到 2000 以下提醒我", "订票提醒"
- User wants to watch a specific flight: "CZ6895 哪天便宜", "盯着南航这班"
- User wants a long-running cron that pushes price updates

## What you (the agent) need to do — 你要做什么

### Step 1: 理解用户意图（自然语言抽取）

用户说的可能是完整描述，也可能只说了一半。**从任何自然语言里抽出下面 5 个字段**：

| 字段 | 例子 |
|---|---|
| **from_city** | "乌鲁木齐" / "URC" / "Wulumuqi" → 统一转成 IATA 码 `URC` |
| **to_city** | "广州" / "CAN" / "白云机场" → `CAN` |
| **date** | "10月5号" / "国庆" / "下周五" / "2026-10-05" → 转成 `YYYY-MM-DD` |
| **focus_flight**（可选） | "CZ6895" / "南航那班" / "下午那班" → `CZ6895`（拿不到就让用户写） |
| **threshold**（可选） | "两千" / "2000" / "2000 以下" / "便宜点" → `2000`（拿不到就让用户写） |

抽取规则：
- 中文城市名 → 查 `references/city-codes.md` 映射成 IATA
- 不在表里 → 用 `web_search` 查
- 相对日期（"下周三"）→ 用当前日期推算（2026-08-11）
- 模糊阈值（"便宜点"、"降点"）→ 反问明确数字

### Step 2: 检查缺什么，提醒补全

抽完之后对比下面清单。**缺的字段用一句话问用户补全**，不要一次性问一堆：

```
已识别：
  ✅ 出发：乌鲁木齐 (URC)
  ✅ 到达：广州 (CAN)
  ✅ 日期：2026-10-05
  ❓ 航班号：CZ6895 是你想盯的那班吗？
  ❓ 心理价位：降到多少提醒你？

还差 2 个信息：
  • 航班号（可选，不填就监测整条航线最便宜的）
  • 心理价位（必需，例如 ¥2000）
```

**最少要凑齐 4 个必填项**：from / to / date / threshold。focus_flight 可选。

### Step 3: 选推送渠道

如果用户没指定推送渠道，**问一次**：

```
你想怎么收到提醒？
  1) 智能体（写到 ~/.hermes/cron/output/，开箱即用）
  2) 飞书（推到你飞书的某会话，需要 FEISHU_FLIGHT_CHAT_ID）
  3) 微信（走 iLink gateway，需要 WEIXIN_TOKEN）
  可多选，逗号分隔，比如 "1,2"
```

### Step 4: 写配置 + 装 cron + 跑一次

确认后：
1. 写 `~/.flight-monitor/config.json`
2. **装 cron**——两种方式二选一：
   - **推荐：`bash scripts/install_hermes_cron.sh`** — 走 Hermes cronjob，自动装**两个 job**（2h 监测 + 12:00 午间总结），不依赖系统 crontab；装在用户自己的 Hermes profile 里
   - 旧式：`bash scripts/install_cron.sh` — 走系统 crontab，只装 2h 监测（**没有午间总结**）
3. 跑一次 `--dry-run` 验证（用户能看到报告但不会被推送打扰）
4. 告诉用户"装好了，下一次价格触发会推 2h 监测 + 每天 12:00 会推午间总结"，并说明第一次推送的时间窗

### Step 5: 监控已启动

不要再问了。让 cron 自动跑。**有结果才推** — 价格跌破阈值才打扰用户，否则保持静默。

## Worked examples — 对话样例

### 例 1：完整描述
```
用户：帮我监测 10 月 5 号乌鲁木齐回广州的 CZ 6895，降到 2000 以下告诉我
你：好的，我整理一下确认：
    • 出发：乌鲁木齐 URC
    • 到达：广州 CAN
    • 日期：2026-10-05
    • 航班：CZ6895
    • 阈值：¥2000
    怎么收到提醒？1) 智能体 2) 飞书 3) 微信
用户：飞书
你：[跑 install_cron.sh + dry-run + 报告] 装好了，CZ6895 一降到 ¥2000 以下就推你飞书。
```

### 例 2：半描述
```
用户：我要监测机票
你：要监测哪条航线？告诉我：
    • 出发地 + 到达地（例如：乌鲁木齐 → 广州）
    • 出发日期（例如：10 月 5 号）
    • 想盯的具体航班（可选）
    • 降到多少提醒你（例如：¥2000）
```

### 例 3：模糊
```
用户：国庆回广州便宜点告诉我
你：国庆是 10 月 1 号 ~ 7 号。你想哪天回？另外"便宜点"具体是降到多少提醒你？
```

### 错误输入的处理
- **国际航班**（v1.2.0 起支持）："支持国际机票——你从哪飞哪？降多少（币种）提醒你？"
- **没填币种**的国际航线："降到 600 美元以下，币种用 USD 还是人民币？"
- **查不到 IATA 码**：用 `web_search "北京大兴机场 IATA 代码"` 查
- **日期已过期**："10 月 5 号是 55 天后，没问题；要监测的是过去的日期请告诉我"
- **多机场城市**："北京" → 反问 PEK 首都 / PKX 大兴
- **舱位没填**：默认 Y 经济；用户说"商务舱"就用 C

## Architecture (one-liner)

`scripts/fetch.py` hits Ctrip + China Southern, picks the lowest matching flight, decides if it crossed your threshold, and emits a notification via your chosen channel.

**v1.1.0 双 job 模式**：

```
            ┌────────────────────────────────────────┐
            │  SQLite snapshots (data/flight.db)    │
            │  + 每 2h fetch.py 写入新快照             │
            └────────┬────────────────────┬─────────┘
                     │                    │
       跌破阈值才推   │                    │   每天 12:00 推
       (no_agent)    ▼                    ▼   (no_agent, deliver=feishu)
              2h 监测 job            12:00 午间总结 job
              fetch.py 直跑         daily_summary.py 读快照
              SILENT/SILENT/告警      飞书 markdown 卡片
```

两个 job 完全独立：
- **2h 监测**只跑 fetch.py → 跌破阈值才推，没跌破静默。**不写 SQLite 快照不算完事**。
- **12:00 午间总结**只读 SQLite 已有快照，**不抓新数据**。总结前必须有 ≥ 1 次 fetch.py 写入。

## Push channel details — 推送渠道详情

| Channel 渠道 | What happens 行为 | Setup 配置 |
|---|---|---|
| `agent` | 写到 `~/.hermes/cron/output/flight-monitor/`，让跑 cron 的智能体拾取。无需配置。 | 无 |
| `feishu` | 通过 `lark-cli im +messages-send` 推送 markdown 到飞书会话 | `export FEISHU_FLIGHT_CHAT_ID=oc_xxx` |
| `wechat` | 调用 Hermes iLink / 微信 gateway 推送 | `export WEIXIN_TOKEN=...`（你已有） |

The user picks at install time. Multiple channels supported.

## Reference docs — 参考文档

- [references/setup.md](references/setup.md) — 安装详解（AI 自动安装 + 手动安装）
- [references/push-channels.md](references/push-channels.md) — 三渠道配置（agent / 飞书 / 微信）
- [references/city-codes.md](references/city-codes.md) — 常用城市 IATA 码表（AI 抽取航线时查；**v1.2.0 加 50+ 国际城市**）
- [references/troubleshooting.md](references/troubleshooting.md) — 故障排查
- [references/dual-cron.md](references/dual-cron.md) — **v1.1.0**：2h 监测 + 12:00 午间总结双 job 装法
- [references/v12-features.md](references/v12-features.md) — **v1.2.0 新**：国际 / 趋势 / 往返 / 多航线 / 多舱位 / 节假日 5+1 大新功能详解

## The hard lesson (don't relearn this) — 经验教训（别重蹈覆辙）

**1. 携程 PC 直访问搜索 URL 会被 `whaleguard` 拦截。** `scripts/fetch.py` 必须走两步流程：先访问 `https://www.ctrip.com/`（种 cookie），再访问搜索列表 URL — 这样 `batchSearch` XHR 才会触发。跳过第 1 步就拿不到数据。**不要删 `fetch_ctrip_batchsearch()` 的两步流程。**

**2. 双 job 不要混。** 2h 监测 job 跟 12:00 午间总结 job 是**两个独立 cron job**：
- 监测 job 用 `scripts/fetch.py` 直跑（no_agent=true，跌破阈值才推，stdout 空 = 静默）
- 总结 job 走 `~/.hermes/scripts/flight-monitor-daily-summary.sh` 包装（no_agent=true，固定推飞书 markdown）
- **不要把 daily_summary.py 塞进 2h 监测 job 里**——fetch.py 跌破阈值才推，summary 必须每天出；混一起要么误推要么漏推。

**3. `daily_summary.py` 不会自己抓数据。** 它只读 SQLite 快照。**装完 cron 后第一次总结前**，必须至少跑过一次 `fetch.py` 写入快照，否则 12:00 总结会空数据推送。

**4. 国际航线去哪儿国际备源当前不可用。** 携程国际是主源（Playwright + XHR 拦截），去哪儿 H5 接口被 JS 渲染挡住，curl 拿不到价格。**主源失败时 silent**——用户必须**手动查**网页确认价格。详见 `references/v12-features.md` 第 1 节。

**5. 节假日表只到 2027 年底。** 2028 年起要补 `CN_HOLIDAYS_2028` 数组。**春节日期按农历每年不同**，硬编码对农历春节不准确。

**6. 趋势段需要历史快照。** 新装 cron 后前 2h 无趋势。建议装完 cron 后**手动跑一次 fetch.py**（让 SQLite 立刻有第一份快照），再启 2h 周期。

**7. 舱位独立去重。** Y 和 C 不会互相去重——经济舱 1500 推过后，商务舱 3000 仍会推。**这是设计意图**，不是 bug。

**8. 多航线的 route_key。** `{from}-{to}-{date}-{cabin}`——同一条航线换舱位会重新去重。换 focus_flight 不会换 route_key（focus_flight 不参与去重）。

**9. v1.3.0：flyai CLI 必装。** 国际航线主源 = `flyai search-flight` subprocess 调。装：`npm i -g @fly-ai/flyai-cli`。**flyai 未装时**自动降级到携程国际 + 去哪儿（行为同 v1.2.0）。  
**10. v1.3.0：flyai 价格是人民币。** `flyai search-flight` 默认返回 CNY 报价。用户说"降到 600 美元"——AI 抽取时把 600 美元转 CNY（约 4320 元）后填入 `threshold` 字段，**不要**在 fetcher 层换算（汇率波动）。  
**11. v1.3.0：flyai 体验模式限制结果数。** `systemMessage` 会提示"部分搜索结果可能受限，请前往飞猪 AI 开放平台获取正式 API Key"。`FLYAI_API_KEY` 设置后无限制（用 `flyai config set FLYAI_API_KEY "..."`）。  
**12. v1.3.0：drop_pct 输出已修。** v1.2.0 时显示 "🔻 +1.7%"（符号冗余），v1.3.0 改成"🔻 +1.7%"（跌用 +1.7%、涨用 -1.7%）。  
**13. v1.3.0：flyai 商务舱远期可能 0 条。** 实测 SHA→PAR 12-20 返 12-27 返 0 条（"智慧交通结果为空"）。远期或小机场 → 飞猪备源也可能 0 → fallback 到携程国际。

**14. v1.5.0：敏感信息铁律。** 本 skill 是**公开 GitHub 仓库**，**禁止**在代码、注释、文档里出现：
- 本机绝对路径（`/home/<user>/...` / `/Users/...` / `C:\...`）→ 用 `$HOME/<dir>` + env 变量
- 飞书 / 微信 chat_id / open_id → 占位符 `oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- 用户私有服务 URL（如 `ilink.bot.<user>.cn`）→ 占位符 `https://example.com` + env 变量
- 用户邮箱 / 手机号 / API token
- 私有的 chat_id / cron job_id（如 `b381db3a25b5`）

**改动姿势**：把 hardcoded 值改成 env 变量读取，默认值用占位符。例如：
```python
# 错误（提交前会被 grep -rn 拦下）：
DEFAULT_DB_PATH = "/home/<your-username>/flight-monitor/data/flight.db"

# 正确：
DEFAULT_DB_PATH = os.environ.get("FLIGHT_DB_PATH", str(Path.home() / "flight-monitor" / "data" / "flight.db"))
```
**提交前自检**：`grep -rn "/home/\|/Users/\|oc_[a-z0-9]\{20,\}\|ilink\.bot" --include="*.py" --include="*.sh" --include="*.md" .` 应为 0 行（除本说明段里作为反例外）。

**15. v1.5.1：`min/max` 等聚合对 `None` 必崩。** Python 3 不允许 `None < float` 比较。如果 SQLite 聚合列（`direct_min` / `transit_min` / `global_min`）可能 NULL（抓数据失败时整行 NULL），任何 `min(r[col] for r in rows)` / `max(...)` / `sorted(...)` 都会抛 `TypeError: '<' not supported between instances of 'NoneType' and 'X'`。**改写姿势**：先过滤 None 再聚合，全空时返 `None`（与脚本其它 None 处理一致）：
```python
# 错误（NULL 时整次 cron 失败）：
"low": min(r[2] for r in snap_rows),
"high": max(r[2] for r in snap_rows),

# 正确：
"low": (lambda vs: min(vs) if vs else None)([r[2] for r in snap_rows if r[2] is not None]),
"high": (lambda vs: max(vs) if vs else None)([r[2] for r in snap_rows if r[2] is not None]),
```
**触发场景**：OTA 接口 502 / 反爬 / whaleguard 拦截 → 抓数据脚本 fallback 写 NULL → cron 整次失败 → 用户收不到总结。**实测 8-14 早上 9:08-10:08 三次抓数据失败，DB 里 9 行 NULL，12:00 cron 修前会崩**。

**16. v1.5.1：发布前必须 bump `SKILL.md` frontmatter `version` 字段。** v1.4.0 / v1.5.0 发布时**忘记 bump frontmatter 版本号**（一直在 v1.3.0）—— `SKILL.md` 是用户/AI 加载时看到的第一份文档，版本号错会让用户误以为还在旧版。**强制自检**：
```bash
# 每次 commit 前跑：
grep -n "^version:" SKILL.md   # 应等于 CHANGELOG.md 顶部 [x.y.z] 的 x.y.z
```
同理 README 顶部 `**当前版本：vX.Y.Z**` 也要同步更新。

**17. v1.5.1：📱 推送示例必须是真实渲染输出，不能编。** README 里"📱 推送示例"段每个代码块必须是 `daily_summary.py` / `fetch.py` 实际打印的 markdown，不是按"看起来合理"凑的格式。**取真实输出的姿势**：
```bash
# 不推送飞书，只渲染 markdown 看真实格式：
FLIGHT_DB_PATH=/path/to/flight.db <venv>/bin/python -c "
import sys; sys.path.insert(0, 'scripts')
from daily_summary import build_summary, render_markdown
s, err = build_summary()
print(render_markdown(s))"
```
然后**整块复制**到 README 文档里。这是 v1.5.1 发布时我下意识编了示例 4 立刻回滚换真实输出的教训。

## Linked scripts

- `scripts/fetch.py` — main fetcher, runs all data sources and pushes to chosen channel
- `scripts/notify_*.py` — channel-specific notifiers (agent / feishu / wechat)
- `scripts/install_cron.sh` — registers the 2h cron line via system crontab (legacy, no daily summary)
- `scripts/install_hermes_cron.sh` — **v1.1.0 推荐**：装两个 Hermes cronjob（2h 监测 + 12:00 午间总结）