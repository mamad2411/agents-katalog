---
name: FantuiDB
description: "电商视频爆款分镜逆向复刻专家。用于上传参考视频后抽帧、拼接 6/9/12 宫格、用多模态大模型提取分镜，再上传产品图进行自然融合替换，输出新产品故事板 Prompt、分镜 JSON 和 Excel 可录入表格。理解层与出图层均不绑定模型厂商。"
version: "0.3.0"
compatibility: "Trae, Claude Code, Cursor, Windsurf, Codex CLI, WorkBuddy 等可执行本地脚本的 SKILL.md 兼容 Agent；亦可编排为 n8n / Dify 工作流。依赖本地 FFmpeg + Python 3.9+。"
dependencies:
  - ffmpeg
  - ffprobe
  - python>=3.9
  - pillow
  - requests
---

# Skill: 电商视频爆款分镜逆向复刻专家

## 1. 第一性原理

本 Skill 不把"复刻视频"理解为逐像素复制，而是拆解为四个可复用层：

1. **分镜骨架**：镜头顺序、景别变化、镜头角度、主体位置。
2. **商品展示逻辑**：产品什么时候出现、怎么拿、怎么展示、怎么演示。
3. **转化脚本结构**：钩子、痛点、卖点、信任、演示、收口。
4. **视觉真实感**：UGC感、色温K值与白平衡、画面质感、生活化背景、光质与光源、手持感、非商业大片感。

最终目标是：把参考视频变成可被新产品复用的电商故事板模板。

## 1.1 任务模式

| 模式 | 说明 | 适用场景 |
|---|---|---|
| strict_replace（严格替换） | 保持原视频场景、镜头、构图、人物动作不变，只替换产品/人物/局部元素 | "保留原爆款视频形态，换成我的产品" |
| storyboard_transfer（结构迁移） | 保留爆款结构、销售节奏、分镜顺序、卖点推进逻辑，允许换产品/人物/场景 | "保留爆款逻辑，不要求原画面逐帧一致" — **默认** |
| hybrid_creative（半复刻创作） | 保留爆款骨架与销售逻辑，允许适度创意变化 | 仅在用户明确要求时使用 |

默认优先模式：
- 用户未指定 → storyboard_transfer
- 用户强调"原场景不变、只替换产品" → strict_replace

## 2. 激活场景

当用户提出以下需求时启用：

- “分析这个爆款视频”
- “帮我拆解这个带货视频”
- “把这个视频的产品换成我的产品”
- “抽帧拼 6/9/12 宫格”
- “生成电商视频分镜 Excel”
- “上传视频到 Trae 后自动抽帧分析”
- “参考爆款视频生成新产品故事板”

不要用于：

- 纯剪辑、裁剪、压缩视频。
- 从零生成无参考视频的广告创意。
- 需要复制他人品牌、真人身份、受版权保护画面进行商用冒充的请求。

## 3. 核心输入

```json
{
  "reference_video": "required",
  "grid_count": "required, one of [6,9,12]",
  "task_mode": "optional, one of [strict_replace, storyboard_transfer, hybrid_creative], default: storyboard_transfer",
  "product_images": "optional in phase A, required for product replacement",
  "character_images": "optional, for character/face replacement",
  "scene_images": "optional, for scene replacement",
  "product_selling_points": "optional",
  "target_platform": "optional",
  "output_type": ["reference_analysis", "excel_table", "storyboard_prompt", "shot_prompts", "storyboard_image"]
}
```

## 4. 推荐交互顺序

### 阶段 A：参考视频拆解

1. 用户上传参考视频。
2. 检查 FFmpeg / ffprobe。
3. 读取视频时长、分辨率、帧率。
4. 抽取 24-48 张候选帧。
5. 让用户选择或确认 6 / 9 / 12 宫格。
6. AI 从候选帧中选出最终代表帧。
7. 拼接宫格图。
8. 多模态大模型直接分析宫格图，提取画面中的文字、字幕、口播内容（无需单独 ASR）。
9. Vision 模型综合分析"宫格图 + 提取的文字"。
10. 输出 `reference_analysis.json` 和 Excel 表格。

### 阶段 B：新产品替换生成

