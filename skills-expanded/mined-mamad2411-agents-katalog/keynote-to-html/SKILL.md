---
name: keynote-to-html
description: |
  把 Apple Keynote（`.key`）演示文稿转成 `deck.json` + HTML deck：逐页遍历，
  把每一页重建为绝对定位的 HTML——图片仍是 `<img>`、文本是可编辑的 HTML
  文本、视频是 `<video>`。与 `feishu-deck-h5` skill 配合使用：本 skill 产出
  `deck.json`，`feishu-deck-h5/deck-json/render-deck.py` 把它包装成带演示模
  式 chrome（← → 翻页 / F 全屏 / 进度条 / 移动端滚动模式）的最终 HTML。

  触发词：「把 Keynote 转成 HTML」、「import keynote」、「.key 转 deck」、
  「.pptx 转 HTML」（先用 Keynote 打开 PPTX 另存为 .key 即可），或者用户给出
  `.key` 文件路径 / Keynote 里已打开的文稿。

  每一页的处理流程：
    1. AppleScript 遍历该页所有 iWork 元素，输出 (类型, 位置, 尺寸,
       文件名, 文本, 字体 / 字号 / 颜色)。
    2. 图片的文件引用按 .key bundle 的 Data/ 目录解析：先精确前缀匹配；
       对模糊的 "pasted-image.pdf" 类情况退回尺寸 / 长宽比匹配。
    3. 每个非文本元素变成原始 (x, y, w, h) 处的 `<img>` / `<video>`；
       每个文本变成带原字体 + 字号的真实 HTML 元素。
    4. 该页以 `layout: "raw"` 形式写入 deck.json。
    5. `feishu-deck-h5/deck-json/render-deck.py` 包装成带演示模式 chrome
       的 HTML。

  可接受的失真（不要因此阻断）：
    · 自定义 Keynote 字体（鸿蒙 / 阿里巴巴普惠 / 方正兰亭）退回到 web-safe
      中文字体栈（PingFang SC、Microsoft YaHei）。
    · 1–2 个模糊的 pasted-image 文件可能匹配错源 —— 记录后继续。
    · 母版背景渐变尚未解析（best-effort）。
    · 动画 / 入场效果会被丢弃（有意为之 —— HTML 不需要）。
---

# keynote-to-html

## 这个 skill 做什么

你给它一个 `.key` 文件。它会用 Keynote 只读打开，通过 AppleScript 遍历每一
页上的每个 iWork 元素，把引用的图片 / 视频从 `.key` bundle 里拷出来，并产出
一份 `deck.json`（每页一条 `layout: "raw"` 记录）。然后调用 `feishu-deck-h5`
的渲染器把 deck 包装成自包含的 HTML 页面。

**PowerPoint（`.pptx`）也支持** —— 用 Keynote 打开 `.pptx`，选「文件 → 存
储为...」，格式选 `.key`，把生成的 `.key` 交给本 skill 即可。Keynote 自带
`.pptx` 导入，转出来的 `.key` 跟原生 Keynote 文件读起来一样。

## 何时调用

当用户手上有 `.key` 文件（或可以用 Keynote 转存的 `.pptx`），并希望产出一份：

  - 视觉与原 Keynote 95% 以上一致
  - 文字可编辑（HTML 元素，不是像素）
  - 视频可播放（通过 AppleScript 的 movie items 提取位置）
  - 自带 `feishu-deck-h5` 演示模式 chrome（← →、F 全屏、底部控制条、进度条）

**不要**在以下场景调用：
  - 只有 PDF 输入（请使用 PDF 路径；`.key` 拥有 PDF 丢失的结构化数据）
  - 从零做"重设计"的 deck（本 skill 是 1:1 忠实转换器；自由创作请直接用
    `feishu-deck-h5` skill）

## 前置检查

1. 确认 `.key` 文件存在。如果用户只给了名字（没有路径），用
   `mdfind "<名字>.key"` 搜一下。
2. `pip install PyMuPDF Pillow keynote-parser` —— 用于 PDF→PNG 转换（光
   栅兜底）、图片尺寸探测、基于 IWA 的确定性资产 / 对齐解析。已装的话跳过。
3. 确认 **Keynote** 已安装（`com.apple.Keynote`，v15+；旧版
   `com.apple.iWork.Keynote` v14 也能用，需修改 `extract.applescript`
   顶部的 bundle id）。
4. 确认 `feishu-deck-h5` skill 可达。默认查找 `../feishu-deck-h5/`（同级
   skill）；用 `--renderer <路径>` 覆盖。

