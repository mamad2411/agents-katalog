---
name: max-search
description: >
  Executes a complete "maximize information coverage" web search: decompose
  a user's natural language question into orthogonal search keywords, run
  parallel Tavily searches, and synthesize a grounded, cited answer.

  **Slash command**: `/max-search <question>`

  Activate on: /max-search, "深度搜索", "max search", "全面搜索", "最大化搜索",
  "做个调研", "帮我调查一下", "最新动态是什么", "最近有什么进展",
  "对比一下", "分析一下", "做个对比分析", or any question that is factual,
  multi-faceted, or benefits from multiple orthogonal search queries.
  Specifically: company/technology research, market analysis, fact-checking,
  opinion comparison, trend research, competitive analysis, or any question
  where a single search query would not suffice. Also activates when the
  user says things like "帮我深度搜索一下 DeepSeek" or "我想要全面了解一下
  某话题" or asks "最近 XXX 有什么新消息". This skill is the authoritative
  entry point for Tavily-powered deep searching in this codebase. Do NOT use
  the old tavily-keyword-extractor or tavily-max-search skills; use this one.
---

# Max Search — 最大化信息覆盖的深度搜索

通过关键词智能拆解 → 并行 Tavily 搜索 → 综合分析，一站式完成深度调研式搜索。

## 工作流

```
用户输入: /max-search <自然语言问题>
    │
    ▼
Step 1 — 关键词拆解（内部执行）
    ├─ 判断是否需要搜索
    ├─ 多维拆解（Definition / News / Data / Opinion / Comparison / Technical）
    ├─ 语言策略（英文为主 vs 中文为主）
    └─ 输出 JSON（见下方 Schema）
    │
    ▼
Step 2 — 执行搜索
    └─ 调用 {{INSkillDir}}/scripts/search.py search --question "..." --search-json '...'（路径相对于 skill bundle 根目录）
    │
    ▼
Step 3 — 综合回答
    ├─ 分析搜索结果
    ├─ 交叉验证多来源
    ├─ 禁止编造未找到的信息
    └─ 输出带来源链接的 Markdown 回答
```

---

## Step 1 — 关键词拆解

### 1.1 判断是否需要搜索

**不需要搜索**（`search_queries` 返回空数组，直接用内部知识回答）：

- 闲聊问候："你好"、"怎么样"
- 纯逻辑/数学/编程基础：无需实时信息
- 翻译改写/纯文本任务

**意图模糊，先问再搜**（不要猜着搜）：

- 问题过于宽泛且无上下文，无法判断用户真正想了解什么（如单独一个词"AI"、"区块链"）
- 问题中有明显歧义，不同理解会导致完全不同的搜索方向
- 处理方式：用一句话说明你的困惑，提出 1-2 个澄清选项，等用户确认后再搜索

**需要搜索**：

- 实时数据：股价、天气、汇率、新闻事件
- 事实核查：某公司状态、事件真伪
- 行业/技术趋势分析
- 观点对比：不同立场对某事件的评价
- 任何需要**多维度交叉验证**的问题

### 1.2 多维拆解策略

从以下维度中选择 1-5 个，生成**正交**的搜索关键词（尽量不重叠）：

| 维度 | 说明 | 示例关键词 |
|------|------|-----------|
| Definition | 核心概念定义 | "DeepSeek 是什么" |
| News | 最新动态 | "DeepSeek 2026 news" |
| Data | 统计数据/市场份额 | "DeepSeek market share" |
| Opinion | 专家评论/争议 | "DeepSeek controversy" |
| Comparison | 竞品对比 | "DeepSeek vs GPT-4" |
| Technical | 技术文档/白皮书 | "DeepSeek architecture paper" |

**正交原则**：关键词之间尽量不重叠，覆盖不同角度。简单问题 1-2 个维度，深度探索 3-5 个。

### 1.3 语言策略

根据信息源分布选择语言比例：

