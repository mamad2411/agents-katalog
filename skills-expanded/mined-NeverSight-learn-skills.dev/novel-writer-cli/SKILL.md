---
name: novel-writer-cli
description: "AI 陪伴式长篇小说创作助手（CLI 版）。通过系统命令行调用 wpsnote-cli 操作 WPS 笔记，实现有记忆、懂上下文、不穿帮的持续创作。触发词：帮我写小说、我想写一部小说、继续写小说、写下一章、我有个故事想法、帮我创作。核心能力：冷启动建档（世界观+人物设定+AI生图）、按章写作、每次自动回顾上文防穿帮、全程归档 WPS 笔记。不适用于：短文、散文、诗歌等非长篇小说创作。"
---

# Novel Writer CLI — AI 小说创作助手（CLI 版）

> 核心设计哲学：用 WPS 笔记作为小说的"大脑"，AI 每次动笔前先"回忆"，写完后再"存档"。所有笔记操作通过系统命令行调用 `wpsnote-cli` 完成，用户只需给方向或提需求，其余全部自动完成。

---

## 前置检查：确认 wpsnote-cli 可用

启动本 Skill 的第一步，必须先检查 `wpsnote-cli` 是否可用：

```bash
wpsnote-cli status --json
```

**如果命令不存在或返回连接失败**，立即停止，告知用户：

> 这个功能需要配合 **WPS 笔记**使用。请按以下步骤开通：
>
> 1. 下载并安装 **WPS 笔记**应用（如已安装请跳过）
> 2. 打开应用后，点击**左下角的「设置」**
> 3. 进入 **「AI 实验室」**
> 4. 开通后重新发送你的需求，即可开始创作

开通后再次调用 `wpsnote-cli status --json` 确认连接正常，再继续后续流程。

---

## CLI 工具约定

所有 WPS 笔记操作直接在系统命令行中执行 `wpsnote-cli` 命令：

```bash
wpsnote-cli <子命令> [参数]
```

复杂参数（含 JSON、XML 内容）一律通过 `--json-args` 传入，避免 shell 转义问题：

```bash
wpsnote-cli <子命令> --json-args '{"key": "value", "content": "<p>XML内容</p>"}'
```

所有写操作加 `--json` 获取结构化返回值，方便提取 note_id / block_id。

---

## 命令速查表

| 操作 | CLI 命令 |
|------|---------|
| 搜索笔记 | `wpsnote-cli find --json-args '{"keyword":"...","tags":["#标签"]}'` |
| 读取全文 | `wpsnote-cli read --note_id <id> --json` |
| 获取大纲 | `wpsnote-cli outline --note_id <id> --json` |
| 读取指定 block | `wpsnote-cli read-blocks --json-args '{"note_id":"...","block_id":"...","after":5}'` |
| 搜索笔记内容 | `wpsnote-cli search --note_id <id> --query "关键词" --json` |
| 创建笔记 | `wpsnote-cli create --title "标题" --json` |
| 编辑单个 block | `wpsnote-cli edit --json-args '{"note_id":"...","op":"replace","block_id":"...","content":"<p>...</p>"}'` |
| 批量编辑 | `wpsnote-cli batch-edit --json-args '{"note_id":"...","operations":[...]}'` |
| 插入图片 | `wpsnote-cli insert-image --json-args '{"note_id":"...","anchor_id":"...","position":"after","src":"<url>","alt":"说明"}'` |
| 文生图 | `wpsnote-cli gen-image --prompt "描述" --width 1536 --height 2688 --json` |
| 查找标签 | `wpsnote-cli tags --keyword "标签名" --json` |
| 同步笔记 | `wpsnote-cli sync --note_id <id> --json` |

---

## 触发条件

满足以下任一条件即启动本 Skill：
- 用户说"帮我写小说"、"我想写一部..."、"续写下一章"、"继续我的小说"
- 用户描述了一个故事想法或梗概
- 用户说"我有个故事想写"、"帮我创作一个关于..."的长篇内容

---

## 笔记标签体系

每部小说独立一套标签树，多级标签用 `/` 分隔写入 WPS 笔记。

```
#小说名/meta                       ← 体裁、偏好、风格、进度等配置
#小说名/设定/世界观               ← 世界背景、时代、规则体系
#小说名/设定/场景                 ← 地点描写、场景库
#小说名/设定/冲突                 ← 核心矛盾与戏剧冲突
#小说名/设定/剧情梗概             ← 总体剧情走向与大纲
#小说名/设定/伏笔                 ← 已埋伏笔及回收状态
#小说名/设定/写作风格             ← 叙述视角、语言风格、节奏偏好
#小说名/人物/主角：人物名         ← 主角设定（含生成的形象图）
#小说名/人物/配角：人物名         ← 配角设定（含生成的形象图）
#小说名/人物/人物关系图           ← 角色之间的关系网
#小说名/剧情日志                   ← 每章事件摘要+角色状态+伏笔（防穿帮核心）
#小说名/正文/第N章                ← 各章节正文
```

