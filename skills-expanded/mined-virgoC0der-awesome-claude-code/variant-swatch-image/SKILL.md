---
name: variant-swatch-image
description: 为电商商品主图自动添加色块浮窗（variant color swatch overlay），生成 1:1 增强版 PDP 主图 PNG。用 CV 自动从 variant 图提取主色 / 检测花色面料，每次输出 6 种固定排版（裸色块 × {左下水平, 右上竖直} × {方形, 圆形} + 胶囊 × {右下横向, 右下竖向}），统一 1000×1000。**触发场景**：用户提到"主图加色块"、"色卡"、"色号缩略图"、"consolidated listing 主图"、"PDP 主图增强"、"shop tab 多色展示"、"variant swatch"、"swatch overlay"、"商品色号合并图"、"多色商品主图"、"color swatch on listing"，或者用户只是说"帮我给这个商品做个带色块的主图"、"shop 页面买家看不出有几个色"，都要触发。即使没有显式说"色块"，只要意图是把一个商品的多个 variant 颜色合并到一张主图上、让买家从缩略图就能看到所有色号选择，就用这个 skill。
---

# Variant Swatch Image

把多个 variant 颜色塞回到一张主图里 —— 让 shop tab / consolidated listing 的主图能一眼看出有几个色号。

每次运行输出 **6 张** 1:1 (1000×1000) PNG，主图相同、色块排版不同。下游可以挑一张推回各渠道，也可以拿 6 张做 A/B。

## Layout 清单

| Layout ID         | 描述                                          | Overflow 处理               |
|-------------------|-----------------------------------------------|-----------------------------|
| `bare-bl-square`  | 裸方形色块、左下角、横向排列                   | 全部展示，无 +N             |
| `bare-bl-circle`  | 裸圆形色块、左下角、横向排列                   | 全部展示，无 +N             |
| `bare-tr-square`  | 裸方形色块、右上角、竖向排列                   | 全部展示，无 +N             |
| `bare-tr-circle`  | 裸圆形色块、右上角、竖向排列                   | 全部展示，无 +N             |
| `pill-br-h`       | 白色圆角胶囊、右下角、横向，max 3 + "+N"      | 超过 3 显示 "+N"            |
| `pill-br-v`       | 白色圆角胶囊、右下角、竖向，max 3 + "+N"      | 超过 3 显示 "+N"            |

裸色块都带 2px 白描边 + 浅阴影，能在深色主图上保持识别。

## When to use

- AfterShip Feed 的 Consolidated Listing 主图增强
- TikTok Shop / SHEIN / Shopify 多色商品在 shop tab 缩略图找色号难
- 商家有多个 color variant 但每个 variant 的主图都长得一样，买家只能点进去才知道有几个色
- 需要批量生成"主图 + 色块"的增强图，推回各渠道作为新的 listing 主图

不适用：单色商品；尺寸 / 材质 variant（这个 skill 只处理 color variant）；商家原始主图本身就已经有色块条（先检测，跳过）。

## Pipeline overview

```
variant 图列表 ──► analyzer.py (CV 提色 / 花色检测) ──► swatch 数据
                                                          │
                                                          ▼
              主图 + layouts.py (6 个 layout 函数) ──► renderer.py
                                                          │
                                                          ▼
                pltf-capture 截图服务 ──► 6 张 public URL + 本地 PNG
```

截图走的是 AfterShip 内网的 `http://pltf-capture.as-in.io/v1/internal/screenshots`，需要环境变量 `AM_API_KEY`。

## Quick start

```bash
export AM_API_KEY=<your-am-api-key>
```

### Mode A — 已经有了主图和 variant 图

```bash
python scripts/run.py \
  --main-image /path/to/main.jpg \
  --variants /path/to/v1.jpg /path/to/v2.jpg /path/to/v3.jpg \
  --output-dir ./out
# 可选: --layouts bare-bl-square,pill-br-h   # 子集而非全 6
```

输出 6 张到 `./out/<layout-id>.png`，并把每张的 public URL 打到 stdout。

### Mode B — 从 Shopify products.json 自动拉

```bash
python scripts/run.py \
  --shopify-url https://store.com/products/handle \
  --main-color "carmine" \
  --output-dir ./out
```

