---
name: life-query
description: Query everyday life info — parcel tracking via Kuaidi100 for Chinese carriers (SF Express, ZTO, YTO, JD), real-time and historical currency exchange rates from ECB (30 currencies including CNY/USD/EUR/JPY), and gasoline/diesel prices for all 31 provinces in China from NDRC. Use when user asks "查快递", "track package", "物流查询", "包裹到哪了", "汇率", "exchange rate", "多少钱换", "美元人民币", "油价", "gas price", "今天92多少钱", "加油多少钱".
clawhub-slug: life-query
clawhub-owner: eamanc-lab
homepage: https://github.com/eamanc-lab/life-query
---

# Life Query — 日常生活查询助手

快递物流跟踪、实时汇率换算、全国油价查询。三合一日常信息查询工具。

## 使用场景

- 用户给了一个快递单号，想查物流到哪了
- 用户问"100美元换多少人民币"、"今天日元汇率"
- 用户问"今天油价多少"、"北京92号多少钱"
- 用户出差/旅行前想了解目的地油价或货币汇率
- 用户想对比一段时间内的汇率走势

## 前置条件

- **必需**：`curl`、`python3`（系统自带即可）
- **可选**：`pip install pyyaml`（run.sh 的 YAML 解析依赖，通常已安装）
- **可选**：自有快递100凭证（不配也能用，有默认免费额度）

## 决策流程

```
用户输入
  │
  ├─ 包含单号/快递/物流关键词 → courier-track
  │     └─ 没给单号？→ 追问用户要单号
  │
  ├─ 包含货币/汇率/换算关键词 → exchange-rate
  │     ├─ 明确了币种和金额 → 直接查询
  │     ├─ 只说了"汇率" → 默认 USD→CNY
  │     └─ 问"走势/趋势" → 用 startDate/endDate 查时间序列
  │
  ├─ 包含油价/加油/汽油关键词 → oil-price
  │     ├─ 提到了省份/城市 → --city 参数
  │     └─ 没提 → 默认全国
  │
  └─ 不确定 → 追问用户想查什么
```

## 可用接口

所有接口通过 `bash scripts/run.sh call <接口名> [参数...]` 统一调用。

| 接口 | 实现方式 | 说明 | 数据源 |
|------|---------|------|--------|
| courier-track | YAML + curl | 快递物流轨迹查询 | 快递100（经 fenxianglife.com 中转） |
| exchange-rate | Shell 脚本 | 实时/历史汇率，货币换算 | 欧洲央行 ECB（frankfurter.app） |
| oil-price | Shell 脚本 | 全国各省油价（92/95/柴油） | 东方财富/国家发改委 |

> **目录约定**：`apis/` 存放所有可调用接口，YAML 和 sh 是两种实现方式。`scripts/run.sh` 是统一调度引擎——先查 `apis/<name>.sh` 直接执行，未找到则解析 `apis/<name>.yaml` 构建 curl 请求。新增接口只需在 `apis/` 下添加文件。

## 使用方式

### 快递查询

```bash
# 查快递（自动识别快递公司）
bash scripts/run.sh call courier-track --trackingNumber SF1234567890

# 指定快递公司
bash scripts/run.sh call courier-track --trackingNumber SF1234567890 --carrierCode shunfeng
```

输出示例（JSON）：
```json
{
  "trackingNumber": "SF1234567890",
  "carrierName": "顺丰速运",
  "status": "已签收",
  "events": [
    {"time": "2026-03-18 14:30", "desc": "已签收，签收人：本人"},
    {"time": "2026-03-18 08:00", "desc": "派件中，快递员张三 138****1234"},
    {"time": "2026-03-17 22:00", "desc": "已到达 北京转运中心"}
  ]
}
```

### 汇率查询

```bash
# 100 人民币换算成美元、欧元、日元
bash scripts/run.sh call exchange-rate --from CNY --to USD,EUR,JPY --amount 100

# 查询某天的历史汇率
bash scripts/run.sh call exchange-rate --from USD --to CNY --date 2025-01-01

# 查询一段时间内的汇率走势
bash scripts/run.sh call exchange-rate --from USD --to CNY --startDate 2026-03-01 --endDate 2026-03-10

# 表格格式输出
bash scripts/run.sh call exchange-rate --from CNY --to USD,EUR,JPY --format table
```

