---
name: anima-prompt-naturalang
description: 把中文场景描述转成 Anima/Anima Base 的英文自然语言 prompt：7 槽位、P/N 规则、负面三层、互斥自检；正负面分开输出直接复制，不输出 Params；禁止自行添加画风词/LoRA 触发词（用户没给就不写）
---

# Anima 自然语言提示词工程（生产级）

把用户的中文画面需求转成**英文自然语言 prompt**：正向 1~3 句 + 负面 5~12 项，正负面各放一个独立代码块（块内纯文本可直接复制），**不输出 Params**（参数按 §参数默认执行）。适用 Anima / Anima Base（LLM 文本编码器，"读句子"而非标签堆）。

核心哲学：写句子不写标签，写语义不写保险，写约束不写愿望。

## 画风词禁令（最易犯错，先读这条）

**禁止自行添加任何画风词、LoRA 触发词、画师名、作品名**——用户明确给出时才写，并置于正向最前；用户没给就**直接从 S2 主体开始写**。任何示例中的触发词只是格式示意，不得模仿。

## 正向：7 槽位 + P 规则

- S1 [风格/触发] 仅当用户明确给出触发词/画风要求时才写，否则跳过
- S2 [主体] 谁/什么，数量
- S3 [外观与着装] 发/眼/表情+服装/配饰，写成关系句
- S4 [姿势与动作] 含方向、朝向、接触关系
- S5 [场景与光影] 环境、时间、光源方向、色调、情绪
- S6 [构图与镜头] 景别、角度、焦点
- S7 [质量补充] 可选 ≤2 项（detailed background, clean lineart）

P 规则：
- P-1 重要在前：主体永远在最前（注意力前偏置）
- P-2 关系成句：属性挂到主体上（a girl with silver hair wearing a white dress），禁散装罗列
- P-3 一句一义：一个短句一个语义单元，不嵌套歧义从句
- P-4 总量：1~3 句或 10~25 个元素，>40 视为稀释
- P-5 禁同义堆砌：beautiful/gorgeous/stunning 只留一个
- P-6 禁矛盾：indoor+outdoor、standing+sitting 出现即事故
- P-7 质量咒语清零：masterpiece/best quality/8k/hdr/highres/ultra detailed/perfect face 一律不写（LLM 编码器上无效甚至干扰）
- P-8 想要就写正面：不用负面塑造画面（粉象效应）
- P-9 空间显式：方向 left/right，朝向 facing the viewer / turned away，接触 holding / resting on
- P-10 名词动词优先，形容词节制
- P-11 不依赖权重语法：(tag:1.2)、((tag)) 无效，用词序和句式强调

## 负面：三层 + N 规则

- 必需层（永远写）：`worst quality, low quality, blurry, jpeg artifacts`
- 按需层（人物图加）：`bad anatomy, bad hands, extra fingers, missing fingers`
- 可选层（风格防护，按需加）：`text, watermark, signature, 3d, realistic, photo`

N 规则：总量 5~12、硬上限 15；worst/low/poor quality 同义，最多留两个；负面只排除常见缺陷不排除"内容"（不想要伞→正面写 clear sky）；禁恐惧词（ugly、nsfw 写进负面可能反向激活）；负面不背锅，构图/内容问题回正面改。

## 参数默认（不随输出打印）

CFG 4（范围 3~5）| Steps 30（28~35）| 采样器 DPM++ 2M Karras（特写/质感场景换 ER_SDE Karras；找灵感用 Euler a）| 总像素 ≈1024²，避免极端长宽比 | 迭代期固定 seed

## LoRA 协同（仅用户用到 LoRA 时）

- 触发词仅在用户给出时写、置于正向最前；推理 prompt 格式必须对齐该 LoRA 的训练 caption 格式（tag 训练→tag/混合推理，句子训练→自然语言）
- 权重 0.8 起试：烧图/伪影降 0.6~0.7，风格不足升 1.0；多 LoRA 同时 ≤2 个

## 场景要点（易错三类）

- **双人互动**：先写空间锚点（A on the left, B on the right），再分别写各自动作，最后写互动关系（A holding B's hand）；禁止只写 two girls 后堆动作
- **场景主导（人物小）**：场景句紧跟主体优先描述，人物用 a small figure of ... 降级，否则人物会被画大
- **NSFW**：解剖/姿势用直白标准英文词（LLM 对俚语映射不稳）；姿势/构图/景别显式写明；负面只留质量层；随机性大，固定 prompt 扫 seed（4~8 个）挑图，而非改词

## Q 系列（互斥与输出协议）

- **Q-1 互斥**：facing the viewer↔turned away、from front↔from behind、from above↔from below、close-up↔full body；standing/sitting/lying/running 同一主体同一时刻只能其一；closed eyes↔looking at the viewer；barefoot↔wearing shoes；同部位状态只写一个（toes curled↔toes spread），足/手细节 ≤2 项；物理兼容（underwater 不配 smoking）
- **Q-2 视线默认**：单人除非明确要求背影/侧脸/from behind，必须写 looking at the viewer / direct eye contact；多人按互动写
- **Q-3 不重复**：同一元素全 prompt 只出现一次，强调靠前移句序
- **Q-5 输出协议**：正、负各一个独立代码块，块内纯文本无前缀；不输出 Params；不寒暄、无多余解释

## 自检清单（输出前过一遍）

- □ 没有自行添加画风词/触发词/画师名？
- □ 总量 ≤3 句 / ≤25 元素？无同义堆砌、无矛盾项？
- □ 无质量咒语？
- □ 姿势/空间写了方向和朝向？单人视线默认已注入？
- □ 想要的都在正面；负面 5~12 项、无同义词、无内容排除？
- □ 正负面各一个代码块，可直接复制？

## 词库（按需取用）

光影：soft diffused light / rim light / backlight / golden hour / window light from the left / warm tone · 镜头：close-up / bust shot / full body / from below / shallow depth of field · 质感：detailed skin texture / clean lineart / detailed eyes / detailed background

## 输出示例

用户："一个银发红瞳的女孩，穿白色吊带裙，手里拿着小花束，坐在窗边，午后阳光从左边照进来，半身像，温柔微笑看向镜头，清新治愈的氛围"

```
A silver-haired girl with red eyes and a gentle smile, looking at the viewer. Wearing a white sundress with thin straps, holding a small bouquet of flowers. Sitting by the window, soft afternoon light from the left, warm and cozy atmosphere. Bust shot, shallow depth of field. Clean lineart, detailed eyes.
```

```
worst quality, low quality, blurry, bad anatomy, bad hands, text, watermark
```

（检查：无自加画风词 ✓ 关系句 ✓ 视线默认注入 ✓ 光影在 S5 ✓ 无质量咒语 ✓ 负面 7 项含必需层 ✓ 无 Params ✓）
