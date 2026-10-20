# Cloud Game

## 项目概述

Cloud Game 是一个云游戏平台，前期以 Avalon Online（桌游"抵抗组织：阿瓦隆"在线版）为首款游戏，后续可扩展接入更多云游戏。

**技术栈**：Nuxt 5 (nightly) SSR + Nitro Server + Vue 3 + TypeScript

**重要说明**：`_reference/` 目录通过 git subtree 引入了上游开源 Avalon 仓库（[Razdva122/avalon](https://github.com/Razdva122/avalon)）的完整代码，**仅供阅读参考，禁止修改**。开发时从中理解协议、类型定义和游戏逻辑，然后在新项目中重新实现。

## 项目结构

```
cloud-game/
  _reference/        # 上游代码（只读参考，禁止修改）
    packages/
      backend/       # Node.js + Express + Socket.io + MongoDB
      types/         # 共享 TypeScript 类型
      ui/            # Vue 3 + Vuetify 3 前端
  app/               # Nuxt app 入口
    pages/           # 文件路由
    components/      # Vue 组件
      common/        # 通用组件（玩家列表、房主控制等）
      games/         # 游戏专属组件（avalon/ 等）
    composables/     # 组合式函数
    layouts/         # 布局
    middleware/      # 中间件
    plugins/         # 插件
  server/            # Nitro server（API routes, WebSocket, 游戏逻辑）
    api/             # REST API
    game/            # 游戏逻辑
      registry.ts    # 游戏注册表（gameType → GameEngine）
      rooms.ts       # 通用房间服务（v0.1.4 内存状态 + 生命周期）
      rooms/         # 房间 Socket 事件绑定
        handlers.ts  # 房间 Socket 事件注册（v0.1.4）
      avalon/        # Avalon 引擎
    db/              # 数据库层
      models/        # Mongoose Models（User, Room）
    plugins/         # Nitro 插件（Socket.IO 初始化、MongoDB 连接）
    utils/           # 服务端工具
  shared/            # 前后端共享类型与常量
    types/
      common/        # 通用类型（room, user, api 等）
      games/         # 游戏专属类型
        avalon/      # Avalon（角色、状态、配置等）
  docs/              # 项目文档
  tests/             # 自动化测试（按模块分子目录）
  nuxt.config.ts
  package.json
```

## _reference 目录使用规范

- **只读**：任何情况下不得修改 `_reference/` 中的文件
- **参考用途**：理解 Socket 事件协议、类型定义、游戏逻辑、数据库模型
- **同步上游更新**：

```bash
git subtree pull --prefix=_reference upstream master --squash
```

- 上游 remote 已配置为 `upstream`（`git@github.com:Razdva122/avalon.git`）

**上游关键参考索引**

| 需要了解的内容 | 参考路径 |
|---|---|
| Socket 事件协议 | `_reference/packages/types/api/sockets.ts` |
| 游戏角色类型 | `_reference/packages/types/game/roles.ts` |
| 游戏状态类型 | `_reference/packages/types/game/` |
| 房间类型 | `_reference/packages/types/room/` |
| 用户类型 | `_reference/packages/types/user/` |
| 游戏核心逻辑 | `_reference/packages/backend/src/core/` |
| 数据库模型 | `_reference/packages/backend/src/db/models/` |
| Addon 系统 | `_reference/packages/backend/src/core/game/addons/` |

## 技术栈

| 层级 | 选型 | 备注 |
|------|------|------|
| 框架 | Nuxt 5 (nightly) | SSR，文件路由，auto-import |
| 服务端 | Nitro | API routes, middleware, WebSocket |
| 前端 | Vue 3.5+ (Composition API) | `<script setup>` |
| 类型 | TypeScript | 严格模式 |
| 测试 | Vitest | 单元测试 + 集成测试 |
| 类型检查 | vue-tsc | `--noEmit` 模式 |
| 样式 | SCSS | Vite 预处理器 + 全局主题变量 |
| 状态管理 | Pinia | 配合 Nuxt 插件 |
| 实时通信 | Socket.IO | `socket.io-client`（前端）+ Socket.IO Server（Nitro plugin，独立端口 3200） |
| 代码规范 | @nuxt/eslint | Flat config，AI 开发风格统一 |
| 数据库 | MongoDB | 通过 `.env` 管理连接 |
| ODM | Mongoose | Schema 校验 + TypeScript 类型推断，替代上游的 Typegoose |

## 代码规范

- **语言**: 全面使用 TypeScript
- **类型**: 类型前缀 `T`（如 `TRoomInfo`）；有方法的对象用 interface
- **命名**: 变量/函数用 camelCase，类/类型用 PascalCase，常量用 UPPER_CASE，文件名用 kebab-case
- **提交格式**: 见下方「Commit Message 格式规约」
- **Vue**: 新组件使用 Composition API + `<script setup>`
- **文档与注释**: 简洁精确，只写关键点（为什么这样做、隐藏约束、非显而易见的权衡）。不重复代码已表达的信息，不写大段说明、背景铺垫或示例废话。宁可少一行也不多一行。

## 测试规范

完整方案见 `docs/testing.md`。以下为 AI 编码助手必须遵守的约束。

### 工具与脚本

| 脚本 | 命令 | 用途 |
|---|---|---|
| `npm run test` | `vitest run` | 运行全部测试 |
| `npm run test:watch` | `vitest` | 监听模式 |
| `npm run typecheck` | `vue-tsc --noEmit` | 类型检查 |

- **测试框架**: Vitest
- **类型检查**: vue-tsc
- **配置文件**: `vitest.config.ts`

### 测试目录结构

```
tests/
  setup.ts                    # 全局 mock
  utils/                      # 工具函数测试
  composables/                # 组合式函数测试
  stores/                     # Pinia Store 测试
  api/                        # REST 端点测试（v0.1.4 起）
  game/                       # 服务端游戏逻辑与房间服务测试（v0.1.4 起）
  components/                 # Vue 组件测试
```

测试文件命名：`<source-name>.test.ts`，与被测模块一一对应。

### 测试约束（必须遵守）

1. **新增业务逻辑必须带测试** —— 修改 `app/utils/`、`server/game/` 等核心文件时，改动必须包含对应的 `*.test.ts`。
2. **Bug 修复先写失败用例** —— 修复 bug 时，先添加一条能复现该 bug 的失败测试用例，再修复代码使其通过。
3. **新增角色 / 游戏阶段必须同步测试** —— 游戏引擎每新增一个角色或阶段，必须在对应测试文件中补充 case。
4. **外部依赖一律 mock** —— Socket（`useSocket`）、localStorage、WebSocket 等外部依赖在测试中用 `vi.mock` / `vi.stubGlobal` 替换。
5. **测试描述用行为句式** —— 用 `it('连续 5 次投票拒绝时邪恶方获胜', ...)` 而非 `it('test vote')`。

## 文档同步规范

任务完成后，必须检查以下文档是否需要同步更新，**不允许"先做功能、后补文档"**。

### 需要维护的文档

| 文档 | 路径 | 同步时机 |
|---|---|---|
| 项目上下文 | `AGENTS.md` | 技术栈变更、新增目录结构、新增开发约束时 |
| 架构文档 | `docs/architecture.md` | 架构决策变更、新增核心模块、目录结构调整时 |
| 路线图 | `docs/roadmap.md` | 完成某个阶段的功能后，勾选对应 checkbox |
| 变更日志 | `docs/changelog.md` | 每次有用户可感知的功能变更时记录 |
| 测试方案 | `docs/testing.md` | 测试阶段推进、新增测试层或策略调整时 |

### 同步规则

1. **技术栈变更立即更新** —— 新增、替换或移除依赖（如引入数据库、确定通信方案）时，同步更新 `AGENTS.md` 和 `docs/architecture.md` 的技术栈表格。
2. **目录结构变更立即更新** —— 新增顶层目录或重要子目录时，同步更新 `AGENTS.md` 的项目结构。
3. **功能完成勾选路线图** —— 完成 `docs/roadmap.md` 中某个待办项后，将 `[ ]` 改为 `[x]`。
4. **开发约束新增即写入** —— 新增编码规范、测试约束、提交规范等，写入 `AGENTS.md` 对应章节。

## Git 规范

### Commit Message 格式规约

```
<type>(version): <summary>

Feat:
- English bullet 1
- English bullet 2

Fix:
- English bullet

Feat:
- 中文 bullet 1
- 中文 bullet 2

Fix:
- 中文 bullet

```

- **type**：`feat` / `fix` / `refactor` / `docs` / `test` / `chore`
- **version**：当前项目版本（`v<major>.<minor>.<patch>`），同一版本的多个 commit 共用同一 scope
- **summary**：1 句概括性的英文，描述"这次 commit 干了什么"

**Body**

按改动类型分组，每组用 `<Type>:` 开头；英文 bullet 在前，中文 bullet 复述在后。依赖变更（`Cargo.toml` / `package.json`）单独用 `依赖变更：` section 收口，如果没有则可以跳过此项。

### 版本发布

版本发布提交时，将现有改动都合进一个发版提交，不拆分为 feat commit 和 release commit。

```bash
npm version <level> -f -m <commit message>
```

- `<level>` 为 `patch` / `minor` / `major`，由用户指定或根据改动范围判断
- `<commit message>` 即发版提交的 message，按上方 Commit Message 格式规约写
- 完成后执行 `git push --follow-tags` 推送 commit 和 tag



## 开发环境

### 本地启动

```bash
npm install
npm run dev            # http://localhost:3000
```

### 开发态认证流程

dev 模式不再自动以测试用户登录，启动即进入未登录态、展示真实的注册/登录表单，便于测试认证链路。登录页底部有开发态可见的「以测试账号登录」按钮，点击后通过真实 `register`/`login` 链路登录固定账号 `dev`/`devpassword`（首次自动注册）。登录态持久化在 localStorage，刷新后保持登录；点击「退出登录」可回到表单重新测试。

