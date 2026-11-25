---
name: frontend-module-api-digest
description: >-
  调研任意前端视图（页面 / 路由 / Section / Tab / 弹窗 / 抽屉 / Dashboard 卡片 / 图表 / 筛选表单 / 列表 / 详情页等）中的功能模块，汇总每个模块展示了哪些字段（label、value 字段、列表 column、筛选条件、统计指标）以及对应的查询接口。
  当用户说“调研/汇总某某页面（或模块）下的展示内容”“各有哪些字段和接口”“字段映射是什么”“这个字段来自哪个接口”“这些 code 如何展示成名称”“筛选条件调了哪些接口”“Dashboard 这个卡片的数据从哪来”等诉求时触发——即使没有明确说“汇总接口”，只要是在梳理某个视图/模块的展示内容与数据来源，就使用本 skill。
  适用于 React / UMI / Vue 等前端仓库中按“视图 -> 模块 -> 字段/列表/指标 -> 接口”结构做数据来源梳理的场景。
---

# 前端模块与接口汇总

帮助用户把任意一个前端视图（页面、路由、Section / Tab、弹窗、抽屉、Dashboard 卡片、图表、筛选表单、列表、详情页……）拆解成：
**功能模块 -> 展示字段（label / 字段 key / 列表 column / 筛选条件 / 统计指标）-> 对应的查询接口**，并输出结构化 Markdown 表格。

本 skill 不限定视图类型：详情页、列表页只是其中两种常见形态；总览看板、浮层、表单筛选区同样适用。

## 核心原则（这些是用户反复强调的，务必遵守）

1. **只汇总查询接口，不要增删改接口。**
   - 保留：`GET`，以及用于查询的 `POST`（如 `/page`、`/list`、`/get`、`/query` 之类）。
   - 剔除：`add` / `create` / `update` / `save` / `delete` / `remove` / `changeStatus` 等写操作接口——除非用户明确要求。

2. **给接口地址，不要给代码里的方法名。**
   - 输出 `GET /api/xxx/yyy`，而不是 `getApiXxxYyy`。
   - 方法名（如 `getApiCrmLeadGet`）只用于你内部定位，最终展示要还原成真实的 HTTP 方法 + 路径。

3. **精确区分字段的真实数据来源，不要想当然地归到一个接口。**
   - 同一个模块里的字段，可能来自**多个不同接口**（例如一部分来自 `/lead/get`，一部分来自 `/lead/keyPlayers/get`；Dashboard 一个卡片可能是聚合接口，另一个卡片是独立接口）。
   - 一定要读组件源码，确认每个字段实际从哪个 API 响应对象取值，再归类。存疑时明确标注“待核实”。

4. **完整追踪 code -> name 的映射链路。**
   - 很多字段接口只返回 id/code（如 `salespersonId`、`billingState: "3920"`、`type: 0`），页面展示的却是名称。
   - 必须查清名称来自哪里：另一个列表接口、前端硬编码常量、Zustand store、还是某个 hook。
   - **要追到链路的最上游**：如果映射用到的列表接口本身还需要入参（如 `state/list/by/countries` 的 `countryIds` 来自 `country/list`），把这一级也交代清楚。

5. **按视图类型选择合适的“字段”口径，不要把不同形态混在一起。**
   - 列表类视图：默认只汇总列表视图的 column，不要混入编辑/新建/Grid 卡片视图的表单字段，除非用户要求。
   - 表单/筛选条件类：汇总字段 key + 控件类型 + 选项来源，而非“只读/可编辑”。
   - 图表/统计卡片类：汇总指标名 + 维度 + 取值字段，并指明是单值还是序列。
   - 详情类：汇总 label + 字段 key + 数据来源。

## 工作流程

### 1. 定位视图与模块
- 先和用户确认要梳理的“视图”范围（某个页面/路由、某个 Section/Tab、某个弹窗/抽屉、某张卡片/图表、某个筛选区），避免范围漂移。
- 用 Explore/general-purpose 子代理做广度搜索，按视图名、路由、Section/Tab 标题、组件名、弹窗 trigger 去找。
- 独立的模块可**并行**派多个子代理分别调研（每个子代理任务自包含）。
- 让子代理**完整读取**相关组件源码，抽取：字段 label / 表单字段 key / 列表 column field / 筛选项 / 统计指标，以及每个数据获取调用。

### 2. 还原接口地址
- 定位数据获取调用后，去 `services/`（或等价目录）里找对应函数定义，读出真实的 HTTP method 与 path。
- 剔除写操作接口（见原则 1）。

### 3. 追踪字段来源与 code->name 映射
- 对每个字段，确认它来自哪个 API 响应或 store（原则 3）。
- 对 id/code 字段，查清名称映射来源与完整链路（原则 4）。
- 对图表/统计卡片，确认序列数据是单接口多组、还是多接口拼装。

