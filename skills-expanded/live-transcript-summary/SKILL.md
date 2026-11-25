---
name: live-transcript-summary
description: 边听边总结：实时监听当前 WPS 笔记中的音频转写，每 60 秒自动循环一次，识别场景后按对应模板整理内容，并写回笔记。当用户提到正在录音、开会、听课、听播客、做采访、开始录制，或者希望 AI 帮忙整理、总结、记录当前正在发生的内容时使用此 skill。也适用于用户说「帮我跟着听」「你帮我记」「边听边整理」「录完帮我整理」「实时帮我总结」，或在笔记中输入 *** 希望 AI 结合录音补全内容的场景。
metadata:
  author: Yicheng Xu
  version: "2.3.0"
  tags: [audio, transcript, summary, real-time, wps-note]
---

# 边听边总结 Skill

实时监听当前 WPS 笔记中的音频录音转写，每 60 秒轮询一次，**只处理新增句子（增量模式）**，根据场景自动选择模板整理内容并写回笔记。

---

## 工具优先级

**优先使用 `wpsnote-cli`（CLI），不支持时才退回 MCP 工具调用。**

| 操作 | CLI 命令 | MCP 工具 |
|------|----------|----------|
| 获取当前笔记 | `wpsnote-cli current --json` | `get_current_note()` |
| 获取大纲 | `wpsnote-cli outline --note_id ID --json` | `get_note_outline()` |
| 获取转写 | `wpsnote-cli audio --shorthand_id ID --json` | `get_audio_transcript()` |
| 搜索笔记 | `wpsnote-cli find --keyword KW --json` | `search_notes()` |
| 搜索笔记内内容 | `wpsnote-cli search --note_id ID --query Q --json` | `search_note_content()` |
| 插入内容 | `wpsnote-cli edit --json-args '...'` | `edit_block(op="insert")` |
| 替换内容 | `wpsnote-cli edit --json-args '...'` | `edit_block(op="replace")` |
| 批量编辑 | `wpsnote-cli batch-edit --json-args '...'` | `batch_edit()` |

> CLI 中 XML 含尖括号时，**统一用 `--json-args` 传 JSON 对象**，避免 shell 转义问题。

---

## ⚠️ 写入笔记时的强制规则

**`content` 参数必须是 XML 字符串，绝不能是数组或对象。**

```json
// ✅ 正确
{ "content": "<h2>标题</h2><p>内容</p>" }

// ❌ 禁止——数组
{ "content": [{"type": "text", "text": "<h2>标题</h2>"}] }

// ❌ 禁止——对象
{ "content": {"type": "text", "text": "<h2>标题</h2>"} }
```

遇到 `BLOCK_NOT_FOUND` 或写入反复失败时，**第一步检查 `content` 是否为字符串**，再用 `outline` 刷新 block_id 后重试。

---

## 核心工作流

```
启动（仅一次）:
  1. 检查 CLI 可用性
  2. 获取当前笔记 note_id
  3. 风格学习（搜索 3-5 篇历史同类笔记）
  4. 初始化状态文件
  5. 输出启动告知

loop（每 60 秒）:
  1. 扫描笔记大纲，找 NoteAudioCard
  2. 全量拉取转写，过滤新增句子（start_time > last_end_time）
  3. 若无新增 → 检测临时区用户输入 → 更新状态 → sleep 60 → continue
  4. 首轮：场景识别 + 发言人推断
  5. 人名联动：提取人名 → 搜索笔记库 → 注入背景上下文
  6. 首轮：先输出内容地图，再开始写入
  7. 用新增句子生成摘要 XML
  8. 写回笔记（首轮在末尾插入；后续追加到 summary_anchor 之后，始终在临时区之前）
  9. 回扫大纲：核查新内容是否落在正确章节，发现位置错误立即修正
 10. 首轮：在笔记末尾创建临时区（hr + 提示块）
 11. 检测临时区用户输入 → 合并到正文 → 清空用户 block
 12. 检测 *** 补全请求
 13. 更新状态文件（last_end_time、summary_anchor_id、temp_zone_anchor_id 等）
 14. 输出本轮简报 → sleep 60 → loop
```

---

## 启动阶段

### Step 1：检查 CLI 可用性

