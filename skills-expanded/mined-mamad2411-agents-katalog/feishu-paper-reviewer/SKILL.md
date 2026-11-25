---
name: feishu-paper-reviewer
version: 1.0.0
description: "飞书文档论文审阅工具。直接在飞书云文档上进行学术论文审阅，支持高亮、删除线、加粗变色、划词批注、插入审阅意见等多种修订标记。当用户提到对飞书文档/云文档进行论文审阅、审稿、评阅、修改批注，或提供飞书文档链接要求审阅时触发。关键词：飞书论文审阅、飞书审稿、云文档评阅、飞书批注论文。"
---

# 飞书文档论文审阅

对飞书云文档（docx）中的学术论文进行专业审阅，直接在文档正文中标注修订（高亮、删除线、变色、替换建议），并通过飞书评论系统添加划词批注和全文总评。审阅完成后，作者在飞书中打开文档即可看到所有修订标记和评论。

## 前置依赖

- `lark-cli`（已安装）
- 需要先阅读 [lark-shared](../lark-shared/SKILL.md) 了解认证和权限
- 操作依赖：[lark-doc](../lark-doc/SKILL.md)（docs +fetch / +update）、[lark-drive](../lark-drive/SKILL.md)（drive +add-comment）

## 工作流程

### 第 1 步：确认文档并获取内容

向用户确认待审阅的飞书文档 URL 或 doc_id。支持 `/docx/` 和 `/wiki/` 链接。

```bash
lark-cli docs +fetch --doc "<文档URL或ID>"
```

获取返回的 Markdown 全文。如果文档较长，可使用 `--offset` 和 `--limit` 分页获取。

如果用户给出的是 `/wiki/` 链接，先查询真实文档类型：
```bash
lark-cli wiki spaces get_node --params '{"token":"<wiki_token>"}'
```
确认 `obj_type` 为 `docx` 后，使用 `obj_token` 进行后续操作。

### 第 2 步：系统评阅论文

以**资深学术期刊审稿人**身份，对论文进行全面、系统的评阅。评阅必须严格、专业、建设性。

#### 评阅维度

**结构层面：**
- 标题是否精准反映研究内容，副标题是否必要
- 摘要是否完整涵盖研究问题、方法、核心发现与贡献
- 引言是否清晰建立了研究问题的学术合法性
- 文献综述是否展现学术脉络与对话关系（而非简单罗列）
- 研究方法是否透明、可信，认识论与方法论是否一致
- 分析与发现是否有充分的证据支撑，论证链条是否完整
- 讨论与结论是否回应了研究问题，理论贡献是否具体

**语言层面：**
- 概念使用是否一致、精确（一个概念一个术语，全文统一）
- 是否存在空话套话（"随着XX的发展""具有重要意义""丰富了XX研究"等）
- 论证是否遵循「主张—证据—推理」结构
- 段落是否有明确主题句
- 衔接是否自然，逻辑推进是否清晰

**学术规范层面：**
- 引用是否规范，是否回到原始文献
- 理论使用是否深入（非贴标签式），是否说明边界条件
- 研究贡献表述是否具体而非泛泛
- 方法论反思性是否充分（定性研究尤其重要）

### 第 3 步：生成修订计划

将评阅结果整理为结构化的修订列表。每条修订必须包含明确的类型、定位信息和理由。

修订总量控制在 **15-30 条**为宜：太少则审阅不够深入，太多则让作者无所适从。优先处理影响论文核心质量的问题。

#### 修订类型（5 种）

详细语法参见 [references/revision-marks.md](references/revision-marks.md)。

| type | 何时使用 | 正文操作 | 评论操作 |
|------|---------|---------|---------|
| `highlight` | 标注需要作者注意的问题文本 | 黄色高亮 | 划词评论说明问题 |
| `suggest_delete` | 建议删除冗余/不当内容 | 红色删除线 | 划词评论说明理由 |
| `suggest_replace` | 建议用更好的表述替换 | 删除线 + 蓝色新文本 | 划词评论说明理由 |
| `comment_only` | 宏观建议，不直接改正文 | 无 | 划词评论 |
| `callout_insert` | 章节级审阅意见 | 插入 callout 块 | 无 |

#### 颜色约定

| 颜色 | 含义 | Markdown 写法 |
|------|------|--------------|
| 黄色高亮 | 需注意的问题 | `<text background-color="yellow">文本</text>` |
| 红色文字 | 严重问题 / 建议删除 | `<text color="red">~~文本~~</text>` |
| 蓝色粗体 | 建议替换的新文本 | `<text color="blue">**新文本**</text>` |
| 绿色 callout | 值得肯定之处 | `<callout emoji="✅" background-color="light-green">` |
| 黄色 callout | 审阅意见 / 修改建议 | `<callout emoji="📝" background-color="light-yellow">` |
| 红色 callout | 严重问题说明 | `<callout emoji="⚠️" background-color="light-red">` |

### 第 4 步：应用正文修订

通过 `docs +update` 逐条应用正文格式修改。

**执行顺序**：**从文档末尾向开头**逐条执行，这样前面未修改的文本定位不会受到影响。

**每次只改一处**，使用 `replace_range` 模式配合 `--selection-with-ellipsis` 精确定位：

