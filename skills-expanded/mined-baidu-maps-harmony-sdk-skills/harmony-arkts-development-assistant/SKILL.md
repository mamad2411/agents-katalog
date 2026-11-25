---
name: harmony-arkts-development-assistant
description: HarmonyOS ArkTS 综合开发与类型安全最佳实践助手。用于在生成或重构 ArkTS/ArkUI 代码时统一组件装饰器、生命周期、样式布局、事件处理、类型与空值安全、性能优化与错误处理等规范，帮助通过 ArkTSCheck，提升代码一致性与可维护性。
---

# HarmonyOS ArkTS 开发规范编程助手 Skill

## 触发场景

当满足以下任意条件时，应启用本 Skill 作为 ArkTS 代码生成与审查的规范依据：

- 用户正在编辑或新建 `.ets` 文件，并提到“规范”“最佳实践”“代码风格”“代码审查”等关键词。
- 对话中出现 **ArkTS / ArkUI / HarmonyOS NEXT** 相关问题，特别是组件写法、生命周期、样式布局、事件处理、状态管理、错误处理与测试实践。
- 用户要求“按照官方/行业最佳实践写 ArkTS 代码”或“帮我按规范检查/重构 ArkTS 页面/组件/模块”。

在这些场景下，代理生成或修改的 ArkTS 代码必须参考本 Skill 中的规范内容。

---

## Skill 主目标
- **统一状态管理版本**：统一工程中的状态管理，优先使用V2版本实现ViewModel。常用的状态管理装饰器包括@Local、@Param、@Event、@ObservedV2、@Trace等等。
- **统一组件装饰器与状态管理用法**：确保入口组件、页面组件、自定义组件使用正确装饰器，`@State` / `@Prop` / `@Link` / `@Provide` / `@Consume` 等按数据流语义选用。
- **规范生命周期使用**：在 `aboutToAppear` / `aboutToDisappear` / `onPageShow` / `onPageHide` 中正确初始化与清理资源，避免内存泄漏。
- **统一样式与布局风格**：使用链式调用、合理属性顺序与响应式单位（`vp` / `fp` / 百分比）构建 UI，保持 ArkUI 风格一致。
- **约束事件处理方式**：使用箭头函数与私有方法封装复杂逻辑，避免在 `build()` 中直接堆叠复杂业务代码。
- **强化类型安全**：通过接口与泛型明确组件间数据结构、回调签名，避免隐式 `any` `unknown` 与弱类型代码。
- **关注性能与资源管理**：避免不必要渲染，合理使用 `@Reusable`、`@Builder`、`LazyForEach`，并在生命周期正确释放资源。
- **规范错误处理与日志**：为异步流程补充 `try/catch` 与 `Promise.catch`，使用 `hilog` 标准化日志输出。
- **强调测试与代码自检**：引导为组件编写 `@ohos/hypium` 单元测试，并使用附带的代码审查清单进行提交前自查。

---

## Skill 使用要求与输出风格

在使用本 Skill 回答 ArkTS 相关问题或生成代码时，代理应：

1. **对照规范自动修正代码**  
   - 若发现组件缺少或误用装饰器（如 `@Entry`、`@Component`、`@State` 等），应按照规范自动补全或更正。  
   - 若生命周期中存在资源泄漏风险（如定时器未清理），应在 `aboutToDisappear()` 中补充清理逻辑。  
   - 若样式链式调用顺序混乱或混搭不同类别属性，应按“尺寸 → 布局 → 背景 → 边框 → 文本 → 对齐 → 交互”的顺序重排。  

2. **优先输出符合规范的示例代码**  
   - 在讲解组件设计、状态管理、列表渲染、事件处理等场景时，示例代码必须遵循本 Skill 约定的写法。  
   - 对用户给出的“不规范示例”，先指出与本规范不符的点，再给出“✅ 推荐写法”。  

3. **显式引用相关章节指导**  
   - 在回答中可提及“参考本 Skill 的 *组件装饰器规范* / *生命周期规范* / *样式和布局规范* / *事件处理规范* / *类型安全规范* / *性能优化规范* / *错误处理规范* / *测试规范* 章节”。  
   - 在代码审查类回答中，可根据文末“代码审查清单”逐项给出建议。  

