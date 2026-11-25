---
name: canvas-design
description: >-
  Create beautiful visual art in .png and .pdf documents using design philosophy.
  You should use this skill when the user asks to create a poster, piece of art,
  design, or other static piece. Create original visual designs, never copying
  existing artists' work to avoid copyright violations. Defaults to Concrete Poetry
  (混凝土诗学), black/gold palette, PNG output, Chinese text with 得意黑 (Smiley Sans).
---

These are instructions for creating design philosophies - aesthetic movements that are then EXPRESSED VISUALLY. Output only .md files, .pdf files, and .png files.

Complete this in two steps:
1. Design Philosophy Creation (.md file)
2. Express by creating it on a canvas (**.png file by default**, or .pdf if user requests)

First, undertake this task:

## DEFAULT STYLE & OUTPUT

**⚠️ 除非用户明确指定其他风格，否则一律默认使用「混凝土诗学 (Concrete Poetry)」风格生成海报。**

**默认输出格式：PNG**（除非用户明确要求 PDF）。

**⚠️ 默认中文字体：得意黑（Smiley Sans / SmileySans-Oblique）**  
海报正文与中文标题一律使用 skill 内置的得意黑：`./canvas-fonts/SmileySans-Oblique.otf`。禁止用英文字体渲染中文。

**⚠️ 默认高分辨率 + 大字号（硬性要求，禁止小图小字）**：
- 画布默认 **至少 2400×3200 px**（竖版海报）；横版至少 **3200×2400 px**
- 主标题字号必须**足够大、一眼可读**，禁止 24–48px 级「小标签感」主文
- 详见下方「画布尺寸与字号规范」

### 默认美学：混凝土诗学 (Concrete Poetry)

Philosophy: Communication through monumental form and bold geometry.
Visual expression: Massive color blocks, sculptural typography (huge single words, strong secondary labels), Brutalist spatial divisions, Polish poster energy meets Le Corbusier. Ideas expressed through visual weight and spatial tension, not explanation. Text as rare, powerful gesture - never paragraphs, only essential words integrated into the visual architecture. Every element placed with the precision of a master craftsman.

**核心视觉语言**：
- 纪念碑式色块与雕塑感排版
- **超大单字 / 极大词组**占视觉主体；次要标签仍清晰可读，禁止「蚊子字」
- 粗野主义空间分割、硬边几何
- 信息靠视觉重量与空间张力传达，而非解释性文字
- 文字稀少、有力、**大而醒目**，嵌入视觉结构本身

### 默认配色方案（核心 — 必须遵守）

| 元素           | 颜色                       | Hex        |
| -------------- | -------------------------- | ---------- |
| **背景**       | 纯黑                       | `#0a0a0a`  |
| **强调色块**   | 金黄                       | `#ffd700`  |
| **主文字**     | 白色                       | `#ffffff`  |
| **次要文字**   | 灰色                       | `#888888` / `#666666` |
| **色块内文字** | 黑色                       | `#000000`  |

**配色使用规则**：
1. 画布底色统一为 `#0a0a0a`，不使用其他底色（除非用户明确改配色）
2. 金黄 `#ffd700` 仅用于强调色块、关键几何块、高权重视觉锚点
3. 主标题 / 核心信息用白色 `#ffffff`
4. 辅助标签、元信息、次级说明用灰色 `#888888` 或 `#666666`
5. 叠在金黄色块上的文字必须用黑色 `#000000`，保证对比与可读性
6. 默认不引入第三强调色；若用户要求扩展色板，仍以黑/金/白/灰为主骨架

**PIL 颜色常量模板**：
```python
BG       = "#0a0a0a"  # 背景
GOLD     = "#ffd700"  # 强调色块
WHITE    = "#ffffff"  # 主文字
GRAY     = "#888888"  # 次要文字
GRAY_DIM = "#666666"  # 更弱次要文字
ON_GOLD  = "#000000"  # 色块内文字
```

---

## DESIGN PHILOSOPHY CREATION

