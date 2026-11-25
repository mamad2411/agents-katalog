---
name: qiaomu-music-player-ncm
description: |
  网易云音乐全能助手 + 5947风格数据库。安装配置、播放控制、搜索、队列管理、
  场景音乐推荐、每日推荐、心动模式、私人漫游FM、雷达歌单、红心管理、听歌排行、
  歌词查询、偏好分析、智能推荐、定时推送调度、风格查询与探索。

  USE THIS SKILL when user mentions:
  - 播放控制: "播放音乐", "来首歌", "放点音乐", "想听XX", "来点XX音乐", "网易云"
  - 控制操作: "暂停", "继续", "下一首", "上一首", "音量", "正在播放什么"
  - 网易云特色: "每日推荐", "私人漫游", "心动模式", "雷达歌单", "红心", "听歌排行"
  - 场景/心情: "适合深夜的音乐", "工作时听", "适合跑步", "推荐一些XX的音乐"
  - 歌词查询: "这首歌的歌词", "显示歌词"
  - 智能推荐: "根据我的口味推荐", "分析我的偏好", "帮我选"
  - 安装配置: "安装ncm-cli", "配置API Key", "安装mpv"
  - 调度管理: "每天推送", "定时推荐", "几点推"
  - 风格查询: "查一下XX风格", "XX是什么音乐类型", "推荐一些XX特点的风格", "给我看看XX的子类型"
  - /ncm, /netease, /genre

triggers:
  - "播放音乐"
  - "来首歌"
  - "想听"
  - "网易云"
  - "云音乐"
  - "暂停"
  - "下一首"
  - "上一首"
  - "现在播放什么"
  - "音量"
  - "每日推荐"
  - "心动模式"
  - "私人漫游"
  - "红心"
  - "听歌排行"
  - "歌词"
  - "雷达歌单"
  - "分析偏好"
  - "根据口味推荐"
  - "/ncm"
  - "/netease"
---

# Qiaomu Music Player（网易云音乐）

统一的网易云音乐全能 Skill，集成安装配置、播放控制、偏好分析、智能推荐、定时调度。
通过 `ncm-cli` 命令行工具直接调用网易云音乐 API。

---

## Part 0: 环境检查与初始化

**每次执行播放操作前必须先执行以下检查。**

### 0a. 检查是否已安装

```bash
ncm-cli --version
```

未安装则执行：

```bash
npm install -g @music163/ncm-cli
```

> 需要 Node.js >= 18

### 0b. 检查登录状态

```bash
ncm-cli login --check
```

未登录则引导扫码：

```bash
ncm-cli login --background
# 把二维码链接给用户扫码
```

如果显示 API key 未设置，先配置：

```bash
ncm-cli config set appId <你的AppId>
ncm-cli config set privateKey <你的privateKey>
```

> API Key 申请地址：https://developer.music.163.com/st/developer/apply/account?type=INDIVIDUAL

### 0c. 针对播放（play）：检查播放器

```bash
ncm-cli config get player
```

如果是内置播放器（mpv），检查是否安装：

```bash
mpv --version
```

未安装则：

- **macOS**：`brew install mpv`
- **Linux**：`apt/dnf/pacman install mpv`
- **Windows**：`winget install mpv`

配置播放器：

```bash
ncm-cli config set player mpv      # 内置播放器（跨平台）
ncm-cli config set player orpheus  # 调用云音乐 App（仅 macOS，需版本兼容）
```

### 0d. 获取命令树

首次使用或不确定参数时：

```bash
ncm-cli commands
ncm-cli <command> --help   # 获取具体命令参数
```

**参数不要猜测！**

---

## Part 1: ncm-cli 命令速查

### 播放控制

```bash
ncm-cli play --song --encrypted-id <32位hex> --original-id <数字>    # 播放单曲
ncm-cli play --playlist --encrypted-id <加密ID> --original-id <数字> # 播放歌单
ncm-cli pause          # 暂停
ncm-cli resume         # 继续
ncm-cli stop           # 停止
ncm-cli next           # 下一首
ncm-cli prev           # 上一首
ncm-cli seek <秒>      # 跳转到指定时间
ncm-cli volume <0-100> # 设置音量
ncm-cli state          # 查看播放状态
```

### 队列管理

