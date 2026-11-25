---
name: "color-palette-advisor"
description: "科学配色顾问。通过两步引导（选择使用场景+选择配色风格）生成专业配色方案，输出 Pantone 风格的 HTML 报告。支持预设风格、流行风格、品牌配色，以及自定义风格描述、参考网站、上传截图三种输入方式。适用于网站设计、小程序、App 界面、UI 图标、海报/平面设计、数据可视化等场景。触发词：配色、色彩搭配、颜色方案、网站配色、UI 配色、设计配色。"
---

# Color Palette Advisor

科学配色顾问。通过两步引导选择生成专业配色方案，输出 Pantone 风格的 HTML 报告。

## Workflow

1. **Collect user intent** via chat interaction (reply with numbers).
2. **Generate palette** by calling `scripts/generate_palette.py` with the collected params.
3. **Validate** by calling `scripts/validate_palette.py` on the generated JSON.
4. **Inject** by calling `scripts/inject_template.py` to merge data into `assets/template.html`.
5. **Deliver** the resulting HTML and preview it if possible.

## Step 1 — Usage Scenario

Present the following options in chat and ask user to reply with the number:

**使用场景（回复数字选择）：**
1. 网站设计（Web Design）— 完整的 UI 色彩系统，包含暗黑模式适配
2. 小程序设计（Mini Program）— 轻量级配色，降低饱和度
3. App 界面设计（Mobile App）— 移动端适配，高对比度，考虑 OLED
4. UI 图标设计（UI Icons）— 高辨识度，小尺寸清晰
5. 海报/平面设计（Poster & Graphic）— 大胆鲜明，允许超饱和
6. 数据可视化（Data Visualization）— 色盲友好，高对比度，限制饱和度

**场景会影响配色生成：**
- **网站设计** → 完整的 UI 色彩系统，包含暗黑模式适配
- **小程序设计** → 轻量级配色，降低饱和度
- **App 界面设计** → 移动端适配，高对比度，考虑 OLED
- **UI 图标设计** → 高辨识度，小尺寸清晰
- **海报/平面设计** → 大胆鲜明，允许超饱和
- **数据可视化** → 色盲友好，高对比度，限制饱和度

## Step 2 — Color Style

Present the following options in chat and ask user to reply with the number:

**配色风格（回复数字选择）：**

**【预设风格】**
1. 清新自然（Fresh & Natural）
2. 科技现代（Tech & Modern）
3. 温暖活力（Warm & Energetic）
4. 高端简约（Premium & Minimal）
5. 复古怀旧（Retro & Vintage）
6. 活泼可爱（Playful & Cute）
7. 商务专业（Business & Professional）
8. 暗黑酷炫（Dark & Cool）

**【流行风格】**
9. 赛博朋克 / Cyberpunk
10. 蒸汽波 / Vaporwave
11. 马卡龙 / Macaron
12. 莫兰迪 / Morandi
13. 日系 / Japanese
14. 北欧 / Scandinavian
15. 波普 / Pop Art
16. 孟菲斯 / Memphis

**【品牌配色】**
17. 任天堂 / Nintendo
18. 星巴克 / Starbucks
19. 麦当劳 / McDonald's
20. 苹果 / Apple
21. 谷歌 / Google
22. Nike / 耐克

**【自定义输入】**
23. 🎨 自定义风格描述 — 输入风格词（必须是已知风格/品牌，否则可能生成不准确）
24. 🌐 参考网站 — 输入网址（如 https://apple.com）
25. 🖼️ 上传截图 — 输入图片绝对路径（如 /Users/xxx/Desktop/image.png）

**自定义输入示例与说明：**

| 输入类型 | 有效示例 | 无效示例 | 说明 |
|---------|---------|---------|------|
| 风格描述 | `赛博朋克`、`莫兰迪`、`霓虹`、`工业风` | `我想要好看的颜色`、`帮我配个色` | 必须是具体风格/品牌名称，系统会匹配数据库或联网搜索 |
| 参考网站 | `https://apple.com`、`https://starbucks.com` | `apple`、`苹果官网` | 必须是完整 URL（含 http:// 或 https://），系统会抓取网页主色调 |
| 上传截图 | `/Users/xxx/Desktop/screenshot.png` | `截图`、`桌面上的图` | 必须是绝对路径且文件存在，系统会提取图片主色调 |

