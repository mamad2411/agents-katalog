---
name: novel-writer-workflow-guide
description: "Use when user starts a novel project, asks how to organize writing, or signals phase transition - acts as phase router that activates the correct sub-skill for the current novel-writing phase"
allowed-tools: Read, Grep
---

# Novel Writer 阶段路由器

## 激活条件

- 用户说"我想写小说" / "开一个小说项目" / "写本书"
- 用户问"下一步做什么" / "现在该干嘛"
- 用户已经在项目里，发出阶段切换信号（"大方向定了" / "开始写 Ch X" / "全书校一遍"）

## 两大阶段 + 五个子 skill

```
Phase 1 · 构思阶段（与用户讨论）
└── novel-ideation
    └─ 主题 / 人物 / 世界观 / 目标读者 / 核心冲突

Phase 2 · 执行阶段
├── novel-framework（搭框架）
│   └─ 大纲 / 钩子矩阵 / 任务分解 / 人物卡 / 世界观细化
│
├── novel-chapter-sop（单章写作 SOP）
│   └─ 8 步 SOP + 两轮 agent review
│
├── novel-consistency-guards（一致性护栏，贯穿写作期）
│   └─ 硬约束锁 + 跨章一致性四表
│
└── novel-finalization（收口定稿）
    └─ 多轮 review / 最小改动 / git 节奏
```

## 主 skill 职责

这个 skill **不负责讲细节**，只做三件事：

1. **听意图判阶段**
2. **激活对应的子 skill**
3. **阶段切换时做 checkpoint**

细节全部在子 skill 里。

## 如何识别当前阶段

听用户语言线索：

| 用户说 | 阶段 | 激活 skill |
|---|---|---|
| "主题应该是什么" / "主角什么性格" / "这个题材怎么破" / "我有个想法" | Phase 1 | `novel-ideation` |
| "大方向定了" / "现在搭大纲" / "分章" / "节奏怎么排" | Phase 2 框架 | `novel-framework` |
| "开始写 Ch X" / "继续写下一章" / "这一章怎么写" | Phase 2 写作中 | `novel-chapter-sop` + `novel-consistency-guards` |
| "改一下 Ch X" / "Review 一遍" / "agent 再审一次" | Phase 2 写作中 | `novel-chapter-sop` + `novel-consistency-guards` |
| "全书校一遍" / "准备发布" / "定稿前再扫一遍" | Phase 2 收口 | `novel-finalization` + `novel-consistency-guards` |

## 阶段切换 Checkpoint

每次从一个阶段过渡到下一个，主 skill 先确认前一个阶段的交付物齐了。

### Phase 1 → Phase 2（构思 → 搭框架）

切换前确认：
- [ ] 主题和核心冲突已定（一句话能说清楚）
- [ ] 主角动机、背景、弧线已定
- [ ] 目标读者画像清晰（年龄带、平台、对标剧/书）
- [ ] `宪法.md`（constitution）已写
- [ ] `specify`（规格文档）已写
- [ ] 至少一轮 `clarify`（模糊点澄清）完成

**提示语**：
> "在进入框架搭建之前，我们需要确认构思阶段的核心决策都已落定。你能一句话说清楚：主题是什么？主角要什么？为什么读者会追？如果这三个都答得上，我们可以切到 `novel-framework`。"

### Phase 2 框架 → 写作（搭框架 → 开始写）

切换前确认：
- [ ] 大纲完整（至少章节级梗概）
- [ ] 分卷/分幕结构确定
- [ ] 钩子矩阵已填（每章末钩子强度评分）
- [ ] 人物卡完整（主角+女主+核心反派+关键配角）
- [ ] 世界观设定文档完整
- [ ] 任务分解（40 章/20 章各自的依赖、优先级）

**提示语**：
> "框架齐全了。接下来进入写作阶段。我会启用 `novel-chapter-sop` 管单章流程，`novel-consistency-guards` 在后台做跨章一致性检测。每写一章跑一遍 SOP。"

### Phase 2 写作 → 收口（初稿完成 → 定稿）

切换前确认：
- [ ] 所有章节初稿已写完
- [ ] 每章都跑过单章 SOP（两轮 agent review）
- [ ] 跨章一致性四表已维护到最新
- [ ] 伏笔矩阵全部回收
- [ ] 硬约束脚本扫描全部通过

**提示语**：
> "全稿完。进入收口阶段。我会启用 `novel-finalization` 指导多轮 review、最小必要改动、git 分批提交。"

## 子 skill 的横向关系

- `novel-chapter-sop` 执行时会**主动引用** `novel-consistency-guards` 的硬约束清单
- `novel-framework` 输出的文档会被 `novel-chapter-sop` 作为单章写作的上下文
- `novel-finalization` 会**再调用**一次 `novel-consistency-guards` 做全书扫描
- `novel-ideation` 的输出（constitution）会被所有后续 skill 作为硬红线来源