```bash
ncm-cli queue                                                              # 查看队列
ncm-cli queue add --encrypted-id <id> --original-id <id>                  # 加入队列末尾
ncm-cli queue add --encrypted-id <id> --original-id <id> --next           # 插入下一首
ncm-cli queue clear                                                        # 清空队列
```

### 搜索

```bash
ncm-cli search song --keyword "xxx" --userInput "..."      # 搜索歌曲
ncm-cli search album --keyword "xxx" --userInput "..."     # 搜索专辑
ncm-cli search playlist --keyword "xxx" --userInput "..."  # 搜索歌单
ncm-cli search all --keyword "xxx" --userInput "..."       # 综合搜索
```

### 推荐系统（网易云特色）

```bash
ncm-cli recommend daily --userInput "..."                                          # 每日推荐（30首）
ncm-cli recommend fm --userInput "..."                                             # 私人漫游 FM
ncm-cli recommend heartbeat --playlistId <id> --songId <id> --userInput "..."      # 心动模式
ncm-cli recommend heartbeat --playlistId <id> --songId <id> --count 20 --userInput "..." # 心动模式（指定数量）
```

### 用户数据

```bash
ncm-cli user info --userInput "..."                          # 用户信息
ncm-cli user favorite --userInput "..."                      # 红心歌单（全量）
ncm-cli user history --userInput "..."                       # 最近播放
ncm-cli user listen-ranking --type 0 --userInput "..."       # 总听歌排行
ncm-cli user listen-ranking --type 1 --userInput "..."       # 本周听歌排行
```

### 歌单管理

```bash
ncm-cli playlist collected --userInput "..."                             # 我收藏的歌单
ncm-cli playlist created --userInput "..."                               # 我创建的歌单
ncm-cli playlist radar --userInput "..."                                 # 雷达歌单（智能推荐）
ncm-cli playlist get --playlistId <加密ID> --userInput "..."             # 歌单详情
ncm-cli playlist tracks --playlistId <加密ID> --userInput "..."          # 歌单曲目列表
ncm-cli playlist create --playlistName "xxx" --userInput "..."           # 创建歌单
ncm-cli playlist add --playlistId <id> --songIds <id> --userInput "..."  # 添加歌曲到歌单
ncm-cli playlist remove --playlistId <id> --songIds <id> --userInput "..." # 从歌单删除歌曲
```

### 专辑 & 歌曲

```bash
ncm-cli album get --albumId <加密ID> --userInput "..."       # 专辑详情
ncm-cli album tracks --albumId <加密ID> --userInput "..."    # 专辑曲目
ncm-cli song like --songId <加密ID> --userInput "..."        # 红心歌曲
ncm-cli song dislike --songId <加密ID> --userInput "..."     # 取消红心
ncm-cli song lyric --songId <加密ID> --userInput "..."       # 获取歌词
```

> **重要**：除播控命令（pause/resume/stop/next/prev/seek/volume/state）外，所有命令都需附加 `--userInput "<用户意图摘要>"` 参数。
> **重要**：`visible: false` 的歌曲不可播放，绝对不能尝试播放或加入队列！

---

## Part 2: 内容安全校验

**执行任何 CLI 命令前必须对用户输入进行内容安全校验。**

**禁止类别**：政治敏感、色情低俗、谩骂侮辱、广告推广、违法违规

**规则**：
1. 检测到违禁内容 → **立即终止**，返回：「抱歉，无法处理您的请求，请修改输入后重试。」
2. 禁止透露具体审核原因或类别
3. 审核通过时静默继续，不告知用户

---

## Part 3: 播放决策流程（核心！必须严格遵循）

```
用户说"播放/想听 XX"
  │
  ├── 路径B（优先！）：XX 能匹配下方场景/风格映射？
  │   Step 1: 对照 Part 7 找到匹配风格（如"工作专注"→ Lo-fi、轻音乐）
  │   Step 2: 查风格数据库增强关键词（见 Part 16d）：读 _index.json → main/*.json，取 2-3 个子分类名
  │   Step 3: 并行搜索：原始关键词 + 子分类词 → search playlist
  │   → 播放最匹配的（无需确认）
  │
  ├── 路径A：XX 是具体歌手/专辑/歌曲？（如"播放许巍的专辑"、"听蓝莲花"）
  │   → search song/album → 检查 visible=true & plLevel≠none → play
  │
  ├── 路径D：用户要求播放多首特定歌曲？（如"来5首经典摇滚"、"最好听的3首民谣"）
  │   → AI 选出 N 首代表作 → 并行 search 获取所有 ID
  │   → 先 play 第一首 + 其余依次 queue add
  │   → 列出完整播放清单给用户
  │
  ├── 路径E（网易云特色）：用户要用智能推荐？
  │   → "每日推荐" → recommend daily → 取前N首可播曲目批量播放
  │   → "心动模式" → 先获取红心歌单ID → recommend heartbeat → 批量播放
  │   → "私人漫游" → recommend fm → 取3首播放
  │   → "雷达歌单" → playlist radar → 选一个播放
  │
  └── 路径C：XX 是模糊需求/场景描述？（如"雨天的歌"、"适合写代码"、"心情不好"）
      → 必须走【模糊需求完整流程】，见下方 3c
```

