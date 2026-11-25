---
name: resource-management-capability
description: 在 mastra-agent 控制台为某类资源（模型/工具/Agent…）补齐管理能力的端到端流程。当用户要求「让 X 管理更智能」「X 登记后不能验证/不能编辑」「给 X 加测试调用/编辑/删掉/列表操作列」，或需要新增一个控制面接口并贯通到控制台时使用。覆盖契约 → 后端 → SDK 生成 → 控制台 → 测试 → 全量校验的完整顺序与全部已知坑位。
agent_created: true
---

# 为资源补齐管理能力（契约 → 后端 → 控制台）

这个仓库已经用同一套流程做过三轮：轨迹采集、模型管理智能化、工具管理补齐。流程固定，坑位固定，照抄顺序即可。

## 「界面已更新但接口不存在」= 旧的后端进程，不是网络问题

**先查这个，别急着改代码。** 前端由 Vite 提供，源码一改 HMR 立刻生效；控制面在
`scripts/dev.ts` 里是独立进程。两者版本不一致时，界面是新的、接口是旧的。

一条命令定位（运行中的服务 vs 仓库生成版）：

```bash
curl -s http://127.0.0.1:4110/openapi.json -o /tmp/live.json
python3 -c "
import json
live=set(json.load(open('/tmp/live.json'))['paths'])
repo=set(json.load(open('packages/contracts/openapi/platform.json'))['paths'])
print('缺失接口:', sorted(repo-live))
"
```

另一个判据在控制面日志里：命中的路由是 `route: "/api/v1/..."`（matched），
未知路由是 `route: "unmatched"`。

`scripts/dev.ts` 的控制面已加 `--watch`（用 node 自带的 `--watch`，
**不要用 `tsx watch`——它会丢掉 `--conditions=development`**，那样工作区包会去读 `dist`）。
Runtime 仍是直跑无 watch，改 Runtime 后仍需手动重启。

## 错误文案：不要把「原因」写错

`apps/console/src/shared/api.ts` 的 `unwrap` 是所有请求失败的唯一出口，**68 个调用点**。
Hono 对**未知路由返回纯文本 `404 Not Found`**（非 `{code,message}`），
SDK 客户端对非 JSON 响应体是 `throw textError`——所以 `error` 可能是**字符串**。

判据顺序按「信息具体程度」排，且**必须先用 `response.status` 判断，再判断 error 形状**：

1. `response === undefined` → 真的连不上（**必须最先判**：传输层的 `TypeError` 也带 `.message`，
   否则会把 `fetch failed` 原文显示给用户）。
2. error 是带 `message` 的对象 → 用服务端原文（最具体）。
3. 404 → 平台没有这个接口，提示后端可能未更新。
4. 5xx 无错误体 → 带状态码说明。

写界面文案时**不要预设请求是否发出**：「请求未发出」在 404 时是错的（请求发出了，
后端没这个路由）。说「没能获取/完成」+ 详情里给原因。

## 铁律：漏一步就报错

改契约后必须按序执行，**第 4 步最容易漏**：

1. `packages/contracts/src/<域>.ts` 定义 Input/Output schema。
2. `apps/control-plane/src/modules/<模块>/` 写实现 + `routes.ts` 注册 `operationId`。
3. `pnpm sdk:generate`（HeyAPI）重新生成 OpenAPI 与 SDK。
4. **`pnpm sdk:build`** —— 控制台通过 `@platform/sdk` 的 `dist` 解析。不重建会出现
   `Property 'xxx' does not exist on type 'typeof import(".../sdk/dist/index")'`。
5. `apps/console/src/features/<域>/` 实现 + 贯通 plumbing（见下）。
6. 测试：契约 `tests/contracts/`、后端 `tests/integration/`、前端 `apps/console/tests/`。
7. `pnpm check`。

## 契约层要点

- 契约是单一事实来源。
- **`export type ToolInput = z.infer<typeof ToolInput>`，不要用 `z.input`。** `z.input` 会让带 `.default()` 的字段变成 `T | undefined`，
  传进要求具体类型的参数时 TS 报错（`resources.ts` 里已经踩过两次：模型轮、工具轮）。
- **zod 4：`.default({})` 在 `.strict()` 对象上会短路内层默认值**，旧行解析直接失败。必须用 `.prefault({})`。
- 人可手写的枚举要和系统投影的枚举分开。例：`AuthoredToolKind = z.enum(["sum","http_get"])` vs `Tool.kind` 含 `mcp`。
  列表/编辑器用窄的，存储/读取用宽的。
- 探测类接口的 outcome **每个值对应一种修法**，不要退化成 `ok/fail`。工具的六态：
  `ok / invalid（样例参数不合 schema）/ rejected（对端拒绝）/ mismatch（返回过不了 outputSchema）/ unreachable / timeout`。
  `mismatch` 是唯一靠改 outputSchema 修的，必须在界面上说清。
- `Id` 是 `z.uuid()`：测试夹具必须写真 UUID，不能写 `"model-1"`。

## 后端要点

