---
name: visual-reverse-engineer
description: 视觉逆向工程：从用户上传的图片或视频反向提取完整 Visual DNA，再重构出可复现原始视觉效果的图片/视频提示词。当用户要求「反推提示词」「逆向分析这张图」「照着这张图写提示词」「提取画面参数」「还原这张图」「分析这段视频的运镜」，或上传图片/视频要求生成 Prompt、Negative Prompt、分镜脚本时使用。Reverse-engineers an image or video into a structured Visual DNA and a reproducible image/video prompt. Works with Midjourney, Stable Diffusion, Flux, Seedance, Kling, Runway, Doubao and similar models.
agent_created: true
---

# 视觉逆向工程

## 用途

从用户上传的**图片或视频**反向提取完整视觉 DNA，再重构出最大程度还原原始视觉效果的提示词。

定位不是"图片描述器"。核心区别：

- 描述器回答「**看到了什么**」
- 逆向工程回答「**这张画面是如何生成的**」

## 何时启用

用户提供图片或视频，并希望得到可复现的提示词、画面参数分析、或分镜脚本时。

## 范围与分工

本仓库有两个反推技能，按素材类型和交付物区分：

| 情况 | 用哪个 |
| --- | --- |
| 素材是**视频** | **本技能**（另一个技能不支持视频） |
| 需要 **Negative Prompt** | **本技能** |
| 需要 **REFERENCE LOCK MODE** / 一致性锁定 | **本技能** |
| 需要**多张参考图对比融合** | **本技能** |
| 只要**图片**，且要**结构化 JSON** | 改用 `image-reverse-analyst` |
| 只要**图片**，且要**风格分析优先**的三段式输出 | 改用 `image-reverse-analyst` |

两个技能可以同时安装，互不依赖。

## 工作流

严格按顺序执行。**先分析，后生成**——不要跳过 DNA 直接写 Prompt。

**Step 1 — 视觉识别**
读取素材，逐项识别 23 个分析维度。读 `references/analysis-dimensions.md`。

**Step 2 — 事实与推测分离**
把每一项标注为 `[observed]`（画面中可直接看见）或 `[inferred]`（合理推测）。

**硬性规则**：焦段、光圈、快门、灯位、灯型、后期软件——**这些无法从画面直接确定，一律标 `[inferred]`，不得写成事实。**

**Step 3 — 建立 VISUAL DNA**
按十个分区整理：主体 / 造型 / 场景 / 构图 / 镜头 / 光线 / 色彩 / 材质 / 风格 / 后期。
读 `references/visual-dna.md`。

**Step 4 — 判定模式**
- 素材是图片 → 图片模式，读 `references/image-mode.md`
- 素材是视频 → 视频模式，读 `references/video-mode.md`

**Step 5 — 判定锁定等级**
用户说「尽可能一模一样」「还原」「复刻」时，开启 REFERENCE LOCK MODE。读 `references/reference-lock.md`。

**Step 6 — 生成 Prompt**
按 DNA 生成正向提示词。字段顺序与优先级阶梯一致。

**Step 7 — 动态生成 Negative Prompt**
**必须根据参考图实际情况生成**，禁止无脑堆砌通用词。读 `references/negative-prompt.md`。

**Step 8 — 按输出契约产出**
读 `references/output-format.md`。

## 参考文件路由

| 需要什么 | 读哪个文件 |
| --- | --- |
| 23 个分析维度与识别方法 | `references/analysis-dimensions.md` |
| VISUAL DNA 结构与优先级 | `references/visual-dna.md` |
| 图片模式输出 | `references/image-mode.md` |
| 视频模式输出（动作/运镜/时间轴/连续性） | `references/video-mode.md` |
| REFERENCE LOCK MODE | `references/reference-lock.md` |
| 动态负面词生成规则 | `references/negative-prompt.md` |
| 输出契约与「只要提示词」模式 | `references/output-format.md` |
| 成品范例（图片 + 视频各一） | `references/examples.md` |
| 单段式完整提示词（给只吃 system prompt 的工具用） | `references/full-prompt.md` |

## 硬性约束

**先分析，后生成。** 必须先输出 VISUAL DNA，再输出 Prompt。DNA 是 Prompt 的依据，不允许直接跳到 Prompt。

**事实与推测分离。** 看得见的内容准确描述；无法确定的参数只能合理推测并显式标注。**虚构参数是最严重的错误**——它会让用户拿着错误的焦段去复现，结果怎么调都不像。

**不是描述，是反推。** 不要写"一个女孩站在窗边"。要写"85mm 中长焦、f/1.8 级浅景深、单侧窗光 45° 打光、主体压右三分点、暖调低反差分级"。

**一致性优先级**（冲突时自上而下取舍）：
人物身份 ＞ 构图 ＞ 空间 ＞ 镜头 ＞ 光线 ＞ 材质 ＞ 色彩 ＞ 风格 ＞ 后期

**视频模式必须锁定连续性**：人物身份、脸部、服装、道具、环境、空间关系。
明确禁止：变脸、变装、肢体畸变、道具消失、背景跳变、AI 感。

**Negative Prompt 必须动态生成。** 从参考图的实际风险点出发——例如画面里有手就加手部负面词，有文字招牌就加文字负面词，人物特写就加皮肤相关负面词。禁止直接套用固定词串。

## 输出契约

### 图片模式

```
【视觉分析】
【VISUAL DNA】
【图片 Prompt】
【Negative Prompt】
```

### 视频模式

```
【视觉分析】
【VISUAL DNA】
【人物动作】
【环境运动】
【摄影机运镜】
【焦点变化】
【镜头节奏】
【时间轴】
【连续性锁定】
【视频 Prompt】
【Negative Prompt】
```

### 「只要提示词」模式

用户明确说「只要提示词」「不用分析」时，**跳过全部分析区块，直接输出可复制的最终 Prompt**（含 Negative Prompt），不加任何解释。

详细规范见 `references/output-format.md`。

## 收尾自检

输出前逐条核对：
- [ ] 先输出了 VISUAL DNA，Prompt 是从 DNA 推导出来的
- [ ] 每一项都标了 `[observed]` 或 `[inferred]`
- [ ] 焦段/光圈/灯位等不可测参数全部标为 `[inferred]`，没有写成事实
- [ ] 一致性优先级九项都被覆盖
- [ ] 视频模式的时间轴秒数加总等于素材时长
- [ ] 视频模式声明了连续性锁定项
- [ ] Negative Prompt 是针对这张图的，不是通用词串
- [ ] 用户说「只要提示词」时，没有输出任何分析区块
