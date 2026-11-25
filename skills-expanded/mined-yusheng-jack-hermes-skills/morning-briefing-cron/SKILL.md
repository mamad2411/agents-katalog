---
name: morning-briefing-cron
description: 每日自动推送晨间简报——聚合新闻、天气和股票行情
version: 1.0.0
---

# Morning Briefing (Cron Job)

每日自动推送的晨间简报，通过 Cron Job 定时执行。聚合新闻、天气和股票行情数据，格式化输出完整简报。

## 前置条件

- Hermes Agent 已配置浏览器工具和飞书/Telegram 等消息平台
- （可选）Bocha API Key：`~/.hermes/.env` 中添加 `BOCHA_API_KEY=YOUR_KEY`

---

## 数据来源

### 1. 节假日判断

在 `~/.hermes/workspace/memory/milestones/china-holidays-2026.json` 中配置节假日数据。

### 2. 新闻聚合

**Google News（可选，高质量国际新闻）：**
- 国内新闻: `https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=zh-CN&gl=CN&ceid=CN:zh-Hans`
- 国际新闻: `https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en`

**国内新闻门户（首选）：**
1. **百度新闻** → `https://news.baidu.com/` — 实时国内头条，含热搜新闻词
2. **新浪国际新闻** → `https://news.sina.com.cn/world/` — 推荐首选，含分钟级时间戳
3. **腾讯新闻** → `https://news.qq.com/` — 实时时间戳
4. **新浪首页** → `https://news.sina.com.cn/` — 右侧"热榜" Top 10 热搜
5. **新浪国内新闻** → `https://news.sina.com.cn/china/`
6. **网易新闻** → `https://news.163.com/`
7. **新华网** → `https://www.xinhuanet.com/politics/`

**补充来源：**
- **BBC 中文 RSS:** `https://feeds.bbci.co.uk/zhongwen/simp/rss.xml`

**批量提取技巧（使用 browser_console）：**
```javascript
browser_console expression="Array.from(document.querySelectorAll('a')).map(a => ({text: a.textContent.trim(), href: a.href})).filter(a => a.text && a.text.length > 5 && a.text.length < 100).slice(0, 100)"
```

### 3. 天气

**方式一（浏览器）：**
```bash
browser_navigate → https://weather.com.cn/weather/{cityID}.shtml
```
城市代码：南京=101190101, 北京=101010100

**方式二（wttr.in，更快）：**
```bash
browser_navigate → https://wttr.in/Nanjing?format=3
browser_navigate → https://wttr.in/Beijing?format=3
```

**终端方式（wttr.in）：**
```bash
curl -s 'https://wttr.in/Nanjing?format=3'
```

### 4. 股票行情

**跟踪标的：**

| 市场 | 股票 |
|------|------|
| 🇨🇳 中概科技 | BABA (阿里), 0700.HK (腾讯), 3690.HK (美团), JD (京东), PDD (拼多多) |
| 🇺🇸 美国科技 | AAPL (苹果), MSFT (微软), GOOGL (谷歌), AMZN (亚马逊), META (Meta), NVDA (英伟达) |

**推荐来源：Sina Finance API（稳定可靠）**

美股（`gb_` 前缀）：
```bash
curl -s "https://hq.sinajs.cn/list=gb_aapl,gb_msft,gb_googl,gb_amzn,gb_meta,gb_nvda,gb_baba,gb_jd,gb_pdd" \
  -H "Referer: https://finance.sina.com.cn"
```

港股（`hk` 前缀）：
```bash
curl -s "https://hq.sinajs.cn/list=hk00700,hk03690" \
  -H "Referer: https://finance.sina.com.cn"
```

**⚠️ 重要：** Sina Finance 需要 `Referer: https://finance.sina.com.cn` 头，否则返回空响应。

**备用来源：Yahoo Finance（curl 到文件后解析）**
```bash
for sym in BABA 0700.HK 3690.HK JD PDD AAPL MSFT GOOGL AMZN META NVDA; do
  curl -s "https://query1.finance.yahoo.com/v8/finance/chart/${sym}?interval=1d&range=1d" \
    -H "User-Agent: Mozilla/5.0" \
    -o "/tmp/stock_${sym}.json"
done
```

---

## 输出格式

```markdown
🌅 晨间简报 | YYYY-MM-DD 周X [工作日/休息日]

🇨🇳 国内热点 Top 10（8-10 条带摘要）
🌍 国际热点 Top 10（8-10 条带摘要）
📈 科技股 Top 11（中国 + 美国，表格格式）
🌤️ 天气（城市1/城市2）
💡 出行建议
```

## 已知注意事项

| 问题 | 说明 |
|------|------|
| Sina Finance 需要 Referer 头 | 必须添加 `-H "Referer: https://finance.sina.com.cn"` |
| Yahoo Finance 有频率限制 | 过度请求会返回 429 Too Many Requests |
| 非交易日股票数据 | 显示上一个交易日收盘价，标注市场已关闭 |
| 节假日配置需手动更新 | 每年更新 holidays JSON 文件 |
| 浏览器安全扫描器 | `execute_code` 不能在 cron 中使用，所有数据抓取需用 `browser_navigate` |