**提示：**
- 风格描述越具体越好，如「赛博朋克」比「酷炫」更准确
- 参考网站建议选择品牌官网或设计参考站，避免内容杂乱的页面
- 上传截图建议提供设计稿、品牌 VI 手册或配色参考图

**输入类型自动检测规则：**
- 如果以 `http://` 或 `https://` 开头 → 自动识别为网站 URL，抓取网页主色调
- 如果以 `/` 开头且指向存在的图片文件 → 自动识别为图片，提取图片主色调
- 其他文本 → 按风格描述处理，匹配 `scripts/generate_palette.py` 中的 `STYLE_PALETTES`（风格库）或 `BRAND_PALETTES`（品牌库）

**处理优先级：**
1. 品牌库匹配（`BRAND_PALETTES`）— 返回品牌官方完整配色
2. 风格库匹配（`STYLE_PALETTES`）— 返回风格参考完整配色
3. 预设风格匹配（`STYLE_SEEDS`）— 基于 HSL 参数生成
4. ColorHunt API — 从网络获取配色方案
5. 自动生成 — 基于描述推断生成

## Script Calls

After collecting choices, run in order:

```bash
# 1. Generate palette JSON（自动生成唯一文件名，防止覆盖）
# 输出格式: {主题名}-{场景}-{时间戳}.json 和 {主题名}-{场景}-{时间戳}-result/index.html
python3 {skill_dir}/scripts/generate_palette.py \
  --style "{style}" \
  --scene "{scene}" \
  --output-dir {workspace}

# 脚本会输出实际生成的文件路径，例如：
# JSON: /Users/xxx/Desktop/TRAE SOLO/color/赛博朋克-网站设计-0611-143022.json
# HTML: /Users/xxx/Desktop/TRAE SOLO/color/赛博朋克-网站设计-0611-143022-result/index.html

# 2. Validate（使用实际生成的 JSON 路径）
python3 {skill_dir}/scripts/validate_palette.py \
  --palette {generated_json_path} \
  --complexity 5

# 3. Inject into template（使用实际生成的路径）
python3 {skill_dir}/scripts/inject_template.py \
  --template {skill_dir}/assets/template.html \
  --palette {generated_json_path} \
  --output {generated_html_dir}/index.html
```

**文件名规则：**
- **自定义描述**: `赛博朋克-网站设计-0611-143022.json`
- **参考网站**: `apple-网站设计-0611-143022.json`（提取域名）
- **上传截图**: `screenshot-网站设计-0611-143022.json`（提取文件名）

**防覆盖机制：**
- 文件名包含时间戳（月日-时分秒），确保每次生成唯一
- 同名文件自动追加序号（极小概率）
- 历史配色方案永久保留，不会被覆盖

## Output

- **JSON**: `{workspace}/{主题名}-{场景}-{时间戳}.json`
- **HTML**: `{workspace}/{主题名}-{场景}-{时间戳}-result/index.html`
- Single-file HTML, zero external dependencies, responsive.
- Features:
  - Pantone-style header card with auto text color (dark on light, light on dark)
  - Circular swatches with visible RGB/HEX codes on gray pill background
  - **RGB and HEX displayed on separate lines**, both clickable to copy with toast feedback
  - Poetic Chinese color names
  - 场景自适应：根据 Step 1 选择自动调整饱和度、对比度、生成暗黑模式/色盲友好方案
  - **历史保留**：每次生成独立文件，不覆盖之前的结果

## Fallbacks

| Condition | Behavior |
|-----------|----------|
| `AskUserQuestion` unavailable | Ask minimal clarifications in chat, or use defaults (网站设计 / 科技现代) |
| `template.html` missing | Stop and report the missing path |
| Output directory exists | Overwrite `index.html` only, preserve other files |
| Validation warnings (non-strict) | Log warnings but continue generation |
| Validation errors (strict) | Regenerate with adjusted seed or notify user |
| `OpenPreview` unavailable | Return the local file path to user |
| Website fetch fails | Fall back to default color generation based on style description |
| Image processing fails | Fall back to default color generation based on style description |
| Pillow not installed | Log error and fall back to description-based generation |
| ColorHunt API fails | Fall back to local STYLE_SEEDS generation |

## Resources

- Template: `assets/template.html`
- Scripts: `scripts/generate_palette.py`, `scripts/validate_palette.py`, `scripts/inject_template.py`
- Rules reference: `references/color-rules.md`
- Agent metadata: `agents/openai.yaml`