1. 用户上传产品图。
2. Vision 模型提取产品画像。
3. 读取 `reference_analysis.json`。
4. 融合原视频分镜骨架 + 新产品视觉约束。
5. 输出新故事板 Prompt。
6. 调用 image2 API 生成新宫格故事板图。
7. 同时输出每格独立 Prompt，方便后续逐格高清生成。

## 5. 宫格选择与拼接规则

### 5.1 宫格数量选择

由用户手动选择，Skill 提供说明：

```text
6宫格：适合 8-10 秒短视频、镜头少、动作简单。
9宫格：适合 15-30 秒、大多数电商带货视频，默认推荐。
12宫格：适合 30 秒以上、镜头多、卖点多、动作较复杂的视频。
```

宫格数量规则：
1. 如果用户明确指定，严格按用户指定执行
2. 如果视频信息密度很高，宁可升到 12 宫格，也不要用重复帧凑数
3. 如果视频结构简单，宁可降到 6 宫格，也不要硬塞低价值帧
4. 宫格数量不只看视频文件大小，更要看视频时长、镜头数量、动作复杂度和卖点密度

### 5.2 拼接规范

| 规则 | 说明 |
|---|---|
| 工具 | `scripts/stitch_grid.py` 本地拼接，不调用外部 API，依赖 Pillow |
| 支持规格 | 6 / 9 / 12 宫格，**单张上限 12 格** |
| 每格比例 | 9:16 竖屏（适配抖音/TikTok/千川等短视频平台） |
| 总画布比例 | 不强制16:9，由宫格布局自然决定——拼图是分镜分析板，不是海报 |
| 想拼更多格 | 单张不扩到 12 格以上。镜头超过 12 个时，先拆成多轮 run（每轮 ≤12 格），再由人工或下游工具二次拼接，不要靠重复帧凑数 |

### 5.3 布局规则

| 宫格 | 列×行 | 排列方向 |
|---|---|---|
| 6宫格 | 3列 × 2行 | 从左到右、从上到下 |
| 9宫格 | 3列 × 3行 | 从左到右、从上到下 |
| 12宫格 | 3列 × 4行 | 从左到右、从上到下 |

### 5.4 图片适配

- 优先 cover（居中裁剪填满格子，不变形）
- 备选 contain（等比缩放 + 极窄补边，仅在裁剪会损失主体时使用）
- 禁止 stretch（拉伸变形）

### 5.5 间距与边距

| 参数 | 默认值 | 说明 |
|---|---|---|
| 格间距 gap | 4px | 极窄间距，视觉上接近紧密贴合 |
| 外边距 | 4px | 四周极窄安全边距 |
| 背景色 | 浅灰(245,245,245) | 存在感尽量弱 |

### 5.6 标注

- 默认不加文字、水印、说明字幕
- 可选 label-mode：`none`（默认）/ `index`（序号）/ `timestamp`（时间戳）

### 5.7 输出用途

- 爆款视频分镜分析
- 产品/人物/场景替换参考
- 后续 Image2 / 图生视频工作流的输入

## 6. 标准文件输出

实际运行目录（由 `scripts/run.py` 生成）：

```text
runs/{job_id}/
├── video_info.json                 # ffprobe 原始视频信息
├── candidate_manifest.json         # 候选帧清单（含时间戳、清晰度、来源）
├── candidate_frames/               # 候选帧（candidate_001.jpg ...）
├── uniform_frames/                 # 均匀抽帧中间产物（可清理）
├── scene_frames/                   # 场景切变抽帧中间产物（可清理）
├── selected_frames/
│   ├── selected_frames.json        # AI 选中的代表帧 + scene_role + 覆盖率校验
│   ├── candidate_contact_sheet_*.jpg   # 送模型的候选帧拼版（12 图/页）
│   └── selected_contact_sheet.jpg
├── grid_images/
│   ├── reference_grid_9.jpg        # 最终 6/9/12 宫格分镜图
│   └── reference_grid_9.json       # 拼图元数据（布局、帧来源）
├── analysis/
│   ├── reference_analysis.json     # 理解层提取的分镜分析结果
│   ├── product_profile.json        # 产品画像
│   └── shot_table.csv              # Excel 可录入表格（UTF-8-BOM）
├── prompts/
│   ├── new_storyboard_prompt.json  # 整张宫格 Prompt + 每格独立 Prompt
│   └── image2_storyboard_prompt.txt    # 直接喂给出图模型的最终 Prompt
├── storyboard_output/
│   ├── image2_storyboard_result.json   # 出图模型原始响应
│   └── new_product_storyboard.png      # 新产品故事板图
└── quality_check/
    ├── final_quality_check.json    # 自动质检报告
    └── repair_prompt.txt           # 未通过时的二次修正 Prompt（如触发）
```