To begin, create a VISUAL PHILOSOPHY (not layouts or templates) that will be interpreted through:
- Form, space, color, composition
- Images, graphics, shapes, patterns
- Minimal text as visual accent

### THE CRITICAL UNDERSTANDING
- What is received: Some subtle input or instructions by the user that should be taken into account, but used as a foundation; it should not constrain creative freedom.
- What is created: A design philosophy/aesthetic movement.
- What happens next: Then, the same version receives the philosophy and EXPRESSES IT VISUALLY - creating artifacts that are 90% visual design, 10% essential text.

**默认路径**：直接以「混凝土诗学 (Concrete Poetry)」为运动名称与哲学内核展开；仅当用户明确要求其他风格时，再命名并撰写新运动。

Consider this approach:
- Write a manifesto for an art movement (默认即 Concrete Poetry)
- The next phase involves making the artwork

The philosophy must emphasize: Visual expression. Spatial communication. Artistic interpretation. Minimal words.

### HOW TO GENERATE A VISUAL PHILOSOPHY

**Name the movement** (1-2 words): 默认固定为 **"Concrete Poetry"** / **「混凝土诗学」**。仅在用户指定其他方向时另命名，例如 "Brutalist Joy" / "Chromatic Silence" / "Metabolist Dreams"。

**Articulate the philosophy** (4-6 paragraphs - concise but complete):

To capture the VISUAL essence, express how the philosophy manifests through:
- Space and form
- Color and material（默认锁定黑/金/白/灰体系）
- Scale and rhythm
- Composition and balance
- Visual hierarchy

**CRITICAL GUIDELINES:**
- **Avoid redundancy**: Each design aspect should be mentioned once. Avoid repeating points about color theory, spatial relationships, or typographic principles unless adding new depth.
- **Emphasize craftsmanship REPEATEDLY**: The philosophy MUST stress multiple times that the final work should appear as though it took countless hours to create, was labored over with care, and comes from someone at the absolute top of their field. This framing is essential - repeat phrases like "meticulously crafted," "the product of deep expertise," "painstaking attention," "master-level execution."
- **Leave creative space**: Remain specific about the aesthetic direction, but concise enough that the next Claude has room to make interpretive choices also at a extremely high level of craftmanship.
- **Honor default palette**: Unless the user overrides colors, the philosophy and canvas must use the black/gold/white/gray system above.

The philosophy must guide the next version to express ideas VISUALLY, not through text. Information lives in design, not paragraphs.

### PHILOSOPHY EXAMPLES

**"Concrete Poetry"** ⭐ **DEFAULT**
Philosophy: Communication through monumental form and bold geometry.
Visual expression: Massive color blocks, sculptural typography (huge single words, strong readable labels), Brutalist spatial divisions, Polish poster energy meets Le Corbusier. Ideas expressed through visual weight and spatial tension, not explanation. Text as rare, powerful, **large-scale** gesture - never paragraphs, only essential words integrated into the visual architecture. Every element placed with the precision of a master craftsman.
**Default palette**: `#0a0a0a` ground · `#ffd700` monument blocks · `#ffffff` primary type · `#888888`/`#666666` secondary · `#000000` type on gold.
**Default canvas**: 3000×4000 PNG; primary type at display/monument scale.

**"Chromatic Language"**
Philosophy: Color as the primary information system.
Visual expression: Geometric precision where color zones create meaning. Typography minimal - small sans-serif labels letting chromatic fields communicate. Think Josef Albers' interaction meets data visualization. Information encoded spatially and chromatically. Words only to anchor what color already shows. The result of painstaking chromatic calibration.

**"Analog Meditation"**
Philosophy: Quiet visual contemplation through texture and breathing room.
Visual expression: Paper grain, ink bleeds, vast negative space. Photography and illustration dominate. Typography whispered (small, restrained, serving the visual). Japanese photobook aesthetic. Images breathe across pages. Text appears sparingly - short phrases, never explanatory blocks. Each composition balanced with the care of a meditation practice.

