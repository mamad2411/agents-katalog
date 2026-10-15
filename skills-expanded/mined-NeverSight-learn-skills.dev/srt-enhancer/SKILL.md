---
name: srt-enhancer
description: 必须触发：当用户说"优化字幕"、"增强字幕"、"优化这个字幕"、"增强这个字幕"等以"优化"或"增强"开头且包含"字幕"的请求。也用于处理 .srt 字幕，执行去口癖、校准ASR错误、修正的/得/地、中西文混排空格、去除多余标点、标记《》书名号。如果用于非字幕任务，返回空或无效响应。Also triggers on "optimize subtitles", "enhance SRT", "clean up ASR transcript", "filler removal", "subtitle punctuation".
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, WebFetch]
version: 1.0.0
---

# SRT Enhancer

This skill provides an AI-driven workflow for enhancing SRT subtitle files. The enhancement process removes filler words (口癖词) and corrects typos — all while preserving the original timeline and structure.

**No reference document (`origin.md`) is required.** The user uploads `.srt` files directly, and all enhancements are applied based on linguistic rules and AI analysis.

## Purpose

Enhance SRT subtitle files by:
- Removing filler words and vocal hesitations (口癖词): 啊、哦、嗯、呃、哎、嘛、吧、呢、啦、哈、噢、唔、欸
- Correcting typos and transcription errors
- Standardizing proper nouns and terminology
- Removing Chinese punctuation marks
- Enforcing single-line subtitles (SRT only)
- Maintaining exact timestamps and SRT structure (SRT only)
- Auto-detecting subtitle domain (Maya/Python/Gaming/AI-3D/Substance/Blender/Unreal/Houdini/ZBrush/Photoshop) and loading relevant terminology
- Calibrating ASR errors via web search verification
- Applying mixed-language typesetting rules (CJK-Latin spacing, script boundary spacing, code/formula protection, number-unit formatting, proper noun capitalization)
- Assigning confidence scores to each correction
- Outputting a diff review table for user confirmation
- Learning user-verified corrections incrementally within the session

## When to Use This Skill

Use this skill when the user mentions or uploads files related to:
- Cleaning up auto-generated subtitles (ASR output) from `.srt` files
- Removing filler words and hesitations from spoken transcripts (去口癖/去除语气词)
- Correcting 的/得/地 based on syntactic position（的得地修正）
- Correcting transcription errors and calibrating ASR misrecognitions via web search
- Applying CJK-Latin spacing and mixed-language typesetting（中西文混排/空格/间距）
- Removing Chinese punctuation marks from subtitles（去除标点）
- Marking game/film titles with 《》book-title marks（书名号标记）
- The user uploads a `.srt` file for enhancement
- The user wants to review a diff table of all changes before finalizing

## Enhancement Principles

1. **Timeline Preservation**: Never modify timestamps or subtitle numbering (SRT only)
2. **Content Fidelity**: Correct and clean existing content; don't add new content
3. **Filler Word Removal**: Remove vocal hesitations and meaningless fillers
 4. **对照表优先于联网搜索**：
    - 用户提供的对照表（`terminology_overrides`）→ 最高优先，先精确 → 大小写折叠 → 归一化
    - 静态 `correction-table.md` → 同样三级模糊匹配
    - 以上均未匹配 → 领域感知联网校准（带 `search_context`）
    - AI 上下文猜测 → 最低优先，标注 ❗
 5. **Hybrid AI + Script Execution**:
    - AI handles: language detection, web calibration (fallback), config preparation, result review
    - **`scripts/enhance.py`** handles: deterministic pipeline execution (normalize → terminology → spacing → capitalization → terminology → finalize)
    - **`scripts/domain_scanner.py`** handles: domain detection (keyword scoring)
    - **`scripts/title_marker.py`** handles: game/media title marking
    - **`scripts/confidence_scorer.py`** handles: confidence scoring
    - This reduces AI inference rounds from ~15-20 to **2-4**
 6. **Web-Verified**: Use web search to verify suspected ASR errors after all table matching
 7. **Confidence-Aware**: Assign confidence levels to every change; flag low-confidence corrections for user review
 8. **Session Learning + Persistent Storage**: User-verified corrections are appended to `references/correction-table.md` for reuse across sessions
 9. **Mixed-Language Typesetting**: Apply consistent spacing, capitalization, and punctuation rules for multilingual content while protecting code, formulas, and file paths