4. **保持解释适度、以实践为导向**  
   - 回答时以“如何写出正确 ArkTS 代码”为核心，适当引用规范要点，但避免长篇理论堆砌。  
   - 对关键规范（如生命周期清理、状态装饰器选择、错误处理等）给出简要原因解释，帮助用户理解而非死记。  

---

## ⚠️ 强制要求（必须严格遵守）

在使用本 Skill 进行开发时，**必须严格遵守**以下规范：

1. **构建与编译验证规范（Auto Run）**：
   - ✅ 当涉及 **ArkTS 语法结构调整**（包括但不限于组件装饰器、生命周期函数签名、状态管理装饰器、接口/类型声明等）或 **依赖相关改动**（如 `oh-package.json5`、`module.json5`、三方 SDK 引入或移除）时，完成主要修改后应触发一次自动化“auto run”构建流程，而不是只在少数节点手动编译。
   - ✅ 推荐在工程根目录配置脚本、IDE Task 或 CI 流水线，使每次提交前自动执行：
     1. `ohpm install`
     2. `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon`
     确保 ArkTSCheck 与打包流程均能通过。
   - ✅ 在连续多轮 ArkTS 重构或大规模重命名后，应在合适的里程碑节点手动或自动重复执行上述 auto run 流程，以尽早暴露类型 / 语法 / 依赖问题。
   - ❌ **禁止**仅依赖本地 Lint 或静态分析结果，而在存在 ArkTS 语法或依赖改动时跳过 hvigor 真机 / 模拟器编译验证或约定的 auto run 流程。

2. **日志输出规范**：
   - ✅ **必须**使用 `Logger` 工具类封装原生 `console`
   - ✅ 第一个参数**必须**固定使用场景名 `"SportHealthMap"`
   - ✅ 第二个参数统一使用 `string | object`，推荐**直接传入对象**，由 `Logger` 负责 JSON 序列化
   - ✅ `Logger` 工具类会自动对非字符串参数执行 `JSON.stringify` 序列化
   - ❌ **禁止**直接使用 `console.info/error/warn/debug`
   - 示例（推荐用法）：`Logger.info('SportHealthMap', JSON.stringify({ action: 'mapReady' }))`

3. **代码注释规范**：
   - ✅ **必须**为关键方法添加注释，说明用途、参数、返回值
   - ❌ **禁止**无意义的注释

4. **模块化规范**：
   - ✅ **必须**将通用工具类、组件、同类Interface等类型定义独立为文件
   - ❌ **禁止**在页面组件内联定义通用类

