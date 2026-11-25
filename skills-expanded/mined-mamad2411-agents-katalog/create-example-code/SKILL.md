---
name: create-example-code
description: This skill should be used when the user asks to "create example code", "create demo project", "add feature to demo", "create sample code", "build example project", or requests to implement/extend ZEGO SDK demo functionality with specific interactions or features.
version: 2.0.0
---

# ZEGO 示例代码创建技能

引导用户逐步创建 ZEGO 产品示例代码项目，或为已存在的 demo 添加新功能。

## 🎯 执行原则

**[CRITICAL] 严格按步骤执行，每步必须等待用户确认后才能继续下一步！**

1. **使用任务管理工具** - 开始前必须调用 `add_tasks` 创建完整任务列表
2. **逐步推进** - 每完成一步立即标记为 COMPLETE，再开始下一步
3. **等待确认** - 每个需要用户确认的步骤，必须使用 `AskUserQuestion` 并等待回复
4. **禁止跳步** - 不得在用户未确认前开始编写代码

## 📋 工作流程

### Step 0: 创建任务列表

**[MUST DO FIRST]** 调用 `add_tasks` 创建以下任务：

```
- [ ] 收集用户需求
- [ ] 确定产品和平台
- [ ] 查阅相关文档
- [ ] 输出交互稿并确认
- [ ] 设计架构并确认
- [ ] 制定实现规划书
- [ ] 执行代码实现
- [ ] 构建测试
- [ ] 输出交付文档
```

标记第一个任务为 IN_PROGRESS。

---

### Step 1: 收集用户需求

**目标**：了解用户对示例代码的完整需求。

**执行**：使用 `AskUserQuestion` 询问：

```
请描述示例代码的详细要求：
1. 目标产品（如：实时音视频、即时通讯）。从`references/products-platforms.md`中获取产品列表和支持的平台。
2. 平台/语言（如：Android Java、iOS Swift、Web React、Node.js）
3. 核心功能（如：1v1视频通话、多人会议、屏幕共享）
4. 交互流程（用户如何操作）
5. 特殊需求（如：美颜、录制、混流）
6. 输出目录（代码保存位置）
```

**完成条件**：用户回复需求描述。

**完成后**：标记任务为 COMPLETE，开始 Step 2。

---

### Step 2: 查阅相关文档

**目标**：收集实现所需的技术文档。

**执行**：

1. 从 `references/products-platforms.md` 获取文档路径
2. 查阅以下文档（参考 `references/doc-path-guide.md`）：
   - 集成指南
   - 快速开始
   - Token 鉴权说明（如需要）
   - 服务端签名说明（如需要）
   - 客户端 API 文档
   - 服务端 API 文档（如需要）

**完成条件**：收集到所有必要文档。

**完成后**：标记任务为 COMPLETE，开始 Step 3。

---

### Step 3: 输出交互稿并确认

**目标**：设计用户交互流程，获得用户确认。

**执行**：

1. 根据需求输出交互稿（Markdown 格式）：
   - 功能概述
   - 用户流程（步骤列表）
   - 界面设计（UI 元素）
   - 核心交互（触发条件 -> 响应）
   - 数据流

2. 使用 `AskUserQuestion` 确认：
   ```
   交互稿如上，请确认：
   1. 确认无误，继续
   2. 需要修改
   ```

**完成条件**：用户确认交互稿无误。

**完成后**：标记任务为 COMPLETE，开始 Step 4。

---


### Step 4: 设计架构并确认

**目标**：设计示例代码架构，获得用户确认。

**核心原则**：
- **扁平化结构** - 避免过度封装
- **直接调用** - Activity/View 中直接调用 SDK API
- **代码集中** - 相关逻辑放在单个文件
- **可读性优先** - 用户能在一个文件看完完整流程

**执行**：

1. 参考 `references/architecture-templates.md`
2. 输出架构设计（Markdown 格式）：
   - 项目结构（扁平化）
   - 核心类设计（职责说明）
   - 调用流程（单文件内完成）
   - 关键 API 调用（直接调用，无封装）

3. 使用 `AskUserQuestion` 确认：
   ```
   架构设计如上，请确认：
   1. 确认无误，继续
   2. 需要修改
   ```

