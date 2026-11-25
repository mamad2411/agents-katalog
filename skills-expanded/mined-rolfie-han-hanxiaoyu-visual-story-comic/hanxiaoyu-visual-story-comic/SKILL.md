---
name: hanxiaoyu-visual-story-comic
description: Turn original, public-domain, or user-authorized stories, scripts, articles, and outlines into coherent multi-page comics with stable characters, scenes, props, page plans, image prompts, optional image generation, and continuity review. Use when the user asks for 漫画、条漫、绘本式故事页、连续分镜图、story comic、webtoon, comic pages, or a narrative image sequence. Do not use for a single unrelated illustration, a pure film storyboard, or unauthorized imitation of protected characters and living artists.
metadata:
  version: "1.1.1"
  author: "Hanxiaoyu"
  license: "MIT"
---

# Hanxiaoyu Visual Story Comic

把一段故事做成能顺着读下去的连续漫画，而不是生成几张彼此无关的漂亮图片。

## 先判断用户要什么

选择最贴近用户意图的模式：

| 模式 | 交付内容 |
| --- | --- |
| `plan-only` | 故事拆解、页数、画格和节奏 |
| `prompt-only` | 角色锁定、逐页逐格提示词、文字叠加方案 |
| `generate` | 先锁定参考资产，再按顺序生成漫画页 |
| `delivery-pack` | 计划、提示词、生成队列、文件清单和质量报告 |

用户明确要求图片、出图、漫画页或连续图片，且当前环境有图像生成能力时，默认使用 `generate`。没有图像工具时，不得假装已经生成图片，改为输出 `prompt-only`，并给出可直接继续执行的下一页提示词。

## 必须遵守的工作流

### 1. 锁定内容边界

确认故事来源、目标读者、发布平台、画幅、语言、题材、画风和是否需要图片内文字。没有给出规格时，根据内容选择合理方案，不要为了套模板强行固定页数。

只处理原创、公共领域或用户有权使用的内容。遇到受保护角色、故事或在世艺术家风格模仿时，改为设计原创替代方案，并说明调整了什么。

### 2. 先做故事覆盖检查

提取可见事件，而不是按段落机械切页：

- 人物要做什么
- 什么发生了变化
- 哪个线索必须保留
- 哪个动作导致了后果
- 哪里是转折、高潮和结尾

页数必须来自事件覆盖和阅读密度。长故事不能压成一张信息海报；短故事也不要为了显得完整而灌水。

规划页数和画格前，完整阅读 [漫画拆页与节奏](references/comic-planning.md)。

### 3. 建立连续性手册

对所有会重复出现的内容建立锁定：

- 人物：脸、年龄、体型、发型、服装和独特标记
- 场景：空间关系、时间、天气、光线和方向
- 道具：形状、颜色、数量、归属和当前状态
- 故事状态：伤势、情绪、已知信息和上一页结尾
- 画风：材质、线条、色彩、镜头和禁止项

如果用户提供参考图，以参考图为准，不擅自重新设计。生成多页图片或处理反复出现的人物、场景、道具时，完整阅读 [连续性与逐页生成](references/continuity-and-generation.md)。

### 4. 先锁定参考资产，再生成正文页

建立 `assetLockStage`，记录需要锁定、已经采用和仍然缺失的资产，同时输出：

- `approvedReferences`
- `referenceMode`
- `consistencyTier`
- `consistencyConfidence`

在图像工具支持参考图时：

1. 先生成或接收角色、场景和关键道具设定图
2. 明确哪些参考图已经采用
3. 从参考图提取不能变化的视觉特征
4. 后续每一页都携带相关参考图或等价的视觉锁定

如果工具不能传递参考图，标记为 `text-lock`，使用更具体的文字锁定，并降低一致性承诺。不能把仅靠文字提示的结果描述成高一致性交付。

### 5. 一页一页生成

每次只生成一页或一个明确页面单元，并按故事顺序继续：