```bash
wpsnote-cli status
# 输出包含"连接中... 成功" → CLI 可用，否则退回 MCP 模式
```

### Step 2：获取当前笔记

```bash
NOTE=$(wpsnote-cli current --json)
NOTE_ID=$(echo $NOTE | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['note_id'])")
```

```
# MCP 备选
get_current_note() → { note_id, title }
```

若返回 `NO_ACTIVE_EDITOR_WINDOW`，提示用户打开笔记后重试。

### Step 3：风格学习

搜索 **3-5 篇**历史同类笔记（会议纪要/课堂笔记/总结），每篇最多读 **3000 字**，综合归纳风格特征：

```bash
NOTES=$(wpsnote-cli find --keyword "会议纪要 纪要 会议总结 周会 月会" --limit 5 --json)
```

**归纳维度**（多篇投票取多数）：语言风格（口语 vs 书面）、结构偏好（bullet list vs 分章节）、详略程度、是否中英混写、是否常用色块/分栏。

样本不足 3 篇时继续，标注「风格样本不足，参考有限」。

### Step 4：初始化状态文件

```python
state = {
    "note_id": note_id,
    "shorthand_id": None,        # 首轮扫描到 AudioCard 后填入
    "scene": None,               # 首轮场景识别后填入
    "last_end_time": -1.0,       # -1 代表从头开始
    "summary_anchor_id": None,   # 上轮最后写入的 block_id（临时区 hr 之前）
    "temp_zone_anchor_id": None, # 临时区 highlightBlock 的 block_id
    "round": 0,
    "speaker_map": {},           # {"发言人 1": "真实姓名"}
    "person_cache": {},          # {"张总": [{"note_title": ..., "snippet": ...}]}
    "started_at": time.time(),
}
# 保存到 /tmp/lts_state_{note_id}.json
```

### Step 5：输出启动告知

```
已开始边听边总结 ✓

当前笔记：[笔记标题]
识别场景：等待录音开始后自动识别
参考风格：[找到 N 篇 / 未找到历史总结]
模式：增量（只处理新增转写）+ 人名联动
轮询间隔：60 秒

---
援助功能：
  ① 补全：在笔记任意位置输入 ***，AI 结合录音自动补全
  ② 临时区：笔记末尾灰色区域，写下想法，AI 下轮自动合并到正文
  ③ 停止：告诉我「停止总结」即可
---
```

---

## 轮询主循环

### Step 1：扫描音频卡片

```python
outline_data = json.loads(wpsnote_cli_outline(note_id))
audio_blocks = [b for b in outline_data["data"]["blocks"] if b["type"] == "note_audio_card"]

if not audio_blocks:
    # sleep 60, continue
    pass

audio_block = audio_blocks[0]  # 取第一个，或 status=recording 的那个
shorthand_id = audio_block["attrs"]["shorthand_id"]
status = audio_block["attrs"].get("status", "unknown")
# recording / paused / stopped 均继续处理
```

### Step 2：增量获取转写

```python
all_sentences = get_transcript(shorthand_id)  # 每个 sentence: {text, speaker, start_time, end_time}

# 只取新增句子
new_sentences = [s for s in all_sentences if s["start_time"] > state["last_end_time"]]

if not new_sentences:
    # → 跳到 Step 8（检测临时区），然后 sleep 60
    pass
```

> `wpsnote-cli audio` 只支持全量拉取，过滤在本地完成，每轮实际处理量恒定。

### Step 3：场景识别（首轮）

```python
if state["scene"] is None and new_sentences:
    sample = " ".join(s["text"] for s in new_sentences[:10])
    state["scene"] = detect_scene(note_title, sample)  # 见「场景识别表」
```

### Step 4：发言人身份推断

```python
for s in new_sentences:
    if "我是" in s["text"] or "我叫" in s["text"]:
        state["speaker_map"][s["speaker"]] = extracted_name
        # 若发现纠正，批量替换笔记中旧名称
```

### Step 5：人名联动（跨笔记背景注入）

从新增句子和 speaker_map 中提取人名，搜索笔记库，将背景上下文注入本轮摘要 prompt。

**搜索策略**（依次降级）：全名 → 后两字 → 名字单字（慎用）

