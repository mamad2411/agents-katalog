---
name: edu-ip-poster
description: |
  将教材内容转化为迪士尼/皮克斯IP风格的教育海报和AI生图提示词。
  核心能力：教材→IP剧情→Prompt，支持7大IP主题库（疯狂动物城/冰雪奇缘/狮子王/玩具总动员/海底总动员/迪士尼公主/赛车总动员）。
  输出类型：预习卡/测验卡/词汇卡/语法卡，适配Midjourney/DALL-E/Gemini多工具。
  触发词：做预习卡、做词汇海报、用疯狂动物城做、IP海报、AI生图prompt、教育海报
---

# 教育IP海报生成器 (edu-ip-poster)

## 📋 SKILL概述

将教材内容转化为迪士尼/皮克斯IP风格的教育海报和AI生图提示词。

**核心能力**：
- 教材内容 → IP剧情设计 → AI生图Prompt
- 支持7大IP主题库
- 预习卡/测验卡/词汇卡/语法卡多种类型
- Midjourney/DALL-E/Gemini多工具适配

---

## 🎯 使用场景

| 场景 | 输入 | 输出 |
|------|------|------|
| 英语预习卡 | 教材PDF截图 | 3-5天分日预习卡Prompt |
| 词汇海报 | 单词列表 | IP角色教单词海报Prompt |
| 语法海报 | 语法点 | 情景化语法海报Prompt |
| 测验卡 | 练习题 | 空白答案的测验卡Prompt |
| 手抄报 | 主题 | 可打印手抄报Prompt |

---

## 🚀 工作流程

```
Step 1: 内容分析
├── 提取核心知识点（词汇/句型/语法）
├── 分析教学目标
└── 规划内容分布（如分3-5天）

Step 2: IP剧情设计  
├── 选择适合的IP主题
├── 设计故事线/场景
└── 分配角色职责

Step 3: Prompt生成
├── 应用IP专属模板
├── 融入教学内容
└── 输出完整Prompt

Step 4: 自动生图
├── 将 Prompt 保存为临时文件
├── 调用 scripts/generate_image.py（自动替换版权角色名）
└── 输出图片路径，展示给用户

Step 5: 检查与修正
└── 文字错误修复指南
```

### ⚙️ Step 4 脚本调用说明

生成 Prompt 后，必须自动调用脚本生成图片，不要让用户手动操作：

```bash
# 将 prompt 保存到临时文件，然后调用脚本
python3 ~/.claude/skills/edu-ip-poster/scripts/generate_image.py \
  --file /tmp/edu_ip_prompt.txt \
  --type 预习卡
```

**--type 参数对应**：

| 卡片类型 | --type 值 |
|---------|----------|
| 预习卡（竖版） | 预习卡 |
| 预习卡（横版） | 预习卡横版 |
| 测验卡 | 测验卡 |
| 词汇卡 | 词汇卡 |
| 封面 | 封面 |

**注意**：
- 脚本内置版权角色名自动替换（Prompt 中可正常使用 Judy Hopps、Elsa 等角色名）
- 如果用户未设置 `LAOZHANG_API_KEY` 环境变量，脚本会报错提示，此时告知用户运行：`export LAOZHANG_API_KEY='你的密钥'`
- 生成的图片默认保存在 `~/edu-ip-poster/output/` 下，用 Read 工具展示给用户

---

## 🎭 IP主题库

### 快速选择指南

| IP主题 | 适合话题 | 主要角色 | 典型场景 |
|--------|---------|---------|---------|
| 🦊 疯狂动物城 | 职业/身份/国家/规则 | Judy, Nick, Bogo | 警局/海关/街道 |
| ❄️ 冰雪奇缘 | 天气/季节/情绪/魔法 | Elsa, Anna, Olaf | 冰宫/雪山/Arendelle |
| 🦁 狮子王 | 动物/家庭/成长/自然 | Simba, Mufasa, Timon | 荣耀石/草原 |
| 🧸 玩具总动员 | 玩具/房间/物品/数字 | Woody, Buzz, Rex | Andy房间/玩具箱 |
| 🐠 海底总动员 | 海洋/颜色/大小/方向 | Nemo, Dory, Marlin | 珊瑚礁/海底 |
| 👸 迪士尼公主 | 城堡/服装/颜色/童话 | 各公主 | 城堡/舞会 |
| 🚗 赛车总动员 | 交通/速度/方向/地点 | McQueen, Mater | 赛道/小镇 |

