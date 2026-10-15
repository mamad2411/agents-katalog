---
name: music-genre-finder
description: |
  Intelligent music genre search assistant with 5947 genres from RateYourMusic. Supports quick lookup, smart recommendations, and hierarchical exploration.

  USE THIS SKILL when user mentions:
  - Explicit commands: /genre, /music-style, "查询音乐风格", "推荐音乐类型"
  - Creation needs: "我想做个XX风格的歌/音乐", "帮我选个音乐风格", "什么风格适合XX场景", "推荐一些XX特点的音乐风格" (e.g., 适合深夜, 有活力, 空灵, 暗黑)
  - Exploration: "XX风格有哪些子分类", "Ambient 下面有什么", "给我看看 Rock 的分支"
  - Suno music generation: Before using suno-music-creator skill when genre needs to be determined, or when user says "用 Suno 生成" but hasn't specified a genre
---

# Music Genre Finder

智能音乐风格查询助手，基于 RateYourMusic 的 5947 个音乐风格数据库，支持快速查询、智能推荐和层级探索。

## 数据结构说明

skill 使用 `~/.claude/skills/music-genre-finder/references/` 目录下的分层数据：

```
references/
├── _index.json          # 49个主分类概览（必读，13KB）
├── _meta.json           # 元数据和使用说明（399B）
├── main/                # 49个文件，每个主分类的直接子分类
│   ├── ambient.json
│   ├── rock.json
│   └── ...
└── detailed/            # 578个文件，有孙分类的子分类详情
    ├── dark-ambient.json
    ├── shoegaze.json
    └── ...
```

**数据统计**：
- 总风格数：5947
- 主分类：49（Rock, Jazz, Ambient, Electronic 等）
- 子分类：737（level: sub）
- 孙分类及以下：5161（sub-2/sub-3/sub-4）

**每个风格的数据字段**：
```json
{
  "name": "Dark Ambient",
  "url": "https://rateyourmusic.com/genre/dark-ambient/",
  "description": "Emphasizes an ominous, gloomy, and dissonant atmosphere.",
  "level": "sub",           // main, sub, sub-2, sub-3, sub-4
  "parent": "Ambient"       // 父分类名称
}
```

## 核心功能

### 1. 快速查询（精确匹配）

**用户说**："查一下 Shoegaze"

**执行流程**：
```
Step 1: 读取 _index.json，检查是否为主分类
Step 2: 如果不是，用 grep/find 在 main/*.json 中搜索
Step 3: 找到后，显示风格信息 + 链接 + 子分类（如果有）
```

**示例输出**：
```
🎵 Shoegaze
📝 Characterized by ethereal vocals buried beneath walls of distorted guitars...

🔗 https://rateyourmusic.com/genre/shoegaze/

📂 属于：Alternative Rock > Noise Pop > Shoegaze

💡 Shoegaze 有 3 个子分类：
  - Blackgaze（融合黑金属元素）
  - Nu-Gaze（现代复兴）
  - Dream Pop（更柔和的变体）
```

---

### 2. 智能推荐（语义匹配）

**用户说**："推荐一些适合深夜、有点空灵的风格"

**执行流程**：
```
Step 1: 读取 _index.json，扫描所有49个主分类的描述
Step 2: 用关键词匹配（deep night, ethereal, ambient, atmospheric）
Step 3: 找到候选主分类后，读取对应的 main/*.json
Step 4: 根据描述进一步筛选子分类
Step 5: 返回 Top 3-5 推荐，带简短说明
```

**关键词映射表**（内置语义规则）：
| 用户描述 | 匹配关键词 | 推荐方向 |
|---------|-----------|---------|
| 深夜、放松、冥想 | ambient, atmospheric, calm, soothing | Ambient, Drone, Space Ambient |
| 有活力、激烈 | energetic, fast, aggressive, intense | Punk, Hardcore, Drum and Bass |
| 暗黑、压抑 | dark, gloomy, ominous, dissonant | Dark Ambient, Black Metal, Industrial |
| 空灵、梦幻 | ethereal, dreamy, atmospheric, reverb | Dream Pop, Shoegaze, Ambient Pop |
| 电子、科技感 | electronic, synthetic, futuristic, digital | Techno, IDM, Ambient Techno |
| 复古、怀旧 | vintage, retro, nostalgic, classic | Synthwave, Vaporwave, Chillwave |
| 实验、前卫 | experimental, avant-garde, unconventional | Noise, Free Jazz, Musique Concrète |

**示例输出**：
```
🌙 根据"深夜 + 空灵"，为你推荐以下风格：

1. ⭐ Dark Ambient
   "强调阴暗、忧郁和不和谐的氛围"
   🔗 https://rateyourmusic.com/genre/dark-ambient/

2. ⭐ Space Ambient
   "流动而放松的合成器音乐，常围绕外太空意象"
   🔗 https://rateyourmusic.com/genre/space-ambient/

3. ⭐ Drone
   "持续或重复的声音、音符或音簇，强调音色变化"
   🔗 https://rateyourmusic.com/genre/drone/

💡 想深入了解某个风格？回复风格名称即可。
```

