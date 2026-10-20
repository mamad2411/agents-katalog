# Meeplit 开发规范

## 项目结构规范

### Monorepo 结构
- 使用 Bun workspaces 管理三个包：`packages/server`、`packages/client`、`packages/shared`
- 共享类型和工具必须放在 `packages/shared` 中
- 包之间的依赖通过 workspace 引用，例如 `"@meeplit/shared": "workspace:*"`

### 代码组织
- **服务器代码**：`packages/server/src/`
  - `main.ts` - 应用入口点
  - `game/` - 局内游戏逻辑
  - `*.ts` - 局外业务逻辑
- **客户端代码**：`packages/client/src/`
  - `game/` - 局内组件和服务
    - `game/components/` - 可复用组件
  - `views/` - 局外组件
- **共享代码**：`packages/shared/`
  - `rpc.ts` - RPC 协议定义
  - `game.ts` - 游戏类型定义
  - `chat.ts` - 聊天类型定义

## 代码风格规范

### TypeScript
- 使用严格模式（`strict: true`）
- 优先使用接口（interface）而非类型别名（type），除非需要联合类型或映射类型
- 避免使用 `any`，使用 `unknown` 或具体类型
- 导出类型时使用 `export type { ... }` 语法
- 使用 `camelCase` 命名变量和函数，`PascalCase` 命名类和接口

### Vue 3 组件
- 使用 `<script setup>` 语法
- 组件文件名使用 `PascalCase`，例如 `GameInfo.vue`
- 组合式函数使用 `use` 前缀，例如 `useGameState`
- Props 使用 TypeScript 接口定义
- 避免在模板中使用复杂的逻辑，提取到计算属性或方法中

### RPC 通信
- RPC 方法命名使用 `camelCase`
- 服务器调用客户端方法时使用 `.` 分隔的路径，例如 `gameService.ask`
- 使用适当的调用模式：
  - `emit()` - 单向通知，不等待响应
  - `call()` - 请求-响应，需要返回值
  - `reserve()` - 收集请求用于批量执行
- 批量调用时指定执行模式：`sequential`（顺序）或 `parallel`（并行）

### 卡牌类设计
- 所有卡牌类必须继承自 `Card` 基类
- 可以在 `play()` 方法中实现卡牌效果

## 开发流程规范
### 提交信息
- 使用 Conventional Commits 格式
- 类型前缀：`feat:`、`fix:`、`docs:`、`style:`、`refactor:`、`test:`、`chore:`
- 示例：`feat: 添加对手区组件显示玩家状态`

## 架构原则
### 通信与控制权
- 游戏局外使用传统的web接口，账号管理、房间管理等，由客户端发起请求服务器响应
- 游戏局内使用反向rpc，服务器务器主动询问客户端（你要出什么牌？），而不是客户端请求服务器
### 反向RPC
- 基于桌面游戏玩家只能在特定时机行动的特点，设计了此通信模式
- 由服务器驱动整个游戏流程，一个函数控制整局游戏，游戏逻辑代码高内聚，且无需状态同步
- 客户端负责响应服务器的请求，收集玩家操作输入，展示游戏状态与变化

### 状态管理原则
- 服务器是唯一的状态源
- 客户端状态是服务器的投影
- 通过 RPC 同步状态变更
- 客户端本地状态仅用于 UI 交互

### 错误处理原则
- RPC 调用必须有超时处理
- 网络异常必须有重连机制
- 游戏状态异常必须有恢复机制
- 用户输入必须有验证和反馈

## 性能优化指南
### 渲染优化
- Vue 组件使用 `shallowRef` 优化性能
- 避免不必要的重新渲染
- 使用虚拟列表处理大量数据
- 图片懒加载和压缩

## 文档要求

### 代码注释
- 公共 API 必须有 JSDoc 注释
- 复杂算法必须有解释性注释
- TODO 注释必须包含负责人和预计完成时间
- FIXME 注释必须包含问题和解决方案

### 项目文档
- `README.md` - 项目概述和快速开始
- `memory-bank/` - 项目知识库
  - `projectbrief.md` - 项目概览
  - `activeContext.md` - 当前工作上下文
  - `progress.md` - 开发进度跟踪
- API 文档 - HTTP 和 RPC 接口文档

## 开发工作流规范

### 前端开发
- 前端代码使用 Vite 开发服务器运行
- 开发者自行查看样式效果，无需 AI 启动测试服务器
- AI 在修改前端代码后只需关注 TypeScript 报错
- 使用 `bun run dev` 启动开发服务器

### 代码质量检查
- 修改代码后运行 `bun run type-check` 检查 TypeScript 类型
- 使用 `bun run lint` 进行代码风格检查
- 提交前确保没有 TypeScript 错误

## 部署规范

### 环境配置
- 使用环境变量管理配置
- 不同环境使用不同配置文件
- 敏感信息不提交到版本控制
- 配置验证在启动时进行

### 构建部署
- 客户端使用 Vite 构建
- 服务器使用 Bun 运行

---

*最后更新：2026-02-24*