**完成条件**：用户确认架构设计无误。

**完成后**：标记任务为 COMPLETE，开始 Step 5。

---

### Step 5: 制定实现规划书

**目标**：制定详细的实现计划，精确到 API 调用。

**执行**：

1. 创建 `implementation-plan.md`，包含：
   - 项目概述（产品/平台/功能）
   - 环境准备（开发环境/依赖）
   - 实现步骤（每步包含：调用 API、参数、说明）
   - 关键代码片段
   - 注意事项

2. 保存到 `{工作目录}/implementation-plan.md`

**完成条件**：规划书已保存。

**完成后**：标记任务为 COMPLETE，开始 Step 6。

---

### Step 6: 执行代码实现

**目标**：按规划书逐步实现代码。

**执行**：

1. **创建实现任务列表**：调用 `add_tasks` 将规划书中的步骤转为任务
2. **逐步实现**：
   - 标记当前任务为 IN_PROGRESS
   - 实现该任务
   - 完成后立即标记为 COMPLETE
   - 继续下一个任务
3. **遇到问题**：创建新的修复任务

**任务管理原则**：
- 每个任务原子化，可独立完成
- 完成后立即标记 COMPLETE
- 不批量标记多个任务

**完成条件**：所有实现任务标记为 COMPLETE。

**完成后**：标记主任务为 COMPLETE，开始 Step 7。

---

### Step 7: 构建测试

**目标**：构建项目并测试功能。

**执行**：

根据平台执行构建命令：

**移动端**：
```bash
# Android
./gradlew assembleDebug

# iOS
xcodebuild -workspace Demo.xcworkspace -scheme Demo build
```

**Web 端**：
```bash
npm install
npm run dev
# 使用 Chrome 开发者工具测试
```

**服务端**：
```bash
# Node.js
npm install && npm start

# Python
pip install -r requirements.txt && python main.py

# Go
go run main.go
```

**测试要求**：
- 尝试自行构建编译
- Web 端使用浏览器开发者工具测试
- 遇到报错分析并修复
- 记录测试结果

**完成条件**：构建成功，功能测试通过。

**完成后**：标记任务为 COMPLETE，开始 Step 8。

---

### Step 8: 输出交付文档

**目标**：输出项目交付文档。

**执行**：

输出交付文档（Markdown 格式）：
- 项目信息（产品/平台/路径）
- 实现功能
- 使用说明（环境要求/运行步骤/配置说明）
- 测试结果
- 已知问题

**完成条件**：交付文档已输出。

**完成后**：标记任务为 COMPLETE，所有任务完成。

---

## 📚 参考资源

### Reference Files

- **`references/products-platforms.md`** - ZEGO 产品列表和各产品支持的平台配置
- **`references/architecture-templates.md`** - 示例代码架构模板
- **`references/doc-path-guide.md`** - 文档路径查找指引

### MCP Tools

可用的 ZEGO MCP 工具（通过 `mcp/zego.json` 配置）：
- 文档搜索和查询功能
- API 文档获取

---

## 💡 使用示例

**场景 1：创建新示例代码**

```
用户: 帮我创建一个音视频通话的示例代码

Claude:
1. 创建任务列表（add_tasks）
2. 询问详细需求（AskUserQuestion）
3. 确定产品和平台
4. 输出交互稿并等待确认
5. 查阅文档
6. 设计架构并等待确认
7. 制定规划书
8. 逐步实现（使用任务管理）
9. 构建测试
10. 输出交付文档
```

**场景 2：为现有 demo 添加功能**

```
用户: 给现有的 demo 添加美颜功能

Claude:
1. 创建任务列表
2. 确认产品和平台（基于现有 demo）
3. 询问美颜功能具体需求
4. 查阅美颜相关文档
5. 输出功能扩展方案并确认
6. 实现并测试
```

---

## ⚠️ 注意事项

1. **严格遵守步骤顺序** - 不得跳过任何步骤
2. **必须等待用户确认** - 交互稿、架构设计必须确认后才能继续
3. **使用任务管理** - 所有实现过程必须使用 task management tools
4. **单文件实现原则** - 示例代码优先可读性，避免过度封装
5. **完整测试** - 必须尝试构建和测试，不能只写代码不验证

