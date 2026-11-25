---
name: project-java-init
version: 1.3.0
updated: 2026-02-26
description: 当用户想要初始化一个新的 Java 全栈项目（Spring Boot + Vue3）或继续中断的初始化会话时使用。该技能处理端到端流程，包括项目创建、依赖管理、配置和基础代码生成。它使用持久化的 INIT_TODO.md 文件来跟踪进度和恢复上下文。
triggers:
  - initialize java project
  - create spring boot project
  - build java framework
  - setup vue3 project
  - java project init
  - 初始化Java项目
  - 新建SpringBoot项目
  - 搭建后端框架
  - 搭建前端框架
  - 项目初始化
  - 继续初始化
changelog:
  - 1.3.0: 修复 Spring Boot 3.x 兼容性问题，新增报错速查表，支持多环境配置
  - 1.2.0: 新增版本推荐矩阵，操作分工标注
  - 1.1.0: 中文化，修复端口硬编码
  - 1.0.0: 初始版本
---

# Java 项目初始化 Skill

## 概述
本 Skill 作为一个交互式向导，用于初始化 Java 全栈项目（Spring Boot + Vue3）。它使用 `INIT_TODO.md` 文件来跟踪进度、维护上下文，并允许断点续期。

## 何时使用
当用户询问以下内容时使用本 Skill：
- "初始化 Java 项目"
- "新建 Spring Boot 项目"
- "搭建后端/前端框架"
- "项目初始化"
- "继续初始化"

## 铁律：INIT_TODO.md
**上下文保存至关重要。** 你必须使用 `INIT_TODO.md` 来跟踪状态。

### 第一步：断点检测（必须最先执行）
**你必须首先询问：**
"您好！在开始之前，请问您是否有 `INIT_TODO.md` 文件？（如果您是继续之前的会话，请上传它。）"

- **如果有：** 读取文件 -> 从"项目配置"恢复上下文 -> 找到第一个未打勾的项目 -> 说"找到进度，从 [X 阶段] 继续..." -> 继续执行。
- **如果没有：** 开始 **配置收集** 流程。

### 第二步：配置收集（新项目）
在一条消息中询问以下 7 个问题：
1. **项目类型**：仅后端 / 仅前端 / 全栈？
2. **项目名称**（英文，如 `yu-picture`）：
3. **[后端] Java 版本意向**：8 / 11 / 17 / 21，或者"不知道，帮我推荐"？
4. **[后端] 特殊依赖**：是否有库要求特定 Java 版本？
5. **[后端] MySQL 版本**（5.7/8.x）：
6. **[后端] 数据库名**（如 `yu_picture`）：
7. **[前端] 需要前端吗？**（是/否）：

### 第三步：版本推荐与确认
根据用户对 Java 版本的回答，推荐最兼容的组合：

*   **Java 8 / 11 (Spring Boot 2.x)**:
    *   Spring Boot: 2.7.x
    *   MyBatis-Plus: 3.5.9 (`mybatis-plus-boot-starter`)
    *   Knife4j: 4.4.0 (`knife4j-openapi2-spring-boot-starter`)
    *   Hutool: 5.8.26
*   **Java 17 / 21 (Spring Boot 3.x)**:
    *   Spring Boot: 3.1.x 或 3.2.x+
    *   MyBatis-Plus: 3.5.9 (`mybatis-plus-spring-boot3-starter`)
    *   Knife4j: 4.4.0 (`knife4j-openapi3-jakarta-spring-boot-starter`)
    *   Hutool: 6.x (如 6.0.0-M14)

**询问用户：** "基于您的 Java 版本，推荐使用上述组合。是否确认使用，还是需要调整？"

确认后，将确定的版本号和 artifactId 记录下来，用于后续替换代码模板中的占位符。

### 第四步：生成 INIT_TODO.md
收集回答并确认版本后，**立即** 使用 `Write` 工具在项目根目录创建 `INIT_TODO.md` 文件（内容见下方模板）。
然后，向用户确认文件已创建。