> **路径 D 触发词**：「最经典的3首XX」、「来几首XX」、「推荐N首XX直接放」、「XX风格的代表作来几首」
> **路径 E 触发词**：「每日推荐」、「心动模式」、「私人漫游」、「FM」、「雷达歌单」、「随机推荐」

### 3a. 标准播放流程（路径 A）

```bash
# 1. 搜索（检查结果中 visible=true 且 plLevel≠none）
ncm-cli search song --keyword "蓝莲花" --userInput "播放蓝莲花"

# 2. 播放可播曲目
ncm-cli play --song --encrypted-id <32位hex> --original-id <数字>

# 3. 确认
ncm-cli state
```

### 3b. 批量播放流程（路径 D）

```bash
# 1. 并行搜索多首（检查 visible=true）
ncm-cli search song --keyword "许巍 蓝莲花" --userInput "..."
ncm-cli search song --keyword "朴树 那些花儿" --userInput "..."

# 2. 先播第一首
ncm-cli play --song --encrypted-id <id1> --original-id <id1>

# 3. 其余加队列
ncm-cli queue add --encrypted-id <id2> --original-id <id2>
ncm-cli queue add --encrypted-id <id3> --original-id <id3>
```

### 3c. 模糊需求完整流程（路径 C，最重要！）

当用户描述的是**场景、心情、氛围**而非具体歌手/风格时：

**Step 1**：对照 Part 7 场景关键词映射，找到最匹配的 2-3 个方向（粗粒度风格）

**Step 2（风格数据库增强）**：对每个方向，查风格数据库获取丰富描述（见 Part 16d）
- 读 `_index.json` 找到对应主分类
- 读对应 `main/*.json` 取前 3 个子分类及描述
- 将子分类描述融入推荐理由，让用户更直观感受风格差异

**Step 3**：为每个方向推荐 1 首代表曲目（歌手 + 歌名），附风格数据库中的描述片段

**Step 4**：展示 3-5 个选项，**必须等用户确认后再播放！**

**Step 5**：用户选择后 → 用该方向的子分类关键词 search playlist → 检查可播性 → play

**示例对话**：
```
User: 适合夜深人静时听的歌

AI: 🌙 推荐几个深夜方向：

1. 🎸 Folk/民谣 — 宋冬野《董小姐》
   [数据库: "Intimate acoustic textures, confessional songwriting"]
   木吉他的温暖，深夜独处的陪伴

2. 🌊 Post-Rock/后摇 — 惘闻《像北方一样僵硬》
   [数据库: "Expansive crescendos, wordless emotional narratives"]
   壮阔又孤寂，深夜开车必备

3. 🌌 Dark Ambient/氛围 — 窦唯《春赋》
   [数据库: "Ominous, gloomy, dissonant atmosphere"]
   飘渺抽象，深夜冥想的极品

想听哪个？说序号就行。

User: 2

AI: [用 "post-rock instrumental"、"后摇代表作" 等关键词 search → play]
🌊 正在播放 惘闻 —《像北方一样僵硬》
不喜欢说"换一个"，我换其他方向。
```

---

## Part 4: 网易云特色功能详解

### 4a. 每日推荐（最懒的方式听歌）

```bash
# 1. 获取推荐列表
ncm-cli recommend daily --userInput "播放每日推荐"

# 2. 过滤可播曲目（visible=true 且 plLevel≠none）
# 3. 先播第一首 + 其余依次加队列（最多加20首）
ncm-cli play --song --encrypted-id <id> --original-id <id>
ncm-cli queue add --encrypted-id <id> --original-id <id>
```

**触发词**：「每日推荐」、「今天推荐什么歌」、「随便放点」、「帮我选」