标签写法（XML 格式）：`<tag>#小说名/设定/世界观</tag>`

---

## 沟通规范（每次操作必须遵守）

### 对话的唯一用途：提问 + 状态通知

AI 在对话中只能做两件事：
1. 提问：向用户确认信息时，必须给出备选项，不让用户面对空白输入框
2. 状态通知：告知正在执行什么操作（调用工具前一句话）、执行结果（章节写完的简报）

对话中绝对不能出现的内容：
- 小说正文（任何长度，哪怕一句话）
- 章节片段、示范段落、草稿
- 任何以"以下是...""正文如下..."开头的写作内容

### 提问规范：必须给备选项

每次向用户提问，必须附上 2–4 个备选项，用户可以直接选一个或在此基础上修改，不让用户面对空白发呆。

```
你希望这部小说是什么体裁？
A. 奇幻/玄幻（有魔法或特殊力量体系）
B. 都市/现代（贴近现实生活）
C. 科幻（未来、技术、星际）
D. 悬疑/推理（谜题、反转、破案）
→ 也可以直接告诉我你想要的风格
```

### 状态通知规范

调用任何 CLI 命令前，必须先说一句话告知用户，不允许沉默直接调用：
- 「好的，先去笔记里搜一下有没有这部小说的设定...」
- 「正在读取上一章的结尾，稍等...」
- 「开始创建世界观笔记...」
- 「正在存档，更新日志和角色状态...」

---

## 笔记结构规范

每篇笔记的结构：标题行 + 标签行 + 正文内容，标题和标签分开写，不混在一起。

对应 XML 写法：
```xml
<h1>笔记标题</h1>
<p><tag>#小说名/设定/世界观</tag></p>
<p>正文内容...</p>
```

---

## 两种启动模式

### 模式 A：冷启动（全新小说）

当以下命令未找到相关笔记时，进入冷启动：
```bash
wpsnote-cli find --keyword "小说名" --json
```

流程：
1. 向用户提 3 个带备选项的问题（故事方向、主角起点、写作节奏）
2. 根据回答 AI 自动推导所有设定
3. 依次创建设定笔记 → 生成人物图 → 写第一章 → 存档展示

### 模式 B：续写模式（已有笔记）

当找到对应小说标签的笔记时，直接加载上下文续写。

流程：
1. 加载 meta 笔记（获取风格约束）
2. 读取最新章节结尾（300–500 字）
3. 读取剧情日志（未回收伏笔、角色状态）
4. 如有用户特殊需求，检索相关设定笔记
5. 写作 → 存档 → 自动更新日志

---

## 冷启动详细流程

### Step 1：收集基础信息

AI 向用户提问，每个问题都必须附上备选项，用户可直接选或自由描述。全部问题收齐后，AI 自动推导所有设定，无需用户逐一确认。

问题 1：故事是关于什么的？
```
你的故事大概是什么方向？
A. 一个人在陌生/异世界的冒险与成长
B. 现代都市里的情感、阴谋或悬疑
C. 末世、星际或未来科技背景的生存/探索
D. 权谋、江湖、历史或古代架空
→ 也可以直接用一句话描述你的故事核心
```

问题 2：主角是什么样的人？
```
主角的起点是？
A. 普通人，被命运推着卷入事件，逐渐觉醒
B. 有天赋但有明显缺陷，需要经历磨砺
C. 已经足够强，故事聚焦更大的阴谋、牺牲或使命
D. 让 AI 根据故事背景自动决定
```

问题 3：你喜欢什么样的写作节奏？
```
偏好哪种风格？
A. 快节奏爽文，冲突密集，读着带劲
B. 慢热叙事，注重人物情感和内心刻画
C. 悬疑紧张，每章留钩子，让人想翻下一章
D. 随 AI 根据体裁自动匹配
```

用户回答后，AI 根据所有回答自动推导以下设定，不再追问：

| 设定项 | 推导依据 |
|--------|---------|
| 体裁 | 根据问题 1 回答自动判断 |
| 世界观 | 基于体裁和描述构建 |
| 主要冲突 | 从故事核心提炼 |
| 主角设定 | 结合问题 2 和体裁生成 |
| 叙述视角 | 默认第三人称有限视角（存入 meta） |
| 章节字数 | 根据体裁推导默认值（见下方字数规则），存入 meta |
| 语言风格 | 根据问题 3 和体裁判断，存入 meta |

