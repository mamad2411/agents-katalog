---
name: cross-platform-webview-ui
description: 深色/浅色主题下 DeepSeek Harness for VS Code 原生工作台 webview 前端的跨平台（Windows / macOS）样式与功能一致性规范。当修改 media/chat.css、media/chat-responsive.css、src/webview/chat/*.ts、src/webview/composer-configuration/*.ts 或 src/ui/workbench-view-provider.ts 中的 UI 元素、弹层、滑杆、字体、布局、交互，或排查“Windows 上表现和 macOS 不一致 / 窄屏出问题 / 弹层不显示 / 拖动卡顿 / 字体忽大忽小”时使用本技能。
whenToUse: 修改工作台 webview 的 UI/CSS/交互、新增 DOM 元素或弹层、调整字体/间距/响应式布局、处理 Windows/macOS 样式或功能不一致、处理窄侧边栏布局、打包前做 UI 回归时。
metadata:
  author: skymecode
  appliesTo: deepseek-harness-for-vscode
---

# 跨平台工作台 UI 规范（Windows / macOS）

本仓库的“工作台”是一个原生 VS Code webview（不是官方 Web UI）。UI 全部由
本仓库自己的 HTML/CSS/TS 渲染，因此**每个跨平台差异都必须由我们自己兜住**。
这套规范把已知的坑、架构约束和验证流程固化下来，改 UI 前先读。

## 1. 架构与文件职责

    src/ui/workbench-view-provider.ts        工作台 HTML 模板 + 消息桥（唯一模板来源）
    media/chat.css                           组件样式（主题 token、气泡、工具卡、配置面板、弹层…）
    media/chat-responsive.css                视口适配（窄侧边栏），必须在 chat.css 之后加载
    src/webview/chat/*.ts                    webview 逻辑（main 入口 / context 元素表 / app 渲染 /
                                             messages 消息 / sessions 历史与权限 / images 图片 /
                                             composer-configuration 模型-推理-预设 / timeline…）
    src/domain/*.ts                          纯领域投影（无 DOM），跨端逻辑放这里并单测
    src/webview/localization.ts              webview 文案（ENGLISH_WEBVIEW_MESSAGES）
    l10n/bundle.l10n.zh-cn.json              扩展宿主文案 + webview 中文文案

- HTML 模板只有一份（workbench-view-provider 的 html()），webview JS 从
  dist/webview/chat.js 加载；CSS 通过 asWebviewUri 直接引用 media/*.css。
- 样式拆分是有意的：chat.css 管“组件本身长什么样”，chat-responsive.css 管
  “视口多窄时怎么收缩”。新 UI 的响应式规则优先放 chat-responsive.css，测试
  test/responsive-layout.test.ts 会校验两者加载顺序。
- 断点：chat.css 里 720/360/320/260px；chat-responsive.css 里 680/360px。

## 2. 铁律（改 UI 前必读）

1. 颜色一律用 VS Code 主题 token（--vscode-foreground、
   --vscode-editorWidget-background、--vscode-widget-border、--vscode-focusBorder、
   --vscode-list-activeSelectionBackground 等），不要写死 hex（个别品牌色如
   provider 紫色可例外并注明）。这样深色/浅色/高对比三套主题自动适配。
2. 字号用相对单位：正文用 calc(var(--vscode-font-size) + Npx)，卡片/辅助文字
   用固定小字号（11px 级），标题用 em。不要整页写死 px 字号，否则 Windows 上
   改了 VS Code 字体设置会忽大忽小。
3. **图标一律用内联 SVG**（src/webview/icons.ts 的 icon()/applyIcon()），禁止在
   UI 里放任何 emoji 或 emoji 呈现字符（⚡⚙⚠⚑⚐★✦✎☑❯ 等：Windows 用
   Segoe UI Emoji 会把它们渲染成彩色 emoji，macOS 却是单色文本——典型跨平台
   不一致）。SVG 用 currentColor 继承主题色；HTML 模板里用 ${icon('name')}，
   动态节点用 applyIcon(el, icon('name'))。纯文本安全符号（✓ ✕ × ← → 箭头、
   几何形状 ◆◇△ 等）可保留。:root 已加 font-variant-emoji:text 兜底，消息正文
   覆盖回 normal 以保留真实 emoji 内容。新增图标先看 icons.ts 有没有，没有再补。
4. 每个 byId 的 DOM id 必须同时存在于 HTML 模板。webview 在模块加载时就用
   byId() 取元素，缺一个就抛 Missing webview element #xxx，整个 webview 白屏
   （曾因 composer-hint 只加了 class 没加 id 导致工作台一直“启动中”）。新增
   元素时：模板 + context.ts 的 elements 一起改，然后重新构建并核对。
4. 弹层不要放在会被 overflow:hidden 裁剪的容器里。绝对定位弹层只要祖先有
   overflow:hidden（或 auto/scroll）就会整块被裁掉。正确姿势：
   - 优先把弹层做成 .composer-shell（position:relative; overflow:visible）
     的直接子元素，如 command-menu / file-mention-menu；
   - 若必须在裁剪容器内（如权限弹层在 composer-tools 里），用 JS 打开时按锚点
     getBoundingClientRect() 设 position:fixed 的内联样式定位，关闭时清空内联
     样式（参考 src/webview/chat/sessions.ts 的 anchorPermissionOverlay）。
5. 原生控件拖拽要 preventDefault。<input type=range> 这类原生控件在 Windows
   Edge 上拖动会连续触发 input 事件风暴；如果还要自定义平滑视觉，按下时
   event.preventDefault() 关掉原生拖拽，自己用 pointer 事件驱动视觉 + 轻量更新
   状态，松手再提交（参考 composer-configuration 的 beginEffortDrag /
   syncEffortDrag）。指针交互统一用 pointerdown/move/up/cancel，不要 mouse/touch 混搭。
6. 带空格的绝对路径过不了插件 spec 校验：normalizePluginSpec 拒绝任何空白/shell
   元字符（Windows 上 dsh 用 shell 转发 pnpm）。macOS 的 globalStorage 在
   Application Support（含空格），所以“把文件拷进 harness-home 再用绝对路径
   pnpm add”行不通——需要相对路径 + 把 dsh 的 cwd 切到 profile 目录
   （参考 plugin-manager.installVendored）。
7. webview 文案双端齐全：新增 vscode.l10n.t 宿主文案或 webview 文案时，同时补
   l10n/bundle.l10n.zh-cn.json；test/localization.test.ts 会强制校验 zh 缺失即红。

## 3. 已知跨平台陷阱（每个都是修过的真 bug）

| 症状 | 根因 | 修复模式 |
|---|---|---|
| 窄侧边栏权限/确认弹层点了不出现，拉宽就出现 | composer-tools 在 ≤680px 切 overflow:hidden，弹层向上弹出被裁 | 打开时 JS + position:fixed 锚定（anchorPermissionOverlay） |
| Windows 上推理滑杆拖动卡顿/一顿一顿 | 原生 range 拖拽的 input 事件风暴触发整面板重渲染 | pointerdown preventDefault + 自定义拖拽轻量同步 + 松手提交一次 |
| 工作台永远“启动中”、webview 白屏 | 模块加载时 byId 找不到 HTML 里的元素（id 只加了 class） | 模板与 context.ts 元素表保持同步 |
| 窄屏工具按钮把输入框撑破 / 横向溢出 | 单行工具条放不下 | chat-responsive.css 用 overflow:hidden + flex-shrink + min-width:0；弹层另用 fixed 逃逸 |
| 弹层被 z-index 盖住 | 叠放层级混乱 | 新弹层用 z-index 20–30（菜单/弹层 20/22/23/24/26，设置/插件面板 fixed 24/30，大图 1000），参考现有清单 |
| 字体在 Windows 上看起来更小/更挤 | 用了固定 px 字号 | 正文 calc(--vscode-font-size + 1px)、行高 1.7、卡片 11px |
| 弹层宽度超过视口 | width 用死 220px | 用 min(220px, calc(100vw - 16px))，并在 JS 里 clamp left |
| 对话框换行 / 文案截断 | 没设 overflow-wrap | 文本容器 overflow-wrap:anywhere + min-width:0 |

## 4. 功能一致性要求（Windows 与 macOS 必须行为一致）

- 输入区：发送、Shift+Enter 换行、@ 文件、图片粘贴/预览、队列、模型配置面板
  （模型/DSH 模式/推理/来源）、权限选择、时间线、历史/搜索/归档恢复。
- 弹层类：command-menu、file-mention-menu、permission-popup/confirm、
  configuration-panel、settings/plugin 全屏面板——在 260px 极窄到宽屏都必须能
  打开、在视口内、可键盘 Escape/点击外部关闭。
- 推理滑杆：拖动/点击轨道/滚轮/键盘方向键四种输入方式全部可用，拖动时旋钮跟手、
  无全量重渲染。
- 流式渲染：增量更新保留展开状态与滚动位置；窄屏弹层不被裁剪。
- 权限/安全：danger-full-access 必须弹确认；权限投影缺失时选项目录仍可用。
- 键盘：Cmd/Ctrl+Alt+H 快捷键、Escape 关闭、焦点可见（focus-visible）、aria 属性齐全。
- 减少动态效果：尊重 prefers-reduced-motion（动画降级）。

## 5. 开发与验证流程

    npm run check-types          # tsc --noEmit
    npx vitest run               # 289 个测试（含 localization / responsive-layout）
    node esbuild.mjs             # 重建 dist/extension.cjs + dist/webview/chat.js
    npm run package              # 全量：类型 + 测试 + 生产构建 + vsce 打包

改 UI 后必须在 Windows 和 macOS 各验证一遍（至少覆盖）：

1. 最窄侧边栏（约 260–300px）打开工作台：所有弹层能弹出且不被裁剪。
2. 推理滑杆：鼠标拖动全程跟手、点击轨道跳档、滚轮、键盘方向键。
3. 深色/浅色/高对比主题下颜色与对比度正常（不写死 hex 的检查）。
4. 工作台第一次打开不出现 Missing webview element / 卡“启动中”。
5. 新文案在中文界面有翻译。
6. VS Code 字体设置为 12px / 14px 时布局不崩、字号按比例缩放。
7. 新用户路径：激活不阻塞、默认插件本地秒装、加载界面立即出现。

## 6. 快速迭代技巧（本仓库开发模式）

- 想立即在已安装的 0.5.6 上验证 webview 改动：改完跑 node esbuild.mjs，把
  dist/webview/chat.js（或 extension.cjs）拷进
  ~/.vscode/extensions/skymecode.deepseek-harness-for-vscode-0.5.6/dist/，
  重载 VS Code 窗口即可，不必重装 VSIX。
- CSS（media/*.css）是静态文件，改完直接拷进已安装扩展的 media/ 再重载。
- 打包发布走 .github/workflows/release.yml（push v* tag 自动构建 4 平台并发布
  GitHub Release）；同版本重发要删旧 Release + force 移动 tag，建议直接升版本号。