**"Organic Systems"**
Philosophy: Natural clustering and modular growth patterns.
Visual expression: Rounded forms, organic arrangements, color from nature through architecture. Information shown through visual diagrams, spatial relationships, iconography. Text only for key labels floating in space. The composition tells the story through expert spatial orchestration.

**"Geometric Silence"**
Philosophy: Pure order and restraint.
Visual expression: Grid-based precision, bold photography or stark graphics, dramatic negative space. Typography precise but minimal - small essential text, large quiet zones. Swiss formalism meets Brutalist material honesty. Structure communicates, not words. Every alignment the work of countless refinements.

*These are condensed examples. The actual design philosophy should be 4-6 substantial paragraphs.*

### ESSENTIAL PRINCIPLES
- **VISUAL PHILOSOPHY**: Create an aesthetic worldview to be expressed through design
- **DEFAULT = CONCRETE POETRY**: Use 混凝土诗学 unless user requests another style
- **DEFAULT OUTPUT = PNG**: Save as `.png` unless user requests PDF
- **DEFAULT CANVAS = LARGE**: Min **2400×3200** (portrait) / **3200×2400** (landscape); prefer **3000×4000** for posters
- **DEFAULT TYPE = LARGE**: Monumental primary type; secondary still ≥ ~1.5–2% of shorter canvas side — never micro-type as default
- **DEFAULT PALETTE**: Black `#0a0a0a` / Gold `#ffd700` / White `#ffffff` / Gray `#888888`·`#666666` / On-gold `#000000`
- **DEFAULT CHINESE FONT = 得意黑 (Smiley Sans)**: Bundled at `./canvas-fonts/SmileySans-Oblique.otf`; never render CJK with English-only fonts
- **MINIMAL TEXT, LARGE SCALE**: Sparse wording, but each word must be **visually large** — few words, big impact
- **SPATIAL EXPRESSION**: Ideas communicate through space, form, color, composition - not paragraphs
- **ARTISTIC FREEDOM**: The next Claude interprets the philosophy visually - provide creative room
- **PURE DESIGN**: This is about making ART OBJECTS, not documents with decoration
- **EXPERT CRAFTSMANSHIP**: Repeatedly emphasize the final work must look meticulously crafted, labored over with care, the product of countless hours by someone at the top of their field

**The design philosophy should be 4-6 paragraphs long.** Fill it with poetic design philosophy that brings together the core vision. Avoid repeating the same points. Keep the design philosophy generic without mentioning the intention of the art, as if it can be used wherever. Output the design philosophy as a .md file.

---

## DEDUCING THE SUBTLE REFERENCE

**CRITICAL STEP**: Before creating the canvas, identify the subtle conceptual thread from the original request.

**THE ESSENTIAL PRINCIPLE**:
The topic is a **subtle, niche reference embedded within the art itself** - not always literal, always sophisticated. Someone familiar with the subject should feel it intuitively, while others simply experience a masterful abstract composition. The design philosophy provides the aesthetic language. The deduced topic provides the soul - the quiet conceptual DNA woven invisibly into form, color, and composition.

This is **VERY IMPORTANT**: The reference must be refined so it enhances the work's depth without announcing itself. Think like a jazz musician quoting another song - only those who know will catch it, but everyone appreciates the music.

---

## CANVAS CREATION

With both the philosophy and the conceptual framework established, express it on a canvas. Take a moment to gather thoughts and clear the mind. Use the design philosophy created and the instructions below to craft a masterpiece, embodying all aspects of the philosophy with expert craftsmanship.

**IMPORTANT**: For any type of content, even if the user requests something for a movie/game/book, the approach should still be sophisticated. Never lose sight of the idea that this should be art, not something that's cartoony or amateur.

**Default mode**: Express **Concrete Poetry** on a pure black ground (`#0a0a0a`) with gold monument blocks (`#ffd700`), white primary type, gray secondary type, and black type on gold. Output a single-page **high-resolution PNG** (see size rules below).