章节字数推导规则：

| 体裁/偏好 | 默认目标字数 |
|----------|------------|
| 轻小说/网络爽文 | 2000–3000 字 |
| 奇幻/科幻/武侠 | 1500–2500 字 |
| 都市/言情/悬疑 | 1000–2000 字 |
| 纯文学/慢热风格 | 800–1500 字 |
| 用户明确指定 | 以用户指定为准 |

字数存入 meta 笔记后，每次写作前必须读取并作为硬约束执行。

---

### Step 2：创建设定笔记

#### 2-1：Meta 笔记

Meta 笔记是整部小说的**唯一索引中心**，存储所有子笔记的 note_id。后续所有流程应优先从 meta 索引读取 note_id，不再每次搜索。

```bash
# 创建笔记
wpsnote-cli create --title "《小说名》创作设定" --json
# → 获取 note_id（记为 META_ID）

# 写入内容（含笔记索引区块）
wpsnote-cli batch-edit --json-args '{
  "note_id": "<META_ID>",
  "operations": [{
    "op": "replace",
    "block_id": "<初始空block_id>",
    "content": "<h1>《小说名》创作设定</h1><p><tag>#小说名/meta</tag></p><h2>基本信息</h2><p>体裁：[奇幻/科幻/现代/悬疑...]</p><p>叙述视角：第三人称有限视角</p><p>语言风格：[沉稳/轻快/诗意/犀利...]</p><p>章节目标字数：[X–Y 字]</p><p>特殊禁忌：[用户不希望出现的内容，若无则写\"无\"]</p><h2>创作记录</h2><p>当前进度：第 0 章（待开始）</p><p>创作开始时间：[YYYY-MM-DD]</p><h2>笔记索引</h2><p>【meta】note_id = <META_ID></p><p>【世界观】note_id = （创建后填入）</p><p>【冲突设定】note_id = （创建后填入）</p><p>【剧情梗概】note_id = （创建后填入）</p><p>【伏笔日志】note_id = （创建后填入）</p><p>【剧情日志】note_id = （创建后填入）</p><h3>人物</h3><p>【人物：角色名】note_id = （创建后填入）</p><h3>场景</h3><p>【场景：场景名】note_id = （创建后填入）</p><h3>正文章节</h3><p>（正文创建后逐章填入）</p>"
  }]
}'
```

> 注意：创建笔记后先调用 `wpsnote-cli outline --note_id <id> --json` 获取初始空 block 的 block_id，再执行 batch-edit。

> **索引维护规则：**
> - 每创建一个新笔记，**立即**将其 note_id 回写到 meta 索引对应条目
> - 使用索引中的 note_id 访问笔记时，若命令返回错误，则用 `wpsnote-cli find` 重新定位，找到后**立即更新 meta 索引**
> - 索引是唯一真相来源，错误的 ID 必须修正，不能留着

#### 2-2：世界观笔记

```bash
wpsnote-cli create --title "《小说名》世界观设定" --json
# → note_id

wpsnote-cli outline --note_id <note_id> --json
# → 获取初始 block_id

wpsnote-cli batch-edit --json-args '{
  "note_id": "<note_id>",
  "operations": [{
    "op": "replace",
    "block_id": "<block_id>",
    "content": "<h1>《小说名》世界观设定</h1><p><tag>#小说名/设定/世界观</tag></p><h2>世界背景</h2><p>[时代/地理/社会结构]</p><h2>核心规则</h2><p>[魔法体系/科技水平/社会规范]</p><h2>特殊设定</h2><p>[独有元素]</p><h2>禁忌与约束</h2><p>[这个世界做不到的事]</p>"
  }]
}'
```

#### 2-3：人物笔记（每个主要角色一篇）

```bash
wpsnote-cli create --title "人物设定 — 角色名" --json
# → note_id

wpsnote-cli outline --note_id <note_id> --json
# → 获取初始 block_id

wpsnote-cli batch-edit --json-args '{
  "note_id": "<note_id>",
  "operations": [{
    "op": "replace",
    "block_id": "<block_id>",
    "content": "<h1>人物设定 — 角色名</h1><p><tag>#小说名/人物/主角：角色名</tag></p><h2>外貌</h2><p>[详细外貌描述，用于生图：发色与发型、体型与身材比例、面部特征、着装偏好与典型服饰、标志性配件]</p><h2>性格</h2><p>[3-5个核心词]</p><h2>口头禅/说话风格</h2><p>[...]</p><h2>背景故事</h2><p>[...]</p><h2>人物动机</h2><p>想要：[...] 害怕：[...]</p><h2>当前状态</h2><p>当前状态：初始状态</p>"
  }]
}'
```