5. **性能优化规范**：

   **5.1 对象缓存与复用**
   - ✅ **必须**高频 UI 更新场景必须缓存复用对象，通过成员变量持有引用而非每次重建
   - ✅ **必须**重型对象（自定义绘制组件、动画控制器、数据适配器等）采用对象池（Object Pool）模式管理，预分配并按需取用归还
   - ❌ **禁止**同一功能重复创建对象、移除对象（如在定时回调 / 数据刷新中反复 new 再 remove）
   - ❌ **禁止**在 `build()` 方法或 `@Builder` 函数内 new 任何非轻量值对象

   **5.2 渲染性能**
   - ✅ **必须**列表场景超过 20 项时使用 `LazyForEach` + `IDataSource` 实现按需加载，禁止一次性渲染全量数据
   - ✅ **必须**使用 `@Builder` 抽取重复 UI 描述片段，避免 `build()` 内大量重复代码
   - ✅ **推荐**条件渲染优先使用 `if/else` 控制组件树分支，而非通过 `.visibility(Visibility.None)` 隐藏（后者仍参与布局计算）
   - ❌ **禁止**在 `build()` 中执行耗时计算、网络请求或文件 I/O

   **5.3 状态管理精细化**
   - ✅ **必须**将高频变化的状态与低频状态拆分到不同的 `@State` / `@Observed` 属性中，避免无关属性变化引发整棵组件树重渲染
   - ✅ **推荐**使用 `@Watch` 装饰器监听特定状态变化并执行副作用，替代在 `build()` 中做差异判断
   - ✅ **推荐**跨层级数据传递优先使用 `@Provide` / `@Consume` 或 AppStorage，而非逐层 `@Prop` 透传
   - ❌ **禁止**将大型数组或深层嵌套对象整体赋值给 `@State`，应使用 `@Observed` + `@ObjectLink` 实现属性级精准刷新

   **5.4 异步与并发**
   - ✅ **必须**耗时操作（网络请求、数据库查询、文件读写、大规模计算）放入 `TaskPool` 或 `Worker` 线程执行，禁止阻塞 UI 线程
   - ✅ **必须**`TaskPool.execute()` 返回的 Promise 添加 `.catch()` 兜底，避免静默丢弃异常
   - ✅ **推荐**批量并发请求使用 `Promise.all()` / `Promise.allSettled()` 合并，减少线程调度开销
   - ❌ **禁止**在定时器回调 (`setInterval` / `setTimeout`) 中直接执行重型业务逻辑，应通过消息派发或 TaskPool 转移到后台

   **5.5 内存管理**
   - ✅ **必须**在 `aboutToDisappear()` 中清理所有定时器（`clearInterval` / `clearTimeout`）、事件订阅（`emitter.off`）、传感器监听、回调注册等
   - ✅ **必须**大图片 / Bitmap 资源使用完毕后显式调用 `release()` 或置空引用，配合 GC 及时回收
   - ✅ **推荐**使用 `WeakRef` 持有仅观察但不阻止回收的对象引用，避免闭包意外延长生命周期
   - ❌ **禁止**组件内持有对其他组件实例的强引用导致交叉引用无法回收
   - ❌ **禁止**在全局单例（AppStorage / 静态变量）中无限累积数据而不设置上限或淘汰策略

   **5.6 启动与加载优化**
   - ✅ **推荐**非首屏模块使用动态 `import()` 延迟加载，减少主包体积与冷启动耗时
   - ✅ **推荐**首屏数据预取与 UI 构建并行：在 `aboutToAppear()` 发起请求的同时展示骨架屏 / Loading 占位
   - ❌ **禁止**在 Ability `onCreate()` 中执行阻塞性同步调用（如同步读取大文件、同步网络请求）

   **5.7 包体积与构建产物**
   - ✅ **推荐**定期执行 `hvigorw analyzeBundle` 分析包体积，识别并移除未使用的资源和依赖
   - ✅ **推荐**三方 SDK 按需引入子模块，避免全量导入（如 `import { SpecificApi } from '@third/sdk'` 而非 `import * as sdk from '@third/sdk'`）
   - ❌ **禁止**在发布构建中保留 `console` / `hilog.debug` 级别日志输出，应通过构建配置或日志等级开关屏蔽

6. **类型声明**：
   - ✅ **必须**自定义的Object对象必须先通过Interface定义类型，然后引用类型定义数据，再使用
   - ❌ **禁止**使用`any` `unknown` 类型标记
   - 示例（推荐用法）：`export interface Out{ xx: string} function getBaseLocation():Out{let m = {xx:'XXX'};return m}`


> 代理在生成或审查 ArkTS 代码时应优先参考下面内容。

## 0. ArkTS 类型与空值安全规范

本节在原有“类型安全规范”基础上，补充 ArkTSCheck 相关的强制规则与空值安全约定，用于统一 ArkTS 代码的类型设计、空值处理和语法约束。

### 1. 类型安全强制规则

- **参数与返回值必须显式类型化**：禁止隐式 `any` `unknown`。所有函数、方法、回调的参数与返回值都要写明类型。  
- **接口驱动的数据结构设计**：对于组件 `@State` / `@Prop` / `@Link`、服务入参/出参、全局配置等，优先通过 `interface` / 类型别名定义结构，再在代码中引用。  
- **禁止访问未声明字段**：不允许通过字符串索引访问未在类型中声明的属性；确需“字典”结构时，使用索引签名：

```ts
interface StringNumberMap {
  [key: string]: number;
}
```

### 2. 空值安全策略

