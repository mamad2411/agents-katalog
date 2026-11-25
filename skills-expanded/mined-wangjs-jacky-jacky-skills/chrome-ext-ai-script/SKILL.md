---
name: chrome-ext-ai-script
description: "📖 参考方案 | AI 驱动的 Chrome Extension 架构方案：Plasmo + Vercel AI SDK，侧边栏对话生成并执行页面脚本。此为蒸馏产物，供开发时参考查阅。触发词：Chrome 扩展参考、AI 脚本方案、Plasmo 参考、侧边栏脚本方案"
---

# AI 驱动的 Chrome Extension — 项目参考方案

> 📖 **蒸馏产物** — 本文件是从开源项目蒸馏提炼的参考方案，不是可执行的 skill。
> 供开发同类项目时参考查阅，包含完整的架构设计、功能模块说明和代码参考。

> 从 [zhuweileo/Monkey](https://github.com/zhuweileo/Monkey) 蒸馏提炼，提供可复用的架构模式和实现参考。

---

## 一、项目定位

**浏览器侧边栏里的 AI 助手** — 用户用自然语言描述需求，AI 感知当前页面结构，生成脚本并直接在页面上执行。

### 核心亮点

| 亮点 | 说明 |
|------|------|
| **看到就能改** | AI 感知当前页面的真实 DOM 结构，生成的脚本精准匹配页面元素 |
| **说了就生效** | 对话完成后代码直接在页面执行，无需复制粘贴 |
| **一键配置可用** | 填入 API Key → 测试连通性 → 确认 Key 有效 → 立即开始使用 |
| **多服务商自由切换** | OpenAI / Claude / Gemini 等随时切换，插件式扩展 |

### 典型使用场景

| 用户说 | 效果 |
|--------|------|
| "把页面右侧的广告栏隐藏掉" | AI 根据真实 DOM 找到广告容器并隐藏 |
| "帮我把这个表单自动填上测试数据" | AI 识别表单字段并填入数据 |
| "提取这个页面所有商品价格" | AI 生成脚本抓取价格信息并展示 |
| "这个按钮太丑了，帮我换个样式" | AI 修改目标元素的 CSS |
| "帮我监控这个页面的价格变化" | AI 生成定时检查脚本 |
| "提取这个页面的所有联系方式" | AI 扫描页面结构，抓取邮箱/电话等信息 |

---

## 二、功能模块总览

```
┌──────────────────────────────────────────────────────────────┐
│                    Chrome Extension 架构                      │
│                                                              │
│  ┌───────────────────┐                                       │
│  │   侧边栏 SidePanel │  ← 用户主界面                         │
│  │                   │                                       │
│  │  ┌─────────────┐  │                                       │
│  │  │  对话界面    │  │  · 流式消息渲染                        │
│  │  │  (ChatView) │  │  · 图片输入支持                        │
│  │  └─────────────┘  │  · 多轮对话上下文                      │
│  │  ┌─────────────┐  │                                       │
│  │  │  代码预览    │  │  · 自动检测 AI 生成的脚本               │
│  │  │ (CodePreview)│ │  · 一键在页面中执行                     │
│  │  └─────────────┘  │                                       │
│  └─────────┬─────────┘                                       │
│            │                                                 │
│  ┌─────────┴─────────┐   ┌─────────────────┐                │
│  │  设置面板 Options  │   │  后台服务 SW     │                │
│  │                   │   │                 │                │
│  │  · 服务商选择      │   │  · 消息路由      │                │
│  │  · API Key 配置   │   │  · Tab 管理      │                │
│  │  · 连通性测试 ✓    │   │  · 生命周期      │                │
│  │  · 模型选择        │   │  (不做 AI 调用)  │                │
│  └─────────┬─────────┘   └────────┬────────┘                │
│            │                      │                          │
│  ┌─────────┴──────────────────────┴──────────────────┐      │
│  │                 AI 服务层                           │      │
│  │                                                    │      │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │      │
│  │  │ Provider │ │ Provider │ │ Provider │ ...       │      │
│  │  │ 注册中心  │ │ OpenAI   │ │ Claude   │           │      │
│  │  │ (插件式)  │ │          │ │          │           │      │
│  │  └──────────┘ └──────────┘ └──────────┘           │      │
│  │                                                    │      │
│  │  · Prompt 构建（注入真实 DOM 快照 → 防幻觉）        │      │
│  │  · 流式调用（Vercel AI SDK 统一接口）               │      │
│  └────────────────────┬───────────────────────────────┘      │
│                       │                                      │
│  ┌────────────────────┴───────────────────────────────┐      │
│  │                 页面交互层                           │      │
│  │                                                    │      │
│  │  · Content Script → DOM 快照提取                    │      │
│  │    - 交互元素（input/button/select）                │      │
│  │    - ID 元素（精准定位）                             │      │
│  │    - 页面正文（Turndown → Markdown）                │      │
│  │    - 标题/地标（页面结构概览）                       │      │
│  │                                                    │      │
│  │  · world:MAIN 注入 → 在页面全局作用域执行代码        │      │
│  └────────────────────┬───────────────────────────────┘      │
│                       │                                      │
│                       ▼                                      │
│  ┌────────────────────────────────────────────────────┐      │
│  │          目标网页（用户正在浏览的页面）               │      │
│  └────────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

### 核心数据流

```
用户输入："把这个页面的广告隐藏掉"
     │
     ▼
① 提取页面信息
   Content Script 扫描当前 Tab：
   · 交互元素 → 选择器信息
   · ID 元素 → 精准定位依据
   · 页面正文 → Turndown 转 Markdown
   · 标题/地标 → 页面结构概览
     │
     ▼
② 构建 AI Prompt
   System Prompt = 角色定义 + 真实 DOM 快照 + 页面正文
   （AI 看到真实的元素 ID 和 class，不会编造）
     │
     ▼
③ 流式调用 AI
   Vercel AI SDK → 自动选对应服务商的 SSE 格式
   侧边栏实时显示回复（一个字一个字出来）
     │
     ▼
④ 检测代码块
   AI 回复包含 ==UserScript== 代码块
   → 展示代码预览 + "在页面执行"按钮
     │
     ▼
⑤ 用户点击执行
   chrome.scripting.executeScript({ world: 'MAIN' })
   代码在目标页面全局作用域运行
   → 广告消失，用户直接看到效果
```

---

## 三、模块功能详解

### 3.1 侧边栏模块（SidePanel）

侧边栏是用户的主操作界面，核心是**对话式交互**：

| 功能 | 说明 |
|------|------|
| 流式对话界面 | 支持文本输入和图片上传，AI 回复一个字一个字显示 |
| 多轮对话上下文 | AI 能理解之前的对话历史，持续优化脚本 |
| 代码预览组件 | 自动检测 AI 生成的 `==UserScript==` 代码块并展示 |
| 一键执行 | 点击按钮，代码直接在当前页面执行 |
| 页面感知 | 每次调用 AI 前自动提取当前页面的 DOM 快照 |

### 3.2 设置面板（Options）

设置面板是用户首次使用的入口，核心是**让用户确认 API Key 可用**：

```
选择服务商 → 填入 API Key → 选择模型 → 点击"测试连接"
                                           │
                                      实际调用一次 API
                                           │
                                ┌──────────┴──────────┐
                                │                     │
                           ✓ 连接成功              ✗ 连接失败
                         （显示延迟）     （Key无效/网络错误/频率限制）
                                │                     │
                                │              429 也算成功 ✓
                                │         （频率限制，但 Key 有效）
                                │
                           保存设置 → 进入侧边栏
```

设计要点：
- **429 也算成功**：频率限制说明 Key 有效，显示"(频率限制，但 Key 有效)"
- **切换不丢失**：服务商之间切换时，内存缓存保存各家的输入内容
- **首安装引导**：扩展安装后自动打开设置页

### 3.3 AI 服务层

| 功能 | 说明 |
|------|------|
| Provider 注册中心 | 插件式架构，新增服务商只需写一个 Provider 文件并注册 |
| DOM 感知 Prompt | 每次调用前注入真实 DOM 快照到 System Prompt，防止 AI 编造选择器 |
| 流式调用 | Vercel AI SDK 统一处理各服务商的 SSE 格式差异 |
| 多模态支持 | 支持文本 + 图片输入 |

### 3.4 页面交互层

| 功能 | 说明 |
|------|------|
| DOM 快照提取 | Content Script 提取交互元素、ID、标题、正文等结构信息 |
| world:MAIN 注入 | 绕过 CSP 限制，在页面全局作用域执行代码 |
| Turndown 转换 | HTML → Markdown，给 AI 精简的页面结构 |
| Readability 提取 | 提取页面正文（去广告、去导航） |

---

## 四、关键设计决策

| 问题 | 解决方案 | 参考 |
|------|---------|------|
| CSP 绕过 | `world:'MAIN'` + 间接 eval `(0,eval)(src)` | `references/architecture-decisions.md` |
| MV3 SW 超时 | AI 调用放 SidePanel，SW 只做消息路由 | `references/architecture-decisions.md` |
| AI 幻觉选择器 | 每次调用前注入真实 DOM 快照到 System Prompt | `references/dom-snapshot.md` |
| 多服务商适配 | Provider 注册中心模式，统一接口 | `references/ai-provider-registry.md` |
| Tab 定位问题 | 使用 `lastFocusedWindow` 而非 `currentWindow` | `references/architecture-decisions.md` |

---

## 五、技术栈

| 维度 | 选择 | 选择理由 |
|------|------|---------|
| 扩展框架 | **Plasmo** | HMR + 自动 manifest + React+TS 开箱即用 |
| AI SDK | **Vercel AI SDK** | useChat hook 直连 React，自动兼容各服务商 SSE |
| 页面感知 | **Turndown + Readability** | 轻量纯浏览器端，HTML→Markdown 成熟 |
| 样式 | **Tailwind CSS** | 原子化，快速迭代 |
| 包管理 | **pnpm** | 速度快、磁盘小 |

---

## 六、从 Monkey 蒸馏的能力映射

| Monkey 原有能力 | 处理方式 | 理由 |
|----------------|---------|------|
| DOM 快照提取 | **保留** | 核心能力，让 AI 看到真实页面 |
| world:MAIN 注入 | **保留** | 核心能力，绕过 CSP 执行代码 |
| System Prompt 构建 | **保留** | 核心能力，注入 DOM 防幻觉 |
| SSE 流式解析（手写） | **用 AI SDK 替代** | SDK 自动处理各服务商差异 |
| 多服务商存储 | **改造** | 从硬编码改为 Provider 注册模式 |
| 脚本持久化自动注入 | **去除** | 新项目不需要 |
| URL glob 匹配 | **去除** | 新项目不需要 |
| 脚本管理 CRUD | **去除** | 新项目不需要 |
| 设计令牌 tokens.css | **用 Tailwind 替代** | 更灵活 |

---

## 七、项目目录结构（参考）

```
src/
├── background/index.ts          # Service Worker（消息路由 + 存储）
├── contents/dom-snapshot.ts     # Content Script（DOM 快照提取）
├── sidepanel/                   # 侧边栏主界面
│   ├── ChatView.tsx             # 对话界面
│   ├── CodePreview.tsx          # 代码预览组件
│   ├── providers/               # AI 服务商配置
│   └── hooks/                   # AI 对话和 DOM 快照 hooks
├── lib/                         # 核心库
│   ├── ai/                      # AI 能力层
│   │   ├── providers/           # 各服务商适配器
│   │   ├── provider-registry.ts # 插件化注册中心
│   │   └── prompt-builder.ts    # System Prompt 构建
│   ├── dom/                     # 页面感知层
│   │   ├── extractor.ts         # 轻量选择器提取
│   │   └── snapshot.ts          # 页面快照
│   ├── injection/               # 代码执行层
│   └── storage/                 # 存储层
└── package.json
```

---

## 八、快速启动

```bash
# 1. 创建项目
pnpm create plasmo script-copilot
cd script-copilot

# 2. 安装核心依赖
pnpm add ai @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google
pnpm add turndown @mozilla/readability
pnpm add -D @types/turndown

# 3. 启动开发
pnpm dev
```

---

## References

详细实现代码和设计决策见 `references/` 目录：

| 文件 | 内容 |
|------|------|
| `references/architecture-decisions.md` | 关键架构决策（CSP 绕过、MV3 超时、Tab 定位等） |
| `references/dom-snapshot.md` | DOM 快照提取器代码 + Turndown/Readability 整合 |
| `references/world-main-injection.md` | world:MAIN 脚本注入代码 |
| `references/ai-provider-registry.md` | Provider 注册中心代码 |
| `references/streaming-chat.md` | 流式对话实现（Vercel AI SDK）+ Prompt 模板构建 |
| `references/tech-stack-setup.md` | 技术栈选型理由 + 初始化命令 |
