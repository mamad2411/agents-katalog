---
name: unity-shader-graph-cn
description: Use this skill when the user asks in Chinese how to build, connect, tune, or troubleshoot Unity Shader Graph effects such as Cel Shading, outline, Fresnel, dissolve, hit flash, UV flow, or character stylized shaders. It asks for Unity version and render pipeline first, then answers in a fixed Chinese structure with English variable names, Graph Settings and Node Settings guidance, node-by-node connections, formula-style summaries, scenario-specific extensions, concise usage instructions, and precise follow-up questions when the desired effect is still unclear.
---

# Unity Shader Graph CN

使用这个 skill 时，目标是给出“能直接照着搭”的中文说明，而不是泛泛原理课。默认面向 Unity Shader Graph；变量名、属性名、公式中的变量统一使用英文。

## 先确认环境

优先确认以下信息：

```text
先确认一下你的环境：
1. Unity 版本是多少？
2. 使用的是 URP、HDRP 还是 Built-in？
3. 这个效果是用在角色、场景物件，还是特定 VFX 上？
```

- 若信息不完整，不要卡住。
- 默认假设写法：`以下说明按 Unity 2022.3 + URP + 3D 角色 Shader Graph 为前提；如果你的版本或管线不同，我会按实际情况调整节点方案。`
- 要区分“能做”和“建议做”。例如：Cel Shading 可以直接在 Shader Graph 中实现；稳定角色描边通常更建议第二材质或屏幕空间方案。

## 固定输出结构

始终按下面顺序输出，除非用户明确要求省略某一部分。

### 1. 实现可行性与步骤概览

- 先说明该效果在当前 Unity 版本和管线下是否可行。
- 再用 3 到 6 句说明大致实现路径。
- 若某部分不适合纯 Shader Graph 完成，要明确指出替代方案。

### 2. Graph Settings 与属性说明

先写 Graph Settings，再写属性表。

Graph Settings 需要根据当前效果说明这些内容：
- `Material`
- `Surface`
- `Blend`
- `Two Sided`
- `Alpha Clipping`
- `Receive Shadows`
- `Cast Shadows`
- `Fragment Normal Space`
- 如有差异，再补充 `Support VFX Graph`、`Precision` 或目标管线特有项

写法要求：
- 说明推荐值
- 说明该设置的含义
- 说明为什么要这么设
- 说明设错后可能出现的现象

属性说明必须使用表格，列至少包括：
- `属性名`
- `类型`
- `含义`
- `作用`
- `调大/调小的影响`

如果某个属性只适用于特定方案，要注明范围，例如：`仅用于 Fresnel Outline`、`仅用于 Ramp Texture`。

### 3. 节点连接顺序

这一部分必须机械、可照抄。逐节点列出：
- 节点名
- 关键 Node Settings
- 输入参数
- 输出参数

写法示例：

```text
节点 1：Normal Vector
- Space：World
- 输出：`normalWS`

节点 2：Main Light Direction
- 输出：`lightDirWS`

节点 3：Dot Product
- 输入 A：`normalWS`
- 输入 B：`lightDirWS`
- 输出：`NdotL`
```

规则：
- 特殊 Node Settings 必须写清楚，例如 `Normal Vector.Space = World`、`Sample Texture 2D.Type = Default`、`Position.Space = Object`
- 如果用户问“连给谁”，最后要明确写最终输出，例如：`finalColor -> Base Color`
- 需要说明每个中间结果的用途，不要只列节点名

### 4. 类公式表述

把整条流程整理成便于检查的伪公式，保持英文变量名。例如：

```text
NdotL = dot(normalWS, lightDirWS)
light = saturate(NdotL)
mask = step(Threshold, light)
shadowed = albedo * ShadowTint
finalColor = lerp(shadowed, albedo, mask)
```

如果存在多个方案，分别给公式，不要混写。

### 5. 不同应用场景的额外建议

按“适用场景 + 建议操作 + 原因”的格式输出。优先覆盖：
- 基础节点流程
- 两段式 Cel Shading
- 三段式 Cel Shading
- Ramp Texture
- Fresnel 假描边
- Inverted Hull 真描边
- 贴图与 Toon 明暗结合
- 背光面过黑修正
- 角色主材质与测试球的不同调法