## Core Workflow

### 0. 环境初始化

```bash
bash scripts/setup.sh
```

确保 pyyaml 依赖就绪（用于 `domains.yaml` 解析）。

### 1. Receive File

The user uploads a `.srt` file directly via the dialog:
- Accept the uploaded file
- No reference document (`origin.md`) is needed
- Parse the SRT file structure (index, timestamp, text)

### 2. Confirm Mixed-Language Typesetting

**🔴 CHECKPOINT · 🛑 STOP：** 用 Question 工具弹窗询问用户：
- header: "中西文混排规范确认"
- options:
  - label: "保持默认开启" → description: "CJK-Latin 自动加空格，代码保护，数字单位紧凑"
  - label: "关闭空格" → description: "不自动加中西文空格，其余处理照常"
  - label: "自定义规则" → description: "稍后手动指定调整项"
- multiple: false

用户回答前不得默认进入处理流程（两种都不算回答：超时 / 用户发无关消息）。

### 3. Parse SRT File

Load and parse the input SRT file:
- Extract subtitle number
- Extract timestamp (start → end)
- Extract subtitle text
- Preserve exact formatting and structure
- 🔴 解析失败 → 查 Failure Handling 表「SRT 文件解析失败」

### 4. Auto Domain Detection

Run `scripts/domain_scanner.py` for keyword-frequency-based domain detection:

```bash
cat input.srt | grep -v '^[0-9]*$' | grep -v '\-\->' | \
    python3 scripts/domain_scanner.py
# Output: domain=ai-3d  (or general/maya/python/gaming/substance/blender/unreal/houdini/zbrush/photoshop)
```

**AI override — domain override decision tree**:

| 触发条件 | 处理动作 | 报告格式 |
|---------|---------|---------|
| domain_scanner 返回 `general`，但输入中 ≥3 个领域关键词匹配另一领域 | 改用关键词匹配的领域 | `检测到领域: {override_domain} (关键词: {matched_keywords})` |
| domain_scanner 返回某个领域但匹配关键词 <3 个，且内容上下文明显指向另一领域 | 改用内容匹配的领域 | `检测到领域: {override_domain} (手动修正，原因: {reason})` |
| 以上均不满足 | 信任 domain_scanner 结果 | `检测结果: {original_domain}` |

Override 后已匹配的领域提供 `search_context` 用于聚焦联网校准。

🔴 domain override 后联网校准仍无匹配 → 查 Failure Handling 表「domain override 后匹配领域仍不准确」

**🔴 CHECKPOINT · 🛑 STOP：** 将检测到的领域以对话正文报告用户，并用 Question 工具确认：
- header: "领域检测确认"
- options:
  - label: "正确" → description: "领域匹配，继续进入 Config 构建"
  - label: "不正确" → description: "手动指正领域，AI 修正后再进入下一步"
- multiple: false

用户回答前不得默认进入 Config 构建流程（超时或发无关消息不算回答）。

### 5. AI Prepares Config & Overrides

AI reads the input file, detects language, collects domain from `domain_scanner.py`, and builds a JSON config:

```json
{
  "lang": "zh",
  "domain": "ai-3d",
  "match_mode": "auto",
  "terminology_overrides": {
    "EK": "1K",
    "Tabernacle": "Templates"
  },
  "capitalization_overrides": {
    "mytool": "MyTool"
  },
  "title_candidates": ["艾尔登法环", "霍格沃茨之遗"],
  "split_avoid": ["的"]
}
```