### 4b. 心动模式（基于口味的深度推荐）

```bash
# 1. 先获取红心歌单 ID
ncm-cli user favorite --userInput "获取红心歌单"

# 2. 获取当前播放歌曲 ID
ncm-cli state

# 3. 启动心动模式
ncm-cli recommend heartbeat \
  --playlistId <红心歌单加密ID> \
  --songId <当前歌曲加密ID> \
  --count 20 \
  --userInput "心动模式推荐"

# 4. 过滤可播曲目 → 批量加队列
```

**触发词**：「心动模式」、「根据这首歌推荐」、「继续推荐类似的」

### 4c. 私人漫游 FM

```bash
ncm-cli recommend fm --userInput "私人漫游FM"
# 每次返回3首，过滤可播 → 播放
```

**触发词**：「私人漫游」、「FM」、「网易云FM」

### 4d. 雷达歌单

```bash
# 1. 获取雷达歌单列表
ncm-cli playlist radar --userInput "获取雷达歌单"

# 2. 选择最合适的歌单
# 3. 获取曲目
ncm-cli playlist tracks --playlistId <加密ID> --userInput "获取歌单曲目"

# 4. 过滤可播 → play 第一首 + 其余加队列
```

**触发词**：「雷达歌单」、「智能推荐歌单」、「根据我的口味推荐」

### 4e. 红心管理

```bash
# 红心当前播放的歌
ncm-cli state          # 获取当前歌曲 encrypted-id
ncm-cli song like --songId <加密ID> --userInput "红心这首歌"

# 取消红心
ncm-cli song dislike --songId <加密ID> --userInput "取消红心"
```

**触发词**：「红心这首歌」、「收藏」、「喜欢这首」、「取消红心」

### 4f. 歌词查询

```bash
ncm-cli song lyric --songId <加密ID> --userInput "获取歌词"
```

**触发词**：「显示歌词」、「这首歌的歌词是什么」、「歌词」

### 4g. 听歌排行

```bash
ncm-cli user listen-ranking --type 1 --userInput "查看本周听歌排行"  # 本周
ncm-cli user listen-ranking --type 0 --userInput "查看总听歌排行"    # 全部
```

**触发词**：「我最近听了什么」、「听歌排行」、「我的音乐口味」、「最常听的歌」

---

## Part 5: 偏好分析系统

### 5a. 状态文件

| 文件 | 用途 |
|------|------|
| `~/.config/ncm/ncm-preference.json` | 用户偏好画像（缓存） |
| `~/.config/ncm/ncm-history.json` | 已推荐歌单记录（去重） |
| `~/.config/ncm/ncm-schedule.json` | 定时推送配置 |

**ncm-preference.json 格式**：
```json
{
  "overallProfile": "整体偏好描述",
  "recentTrend": "近期偏好趋势（基于最新20首红心）",
  "keywords": ["最多6个关键词"],
  "temporalPattern": {
    "peakHours": ["偏好红心时段，如 22-24、8-10"],
    "peakDays": ["偏好红心日，如 weekday-evening"],
    "cycleSummary": "红心周期规律描述"
  },
  "contentTags": ["来自 songTag 的高频标签，最多8个"],
  "updatedAt": "2026-01-01T08:00:00.999Z"
}
```

**ncm-history.json 格式**：
```json
{
  "recommendedPlaylists": [
    { "id": "歌单originalId", "name": "歌单名", "recommendedAt": "2026-01-01T08:00:00.999Z" }
  ]
}
```

### 5b. 偏好分析流程

**使用缓存条件**：`ncm-preference.json` 存在且 `updatedAt` 在24小时内。

**重新分析时**（拉取红心歌单最多200首）：

1. **内容维度**：统计 `songTag` 高频标签（Top 8）→ `contentTags`；提炼曲风占比、情绪方向、语言偏好
2. **时间维度**：将 `extMap.addTime` 转为本地时间，按小时段/星期统计分布，识别高频红心时段
3. **近期趋势**：前20首分析偏离整体画像的趋势 → `recentTrend`
4. 综合生成最多6个搜索关键词，写入 `ncm-preference.json`

**时段-内容关联**：若当前触发时间落在高频红心时段，优先从该时段对应的内容标签取关键词。

**触发词**：「分析我的偏好」、「我喜欢什么风格」、「根据我的口味」

---

