---
name: ui-dev
description: 当需要基于需求文档、设计上下文、UI 设计稿或直接实现指令，按当前业务模块模板创建或扩展前端模块时使用
---

# UI 开发

## 概述

根据需求文档、设计上下文、UI 图或明确的口头描述，在现有业务模块内开发页面与交互，或按当前 mission 指定的业务模块模板搭建新模块。输出必须能直接进入 `api-integrate` 和后续 `module-test`，而不是只交付一个“先能跑起来”的页面。

**核心原则：** 先定位业务模块模板、读取 `template.json`、对齐设计上下文和职责边界，再写具体 UI。结构错了，后面的联调、审计和测试都会变慢。

**违反规则的字面意思就是违反规则的精神。**

## 适用场景

**必须使用：**
- 新建业务模块或页面
- 在现有模块上新增一组完整功能或交互
- 根据 `req-collect` 产出的需求文档实现页面
- 只有 UI 图或明确口头描述，但仍需落到标准模块结构

**例外情况（需征询开发者）：**
- 一次性 PoC 或演示稿，不会进入正式模块体系
- 明确要求保留现有模块结构，本次不按业务模块模板重建

觉得“页面很简单，先糊一个文件再说”？停下来。简单页面最容易因为省结构，把后续每一步都拖慢。

## 铁律

```text
EVERY NEW MODULE STARTS FROM THE CONFIGURED MODULE TEMPLATE - STRUCTURE FIRST, UI SECOND
```

布局里混入请求、状态或业务逻辑，就不是“先把页面写出来”，而是在制造后续联调和测试成本。

**没有例外：**
- 新建模块必须先按 `config.json.moduleTemplate` 定位业务模块模板目录，并读取 `template.json`
- 业务模块模板是完整代码目录，新建模块时整套复制到目标模块路径，再替换占位符
- 必须满足模板 `template.json.requiredFiles`；模板要求保留的空文件也要保留
- `layouts/` 只做展示，不直接发请求，不直接写业务逻辑；如果项目模板使用不同目录名，以模板职责说明为准
- 优先沿用当前业务模块模板的 hooks 组织方式与工程约定，不额外发明一套分层
- 类型先落地，再填实现；禁止一路 `any` 写到底

## 违反后果

如果模块骨架、Hook 链路或布局职责不符合模板，当前实现视为未完成；在继续接口联调、缺陷修复或最终测试前，必须先回退并补齐结构。

## 第 1 步：读取上下文

读取以下信息：
- `.ai/missions/{missionId}/config.json`，确认 `module.name`、模块根路径、上下文和输入来源
- `{projectRoot}/.ai/docs/design-context.md`（如存在）
- `{projectRoot}/.ai/docs/component-catalog.md`（如存在）
- 需求文档或 `req-collect` 产物（如存在）
- UI 图、交互说明、组件清单或用户补充说明

必须先搞清楚：
- 本次是新建模块，还是在现有模块内扩展
- 真实目标模块目录名是什么，是否已经写入 `config.json.module.name`
- 当前 mission 使用哪个 `moduleTemplate.id` 或 `moduleTemplate.root`
- 当前业务模块模板的目录路径、`targetPath`、`requiredFiles`
- 当前项目的主题接入方式是什么，是否存在 `ConfigProvider` 或自定义 Provider 约束
- 哪些颜色、字号、间距、圆角、阴影等必须沿用现有 token / CSS Variables
- 哪些全局组件或 npm 组件必须优先复用，哪些场景才允许新增本地样式或本地组件
- 页面要展示哪些数据，分别有哪些加载态、空态、错误态
- 哪些动作归 `useController`，哪些监听归 `useWatcher`
- 哪些组件可以直接复用，哪些需要新增本地 `components/`

设计上下文读取顺序：
1. `{projectRoot}/.ai/docs/design-context.md`
2. `{projectRoot}/.ai/docs/component-catalog.md`
3. `ui/component-mapping.md`
4. `ui/` 原始素材
5. 当前轮文字描述
6. `reqDocs/req.md` 中已结构化的页面/交互描述

规则：
- 若存在 `component-catalog.md`，新增本地组件前必须先检查是否已有可复用的全局组件或 npm 组件
- 若不存在任何 `design-context.md`，可以继续开发，但必须显式说明“缺少设计上下文，样式仅按通用实现落地”

目标模块路径解析顺序：
1. `config.json.module.name`
2. `reqDocs/req.md` 顶部 `模块名`
3. 若两者冲突、为空，或包含非法路径片段，则返回 `NEEDS_CONTEXT`

