---
name: motion-design-prompt-generator
description: "把一句话想法、产品、品牌或脚本，转成可直接投喂给 AI 视频/动效工具的专业提示词：分镜节拍、运动语言、缓动与时长、镜头与风格规格，并输出平台变体（Sora / Veo / Kling / 即梦 Seedance / Runway）或代码动效规格（Remotion / HyperFrames / GSAP / Lottie）。当用户要「动效提示词」「motion design prompt」「AI 视频提示词」「分镜提示词」「logo 演绎 / UI 动效 / 产品宣传片脚本」，或要把 brief 变成可生成的 prompt 时使用。"
whenToUse: "用户给出模糊创意、产品或脚本，想要能直接生成视频/动效的提示词、分镜或动效规格时。"
---

# 动效提示词生成器（Motion Design Prompt Generator）

把「我想要一个高级感的开场」这种话，变成一条**可执行、可复现、可交付**的动效提示词。

核心主张：**提示词不是形容词的堆叠，而是一份运动规格书。** 每一句都要能被拍摄、被渲染、被验收。

---

## 一、这个技能产出什么

按需要组合，默认给 ①+②：

| # | 交付物 | 形态 | 用途 |
|---|---|---|---|
| ① | **主提示词（Master Prompt）** | 一段 80–160 词的生成式提示词 | 直接粘贴进 Sora / Veo / Kling / 即梦 |
| ② | **分镜节拍表（Beat Sheet）** | Markdown 表格：时间码 / 画面 / 运动 / 转场 / 声音 | 人工拍摄、剪辑对齐、团队沟通 |
| ③ | **平台变体包** | 每个平台一条改写版 | 同一创意跨模型复用 |
| ④ | **代码动效规格** | JSON / TS 参数：fps、时长、缓动、spring | Remotion、HyperFrames、GSAP、Lottie |
| ⑤ | **负向与约束清单** | 负面提示词 + 一致性锚点 | 降低废片率 |

---

## 二、工作流（严格按序，别跳步）

### Step 0 · 先判断输出目标（1 秒决策）

- **视频模型**（要"拍出来"的片子）→ 走 Step 1–4，用 `references/platform-presets.md`
- **代码动效**（网页 / App / 组件）→ 走 Step 1–3，用 `references/motion-grammar.md` 的时长与缓动表
- **设计提案**（还没定方向）→ 先给 3 条创意路线，再展开用户选中的那条

### Step 1 · 取材（能推断就推断，最多问 3 个问题）

必须凑齐这 6 格，缺的用合理默认值填，**不要空着**：

1. **主体**：产品 / 角色 / 文字 / 抽象图形？有没有必须保持一致的锚点（logo 形状、包装色、人脸）？
2. **动作**：它要"发生"什么？一个动词就够（展开、聚合、崩解、穿越、生长）。
3. **场景**：纯色棚拍 / 实景 / 3D 空间 / 界面录屏风格？
4. **时长与画幅**：默认 15s、16:9；竖版短视频用 9:16、8s。
5. **情绪与参照**：三个形容词 + 一个可对标的片子（"像 Apple 的产品页开场"）。
6. **投放位置**：社媒信息流 / 官网首屏 / 展会大屏 / 应用内动效——决定节奏和信息密度。

用户只给一句话时，直接给方案，把假设写在开头一行：`假设：15s / 16:9 / 无真人 / 冷色调`。

### Step 2 · 定创意方向（只在提案场景做）

给三条并列路线，各一句话 + 一句风险：

- **A 稳妥**：品类惯例，转化率高，但辨识度低
- **B 风格化**：强视觉母题（材质 / 字体 / 色彩），记忆点强，制作要求高
- **C 大胆**：非常规镜头或结构，传播潜力大，可能偏离品牌

### Step 3 · 建运动叙事（Beat Sheet）

短视频动效的通用骨架（15s）：