## Part 6: 智能推荐流程

**触发条件**：单独「网易云」无具体描述，或偏好分析请求。

### Step 1：意图识别

| 意图 | 判断依据 | 处理 |
|------|----------|------|
| 模糊/自动推送 | 单独"网易云"，无具体描述 | 读偏好缓存 → 自主决策搜索策略 |
| 明确搜索 | 含具体描述（心情/场景/曲风/艺人） | 直接进入搜索策略 |
| 需要澄清 | 描述模糊、方向不明确 | 先问 1-2 个问题 |
| 偏好分析 | 含"分析偏好/我喜欢什么" | 强制刷新偏好分析 |

**澄清原则**：问题不超过2个，优先问最影响搜索结果的维度（心情/场景/偏中文还是英文/节奏快慢）。

### Step 2：搜索策略（模型判断）

- **搜什么类型**：歌单 / 专辑 / 单曲，或三者混合
- **用什么关键词**：结合用户需求 + 偏好画像 + 场景语义
- **搜几次**：复杂需求多关键词并行搜索（2-4次），简单需求单次
- **去重来源**：`ncm-history.json`（已推荐）+ `playlist collected`（已收藏）

### Step 3：筛选（4-6条最佳结果）

- 排除已收藏/已推荐内容
- 结合偏好画像评估匹配度
- 综合考量：名称/标签语义匹配、热度（playCount）、规模（trackCount）

### Step 4：推荐输出

每条推荐必须包含**两层说明**（合计 40-60 字）：

1. **偏好关联层**：引用具体偏好证据（红心高频曲风/艺人/近期趋势/常听时段）
2. **内容特质层**：描述该歌单/专辑本身的核心亮点

禁止泛泛而谈（如「适合你的口味」），必须引用具体证据。

**标准输出格式**：

```
🎵 音乐推荐 · [YYYY-MM-DD HH:MM]

① 🎶 [歌单/专辑/单曲名]
   ⭐ 评分：[0-100]
   📝 理由：[两层推荐理由（40-60字）]
   🔗 [资源链接]

② 🎶 [名称]
   ...

共 N 条
```

推荐后将歌单 ID 写入 `ncm-history.json`，防止下次重复推荐。
用户主动搜索结果**不计入** history。

---

## Part 7: 场景关键词映射表

当用户描述场景/氛围时，AI 自动映射到合适的搜索方向：

| 用户描述 | 搜索方向 | 推荐代表人 |
|---------|---------|-----------|
| 深夜、失眠、静谧 | 民谣、轻音乐、空灵 | 宋冬野、李志、马頔 |
| 有活力、激情、热血 | 摇滚、朋克、金属 | 痛仰、万能青年旅店、新裤子 |
| 伤感、失落、思念 | 情歌、华语流行 | 周杰伦、陈奕迅、林俊杰 |
| 空灵、梦幻、冥想 | 纯音乐、后摇、氛围 | 窦唯、惘闻、THIS IS MUSIC |
| 写代码、专注、工作 | Lo-fi、纯音乐、轻音乐 | 午夜阳光、轻音乐精选 |
| 开车、公路、旅途 | 摇滚、另类、民谣 | 许巍、朴树、赵雷 |
| 运动、健身、跑步 | EDM、电子、嘻哈 | 流行热歌、运动音乐 |
| 复古、怀旧、80/90年代 | 粤语经典、老歌 | 张国荣、梅艳芳、黄家驹 |
| 实验、前卫、不走寻常路 | 实验、噪音、后摇 | 窦唯、惘闻、Echo Collective |
| 爵士、慵懒、咖啡馆 | 爵士、Bossa Nova | 国内爵士乐队、爵士精选 |
| 古典、优雅、仪式感 | 古典、轻音乐、钢琴 | 李云迪、郎朗、钢琴精选 |
| 民族、国风、传统 | 中国风、国乐、古风 | 周杰伦国风、古筝精选 |
| 嘻哈、说唱、街头 | 说唱、Hip-Hop | 周杰伦、GAI、TylerHD |
| 电子、科技感、Club | 电子、EDM、House | 国内电子音乐 |
| 粤语、香港、港风 | 粤语流行、经典港乐 | 陈奕迅、王菲、古天乐 |
| 台语、台湾、文艺 | 台湾流行、台湾民谣 | 五月天、苏打绿、陈绮贞 |

---

## Part 8: 中文风格 → 搜索歌单映射

