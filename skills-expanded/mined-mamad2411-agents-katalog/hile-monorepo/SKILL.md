---
name: hile-monorepo
description: "引导 AI 在本仓库或使用 Hile 的项目中，正确选用并遵守各 Hile 模块的约束与用法。编辑/生成涉及 @hile/* 或 create-hile 的代码时必读。凡依赖 @hile/http-next 的应用须同时严格遵守 packages/http-next/SKILL.md 全文，不得选择性遵守。"
---

# Hile monorepo — AI 编程约束

本文档面向 AI 编码模型：在**本仓库**或**使用 Hile 的应用项目**中生成或修改代码时，必须按本 SKILL 选用模块并遵守各包约束，确保与 Hile 架构一致。

**`@hile/http-next`（Next + API 同端口）**：只要项目的 `package.json` 依赖了 **`@hile/http-next`**，或代码中出现 **`HttpNext`** / **`from "@hile/http-next"`**，AI **必须**将 **`packages/http-next/SKILL.md`**（或应用内已同步的同名约束文档）视为**硬约束**：**全文条例均需遵守**，包括目录（`src/services/`、`src/controllers/` 为默认 API 根、`src/models/`）、**`controllerDirectory` 默认值**、**`defineModel`** 仅在 **`src/models`**、**`src/app` 可直接 `loadModel(xxxModel)`**、**`src/controllers` 允许 `loadService` 与 `loadModel(xxxModel)`**、boot 路径与 **`cwd`** 等；**禁止**只采纳其中部分条款或凭经验改写架构。

---

## 1. 何时必须遵守本 SKILL

- 编辑或新增的代码**引用**了任意 `@hile/*` 或 `create-hile`
- 项目依赖 **`@hile/http-next`** 时：**除本 SKILL 外**，**必须**完整遵守 **`packages/http-next/SKILL.md`**（见上文 **http-next 强制** 段）
- 编辑或新增 **`*.boot.ts` / `*.boot.js`**、**`*.service.ts` / `*.service.js`**（`defineService` 领域模块）、**`*.model.ts` / `*.model.js`**（业务/领域模块）、**`*.controller.ts`**、或涉及 **Hile 服务**（`defineService` / `loadService`）
- 修改 **`packages/*`** 下任意子包源码时，除本 SKILL 外**必须同时阅读并遵守**该包目录下的 **`SKILL.md`**

---

## 2. 包与职责速查（选对模块）

| 场景 | 使用包 | 说明 |
|------|--------|------|
| 定义/加载异步服务、生命周期、依赖图、优雅关闭 | `@hile/core` | 基础容器，所有依赖容器的包都基于它 |
| 启动应用、扫描 boot、容器事件日志、退出钩子 | `@hile/cli` | 与 core 配合，入口为 `hile start` |
| HTTP API：Koa、路由、中间件、文件系统路由 | `@hile/http` | 与 core 集成时在 defineService 内 new Http、load、listen、shutdown(close) |
| API + Next.js SSR 同端口 | `@hile/http-next` | 基于 http；**应用侧 AI 须严格执行 `packages/http-next/SKILL.md`**；默认前缀 `/-`、API 默认 `src/controllers`（可选 `controllerDirectory: "app"`） |
| TypeORM DataSource、事务与补偿回调 | `@hile/typeorm` | 默认导出为 Hile 服务，配合 `auto_load_packages` 或 boot 中 loadService |
| Redis 客户端、环境变量配置、优雅断连 | `@hile/ioredis` | 同上，环境变量 `REDIS_*` |
| 传输无关的请求/响应消息抽象（超时、中止、错误透传） | `@hile/message-modem` | 独立于 core，实现类需实现 `post` / `exec` |
| Node 父子进程 IPC 请求/响应 | `@hile/message-ipc` | 基于 message-modem |
| 主线程与 Worker 线程请求/响应 | `@hile/message-worker-thread` | 基于 message-modem |
| WebSocket 请求/响应 | `@hile/message-ws` | 基于 message-modem + ws |
| 按目录映射消息路由（`*.msg.ts`）、与 message-* 搭配 | `@hile/message-loader` | 独立于 core，`MessageLoader` + `defineMessage` |
| 一键创建 Hile + Next.js 项目 | `create-hile` | `npx create-hile create <name>` |

