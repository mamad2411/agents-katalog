---
name: aionforge-product
description: >
  阶段 2 T 恤实拍撞色适配与商品图合成：按「思考 → 事实锁定 → 生成 → 检查」四步闭环，
  检测印花与各颜色 T 恤实拍底图的颜色冲突，按成衣底色调整适配印花颜色，并将正面印花（或左胸核心小标）
  与背面主印花分别合成到对应 T 恤实拍图上，输出 bg_white 商品图。
  用户说把图案合成到 T 恤实拍图上、印花和衣服颜色冲突调整、撞色适配、出白底/实拍商品图、背面商品图时使用。
  Use when the user runs /aionforge-product.
---

# 阶段 2：T 恤实拍撞色适配与商品图合成（product）

本流程承接 `aionforge-print` 的透明印花与位置计划，针对**每一件具体颜色的 T 恤实拍图**检测颜色冲突、执行印花颜色调整适配，并将正面印花（或左胸小印花）与背面大印花合成到 T 恤实拍图上，产出作为后续全局唯一衣服真相源的 `bg_white` 商品图。

未加载入口时先读 `../aionforge/SKILL.md`。工具只按名称引用，参数见工具卡；本文件不写命令。

## 输入与输出

| 方向 | 内容 | 说明 |
| --- | --- | --- |
| **输入** | `facts.print.placements`、透明主印花与左胸小标、各颜色正面 T 恤实拍（`garment`）、各颜色背面 T 恤实拍（`garment_back`，有背面印花时必填） | 缺少 `placements` 先回 `aionforge-print` |
| **输出文件** | 适配印花 `refs/<product>-<color>-print-fit.png`、正面商品图 `bg_white/<product>-<color>.png`、背面商品图 `bg_white/<product>-<color>-back.png` | 保留原实拍底图质感与背景 |
| **输出事实** | `colors[].color_adaptation`、`colors[].bg_white`、`colors[].bg_white_back`、`canonical.garment`、`canonical.garment_back` | 见 [contracts/facts.md](../aionforge/references/contracts/facts.md) |

---

## 四步闭环执行流程

### 第一步：思考（Think —— 实拍底图清点与逐色撞色冲突分析）

1. **正反面实拍底图清点**：
   - 检查 `colors[]` 中每个颜色的正面 T 恤实拍（`source`）和背面 T 恤实拍（`source_back`）。
   - **硬拦截**：若 `placements` 含背面主印花，但某个颜色缺少背面 T 恤实拍图，**立即停下请用户补充背面实拍**，严禁拿正面实拍图镜像、拉伸或让模型凭空捏造背面。
2. **逐色撞色冲突诊断**（规则详见 [print/ink.md](../aionforge/references/print/ink.md)）：
   - 同一印花在不同颜色 T 恤上表现不同（如深色印花在白 T 恤上清晰，在黑/藏青 T 恤上会撞色隐形）。
   - 针对每个颜色的 T 恤底色，评估主印花与左胸小标的 WCAG 对比度（图形要求 `≥ 3:1`，小字/细线要求 `≥ 4.5:1`）：
     - **浅色 T 恤 + 深色/彩色印花（对比度达标）**：无需改色，合成墨色用 `multiply`（正片叠底融入布料纹理）。
     - **浅色 T 恤 + 白色/浅黄印花（对比度 `< 3:1`）**：存在浅底浅印冲突，适配策略选 `darken`（压暗明度）或 `outline`（加深色细描边），合成墨色用 `normal`。
     - **深色 T 恤 + 中性深色/黑色笔画（对比度 `< 3:1`）**：存在深底深印冲突，适配策略选 `white`（深色笔画精准转白），合成墨色用 `white`。
     - **深色 T 恤 + 多彩暗调印花（对比度 `< 3:1`）**：适配策略选 `lighten`（提亮明度、保留原色相与彩度），合成墨色用 `normal` 或 `white`。

### 第二步：事实锁定（Lock —— 锁定各颜色适配方案与合成映射）

