---
name: arxiv-paper-expert
description: 面向中文自然语言的 arXiv 论文检索、整理、分析与简报生成技能。支持两大领域：1) 语音与音频深度学习（speech/audio/TTS/ASR/AudioLLM）；2) 金融量化与 AI（quantitative trading/algorithmic trading/portfolio/risk management）。用于处理"最近语音/量化有什么新论文""帮我整理 speech/audio/金融量化方向论文""给我一版最近论文的浓缩总结"这类请求；执行搜索、全文抓取、LLM 分析、Markdown/HTML 报告生成，以及执行后摘要回复。
---

# arxiv-paper-expert

用于整理**语音相关深度学习论文**和**金融量化 AI 论文**，在指定时间范围内的 arXiv 新论文。

## 典型触发

### 语音/音频方向
- 帮我看最近几天语音有什么新论文
- 帮我整理最近 speech / audio / TTS / ASR 论文
- 最近 AudioLLM 有什么新工作
- 帮我生成一版语音论文简报
- 把这批语音相关论文做成 HTML 和 Markdown

### 金融量化方向
- 最近金融量化有什么新论文
- 帮我看 AI 在量化交易中的应用
- 帮我整理 reinforcement learning trading / portfolio optimization 论文
- 最近 alpha generation / risk management 有什么新工作

## 默认范围

优先把这个 skill 理解为：**语音、音频、说话人、语音生成、语音理解、AudioLLM、金融量化 AI 相关深度学习论文整理器**。

常见主题包括：

### 语音/音频方向
- speech
- audio
- voice
- TTS / text-to-speech
- ASR / speech recognition
- speech enhancement
- speech separation
- speaker / diarization / verification
- audio deepfake
- audio language model / speech LLM

### 金融量化方向
- quantitative trading / algorithmic trading
- portfolio optimization / portfolio allocation
- risk management / volatility modeling
- options pricing / derivative pricing
- stock prediction / market prediction
- reinforcement learning trading
- deep learning finance
- factor model / alpha generation

## 执行流程

统一入口：`python -m src`（调用 src/main.py）

完整流程按顺序执行 4 个阶段（中间结果自动复用）：

1. **搜索论文** → `results/arxiv_results.json`
2. **抓取全文** → `results/arxiv_results_content.json`
3. **LLM 分析** → `results/arxiv_results_content_analysis.json`
4. **生成报告** → `results/arxiv_results_content_report.html/.md`

执行后必须收尾：读取本次新生成的 Markdown 报告，提炼一版可直接发送给用户的浓缩总结，附上自己的简短评价，通过消息告知用户，不要只说"文件已生成"。

---

## 使用方式

### 默认配置

`config.json` 中的默认配置如下：

```json
{
  "search": {
    "domain": "speech",
    "start_date": "2026-04-01",
    "end_date": "2026-04-03",
    "max_results": 200
  }
}
```

含义：
- **domain = "speech"**：默认检索语音/音频方向论文（ASR/TTS/增强/分离/说话人/AudioLLM 等）
- **时间范围**：由 `start_date` 和 `end_date` 决定，格式必须为 `YYYY-MM-DD`
- 预置 topic（speech / quant 的完整查询语句）已内置于代码中，无需手动填写

### 指定检索领域

通过 `--domain` 参数切换，默认已经是 speech，常见用法：

```bash
# 默认：检索语音/音频方向（等同于 --domain speech）
python -m src --full

# 切换到金融量化方向
python -m src --domain quant --full

# 同时检索语音 + 量化两个领域
python -m src --domain both --full
```

> `--domain` 参数会覆盖 `config.json` 中的 `search.domain`，但不会改变 config 文件本身。

### 指定时间范围

通过 `--start-date` 和 `--end-date` 参数设置，格式为 `YYYY-MM-DD`：

```bash
# 检索最近一周（语音方向，默认 domain）
python -m src --start-date 2026-03-27 --end-date 2026-04-03 --full

# 检索最近一个月（量化方向）
python -m src --domain quant --start-date 2026-03-03 --end-date 2026-04-03 --full

# 检索特定月份（两个领域）
python -m src --domain both --start-date 2026-03-01 --end-date 2026-03-31 --full
```

> `--start-date` / `--end-date` 会覆盖 `config.json` 中的对应值。

### 完全自定义查询

如果预置的 speech / quant / both 都不满足需求，可以用 `--query` 参数传入自定义 arXiv query，会完全覆盖 domain 的行为：

```bash
# 只检 speech enhancement 相关
python -m src --query "cat:eess.AS AND all:\"speech enhancement\"" --full

# 混查任意方向
python -m src --query "(cat:eess.AS OR cat:cs.CL) AND all:\"LLM\"" --full
```

### 常用场景速查

| 需求 | 推荐命令 |
|------|----------|
| 最近一周语音论文 | `python -m src --start-date 2026-03-27 --end-date 2026-04-03 --full` |
| 最近一周量化论文 | `python -m src --domain quant --start-date 2026-03-27 --end-date 2026-04-03 --full` |
| 最近两周两个领域都看 | `python -m src --domain both --start-date 2026-03-20 --end-date 2026-04-03 --full` |
| 自定义查询 | `python -m src --query "..." --full` |

---

## 执行后默认回复模板

完成一次标准执行后，默认按下面结构回复，除非用户明确要求别的格式：