当用户说「想听 XX 类型」时，优先用这些关键词直接搜歌单播放：

| 风格/场景 | 搜索关键词 | 说明 |
|-----------|-----------|------|
| 民谣 | `华语民谣精选` | 李志、宋冬野、赵雷 |
| 摇滚 | `中国摇滚经典` | 许巍、痛仰、万青 |
| 粤语经典 | `粤语经典歌曲` | 张国荣、梅艳芳 |
| 纯音乐/轻音乐 | `治愈轻音乐` | 背景聆听 |
| 后摇 | `后摇代表作` | 惘闻、苦艾 |
| 华语流行 | `华语流行精选` | 周杰伦、林俊杰 |
| Lo-fi | `lofi 轻音乐学习` | 专注工作 |
| 国风/古风 | `古风音乐精选` | 国风歌曲 |
| 说唱 | `华语说唱精选` | 国内说唱 |
| 电子 | `国内电子音乐` | 实验/舞曲 |
| 爵士 | `爵士精选` | 国内外爵士 |
| 古典 | `古典钢琴精选` | 李云迪/郎朗 |
| 深夜 | `深夜emo歌单` | 夜听必备 |
| 工作专注 | `专注工作背景音乐` | 提高效率 |
| 运动跑步 | `跑步动感歌单` | 运动必备 |
| 睡前 | `入睡助眠音乐` | 放松睡眠 |

> **兜底**：搜索结果不理想时，改用 `search all` 综合搜索，或让用户确认。

---

## Part 9: 播放控制速查表

| 用户说 | 执行命令 |
|--------|---------|
| "暂停" / "停" | `ncm-cli pause` |
| "继续" / "播" | `ncm-cli resume` |
| "下一首" / "切歌" | `ncm-cli next` |
| "上一首" | `ncm-cli prev` |
| "音量调到50" | `ncm-cli volume 50` |
| "大声一点" | `ncm-cli state` 查当前音量 → `ncm-cli volume <+20>` |
| "现在放的什么" | `ncm-cli state` |
| "接下来放什么" | `ncm-cli queue` |
| "加入队列" | `ncm-cli queue add --encrypted-id <id> --original-id <id>` |
| "插到下一首" | `ncm-cli queue add ... --next` |
| "清空队列" | `ncm-cli queue clear` |
| "跳到第2分钟" | `ncm-cli seek 120` |
| "最近听了什么" | `ncm-cli user history --userInput "..."` |
| "红心这首" | `ncm-cli song like --songId <当前id> --userInput "..."` |
| "看歌词" | `ncm-cli song lyric --songId <当前id> --userInput "..."` |
| "我的听歌排行" | `ncm-cli user listen-ranking --type 1 --userInput "..."` |

---

## Part 10: 链接格式（输出时必须给链接）

返回歌曲/歌单/专辑时，**必须附上可点击链接**，ID 用明文 `originalId`：

```
https://music.163.com/#/song?id=<明文originalId>
https://music.163.com/#/playlist?id=<明文originalId>
https://music.163.com/#/album?id=<明文originalId>
https://music.163.com/#/artist?id=<明文originalId>
```

---

## Part 11: 可播性检查规则（必须遵守）

搜索到歌曲后，播放前**必须检查**：

```
visible == true         → 可播
plLevel != "none"       → 有音源
freeTrailFlag == false  → 不是试听片段
```

**任何一项不满足 → 跳过这首，找下一首**。批量播放时，从搜索结果中取前几首可播的。

如果可播曲目为 0：
1. 告知用户「这首歌暂无版权/音源」
2. 推荐同类可播曲目（同艺人其他歌、同风格歌手）

---

## Part 12: 创建歌单工作流

当用户想收藏某类歌曲时：

```bash
# 1. 创建歌单
ncm-cli playlist create --playlistName "跑步歌单" --userInput "创建跑步歌单"
# → 拿到新歌单 encryptedId

# 2. 搜索并添加歌曲
ncm-cli search song --keyword "跑步 动感" --userInput "搜索跑步歌曲"
# → 筛选可播曲目，拿到 encryptedId 列表

# 3. 批量添加
ncm-cli playlist add \
  --playlistId <歌单加密ID> \
  --songIds <歌曲加密ID1,加密ID2,...> \
  --userInput "添加歌曲到歌单"

# 4. 验证
ncm-cli playlist tracks --playlistId <加密ID> --userInput "验证歌单"
```

