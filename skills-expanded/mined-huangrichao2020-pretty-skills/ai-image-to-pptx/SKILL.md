---
name: ai-image-to-pptx
description: 用 AI 直接生成 N 张风格统一的图，再嵌入到**真正的 PowerPoint 文件**（.pptx），用户能在 PowerPoint / Keynote / WPS 打开、可编辑、可投屏、可二次加工。这是 2026 年"知识传播 + 真实交付"的最佳组合：AI 出图效率 + PPT 格式兼容性。
version: 2.0.0
author: Mavis · MiniMax Agent
triggers:
  - "做成 PPT"
  - "真实的 PowerPoint 文件"
  - "把图打包成 .pptx"
  - "AI 生图 + PPT"
  - "用 .pptx 给我"
  - "PowerPoint 可编辑的"
  - "生成真实 PPTX"
---

# AI 生图 → 真实 PPTX Skill

## ⚠️ 出图前必走 · ppt 出图法 V2 7 步

**重要**：本 skill 只负责"把已有图嵌入 .pptx"。**生图前**必须走ppt 出图法 V2 7 步：

```
1. fetch 完整仓库内容（README + 子目录 + examples 并行）  ⚠️ 不能"读 80 行就开干"
2. reset todo（明确节奏）                                  ⚠️ 不能"流式想到啥做啥"
3. 整理 "N 张图主题+核心一句话" 清单（每张 1 行）          ⚠️ 不能把所有画面细节列死
4. 单张 prompt ≤ 60 行（不堆字体铁律）                    ⚠️ 不能堆 100+ 行
5. 出 P1 hook → 渲染核对清单（10+ 项）→ 走批量            ⚠️ 不能凭感觉看图就过
6. 接受 AI 主动加的细节和布局调整                          ⚠️ 不能否定 AI 偏差
7. 沉淀到 case 文档                                        ⚠️ 不能不做 case 沉淀
```

ppt 出图法 V2 完整方法论见 `~/.mavis/knowledge/knowhub/domains/visual-creation/methodology/ppt-out-image-method.md`。

**反例教训**（2026-07-02 how-to-agent-ppt）：没走 V2 7 步 → PPT 图字体幼稚、布局不丰富 → 用户反馈"前天的好多了"。

**正例**（2026-06-30 ai-training-ppt）：走了 V2 → 8 张图 + 真实 .pptx（20MB）一气呵成。

跳过 V2 7 步直接调本 skill = 极大概率翻车。

---

## 一句话定位

```
"AI 生图很强，但用户要能打开的 PPT 文件"
       ↓
   AI 直生图（matrix MCP）→ python-pptx 嵌入图片 → .pptx 文件
       ↓
   ai-training-methodology-handdrawn.pptx · 任何"知识图集 PPT"
```

## 完整流程（5 步）

```
1. 确定章节结构（问"做几张图？每张讲什么？"）
       ↓
2. 选风格 + 写 5 段式 prompt 模板（统一风格段）
       ↓
3. 批量调 matrix_generate_image 生成图（2 张/批防 timeout）
       ↓
4. 复制图到 PPT 项目目录，命名 01-overview.png / 02-xxx.png ...
       ↓
5. python-pptx 脚本嵌入图片 → 输出 .pptx
       ↓
6. （可选）部署或导出 PDF
```

## Step 1：5 段式 Prompt 模板

```
[1 场景]   是什么类型的图（信息图/海报/分镜）
[2 主体]   核心内容是什么（一句话）
[3 结构]   画面分几块、每块放什么（编号 1./2./3.）
[4 风格]   风格关键词 + 配色 + 字体 + 构图   ← 关键，跨图必须共享
[5 约束]   无错字、中文/英文、分辨率、不许出现XX
```

**核心原则**：结构 > 文采。把"画面分几块、每块放什么"编号说清楚，比写漂亮话有用 10 倍。

### 共享 [4 STYLE] 段（3 套速选）

