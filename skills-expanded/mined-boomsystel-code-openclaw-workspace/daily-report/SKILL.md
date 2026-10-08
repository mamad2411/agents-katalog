# OpenClaw 每日智能日报技能

*创建时间：2026-02-07*

## 📋 功能说明

每日自动生成并推送智能日报，包含：
- 💰 BTC 实时行情
- 🌤️ 天气预报
- 📝 每日一句
- 📊 简易健康/效率提示

## 🚀 使用方式

### 手动触发
```
说 "生成日报" 或 "今日日报"
```

### 自动定时
- 每天早上 8:00 自动生成
- 可自定义时间

## 📊 输出示例

```
📅 2026-02-07 智能日报

💰 BTC 行情
- 当前价格：$96,500
- 24h 涨跌：+2.3%
- 恐惧贪婪指数：55（中立）

🌤️ 天气
- 北京：晴，3-12°C
- 空气质量：良

📝 每日一句
"投资的第一条规则是不要亏钱。第二条规则是永远不要忘记第一条。"

💡 效率提示
- 今天适合：学习新知识、整理文件
- 注意事项：避免冲动决策

🌟 祝你今天愉快！
```

## 🔧 技术实现

### 核心模块

#### 1. BTC 行情抓取
```python
import ccxt

def get_btc_price():
    exchange = ccxt.binance()
    btc = exchange.fetch_ticker('BTC/USDT')
    return {
        'price': btc['last'],
        'change_24h': btc['percentage'],
        'high': btc['high'],
        'low': btc['low']
    }
```

#### 2. 天气信息
```python
def get_weather(city='北京'):
    # 使用 weather 技能获取天气
    result = await weather.call(city=city)
    return result
```

#### 3. 每日一句
```python
QUOTES = [
    "投资的第一条规则是不要亏钱。",
    "别人贪婪时我恐惧，别人恐惧时我贪婪。",
    "时间是优秀企业的朋友，是平庸企业的敌人。",
    "投资比的是谁更少犯错，而不是谁更聪明。",
]

def get_daily_quote():
    import datetime
    day = datetime.datetime.now().day
    return QUOTES[day % len(QUOTES)]
```

#### 4. 日报生成
```python
async def generate_daily_report():
    btc = get_btc_price()
    weather = get_weather()
    quote = get_daily_quote()
    
    report = f"""
📅 {get_today_date()} 智能日报

💰 BTC 行情
- 当前价格：${btc['price']:,.0f}
- 24h 涨跌：{btc['change_24h']:+.2f}%

🌤️ 天气
- {weather['city']}：{weather['condition']}，{weather['temp']}°C

📝 每日一句
"{quote}"

💡 效率提示
{get_daily_tip()}

🌟 祝你今天愉快！
"""
    return report
```

#### 5. Telegram 推送
```python
async def send_to_telegram(report):
    await telegram.send_message(
        message=report,
        channel='main'  # 或指定用户
    )
```

## ⏰ 定时配置

### Cron 表达式
```json
{
  "name": "daily-report",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "生成今日日报并发送到 Telegram"
  },
  "sessionTarget": "main"
}
```

### 含义
- 每天早上 8:00 (北京时间)
- 自动生成日报
- 推送到主会话

## 🛠️ 依赖

- `ccxt` - 加密货币数据
- `python-binance` - 可选替代
- `openclaw-weather` - 天气技能
- `openclaw-telegram` - 消息推送

## 📁 文件结构

```
skills/daily-report/
├── SKILL.md          # 技能说明
├── daily_report.py   # 核心逻辑
├── config.json       # 配置文件
└── README.md         # 使用文档
```

## 🎯 扩展功能

### 未来可添加
- [ ] 股票行情
- [ ] 新闻摘要
- [ ] 日程提醒
- [ ] 习惯追踪
- [ ] 体重/健康记录
- [ ] 支出记录

### 进阶版
- AI 分析建议
- 多城市天气
- 多语言支持
- 语音播报

## 💡 使用建议

1. **先测试**：手动触发几次，确认数据准确
2. **调整时间**：根据个人习惯设置合适的时间
3. **优化内容**：根据需求增删模块
4. **保持简洁**：日报不宜过长，1屏内完成

## 🔒 注意事项

- 保护 API Key
- 控制请求频率
- 避免敏感信息泄露
- 定期检查数据来源可靠性

---

*最后更新：2026-02-07*
