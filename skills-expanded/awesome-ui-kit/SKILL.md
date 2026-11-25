---
name: awesome-ui-kit
description: >
  Use when building AI-native Web interfaces, AI chat applications, RAG search result pages,
  DeepSeek R1/OpenAI o1 reasoning viewers, Agent tool invocation monitors, split-pane Canvas/Artifacts,
  or modernizing existing pages with self-contained Web Components.
  Guides the agent to select and copy standard, zero-blackbox single-file components and the shared icon system from
  the awesome-ui repository (React/Vue/Vanilla) instead of reinventing UI primitives.
---

# Awesome UI Kit (AI 原生前端页面装配规范)

## 🎯 核心使命 (Mission)
使用 `awesome-ui` 标准组件库快速装配现代 AI 页面。禁止 AI 从零手写易出错的流式渲染、思维链折叠、自动跟底或工具调用状态卡片。必须直接引用或复用 `awesome-ui` 中经过验证的原子单文件组件。

---

## ⚡ 触发场景 (When to Trigger)
当用户提出以下需求时触发本 Skill：
- 开发类似 ChatGPT / Claude / Perplexity / v0 的 AI 网页或聊天对话界面
- 需要展示 DeepSeek R1 / OpenAI o1 思维链（Thinking / Reasoning）过程
- 需要展示 Agent 工具调用过程（Tool Calls / Function Calling Traces）
- 需要展示 RAG / AI 搜索来源引文（Sources & Citations）
- 需要实现分屏实时预览沙盒（Artifacts / Canvas）
- 用户明确提及 "使用 awesome-ui" 或 "帮我写个 AI 页面"

---

## 🎨 组件与图标优先级 (Component & Icon Priority)
1. 先检索 `awesome-ui/react/`、`awesome-ui/vue/` 或 `awesome-ui/vanilla/`，复用现成单文件组件。
2. 所有界面图标优先使用对应技术栈的 `UiIcon`：`react/UiIcon.tsx`、`vue/UiIcon.vue`、`vanilla/UiIcon.js`。
3. React 命名图标从 `react/UiIcon.tsx` 导入，例如 `Sparkles`、`Check`、`X`、`ChevronRight`；Vue 使用 `<UiIcon name="sparkles" />`；Vanilla 使用 `uiIcon('sparkles')`。
4. 禁止用 emoji、Unicode 字符（如 `✓`、`▶`、`✕`）或临时手写 SVG 代替 UI 图标。
5. **项目品牌 Logo 规范（开源通用原则）**：
   - 页面装配需要品牌 Logo / 产品标识时，**优先检索并使用当前项目自身的 Logo 资产**（按优先级检索 `public/logo.*`、`public/favicon.*`、`src/assets/logo.*`、`assets/brand/` 或用户显式传入的品牌图）。
   - 本 Skill 为面向全网的通用开源规范，**严禁硬编码任何特定组织或个人的私有 Logo / 专属 CDN 链接**。
   - 若当前项目尚未定义自有 Logo，优先使用产品名称文本配合 `UiIcon` 通用几何图形（如 `Sparkles`、`Bot`）作为中性占位，并预留标准的外部配置属性（如 `logoUrl`）或插槽（`<slot name="logo">`）。
6. 只有仓库没有匹配图标时，才允许引入外部开源图标库；新增依赖前必须说明原因和许可证。

## 🛠️ 标准装配执行工作流 (Standard Workflow)

### 第一步：确认技术栈 (Stack Selection)
根据用户当前项目环境选择对应源码目录：
- **React / Next.js / Vite** ➔ 使用 `awesome-ui/react/*.tsx`
- **Vue 3 / Nuxt / Vite** ➔ 使用 `awesome-ui/vue/*.vue`
- **原生 HTML / Web Components** ➔ 使用 `awesome-ui/vanilla/*.js`

### 第二步：场景装配配方 (Choose Page Recipe)

#### 配方 A：经典 AI 助手 / 对话流 (Standard AI Chatbot)
- 顶部/主区：`StreamMarkdown` + `ThinkingBlock` + `ToolCallBadge` + `MessageActionToolbar`
- 底部：`AutoScrollAnchor` + `PromptChips` + `ChatPromptInput`

#### 配方 B：Perplexity 风格深度搜索 / RAG 问答 (RAG & Search)
- 顶部：`SourcesCitation`（展示引文来源网格）
- 中部：`ThinkingBlock` + `StreamMarkdown`（带引用角标跳转）
- 底部：`PromptChips` + `ChatPromptInput`

