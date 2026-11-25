---
name: module-template-skill
description: 当需要根据现有业务模块模板创建新前端业务模块，或审查/修正现有业务模块是否符合当前模板代码规范时使用。用户提到“创建业务模板模块”、“复制 module-template”、“检查模板规范”、“review 业务模板代码”、“补模块注册”等场景都应使用本技能。
---

# 业务模块模板

## 概述

本技能处理两类任务：

1. 根据用户要求，从 `packages/dev-frontend/references/module-templates` 或项目内 `.ai/dev-frontend/references/module-templates` 选择合适模板，复制为新的业务模块，并替换占位符。
2. 审查已有业务模块是否符合其模板规范；发现不合理实现时直接调整。

创建和审查共享同一套模板定位、占位符、注册文件和模板规则读取逻辑。创建模板本身较轻，所以放在同一个技能里。

## 核心原则

- 业务模块模板是可复制的完整代码目录，不是文档片段。
- 除非用户明确要求重构模板本身，否则不要修改模板源目录；创建模块时修改目标业务模块。
- 模板选择、模块命名、目标路径不明确时先从项目上下文推断；无法可靠判断时再问用户。
- 不要把注册文件路径写死为某个项目的固定路径，要通过现有代码结构发现。
- Review 时以当前模块所属模板的规则为准；如果模板目录内有 `rule.md` 或 `rules/`，优先读取。

## 适用输入

用户可能提供：

- 模板 ID，例如 `m9-module`、`gz-module`
- 中文模块名，例如 `模拟推算表单`
- 英文模块名/目录名，例如 `SimulatedEstimation`
- 目标路径，例如 `src/modules/SimulatedEstimation`
- 现有模块路径，用于 review

缺失信息时按本技能的推断顺序处理。

## Workflow A：创建业务模块

### 1. 读取上下文

先确认当前仓库和可用模板：

- 读取项目根 `AGENTS.md` 或相关说明。
- 查找模板目录：
  1. 当前项目 `.ai/dev-frontend/references/module-templates/{templateId}`
  2. 当前仓库 `packages/dev-frontend/references/module-templates/{templateId}`
  3. 如果用户给了绝对模板路径，直接使用该路径
- 读取候选模板的 `template.json`、`README.md`、`rule.md` 或 `rules/`。

模板选择规则：

1. 用户明确指定模板 ID 或路径时使用该模板。
2. 未指定时，先检查当前项目是否只有一种业务模板；如果只有一种，使用它。
3. 如果项目已有同类模块，读取已有模块结构、状态管理方式、导出注册方式，选择最接近的模板。
4. 如果仍无法判断，询问用户使用哪个模板。

### 2. 补齐模块名和目标路径

需要两个占位符值：

- `__MODULE_NAME_EN__`：英文模块名，通常是目录名或模块唯一标识。
- `__MODULE_NAME__`：中文模块名，通常用于注释、展示名或文档。

命名规则：

- 用户同时给出中文和英文时直接使用。
- 只给英文时，不要臆造中文；询问用户中文名。
- 只给中文时，可以给出建议英文名，但需要用户确认。
- 英文名必须可作为目录名和 TypeScript 标识相关名称使用；发现空格、斜杠、特殊字符时先规范化并确认。

目标路径规则：

1. 用户明确给出目标路径时使用该路径。
2. 如果有 mission `config.json`，按 `module.name`、`moduleRoot` 和模板 `targetPath` 渲染。
3. 如果项目有明显业务模块根目录，例如多个模块都在同一 `modules/` 目录下，则使用该目录加英文模块名。
4. 如果无法判断应放的位置，询问用户。

### 3. 复制模板

复制模板时：

- 将模板目录的完整代码树复制到目标模块路径。
- 排除 `template.json`、`README.md`、`rule.md`、`rules/` 等模板说明文件。
- 保留模板声明的空文件。
- 如果目标路径已存在，先读取并确认内容；不要覆盖用户已有实现，除非用户明确要求覆盖或 review 调整。

复制后执行占位符替换：

- 替换所有文本文件中的 `__MODULE_NAME_EN__`
- 替换所有文本文件中的 `__MODULE_NAME__`

当前只处理这两个占位符；发现其它 `__PLACEHOLDER__` 时列出并询问处理方式。

### 4. 自动补关联文件

创建模块后，尝试自动补模块注册和导出。

不要写死注册文件路径。按以下方式发现：

1. 从目标模块目录向上找最近的模块根目录，例如包含多个模块子目录的目录。
2. 在模块根目录下查找聚合导出文件，常见特征：
   - `index.ts`
   - `index.tsx`
   - 包含 `export { default as Xxx } from "./Xxx"`
   - 包含 `export type { ModuleRef as XxxRef } from "./Xxx"`
3. 在模块根目录下查找模块映射文件，常见特征：
   - `Modules.ts`
   - `Modules.tsx`
   - 包含 `export const ModuleComponents = { ... }`
   - 多个同级模块 import 后放入对象
4. 如果发现多个候选，读取内容后选择与已有模块注册风格一致的文件。
5. 如果没有发现候选，不新建注册体系；向用户说明未发现自动注册位置。