**依赖关系**：core ← cli / typeorm / ioredis；http ← http-next。message-modem ← message-ipc / message-worker-thread / message-ws。message-loader 可单独与任意 message 传输层搭配。

---

## 3. 跨包强约束（必须遵守）

以下约束适用于所有使用 `@hile/core`、`@hile/cli`、`@hile/http` 的代码。

### 3.1 服务定义与加载（@hile/core）

- 服务**必须**用 `defineService(key, async (shutdown) => { ... })` 定义：第一个参数为 **服务 key**（`string` 或 `symbol`，全局唯一标识该槽位），`shutdown` 参数名建议不变。
- **禁止**在模块顶层写 `const x = await loadService(...)`；只在**函数/服务内部**或 boot 内按需 `loadService`。
- 创建外部资源（连接、服务器、定时器等）后**必须**立即 `shutdown(() => ...)` 注册清理；清理顺序为 LIFO。
- 获取实例**只能**通过 `loadService(service)` 或 `container.resolve(service)`，禁止手造 `{ key, fn, flag }` 等假服务对象。
- **`src/services/`** 下的 **`*.boot.*`** 与 **`*.service.*`** **同属 service 模块**（均基于 **`defineService`** / **`register`**），区别仅在于加载方式：**`*.boot.*`** 由 CLI **进程启动时自动加载**；**`*.service.*`** 在 **boot / 其它服务 / models** 内按需 **`loadService`** **依赖加载**（见 §3.2）。
- **系统逻辑与业务逻辑分层**：**系统/基础设施逻辑**（连接与资源封装、与 Hile 集成、可复用技术能力）**全部**写在 **`src/services/`** 的 **`*.service.*`**（及 **`*.boot.*`** 入口）；**业务/领域逻辑**（用例、规则、面向产品的数据编排）**全部**写在 **`src/models/`** 的 **`*.model.*`**。**`@hile/http-next`** 下：**`src/app/**`** 可直接 **`loadModel(xxxModel)`**（**`xxxModel`** 由 models **`defineModel`** 并导出）；**`src/controllers/**`** **允许** **`loadService`** 与 **`loadModel(xxxModel)`**，**复杂业务**仍建议 **`import`** models 已导出函数；**models** 内组合 **services**（详见 **`packages/http-next/SKILL.md`**，纯 **`@hile/http`** 项目可只遵守 **services** 侧约定）。

### 3.2 Boot 与启动（@hile/cli）

- **`*.boot.ts`** / **`*.boot.js`**：service 模块的一种，**默认导出**为 **`defineService(key, ...)`** 或 **`container.register(key, ...)`** 的返回值，由 CLI **扫描并自启动**。
- Boot 文件**必须**放在 **`src/services/`** 目录下（如 **`src/services/index.boot.ts`**），**禁止**放在 **`src/`** 根或其它非 **`services`** 目录；生产构建对应 **`dist/services/`**。
- `package.json` 中的 **`hile.auto_load_packages`** 仅允许**模块名**（如 `@hile/typeorm`），禁止文件路径。
- 加载顺序固定：先 `auto_load_packages`，再扫描运行目录下的 `*.boot.{ts,js}`。运行目录：`HILE_RUNTIME_DIR` > `--dev` 时 `src/` > 否则 `dist/`。

### 3.3 HTTP 与控制器（@hile/http / @hile/http-next）