**手绘科教风**（传播首选）：
```
Chinese hand-drawn doodle educational infographic.
Soft cream-pink paper background (#FFF5F5).
All outlines are sketchy hand-drawn black ink lines with slight wobble,
like drawn with a marker.
Hand-written style mixed Chinese text, key words in coral pink (#FF6B9D)
with hand-drawn wavy underlines.
Cards have soft pastel borders alternating:
mint green #B5EAD7, baby blue #A2D2FF, peach pink #FFC8DD,
butter yellow #FFF1A8, lavender #CDB4DB.
Macaron pastel color scheme, NO realistic textures, NO photo,
hand-drawn cute sticker style, kawaii aesthetic,
slightly imperfect charming lines, watercolor wash fills,
educational comic infographic, very clean and readable,
soft and friendly.
```

**商务科技风**（技术/B 端报告）：
```
Chinese knowledge comic infographic.
Soft light blue paper background (#eaf5fa).
Bold dark navy blue (#1e3a5f) thick borders and outlines.
Comic-style flat illustration with cute cartoon emojis as icons.
Bold mixed Chinese text, key words highlighted in red.
White cards arranged in modular grids with hard navy shadows.
Flat vector illustration, no photo elements, no realistic textures,
infographic poster, educational comic style, very clean and readable.
```

**博物图鉴风**（年度报告）：
```
Chinese flat illustration infographic in encyclopedia style.
Soft muted blue-gray background (#F4F6F8).
Pastel palette: sage green #87A96B, dusty rose #C9A0A0, soft beige #D9C9B0,
slate blue #6B8CAE, muted gold #B8A678.
Thin clean outlines, slightly muted saturation.
Information-dense modular layout with symmetric grid arrangement.
Hand-written serif mixed Chinese text, key words in dusty rose.
Educational poster style, flat illustration, clean typography,
museum catalog aesthetic, very readable.
```

## Step 2：matrix MCP 批量生图

```bash
# 推荐：2 张/批，timeout 360s
for i in 1 2 3 4; do
  start=$(( (i-1)*2 + 1 ))
  end=$(( i*2 ))
  echo "Batch $i: page $start - $end"
  # 实际：mavis mcp call matrix matrix_generate_image '{"prompt":"...","aspect_ratio":"16:9","resolution":"2K"}'
done
```

**关键参数**：
- `aspect_ratio`: `16:9`（PPT 宽屏）
- `resolution`: `2K`
- `batch_size`: 2（更高易 timeout）
- `timeout_per_request`: 360 秒（长 prompt 必须设够）

## Step 3：完整 python-pptx 脚本（98 行）

```python
#!/usr/bin/env python3
"""生成真实的 .pptx 文件：N 张图，每页一张全屏显示"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Emu

# === 配置 ===
PPT_DIR = Path("/path/to/your/ppt")
IMAGES_DIR = PPT_DIR / "images"
OUTPUT_PPTX = PPT_DIR / "output.pptx"

# === N 页配置（按顺序）===
PAGES = [
    {"file": "01-overview.png", "title": "第 1 章 · 总纲",   "subtitle": "..."},
    {"file": "02-two-layer.png", "title": "第 2 章 · 分层",  "subtitle": "..."},
    # ... N 个
]


def build_pptx():
    prs = Presentation()

    # === 关键 1: 设置 16:9 宽屏 ===
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # === 关键 2: 修正核心元数据，让 PowerPoint 正确识别 ===
    prs.core_properties.title = "你的 PPT 标题"
    prs.core_properties.author = "Mavis · MiniMax Agent"
    prs.core_properties.subject = "一句话描述"
    prs.core_properties.keywords = "关键词 1 关键词 2"

    blank_layout = prs.slide_layouts[6]  # 空白版式

    for i, page in enumerate(PAGES, 1):
        slide = prs.slides.add_slide(blank_layout)

        img_path = IMAGES_DIR / page["file"]
        if not img_path.exists():
            print(f"⚠️ Missing image: {img_path}")
            continue

        # 全屏图片
        slide.shapes.add_picture(
            str(img_path),
            left=Emu(0), top=Emu(0),
            width=prs.slide_width, height=prs.slide_height,
        )

        # === 关键 3: 页码 badge ===
        from pptx.util import Pt
        from pptx.dml.color import RGBColor
        from pptx.enum.shapes import MSO_SHAPE

        badge_w, badge_h = Inches(1.0), Inches(0.35)
        badge = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            left=prs.slide_width - badge_w - Inches(0.3),
            top=prs.slide_height - badge_h - Inches(0.3),
            width=badge_w, height=badge_h,
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(0xB8, 0x86, 0x0B)  # 古铜金
        badge.line.fill.background()
        badge_tf = badge.text_frame
        badge_tf.margin_top = Emu(0)
        badge_tf.margin_bottom = Emu(0)
        p = badge_tf.paragraphs[0]
        p.alignment = 2  # center
        run = p.add_run()
        run.text = f"{i} / {len(PAGES)}"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.name = "Microsoft YaHei"

        print(f"  ✓ Page {i}: {page['title']}")

    prs.save(str(OUTPUT_PPTX))
    print(f"\n✅ PPT 生成成功: {OUTPUT_PPTX}")
    print(f"   共 {len(PAGES)} 页 · 16:9 宽屏 · 单页贴图")


if __name__ == "__main__":
    build_pptx()
```

