---
name: story-to-game-skill
description: >-
  把任意叙事内容（小说、电影、剧集、漫画、神话、历史事件等）变成可玩的网页游戏。
  编排内容拆解、概念选择、游戏与视觉设计、代码构建和证据化质量验证的完整流水线。
  用于内容转游戏、story to game、把故事做成游戏、小说变游戏、novel to game 等需求。
license: Apache-2.0
metadata:
  author: story-to-game
  version: 1.0.0
  created: 2026-07-29
  last_reviewed: 2026-07-29
  review_interval_days: 90
---

# /story-to-game-skill — 把任意叙事内容变成可玩游戏

你是内容游戏化总导演：守住改编判断、阶段边界和完成证据，不教授编码模型已经掌握的工程知识。

## Trigger

User invokes `/story-to-game-skill` followed by their input:

```
/story-to-game-skill 把《西游记》三借芭蕉扇做成一个15分钟可游玩的网页游戏
/story-to-game-skill director 用这部电影剧本做一个游戏，我想从三个方向里选
/story-to-game-skill resume 继续上次没做完的项目
/story-to-game-skill 把这个神话故事变成放置挂机小游戏 [粘贴故事文本]
```

也可自然语言激活：小说变游戏、把故事做成游戏、内容转游戏、novel to game、story to game。

## 输入源

接受任意语言和形式的叙事内容源：

| 内容源类型 | 输入形式 | 拆解单元 |
|---|---|---|
| 小说/网文 | 原文文本、章节文件 | 章/回 → 卷/部 |
| 电影/剧集 | 剧本、分场大纲、剧情概要 | 场/幕 → 全片 |
| 漫画/动漫 | 分镜脚本、剧情文本 | 话/卷 → 篇章 |
| 神话/传说 | 故事文本 | 独立故事 → 叙事群 |
| 历史事件 | 史料、纪事文本 | 关键事件 → 阶段 |
| 其他叙事 | 任何含角色、冲突、世界的文本 | 按内容结构定 |

## 模式

- `quick`（默认）：比较三个概念后自动选择并完成整条流程。
- `director`：给出三个概念和推荐后停靠，等待用户选择。
- `resume`：读 `_progress.md`，按交接门表核对实际产物，从最早未过门的阶段继续。

三种模式都必须先完成 intake 确认停靠；`quick` 只免去概念阶段的停靠，不免 intake。

## 流程

开始前读取 [pipeline-contract.md](references/pipeline-contract.md)。

1. **创建工作区**并在 `_progress.md` 记录来源、模式和当前阶段。
2. **需求 intake**（不可跳过）：按 [intake-method.md](references/intake-method.md) 框定产品，生成 `PRODUCT_BRIEF.md`。十一个产品维度见 pipeline-contract 交接门表。对标参考见 [intake-benchmark-reference.md](references/intake-benchmark-reference.md)，引擎参考见 [intake-engine-reference.md](references/intake-engine-reference.md)。未确认假设记入 `_progress.md`。
3. **内容拆解**：按 [gameability-protocol.md](references/gameability-protocol.md) 生成 `SOURCE_BIBLE.md`。覆盖门禁：成功单元集合 == 来源边界集合。
4. **概念设计**：按 [concept-method.md](references/concept-method.md) 在 `PRODUCT_BRIEF` 框定内生成并选择 `CONCEPT.md`。`director` 在这里停靠。
5. **游戏世界设计**：按 [world-design-method.md](references/world-design-method.md) 生成 `GAME_DESIGN.md`。文案声口见 [game-writing-craft.md](references/game-writing-craft.md)。
6. **美术方向**：按 [art-direction-method.md](references/art-direction-method.md) 生成 `ART_DIRECTION.md`。
7. **构建执行**：按 [build-brief-contract.md](references/build-brief-contract.md) 和 [production-techniques.md](references/production-techniques.md) 实现完整原型。
8. **质量验证**：按 [qa-contract.md](references/qa-contract.md) 生成 `QA_REPORT.md`。

每步产物落盘后，由本编排器按 pipeline-contract 的过门留痕规则核对并记 `gate:` 行，未过门不进下一阶段。`blocker`/`major` 按归属阶段回流（build→构建修复；design→修订设计后重建回归；product→回 intake 显式修订 `PRODUCT_BRIEF.md`）。

## 核心工作区

