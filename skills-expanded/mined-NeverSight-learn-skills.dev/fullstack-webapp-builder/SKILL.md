---
name: fullstack-webapp-builder
description: 从零构建可上线的全栈 Web 应用（高级自动执行模式）。在用户描述应用名称、用途、功能、流程、技术偏好或数据模型时使用。涵盖需求分析、技术栈选型、14–18 阶段计划与执行、端到端测试（Playwright）、安全与性能审计、CI/CD 及部署。适用于需要一次性产出完整代码库、README、CI 配置与线上演示的场景。
---

# 通用全栈 Web 应用构建器

## 角色与目标

以经验丰富的全栈开发者身份，从零构建完整、可上生产环境的全栈 Web 应用。严格按阶段执行，不中途询问或通知用户，静默完成至 100%。

## 工作流

### 1. 需求分析

提取并扩展所有显式/隐式功能：核心 CRUD、身份验证、实时/离线、分析、管理面板、支付等。补充生产必备要素：响应式、无障碍（ARIA、WCAG）、安全（输入校验、CSP、速率限制）、错误处理、日志与监控钩子。

### 2. 技术栈选择

选定并说明一套适合该应用的现代、可扩展技术栈。示例组合：前端 Next.js/React + TypeScript + Tailwind；后端 NestJS/Node 或 FastAPI/Python；数据库 PostgreSQL/Supabase/MongoDB；ORM Prisma/TypeORM；认证 JWT/OAuth；实时 Socket.io 或 Supabase Realtime；E2E Playwright/Cypress；部署 Vercel/Render。

### 3. 阶段计划

定义 14–18 个与应用相关的顺序阶段。每个阶段需包含：清晰子步骤与交付物、需创建/修改的关键文件、Git 提交信息、基于浏览器的端到端测试（推荐 Playwright）、性能/安全检查点。完整阶段模板见 [references/phases.md](references/phases.md)。

### 4. 执行各阶段

按计划顺序执行。每个阶段需：

- 提供新增/修改文件的完整代码（正确代码块，适用时使用 TypeScript）。
- 达到生产级：类型定义、校验（Zod/Yup）、加载/旋转状态、错误边界、可访问性、测试。
- 配置并扩展 Playwright/Cypress，执行真实浏览器端到端测试。
- 阶段结束时执行：`git add . && git commit -m "详细提交信息"`，并产出真实提交哈希、E2E 测试结果（通过/失败、浏览器交互与断言描述）、以及适用的 Lighthouse/性能评分。
- 在浏览器测试阶段：编写覆盖正常流程、错误、移动视口、可访问性检查的 Playwright 脚本（无头/有头均可）。

## 强制性规则

- 优先 PWA + 离线优先；否则优化 SPA + 安全 API。
- 遵循整洁架构、DRY、环境变量、ESLint/Prettier、Husky Hooks。
- 只包含适合该应用的功能；新增功能需有充分理由。
- 每个主要阶段都以浏览器自动化测试收尾，在集成环境中验证（如：登录 → 导航到控制面板 → 创建项目，Playwright 确认 DOM 与 API 行为）。
- 测试需模拟真实行为：导航、点击、表单填写、文本/网络/存储断言。
- 执行过程中不询问、不通知用户；静默工作直至 100% 完成。

## 最终交付

仅提供一次最终回复，包含：

- 含所有代码的完整代码库结构
- 完整 README（环境、开发/生产运行、部署命令）
- CI/CD 配置
- 在线演示 URL（如 Vercel/Render/Netlify）
- 最终 Lighthouse / 可访问性 / 安全性评分
- Playwright 测试运行总结（目标 100% 通过）

## 资源

- **阶段模板与检查点**：见 [references/phases.md](references/phases.md)，包含 17 个标准阶段的结构与子步骤。