---

### 3. 层级探索（树状浏览）

**用户说**："给我看看 Ambient 下面都有什么"

**执行流程**：
```
Step 1: 读取 main/ambient.json
Step 2: 列出所有直接子分类（level: sub）
Step 3: 如果用户进一步询问某个子分类，读取 detailed/{subgenre}.json
Step 4: 显示完整的层级树
```

**示例输出**：
```
🎵 Ambient 的子分类树：

Ambient （主分类）
├── Ambient Americana
│   └── 使用传统美式乡村乐器，营造田园氛围
├── Dark Ambient ⭐
│   ├── Black Ambient（融合黑金属元素）
│   ├── Ritual Ambient（仪式感、神秘）
│   └── ...
├── Space Ambient
│   └── 太空主题，合成器为主
└── Tribal Ambient
    └── 结合全球传统乐器和氛围

💡 点击 ⭐ 标记的分类可以继续展开更多子分类
```

---

### 4. 与 Suno 集成（自动流程）

当用户要用 Suno 生成音乐但没指定风格时，主动触发此 skill：

**用户说**："用 Suno 帮我生成一首歌"

**执行流程**：
```
Step 1: 询问用户想要什么氛围/场景（或直接推荐热门风格）
Step 2: 使用智能推荐功能，给出 3-5 个风格
Step 3: 用户选择后，将风格名称传递给 suno-music-creator
Step 4: Suno 生成时，在 tags 参数中包含风格名称
```

**示例对话**：
```
User: 用 Suno 帮我生成一首歌
AI: 好的！想要什么风格？我可以帮你推荐：
    1. Synthwave（复古电子，80年代感）
    2. Lo-fi Hip Hop（放松、学习背景音乐）
    3. Shoegaze（空灵、吉他噪音墙）
    或者告诉我你想要的氛围（如：有活力、适合深夜、暗黑等）

User: 有活力的
AI: 推荐：Drum and Bass, Hardcore Punk, Electro House
    选哪个？

User: Drum and Bass
AI: [调用 suno-music-creator，tags 包含 "drum and bass, energetic"]
```

---

## 实现细节

### 读取优化策略

**原则**：渐进式加载，最小化上下文消耗

1. **必读文件**：
   - `_index.json`（13KB）- 每次查询都要读，作为索引