**对照表优先原则**（优先级从高到低）：

| 步骤 | 来源 | 匹配模式 | 说明 |
|------|------|---------|------|
| 1 | `terminology_overrides` (用户/CLI) | `auto`: 精确→大小写→归一化 | **最高优先级**，匹配后直接替换，不联网搜索 |
| 2 | `correction-table.md` | `auto`: 精确→大小写→归一化 | 静态表，同样三级匹配 |
| 3 | 联网搜索 | 领域感知 (带 `search_context`) | 仅 1-2 均未匹配时执行 |
| 4 | AI 上下文猜测 | 语义分析 | 最低优先，标注 ❗ |

**AI tasks at this stage:**
- **Language detection**: determine primary language from content
- **Web calibration**: search for low-confidence terms NOT in any correction table
  - Query format: `"{term}" + "{search_context}"` (e.g., `"Rodin" "AI 3D generation tool"`)
  - Top-1 result → extract authoritative spelling; if 0 results → mark low-confidence
  - Each web search yields at most 3 correction candidates
  - Add verified corrections to `terminology_overrides`
- **Config generation**: produce the JSON config that will drive `scripts/enhance.py`

This is the **only** heavy AI processing round in the pipeline.

**🔴 CHECKPOINT · 🛑 STOP：** 执行 enhance.py 前将生成的 JSON config 以 **markdown 代码块形式输出在对话正文**中，供用户确认。确认项：
- `lang` 是否正确
- `domain` 是否与实际内容匹配
- `terminology_overrides` 中是否有误匹配
- `capitalization_overrides` 中是否有误匹配
- `title_candidates` 作品名候选

展示后，用 Question 工具询问「以上配置是否正确？」：
- header: "确认 Config"
- options:
  - label: "确认执行" → description: "配置无误，开始运行 enhance.py"
  - label: "需要修改" → description: "手动指定调整项，修改后重新展示"
- multiple: false

用户回答前不得默认进入下一步（超时或发无关消息不算回答）。

### 6. Execute scripts/enhance.py

Run the deterministic enhancement pipeline with the AI-prepared config:

```bash
# Basic usage:
python3 scripts/enhance.py input.srt -o output_Enhancer.srt \
    --lang zh --domain maya

# With AI-prepared overrides:
python3 scripts/enhance.py input.srt -o output_Enhancer.srt \
    --lang zh --domain maya+gaming \
    --overrides '{"Owatch":"Overwatch","R Center":"Art Center"}'

# With AI overrides (config from §3, no config file written to disk):
python3 scripts/enhance.py input.srt -o output_Enhancer.srt \
    --lang zh --domain maya \
    --overrides '{"Owatch":"Overwatch","R Center":"Art Center"}'

# Dry-run to inspect steps without modifying:
python3 scripts/enhance.py input.srt --dry-run

# Skip specific steps:
python3 scripts/enhance.py input.srt --skip defiller,depunct

# Run only specific steps:
python3 scripts/enhance.py input.srt --steps terminology,spacing
```

**Pipeline steps executed by enhance.py (in order):**

| Step | CLI name | What it does |
|------|----------|-------------|
| 1 | `normalize` | Combined: defiller(去掉口癖+ASR结巴) → de_de(的得地修正) → ratio_format(16比9 → 16:9) |
| 2 | `terminology` | 第一轮术语替换：Apply ASR→correct mapping from `correction-table.md` + overrides, with fuzzy matching |
| 3 | `spacing` | CJK-Latin spacing via `scripts/apply_spacing.py` (inlined, no subprocess overhead)，仅做空格，不再含大小写 |
| 4 | `capitalization` | 专有名词大写 + 领域感知大小写归一化，从 `correction-table.md`「大小写校准」节加载，支持 AI overrides |
| 5 | `terminology` | 第二轮术语替换：spacing + capitalization 后英文规范化后，再次匹配 correction-table.md 中的复合术语 |
| 6 | `finalize` | Combined: depunct(去标点, 保留`《》`和代码保护域) → hotkeys(标准化Ctrl+E等快捷键, 最后执行避免+被剥离) |