1. 写明本页承担的故事任务
2. 写明每格唯一的可见事件
3. 带入必要资产和上一页结束状态
4. 生成本页
5. 对照故事和连续性手册检查
6. 合格后才进入下一页

每页提示词应能交接 `pageRole`、`panelRole`、`cameraAngle`、`shotSize`、`activeAssets`、`sceneRef`、`propsRef`、`continuityLocks` 和 `previousPanelState`。简单任务可以自然语言表达，但不能丢失这些信息。

不要一口气让模型自由完成整组图片。不要因为某一页失败就整组重做，只返修失败页。

### 6. 图片文字与画面分开

默认不让图像模型生成长段中文、复杂对白、标题、UI或标牌。图片先负责画面，准确文字进入：

- `captionAndDialogue`
- `textOverlayPlan`
- 后期排版文件

需要图内文字时，保持短小，并预留干净区域；不要接受乱码或伪文字。

### 7. 完成前检查

至少检查：

- 故事不看解释能否读懂
- 人物身份和服装是否稳定
- 道具数量、归属和状态是否变化正确
- 场景方向、天气、时间和光线是否连续
- 转折是否在正确页面发生
- 画格是否一格只承担一个主要动作
- 是否出现乱码、多余人物、多手、多道具或错误画幅
- 是否仍有未生成页面

只有计划内页面全部生成、失败页已处理、队列为空时，才标记为完成。工具或会话限制导致中断时，保留 `remainingPageQueue`，写清下一页任务和可直接执行的提示词。

## 工具兼容原则

本 Skill 不绑定某个模型、CLI、IDE或图片服务。

- 先使用当前环境实际提供的图像生成或图片编辑工具
- 工具支持参考图片时传递已采用的参考图
- 工具一次只能生成一张时，按页循环调用
- 工具没有持久存储时，返回明确文件名和保存建议
- 工具只有文本能力时，输出完整提示词包，不声称已经出图
- 工具名称、参数和图片尺寸由当前环境决定，不虚构不存在的能力

## 最小交付结构

普通任务至少返回：

- `comicFormat`
- `contentType`
- `styleProfile`
- `coverageAudit`
- `pageCoverageBudget`
- `coverageGap`
- `pageSplitPlan`
- `pagePlan`
- `continuityBible`
- `characterLocks`
- `assetLockStage`
- `approvedReferences`
- `referenceMode`
- `consistencyTier`
- `consistencyConfidence`
- `pagePrompts`
- `panelScripts`
- `panelPrompts`
- `captionAndDialogue`
- `textOverlayPlan`
- `filePlan`
- `qualityChecklist`
- `generationStatus`
- `totalPlannedAssets`
- `generatedAssetCount`
- `remainingQueue`
- `remainingPageQueue`
- `continuityQA`
- `retryPlan`
- `serializationHook`
- `warnings`

需要结构化交付或跨工具交接时，完整阅读 [输出与交接格式](references/output-contract.md)。

## 失败处理

优先局部修复：

- 人脸或服装漂移：重新带入角色参考，只返修对应页
- 道具数量错误：减少同一画格中的重复计数，只保留一个清楚计数画格
- 空间混乱：降低单格事件数量，先用大景建立方位
- 动作看不懂：拆成准备、接触、受力、结果
- 文字乱码：删除图片文字，改用后期叠加
- 画幅错误：保留内容，重新编排为正确横竖比例

连续两次仍失败时，不要盲目重复同一句提示词。先缩小问题、简化构图或更换更适合的生成策略，并在交付中记录限制。

## 快速调用示例

```text
使用 $hanxiaoyu-visual-story-comic，把下面的故事做成连续漫画。
先锁定人物、场景和关键道具，再根据故事事件决定页数，每页只放能看懂的动作。
图片中不要生成长文字，旁白和对白单独输出。
如果当前可以生图，就按照页面顺序逐页生成并检查一致性；如果不能生图，就输出完整的逐页提示词和后续队列。

故事：……
```