会自动 GET `{shopify-url}.json`，对每个 variant 拉 `featured_image.src`，用 `--main-color` 对应的 variant 作为主图，其余的颜色全部出现在色块里。**每个有 featured_image 的 variant 默认就用图本身当 swatch**（中心裁切到鞋身/服装主体），不会退化成单色。

### Mode C — 从 Shopify PDP 解析商家原配 color swatch

**推荐用于"颜色选项本身就是图片"的场景**（如 SHEIN 风格的花色 swatch，或 Shopify 主题给某些色号配的纹理小图）。Shopify 主题通常把 swatch 渲染成 `<tooltip-component style="--swatch: rgb(...);">` 或 `style="--swatch: url(...);">`，inline 在 PDP HTML 里。

```bash
python scripts/run.py \
  --pdp-url https://store.com/products/rose-gold-glitz \
  --output-dir ./out
```

skill 会：
1. 抓 PDP HTML，提取每个 color option 的 `--swatch` 值（rgb → hex；url → 下载图片）；
2. 从同一个 product 的 `products.json` 拿主图；
3. 用提取的 swatch 列表渲染 6 个 layout。

混合模式（部分纯色 + 部分图片）原生支持——每个 swatch 各自走对应分支。

**外部 swatches.json 兜底**：有些主题（如 redaspenlove 用的 Shopify 主题）的 inline `--swatch` 是 JS 运行时注入的，SSR HTML 里取不到；但同时主题会在 JS config 里引用一个 `swatches.json` 文件，里面是 `name → hex` 的查表。Mode C 会在 inline `--swatch` 路径返回 0 时自动：
1. 从 PDP HTML 里找 `swatches: '//.../swatches.json'` 引用；
2. 从 `<input name="options[Color]" value="...">`（或 `data-swatch="..."`）拿到 variant 名字列表；
3. 用名字去 swatches.json 里查 hex，拼成 swatch 列表。

也就是说，对这种 "色号在外部 JSON 里" 的主题，照样 `--pdp-url <pdp>` 一条命令搞定，不需要手动指定 swatches.json URL。

### 图片色块 vs 单色色块 — 优先级

1. **`--swatch-images URL1 URL2 ...`**（最高）—— 显式覆盖，全部当图片 swatch，URL 和本地路径混用都行。
2. **`--pdp-url`** —— 从 PDP HTML 解析商家原配 option swatch（混合 rgb/url）。
3. **Mode B 自动** —— `variant.featured_image.src` 有值时把 variant 商品图直接当 swatch（中心裁切）。
4. **CV 提取** —— `classify_variant()` 从 variant 照片里抠主色 / 检测花色纹理。

什么时候要 `--swatch-images`？商家把每色拆成独立 listing 时，PDP 也可能只渲染当前色——这时手动列出兄弟 listing 的代表图，或者从父 consolidated listing 拷图。

### 程序化调用

```python
from scripts.analyzer import classify_variant
from scripts.renderer import render_layouts

swatches = []
for path in variant_paths:
    info = classify_variant(path)
    if info["is_pattern"]:
        swatches.append({"image_path": path})
    else:
        swatches.append({"color": info["hex"]})

results = render_layouts(
    main_image_path="main.jpg",
    swatches=swatches,
    output_dir="./out",      # 可选；省略则只返回 URL
    bg_color="#FFFFFF",
    # layouts=["pill-br-h"]  # 可选；默认全 6
)
# results = [{"layout", "url", "file_id", "local_path"}, ...]
for r in results:
    print(r["layout"], r["url"])
```

## Component reference

### `scripts/analyzer.py` — Color extraction

- `extract_dominant_color(image_path) -> hex_str`
  通过过滤白底 + 16-step 颜色 bucket + 取 top bucket 均值得到主色。对正常 Shopify 风格的纯色商品图准确度很高（实测误差 < 2/255 per channel）。

- `classify_variant(image_path) -> {"hex", "variance", "is_pattern"}`
  双信号花色检测：颜色 stdev > 28 **且** top bucket 占比 < 50% → 判定为 pattern。Pattern 的 variant 在渲染时会保留图片纹理本身作为 swatch（中心裁切）而不是退化成单色。