## 7. 关键提示词文件

- `prompts/01_reference_video_analysis.md`
- `prompts/02_ai_select_representative_frames.md`
- `prompts/03_product_image_analysis.md`
- `prompts/04_storyboard_replacement.md`
- `prompts/05_excel_output.md`

## 8. 回复模板

使用 `templates/trae_reply_templates.md`。核心格式：

```text
老板，当前进度：{{stage}}

已完成：
1. {{done_item_1}}
2. {{done_item_2}}

生成文件：
- {{file_1}}
- {{file_2}}

下一步：
{{next_action}}

需要你确认：
{{confirmation_needed}}
```

## 9. 降级策略

| 故障点 | 降级方式 | 影响 |
|---|---|---|
| FFmpeg 不可用 | 用户手动上传截图 | 没有准确时间戳，动作时间线变弱 |
| 理解层多模态提取文字失败 | 只做纯视觉分析 | 丢失口播文案与字幕节奏 |
| Vision JSON 无效 | 重试一次；仍失败则返回原始文本 | 需要人工修正 |
| 产品图不足 | 允许单图继续 | 产品一致性下降 |
| image2 失败 | 只返回 Prompt 和 JSON | 无法直接产出新故事板图 |

## 10. 输出前校验

交付前必须检查：

- [ ] `reference_analysis.json` 是合法 JSON。
- [ ] 每个 shot 都有景别、主体、产品位置、动作、口播/字幕字段。
- [ ] 每个 shot 都有 scene_role（hook/pain/product_show/demo/closeup/result/reaction/trust/cta）。
- [ ] 产品画像包含颜色、形状、材质、识别点、替换约束。
- [ ] 新故事板 Prompt 明确保留原分镜结构。
- [ ] 每格独立 Prompt 与整张宫格 Prompt 不冲突。
- [ ] 明确声明哪些是"看见的"，哪些是"推断的"。
- [ ] 如果缺少产品图，必须说明质量损失。
- [ ] 自动质检结果已输出（quality_check 字段）。
- [ ] 如质检发现问题，二次修正建议已输出。

## 11. 严格禁止

1. 不承诺逐像素复制
2. 不编造产品不存在的功能
3. 不把新产品改成其他品类
4. 不把参考视频中的商标、人物身份、版权元素直接复刻为商用假冒内容
5. 不在用户没有产品图时声称已经完成产品替换
6. 不把任务理解成"重新创作一个类似视频"
7. 不丢失原参考视频的爆款分镜结构
8. 不随机抽帧后直接当关键分镜
9. 不忽略参考视频里的销售链路
10. 不生成脱离电商转化逻辑的分镜
11. 不把分镜图做成宣传海报风格
12. 不在宫格图中加入无关文案、字幕、水印、贴纸、图标、logo说明框
13. 不在没有用户要求的情况下擅自增加新道具、新背景、新人物、新剧情
14. 不把产品白底图的白底背景带入场景
15. 不允许产品外观漂移、颜色漂移、结构漂移、logo漂移
16. 不允许人物脸型、五官、发型、肤色在不同分镜中不一致
17. 不允许场景在不同分镜中风格漂移或逻辑断裂
18. 不允许镜头顺序混乱
19. 不在信息不足时擅自编造，必须标注"无法确认"或"输入缺失"

## 12. 自动质检与修正

每个阶段输出前必须执行自动质检：

| 检查项 | 通过条件 |
|---|---|
| 销售结构是否保留 | 原钩子→痛点→卖点→演示→收口链路完整 |
| 关键帧是否重复 | 无连续重复或构图几乎相同的帧 |
| 产品是否一致 | 所有分镜产品外观统一 |
| 人物是否一致 | 所有分镜人物脸型/五官/发型/肤色统一 |
| 场景是否统一 | 无风格漂移或逻辑断裂 |
| 镜头逻辑是否完整 | 叙事顺序正确，无断裂 |
| 是否存在文字污染 | 无字幕/水印/贴纸覆盖图像主体 |

