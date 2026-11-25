---
name: subtitle-optimizer
description: Use when reviewing or correcting SRT subtitle text while preserving timestamps, especially ASR transcript errors, product-name terminology, homophone mistakes, and visual review workflows.
---

# SRT 字幕文字优化

此 skill 用于优化 SRT 字幕文件中的文字内容，提高准确性，同时严格保留原始时间戳。所有实际写入最终 SRT 的修改都必须经过审查面板或用户明确确认。

## 核心概念

**词汇列表**（`assets/corrections.json`）：包含已知需要修正的词汇对，支持两种匹配模式：

**普通模式（默认）：**
```json
{"from": "cloud code", "to": "Claude Code", "reason": "产品名称"}
```

**正则模式（`regex: true`）：** 用于处理多种变体，如大小写、空格差异：
```json
{"from": "cloud\\s?code", "to": "Claude Code", "reason": "产品名称", "regex": true}
```
- `cloud code` → Claude Code
- `cloudcode` → Claude Code（无空格）
- `Cloud Code` → Claude Code（大写）

常用正则语法：
- `\s?` — 可选空格
- `\s*` — 零或多空格
- `-?` — 可选连字符
- 大小写不敏感由脚本默认处理，不需要在规则中写 `(?i)`

## 工作流程

### 第一步：加载词汇列表

读取 skill 目录下的 `assets/corrections.json`，了解已知的修正规则。

### 第二步：读取并解析 SRT 文件

使用 Read 工具读取用户提供的 SRT 文件。SRT 格式结构：
```
1
00:00:01,000 --> 00:00:04,000
第一行字幕文本

2
00:00:05,000 --> 00:00:08,000
第二行字幕文本
```

解析要点：
- 序号（1, 2, 3...）
- 时间码（开始时间 --> 结束时间）
- 字幕文本（可有多行）
- 区块之间以空行分隔

### 第三步：分析字幕内容

逐一检查每个字幕条目，识别以下类型的问题：

**基于词汇列表的修正：**
- 遍历 `corrections.json` 中的每条规则
- 如果 `regex: true`，使用正则匹配（考虑大小写不敏感）
- 如果 `regex: false` 或省略，使用普通字符串匹配
- 匹配成功后标记待修正

**转录错误：**
- 同音字/近音字错误（如"未"vs"位"、"时"vs"是"）
- ASR 识别错误
- 标点符号错误

**语义偏差：**
- 上下文理解错误
- 表述不够准确或完整
- 前后文不一致

**判断依据：**
- 句子语法和语义是否通顺
- 同一概念在多个字幕中的表述是否一致
- 是否符合常识和上下文语境

### 第四步：准备候选 SRT 和审查面板

先从 skill 目录运行 `prepare-review`。它会读取原始 SRT 和词汇列表，在原始 SRT 同目录生成：
- `{原文件名}_candidate.srt`
- `{原文件名}_diff_preview.html`

```bash
node scripts/generate_diff.js prepare-review \
  /path/to/video.srt \
  --corrections assets/corrections.json
```

不要把真实用户产物写入 skill 仓库目录或仓库内临时目录。默认只在原始 SRT 同目录生成候选 SRT 和审查面板；调试产物不是最终交付物，确实需要时写到系统临时位置并在完成后清理。

`prepare-review` 生成的候选文件包含词汇列表命中的自动修正。候选文件不是最终输出，必须进入审查流程。

### 第五步：执行 AI 审阅并补充候选修正

`prepare-review` 只是规则词汇预处理，不会自动产生上下文级 AI 建议。不能只运行 `prepare-review` 就向用户汇报审查完成。

运行 `prepare-review` 之后，必须继续阅读原始 SRT 和候选 SRT，做完整逐条审阅，逐段检查候选文件中仍然存在的 ASR 错字、近音字、断句问题、上下文语义偏差和术语不一致。不得只抽样、不得只搜索品牌名或已知词汇、不得只检查脚本输出的差异行。