如果方案超出纯 Shader Graph 范围，要明确指出需要第二材质、Renderer Feature、后处理或代码支持。

### 6. 简明使用说明

使用中文简体，控制在 4 到 6 条内，偏施工说明，例如：
- 先确认 Render Pipeline
- 先在测试球上验证 `light` 和 `mask`
- 再接贴图和额外效果
- 先调 `Threshold`，再调 `ShadowTint`

### 7. 原理说明按需追加

默认不主动展开原理。结尾固定询问一次，例如：

```text
如果你需要，我可以继续说明这套效果背后的原理，例如 `dot(normalWS, lightDirWS)`、`Step` 和 `Smoothstep` 的区别，或者为什么背光面容易发黑。
如果你现在只想先把效果做出来，这一部分可以先跳过。
```

若用户不需要，不继续输出原理。

## 回答风格要求

- 全程使用中文说明。
- 变量、属性、公式变量统一使用英文。
- 使用说明必须是中文简体。
- 回答先给可执行步骤，再给补充解释。
- 不要只说“可以这样做”，要说清楚“接到谁、设成什么、为什么”。

## 质量要求

### Graph Settings

凡是会影响结果的 Graph Settings，都要明确说明。尤其是：
- `Surface = Opaque` 还是 `Transparent`
- `Two Sided` 是否开启
- `Alpha Clipping` 是否启用
- `Receive Shadows` 和 `Cast Shadows` 是否影响视觉目标

### Node Settings

凡是节点存在关键配置项，都要明确写出来。尤其是：
- 向量或法线节点的 `Space`
- 纹理采样节点的类型和输入
- 顶点阶段与片元阶段的区别
- 需要 `Step` 还是 `Smoothstep`
- 需要 `One Minus`、`Negate`、`Normalize` 时为什么要加

如果某个节点在不同 Unity 版本中名字不同，要在回答中指出。

## 效果不达预期时的追问规则

当用户说“怪”“不对”“不像”“效果不够好”时，不要只问“你想调成什么样”。改为用专业词汇引导，并附上中文解释。优先用下面这些方向：

1. `Threshold`
含义：亮部和暗部切换的位置。

2. `Softness`
含义：亮暗边界是硬切还是柔和过渡。

3. `Shadow Tint`
含义：暗部颜色倾向，是否过黑、过灰或色偏不对。

4. `Contrast`
含义：亮暗反差是否过强或过弱。

5. `Banding Count`
含义：你想要两段式、三段式，还是更多层次的明暗分层。

6. `Backface Darkness`
含义：背光面是否太黑、细节是否丢失。

7. `Rim Light / Fresnel`
含义：边缘发亮区域是否过宽、过亮或不够明显。

8. `Outline Width`
含义：描边宽度是否稳定，是否过粗、过细、忽粗忽细。

9. `Ramp Control`
含义：是否希望通过渐变贴图而不是固定阈值来精细控制明暗层次。

追问格式建议：

```text
为了避免调整方向过于模糊，我先确认一下你想优化的是哪一类问题：
- `Threshold`：明暗分界位置
- `Softness`：边界软硬
- `Shadow Tint`：暗部颜色倾向
- `Backface Darkness`：背光面过黑
- `Outline Width`：描边粗细稳定性
```

若用户给出的方向仍然模糊，继续补一句中文解释，再给出对应可调属性和节点。

## 方案建议规则

- 测试基础明暗时，优先建议从无贴图测试球开始。
- 角色有贴图时，优先建议 `finalColor = lerp(albedo * ShadowTint, albedo, mask)` 一类的组合方式。
- 如果背光面死黑，优先建议 `Half-Lambert`、抬高暗部、增加环境补光，不要先建议乱改贴图。
- 如果用户追求稳定描边，优先说明 `Inverted Hull` 或屏幕空间方案；不要把 `Fresnel` 说成真正外轮廓描边。
- 如果用户只想先出结果，优先给最短可运行方案。
