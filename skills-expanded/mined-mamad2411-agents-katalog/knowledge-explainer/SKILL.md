---
name: knowledge-explainer-skill
description: 把 markdown / 笔记类文档自动生成讲解动画视频，Remotion 渲染、本地跑、不依赖云 API。by nyx研究所 (GitHub @znyupup · B站/小红书 @nyx研究所)
version: 0.2.0
type: video-generation
tags: [video-generation, remotion, knowledge-explainer, animation, agent]
author: nyx研究所 (https://github.com/znyupup)
status: stable
---

# knowledge-explainer-skill

**Author:** nyx研究所 · [GitHub](https://github.com/znyupup) · [B站 @nyx研究所](https://space.bilibili.com/4330525) · 小红书 @nyx研究所 · [X @znyupup_music](https://x.com/znyupup_music)

> Skill 元信息文件 — 给 AI agent 读取使用

## 触发场景

当用户:
- 想把一份文档变成视频
- 提到"讲解动画"、"知识科普视频"、"科普讲解"
- 给你一份 markdown / Word / 笔记类内容,问能不能做成视频
- 提到"用 Remotion 做视频"

## 工作流程

1. **读取用户文档**
   - 路径通常在 `~/Downloads/`,文件可能是 `.md` / `.txt` / 复制黏贴的内容
   - 如果不是 markdown,先转换成 markdown

2. **生成 script.md**
   - 参考 [examples/script.md](examples/script.md) 的格式
   - 每个章节 `## 模板名`,选择合适的内置模板
   - 每页给一个 `duration`(秒)
   - 复杂可视化(几何图、电路图等)用 `## CustomXxx` 段名

3. **检查模板**
   - 内置: Title / ContentCard / TwoColumn / Triangle / BeforeAfter / Outro(都是排版类)
   - **真正的能力在 custom/** — 任何内置模板做不出来的(物理仿真、数据可视化、特效转场)主动写 jsx
     - 文件名 = script.md 里的段名(`## CustomFunFact` → `custom/CustomFunFact.jsx`)
     - 参考 [custom/_TEMPLATE.jsx.example](custom/_TEMPLATE.jsx.example)
     - 已有的 showcase 优先抄(范式覆盖广):
       - [`custom/DoublePendulum.jsx`](custom/DoublePendulum.jsx) — 物理仿真(微分方程数值积分)
       - [`custom/PaperFold.jsx`](custom/PaperFold.jsx) — 指数 / log scale 数据可视化
       - [`custom/AlgorithmBubble.jsx`](custom/AlgorithmBubble.jsx) — 离散状态机 + 时间轴脚本编排
     - 用 Remotion API: useCurrentFrame / useVideoConfig / interpolate / spring / useMemo

4. **跑渲染**
   ```
   node cli.js script.md out/video.mp4
   ```

5. **检查输出**
   - 看时长是否符合预期
   - 看渲染日志有无错误
   - 用 `open out/video.mp4` 让用户自己看

## 内置模板速查

| 模板 | 关键参数 | 适用场景 |
|---|---|---|
| `Title` | `title, subtitle` | 章节开头 |
| `ContentCard` | `title, items[], color` | 知识点列表 / 步骤拆解 |
| `TwoColumn` | `title, left[], right[], callout` | 输入→输出对比 |
| `Triangle` | `base, height, formula, result` | 三角形几何题 |
| `BeforeAfter` | `title, before, after, unit, viz` | **数值/时长前后对比**(波形条 / 时间轴削减,动画) |
| `Outro` | `title, cta` | 收尾 / CTA |

`BeforeAfter` 的 `viz`:
- `bars` — 两组波形条柱对比(适合数值类:音量、得分、占比)
- `duration` — 横条对比 + 削掉的碎片飞出(适合时长类:剪辑前后、加载耗时)

## Custom 模板生成原则

- 每个 custom 文件 export 一个跟文件同名的 React component
- 用 Remotion API 写动画(**不要**用 setTimeout / setInterval / requestAnimationFrame — Remotion 是逐帧渲染,所有状态都从 frame 推导)
- 字号:标签 14, 正文 22, 标题 28-44, 大字 60+
- 颜色:bg #0a0a0f, 主色 #6c5ce7 / #00cec9, 文字 #fff,辅助色 #fdcb6e #fd79a8 #e17055 #74b9ff
- 出现节奏:先静(0-22f)再入场,避免一次全出
- 复杂仿真用 `useMemo(() => simulate(...), [deps])` 一次预计算所有帧,逐帧索引 — 见 DoublePendulum.jsx
- 离散状态机用"时间轴脚本"模式 — 在组件外预生成"每帧的 state 数组",逐帧索引 — 见 AlgorithmBubble.jsx
- 数据可视化优先 SVG(轻、清晰、好控制),CSS 用于动效层

## 选择策略 — 排版 vs 自定义

**用内置排版(快、不卡):**
- 知识点列表 / 步骤拆解 → ContentCard
- 输入对输出 → TwoColumn
- 数值/时长前后对比 → BeforeAfter
- 几何题 → Triangle

**写 custom(真生动):**
- 物理过程(运动、振动、碰撞)→ 抄 DoublePendulum 范式
- 时间线 / 量级对比(指数、对数)→ 抄 PaperFold 范式
- 算法流程 / 状态变化 / 信息流→ 抄 AlgorithmBubble 范式
- 化学反应、生物过程、电路、流程图、地图… → 必写 custom

**关键判断**:如果你的内容会让观众想看"它怎么动的",就要 custom,内置排版做不出"动"的感觉。

## 推荐用户动作

```bash
# 1. 装 skill
git clone https://github.com/znyupup/knowledge-explainer-skill
cd knowledge-explainer-skill
npm install

# 2. 写文稿(或让 agent 写)
vim examples/my_topic.md

# 3. 跑 skill
node cli.js examples/my_topic.md out/my_topic.mp4

# 4. 看
open out/my_topic.mp4
```
