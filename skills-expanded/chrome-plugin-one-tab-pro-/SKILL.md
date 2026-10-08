# OneTabPro 项目规则和模式

## 项目结构

- 前端代码按功能和组件类型组织
- 后端代码遵循控制器-服务-仓库模式
- 所有组件都使用 TypeScript 接口进行类型定义
- 扩展使用Manifest V3规范开发
- API服务使用Hono.js框架开发
- 数据库使用Prisma ORM管理

## 命名约定

- React 组件：PascalCase（例如，TabGroup.tsx）
- React hooks：camelCase 带 use 前缀（例如，useTabGroups.ts）
- API 端点：kebab-case（例如，/api/tab-groups）
- 数据库表：snake_case（例如，tab_groups）
- TypeScript 接口：PascalCase 带 I 前缀（例如，ITabGroup）
- TypeScript 类型：PascalCase（例如，TabGroupResponse）
- 项目目录：使用规范化的分层结构（例如，components/, services/, hooks/）

## 代码模式

- 在 React 中使用函数组件和 hooks
- 除非绝对必要，否则避免使用类组件
- 使用 Context API 进行状态管理
- 相比于 Promise 链，更倾向于使用 async/await
- 使用 try/catch 块进行错误处理
- 使用 TypeScript 类型接口确保代码类型安全

## API 约定

- 用于 CRUD 操作的 RESTful 端点
- 适当使用 HTTP 状态码（200, 201, 400, 401, 403, 404, 500）
- 所有响应采用一致的 JSON 格式
- 错误响应中始终包含错误消息和代码
- 在 Authorization 头中使用 JWT 令牌（Bearer 方案）
- 请求参数使用Zod进行验证

## 扩展模式

- 后台 service worker 用于处理事件和 API 调用
- 弹出式 UI 用于用户交互
- 本地存储用于缓存和离线功能
- Chrome API 交互封装在服务类中
- React组件用于UI渲染和交互
- Axios用于处理API请求
- Tailwind CSS用于样式设计

## 数据库模式

- 对主键使用 UUID
- 包含 created_at 和 updated_at 时间戳
- 使用外键表示关系
- 适当时使用软删除
- 对频繁查询的字段进行适当索引
- 使用Prisma模型定义数据结构
- 采用一对多关联模型（用户->标签组->标签页）

## 测试方法

- 对工具函数和服务进行单元测试
- 对 React 组件进行组件测试
- 对 API 端点进行集成测试
- 对关键流程进行端到端测试
- 使用手动测试验证扩展功能

## 文档要求

- 所有函数使用 JSDoc 注释
- 每个主要目录都有 README 文件
- 带有示例的 API 文档
- 复杂功能的架构图
- 清晰的用户指南文档

## 开发工作流

- 功能分支工作流
- 所有更改都需要拉取请求
- 需要代码审查
- 合并前必须通过代码检查和测试
- 使用规范的提交消息
- 创建一致的项目结构

## 安全考虑

- 永不在 localStorage 中存储敏感数据
- JWT 令牌必须具有适当的过期时间
- 始终验证和净化用户输入
- 为扩展使用内容安全策略
- 所有 API 通信使用 HTTPS
- 确保资源授权和用户数据隔离

## 性能指南

- 优化 React 组件渲染
- 对昂贵的计算使用记忆化
- 尽可能批量处理 API 请求
- 实现高效的标签页操作
- 注意扩展的内存使用
- 使用本地缓存减少网络请求

## 当前开发状态

- 已完成基本项目结构和配置
- 已实现UI框架和基本组件
- 已设计核心数据模型和API端点
- 已设计基本认证流程
- 待实现数据库连接和同步逻辑
- 待完善微信登录流程
- 待解决开发环境中的类型错误