- 与 core 集成时：在 **defineService** 内创建 **Http** / **HttpNext**，在 **listen() 之前**完成 `use`、`load`，**listen()** 返回的关闭函数必须传给 **shutdown(close)**。
- 控制器**必须**用 **defineController(method, fn)** 或 **defineController(method, [middlewares], fn)**，文件 **export default** 单个控制器或数组；控制器函数签名为 **(ctx)**，不要 **(ctx, next)**。
- 使用 **@hile/http-next** 时：默认 API 前缀为 **`/-`**；**非 Next 的 API 路由**均在 **`src/controllers/*.controller.ts`**。若放在 **`src/app/`** 与页面同目录，需设置 **`controllerDirectory: "app"`**。
- 使用 **@hile/http-next** 时：**`loadService`** 与直引 **`src/services/**`** **禁止**仅在 **`src/app/**`**。**`src/controllers/**`** **允许** **`loadService`** 与 **`loadModel(xxxModel)`**（**`xxxModel`** 由 **`src/models`** 导出）。**`src/app/**`**：**允许** **`loadModel`**（仅配合 **`src/models`** 导出的 **`xxxModel`**）；**禁止** **`loadService`**、**`defineModel`**（详见 **`packages/http-next/SKILL.md`**）。

### 3.4 数据库与缓存（@hile/typeorm / @hile/ioredis）

- 通过 **loadService(typeormService)** / **loadService(ioredisService)** 获取实例；需在应用启动时即加载时，在 **`hile.auto_load_packages`** 中加入 **`@hile/typeorm`** / **`@hile/ioredis`**。
- TypeORM 事务与补偿使用 **transaction(ds, async (runner, rollback) => { ... })**，禁止在事务外混用 runner 或忽略 rollback 注册。

---

## 4. 按场景的代码导向

- **新建一个“可运行的服务入口”**  
  → 在 **`src/services/`** 下新增 **`*.boot.ts`**（如 **`src/services/http.boot.ts`**），**export default defineService('http', async (shutdown) => { ... })**（或你选定的唯一 key），其中创建 Http/HttpNext 或其它资源并 **shutdown(close)**；**`cwd`** 等路径需按 **`src/services/`** 相对项目根多一层 **`".."`**（见各包 SKILL）。用 **`hile start --dev`** 加载。

- **新增 HTTP API 路由**  
  → 使用 **defineController** 的 **`*.controller.ts`**，放在 http-next 默认的 **`src/controllers/`**（或 **`controllerDirectory`** 指定目录）；**不要**在控制器里写 **ctx.body = ... 再 return**，只 **return** 结果，由响应插件链写 **ctx.body**。

- **API + 页面同端口（Next.js）**  
  → 使用 **@hile/http-next**，在 boot 中 **new HttpNext({ port, cwd, publicPath })**（按需 **`controllerDirectory`**），**shutdown(await httpNext.start())**；默认 API 前缀 **`/-`**，页面用 Next 约定文件（如 **page.tsx**）。

- **使用数据库/Redis**  
  → 在 **package.json** 的 **hile.auto_load_packages** 中加入 **@hile/typeorm** / **@hile/ioredis**，在 **services**、**models**、**boot**、**`src/controllers/**`**（**@hile/http-next**）等**内部** **await loadService(...)**（**`src/app/**`** **禁止** **loadService**，见 **`packages/http-next/SKILL.md`**）；环境变量按各包 README/SKILL 配置。

- **消息通信（IPC/Worker/WS）+ 文件系统路由**  
  → 用 **@hile/message-loader** 的 **MessageLoader** 与 **defineMessage** 做路由表，在 **@hile/message-ipc** / **message-worker-thread** / **message-ws** 子类的 **exec** 中调用 **loader.dispatch(url, data)**。

---

## 5. 各包 SKILL 的引用规则

在**修改或生成**下列目录/包内代码时，**必须**打开并遵守对应 SKILL，再写代码：

**`@hile/http-next`**：凡应用**使用**该包，在编写 **`src/app` / `src/controllers` / `src/models` / `src/services` / boot / `HttpNext` 配置**等任何相关代码前，**必须先读** **`packages/http-next/SKILL.md`**，且**不得遗漏**其中「强约束」类条款（目录、分层、命名、`cwd`、`defineModel` 等）。