- 有界读取 / 超时 / provider 原文提取统一放 `resources/transport.ts`，探测与列表共用。
- **探测必须复现 Runtime 的真实调用方式**，否则探测通过而运行失败。要点：
  - `http_get` 把输入拼进查询参数（字符串直传、其余 `JSON.stringify`）、GET、**超时 `10000ms`（Runtime 的值，不要沿用控制面的 15000）**、要求 JSON、过 `outputSchema`。
  - `sum` 是本地求值，不发请求。
- 凭据解析用同一个泛化方法（`resolveKey(actor, projectId, kind, supplied, credentialFrom)`），靠 `kind` 隔离，避免模型/工具 token 串路。
- 编辑时留空凭据 = 保留已存值；不要写成覆盖成空。
- 系统投影出来的资源明确拒改：MCP 工具 `409 MCP_TOOL_IMMUTABLE`，并拒绝对它做 `mcp` 类型的探测。
- 坏 schema 要**显式 400 `INVALID_TOOL_SCHEMA`**，不要静默存进去。

## 控制台 plumbing（新资源或把资源接进编辑器时）

1. `apps/console/src/app/routing/context.ts`：`EditorResource = Agent | Model | Tool | ...`。
2. `apps/console/src/app/ProjectConsole.tsx`：`editing` 状态带 `resource?`，加 `openEditor(kind, resource?)` 直通（**传资源=编辑，不传=新建**）。
3. `apps/console/src/app/EditorHost.tsx`：接住并透传给具体编辑器。
4. `apps/console/src/app/routing/ProjectPage.tsx`：列表 `onEdit={(r) => openEditor("<kind>", r)}`。
5. 编辑器统一走 `shared/EditorForm`（抽屉 + 提交生命周期）。

## 前端交互坑（都真实踩过）

- **SDK 客户端把 HTTP 失败解析为 `error` 值，不 reject**：`api.xxx().catch(...)` 永不触发，失败时静默渲染空列表。
  必须检查 `response.error`。
- **`Form.useWatch` 首次返回 `undefined`**，真实值下一次渲染才到。用 effect 依赖它清状态会在探测完成那刻误清。
  正解：把「探测实际用到的值」拼成签名随结果保存，渲染时比对，**不要用 effect 清**。
- **`form.validateFields([...])` 只返回被验证的子集**，不是全量值。要全量得在验证后调 `form.getFieldsValue()`。
  踩过的表现：只验证 `input` 时 `values.url` 是 `undefined` → 校验失败 → 点「测试」没反应。
  正解：先 `form.getFieldValue("kind")` 决定验证哪些字段，再取全量构建请求。
- 前端先本地 `JSON.parse` 校验用户填的 schema，非法就本地报错、**零请求**。
- 结果区要展示**实际发出的请求 URL**，让用户能自己复核对端。
- `unreachable` / `timeout` 的文案只说「平台网络连不上」，不要暗示用户配置错了。
- 用 `useEffect` 调组件内定义的 async 函数会被 biome 的 `useExhaustiveDependencies` 拦下；
  直接把函数加进依赖数组会导致每次渲染重跑。要**用 `useCallback` 包住**再依赖它。
- 请求失败要**可见**：只塞进字段的 `extra` 或留个空下拉，会被读成「本来就没有数据」。
  给独立的 Alert + 重试按钮，并说明该数据是否影响保存。
- antd `Select` + `showSearch` **不能自由输入**；要「建议 + 自由填写」用 `AutoComplete`。
  且 `AutoComplete` 的**预填值本身就是过滤词**（编辑已有值时建议会被过滤空），这是 antd 默认行为，测试按真实用法写。
- 主题是浅色：底色 `#f6f8f7`、文字 `#263b36`、主色 `#246b59`、边框 `#e5ece7`、次要文字 `#809087`。
- antd 是 **v6**：`Alert` 用 `title`（不是 `message`）+ `description`。

## 测试要点

- 可选字段 label 渲染成 `名称(optional)`，精确 `getByLabelText` 会失败 → 用 `screen.getByLabelText(new RegExp(text))`。
- 集成测试需要本地 Postgres（`compose.yaml`，127.0.0.1:5442），先 `pnpm db:migrate`。
- 探测类测试用真实 HTTP 夹具覆盖每个 outcome，不要 mock 掉——mock 会掩盖「探测方式与 Runtime 不一致」这个最关键的缺陷。
- **`tests/**` 引用契约必须用相对路径 `../../packages/contracts/src/index.ts`**：根 `node_modules/@platform` 只链接了 `database`，没有 `contracts`。`apps/**` 内用 `@platform/contracts` 正常。

## 校验

- `pnpm check` = lint + architecture:check + build + sdk:check + test + test:console。
- `pnpm format` **只格式化，不整理 import 顺序**；格式化后必须再跑 `pnpm lint` 才能发现导入顺序问题（或直接 `npx biome check --write`）。
- 跳过项是「需要专用镜像的 Docker 沙箱测试」，**不计为通过**。
- 架构约束在 `.dependency-cruiser.cjs`：`console/features` 不能依赖 `app/`，`contracts` 不能导入自身 barrel。

## 交付收尾

- 写 `docs/research/<主题>-YYYY-MM-DD.md`：改了什么、验收数据、**未实施项**。
- 未实施项要在文档和回复里都写明（如：删除需引用判定、SSRF 未完全消除、无浏览器实测）。
