---
name: react-ddt
description: 审查并修正 React hook、React 组件和 TSX 文件里的职责放置错误；当用户要求拆分纯函数、静态常量、按项目规范放置类型，或 review React 组件 / hook 结构时使用。
---

# react-ddt

react-ddt 是 React dont-do-that packaging。

这个 skill 专门约束 React 组件和 hook 里最容易反复出错的一类问题：把与 React state 无关的纯函数、静态常量和类型定义耦合在 `.tsx` 或 hook 主文件里，导致组件文件越来越重，review 时很难快速判断哪些是渲染逻辑，哪些只是普通计算逻辑。

它和 `ddt` 不是互相替代关系。`ddt` 负责反对无收益的过度封装，`react-ddt` 负责把 React 文件里的非 React 职责放到项目约定位置。执行时要同时考虑两边规则：该抽离的纯函数要抽离，不该为了形式新增一堆薄包装。

## 规范读取要求

如果这个 skill 要审查或修改项目代码，必须先读取仓库内的 `CLAUDE.md` 和存在的 `AGENTS.md`，再按任务需要读取相关模块文档和源码目录旁说明。

如果当前改动属于 React 页面、组件、hook 或前端状态链路，还要检查是否命中项目里的页面拆分、类型放置、文档维护、i18n 和验证要求。

## 什么时候触发

当用户表达下面这些意思时，优先使用这个 skill：

- 要求 review React hook、React 组件、`.tsx` 文件结构
- 指出纯函数不应该放在组件或 hook 主文件里
- 要求把常量放到 `enum.ts`
- 要求把类型移出组件或 hook 主文件，并按项目规范放置
- 要求把类型放到 `types.ts`，或质疑类型不应一刀切放 `types.ts`
- 要求把刚才改动的 TS / TSX 文件按目录职责复查
- 组件文件里同时出现 UI、状态逻辑、纯计算、静态配置和类型定义
- hook 主文件里出现与 hook state 无关的判断、构造、解析、比较函数

## 核心规则

React 组件文件只保留渲染、props 解构、React hook 调用、事件 handler、与当前组件 state / ref / effect 强绑定的逻辑，以及必要的 JSX 分支。

React hook 主文件只保留 hook 自身的 state、ref、memo、effect、callback 编排，以及必须读取 hook 内状态的闭包逻辑。

如果组件或 hook 里存在与 React state、ref、effect 生命周期无关的纯函数，必须抽到当前目录下的 `util.ts`。没有 `util.ts` 就新建。这个规则适用于解析 ID、构造摘要、过滤列表、比较对象、格式化展示文本、转换 DTO、计算勾选态、生成 className 配置等纯逻辑。

如果存在静态常量，必须抽到当前目录下的 `enum.ts`。没有 `enum.ts` 就新建。这个规则适用于 UI 尺寸、间距、阈值、ID 前缀、正则、固定 key、状态码、静态 Set、静态 Map、固定 tool name 等不会随组件运行态变化的值。

如果存在类型定义，先判断它是否应该从 React 主文件中移出，再按项目类型规范和现有目录模式决定落点，不能一刀切新建或搬到当前目录 `types.ts`。这个规则适用于组件 props、hook 参数、hook 返回值、局部业务类型、选择器状态、内部映射结构等。只有项目没有明确类型放置要求，且同目录已有或适合承载局部类型时，才把同目录 `types.ts` 作为默认落点。

`enum.ts` 在本项目里可以承载语义化 `const`、`Set`、正则和真正的 `enum`。不要为了文件名叫 enum 就把所有值强行改成 TypeScript `enum`。业务状态码、任务码、类型码这类语义明确的数字常量，才优先使用真正的 `enum` 或项目既有枚举模式。

## 前置判断：先判断该不该抽

`react-ddt` 的顺序是先判断拆分有没有收益，再判断放到 `util.ts`、`enum.ts` 还是类型文件。不要只因为某段逻辑是纯函数、静态常量或类型定义，就机械抽出去。