---

## 📐 Prompt架构

### 必须包含的5个部分

```
1. 【核心风格定调】
   - 艺术风格（Disney 2D cartoon / Pixar 3D style）
   - 氛围色调（warm and soft / magical winter）
   - 质感（hand-painted watercolor feel）

2. 【结构化布局】
   - 标题区（Title banner）
   - 内容分区（Left/Right section 或 Top/Bottom）
   - 练习区（Practice section）

3. 【IP角色融入】⚠️ 关键
   - 角色必须与教学内容互动
   - 不是摆pose，而是doing something
   - 使用speech bubble承载句型

4. 【文本与连接】
   - 文字必须有载体（sign/tag/bubble/label）
   - 使用hand-drawn arrow连接概念
   - 中英双语标注

5. 【装饰与比例】
   - 主题相关的边框装饰
   - 指定aspect ratio（通常3:4竖版）
   - 背景氛围描述
```

### Prompt模板

```
[Style Definition]
Disney 2D cartoon animation style, hand-painted watercolor feel, 
{IP_NAME}-inspired educational poster, {COLOR_PALETTE}, 
detailed but organized composition.

[Title Banner]
Title banner at top with decorative {THEME_ICONS}: "{TITLE_EN} {TITLE_CN}"

[Main Content - Section 1]
{SECTION_LABEL}:
{CHARACTER_NAME} ({CHARACTER_DESCRIPTION}) {ACTION_WITH_PURPOSE}.
Speech bubble reads: "{DIALOGUE_EN} {DIALOGUE_CN}"

Labeled elements with hand-drawn arrows:
- {ITEM_1}: "{LABEL_EN_1} {LABEL_CN_1}"
- {ITEM_2}: "{LABEL_EN_2} {LABEL_CN_2}"

[Main Content - Section 2]
...

[Practice Section] (可选)
Bottom section with word boxes / blank spaces for practice.

[Decorations]
Border decorated with: {THEME_DECORATIONS}.
Background: {BACKGROUND_DESCRIPTION}.
Aspect ratio: 3:4, vertical orientation.
```

---

## 🦊 疯狂动物城完整模板

### 角色库

| 角色 | 英文名 | 外观描述 | 适合用途 |
|------|--------|---------|---------|
| 朱迪 | Judy Hopps | gray rabbit, blue police uniform, purple eyes, determined | 讲解/指导/欢迎 |
| 尼克 | Nick Wilde | red fox, green Hawaiian shirt OR police uniform, sly smile | 对话/示范/互动 |
| 牛局长 | Chief Bogo | water buffalo, police chief uniform, stern, arms crossed | 考核/测验/评估 |
| 豹警官 | Clawhauser | cheetah, front desk officer, friendly, loves donuts | 欢迎/前台/信息 |
| 闪电 | Flash | sloth, very slow movements, DMV worker | 慢动作/强调 |

### 场景库

| 场景 | 英文描述 | 适合话题 |
|------|---------|---------|
| 警局大厅 | ZPD lobby with "To Protect and Serve" banner | 职业/身份 |
| 海关入境 | Zootopia Customs entrance hall | 国家/来源 |
| 街道巡逻 | Zootopia busy street with diverse animals | 交通/礼貌 |
| 会议室 | ZPD briefing room with Bogo at front | 指令/规则 |

### 装饰词汇

```
Border decorated with: police badges, carrots, paw prints, 
traffic cones, ZPD logos, orange carrot patterns, 
small handcuffs in cartoon style.
```