## 跨图风格一致 3 道防线

1. **共享 [4 STYLE] 段**：所有页 Prompt 里用同一段风格描述
2. **`input_urls` 喂参考图**：把第 1 张上传到 CDN 拿 url，作为后续图参考（matrix MCP 支持）
3. **图生图（image-to-image）**：拿第 1 张作为输入喂后续

**实测**：本 skill 的 case (8 张图) 用"共享 [4 STYLE] 段"一道防线就达到完美一致。

## 实战案例

| 案例 | 文件 | 特点 |
|---|---|---|
| ai-training-methodology-handdrawn.pptx | 8 页 · 20 MB | 手绘科教风 · AI 培训方法论 · 元数据修正 + badge |

**完整 case 文档**：
- `~/.mavis/knowledge/knowhub/domains/visual-creation/cases/2026-07-01-ai-image-to-pptx-ai-training.md`
- `~/.mavis/knowledge/knowhub/domains/visual-creation/methodology/ai-image-to-pptx.md`（源头，最全）

## 常见坑

| 坑 | 怎么避免 |
|---|---|
| PowerPoint 打开是空白 | 必须修正 `core_properties` + 设置 16:9 宽屏 |
| 中文乱码 / 字体错 | 图生成用中文，pptx badge 字体设 `Microsoft YaHei` |
| 风格漂移（5 张图看起来像 5 套设计） | 共享 [4 STYLE] 段 + 推荐 input_urls |
| 矩阵生图 timeout | 2 张/批 + timeout=360s |
| badge 抢图 | badge 放右下角 + 小尺寸（1.0" × 0.35"） |
| pptx 文件太大 | 8 页 2K 图 ≈ 20MB 正常；想小可降到 1K |
| 页数记错（badge 显示 5/8 实际 8 页） | 用 `f"{i} / {len(PAGES)}"` 动态 |

## 30 秒起步

```bash
# 1. 准备 images/ 目录 + N 张图（PNG/JPG 都行）
# 2. 复制上面 build_pptx.py 改成你的 pages
# 3. 跑
python3 build_pptx.py
# 4. 双击 .pptx
```

## 进阶扩展

- **可编辑文本层**：用 `add_textbox()` 在图片上方加文字框，用户能改
- **通用化**：接受 `pages.json` 输入，自动出 HTML + PPTX 双版本
- **PDF 导出**：`libreoffice --headless --convert-to pdf output.pptx`
- **元数据时间戳**：`prs.core_properties.created = datetime.now()`

## 跟 html-ppt-viewer 的关系

| 维度 | html-ppt-viewer | ai-image-to-pptx |
|---|---|---|
| 输出 | index.html + 图 | .pptx 真实文件 |
| 适合 | 分享 / 看效果 | 编辑 / 投屏 / 客户交付 |
| 大小 | ~2MB | ~20MB |
| 双击打开 | 不行（要浏览器） | ✅ |
| 编辑内容 | 不能 | ✅ |

**默认工作流**：HTML 先试（5min）→ 用户确认 → PPTX 落定（10min）。
