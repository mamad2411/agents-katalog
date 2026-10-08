---
name: nonogram-ui
description: Nonogram 前端 UI、响应式布局与棋盘交互。用于修改 src/components/**、src/App.jsx、src/main.jsx、src/index.css、src/App.css、tailwind.config.js、src/i18n/**，以及棋盘鼠标/触摸/测量/悬停提示、桌面/移动布局、可访问性与视觉一致性。
---

# Nonogram UI

## 职责范围

- `src/components/**` 与 `src/App.jsx` / `src/main.jsx`：布局、面板、弹窗、棋盘渲染与交互（SidePanel 已拆 Header/EditToolbar/UserArea/GameControls/ViewSettings/ImportExport/Footer；AuthModal 拆 Login/Register/Forgot + authFields；IntroModal 内置语言选择）。
- `src/i18n/**`：前端多语言（zh / zh-Hant / en / ja）。
- `src/index.css` / `src/App.css` / `tailwind.config.js`：Tailwind 样式与视觉系统。
- UI 相关的交互常量（cellSize 范围、brush 模式等）在 `src/constants.js`，修改需同时看 nonogram-core 的约束。

## 交互红线

- 棋盘格子必须保留 `data-cell` / `data-r` / `data-c` 属性，E2E 测试依赖它们定位。
- 关键控件保留稳定 `data-testid`（面板标题/登录按钮/随机/计时/复盘 GIF/自动求解等），与 nonogram-e2e 的定位约定一致。
- 触摸事件在 `Board.jsx` 用原生监听，`touchmove` 需要非 passive 才能阻止滚动；改动手势时不要引入页面滚动/缩放冲突。
- hover 使用 rAF 节流；拖拽/画笔批次在结束时 flush 成一条 moveHistory（与 nonogram-core 语义一致）。
- Ctrl 测量、滚轮缩放（MIN_CELL_SIZE=12 / MAX_CELL_SIZE=80）、fit-to-width 是既有交互，不要破坏。
- 切换模式（play/edit）、面板 pin/hover、抽屉开合是核心 UX，改动后必须跑移动端视口检查。

## 布局与可访问性

- 桌面：左侧面板 + 棋盘（`md:flex-row`）；移动：顶部栏 + 全屏抽屉 + 底部导航。
- 移动端底部导航不得遮挡内容；面板/drawer 打开时棋盘仍可操作或明确不可操作。
- 所有用户可见文案必须走 `useI18n` / `translate`，禁止硬编码中英文。新增语言 = 新文件 + LANGS + messages + HTML_LANG + TITLES。
- 当前棋盘格子是 div，没有键盘格级导航与 ARIA；涉及可访问性改动时补齐 role/tabIndex/焦点管理，不要假装已支持。
- 目前只有浅色主题；若加入深色主题，需在 nonogram-e2e 中补两套主题与对比度检查。

## 视觉协作（截图后必须用 Claude Vision 检查）

- UI 改动影响布局/视觉时：用 `nonogram-e2e` 的视口矩阵截图，然后必须调用 `claude-vision-skill` 检查截图：
  `node <claude-vision-skill 目录>/vision.js "<png>" "<问题>"`（目录通常为 `~/.codex/skills/claude-vision-skill`）。
- 不要自己“看”图、不要声称看不了图片、不要用 DOM 断言代替视觉检查；vision.js 的文字输出是视觉结论的来源。
- 临时调试浏览器行为用 `webapp-testing`（通用 Playwright 工具包），不要新装视觉工具。
- 保持视觉一致性：颜色取自既有色板/常量，新增样式先确认是否必要。

## 验证

- `npm run lint` + `npm run build`；涉及布局/交互跑 `npm run test:e2e`（含 1440x900 与移动端 420x800 检查）。
- 涉及视觉：按 nonogram-e2e 的视口矩阵截图 → claude-vision 检查 → 修复后重跑。