### 完整示例 - 国家介绍预习卡

```
Disney 2D cartoon animation style, hand-painted watercolor feel, 
Zootopia-inspired educational poster, warm and soft colors, 
detailed but organized composition.

Title banner with police badge decorations: 
"Welcome to Zootopia! 欢迎来到动物城！"
Subtitle: "Where are you from? 你来自哪里？"

Scene: Zootopia Customs entrance hall with wooden "CUSTOMS" sign.

Judy Hopps (gray rabbit in blue police uniform with badge) 
stands behind customs desk, waving happily and welcoming visitors.
Speech bubble reads: "Welcome! Where are you from? 欢迎！你来自哪里？"

Four cute cartoon animal characters standing in a line, 
each holding their country flag:

1. A friendly panda wearing red Chinese vest, holding China flag
   Wooden tag label: "China 中国"
   
2. A gentleman fox wearing British bowler hat, holding UK flag
   Wooden tag label: "UK 英国"
   
3. A proud bald eagle with American themed outfit, holding USA flag
   Wooden tag label: "USA 美国"
   
4. A friendly moose with red plaid shirt, holding Canada maple leaf flag
   Wooden tag label: "Canada 加拿大"

Nick Wilde (red fox in green Hawaiian shirt) stands on the right,
pointing at himself with a friendly gesture.
Speech bubble: "Hi, I'm Nick. I'm from the USA. 嗨，我是尼克。我来自美国。"

Hand-drawn arrows connect each flag to its country label.

Border decorated with: police badges, carrots, paw prints.
Background: Soft pastel watercolor Zootopia cityscape.
Aspect ratio: 3:4, vertical orientation.
```

---

## ❄️ 冰雪奇缘完整模板

### 角色库

| 角色 | 英文名 | 外观描述 | 适合用途 |
|------|--------|---------|---------|
| 艾莎 | Elsa | platinum blonde braid, ice blue dress, magical powers | 展示/变化/魔法 |
| 安娜 | Anna | ginger hair with white streak, green/pink dress, cheerful | 互动/鼓励/活力 |
| 雪宝 | Olaf | snowman, carrot nose, twig arms, loves warm hugs | 趣味讲解/可爱 |
| 克里斯托夫 | Kristoff | blonde, ice harvester outfit | 户外/冒险 |

### 场景库

| 场景 | 英文描述 | 适合话题 |
|------|---------|---------|
| 冰雪城堡 | Elsa's ice palace on the mountain | 魔法/冬天/建筑 |
| 阿伦戴尔 | Arendelle castle and village | 四季/城市 |
| 雪山 | snowy mountains with Northern Lights | 天气/自然 |

### 装饰词汇

```
Border decorated with: snowflakes, ice crystals, 
Nordic patterns, frozen vines, small snowmen, 
sparkling snow effects.
```

---

## 📝 测验卡特别规范

### ⚠️ 核心原则：绝不显示正确答案

```
【❌ 错误】
Look at Judy. (✓ She / He) is a police officer.

【✅ 正确】
Look at Judy. ( She / He ) is a police officer.
□ She  □ He
```

### 测验卡专用Prompt关键词

```
quiz card format, blank answer options, 
EMPTY checkboxes showing "□", 
no answers revealed, test worksheet style,
student needs to fill in answers.

Each question shows EMPTY checkbox options:
"□ Option A" and "□ Option B"
NO checkmarks, NO circles, NO highlighting indicating correct answers.
```

### 测验卡结构模板

```
Title: "[角色]'s Test! [角色]的考核！"

Part 1: [题型名称]
[题目 + 空白选项 □ □]

Part 2: [题型名称]  
[两列内容 + 空白连线区域]

Part 3: [题型名称]
[情景描述 + 空白选项 ○ A ○ B]

Bottom: 鼓励语 + 角色挥手
"Great job! 你真棒！"
```

---

## 🔧 文字错误修复指南

AI生成的图片常见中文错误，修复方法：

### 方法1: Canva覆盖