## 调用方式

```bash
bash skills/keynote-to-html/assets/run.sh \
  "<path-to-.key>" \
  "<output-dir>" \
  [--limit N]            # 只转前 N 个非跳过的 slide
  [--renderer PATH]      # 渲染器 skill 路径（默认: ../feishu-deck-h5/）
  [--rasters-dir DIR]    # 兜底裁剪用的每页 PNG 目录（slide-NN.png）
  [--pdf PATH]           # 源 PDF，按需做兜底光栅化
```

本 skill 会用 Keynote 打开 `.key`，跑 AppleScript 把每页元素数据写到
`<output-dir>/extract.tsv`，把匹配到的资源拷 / 转到
`<output-dir>/assets/slide-NN/`，构造 DeckJSON 的 `deck.json`，再调用渲
染器的 `render-deck.py` 产出 `index.html`。

`.key` 文件本身不会被改动，Keynote 也是只读打开。

### 光栅兜底 —— `--rasters-dir DIR` / `--pdf PATH`

二选一（或都不给）来启用光栅兜底。启用后，所有无法结构化重建的元素类型
（线条、图表、表格、矢量蒙版、无法提取填充的形状）会从该页的 PNG 上裁出
来，作为 `<img>` 嵌入 —— 这样即使结构化提取失败，视觉也能落地。

## Pipeline 文件

| 文件 | 作用 |
|---|---|
| `assets/extract.applescript` | 驱动 Keynote，输出每页一行 (slide, element) 的 TSV |
| `assets/iwa_resolver.py` | 读 `.key` bundle 的 IWA 归档（通过 `keynote-parser`），恢复 AppleScript 不提供的资产 stem、真实 bbox、对齐元数据 |
| `assets/build.py` | 解析 TSV → 匹配图片 → 组合定位 HTML → 写 `deck.json` → 调用渲染器 |
| `assets/run.sh` | Bash 入口 |

## 验收

每次跑完手动检查这几项：

  - 浏览器打开 `<output-dir>/index.html`
  - ← → 键能翻页
  - F 键能进入全屏演示模式
  - 选一个文本元素 → DevTools → 编辑 → 渲染同步更新
  - 与原 Keynote 并排比对 —— 标出布局明显漂移的页（文字压在图上、图片裁
    错、字体差很多）。大部分漂移可以靠调 AppleScript 报告的位置 / 尺寸，
    或者调图片匹配启发式来修。

## 已知限制

  - **富文本 run**：一个文本框内多 style run（比如一段里有一个变色的词、
    粗细混排）—— 通过 per-run 提取已支持。早期版本会折叠到主样式。
  - **形状圆角**：AppleScript 没法干净地拿到 Keynote 的 corner-radius
    属性，用启发式（h<200 且 1.5 < aspect < 6 视为药丸；否则圆角矩形）
    覆盖大多数情况，但定制圆角不行。
  - **矢量线 / 箭头**：用光栅兜底输出（没启用兜底则跳过）。线的 h=0 让
    结构化渲染无意义；视觉由裁剪图承担。
  - **图表 / 表格**：不做结构化解析，靠光栅兜底输出视觉。
  - **自动缩字适应文本**：Keynote 会视觉缩小文字让它放进框里。AppleScript
    报告的是"作者设定"的字号，不是"显示"的字号。HTML 里溢出的文字可能与
    原图不符 —— 手动改 HTML 的 font-size 即可。
  - **图片裁剪** (`crop bounds`)：Keynote 14.5+ 关闭了 `crop bounds` /
    `image scale` / `image offset` 给 AppleScript 自动化。本 skill 用
    `object-fit: cover` 把整张原图塞进 bbox。对于 Keynote 里被裁出子区
    域的图片，视觉会与原图有差（通常会变亮）。
  - **图片旋转** 已提取；perspective / flip 变换没有。
  - **形状填充**：渐变 / 高级渐变 / 图片填充类形状的颜色 AppleScript 拿
    不到。同 bbox 的"形状 + 图片"对会兜底走光栅裁剪；否则形状视觉丢失。
  - **母版背景**：母版的背景**颜色**会提取；背景**图片 / 渐变**暂未解析。
    母版的 iWork items（图片、形状、文本）会提取；占位符文本（"幻灯片
    标题" / "正文级别 1" 等）会过滤掉。

本 skill 设计上随真实 deck 暴露出的边缘情况持续打补丁。欢迎 PR。
