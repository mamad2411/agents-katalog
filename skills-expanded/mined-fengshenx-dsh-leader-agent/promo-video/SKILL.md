---
name: promo-video
description: 端到端制作产品宣传片/竖屏短视频：文案分镜、真实 UI 素材、豆包旁白、HTML/CSS 动画、Playwright 录制、ffmpeg 音画合成、封面与验收。要从截图或文案一路做到成片时使用。
whenToUse: 需要把产品能力做成 30–90 秒宣传片、竖屏短视频或演示视频，且希望画面与旁白同步时。
---

# 产品宣传片流水线

这是一个**入口技能**：负责把“要讲什么”变成“能发的视频”，并在关键接缝上做验收。单项能力不在这里重复实现，按阶段加载：

- 真实 UI 截图：[`e2e-scenarios`](../e2e-scenarios/SKILL.md) 的“宣传素材截图”一节。
- 中文旁白：[`doubao-tts`](../doubao-tts/SKILL.md)。
- 封面/标题图：[`promo-stills`](../promo-stills/SKILL.md)。

**运行前提**：录制与封面脚本依赖 Playwright 与 `ffmpeg`/`ffprobe`，都不随 npm 包安装。Playwright 的安装命令见 [`promo-stills`](../promo-stills/SKILL.md) 的“运行前提”；`ffmpeg -version` 与 `ffprobe -version` 要能在 PATH 里跑通。TTS 脚本只依赖 Node 内置模块与环境变量。

## 核心原则

1. **一条片只讲一个转变**：问题 → 转折 → 解决 → 结果。不要塞功能清单。
2. **先有旁白，再有时间轴**：每段 TTS 实测时长决定场景边界；禁止先写死 60/72 秒再硬贴音频。
3. **画面跟着语义走**：旁白说到“卡长出来”，卡片才出现；说到“汇报”，汇报卡才展开。不要用固定节拍器。
4. **真实截图只做上下文，关键信息用大字号重排**：手机上看不清的 12px 截图文字，不要靠放大整张图解决。
5. **9:16 是重新排版，不是把 16:9 塞进竖屏**。横版素材要重组成纵向节奏。
6. **最后一帧停在品牌**，不要淡成黑屏；封面另做，不要把视频第一帧当封面。

## 阶段与门禁

### 1. 简报

先定：平台、比例、目标时长、受众、旁白音色、必须出现的真实素材、不能出现的内容。没有这些就开工，后面一定返工。

### 2. 文案与分镜

写一张分镜表，一行一个节拍：

| 时间 | 旁白 | 画面 | 素材 | 转场 |
|---|---|---|---|---|
| 0–9s | 同时跑五个任务…… | 五张任务卡纵向堆叠 | 真实任务卡 | 硬切 |
| 9–19s | 人成了循环里的阻碍点 | 竖环 + 中心“你” | HTML | 叠化 |

规则：

- 30–70 秒通常 5–7 个场景；一个场景只承担一个信息。
- 中文口播按 4–6 字/秒估算，最终以 TTS 实测为准。
- 第一屏 3 秒内出现冲突；最后 3–5 秒出现品牌和一句记忆点。
- 旁白与画面文字不打架：画面写短句，旁白说完整句。
- 详细模板与口播写法见 [`references/copy-and-storyboard.md`](references/copy-and-storyboard.md)；封面标题公式见 [`promo-stills`](../promo-stills/SKILL.md)。

### 3. 真实素材

采集、seed、脱敏与截图的唯一归属是 [`e2e-scenarios`](../e2e-scenarios/SKILL.md) 的“为宣传素材截真实 UI”一节。这里只保留宣传片的用法：

- 截图要包含足够上下文（窗口、侧栏、看板），但关键卡片另裁大图。
- 桌面 UI 在竖屏里只作为“真实感”背景；真正要读的信息用 HTML 或裁切卡片重排。

### 4. 旁白

- 按场景拆段，每段 1–3 句；逐段合成、逐段测长。
- 每段保留 lead/tail 静音；整条做一次响度标准化。
- 输出 `timeline.json`：字段定义见 [`doubao-tts`](../doubao-tts/SKILL.md) 的“时间轴接口”，这里不重复。
- 语速先 `0`，宣传片常用 `-10..-5`；改语速必须重测。
- 合成、测长、补静音与响度标准化的命令在 [`doubao-tts`](../doubao-tts/SKILL.md)；场景边界与录制算法见 [`references/timeline-and-render.md`](references/timeline-and-render.md)。