| 时间 | 功能 | 运动任务 |
|---|---|---|
| 0.0–1.5s | Hook | 一个反直觉的运动（急推、断裂、坠落），0.3s 内给出视觉钩子 |
| 1.5–4s | 建立 | 主体入场，镜头稳定，交代空间 |
| 4–9s | 展开 | 主运动 2–3 次递进，每次幅度递减但精度递增 |
| 9–12s | 转折 | 一次节奏变化（急停 / 反向 / 材质切换） |
| 12–15s | 收束 | 落版：logo / 产品 / CTA，留 0.5s 静止余韵 |

规则：**每 2 秒必须有一个运动事件**；静止超过 1s 只允许出现在结尾。

### Step 4 · 写提示词（9 槽位法）

按顺序写，一句一槽，不要合并：

1. **主体**：`a matte-black aluminum cube, 12cm, sharp bevels`
2. **动作**：`splits into 8 panels that unfold like petals`
3. **镜头**：`macro lens, 100mm, slow dolly-in from 40cm to 15cm`
4. **运动弧线**：`starts fast, decelerates hard in the last 20%`
5. **时间与节奏**：`5 seconds, 24fps, one continuous take, no cuts`
6. **光线与材质**：`single soft key from top-left, cool rim light, brushed metal micro-texture`
7. **风格与质感**：`product-film realism, shallow depth of field, subtle grain`
8. **约束与负向**：`no text, no people, no logo distortion; keep proportions identical to reference`
9. **声音**（仅 Veo / 有声平台）：`low mechanical hum, single soft click on lock-in`

**硬性门槛（缺一条就不算完成）**：时长 + 画幅 + 镜头 + 一个物理细节（材质/惯性/接触阴影）+ 一条负向约束。

### Step 5 · 交付与自检

交付前逐条过 `## 五、质量门槛`。默认输出为一张 **Prompt Card**（模板见 `assets/prompt-card.md`），需要管线时再附 JSON 规格（`assets/spec.schema.json`）。

---

## 三、运动语言速查

### 缓动（决定"贵不贵"）

| 意图 | 曲线 | 参数 |
|---|---|---|
| 入场（轻盈） | ease-out | `cubic-bezier(0.16, 1, 0.3, 1)` |
| 退场（干脆） | ease-in | `cubic-bezier(0.7, 0, 0.84, 0)` |
| 位移（通用） | ease-in-out | `cubic-bezier(0.65, 0, 0.35, 1)` |
| 物理感 / 弹性 | spring | `stiffness 180–260, damping 18–26, mass 1` |
| 强调（回弹） | back-out | `cubic-bezier(0.34, 1.56, 0.64, 1)` |

**永远不要写 `smooth`、`nice easing`、`fluid motion`——写曲线或写"先快后慢，末段 20% 急停"。**

### 时长基线（UI / 代码动效）

| 元素 | 时长 |
|---|---|
| 微反馈（按钮、开关） | 120–180ms |
| 元素进出场 | 200–320ms |
| 面板 / 页面转场 | 300–450ms |
| 品牌级演绎 | 800–2000ms |

大于 500ms 的 UI 动效必须可被 `prefers-reduced-motion` 关闭。

### 镜头词汇（中英对照，写提示词时用英文更稳）

| 效果 | 英文写法 |
|---|---|
| 推近 / 拉远 | dolly in / dolly out, push in |
| 环绕 | orbit / arc shot around subject |
| 跟随 | tracking shot, follow cam |
| 手持感 | handheld, subtle shake |
| 微距 | macro, extreme close-up |
| 俯拍 / 仰拍 | top-down / low angle |
| 变焦 | zoom (optical) vs. dolly (physical)——**别混用** |
| 移轴 / 景深 | tilt-shift, shallow DOF, f/1.8 |

### 转场词汇

match cut（形状/动作匹配）· whip pan（甩镜）· mask reveal（遮罩揭示）· morph（形变）· light leak（漏光）· hard cut on beat（卡点硬切）· object wipe（物体擦除转场）

---

## 四、平台适配（写之前先看）