**若上下文来自 mission 目录，至少执行：**
- `test -f ".ai/missions/{missionId}/config.json"`
- `find ".ai/missions/{missionId}" -maxdepth 3 -type f | sort`

模板定位规则：
1. `config.json.moduleTemplate.root` 非空时，直接使用该路径
2. 否则使用 `{devFrontendRoot}/references/module-templates/{moduleTemplate.id}`
3. 如果 `moduleTemplate.id` 为空、模板目录不存在、`template.json` 不存在或 `requiredFiles` 缺失，返回 `NEEDS_CONTEXT` / `BLOCKED`

## 第 2 步：搭建骨架（仅新建模块时）

以当前业务模块模板为准：
- 模板目录
- `template.json`
- `template.json.targetPath`
- `template.json.requiredFiles`
- `../../references/rules/frontend-code-rules.md`

新建模块规则：
- 将业务模块模板目录完整复制到目标模块路径
- 复制时排除 `template.json` 等非代码说明文件
- 复制后替换模块名、显示名、路由名等当前模板中的占位符
- 按真实业务删除或替换占位符、示例组件、示例接口和示例数据

内置 `m9-module` 目标结构至少包含：

```text
{moduleRoot}/{module.name}/
├── index.tsx
├── defs/
│   ├── constant.ts
│   ├── type.ts
│   └── service.ts
├── hooks/
│   ├── index.ts
│   ├── useData.ts
│   ├── useController.ts
│   └── useWatcher.ts
├── layouts/
│   ├── index.ts
│   └── Default/
│       ├── index.tsx
│       └── style.module.less
├── __test__/
│   ├── index.tsx
│   └── mock.ts
└── utils.ts
```

说明：
- `components/` 为按需目录；如果存在，必须补 `components/index.ts`
- 模板里的示例占位代码可以作为起点，但交付前必须替换或删除
- 已有模块扩展时，不重建目录；在现有结构上补缺文件并对齐命名

错误示例：

```text
{moduleRoot}/{module.name}/
├── index.tsx
└── page.tsx
```

这不满足内置 `m9-module` 的业务模块模板，只是临时页面。若项目模板本身就是扁平页面结构，则必须在该模板的 `template.json.requiredFiles` 中明确声明。

**至少执行：**
- `find "{targetModulePath}" -maxdepth 3 -type f | sort`
- 按 `template.requiredFiles` 逐项确认文件存在
- 内置 `m9-module` 至少执行：`rg -n "__MODULE_NAME__|exampleFn|queryExample|ExampleChildComponent" "{targetModulePath}"`
- 内置 `m9-module` 至少执行：`rg -n "useState|useCallback|useMemo|index\\.module\\.less" "{targetModulePath}"`

## 第 3 步：先定义契约（defs/）

先写 `defs/`，再写实现。最低要求：
- `constant.ts`：真实的 `MODULE_NAME`、`LayoutEnum` 及静态配置
- `type.ts`：补齐并连通 `ModuleRef`、`Props`、`DataParams`、`CtrlParams`、`WatcherParams`、`LayoutProps`、`DataState`
- `service.ts`：先保留 service 壳或占位实现，后续由 `api-integrate` 替换为真实接口

约束：
- 字段名、枚举值、回调签名先定下来，再让 Hook 和布局围绕它实现
- 新类型是扩展既有类型链，不是随手另起一套命名
- 可空字段用 `| null` 表达，不用 `?` 假装“可选”

## 第 4 步：实现 Hook 链

顺序固定：
1. `useData.ts`：状态、派生数据、请求触发入口
2. `useController.ts`：事件处理与业务动作
3. `useWatcher.ts`：初始化和监听副作用
4. `hooks/index.ts`：编排 `useData -> useController -> useWatcher`

约束：
- `useController` 通过参数接收 `data`，不跨层直接拿状态
- `useWatcher` 只处理监听和初始化，不把主要请求逻辑塞进去
- `hooks/index.ts` 最终返回 `data` 和 `controllers`
- 默认遵循 `../../references/rules/frontend-code-rules.md` 的 ahooks 映射；如果模板示例仍保留旧写法，以 `frontend-code-rules.md` 为准

## 第 5 步：实现布局与组件