## Novel Writer 七步方法论对应

本主 skill 所用的七步法，分布在各子 skill 里：

| 七步命令 | 对应 skill | 阶段 |
|---|---|---|
| /constitution | `novel-ideation` | Phase 1 |
| /specify | `novel-ideation` | Phase 1 |
| /clarify | `novel-ideation` | Phase 1 |
| /plan | `novel-framework` | Phase 2 |
| /tasks | `novel-framework` | Phase 2 |
| /write | `novel-chapter-sop` + `novel-consistency-guards` | Phase 2 |
| /analyze | `novel-finalization` + `novel-consistency-guards` | Phase 2 |

## 不同规模项目调整

### 短篇（1-3 万字）

简化流程：**只用** `novel-ideation` + `novel-chapter-sop`。跳过 `novel-framework`，直接写；跳过 `novel-finalization`，只做一次 review 收。

### 中篇（3-10 万字）

标准流程：**五个 skill 全用**，但 `novel-framework` 轻量化（不分卷、三到四幕即可）。

### 长篇（10-30 万字）

标准流程：**五个 skill 全用**，重点在 `novel-consistency-guards` 和 `novel-finalization`。跨章 bug 会爆炸式增长，必须脚本化维护。

### 超长篇连载（50 万字+）

**循环流程**：`novel-framework` → `novel-chapter-sop`（写 5-10 章） → `novel-finalization`（阶段性定稿）→ 回到 `novel-framework`（下一批章节的铺垫和调整）。不是一次性全走完七步。

## 成功模式

### 高生产力模式（一周启动）

```
Day 1：novel-ideation（2-3 小时）→ constitution + specify + clarify
Day 2：novel-framework（2-3 小时）→ 大纲 + 钩子矩阵 + 人物卡
Day 3：开始 novel-chapter-sop，写 Ch 1（2-3 小时）
Day 4-N：每天 1-2 章，`novel-consistency-guards` 后台扫
完稿后：novel-finalization（占 30-50% 总工时）
```

### 探索性模式（边写边改）

```
Week 1：novel-ideation + 轻量 novel-framework
Week 2-3：novel-chapter-sop 写 2-3 章探索性章节
Week 4：回到 novel-framework，基于探索调整大纲和人物
Week 5-N：结构化 novel-chapter-sop
完稿后：novel-finalization
```

### 冲刺模式（NaNoWriMo 类）

```
Day 1：快速 novel-ideation + novel-framework（4 小时，粗版）
Day 2-27：密集 novel-chapter-sop，每天 2000 字
         省略部分单章 SOP（每 5 章才跑一次 agent review）
Day 28-30：novel-finalization 紧急收口
```

## 用户偏离时

**如果用户跳过 Phase 1 直接说"开始写第一章"**：

> "我注意到你直接跳到写作。没有构思阶段的 constitution 和 specify，单章 SOP 里的一致性检查会没有红线对照。建议先花 30 分钟走 `novel-ideation`，至少把主题、主角、目标读者定死。你要继续跳过吗？"

**如果用户坚持跳过**：

> "好。启用 `novel-chapter-sop`，但你需要手动提供每一章的'上下文'（主角在这一章要干什么、和谁冲突）。一致性检查只能做机械项（引号/破折号/姓氏），跨章语义一致性要你自己把关。"

**如果用户在写作期想回去改设定**：

> "修改设定是合理的。我们先把当前写作状态标记为暂停，回 Phase 1 激活 `novel-ideation` 做设定调整，调整完再回 `novel-chapter-sop`。已经写完的章节需要根据新设定过一遍 `novel-consistency-guards`。"

## 进度追踪

### 视觉进度指示器

当你进行工作流时，我会显示你的位置：

```
Phase 1 · 构思阶段
✅ constitution  完成
✅ specify       完成
✅ clarify       完成（3 个模糊点已澄清）

Phase 2 · 执行阶段
🔄 framework    进行中...
⏸️ chapter-sop  待定
⏸️ finalization 待定
```

### 里程碑

- **Phase 1 完成**：设定红线已锁，可以进入框架层
- **Phase 2 框架完成**：大纲 + 人物 + 世界观齐全，可以开始写
- **Phase 2 写作完成**：全稿初稿完，进入收口
- **Phase 2 收口完成**：定稿入库，可以发布

## 你总是掌控

- 跳过不需要的 skill
- 调整以适应你的写作风格
- 随时从一个阶段回到前一个阶段
- 工具服务于你，不是反过来

---

**记住**：这个主 skill 只做路由。具体怎么干，在各子 skill 里。

**准备开始了吗？告诉我你现在在哪个阶段，或者你想从哪里开始。**
