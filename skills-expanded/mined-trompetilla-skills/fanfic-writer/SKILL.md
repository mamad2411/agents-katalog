---
name: fanfic-writer
version: 1.0.0
description: Automated novel writing assistant for creating long-form fiction with systematic workflow - genre research, outline generation, worldbuilding, chapter-by-chapter writing with quality control.
homepage: https://github.com/openclaw/clawd
metadata:
  openclaw:
    emoji: "📖"
    category: "creative"
---
# Fanfic Writer - Automated Novel Writing Assistant

This is a complete novel writing pipeline with 6 phases and rigorous quality control.

---

## 格式规范（强制性要求）

**⚠️ 每次回复必须遵守：**

1. **Markdown 格式必须正确**
   - 表格必须有表头和分隔行
   - 列表项之间要有空行
   - 段落之间要有空行
   - 代码块必须用 ``` 包裹

2. **禁止文字挤成一团**
   - 不同章节之间用 `---` 分隔
   - 使用清晰的标题层级
   - 重要内容用列表或表格展示

---

## Phase 1: Genre Selection

- 用户直接指定题材（如："都市异能"、"玄幻修仙"、"历史架空"等）
- 也可以提供详细设定："帮我写一本关于XXX的小说"
- 记录用户选择，进入下一阶段

---

## Phase 2: Scope Definition

- 用户选定题材后，确认总字数（≤300,000 words）
- 保存到工作目录中的 `0-book-config.json`
- Remember user's choices persistently

---

## Phase 3: Main Outline Generation

- 基于选定题材和字数，生成完整剧情大纲
- Structure: 主线剧情 + 分卷规划（如有）+ 关键转折点
- Present to user for confirmation/modification
- 确认后保存到 `1-main-outline.md`

---

## Phase 4: Chapter Planning

**提示词：**

> "请根据字数要求和前期设定编写每章的规划，要注意网文的阅读节奏，规划好每章的作用和剧情。每章必须包含具体的场景、人物、冲突点和剧情走向，确保整体节奏张弛有度。"

**生成要求：**

- 基于主线大纲，生成完整章节列表
- 总章节数需符合字数规划
- 每章必须包含以下要素：

**格式案例：**

```
第一卷 卷名（第001-020章）
第001章 章节名
- 场景与视角：第几人称/谁的视角
- 地点：具体地点
- 人物：出现的主要人物
- 环境描写：氛围/天气/特殊环境
- 冲突点：本章核心冲突
- 转折：剧情转折点
- 剧情：详细剧情走向
- 结尾：章末悬念/钩子
```

**流程：**

1. 读取 `1-main-outline.md` 主线大纲
2. 按格式生成完整章节规划
3. Present to user for confirmation
4. 确认后保存到 `2-chapter-plan.json`

---

## Phase 5: Worldbuilding

**提示词：**

> "需要全文阅读前面的设计来编写设定，尤其是章节规划。需要阅读 `1-main-outline.md` 主线大纲和 `2-chapter-plan.json` 章节规划，考虑剧情需要设定人物卡、势力范围、技能、道具等详细设定。确保世界观设定能够支撑全部100章的剧情需求。"

**生成要求：**

- 生成并细化小说设定：
  1. 世界观（时间/空间/规则/时代背景）
  2. 主角色（姓名/性格/背景/目标/成长线/所属势力）
  3. 配角群像（每卷配角及其势力归属）
  4. 力量/技能体系（含道具、积分、能力）
  5. 关键道具/地点
  6. 势力分布图（各势力立场、关系）

**流程：**

1. 读取 `1-main-outline.md` 主线大纲
2. 读取 `2-chapter-plan.json` 章节规划
3. 根据剧情需要生成完整设定
4. Present to user for confirmation
5. 确认后保存到 `3-world-building.md`

---

## Phase 6: Chapter-by-Chapter Writing

Once chapters and worldbuilding are confirmed, begin writing.

**⚠️ 严格子流程（必须按顺序执行，每步需用户确认）：**

```
6.1 生成详细大纲 → 6.2 用户确认 → 6.3 起草正文 → 6.4 质量检查 → 6.5 用户确认 → 6.6 保存章节
     ↑                    ↑                               ↑
     └────────────────────┴───────────────────────────────┘
                              (用户不确认则返回修改)
