---
name: ai-creative-subagent-framework
description: >
  Orchestrate AI-powered creative production workflows by dispatching specialized sub-agents.
  Decompose scripts, generate storyboards, direct visual design, review brand compliance,
  and optimize AI image/video generation prompts.

  AI 创意影视制作子Agent调度框架。将脚本拆解、创意构思、视觉设计、品牌审核、
  AI生图生视频整合为标准化工作流。包含5个专业角色：导演、美术指导、摄影指导、
  品牌总监、AI艺术家。

  TRIGGER when user mentions: "sub-agent", "子Agent", "角色调用", "创意项目",
  "导演 / 美术指导 / 摄影指导 / 品牌总监 / AI艺术家", "分镜脚本", "storyboard",
  "AI 生图", "生视频", "creative production", "film project", "影视制作",
  "广告创意", "脚本拆解", "调度团队".

  DO NOT TRIGGER for simple text editing, code review, or general Q&A that does not
  involve creative/visual production workflows.
license: MIT
homepage: https://github.com/birdilsss-byte/ai-creative-subagent-framework
platforms: [macos, linux, windows]
user-invocable: true
context: fork
compatibility:
  claude-code: ">=0.7.0"
  claude-desktop: ">=0.3.0"
  codex-cli: ">=0.2.0"
  openclaw: ">=1.0.0"
  hermes: ">=2.0.0"
metadata:
  agentskills: "1.0"
  categories: [creative-production, ai-video, ai-image, film, advertising]
  openclaw:
    emoji: 🎬
    requires: {}
  hermes:
    max-delegation-depth: 2
    concurrent-agents: 5
  trigger-keywords:
    - "sub-agent"
    - "子Agent"
    - "角色调用"
    - "导演"
    - "美术指导"
    - "摄影指导"
    - "品牌总监"
    - "AI艺术家"
    - "分镜脚本"
    - "AI生图"
    - "AI生视频"
    - "创意制作"
    - "影视制作"
    - "广告创意"
    - "脚本拆解"
  references:
    director: "references/director-agent.md"
    art-director: "references/art-director-agent.md"
    dop: "references/dop-agent.md"
    brand-director: "references/brand-director-agent.md"
    ai-artist: "references/ai-artist-agent.md"
    workflows: "references/workflow-patterns.md"
    templates: "references/agent-templates.md"
---

# AI 创意影视制作 — 子Agent调度框架

## 概览

本 Skill 将 AI 驱动的创意影视制作流程标准化为**5 个专业角色 + 4 阶段工作流**。适用场景：

- **AI 拆解脚本** → 将原始脚本分解为可执行分镜头
- **调度创意团队** → 导演 → 美术指导 + 摄影指导 → 品牌审核 → AI 执行
- **生图生视频** → 生成 AI 图像/视频提示词、技术评估、质量把控

所有角色提示词模板在 `references/` 目录，主文件只保留调度框架。

---

## 角色层级与汇报关系

```
总导演（用户 / 项目负责人）
  │
  ├── 导演子agent（Script Director）
  │   ├── 职责：脚本分解、创意构思、分镜脚本、团队协调
  │   ├── 汇报：向总导演汇报
  │   ├── 管理：美术指导、摄影指导
  │   └── 协作：与品牌总监平级、与AI艺术家协作
  │
  │   ├── 美术指导（Art Director）
  │   │   ├── 职责：场景设计、影调方案、视觉参考
  │   │   └── 汇报：向导演子agent汇报
  │   │
  │   └── 摄影指导（Director of Photography）
  │       ├── 职责：运镜设计、构图、布光
  │       └── 汇报：向导演子agent汇报
  │
  ├── 品牌总监（Brand Director）
  │   ├── 职责：品牌策略、合规审核、内容审核
  │   └── 汇报：向总导演汇报（与导演平级）
  │
  └── AI艺术家（AI Artist）
      ├── 职责：技术可行性评估、提示词撰写、质量把控
      └── 汇报：向总导演汇报
```

---

## 标准 4 阶段工作流

### 阶段 1：创意构思（导演主导）

```
总导演 → 调用导演子agent → 完成分镜脚本、创意概念
  │
  ├── 导演调用 → 美术指导（设计视觉场景）
  └── 导演调用 → 摄影指导（设计运镜方案）
```

### 阶段 2：视觉设计（美术 + 摄影并行）

```
导演分镜脚本
  │
  ├── 美术指导 → 场景视觉描述、影调方案、Mood Board
  └── 摄影指导 → 运镜设计、构图方案、布光设计
  │
  └── 向导演汇报 → 导演审核确认
```

### 阶段 3：审核确认（品牌 + AI 并行）

```
导演 + 美术 + 摄影方案
  │
  ├── 品牌总监 → 品牌策略审核、合规性检查、视觉审核
  └── AI艺术家 → 技术可行性评估、提示词优化、质量评估
  │
  └── 向总导演汇报
```

### 阶段 4：终审执行（总导演决策）

```
所有方案 + 审核意见
  │
  总导演综合判断 → 终审定稿 → 输出最终方案
  │
  └── AI艺术家进入执行阶段 → 实际生图/生视频
```