AI 审阅协议：
1. 先生成审阅分块计划。长文件必须使用 `review-plan` 获得连续审阅范围，不得只靠一次整文件 Read；默认不要生成 `*_review_chunks.json`：
   ```bash
   node scripts/generate_diff.js review-plan \
     /path/to/video.srt \
     --size 100
   ```
   `review-plan` 只输出范围，不创建额外文件。只有在调试或需要机器可读审计记录时，才可以显式运行 `review-chunks`，并且输出到系统临时位置或 Agent 临时目录，不要写到用户字幕目录，也不要作为 skill 文件保留。
2. 按连续字幕区间分批审阅原始 SRT 和候选 SRT，以 `review-plan` 输出的 chunk 范围为准。长文件可以按每 80-150 条字幕一批处理，但必须覆盖完整文件。不得通过一次整文件读取后直接宣称完成；必须能说明已审阅的连续区间。
3. 每批都要同时看前后相邻字幕，判断口语上下文、技术术语、产品名、命令、文件名、英文缩写和中文近音字。
4. 建立候选 AI 修正清单，记录 SRT 序号、原文、修正后文本和原因。只有在上下文证据充分时才加入清单。
5. 对规则已修改的字幕块，确认修正没有误伤上下文；对未修改字幕块，主动检查词汇表漏掉的问题。
6. 全量审阅完成后，再一次性把候选 AI 修正清单写入 `{原文件名}_candidate.srt`，随后刷新审查面板。
7. 最终回复必须列出已审阅的 chunk 范围，例如 `1-100, 101-200, ...`，不能只说“已逐条审阅”。

硬性汇报规则：
- 只要发现任何可修正问题，就必须把它加入候选 AI 修正清单，写入 candidate，并刷新审查面板；不能汇报 “AI 建议 0 条”。
- 不得把发现的问题留给用户在页面里手动修。页面审查用于让用户接受或拒绝候选修正，不是替 Agent 完成已发现问题。
- 如果某个问题证据不足，才可以不写入 candidate，但必须归为“需要人工核对”，不能同时把它称为“高置信度修正”。
- 最终摘要中的 AI 建议数量必须来自刷新审查面板后的脚本统计，而不是人工估算。

重点检查类型：
- ASR 把英文产品名、模型名、命令、文件名、扩展名听错或拆错
- 中文近音字、同音词、错别字，例如术语场景里的“用力/用例”这类问题
- 上下文中已经出现过的同一概念前后写法不一致
- 断句导致的语义不通顺、漏词、多词
- 技术表达不自然但可以从前后文安全还原的内容

分析时至少覆盖：
- 规则已修改的字幕块，确认修正没有误伤上下文
- 未修改的字幕块，检查是否有词汇表漏掉的问题
- 相邻字幕块，确认前后文是否连贯

如果识别出高置信度 AI 修正：
1. 继续编辑同一个 `{原文件名}_candidate.srt`
2. 保留原始序号和时间码
3. 只修改字幕文本
4. 只把有明确把握的修正写入候选文件；审查面板默认接受候选修正，用户可逐条拒绝

如果没有发现高置信度 AI 修正，也要在最终回复中明确说明“已完成上下文 AI 审阅，未发现可安全加入候选文件的 AI 建议”。不要把脚本输出中的 `AI corrections: 0` 当作已经完成 AI 审阅的证据；它只表示当前候选文件里没有非词汇表来源的差异。

### 第六步：刷新审查面板

如果第五步之后没有再修改候选 SRT，`prepare-review` 已经生成审查面板，不需要重复运行命令。若你编辑了候选 SRT 来加入 AI 修正，则用同一个候选文件重新生成 HTML 审查面板：

```bash
node scripts/generate_diff.js \
  /path/to/video.srt \
  /path/to/video_candidate.srt \
  /path/to/video_diff_preview.html \
  --corrections assets/corrections.json
```

审查面板默认展示发生变化的字幕块，同时必须支持切换到“全部字幕”和“未修改”，用于检查是否有漏改。面板包含：

1. **统计信息**：
   - 字幕总数
   - 已修改数
   - 未修改数
   - 规则命中数
   - 已拒绝数
   - 已接受数