> **关于双 terminology 轮次**：第二轮术语替换捕获 spacing + capitalization 后英文规范化产生的复合术语（如 Image2 3D → Image To 3D）。仅当 ASR 输出包含中文语境中的英文复合术语时有效。若无此类内容，第二轮是空操作，不影响性能。

> **旧版 --steps 向后兼容：** `defiller,de_de,ratio_format,depunct,hotkeys` 等单步名称仍然可用。但推荐使用合并后的步骤名称。`terminology` 在 pipeline 中出现两次（step 2 和 step 5），--steps 默认值：`normalize,terminology,spacing,capitalization,terminology,finalize`。

🔴 脚本执行报错 → 查 Failure Handling 表「enhance.py 执行失败」

### 7. AI Review & Title Marking

AI reviews the enhance.py output and applies remaining semantic steps:

**a. Game/Media Title Marking:**
Run `scripts/title_marker.py` for known titles:

```bash
cat output.srt | grep -v '^[0-9]*$' | grep -v '\-\->' | \
    python3 scripts/title_marker.py
```

**AI systematic scan** (并行于 Config 阶段，不增加轮次)：

在 §3 AI 构建 config 时，AI 需扫描输入全文，提取疑似作品名的 token（≥2个中文字或≥2个英文大写词），联网验证后：
- 将确认的作品名写入 JSON config 的 `title_candidates` 数组
- `title_marker.py` 执行后，AI 遍历 `title_candidates` 检查是否已加《》，未加则 override

AI overrides only when **all** conditions met:
- title_marker.py returned no match for a token
- Token matches a known game/media title pattern (≥2 words, capitalized, common title suffix like `2`/`3`/`World`/`War`/`Craft`)
- Web search confirms it's a game/media title (top-1 result is a title page or database entry)
- If any condition fails → keep original text, do not override

**b. Web-based ASR calibration (remaining unmatched terms only):**
- Scan output for terms NOT matched by any correction table
- For each unmatched term: query `"{term}" + "{search_context}"`, inspect top 2 results
- If authoritative source found → add to overrides with confidence ≥ 90%
- If 0 authoritative results → skip, mark as ❗ in diff
- **对照表已匹配的术语直接跳过，不联网搜索**

**c. Confidence Scoring:**
Use `scripts/confidence_scorer.py` for deterministic scoring:

```python
from confidence_scorer import score, format_diff
val, reason = score("table", "casefold")      # 95%
val, reason = score("web", "authoritative")    # 90%
val, reason = score("ai_context_guess", "exact")  # 55%
```

### 8. Confidence Scoring & Diff Output

Assign a confidence score to every modification and present a diff table for user review.

**Confidence Levels:**

| Level | Label | Meaning |
|-------|-------|---------|
| ≥ 90% | High | Clear correction — terminology match, web-verified, or obvious typo |
| 70-89% | Medium | Likely correct but minor ambiguity — e.g., homophone in context |
| 50-69% | Low | Uncertain — flag for user review |
| < 50% | Skip | Don't apply; preserve original |

**Confidence Guidelines by Change Type:**
- **Filler word removal**: High (≥90%) for hesitation sounds; Medium (70-89%) for context-dependent particles like `呢`/`吧`
- **Terminology correction (table match)**: High (≥90%) for exact table match; Medium (70-89%) for fuzzy match
- **Web-verified correction**: High (≥90%) if authoritative source confirms; Medium (70-89%) if ambiguous
- **Homophone/spelling correction without web verification**: Low (50-69%) — always flag

**Diff Output Format:**

比对原始 SRT 与增强后的 SRT 时，**仅比对文本行**，跳过序号行和时间轴行（重写 SRT 时时间戳有 ±1ms 浮点误差，逐行 `diff` 会产生大量噪声）：