| 领域 | 推荐比例 |
|------|---------|
| 计算机科学、Web3/Crypto、国际金融、前沿医学、国际政治 | 英文为主（4:1 ~ 5:0） |
| 中国本土政策、A股、中文流行文化、本地生活服务 | 中文为主（1:4 ~ 0:5） |

### 1.4 输出 Schema（JSON）

**Keyword Extraction Output Contract**

```json
{
  "refined_question": "string  — 改写后的专业化问题，保留核心意图但更精准",
  "search_queries": ["query1", "query2", "query3"],
  "num_results": "integer  — 每个查询返回的结果数，默认 7，范围 5-10",
  "reasoning": "string  — 拆解逻辑说明，包含维度选择原因和语言策略依据"
}
```

**约束**：
- `search_queries.length × num_results ≤ 40`（总条目数控制）
- 关键词要精炼，加上具体限定词（避免单独搜"AI"、"中国"这类过泛的词）
- `refined_question` 需保留用户原始意图，不能偏离
- `search_queries` 是字符串数组，每个元素就是一个独立的搜索关键词

---

## Step 2 — 调用搜索脚本

### 脚本路径与调用方式

```bash
python {{INSkillDir}}/scripts/search.py search \
  --question "<用户原始问题>" \
  --search-json '{
    "search_queries": ["<query1>", "<query2>", ...],
    "num_results": <N>
  }'
```

> **注意**：`--search-json` 中的 `search_queries` 是**字符串数组**。

### API Key 配置（首次使用）

```bash
# 查看配置状态（含已加载的 key 数量）
python {{INSkillDir}}/scripts/search.py config

# 设置单个 API Key（保存到 ~/.tavily_api_key）
python {{INSkillDir}}/scripts/search.py config --set-api-key YOUR_TAVILY_API_KEY
```

支持多 Key 轮询（每次搜索随机选一个）：

- **推荐：`~/.env`**（标准 KEY=VALUE 格式，逗号或换行分隔）
  ```
  TAVILY_API_KEY=tvly-key1,tvly-key2,tvly-key3
  ```
- **环境变量**：`export TAVILY_API_KEY="tvly-key1,tvly-key2"`
- **`~/.tavily_api_key`**（旧格式，向后兼容）

加载优先级：环境变量 → `~/.env` → `~/.tavily_api_key`

获取 Key：<https://app.tavily.com/home>

---

## Step 3 — 综合回答

### 核心原则

1. **事实基准**：搜索结果**优先于**内部训练知识，特别是时效性信息
2. **禁止编造**：搜索结果中没有的信息，明确说明"搜索结果未提及"，绝不猜测
3. **交叉验证**：不要简单罗列，合并不同来源的数据和观点
4. **引用来源**：每条引用必须有真实可点击的链接，格式 `[标题](URL)`

### 输出格式要求

**结论先行**：开头先简述搜索执行情况（查询次数、结果数量）并给出核心结论。

格式根据内容决定，不强制套模板。基本原则：

1. **开头**：一句话复述理解的问题方向（来自 `refined_question`）、搜索概况，然后直接给出核心结论
其中，搜索概况（查询次数、结果数量）示例如下：
```
📊 搜索概况：执行了 N 次查询（M 次成功），获取 X 条结果，
   其中 Y 条高度相关（相关度 ≥ 0.8）
```
2. **中间**：根据内容选择最合适的结构——可以是分点、可以是对比表格、可以是叙述段落
3. **结尾**：参考来源列表，格式 `[标题](URL)`

---

## 特殊情况处理

### 情况 1：`search_queries` 为空（不需要搜索）

**触发**：问题属于纯闲聊、基础知识、翻译等不需要实时信息的类型。

**处理**：
1. 输出 `{}`（空 JSON 对象）
2. 直接用内部知识回答，无需调用搜索脚本

### 情况 2：API Key 未配置

**脚本输出**：
```
[FATAL] Tavily API key is not configured.
Option A — Save permanently (recommended):
  python {{INSkillDir}}/scripts/search.py config --set-api-key YOUR_KEY
Option B — Set environment variable:
  export TAVILY_API_KEY="YOUR_KEY"
Get your key at: https://app.tavily.com/home
```