创建完人物笔记后，立即生成人物形象图：

> ⚠️ **生成任何角色图片前，必须先完整阅读该角色笔记**，提取并记录以下人设细节，生图 prompt 必须包含所有这些细节以保证跨章一致性：
> - 发色与发型（如：银白色长直发、黑色短发、棕色卷发）
> - 体型与身材比例（如：修长高挑、娇小纤细、壮实宽肩）
> - 面部特征（如：眼睛颜色形状、肤色、标志性特征）
> - 着装偏好与典型服饰（如：总穿深色风衣、偏爱白色宽袖长袍）
> - 标志性配件（如：左耳银环、颈间红绳）
>
> 这些细节**非常非常重要**，后续所有涉及该角色的图片都必须严格遵循，不得出现与人设不符的外貌。
>
> **若角色有形象变迁历史，使用最新变迁后的描述生图，而非初始描述。**

```bash
# Step 0：阅读人物笔记，提取人设细节（必做，不可跳过）
wpsnote-cli read --note_id <人物笔记note_id> --json
# → 从输出中提取：发色、发型、体型、面部特征、着装偏好、标志性配件
# → 若有形象变迁历史，读取最新变迁描述作为生图依据
# → 将这些细节全部写入 prompt

# Step A：文生图（默认 4:3，最大 2048x1536；每 10 分钟最多 10 张）
wpsnote-cli gen-image \
  --prompt "[角色名]，[发色发型]，[体型描述]，[面部特征]，[典型着装]，[标志性配件]，[体裁]插画风格，精细人物肖像，[主要色调]" \
  --width 2048 \
  --height 1536 \
  --json
# → 成功：返回 image_url
# → 失败：跳过插图，在笔记对应位置写"（形象图待补）"，继续后续流程

# Step B：获取人物笔记末尾 block_id
wpsnote-cli outline --note_id <人物笔记note_id> --json
# → 找到最后一个 block_id（last_block）

# Step C：插入图片（生图成功时执行）
wpsnote-cli insert-image --json-args '{
  "note_id": "<人物笔记note_id>",
  "anchor_id": "<last_block_id>",
  "position": "after",
  "src": "<image_url>",
  "alt": "角色名 初始形象图"
}'
```

**人物形象变迁规则：**
- 当角色外貌发生显著变化（受伤留疤、换装、成长蜕变、被诅咒改变容貌等），**不修改原始外貌描述**，在笔记末尾追加变迁历史：

```bash
wpsnote-cli outline --note_id <人物笔记> --json  # → last_block_id

wpsnote-cli edit --json-args '{
  "note_id": "<人物笔记>",
  "op": "insert",
  "anchor_id": "<last_block_id>",
  "position": "after",
  "content": "<h2>形象变迁历史</h2><h3>第X章之后</h3><p>变迁类型：[受伤/换装/成长/魔化/其他...]</p><p>触发事件：[导致外貌变化的具体事件]</p><p>变迁描述：[详细说明外貌变成了什么样，哪些改变，哪些保留]</p><p>【变迁后形象图描述】[此图展示变迁后的外貌，角度/重点描述]</p>"
}'
# 然后生图并插入（流程同 Step A-C；失败时写"（变迁形象图待补）"占位）
```

> 后续所有涉及该角色的生图 prompt，都必须使用**最新变迁描述**而非初始外貌。

#### 2-3b：场景设定笔记（剧情中出现的每个场景必须单独建档）

> ⚠️ **每个新场景必须独立创建设定笔记**，不可合并。

```bash
wpsnote-cli create --title "场景设定 — 场景名" --json
wpsnote-cli outline --note_id <note_id> --json

wpsnote-cli batch-edit --json-args '{
  "note_id": "<note_id>",
  "operations": [{
    "op": "replace",
    "block_id": "<block_id>",
    "content": "<h1>场景设定 — 场景名</h1><p><tag>#小说名/设定/场景/场景名</tag></p><h2>场景概述</h2><p>场景类型：[室内/室外/地下/空中...]</p><p>所属区域/位置：[...]</p><p>首次出现：第X章</p><h2>环境细节</h2><p>地面：[材质、颜色、状态]</p><p>建筑/结构：[样式、材料、破损程度、高度层次]</p><p>光线：[光源类型、颜色、照射角度、氛围感]</p><p>气味：[...]</p><p>声音：[...]</p><p>温度/气候：[...]</p><p>常驻元素：[固定摆设、标志性物件]</p><h2>配图</h2><p>（见下方生图流程）</p>"
  }]
}'
```