| 包路径 | SKILL 路径 | 侧重 |
|--------|------------|------|
| `packages/core` | `packages/core/SKILL.md` | 服务形态、**`services/`** 下 **`.boot`**（自启动）与 **`.service`**（依赖加载）、shutdown、依赖图、事件、反模式 |
| `packages/http` | `packages/http/SKILL.md` | Http、defineController、Loader、响应插件、与 core 集成 |
| `packages/http-next` | `packages/http-next/SKILL.md` | **应用项目须全文遵守**；HttpNext、**`services/*`** vs **`models/*`**、默认 **`src/controllers`**、`start`、`defineModel` / `loadModel` |
| `packages/cli` | `packages/cli/SKILL.md` | boot 须在 `src/services/`、**`*.service.ts`** 领域命名、auto_load_packages、事件日志、退出钩子 |
| `packages/typeorm` | `packages/typeorm/SKILL.md` | DataSource 服务、transaction、rollback、环境变量 |
| `packages/ioredis` | `packages/ioredis/SKILL.md` | 客户端服务、环境变量、断连 |
| `packages/message-modem` | `packages/message-modem/SKILL.md` | MessageModem、post/exec、超时与错误 |
| `packages/message-ipc` | `packages/message-ipc/SKILL.md` | IPC 实现与用法 |
| `packages/message-worker-thread` | `packages/message-worker-thread/SKILL.md` | Worker 实现与用法 |
| `packages/message-ws` | `packages/message-ws/SKILL.md` | WebSocket 实现与用法 |
| `packages/message-loader` | `packages/message-loader/SKILL.md` | MessageLoader、defineMessage、路径映射 |

---

## 6. 常见反模式（禁止）

- 在**模块顶层** **await loadService(...)** 并导出或缓存该实例。
- **Boot 文件** **export default** 普通函数、配置对象或空实现。
- **控制器**中同时写 **ctx.body = ...** 和 **return ...**（应只 **return**，由响应插件写 body）。
- **控制器**签名为 **(ctx, next)** 并调用 **next()**（控制器无 next，需 next 的逻辑放中间件）。
- 在 **@hile/http-next** 中把控制器放在非默认目录却未设置 **`controllerDirectory`**，或自定义 **`controllerPrefix`** 与 Next 页面路由冲突。
- 在 **@hile/http-next** 的 **`src/app/**`** 内**直引** **`src/services/**`** 或 **`loadService`**；或在 **`src/app/**`** **`defineModel`**（见 **`packages/http-next/SKILL.md`**）。
- 将 **`*.boot.{ts,js}`** 放在 **`src/services/`** 外（如 **`src/index.boot.ts`**）。
- 在 **`src/services/`** 内：**依赖加载**的 service 文件名**未**以 **`*.service.{ts,js}`** 结尾，或**自启动**入口**未**以 **`*.boot.{ts,js}`** 结尾。
- **@hile/http-next** 项目中：把**业务/领域逻辑**写在 **`src/services/`**，或把**系统/基础设施**写在 **`src/models/`**；或 **`src/models/`** 内业务模块**未**以 **`*.model.{ts,js}`** 命名。
- **auto_load_packages** 中写相对路径或 `.ts` 文件路径而非模块名。
- 创建 **Http** / **HttpNext** 后未将 **listen()** 返回的关闭函数传给 **shutdown(...)**。
- 使用 **@hile/typeorm** 事务时在 **transaction** 外使用同一 **runner** 或忘记在失败路径注册 **rollback**。

---

## 7. 文档与版本

- 各包**使用方式**以该包 **README.md** 与 **docs/** 为准；**代码生成与约束**以各包 **SKILL.md** 为准。
- 根目录 **README.md** 中的「包一览」与「依赖关系」描述当前仓库包划分与依赖；版本号以各包 **package.json** 为准。

遵守本 SKILL 并结合具体包的 SKILL，可保证生成的 Hile 相关代码与仓库架构一致、可被 CLI 正确加载并优雅关闭。**使用 `@hile/http-next` 的应用还须与 `packages/http-next/SKILL.md` 完全一致，否则视为未通过技能约束。**
