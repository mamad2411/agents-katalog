---
name: wechat-article-remotion
description: 用 Remotion 把任意一篇微信公众号文章（mp.weixin.qq.com）转成 Studio 风格的视频：暖白画布 + 上下镜像透视格子 + 顶部章节进度 + 底部无底色黑字字幕 + 公众号原文图完整保留（object-fit: contain 永不裁切）。6 个场景类型（cover/list/stat/compare/outro + article-image），与 talking-head-remotion 共用字体和 SFX 公共素材库。当用户要转一篇公众号文章、把公众号链接变成可发布的视频、或复刻任意一篇微信文章为 Remotion 工程时，必须使用这个 skill。
---

# WeChat Article Remotion

把任意一篇微信公众号文章转成 Studio 风格的 Remotion 视频。主舞台给足空间给图片和文字，**完全没有 PIP**。

## 视觉核心

- 暖白画布 `#f7f8f3` + 上下镜像透视格子背景
- 顶部黑色章节进度条（白色填充）
- 底部无底色黑字字幕，关键词蓝色 `#2f6fff` 强调
- 默认画幅 **1080×1920 @ 30fps 竖屏**（适配公众号图文、抖音/小红书/视频号）
- **公众号图片永远 `object-fit: contain`，永不裁切**（铁律）

与 [talking-head-remotion](../talking-head-remotion/SKILL.md) 的差异：

| 维度 | talking-head-remotion | wechat-article-remotion |
|---|---|---|
| 场景 | 5（cover/list/stat/compare/outro） | 6（+ article-image） |
| PIP | 右下圆形 206px | **无** |
| 视觉调性 | Studio 暖白 | Studio 暖白（一致） |
| 公共素材库 | 字体/SFX/动效组件 | **完全共用** |

## 输入要求

- **公众号文章 URL（必填）**：`https://mp.weixin.qq.com/s/xxx`
- TTS 配音、字幕可选；脚本与音频按需由 pipeline 生成

## 新项目：先跑脚手架

```bash
python3 skills/wechat-article-remotion/scripts/scaffold_wechat_article_project.py \
  --project-dir ./demo-wx-article \
  --title "示例公众号文章" \
  --article-url "https://mp.weixin.qq.com/s/xxxxx"

cd demo-wx-article
npm install
npm run still
```

脚手架自动从 [talking-head-remotion 公共素材库](../talking-head-remotion/assets/library/) 播种字体（Noto Sans SC / Space Grotesk）和 SFX。

## 端到端 pipeline

```text
用户：https://mp.weixin.qq.com/s/xxx
   │
   ▼
[1] scripts/fetch_article.py
    · ideaflow API → markdown
    · 提取 ![](url) + 下载原文图到 public/assets/article-images/img-NN.jpg
    · PIL 读每张图 WxH → imageAspect
    · 写 work/source/article.md 和 work/source/images.json
   │
   ▼
[2] 运行时 LLM 拆稿（在本会话里执行）
    · 按 references/beat-checklist.md 拆 6-12 个 scene
    · 输出 scenes[]、captions[]、chapters[] 到 src/demoData.ts
   │
   ▼
[3] TTS 配音（统一入口 `scripts/generate_tts.py`）
    · 默认探测 minimax 凭据（`../.env` 的 `minimaxi=` + `minimaxi-group-id=`）
        - 有 → 用 MiniMax T2A v2（`speech-02-hd`，hex 解码 `data.audio`）
        - 无 → 自动降级到 edge-tts（Microsoft 神经语音，**免费 / 无需 key**）
    · 显式指定：`--engine minimax` 或 `--engine edge-tts`
    · Windows 下避免依赖 audio-to-subtitles 的 `npx -y bun`（FileNotFoundError）
    · 必须 ffprobe 验证每段 mp3 能解码 + 量时长，否则杂音
    · 产物归档路径（两个引擎输出格式完全一致）：
        - public/assets/audio/voice.m4a     # 最终 AAC，Remotion 用
        - public/assets/audio/voice.mp3     # 备用
        - work/captions/segments.json       # 每段时长 + 累计起点 + engine 元信息
        - work/audio/tts-segments/seg-NN.mp3  # 临时分段
        - work/source/narration.md          # TTS 专用稿（每段一段）
    · 详细用法见脚本 docstring 和 [scripts/README.md](scripts/README.md)
   │
   ▼
[4] 用真实音频时长回写 demoData.ts 的 captions time
   │
   ▼
[5] npm run typecheck / still / render:preview
   │
   ▼
[6] Subagent 独立视觉审核
    · 每场景抽"开始 0.3s"和"中段"两帧
    · 重点：图片 contain 不裁切、关键词不先于字幕、每场景元素数 ≤ 5
   │
   ▼
[7] 询问用户是否需要最终 1080p 渲染（可选）
    · 展示 preview 结果：时长、质量、内容覆盖情况
    · 只有用户明确确认后才跑 `npm run render`
    · 如果用户满意 preview，无需跑最终版
```