每人最多取 2 篇 × 3 段，结果缓存在 `state["person_cache"]`，同一 session 不重复搜索。

> 详细代码见 [person-linking.md](person-linking.md)

### Step 6：首轮输出内容地图

**仅首轮（`state["round"] == 0`）触发**：在写入笔记之前，根据全量转写梳理整体逻辑结构，以树形图展示给用户，然后直接开始写入。

```
📋 内容地图

[笔记标题]
├── 基本信息（时间、参与人等）
├── 第一部分：[主题名称]
├── 第二部分：[主题名称]
│   ├── [子主题]
│   └── [子主题]
├── 第 N 部分：[主题名称]
└── 行动项
```

展示后立即开始写入，大标题从 H2 开始，无需等待用户确认。

### Step 7：生成摘要 XML

**输入给 AI 的 prompt**：

```
[场景: {scene}] [发言人映射: {speaker_map}]

新增转写（{N} 句，{时长}秒）：
{speaker}: {text}
...

[人物背景（来自笔记库，供参考）]:
- 张总（来自《Q4 复盘》）：...

请按 {模板名} 模板提取要点，生成 WPS XML 格式的增量摘要。
只写本段新增内容对应的要点，不要重复已有内容。
```

**约束**：严格基于转写、跳过空章节、模糊信息标注「待确认」、参考用户风格、默认富文本排版。

### Step 8：写回笔记

**核心原则：新摘要内容始终插入到临时区 hr 之前，临时区永远压底。**

**首轮写入**（临时区尚不存在）：

```bash
# 1. 插入摘要内容到笔记末尾
wpsnote-cli edit --json-args "{
  \"note_id\": \"$NOTE_ID\",
  \"op\": \"insert\",
  \"anchor_id\": \"$LAST_BLOCK\",
  \"position\": \"after\",
  \"content\": \"<h2>转写摘要</h2><p>...</p>\"
}"
# 记录 summary_anchor_id = 本次最后插入的 block_id

# 2. 在末尾创建临时区
wpsnote-cli edit --json-args "{
  \"note_id\": \"$NOTE_ID\",
  \"op\": \"insert\",
  \"anchor_id\": \"$SUMMARY_ANCHOR_ID\",
  \"position\": \"after\",
  \"content\": \"<hr/><highlightBlock emoji=\\\"💬\\\" highlightBlockBackgroundColor=\\\"#EBEBEB\\\" highlightBlockBorderColor=\\\"#C5C5C5\\\"><p><span fontColor=\\\"#757575\\\">把你的想法、补充、纠正贴到这里，AI 下轮自动合并到正文对应位置。也可以直接改上面的正文。</span></p></highlightBlock>\"
}"
# 记录 temp_zone_anchor_id = highlightBlock 的 block_id
```

**后续轮次**（临时区已存在）：

```bash
# 新内容追加到 summary_anchor_id 之后（临时区 hr 之前）
wpsnote-cli edit --json-args "{
  \"note_id\": \"$NOTE_ID\",
  \"op\": \"insert\",
  \"anchor_id\": \"$SUMMARY_ANCHOR_ID\",
  \"position\": \"after\",
  \"content\": \"<p>新增摘要内容...</p>\"
}"
# 更新 summary_anchor_id = 本次最后插入的 block_id
```

### Step 9：写入后回扫大纲（每轮必做）

每轮写入完成后，**立即重新拉取笔记大纲**，逐章核查内容是否在正确位置：

```bash
OUTLINE=$(wpsnote-cli outline --note_id "$NOTE_ID" --json)
```

**检查项**：
- 各 h2 章节标题是否与内容地图一致（首轮建立后不应新增游离章节）
- 本轮新增内容是否落在对应章节下，而非全部堆在笔记末尾
- 临时区（hr + 提示块）是否仍在最末尾

**发现异常时**：
- 若新内容错误地插到了末尾而非对应章节，用 `batch_edit` 将其移动到正确的 h2 节下
- 若章节标题顺序乱了，修正后更新 `summary_anchor_id` 为当前章节末尾的正确 block_id
- 输出简报时注明「⚠️ 本轮修正了 N 处位置错误」

### Step 10：处理临时区用户输入

检查用户是否在临时区写了内容（提示块之后的任意 block 即为用户输入）：