2. **对比表格**：
   - 定位信息（变更编号、SRT 序号、时间戳）
   - 修改前内容（红色高亮差异部分）
   - 修改后内容（绿色高亮新内容）
   - 依据标签（规则命中 / AI 建议 / 未修改）
   - 处理按钮（修改行：接受 / 拒绝；未修改行：手动修正）

3. **操作按钮**：
   - 审查范围筛选（修改 / 未修改 / 全部字幕）
   - 修改来源筛选（全部修改 / 规则命中 / AI 建议，仅在“修改”范围下显示）
   - 全部接受 / 全部拒绝 / 手动修正
   - **导出最终 SRT**（直接下载 `{原文件名}_fixed.srt`）

4. **手动添加功能**：
   - **追加词汇规则**：用户可输入 `from`、`to`、`regex`，用于沉淀后续可复用的规则；页面会自动写入默认 `reason`
   - **导出新增规则**：下载 `new_corrections.json`，提示用户把文件交给 Agent，并让它合并到 `assets/corrections.json`
   - **手动修正字幕行**：用户可输入未发生自动修改的字幕序号、原文、修正后文本和原因，用于直接写入最终 SRT

审查面板特性：
- 使用 `assets/diff_preview_template.html` 中的优化审查台 UI；不要临时生成简化版、旧版或一次性 HTML
- 审查台使用浅暖色高对比主题：暖纸背景、深色正文，暖铜用于主导航和定位，玫瑰红用于删除/拒绝，绿色仅用于接受/应用
- 顶部必须包含统计卡片、视图切换、搜索框、结果计数和“导出最终 SRT”按钮
- 表格必须使用“定位 / 修改前 / 修改后 / 依据 / 处理”的结构，避免序号、时间戳和正文混杂
- 变化文字用颜色区分（红色=删除，绿色=新增）
- 默认只显示修改行，避免长字幕文件难以审查
- 支持切换到全部字幕或仅未修改行，用于检查漏改
- 修改行和未修改行必须有明显视觉区分
- 同时展示连续的“变更编号”和原始“SRT 序号”：变更编号只对修改行连续计数，SRT 序号来自原文件，因此在修改视图里会跳号
- 支持按修改来源筛选
- 支持逐条接受或拒绝
- 页面必须支持直接导出最终 SRT，不要求用户下载 JSON 后再运行命令
- 手动行级修正直接写入页面导出的最终 SRT
- 手动词汇规则通过“导出新增规则”进入 `new_corrections.json`；静态页面本身不直接修改本地词汇表文件

### 第七步：展示审查面板并等待用户决策

1. 将预览页面路径告知用户
2. 展示修正统计摘要
3. 询问用户：
   - "以上是所有候选修正（共 N 条，来自规则命中 X 条，AI 建议 Y 条）。审查面板已生成：`{文件名}_diff_preview.html`。默认展示修改行，你也可以切换到全部字幕或未修改行检查漏改。请在页面中接受/拒绝修改，也可以添加遗漏词汇或手动修正未修改的字幕行。完成后点击“导出最终 SRT”即可下载 `{文件名}_fixed.srt`。如果新增了可复用词汇规则，请在“追加词汇规则”区域点击“导出新增规则”，下载后把 `new_corrections.json` 交给 Agent 合并到规则库。"

### 第八步：合并新增词汇规则（可选）

普通用户生成最终字幕不需要 JSON。只有当用户在页面里追加了可复用词汇规则，并导出了 `new_corrections.json` 时，才需要合并到 `assets/corrections.json`：

```bash
node scripts/generate_diff.js update-corrections \
  new_corrections.json \
  --corrections assets/corrections.json
```

合并规则：
- 接受 `new_corrections.json` 中的 `corrections`
- 兼容旧审查记录中的 `manualCorrections`
- 按 `from`、`to`、`regex` 自动去重
- 只更新 `assets/corrections.json`，不会修改当前 SRT 文件

如果希望新增规则也立刻影响当前字幕，应先合并规则，再重新从第三步开始扫描并生成新的候选文件和审查面板。若只是想修改当前某条字幕，应使用“手动修正字幕行”，它会直接进入页面导出的最终 SRT。