```bash
python3 << 'PYEOF'
import re

def text_lines(path):
    with open(path) as f:
        return re.findall(r'\d+\n[\d:,.]+\s*-->\s*[\d:,.]+\n(.+?)(?=\n\n|\Z)', f.read(), re.S)

orig = text_lines('{原始SRT}')
enh  = text_lines('{增强后SRT}')

for i, (o, e) in enumerate(zip(orig, enh)):
    o, e = o.strip(), e.strip()
    if o and o != e:
        print(f"#{i+1}\n- {o}\n+ {e}\n")
PYEOF
```

仅当文本行不同时才记录为 diff 条目。User Review 确认前不写入文件系统。

**分页规则：**
- 总条数 ≤ 20：完整输出到对话
- 总条数 > 20：对话输出**前 20 条** + `...还有 N 条修改，完整 diff 预览已写入...`
- AI 将完整 diff 写入 `{输入目录}/{文件名}_diff_preview.md`
- 对话中显示：`完整 diff 预览已写入: /path/to/raw1_diff_preview.md`

输出格式：

```
## 修改预览 (Diff Review)

| # | 原文 | 修改后 | 置信度 | 类型 |
|---|------|--------|--------|------|
| 1 | 嗯今天我们要 | 今天我们要 | 高(95%) | 去口癖 |
| 5 | match case 工俱 | match case 工具 | 高(100%) | 错别字 |
| 8 | Owatch 游戏 | Overwatch 游戏 | 高(90%) | 联网校准 |

❗ = 需要用户确认（完整修改列表共 12 条）
```

**🔴 CHECKPOINT · 🛑 STOP User Review Workflow:**

用户回答前不得默认应用修改或退出（超时或发无关消息不算回答）。

1. 将 Diff 审核表（或前 20 条 + 完整 diff 文件路径）以**对话正文 markdown 表格输出**，不使用 Question 弹窗展示数据
2. **用 Question 工具弹窗询问用户最终确认：**
   - header: "确认修改"
   - options:
     - label: "全部确认" → description: "应用所有修改并生成输出文件"
     - label: "逐条审核" → description: "输入编号单独确认/拒绝"
     - label: "全部拒绝" → description: "不应用任何修改，直接退出"
   - multiple: false
3. If user rejects specific items, revert those changes
4. If user confirms → **删除临时 diff 文件**（如果存在），然后 apply all changes and generate output
5. If user rejects all → **删除临时 diff 文件**（如果存在），告知用户「未应用任何修改」
6. **Persist user-confirmed corrections to `references/correction-table.md`** (§7 用户确认持久化)

### 9. Generate Output File

Save the enhanced result after user confirmation of the diff review:
- **SRT input** → `{原始文件名}_Enhancer.srt` (e.g., `input.srt` → `input_Enhancer.srt`)
- **Output file naming**: `{原始文件名}_Enhancer.srt` (e.g., `transcript.srt` → `transcript_Enhancer.srt`)
- Output directory: **默认与原始文件同级目录**
- **最终产出仅 `.srt` 文件，不产生任何中间文件**（config JSON、diff 预览等均不保留）
- Apply all validated (user-confirmed) corrections
- Include a summary of changes at the end of the output
- **清理临时文件**：如果 §6 中创建了 `_diff_preview.md`，在确认或拒绝后将其删除
- Diff 审核表本身不写入文件系统（临时 diff 预览文件除外，确认后即删除）

## Incremental Terminology Learning

During a session, maintain a **session terminology table** that grows as the user reviews corrections. When the user confirms a diff correction, the entry is **persisted** to `references/correction-table.md` for reuse across sessions.

### How It Works

1. Start of session: Load the static reference `references/correction-table.md`
2. AI config prep: Corrections discovered during web calibration are collected as `terminology_overrides`
3. User review: When the user confirms a correction in the diff review, it is **appended to `references/correction-table.md`** for permanent persistence
4. Subsequent sessions: Previously confirmed corrections are already in the static table