#### INIT_TODO.md 模板
```markdown
# {PROJECT_NAME} 初始化进度

> 本文件由 AI 自动生成以跟踪进度。
> 如果会话结束，上传此文件以恢复进度。

## [配置] 项目配置
| 配置项 | 值 |
|---|---|
| 项目名称 | {PROJECT_NAME} |
| 类型 | {TYPE} |
| 后端端口 | {PORT} |
| Java 版本 | {JAVA_VERSION} |
| Spring Boot 版本 | {SPRING_BOOT_VERSION} |
| 数据库名 | {DB_NAME} |
| 包名前缀 | com.xxx.{PROJECT_NAME} |
| 创建时间 | {TIME} |

---

## [后端] 后端进度

### 阶段一：项目创建
- [ ] 确认 JDK ({JAVA_VERSION})
- [ ] 确认 MySQL 已安装
- [ ] Spring Initializr 创建完成
- [ ] Maven 依赖安装完成
- [ ] .gitignore 已配置 [重要]
**验证结果：** 待填写

### 阶段二：application.yml
- [ ] application.yml (公共) 已配置
- [ ] application-local.yml (私密) 已配置
- [ ] 项目启动成功
**验证结果：** 待填写

### 阶段三：核心依赖
- [ ] MyBatis-Plus 已添加且原生 MyBatis 已移除 [重要]
- [ ] @MapperScan 已配置
- [ ] Hutool 已添加
- [ ] Knife4j 已添加
**验证结果：** 待填写

### 阶段四：通用代码
- [ ] exception/* 已创建
- [ ] common/* 已创建
- [ ] config/* 已创建
- [ ] controller/MainController 已创建
**验证结果：** 待填写

### 阶段五：验证 [已验证]
- [ ] /health 返回 "ok"
**实际响应：** 待填写

---

## [前端] 前端进度

### 阶段一：创建
- [ ] Node.js >= 18.12
- [ ] create-vue 执行完成
- [ ] .gitignore 已配置
- [ ] npm install & dev 完成
**验证结果：** 待填写

### 阶段二：工程化
- [ ] Prettier 已配置
- [ ] ESLint 已关闭
**验证结果：** 待填写

### 阶段三：Ant Design Vue
- [ ] 已安装并注册
- [ ] 组件已验证
**验证结果：** 待填写

### 阶段四：全局布局
- [ ] BasicLayout 已创建
- [ ] GlobalHeader 已创建
- [ ] App.vue 已修改
**验证结果：** 待填写

### 阶段五：路由配置
- [ ] pages 目录已创建
- [ ] router/index.ts 已配置
**验证结果：** 待填写

### 阶段六：Axios & OpenAPI
- [ ] Axios 已安装
- [ ] request.ts 已创建
- [ ] openapi.config.js 已创建
**验证结果：** 待填写

### 阶段七：Pinia 状态管理
- [ ] useLoginUserStore 已创建
- [ ] App.vue 调用 fetchLoginUser
**验证结果：** 待填写

### 阶段八：最终验证
- [ ] 页面显示正常
- [ ] 路由跳转正常
**验证结果：** 待填写

---

## [完成] 整体完成
- [ ] 后端就绪（/health 接口返回 ok）
- [ ] 前端就绪（页面正常）
- [ ] 联调通过：前端调用后端 /health，无 CORS 错误
- [ ] 联调通过：浏览器控制台无报错
```

## 后端工作流

### 阶段一：创建
- 👤 **需要你来操作：** 确认本地 JDK 版本与选择的一致。
- 👤 **需要你来操作：** 使用 IDEA 或浏览器访问 `https://start.aliyun.com/` 创建项目。
- **依赖选择**：Spring Web, MyBatis Framework, MySQL Driver, Lombok。
- 👤 **需要你来操作：** 等待 Maven 依赖下载完成。
- 🤖 **AI 生成代码：** 生成 `.gitignore`。
- 👤 **需要你来操作：** 创建 `.gitignore` 文件。

### 阶段二：application.yml
- 🤖 **AI 生成代码：** 根据 `references/backend.md` 生成配置内容（包含 `application-local.yml`）。
- **注意**：如果使用 **Spring Boot 3.x**，请**删除** `mvc.pathmatch` 配置块（不支持 `ant_path_matcher`）。
- 👤 **需要你来操作：** 创建 `src/main/resources/application.yml` 和 `application-local.yml`。
- 👤 **需要你来操作：** 将 `application-local.yml` 加入 `.gitignore`。
- 👤 **需要你来操作：** 启动项目，验证无数据库连接错误。