**场景配图规范：**
- 每个场景必须生成 **2–3 张不同角度的图**（正面全景、内部视角、特写细节）
- **每张图上方必须先写入一段文字**，描述该图的拍摄角度和画面重点，再插入图片
- **默认图片尺寸：4:3，最大 2048×1536**
- **生图失败处理：失败时写 `（图待补）` 占位，继续后续流程，不阻塞创作**

```bash
# 角度 1（正面全景）— 先写描述文字
wpsnote-cli outline --note_id <场景笔记> --json  # → last_block_id
wpsnote-cli edit --json-args '{
  "note_id": "<场景笔记>",
  "op": "insert",
  "anchor_id": "<last_block_id>",
  "position": "after",
  "content": "<p>【正面全景】[角度描述：从哪里看、光线方向、画面重点]</p>"
}'

# 生成图片（失败时写占位符后继续）
wpsnote-cli gen-image \
  --prompt "[场景名]，[所有环境细节]，正面全景，[光线色调]，[体裁]插画风格，写实背景艺术" \
  --width 2048 --height 1536 --json
# → 成功：获取 image_url，然后插图
# → 失败：wpsnote-cli edit --json-args '{"note_id":"<场景笔记>","op":"insert","anchor_id":"<last_block_id>","position":"after","content":"<p>（正面全景图待补）</p>"}' 然后继续

wpsnote-cli outline --note_id <场景笔记> --json  # → 最新 last_block_id（生图成功时）
wpsnote-cli insert-image --json-args '{"note_id":"<场景笔记>","anchor_id":"<last_block_id>","position":"after","src":"<image_url>","alt":"场景名 正面全景"}'

# 角度 2（内部视角）— 先写描述文字，再生图插入（同上流程）
# 角度 3（特写细节，可选）— 同上
```

**场景变更规则：**
- 当场景在剧情中被**改变或破坏**，**不修改原始描述**，而是在笔记末尾追加变更历史：

```bash
wpsnote-cli outline --note_id <场景笔记> --json  # → last_block_id

wpsnote-cli edit --json-args '{
  "note_id": "<场景笔记>",
  "op": "insert",
  "anchor_id": "<last_block_id>",
  "position": "after",
  "content": "<h2>场景变更历史</h2><h3>第X章之后</h3><p>变更类型：[破坏/改造/废弃/占领...]</p><p>变更描述：[详细说明场景变成什么样，哪些细节改变，哪些保留]</p><p>触发事件：[导致变更的具体事件]</p>"
}'
# 变更后如需配图，同样先写角度描述文字再插入图片；失败时写"（变更状态图待补）"占位
```

#### 2-4：剧情梗概笔记

```bash
wpsnote-cli create --title "《小说名》剧情梗概" --json
wpsnote-cli outline --note_id <note_id> --json

wpsnote-cli batch-edit --json-args '{
  "note_id": "<note_id>",
  "operations": [{
    "op": "replace",
    "block_id": "<block_id>",
    "content": "<h1>《小说名》剧情梗概</h1><p><tag>#小说名/设定/剧情梗概</tag></p><h2>故事起点</h2><p>[...]</p><h2>主线走向</h2><p>[3-5个关键转折点]</p><h2>预计结局</h2><p>[可以模糊]</p><h2>核心主题</h2><p>[...]</p>"
  }]
}'
```

#### 2-5：伏笔日志笔记（初始为空）

```bash
wpsnote-cli create --title "《小说名》伏笔日志" --json
wpsnote-cli outline --note_id <note_id> --json

wpsnote-cli batch-edit --json-args '{
  "note_id": "<note_id>",
  "operations": [{
    "op": "replace",
    "block_id": "<block_id>",
    "content": "<h1>《小说名》伏笔日志</h1><p><tag>#小说名/设定/伏笔</tag></p><p>（尚未埋入伏笔）</p>"
  }]
}'
```

后续每章追加格式（全局唯一编号 F-1、F-2…）：
```xml
<p>[F-1] 伏笔内容描述 → 埋入：第1章 / 状态：未回收</p>
<p>[F-2] 伏笔内容描述 → 埋入：第2章 / 已回收：第5章</p>
```

#### 2-6：剧情日志笔记（初始为空）

```bash
wpsnote-cli create --title "《小说名》剧情日志" --json
wpsnote-cli outline --note_id <note_id> --json

wpsnote-cli batch-edit --json-args '{
  "note_id": "<note_id>",
  "operations": [{
    "op": "replace",
    "block_id": "<block_id>",
    "content": "<h1>《小说名》剧情日志</h1><p><tag>#小说名/剧情日志</tag></p><p>（尚未开始写作）</p>"
  }]
}'
```