To create museum or magazine quality work, use the design philosophy as the foundation. Create one single page, highly visual, design-forward **PNG** output by default (or PDF if asked; unless asked for more pages). Generally use repeating patterns and perfect shapes. Treat the abstract philosophical design as if it were a scientific bible, borrowing the visual language of systematic observation—dense accumulation of marks, repeated elements, or layered patterns that build meaning through patient repetition and reward sustained viewing. Add sparse but **monumental** typography and systematic reference markers that suggest this could be a diagram from an imaginary discipline, treating the invisible subject with the same reverence typically reserved for documenting observable phenomena. Anchor the piece with simple phrase(s) or details, using the **default limited color palette** (black / gold / white / gray) that feels intentional and cohesive. Embrace the paradox of using analytical visual language to express ideas about human experience: the result should feel like an artifact that proves something ephemeral can be studied, mapped, and understood through careful attention. This is true art.

### 画布尺寸与字号规范（硬性 — 解决「图太小、字太小」）

**禁止**默认使用 800×1000、1080×1350、1200×1600 等偏小画布。手机预览缩小时，小画布 + 小字号会完全不可读。

#### 画布尺寸（像素）

| 用途 | 默认尺寸（宽×高） | 下限 |
|------|-------------------|------|
| **竖版海报（默认）** | **3000 × 4000** | **≥ 2400 × 3200** |
| 横版海报 | **4000 × 3000** | **≥ 3200 × 2400** |
| 方版 | **3000 × 3000** | **≥ 2400 × 2400** |
| 社交媒体竖图 | **2160 × 3840**（9:16） | **≥ 1080 × 1920**（仅用户明确要求小图时） |

- 用 PIL：`Image.new("RGB", (W, H), BG)`，**W、H 必须满足上表**
- 导出 PNG 时保持全尺寸，**不要**再缩放到半分辨率保存
- 可选：`img.save(path, "PNG", dpi=(300, 300))` 便于打印
- 用户未指定尺寸 → **一律竖版 3000×4000**

#### 字号阶梯（相对画布短边 `S = min(W, H)`）

在 **3000×4000**（S=3000）上的参考像素；其他尺寸按比例缩放。

| 层级 | 用途 | 相对短边 | 在 3000 宽上约等于 | 禁止低于 |
|------|------|----------|-------------------|----------|
| **monument / 纪念碑** | 单字、主标题、核心词 | **12%–28% of S** | **360–840 px** | **280 px** |
| **display / 大标题** | 2–6 字主句 | **6%–12% of S** | **180–360 px** | **140 px** |
| **title / 副标题** | 次级标题、区块名 | **3.5%–6% of S** | **105–180 px** | **90 px** |
| **body / 正文标签** | 短句、要点（仍要清晰） | **2.2%–3.5% of S** | **66–105 px** | **56 px** |
| **meta / 元信息** | 日期、编号、英文小标签 | **1.5%–2.2% of S** | **45–66 px** | **40 px** |

**字号铁律**：
1. 主视觉文字（海报「一句话/一个词」）必须用 **monument 或 display**，占画面显著体量
2. **禁止**把主文做成 24 / 32 / 48 px — 那是旧模板错误，在 3K 画布上等于蚊子字
3. 次要文字可以更小，但 **任何中文不得小于 ~40 px**（在 ≥2400 短边画布上）
4. 「文字少」≠「字号小」：字要少、字要**大**
5. 写完后自检：缩略图里主标题仍应可辨认；若缩略图看不清字 → 字号再加大或删减字数

#### 快速自检清单（导出前必过）

```
□ 画布 ≥ 2400×3200（竖）或用户指定且足够大
□ 主标题字号 ≥ 140 px（3000 宽画布上通常 ≥ 180）
□ 没有任何「重要信息」用 < 56 px 的字
□ PNG 未做二次缩小
□ 中文全部使用 canvas-fonts/SmileySans-Oblique.otf
```