布局入口必须是纯展示层。内置 `m9-module` 的默认入口是 `layouts/Default/index.tsx`：
- 只接收 `data` 和 `controllers`
- 不写请求，不持有业务状态，不绕过 Hook 直接操作 service
- 样式文件统一使用 `style.module.less`
- 通过 `classNames` + CSS Modules 组织样式
- 如存在 `design-context.md`，优先复用其中约定的项目组件、token 与 CSS Variables
- 只有现有主题体系无法表达需求时，才允许新增局部样式；新增样式时仍应优先引用既有 token
- 如果项目通过 `ConfigProvider` 或自定义 Provider 注入 token，不要绕过这条链路另写一套视觉常量

本地 `components/`：
- 只有在现成组件不满足需求时才新增
- 每个组件单独目录，使用 `index.tsx` + `style.module.less`
- 保持“展示组件优先”，不要把模块业务逻辑挪进局部组件
- 新增本地组件前，先确认 `component-catalog.md` 中是否已有可复用全局组件或 npm 组件

## 第 6 步：收尾校验

逐项检查：
- [ ] 已定位业务模块模板目录，并读取 `template.json`
- [ ] 新模块结构满足模板 `requiredFiles`
- [ ] 模板入口文件只负责模块组装，不写业务逻辑
- [ ] 类型链完整且能连通；内置 `m9-module` 至少检查 `defs/type.ts`
- [ ] Hook 编排符合模板契约；内置 `m9-module` 保持 `useData -> useController -> useWatcher`
- [ ] 布局映射符合模板契约；内置 `m9-module` 检查 `layouts/index.ts` 的 `LayoutEnum.Default -> Default` 映射
- [ ] 布局和组件样式文件符合当前业务模块模板命名约定
- [ ] 布局层只消费 `data` / `controllers`
- [ ] 如存在 `design-context.md`，实现已遵循其中的主题接入、token 复用和组件优先级约束
- [ ] 无新增的硬编码颜色、字号、间距、圆角、阴影等视觉体系常量
- [ ] 未绕过项目既有 `ConfigProvider` / 自定义 Provider / CSS Variables 另写一套主题
- [ ] 无模板占位符、示例组件、示例接口和当前模板禁用写法残留
- [ ] `requiredFiles` 中声明的空文件也已保留

**至少执行：**
- 内置 `m9-module`：`rg -n "__MODULE_NAME__|exampleFn|queryExample|ExampleChildComponent" "{targetModulePath}"`
- 内置 `m9-module`：`rg -n "useState|useCallback|useMemo|index\\.module\\.less" "{targetModulePath}"`
- `find "{targetModulePath}" -maxdepth 3 -type f | sort`

## 速查表

| 阶段 | 关键动作 | 完成标准 |
|------|---------|---------|
| 读取上下文 | 确认模块边界、数据和交互 | 明确本次是新建还是扩展，输入信息足够落地 |
| 搭建骨架 | 对齐当前业务模块模板 | 文件树和命名符合模板 `requiredFiles` |
| 定义契约 | 先写 `defs/` | 类型链和静态配置可支撑后续实现 |
| 实现 Hook | 按固定顺序落地 | 数据、控制器、副作用职责清晰 |
| 实现布局 | 保持展示层纯净 | 布局不直接碰 service 和业务状态 |
| 收尾校验 | 扫描结构和禁用模式 | 无模板残留和结构性违规 |

## 常见借口

| 借口 | 现实 |
|------|------|
| “这个页面太简单了，不需要 Hook” | 再简单的页面也会从一致的结构中受益 |
| “先堆在一个文件里，后面再拆” | 后面通常不会拆，而且联调时更难拆 |
| “一个字段没必要用 `useSetState`” | 一致性比这点微优化更重要 |
| “布局里放一个小处理函数没关系” | 放到 `useController`，展示层不要偷带逻辑 |
| “现在没副作用，`useWatcher.ts` 可以不建” | 空文件也是契约的一部分，后面会省事 |

## 危险信号 - 立即停下来重做

- 你在布局组件中使用 `useEffect`、`useState` 或直接导入 service
- 你创建了扁平模块，没有 `defs/`、`hooks/`、`layouts/` 分层
- 你在 `index.tsx` 里编写业务逻辑，而不是只组装模块
- 你跳过类型链，直接用 `any` 或匿名对象向下传
- 你保留了模板占位符，打算“联调时再说”

## 参考文档

| 主题 | 文件 |
|------|------|
| 通用规则 | `../../references/rules/common-rules.md` |
| 内置业务模块模板 | `../../references/module-templates/{templateId}/` |
| 业务侧与工程侧代码规则 | `../../references/rules/frontend-code-rules.md` |

## 集成关系

- **可选上游：** `req-collect`
- **直接下游：** `api-integrate`
- **主测试阶段：** `module-test`
- **失败回流：** `bug-fix`