---

## 写作前上下文检查（每次必做）

### 检查 0：读 Meta，获取写作约束和笔记索引

```bash
# 首次启动时通过标签搜索找到 meta 笔记（此后通过已知 note_id 直接访问）
wpsnote-cli find --json-args '{"tags":["#小说名/meta"],"limit":1}' --json
# → META_ID

# 读取整个 meta 笔记（含基本信息 + 笔记索引）
wpsnote-cli read --note_id <META_ID> --json
# → 从"基本信息"提取：章节目标字数、叙述视角、语言风格
# → 从"笔记索引"提取：世界观、剧情日志、伏笔日志、各角色、各场景、各章节的 note_id
# → 将所有 note_id 缓存在本次上下文，后续步骤直接使用，无需再搜索
```

> **索引容错规则：** 使用索引中的 note_id 时，若命令返回错误，立即用 `wpsnote-cli find` 重新定位，找到后更新 meta 索引中对应条目，再继续流程。

将目标字数作为硬约束：写作时严格控制在目标字数 ±20% 以内。

### 检查 1：读上一章结尾

```bash
# 从 meta 索引取最新章节 note_id（检查 0 已缓存，取编号最大的章节）
# 若索引中有多章，取最后一条

# 获取大纲，找末尾 block
wpsnote-cli outline --note_id <最新章节note_id> --json

# 读取结尾约 300-500 字
wpsnote-cli read-blocks --json-args '{"note_id":"<最新章节note_id>","block_id":"<倒数第二个block_id>","after":5}' --json
```

记录：最后的情绪基调、主角所在位置、时间点。

### 检查 2：扫描剧情日志

```bash
# 从 meta 索引取剧情日志 note_id（检查 0 已缓存）
wpsnote-cli read --note_id <剧情日志note_id> --json
```

关注：未回收的伏笔（本章适合回收吗？）、近期章节走向、有无角色消失太久。

### 检查 3：读本章相关角色状态

```bash
# 从 meta 索引取将要出场角色的 note_id（检查 0 已缓存）
wpsnote-cli search --note_id <角色note_id> --query "当前状态" --json
# → block_id

wpsnote-cli read-blocks --json-args '{"note_id":"<角色note_id>","block_id":"<当前状态block_id>"}' --json
# 同时确认是否有形象变迁历史，使用最新状态
```

### 检查 4：处理用户特殊需求（若有）

```bash
# 语义检索相关设定
wpsnote-cli find --json-args '{"keyword":"用户提到的关键词","tags":["#小说名"]}' --json

# 检查剧情日志有无相关铺垫
wpsnote-cli search --note_id <剧情日志> --query "关键词" --json
```

### 检查 5：确认本章涉及的场景

```bash
# 检索本章将要出现的场景设定笔记
wpsnote-cli find --json-args '{"keyword":"场景名","tags":["#小说名/设定/场景"]}' --json
```

- **已有场景**：读取场景笔记，确认当前状态（是否有变更历史），写作时严格遵循细节
- **新场景首次登场**：在写作之前必须先创建场景设定笔记（含环境细节 + 多角度配图），再开始写正文

---

## 正式写作

> ### 绝对禁止：在对话中输出小说正文
>
> AI 不允许在对话消息里写任何小说正文，无论任何情况，无一例外。
>
> - 禁止在对话中写正文、片段、示范、草稿，哪怕只有一句话
> - 唯一合法的写作方式：调用 `wpsnote-cli create` + `wpsnote-cli batch-edit` 将正文写入 WPS 笔记
> - 写完后对话中只允许出现：章节标题、字数、一句话剧情摘要、"笔记已保存"
> - 违反以上任一条，即为执行错误，必须立刻停止并重新通过 CLI 写入

根据 Meta 笔记中的风格约束进行写作。

写作 6 原则：
1. 字数约束：严格控制在 Meta 笔记中"章节目标字数"的 ±20% 以内（硬约束）
2. 不穿帮：所有细节必须与设定笔记一致
3. 风格一致：严格遵循 Meta 笔记中的叙述视角、语言风格描述
4. 节奏控制：每章有起伏，不要全程平铺
5. 结尾钩子：每章结尾留悬念或情绪钩子
6. 多样性：不同章节可变换焦点、张弛节奏，避免雷同

---

## 写作后归档（每次必做，全自动）

### 归档 1：创建正文笔记（写作时同步执行）