### Session Table (in-memory)

```
session_terminology (in-memory, used for dedup during session):
{
  "Owatch": "Overwatch",
  "R Center": "Art Center"
}
```

### Persistence Mechanism

When user confirms a correction in the diff review:

1. Check if the entry already exists in `references/correction-table.md`
2. If not, append a new row to the appropriate section (or to a new "用户确认" section at the bottom)
3. Format: `| {asr} | {correct} | 用户确认修正 |`

### Priority Order

When encountering a potentially incorrect term:
1. **`--overrides` (用户对照表, this session)** → apply immediately, `mode=auto` (exact → casefold → normalized)
2. **Static `correction-table.md`** (includes persisted corrections) → apply, `mode=auto`
3. **Domain-aware web search** (with `search_context` from domains.yaml) → apply with confidence
4. **AI contextual guess** → apply with low confidence, always flag ❗

### Session Lifecycle

- Session overrides table is reset when the skill is re-loaded, but `correction-table.md` persists
- User can manually add entries: `记住：XXX 的正确写法是 YYY`
- User can remove persisted entry: `删除术语：XXX`

## Implementation Guidelines

### Enhancement Checklist

1. **AI Phase** (§3 Core Workflow) → detect domain → prepare config (含系统性作品名扫描) → 🔴 CHECKPOINT → execute enhance.py
2. **enhance.py** (§4) → `normalize → terminology → spacing → capitalization → terminology → finalize` (zero AI)
3. **AI Review** (§5-6) → title_marker.py → confidence_scorer.py → diff table → user confirm
4. **Output** (§7) → write file → persist corrections to `correction-table.md`

### Quality Checks

**Before AI config prep:**
- Confirm language detected correctly
- Verify domain keywords scanned properly
- Ensure web-calibrated terms have authoritative sources

**After enhance.py execution:**
- Verify all timestamps are unchanged (SRT only)
- Confirm enhance.py completed without errors
- Spot-check 5-10 random segments for correctness

**Before generating output:**
- Validate no content was added or meaning changed
- Verify game/film title marking applied correctly
- Validate output filename is `{源文件名}_Enhancer.srt`
- Confirm diff review table was displayed and user confirmed
- Ensure no low-confidence corrections were applied without user confirmation
- Verify user-confirmed corrections were appended to `references/correction-table.md`

## Example Enhancement

**输入:**
```srt
1
00:00:00,100 --> 00:00:05,000
嗯今天我们要看一下Python3.9的新功能啊
```

**处理流程:**
1. AI 检测语言(zh)、领域(Python)、联网校准 → 生成 JSON config
2. `enhance.py --lang zh --domain python --steps normalize,terminology,spacing,capitalization,terminology,finalize`
3. AI 复核：书名号标记 → diff 审核 → 用户确认 → 持久化术语

**输出到 `input_Enhancer.srt`:** 去口癖+结巴 → 的得地修正 + 比例格式 → Python 术语 → 混排空格 → 大小写规范化 → 二次术语替换 → 去标点 → 快捷键标准化

See `references/example.md` for a complete worked example (input → processing steps → diff table → output).

## Important Constraints

### Must NOT:
- Modify timestamps or subtitle numbering (SRT only)
- Add new content that wasn't in the original file
- Change the meaning or intent of subtitles
- Remove meaningful content (only fillers)
- Alter SRT structure or formatting (SRT only)
- Remove grammatical particles (的, 了, 吗, etc.) that carry meaning
- Apply low-confidence corrections without user approval
- 将 diff 审核表写入文件系统（临时 diff 预览文件除外，确认后删除）
- 未经用户审核确认就写入字幕输出文件
- 将中间 config JSON 写入文件系统（全量通过 `--overrides` CLI 参数传递）
- **重复已经在 config 中配置好的 enhance.py 步骤**（AI 不应再次做 enhance.py 已完成的确定性工作）