常用货币代码：CNY（人民币）、USD（美元）、EUR（欧元）、JPY（日元）、GBP（英镑）、HKD（港币）、KRW（韩元）。完整列表约 30 种，详见 ECB 支持范围。

### 油价查询

```bash
# 查询全国所有省份最新油价
bash scripts/run.sh call oil-price

# 查询指定省份
bash scripts/run.sh call oil-price --city 北京

# 查询指定省份的历史油价（取最近5条）
bash scripts/run.sh call oil-price --city 北京 --pageSize 5

# 表格格式输出
bash scripts/run.sh call oil-price --format table
```

输出示例（table 格式）：
```
调价日期: 2026-03-04

省份     92号     95号     柴油    92涨跌   95涨跌
──────────────────────────────────────────────────
北京     7.78    8.28    7.45   +0.10   +0.11
上海     7.74    8.24    7.40   +0.10   +0.11
```

## 自然语言映射

| 用户说 | 接口 | 关键参数 |
|--------|------|---------|
| "帮我查一下 SF1234567890" | courier-track | trackingNumber=SF1234567890 |
| "这个单号的物流在哪里" | courier-track | trackingNumber=... |
| "100美元换多少人民币" | exchange-rate | from=USD, to=CNY, amount=100 |
| "今天美元汇率多少" | exchange-rate | from=USD, to=CNY |
| "最近一周日元走势" | exchange-rate | from=JPY, to=CNY, startDate/endDate |
| "今天油价多少" | oil-price | 默认全国 |
| "北京92号汽油多少钱" | oil-price | city=北京 |
| "广东最近几次油价调整" | oil-price | city=广东, pageSize=5 |

## 错误处理

| 故障点 | 分类 | 现象 | 处理方式 |
|--------|------|------|---------|
| 快递中转服务不可用 | B-API | curl 返回非 0 | 提示用户"快递服务暂时不可用，请稍后重试"；如果配置了自有 Key，提示检查凭证 |
| 单号不存在或格式错误 | C-运行时 | 返回空 data 或错误码 | 提示用户核实单号，建议检查位数和字母 |
| 快递公司识别失败 | C-运行时 | carrierName 为空 | 追问用户快递公司名称，用 --carrierCode 指定 |
| frankfurter.app 不可用 | B-API | curl 超时/失败 | 告知用户"汇率服务暂时不可用"，建议稍后重试 |
| 不支持的货币代码 | C-运行时 | 返回 404 或空 rates | 提示用户检查货币代码，给出常用代码列表 |
| 东方财富 API 反爬/限流 | B-API | 返回 success=False | 告知用户"油价数据暂时获取失败"，可稍后重试 |
| python3/pyyaml 未安装 | A-环境 | 命令不存在 | 提示用户安装：`pip install pyyaml` |

**铁律**：单个接口失败不影响其他接口。用户同时问了汇率和油价，一个挂了另一个照常查。

## 外部服务声明

本 skill 通过中转服务 `https://api.fenxianglife.com` 查询快递数据，该服务再调用快递100等数据源。你提供的快递单号会发送到该端点。

默认提供一定的免费查询额度，无需任何配置即可使用。如需更高额度，配置自有快递100凭证：

```bash
export KUAIDI100_KEY=你的授权Key
export KUAIDI100_CUSTOMER=你的Customer编码
```

配置后自动读取，也可通过命令行参数临时覆盖：

```bash
bash scripts/run.sh call courier-track --trackingNumber SF1234567890 \
  --kuaidi100Key YOUR_KEY --kuaidi100Customer YOUR_CUSTOMER
```

## 更新本 Skill

ClawHub 唯一标识：**slug `life-query`**（owner: `eamanc-lab`）

```bash
npx clawhub@latest update life-query
```

⚠️ ClawHub 上有多个物流/快递类 skill（如 logistics、package-track），与本 skill 无关。更新时必须使用精确 slug，禁止通过搜索替换。
