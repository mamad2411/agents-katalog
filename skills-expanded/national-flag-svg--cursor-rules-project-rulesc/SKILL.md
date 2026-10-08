---
description: Rough Emoji Draw 项目通用开发规范，覆盖目录职责、TypeScript、Canvas 绘制、Rough.js 依赖、HTML 示例与 Rslib 构建验证。
alwaysApply: true
---

# Rough Emoji Draw 项目规则

## 项目定位

- 当前项目是一个基于 TypeScript、DOM Canvas、Rough.js npm 依赖与 Rslib 的轻量前端绘图库，核心目标是把 emoji / 国旗绘制成手写风格画布内容。
- 优先遵循现有单入口结构和命名风格，避免为了小功能引入框架、运行时状态库或复杂目录拆分。
- 输出产物面向浏览器全局变量 `window.RoughEmoji`，修改公开 API 时必须同时考虑 `rough-emoji.html` 和 `flag-qa.html` 的调用方式。

## 当前目录

- 项目根目录是 `/Users/shuaxin/Documents/draw`，所有读写、生成和命令执行默认以此目录为工作区。
- `.cursor/rules/`：Cursor 项目规则目录，规则文件使用 `.mdc`。
- `src/rough-emoji.ts`：核心源码入口，集中声明类型、全局 API、Canvas 上下文切换、旗帜识别、手写模板绘制和像素采样降级逻辑。
- `rslib.config.ts`：Rslib 库构建配置，当前入口为 `./src/rough-emoji.ts`，输出浏览器 `iife` bundle。
- `rough-emoji.html`：交互演示页，依赖 `dist/rough-emoji.js` 中打包后的绘制逻辑。
- `flag-qa.html`：批量 QA 页面，用于检查不同国家/地区旗帜绘制效果。
- `dist/`、`node_modules/` 和缓存目录属于生成或依赖内容，除非用户明确要求，不要把它们作为源码维护对象。

## TypeScript 规范

- 新增或修改函数、接口、具名类型和对外 API 时补充明确类型；不要用 `any` 逃避建模，确需接受外部输入时优先用 `unknown` 并在入口收窄。
- 保持现有 JSDoc 风格：类型、常量和函数前用简短中文注释说明语义、输入输出或绘制意图，避免解释表面赋值。
- Canvas 与 Rough.js 相关类型集中放在 `src/types.ts`，只声明当前实际使用的最小方法集，不为了完整覆盖第三方库而扩大类型面。
- 坐标和尺寸计算优先使用 `size` 派生比例，避免散落无语义魔法数字；新增固定比例、颜色、偏移量时提取为具名常量或在局部写清用途。

## 绘制与数据流

- 绘制函数应尽量保持确定性：相同 flag、canvas 尺寸和输入状态应得到一致结构的结果。
- 所有直接读写 Canvas、DOM、`window`、下载链接或全局上下文的逻辑都要集中在明确入口或具名辅助函数中。
- `withCanvas` 负责临时切换全局绘制上下文；新增多画布场景时必须恢复旧上下文，避免 QA 页面串画布。
- 已有手写模板优先用专门函数表达；未知或未覆盖旗帜继续走现有 emoji 栅格化 / 像素采样降级路径。
- 修改国旗识别、地区码转换或 fallback 行为时，要同时考虑普通输入、国家中文名、emoji、多字符异常输入和空输入。

## HTML 与前端体验

- HTML 示例页保持无框架、可直接打开的结构；页面只加载 `dist/rough-emoji.js`，Rough.js 由源码 import 后随构建产物打包。
- 表单、按钮、状态文本和画布容器需要保持基本可访问性：语义标签、可读 `aria-label`、键盘提交和响应式宽度。
- 新增样式优先沿用当前纸张色、边框色、深绿色按钮和响应式网格风格，不引入不一致的视觉系统。
- QA 页面用于视觉回归检查；大批量渲染时注意性能，不要在循环中制造不必要的全局状态泄漏。

## Rslib 与构建

- 修改入口、输出格式、全局暴露方式、依赖打包或资源处理时，先确认 `rslib.config.ts` 与 HTML 页面引用路径仍一致。
- 当前项目使用 `pnpm`（`pnpm-lock.yaml`）与 Node.js 20+；新增依赖必须通过 `pnpm add` 安装，避免手写版本号。
- 不要提交无关格式化、缓存、临时脚本或一次性调试文件。

## 验证与交付

- 修改 TypeScript 或构建配置后优先运行 `pnpm run typecheck`；影响产物或 HTML 引用时运行 `pnpm run build`。
- 修改绘制行为后，用 `pnpm run dev` 启动本地静态服务，通过 `http://localhost:3000/flag-qa.html` 检查批量旗帜效果（勿用 `file://` 打开）。
- 交付前使用 `ReadLints` 检查本次修改过的文件；如果无法运行某项验证，需要在回复中说明。