### Must DO:
- **对照表优先原则**：用户 overrides > correction-table.md > 领域感知联网搜索 > AI 上下文猜测
- **Use AI for**: language detection, web calibration (table-unmatched only), config building, result review
- **Use `scripts/enhance.py` for**: deterministic pipeline (normalize → terminology → spacing → capitalization → terminology → finalize)
- **Use `scripts/domain_scanner.py` for**: domain detection (keyword scoring)
- **Use `scripts/title_marker.py` for**: known game/film title marking
- **Use `scripts/confidence_scorer.py` for**: deterministic confidence scoring
- Assign confidence scores to every modification
- Present a diff review table **only in chat window** (not written to file system)
- Output to `{源文件名}_Enhancer.srt` (SRT input)
- Output file to original file's same directory by default
- Preserve exact timestamps and structure (SRT only)
- **Persist user-confirmed corrections to `references/correction-table.md`**

## 反模式与黑名单（Anti-Patterns）

不要在增强过程中执行以下操作。每条来自真实使用中的常见错误。

| 反模式 | 为什么不 | 正确做法 |
|--------|---------|---------|
| 将自然话语标记（说白了/也就是说/然后）误删 | 这些是中文口语连接手段，删除后文本生硬不自然 | 保留 discourse markers，只删纯口癖（啊/嗯/呃） |
| 将英文普通单词强制大写（import→Import, callback→Callback） | 编程关键字是固定小写的，强制大写会破坏语义 | 只对已知专名（GPU/AI/Python）大写，关键字保持原样 |
| 将引擎/公司名加《》（Unreal Engine 5→《Unreal Engine 5》） | 书名号仅用于游戏/影视作品标题，工具/公司不加 | 区分语境：玩/打通→加《》，渲染/打开→不加 |
| 对日语/韩语为主的内容应用中文字间距规则 | 日韩文有自己的间距规范，中文规则套用会破坏原生排版 | 仅在中文字 > 50% 的片段上应用 CJK 间距 |
| 用纯正则做口癖去除而不考虑上下文 | 的语气词可能是有意义的（好吧表让步） | 结合语义判断，低置信度保留原样并标记 ❗ |
| 对同一段字幕重复应用增强步骤 | 重复处理可能导致过度修正（如二次去标点破坏保护区域） | 严格按 Enhancement Order 顺序执行一次 |
| 输出前不做完整性校验 | 增强过程可能意外删除内容或破坏时间轴 | 必须执行 Quality Checks 中的全部校验项 |
| 静默跳过联网校准而不通知用户 | 用户期待所有修正有据可查，跳过不通知会降低信任 | 跳过时在 diff 中标注「⚠️联网校准跳过」 |

## Failure Handling