#### 配方 C：Claude Artifacts / v0 即时预览画布 (Generative Canvas)
- 左侧（主对话流）：配方 A 对话区
- 右侧（预览面板）：`ArtifactCanvas`（支持 Code 源码模式与 iframe 沙盒渲染一键切换）

#### 配方 D：Agent 自动化执行与调用流 (Agent Task Console)
- 流程列表：多个 `ToolCallBadge`（实时展示 running/success/error 状态及参数返回值抽屉）
- 节点状态：`StatusIndicator` + `ThemeToggle`
- 实时日志：`StreamMarkdown`

#### 配方 E：存量 SSR / PHP / Go / 静态 HTML 渐进式增强 (In-Place Modernization)
- 引入 `<script type="module" src=".../vanilla/<component>.js"></script>`
- 在现有模板中直接使用对应 Web Component（如 `<chat-prompt-input>`、`<theme-toggle>`、`<status-indicator>`），零打包构建侵入。

---

## 📋 组件检索与 Props 规范

| 组件 | 对应单文件路径 | 核心扁平 Props |
|---|---|---|
| **`UiIcon`** | `<stack>/UiIcon.*` | React: `name`, `size`, `strokeWidth`; Vue: `name`, `size`, `strokeWidth`; Vanilla: `uiIcon(name, options)` |
| **`ChatPromptInput`** | `<stack>/ChatPromptInput.*` | `value`, `onChange`, `onSubmit`, `onStop`, `isGenerating`, `allowAttachments`, `attachments` |
| **`StreamMarkdown`** | `<stack>/StreamMarkdown.*` | `content`, `isStreaming` |
| **`ThinkingBlock`** | `<stack>/ThinkingBlock.*` | `content`, `isThinking`, `durationSeconds`, `defaultExpanded` |
| **`ToolCallBadge`** | `<stack>/ToolCallBadge.*` | `name`, `status ('running'\|'success'\|'error')`, `args`, `output`, `error` |
| **`SourcesCitation`** | `<stack>/SourcesCitation.*` | `sources: [{ title, url, snippet, siteName }]` |
| **`AutoScrollAnchor`** | `<stack>/AutoScrollAnchor.*` | `isStreaming` |
| **`ArtifactCanvas`** | `<stack>/ArtifactCanvas.*` | `title`, `code`, `language`, `isOpen`, `onClose` |
| **`MessageActionToolbar`**| `<stack>/MessageActionToolbar.*`| `content`, `role`, `onRetry`, `onFeedback`, `branchIndex`, `totalBranches`, `onBranchChange` |
| **`PromptChips`** | `<stack>/PromptChips.*` | `suggestions: string[]`, `onSelect` |
| **`FluidContourBackdrop`** | `<stack>/FluidContourBackdrop.*` | WebGL 等高线流体背景：`speed`, `interactive`, `inkColor`, `paperColor` |
| **`SpotlightGlareCard`** | `<stack>/SpotlightGlareCard.*` | 3D 光标镜面高光反射卡片：`glareOpacity`, `glareRadius`, `enableTilt`, `maxTilt` |
| **`AnimatedCounter`** | `<stack>/AnimatedCounter.*` | 平滑缓动指标计数器：`target`, `start`, `duration`, `delay`, `prefix`, `suffix` |
| **`PointerRipples`** | `<stack>/PointerRipples.*` | WebGL 多彩流体鼠标涟漪背景，光标跟随彩虹拖尾与 3D 漫反射：`curl`, `splatRadius`, `idleMs`, `opacity` |
| **`LiquidGlass`** | `<stack>/LiquidGlass.*` | Apple 液体玻璃材质容器：`variant ('capsule'\|'card'\|'sidebar')`, `intensity ('light'\|'regular'\|'thick')`, `interactive`, `enableTilt`, `maxTilt`, `glareOpacity` |

---

## 🚫 禁忌事项 (Anti-Patterns)
1. **严禁重新造轮子**：不要在用户代码里手写 `textarea` 的高度自适应或重新写一段包含 Bug 的 Markdown 流式打字逻辑，直接复制对应单文件。
2. **严禁引入复杂第三方重黑盒库**：不随意引入需要复杂 Context Provider 包裹的重量级组件库。
3. **保持 Tailwind 纯洁度**：各组件均基于标准 Tailwind CSS 工具类，尽量通过外部 `className` 传递覆盖，不要破坏组件内部的原子结构。
4. **严禁硬编码私有品牌资产**：装配页面、顶部导航栏或侧边栏时，禁止擅自注入未被当前工程声明的外部个人 Logo、特定站点专属静态链接或作者个人头像；必须优先探测目标工程已有资产，或通过插槽/中性几何图标占位。
