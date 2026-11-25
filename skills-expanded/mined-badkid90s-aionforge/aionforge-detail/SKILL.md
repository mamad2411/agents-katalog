---
name: aionforge-detail
description: >
  阶段 4 详情卖点图生成：按「思考 → 事实锁定 → 生成 → 检查」四步闭环，
  基于已通过质检的 T 恤实拍合成图（bg_white 正面/背面）和模特主图（main），
  生成放大镜细节图、正反双面/三角度对比图、60:40 主次分屏、左衣右签卖点图与多场景穿搭详情图。
  用户说根据主图和商品图生成详情图、详情页、卖点信息图、正反细节对比、面料微距时使用。
  Use when the user runs /aionforge-detail.
---

# 阶段 4：基于主图与商品实拍图生成详情图（detail）

本流程结合阶段 2 产出的 **T 恤正反面实拍合成图（`bg_white` / `bg_white_back`）** 和阶段 3 产出的 **模特主图（`main`）**，生成一套视觉统一、信息层级清晰的电商详情图，把主图没讲完的「正反面印花呼应、印花与面料微距、版型剪裁、多场景上身效果」讲清楚。

未加载入口时先读 `../aionforge/SKILL.md`。工具只按名称引用，参数见工具卡；本文件不写命令。Prompt 模板见 [infographic.md](../aionforge/references/prompts/infographic.md) 与 [vary.md](../aionforge/references/prompts/vary.md)。

## 输入与输出

| 方向 | 内容 | 说明 |
| --- | --- | --- |
| **输入** | 正面商品图 `bg_white`（`garment`）、背面商品图 `bg_white_back`（`garment_back`）、已通过的模特主图 `main`（`source`）、`facts.json` | 模特详情镜头强制复用 `main` 成片作为 `source`，确保详情与主图同一模特、同一件 T 恤 |
| **输出文件** | `output/<logo>/detail/<product>-<color>-<detail-id>.png` | 默认比例 `3:4`；指定平台时按 [platforms.md](../aionforge/references/platforms.md) |
| **输出事实** | `facts.selling_points`、`facts.target_scenes`、`facts.style_lock` | 锁死整套详情页的配色、字体与卖点文案 |

---

## 四步闭环执行流程

### 第一步：思考（Think —— 提炼 T 恤卖点与匹配详情板式）

1. **结合主图与商品图提炼卖点**：
   - 观察 `bg_white`（正背面实拍合成图）与 `main`（模特主图），避免用无意义的整屏纯图案充数，每张详情图必须回答买家的一个具体问题：
     - **有背面大印花 + 左胸小标时**：优先规划 **「正反双面 / 三角度同框 (`detail-three-angle`)」**（同屏展示正面左胸小标与背面大主印花的呼应）或 **「60:40 非对称主次分屏 (`asymmetric`)」**（左栏模特上身主视觉，右栏上下分格特写左胸小标与背面大印花/领口工艺）。
     - **突出印花质感与 T 恤做工时**：选 **「放大镜气泡 (`magnifier`)」**（微距放大圆领螺纹包边、纯棉平纹肌理、胶印/印花清晰边缘）。
     - **突出面料舒适度与百搭属性时**：选 **「左衣右签图标列表 (`icon-list`)」** 或 **「版型标注线 (`annotation`)」**（落肩袖、宽松直筒遮肉、克重透气）。
     - **突出实穿氛围时**：选 **「一衣多穿多场景分屏 (`detail-multi-scene`)」**。
2. **排版与配色思考**：
   - 根据目标平台从 [typography.md](../aionforge/references/typography.md) 与 `catalog/typography.json` 选取现代克制的色板（主底色、副底色、文字 Hex、强调色 Hex），拒绝廉价红黄爆炸贴和粗黑描边字。

### 第二步：事实锁定（Lock —— 锁定详情页菜单、文案与参考图映射）

1. 在 `facts.json` 中锁定：
   - `selling_points[]`：每条含类型、短标题（`≤10` 字）及 `visual_keywords`。
   - `target_scenes[]`：符合该 T 恤风格的 2–3 个真实穿着场景（如日常街拍、周末咖啡馆、通勤休闲）。
   - `style_lock`：包含色温、主副背景 6 位 Hex、文字 Hex 与字体规范（见 [style-lock.md](../aionforge/references/style-lock.md)）。
2. 明确每张详情图的参考图角色绑定：
   - 凡出现模特的板式（如 `asymmetric`、`detail-three-angle`、`detail-multi-scene`），必须同时传入 `source=模特主图` + `garment=正面商品图`（涉及背面展示时加传 `garment_back=背面商品图`）。
   - 纯平铺/静物特写板式（如纯成衣 `magnifier`、`icon-list`），传入 `garment=正面商品图`（或 `garment_back`）。

### 第三步：生成（Generate —— 逐屏编写 Prompt、静态检查并出图）

1. 按 [infographic.md](../aionforge/references/prompts/infographic.md) 对应板式编写 `<product_dir>/prompts/detail/<product>-<color>-<detail-id>.txt`：
   - 所有需要在画面中渲染的中文文案必须放入 `【VISIBLE_TEXT_BLOCK】` 并用中文引号 `「」` 包裹；单屏主标题 `≤12` 字，短签 `≤6` 字，总字数不超过 40 字。
   - 严禁把字号数值（如 `28pt`）、色号代码（如 `#2D2D2D`）当成画面可见文字渲染出来。
2. 调用 [prompt check](../aionforge/references/tools/prompt-check.md)（带可见文字时开启文字块检查），确认无「图1/图2」指代、Hex 色号齐全、印花原文一致。
3. 逐张调用 [generate](../aionforge/references/tools/generate.md) 生成详情图至 `detail/`。

### 第四步：检查（Verify —— 客观校验与排版/商品一致性检查）

1. **客观检查**：调用 [verify](../aionforge/references/tools/verify.md) 检查尺寸与 `3:4`（或平台指定）画幅比例。
2. **看图质检清单**：
   - **货不对板零容忍**：详情图里的 T 恤颜色、领口、袖口、正面左胸小标、背面主印花必须与 `bg_white` 100% 一致；模特五官与 `main` 主图完全同一人。
   - **正背面逻辑正确**：三角度图或正反对比图中，背面栏只展示后脑与后背大印花，绝不扭头露正脸，也绝不把胸前小标画到后背。
   - **排版呼吸感与文字清晰度**：版式留白充足（信息图留白 `≥45%`），文字与指示线全部落在留白区，未压挡人脸、领口或印花；放大 200% 检查汉字无乱码、无漏笔画、未把排版元指令画进画面。
3. **交付汇总**：列出 `detail/` 下生成的全部详情图文件，说明每张图回答的核心卖点及引用的主图/商品图来源。

---

## 失败路由

| 现象 | 处置 |
| --- | --- |
| 画面内汉字乱码或笔画粘连 | 精简标签字数（控制在 4–6 字）、替换为笔画简单的同义词，同一名称重跑一次 |
| 字号 / Hex 色码被画进了画面里 | 从 Prompt 描述中移除裸露的参数式写法，只保留 `「文案内容」` 与定性描述后重跑 |
| 详情图模特与主图不是同一人 | 检查是否漏传了 `source=main锚点图`，补齐角色参考后重跑 |
| 背面栏出现了正面印花或正脸 | 检查是否传入了 `garment_back`，在负面约束中加固「背面严禁露正脸、严禁出现左胸小标」 |
| 文字或放大镜压住了胸前/后背印花 | 在构图段明确指定气泡/标签分布在画面四周留白区，避开衣身中心 |