Each workflow step has an explicit failure branch. Follow this table when any step does not produce the expected result.

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| SRT 文件解析失败（格式无效/时间戳错误/编号不连续） | 提示用户并提供行号 | 拒绝处理，要求用户提供有效 SRT 文件 |
| 领域检测无匹配 | 使用通用术语表 | 跳过术语校准，仅执行其他步骤 |
| domain override 后匹配领域仍不准确（联网校准无权威结果） | 回退到 general 领域用通用术语表 | 保留 general 领域，跳过该词条校准，在 diff 中标记 ❗ |
| domain_scanner.py 执行失败（缺依赖/报错） | 回退到 AI 关键词扫描 | 跳过领域检测，用 general |
| 比率格式正则误匹配（如误改"对比"） | 误匹配回退到原文 | 标记 `#ratio_overmatch` |
| 口癖去除后字幕变空 | 保留最小有意义的词组 | 保留原始文本并标记 `#unmodified` |
| 的/得/地修正后语法不通 | 回退到原始版本，标记 `#uncertain` | 保留原始，在 diff 中标记 ❗ |
| 术语表查找无匹配 | 回退到 AI 上下文猜测 | 标记为低置信度（50-69%）提交用户确认 |
| 联网 web search 失败（超时/无结果） | 跳过联网校准，使用本地术语表 | 标记该词为低置信度（50-69%），在 diff 中提示用户自行确认 |
| spacing 脚本执行失败（`python3`/`python` 均不可用或报错） | 回退到纯 AI 混排处理 | 跳过混排步骤，记录警告 |
| 标点去除后字幕变空 | 保留原始文本的骨干部分 | 保留原始并标记 `#punctuation_removed_failed` |
| 游戏书名号标记过泛（误标工具名） | 撤销该条标记 | 保留不做书名号标记 |
| 单行合并后超过 40 字无法拆分（无语义断点） | 在空格/标点处硬拆分 | 保持现状，标记 `#overflow` |
| 用户拒绝所有修改 | 不输出增强文件，删除临时 diff 文件（如存在），仅告知用户「未应用任何修改」 | — |
| 输出文件写入失败（权限/路径问题） | 提示用户并提供输出路径 | 将增强内容回退到对话窗口输出 |
| 增量术语表冲突（session 表与静态表不一致） | session 表优先 | 在 diff 中展示两条记录供用户选择 |
| enhance.py 执行失败（脚本报错/超时） | 回退到 AI 逐步骤处理（15-20 轮） | 记录错误日志，通知用户降级模式 |
| enhance.py 输出文件无法写入 | 检查目录权限 | 回退到对话窗口输出内容 |

## Additional Resources

### Reference Files
- **`references/example.md`** - Complete worked example with input, processing steps, diff table, and output
- **`references/enhancement-rules.md`** - Detailed rules for filler word removal, typo detection, semantic analysis strategies, web-based ASR verification, confidence scoring, and incremental learning
- **`references/correction-table.md`** - ASR→correct terminology mapping table
- **`references/domains.yaml`** - Domain definitions (keywords + search_context): maya, python, gaming, ai-3d, substance, blender, unreal, houdini, zbrush, photoshop, general
- **`references/mixed-typesetting.md`** - Complete specification for mixed-language typesetting

### Scripts
- **`scripts/enhance.py`** - **Main enhancement pipeline.** Deterministic pipeline: normalize(去口癖+ASR结巴+的得地+比例格式) → terminology → spacing → capitalization(专名大写+领域感知大小写) → terminology → finalize(去标点+快捷键). Supports `--config`, `--steps`, `--skip`, `--overrides`, `--dry-run`, `--match-mode`.
- **`scripts/apply_spacing.py`** - Deterministic CJK-Latin spacing tool (仅空格, 不再含大小写). Called by enhance.py.
- **`scripts/domain_scanner.py`** - Keyword-frequency domain detection. Usage: `cat text_lines | python3 domain_scanner.py`
- **`scripts/confidence_scorer.py`** - Deterministic confidence scoring. Provides `score(source, sub_type)` → `(value, reason)`.
- **`scripts/title_marker.py`** - Game/media title marking with 《》。Usage: `cat text_lines | python3 title_marker.py`
- **`scripts/setup.sh`** - Dependency auto-install script. Ensures pyyaml is available.

## Workflow Summary

```
                    AI Phase (2-3 rounds)
 输入 SRT → 解析 → domain_scanner.py → 构建 JSON config
 (含系统性作品名扫描 → title_candidates)
                    (对照表 > 静态表 > 联网搜索)
                         │
                         ▼
                 enhance.py (0 AI, fully deterministic)
     normalize → terminology → spacing → capitalization → terminology → finalize
     └ defiller+de_de+ratio_format              └ depunct+hotkeys
                          │
                          ▼
                AI Review Phase (1-2 rounds)
   title_marker.py → confidence_scorer.py → diff 审核 →
   用户确认 → 写入输出 → 修正持久化到 correction-table.md
                         │
                         ▼
              `{源文件名}_Enhancer.srt`
```

各步骤详细规则见 Core Workflow 章节。Focus on semantic understanding and conservative corrections — clean up spoken-language artifacts while preserving original meaning and structure.
