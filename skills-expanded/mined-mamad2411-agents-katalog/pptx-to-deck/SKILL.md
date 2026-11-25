---
name: pptx-to-deck
description: |
  Convert an existing PowerPoint (.pptx) into an EDITABLE feishu-deck-h5 deck —
  a structured `canvas` deck.json that renders to a 16:9 present-mode HTML deck.
  STANDALONE skill that uses feishu-deck-h5 as its RENDER BACKEND (shells into its
  deck-json/render-deck.py; the final deck needs that skill's framework CSS/JS).
  feishu-deck-h5's parser also delegates .pptx import to this skill.

  Triggers: "把 PPT/PPTX 转成 deck/HTML/H5", "import pptx", ".pptx 转 deck",
  "把这份 PowerPoint 还原成网页/可编辑 deck", or when the user hands over a .pptx
  and wants it as an editable deck. Do NOT use for `.key` Keynote (use
  keynote-to-html), a from-scratch redesign (use feishu-deck-h5 directly), or
  producing a real .pptx.

  ONE pipeline: build_pptx.py = PURE CODE RECONSTRUCTION (python-pptx) → a
  `layout:"canvas"` deck.json of fully editable typed elements, rendered by
  render-deck.py. No extra deps (no LibreOffice / PyMuPDF). Decorative elements
  (gradients/glow/freeform/cropped images) are best-effort APPROXIMATE — the
  trade for full editability. (A LibreOffice/raster "hybrid" pipeline once
  existed; it was retired — see skills/_deprecated/.)

  See the SKILL.md body for deps, the lossy/approximation list, and placeholder +
  retired-flag (--raster/--full-raster are no-ops) behavior.
---

# pptx-to-deck

## When to invoke

Trigger when the user has a `.pptx` and wants a structured, editable deck that:
  - Reconstructs the original PowerPoint as best-effort (尽可能还原, not pixel-perfect)
  - Has editable text + typed/positioned elements (deck.json, NOT pixels)
  - Carries feishu-deck-h5's present-mode chrome (←/→ nav, F fullscreen,
    progress bar, mobile scroll mode)

Do NOT use for: `.key` (use keynote-to-html), or a from-scratch redesign
(use feishu-deck-h5 directly with a hand-authored deck.json).

## 管线：纯代码重建（唯一）

`build_pptx.py`（python-pptx）把 PPTX 重建成 `layout:"canvas"` deck.json——全结构化、
全可编辑的 typed elements，再用 render-deck.py 渲成 16:9 present-mode HTML。**不需要
LibreOffice / PyMuPDF**，只要 `python-pptx` + `lxml`。

取舍：装饰性元素（渐变、glow、阴影、自由曲线、艺术字、被裁剪的图片）永远是**近似**
还原——这是换「完全可编辑」付的代价。要的就是结构化可编辑，不是逐像素临摹（要临摹就
直接给客户原 PPT 导出图）。

一条命令（**自动**：重建 deck.json → 渲染 → `make_portable` 自包含打包 →
`post_process` 注入 letterbox + fitText 超框自适配）。产物**默认即交付级自包含**：
框架 CSS/JS（及其内部 `url()` 引的 lark logo）自动拷进 `<deck>/assets/` 并改写成相对
引用，`input/` 本就是 deck 本地目录——整夹拷走 / 打包 / 发给别人都不断，无需再单独跑
交付/copy-assets。收尾两步在 `assets/canvas_finish.py`（纯 stdlib，build 与
`rerender-deck.py` 共用）。

```bash
skills/pptx-to-deck/.venv/bin/python3 \
  skills/pptx-to-deck/assets/build_pptx.py \
  <in.pptx>  skills/feishu-deck-h5/runs/<deck-name> \
  [--renderer DIR] [--title TEXT] [--limit N] [--no-render]
```

依赖：`python-pptx`、`lxml`（skill 根的 `.venv` 里）。

> **fitText 超框自适配的边界**：`post_process` 注入的 fitText 在浏览器侧把**真正单行**
> 却超框的文本框 nowrap+scaleX 贴合（PPT autofit「溢出缩字」的确定性等价物，量真实
> bbox 不估算）。它**故意不动**多行 / 含 `<br>` 的框（避免把合法换行的段落挤成一行后
> 再压扁，见 canvas_finish 的 C4 注）。所以多行框的横向溢出目前仍可能 spill（overflow
> visible，不裁切但会越界）——属已知待办。

