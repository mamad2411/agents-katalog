---
name: gold-copper-trading
description: 黄金和铜的实时行情查询与模拟交易（对接 openctp 模拟交易所）
version: 1.0.0
---

# 黄金铜交易技能

连接 openctp 模拟交易所，提供黄金和铜的实时行情查询、模拟买卖和持仓管理功能。
使用真实行情数据，模拟资金交易，不涉及真实账户和资金。

## 可用命令

### 获取黄金实时价格
```bash
python3 {baseDir}/scripts/get_price.py --symbol gold
```
返回黄金主力合约的最新价格、涨跌幅等信息（JSON格式）。

### 获取铜实时价格
```bash
python3 {baseDir}/scripts/get_price.py --symbol copper
```
返回铜主力合约的最新价格（JSON格式）。

### 获取铜金价比
```bash
python3 {baseDir}/scripts/get_price.py --ratio
```
返回铜价÷金价的比值，与阈值90的关系，以及方向建议。

### 买入黄金
```bash
python3 {baseDir}/scripts/trade.py --action buy --asset gold --amount 数量
```
买入指定克数的黄金。amount 单位为克。
⚠️ 重要：调用此命令前，必须先告知用户交易计划并等待用户确认。

### 卖出黄金
```bash
python3 {baseDir}/scripts/trade.py --action sell --asset gold --amount 数量
```

### 买入铜
```bash
python3 {baseDir}/scripts/trade.py --action buy --asset copper --amount 数量
```
amount 单位为吨。
⚠️ 重要：调用此命令前，必须先告知用户交易计划并等待用户确认。

### 卖出铜
```bash
python3 {baseDir}/scripts/trade.py --action sell --asset copper --amount 数量
```

### 查看持仓和损益
```bash
python3 {baseDir}/scripts/portfolio.py
```
返回当前现金、黄金持仓、铜持仓、总资产、浮动盈亏。

### 查看交易记录
```bash
python3 {baseDir}/scripts/portfolio.py --history
```

### 重置账户（回到初始状态）
```bash
python3 {baseDir}/scripts/portfolio.py --reset
```
将账户重置为初始状态：1亿元现金，无持仓。录制视频前使用。
