---
name: capture-alphapai-unified
description: "Alpha派默认投研技能 — 融合官方API（问答/RAG/Agent）和Web版（路演/点评/热门话题）。适合一般性投研问题、公司分析、行业研究等日常使用。如需大批量抓数据或获取完整列表，请改用 alphapai-web skill。"
when: "When user asks about company analysis, industry research, earnings review, investment logic, peer comparison, stock screening, fund selection, chart search, roadshow transcript, analyst comment, hot topics, or mentions AlphaPai/Alpha派/PaiPai. NOT for bulk data scraping — use alphapai-web instead."
examples:
  - "帮我分析贵州茅台的投资逻辑"
  - "比亚迪的可比公司有哪些"
  - "白酒行业一页纸"
  - "茅台最新的业绩点评"
  - "帮我选一些新能源相关的股票"
  - "挑战这个观点：小米汽车增长空间很大"
  - "搜索茅台的路演纪要"
  - "今天的财经热门话题"
  - "新能源车销量趋势图表"
metadata:
  version: 2.1
  openclaw:
    requires:
      bins: ["python3"]
    primaryEnv: "ALPHAPAI_API_KEY"
    emoji: "📊"
    install:
      - id: "setup"
        kind: "bash"
        label: "Setup dependencies"
        script: "bash {skillDir}/scripts/setup.sh"
---

# AlphaPai Unified — 默认投研技能

融合**官方API**（问答/RAG/Agent）和**Web版**（路演/点评/热门话题），适合日常投研使用。

> **选择指南：** 一般性问题 → 用本 skill（默认）；大批量抓数据/获取列表 → 用 `alphapai-web`。

## 功能矩阵

| 功能 | 数据源 | 命令 |
|------|--------|------|
| 投研问答 | 官方API | `qa` |
| 数据召回(RAG) | 官方API | `recall` |
| 公司一页纸 | 官方API | `company` |
| 业绩点评 | 官方API | `earnings` |
| 投资逻辑 | 官方API | `logic` |
| 可比公司 | 官方API | `peers` |
| 行业一页纸 | 官方API | `industry` |
| 主题选股 | 官方API | `screen` |
| 观点Challenge | 官方API | `challenge` |
| 公告列表 | 官方API | `report` |
| 图表搜索 | 官方API | `chart` |
| 路演纪要 | Web版 | `roadshow` |
| 点评 | Web版 | `comment` |
| 热门话题 | Web版 | `hot` |
| 热词 | Web版 | `hot-word` |
| 热门报告 | Web版 | `hot-report` |
| 热门股票 | Web版 | `hot-stock` |
| 综合搜索 | Web版 | `search` |
| 用户信息 | Web版 | `user-info` |

## 认证配置

**优先级：**
1. 环境变量 `ALPHAPAI_API_KEY`（推荐）
2. 同级/上级/上上级目录 `.env`
3. `config.json`

**API Key（官方API）：**
```bash
export ALPHAPAI_API_KEY=your_key_here
# 或
python scripts/alphapai.py config --set-key YOUR_KEY
```

**账号密码（Web版）：**
```bash
export ALPHAPAI_ACCOUNT=手机号
export ALPHAPAI_PASSWORD=密码
# 或
python scripts/alphapai.py config --set-account 手机号 --set-password 密码
```

> API Key 可在 Alpha 派电脑端获取。账号密码用于 Web 版独有功能（路演、点评、热门话题）。

---

## 官方API命令

### 投研问答

```bash
python scripts/alphapai.py qa "茅台2024经营情况"
python scripts/alphapai.py qa "新能源趋势" --think      # Think模式（Wide Search）
python scripts/alphapai.py qa "近期新闻" --web-search   # 联网搜索
```

### 数据召回

```bash
python scripts/alphapai.py recall "茅台市值" --type comment,report
python scripts/alphapai.py recall "新能源" --no-cutoff   # 完整内容
```

**数据类型：** `comment`(点评) / `report`(研报) / `roadShow`(路演) / `ann`(公告) / `qa`(问答) / `edb`(时序数据)

### 快捷命令

```bash
# 公司一页纸
python scripts/alphapai.py company 300014.SZ:亿纬锂能

# 业绩点评（自动查询最新公告）
python scripts/alphapai.py earnings 603380.SH:易德龙

# 投资逻辑
python scripts/alphapai.py logic 300014.SZ:亿纬锂能

# 可比公司
python scripts/alphapai.py peers 002594.SZ:比亚迪

# 行业一页纸
python scripts/alphapai.py industry 白酒

# 主题选股
python scripts/alphapai.py screen "和白酒相关的公司"

# 观点Challenge
python scripts/alphapai.py challenge "小米汽车未来增长空间很大"
```

### 公告/图表

```bash
# 公告列表
python scripts/alphapai.py report 603380.SH

# 图表搜索
python scripts/alphapai.py chart "新能源车销量趋势"
```

---

## Web版命令

### 路演纪要

```bash
# 列表
python scripts/alphapai.py roadshow --list

# 搜索
python scripts/alphapai.py roadshow --search "茅台业绩会"

# 详情（含AI摘要）
python scripts/alphapai.py roadshow --detail <纪要ID>
```

### 点评

```bash
# 推荐列表
python scripts/alphapai.py comment --list

# 搜索
python scripts/alphapai.py comment --search "茅台"

# 详情（含盈利预测）
python scripts/alphapai.py comment --detail <点评ID>
```

### 热门话题 / 热门报告 / 热门股票

```bash
# 热门话题列表
python scripts/alphapai.py hot

# 话题详情
python scripts/alphapai.py hot --detail <话题ID>

# 热词
python scripts/alphapai.py hot-word

# 热门报告
python scripts/alphapai.py hot-report

# 热门股票（公募/私募/险资持仓）
python scripts/alphapai.py hot-stock
```

### 综合搜索 / 用户信息

```bash
# 综合搜索（路演+公众号+股票一次全返回）
python scripts/alphapai.py search "贵州茅台"

# 用户信息
python scripts/alphapai.py user-info
```

---

## 输出原则

Alpha派返回内容由专业投研模型生成，**直接呈现原始输出，不做二次加工**：
- 禁止总结或压缩
- 禁止截断
- 保留原始 Markdown 格式
- 引用来源随正文输出

---

## 文件结构

```
capture-alphapai-unified/
├── SKILL.md
├── scripts/
│   ├── alphapai.py              # 统一入口CLI
│   ├── alphapai_client.py       # 官方API客户端
│   ├── alphapai_web_client.py   # Web版客户端
│   └── setup.sh
├── references/
│   ├── api_reference.md         # 官方API参考
│   ├── web_api_reference.md     # Web版API参考
│   └── agent_modes.md           # Agent模式详解
└── .env.example
```

---

## 参考文件

| 文件 | 内容 |
|------|------|
| [`references/api_reference.md`](references/api_reference.md) | 官方API完整字段定义 |
| [`references/web_api_reference.md`](references/web_api_reference.md) | Web版API参考 |
| [`references/agent_modes.md`](references/agent_modes.md) | 11种Agent模式详解 |

---

## 升级

当用户要求升级时，拉取官方安装指引并按流程执行。