- **显式处理 `null` / `undefined`**：对类型为 `T | null | undefined` 或带 `?:` 的可选属性，访问前必须通过可选链或显式判空。  
- **推荐写法**：
  - 可选链：`user?.name`、`config?.options?.timeout ?? 3000`；  
  - 显式判空：`if (user !== null && user !== undefined) { ... }`。  
- **避免滥用非空断言 `!`**：只有在前面已通过逻辑分支、早返回、抛错等方式**完全覆盖空值分支**时，才允许使用 `!`，并建议配合注释说明原因。

### 3. 函数声明与结构约束（ArkTSCheck 语法规则）

- **禁止解构变量声明**：`ArkTS` 不支持 `const { a, b } = obj` 形式的解构变量声明（`arkts-no-destruct-decls`），必须改写为逐一赋值：

```ts
// ❌ 不允许
const { lat, lng } = coord;

// ✅ 推荐
const lat = coord.lat;
const lng = coord.lng;
```

- **业务函数避免参数解构**：推荐为参数定义接口或独立参数，而不是 `function draw({ text, location }) { ... }` 这类难以追踪类型的写法。  
- **组件内部优先使用箭头函数**：在 `build()` 中定义事件回调或内部小函数时，推荐 `const handler = (): void => { ... }`，有利于类型推断与闭包语义清晰。

### 4. ArkUI 组件属性约束补充

- **`TextInput` 不支持 `placeholder` 属性**：`TextInputAttribute` 中无 `placeholder`，不能调用 `.placeholder()` 或通过构造参数设置占位符。  
- 占位符需求推荐替代方案：
  - 使用上方标签文本提示输入含义；  
  - 使用 `Stack` 条件渲染一个灰色 `Text` 叠加在 `TextInput` 上，在输入内容为空时显示；  
  - 如当前 HarmonyOS 版本支持，可使用 `.placeholderFont()` / `.placeholderColor()` 等 API，而非自定义 `.placeholder()`。

### 5. 类型系统约束与接口设计

- **避免依赖纯结构等价赋值**：不要仅因为两个类字段“长得一样”就在它们之间互相赋值，应通过接口或基类统一约束：

```ts
interface WithNumber {
  n: number;
}

class X implements WithNumber {
  n: number = 0;
}

class Y implements WithNumber {
  n: number = 0;
}

let value: WithNumber = new X(); // ✅ 通过公共接口约束
```

- 在建模与重构时，优先：
  - 定义领域接口 / 抽象基类；  
  - 让具体实现 `implements` / `extends` 这些公共类型，而不是在不同类之间直接赋值。

### 6. 综合示例：类型安全 + 空值安全的路由跳转

在涉及路由表的场景中，必须为路由配置定义接口，并对 `find` 结果与可选 `path` 做空值处理：

```ts
interface RouteConfig {
  id: string;
  path?: string;
}

const routes: RouteConfig[] = [
  { id: 'home', path: 'pages/Home' },
  { id: 'detail', path: 'pages/Detail' }
];

function navigateToPage(pageId: string): void {
  const targetRoute: RouteConfig | undefined = routes.find(
    (route: RouteConfig) => route.id === pageId
  );

  if (targetRoute?.path) {
    router.push({ url: targetRoute.path });
    return;
  }

  if (!targetRoute || !targetRoute.path) {
    // 记录日志或给出兜底处理
    return;
  }

  router.push({ url: targetRoute.path });
}
```

在回答类似问题时，应通过上述模式同时保证：  
- 所有参数 / 返回值有显式类型；  
- 通过接口约束配置结构；  
- 对可能为空的字段和查找结果做完备校验。

---

## 1. 组件装饰器规范

### 1.1 组件必须使用装饰器
- **入口组件**必须使用 `@Entry` 装饰器
- **页面组件**必须使用 `@Component` 装饰器
- **自定义组件**必须使用 `@Component` 装饰器

```typescript
// ✅ 正确示例
@Entry
@Component
struct Index {
  // 组件实现
}

@Component
struct ChildChip {
  // 组件实现
}
```

