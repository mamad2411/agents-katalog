# Portfolio OCR Skill

> 把"持仓页截图（理财通 / 支付宝 / 银行 App / 券商 App 等）"识别成 EE_AI_Fund_Management 可直接导入的 JSON 文件。
>
> 你可以把这份 Skill 喂给任何**支持图片输入的多模态对话模型**（Kimi 网页版 / 通义千问 / 豆包 / GPT-4V / Claude / 本地 Qwen-VL / GLM-4V 等），让它生成一份标准 JSON 文件，再到 App 里点"导入 JSON"完成入库。

---

## 一、使用方式（给人类看）

### A. 在网页 ChatBot 里手工跑（最常见）

1. 打开任意支持多图上传的对话模型网页（推荐 **Kimi**、**通义千问**、**ChatGPT-4V**、**Claude**、本地部署的 OpenWebUI/LobeChat 等）
2. 把本文件里 [§ 三、System Prompt（可直接复制）](#三system-prompt可直接复制) 整段贴进对话框，作为第一条消息
3. **拖入一张或多张持仓页截图**（同一次对话里可以连续上传多次，每次都会输出一份 JSON）
4. 对话模型应当只返回**一个合法的 JSON 对象**，没有任何说明文字 / 不带 ```` ```json ```` 围栏
5. 把模型输出复制保存为 `portfolio.json`（或随便起名）
6. 打开 App → 「OCR 批量导入」页 → 点击 **「导入 JSON 文件」** → 选择刚才保存的 json
7. 走标准的对账确认流程，确认无误后点击「确认导入」

> **多张图怎么办？** 两种都行：
> - **方式 A（推荐）**：让模型把多张图合并成一份 JSON，`items` 里把所有持仓项铺平 —— 操作最省事
> - **方式 B**：每张图单独一份 JSON，分别保存成 `portfolio_1.json`、`portfolio_2.json`... App 的"导入 JSON"按钮支持一次选多个文件

### B. 在 CodeBuddy / Claude Skills 里作为 Skill 使用

把整个 `skills/portfolio-ocr/` 目录拷到你的 Skills 根目录，加载本 Skill 后直接说「帮我识别这张持仓截图」并附图，模型会按本文档约定输出。

---

## 二、产物 Schema

模型必须输出**恰好一个 JSON 对象**，外层结构如下：

```jsonc
{
  // 可选：标记这是 Skill 产物（便于 App 校验）。没有也行。
  "schema": "ee-fund-mgr/portfolio-ocr@1",

  // 可选：识别到的平台名；未识别就填 "未知"
  "platform": "微信理财通",

  // 可选：截图日期（如截图右上角时间），看不出就填 null
  "screenshot_date": "2026-05-08",

  // 必填：持仓项数组。可以为空数组（识别到不是持仓页时）
  "items": [
    {
      "name": "兴全合宜",                  // 必填，完整产品名
      "code": "163406",                    // 6 位基金代码 / 股票代码 / 没显示填 null
      "asset_type": "fund",                // 必填，见下文枚举
      "shares": 1234.5678,                 // 份额/股数；货基/理财/现金可填 null
      "amount": null,                      // 持有金额（元），货基/理财/现金必填
      "avg_cost": 1.234,                   // 平均成本/持仓单价
      "current_price": 1.345,              // 最新价/净值
      "market_value": 12345.67,            // 当前市值（元）
      "profit": 123.45,                    // 累计收益（元），亏损为负
      "profit_pct": 1.23,                  // 收益率（%）数字
      "yield_7d": null,                    // 货基 7 日年化(%)
      "expected_apr": null,                // 理财预期年化(%)
      "maturity_date": null                // 到期日 "YYYY-MM-DD"
    }
  ]
}
```

### `asset_type` 枚举（必须严格用这 7 个值）

| 值 | 中文 | 典型例子 |
|---|---|---|
| `fund` | 普通公募基金 | 兴全合宜、易方达蓝筹 |
| `stock` | 股票 | 贵州茅台、腾讯控股 |
| `etf` | ETF / LOF / 场内基金 | 沪深300ETF、中概互联ETF |
| `money_fund` | 货币基金类 | 余额宝、朝朝宝、零钱通、添益宝 |
| `wealth` | 理财产品（净值型/定期/结构性/大额存单） | XX天/XX个月/招银私行 XX |
| `cash` | 现金类 | 活期、活期+、活钱、现金宝 |
| `bond` | 国债 / 企业债 / 地方债 | 国债 220015 |

### 数值字段规则

- **裸数字**，不要带 `元` / `¥` / `%` / `约` 等单位
- 看不清就填 `null`，**不要瞎猜**
- 亏损用负数（`profit: -123.45`）
- `profit_pct` 是数字 **1.23 表示 1.23%**，不要写成 0.0123

---

## 三、System Prompt（可直接复制）

> 复制下面整段（包括三道 `---`）粘贴给多模态对话模型，作为第一条 system / user 消息。

```text
你是一个个人理财截图识别助手。用户会上传"持仓页"截图（理财通/支付宝/银行 App/券商 App 等）。

任务：识别图中所有持仓项，输出**纯 JSON**（必须可被 JSON.parse 解析，不要任何解释、不要 ```json``` 围栏）。

Schema：
{
  "schema": "ee-fund-mgr/portfolio-ocr@2",
  "platform": "<识别到的平台名，未识别填'未知'>",
  "screenshot_date": "YYYY-MM-DD" 或 null,
  "items": [{
    "name": "<完整产品名>",
    "code": "<6 位基金代码 / 股票代码，没显示填 null>",
    "asset_type": "fund" | "stock" | "etf" | "money_fund" | "wealth" | "cash" | "bond",
    "market": "A" | "HK" | "US" | "OTC" | "CNY" | "USD" | "HKD",
    "exchange": "SH" | "SZ" | "BJ" | "HK" | "NYSE" | "NASDAQ" | "AMEX" | "OTC" | "CNY" | "USD" | "HKD" | "UNKNOWN",
    "shares": <份额/股数，货基/理财/现金可填 null>,

    "amount": <持有金额（元），货基/理财/现金必填>,
    "avg_cost": <平均成本/持仓单价>,
    "current_price": <最新价/净值>,
    "market_value": <当前市值（元）>,
    "profit": <累计收益（元），亏损填负数>,
    "profit_pct": <收益率（%）数字>,
    "yield_7d": <货基7日年化(%)>,
    "expected_apr": <理财预期年化(%)>,
    "maturity_date": "YYYY-MM-DD" 或 null
  }]
}

类型判定：
- 余额宝/朝朝宝/朝朝盈/零钱通/添益宝/余利宝 → money_fund
- 活期/活期+/活钱/现金宝 → cash
- XX天/XX个月/定期/净值型/结构性/大额存单 → wealth；国债且有代码 → bond
- ETF/LOF/场内基金 → etf；普通公募基金 → fund；个股 → stock

约束：
1. 数值字段必须是裸数字，不带"元"/"%"/"约"等；看不清就填 null（不要瞎猜）。
2. 一张图 5-15 项要全部列出。
3. 不是持仓页（首页/广告/聊天）→ {"schema":"ee-fund-mgr/portfolio-ocr@2","platform":"未知","items":[]}。

4. 多张图：把所有持仓项合并到同一份 JSON 的 items 数组里。
5. 只输出一个 JSON 对象，不要任何前后说明文字、不要 markdown 代码块围栏。
```

---

## 四、完整示例

### 输入
用户上传了一张微信理财通持仓页截图（5 个持仓项：1 个货基朝朝宝、2 个基金、1 个股票、1 个理财）

### 期望输出（严格按此格式）
见同目录 [`example_output.json`](./example_output.json)。

---

## 五、校验你的 JSON 是否合法

提交到 App 前，可以用同目录的 `validate.py` 自检：

```bash
python skills/portfolio-ocr/validate.py path/to/your.json
```

通过会输出 `✓ JSON 合法，共识别到 N 项持仓`，否则会指出哪个字段不合规。

---

## 六、与 App 内置 OCR 的关系

App 内置的 OCR（「OCR 批量导入」页直接传图）和这个 Skill **共用同一份 prompt 和 schema**，区别只是：

| 维度 | 内置 OCR | Skill + 导入 JSON |
|---|---|---|
| 视觉模型 | 走 App 设置里的 vision 配置 | 你想用啥就用啥（网页 ChatBot / 本地模型 / Claude...） |
| 速度 | 受限于配置的模型 | 想用最快的网页 ChatBot 就行 |
| 隐私 | 截图发给你配置的模型 | 截图发给你选的模型 |
| 限流 | 受 vision 模型 RPM/TPM 限制 | 网页 ChatBot 一般无 RPM 限制 |
| 复杂度 | 一键 | 两步：先生成 JSON，再导入 |

适用场景：

- **截图量大 / 视觉模型限流严重** → 用 Skill 在网页 ChatBot 里手动跑
- **想验证识别质量 / 调试 prompt** → 用 Skill 跑完看看 JSON 再决定
- **图片含敏感信息，只想发给特定模型** → 用 Skill 自己控制送给谁
- **日常少量截图** → 直接用内置 OCR 最方便
