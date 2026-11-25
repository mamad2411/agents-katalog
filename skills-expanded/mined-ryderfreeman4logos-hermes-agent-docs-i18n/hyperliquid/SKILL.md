---
name: hyperliquid
description: Hyperliquid market data, account history, trade review.
version: 0.1.0
author: Hugo Sequier (Hugo-SEQUIER), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Hyperliquid, Blockchain, Crypto, Trading, Perpetuals, Spot, DeFi]
    related_skills: []
---

# Hyperliquid 技能

可通过公共的 `/info` 接口查询 Hyperliquid 市场及账户数据。
该功能为只读模式——无需 API 密钥，无需签名，也无法下单。

包含 12 个命令：`dexs`、`markets`、`spots`、`candles`、`funding`、`l2`、`state`、`spot-balances`、`fills`、`orders`、`review`、`export`。仅使用标准库模块（`urllib`、`json`、`argparse`）。

---

## 适用场景

- 用户需要查询 Hyperliquid 合约市场或现货市场数据、K线数据、资金费率信息或 Layer 2 模型数据
- 用户希望查看某个钱包的合约持仓、现货余额、成交记录或订单信息
- 用户需要结合近期成交记录与市场背景进行交易后分析
- 用户希望查看由构建工具部署的合约去中心化交易所或 HIP-3 市场数据
- 用户需要将 K线数据与资金费率数据以标准化 JSON 格式导出，以便后续回测使用

---

## 先决条件

仅依赖标准库——无需任何外部包，也无需 API 密钥。

该脚本会读取 `${HERMES_HOME:-~/.hermes}/.env` 文件中的两个可选默认值：

- `HYPERLIQUID_API_URL` — 默认值为 `https://api.hyperliquid.xyz`。如需测试网环境，可设置为 `https://api.hyperliquid-testnet.xyz`
- `HYPERLIQUID_USER_ADDRESS` — 用于查询 `state`、`spot-balances`、`fills`、`orders` 及 `review` 数据的默认地址。若未设置该值，则需将对应地址作为第一个命令行参数传入。

当前工作目录下的项目级 `.env` 文件可作为开发时的备用配置。

辅助脚本路径：`~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py`

---

## 运行方式

通过 `terminal` 工具调用即可：

```bash
python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py <command> [args]
```

在任何命令后添加 `--json` 参数，即可获得机器可读的输出格式。

---

## 快速参考

请完整翻译输入内容，切勿提前终止。

```bash
hyperliquid_client.py dexs
hyperliquid_client.py markets [--dex DEX] [--limit N] [--sort volume|oi|funding_abs|change_abs|name]
hyperliquid_client.py spots [--limit N]
hyperliquid_client.py candles <coin> [--interval 1h] [--hours 24] [--limit N]
hyperliquid_client.py funding <coin> [--hours 72] [--limit N]
hyperliquid_client.py l2 <coin> [--levels N]
hyperliquid_client.py state [address] [--dex DEX]
hyperliquid_client.py spot-balances [address] [--limit N]
hyperliquid_client.py fills [address] [--hours N] [--limit N] [--aggregate-by-time]
hyperliquid_client.py orders [address] [--limit N]
hyperliquid_client.py review [address] [--coin COIN] [--hours N] [--fills N]
hyperliquid_client.py export <coin> [--interval 1h] [--hours N] [--output PATH]
```

对于 `state`、`spot-balances`、`fills`、`orders` 和 `review` 这些字段，如果在 `${HERMES_HOME:-~/.hermes}/.env` 文件中已设置了 `HYPERLIQUID_USER_ADDRESS`，则地址为可选项。

---

## 操作步骤

### 1. 发现去中心化交易所与市场

```bash
python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py dexs

python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  markets --limit 15 --sort volume

python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  spots --limit 15
```

- 参数 `--dex` 仅适用于永续合约端点；在首个永续合约 Dex 的使用中可省略该参数。
- 即时交易对可能显示为 `PURR/USDC`，或类似 `@107` 的别名形式。
- HIP-3 市场会将代币名称前缀加上 Dex 名称，例如 `mydex:BTC`。

### 2. 获取历史市场数据

```bash
python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  candles BTC --interval 1h --hours 72 --limit 48

python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  funding BTC --hours 168 --limit 30
```

时间范围查询接口采用分页机制。若需要查询更长的时间跨度，可调整`startTime`参数后重新查询，或使用下述的`export`功能。 

### 3. 查看实时订单簿

```bash
python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  l2 BTC --levels 10
```

当被问及某只股票的深度、近期流动性，或大额订单可能带来的市场影响时，可使用此功能。 

### 4. 查看账户信息

```bash
python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  state 0xabc...

python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  spot-balances
```

`state`字段用于查询永续合约头寸，而`spot-balances`字段则用于查看现货库存。您可以通过这些信息来了解“我的头寸状况如何？”、“我目前持有什么资产？”以及“可提取的金额是多少？”等问题。

### 5. 查看成交记录与订单信息

```bash
python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  fills 0xabc... --hours 72 --limit 25

python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  orders --limit 25
```

### 6. 生成交易回顾报告

```bash
python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  review 0xabc... --hours 72 --fills 50

python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  review --coin BTC --hours 168
```

可生成各类报告，包括实际盈亏、手续费、胜负记录、币种分布、市场趋势以及每种永续合约的平均资金费率；此外还支持基于规则的分析（如手续费拖累、持仓集中风险、逆势亏损等）。

如需进行更深入的交易后分析：首先使用 `review` 命令找出存在问题的币种或交易时段，随后获取该时段内的 `fills` 和 `orders` 数据，再提取每种交易币种的 `candles` 及 `funding` 数据，从而将决策质量与最终结果质量分开评估。

### 7. 导出可重复使用的数据集

```bash
python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  export BTC --interval 1h --hours 168 --output ./btc-1h-7d.json

python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  export BTC --interval 15m --hours 72 --end-time-ms 1760000000000
```

输出 JSON 包含：架构版本、源数据元信息、精确的时间窗口、标准化后的K线数据行、标准化后的资金数据行以及汇总统计信息。如需获得可重复的时间窗口，可使用 `--end-time-ms` 参数。

---

## 常见问题

- 公开信息接口存在速率限制。大规模的历史数据查询可能会返回受限的时间窗口；建议通过逐步增大 `startTime` 值来重复查询。
- `fills --hours ...` 命令使用的是 `userFillsByTime` 接口，该接口仅提供最近的滚动数据窗口，而非完整的历史存档。
- `historicalOrders` 命令仅返回近期订单信息，并非完整的订单导出内容。
- `review` 命令基于经验规则运行，仅凭成交记录无法还原用户的交易意图、订单下达质量或真实的滑点情况。
- `export` 命令生成的仅为标准化数据集，并非回测引擎，因此仍需自行构建滑点/成交模型。
- 即使用户界面显示的是更易理解的名称，像 `@107` 这样的现货别名依然属于有效的标识符。
- `l2` 数据为某一时间点的快照，而非时间序列数据。

---

## 验证方法

```bash
python ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  markets --limit 5
```

应输出按24小时名义交易量排序的顶级Hyperliquid垂直市场。