### 1.2 状态管理装饰器
根据数据流动方向选择合适的装饰器：
- `@State`：组件内部的状态，变化会触发UI更新
- `@Prop`：从父组件传递到子组件的只读数据
- `@Link`：父子组件双向绑定的数据
- `@Provide` / `@Consume`：跨层级组件数据共享
- `@Observed` / `@ObjectLink`：对象属性级别的响应式更新
- `@StorageProp` / `@StorageLink`：持久化存储

```typescript
@Component
struct ParentComponent {
  @State count: number = 0;          // 内部状态
  @State message: string = "Hello";

  build() {
    Column() {
      ChildComponent({ count: this.count, message: this.message })
    }
  }
}

@Component
struct ChildComponent {
  @Prop count: number;               // 只读属性
  @Link message: string;             // 双向绑定

  build() {
    // ...
  }
}
```

## 2. 组件生命周期规范

### 2.1 生命周期装饰器
必须按照规范的顺序定义生命周期方法：
- `aboutToAppear()`：组件即将显示时调用
- `aboutToDisappear()`：组件即将消失时调用
- `onPageShow()`：页面显示时调用（仅Page组件）
- `onPageHide()`：页面隐藏时调用（仅Page组件）

```typescript
@Component
struct MyComponent {
  private timerId: number | undefined = undefined;

  aboutToAppear() {
    // 初始化数据
    this.timerId = setInterval(() => {
      // 定时任务
    }, 1000);
  }

  aboutToDisappear() {
    // 清理资源
    if (this.timerId) {
      clearInterval(this.timerId);
    }
  }
}
```

## 3. 样式和布局规范

### 3.1 链式调用
样式属性必须使用链式调用，按以下顺序组织：
1. 尺寸属性：`.width()`, `.height()`, `.size()`
2. 布局属性：`.margin()`, `.padding()`
3. 背景属性：`.backgroundColor()`, `.backgroundImage()`
4. 边框属性：`.borderRadius()`, `.borderWidth()`, `.borderColor()`
5. 文本属性：`.fontSize()`, `.fontColor()`, `.fontWeight()`
6. 对齐属性：`.justifyContent()`, `.alignItems()`
7. 交互属性：`.onClick()`, `.onTouch()`

```typescript
// ✅ 最佳实践
Text('Hello ArkTS')
  .fontSize(20)
  .fontColor(Color.White)
  .fontWeight(FontWeight.Bold)
  .backgroundColor('#4F8DFF')
  .padding({ left: 16, right: 16, top: 8, bottom: 8 })
  .borderRadius(8)
  .onClick(() => {
    // 点击事件
  })

// ❌ 避免：混合编码风格
Text('Hello ArkTS')
  .fontSize(20).backgroundColor('#4F8DFF')  // 不应该混合不同类型的属性
```

### 3.2 响应式单位
- 优先使用百分比：`'100%'` 而不是固定值
- 推荐使用 `vp`（虚拟像素）适配不同分辨率
- 文本使用 `fp`（字体像素）保证字体大小一致性

```typescript
// ✅ 响应式设计
Column()
  .width('100%')
  .height('100%')
  .padding(10)

Text('标题')
  .fontSize(16)
  .margin({ top: 10 })
```

## 4. 事件处理规范

### 4.1 事件回调函数
- 使用箭头函数避免this绑定的问题
- 复杂逻辑封装到私有方法中
- 避免在build方法中直接写复杂逻辑

```typescript
@Component
struct MyComponent {
  @State count: number = 0;

  private handleClick() {
    this.count++;
    // 复杂逻辑处理
  }

  build() {
    Column() {
      Button('点击')
        .onClick(() => {
          this.handleClick();  // ✅ 调用封装的方法
        })

      // ❌ 避免：直接在事件中写复杂逻辑
      Button('不推荐')
        .onClick(() => {
          this.count++;
          fetchData().then(() => {
            // 复杂异步逻辑
          });
        })
    }
  }
}
```

## 5. 类型安全规范

### 5.1 接口定义
组件之间的数据传递必须定义明确的接口：

```typescript
// ✅ 明确的接口定义
interface ChildInfo {
  id: string;
  name: string;
  avatarColor: string;
}

@Component
struct ChildChip {
  @Prop child: ChildInfo;  // 明确指定类型
  @Prop selected: boolean;
  @Prop onSelect: (id: string) => void;  // 明确的函数签名

  build() {
    // ...
  }
}
```