2. **按需读取**：
   - 精确查询：只读 1 个 main/*.json 或 detailed/*.json
   - 智能推荐：读 _index.json + 最多 3 个候选 main/*.json
   - 层级探索：逐层展开，用户点击才读下一层

3. **上下文预算**：
   - 单次查询通常 < 30KB（_index + 1-3个分类文件）
   - 远小于原始 1.7MB 的完整数据

### 搜索算法

**精确匹配**：
```bash
# 先在主分类中查找
jq '.genres[] | select(.name == "Ambient")' _index.json

# 如果没找到，在所有 main/*.json 中搜索
grep -l "\"name\": \"Shoegaze\"" main/*.json

# 再在 detailed/*.json 中搜索
grep -l "\"name\": \"Blackgaze\"" detailed/*.json
```

**模糊匹配**（用户描述不精确时）：
```bash
# 关键词匹配描述
jq '.genres[] | select(.description | test("dark|ominous|gloomy"; "i"))' _index.json
```

### 输出格式规范

**统一模板**：
```
🎵 {风格名称}
📝 {描述}
🔗 {RateYourMusic 链接}
📂 {层级路径}（如果不是主分类）
💡 {额外信息}（如子分类数量、推荐理由等）
```

---

## 使用示例

### 示例1：快速查询
```
User: 查一下 Vaporwave
AI: 🎵 Vaporwave
    📝 Nostalgic, surrealist take on elevator music, sampling 1980s-90s muzak,
        smooth jazz, and lounge music, often with a chopped and screwed aesthetic.
    🔗 https://rateyourmusic.com/genre/vaporwave/
    📂 Electronic > Vaporwave

    💡 Vaporwave 有 5 个子分类：
      - Hardvapour（更激进的变体）
      - Mallsoft（商场环境音乐）
      - Future Funk（融合 Funk 元素）
      - Eccojams（循环和失真）
      - Signalwave（广播信号美学）
```

### 示例2：智能推荐
```
User: 推荐一些适合写代码时听的音乐风格
AI: 🖥️ 根据"写代码"场景，推荐以下风格（不分散注意力 + 有节奏感）：

    1. ⭐ Lo-fi Hip Hop
       "放松的嘻哈节奏 + 爵士采样，专注学习/工作的首选"

    2. ⭐ Ambient Techno
       "电子氛围 + 稳定节奏，既不无聊又不干扰"

    3. ⭐ Post-Rock
       "器乐为主，渐进式发展，适合长时间专注"

    4. ⭐ Downtempo
       "慢节奏电子，平静但不催眠"

    💡 想了解更多？回复风格名称或序号。
```

### 示例3：层级探索
```
User: Electronic 下面都有什么大分类？
AI: 🎵 Electronic 的主要子分类：

    📂 Electronic（主分类）
    ├── 🎛️ Ambient（氛围电子）
    ├── 💃 Dance（舞曲类）
    │   ├── House
    │   ├── Techno
    │   ├── Trance
    │   └── Drum and Bass
    ├── 🧠 IDM（智能舞曲，实验电子）
    ├── 🌊 Downtempo（慢节奏）
    ├── 🔊 Bass Music（低音音乐）
    └── 🎹 Synthwave（合成器波）

    总共 37 个子分类，以上是最热门的几类。

    💡 想深入某个分类？告诉我名称即可。
```

---

## 错误处理

### 找不到风格时
```
User: 查一下 Qiaomu Style
AI: ❌ 没有找到 "Qiaomu Style" 这个风格。

    💡 可能的原因：
    - 风格名称拼写错误？试试相似的：Shoegaze, Noise Pop
    - RateYourMusic 数据库中没有此风格

    🔍 你可以：
    1. 描述一下这个风格的特点，我帮你找相似的
    2. 直接访问 https://rateyourmusic.com/genres/ 浏览完整列表
```

### 描述太模糊时
```
User: 推荐一些好听的音乐风格
AI: 🤔 "好听"的定义因人而异！能具体描述一下吗？

    例如：
    - 场景：适合深夜/运动/工作/开车
    - 氛围：放松/激烈/暗黑/欢快
    - 乐器：吉他为主/电子/管弦乐
    - 参考：类似 XX 乐队/歌手

    或者我可以推荐几个通用的热门风格？
```

---

## 数据维护

### 更新数据
如果 RateYourMusic 网站更新，需要重新抓取：
```bash
# 重新运行抓取脚本（使用 playwright）
python scrape_rateyourmusic.py

# 重新拆分数据
python split_genres.py
```

### 添加自定义标签
可以在 `_meta.json` 中添加 `custom_tags` 字段，用于更精准的推荐：
```json
{
  "custom_tags": {
    "coding": ["Lo-fi Hip Hop", "Ambient Techno", "Post-Rock"],
    "workout": ["Drum and Bass", "Hardcore Punk", "Trap"],
    "sleep": ["Dark Ambient", "Drone", "Field Recordings"]
  }
}
```

---

## 技术规范

### 文件读取优先级
1. 优先使用 `Read` tool（快速、直接）
2. 需要搜索时用 `Grep` tool
3. 避免用 `Bash` cat/grep（Read 和 Grep 更高效）

### JSON 解析
- 使用 `jq` 进行复杂查询（如过滤、排序）
- Python 脚本用于批量处理或复杂逻辑

### 链接处理
- 所有输出的 RateYourMusic 链接都要完整、可点击
- 格式：`🔗 https://rateyourmusic.com/genre/{genre-slug}/`

---

## 与其他 Skills 的协作

### 与 suno-music-creator 配合
```
music-genre-finder → 推荐风格 → suno-music-creator 生成音乐
```

**工作流**：
1. 用户说"用 Suno 生成一首歌"
2. music-genre-finder 推荐风格（如 "Synthwave"）
3. 用户确认后，调用 suno-music-creator，tags 包含风格名称
4. Suno 生成符合该风格的音乐

### 与 qiaomu-writer 配合
```
music-genre-finder → 查询风格 → qiaomu-writer 写风格解读文章
```

**示例**：
- 用户："写一篇关于 Shoegaze 的文章"
- music-genre-finder 提供 Shoegaze 的详细信息（描述、历史、子分类）
- qiaomu-writer 基于这些信息生成乔木风格的文章

---

## 最佳实践

### DO ✅
- 总是先读 `_index.json` 建立索引
- 根据用户需求渐进式加载（不要一次读太多文件）
- 输出时包含 RateYourMusic 链接，方便用户深入了解
- 用 emoji 让输出更直观（🎵 🔗 📂 💡）
- 推荐时给出 3-5 个选项，不要太多（选择困难）

### DON'T ❌
- 不要一次性读取所有 main/*.json 和 detailed/*.json（浪费上下文）
- 不要假设用户知道专业术语（用简单描述 + 链接）
- 不要只返回风格名称列表（要有描述和推荐理由）
- 不要忽略用户的隐式需求（如"用 Suno 生成"隐式需要风格推荐）

---

## 更新日志

### v1.1 (2026-01-31)
- 规范化 skill 结构：添加 YAML frontmatter
- 重命名 data/ → references/（符合 skill 最佳实践）
- 优化 description 字段，整合触发条件

### v1.0 (2026-01-31)
- 初始版本
- 支持 5947 个音乐风格的查询、推荐、探索
- 基于 RateYourMusic 2026-01-31 数据
- 三层数据结构（_index.json, main/, detailed/）
- 与 suno-music-creator 集成

---

## 作者

Created by 乔帮主 with Claude Code
Data source: https://rateyourmusic.com/genres/