```python
temp_anchor_id = state.get("temp_zone_anchor_id")
if not temp_anchor_id:
    pass  # 临时区尚未创建，跳过
else:
    # 读取 temp_zone_anchor_id 后方 10 个 block
    # 过滤掉 hr 块和含「把你的想法」的提示块
    user_blocks = [b for b in after_blocks
                   if b["type"] != "hr"
                   and "把你的想法" not in b.get("content_text", "")]
```

若有用户输入，执行合并：

1. 将用户内容 + 当前摘要大纲喂给 AI，判断每条应插入到哪个位置（补充/新话题/纠正）
2. 用 `batch_edit` 插入/替换到正文对应位置
3. 删除临时区中用户写的 block，保留 `<hr/>` 和提示块

**合并 prompt**：

```
用户写在临时区的内容：
{user_temp_content}

当前笔记摘要大纲（含 block_id）：
{summary_outline}

请判断每条内容应插入到哪个 block_id 之后，生成对应 WPS XML。
规则：补充 → 插入对应观点之后；新话题 → 插入摘要末尾（临时区 hr 之前）；纠正 → 替换对应 block。
保持原有排版风格。
```

### Step 11：检测 *** 补全请求

```bash
STARS=$(wpsnote-cli search --note_id "$NOTE_ID" --query "***" --json)
```

若找到 `***`，读取其前后 3 个 block，生成补全内容后替换：

```bash
wpsnote-cli edit --json-args "{
  \"note_id\": \"$NOTE_ID\",
  \"op\": \"replace\",
  \"block_id\": \"$STAR_BLOCK\",
  \"content\": \"<p>补全后的内容</p>\"
}"
```

### Step 12：更新状态文件

```python
if new_sentences:
    state["last_end_time"] = new_sentences[-1]["end_time"]
    state["summary_anchor_id"] = last_inserted_block_id
    if state["temp_zone_anchor_id"] is None and temp_zone_block_id:
        state["temp_zone_anchor_id"] = temp_zone_block_id
state["round"] += 1
json.dump(state, open(state_path, "w"), ensure_ascii=False)
```

### Step 13：输出本轮简报

```
✓ 第 3 轮完成（新增 18 句 / 142 秒 → 摘要 +85 字）
  场景：会议记录  发言人：张总、李工❓
  人名联动：张总→《Q4 复盘》、李工→未找到
  行动项：+2 条  ***补全：1 处  临时区合并：1 条
  下一轮：60 秒后
```

---

## 场景识别表

| 场景关键词 | 场景类型 | 使用模板 |
|-----------|---------|---------|
| 会议、讨论、周会、评审 | 会议记录 | 会议纪要模板 |
| 课堂、授课、教学、老师 | 课堂笔记 | 课堂笔记模板 |
| 培训、讲师、学员 | 培训课程 | 培训课程模板 |
| 知识分享、分享会、经验分享 | 知识分享 | 知识分享模板 |
| 直播、主播、观众 | 直播内容 | 直播记录模板 |
| 播客、嘉宾、节目 | 播客/视频 | 播客纪要模板 |
| 采访、记者、被采访 | 采访记录 | 采访记录模板 |
| 谈判、甲方、乙方、合同 | 商务谈判 | 商务谈判模板 |
| 复盘、总结、里程碑 | 项目复盘 | 项目复盘模板 |
| 庭审、原告、被告、法庭 | 庭审记录 | 庭审纪要模板 |
| 患者、诊断、医嘱、症状 | 病例记录 | 病例记录模板 |
| 口述、文章、博客 | 口述转文章 | 文章模板 |
| 电话、通话、客服 | 电话录音 | 电话记录模板 |
| 无明显特征 | 通用场景 | 通用转写模板 |

---

## 排版规范

默认使用富文本排版。用户明确说「纯文本」「不要排版」时才退回普通段落。

### 色块颜色语义

`columnBackgroundColor`：
- 蓝色 `#EBF2FF`：中性信息、发言人观点
- 绿色 `#E8FCEF`：结论、共识
- 黄色 `#FFF5EB`：注意事项、待确认
- 红色 `#FFECEB`：风险、问题、争议点
- 紫色 `#FAF0FF`：补充信息、延伸内容