### 5.2 泛型使用
对于可复用的组件，使用泛型提高类型安全性：

```typescript
@Component
struct ListItem<T> {
  @Prop item: T;
  @Prop renderItem: (item: T) => void;

  build() {
    // 渲染逻辑
  }
}
```

## 6. 性能优化规范

### 6.1 对象缓存与复用
- 高频更新场景（如实时数据刷新、动画帧更新）必须缓存对象引用，仅更新属性而非销毁重建
- 使用对象池模式管理重型对象的分配与回收

```typescript
// ✅ 通用对象池模式示例
class ObjectPool<T> {
  private pool: Array<T> = [];
  private activeMap: Map<string, T> = new Map();
  private factory: (options: object) => T;
  private resetter: (item: T, options: object) => void;

  constructor(factory: (options: object) => T, resetter: (item: T, options: object) => void) {
    this.factory = factory;
    this.resetter = resetter;
  }

  /** 从池中取出或新建对象 */
  acquire(id: string, options: object): T {
    let item: T | undefined = this.pool.pop();
    if (item === undefined) {
      item = this.factory(options);
    } else {
      this.resetter(item, options);
    }
    this.activeMap.set(id, item);
    return item;
  }

  /** 归还对象到池中 */
  release(id: string): void {
    const item: T | undefined = this.activeMap.get(id);
    if (item !== undefined) {
      this.activeMap.delete(id);
      this.pool.push(item);
    }
  }

  /** 释放全部资源 */
  clear(): void {
    this.activeMap.clear();
    this.pool = [];
  }
}
```

### 6.2 渲染性能优化
- 避免在 `build()` 方法中创建新对象或数组
- 使用 `@Reusable` 装饰器标记可复用的 UI 组件
- 大列表必须使用 `LazyForEach` + `IDataSource` 实现按需加载

```typescript
// ✅ LazyForEach + IDataSource 示例
class ListDataSource implements IDataSource {
  private dataArray: Array<string> = [];
  private listeners: Array<DataChangeListener> = [];

  totalCount(): number {
    return this.dataArray.length;
  }

  getData(index: number): string {
    return this.dataArray[index];
  }

  registerDataChangeListener(listener: DataChangeListener): void {
    this.listeners.push(listener);
  }

  unregisterDataChangeListener(listener: DataChangeListener): void {
    const idx: number = this.listeners.indexOf(listener);
    if (idx >= 0) {
      this.listeners.splice(idx, 1);
    }
  }

  pushData(data: string): void {
    this.dataArray.push(data);
    this.listeners.forEach((listener: DataChangeListener) => {
      listener.onDataAdd(this.dataArray.length - 1);
    });
  }
}

@Component
struct HighPerfList {
  private dataSource: ListDataSource = new ListDataSource();

  build() {
    List() {
      LazyForEach(this.dataSource, (item: string, index: number) => {
        ListItem() {
          this.ItemBuilder(item)
        }
      }, (item: string) => item) // keyGenerator 保证 diff 精准
    }
    .cachedCount(5) // 预加载屏外 5 项，平衡内存与流畅度
  }

  @Builder
  ItemBuilder(item: string) {
    Text(item)
      .fontSize(14)
      .margin({ bottom: 4 })
  }
}
```

### 6.3 状态拆分与精准刷新
- 将高频变化状态与低频状态拆分到不同属性，避免无关渲染
- 深层嵌套对象使用 `@Observed` + `@ObjectLink` 实现属性级刷新

```typescript
// ✅ 状态拆分示例：高低频状态分离
@Observed
class RealtimeData {
  value: number = 0;
  updateTime: number = 0;
}

@Component
struct DashboardPage {
  @State realtimeData: RealtimeData = new RealtimeData(); // 高频：实时数据刷新
  @State configLoaded: boolean = false;                    // 低频：配置加载

  build() {
    Column() {
      ConfigPanel()                                        // 不受 realtimeData 变化影响
      RealtimePanel({ data: this.realtimeData })           // 仅 realtimeData 变化时刷新
    }
  }
}

@Component
struct RealtimePanel {
  @ObjectLink data: RealtimeData; // 精准订阅，不受父组件其他状态影响

  build() {
    Text(`${this.data.value} @ ${this.data.updateTime}`)
      .fontSize(12)
  }
}
```

