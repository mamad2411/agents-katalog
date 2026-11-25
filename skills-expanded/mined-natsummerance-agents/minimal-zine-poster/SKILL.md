---
name: minimal-zine-poster
description: |
  将主题、短文、文章、物品、氛围或照片转化为纸质质感的极简 Zine 海报：大面积负空间（70-90%）+ 单一小焦点元素 + 实验性排版 + 一个明确的高饱和色彩强调。支持生成模式、照片输入模式、参考分析模式、仅 prompt 模式与分析+生成五种路由。触发场景：用户给出主题词/一句话/文章/情绪物件要求"做一张海报"，或要求分析参考图提炼可复用风格系统。边界：不做数据可视化、UI 设计与无源摄影虚构；参考图只学视觉语法，不复制源文字/品牌/精确构图。
source_project: LiamGvchi/gc-minimal-zine-poster
tags: [zine, poster, minimal, paper-texture, editorial]
related_skills: ["photo-relic-editorial", "gathered-scenes-zine", "photo-abstract-editorial"]
---

# Minimal Zine Poster — 极简 Zine 海报

## R (Reading) — 源项目核心设计

> "Turn content or visual references into a coherent paper-poster system… A successful generation must remain a sparse vertical paper poster with **one clear visual event**, not a commercial ad or a generic collage template. A successful analysis must explain what stays fixed and what can change." 质检锚点：约 70%-90% 开放纸面，主视觉事件占画布 8%-25%，主色占画布 0.8%-2.5%。

（来源：vendor/LiamGvchi__gc-minimal-zine-poster/SKILL.md 及 references/prompt-compiler.md）

## I (Interpretation) — 方法论骨架

**五种路由模式**：
1. **Generate Mode**（默认）：主题/文字 → 视觉隐喻 → prompt → 生成图像 → 质检
2. **Photo Input Mode**：用户照片影响输出 → 分类角色 → 定保留级别 → 实图传入生成 → 双重质检
3. **Reference Analysis Mode**：分析参考图风格 → 提取固定系统/可变系统/样本残留三类规则
4. **Prompt-only Mode**：仅当用户明确只要 prompt 不要图像时使用
5. **Analyze + Generate**：先分析参考提取系统，再用新配方生成不抄构图

**照片角色分类**：
| 角色 | 判断依据 |
|------|----------|
| 编辑目标 | "把这张照片做成海报"/"基于这张图改"/给了图只说"做一张" |
| 参考图 | "参考这张图的风格/配色/构图" |
| 辅助插入 | "把照片里的这个人/物体放进去" |

**prompt 编译规则（字段序）**：画布→注意力几何（负空间%/簇位置尺寸）→照片契约（角色+不变量+允许变化）→视觉隐喻→焦点载体形式→材质处理→排版→精确主色相及占比→复刻氛围→hard avoids；输出为四段式紧凑 prompt，禁用 somewhere/minimal/artistic 等不可渲染形容词。

## A1 (Past Application) — 源项目的典型应用

### 案例: 同主题系列海报的变奏生产
- **输入**: "雨天"主题 + 要求三张不同布局。
- **做法**: 从 variation-engine 选三套配方（布局族/焦点类型/排布分布/纸色调/强调色各不同），按四段式分别编译 prompt，逐张过质检门。
- **结果**: 三张海报同属一个视觉家族（纸质+大负空间+单强调色）但构图语法互异——变奏改变的是视觉语法而非仅挪动位置；避免连续默认"居中小照片+蓝点+微字"套路。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 主题转海报："用'孤独的城市'这个主题做一张 Zine 海报"——无照片输入，纯内容驱动。
2. 参考风格提炼："分析这个文件夹里的参考图，总结出一套能复用的视觉系统。"
3. 照片参与创作："用这张人物照做海报，保留人像只改排版与纸张质感"——进入 Photo Input Mode。

### 语言信号
- "做一张海报 / zine / 纸质质感"
- "视觉隐喻 / 把这篇文章浓缩成一个画面"
- "分析这组图的风格 / 提炼视觉系统"
- "只给我生图 prompt"

### 与同 agent 兄弟 skill 的区分（互设诱饵）
- 与 photo-relic-editorial：本 skill 可**无照片纯主题**起稿；对方必须以真实照片为源且签名是"上真照片下遗存墨迹"。有主题没照片来这里。
- 与 gathered-scenes-zine：对方是实景照片锚定+插画场域+手撕纸边的拼贴；本 skill 的画面是一个小焦点事件而非"场域"。要撕纸拼贴质感去那里。
- 与 photo-abstract-editorial：对方从照片重建空间关系抽象面板；本 skill 从**语义主题**造隐喻，不依赖照片空间事实。

## E (Execution) — 可执行步骤

1. **解析输入** — 提取核心主体、情感温度、 supplied 文本与每张图片的角色；文章类输入压缩为一个可成像的中心关系而非全文插图。完成标准: 一句话写出"中心视觉隐喻+情绪温度"。
2. **选路由模式** — 按 I 段五模式选最小满足的模式；意图模糊但明确要"做一张"时直接走 Generate Mode 不追问。完成标准: 模式名+理由记录在案。
3. **选变化配方** — 从 variation-engine 定布局族/焦点元素/排版模式/纹理/纸调/强调色/装饰记号系统；批量出图时相邻两张至少换布局族与排版分布。完成标准: 配方七轴各有明确取值。
4. **编译 prompt** — 按字段序写四段式，点名焦点载体的具体名词与颜色载体，附相关 hard avoids；照片模式补"须保持可辨认/允许变化/新增元素"三段契约。完成标准: prompt 中无抽象速记词，占比与位置均为具体数值。
5. **生成并质检** — 全图与缩略图两档检查：负空间 70-90%、单一视觉事件、主色 thumbnail 可见、无商业广告/全出血/多色模板漂移；照片模式另核保留不变量。完成标准: 质检清单逐项通过或触发一次定向重生成。
6. **交付** — 返回图像+最终 prompt+配方+一句解读；照片模式加注角色与保留级别；二次仍失败则如实声明局限。完成标准: 输出格式符合上游 Output Formats 约定。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- 数据可视化、图表、信息图 → 走数据可视化 agent 的 skill。
- UI 设计、商业广告头图、品牌 campaign 物料 → 本 skill 明确规避广告层级与 CTA。
- 无任何源的凭空写实摄影 → 不虚构"真实拍摄"的照片。

### 已知局限 / 失效模式（≥1条）
- 图像模型对长文本必然变形：可读文字须短；参考图样本量小时只能给单图观察不能冒充系列规律；模型可能漂移成全场景插画或多色模板，需靠质检门拦截后定向重生成一次。

### 内容边界
- 参考图仅学视觉语法：不得复制源文字、品牌、水印、签名、精确日期地点或原构图；用户自有照片按保留级别契约处理，High 级优先原图裁切拼贴而非重绘。

## 相关 skills
- contrasts-with: photo-relic-editorial（主题驱动 vs 照片遗存）、gathered-scenes-zine(焦点事件 vs 场域拼贴)、photo-abstract-editorial（语义隐喻 vs 空间关系重建）

---

## 审计信息
- **验证**: V1 ✓（本地 upstream 已核） / V2 ✓（RIA++ 六段齐备） / V3 ✓（darwin 用例 7 条推演全过）
- **蒸馏时间**: 2026-08-25；**来源**: upstream `D:\outcome\self\vendor/LiamGvchi__gc-minimal-zine-poster`（SKILL.md + references/prompt-compiler.md + quality-gate.md），在既有 43 行半成品上扩写，保留五模式/角色表/保留级别等原有正确内容