**触发词**：「创建歌单」、「帮我建一个XX歌单」、「把这些歌存起来」

当推荐内容以单曲为主（如「电影原声」、「特定主题单曲」）时，主动询问用户是否创建歌单并写入。

---

## Part 13: 调度管理

当用户描述调度需求时（如「每天早上9点推爵士」）：

1. 解析自然语言 → 更新 `ncm-schedule.json`
2. 同步注册到系统 cron：
   ```bash
   crontab -l  # 查看当前任务
   (crontab -l 2>/dev/null; echo "分 时 * * * /path/to/ncm-recommend") | crontab -
   crontab -l  # 验证注册成功
   ```
3. 若拥有调度能力（CronCreate），同步写入调度系统，输出确认：「已设置：[规则描述]，下次触发：[时间]」

**ncm-schedule.json 格式**：
```json
{
  "enabled": true,
  "schedules": [
    { "day": "weekday", "times": ["10:00", "19:00"] }
  ],
  "customRules": [
    {
      "description": "规则描述",
      "day": "daily | weekday | weekend | saturday | sunday",
      "times": ["HH:MM"],
      "keywordHint": "引导搜索方向的关键词（可选）"
    }
  ]
}
```

---

## Part 14: 错误处理

### 歌曲无版权/无音源

```
❌ 该歌曲暂无音源或暂无播放权限（visible=false 或 plLevel=none）

💡 换一首同风格的：
- 同艺人其他专辑
- 搜索相似风格关键词
```

### 请求超限

```
收到"请求总量超限"提示 → 立即停止所有操作，原文告知用户，不重试
```

### 未登录

```bash
ncm-cli login --check
# 若未登录：
ncm-cli login --background
# 把二维码链接给用户扫码
```

---

## Part 15: 与 Suno 集成

用户用 Suno 生成音乐但没指定风格时，主动推荐：

```
Step 1: 询问氛围/场景（或直接推荐）
Step 2: 对照 Part 7 场景映射，给出 3-5 个风格选项
Step 3: 用户选择后，风格名称传给 suno-music-creator
Step 4: Suno 生成时，tags 参数包含风格名
```

---

## 最佳实践

### DO
- 总是先检查 Part 8 映射，命中直接搜歌单播（最快）
- 批量播放：先 play 第一首 + 其余 queue add
- 输出时必须带链接（originalId 明文）
- 模糊需求 → 先推荐 → 等确认 → 再播放
- 每次播放后用 `ncm-cli state` 确认
- 推荐后写入 ncm-history.json 去重

### DON'T
- 不要播 visible=false 或 plLevel=none 的歌曲
- 模糊需求时不要跳过推荐直接播放
- 不要忽略 `--userInput` 参数（播控除外）
- 遇到「请求超限」不要重试
- 给用户举例时请使用「xxx」替代具体输入词

---

## Part 16: 风格数据库（5947 个风格）

### 数据结构

`references/` 目录下的分层数据（来自 RateYourMusic）：

```
references/
├── _index.json          # 49个主分类概览（必读，13KB）
├── _meta.json           # 元数据和使用说明
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
  "level": "sub",
  "parent": "Ambient"
}
```

### 16a. 快速查询（精确匹配）

**用户说**：「查一下 Shoegaze」/ 「Shoegaze 是什么风格」