### 6.4 异步任务与线程管理
- 耗时操作必须使用 `TaskPool` / `Worker` 执行，禁止阻塞 UI 线程

```typescript
import { taskpool } from '@kit.ArkTS';

// ✅ 使用 TaskPool 执行耗时计算
@Concurrent
function parseJsonData(raw: string): Array<DataItem> {
  // 在后台线程中解析大量 JSON 数据
  const data: RawDataSet = JSON.parse(raw) as RawDataSet;
  return data.items.map((item: RawItem) => {
    return { id: item.id, value: item.value } as DataItem;
  });
}

async function loadData(url: string): Promise<Array<DataItem>> {
  const rawData: string = await fetchRawData(url);
  const task: taskpool.Task = new taskpool.Task(parseJsonData, rawData);
  const result: Array<DataItem> = await taskpool.execute(task) as Array<DataItem>;
  return result;
}
```

### 6.5 内存与资源生命周期管理
- 在 `aboutToDisappear()` 中清理所有定时器、事件监听器、传感器、回调注册

```typescript
@Component
struct ResourceManagedComponent {
  private timerId: number | undefined = undefined;
  private eventCallbackId: number | undefined = undefined;
  private objectPool: ObjectPool<CustomItem> | undefined = undefined;

  aboutToAppear(): void {
    this.objectPool = new ObjectPool<CustomItem>(
      (opts: object) => new CustomItem(opts),
      (item: CustomItem, opts: object) => item.reset(opts)
    );
    this.timerId = setInterval(() => {
      this.refreshData();
    }, 5000);
    this.eventCallbackId = emitter.on('dataUpdate', (data: EventData) => {
      this.handleDataUpdate(data);
    });
  }

  aboutToDisappear(): void {
    // ✅ 逐一清理全部资源
    if (this.timerId !== undefined) {
      clearInterval(this.timerId);
      this.timerId = undefined;
    }
    if (this.eventCallbackId !== undefined) {
      emitter.off('dataUpdate');
      this.eventCallbackId = undefined;
    }
    if (this.objectPool !== undefined) {
      this.objectPool.clear();
    }
  }

  private refreshData(): void { /* ... */ }
  private handleDataUpdate(data: EventData): void { /* ... */ }

  build() {
    Column() {
      Text('资源已管理')
    }
  }
}
```

### 6.6 启动与加载优化
- 非首屏模块使用动态 `import()` 延迟加载
- 首屏数据预取与 UI 构建并行，展示骨架屏占位

```typescript
// ✅ 动态导入 + 骨架屏示例
@Entry
@Component
struct MainPage {
  @State dataReady: boolean = false;
  @State listData: Array<ItemInfo> = [];

  aboutToAppear(): void {
    // 数据预取与 UI 构建并行
    this.prefetchData();
  }

  private async prefetchData(): Promise<void> {
    try {
      this.listData = await fetchHomeList();
      this.dataReady = true;
    } catch (e) {
      Logger.error('SportHealthMap', JSON.stringify({ action: 'prefetch_fail', error: e }));
    }
  }

  build() {
    Column() {
      if (!this.dataReady) {
        this.SkeletonBuilder() // 骨架屏占位
      } else {
        this.ContentBuilder()
      }
    }
  }

  @Builder
  SkeletonBuilder() {
    Column() {
      ForEach([1, 2, 3, 4], () => {
        Row()
          .width('100%')
          .height(60)
          .backgroundColor('#F2F2F2')
          .borderRadius(8)
          .margin({ bottom: 12 })
      })
    }
    .padding(16)
  }

  @Builder
  ContentBuilder() {
    List() {
      LazyForEach(new HomeDataSource(this.listData), (item: ItemInfo) => {
        ListItem() {
          Text(item.title).fontSize(16)
        }
      }, (item: ItemInfo) => item.id)
    }
  }
}
```

