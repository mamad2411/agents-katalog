---
name: bilingual-story-video
description: 从一个主题生成"教育意义短视频"：米色底板卡片布局，每幕首帧留白，随后黑白插画与中英文字开始渐显，彩色插画接着覆盖；文字、彩色和 edge-tts 中文旁白在最后一帧同步完成。基于 Remotion 渲染 MP4。当用户想把一个主题/故事做成这种双语字幕视频，或提到"双语视频""打字机字幕视频""黑白转彩色渐现视频"时使用。
---

# Bilingual Story Video（双语打字机故事视频）

输入一个主题，产出一支竖版教育短视频。每个场景 = 首帧留白 + 插画卡片（黑白→彩色左右渐现）+ 中英双语逐字渐显字幕 + 与整条揭示轨道同步的中文旁白。

## 本机环境（重要，先读）

这台机器没有系统级 node。可用的工具链：

- **node/npm**：`~/.local/node-bin/node`（从 ChatGPT.app 复制并重新 ad-hoc 签名的 node，可加载原生模块）。npm/npx 用 ChatGPT 自带的脚本。每个 shell 先执行：
  ```bash
  export PATH="$HOME/.local/node-bin:/Applications/ChatGPT.app/Contents/Resources/cua_node/bin:$PATH"
  ```
  ⚠️ 不要直接用 `/Applications/ChatGPT.app/.../bin/node` 跑 Remotion——它开了 library validation，加载 rspack 原生模块会报 "different Team IDs"。如果 `~/.local/node-bin/node` 不存在，重建：
  ```bash
  mkdir -p ~/.local/node-bin
  cp /Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node ~/.local/node-bin/node
  codesign --remove-signature ~/.local/node-bin/node && codesign -s - ~/.local/node-bin/node
  ```
- **ffmpeg**：`~/.local/bin/ffmpeg`（tts_generate.py 会自动找到）。
- **edge-tts**：系统 python3 已装（`pip3 install --user edge-tts`）。
- **SVG→PNG**（占位图/自绘插画用）：`qlmanage -t -s 1440 -o . file.svg`。注意 qlmanage 对 SVG 强制输出正方形，SVG 画布必须做成正方形（如 1440×1440），否则会被拉伸。

## 工作流

### 1. 写故事

先读 [references/story-writing.md](references/story-writing.md)（三幕结构、文案与提示词规则）。根据主题写 3–6 个场景。每个场景：

- `title`：大标题，6–10 个字，有钩子（如"他一天要抱二十次"）。
- `zh`：中文旁白句，18–30 字，一句话讲完一个画面。这句话同时是字幕和 TTS 文本。引号内容用逗号代替引号（TTS 读引号会怪）。
- `en`：对应英文翻译，口语化。
- `imagePrompt`：插画提示词。统一风格（如"soft watercolor children's book illustration"），只要**彩色**图——黑白版由 CSS 灰度滤镜自动生成，一张图两用。构图注意留白，画面会被裁成约 1.4:1 的横向卡片（objectFit: cover，上下会裁掉）。

系列信息：`meta.category`（如"亲子"）、`meta.series`（如"成长不会提醒"）。

### 2. 建项目

```bash
python3 scripts/new_project.py --output /abs/path/to/项目目录
cd 项目目录 && npm install --no-audit --no-fund
```

### 3. 填 story.json

编辑 `public/story/story.json`（结构见模板内的示例）。只填 meta + 每个场景的 id/title/zh/en/image/imagePrompt；audio、时间戳字段由脚本生成。

### 4. 生成插画

每个场景一张彩色图 → `public/assets/scene-<id>.png`。

```bash
python3 scripts/gen_images.py /abs/path/to/项目目录
```

- 有 `OPENAI_API_KEY` 时自动调 gpt-image-1 生成。
- 没有 key 时脚本会写出 `ASSET_PROMPTS.md`，把提示词交给用户在 ChatGPT 里生成后放入 `public/assets/`；或者用正方形 SVG 自绘 + qlmanage 转 PNG 做占位。

### 5. 生成旁白 + 时间数据

```bash
python3 scripts/tts_generate.py /abs/path/to/项目目录
```

对每个场景：合成 MP3 到 `public/audio/`，记录准确音频时长，并保留 WordBoundary/逐字时间数据到 story.json。渲染时以旁白总时长作为统一轨道：文字从黑白阶段开始线性逐字出现，彩色随后覆盖，二者在旁白结束的最后一帧同时完成。默认音色 `zh-CN-YunxiNeural`（男声，适合亲子/故事），女声可用 `zh-CN-XiaoxiaoNeural`，在 `meta.voice` 里改。语速 `meta.rate`（如 `-10%`）。

**必须先有 story.json 的 zh/en 再跑此脚本；改了文案要 `--force` 重跑。**

### 6. 预览静帧（渲染前必查）

```bash
npx remotion still StoryVideo out/check.png --frame=<每个场景中段的帧> --overwrite
```

每个场景至少检查 4 个关键帧：首帧、黑白完成帧、彩色中段、最后一帧。场景时长 = `1 + ceil(音频秒数×fps)`，逐场景累加偏移。检查：首帧只有米色底；黑白阶段已有文字；标题不换行溢出；图片构图没裁坏；中文字幕最多两行；英文没顶出安全区；最后一帧彩色与文字均为 100%。

### 7. 渲染 + 验证

```bash
npm run render   # 输出 out/story.mp4，H.264 + AAC
npx remotion ffmpeg -i out/story.mp4 2>&1 | grep -E "Duration|Stream"
```

确认：时长 = 各场景之和、有一路视频一路音频、分辨率 1080×1350。

## 视觉规格（模板已实现，一般不用改）

- 1080×1350（4:5 竖版）、30fps；米色底 `#F7F1E3`，主题色在 `meta.theme`。
- 每场景时间线：第 0 帧完全留白；第 1 帧起黑白图、旁白和文字同时开始；黑白在第 30 帧完成；彩色从第 31 帧开始覆盖；最后一帧彩色、中文、英文和旁白恰好同时完成，不加尾停顿或场景淡出。
- 打字机：以旁白总时长归一化，使用字符串切片逐字揭示；不可见的完整文本预留最终排版空间，因此换行不会抖动。
- 标题带黄色下划线生长动画；图片卡片左上角深绿圆形场景序号；字幕左侧黄色竖条。

## 常见坑

- **渲染报 rspack "different Team IDs"**：用了 ChatGPT 原始 node，见上文环境一节。
- **WordBoundary 为空**：edge-tts 7.x 必须传 `boundary="WordBoundary"`（脚本已处理，别改掉）。
- **图片 404 导致渲染失败**：所有 `scene.image` 必须真实存在于 `public/` 下再渲染。
- **中文标点时间戳**：标点不在 WordBoundary 里，脚本让它跟随前一个词的结尾出现，属正常。
- **浏览器复用**：模板通过 `remotion.config.ts` 自动探测 macOS/Linux 常见的 Google Chrome 或 Chromium 路径，优先复用系统浏览器，避免每个项目重复下载约 100MB 的 Headless Chrome。若未探测到，Remotion 会使用默认浏览器流程。