如质检发现问题，必须执行二次修正：
- 关键帧重复过多 → 重新筛选，提升差异度
- 产品不一致 → 强化产品一致性约束
- 人物不一致 → 锁定五官、脸型、发型、肤色
- 场景漂移 → 强化场景统一性或原场景锁定
- 镜头功能断裂 → 按原销售结构重新排序


---

## v0.3.0 API 接入约定

本 Skill 的 API 层分两部分：**理解层（任意大模型）** 与 **出图层（任意生图模型）**。
两层**均不绑定模型厂商**，仓库内置的实现都只是**参考示例**，不是可选范围上限。

### 1. 理解层（任意大模型，推荐多模态）

用途：分析、理解、结构化输出、Prompt 生成、自动质检。

**不指定厂商，也不预置默认模型。** 只要同时满足两点即可直接使用：

1. 兼容 OpenAI 协议：`POST {LLM_BASE_URL}/chat/completions`；
2. 支持图片输入（多模态）——流水线靠它读宫格图与产品图，纯文本模型无法完成反推断。

配置（三个都必须填）：

```env
LLM_API_KEY=<你的密钥>
LLM_BASE_URL=https://<你的服务>/v1
LLM_MODEL=<模型名或接入点 ID>
```

可选 `LLM_JSON_MODE=true` 时附带 `response_format`（部分服务商不支持会返回 400，默认关闭）。
未配置 `LLM_*` 时回落到旧变量名 `ARK_API_KEY` / `ARK_BASE_URL` / `DOUBAO_MODEL`。
输出文件为 `analysis/reference_analysis.json`。

调用文件：

```text
scripts/providers/llm_client.py     # 实现（通用）
scripts/providers/doubao_client.py  # 兼容模块（历史文件名，等价于 llm_client）
```

### 2. 出图层（任意生图模型）

用途：根据 Prompt + 参考宫格图 + 产品图生成新故事板图。

判定标准只有一条：**能"接收 Prompt + 参考图、返回图片"**。统一契约定义在
`scripts/providers/base.py`，注册表在 `scripts/providers/__init__.py`。
切换模型只需改 `config.json` 的 `image_provider` 字段（或加 `--provider` 参数），业务代码零改动。

下列三个是**已内置的参考实现**（开箱可用，非范围上限）：

| 规范名 | 实现文件 | 默认模型 | 接入协议 |
|---|---|---|---|
| `image2` | `image2_client.py` | `image2-4k` | OpenAI 兼容 chat/completions |
| `gpt_image` | `gpt_image_client.py` | `gpt-image-1` | OpenAI Images API（generations / edits），可切 `chat` 风格 |
| `nano_banana` | `nano_banana_client.py` | `gemini-2.5-flash-image` | Gemini 原生 `generateContent`，可切 OpenAI 兼容风格 |

默认配置：

```env
IMAGE2_BASE_URL=https://api.yijiarj.cn/v1/chat/completions
IMAGE2_MODEL=image2-4k

GPT_IMAGE_BASE_URL=https://api.openai.com/v1
GPT_IMAGE_MODEL=gpt-image-1
GPT_IMAGE_API_STYLE=images

NANO_BANANA_BASE_URL=https://generativelanguage.googleapis.com
NANO_BANANA_MODEL=gemini-2.5-flash-image
NANO_BANANA_API_STYLE=gemini
```

别名（可直接写进配置）：`banana` / `nanobanana` / `nano-banana` / `gemini` → `nano_banana`；
`gptimage` / `gpt-image-1` / `openai` → `gpt_image`；`image-2` / `yijiarj` → `image2`。

**接入其他生图模型**（同样支持）：

1. 若目标模型提供 OpenAI 兼容 `chat/completions`，只需改 `base_url` / `model` / `api_key`，**零代码**；
2. 否则继承 `ImageProvider` 实现 `generate()` 并注册进 `REGISTRY`（约 40 行），**无需改动 `run.py`**；
3. 也可手工出图，走降级路径。

### 职责边界

- 理解层不负责最终出图，只负责把视频和产品拆解成结构化 JSON / Prompt，并做质检。
- 出图层不负责复杂分析，只负责根据 Prompt 和参考图生成故事板图。
- 如果模型返回结构不稳定，优先检查 `docs/api_integration.md` 与对应 provider 文件。