**处理**：向用户说明配置步骤，等用户完成后再执行。

### 情况 3：部分搜索失败

**脚本输出**：`[INFO] N/M searches succeeded.`

**处理**：
- 告知用户有部分查询失败，不阻塞流程
- 用成功的搜索结果回答，对失败维度予以说明

### 情况 4：所有搜索失败

**处理**：告知用户，检查 API Key 和网络连接，建议重新配置。

---

## 示例

### 示例 1：正常流程

**用户输入**：`/max-search DeepSeek 最近有什么进展？`

**Step 1 关键词拆解**（内部输出）：

```json
{
  "refined_question": "DeepSeek AI 在 2026 年的最新技术进展和产品发布情况",
  "search_queries": [
    "DeepSeek AI 2026 news",
    "DeepSeek latest model release",
    "DeepSeek R1 update"
  ],
  "num_results": 8,
  "reasoning": "技术公司动态，英文信息源更全面，覆盖新闻发布和技术更新两个维度"
}
```

**Step 2 调用脚本**：

```bash
python {{INSkillDir}}/scripts/search.py search \
  --question "DeepSeek 最近有什么进展？" \
  --search-json '{"search_queries":["DeepSeek AI 2026 news","DeepSeek latest model release","DeepSeek R1 update"],"num_results":8}'
```

**Step 3 综合回答**：基于脚本输出，合成带来源的 Markdown 回答。

---

### 示例 2：不需要搜索

**用户输入**：`/max-search Python 列表推导式怎么写？`

**Step 1 输出**：

```json
{
  "refined_question": "Python 列表推导式的语法结构和使用方法",
  "search_queries": [],
  "num_results": 0,
  "reasoning": "编程基础知识，无需实时信息，可直接用内部知识回答"
}
```

**处理**：直接用内部知识回答，无需调用搜索脚本。

---

### 示例 3：中文话题

**用户输入**：`/max-search 打工人最近流行什么减压方式？`

**Step 1 关键词拆解**（内部输出）：

```json
{
  "refined_question": "职场人士当前主流的压力管理方法和减压活动有哪些？",
  "search_queries": [
    "职场人士 减压方式 2026 趋势",
    "上班族 压力管理 流行活动",
    "工作压力 缓解方法 调查报告"
  ],
  "num_results": 7,
  "reasoning": "打工人是网络用语（指职场人士），拆解为趋势数据、流行观点、调查报告三个维度，中文为主"
}
```

---

## 注意事项

1. **关键词精炼**：去除"的"、"是"、"如何"等停用词，加上具体限定词
2. **总条目数控制**：`search_queries.length × num_results ≤ 40`，避免 context 过载
3. **禁止过度搜索**：简单事实查询不需要 5 个维度的关键词，控制在 1-2 个
4. **脚本路径**：始终使用 `{{INSkillDir}}/scripts/search.py`，不要使用相对路径
5. **stderr vs stdout**：脚本的 stderr 包含执行日志（可忽略），stdout 才是搜索结果

---

## 简化 CLI 接口

除了标准的 `--search-json` 格式，脚本支持更直观的参数格式：

### 标准模式（JSON 格式）

```bash
python {{INSkillDir}}/scripts/search.py search \
  --question "用户问题" \
  --search-json '{"search_queries": ["query1", "query2"], "num_results": 8}'
```

### 简化模式（直接指定查询）

```bash
python {{INSkillDir}}/scripts/search.py search \
  --question "用户问题" \
  --queries "query1" "query2" "query3" \
  --num-results 8
```

**说明**：
- `--queries` 和 `--search-json` 互斥，只能使用其中一个
- `--num-results` 默认值为 8
- 简化模式适合手动测试和快速调用

### 示例对比

**标准模式**：
```bash
python scripts/search.py search \
  --question "WordPress 迁移插件对比" \
  --search-json '{"search_queries": ["WordPress Duplicator review", "WP Migrate Guru features"], "num_results": 8}'
```