```

**禁止：**

❌ 跳过任何步骤或未经用户确认直接保存

---

### 6.1 Generate Chapter-Specific Outline

**步骤：**

1. 读取 `1-main-outline.md` 主线大纲
2. 读取 `3-world-building.md` 世界观设定
3. 读取上一章正文（保持连贯性）
4. 生成本章详细大纲

**详细大纲必须包含：**

- 本章主题
- 故事作用（推进/转折/铺垫/高潮等）
- 字数要求
- 场景分解（逐幕，含字数分配）
- 涉及角色
- 关键对话
- 章节钩子

**格式要求：**

- 使用 Markdown 格式
- 表格、列表必须正确换行
- 清晰易读

**Token记录：**

记录本步骤消耗到 `token-report.json`

---

### 6.2 Chapter Outline Validation (用户确认环节)

**必须执行：**

- 向用户展示详细大纲
- 等待用户确认或修改意见
- **用户确认后，立即保存到 `5-chapter-outlines.json`**

**禁止：**

❌ 未经用户确认直接写正文

**Token记录：**

记录本步骤消耗到 `token-report.json`

---

### 6.3 Draft Writing

**步骤：**

1. 读取本章详细大纲（从 `5-chapter-outlines.json`）
2. 基于大纲起草正文
3. 字数限制：每段 ≤2000 字
4. 保持与前文章节风格一致

**格式要求：**

- 每次回复必须确保 Markdown 格式正确
- 特别是换行，避免文字挤成一团
- 使用代码块展示正文内容

**Token记录：**

记录本步骤消耗到 `token-report.json`

---

### 6.4 Quality Check (质量检查)

**必须展示结构化 QC 报告：**

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 符合详细大纲 | ✅/⚠️/❌ | |
| 符合主线大纲 | ✅/⚠️/❌ | |
| 角色行为/语言 | ✅/⚠️/❌ | |
| 无逻辑矛盾 | ✅/⚠️/❌ | |
| 与前文衔接 | ✅/⚠️/❌ | |
| 字数达标 | ✅/⚠️/❌ | |
| 无重复描写 | ✅/⚠️/❌ | |
| 伏笔/线索 | ✅/⚠️/❌ | |

**QC 结论格式：**

- ✅ **PASS** → 进入 6.5
- ⚠️ **WARNING** → 列出问题，建议修改但可继续
- ❌ **REVISE** → 必须返修，重新 QC

**Token记录：**

记录本步骤消耗到 `token-report.json`

---

### 6.5 User Confirmation (用户确认正文)

**必须执行：**

- 向用户展示完整正文
- 等待用户确认
- **用户说"保存"或"OK"后才能执行 6.6**

**禁止：**

❌ 未经用户确认直接保存文件

**Token记录：**

记录本步骤消耗到 `token-report.json`

---

### 6.6 File Output

**步骤：**

1. 保存章节到 `chapters/第XXX章_章节名.txt`
2. 文件命名：`第{3位数字}章_{章节名}.txt`
3. 更新 `4-writing-state.json` 进度
4. 生成保存确认信息

**完成后：**

- 报告已保存的文件路径
- 更新字数统计
- 准备进入下一章

**Token记录：**

记录本步骤消耗到 `token-report.json`

---

## Token Usage Tracking (Token 统计)

**记录位置：** `token-report.json`

**必须在每个步骤记录：**

- Phase 切换
- 大纲生成
- 用户确认交互
- 正文起草
- 质量检查
- 文件保存

**格式：**

```json
{
  "book_id": "...",
  "total_prompt_tokens": 0,
  "total_completion_tokens": 0,
  "total_tokens": 0,
  "steps": [
    {
      "phase": "6.1",
      "chapter": 1,
      "action": "generate_outline",
      "timestamp": "...",
      "prompt_tokens": 500,
      "completion_tokens": 2000,
      "total": 2500
    }
  ]
}
```

---

## Phase 7: Book Integration & Whole-Book Check

After all chapters completed:

### 7.1 Merge Book

- Concatenate all chapters
- Generate `final/{书名}_完整版.txt`

### 7.2 Whole-Book Quality Check

**Critical Step:** Must perform comprehensive check on complete book:

| 检查项 | 内容 |
|--------|------|
| **设定一致性** | 角色能力是否前后一致？世界观规则有无矛盾？ |
| **大纲符合度** | 整体剧情是否偏离主线大纲？章节与规划是否对应？ |
| **剧情逻辑** | 情节推进是否合理？有无逻辑漏洞？ |
| **人物性格** | 角色行为是否符合人设？成长弧线是否自然？ |
| **伏笔回收** | 前文伏笔是否在后文回收？有无废弃伏笔？ |
| **节奏把控** | 整体松紧是否得当？有无拖沓/跳跃？ |
| **字数统计** | 是否达到目标字数？各章节字数分配是否合理？ |

**流程：**

1. 读取完整书籍
2. 读取主线大纲、世界观设定
3. 逐卷/逐章检查上述 7 项
4. 生成问题报告 (`final/quality-report.md`)
5. 如有问题：定位章节 → 提出修改方案 → 用户同意后重写 → 重新检查
6. 无问题 → 通过

---

## Workspace Structure

```
novels/
└── {timestamp}_{book_title}/
    ├── 0-book-config.json              # 总配置
    ├── 1-main-outline.md               # 主线大纲
    ├── 2-chapter-plan.json             # 章节规划
    ├── 3-world-building.md             # 世界观设定
    ├── 4-writing-state.json            # 写作进度
    ├── 5-chapter-outlines.json         # 各章详细大纲索引
    ├── 6-session-context.json          # 短期记忆
    ├── token-report.json               # Token 消耗统计
    ├── chapters/                       # 章节文件
    │   ├── 第001章_开篇.txt
    │   └── ...
    ├── drafts/                         # 草稿/修订版本
    └── final/                          # 最终版本
        ├── {书名}_完整版.txt
        └── 7-whole-book-check.md
```

---

## Quality Control Checklist

Every chapter must pass:

- [ ] 符合详细大纲
- [ ] 符合主线大纲方向
- [ ] 角色行为/语言符合人设
- [ ] 无逻辑矛盾
- [ ] 与前文章节衔接自然
- [ ] 字数达标（±10%）
- [ ] 无重复描写
- [ ] 伏笔/线索处理一致

---

## Important Notes

1. ✅ **Stop and wait for user confirmation at:**
   - Phase 3, 4, 5 ends
   - Phase 6.2 (大纲确认)
   - Phase 6.5 (正文确认)
2. ✅ **Save progress immediately after each chapter completes**
3. ✅ **Always use file I/O for novel content** - never rely on conversation context
4. ✅ **Auto-save session context after every user interaction**
5. ✅ **Record token usage at every step** to `token-report.json`
6. ✅ **Ensure Markdown format is correct** in every reply