```bash
# 创建笔记
wpsnote-cli create --title "第X章 章节名" --json
# → new_note_id

# 获取初始 block_id
wpsnote-cli outline --note_id <new_note_id> --json
# → 初始 block_id

# 写入全文
wpsnote-cli batch-edit --json-args '{
  "note_id": "<new_note_id>",
  "operations": [{
    "op": "replace",
    "block_id": "<初始block_id>",
    "content": "<h1>第X章 章节名</h1><p><tag>#小说名/正文/第X章</tag></p><p>正文第一段...</p><p>正文第二段...</p>..."
  }]
}'

# 写入成功后，立即将新章节 note_id 回写到 meta 索引
wpsnote-cli search --note_id <META_ID> --query "正文章节" --json
# → 找到索引末尾 block_id
wpsnote-cli edit --json-args '{
  "note_id": "<META_ID>",
  "op": "insert",
  "anchor_id": "<章节索引末尾block_id>",
  "position": "after",
  "content": "<p>【第X章】note_id = <new_note_id></p>"
}'
```

### 归档 2：追加剧情日志（必做）

```bash
# 获取日志末尾 block_id
wpsnote-cli outline --note_id <剧情日志note_id> --json
# → last_block_id

# 追加本章记录
wpsnote-cli edit --json-args '{
  "note_id": "<剧情日志note_id>",
  "op": "insert",
  "anchor_id": "<last_block_id>",
  "position": "after",
  "content": "<h2>第X章《章节标题》</h2><p>主要事件：[本章核心剧情一两句]</p><p>在场角色：[角色名, 角色名, ...]</p><p>角色状态变化：[无 / 角色名：变化描述]</p><p>结尾句：[本章最后一句原文]</p><h3>本章伏笔清单</h3><p>【新埋】[F-X] [伏笔描述] → 状态：未回收</p><p>（本章无新伏笔则写：本章无新伏笔）</p><p>累计未回收伏笔：[F-1、F-3...] 共 N 条</p>"
}'
```

> 伏笔编号规则：全局唯一，按埋入顺序编号，格式 `F-1`、`F-2`……跨章一致。

### 归档 3：更新角色当前状态

```bash
# 定位"当前状态"字段
wpsnote-cli search --note_id <角色笔记> --query "当前状态" --json
# → block_id

# 替换状态描述
wpsnote-cli edit --json-args '{
  "note_id": "<角色笔记>",
  "op": "replace",
  "block_id": "<状态block_id>",
  "content": "<p>当前状态：[新状态描述]</p>"
}'
```

### 归档 4：同步伏笔日志（必做，每章都要执行）

情况 A：本章埋入新伏笔

```bash
wpsnote-cli outline --note_id <伏笔日志> --json
# → last_block_id

wpsnote-cli edit --json-args '{
  "note_id": "<伏笔日志>",
  "op": "insert",
  "anchor_id": "<last_block_id>",
  "position": "after",
  "content": "<p>[F-X] [伏笔描述] → 埋入：第X章 / 状态：未回收</p>"
}'
```

情况 B：本章回收了已有伏笔

```bash
wpsnote-cli search --note_id <伏笔日志> --query "F-X" --json
# → block_id

wpsnote-cli edit --json-args '{
  "note_id": "<伏笔日志>",
  "op": "replace",
  "block_id": "<伏笔block_id>",
  "content": "<p>[F-X] [伏笔描述] → 埋入：第X章 / 已回收：第Y章</p>"
}'
```

情况 C：本章无伏笔变动（也必须执行）

```bash
# 核对未回收数量与剧情日志最新条目一致
wpsnote-cli search --note_id <伏笔日志> --query "未回收" --json
# → 若数量与剧情日志对得上，归档完成；若对不上，逐条比对补齐
```

### 归档 5：更新 Meta 进度

```bash
wpsnote-cli search --note_id <meta笔记> --query "当前进度" --json
# → block_id

wpsnote-cli edit --json-args '{
  "note_id": "<meta笔记>",
  "op": "replace",
  "block_id": "<进度block_id>",
  "content": "<p>当前进度：第 X 章</p>"
}'
```

---

## 防穿帮速查表

| 穿帮类型 | 触发场景 | 防护措施 |
|---------|---------|---------|
| 角色状态矛盾 | 第三章受伤，第四章却行动如常 | 写前读角色"当前状态"字段 |
| 能力越界 | 角色突然会了设定里没有的技能 | 写前读世界观/角色设定笔记 |
| 人际关系错误 | 已决裂的人突然像老朋友 | 读人物关系图笔记 |
| 地理矛盾 | 三天路程突然一天到 | 场景笔记标注地理距离 |
| 场景细节矛盾 | 同一地点描述前后不一致 | 写前读场景设定笔记，照实执行细节 |
| 场景状态错误 | 已破坏的房间又恢复原样 | 查看场景变更历史，使用最新状态 |
| 角色外貌不一致 | 同一角色发色或着装前后矛盾 | 生图/写作前必须先读人物笔记人设细节 |
| 伏笔遗忘 | 第二章埋的东西从未回收 | 每次写前扫描剧情日志 |
| 时间线混乱 | 事件先后顺序不清楚 | 剧情日志按章节顺序记录 |

