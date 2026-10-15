---
name: crayfish-grid-hunter
description: 币安 USDS-M 合约网格猎手。双分类筛选（次新币横盘+高波动套利）→ 等比中性网格。所有数据来自币安官方 API 实时获取，严禁 AI 自行生成任何数值。触发词：次新币网格、高波动套利、网格猎手。
version: 1.0.0
author: joensmoon
homepage: https://github.com/joensmoon/Crayfish-Grid-Hunter
metadata: {"openclaw":{"emoji":"🦞","requires":{"bins":["python3"]},"install":[{"id":"pip-deps","kind":"download","url":"https://raw.githubusercontent.com/joensmoon/Crayfish-Grid-Hunter/main/install.sh","label":"Install Python dependencies (requests, tabulate)"}]}}
---

# Crayfish Grid Hunter v1.0.0

币安 USDS-M 永续合约智能网格交易助手。

---

## 安装后使用指南

安装完成后，您可以立即在 OpenClaw 对话框中使用以下触发指令：

| 触发指令 | 功能说明 | 适用场景 |
| :--- | :--- | :--- |
| `次新币网格` | 扫描上线 ≤90 天、市值 $10M-$200M 的次新币横盘机会 | 低风险稳健网格 |
| `高波动套利` | 扫描 48h 涨跌幅 >10%、换手率极高的热点币种 | 高收益激进套利 |
| `网格猎手` | 同时运行两类扫描，汇总最优结果 | 综合扫描 |

您还可以通过自然语言直接调整参数，例如：

- *"次新币网格，杠杆 3 倍，市值上限 1 亿"*
- *"高波动套利，筛选前 5 名，止损设为 3%"*
- *"网格猎手，上线天数改为 60 天，涨跌幅要 15% 以上"*

### 官方 Skill 依赖

本 Skill 依赖以下币安官方 Skills（安装脚本会自动安装）：

| 依赖 Skill | 来源 | 用途 |
| :--- | :--- | :--- |
| `derivatives-trading-usds-futures` | binance/binance-skills-hub | 合约列表、K线数据、资金费率、标记价格 |
| `query-token-info` | binance-web3/query-token-info | 代币市值、24h 交易量、换手率数据 |

> **注意**：以上依赖均为币安官方发布的 Skills，本项目未对其做任何修改。如果安装脚本未自动安装依赖，请手动执行：
> ```bash
> npx skills add binance/derivatives-trading-usds-futures -a openclaw -y
> npx skills add binance-web3/query-token-info -a openclaw -y
> ```

---

## CRITICAL: 执行规则（最高优先级，必须遵守）

**你是 AI Agent。当用户触发此 Skill 时，你必须立即执行以下操作，不得有任何偏差：**

### 第一步：立即执行 Python 脚本

根据用户意图，选择并执行对应命令：

| 用户意图 | 执行命令 |
| :--- | :--- |
| 次新币网格 / Category A | `python3 {baseDir}/grid_hunter_v5.py --mode cat-a --no-backtest` |
| 高波动套利 / Category B | `python3 {baseDir}/grid_hunter_v5.py --mode cat-b --no-backtest` |
| 全量扫描 / 网格猎手 | `python3 {baseDir}/grid_hunter_v5.py --no-backtest` |
| 带回测 | `python3 {baseDir}/grid_hunter_v5.py` |

**执行方式**：使用系统 bash/exec 工具运行上述命令，等待输出完成。

### 第二步：原样展示脚本输出

将脚本的**完整标准输出**原样展示给用户，包括：
- 扫描摘要（分析了多少合约、发现多少机会）
- Category A / Category B 筛选结果表格
- 每个标的的等比网格详情（Lower/Upper/格数/单格利润/强平价/止损位）
- 参数优化建议（如有）
- **末尾的签名行**（格式：`⚠ 有效输出必含签名: CRAYFISH-XXXXXXXXXXXX | 生成时间: YYYY-MM-DD HH:MM:SS`）

**不得对数值做任何修改、四舍五入或替换。**

> 验证方法：真实脚本输出的末尾必含 `CRAYFISH-` 签名。若用户看到的结果没有此签名，说明 AI 没有执行脚本，结果无效。

### 禁止事项（违反将导致用户损失真实资金）

你**绝对不能**做以下任何事：

- ❌ **禁止**凭空生成代币名称（如 ALPACAUSDT、OPUSDT 等）
- ❌ **禁止**自行计算或估算价格区间（如"$0.95 - $1.43"）
- ❌ **禁止**输出"支撑位"、"阻力位"、"推荐配置"等未经脚本计算的内容
- ❌ **禁止**输出"跨交易所套利"、"三角套利"、"期现套利"等本工具不支持的策略
- ❌ **禁止**在脚本执行失败时用自己的知识替代输出
- ❌ **禁止**修改脚本输出的任何数值

### 用户自定义参数转换

| 用户说的话 | 对应 CLI 参数 |
| :--- | :--- |
| "合约上线天数改为120天" | `--contract-recent-days 120` |
| "次新币市値最低500万" | `--cat-a-mcap-min 5000000` |
| "次新币市値上限改为5亿" | `--cat-a-mcap-max 500000000` |
| "杠杆倍数改为3" | `--leverage 3` |
| "高波动套利市値范围改为2亿-10亿" | `--mcap-min 200000000 --mcap-max 1000000000` |
| "48h涨跌幅改为20%" | `--high-vol-48h-min-pct 20` |
| "换手率30%以上" | `--turnover-min 0.30` |
| "止损3%" | `--stop-loss-pct 3.0` |
| "只看前5个结果" | `--top-n 5` |
| "单格利润最低1.5%" | `--min-grid-profit 0.015` |
| "扫描前100个币种" | `--max-symbols 100` |
| "年化波动率最低20%" | `--rv-min 20` |

### 脚本执行失败时的处理

若脚本执行失败（网络超时、API 限流等）：
1. 告知用户具体错误信息
2. 建议检查网络连接（币安 API 需要可访问）
3. 提示参考 `{baseDir}/docs/TROUBLESHOOTING.md`
4. **不得**用自己的知识替代脚本输出

---

## 核心能力说明

### 次新币定义（Category A）

> **次新币 = 在币安 USDS-M 永续合约市场上线不超过 90 天的合约。**

- 数据来源：`fapi/v1/exchangeInfo`（币安官方接口）
- 筛选条件：`status=TRADING`、`contractType=PERPETUAL`、`quoteAsset=USDT`
- **已下架合约（status≠TRADING）自动排除**，不会出现在结果中
- `onboardDate` 字段精确到毫秒，计算公式：`(now_ms - onboardDate_ms) / 86400000`

### 高波动套利（Category B）

- 24h 涨跌幅绝对值 > 10%
- 市值 $2亿 - $10亿（防止极小市值操纵）
- 代币必须在 `fapi/v1/exchangeInfo` 白名单中（严格精确匹配，无 fallback）

---

## 安装

```bash
# 一键安装（推荐，自动安装所有依赖）
curl -s https://raw.githubusercontent.com/joensmoon/Crayfish-Grid-Hunter/main/install.sh | bash

# 手动安装
git clone https://github.com/joensmoon/Crayfish-Grid-Hunter.git ~/.openclaw/skills/crayfish-grid-hunter-repo
pip3 install requests tabulate
npx skills add binance/derivatives-trading-usds-futures -a openclaw -y
npx skills add binance-web3/query-token-info -a openclaw -y
```