```text
看到 React 文件里的函数 / 常量 / 类型 / 兜底分支
        │
        ▼
它是否属于 React 主流程？
        ├─ 是：保留在组件或 hook 主文件
        │
        └─ 否
             │
             ▼
它是否有稳定复用、复杂逻辑、外部协议或测试边界？
             ├─ 否：内联、合并类型、保留局部字面量或删除重复兜底
             │
             └─ 是
                  │
                  ▼
       按职责落点：纯逻辑 -> util.ts；固定配置 -> enum.ts；类型 -> 项目类型规范
```

小函数只有一个调用方、2 到 5 行、名字只是 `parse` / `build` / `normalize` / `to` 这类实现描述、调用者仍要点进去看细节、没有独立测试价值时，默认内联。只有被稳定复用、能明显压低主流程复杂度、表达外部协议或复杂业务边界时，才保留函数。

薄类型只服务一个父类型、只是改名 / 摘字段 / 一层别名、拆完增加跳转时，默认合并。只有类型本身是 API 返回体、事件载荷、消息体、稳定嵌套结构，或被多个模块独立消费时，才拆出来。

兜底逻辑只在输入来自用户、网络、浏览器 API、外部 SDK、历史脏数据等不稳定边界时保留。状态已经由 React 生命周期、事件顺序、状态机或类型定义保证时，不要再加“更稳”的重复兜底。

## 判断纯函数是否应该抽离

满足这些条件时，只能说明它是抽离候选；是否真的抽离，还要先走前置判断：

- 不调用 React hook
- 不读取组件或 hook 内部 state、ref、context、dispatch
- 不调用 setState
- 不依赖 DOM 实例、事件对象或组件生命周期
- 输入由参数完整提供
- 输出只由输入决定，或只做确定性的解析、构造、过滤、比较、格式化

如果函数虽然写在组件里，但只是因为要读 `props` 或 `state`，且可以通过参数完整传入，就应该抽离，让组件只负责把参数传进去。

这个判断还有一个前提：抽离后要降低阅读成本。抽离出来的方法必须包含值得命名的复杂逻辑、复用价值或明确业务边界。只被调用一次、函数体只是简单字段映射、`typeof` 判断、一次性 type guard、包装已有工具函数、类型转换或空值兜底的薄 helper，不应该为了满足“纯函数放 util”而新增函数；直接把表达式写在调用处，必要时用局部变量承接。

如果函数必须直接操作 `setState`、读取 ref、处理事件对象、关闭弹窗、发起当前组件的副作用，通常保留在组件或 hook 主文件里。它属于 React 交互逻辑，不要为了形式抽成 util。

## 判断常量是否应该抽离

满足这些条件时，默认抽到同目录 `enum.ts`：

- 文件顶层定义的 UI 宽高、间距、最大数量、延迟时间、阈值
- 字符串 ID 前缀、storage key、metadata key、tool name、agent id
- 正则表达式、静态白名单、静态状态集合
- 多处分支复用的固定 label、mode、type、status

只在 JSX 里出现一次且读起来就是样式本身的 Tailwind className，不需要为了常量化抽出去。常量抽离是为了消除散落配置，不是为了把 JSX 样式变成另一层间接引用。

## 判断类型应该放哪里

先读取项目规范、同目录既有文件和上层模块约定，再决定类型落点。类型剥离的目标是让 React 主文件更聚焦，不是强制制造 `types.ts`。

如果项目规定组件 props、hook 参数或 hook 返回值放在组件目录 `types.ts`，就复用现有 `types.ts`；没有时再判断是否需要新建。若项目规定放在模块级 `types.ts`、`src/types/**`、feature 级类型文件、接口层类型文件，必须按项目规范走。

如果项目惯例允许很小的局部 props 类型贴在组件文件内，且该类型没有复用价值、不会压重主流程，可以保留在组件文件内。不要为了“类型与逻辑剥离”把所有局部类型机械搬走。

