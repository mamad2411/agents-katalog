---
name: novel-drafting
description: Use when 中文小说项目已经具备调研文件，并需要按章节起草、经过审查闸门、执行连续性检查或从阻塞状态恢复起草
---

# 小说起草

## 概述

验证调研阶段产物，从任意中断点恢复进度，并通过子 agent 循环执行章节写作与审查，直到计划中的整本小说完成且所有审查闸门通过。

流程推进受 lint 监督。控制器不能仅凭聊天中的口头声明推进起草状态；它必须读取项目产物并运行起草验证器。

## 何时使用

- 项目状态为 `research_complete` 或 `draft_blocked`
- 所有必需调研文件均存在且内容充分
- 用户希望开始或继续写章节
- 在审查通过前，起草流程必须保持阻塞

## 入口闸门

开始写作前，检查：
- `00-project/workflow-status.md` 的 status 为 `research_complete` 或 `draft_blocked`
- `00-project/workflow-status.md` 的 current stage 与起草阶段兼容
- `00-project/success-criteria.md`
- `20-story/characters.md`
- `20-story/plot-outline.md`
- `20-story/foreshadowing.md`
- `30-draft/chapter-plan.md`

如果任一项缺失或内容薄弱，立即停止并报告阻塞。

## 验证闸门

在推进工作流状态之前，对小说根目录运行起草验证器：

```bash
node --experimental-strip-types <skill-root>/scripts/validate-drafting-project.mts --project-root <project-root> --mode Entry
node --experimental-strip-types <skill-root>/scripts/validate-drafting-project.mts --project-root <project-root> --mode Progress
node --experimental-strip-types <skill-root>/scripts/validate-drafting-project.mts --project-root <project-root> --mode Completion
node --experimental-strip-types <skill-root>/scripts/validate-drafting-project.mts --project-root <project-root> --mode WordCount
node --experimental-strip-types <skill-root>/scripts/validate-drafting-project.mts --project-root <project-root> --mode WordCount --chapter chapter-03
```

使用方式：
- `Entry`：起草开始或恢复前
- `Progress`：writer 或 reviewer 的输出改变当前章节状态后
- `Completion`：设置 `draft_complete` 或 `Next Allowed Skill: novel-delivery` 之前
- `WordCount`：只做字数检查，不推进工作流，也不检查 review / completion gate

`WordCount` 规则：
- 不带 `--chapter` 时，检查所有已有章节文件的章节字数是否落在目标区间内
- 带 `--chapter chapter-XX` 或 `--chapter 3` 时，只检查指定章节
- `WordCount` 不检查全书完成状态；全书总字数仍由 `Completion` 负责

字数验证优先规则：
- 当 agent 只需要确认章节或单章字数是否达标时，必须优先运行 `WordCount` 模式
- 不要在聊天中自行估算字数，也不要临时搓新的统计命令来替代 validator
- 只有在调试 `check-word-count.mts` 本身时，才允许绕开这个入口

验证器输出具有最终权威性。只要失败，就不得推进流程。

## 项目根目录识别

本 skill 中的所有路径都应视为相对于小说项目根目录，而不是默认相对于工作区根目录。

在读写 `00-project`、`30-draft`、`40-review` 或 `50-delivery` 之前，按以下规则识别根目录：
- 如果当前目录已经包含 `00-project/workflow-status.md`，就使用当前目录
- 否则，如果当前目录下恰好只有一个子级书籍目录包含 `00-project/workflow-status.md`，就使用那个子目录
- 否则，停止并报告项目根目录存在歧义

一旦识别出有效的小说根目录，就不要继续在同级目录树中反复搜索。

## 恢复逻辑

检查：
- `30-draft/chapters/`
- `40-review/chapter-reviews/`

从第一个缺失、审查未通过或尚未标记为通过的章节继续。

## Writer 子 Agent 契约

只向 writer 提供：
- `00-project/project-brief.md`
- `10-research/style-research.md`
- `20-story/characters.md`
- `20-story/plot-outline.md`
- `20-story/foreshadowing.md`
- 已批准的前文章节摘要，或为保持连续性所需的已批准正文
- `30-draft/chapter-plan.md` 中当前章节的目标

writer 只输出当前章节草稿。

## Reviewer 子 Agent 契约

reviewer 需要检查：
- 章节字数是否符合目标
- 是否符合当前章节目标
- 是否符合整体大纲
- 人物一致性
- 是否出现不允许的提前揭示
- 与前文章节的连续性
- 节奏与可读性

当 reviewer 或 controller 只需要确认字数是否达标，而不是做完整 `Progress` / `Completion` 验证时：
- 运行 `node --experimental-strip-types <skill-root>/scripts/validate-drafting-project.mts --project-root <project-root> --mode WordCount`
- 如需点查单章，运行 `node --experimental-strip-types <skill-root>/scripts/validate-drafting-project.mts --project-root <project-root> --mode WordCount --chapter chapter-XX`
- 不要自行实现字数统计逻辑

reviewer 必须将结构化审查文件写入 `40-review/chapter-reviews/chapter-XX-review.md`，并返回 `通过` 或 `不通过`。
reviewer 不负责重写章节正文。

## 修订循环

- 若 review 返回 `不通过`，只把审查结论回传给 writer。
- 同一章节最多尝试 3 次草稿。
- 第 3 次仍失败时，停止并标记 `draft_blocked`。

对应要求：
- 若 review 返回 `不通过`，只把审查结论回传给 writer
- 同一章节最多尝试 3 次草稿
- 第 3 次仍失败时，停止并标记 `draft_blocked`

## 状态更新

起草开始时：
- 将状态设为 `draft_in_progress`

某章节失败次数过多时：
- 将状态设为 `draft_blocked`
- 列出被阻塞的章节与原因

当所有章节和最终审查都通过时：
- 将状态设为 `draft_complete`

## 全书完成闸门

最后一个计划章节通过后，执行整书级审查：
- 将已完成章节与 `30-draft/chapter-plan.md` 对比
- 验证每个 `40-review/chapter-reviews/chapter-XX-review.md` 都已通过
- 将总字数与目标区间对比

只有在上述检查都通过后，才能设置 `draft_complete`。

## 风险信号

- "这一章差不多了，继续吧"
- "审查看到了问题，但后面再改也行"
- "这个揭示很精彩，提前放出来也没关系"
- "第三次重试应该已经够继续了"

出现以上说法都意味着：不要推进流程。

## 常见自我说服

| 借口 | 现实 |
|------|------|
| "缺一个文件不该妨碍创作" | 缺文件就说明契约不完整。 |
| "审查放松一点没关系，后面章节会补救" | 后续章节只会放大连续性损伤。 |
| "再多试一次也没坏处" | 无限重试会掩盖真正阻塞的工作。 |

## 下一步

在 `draft_complete` 之后，下一个允许使用的 skill 是 `novel-delivery`。

验证器模式和强制产物检查见 `lint-contract.md`。