**禁止**把 API Key 写进脚本、HTML、时间轴或提交记录；只从环境变量读。

### 5. HTML 动画

- 一个固定舞台，例如 `1080×1920`；用 `transform: scale()` 适配浏览器窗口，不改内部坐标。
- 手机适配：`scale = min(innerWidth / 1080, innerHeight / 1920)`，剩余区域用同色背景，不要裁掉内容。
- 场景容器只做透明度交叉淡化；场景内部动画用局部时间，避免全局时间互相耦合。
- 多阶段场景（输入 → 卡片 → 汇报）单独记 phase mark，按音频时长算，不写死绝对值。
- 提供截图/录制入口：`?capture` 隐藏 HUD 并停在 `t=0`，`?capture&t=<秒>` 停在指定时刻；两种模式都不自动播放，录制脚本必须显式 `window.__promo.play()`。`window.__promo` 暴露 `duration/seek/play/pause/time/playing`。
- 单文件交付时把图片 base64 内嵌；开发版保留 `assets/` 方便替换。

### 6. 录制与合成

- Playwright 以目标尺寸录制，例如 `1080×1920`，25/30fps。
- 录制会拖慢 `requestAnimationFrame`；时间轴不要用“每帧固定加 0.05 秒”的写法，否则成片会比音频慢。按真实时间差推进，或放宽 dt 上限。
- 录完按预滚的实测终点裁掉加载期，再与旁白 mux；视频时长以旁白总长为准。
- 输出 H.264 + AAC、`yuv420p`、`+faststart`；手机平台优先 1080 宽。
- 具体命令见 [`references/timeline-and-render.md`](references/timeline-and-render.md)。

### 7. 封面与交付

- 封面独立做 9:16 与 3:4 两版；标题公式与版式见 [`promo-stills`](../promo-stills/SKILL.md)。
- 交付：MP4、9:16 封面、3:4 封面、旁白 MP3、SRT、交互 HTML、可编辑 HTML、素材目录。
- SRT 从 `timeline.json` 生成，命令见 [`references/timeline-and-render.md`](references/timeline-and-render.md) 的“字幕 SRT”。
- 文件名带比例与用途，例如 `xxx-1080x1920.mp4`、`xxx-cover-9x16.png`。

## 时间轴契约

不要手写一堆散落的时间常量。先算出一个 `TL`，所有场景、字幕和 phase 都引用它：

```js
const TL = {
  s1: { start: 0, end: 8.958 },
  s2: { start: 8.958, end: 18.796 },
  s3: { start: 18.796, end: 27.246 },
  s4: { start: 27.246, end: 49.806, b: 6.918, c: 15.708 },
  s5: { start: 49.806, end: 59.096 },
  s6: { start: 59.096, end: 66.914 },
}
const DURATION = 66.914
```

- `b` / `c` 是 S4 内部的局部偏移，不是全局时间。
- 交叉淡化 0.45 秒；旁白在场景开始后 `lead` 秒进入。
- 末屏不参与淡出，保证最后一帧是品牌。
- 时间轴由音频实测值生成，不靠“看起来差不多”。

## 验收

完整清单见 [`references/qa.md`](references/qa.md)。最低限度：

- [ ] 1080×1920 与 390×844 都能读；关键文字不小于约 13–15 CSS px。
- [ ] 图片全部加载，`pageerror` 为空。
- [ ] 每个场景的旁白与画面动作对得上；无累积漂移。
- [ ] 音轨有声音、无削波、无长黑场；最后一帧是品牌。
- [ ] 旁白与画面文字不矛盾；封面标题与视频主张一致。
- [ ] 交付文件名/比例/用途一一对应。

## 边界

- 不伪造产品界面、用户数据或运行结果；展示用 seed 数据可以，但要脱敏并标注为演示数据。
- 不为“真实感”把不可读的整张截图硬塞进手机屏；真实感与可读性分工。
- 不把横版视频简单加黑边当竖屏。
- 不在仓库里提交 .dev 下的临时截图、录屏、密钥或个人路径。
- 付费 API 只在用户明确要求时调用；凭据只走环境变量。

## 参考

- [`references/copy-and-storyboard.md`](references/copy-and-storyboard.md)：分镜模板、口播写法、封面标题。
- [`references/timeline-and-render.md`](references/timeline-and-render.md)：时间轴、录制与 mux；TTS 测长与补静音的命令归 `doubao-tts`。
- [`references/qa.md`](references/qa.md)：帧检查、移动端、音频、交付验收。