1. 上传图片到Canva
2. 添加与背景相近的矩形遮盖错误文字
3. 使用"站酷快乐体"等手写风格字体添加正确文字
4. 调整字体颜色匹配背景

### 方法2: Photoshop内容识别

1. 用内容识别填充移除错误文字
2. 使用文字工具添加正确内容

### 推荐字体

- 站酷快乐体（免费商用）
- 汉仪糖糖体
- 方正喵呜体

---

## 📏 输出规格

| 用途 | 推荐比例 | 分辨率 |
|------|---------|--------|
| 预习卡（竖版） | 3:4 | 1200×1600 |
| 预习卡（横版） | 4:3 | 1600×1200 |
| 测验卡 | 3:4 | 1200×1600 |
| 词汇卡 | 1:1 | 1200×1200 |
| 封面 | 3:4 | 1200×1600 |

---

## 🔗 与其他SKILL的关系

| SKILL | 关系 | 说明 |
|-------|------|------|
| **pdf2preview** | 上游调用方 | Mode B调用本SKILL生成预习卡Prompt |
| **pdf2lesson** | 内容来源 | 可接收其提取的教学内容 |
| **teacher-visual-prompter** | 可整合 | 本SKILL是其"课件配图"模式的增强版 |
| **edu-poster-gen** | 可整合 | 本SKILL覆盖其IP海报功能 |
| **handcopy-poster-gen** | 并行 | 手抄报是不同品类，保持独立 |

### 整合建议

**teacher-visual-prompter** 可简化为路由层：
```
用户输入
   ↓
检测意图
   ├── "课件配图" → lesson-image-prompter
   ├── "教育海报/IP海报" → edu-ip-poster (本SKILL)
   └── "手抄报" → handcopy-poster-gen
```

---

## 📚 使用示例

### 示例1: 完整预习卡生成

**用户**: 帮我用疯狂动物城做人教版三下Unit 1的预习，这个单元学习"I'm from..."

**Claude**:

```
=== Step 1: 内容分析 ===

📚 教材: 人教版三年级下册 Unit 1
🎯 核心句型: I'm from... / Where are you from?
📝 核心词汇: China, UK, USA, Canada, boy, girl, teacher, student

📅 预习计划 (3天):
- Day 1: 国家名称 + 自我介绍
- Day 2: He/She人称 + 身份词汇
- Day 3: 礼貌用语 + 综合对话

=== Step 2: IP剧情设计 ===

🎭 主题: 动物城警局国际警员报到

【故事线】
Day 1: 海关报到 - 各国警员自我介绍
Day 2: 认识搭档 - 学习He/She区分男女
Day 3: 文明执勤 - 礼貌用语实践

=== Step 3: Day 1 Prompt ===

[完整Prompt输出...]

=== Step 4: 自动生图 ===

[将Prompt保存到临时文件，调用 generate_image.py --type 预习卡，展示生成的图片]
```

### 示例2: 快速词汇卡

**用户**: 帮我做一张身体部位的词汇卡，用海底总动员

**Claude**:

```
Disney Pixar underwater animation style, Finding Nemo inspired,
vibrant coral reef colors, educational vocabulary poster.

Title: "Body Parts with Nemo! 和尼莫学身体部位！"

Center: Large diagram of Nemo (clownfish) with labeled body parts:
- Head pointing to: "head 头"
- Eye pointing to: "eye 眼睛"
- Fin pointing to: "fin 鳍 (like our arm 像我们的手臂)"
- Tail pointing to: "tail 尾巴"

Dory (blue tang) in corner with speech bubble:
"Touch your head! 摸摸你的头！"

Border: Bubbles, seaweed, small fish.
Background: Soft blue ocean gradient.
Aspect ratio: 1:1
```

[调用 generate_image.py --type 词汇卡，展示生成的图片]

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0 | 2026-02-10 | 从pdf2preview Mode B独立，形成通用SKILL |
| 1.1 | 2026-02-15 | 新增 scripts/ 自动生图，集成版权角色名替换 |