```xml
<columns>
  <column columnBackgroundColor="#EBF2FF">
    <h4>发言人 · 身份信息</h4>
    <p listType="bullet" listLevel="0">要点一</p>
    <blockquote>「原话片段」</blockquote>
  </column>
</columns>
```

### 使用判断

- **用色块**：有明确发言人且 2+ 条观点；一个主题超过 3 条要点
- **不用色块**：只有 1 条信息；行动项/Todo；内容少结构简单时
- **双栏**：仅用于内容天然对立的场景（谈判双方、优缺点对比）

### 结构原则

先按主题/议题分 `h2`/`h3` 章节，再在章节内用色块区分发言人：

```
h2 主题一
  ├── columns(蓝) 发言人 A
  ├── columns(蓝) 发言人 B
  └── columns(绿) 结论/共识
h2 行动项
  └── todo list（不套色块）
```

---

## 场景模板

各模板均遵循「严格基于转写、跳过空章节、默认富文本排版」原则。

| 场景 | 主结构 | 特殊要求 |
|------|--------|---------|
| 通用 | h2摘要 → h3主题 → columns(蓝) → todo | — |
| 会议纪要 | h2纪要 → h3议题 → columns(蓝)发言人 → columns(绿)结论 → todo | 含参会人、决策标注 |
| 课堂笔记 | h2笔记 → h3知识点 → h4细节 → h3重点 → todo作业 | 无色块，以层级代替 |
| 知识分享 | h2记录 → h3核心知识 → h4知识点 → h3要点 → todo学习 | — |
| 直播/播客 | h2纪要 → h3主题 → columns(黄)嘉宾A → columns(蓝)嘉宾B | 注明嘉宾身份 |
| 商务谈判 | h2记录 → h3议题 → 双栏(蓝/红)甲乙方 → columns(绿)协议 → todo | 双栏对立布局 |
| 项目复盘 | h2复盘 → h3成果 → h3问题 → h3经验 → todo改进 | 量化成果 |
| 庭审/病例/采访/电话/培训 | 按各专业流程顺序组织，见下方说明 | — |

**专业场景结构**：
- **庭审**：庭前准备 → 法庭调查 → 举证质证 → 法庭辩论 → 最后陈述
- **病例**：主诉 → 现病史 → 诊断 → 治疗方案 → 医嘱
- **采访**：5W1H要素 → 精彩引用 → 后续跟进
- **电话录音**：通话目的 → 讨论内容 → 承诺事项 → 后续行动
- **培训课程**：课程大纲 → 知识点 → 实践练习 → 课后作业
- **口述转文章**：引言 → 章节 → 结论（口语转书面语）

> 完整 XML 模板见 [templates.md](templates.md)

---

## Todo 提取规则

从新增转写中识别任务：

1. **明确任务**：含动作动词（完成、提交、准备、跟进）+ 时间限定或责任人
2. **承诺事项**：「我会/我们将...」「XX 时候给您...」
3. **学习任务**：「需要学习/实践/应用...」

```xml
<p listType="todo" listLevel="0" checked="0">[任务]（负责人：XX，截止：XX）</p>
```

---

## 停止条件

- 用户明确说「停止」「结束总结」「stop」
- 连续 **5 轮**无新增转写
- 音频 `status=stopped` 且已完成最终总结

停止时清理状态文件：`rm /tmp/lts_state_{note_id}.json`

---

## 错误处理

| 错误 | 处理方式 |
|------|---------|
| CLI 不可用 | 退回 MCP 模式 |
| `NO_ACTIVE_EDITOR_WINDOW` | 提示用户打开笔记，等待 30 秒后重试 |
| `WEBSOCKET_NOT_CONNECTED` | 等待 10 秒后重试转写获取 |
| `EDITOR_NOT_READY` | 等待 2 秒后重试写入 |
| `BLOCK_NOT_FOUND` | 用 `outline` 刷新 ID 后重试；检查 `content` 是否为字符串 |
| `DOCUMENT_READ_ONLY` | 告知用户笔记为只读，停止写入但继续读取 |
| 转写返回空 | 等待 30 秒（可能正在转写中）后重试 |
| 写入反复失败 | **检查 `content` 是否为 XML 字符串**，不能是数组/对象；刷新 block_id 后重试 |