**Concrete Poetry 构图要点（默认执行）**：
- 大面积色块切割画面，硬边、直角、纪念碑感
- **主词极大，占满结构**；次要文字克制但仍清晰（≥ body/meta 下限）
- 金黄色块作为「建筑体量」，白字在黑底上，黑字在金黄上
- 留白是有重量的负空间（黑），不是空
- 避免花哨渐变、柔光、紫色 AI 味配色

**Text as a contextual element**: Text is sparse and visual-first — **few words, large scale**. Prefer bold typographic gestures over whisper-quiet micro labels. All use of fonts must be design-forward. Regardless of text scale, nothing falls off the page and nothing overlaps. Every element must be contained within the canvas boundaries with proper margins. Check carefully that all text, graphics, and visual elements have breathing room and clear separation. This is non-negotiable for professional execution. **IMPORTANT: Use fonts from `./canvas-fonts`（中文默认得意黑）。** Get creative by making the typography part of the art itself.

### 语言与字体规范

**⚠️ 核心规则：海报内容统一使用中文！**

无论用户提供的原始内容是中文还是英文，生成的海报**必须使用中文**作为主要语言。

**例外情况（保留英文）**：
- 专业术语/关键词：`MASK`、`KEYFRAME`、`OVERLAY`、`EASING`、`FAQ`
- 技术参数：`5-20px`、`0.5s`、`25%`
- 品牌名/专有名词

**翻译示例**：
| 原始内容（英文） | 海报显示（中文） |
|----------------|----------------|
| Overlay Method | 覆盖层方法 |
| Six Details | 六个细节 |
| Common Problems | 常见问题 |
| Mask Geometry | 蒙版几何 |

---

### 默认中文字体：得意黑（Smiley Sans）— 必须遵守

**⚠️ 默认且唯一的中文字体：得意黑**，本 skill **已内置**，直接使用：

| 项 | 说明 |
|----|------|
| 中文名 | 得意黑 |
| 英文名 | Smiley Sans |
| **路径** | `./canvas-fonts/SmileySans-Oblique.otf`（备选 `.ttf`） |
| 用途 | **所有中文**：标题、正文、标签、色块内文字 |
| 授权 | SIL Open Font License 1.1（`canvas-fonts/SmileySans-OFL.txt`） |

**为什么必须用中文字体**：`./canvas-fonts` 里除得意黑外多为**纯英文**字体，用它们渲染中文会变成方框 `□□□`。

**英文字体（仅用于纯英文内容）**:
| 字体文件 | 用途 |
|---------|------|
| `GeistMono-Bold.ttf` | 英文代码、数字、技术标签 |
| `BigShoulders-Bold.ttf` | 英文大标题 |
| 其他 `./canvas-fonts/*.ttf`（非 SmileySans） | 仅限英文装饰文字 |

**核心规则**:
1. **任何包含中文的文本** → **必须**使用 `./canvas-fonts/SmileySans-Oblique.otf`
2. **纯英文/数字** → 可使用 `./canvas-fonts` 中的英文字体
3. **中英文混排** → 统一用得意黑，或分开渲染（中文得意黑，英文其他）
4. **默认不要换中文字体**；用户未指定时，禁止换成思源黑体、苹方、微软雅黑等

**常见错误示例**:
```python
# ❌ 错误：用英文字体渲染中文 → 乱码
font_mono = ImageFont.truetype("GeistMono-Regular.ttf", 24)
draw.text((x, y), "一行一行做", font=font_mono)

# ❌ 错误：画布太小 + 字号太小
img = Image.new("RGB", (800, 1000), BG)
font = ImageFont.truetype(FONT_CN, 32)  # 主文 32px 不可接受

# ✅ 正确：大画布 + 得意黑 + 大字号
img = Image.new("RGB", (3000, 4000), BG)
font = ImageFont.truetype(FONT_CN, 280)  # 主标题级
```