| 平台 | 语言 | 结构偏好 | 关键约束 |
|---|---|---|---|
| **Sora 2** | 英文 | 一段连贯叙述，镜头优先 | 写清物理与时间；避免分镜清单式罗列 |
| **Veo 3** | 英文 | 画面 + 对白/音效分行 | 支持原生音频，声音要单独写 |
| **Kling 2.x** | 中文更稳 | 主体 → 动作 → 运镜 → 风格 | 动作幅度写小一点，避免多人交互 |
| **即梦 / Seedance** | 中文 | 首帧描述 + 运镜 + 风格词 | 强烈依赖首帧图，先定构图 |
| **Runway Gen-4** | 英文 | 短句，参考图驱动 | 提示词越短越听话，细节交给参考图 |
| **Remotion / HyperFrames** | 代码 | 帧级参数 | 给 fps、durationInFrames、spring 配置，不给形容词 |

详细骨架、示例与常见翻车点见 `references/platform-presets.md`。

---

## 五、质量门槛（交付前逐条打勾）

- [ ] 有明确时长与画幅
- [ ] 有镜头语言（焦段 / 机位 / 运动方式至少一项）
- [ ] 有一个**物理细节**（惯性、接触阴影、材质微纹理、液体黏度）
- [ ] 有负向约束（不出现什么）
- [ ] 主体一致性锚点写死在提示词里（颜色 / 形状 / 比例）
- [ ] 没有空洞形容词（见下方禁用清单）
- [ ] 节奏上每 2 秒一个运动事件
- [ ] 若是 UI 动效：时长在基线内，且可降级

**禁用词清单**（出现即改写）：stunning, beautiful, amazing, cinematic（除非说明是哪种电影感）, high quality, 4K（除非平台参数位）, smooth, dynamic, modern, futuristic, epic, ultra-detailed。

替换法：把形容词换成**可观测事实**——不写 "cinematic lighting"，写 "single hard key from camera-left, 45°, deep falloff, no fill"。

---

## 六、两个最小示例

**A. 产品开场（Sora / Veo）**

> A matte-black aluminum cube, 12 cm, sharp bevels, sits on a seamless graphite surface. It splits along invisible seams into eight panels that unfold like petals, each panel rotating 45° with slight mechanical overshoot before locking. Macro lens, 100 mm, slow dolly-in from 40 cm to 15 cm over 5 seconds, 24 fps, one continuous take. Single soft key from top-left, cool rim light, brushed-metal micro-texture, shallow depth of field, subtle grain. No text, no people, no reflection artifacts; proportions must stay identical to the reference. Sound: low mechanical hum, one soft click at lock-in.

**B. UI 微交互（代码规格）**

```json
{
  "target": "bottom-sheet",
  "durationMs": 320,
  "easing": "cubic-bezier(0.16, 1, 0.3, 1)",
  "from": { "translateY": "100%", "opacity": 0.6 },
  "to": { "translateY": "0%", "opacity": 1 },
  "scrim": { "opacity": [0, 0.4], "durationMs": 240 },
  "reducedMotion": "fade-only, 120ms"
}
```

---

## 七、参考文件

- `references/motion-grammar.md` — 缓动/时长/镜头/转场完整词表与数值
- `references/platform-presets.md` — 六个平台的提示词骨架、示例、翻车点
- `references/examples.md` — 4 个完整案例（产品片 / logo 演绎 /  kinetic type / 数据可视化）
- `assets/prompt-card.md` — 默认交付模板
- `assets/spec.schema.json` — 代码动效 JSON 规格 schema

## 八、反模式

1. **形容词驱动**：整段没有可执行参数。
2. **镜头漂移**：一条提示词里同时推、拉、环绕——模型会乱。
3. **无锚点复用**：同一角色/产品在多条提示词里描述不一致，成片对不上。
4. **忽略时长**：写 10 个动作却只给 3 秒。
5. **只给正向**：不写负向约束，废片率翻倍。
6. **中文直译英文术语**：`运镜如丝般顺滑` 这类描述对模型无信息量。