## Preflight

1. Verify the `.pptx` exists. If only a name was given, `mdfind "<name>.pptx"`.
2. Python deps: `python-pptx`, `lxml`. A venv at this skill's root is used
   if present:
   ```bash
   python3 -m venv skills/pptx-to-deck/.venv
   skills/pptx-to-deck/.venv/bin/pip install python-pptx
   ```
   (Or install on the system python; run.sh falls back to `python3`.)
   No LibreOffice / Pillow / PyMuPDF needed — rasterization is retired.
3. The renderer is the **sibling feishu-deck-h5** skill (auto-located as the
   sibling `<skills>/feishu-deck-h5/` dir, else `~/.claude/skills/feishu-deck-h5`).
   Override with `--renderer DIR`.

## Invocation

**Output convention:** generated decks go to the MAIN feishu-deck-h5 skill's
**outer** `runs/` (`skills/feishu-deck-h5/runs/<deck-name>/`) — alongside every
other deck the main skill produces, NOT inside this skill. (`runs/` is
gitignored repo-wide: regenerable, never committed.)

```bash
bash skills/pptx-to-deck/assets/run.sh \
  <in.pptx>  skills/feishu-deck-h5/runs/<deck-name> \
  [--limit N]        # only first N slides
  [--no-render]      # emit deck.json + input/ assets only, skip HTML render
  [--inline]         # single-file delivery (base64-inline) — avoid for image-heavy decks
  [--renderer DIR]   # feishu-deck-h5 skill root (default: sibling feishu-deck-h5, auto-located)
  [--title TEXT]
  [--raster]         # ⚠ RETIRED no-op (no screenshots)
  [--full-raster]    # ⚠ RETIRED no-op (no screenshots)
```

The build self-validates (DeckJSON schema gate runs before render) and prints
`unreconstructed slides: [..]` — any listed page is a placeholder the user must
redo by hand. Image assets are extracted to `<out-dir>/input/` and referenced
as `elements[].src = "input/<file>"` (real scannable paths for copy-assets/lift).

Preview: `bash skills/feishu-deck-h5/runs/<deck-name>/serve.sh` → localhost:8765

## Example / test fixture

`example/营销人的AI副驾/` is the kept reference deck — the real 60-page PowerPoint
this skill was hardened against (every fix in FIXLOG was verified here). It is
NOT a runtime output; it stays in the skill as the regression/demo fixture.
Committed lightweight (deck.json + montage_*.png + RESTORATION-REPORT.md +
index.html); the heavy regenerable `assets/` are gitignored.

## QA sweep

Screenshot every slide and build contact-sheet montages to scan for drift:

```bash
bash skills/pptx-to-deck/assets/sweep.sh <out-dir> [N]   # writes <out-dir>/montage_*.png
```

Montage thumbnails downscale dark/detailed slides toward black — confirm any
"black" suspect against its full-res `<out-dir>/sweep/sNN.png` before treating
it as a defect.

## Pipeline files

| File | Role |
|---|---|
| `assets/build_pptx.py` | python-pptx → positioned HTML → deck.json → 渲染 → canvas_finish 收尾（唯一管线） |
| `assets/canvas_finish.py` | 渲染层收尾（纯 stdlib）：make_portable 自包含打包 + post_process letterbox/fitText；build 与 rerender 共用 |
| `assets/rerender-deck.py` | 重渲已存在的 canvas deck.json（翻译/编辑后），render + canvas_finish 收尾 |
| `assets/run.sh` | bash entry point (venv-aware) |
| `assets/sweep.sh` | full-deck screenshot QA + montage |
| `assets/montage.py` | contact-sheet builder |

## Known limitations & the fix log

`FIXLOG.md` records every defect a real deck has exposed, its root cause, and
the **generalized** fix folded into `build_pptx.py` — the goal is that the next
PPT works first-try. When a new defect surfaces, fix it generically and append
to FIXLOG (don't hard-code per-deck workarounds). See `README.md` for the full
element-support table and the current lossy list.

**Hard-won gotcha (FIXLOG F3):** any value interpolated into an inline
`style="…"` attribute must use SINGLE quotes for font names — a nested double
quote truncates the attribute and silently drops every declaration after it
(color/weight), making light text render as the inherited dark default.
