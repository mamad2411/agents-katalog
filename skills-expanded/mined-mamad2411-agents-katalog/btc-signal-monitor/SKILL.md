# BTC 信号监控系统

*创建时间：2026-02-07*

## 📋 功能说明

实时监控 BTC 行情，自动检测买卖信号并推送提醒。

### 核心功能

- 📊 **实时行情** - 获取 Binance 实时数据
- 📈 **技术分析** - RSI、MA 交叉、波动率
- 🎯 **信号检测** - 多维度信号评分
- 🔔 **自动报警** - Telegram 推送

---

## 🎯 监控指标

### RSI（相对强弱指数）

| 信号 | 阈值 | 说明 |
|------|------|------|
| 强烈买入 | < 25 | 极度超卖，可能反转 |
| 买入 | < 30 | 超卖区域 |
| 卖出 | > 70 | 超买区域 |
| 强烈卖出 | > 75 | 极度超买，可能反转 |

### MA 交叉

| 信号 | 条件 | 说明 |
|------|------|------|
| 金叉 | MA7 > MA25 | 短期上涨动能强 |
| 死叉 | MA7 < MA25 | 短期下跌动能强 |

### 综合评分

- **+3**: RSI 极度超卖 + 金叉 → 强烈买入
- **+2**: RSI 超卖 + 金叉 → 买入
- **-2**: RSI 超买 + 死叉 → 卖出
- **-3**: RSI 极度超买 + 死叉 → 强烈卖出

---

## 🚀 使用方式

### 单次检测

```bash
python3 btc_signal_monitor.py
```

### 持续监控（每60秒检测一次）

```bash
python3 btc_signal_monitor.py --continuous
```

### 监控其他交易对

```bash
# 监控 ETH
python3 btc_signal_monitor.py ETH/USDT

# 监控 SOL
python3 btc_signal_monitor.py SOL/USDT
```

---

## 📊 输出示例

```
⏰ 2026-02-07 10:00:00
--------------------------------------------------
✅ 获取数据 100 条
📊 当前价格：$70,031
📉 RSI：42.5（NEUTRAL）
📈 MA7：$69,800 | MA25：$71,200
📐 交叉：GOLDEN
📊 趋势：DOWNTREND | BULLISH

🎯 信号：BUY
   评分：2
   置信度：70%
   • RSI 中性 (42.5)
   • 均线金叉

💡 建议：
🟢 **买入信号**
当前价格：$70,031
建议：可以小仓位试探性买入
止损位：$68,500
```

---

## 🔧 配置说明

编辑 `btc_signal_monitor.py` 中的 `CONFIG` 字典：

```python
CONFIG = {
    "symbol": "BTC/USDT",        # 监控的交易对
    "timeframe": "1h",           # K线周期
    "rsi_period": 14,            # RSI 周期
    "rsi_oversold": 30,          # RSI 超卖阈值
    "rsi_overbought": 70,        # RSI 超买阈值
    "ma_fast": 7,                # 快速均线周期
    "ma_slow": 25,               # 慢速均线周期
    "check_interval": 60,        # 检查间隔（秒）
    "cooldown_minutes": 60,      # 报警冷却时间
}
```

---

## 🔔 Telegram 配置

```python
CONFIG = {
    "telegram_enabled": True,
    "telegram_chat_id": "你的ChatID",
}
```

---

## 📁 文件结构

```
btc-signal-monitor/
├── SKILL.md                 # 本文档
├── btc_signal_monitor.py   # 核心代码
├── README.md               # 快速开始
└── requirements.txt        # 依赖
```

---

## ⚠️ 风险提示

- **仅供参考**：信号不构成投资建议
- **历史不代表未来**：历史准确率不代表未来表现
- **设置止损**：建议设置合理的止损位
- **控制仓位**：不要满仓操作

---

*最后更新：2026-02-07*