```markdown
已完成指定时间范围的论文整理。

**产出文件**
- Markdown: `results/arxiv_results_content_report.md`
- HTML: `results/arxiv_results_content_report.html`

**本次范围**
- 时间范围：...
- 论文总数：...
- 分类分布：frontend X / backend Y / audiollm Z / quant W / other O

**浓缩版结论**
- 最值得优先看的 3-5 篇：...
- 这一批论文的共同趋势：...
- 哪些更偏方法创新，哪些更偏工程整合：...

**我的评价**
- 用 3-6 句话给出判断，不要只复述报告内容。
- 可以直接说：这批论文整体偏扎实 / 偏热闹 / 偏生成 / 偏安全 / 偏工程。
- 如果有明显最值得追踪的方向，也直接点出来。
```

回复风格要求：
- 先给结果，再给判断
- 默认简洁，不写流水账
- 不要只说"文件已生成"
- 尽量给出明确偏好和取舍，而不是平均用力地罗列

## "最值得看"默认筛选标准

当你需要从一批论文里挑出"最值得优先看"的 3-5 篇时，默认按下面标准排序和判断：

### 优先项

- **方法新意优先于纯工程堆料**
  - 如果一篇论文只是把已有模块重新拼装、主要靠堆参数、堆数据或堆训练技巧提分，应降低优先级
  - 如果一篇论文提出了新的问题建模方式、结构设计、训练视角、分析框架或评估思路，应提高优先级

- **跨方向迁移价值高的优先**
  - 不只看它在单一 benchmark 上是否有效，还要看它的方法能否迁移到其他任务
  - 对语音、音频、金融量化等方向都可能有启发的方法，应优先推荐

- **对领域主线问题有结构性推进的优先**
  - 例如在语音领域（ASR、TTS、增强、分离）或量化领域（alpha 生成、风险建模）给出明确改进
  - 如果只是对已有主线做边角优化，优先级应更低

### 降权项

- **单纯刷指标但缺少洞察的降权**
  - 如果论文主要卖点只是"某个 benchmark 上又涨了几点"，但看不出为什么有效、也没有新的分析或可迁移的设计，应降权
  - 如果实验做得很满但核心思想薄弱，也不要因为表格好看就优先推荐

### 结果表达要求

在给"最值得看"推荐时，不要只列标题。要顺带说明：
- 为什么它值得优先看
- 它更偏方法创新、结构创新、问题定义创新，还是只是工程整合
- 它是否可能影响其他方向，而不只是当前子任务

## 输出与覆盖规则

默认输出都写入 `results/`，并且**直接覆盖同名文件**：

- `results/arxiv_results.json`
- `results/arxiv_results_content.json`
- `results/arxiv_results_content_analysis.json`
- `results/arxiv_results_content_report.md`
- `results/arxiv_results_content_report.html`

含义：
- 下次执行会覆盖这次结果
- 对于滚动追踪，这是合理默认行为
- 如果需要保留历史快照，应手动另存一份

## 配置说明

`config.json` 中 `search` 节的完整结构（预置 topic 已内置，通常无需修改）：

```json
{
  "search": {
    "domain": "speech",
    "topic": {
      "speech": "...",
      "quant": "..."
    },
    "start_date": "2026-04-01",
    "end_date": "2026-04-03",
    "max_results": 200,
    "page_size": 100
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `domain` | string | `speech`（默认）/ `quant` / `both`，决定预置 topic 选哪个 |
| `topic` | object | speech / quant 对应的完整 arXiv 查询语句，已内置 |
| `start_date` | string | 检索开始日期，格式 YYYY-MM-DD |
| `end_date` | string | 检索结束日期，格式 YYYY-MM-DD |
| `max_results` | int | 最大返回论文数 |
| `page_size` | int | 每次请求的批量大小 |

> **注意**：domain 参数的行为说明和完整使用示例见上方「使用方式」一节。

### 论文分类（五类）
- **frontend**：语音前端（增强、分离、VAD 等）
- **backend**：语音后端（ASR、TTS、说话人等）
- **audiollm**：音频大模型
- **quant**：金融量化 AI
- **other**：其他领域论文（不属于上述四类的）

## 注意事项

- 默认优先给用户一版**浓缩摘要 + 个人评价**，文件路径放在前面或后面都可以
- 如果用户明确只要文件，再简化回复
- 如果分析阶段发现旧文件干扰，应坚持使用本次流程生成的 `results/arxiv_results_content*.json`
- 如果用户问"下次会不会覆盖结果"，答案是：**会，默认覆盖同名 results 文件**
- 时间范围通过修改 `config.json` 中的 `start_date` 和 `end_date` 设置，不要使用 --days 参数
- **时间转换规则**：如果用户说"最近一周"，计算 `end_date = 今天`，`start_date = 今天 - 7 天`（使用 Python: `datetime.date.today() - datetime.timedelta(days=7)`）

## 快速时间转换参考

| 用户表达 | start_date | end_date |
|---------|-----------|----------|
| 最近一周 | 今天 - 7天 | 今天 |
| 最近两周 | 今天 - 14天 | 今天 |
| 最近一个月 | 今天 - 30天 | 今天 |
| 3月1日到3月31日 | 2026-03-01 | 2026-03-31 |

> 今天是 2026-04-03，可直接使用此日期进行计算。