## 7 个场景类型

| kind | 用途 | 数据关键字段 |
|---|---|---|
| `cover` | 开头标题 | `eyebrow, titleLines, subtitle` |
| `list` | 步骤、要点、清单 | `eyebrow, heading, items[]` |
| `stat` | 数据、金句 | `eyebrow, number, unit, title, metrics[]` |
| `compare` | 对比、选 A/B | `eyebrow, heading, choices[]` |
| `outro` | 结尾 CTA | `eyebrow, title, subtitle` |
| **`article-image`** | **公众号原文图完整展示（单图）** | `eyebrow, imageSrc, imageAspect, title, caption?, source?` |
| **`article-image-stack`** | **多图布局：row/column/carousel** | `eyebrow, title, layout, images[], slideSeconds?, transition?, source?` |

详见 [references/scene-types.md](references/scene-types.md)。

## 不能妥协的硬规则

1. **公众号图片永远 `object-fit: contain`**，永不裁切 —— Code Review 看到 `object-fit: cover` 用在 article image 上即 fail。
2. **每屏 ≤ 5 个文字元素 + 至少一个非文字视觉主体**（沿用 talking-head-remotion 硬规则）。`article-image` 场景的非文字主体就是那张图。
3. **逐元素进场**：`article-image` 场景里图片 / 标题 / 解读 / 图源各有 `appearAt`，错开 0.18s 进场。
4. **数据驱动**：`demoData.ts` 是唯一真相，component 内不写死画面。
5. **音画强同步**：用「前 1s / 后 0.5s 双帧」抽帧审计，关键词不能先于字幕。
6. **图文映射规则**（★★★ 曾因搞反导致图文错位 bug）：
   - **公众号文章的常见结构是「一段介绍 + 一张配图」，图片属于其前面紧邻的段落，不是后面的。** 牢记这个结构，避免把图配到下一个章节。
   - `fetch_article.py` 已实现向上扫描：先找图片说明行（如 `👇🏼韶关南雄珠玑古巷`），再找所属正文段落
   - `images.json` 新增 `context` 字段：当 `caption` 是图片说明行时，`context` 存储所属正文段落全文
   - 写 `demoData.ts` 前必须先 `ls public/assets/article-images/` 看实际下载了多少张
   - 必须读 `work/source/article.md` 把每张图映射到所属章节：
     - 在 `article.md` 中找到每个 `![...](url)` 的位置
     - 该图片属于其**前一个**非空正文段落（向上找，不是向下）
     - `images.json` 的 `caption` / `context` 字段可作为辅助参考，但最终以 `article.md` 中的实际位置为准
   - **图文不是必须一一对应**：某段文字在原文没配图，视频里就不要硬配图，用 `list` / `stat` 等非图片场景展示
   - **某段有多张图就用轮播**（`article-image-stack` 的 `carousel` 布局），不要只挑 1 张代表
   - **尽可能保留正文有用的图片**——内容图、景观图、细节图都该用上；判定为无用（二维码 / 分割线装饰 / 重复 / 模糊缩略图）才能丢，且必须向用户说明丢了几张、为什么
   - 单图场景停留 ≤ 6s；多图轮播间隔 1.5-3s（更短观感眼花）
7. **共用 talking-head-remotion 公共素材库** —— 字体/SFX 用 `seed_from_library()` 复制，新动效回流到 `talking-head-remotion/assets/library/animations/`。
8. **国际化（i18n）先不处理**，按 user_profile 偏好默认中文。

## 常用命令

```bash
npm install
npm run typecheck         # tsc --noEmit
npm run still             # 渲 1 帧静态图（校对场景布局）
npm run render:preview    # 低清 proof（先出这个）
npm run render            # 正式 1080p
```

## 渲染调试节奏

- 默认先出低清 proof（`npm run render:preview`），不要一上来跑 1920×1080 全片。
- preview 完成后，**必须先向用户展示结果，询问是否需要最终版**，得到确认后才跑 `npm run render`。禁止自动推进到最终渲染。
- 长渲染把输出重定向到 `work/render.log`，只 tail 日志尾部。
- 用户打断后先检查后台进程：`pgrep -fl "remotion|chrome-headless|Google Chrome for Testing|Chromium"`。
- 不要用模糊的 CLI 探测命令（如 `remotion render --help`），优先看 `package.json` 里已有脚本或官方文档。

## 相关 references

- [references/visual-guide.md](references/visual-guide.md) —— 视觉规范、动效词汇表、抽帧检查清单
- [references/scene-types.md](references/scene-types.md) —— 6 个场景的详细数据模型和动效配方
- [references/beat-checklist.md](references/beat-checklist.md) —— 拆稿 beat checklist 模板
