---
name: gold-investor
description: "黄金投资助手 - 实时监控金价、分析市场动态、提供投资建议。当用户需要查询金价、监控黄金投资、获取市场分析时使用。支持国际金价(XAU/USD)、国内金价(AU9999)、汇率换算。"
---

# 黄金投资助手 (Gold Investor)

专业的黄金投资监控和分析工具，帮助投资者实时掌握市场动态。

## 功能特性

- 📊 **实时金价查询** - 国际金价(XAU/USD)、国内金价(AU9999)
- 💱 **汇率监控** - USD/CNY 实时汇率
- 📈 **价格变动提醒** - 单日涨跌超过阈值自动通知
- 📰 **市场分析** - 地缘冲突、美联储政策对金价影响
- 📋 **持仓管理** - 记录成本价、持仓量、止盈止损位

## 快速开始

### 查询实时金价

```bash
# 获取当前金价
openclaw run gold-investor -- get-price

# 获取详细行情
openclaw run gold-investor -- get-market
```

### 设置价格提醒

```bash
# 涨跌超过2%时提醒
openclaw run gold-investor -- set-alert --threshold 2
```

### 查看持仓分析

```bash
# 分析当前持仓盈亏
openclaw run gold-investor -- analyze
```

## 工作流程

### 1. 金价监控模式

当用户要求监控金价时：
1. 获取当前 XAU/USD 价格
2. 获取 USD/CNY 汇率
3. 计算国内金价估算值
4. 对比前一日价格计算涨跌幅
5. 如果涨跌超过阈值，生成提醒

### 2. 市场分析模式

当用户要求市场分析时：
1. 搜索最新黄金相关新闻
2. 分析地缘冲突、美联储政策等影响因素
3. 提供技术面和基本面分析
4. 给出投资建议（仅供参考）

### 3. 持仓管理模式

当用户要求管理持仓时：
1. 读取持仓配置（成本价、持仓量）
2. 计算当前市值和盈亏
3. 对比止盈止损位
4. 生成持仓报告

## 配置文件

创建 `~/.openclaw/skills/gold-investor/config.json`:

```json
{
  "holdings": {
    "type": "纸黄金",
    "costPrice": 480.5,
    "quantity": 10,
    "targetProfit": 520.0,
    "stopLoss": 460.0
  },
  "alert": {
    "enabled": true,
    "threshold": 2.0
  },
  "dataSources": {
    "international": "https://www.gold.org/goldhub/data/gold-prices",
    "domestic": "上海黄金交易所"
  }
}
```

## 命令参考

| 命令 | 说明 |
|------|------|
| `get-price` | 获取实时金价 |
| `get-market` | 获取市场行情 |
| `set-alert` | 设置价格提醒 |
| `analyze` | 分析持仓 |
| `report` | 生成日报 |

## 免责声明

⚠️ **投资有风险，本 Skill 仅供参考，不构成投资建议。**

## 相关链接

- [黄金投资指南](https://www.gold.org/investment)
- [上海黄金交易所](https://www.sge.com.cn)
- [美联储政策](https://www.federalreserve.gov)

---

*Powered by OpenClaw 🦕*
