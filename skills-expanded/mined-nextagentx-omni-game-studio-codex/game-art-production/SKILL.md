---
name: game-art-production
description: Produce release-grade 2D game art with AI image generation plus post-processing — style bible, per-asset prompts, consistency control, background keying, spec-compliant resizing, nine-slice validation and final asset gate. Use when the user needs real shippable art instead of placeholder rectangles.
---

# 正式美术生产

产出可上线的 2D 资源：立绘、背景、UI、道具、图标。**不是占位方块**——但要先说清边界（见文末）。

## 第 0 步：确认出图能力

按顺序确认，不要假设：

1. 先检查当前会话可用的原生图像生成或编辑工具，并在可用时直接调用；不要只写提示词。
2. Codex 的图像生成技能默认使用内置 `image_gen` 工具，不需要 API key。若用户明确选择直接 API 路线，可用下方插件适配器；该路线需单独配置 key 和模型权限。
3. 都不行就明确告知：**这条路当前产不出正式美术**，不要用脚本画方块冒充

### OpenAI Images API（可选）

仅在用户明确选择 API 服务后使用：需要用户在本机设置 `OPENAI_API_KEY`，组织具备图像模型访问权限，且真实生成请求可能计费。先用 `--dry-run` 预览。脚本要求 `--backup-dir`，先将 API 原始返回图片备份，再复制到运行时目录，不覆盖已有文件。

```bash
python scripts/gen_ai_image.py --prompt "single centered hand-painted blue space-helmet pickup icon, transparent background" --format png --background transparent --out assets/art/items/helmet.png --backup-dir doc/temp
python scripts/gen_ai_image.py --prompt "A tiny green robot waves, then turns and walks away; clean looping pixel-art animation" --format gif --frames 8 --frame-duration-ms 100 --out assets/animation/robot.gif --backup-dir doc/temp
```

内置 `image_gen` 的默认保存位置在 `$CODEX_HOME/generated_images/`。面向当前项目的图片生成后，马上将原图副本保存到项目规则指定的备份目录（此项目是 `doc/temp/`），再进行裁切、缩放、抠图等处理；最终资源也留在运行时资源目录。不要假设内置工具支持直接指定文件路径。

`--format gif` 使用模型生成的 2–16 帧短动画，不等同于经过游戏优化的精灵表；GIF 预览资格、尺寸限制与支持模型以[官方图像 API 文档](https://developers.openai.com/api/reference/resources/images/methods/generate)为准。需要逐帧控制时生成静态精灵表并使用 `game-animation-production`。Codex 会话内置图像生成工具可直接生成或编辑图像；它与该脚本的 API 密钥配置分开。

## 第 1 步：先做风格圣经（决定成败的一步）

系列素材需要统一风格时，可先用已有画面或一张主视觉作为视觉锚点；单项编辑沿用已有素材，不强制新增主视觉。

输出 `docs/art-style-bible.md`：

```
## 风格锚定段（每次生成都必须原样粘贴）
<一句话：媒介 + 画风 + 光照 + 色板 + 线条/材质特征>
例：2D 手绘卡通，粗描边，柔和顶光，紫金主色板（#7C3AED / #FBBF24），
    平涂加轻微噪点纹理，无渐变背景

## 色板（HEX）
主色 / 辅色 / 强调色 / 阴影色 / 高光色

## 禁止项
不要写实照片质感 / 不要赛博霓虹 / 不要 3D 渲染感 / 不要文字水印
```

**风格锚定段必须是固定文本**，每张图都原样带上，这是保证 40 张图像一个游戏的主要手段。

## 第 2 步：逐资产生成

单张提示词结构（顺序别乱）：

```
[风格锚定段] + [主体与姿态] + [尺寸/构图：正面/居中/留白] + [背景：纯白便于抠图] + [技术要求：无文字、无阴影投地]
```

- 需要透明背景时优先要求生成工具直接输出透明背景；仅在适合素材时使用纯色背景及抠色。
- 根据需要和预算生成变体，不强制固定数量。
- **同一角色**：带上已选定的那张作为参考图（若宿主支持 image-to-image），并复用同一段锚定文本
- 精灵表与动画生成、切帧和验收参见 `game-animation-production`；逐帧核查一致性，必要时修图。
- 遵守项目图片备份规则，原图、草稿和所有处理后图片均按项目要求先备份再处理。

## 第 3 步：后处理成规格

```bash
python scripts/process_art.py \
  --in raw/ui_btn_raw.png \
  --out assets/art/ui/ui_btn_primary.png \
  --size 256x64 --mode fit \
  --key-color "#FFFFFF" --key-tolerance 14 \
  --nine-slice 24 --check-nine \
  --report assets/art/ui/ui_btn_primary.report.json
```

关键判断：
- `--mode fit` 等比缩放 + 居中补透明，**不要用 stretch**，会变形
- `--check-nine` 会验证外圈是否可九宫格拉伸；不过就重新设计，别硬上
- 报告里的 `transparent_ratio` 如果接近 0，说明抠图没成功

## 第 4 步：图集与压缩

```bash
python scripts/pack_atlas.py --input assets/art/ui --out-sheet assets/art/ui_atlas.png \
  --out-data assets/art/ui_atlas.json --max-size 2048 --padding 2
```

图集划分按"同屏同集"，不按资源类型。单张不超过 2048×2048，低端机 1024×1024 更稳。

## 第 5 步：登记与终检

每条资源在 `assets/manifest.json` 里必须写全：

```json
{
  "path": "assets/art/ui/ui_btn_primary.png",
  "kind": "ui",
  "tier": "final",
  "size": [256, 64],
  "nine_slice": 24,
  "source": "ai",
  "ai_generated": true,
  "model": "gpt-image",
  "license": "AI-generated, commercially cleared under <service> terms",
  "commercial_ok": true,
  "note": "主按钮，三态"
}
```

```bash
python scripts/validate_assets.py --manifest assets/manifest.json --final --strict-license
```

终检会拦：仍是 draft、缺 license、sprite/ui 没有 alpha、全不透明（抠图没做）、尺寸不符。

## 授权与审核（不能跳过）

- **AI 生成素材的商用条款按服务而定**，逐服务核对并在 `license` 字段写清来源
- 部分平台（国内小游戏审核尤其）要求说明素材来源；`ai_generated: true` 就是给审核用的标记，别漏
- 字体只能用 OFL 开源字体（Noto / 思源系列），商用字体必须用户自购授权，**不要下载来源不明的字体**

## 做不到的部分（必须如实告知用户）

| 需求 | 结论 |
|------|------|
| 2D 立绘 / 背景 / UI / 图标 / 道具 | 能做，需人工筛选与修图 |
| 同角色逐帧动画 | 可尝试 AI 精灵表或序列帧，需检查一致性并视情况修图 |
| 3D 模型 / 骨骼绑定 | 本链路做不到 |
| 像素级严格统一（如严格像素风网格对齐） | 需人工逐像素修，AI 出图常半像素偏移 |
| 商用字体 | 只能给开源替代方案 |