### 6.7 性能度量与监控
- 关键路径使用 `hiTraceMeter` 打点，在 SmartPerf 中验证帧率与耗时

```typescript
import { hiTraceMeter } from '@kit.PerformanceAnalysisKit';

// ✅ 性能打点示例
function renderListItems(items: Array<ItemInfo>): void {
  hiTraceMeter.startTrace('renderListItems', 1);
  // 批量渲染列表项
  items.forEach((item: ItemInfo) => {
    applyItem(item);
  });
  hiTraceMeter.finishTrace('renderListItems', 1);
}
```

## 7. 代码组织规范

### 7.1 文件结构
```
entry/src/main/ets/
├── pages/           # 页面组件
│   ├── Index.ets
│   └── Detail.ets
├── components/      # 公共组件
│   ├── Button.ets
│   └── Card.ets
├── utils/           # 工具函数
│   ├── FormatUtils.ets
│   └── Validation.ets
├── models/          # 数据模型
│   ├── User.ets
│   └── Product.ets
└── services/        # 服务层
    ├── ApiService.ets
    └── StorageService.ets
```

### 7.2 导入规范
- 相对路径导入：`import { ... } from '../utils/FormatUtils'`
- 绝对路径导入：`import { ... } from '@kit.ArkUI'`
- 第三方库导入：`import { ... } from '@bdmap/map'`

### 7.3 命名规范
- 组件名：PascalCase，如 `UserProfile`
- 变量名：camelCase，如 `userName`
- 常量名：UPPER_SNAKE_CASE，如 `MAX_COUNT`
- 接口名：PascalCase，如 `UserInfo`
- 私有成员：camelCase，前缀可加 `_`，如 `_internalData`

## 8. 错误处理规范

### 8.1 异步错误处理
- Promise必须添加catch处理
- try-catch包裹可能抛出异常的代码

```typescript
private async fetchData() {
  try {
    const response = await http.get('/api/data');
    // 处理数据
  } catch (error) {
    promptAction.showToast({
      message: '网络请求失败',
      duration: 2000
    });
    // 记录日志
    hilog.error(DOMAIN, 'App', 'Fetch data failed: %{public}s', JSON.stringify(error));
  }
}
```

### 8.2 日志规范
```typescript
import { hilog } from '@kit.PerformanceAnalysisKit';

const DOMAIN = 0x0000;  // 定义日志域

// 不同级别的日志
hilog.debug(DOMAIN, 'Tag', 'Debug message');    // 调试信息
hilog.info(DOMAIN, 'Tag', 'Info message');      // 普通信息
hilog.warn(DOMAIN, 'Tag', 'Warning message');   // 警告信息
hilog.error(DOMAIN, 'Tag', 'Error message');    // 错误信息
```

## 9. 测试规范

### 9.1 单元测试
- 每个组件都应该有对应的单元测试
- 使用 `@ohos/hypium` 测试框架
- 测试文件和源码文件保持相同目录结构

### 9.2 测试文件命名
```
UserComponent.ets      # 源码
UserComponent.test.ets # 对应测试文件
```

## 10. 代码审查清单

每次[代码生成结完成时/提交代码时]检查：
- [ ] 组件是否使用了正确的装饰器
- [ ] 状态管理是否正确（@State/@Prop/@Link）
- [ ] 生命周期方法是否正确清理资源
- [ ] 样式是否使用链式调用且顺序正确
- [ ] 事件处理是否使用箭头函数
- [ ] 类型定义是否完整
- [ ] 错误处理是否完整
- [ ] 日志记录是否得当
- [ ] 性能考虑是否充分（对象缓存复用、LazyForEach、状态拆分、异步线程化）
- [ ] 是否存在内存泄漏风险（定时器、事件监听、传感器、回调注册是否在 aboutToDisappear 中清理）
- [ ] 启动路径是否存在阻塞性同步调用
- [ ] 大列表是否使用 LazyForEach + IDataSource + cachedCount
- [ ] 高频刷新场景是否做了对象池 / 缓存复用

---

**适用版本**：HarmonyOS 4.0+  
**ArkTS版本**：API 12+