1. 将每个颜色 T 恤的撞色诊断结果、拟采用的适配策略（`strategy`）和合成墨色（`ink`）写入 `facts.json` 的 `colors[].color_adaptation` 及 `placements[].adaptations`。
2. 若存在颜色冲突需要调整印花颜色，把**「某颜色 T 恤 → 原对比度 → 调整策略 → 调整后效果」**清晰告知用户。
3. 锁定每面合成关系：
   - **正面 T 恤实拍**：只合成 `side: "front"` 的 placement（正面主印花，或背面主印花配套的 `left_chest` 左胸核心小标）。
   - **背面 T 恤实拍**：只合成 `side: "back"` 的 placement（背面主印花）。

### 第三步：生成（Generate —— 印花颜色适配与 T 恤实拍合成）

1. **执行印花颜色调整适配**：
   - 对存在撞色冲突的 T 恤颜色，调用 [print adapt](../aionforge/references/tools/print-adapt.md)，传入透明印花与该颜色 T 恤实拍图，生成该色专属的适配印花 `refs/<product>-<color>-print-fit.png`（左胸小标若也撞色，同样生成 `refs/<product>-<color>-core-fit.png`）。
   - 确认返回的 `contrast_after ≥ 3.0`；若仍不足，改用 `outline` 策略重跑一次。
2. **合成到 T 恤实拍图**：
   - **优先本地确定性合成**：调用 [composite](../aionforge/references/tools/composite.md)，按锁定的 `placement` 与颜色将印花合成到各颜色正面/背面 T 恤实拍图上，输出 `bg_white/<product>-<color>.png` 与 `bg_white/<product>-<color>-back.png`。本地合成可 100% 保证文字笔画、图案几何与实拍衣服版型零篡改。
   - **复杂褶皱贴合（仅在用户明确要求深度贴合大褶皱时使用）**：按 [prompts/compose.md](../aionforge/references/prompts/compose.md) 编写 Prompt，先跑 [prompt check](../aionforge/references/tools/prompt-check.md)，再调用 [generate](../aionforge/references/tools/generate.md)。

### 第四步：检查（Verify —— 实拍合成图客观与视觉质检）

1. **客观检查**：对每张生成的 `bg_white` 图片调用 [verify](../aionforge/references/tools/verify.md)（若用户要求纯白底则开启白底检查；若为带场景的实拍平铺/挂拍图则保持原实拍背景，只检尺寸与完整性）。
2. **看图质检清单**：
   - **衣服零变形**：领口、肩线、袖长、袖口、下摆、面料纹理及背景与原始 T 恤实拍图 100% 一致。
   - **正背面零串位**：正面实拍图上只有正面主印花或左胸核心小标；背面实拍图上只有背面大印花，绝不把左胸小标印到后背。
   - **色彩与文字达标**：调色适配后的印花在 T 恤底色上清晰醒目，无白边/黑边毛刺，文字逐字准确、未镜像、只出现一次。
3. **回写真相源**：质检通过后，将路径回写到 `facts.colors[].bg_white`、`bg_white_back` 以及 `facts.canonical.garment`、`canonical.garment_back`。下游 `aionforge-main` 和 `aionforge-detail` 必须且只能引用这些合成好的商品图作为衣服标准。

---

## 失败路由

| 现象 | 处置 |
| --- | --- |
| 缺少背面 T 恤实拍图 | 停下请用户补图；绝不拿正面图冒充背面 |
| 合成后印花在深色/浅色 T 恤上看不清 | 回到第三步第 1 节，调用 [print adapt](../aionforge/references/tools/print-adapt.md) 切换 `white` / `lighten` / `darken` / `outline` 重新适配后再合成 |
| 印花边缘有白边或黑边 | 检查透明印花质量，或将合成墨色调整为匹配的模式重跑 |
| 模型合成导致文字变糊或衣服走形 | 立即切换回本地 [composite](../aionforge/references/tools/composite.md) 合成 |