**画布 + 字体加载模板** (PIL/Pillow) — 默认 3000×4000、大字号阶梯：
```python
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---------- 画布：默认大尺寸 ----------
W, H = 3000, 4000          # 竖版海报默认；禁止随意改成 < 2400 短边
S = min(W, H)

# skill 根目录下的 canvas-fonts（字体已随 skill 打包）
FONT_DIR = Path(__file__).resolve().parent / "canvas-fonts"
FONT_CN = str(FONT_DIR / "SmileySans-Oblique.otf")
FONT_EN_MONO = str(FONT_DIR / "GeistMono-Bold.ttf")
FONT_EN_TITLE = str(FONT_DIR / "BigShoulders-Bold.ttf")

BG, GOLD, WHITE, GRAY, GRAY_DIM, ON_GOLD = (
    "#0a0a0a", "#ffd700", "#ffffff", "#888888", "#666666", "#000000"
)

# ---------- 字号：相对短边，禁止再用 24/32/48 当主文 ----------
def px(ratio: float) -> int:
    return max(40, int(S * ratio))

fonts = {
    # 中文 · 得意黑 — 大阶梯
    "cn_monument": ImageFont.truetype(FONT_CN, px(0.20)),  # ~600 @ 3000 — 单字/核心词
    "cn_display":  ImageFont.truetype(FONT_CN, px(0.10)),  # ~300 — 主标题
    "cn_title":    ImageFont.truetype(FONT_CN, px(0.045)), # ~135 — 副标题
    "cn_body":     ImageFont.truetype(FONT_CN, px(0.028)), # ~84  — 正文标签
    "cn_meta":     ImageFont.truetype(FONT_CN, px(0.018)), # ~54  — 元信息下限附近
    # 英文 · 仅纯英文
    "en_display":  ImageFont.truetype(FONT_EN_TITLE, px(0.10)),
    "en_meta":     ImageFont.truetype(FONT_EN_MONO, px(0.018)),
}

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

draw.text((120, 200), "诗", font=fonts["cn_monument"], fill=ON_GOLD)      # 金块内超大字
draw.text((120, 900), "关键帧动画", font=fonts["cn_display"], fill=WHITE)  # 主标题
draw.text((120, 1300), "六个细节", font=fonts["cn_title"], fill=GRAY)     # 副级
draw.text((120, 1500), "KEYFRAME", font=fonts["en_meta"], fill=GRAY_DIM)

img.save("poster.png", "PNG", dpi=(300, 300))  # 全尺寸导出，勿再缩小
```

To push boundaries, follow design instinct/intuition while using the philosophy as a guiding principle. Embrace ultimate design freedom and choice. Push aesthetics and design to the frontier.

**CRITICAL**: To achieve human-crafted quality (not AI-generated), create work that looks like it took countless hours. Make it appear as though someone at the absolute top of their field labored over every detail with painstaking care. Ensure the composition, spacing, color choices, typography - everything screams expert-level craftsmanship. Double-check that nothing overlaps, formatting is flawless, every detail perfect. Create something that could be shown to people to prove expertise and rank as undeniably impressive.

**Output the final result as a single, downloadable .png file by default** (or .pdf only if the user asks), alongside the design philosophy used as a .md file.

---

## FINAL STEP

**IMPORTANT**: The user ALREADY said "It isn't perfect enough. It must be pristine, a masterpiece if craftsmanship, as if it were about to be displayed in a museum."

**CRITICAL**: To refine the work, avoid adding more graphics; instead refine what has been created and make it extremely crisp, respecting the design philosophy and the principles of minimalism entirely. Rather than adding a fun filter or refactoring a font, consider how to make the existing composition more cohesive with the art. If the instinct is to call a new function or draw a new shape, STOP and instead ask: "How can I make what's already here more of a piece of art?"

Take a second pass. Go back to the code and refine/polish further to make this a philosophically designed masterpiece.

## MULTI-PAGE OPTION

To create additional pages when requested, create more creative pages along the same lines as the design philosophy but distinctly different as well. Bundle those pages as many .pngs (default) or one .pdf if requested. Treat the first page as just a single page in a whole coffee table book waiting to be filled. Make the next pages unique twists and memories of the original. Have them almost tell a story in a very tasteful way. Exercise full creative freedom.