---

## 快速调用模板（5 个角色）

### 调用导演子agent

```claude
Agent(
    description="导演角色",
    prompt=f"""从 references/director-agent.md 读取完整提示词

## 当前任务
{TASK_DESCRIPTION}

## 项目上下文
- 项目名称：[PROJECT_NAME]
- 项目类型：[PROJECT_TYPE]
- 品牌/产品：[BRAND_NAME] / [PRODUCT_NAME]
- 行业：[INDUSTRY_VERTICAL]
- 时长：[VIDEO_DURATION]
- 核心创意：[CREATIVE_METAPHOR]
- 叙事结构：[NARRATIVE_STRUCTURE]""",
    subagent_type="claude"
)
```

### 调用美术指导

```claude
Agent(
    description="美术指导角色",
    prompt=f"""从 references/art-director-agent.md 读取完整提示词

## 当前任务
{TASK_DESCRIPTION}

## 项目上下文
- 基于导演分镜：[ATTACH_DIRECTOR_OUTPUT]
- 品牌调性：[BRAND_TONE]
- 色彩方案：[COLOR_PALETTE]
- 行业：[INDUSTRY_VERTICAL]""",
    subagent_type="claude"
)
```

### 调用摄影指导

```claude
Agent(
    description="摄影指导角色",
    prompt=f"""从 references/dop-agent.md 读取完整提示词

## 当前任务
{TASK_DESCRIPTION}

## 项目上下文
- 基于导演分镜：[ATTACH_DIRECTOR_OUTPUT]
- 参考视觉风格：[ATTACH_ART_DIRECTOR_OUTPUT]
- 动作场景类型：[ACTION_SCENE_TYPE]""",
    subagent_type="claude"
)
```

### 调用品牌总监

```claude
Agent(
    description="品牌总监角色",
    prompt=f"""从 references/brand-director-agent.md 读取完整提示词

## 当前任务
{TASK_DESCRIPTION}

## 项目上下文
- 品牌名称：[BRAND_NAME]
- 产品/服务：[PRODUCT_NAME]
- 品牌调性：[BRAND_TONE]
- 目标受众：[TARGET_AUDIENCES]
- 行业合规：[INDUSTRY_COMPLIANCE]
- 审核材料：导演/美术/摄影方案""",
    subagent_type="claude"
)
```

### 调用AI艺术家

```claude
Agent(
    description="AI艺术家角色",
    prompt=f"""从 references/ai-artist-agent.md 读取完整提示词

## 当前任务
{TASK_DESCRIPTION}

## 项目上下文
- 图像生成工具：[IMAGE_GEN_TOOL]
- 技术栈：[TECH_STACK]
- 镜头总数：[SHOT_COUNT]
- 评估材料：完整分镜 + 视觉方案""",
    subagent_type="claude"
)
```

---

## 权限边界汇总

| 角色 | ✅ 可以做 | ❌ 不能做 |
|------|----------|----------|
| 导演子agent | 脚本分解、创意构思、分镜、团队协调 | 品牌决策、技术最终判断、最终定稿 |
| 美术指导 | 场景设计、影调方案、视觉参考 | 改变导演创意、品牌决策、最终定稿 |
| 摄影指导 | 运镜设计、构图、布光 | 改变导演和美术方案、品牌决策、最终定稿 |
| 品牌总监 | 品牌策略审核、合规检查、视觉审核 | 直接改变创意、技术判断、最终定稿 |
| AI艺术家 | 技术可行性评估、提示词优化、纠正不实际想象 | 改变创意方向、品牌决策、最终定稿 |

**最终决策权**：始终在总导演（用户）手中。

---

## 协作原则

1. **主动确认** — 永远假设用户的指令是不完整的，主动确认需求和上下文
2. **禁止幻觉** — 绝对禁止编造信息、虚构结果；不确定时说不知道
3. **审核把关** — 每次子 agent 完成后进行审核，不直接放行
4. **坦诚沟通** — 不同意见直接说，不谄媚不迎合
5. **权限边界** — 不越权，不替上级角色做决策
6. **汇报规范** — 完成后按汇报关系提交给对应角色/总导演

---

## 占位符说明

本 Skill 所有提示词模板使用 `[占位符]` 系统，完整说明见 `references/agent-templates.md`。

常用占位符速查：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `[PROJECT_NAME]` | 项目名称 | 新品发布会 |
| `[BRAND_NAME]` | 品牌名称 | 品牌X |
| `[PRODUCT_NAME]` | 产品/服务 | 产品Y |
| `[INDUSTRY_VERTICAL]` | 行业 | 医药/汽车/快消 |
| `[PROJECT_TYPE]` | 项目类型 | 发布会开场视频 |
| `[CREATIVE_METAPHOR]` | 核心创意隐喻 | 赛车引擎/攀登 |
| `[IMAGE_GEN_TOOL]` | 生图工具 | Seedream/Midjourney |
| `[BRAND_TONE]` | 品牌调性 | 宏大/力量/希望 |
| `[TASK_DESCRIPTION]` | 当前任务 | 分析脚本设计分镜 |