**简化模式**：
```bash
python scripts/search.py search \
  --question "WordPress 迁移插件对比" \
  --queries "WordPress Duplicator review" "WP Migrate Guru features" \
  --num-results 8
```

---

## 常见问题（FAQ）

### Q1: 为什么在 Windows 上出现编码错误？

**问题**：运行脚本时出现 `UnicodeEncodeError: 'gbk' codec can't encode character` 错误。

**解决方案**：此问题已在最新版本中修复。脚本会自动检测 Windows 平台并强制使用 UTF-8 编码。如果仍然遇到问题，可以手动设置环境变量：

```bash
set PYTHONIOENCODING=utf-8
python scripts/search.py search --question "..." --queries "..."
```

### Q2: 如何使用多个 API Key？

**解决方案**：在 `~/.env` 文件中使用逗号或换行分隔多个 key：

```
TAVILY_API_KEY=tvly-key1,tvly-key2,tvly-key3
```

脚本会在每次搜索时随机选择一个 key，实现负载均衡。

### Q3: 搜索失败怎么办？

**可能原因**：
1. API key 未配置或已过期
2. 网络连接问题
3. API 配额用尽

**排查步骤**：
1. 检查 API key 配置：`python scripts/search.py config`
2. 测试网络连接：`curl https://api.tavily.com`
3. 查看 Tavily 控制台的配额使用情况

### Q4: 简化模式和标准模式有什么区别？

**简化模式**（`--queries`）：
- 适合手动测试和快速调用
- 参数更直观，无需构造 JSON

**标准模式**（`--search-json`）：
- 适合程序化调用
- 支持更复杂的配置（未来可能扩展更多参数）

两种模式功能完全相同，选择你喜欢的即可。

### Q5: 每次搜索最多可以有多少个查询？

**限制**：`search_queries.length × num_results ≤ 40`

**示例**：
- 4 个查询 × 10 结果 = 40 条（最大）
- 5 个查询 × 8 结果 = 40 条（最大）
- 8 个查询 × 5 结果 = 40 条（最大）

超过此限制会导致 context 过载，影响综合分析质量。


---

## 故障排除指南

### 问题 1：脚本无法找到或导入失败

**症状**：`ModuleNotFoundError` 或 `No such file or directory`

**解决方案**：
1. 确认当前工作目录
2. 使用完整路径：`python ~/.claude/skills/max-search/scripts/search.py`
3. 在技能中使用：`{{INSkillDir}}/scripts/search.py`

### 问题 2：API Key 配置后仍然提示未找到

**症状**：`[FATAL] Tavily API key is not configured`

**排查步骤**：
1. 检查配置文件权限：`ls -la ~/.tavily_api_key`
2. 验证文件内容：`cat ~/.tavily_api_key`（确保没有多余空格或换行）
3. 尝试使用环境变量：`export TAVILY_API_KEY="your-key"`
4. 重新配置：`python scripts/search.py config --set-api-key YOUR_KEY`

### 问题 3：搜索速度很慢

**可能原因**：
1. 网络延迟
2. 查询数量过多
3. 未安装 `aiohttp`（使用同步 fallback）

**优化方案**：
1. 安装异步库：`pip install aiohttp`
2. 减少查询数量（控制在 3-5 个）
3. 降低 `num_results`（推荐 5-8）

### 问题 4：部分搜索失败

**症状**：`[INFO] 3/4 searches succeeded`

**处理方式**：
- 这是正常现象，脚本会继续使用成功的结果
- 如果失败率过高（>50%），检查：
  1. API key 是否有效
  2. 网络连接是否稳定
  3. Tavily 服务状态

### 问题 5：输出结果为空或不完整

**可能原因**：
1. 查询关键词过于宽泛或不准确
2. 搜索结果被域名黑名单过滤
3. Tavily 返回的结果质量较低

**解决方案**：
1. 优化查询关键词，添加具体限定词
2. 增加查询的多样性（不同角度）
3. 提高 `num_results` 参数