注册补齐规则：

- 保持已有排序风格；如果没有明显排序，追加到同类导出末尾。
- 聚合导出文件通常补：
  - `export { default as ModuleName } from "./ModuleName";`
  - `export type { ModuleRef as ModuleNameRef } from "./ModuleName";`
- `ModuleComponents` 文件通常补：
  - `import ModuleName from "./ModuleName";`
  - 在 `ModuleComponents` 对象中加入 `ModuleName`
- 不要修改业务无关的注册文件。
- 如果目标项目使用路由、菜单或插件注册，还要先读取现有模式；无法确定时不要猜。

### 5. 创建后自检

至少检查：

- 目标目录文件树满足模板 `template.json.requiredFiles`。
- 不存在未处理的 `__MODULE_NAME_EN__`、`__MODULE_NAME__`。
- 新模块入口只做模块组装，不写业务逻辑。
- `defs/`、`hooks/`、`layouts/` 结构与模板一致。
- 关联导出和 `ModuleComponents` 已按项目风格补齐，或明确说明未发现注册点。

建议命令：

```bash
find "{targetModulePath}" -maxdepth 4 -type f | sort
rg -n "__MODULE_NAME_EN__|__MODULE_NAME__" "{targetModulePath}"
rg -n "export \\{ default as|ModuleComponents|ModuleRef as" "{moduleRoot}"
```

## Workflow B：Review 并修正业务模块

### 1. 定位模块与模板

先确认 review 的目标模块路径。

模板定位顺序：

1. 用户明确指定模板 ID 或路径。
2. 读取 mission `config.json.moduleTemplate`。
3. 对比目标模块文件树与可用模板的 `requiredFiles`，选择匹配度最高的模板。
4. 如果无法判断，询问用户。

### 2. 读取模板规则

规则读取顺序：

1. `{templateDir}/rule.md`
2. `{templateDir}/rules/`
3. `{templateDir}/README.md`
4. `packages/dev-frontend/references/rules/frontend-code-rules.md`
5. 模板源码文件顶部注释中的规范

如果模板有专属规则，以专属规则优先。不同项目各自通常只使用一种模板，不要把其它模板的约定混进当前模块。

### 3. 审查维度

按模板要求检查并直接修正：

- 文件结构是否满足 `template.json.requiredFiles`。
- 入口文件是否只做模块组装。
- `defs/constant.ts`、`defs/type.ts`、`defs/service.ts` 是否职责清楚。
- `hooks/index.ts` 是否按模板编排 `useData -> useController -> useWatcher`。
- `useData` 是否集中状态、请求和派生数据。
- `useController` 是否集中事件和业务动作。
- `useWatcher` 是否只处理初始化和监听副作用。
- `layouts/` 是否保持展示层，不直接发请求、不直接持有业务状态。
- 本地 `components/` 是否为展示组件，且通过 `components/index.ts` 管理。
- 状态管理是否符合模板：
  - Jotai 模板检查 `moduleAtom`、`.atom`、`useAtomState`、`p.atoms`。
  - Zustand 模板检查 `moduleStore`、`.store`、`useZustandState`、`p.stores`。
- 是否存在模板占位符、示例接口、示例组件和明显残留。

### 4. 修正规则

- 优先做最小改动，让现有模块回到模板规范。
- 不因为 review 顺手重写业务逻辑，除非现有写法违反模板职责边界。
- 不删除用户业务代码；需要移动职责时，保留行为并把代码移动到模板规定层。
- 修正后更新相关类型链，确保 `Props`、`DataParams`、`CtrlParams`、`WatcherParams`、`LayoutProps` 能连通。
- 如果模板要求新增 `rule.md`，可以在模板目录补专属规则文件；不要在每个业务模块重复复制规则文档。

### 5. Review 后自检

至少执行：

```bash
find "{targetModulePath}" -maxdepth 4 -type f | sort
rg -n "__MODULE_NAME_EN__|__MODULE_NAME__|ExampleChildComponent|queryExample|exampleFn" "{targetModulePath}"
```

如果是 Jotai 模板：

```bash
rg -n "moduleAtom|useAtomState|\\.atom|p\\.atoms" "{targetModulePath}"
```

如果是 Zustand 模板：

```bash
rg -n "moduleStore|useZustandState|\\.store|p\\.stores" "{targetModulePath}"
```

最后运行项目已有的低成本测试、typecheck 或 lint。没有可用命令时说明未运行原因。

## 模板规则文件建议

当某个模板的约束开始超过源码顶部注释时，在模板目录增加：

```text
rule.md
```

规则较多时使用：

```text
rules/
├── structure.md
├── state.md
└── review.md
```

规则文件只描述该模板的约定，例如状态管理、目录结构、注册方式、禁用写法和自检命令。不要把所有项目的规则塞进全局规则文件。

## 输出要求

完成后简要说明：

- 使用了哪个模板。
- 创建或审查的目标模块路径。
- 替换了哪些占位符。
- 自动补了哪些注册文件；如果没有补，说明原因。
- 做了哪些结构或规范修正。
- 执行了哪些验证命令和结果。

不要提交代码，除非用户明确要求。