API 请求参数、响应 DTO 和数据库结构不要放 React 组件目录的 `types.ts`，要继续遵守项目 API 类型规范。

跨模块稳定复用的类型不要放局部 `types.ts`，要进入项目既有公共类型位置。不要为了当前组件方便，把全局类型偷放到局部目录。

## 执行步骤

审查当前改动时，先列出所有被改到的 React hook、React 组件和 `.tsx` 文件，再按文件逐个检查。

对每个文件先找顶层 `const`、`function`、`type`、`interface`。先判断它们是否属于 React 主流程，再判断拆分是否有真实收益。确认值得拆分后，纯函数移到 `util.ts`，静态常量移到 `enum.ts`，类型按项目类型规范移动；没有明确规范时，才考虑同目录 `types.ts`。

移动后要更新 import。`import` 和 `import type` 不能从同一路径拆成重复导入，必须合并。类型导入使用 `import type`。

移动后要检查循环引用。`util.ts` 可以 import 类型文件和 `enum.ts`，组件可以 import `util.ts`、`enum.ts` 和项目规定的类型文件。不要让类型文件反向 import 组件，也不要让 `enum.ts` import React 组件。

移动后要检查注释。所有保留的方法都必须有简短方法级 JSDoc；如果 JSDoc 只能复述函数名或表面行为，优先判断该方法是否过度封装并内联。复杂纯逻辑里的关键业务判断保留行内注释，不要删掉有价值的中文说明。

最后运行最小必要验证。默认至少对受影响文件跑 ESLint，再按任务影响补 `npm run check-types`、`npm run verify:i18n` 或页面手动验证。

## 和 ddt 的边界

`react-ddt` 要把纯函数、常量，以及应该剥离的类型移出 React 主文件，但不鼓励新增没有收益的中间层。

如果一段逻辑本来就是组件事件 handler 里的两三行 state 更新，不要抽到 util。

如果一个纯函数只被调用一次，且函数体只是简单字段映射、`typeof` 判断、一次性 type guard、单行包装已有工具函数、类型转换或空值兜底，优先内联到调用处；不要抽成 util 函数。抽离是为了复用或隔离复杂判断，不是给简单表达式取一个更长的名字。

如果一个类型只是某个 props 的一行字段别名，不要为了拆分再造一层薄类型，直接写进 props 类型里。

如果一个常量只用于解释复杂业务状态或跨多个文件复用，才给它更强的语义名称。不要把所有单次出现的字面量都搬到 `enum.ts`。

拿不准时按这句话判断：React 文件里只留下 React 相关的阅读路径，普通计算逻辑去 util，固定配置去 enum，类型按项目规范放置；但单次使用的薄包装逻辑和很小的局部类型优先留在最直接的位置。

## 反模式清单

下面这些默认需要修：

- `ExamplePanel.tsx` 顶层同时定义面板尺寸常量和 `buildSelectedSummary()`
- `ExampleList.tsx` 顶层定义 `buildInitialRange()`；它只根据入参构造默认范围，不读取组件 state、ref 或生命周期，应该放同级 `util.ts`
- `useExampleSelection.ts` 里定义不读取 hook state 的 `isSameSelection()`
- `util.ts` 里新增只被调用一次的 `normalizeSignInTemplateCourseId()`；函数体只是 `normalizePositiveFiniteNumber(courseId) ?? null`，应该内联到调用处
- `util.ts` 里新增 `buildUserInfo()`，函数体只是把几个字段按 `typeof` 映射成对象，应该耦合在生成上下文的函数里
- `util.ts` 里新增 `isAppJwtClaims()`，函数体只是一次性对象 / 数组判断，应该内联到使用它的解析函数里
- 组件文件里塞入很长的 props、映射结构或复用类型，而项目规范要求这类类型放到独立类型文件
- hook 主文件里定义复杂参数 interface，而项目已有 hook 类型统一放置位置
- TSX 里散落 `example-`、`item-` 这类 ID 前缀字符串
- TSX 里散落用于浮层定位的宽度、高度、gap、padding 数字
- util 里重复写和 enum 里同语义的固定字符串或数字
- 为单次出现且上下文自解释的 JSX 字符串、样式值、简单布尔判断新增 `enum.ts` 或 `util.ts`