### 第九步：应用审查决策（可选自动化入口）

普通用户优先使用页面中的“导出最终 SRT”。当需要在 Agent/CI 中复现同一批审查决策时，仍可使用脚本生成最终字幕文件：

```bash
node scripts/generate_diff.js apply-decisions \
  original.srt \
  video_candidate.srt \
  review_decisions.json \
  video_fixed.srt \
  --corrections assets/corrections.json
```

应用规则：
- `acceptedChangeIds`：使用候选文件中的修正文本
- `rejectedChangeIds`：保留原字幕文本，除非同一序号存在手动行级修正
- `pendingChangeIds`：兼容字段，当前页面通常导出为空数组
- `manualLineEdits`：直接覆盖指定字幕块文本
- `manualCorrections`：兼容旧审查记录，可追加到 `assets/corrections.json`，自动去重
- 始终保留原始时间戳不变

### 第十步：生成输出文件

最终文件要求：
- **保留所有原始时间戳不变**
- 仅替换用户接受或手动添加的文字内容
- 使用 `_fixed` 后缀命名输出文件（例：`video.srt` → `video_fixed.srt`）
- 页面导出：浏览器下载 `{原文件名}_fixed.srt`
- 审查面板和候选文件：默认建议与原始 SRT 放在同一目录
- 脚本导出：输出路径由命令参数指定，默认建议与原始 SRT 放在同一目录
- `new_corrections.json` 只用于更新规则库，不是生成最终字幕的必需步骤

### 输出文件格式

```srt
[原始序号]
[原始时间码]
[修正后文本]

[原始序号]
[原始时间码]
[修正后文本]
...
```

## 预览页面技术规格

预览页面为一个独立的 HTML 文件，包含内联 CSS 和 JavaScript，无需外部依赖。

**设计风格**：
- 浅暖色高对比主题，适合长时间审查字幕
- JetBrains Mono 等宽字体显示代码/时间戳
- 清晰的表格布局

**数据结构**：
```javascript
const diffData = [
  {
    id: 1,
    timestamp: "00:00:01,000 --> 00:00:04,000",
    before: "原文",
    after: "修正后",
    type: "vocabulary",  // 或 "ai"
    status: "accepted",  // accepted / rejected
    reason: "产品名称",
    sourceCorrection: {
      from: "cloud\\s?code",
      to: "Claude Code",
      reason: "产品名称",
      regex: true
    }
  }
];

const reviewRows = [
  {
    id: 1,
    timestamp: "00:00:01,000 --> 00:00:04,000",
    before: "原文",
    after: "修正后",
    beforeHtml: "原文",
    afterHtml: "修正后",
    type: "vocabulary",
    status: "accepted",
    kind: "changed",      // changed / unchanged
    changeNumber: 1       // 未修改行为 null
  }
];
```

**新增规则导出格式**：
```json
{
  "version": 1,
  "generatedAt": "2026-04-16T00:00:00.000Z",
  "corrections": [
    {"from": "原文", "to": "修正后", "reason": "遗漏词汇", "regex": false}
  ]
}
```

## 注意事项

- **不修改时间码**：即使发现时间轴有问题，也只修正文字，时间轴问题需要用户通过专业工具调整
- **保守修正**：只有当 AI 对修正有较高置信度时才提出建议，不确定的地方标注"可能需要人工核对"
- **上下文窗口**：分析时考虑前后字幕的语境，而不仅仅是单句
- **多行字幕**：如果一个时间码对应多行文本，逐行检查并修正
- **遗漏补充**：如果发现词汇列表中没有的常见错误，告知用户可在预览页面中添加；这些词汇会进入 `new_corrections.json`，再由 Agent 或脚本追加到 `assets/corrections.json`
- **审查优先**：先生成候选文件和审查面板，用户审查后直接从页面导出最终 SRT
- **静态页面限制**：HTML 面板可以下载最终 SRT 和新增规则，但不能直接写入本地 `corrections.json`；更新词汇表仍需要 Agent 或脚本处理