```bash
# highlight — 黄色高亮
lark-cli docs +update --doc "<doc_id>" \
  --mode replace_range \
  --selection-with-ellipsis "需要高亮的原文片段" \
  --markdown '<text background-color="yellow">需要高亮的原文片段</text>'

# suggest_delete — 红色删除线
lark-cli docs +update --doc "<doc_id>" \
  --mode replace_range \
  --selection-with-ellipsis "建议删除的原文" \
  --markdown '<text color="red">~~建议删除的原文~~</text>'

# suggest_replace — 删除线旧文 + 蓝色新文
lark-cli docs +update --doc "<doc_id>" \
  --mode replace_range \
  --selection-with-ellipsis "需要替换的旧文本" \
  --markdown '<text color="red">~~需要替换的旧文本~~</text><text color="blue">**建议的新文本**</text>'

# callout_insert — 在指定位置后插入审阅意见块
lark-cli docs +update --doc "<doc_id>" \
  --mode insert_after \
  --selection-with-ellipsis "定位文本...该段结尾" \
  --markdown '<callout emoji="📝" background-color="light-yellow">
**审阅意见**：此处需要补充方法论说明...
</callout>'
```

**定位要点：**
- `--selection-with-ellipsis` 使用 15-25 个字符确保唯一匹配
- 如果匹配失败（返回错误），尝试扩大定位范围或使用 `开头...结尾` 格式
- 定位文本必须与文档中的**纯文本内容**完全一致（不含 Markdown 标记）
- 修改前不需要重新 fetch 文档（lark-cli 内部定位）

**错误处理：**
- 如果某条修订定位失败，记录下来继续执行后续修订，最后汇总告知用户
- 如果多次定位失败，考虑原文中是否有重复内容，需要扩大定位上下文

### 第 5 步：添加批注评论

通过 `drive +add-comment` 添加评论。评论分两类：

#### 划词批注（局部评论）

针对具体文本段落添加审阅意见。对应 `highlight`、`suggest_delete`、`suggest_replace`、`comment_only` 类型的修订。

```bash
lark-cli drive +add-comment \
  --doc "<doc_id>" \
  --selection-with-ellipsis "目标文本片段" \
  --content '[{"type":"text","text":"【审阅意见】此处论证逻辑存在跳跃，建议补充从A到B的推理过程。"}]'
```

**注意：**
- 划词评论的定位文本应基于**修改后**的文档内容（如果该位置已被加了格式标记，定位时使用原始纯文本即可，lark-cli 会在底层匹配）
- 评论内容以 `【审阅意见】` 开头，使作者一目了然
- 评论中区分「必须修改」和「建议修改」：
  - `【必改】` — 影响论文质量的关键问题
  - `【建议】` — 可以改善但非必须的建议
  - `【肯定】` — 值得肯定的写作亮点

#### 全文总评

在所有局部修订完成后，添加一条全文评论作为总体评审意见。

```bash
lark-cli drive +add-comment \
  --doc "<doc_id>" \
  --full-comment \
  --content '[{"type":"text","text":"【论文总评】\n\n一、总体评价\n...\n\n二、主要优点\n...\n\n三、主要问题\n...\n\n四、修改建议\n...\n\n五、综合判断\n..."}]'
```

全文总评的结构：
1. **总体评价**：一两句话概括论文的核心贡献和总体水平
2. **主要优点**：2-3 个具体的学术亮点（选题、方法、发现等）
3. **主要问题**：按严重程度排列，区分必改项和建议项
4. **修改建议**：针对主要问题给出具体、可操作的改进方向
5. **综合判断**：给出审稿建议（如：大修后重审 / 小修后接受 / 建议退稿）

### 第 6 步：汇报审阅结果

向用户汇报：

1. 审阅完成，文档链接
2. 修订统计：共 N 条修订（M 条高亮、X 条删除建议、Y 条替换建议、Z 条评论、W 条审阅意见块）
3. 全文总评已添加
4. 如有定位失败的修订，列出未能应用的条目
5. 提示作者打开飞书文档查看修订和评论

## 审阅原则

- **批判性优先**：以学术共同体的高标准审视，不因"已经很好了"而降低要求
- **建设性表达**：指出问题的同时给出改进方向，而非只批评不建议
- **区分轻重**：严格区分「必须修改」与「建议修改」，帮助作者抓住重点
- **具体精准**：评审意见必须指向具体的段落、句子或概念，不做空泛评价
- **学科专业性**：评审语言和标准应符合社会学学科的学术规范
- **尊重作者**：审阅是学术对话，不是单方面批判；肯定优点与指出问题同等重要

## 审阅深度选项

用户可以指定审阅深度，默认为「标准审阅」：

| 深度 | 说明 | 修订量 | 适用场景 |
|------|------|--------|---------|
| 快速 | 聚焦结构和核心论证 | 8-15 条 | 初稿快速反馈 |
| 标准 | 结构 + 论证 + 语言 | 15-30 条 | 正式审稿 |
| 深度 | 全方位细致审阅 | 30-50 条 | 投稿前终审 |

用户也可以指定只审阅某个维度（如"只看语言问题"）或某个章节（如"重点审阅方法部分"）。

## Wiki 链接处理

如果用户提供的是 `/wiki/` 链接：

1. 先解析 wiki token：`lark-cli wiki spaces get_node --params '{"token":"<wiki_token>"}'`
2. 确认 `obj_type` 为 `docx`（其他类型不支持审阅）
3. 后续所有 `docs +update` 和 `drive +add-comment` 使用 `obj_token`（真实文档 token）

## 注意事项

- 正文修订从**文档末尾向开头**执行，避免位置偏移导致定位失败
- 每条 `docs +update` 只改一处，不要合并多处修改
- `drive +add-comment` 的划词评论仅支持 `docx` 格式文档
- 如果文档是只读或无编辑权限，会返回权限错误，需提示用户授权
- 修订完成后**不要**使用 `overwrite` 模式，否则会丢失已添加的评论
