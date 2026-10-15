---
name: prd-prototype
description: 从 PRD 文档生成交互式原型。**当用户需要根据 PRD 生成可交互的 UI 原型、多页面跳转演示、或快速验证产品设计时必须使用此技能**。触发场景：用户说"生成原型"、"做个 demo 看看"、"生成可跳转的原型"、"把 PRD 变成可点击的页面"。
---

# PRD 原型生成技能

## ⚡ 快速开始

**何时使用**：
- PRD 文档已完成，需要生成可交互的原型进行演示
- 需要快速验证产品设计和页面流程
- 开发前需要可视化原型供团队评审
- 用户上传了 PRD 文档并要求生成原型

**使用方式**：
```
/prd-prototype  # 启动原型生成流程
```

## 📚 核心资源导航

| 资源 | 用途 | 何时读取 |
|------|------|----------|
| `commands/generate.md` | 原型生成详细流程 | 执行 generate 命令时 |
| `commands/preview.md` | 原型预览和导出流程 | 执行 preview 命令时 |
| `templates/html_tailwind.html` | HTML+Tailwind 模板（默认） | 生成 Tailwind 原型时 |
| `templates/html_tailwind_zhongcheng.html` | HTML+Tailwind 模板（众诚 UI） | 生成 Tailwind 原型且应用众诚 UI 规范时 |
| `templates/react_shadcn.html` | React+shadcn/ui 模板 | 生成 React 原型时 |
| `templates/vue_element.html` | Vue+Element Plus 模板 | 生成 Vue 原型时 |
| `templates/native_html.html` | 原生 HTML/CSS 模板 | 生成原生原型时 |
| `ui-presets/zhongcheng-ui.json` | 众诚 UI 规范配置 | 用户选择应用 UI 规范时 |
| `scripts/page_analyzer.js` | 页面分析脚本 | 需要从 PRD 提取页面列表时 |
| `scripts/router_generator.js` | 路由生成脚本 | 需要生成页面跳转逻辑时 |
| `scripts/link_checker.js` | 链接检查脚本 | 生成完成后检查和修复链接路径 |

## 🎯 核心功能

### generate 命令

**功能**：从 PRD 文档生成交互式原型

**支持的技术栈**：
| 技术栈 | 适用场景 | 输出 |
|--------|----------|------|
| **HTML + Tailwind** | 快速原型、轻量演示 | 多个 HTML 文件 + Tailwind CDN |
| **React + shadcn/ui** | 现代化 Web 应用原型 | React 组件 + 路由 |
| **Vue + Element Plus** | 企业级后台原型 | Vue 组件 + Element Plus |
| **原生 HTML/CSS** | 无依赖、兼容性要求高 | 纯静态文件 |

**生成的目录结构**：
```
项目名称-prototype/
├── index.html              # 首页/登录页
├── dashboard.html          # 仪表盘
├── pages/                  # 功能页面
│   ├── user-management.html
│   ├── order-list.html
│   └── ...
├── components/             # 可复用组件（React/Vue 模式）
├── styles/                 # 样式文件
├── ui-config/              # UI 配置文件（如应用 UI 规范）
├── router.js               # 路由配置
└── README.md               # 原型说明
```

**执行流程**：
1. 读取 PRD 文档（main_prd.md + modules/）
2. 分析功能模块和业务流程
3. 生成页面列表和跳转关系
4. 选择技术栈（HTML+Tailwind、React+shadcn、Vue+Element、原生 HTML）
5. 选择 UI 规范（可选）：众诚 UI 规范 / 不使用
6. 逐页生成原型内容（应用选定的 UI 规范）
7. 生成路由和导航
8. 检查和修复链接路径（确保跨目录跳转正确）← 新增
9. 确认完成并提示预览

### preview 命令

**功能**：预览和导出生成的原型

**执行流程**：
1. 检查原型目录是否存在
2. 在浏览器中打开原型首页
3. 提供导出选项（ZIP 打包等）

## 📋 PRD 页面映射规则

从 PRD 文档中提取页面信息：

| PRD 内容 | 映射为 |
|----------|--------|
| 功能模块清单 | 主要页面列表 |
| 业务流程图 | 页面跳转关系 |
| 用户角色 | 权限控制和导航菜单 |
| 详细功能需求 | 页面元素和交互 |
| 用户故事 | 页面操作和反馈 |

## ⚠️ 重要原则

1. **先分析后生成**：先完整读取 PRD，分析页面结构，再生成原型
2. **保持页面可跳转**：所有页面必须有导航，支持返回和跳转
3. **技术栈一致性**：整个原型使用同一技术栈，不混用
4. **响应式设计**：生成的原型支持桌面和移动端视图
5. **UI 规范可选**：用户可选择应用众诚 UI 规范或使用默认样式

## 🔗 与其他技能的协作

- **前置依赖**：需要先有 PRD 文档（由 `/prd-suite` 生成）
- **后续流程**：原型确认后可进入开发阶段

## 🎨 UI 规范支持

### 众诚 UI 规范（可选）

基于实验室考试系统设计系统的 UI 规范，包含：

**设计规范**：
- 颜色体系：品牌色 (#246FE5)、中性色板、功能色板
- 字体规范：6 级字阶、字重规范
- 间距规则：4px 倍数、预设间距
- 布局规范：顶部导航 47px、侧边栏 216px、页签 44px

**组件规范**：
- 按钮：4 级按钮体系、尺寸规范
- 表格：表头 37px、行高 47px
- 弹窗：头部 56px、底部 56px、圆角 8px
- 卡片：padding 24px、圆角 12px

**何时推荐使用**：
- 需要与企业级设计系统保持一致
- 中后台管理系统原型
- 需要遵循统一设计规范的项目

**配置文件**：`ui-presets/zhongcheng-ui.json`

## 📖 详细流程

完整工作流程请参考：
- [commands/generate.md](commands/generate.md) - 原型生成详细流程（含 UI 规范选择）
- [commands/preview.md](commands/preview.md) - 原型预览和导出
- [tech-stack.md](../document/docs/prd-prototype/tech-stack.md) - 技术栈和 UI 规范说明

---

*最后更新：2026-03-20 (增加 pages 内跳转链接修复)*