### 阶段三：核心依赖
- 🤖 **AI 生成代码：** 生成 `pom.xml` 依赖片段。
- **注意**：AI 必须根据版本替换 `{MYBATIS_PLUS_ARTIFACT_ID}`, `{KNIFE4J_ARTIFACT_ID}`, `{KNIFE4J_VERSION}` 等占位符。
    - Spring Boot 2.x -> `mybatis-plus-boot-starter`, `knife4j-openapi2-spring-boot-starter`
    - Spring Boot 3.x -> `mybatis-plus-spring-boot3-starter`, `knife4j-openapi3-jakarta-spring-boot-starter`
- 👤 **需要你来操作：** 将依赖添加到 `pom.xml`，并**移除**原生的 `mybatis-spring-boot-starter`。
- 👤 **需要你来操作：** 刷新 Maven。
- 🤖 **AI 生成代码：** 提供 `@MapperScan` 和 `application.yml` 追加配置。
- 👤 **需要你来操作：** 添加配置。

### 阶段四：通用基础代码
- 🤖 **AI 生成代码：** 逐个生成 `references/backend.md` 中的 Java 文件。
- **重要**：将 `{BASE_PACKAGE}` 替换为实际包名。
- 👤 **需要你来操作：** 在项目中创建对应文件并粘贴代码。

### 阶段五：验证
- 👤 **需要你来操作：** 启动后端项目。
- 👤 **需要你来操作：** 浏览器访问 `http://localhost:{PORT}/api/health`。
- **更新 INIT_TODO.md**：填写实际响应并标记为已检查。

## 前端工作流 (Vue3 + TS + Vite)

### 阶段一：创建
- 👤 **需要你来操作：** 确认 Node.js >= 18.12。
- 👤 **需要你来操作：** 在终端执行 `npm create vue@3.12.1`。
- **说明**：锁定版本是为了确保教程兼容性。如需最新版，可使用 `npm create vue@latest`。
- **选项**：TS=是, JSX=否, Router=是, Pinia=是, ESLint=是, Prettier=是。
- 🤖 **AI 生成代码：** 生成 `.gitignore`。
- 👤 **需要你来操作：** 执行 `cd {项目名} && npm install && npm run dev`。

### 阶段二：配置
- 👤 **需要你来操作：** 配置 Prettier 为 Manual 模式（IDE 设置）。
- 👤 **需要你来操作：** 关闭 ESLint 实时检查（IDE 设置）。

### 阶段三：Ant Design Vue
- 👤 **需要你来操作：** 执行 `npm i --save ant-design-vue@4.x`。
- 🤖 **AI 生成代码：** 生成 `main.ts` 代码。
- 👤 **需要你来操作：** 覆盖 `src/main.ts`。

### 阶段四：全局布局
- 🤖 **AI 生成代码：** 生成布局组件代码（见 `references/frontend.md`）。
- 👤 **需要你来操作：** 创建文件并粘贴代码。

### 阶段五：路由配置
- 🤖 **AI 生成代码：** 生成页面和路由代码。
- 👤 **需要你来操作：** 先创建 `src/pages` 下的页面文件，再配置路由。

### 阶段六：Axios & OpenAPI
- 👤 **需要你来操作：** 执行 `npm install axios` 和 `npm install --save-dev @umijs/openapi`。
- 🤖 **AI 生成代码：** 生成 `src/request.ts` 和 `openapi.config.js`。
- **注意**：AI 必须将 `{PORT}` 替换为后端实际端口。
- 👤 **需要你来操作：** 创建文件并粘贴代码。

### 阶段七：Pinia 状态管理
- 🤖 **AI 生成代码：** 生成 Store 代码。
- 👤 **需要你来操作：** 创建文件并粘贴代码。

### 阶段八：最终验证
- 👤 **需要你来操作：** 浏览器访问前端页面。
- 👤 **需要你来操作：** 点击菜单验证路由跳转。
- **更新 INIT_TODO.md**：标记完成。

## 常见问题
如果在初始化过程中遇到报错，请查阅 `references/troubleshooting.md`。

## 更新规则
1. **每个阶段后**：要求用户验证。
2. **成功时**：更新 `INIT_TODO.md`（勾选项目，填写验证结果）。
3. **展示文件**：始终展示**完整更新后**的 `INIT_TODO.md` 并要求用户保存。