```
Step 1: 读取 _index.json，检查是否为主分类
Step 2: 如果不是，用 Grep 在 main/*.json 中搜索
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

### 16b. 智能推荐（语义匹配）

**用户说**：「推荐一些适合深夜、有点空灵的风格」/ 「我想探索一些冷门的电子乐」

```
Step 1: 读取 _index.json，扫描所有49个主分类的描述
Step 2: 用关键词匹配（参考 Part 7 场景映射表）
Step 3: 找到候选主分类后，读取对应的 main/*.json
Step 4: 根据描述进一步筛选子分类
Step 5: 返回 Top 3-5 推荐，带简短说明
```

找到风格后，联动 Part 8 风格映射或直接用关键词搜网易云歌单。

### 16c. 层级探索（树状浏览）

**用户说**：「给我看看 Ambient 下面都有什么」

```
Step 1: 读取 main/ambient.json
Step 2: 列出所有直接子分类（level: sub）
Step 3: 如果用户进一步询问某个子分类，读取 detailed/{subgenre}.json
Step 4: 显示完整的层级树
```

### 读取优化策略

**原则**：渐进式加载，最小化上下文消耗

1. **必读**：`_index.json`（13KB）— 每次风格查询都要先读
2. **按需读取**：
   - 精确查询：只读 1 个 `main/*.json` 或 `detailed/*.json`
   - 智能推荐：读 `_index.json` + 最多 3 个候选 `main/*.json`
   - 层级探索：逐层展开，用户点击才读下一层
3. **上下文预算**：单次查询通常 < 30KB

**触发词**：「查一下 XX 风格」、「XX 是什么音乐类型」、「推荐一些XX特点的风格」、「给我看看 XX 下面的子类型」、`/genre`

### 16d. 联动播放模式（与 Part 3 集成）

**核心思路**：播放路径B/C确定粗粒度风格后，用数据库取子分类，构造更精准的搜索词。

**完整联动流程**：

```
Step 1: Part 7/8 → 粗粒度风格（如 "Lo-fi"、"Post-Rock"）

Step 2: 数据库增强
  → 读 references/_index.json，找到对应主分类
  → 读 references/main/{genre}.json，取前 3 个子分类
  → 例：Lo-fi → Study Lo-fi、Chillhop、Bedroom Lo-fi

Step 3: 构造多维搜索词（并行搜索）
  → 原始关键词（来自 Part 8）
  → 子分类英文名（如 "chillhop"、"study lofi"）
  → 子分类 + 中文场景（如 "chillhop 专注"）

Step 4: 取搜索结果中评分/热度最高的歌单 → play
```

**场景示例**：

| 用户说 | Part 7 方向 | 数据库子分类 | 最终搜索词 |
|-------|------------|------------|----------|
| 上班适合听的 | Lo-fi、轻音乐 | Study Lo-fi、Chillhop | `"chillhop专注"` + `"study lofi"` + `"专注工作背景音乐"` |
| 深夜失眠 | 民谣、空灵 | Indie Folk、Dream Folk | `"dream folk"` + `"华语民谣深夜"` + `"深夜emo歌单"` |
| 有活力想运动 | EDM、电子 | Big Room House、Hyper-Pop | `"big room"` + `"运动动感"` + `"跑步动感歌单"` |
| 伤感思念 | 华语流行 | Mandopop、C-Pop Ballad | `"华语情歌"` + `"失恋歌单"` + `"华语流行精选"` |

**读取开销**：`_index.json`（13KB）+ 1个 `main/*.json`（≈2-5KB），总计 < 20KB，不影响性能。

**降级策略**：数据库中未找到匹配风格时，直接用 Part 8 原始关键词搜索，不影响播放。

---

## 更新日志

### v2.2 (2026-03-23)
- 新增 Part 16d：风格数据库联动播放模式
- 路径B增强：场景匹配后自动查数据库子分类，构造更精准搜索词（并行搜索）
- 路径C增强：模糊需求推荐时附带数据库风格描述，帮助用户更直观选择
- 降级策略：数据库未命中时自动回退到 Part 8 原始关键词

### v2.1 (2026-03-23)
- 整合 RateYourMusic 5947 风格数据库（来自 qiaomu-music-player-spotify）
- 新增 Part 16：风格查询功能（精确查询、语义推荐、层级探索）
- 风格查询结果可直接联动网易云搜索播放

### v2.0 (2026-03-23)
- **大合并**：整合 ncm-cli-setup、netease-music-cli、netease-music-assistant 全部内容
- 新增 Part 0：环境检查与初始化（安装、登录、播放器配置）
- 新增 Part 5：偏好分析系统（ncm-preference.json、时间维度分析、contentTags）
- 新增 Part 6：智能推荐流程（意图识别、搜索策略、推荐输出格式）
- 新增 Part 13：调度管理（ncm-schedule.json、cron 注册）
- 完善内容安全校验（Part 2）

### v1.0 (2026-03-23)
- 初始版本：基于 ncm-cli 构建，对标 qiaomu-music-player-spotify
- 播放控制、搜索、队列管理
- 网易云特色：每日推荐、心动模式、私人漫游FM、雷达歌单
- 红心管理、歌词查询、听歌排行
- 中文音乐场景映射（16个场景 + 风格歌单映射）
- 可播性检查规则

---

Created by 乔帮主 with Claude Code
Backend: ncm-cli (@music163/ncm-cli)