## 示例

错误写法：

```tsx
const PANEL_WIDTH = 280;

interface UseExampleSelectionParams {
  selectedIds: string[];
  allIds: string[];
}

function isAllSelected(selectedIds: string[], allIds: string[]) {
  return selectedIds.length === allIds.length;
}

export function useExampleSelection(params: UseExampleSelectionParams) {
  const allSelected = useMemo(() => isAllSelected(params.selectedIds, params.allIds), [params.selectedIds, params.allIds]);

  return { allSelected };
}
```

更合适的放置方式：

这个判断只有一个调用方，且只是长度比较，内联后阅读路径更短。下面示例假设项目约定把当前 hook 的局部类型放在同目录 `types.ts`。真实项目要按其类型规范替换类型落点。

```ts
// enum.ts
export const optionPanelWidth = 280;
```

```ts
// types.ts
export interface UseExampleSelectionParams {
  selectedIds: string[];
  allIds: string[];
}
```

```ts
// useExampleSelection.ts
import type { UseExampleSelectionParams } from "./types";

/** 管理示例选择状态。 */
export function useExampleSelection(params: UseExampleSelectionParams) {
  const allSelected = useMemo(() => params.selectedIds.length === params.allIds.length, [params.selectedIds, params.allIds]);

  return { allSelected };
}
```

另一个错误写法：

```tsx
// ExampleList.tsx
function buildInitialRange(value?: string): { start: string; end: string } | null {
  const trimmedValue = value?.trim();

  if (!trimmedValue) return null;

  return {
    start: `${trimmedValue}-start`,
    end: `${trimmedValue}-end`,
  };
}

export function ExampleList(props: ExampleListProps) {
  const [range] = useState(() => buildInitialRange(props.initialValue));

  return <RangeView value={range} />;
}
```

更合适的放置方式：

```ts
// util.ts
/** 根据外部传入值构造初始范围；空值不生成范围。 */
export function buildInitialRange(value?: string): { start: string; end: string } | null {
  const trimmedValue = value?.trim();

  if (!trimmedValue) return null;

  return {
    start: `${trimmedValue}-start`,
    end: `${trimmedValue}-end`,
  };
}
```

```tsx
// ExampleList.tsx
import { buildInitialRange } from "./util";

export function ExampleList(props: ExampleListProps) {
  const [range] = useState(() => buildInitialRange(props.initialValue));

  return <RangeView value={range} />;
}
```

过度抽离的错误写法：

```ts
// util.ts
export function normalizeSignInTemplateCourseId(courseId: string | number) {
  return normalizePositiveFiniteNumber(courseId) ?? null;
}
```

```tsx
// SignInTemplate.tsx
const courseId = normalizeSignInTemplateCourseId(params.courseId);
```

更合适的写法：

```tsx
// SignInTemplate.tsx
const courseId = normalizePositiveFiniteNumber(params.courseId) ?? null;
```

这个 helper 只被调用一次，函数体也只是给已有 `normalizePositiveFiniteNumber` 补 `?? null`。抽出去没有复用收益，反而让读者多跳一次文件。

## 输出要求

如果用户要求直接修，就完成文件移动和 import 更新后再回复结果。

如果用户要求 review，就按文件指出哪些纯函数、常量和类型放错了位置，并给出最小修改建议。不要泛泛评价组件复杂度。

回复里要说明验证结果。如果没跑浏览器手动验证，要明确说没有跑。不要把 ESLint warning 说成错误。
