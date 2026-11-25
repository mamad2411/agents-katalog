---
name: hbg-rubber-stamp-field-note
description: "Transform each supplied travel photo into its own 4:3 editorial comparison poster: a high-fidelity photograph on the left and a small hand-carved, distressed, spot-color rubber-stamp interpretation of the same scene on warm archival paper at right. Use for 橡皮章旅行记录、旅行观察笔记、照片与章印对照、建筑地标章印、山岸船车人物的手工套色版画; do not use for passport stamps, circular seals, souvenir logos, pure vector icons, or multi-photo collages."
---

# HBG Rubber Stamp Field Note

把旅行照片保留为现场证据，再把同一场景压缩成一枚小而克制的手工印记。这里的 `field note` 指旅行观察记录，不限定田园题材。

## 默认交付

- 一张输入照片对应一张独立成品；多张照片逐张生成，禁止拼贴。
- 默认采用 4:3 横版，左侧约 58% 为高保真原照片，右侧约 42% 为旧纸与小型多色章印。
- 整张作品在一次图像生成或编辑中完成，不用代码硬拼。
- 左右必须来自同一张照片，主体身份、数量、姿态、结构、方向和空间关系可追溯。
- 图片任务只有在聊天中出现可见图片、且给出保存路径后才算完成。

## 请求模式

### Generate

用户提供照片并要求生成时：读取 [references/style-system.md](references/style-system.md) 与 [references/quality-gate.md](references/quality-gate.md)，分析照片后使用内置图像生成工具逐张完成。

### Prompt-only

用户只要提示词时：返回 [references/prompt.zh-CN.md](references/prompt.zh-CN.md) 的完整提示词。可以把已经确认的地点、标题和关键词替换进去，但不要删去版式、保真、制版与避错约束。

### Analyze

用户只要分析时：说明照片中应保留的主体、最适合雕刻的轮廓、建议的 2–4 种照片取样专色、标题候选和潜在失败点；不要擅自生成图片。

## 工作流

1. 识别照片事实：主体、数量、姿态、建筑或地形结构、观察角度、空间方向、主色和可删除噪声。
2. 判断最值得刻下的 1–3 个视觉锚点。复杂场景不逐物复制，只保留能够认出原场景的线面关系。
3. 从照片提取 2–4 种专色：一组深色结构墨、一种主体特征色、可选的一种环境色与极小强调色。
4. 若地点可靠，提炼 1–3 个英文单词标题；地点不可靠时用场景主题，禁止编造地名、年份、坐标或品牌。
5. 将照片摘要与 [references/prompt.zh-CN.md](references/prompt.zh-CN.md) 合并，逐张调用图像生成工具。
6. 按 [references/quality-gate.md](references/quality-gate.md) 检查。只修正明确失败点，不在迭代中更换主体或媒介逻辑。
7. 将成品保存到工作区，并把每张图片作为可见图片显示在聊天中。

## 不可破坏的规则

- 左侧必须具有实质面积，仍然像原始照片，只允许轻微出版物调色。
- 右侧必须是真正重新雕刻和套印的图形，不是在照片上叠颗粒或盖章滤镜。
- 章印位于右侧中下部或下部，只占右侧高度约 28%–38%；大面积纸白是风格核心。
- 章印使用 2–4 种从照片提取的低至中饱和专色，具有缺墨、断边、针孔、颗粒和轻微 1–2 mm 套印错位。
- 左右之间使用干净、笔直、清晰的垂直边界，不加相框、卡片阴影、撕纸或装饰分隔条。
- 文字必须少、小、准确。不能确认地点时，不得生成具体地名。
- 禁止圆形印章、红色姓名章、蜡封、护照章、邮票齿孔、纪念品 Logo、光滑 SVG、水彩晕染、塑料 3D 和巨大满版章印。

## 视觉参考

只有在需要校准版式密度与印刷质感时，查看 `assets/examples/`。案例是媒介参考，不是内容模板；不得把意大利地标、标题或色盘复制到其他照片。