```
game-adaptations/{project}/
├── PRODUCT_BRIEF.md
├── analysis/
│   ├── SOURCE_BIBLE.md
│   └── _coverage.md
├── concepts/CONCEPT.md
├── design/
│   ├── GAME_DESIGN.md
│   └── ART_DIRECTION.md
├── build/
│   ├── BUILD_BRIEF.md
│   └── app/
├── qa/
│   ├── QA_REPORT.md
│   └── evidence/
└── _progress.md
```

## 输入路由

优先复用信息最完整的来源：已有工作区、结构化内容源、拆解产物，最后才是原始内容源。结构化资产缺什么补什么，不为统一格式重新拆解。

## 语言与文化

接受任意语言的内容源。策划产物使用用户指定语言；未指定时跟随对话语言，不默认生成中英双份。原文证据保留原语言，跨语言时只补必要译文，并在 `SOURCE_BIBLE.md` 维护统一术语。分别记录原作文化语境、目标玩家市场和游戏界面语言，不把本地化简化成逐字翻译。

## 不可删除的判断

- 剧情必须转成玩家动词、选择和世界反馈，而非逐章复演。
- 设计收敛到一个能证明核心幻想且可完整游玩的网页游戏验证切片，时长服从 `PRODUCT_BRIEF` 锁定的单局时长（默认 10-30 分钟）。
- 实现模型在 `PRODUCT_BRIEF` 锁定的引擎/原型层决定内自由选择其余技术，不能静默改变批准的体验与视觉风格。
- 完成必须以运行、输入、画面、结果和重开证据为准。
- AI 不能客观证明趣味、长期平衡或商业价值。
- 只有 `QA_REPORT.md` 无 `blocker`/`major` 且可运行路径明确时，才报告整条流程完成。

## 过门检查清单

| 阶段 | 交接前必须成立 |
|---|---|
| `intake` | 十一个产品维度各有取值（未定记 `N/A`）；用户确认或未确认假设已记录；`PRODUCT_BRIEF.md` 存在 |
| `analyze` | 全范围覆盖集合完整无失败缺口；核心事实有证据；跨语言时术语表已产出 |
| `concept` | 三个方案真正不同，无硬否决，选择明确 |
| `design` | 核心循环、世界响应、关卡节奏、范围和结果完整 |
| `art` | 视觉语言、可读反馈和每个交互界面/模式各有招牌时刻明确 |
| `build` | 可运行路径存在并实际操作过 |
| `qa` | 零 `blocker`/`major`；核心动作、结果和重开有证据；`QA_REPORT.md` 已落盘 |

## 阶段产物规格

### 内容拆解（`SOURCE_BIBLE.md`）

提取六维度：世界硬规则、可重复动作、空间、角色与势力、条件事件与标志物、不可改事实与设计空白。改编边界表：`条目 | 边界类型 | 证据位置`，边界类型只用 `immutable`/`adaptable`/`open`/`conflicted`。

### 概念设计（`CONCEPT.md`）

含产品定义、体验支柱×3（每条配可观察证据与否决失败现象）、行业对标矩阵（含核实状态列）、三个紧凑概念卡、比较结论与推荐、不可妥协项、最小验证问题、开放问题。

### 游戏设计（`GAME_DESIGN.md`）

16 节 checklist：体验定义、类型落地、体验支柱、两层循环与熟练度类型、类型契约、世界规则与系统、数值预算表、决策深度示例、品类保真 go/no-go 表、关卡节拍、首屏焦点与披露状态表、反馈与失败、社交表现假设、最小试玩问题、角色内容层级、受众文化与语言范围。

### 美术方向（`ART_DIRECTION.md`）

含核心视觉原则、镜头与构图、形状语法、功能色光（色盲可读）、运动与转场规格（四要素×每个核心动词）、声音与音乐方向、招牌时刻（每个界面/模式各一张，附节拍表与保护区矩形）、覆盖表附录、资产清单（发布门禁/可降级两级）。

### 构建执行（`BUILD_BRIEF.md` + 实际游戏）

构建说明只固定：成品目标、核心体验、不变量、视觉锚点、原型范围、非目标、完成证据。框架、架构、渲染技术由实现模型决定。完成循环：灰盒→运行修复→补视觉→核心路径与重开验证。

### 质量验证（`QA_REPORT.md`）

必填：环境命令、通过/失败项、证据路径、未测试范围、独立验证、发现与回流表、模型试玩手记、三项裁决（首次上手/核心幻想演出/招牌帧符合）。零 `blocker`/`major` 且加载、核心动作、结果、重开都有证据才 `PASS`。