阈值已经在合成数据 + 真实 Shopify 图上调过；如果你的场景假阳率高（纯色被当成花色），把 `variance > 28.0` 调到 35–40。

### `scripts/layouts.py` — Layout 注册表

每个 layout 是一个 `(main_uri, swatches, bg_color, swatch_to_uri) -> html_str` 函数，注册在 `LAYOUTS` dict 里，key 就是上面表格里的 layout ID。新增 layout 时：

1. 在 `layouts.py` 里写一个返回完整 HTML 的函数；
2. 加进 `LAYOUTS` 字典；
3. 自动会被 `render_layouts` 和 CLI `--layouts` 识别。

胶囊类 layout 的 `max_visible` 常量是 `PILL_MAX_VISIBLE = 3`，改这里全局生效。

### `scripts/renderer.py` — 渲染入口 + 截图

- `render_layouts(main_image_path, swatches, layouts=None, output_dir=None, bg_color="#FFFFFF", width=1000, wait_seconds=1.0) -> List[dict]`
  **主入口**。`layouts=None` 时跑全 6 个，否则按 ID 子集跑。`output_dir` 给定则把每张 PNG 下载到 `{output_dir}/{layout_id}.png` 并 crop 成 1:1。返回 list，每项 `{"layout", "url", "file_id", "local_path"}`。

- `render_listing_image(...)` — 旧的单图入口，保留兼容。新代码请用 `render_layouts`。

- `screenshot(html, width=1000, wait_seconds=1.0) -> dict`
  调 `pltf-capture` 服务，返回 `{"image_url", "file_id"}`。`AM_API_KEY` 没设或者 API 返回非成功（既不是 200 也不是 20000）都会 raise `RuntimeError`。

所有图片用 base64 data URI 内联到 HTML 里，所以渲染时不会因为 CDN 慢导致空白。HTML 大小通常 60–300KB（取决于主图分辨率），完全在 pltf-capture 的 payload 限制内。Pattern 类 swatch 自动中心裁切，去掉服装剪影边缘，只保留花纹纹理。下载本地 PNG 时会自动 crop 成 1:1（pltf-capture 的 full_page 截图常常会比声明的 1000px 高几十像素）。

### `assets/template.html` — 旧的单 layout 模板（仅 `render_listing_image` 用）

老入口还指向这个文件，但新的 6 layout 路径完全在 `layouts.py` 里生成 HTML，不读 `template.html`。

## Dependencies

```bash
pip install pillow
export AM_API_KEY=<your-am-api-key>
```

只依赖 Pillow + stdlib（截图走的是 AfterShip 内网 pltf-capture 服务，本地不需要 Chromium）。

测试环境：Python 3.11+, Pillow 11.x。要从 AfterShip 内网外面访问，先确认 `pltf-capture.as-in.io` 可达。

## Known issues / extensions

1. **Pattern 检测假阴性**：拼色 / 撞色等"两色块"商品 variance 可能低于阈值。如果业务场景多见拼色，把判定从纯阈值改成基于 LLM 的 multimodal 分类（用 Vertex AI Gemini Vision 或 Claude Sonnet 4.x 看图判断 `is_pattern`）。

2. **主图背景不一致**：商家主图如果有 drop shadow 或浅灰底，跟模板白底会有色差。`renderer.py` 里加一步 PIL `replace_near_white(threshold=240)` 预处理可以拉齐。

3. **浮窗压到主图主体**：右下/左下/右上角浮窗对模特出镜 / 满构图主图不友好（会盖住人物）。当前没做避让逻辑；如果业务场景普遍是满图，可以加一步检测对应角的亮度，亮 → 直接叠 / 暗 → 换到对角。

## Bundled files

```
variant-swatch-image/
├── SKILL.md                  # 本文档
├── scripts/
│   ├── analyzer.py           # Color extraction + pattern detection
│   ├── layouts.py            # 6 个 layout 的 HTML 生成函数
│   ├── renderer.py           # render_layouts + screenshot
│   ├── shopify_pdp.py        # PDP option-swatch HTML 解析器
│   └── run.py                # CLI entry (Mode A / B / C + overrides)
└── assets/
    └── template.html         # 旧单 layout 模板（兼容路径）
```