### 4. 输出结构化汇总
按视图类型选择对应的输出模板（见下）。每个模块先给主查询接口，再给字段/列表/指标表格；最后给一张全局“查询接口汇总表”。

## 输出格式示例

### 详情/表单类模块

````markdown
## <视图名>

### <模块名 A>（表单类）

**查询接口：** `GET /api/xxx/get`

| # | Label | 字段 key | 类型 | 可编辑 |
|---|---|---|---|---|
| 1 | Project | `projectName` | 只读文本 | 否 |
| 2 | Name | `name` | 文本输入 | 是 |

**下拉/映射来源：**
- Service：`GET /api/xxx/options`
- Priority：前端硬编码（High / Medium / Low）
````

### 列表类模块

````markdown
### <模块名 B>（列表类）

**查询接口：** `POST /api/xxx/page`

| Column | 字段 key | 备注 |
|---|---|---|
| Salesperson | `salespersonId` | 用 `resEmployeeList` 按 `userId` 匹配取 `fullName`（`GET /api/.../getSalesperson`） |
| Type | `type` | 前端常量 TYPE_LIST 映射（0=Email, 1=Phone） |
````

### 筛选条件类模块

````markdown
### <模块名 C>（筛选条件）

**选项接口：** `GET /api/xxx/options`（一次拉回多个下拉）

| 筛选项 | 字段 key | 控件 | 选项来源 |
|---|---|---|---|
| Status | `status` | 单选 | `GET /api/xxx/status/list` |
| Date range | `startDate`/`endDate` | 日期区间 | 无接口，用户输入 |
````

### Dashboard / 图表 / 统计卡片类模块

````markdown
### <模块名 D>（统计卡片）

**查询接口：** `GET /api/xxx/stat/summary`

| 指标 | 取值字段 | 备注 |
|---|---|---|
| Total revenue | `totalRevenue` | 单值，单位元 |
| Active users | `activeUserCount` | 单值 |

### <模块名 E>（图表）

**查询接口：** `POST /api/xxx/stat/trend`

| 维度 | 序列字段 | 备注 |
|---|---|---|
| 日期（X 轴） | `date` | 按天 |
| 成交额（Y 轴） | `amount` | 来自 `series[0].amount` |
````

### 全局查询接口汇总

````markdown
---

## 查询接口汇总

| 模块 | 接口 | Method | 用途 |
|---|---|---|---|
| 模块 A | `/api/xxx/get` | GET | 详情数据 |
| 模块 A | `/api/xxx/options` | GET | Service 下拉选项 |
| 模块 B | `/api/xxx/page` | POST | 列表数据 |
| 模块 B | `/api/.../getSalesperson` | GET | Salesperson id->name 映射 |
| 模块 D | `/api/xxx/stat/summary` | GET | 统计卡片汇总 |
| 模块 E | `/api/xxx/stat/trend` | POST | 图表趋势序列 |
````

## 常见模式提示（不同仓库不同，仅供加速定位，不是硬规则）

- **自动生成的 service 层**：函数常按 `<method>Api<Path>` 命名（如 `getApiCrmLeadGet` ↔ `GET /api/crm/lead/get`）。真实路径通常写在函数体的 `request('/api/...', { method })` 里，以此为准。
- **详情数据常来自共享 store**（Zustand / dva model）而非组件内直接请求——顺着 `useXxxStore`、`fetchXxx` 往上找到真正的接口。
- **code->name 映射的常见形态**：
  - 员工/用户：另调一个员工列表接口，按 `userId` 匹配取 `fullName`。
  - 枚举/类型：前端硬编码常量数组，按 `value` 匹配取 `label`。
  - 省市/地区：级联接口，城市列表依赖 state、state 列表依赖 country。
  - 状态颜色/文案：状态码经 enum 映射成数字或名称，再查颜色/样式表。
- **只返回 code 的字段**若对应列表未加载或未命中，页面通常**原样显示 code**——值得在结论里点明这个边界。
- **Dashboard / 图表常见形态**：
  - 单卡片单接口（`/stat/summary` 一次返回多个指标）。
  - 多卡片共享一个聚合接口，按字段拆分展示。
  - 图表序列可能是接口直接返回 `series`，也可能是前端按维度二次分组；务必读图表组件的 data transform 逻辑再下结论。
- **弹窗 / 抽屉常见形态**：
  - 打开时才触发请求（`onOpen` / `useEffect` 依赖 visible），容易被漏看——确认 visible 变化时的 effect。
  - 数据可能复用父级已加载的 store，而非独立请求。
- **筛选条件常见形态**：
  - 选项接口常在页面初始化时**一次拉回多个下拉**（如 `/options` 返回 `{ statusList, typeList }`），不要误判为每项单独请求。
  - 级联筛选（省->市->区）需把依赖关系和上游入参来源一并交代。
