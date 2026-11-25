---
name: kubai-duotone
description: 生成风格统一的双色面性功能图标：16 网格的实心图标，浅色主体加主色点缀，所有颜色由一个主色推导，悬停时播放表现图标含义的动效，也可导出静态 SVG。新建、完成、删除、AI、关闭等变体用统一的角标生成。用户要求面性、实心、填充、双色、duotone 或 bulk 图标，界面中 16–48px 的功能图标，或向这套双色图标添加新图标时使用。
license: Kubai Icons License (source-available). Complete terms in LICENSE.
metadata:
  version: "2.0.0"
  display_name: "Kubai 双色图标"
  display_name_en: "Kubai Duotone Icons"
  description_zh: "按统一风格绘制双色面性功能图标：16 网格，浅色主体加主色点缀，悬停时播放表现图标含义的动效，可导出静态 SVG。"
  description_en: "Draws two-tone solid functional icons in one consistent style: a 16 grid, light bodies with accents in the brand colour, hover motion that acts out each icon, and static SVG export."
---

# Kubai 双色图标

本 skill 包含双色面性风格的完整实现：规则、几何工具、范例、悬停动效、自检和导出。你的任务是按规则编写新图标，不要改写几何或渲染代码。

## 文件

- `GUIDE.md`：全部规则，均为硬性要求。开始前通读。
- `kit.mjs`：几何与渲染，包括平滑圆角、圆角矩形、胶囊、带凸起的主体、关键形状、角标和辅色推导。直接使用，不要修改。
- `icons.mjs`：范例，多为功能图标，包括带角标和关闭斜线的变体。新图标按相同格式追加。
- `motions.mjs`：各范例的悬停动效（`GUIDE.md` 第 11 节）。
- `motion.mjs`：动效运行代码，无依赖，可直接用于页面。
- `check.mjs`：自检。生成各尺寸截图、参考线对位图和 1 倍屏 16px 图，测量关键形状、主色占比、颜色数量、间距、遮挡、小部件尺寸、内嵌部件边距，以及动效是否超出画布，结果写入 `findings.md`。
- `export.mjs`：导出独立 SVG，可更换品牌色，辅色自动推导。
- `chrome.mjs`：自检和导出共用的无头 Chrome 工具。
- `CHANGELOG.md`：历次修改的问题和改法。遇到类似问题先查阅此文件。

## 流程

1. 通读 `GUIDE.md`。
2. 确定交付形式。用户未说明时先询问：
   - 静态：独立的 `.svg` 文件，可用于任何场合。用户提到"切图""SVG 文件""放进 Figma""在 App 中使用"等，即为静态。
   - 带悬停动效：SVG 加 `motion.mjs`，在网页中运行。
3. 确定工作位置：
   - 新建一套：将 `kit.mjs`、`icons.mjs`、`motion.mjs`、`motions.mjs`、`check.mjs`、`export.mjs`、`chrome.mjs` 复制到目标位置，在副本中工作，保留各文件开头的版权声明。`GUIDE.md`、`SKILL.md` 和 `CHANGELOG.md` 只保留在 skill 中，不复制（见 `LICENSE` 第 3 条）。
   - 向已有的一套添加：直接在其 `icons.mjs` 和 `motions.mjs` 中追加。
4. 按 `GUIDE.md` 绘制：为每个功能确定物体（第 1 节），选定关键形状（第 2 节），先阅读结构最接近的范例（第 8 节）。同一物体的新建、完成、删除、AI、关闭等变体用角标表示（第 12 节），不另画物体。
5. 运行自检（第 9 节），清空 Findings，再按清单检查截图。有动效的图标，在 22px 下确认停留姿态清晰可辨（第 11 节）。
6. 导出（第 10 节），并告知用户所用的主色和辅色。

```bash
node check.mjs --only 新图标A,新图标B --with folder,lock,calendar
node export.mjs --only 新图标A,新图标B --size 24 --out 目标目录
node export.mjs --primary #0EA5E9 --out 目标目录
```

## 环境

- Node 18 及以上，以及 Chrome。可用环境变量 `CHROME` 指定浏览器路径。
- 所有检查在无头模式下运行，不打开可见窗口，也不影响用户正在使用的浏览器。

---

Copyright (c) 2026 Kubai087. Licensed under the Kubai Icons License; see LICENSE.
