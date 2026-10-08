---
name: stock-trading
description: A股股票实时行情查询与模拟交易，使用真实沪深行情数据
version: 1.0.0
---

# A股智能交易技能

连接新浪财经实时行情接口，提供A股股票的实时价格查询、模拟买卖和持仓管理。
行情数据为沪深交易所真实数据，交易为模拟盘，不涉及真实账户和资金。

## 可用命令

### 查询股票实时价格
```bash
python3 {baseDir}/scripts/get_price.py --code 600519
```
支持沪深两市股票代码。示例：600519（贵州茅台）、000858（五粮液）、300750（宁德时代）
返回：股票名称、最新价、涨跌幅、成交量、买卖五档等（JSON格式）

### 批量查询多只股票
```bash
python3 {baseDir}/scripts/get_price.py --code 600519,000858,000001
```
用逗号分隔多个股票代码，一次查询多只。

### 查询大盘指数
```bash
python3 {baseDir}/scripts/get_price.py --index sh000001
```
支持：sh000001（上证指数）、sz399001（深证成指）、sz399006（创业板指）

### 买入股票
```bash
python3 {baseDir}/scripts/trade.py --action buy --code 600519 --shares 100
```
买入指定股数的股票。shares 必须为100的整数倍（A股最小交易单位为1手=100股）。
⚠️ 重要：调用前必须先告知用户交易计划并等待确认。

### 卖出股票
```bash
python3 {baseDir}/scripts/trade.py --action sell --code 600519 --shares 100
```

### 查看持仓和损益
```bash
python3 {baseDir}/scripts/portfolio.py
```

### 查看交易记录
```bash
python3 {baseDir}/scripts/portfolio.py --history
```

### 重置账户
```bash
python3 {baseDir}/scripts/portfolio.py --reset
```
重置为初始状态：100万元现金，无持仓。录制视频前使用。
