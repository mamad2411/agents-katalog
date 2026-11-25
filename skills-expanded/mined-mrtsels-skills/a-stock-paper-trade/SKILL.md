---
name: a-stock-paper-trade
description: A股模拟炒股系统。实时行情、买卖下单、持仓管理、盈亏计算、涨跌排行。基于 akshare + 新浪财经实时行情，纯本地模拟，无需外部账号。
---

# A股模拟炒股 — Stock Paper Trade

本地纸面交易系统，基于 akshare 和新浪财经实时行情。无需任何外部账号，纯模拟。

## 脚本路径

`{baseDir}/scripts/trader.py`

## 快速开始

```bash
# 初始化账户（5万虚拟资金）
python3 scripts/trader.py init

# 查大盘
python3 scripts/trader.py quote --all

# 查个股行情
python3 scripts/trader.py quote 600519 000001

# 搜索股票
python3 scripts/trader.py search 茅台

# 买入（1手=100股，市价）
python3 scripts/trader.py buy 600519 1

# 买入（指定价格）
python3 scripts/trader.py buy 600519 2 --price 1700

# 卖出
python3 scripts/trader.py sell 600519 1

# 查持仓
python3 scripts/trader.py positions

# 账户总览
python3 scripts/trader.py balance

# 交易记录
python3 scripts/trader.py history --limit 10

# K线
python3 scripts/trader.py kline 600519 --days 60

# 涨幅TOP10
python3 scripts/trader.py rank --top 10

# 跌幅TOP10
python3 scripts/trader.py rank --bottom --top 10
```

## 交易规则

- 最小单位：1手 = 100股
- 佣金：万三（最低5元）
- 印花税：千一（仅卖出）
- 不支持涨跌停价格下单（当前版本未强制校验，agent 应自行判断）
- 数据来源：东方财富/新浪财经，仅交易时间内有效

## 费用计算

| 费用 | 买入 | 卖出 |
|------|------|------|
| 佣金 | 万三（最低5元） | 万三（最低5元） |
| 印花税 | — | 千一 |
| 过户费 | — | 忽略（模拟简化） |

## 数据存储

- 位置：`~/.openclaw/paper-trade/portfolio.json`
- 重置：`python3 scripts/trader.py init --reset`

## 注意

- 行情数据来自 akshare（东方财富）和新浪财经。`quote --all`、`rank`、`search`、`kline` 依赖 akshare→东方财富 API；`quote <代码>`、`buy`、`sell` 使用新浪 HTTP API
- 非 A 股交易时间行情不可用（实时价=0，只有昨收）
- 所有操作输出 JSON，方便解析

## 常见问题

### ETF/科创板/Reits 代码映射

**现象：** `quote 588000` 返回 `"未找到该股票"`，但新浪行情实际有该 ETF 数据。

**原因：** `_sina_code()` 中 5xxx 代码（如 588000 科创50ETF）未正确映射到 `sh` 前缀，被默认赋为 `sz` 导致查询失败。

**解决：** 已在 `_sina_code()` 中添加 `elif code.startswith("5"): return f"sh{code}"`。完整映射：6→sh, 0/3→sz, 5→sh, 8/4→bj。

### 代理阻断 — akshare 连不上东方财富

**现象：** `quote --all` / `rank` / `search` 报 `ProxyError`（如 `Caused by ProxyError('Unable to connect to proxy')`），但 `quote 600519` 等个股查询正常。

**原因：** akshare 内部使用 `requests` 请求东方财富 API，走系统代理（`http_proxy`/`https_proxy`）时被阻断。而脚本中的个股行情函数（`_get_realtime_quote`）直接调用新浪 HTTP API，不受此限。

**解决方案（按优先级）：**

1. **如果不需批量查询**：直接用 `quote <代码 1> <代码 2>`（走新浪 API，过代理正常）
2. **如果需 rank/search/kline**：临时取消代理执行
   ```bash
   http_proxy= https_proxy= python3 scripts/trader.py rank --top 10
   ```
3. **切换到 thsdk（同花顺）**：`from thsdk import THS`，thsdk 不走东方财富，不受此代理限制

### Python 版本路径不一致

**现象：** `pip show akshare` 显示已安装，但 `python3 -c "import akshare"` 报 `ModuleNotFoundError`。

**原因：** `pip` 指向 venv（如 `/Users/minimx/.agent-reach-venv/bin/pip`），而 `python3` 指向系统 Python。两者互相独立。

**解决方案：**
```bash
# 方法1：用 venv 的 Python 运行
/Users/minimx/.agent-reach-venv/bin/python scripts/trader.py quote 600519

# 方法2：检查当前 pip 对应的 Python
python3 -m pip show akshare  # 看是不是同一个 pip/python
```

## 依赖安装

```bash
pip install akshare requests
```

> ⚠️ 如果 `pip` 和 `python3` 是不同环境，需用同一 Python 的 `pip` 安装：`python3 -m pip install akshare requests`