---

## 特殊情况处理

### 用户想改变已有设定

```bash
# 找出所有相关笔记
wpsnote-cli find --json-args '{"keyword":"角色名/设定名","tags":["#小说名"]}' --json
# 评估影响范围，告知用户（一句话说明）
# 确认后批量更新相关笔记
# 在剧情日志中标注"设定变更点：第X章起，XX设定改为YY"
```

### 用户想插入新角色

1. 询问："这个角色有什么特点？"（如用户没想法，AI 直接生成）
2. 创建人物笔记 → 生成形象图（见 2-3）
3. 在人物关系图笔记中追加与已有角色的关系
4. 检查前文是否适合补充伏笔铺垫

### 用户想跳章节写

```bash
# 在剧情日志中为跳过的章节预留标记
wpsnote-cli edit --json-args '{
  "note_id": "<剧情日志>",
  "op": "insert",
  "anchor_id": "<last_block_id>",
  "position": "after",
  "content": "<p>[待写] 第X章 占位</p>"
}'
# 在 Meta 笔记"当前进度"后追加跳写记录
# 正常写指定章节并存档
```

---

## 续写序列快速参考

```bash
# Step 1：加载 meta 笔记（索引 + 风格约束）
# 首次使用标签搜索定位 meta，后续直接用已知 META_ID
wpsnote-cli find --json-args '{"tags":["#小说名/meta"],"limit":1}' --json
wpsnote-cli read --note_id <META_ID> --json
# → 从"基本信息"取：目标字数、叙述视角、语言风格
# → 从"笔记索引"取：剧情日志、伏笔日志、各角色、各场景、最新章节的 note_id
# → 将所有 note_id 缓存在本次上下文

# Step 2：读最新章节结尾（直接用索引中的 note_id）
wpsnote-cli outline --note_id <最新章节note_id> --json
wpsnote-cli read-blocks --json-args '{"note_id":"<最新章节note_id>","block_id":"<倒数block_id>","after":5}' --json

# Step 3：扫描剧情日志（直接用索引 note_id）
wpsnote-cli read --note_id <剧情日志note_id> --json

# Step 4：[如有用户需求] 从 meta 索引查找对应笔记，索引没有则搜索后更新索引

# Step 5：写作（通过 create + batch-edit 写入笔记）

# Step 6：存档（见"写作后归档"章节，含回写 note_id 到索引）
```

---

## Troubleshooting

### 找不到已有小说笔记

```bash
# 先从 meta 索引直接读取 note_id（检查 0 已加载）
# 若 meta 索引中的 note_id 访问失败，执行以下修复流程：
wpsnote-cli find --keyword "小说名" --json
wpsnote-cli list --limit 20 --sort update_time --direction desc --json
# 找到正确 note_id 后，立即更新 meta 索引中对应条目
```

### 生图失败（RATE_LIMITED 或其他错误）

- **不要重试阻塞流程**：生图失败时，在对应位置写 `（图待补）` 占位，继续后续步骤
- 速率限制：每 10 分钟最多生成 10 张图，超出时同样占位继续
- 因为文字描述已经完整记录了所有细节，后续回到该笔记时发现占位符再补生即可

### block_id 失效

编辑操作后 block_id 会变化，重新获取：
```bash
wpsnote-cli outline --note_id <note_id> --json
# → 获取最新 block_id 后重试
```

### 剧情日志太长读取缓慢

当日志内容量较大时，改用精准搜索：
```bash
wpsnote-cli search --note_id <剧情日志> --query "未回收" --json
```

### XML 内容含特殊字符导致 JSON 解析失败

含中文引号、双引号、换行符时，将 XML 内容写入临时文件再通过 `--json-args` 引用，或对特殊字符做转义：
- `"` → `\"`
- 换行 → `\n`

---

## 与其他 Skill 的配合

| 场景 | 配合 Skill |
|------|-----------|
| 写完后发公众号 | wechat-publisher |
| 生成小红书图片 | xiaohongshu-article-layout |
| 回顾笔记找灵感 | ie-recall-memory / ie-engine |
| 整理标签 | tag-organize |
| 美化设定笔记排版 | wpsnote-beautifier |
