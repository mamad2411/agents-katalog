---
name: math-curve-loading-reference
description: "参考方案 | 基于 Paidax01/math-curve-loaders 选择、改造和验收数学曲线 Loading 动效。用于 Paws 或其他 Web/App 的首屏 loading、启动占位、等待状态、粒子轨迹、Lissajous/玫瑰线/摆线等动效设计，以及排查 SVG SMIL、WebView 和 Safari 兼容问题。触发词：loading 效果、加载动画、首屏动效、启动页、loader、数学曲线、粒子轨迹、Lissajous。"
---

# Math Curve Loading Reference

把 [Paidax01/math-curve-loaders](https://github.com/Paidax01/math-curve-loaders) 作为数学曲线 loading 的首选灵感库。先选曲线和运动语言，再按目标运行环境重新实现并验证；不要默认复制上游代码。

## 使用流程

1. 明确 loading 所在阶段：HTML 首屏、React 挂载后、原生启动页、局部异步操作或长任务等待。
2. 浏览上游 [在线画廊](https://paidax01.github.io/math-curve-loaders/) 或仓库，按品牌气质和等待时长选择曲线。
3. 阅读 [source-catalog.md](references/source-catalog.md)，了解可选曲线、参数和抽象模型。
4. 如果目标包含 WebView、Safari、HTML 首屏或跨端 App，必须再读 [paws-compatibility.md](references/paws-compatibility.md)。
5. 用目标项目现有主题、生命周期和无障碍机制重新实现。
6. 在真实目标渲染器中冻结 loading 状态，检查静态布局、连续运动、降级路径和应用接管。

## 选型原则

- 短等待优先单一、低频、易识别的轨迹；长等待可以使用更丰富的曲线，但避免制造进度已知的错觉。
- 品牌感来自曲线、节奏、粒子密度和主题色，不要依赖“加载中”文案弥补普通 spinner。
- 首屏动效必须先有正确静态帧，再增强为动画。动画 API 失败时不能退化成脱轨孤点、空白或布局跳动。
- 粒子拖尾通常由同一参数曲线上的相位偏移产生；用半径和透明度衰减表达方向，不需要额外位图资产。
- 主题颜色取自目标项目的语义 token。首屏早于框架挂载时，应从持久化设置和系统偏好完成最小主题引导。
- 支持 `prefers-reduced-motion`。减少动态时保留可理解的静态轨迹或简化标记，不强制播放粒子运动。

## 实现边界

- 跨 WebView/Safari 的默认实现使用静态 SVG 几何节点加 `requestAnimationFrame` 更新属性，或使用目标框架已验证的动画库。
- 不把 SVG SMIL (`animateMotion`, `mpath`) 或 SVG 引用链 (`use`, `href`) 作为关键首屏路径的唯一实现。
- 动画启动前直接输出所有粒子的静态 `cx/cy`，确保 JavaScript、RAF 或路径长度 API 失败时仍然成立。
- 框架接管后立即停止 RAF 并隐藏/移除占位，避免后台循环和双层 UI。
- HTML 注入器必须幂等，找不到挂载锚点时明确失败，不静默生成损坏页面。

## 验收门槛

- 粒子数量符合设计，初始坐标不是全部相同，所有粒子位于预期轨迹附近。
- 至少间隔 500-700 ms 读取一次坐标，确认头粒子移动且拖尾仍保持分布。
- 阻断主应用 bundle 后，loading 仍正确显示；放行后，应用挂载且 loading 隐藏，RAF 停止。
- 检查深浅主题、至少一个非默认主题和 `prefers-reduced-motion`。
- 在实际目标 WebView/Safari/移动端浏览器截图，不以桌面 Chromium 单一结果代替跨端验收。
- 对用户可见改动保留同尺寸 Before/After 证据；动效结构回归还应有 DOM/运行时断言。

## 来源与许可

- 参考源固定到上游提交 `70f4e00a6d452532039ff7c2ccb4c379ec90c772`（2026-04-04）。
- 上游仓库在采集时未声明许可证。可参考公开展示的数学公式、交互思路和视觉方向；不要直接复制源码、样式或资产到可发布项目，除非后续确认了授权。
- Paws 的可复用实现位于 `packages/happy-app/sources/scripts/injectWebLoading.ts`，演进记录见 PR [#327](https://github.com/wangjs-jacky/happy/pull/327)、[#328](https://github.com/wangjs-jacky/happy/pull/328) 和 [#330](https://github.com/wangjs-jacky/happy/pull/330)。
